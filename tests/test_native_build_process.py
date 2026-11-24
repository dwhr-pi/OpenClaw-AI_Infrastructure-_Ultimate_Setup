"""Exercise only tiny local child processes, never Go or an installer."""
from contextlib import redirect_stdout
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts/tools/helpers'))
import native_build_process as runner


class BuildProcessTests(unittest.TestCase):
    def execute(self, code, **options):
        return runner.run([sys.executable, '-I', '-B', '-c', code],
                          Path(__file__).resolve().parent, dict(os.environ), **options)

    def test_output_and_success_status(self):
        output = io.StringIO()
        with redirect_stdout(output):
            result = self.execute("import sys; print('stdout-fixture'); print('stderr-fixture', file=sys.stderr)")
        self.assertIn('stdout-fixture', result)
        self.assertIn('stderr-fixture', result)
        self.assertIn('PID:', output.getvalue())
        self.assertIn('Exit: 0', output.getvalue())

    def test_nonzero_exit_preserved(self):
        with redirect_stdout(io.StringIO()):
            with self.assertRaises(subprocess.CalledProcessError) as caught:
                self.execute('raise SystemExit(23)')
        self.assertEqual(caught.exception.returncode, 23)

    def test_unlimited_wait_keeps_heartbeat_past_former_two_hour_limit(self):
        process = Mock(pid=12345, stdout=io.StringIO('fixture\n'), returncode=0)
        process.wait.side_effect = [subprocess.TimeoutExpired(['fixture'], 30), 0]
        output = io.StringIO()
        with patch.object(runner.subprocess, 'Popen', return_value=process), \
                patch.object(runner.time, 'monotonic', side_effect=[0, 8000]), redirect_stdout(output):
            self.assertEqual(runner.run(['fixture'], Path('.'), {}, timeout=None), 'fixture')
        self.assertEqual([call.kwargs['timeout'] for call in process.wait.call_args_list], [30, 30])
        self.assertIn('kein automatisches Zeitlimit', output.getvalue())
        self.assertNotIn('Restbudget:', output.getvalue())
        process.kill.assert_not_called()

    def test_unlimited_wait_still_propagates_manual_interrupt_and_cleans_up(self):
        process = Mock(pid=12345, stdout=io.StringIO('fixture\n'), returncode=-9)
        process.wait.side_effect = [KeyboardInterrupt(), 0]
        process.poll.return_value = None
        with patch.object(runner.subprocess, 'Popen', return_value=process), \
                patch.object(runner.os, 'killpg', create=True) as killpg, redirect_stdout(io.StringIO()):
            with self.assertRaises(KeyboardInterrupt):
                runner.run(['fixture'], Path('.'), {}, timeout=None)
        if os.name == 'posix':
            killpg.assert_called_once_with(process.pid, runner.signal.SIGKILL)
        else:
            process.kill.assert_called_once()

    def test_unlimited_child_nonzero_exit_remains_failure(self):
        with redirect_stdout(io.StringIO()):
            with self.assertRaises(subprocess.CalledProcessError) as caught:
                self.execute('raise SystemExit(23)', timeout=None)
        self.assertEqual(caught.exception.returncode, 23)

    def test_timeout_reports_failure_and_terminates_child(self):
        output = io.StringIO()
        with redirect_stdout(output):
            with self.assertRaises(subprocess.TimeoutExpired):
                self.execute("import time; print('partial-before-timeout', flush=True); time.sleep(60)", timeout=1, heartbeat=0.2)
        self.assertIn('Build abgebrochen', output.getvalue())
        self.assertIn('Zeitlimit erreicht', output.getvalue())
        self.assertIn('partial-before-timeout', output.getvalue())
        self.assertIn('kein Fortschritts-/Erfolgsnachweis', output.getvalue())

    def test_return_buffer_is_bounded(self):
        with redirect_stdout(io.StringIO()):
            result = self.execute("print('x'*2000000)")
        self.assertLessEqual(len(result), 256 * 4096)

    @unittest.skipUnless(os.name == 'posix', 'POSIX process-group cleanup')
    def test_timeout_terminates_spawned_build_child(self):
        with tempfile.TemporaryDirectory() as directory:
            pidfile = Path(directory) / 'child.pid'
            code = ("import subprocess,sys,time; from pathlib import Path; "
                    "p=subprocess.Popen([sys.executable,'-c','import time; time.sleep(60)']); "
                    "Path(" + repr(str(pidfile)) + ").write_text(str(p.pid)); time.sleep(60)")
            with redirect_stdout(io.StringIO()), self.assertRaises(subprocess.TimeoutExpired):
                self.execute(code, timeout=2, heartbeat=0.2)
            pid = int(pidfile.read_text())
            # A killed orphan can briefly remain a zombie until init reaps it.
            for _ in range(20):
                status = Path('/proc') / str(pid) / 'stat'
                if not status.exists() or status.read_text().split(') ', 1)[1].startswith('Z '):
                    break
                time.sleep(0.1)
            else:
                self.fail('Spawned build child remained running after timeout')

    @unittest.skipUnless(os.name == 'posix', 'POSIX signal return codes')
    def test_signal_is_reported_without_claiming_oom(self):
        output = io.StringIO()
        with redirect_stdout(output):
            with self.assertRaises(subprocess.CalledProcessError) as caught:
                self.execute('import os,signal; os.kill(os.getpid(), signal.SIGKILL)')
        self.assertEqual(caught.exception.returncode, -9)
        self.assertIn('kein OOM-Nachweis', output.getvalue())


if __name__ == '__main__':
    unittest.main()
