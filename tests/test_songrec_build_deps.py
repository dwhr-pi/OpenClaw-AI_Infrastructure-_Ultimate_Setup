"""Offline SongRec prerequisites: never invokes APT, sudo or a compiler."""
from contextlib import redirect_stdout
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts/tools/helpers'))
import gap_native_build as native
import gap_tools as tools
import native_build_deps as deps


class SongRecDependencies(unittest.TestCase):
    def setUp(self):
        self.spec = native.songrec_dependency_spec()
        for mocked in (patch.object(deps, 'ubuntu_release', return_value=True),
                       patch.object(deps.shutil, 'which', side_effect=lambda name: None if name in ('cargo', 'rustc') else 'fixture'),
                       patch.object(deps.sys, 'stdin', Mock(isatty=Mock(return_value=False)))):
            mocked.start()
            self.addCleanup(mocked.stop)

    def test_whitelist_contains_only_compilers_and_headers(self):
        self.assertEqual(tuple(self.spec['recipe']['apt_build_deps']), deps.SONGREC_PACKAGES)
        self.assertIn('cargo', deps.SONGREC_PACKAGES)
        self.assertIn('rustc', deps.SONGREC_PACKAGES)
        self.assertIn('libasound2-dev', deps.SONGREC_PACKAGES)
        self.assertNotIn('songrec', deps.SONGREC_PACKAGES)
        self.assertNotIn('docker.io', deps.SONGREC_PACKAGES)

    def test_no_consent_never_runs_apt(self):
        with patch.object(deps, 'installed', return_value=False), patch.object(deps.common, 'run') as run, \
                redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, 'Zustimmung'):
                deps.prepare(self.spec)
            run.assert_not_called()

    def test_interactive_no_and_eof_never_run_apt(self):
        for answer in ('n', EOFError()):
            with self.subTest(answer=answer), patch.object(deps.sys.stdin, 'isatty', return_value=True), \
                    patch('builtins.input', side_effect=answer if isinstance(answer, Exception) else None,
                          return_value=answer), patch.object(deps, 'installed', return_value=False), \
                    patch.object(deps.common, 'run') as run, redirect_stdout(io.StringIO()):
                with self.assertRaises(ValueError):
                    deps.prepare(self.spec)
                run.assert_not_called()

    def test_explicit_and_interactive_approval_install_cargo_only_when_missing(self):
        for approved in (True, False):
            state = {'ready': False}

            def which(name):
                return None if name == 'cargo' and not state['ready'] else 'fixture'

            def run(args, cwd, env):
                self.assertNotIn('OPENAI_API_KEY', env)
                if 'install' in args:
                    self.assertEqual(args[-1], 'cargo')
                    self.assertNotIn('rustc', args)
                    self.assertNotIn('songrec', args)
                    self.assertIn('--no-remove', args)
                    self.assertIn('--no-install-recommends', args)
                    state['ready'] = True

            with self.subTest(approved=approved), patch.object(deps.shutil, 'which', side_effect=which), \
                    patch.object(deps, 'installed', side_effect=lambda name: name != 'cargo' or state['ready']), \
                    patch.object(deps.common, 'run', side_effect=run) as calls, \
                    patch.object(deps.os, 'geteuid', return_value=1000, create=True), \
                    patch.object(deps.sys.stdin, 'isatty', return_value=True), patch('builtins.input', return_value='j'), \
                    patch.dict(os.environ, {'OPENAI_API_KEY': 'fixture-only'}), redirect_stdout(io.StringIO()):
                deps.prepare(self.spec, approved=approved)
                self.assertEqual(calls.call_count, 2)
                self.assertEqual(calls.call_args.args[0][:2], ['fixture', '--'])

    def test_existing_private_rust_is_not_replaced_by_apt(self):
        with patch.object(deps.shutil, 'which', return_value='/fixture/private/tool'), \
                patch.object(deps, 'installed', return_value=True) as installed, \
                patch.object(deps.common, 'run') as run, redirect_stdout(io.StringIO()):
            deps.prepare(self.spec, approved=True)
            self.assertNotIn('cargo', [call.args[0] for call in installed.call_args_list])
            self.assertNotIn('rustc', [call.args[0] for call in installed.call_args_list])
            run.assert_not_called()

    def test_installed_packages_with_broken_path_fail_without_apt(self):
        with patch.object(deps, 'installed', return_value=True), patch.object(deps.common, 'run') as run, \
                redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, 'PATH'):
                deps.prepare(self.spec, approved=True)
            run.assert_not_called()

    def test_foreign_package_list_is_rejected(self):
        with patch.object(deps.common, 'run') as run:
            with self.assertRaisesRegex(ValueError, 'Nicht freigegebene'):
                deps.prepare({'id': 'songrec', 'recipe': {'apt_build_deps': ['docker.io']}}, approved=True)
            run.assert_not_called()

    def test_non_ubuntu_explicit_install_is_refused(self):
        with patch.object(deps, 'ubuntu_release', return_value=False), patch.object(deps.common, 'run') as run:
            with self.assertRaisesRegex(ValueError, 'Keine Systemaenderung'):
                deps.prepare(self.spec, approved=True)
            run.assert_not_called()

    def test_apt_failure_never_becomes_success(self):
        with patch.object(deps, 'installed', return_value=False), \
                patch.object(deps.os, 'geteuid', return_value=1000, create=True), \
                patch.object(deps.common, 'run', side_effect=subprocess.CalledProcessError(100, 'fixture')), \
                redirect_stdout(io.StringIO()):
            with self.assertRaises(subprocess.CalledProcessError):
                deps.prepare(self.spec, approved=True)

    def test_plan_status_and_doctor_never_prepare_packages(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {'OPENCLAW_USER_DATA_DIR': str(Path(directory).resolve())}), \
                patch.object(deps, 'prepare') as prepare, patch.object(deps, 'installed') as query, \
                redirect_stdout(io.StringIO()):
            self.assertEqual(tools.main(['songrec', 'plan', '--install-build-deps']), 0)
            self.assertEqual(tools.main(['songrec', 'install', '--dry-run', '--install-build-deps']), 0)
            self.assertEqual(tools.main(['songrec', 'status']), 0)
            self.assertEqual(tools.main(['songrec', 'doctor']), 1)
            prepare.assert_not_called()
            query.assert_not_called()
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_storage_failure_precedes_package_phase_and_fetch(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            spec = native.specification('songrec', tools.SPECS['songrec'])
            with patch.object(tools, 'reserve', side_effect=ValueError('Speicherplatzmangel')), \
                    patch.object(deps, 'prepare') as prepare, patch.object(tools, 'git') as git:
                with self.assertRaisesRegex(ValueError, 'Speicherplatzmangel'):
                    tools.install(base / 'runtime', base / 'ready.json', base, spec, install_build_deps=True)
                prepare.assert_not_called()
                git.assert_not_called()
                self.assertFalse((base / 'runtime').exists())

    def test_preflight_passes_explicit_approval_to_package_phase(self):
        with patch.object(native.platform, 'system', return_value='Linux'), \
                patch.object(native.os, 'geteuid', return_value=1000, create=True), \
                patch.object(deps, 'prepare') as prepare, patch.object(native.common, 'executable', return_value='fixture'), \
                patch.object(native, 'probe'):
            native.preflight('songrec', Path('.'), approved=True)
        prepare.assert_called_once_with(self.spec, approved=True)


if __name__ == '__main__':
    unittest.main()
