"""Offline contracts only; these fixtures are not Linux runtime acceptance."""
from contextlib import redirect_stdout
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
        self.assertEqual({s['id'] for s in self.specs()}, {'phoenix', 'checkov', 'ragas', 'openjarvis'})
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

    def test_ragas_compatibility_is_explicit_and_does_not_affect_other_tools(self):
        for spec in self.specs():
            requirements = helper.runtime_compatibility_requirements(spec)
            if spec['id'] == 'ragas':
                self.assertEqual(requirements, ['langchain-community==0.3.31', 'langchain>=0.3.27,<1.0',
                                                'langchain-core>=0.3.78,<1.0', 'langchain-openai>=0.3,<1.0'])
                changed = copy.deepcopy(spec)
                changed['recipe']['version'] = '0.4.0'
                with self.assertRaisesRegex(ValueError, 'nur fuer'):
                    helper.runtime_compatibility_requirements(changed)
            else:
                self.assertEqual(requirements, [])

    def test_ragas_runtime_compatibility_flows_through_hash_lock_and_guarded_probe(self):
        spec = next(spec for spec in self.specs() if spec['id'] == 'ragas')
        with tempfile.TemporaryDirectory() as directory:
            prefix = Path(directory) / 'native'
            source = prefix / 'source'
            source.mkdir(parents=True)
            calls = []
            def run(args, cwd, env):
                calls.append(args)
                if '-m' in args and 'build' in args:
                    (prefix / 'wheels/ragas-fixture.whl').write_bytes(b'synthetic, never imported')
                if args[1:3] == ['pip', 'compile']:
                    self.assertIn('--generate-hashes', args)
                    if Path(args[3]).name == 'runtime-requirements.in':
                        lines = Path(args[3]).read_text(encoding='utf-8').splitlines()
                        self.assertEqual(lines[1:], list(helper.RAGAS_COMPATIBILITY))
                if args[1:3] == ['pip', 'install']:
                    self.assertIn('--require-hashes', args)
                    self.assertIn('--only-binary', args)
                    self.assertIn('https://pypi.org/simple', args)
                    cli = prefix / 'venv/bin/ragas'
                    cli.parent.mkdir(parents=True, exist_ok=True)
                    cli.write_bytes(b'fixture')
            report = {'distributions': [{'name': 'ragas', 'version': '0.3.9'}]}
            with patch.object(helper, 'verify_source'), patch.object(helper, 'inspect_wheel'), \
                    patch.object(helper.native_uv, 'select', return_value='/uv'), \
                    patch.object(helper, 'select_python', return_value='/python'), \
                    patch.object(helper, 'execute', return_value=json.dumps(report)) as probe:
                helper.build(source, prefix, spec, {}, run=run)
                self.assertEqual(probe.call_args.args[-1], 45)
                self.assertIn('sys.addaudithook(audit_runtime)', probe.call_args.args[0][-1])
            receipt = json.loads((prefix / 'python-build-receipt.json').read_text(encoding='utf-8'))
            self.assertEqual(receipt['runtime_compatibility_requirements'], list(helper.RAGAS_COMPATIBILITY))
            self.assertFalse(receipt['application_tested'])
            self.assertEqual(sum(args[1:3] == ['pip', 'install'] for args in calls), 2)

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

    def test_phoenix_frontend_executor_has_no_total_timeout(self):
        args = [Path('/private/pnpm'), 'install', '--frozen-lockfile', '--ignore-scripts']
        with patch.object(helper.native_build_process, 'run', return_value='ok') as run, \
                redirect_stdout(io.StringIO()):
            self.assertEqual(helper.frontend_execute(args, Path('/source/app'), {}), 'ok')
        self.assertIsNone(run.call_args.kwargs['timeout'])
        self.assertEqual(run.call_args.args, (args, Path('/source/app'), {}))

    def test_phoenix_build_routes_only_frontend_commands_to_unlimited_executor(self):
        spec = next(spec for spec in self.specs() if spec['id'] == 'phoenix')
        with tempfile.TemporaryDirectory() as directory:
            prefix = Path(directory) / 'native'
            source = prefix / 'source'
            manifest = source / 'src/phoenix/server/static/.vite/manifest.json'
            manifest.parent.mkdir(parents=True)
            manifest.write_text('{}')
            calls = []

            def run(args, cwd, env):
                calls.append(list(map(str, args)))
                if '-m' in args and 'build' in args:
                    (prefix / 'wheels/phoenix-fixture.whl').write_bytes(b'fixture, never imported')
                if args[1:3] == ['pip', 'install']:
                    cli = prefix / 'venv/bin' / spec['recipe']['cli']
                    cli.parent.mkdir(parents=True, exist_ok=True)
                    cli.write_bytes(b'fixture')

            with patch.object(helper, 'verify_source'), patch.object(helper, 'inspect_wheel'), \
                    patch.object(helper.native_uv, 'select', return_value='/uv'), \
                    patch.object(helper, 'select_python', return_value='/python'), \
                    patch.object(helper, 'frontend', return_value=Path('/private/frontend')), \
                    patch.object(helper, 'build_execute', side_effect=run), \
                    patch.object(helper, 'frontend_execute', return_value='ok') as frontend, \
                    patch.object(helper, 'install_locked_wheels', return_value='ok'), \
                    patch.object(helper, 'execute', return_value='{"distributions": []}') as probe, \
                    redirect_stdout(io.StringIO()):
                # The application CLI is created only by the mocked wheel installer.
                cli = prefix / 'venv/bin' / spec['recipe']['cli']
                cli.parent.mkdir(parents=True)
                cli.write_bytes(b'fixture')
                helper.build(source, prefix, spec, {})
                self.assertEqual(probe.call_args.args[-1], 45)
            self.assertEqual([list(map(str, call.args[0]))[1:] for call in frontend.call_args_list], [
                ['install', '--frozen-lockfile', '--ignore-scripts'], ['rebuild', 'esbuild'], ['run', 'build']])
            self.assertFalse(any(Path(call[0]).name == 'pnpm' for call in calls))

    def wheel_install_command(self):
        return ['/uv', 'pip', 'install', '--python', '/venv/python', '--require-hashes',
                '--only-binary', ':all:', '-r', '/private/runtime-requirements.lock',
                '--index-url', 'https://pypi.org/simple', '--no-config', '--keyring-provider', 'disabled']

    def test_wheel_download_timeout_retries_same_lock_and_cache_in_shared_budget(self):
        args = self.wheel_install_command()
        env = {'UV_HTTP_TIMEOUT': '300', 'UV_CONCURRENT_DOWNLOADS': '2',
               'UV_CACHE_DIR': '/private/cache', 'UV_HTTP_CONNECT_TIMEOUT': '30', 'UV_HTTP_RETRIES': '3'}
        error = subprocess.CalledProcessError(1, args, stderr=(
            b'Failed to download `pyarrow==26.0.1`\nI/O operation failed during extraction\n'
            b'Failed to download distribution due to network timeout'))
        with patch.object(helper.time, 'monotonic', side_effect=[0, 0, 420, 420]), \
                patch.object(helper.native_build_process, 'run', side_effect=[error, 'ok']) as run, \
                redirect_stdout(io.StringIO()):
            self.assertEqual(helper.install_locked_wheels(args, Path('/private'), env), 'ok')
        first, second = run.call_args_list
        self.assertEqual(run.call_count, 2)
        self.assertEqual(first.args[:2], second.args[:2])
        self.assertEqual(first.args[0], args)
        self.assertEqual(first.kwargs['timeout'], 7200)
        self.assertEqual(second.kwargs['timeout'], 6780)
        self.assertEqual(first.args[2]['UV_HTTP_TIMEOUT'], '300')
        self.assertEqual(second.args[2], dict(env, UV_HTTP_TIMEOUT='900', UV_CONCURRENT_DOWNLOADS='1'))
        self.assertEqual(env['UV_HTTP_TIMEOUT'], '300')

    def test_other_wheel_errors_never_relax_hash_tls_or_disk_failures(self):
        args = self.wheel_install_command()
        for message in ('Hash mismatch', 'certificate verify failed', 'No space left on device',
                        'Disk quota exceeded', 'Permission denied', '401 Unauthorized', '403 Forbidden',
                        'No solution found', 'I/O operation failed during extraction'):
            error = subprocess.CalledProcessError(1, args, stderr=message)
            if message not in ('No solution found', 'I/O operation failed during extraction'):
                error.stderr += '\nFailed to download distribution due to network timeout'
            with self.subTest(message=message), \
                    patch.object(helper.native_build_process, 'run', side_effect=error) as run, \
                    redirect_stdout(io.StringIO()):
                with self.assertRaises(subprocess.CalledProcessError) as raised:
                    helper.install_locked_wheels(args, Path('/private'), {})
                self.assertIs(raised.exception, error)
                run.assert_called_once()

    def test_temporary_dns_uses_only_existing_second_attempt_and_same_lock(self):
        args = self.wheel_install_command()
        env = {'UV_CACHE_DIR': '/private/cache', 'UV_HTTP_TIMEOUT': '300'}
        error = subprocess.CalledProcessError(2, args, stderr=(
            b'Failed to download `huggingface-hub==2.4.0`\ncause: dns error\n'
            b'failed to lookup address information: Temporary failure in name resolution'))
        output = io.StringIO()
        with patch.object(helper.time, 'monotonic', side_effect=[0, 0, 20, 20]), \
                patch.object(helper.native_build_process, 'run', side_effect=[error, 'ok']) as run, \
                redirect_stdout(output):
            self.assertEqual(helper.install_locked_wheels(args, Path('/private'), env), 'ok')
        self.assertEqual(run.call_count, 2)
        first, second = run.call_args_list
        self.assertEqual(first.args[:2], second.args[:2])
        self.assertEqual(second.args[2], dict(env, UV_HTTP_TIMEOUT='900', UV_CONCURRENT_DOWNLOADS='1'))
        self.assertEqual(second.kwargs['timeout'], 7180)
        self.assertIn('DNS-/Namensaufloesung', output.getvalue())
        self.assertNotIn('UV_CONCURRENT_DOWNLOADS', env)

    def test_timeout_then_dns_reports_root_cause_without_third_attempt(self):
        args = self.wheel_install_command()
        timeout = subprocess.CalledProcessError(1, args, stderr='Failed to download due to network timeout')
        dns = subprocess.CalledProcessError(2, args, stderr=(
            'Failed to download `huggingface-hub`\ndns error\nTemporary failure in name resolution'))
        with patch.object(helper.native_build_process, 'run', side_effect=[timeout, dns]) as run, \
                redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, 'DNS-/Namensaufloesung') as raised:
                helper.install_locked_wheels(args, Path('/private'), {})
        self.assertEqual(run.call_count, 2)
        self.assertIs(raised.exception.__cause__, dns)

    def test_dns_does_not_override_permanent_errors_or_retry_permanent_resolution_failure(self):
        args = self.wheel_install_command()
        for reason in ('Hash mismatch', 'certificate verify failed', 'No space left on device',
                       '403 Forbidden', 'Name or service not known'):
            error = subprocess.CalledProcessError(2, args, stderr=(
                'Failed to download package\ndns error\n' + reason))
            with self.subTest(reason=reason), \
                    patch.object(helper.native_build_process, 'run', side_effect=error) as run, \
                    redirect_stdout(io.StringIO()):
                expected = ValueError if reason == 'Name or service not known' else subprocess.CalledProcessError
                with self.assertRaises(expected):
                    helper.install_locked_wheels(args, Path('/private'), {})
                run.assert_called_once()

    def test_expired_budget_does_not_retry_temporary_dns(self):
        args = self.wheel_install_command()
        error = subprocess.CalledProcessError(2, args, stderr=(
            'Failed to download package\ndns error\nTemporary failure in name resolution'))
        with patch.object(helper.time, 'monotonic', side_effect=[0, 0, 7201]), \
                patch.object(helper.native_build_process, 'run', side_effect=error) as run, \
                redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, 'DNS-/Namensaufloesung'):
                helper.install_locked_wheels(args, Path('/private'), {})
            run.assert_called_once()

    def test_second_wheel_timeout_is_final_and_process_timeout_never_retries(self):
        args = self.wheel_install_command()
        for error, count in ((subprocess.CalledProcessError(1, args, stderr=(
                'Failed to download distribution due to network timeout')), 2),
                (subprocess.TimeoutExpired(args, 7200), 1), (KeyboardInterrupt(), 1)):
            with self.subTest(error=type(error).__name__), \
                    patch.object(helper.native_build_process, 'run', side_effect=error) as run, \
                    redirect_stdout(io.StringIO()):
                with self.assertRaises(type(error)):
                    helper.install_locked_wheels(args, Path('/private'), {})
                self.assertEqual(run.call_count, count)

    def test_expired_wheel_budget_keeps_original_error_without_retry(self):
        args = self.wheel_install_command()
        error = subprocess.CalledProcessError(1, args, stderr='Failed to download due to network timeout')
        with patch.object(helper.time, 'monotonic', side_effect=[0, 0, 7201]), \
                patch.object(helper.native_build_process, 'run', side_effect=error) as run, \
                redirect_stdout(io.StringIO()):
            with self.assertRaises(subprocess.CalledProcessError) as raised:
                helper.install_locked_wheels(args, Path('/private'), {})
            self.assertIs(raised.exception, error)
            run.assert_called_once()

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

    def test_ragas_probe_handles_denied_git_refresh_without_starting_any_process(self):
        recipe = next(spec['recipe'] for spec in self.specs() if spec['id'] == 'ragas')
        guard = helper.probe_script(recipe).split('assert sys.prefix != sys.base_prefix')[0]
        body = '''
assert os.environ["GIT_PYTHON_REFRESH"] == "quiet"
assert subprocess.Popen is original
assert subprocess.Popen[str]
# Reproduce GitPython's refresh exception handling, without importing upstream code.
git_ok = False
try:
    subprocess.run(["git", "version"], check=True, capture_output=True)
    git_ok = True
except (FileNotFoundError, PermissionError):
    pass
assert git_ok is False
for args in ([sys.executable, "-c", "raise SystemExit(99)"], ["git", "fetch", "https://example.invalid"]):
    try:
        original(args)
    except PermissionError as error:
        assert 'blockiert Audit-Ereignis' in str(error)
    else:
        raise AssertionError("Process was allowed")
for event in ('socket.connect', 'socket.bind', 'socket.sendto', 'os.posix_spawn', 'os.fork', 'os.system'):
    try:
        sys.audit(event, None)
    except RuntimeError:
        pass
    else:
        raise AssertionError(event)
print('ragas-guard-ok')
'''
        script = 'import subprocess\noriginal = subprocess.Popen\n' + guard + body
        result = subprocess.run([sys.executable, '-I', '-B', '-c', script],
                                capture_output=True, text=True, timeout=15, check=True)
        self.assertEqual(result.stdout.strip(), 'ragas-guard-ok')
        self.assertIn('importlib.import_module("git").GIT_OK is False', helper.probe_script(recipe))
        for spec in self.specs():
            if spec['id'] != 'ragas':
                self.assertNotIn('GIT_PYTHON_REFRESH', helper.probe_script(spec['recipe']))
        self.assertIn('"git_runtime_tested": False', helper.probe_script(recipe))

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
