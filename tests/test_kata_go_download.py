"""Offline Kata phase fixtures; never invoke Go, make, downloads or services."""
from contextlib import redirect_stdout
from copy import deepcopy
import hashlib
import io
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/tools/helpers'))
import native_sandbox_candidates as kata


class KataGoTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.prefix = Path(temporary.name).resolve()
        self.source = self.prefix / 'source'
        self.module = self.source / 'src/runtime'
        self.module.mkdir(parents=True)
        self.item = {'version': '4.3.1', 'source_sha256': {}}
        for name in ('go.mod', 'go.sum'):
            data = ('synthetic ' + name + '\n').encode()
            (self.module / name).write_bytes(data)
            self.item['source_sha256']['src/runtime/' + name] = hashlib.sha256(data).hexdigest()
        self.environment = {'PATH': 'fixture', 'GOPROXY': 'https://proxy.golang.org',
                            'GOSUMDB': 'sum.golang.org'}
        self.addCleanup(patch.stopall)
        patch.dict(os.environ, {name: str(default) for name, default, _, _ in kata.KATA_TIMEOUTS.values()}).start()
        patch('socket.socket', side_effect=AssertionError('no network')).start()

    def phases(self, run=None, env=None):
        with redirect_stdout(io.StringIO()) as output:
            kata.kata_go_phases(self.module, self.prefix, self.item,
                               self.environment if env is None else env, run)
        return output.getvalue()

    def test_defaults_and_valid_phase_overrides(self):
        self.assertEqual({'download': 1800, 'verify': 300, 'build': 7200}, kata.kata_timeouts({}))
        for phase, (name, _, minimum, maximum) in kata.KATA_TIMEOUTS.items():
            for value in (minimum, maximum):
                with self.subTest(phase=phase, value=value):
                    self.assertEqual(value, kata.kata_timeouts({name: str(value)})[phase])
            with patch.dict(os.environ, {name: str(minimum)}):
                self.assertEqual(minimum, kata.kata_timeouts({})[phase])

    def test_invalid_timeouts_redacted_before_any_process(self):
        for phase, (name, _, minimum, maximum) in kata.KATA_TIMEOUTS.items():
            for value in ('PRIVATE-VALUE', '', '1.5', '-1', ' 300', '300 ', '1e3',
                          '999999999999999', str(minimum - 1), str(maximum + 1), True, 300):
                with self.subTest(phase=phase, value=value), patch.object(kata.native_build_process, 'run') as run:
                    with self.assertRaises(kata.KataPhaseError) as caught:
                        self.phases(env={**self.environment, name: value})
                    self.assertEqual('kata_go_' + phase + '_timeout_invalid', str(caught.exception))
                    run.assert_not_called()

    def test_invalid_config_fails_preflight_before_dependencies(self):
        spec = {'id': 'kata_containers', 'recipe': {'pin': kata.PINS['kata_containers'],
                                                 'kind': 'candidate-native'}}
        with patch.dict(os.environ, {'KATA_GO_DOWNLOAD_TIMEOUT_SECONDS': 'PRIVATE'}), \
                patch.object(kata, 'toolchains') as toolchains, \
                patch.object(kata, 'executable') as executable:
            with self.assertRaisesRegex(kata.KataPhaseError, 'download_timeout_invalid'):
                kata.preflight(self.prefix, spec, approved=True)
        toolchains.assert_not_called()
        executable.assert_not_called()

    def test_invalid_config_fails_build_before_source_or_toolchain(self):
        spec = {'id': 'kata_containers', 'recipe': {'pin': kata.PINS['kata_containers'],
                                                 'kind': 'candidate-native'}}
        with patch.object(kata, 'verify_source') as source, patch.object(kata, 'toolchains') as tools:
            with self.assertRaises(kata.KataPhaseError):
                kata.build(self.source, self.prefix, spec, {'KATA_GO_VERIFY_TIMEOUT_SECONDS': 'PRIVATE'})
        source.assert_not_called()
        tools.assert_not_called()

    def test_delegates_all_phases_to_shared_heartbeat_runner(self):
        original = deepcopy(self.environment)
        with patch.object(kata.native_build_process, 'run', return_value='truncated JSON tail') as run:
            output = self.phases(env={**self.environment, 'KATA_GO_DOWNLOAD_TIMEOUT_SECONDS': '60'})
        self.assertEqual(3, run.call_count)
        self.assertEqual(['go', 'mod', 'download', '-json'], run.call_args_list[0].args[0])
        self.assertEqual(['go', 'mod', 'verify'], run.call_args_list[1].args[0])
        self.assertEqual(['make', '-j2', 'runtime', 'containerd-shim-v2',
                          'VERSION=4.3.1', 'PREFIX=' + str(self.prefix)], run.call_args_list[2].args[0])
        for call, phase, timeout in zip(run.call_args_list, ('download', 'verify', 'build'), (60, 300, 7200)):
            self.assertEqual(self.module, call.args[1])
            self.assertEqual({'timeout': timeout, 'heartbeat': 30, 'label': 'Kata-Go-' + phase}, call.kwargs)
            self.assertEqual('-mod=readonly -p=2', call.args[2]['GOFLAGS'])
            self.assertEqual('local', call.args[2]['GOTOOLCHAIN'])
            self.assertEqual('https://proxy.golang.org', call.args[2]['GOPROXY'])
            self.assertEqual('sum.golang.org', call.args[2]['GOSUMDB'])
        self.assertIn('Heartbeat ist kein Fortschrittsnachweis', output)
        self.assertEqual(original, self.environment)

    def test_injected_runner_retains_three_argument_contract(self):
        run = Mock(return_value='')
        with patch.object(kata.native_build_process, 'run') as shared:
            self.phases(run)
        self.assertEqual(3, run.call_count)
        for call in run.call_args_list:
            self.assertEqual(3, len(call.args))
            self.assertEqual({}, call.kwargs)
        shared.assert_not_called()

    def test_each_phase_timeout_or_failure_stops_without_retry_and_redacts(self):
        for index, phase in enumerate(('download', 'verify', 'build')):
            for error, suffix in [(subprocess.TimeoutExpired(['PRIVATE'], 60, output='PRIVATE'), 'timeout'),
                                  (subprocess.CalledProcessError(1, ['PRIVATE'], output='PRIVATE'), 'failed'),
                                  (OSError('PRIVATE'), 'failed'), (KeyboardInterrupt(), 'interrupted')]:
                with self.subTest(phase=phase, suffix=suffix), \
                        patch.object(kata.native_build_process, 'run', side_effect=[''] * index + [error]) as run:
                    with self.assertRaises(kata.KataPhaseError) as caught:
                        self.phases()
                    self.assertEqual('kata_go_' + phase + '_' + suffix, str(caught.exception))
                    self.assertTrue(caught.exception.__suppress_context__)
                    self.assertEqual(index + 1, run.call_count)
                    self.assertFalse((self.prefix / 'build-ready.json').exists())

    def test_changed_lock_stops_before_next_phase(self):
        for index, phase in enumerate(('download', 'verify', 'build')):
            for name in ('go.mod', 'go.sum'):
                original = (self.module / name).read_bytes()
                count = 0

                def change(*args, **kwargs):
                    nonlocal count
                    if count == index:
                        (self.module / name).write_bytes(b'changed fixture')
                    count += 1

                with self.subTest(phase=phase, name=name), \
                        patch.object(kata.native_build_process, 'run', side_effect=change) as run:
                    with self.assertRaisesRegex(kata.KataPhaseError, phase + '_source_contract_changed'):
                        self.phases()
                    self.assertEqual(index + 1, run.call_count)
                (self.module / name).write_bytes(original)

    def test_missing_or_changed_initial_lock_never_downloads(self):
        (self.module / 'go.sum').write_bytes(b'changed')
        with patch.object(kata.native_build_process, 'run') as run:
            with self.assertRaisesRegex(kata.KataPhaseError, 'download_source_contract_changed'):
                self.phases()
        run.assert_not_called()

    def test_shared_runner_emits_silent_process_heartbeat_without_real_process(self):
        processes = []
        for _ in range(3):
            process = Mock(pid=1234, returncode=0)
            process.stdout = io.StringIO('')
            process.wait.return_value = 0
            processes.append(process)
        processes[0].wait.side_effect = [subprocess.TimeoutExpired(['fixture'], 30), 0]
        with patch.object(kata.native_build_process.subprocess, 'Popen', side_effect=processes) as popen:
            output = self.phases()
        self.assertIn('Kata-Go-download laeuft; PID: 1234', output)
        self.assertIn('kein Fortschritts-/Erfolgsnachweis', output)
        self.assertEqual(os.name == 'posix', popen.call_args_list[0].kwargs['start_new_session'])

    def test_shared_runner_timeout_delegates_process_group_cleanup(self):
        process = Mock(pid=1234, returncode=-9)
        process.stdout = io.StringIO('')
        process.poll.return_value = None
        process.wait.side_effect = [subprocess.TimeoutExpired(['fixture'], 30), 0]
        # Advance the deadline without waiting or launching any child process.
        with patch.object(kata.native_build_process.subprocess, 'Popen', return_value=process), \
                patch.object(kata.native_build_process.time, 'monotonic', side_effect=[0, 0, 0, 1801, 1801, 1801]), \
                patch.object(kata.native_build_process.os, 'killpg', create=True) as killpg:
            with self.assertRaisesRegex(kata.KataPhaseError, 'download_timeout'):
                self.phases()
        if os.name == 'posix':
            killpg.assert_called_once_with(1234, signal.SIGKILL)
        else:
            process.kill.assert_called_once_with()
        self.assertEqual(2, process.wait.call_count)

    def test_build_download_timeout_never_copies_artifacts_or_writes_receipts(self):
        spec = {'id': 'kata_containers', 'recipe': {
            **self.item, 'pin': kata.PINS['kata_containers'], 'kind': 'candidate-native'}}
        run = Mock(side_effect=subprocess.TimeoutExpired(['PRIVATE'], 60))
        with patch.object(kata, 'verify_source'), patch.object(kata, 'toolchains', return_value={}), \
                patch.object(kata, 'copy_binary') as copy, patch.object(kata, 'probe') as probe, \
                redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(kata.KataPhaseError, 'kata_go_download_timeout'):
                kata.build(self.source, self.prefix, spec, self.environment, run)
        run.assert_called_once()
        self.assertEqual(['go', 'mod', 'download', '-json'], run.call_args.args[0])
        copy.assert_not_called()
        probe.assert_not_called()
        self.assertEqual([], list((self.prefix / 'sandbox-receipts').iterdir()))
        self.assertFalse((self.prefix / 'build-ready.json').exists())


if __name__ == '__main__':
    unittest.main()
