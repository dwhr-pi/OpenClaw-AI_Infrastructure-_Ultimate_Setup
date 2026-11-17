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
        self.assertEqual(command[-5:], ['fetch', '--progress', '--depth=1', 'origin', PIN])
        self.assertAlmostEqual(run.call_args.kwargs['timeout'], 900, delta=1)
        for option in ('http.version=HTTP/1.1', 'http.lowSpeedLimit=1024', 'http.lowSpeedTime=120'):
            self.assertIn(option, command)
        self.assertIn('credential.helper=', command)
        self.assertIn('core.fsmonitor=false', command)
        capture.assert_not_called()

    def test_explicit_bounded_budget(self):
        for budget in ('180', '1200', '3600'):
            with patch.dict(os.environ, {'OPENCLAW_GIT_FETCH_TIMEOUT_SECONDS': budget}), \
                    patch.object(runner, 'run') as run, redirect_stdout(io.StringIO()):
                self.fetch()
            self.assertAlmostEqual(run.call_args.kwargs['timeout'], int(budget), delta=1)

    def test_invalid_budget_stops_before_process(self):
        for budget in ('0', '179', '3601', '-1', '900.5', 'infinite', ' 900', '900;echo bad'):
            with patch.dict(os.environ, {'OPENCLAW_GIT_FETCH_TIMEOUT_SECONDS': budget}), \
                    patch.object(runner, 'run') as run:
                with self.assertRaises(ValueError):
                    self.fetch()
                run.assert_not_called()

    def test_nontransport_errors_are_not_retried_or_reported_success(self):
        for text in ('', 'fatal: not our ref', 'Authentication failed', 'certificate verify failed'):
            error = subprocess.CalledProcessError(128, 'fixture', output=text)
            with patch.dict(os.environ, {}, clear=True), patch.object(runner, 'run', side_effect=error) as run, \
                    redirect_stdout(io.StringIO()):
                with self.assertRaises(type(error)):
                    self.fetch()
                run.assert_called_once()

    def test_transient_failure_retries_identical_command_with_remaining_budget(self):
        for error in (subprocess.TimeoutExpired('fixture', 450),
                      subprocess.CalledProcessError(128, 'fixture', output=b'error: RPC failed; curl 56'),
                      subprocess.CalledProcessError(128, 'fixture', stderr='Operation too slow')):
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
