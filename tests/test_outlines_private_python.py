"""Offline private interpreter fixtures; never downloads or executes Python/uv."""
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts/tools/helpers'))
import outlines_python as runtime
import gap_native_build as native
import native_build_deps as deps


class PrivatePython(unittest.TestCase):
    def test_refusal_does_not_download_or_create_files(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(runtime.sys, 'stdin', Mock(isatty=Mock(return_value=False))), \
                patch.object(runtime.native_uv, 'select') as uv, \
                patch.object(runtime.common, 'run') as run, redirect_stdout(io.StringIO()):
            base = Path(directory).resolve()
            with self.assertRaisesRegex(ValueError, 'nicht freigegeben'):
                runtime.select(base)
            self.assertEqual(list(base.iterdir()), [])
            uv.assert_not_called()
            run.assert_not_called()

    def test_private_install_is_reusable_and_detects_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            slot = base / 'toolchain/outlines-python313'
            python = slot / 'managed/cpython/bin/python3.13'

            def command(args, cwd, env):
                self.assertNotIn('OPENAI_API_KEY', env)
                if 'install' in args:
                    self.assertIn('--no-bin', args)
                    self.assertEqual(env['UV_PYTHON_INSTALL_DIR'], str(slot / 'managed'))
                    python.parent.mkdir(parents=True)
                    python.write_text('fixture-never-executed')
                    return ''
                if 'find' in args:
                    return str(python)
                self.assertIn('assert sys.version_info[:2] == (3,13)', args[-1])
                return '3.13 fixture'

            with patch.object(runtime.common, 'reserve') as reserve, \
                    patch.object(runtime.native_uv, 'select', return_value='/fixture/uv') as uv, \
                    patch.object(runtime.common, 'run', side_effect=command), \
                    patch.dict(os.environ, {'OPENAI_API_KEY': 'fixture-secret'}), redirect_stdout(io.StringIO()):
                self.assertEqual(runtime.select(base, approved=True), str(python))
                self.assertEqual(runtime.select(base), str(python))
                uv.assert_called_once()
                reserve.assert_called_once_with(base, {'reserve_mb': 5120})
                python.write_text('changed')
                with self.assertRaisesRegex(ValueError, 'veraendert'):
                    runtime.select(base, approved=True)

    def test_failed_download_removes_only_new_slot(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            keep = base / 'preserve.txt'
            keep.write_text('unchanged')
            with patch.object(runtime.common, 'reserve'), \
                    patch.object(runtime.native_uv, 'select', return_value='/fixture/uv'), \
                    patch.object(runtime.common, 'run', side_effect=ValueError('download failed')), redirect_stdout(io.StringIO()):
                with self.assertRaisesRegex(ValueError, 'download failed'):
                    runtime.select(base, approved=True)
            self.assertFalse((base / 'toolchain/outlines-python313').exists())
            self.assertEqual(keep.read_text(), 'unchanged')

    def test_ubuntu26_preflight_uses_private_python_not_ubuntu24_packages(self):
        with patch.object(native.platform, 'system', return_value='Linux'), \
                patch.object(native.os, 'geteuid', return_value=1000, create=True), \
                patch.dict(os.environ, {}, clear=True), \
                patch.object(native, 'select_outlines_python', side_effect=ValueError('incompatible')), \
                patch.object(deps, 'ubuntu_release', return_value=False), \
                patch.object(deps, 'prepare') as prepare, \
                patch.object(runtime, 'select', return_value='/private/python3.13') as select, \
                patch.object(runtime.native_uv, 'select'):
            self.assertEqual(native.preflight('outlines', Path('.'), approved=True), '/private/python3.13')
            prepare.assert_not_called()
            select.assert_called_once_with(Path('.'), approved=True)

    def test_songrec_and_espeak_allow_ubuntu26_package_phase(self):
        for key, packages in (('songrec', deps.SONGREC_PACKAGES), ('espeak_ng', deps.ESPEAK_PACKAGES)):
            with patch.object(deps, 'os_release', return_value={'ID': 'ubuntu', 'VERSION_ID': '26.04'}), \
                    patch.object(deps.shutil, 'which', return_value='/fixture/tool'), \
                    patch.object(deps, 'installed', return_value=True), patch.object(deps.common, 'run') as run, \
                    redirect_stdout(io.StringIO()):
                deps.prepare({'id': key, 'recipe': {'apt_build_deps': list(packages)}}, approved=True)
                run.assert_not_called()

    def test_other_debian_bases_require_successful_simulation(self):
        for release in ({'ID': 'ubuntu', 'VERSION_ID': '26.04'},
                        {'ID': 'debian', 'VERSION_ID': '13'},
                        {'ID': 'dietpi', 'ID_LIKE': 'debian', 'VERSION_ID': '13'}):
            for simulation_ok in (True, False):
                calls = []
                state = {'installed': False}

                def run(args, cwd, env):
                    calls.append(args)
                    if '--simulate' in args and not simulation_ok:
                        raise subprocess.CalledProcessError(100, args)
                    if 'install' in args and '--simulate' not in args:
                        self.assertIn('--no-remove', args)
                        state['installed'] = True

                with self.subTest(release=release, simulation_ok=simulation_ok), \
                        patch.object(deps, 'os_release', return_value=release), \
                        patch.object(deps.shutil, 'which', return_value='/fixture/tool'), \
                        patch.object(deps, 'installed', side_effect=lambda p: state['installed']), \
                        patch.object(deps.os, 'geteuid', return_value=1000, create=True), \
                        patch.object(deps.common, 'run', side_effect=run), redirect_stdout(io.StringIO()):
                    spec = {'id': 'espeak_ng', 'recipe': {'apt_build_deps': list(deps.ESPEAK_PACKAGES)}}
                    if simulation_ok:
                        deps.prepare(spec, approved=True)
                        self.assertEqual(len(calls), 3)
                    else:
                        with self.assertRaises(subprocess.CalledProcessError):
                            deps.prepare(spec, approved=True)
                        self.assertEqual(len(calls), 2)
                        self.assertFalse(state['installed'])
                    self.assertIn('--simulate', calls[1])


if __name__ == '__main__':
    unittest.main()
