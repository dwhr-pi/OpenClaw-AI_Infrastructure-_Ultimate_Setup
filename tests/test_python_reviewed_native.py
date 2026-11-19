"""Offline contracts only; these fixtures are not Linux runtime acceptance."""
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/tools/helpers'))
import python_reviewed_native as helper


class ReviewedPythonTests(unittest.TestCase):
    def specs(self):
        return json.loads(helper.CANDIDATES.read_text())['tools']

    def test_exact_candidate_contracts(self):
        self.assertEqual({s['id'] for s in self.specs()}, {'phoenix', 'checkov', 'ragas'})
        for spec in self.specs():
            self.assertEqual(helper.contract(spec), spec['recipe'])
            self.assertRegex(spec['recipe']['pin'], '^[a-f0-9]{40}$')
            for digest in spec['recipe']['source_sha256'].values():
                self.assertRegex(digest, '^[a-f0-9]{64}$')
            changed = copy.deepcopy(spec)
            changed['recipe']['pin'] = '0' * 40
            with self.assertRaises(ValueError):
                helper.contract(changed)

    def test_environment_drops_credentials_and_python_injection(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {'OPENAI_API_KEY': 'not-a-key', 'AWS_PROFILE': 'not-read',
                                         'PYTHONPATH': '/not-read', 'UV_INDEX_URL': 'https://not-used'}, clear=False):
                env = helper.environment(Path(directory))
            for key in ('OPENAI_API_KEY', 'AWS_PROFILE', 'PYTHONPATH', 'UV_INDEX_URL'):
                self.assertNotIn(key, env)
            self.assertEqual(env['UV_PYTHON_DOWNLOADS'], 'never')
            self.assertEqual(env['RAGAS_DO_NOT_TRACK'], 'true')

    def test_source_mismatch_prevents_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / 'pyproject.toml').write_bytes(b'fixture')
            recipe = {'pin': 'a' * 40, 'repo': 'owner/repo',
                      'source_sha256': {'pyproject.toml': hashlib.sha256(b'other').hexdigest()}}
            with patch.object(helper.common, 'git', side_effect=[recipe['pin'], 'https://github.com/owner/repo.git']):
                with self.assertRaisesRegex(ValueError, 'Quellhash'):
                    helper.verify_source(source, recipe)

    def test_download_budgets_are_fixed_and_do_not_inherit_unsafe_uv_settings(self):
        injected = {'UV_HTTP_TIMEOUT': '999999', 'UV_HTTP_CONNECT_TIMEOUT': '0',
                    'UV_HTTP_RETRIES': '9999', 'UV_CONCURRENT_DOWNLOADS': '1000',
                    'UV_INSECURE_HOST': 'files.pythonhosted.org', 'UV_NATIVE_TLS': '0',
                    'HTTPS_PROXY': 'https://not-used', 'UV_EXTRA_INDEX_URL': 'https://not-used'}
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, injected):
            env = helper.environment(Path(directory))
        self.assertEqual(env['UV_HTTP_TIMEOUT'], '300')
        self.assertEqual(env['UV_HTTP_CONNECT_TIMEOUT'], '30')
        self.assertEqual(env['UV_HTTP_RETRIES'], '3')
        self.assertEqual(env['UV_CONCURRENT_DOWNLOADS'], '2')
        for key in ('UV_INSECURE_HOST', 'UV_NATIVE_TLS', 'HTTPS_PROXY', 'UV_EXTRA_INDEX_URL'):
            self.assertNotIn(key, env)

    def test_resolver_timeout_does_not_retry_build_or_write_success_receipt(self):
        spec = next(spec for spec in self.specs() if spec['id'] == 'ragas')
        calls = []
        def run(args, cwd, env):
            calls.append(args)
            self.assertEqual(env['UV_HTTP_TIMEOUT'], '300')
            self.assertEqual(env['UV_CONCURRENT_DOWNLOADS'], '2')
            if args[1:3] == ['pip', 'compile']:
                self.assertIn('--generate-hashes', args)
                self.assertIn('--only-binary', args)
                self.assertIn('https://pypi.org/simple', args)
                self.assertNotIn('--allow-insecure-host', args)
                raise subprocess.TimeoutExpired(args, 7200)
        with tempfile.TemporaryDirectory() as directory:
            prefix = Path(directory) / 'native'
            source = prefix / 'source'
            source.mkdir(parents=True)
            with patch.object(helper, 'verify_source'), patch.object(helper.native_uv, 'select', return_value='/uv'), \
                    patch.object(helper, 'select_python', return_value='/python'), \
                    patch.object(helper, 'execute') as probe:
                with self.assertRaises(subprocess.TimeoutExpired):
                    helper.build(source, prefix, spec, {}, run=run)
                probe.assert_not_called()
            self.assertEqual(sum(args[1:3] == ['pip', 'compile'] for args in calls), 1)
            self.assertFalse((prefix / 'python-build-receipt.json').exists())
            self.assertFalse((prefix / 'python-sbom.cdx.json').exists())

    def test_incomplete_wheels_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            wheel = Path(directory) / 'fixture.whl'
            with zipfile.ZipFile(wheel, 'w') as archive:
                archive.writestr('placeholder', 'not-a-runtime')
            for spec in self.specs():
                with self.assertRaises(ValueError):
                    helper.inspect_wheel(wheel, spec['recipe'])

    def test_probe_is_bounded_and_never_cli_execution(self):
        result = subprocess.CompletedProcess([], 0, stdout='ok')
        with patch.object(helper.subprocess, 'run', return_value=result) as run:
            self.assertEqual(helper.execute(['/python', '-I', '-c', 'pass'], ROOT, {}, 45), 'ok')
        self.assertEqual(run.call_args.kwargs['timeout'], 45)
        self.assertTrue(run.call_args.kwargs['check'])
        for spec in self.specs():
            script = helper.probe_script(spec['recipe'])
            compile(script, '<probe>', 'exec')
            self.assertIn('socket.socket.bind = denied', script)
            self.assertIn('sys.addaudithook(audit_runtime)', script)
            self.assertNotIn('subprocess.Popen = denied', script)
            self.assertNotIn('launch_app(', script)
            self.assertNotIn('evaluate(', script)

    def test_import_guard_preserves_popen_types_and_blocks_cached_process_calls(self):
        guard = helper.probe_script(self.specs()[0]['recipe']).split('assert sys.prefix != sys.base_prefix')[0]
        body = '''
assert subprocess.Popen is original
class ImportCompatiblePopen(subprocess.Popen):
    pass
assert subprocess.Popen[str]
for action in (lambda: original([sys.executable, '-c', 'raise SystemExit(99)']),
               lambda: os.system('exit 99')):
    try:
        action()
    except RuntimeError as error:
        assert 'blockiert Audit-Ereignis' in str(error)
    else:
        raise AssertionError('Process creation was not blocked')
for event in ('socket.connect', 'socket.bind', 'socket.sendto', 'os.posix_spawn', 'os.fork'):
    try:
        sys.audit(event, None)
    except RuntimeError:
        pass
    else:
        raise AssertionError(event)
print('guard-ok')
'''
        script = 'import os, subprocess\noriginal = subprocess.Popen\n' + guard + body
        result = subprocess.run([sys.executable, '-I', '-B', '-c', script],
                                capture_output=True, text=True, timeout=15, check=True)
        self.assertEqual(result.stdout.strip(), 'guard-ok')

    def test_failed_probe_logs_traceback_without_credential_shaped_values(self):
        error = subprocess.CalledProcessError(1, 'probe', stderr=(
            '\x1b[31mTraceback\x1b[0m\nModuleNotFoundError: missing_fixture\n'
            'token=hidden-value Bearer hidden-bearer https://user:hidden-password@example.test\n'))
        output = io.StringIO()
        with patch.object(helper.subprocess, 'run', side_effect=error), patch('sys.stdout', output):
            with self.assertRaises(subprocess.CalledProcessError):
                helper.execute(['python', '-c', 'probe'], ROOT, {}, 45)
        text = output.getvalue()
        self.assertIn('ModuleNotFoundError: missing_fixture', text)
        for forbidden in ('\x1b', 'hidden-value', 'hidden-bearer', 'hidden-password'):
            self.assertNotIn(forbidden, text)

    def test_timeout_diagnostics_are_bounded_and_decode_bytes(self):
        error = subprocess.TimeoutExpired('probe', 45, output=b'x' * 10000,
                                         stderr=b'Timeout detail\xff\x00')
        details = helper.failure_details(error)
        self.assertIn('Timeout detail', details)
        self.assertNotIn('\x00', details)
        self.assertLess(len(details), 6100)
        with patch.object(helper.subprocess, 'run', side_effect=error), patch('sys.stdout', io.StringIO()):
            with self.assertRaises(subprocess.TimeoutExpired):
                helper.execute(['python'], ROOT, {}, 45)
        self.assertIn('Keine Kindprozess-Ausgabe', helper.failure_details(
            subprocess.CalledProcessError(1, 'probe')))

    def test_build_runner_streams_with_shared_timeout(self):
        with patch.object(helper.native_build_process, 'run', return_value='done') as run:
            self.assertEqual(helper.build_execute(['python', '-m', 'build'], ROOT, {}), 'done')
        self.assertEqual(run.call_args.kwargs['timeout'], 7200)
        self.assertEqual(run.call_args.kwargs['label'], 'Python-/Frontend-Build')

    def test_explicit_unsupported_python_never_downloads(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {'NATIVE_SOURCE_PYTHON_BIN': '/explicit-python'}):
                with patch.object(helper, 'execute', side_effect=subprocess.CalledProcessError(1, 'probe')):
                    with patch.object(helper.native_uv, 'select') as uv:
                        with self.assertRaisesRegex(ValueError, 'Explizites'):
                            helper.select_python(Path(directory), self.specs()[0], approved=True)
                        uv.assert_not_called()

    def test_missing_python_requires_explicit_consent(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {}, clear=True), patch.object(helper.shutil, 'which', return_value=None):
                with patch.object(helper, 'execute', side_effect=subprocess.CalledProcessError(1, 'probe')):
                    with self.assertRaisesRegex(ValueError, 'freigeben'):
                        helper.select_python(Path(directory), self.specs()[0])

    def test_build_rejects_wrong_source_layout(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, 'Buildquelle'):
                helper.build(Path(directory) / 'elsewhere', Path(directory), self.specs()[0], {})


if __name__ == '__main__':
    unittest.main()
