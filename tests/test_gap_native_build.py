"""Offline native-recipe fixtures; no compiler, upstream code or model executed."""
from contextlib import redirect_stdout
import io
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/tools/helpers'))
sys.path.insert(0, str(ROOT / 'scripts/quality'))
import gap_tools as common
import gap_native_build as native
import source_install_readiness as readiness


class NativeRecipeTests(unittest.TestCase):
    def test_source_specs_are_not_mutated(self):
        for key in native.TOOLS:
            original = json.dumps(common.SPECS[key], sort_keys=True)
            spec = native.specification(key, common.SPECS[key])
            self.assertEqual(spec['mode'], 'native-build')
            self.assertFalse(spec['source_status_only'])
            self.assertEqual(json.dumps(common.SPECS[key], sort_keys=True), original)
            self.assertRegex(spec['pin'], r'^[0-9a-f]{40}$')
            for digest in spec['contracts'].values():
                self.assertRegex(digest, r'^[0-9a-f]{64}$')

    def test_songrec_uses_locked_ubuntu_compatible_cli_pin(self):
        spec = native.specification('songrec', common.SPECS['songrec'])
        self.assertEqual(spec['pin'], '15da6b224297d7bf8a9c91b9f70af3d499a9636d')
        self.assertIn('Cargo.lock', spec['contracts'])

    def test_plan_and_status_do_not_execute_or_write(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            with patch.dict(os.environ, {'OPENCLAW_USER_DATA_DIR': str(root)}), \
                    patch.object(common, 'git') as git, patch.object(common, 'run') as run, \
                    patch.object(native, 'probe') as probe, redirect_stdout(io.StringIO()):
                for key in native.TOOLS:
                    self.assertEqual(common.main([key, 'plan']), 0)
                    self.assertEqual(common.main([key, 'status']), 0)
                git.assert_not_called()
                run.assert_not_called()
                probe.assert_not_called()
            self.assertEqual(list(root.iterdir()), [])

    def test_legacy_source_plan_is_explicit(self):
        with redirect_stdout(io.StringIO()) as out:
            self.assertEqual(common.main(['songrec', 'plan', '--source-only']), 0)
        self.assertIn(common.SPECS['songrec']['pin'], out.getvalue())
        self.assertIn('"mode": "source"', out.getvalue())

    def test_smoke_rejects_model_and_source_only_requests(self):
        with redirect_stdout(io.StringIO()), patch('sys.stderr', io.StringIO()):
            for args in (['minimax_m3', 'doctor', '--smoke'],
                         ['musetalk', 'doctor', '--smoke'],
                         ['outlines', 'doctor', '--source-only', '--smoke']):
                with self.assertRaises(SystemExit):
                    common.main(args)

    def test_probe_has_timeout_and_no_shell(self):
        with patch.object(native.subprocess, 'run') as run:
            run.return_value.stdout = 'ok'
            self.assertEqual(native.probe(['example', '--version'], Path('.'), {}), 'ok')
            self.assertEqual(run.call_args.kwargs['timeout'], 30)
            self.assertNotIn('shell', run.call_args.kwargs)

    def test_native_build_output_uses_bounded_streaming(self):
        with patch('native_build_process.run', return_value='ok') as run:
            self.assertEqual(common.run(['cmake', '--build', 'build'], Path('.'),
                                        {'NATIVE_BUILD_STREAM': 'gap-native'}), 'ok')
        self.assertEqual(run.call_args.kwargs['timeout'], 7200)

    def test_foreign_platform_fails_before_dependency_lookup(self):
        with patch.object(native.platform, 'system', return_value='Windows'), \
                patch.object(common, 'executable') as executable:
            with self.assertRaises(ValueError):
                native.preflight('espeak_ng', Path('.'))
            executable.assert_not_called()

    def test_root_build_is_rejected_before_download(self):
        with patch.object(native.platform, 'system', return_value='Linux'), \
                patch.object(native.os, 'geteuid', return_value=0, create=True), \
                patch.object(common, 'executable') as executable:
            with self.assertRaisesRegex(ValueError, 'normaler Benutzer'):
                native.preflight('outlines', Path('.'), approved=True)
            executable.assert_not_called()

    def test_prerequisite_failure_never_fetches(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            spec = native.specification('espeak_ng', common.SPECS['espeak_ng'])
            with patch.object(common, 'reserve'), patch.object(native, 'preflight', side_effect=ValueError('missing')), \
                    patch.object(common, 'git') as git:
                with self.assertRaisesRegex(ValueError, 'missing'):
                    common.install(base / 'runtime', base / 'ready.json', base, spec)
                git.assert_not_called()
                self.assertFalse((base / 'runtime').exists())

    def test_native_install_proof_and_failure_rollback(self):
        for fail in (False, True):
            with self.subTest(fail=fail), tempfile.TemporaryDirectory() as temporary:
                base = Path(temporary).resolve()
                runtime, marker = base / 'runtime', base / 'ready.json'
                (base / 'keep.log').write_text('preserve')
                spec = native.specification('espeak_ng', common.SPECS['espeak_ng'])
                spec['contracts'] = {'README.md': hashlib.sha256(b'fixture').hexdigest()}

                def fake_git(directory, *args):
                    if args[0] == 'init':
                        (directory / '.git').mkdir()
                        (directory / '.git/HEAD').write_text('fixture')
                        (directory / 'README.md').write_bytes(b'fixture')
                    if args[:2] == ('rev-parse', 'HEAD'):
                        return spec['pin']
                    if args[:3] == ('remote', 'get-url', 'origin'):
                        return 'https://github.com/' + spec['repo'] + '.git'
                    return ''

                def build(directory, env, selected):
                    (directory / 'artifact').write_text('fixture binary, not executable')
                    if fail:
                        raise ValueError('fixture build failed')
                    return ['artifact']

                with patch.object(common, 'reserve'), patch.object(common, 'git', side_effect=fake_git), \
                        patch.object(native, 'preflight'), patch.object(native, 'build', side_effect=build), \
                        redirect_stdout(io.StringIO()):
                    if fail:
                        with self.assertRaisesRegex(ValueError, 'fixture build failed'):
                            common.install(runtime, marker, base, spec)
                        self.assertFalse(runtime.exists())
                        self.assertFalse(marker.exists())
                    else:
                        common.install(runtime, marker, base, spec)
                        record = common.validate(runtime, marker, spec, full=True)
                        self.assertTrue(record['installed'])
                        self.assertTrue(record['local_smoke_passed'])
                        self.assertFalse(record['runtime_tested'])
                        (runtime / 'artifact').write_text('tampered')
                        with self.assertRaisesRegex(ValueError, 'veraendert'):
                            common.validate(runtime, marker, spec, full=True)
                    self.assertEqual((base / 'keep.log').read_text(), 'preserve')

    def test_bad_contract_never_builds(self):
        with tempfile.TemporaryDirectory() as temporary:
            with patch.object(common, 'run') as run:
                spec = native.specification('espeak_ng', common.SPECS['espeak_ng'])
                with self.assertRaises(ValueError):
                    native.build(Path(temporary).resolve(), {}, spec)
                run.assert_not_called()

    def test_espeak_commands_are_private_and_silent(self):
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary).resolve()
            spec = native.specification('espeak_ng', common.SPECS['espeak_ng'])
            with patch.object(common, 'source_contracts'), patch.object(common, 'run') as run, \
                    patch.object(native, 'probe') as probe:
                entries = native.build(runtime, {}, spec)
            args = run.call_args_list[0].args[0]
            self.assertIn('-DCMAKE_INSTALL_PREFIX=' + str(runtime / 'install'), args)
            self.assertIn('-DUSE_LIBPCAUDIO=OFF', args)
            self.assertEqual(probe.call_args.args[0][-1], '--version')
            self.assertIn('native-sbom.cdx.json', entries)
            self.assertEqual(json.loads((runtime / 'native-sbom.cdx.json').read_text())['bomFormat'], 'CycloneDX')

    def test_outlines_sync_is_frozen_without_optional_models(self):
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary).resolve()
            spec = native.specification('outlines', common.SPECS['outlines'])
            env = {}
            with patch.object(common, 'source_contracts'), patch.object(common, 'run') as run, \
                    patch('native_uv.activate'), patch.object(native, 'select_outlines_python', return_value='/fixture/python3.12'), \
                    patch.object(native, 'probe', side_effect=['[]', 'ok']):
                native.build(runtime, env, spec)
            command = run.call_args.args[0]
            self.assertIn('--frozen', command)
            self.assertIn('--no-default-groups', command)
            self.assertIn('--no-python-downloads', command)
            self.assertEqual(command[-1], '/fixture/python3.12')
            self.assertNotIn('--all-extras', command)
            self.assertEqual(env['HF_HUB_OFFLINE'], '1')

    def test_songrec_locked_no_gui_build(self):
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary).resolve()
            (runtime / 'Cargo.lock').write_text('[[package]]\nname="fixture"\nversion="1.0.0"\n')
            spec = native.specification('songrec', common.SPECS['songrec'])
            with patch.object(common, 'source_contracts'), patch.object(common, 'run') as run, \
                    patch.object(native, 'probe'):
                native.build(runtime, {}, spec)
            self.assertEqual(run.call_args.args[0],
                             ['cargo', 'build', '--release', '--locked', '--no-default-features', '--jobs', '1'])

    def test_readiness_inventory_has_no_runtime_claim(self):
        with patch.object(common, 'git') as git:
            report = readiness.report()
        git.assert_not_called()
        rows = {row['id']: row for row in report['tools']}
        self.assertFalse(any(row['runtime_tested'] or row['installed'] for row in rows.values()))
        self.assertEqual(rows['songsage']['state'], 'blocked')
        self.assertEqual(rows['dejavu']['state'], 'compatibility-blocked')
        self.assertEqual(rows['cloudflared']['state'], 'existing-native-build')
        self.assertTrue(all(row['reason'] for row in rows.values()))


if __name__ == '__main__':
    unittest.main()
