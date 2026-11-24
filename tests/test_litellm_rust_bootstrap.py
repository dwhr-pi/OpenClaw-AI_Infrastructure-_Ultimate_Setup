"""Fixture-only private Rust bootstrap: no downloads, compiler or rustup execution."""
import io
import hashlib
import http.client
import os
from pathlib import Path
import sys
import ssl
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts/tools/helpers'))
import litellm_rust_bootstrap as bootstrap


class PrivateRustTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name) / 'litellm'
        self.base.mkdir()
        self.spec = {'id': 'litellm', 'recipe': {'disk_mb': 8192}}
        for context in (patch.dict(os.environ, {}, clear=True),
                        patch.object(bootstrap.releases, 'host_key', return_value='linux-amd64'),
                        patch.object(bootstrap.rust, 'select', side_effect=ValueError('missing')),
                        patch.object(bootstrap.sys.stdin, 'isatty', return_value=False)):
            context.start()
            self.addCleanup(context.stop)

    def fake_download(self, url, target, size, digest):
        self.assertTrue(url.startswith('https://static.rust-lang.org/rustup/archive/1.29.2/'))
        target.write_bytes(b'fixture')

    def fake_run(self, args, cwd, env):
        self.assertNotIn('OPENAI_API_KEY', env)
        self.assertEqual(env['RUSTUP_DIST_SERVER'], 'https://static.rust-lang.org')
        self.assertTrue(Path(env['CARGO_HOME']).is_relative_to(self.base))
        self.assertTrue(Path(env['HOME']).is_relative_to(self.base))
        if '--version' in args:
            return 'rustup-init 1.29.2 (fixture)'
        self.assertIn('--no-modify-path', args)
        self.assertIn(args[-1], (bootstrap.rust.VERSION, '1.99.1'))
        root = Path(env['RUSTUP_HOME']) / 'toolchains' / (args[-1] + '-x86_64-unknown-linux-gnu')
        (root / 'bin').mkdir(parents=True)
        for name in ('cargo', 'rustc'):
            (root / 'bin' / name).write_bytes(b'fixture')
        return ''

    def test_no_consent_no_download_or_mutation(self):
        for key in bootstrap.SUPPORTED:
            spec = {**self.spec, 'id': key}
            if key == 'vaultwarden':
                spec['recipe'] = {**spec['recipe'], 'rust_exact': '1.99.1'}
            with self.subTest(tool=key), patch.object(bootstrap, 'download') as download, patch.object(bootstrap.common, 'run') as run:
                with self.assertRaisesRegex(ValueError, 'nicht freigegeben'):
                    bootstrap.prepare(self.base, spec)
            download.assert_not_called()
            run.assert_not_called()
        self.assertEqual(list(self.base.iterdir()), [])

    def test_explicit_invalid_path_never_bootstraps(self):
        with patch.dict(os.environ, {'NATIVE_SOURCE_RUST_TOOLCHAIN': '/explicit'}), patch.object(bootstrap, 'download') as download:
            with self.assertRaises(ValueError):
                bootstrap.prepare(self.base, self.spec, approved=True)
        download.assert_not_called()

    def test_success_reuse_and_private_environment(self):
        with patch.object(bootstrap, 'download', side_effect=self.fake_download) as download, patch.object(bootstrap.common, 'run', side_effect=self.fake_run), patch.object(bootstrap.common, 'reserve') as reserve, patch.object(bootstrap.rust, 'verify', side_effect=lambda root, cwd, **_: root.resolve()):
            root = bootstrap.prepare(self.base, self.spec, approved=True)
            self.assertTrue((root / 'bin/cargo').is_file())
            self.assertEqual(bootstrap.prepare(self.base, self.spec), root)
            self.assertEqual(download.call_count, 1)
            reserve.assert_called_once_with(self.base, {'reserve_mb': 10240})
            self.assertFalse(list((self.base / 'toolchain').glob('rust-bootstrap-*')))

    def test_vaultwarden_has_separate_pin_and_reuses_verified_private_toolchain(self):
        spec = {'id': 'vaultwarden', 'recipe': {'disk_mb': 12288, 'rust_exact': '1.99.1'}}
        with patch.object(bootstrap, 'download', side_effect=self.fake_download) as download, \
                patch.object(bootstrap.common, 'run', side_effect=self.fake_run) as run, \
                patch.object(bootstrap.common, 'reserve') as reserve, \
                patch.object(bootstrap.rust, 'verify', side_effect=lambda root, cwd, **_: root.resolve()) as verify:
            root = bootstrap.prepare(self.base, spec, approved=True)
            self.assertIn('rust-1.99.1-linux-amd64', str(root))
            self.assertEqual(bootstrap.prepare(self.base, spec), root)
            self.assertEqual(download.call_count, 1)
            self.assertEqual(run.call_args.args[0][-1], '1.99.1')
            self.assertTrue(all(call.kwargs['version'] == '1.99.1' for call in verify.call_args_list))
            reserve.assert_called_once_with(self.base, {'reserve_mb': 14336})
            self.assertEqual(bootstrap.rust.VERSION, '1.98.0')

    def test_vaultwarden_changed_pin_is_not_bootstrapped(self):
        with patch.object(bootstrap, 'download') as download:
            with self.assertRaisesRegex(ValueError, 'Pin abweichend'):
                bootstrap.prepare(self.base, {'id': 'vaultwarden', 'recipe': {'rust_exact': 'latest'}}, approved=True)
            download.assert_not_called()

    def test_explicit_denial_never_prompts_or_downloads_a_missing_rust_toolchain(self):
        with patch.dict(os.environ, {'OPENCLAW_BUILD_DEPS_DENY': '1'}), \
                patch.object(bootstrap.sys.stdin, 'isatty', return_value=True), \
                patch('builtins.input', side_effect=AssertionError('No repeated question')) as question, \
                patch.object(bootstrap, 'download') as download, \
                patch.object(bootstrap.common, 'run') as run:
            with self.assertRaisesRegex(ValueError, 'nicht freigegeben'):
                bootstrap.prepare(self.base, self.spec, approved=True)
        question.assert_not_called()
        download.assert_not_called()
        run.assert_not_called()
        self.assertEqual(list(self.base.iterdir()), [])

    def test_vaultwarden_storage_shortfall_stops_before_staging_or_download(self):
        spec = {'id': 'vaultwarden', 'recipe': {'disk_mb': 12288, 'rust_exact': '1.99.1'}}
        with patch.object(bootstrap.common, 'reserve', side_effect=ValueError('390 MiB fehlen')) as reserve, \
                patch.object(bootstrap, 'download') as download, patch.object(bootstrap.common, 'run') as run:
            with self.assertRaisesRegex(ValueError, '390 MiB fehlen'):
                bootstrap.prepare(self.base, spec, approved=True)
        reserve.assert_called_once_with(self.base, {'reserve_mb': 14336})
        download.assert_not_called()
        run.assert_not_called()
        self.assertEqual(list(self.base.iterdir()), [])

    def test_vaultwarden_invalid_explicit_path_never_downloads(self):
        spec = {'id': 'vaultwarden', 'recipe': {'disk_mb': 12288, 'rust_exact': '1.99.1'}}
        with patch.dict(os.environ, {'NATIVE_SOURCE_RUST_TOOLCHAIN': '/explicit'}), \
                patch.object(bootstrap, 'download') as download:
            with self.assertRaises(ValueError):
                bootstrap.prepare(self.base, spec, approved=True)
            download.assert_not_called()

    def test_failed_download_cleans_only_its_staging(self):
        keep = self.base / 'keep.txt'
        keep.write_bytes(b'keep')
        with patch.object(bootstrap, 'download', side_effect=ValueError('checksum')), patch.object(bootstrap.common, 'reserve'), patch.object(bootstrap.common, 'run') as run:
            with self.assertRaisesRegex(ValueError, 'checksum'):
                bootstrap.prepare(self.base, self.spec, approved=True)
        run.assert_not_called()
        self.assertEqual(keep.read_bytes(), b'keep')
        slot, _, _, _ = bootstrap.location(self.base)
        self.assertFalse(slot.exists())
        self.assertFalse(list(slot.parent.glob('rust-bootstrap-*')))

    def test_partial_or_changed_slot_is_not_overwritten(self):
        slot, _, _, _ = bootstrap.location(self.base)
        slot.mkdir(parents=True)
        (slot / 'foreign.txt').write_bytes(b'keep')
        with patch.object(bootstrap, 'download') as download:
            with self.assertRaises(OSError):
                bootstrap.prepare(self.base, self.spec, approved=True)
        download.assert_not_called()
        self.assertEqual((slot / 'foreign.txt').read_bytes(), b'keep')

    def test_corrupt_payload_not_executed(self):
        class Response(io.BytesIO):
            def __enter__(self):
                return self
            def __exit__(self, *args):
                self.close()
        with patch.object(bootstrap, 'build_opener') as opener:
            opener.return_value.open.return_value = Response(b'wrong')
            with self.assertRaisesRegex(ValueError, 'SHA256'):
                bootstrap.download('https://static.rust-lang.org/fixture', self.base / 'payload', 5, '0' * 64)
        with self.assertRaisesRegex(ValueError, 'Host'):
            bootstrap.download('https://evil.example/fixture', self.base / 'another', 5, '0' * 64)

    def test_transport_retry_restarts_partial_file_and_checks_full_digest(self):
        class Interrupted(io.BytesIO):
            def read(self, size):
                if self.tell():
                    raise TimeoutError('fixture timeout')
                return super().read(size)
        payload = b'fixture'
        target = self.base / 'payload'
        with patch.object(bootstrap, 'build_opener') as opener:
            opener.return_value.open.side_effect = [Interrupted(b'partial'), io.BytesIO(payload)]
            bootstrap.download('https://static.rust-lang.org/fixture', target, len(payload),
                               hashlib.sha256(payload).hexdigest())
            self.assertEqual(opener.return_value.open.call_count, 2)
            for call in opener.return_value.open.call_args_list:
                self.assertEqual(call.args, ('https://static.rust-lang.org/fixture',))
                self.assertEqual(call.kwargs, {'timeout': 45})
        self.assertEqual(target.read_bytes(), payload)

    def test_two_transport_failures_stop_and_remove_only_new_payload(self):
        for error in (TimeoutError('timeout'), URLError(TimeoutError('timeout')),
                      ConnectionResetError('reset'), http.client.IncompleteRead(b'part')):
            with self.subTest(error=type(error).__name__), patch.object(bootstrap, 'build_opener') as opener:
                opener.return_value.open.side_effect = error
                with self.assertRaisesRegex(ValueError, 'nach zwei Downloadversuchen'):
                    bootstrap.download('https://static.rust-lang.org/fixture', self.base / 'payload', 5, '0' * 64)
                self.assertEqual(opener.return_value.open.call_count, 2)
                self.assertFalse((self.base / 'payload').exists())

    def test_integrity_and_security_errors_never_retry(self):
        errors = (URLError(ssl.SSLCertVerificationError('certificate')),
                  HTTPError('https://static.rust-lang.org/fixture', 403, 'denied', {}, None),
                  PermissionError('denied'), KeyboardInterrupt())
        for error in errors:
            with self.subTest(error=type(error).__name__), patch.object(bootstrap, 'build_opener') as opener:
                opener.return_value.open.side_effect = error
                with self.assertRaises(type(error)):
                    bootstrap.download('https://static.rust-lang.org/fixture', self.base / 'payload', 5, '0' * 64)
                self.assertEqual(opener.return_value.open.call_count, 1)
                self.assertFalse((self.base / 'payload').exists())
        for payload in (b'wrong', b'oversize', b''):
            with self.subTest(payload=payload), patch.object(bootstrap, 'build_opener') as opener:
                opener.return_value.open.return_value = io.BytesIO(payload)
                with self.assertRaises(ValueError):
                    bootstrap.download('https://static.rust-lang.org/fixture', self.base / 'payload', 5, '0' * 64)
                self.assertEqual(opener.return_value.open.call_count, 1)
                self.assertFalse((self.base / 'payload').exists())

    def test_existing_download_target_never_overwritten_or_removed(self):
        target = self.base / 'payload'
        target.write_bytes(b'keep')
        with patch.object(bootstrap, 'build_opener') as opener:
            with self.assertRaises(FileExistsError):
                bootstrap.download('https://static.rust-lang.org/fixture', target, 5, '0' * 64)
            opener.assert_not_called()
        self.assertEqual(target.read_bytes(), b'keep')


if __name__ == '__main__':
    unittest.main()
