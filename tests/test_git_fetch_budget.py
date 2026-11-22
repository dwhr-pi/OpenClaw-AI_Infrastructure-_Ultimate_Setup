"""Offline fetch contract; no remote, checkout, model or credential access."""
from contextlib import redirect_stdout
import io
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts/tools/helpers'))
import find_skills as helper
import native_build_process as runner

PIN = '33bc6aabd7791ad7b32f7e92104f11f2359ba890'


class GitFetchBudget(unittest.TestCase):
    def fetch(self):
        return helper.git(Path('/fixture'), 'fetch', '--depth=1', 'origin', PIN)

    def test_default_streaming_fetch_preserves_exact_pin(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(runner, 'run', return_value='ok') as run, \
                patch.object(helper.subprocess, 'run') as capture, redirect_stdout(io.StringIO()):
            self.assertEqual(self.fetch(), 'ok')
        command = run.call_args.args[0]
        self.assertEqual(command[command.index('fetch'):],
                         ['fetch', '--progress', '--no-tags', '--no-recurse-submodules',
                          '--depth=1', 'origin', PIN])
        self.assertAlmostEqual(run.call_args.kwargs['timeout'], 900, delta=1)
        for option in ('protocol.version=2', 'http.version=HTTP/1.1',
                       'http.lowSpeedLimit=1024', 'http.lowSpeedTime=120'):
            self.assertIn(option, command)
        self.assertIn('credential.helper=', command)
        self.assertIn('core.fsmonitor=false', command)
        capture.assert_not_called()

    def test_explicit_narrow_fetch_options_are_not_duplicated(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(runner, 'run') as run, \
                redirect_stdout(io.StringIO()):
            helper.git(Path('/fixture'), 'fetch', '--progress', '--no-tags',
                       '--no-recurse-submodules', '--depth=1', 'origin', PIN)
        command = run.call_args.args[0]
        for flag in ('--progress', '--no-tags', '--no-recurse-submodules'):
            self.assertEqual(command.count(flag), 1)
        self.assertEqual(command[-3:], ['--depth=1', 'origin', PIN])

    def test_truncated_ref_listing_remains_failed_after_bounded_slow_retry(self):
        error = subprocess.CalledProcessError(128, 'fixture', stderr=(
            'curl 28 Operation too slow\nfatal: expected flush after ref listing'))
        with patch.dict(os.environ, {}, clear=True), patch.object(runner, 'run', side_effect=error) as run, \
                redirect_stdout(io.StringIO()) as output:
            with self.assertRaises(subprocess.CalledProcessError) as raised:
                self.fetch()
        self.assertIs(raised.exception, error)
        self.assertEqual(run.call_count, 2)
        for call in run.call_args_list:
            command = call.args[0]
            self.assertIn('protocol.version=2', command)
            self.assertIn('--no-tags', command)
            self.assertIn('--no-recurse-submodules', command)
            self.assertEqual(command[-1], PIN)
            self.assertFalse(any(arg.startswith('--filter') for arg in command))
            self.assertNotIn('http.sslVerify=false', command)
        self.assertIn('kein weiterer Versuch', output.getvalue())

    def test_explicit_bounded_budget(self):
        for budget in ('180', '1200', '3600'):
            with patch.dict(os.environ, {'OPENCLAW_GIT_FETCH_TIMEOUT_SECONDS': budget}), \
                    patch.object(runner, 'run') as run, redirect_stdout(io.StringIO()):
                self.fetch()
            self.assertAlmostEqual(run.call_args.kwargs['timeout'], int(budget), delta=1)

    def test_invalid_budget_stops_before_process(self):
        for budget in ('00', '179', '3601', '-1', '900.5', 'infinite', ' 900', '900;echo bad'):
            with patch.dict(os.environ, {'OPENCLAW_GIT_FETCH_TIMEOUT_SECONDS': budget}), \
                    patch.object(runner, 'run') as run:
                with self.assertRaises(ValueError):
                    self.fetch()
                run.assert_not_called()

    def test_explicit_zero_removes_total_and_low_speed_limits_only_for_fetch(self):
        with patch.dict(os.environ, {'OPENCLAW_GIT_FETCH_TIMEOUT_SECONDS': '0'}), \
                patch.object(helper.time, 'monotonic', side_effect=AssertionError('No deadline')), \
                patch.object(runner, 'run', return_value='ok') as run, redirect_stdout(io.StringIO()) as output:
            self.assertEqual(self.fetch(), 'ok')
        command = run.call_args.args[0]
        self.assertIsNone(run.call_args.kwargs['timeout'])
        for flag in ('http.lowSpeedLimit=0', 'http.lowSpeedTime=0', 'protocol.version=2',
                     '--no-tags', '--no-recurse-submodules'):
            self.assertIn(flag, command)
        self.assertEqual(command[-1], PIN)
        self.assertNotIn('http.sslVerify=false', command)
        self.assertIn('unbegrenzt', output.getvalue())
        self.assertIn('keine Mindestdatenrate/Stillstandsfrist', output.getvalue())

    def test_unlimited_transport_failure_never_reenables_low_speed_limits_or_retries_forever(self):
        for message in ('curl 56 connection reset', 'curl 28 Operation too slow', 'Could not resolve host'):
            error = subprocess.CalledProcessError(128, 'fixture', stderr=message)
            with self.subTest(message=message), \
                    patch.dict(os.environ, {'OPENCLAW_GIT_FETCH_TIMEOUT_SECONDS': '0'}), \
                    patch.object(helper.time, 'sleep'), \
                    patch.object(runner, 'run', side_effect=error) as run, redirect_stdout(io.StringIO()):
                with self.assertRaises(subprocess.CalledProcessError) as raised:
                    self.fetch()
            self.assertIs(raised.exception, error)
            self.assertEqual(run.call_count, 2)
            first, second = run.call_args_list
            self.assertEqual(first.args, second.args)
            for call in run.call_args_list:
                self.assertIsNone(call.kwargs['timeout'])
                self.assertIn('http.lowSpeedTime=0', call.args[0])

    def test_unlimited_mode_preserves_interrupt_and_permanent_error_stop(self):
        for error in (KeyboardInterrupt(), subprocess.CalledProcessError(128, 'fixture', stderr='certificate verify failed')):
            with self.subTest(error=type(error).__name__), \
                    patch.dict(os.environ, {'OPENCLAW_GIT_FETCH_TIMEOUT_SECONDS': '0'}), \
                    patch.object(runner, 'run', side_effect=error) as run, redirect_stdout(io.StringIO()):
                with self.assertRaises(type(error)):
                    self.fetch()
            run.assert_called_once()

    def test_unlimited_mode_is_not_persisted_and_local_checks_remain_bounded(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(runner, 'run') as run, \
                redirect_stdout(io.StringIO()):
            with patch.dict(os.environ, {'OPENCLAW_GIT_FETCH_TIMEOUT_SECONDS': '0'}):
                self.fetch()
                with patch.object(helper.subprocess, 'run') as local:
                    local.return_value.stdout = PIN
                    self.assertEqual(helper.git(Path('/fixture'), 'rev-parse', 'HEAD'), PIN)
                self.assertEqual(local.call_args.kwargs['timeout'], 180)
            self.fetch()
        self.assertIsNone(run.call_args_list[0].kwargs['timeout'])
        self.assertAlmostEqual(run.call_args_list[1].kwargs['timeout'], 900, delta=1)
        self.assertIn('http.lowSpeedTime=120', run.call_args_list[1].args[0])

    def test_nontransport_errors_are_not_retried_or_reported_success(self):
        for text in ('', 'fatal: not our ref', 'Authentication failed', 'certificate verify failed',
                     'curl 60: SSL certificate problem', 'curl 65: send failed'):
            error = subprocess.CalledProcessError(128, 'fixture', output=text)
            with patch.dict(os.environ, {}, clear=True), patch.object(runner, 'run', side_effect=error) as run, \
                    redirect_stdout(io.StringIO()):
                with self.assertRaises(type(error)):
                    self.fetch()
                run.assert_called_once()

    def test_transient_failure_retries_identical_command_with_remaining_budget(self):
        for error in (subprocess.TimeoutExpired('fixture', 450),
                      subprocess.CalledProcessError(128, 'fixture', output=b'error: RPC failed; curl 56')):
            with patch.dict(os.environ, {}, clear=True), \
                    patch.object(helper.time, 'monotonic', side_effect=[0, 0, 450, 450]), \
                    patch.object(runner, 'run', side_effect=[error, 'ok']) as run, \
                    redirect_stdout(io.StringIO()):
                self.assertEqual(self.fetch(), 'ok')
            self.assertEqual(run.call_count, 2)
            first, second = run.call_args_list
            self.assertEqual(first.args, second.args)
            self.assertEqual(first.kwargs['timeout'], 900)
            self.assertEqual(second.kwargs['timeout'], 450)

    def test_slow_transfer_retry_changes_only_floor_and_window_with_same_deadline(self):
        error = subprocess.CalledProcessError(128, 'fixture', output=(
            b'error: RPC failed; curl 28 Operation too slow. '
            b'Less than 1024 bytes/sec transferred the last 120 seconds\nfatal: early EOF'))
        with patch.dict(os.environ, {}, clear=True), \
                patch.object(helper.time, 'monotonic', side_effect=[0, 0, 128, 128]), \
                patch.object(runner, 'run', side_effect=[error, 'ok']) as run, \
                redirect_stdout(io.StringIO()) as output:
            self.assertEqual(self.fetch(), 'ok')
        first, second = run.call_args_list
        fallback = {'http.lowSpeedLimit=1024': 'http.lowSpeedLimit=128',
                    'http.lowSpeedTime=120': 'http.lowSpeedTime=300'}
        expected = [fallback.get(item, item)
                    for item in first.args[0]]
        self.assertEqual(second.args[0], expected)
        self.assertIn('http.lowSpeedLimit=1024', first.args[0])
        self.assertIn('http.lowSpeedTime=120', first.args[0])
        self.assertIn('http.lowSpeedTime=300', second.args[0])
        self.assertEqual(second.args[0][-1], PIN)
        self.assertEqual(first.args[1:], second.args[1:])
        self.assertEqual(second.kwargs['timeout'], 772)
        self.assertIn('128 Bytes/s', output.getvalue())
        self.assertIn('300s im Restbudget', output.getvalue())

    def test_extended_stall_window_never_extends_remaining_total_budget(self):
        error = subprocess.CalledProcessError(128, 'fixture', stderr='curl 28 Operation too slow')
        with patch.dict(os.environ, {}, clear=True), \
                patch.object(helper.time, 'monotonic', side_effect=[0, 0, 700, 700]), \
                patch.object(runner, 'run', side_effect=[error, 'ok']) as run, redirect_stdout(io.StringIO()):
            self.assertEqual(self.fetch(), 'ok')
        self.assertEqual(run.call_count, 2)
        self.assertIn('http.lowSpeedTime=300', run.call_args.args[0])
        self.assertEqual(run.call_args.kwargs['timeout'], 200)
        self.assertEqual(run.call_args.args[0][-1], PIN)

    def test_slow_second_attempt_is_final_and_expiry_never_retries(self):
        error = subprocess.CalledProcessError(128, 'fixture', stderr='Operation too slow')
        with patch.dict(os.environ, {}, clear=True), patch.object(runner, 'run', side_effect=error) as run, \
                redirect_stdout(io.StringIO()) as output:
            with self.assertRaises(subprocess.CalledProcessError):
                self.fetch()
        self.assertEqual(run.call_count, 2)
        self.assertIn('kein weiterer Versuch', output.getvalue())
        with patch.dict(os.environ, {}, clear=True), \
                patch.object(helper.time, 'monotonic', side_effect=[0, 0, 901]), \
                patch.object(runner, 'run', side_effect=error) as run, redirect_stdout(io.StringIO()):
            with self.assertRaises(subprocess.CalledProcessError):
                self.fetch()
        run.assert_called_once()

    def test_permanent_errors_override_transport_words_without_relaxation(self):
        for text in ('Authentication failed', 'SSL certificate problem', 'not our ref',
                     'Permission denied', 'Repository not found'):
            error = subprocess.CalledProcessError(128, 'fixture', output=text + '\nOperation too slow; curl 28')
            with self.subTest(text=text), patch.dict(os.environ, {}, clear=True), \
                    patch.object(runner, 'run', side_effect=error) as run, redirect_stdout(io.StringIO()):
                with self.assertRaises(subprocess.CalledProcessError):
                    self.fetch()
            run.assert_called_once()
            self.assertIn('http.lowSpeedLimit=1024', run.call_args.args[0])

    def test_second_failure_is_final_and_never_reports_success(self):
        error = subprocess.TimeoutExpired('fixture', 450)
        with patch.dict(os.environ, {}, clear=True), patch.object(runner, 'run', side_effect=error) as run, \
                redirect_stdout(io.StringIO()):
            with self.assertRaises(subprocess.TimeoutExpired):
                self.fetch()
        self.assertEqual(run.call_count, 2)

    def test_expired_total_budget_prevents_retry(self):
        with patch.dict(os.environ, {}, clear=True), \
                patch.object(helper.time, 'monotonic', side_effect=[0, 0, 901]), \
                patch.object(runner, 'run', side_effect=subprocess.TimeoutExpired('fixture', 450)) as run, \
                redirect_stdout(io.StringIO()):
            with self.assertRaises(subprocess.TimeoutExpired):
                self.fetch()
        run.assert_called_once()

    def test_user_interrupt_never_retries(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(runner, 'run', side_effect=KeyboardInterrupt) as run, \
                redirect_stdout(io.StringIO()):
            with self.assertRaises(KeyboardInterrupt):
                self.fetch()
        run.assert_called_once()

    def test_dns_retries_same_command_after_delay_within_total_budget(self):
        for message in (b'Could not resolve host: github.com',
                        b'Could not resolve proxy: fixture.invalid',
                        b'Temporary failure in name resolution', b'curl 6', b'curl 5'):
            error = subprocess.CalledProcessError(128, 'fixture', stderr=message)
            with self.subTest(message=message), patch.dict(os.environ, {}, clear=True), \
                    patch.object(helper.time, 'monotonic', side_effect=[0, 0, 10, 10, 12]), \
                    patch.object(helper.time, 'sleep') as sleep, \
                    patch.object(runner, 'run', side_effect=[error, 'ok']) as run, \
                    redirect_stdout(io.StringIO()) as output:
                self.assertEqual(self.fetch(), 'ok')
            first, second = run.call_args_list
            self.assertEqual(first.args, second.args)
            self.assertEqual(second.kwargs['timeout'], 888)
            sleep.assert_called_once_with(2.0)
            self.assertIn('DNS-/Namensaufloesung', output.getvalue())
            self.assertIn('Keine Aenderung an DNS, WSL oder TLS', output.getvalue())

    def test_persistent_dns_failure_stops_after_two_attempts(self):
        error = subprocess.CalledProcessError(128, 'fixture', output='Could not resolve host: github.com')
        with patch.dict(os.environ, {}, clear=True), patch.object(helper.time, 'sleep') as sleep, \
                patch.object(runner, 'run', side_effect=error) as run, redirect_stdout(io.StringIO()):
            with self.assertRaises(subprocess.CalledProcessError):
                self.fetch()
        self.assertEqual(run.call_count, 2)
        sleep.assert_called_once()

    def test_dns_at_expired_deadline_never_sleeps_or_retries(self):
        error = subprocess.CalledProcessError(128, 'fixture', output='Could not resolve host: github.com')
        with patch.dict(os.environ, {}, clear=True), \
                patch.object(helper.time, 'monotonic', side_effect=[0, 0, 901]), \
                patch.object(helper.time, 'sleep') as sleep, patch.object(runner, 'run', side_effect=error) as run, \
                redirect_stdout(io.StringIO()):
            with self.assertRaises(subprocess.CalledProcessError):
                self.fetch()
        run.assert_called_once()
        sleep.assert_not_called()

    def test_interrupt_during_dns_backoff_never_starts_second_attempt(self):
        error = subprocess.CalledProcessError(128, 'fixture', output='Could not resolve host: github.com')
        with patch.dict(os.environ, {}, clear=True), \
                patch.object(helper.time, 'sleep', side_effect=KeyboardInterrupt), \
                patch.object(runner, 'run', side_effect=error) as run, redirect_stdout(io.StringIO()):
            with self.assertRaises(KeyboardInterrupt):
                self.fetch()
        run.assert_called_once()

    def test_provider_secrets_and_git_injection_not_inherited(self):
        with patch.dict(os.environ, {'OPENCLAW_GIT_FETCH_TIMEOUT_SECONDS': '900',
                                   'OPENAI_API_KEY': 'fixture-only', 'GITHUB_TOKEN': 'fixture-only',
                                   'GIT_CONFIG_COUNT': '99', 'GIT_CONFIG_GLOBAL': '/fixture/untrusted'}), \
                patch.object(runner, 'run') as run, redirect_stdout(io.StringIO()):
            self.fetch()
        env = run.call_args.args[2]
        self.assertNotIn('OPENAI_API_KEY', env)
        self.assertNotIn('GITHUB_TOKEN', env)
        self.assertNotIn('GIT_CONFIG_COUNT', env)
        self.assertEqual(env['GIT_CONFIG_GLOBAL'], os.devnull)
        self.assertEqual(env['GIT_LFS_SKIP_SMUDGE'], '1')

    def test_local_git_commands_keep_short_budget_and_stdout(self):
        with patch.object(helper.subprocess, 'run') as run, patch.object(runner, 'run') as stream:
            run.return_value.stdout = PIN + '\n'
            self.assertEqual(helper.git(Path('/fixture'), 'rev-parse', 'HEAD'), PIN)
        self.assertEqual(run.call_args.kwargs['timeout'], 180)
        stream.assert_not_called()


if __name__ == '__main__':
    unittest.main()
