"""Offline bindgen prerequisites; no system library, package or Cargo execution."""
from contextlib import redirect_stdout
from copy import deepcopy
import io
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/tools/helpers'))
import native_build_deps as deps
import native_github_tools as engine
import native_sandbox_candidates as sandbox


class FirecrackerLibclangTests(unittest.TestCase):
    def setUp(self):
        self.spec = deepcopy(engine.TOOLS['firecracker'])
        self.env = {'PATH': '/usr/bin', 'LANG': 'C', 'LIBCLANG_PATH': '/untrusted',
                    'LD_LIBRARY_PATH': '/untrusted', 'PYTHONPATH': '/untrusted'}

    def probe(self, result):
        runner = Mock(return_value=result)
        with patch.object(sandbox, 'Path', PurePosixPath):
            value = sandbox.require_libclang('/fixture', self.env, runner)
        return value, runner

    def test_fragment_manifest_and_package_allowlist_match(self):
        fragment = json.loads((ROOT / 'config/native-candidates/sandbox.json').read_text())
        entry = next(item for item in fragment['tools'] if item['id'] == 'firecracker')
        self.assertEqual(entry, self.spec)
        self.assertEqual(tuple(entry['recipe']['apt_build_deps']), deps.SANDBOX_PACKAGES['firecracker'])
        self.assertIn('libclang-dev', entry['recipe']['apt_build_deps'])

    def test_loadable_host_library_sets_private_build_environment(self):
        value, runner = self.probe('{"library":"/usr/lib/x86_64-linux-gnu/libclang-21.so.21"}')
        self.assertEqual(value, '/usr/lib/x86_64-linux-gnu/libclang-21.so.21')
        self.assertEqual(self.env['LIBCLANG_PATH'], '/usr/lib/x86_64-linux-gnu')
        args, cwd, child = runner.call_args.args
        self.assertEqual(args[:4], [sys.executable, '-I', '-B', '-c'])
        self.assertEqual(args[4], sandbox.LIBCLANG_PROBE)
        self.assertEqual(child, {'PATH': '/usr/bin', 'LANG': 'C'})

    def test_llvm_and_arm64_system_layouts_supported(self):
        for library in ('/usr/lib/llvm-21/lib/libclang.so.1',
                        '/usr/lib/aarch64-linux-gnu/libclang-21.so.21',
                        '/usr/lib64/libclang.so'):
            with self.subTest(library=library):
                self.assertEqual(self.probe(json.dumps({'library': library}))[0], library)

    def test_invalid_probe_results_are_redacted_and_do_not_set_path(self):
        for result in ('{}', '[]', 'null', 'PRIVATE-MARKER', '{"library":42}',
                       '{"library":"/tmp/libclang.so"}',
                       '{"library":"/usr/lib/../tmp/libclang.so"}',
                       '{"library":"/usr/lib/libclang-cpp.so"}',
                       '{"library":"/usr/lib/libother.so"}',
                       '{"library":"/usr/lib/libclang.so","extra":"PRIVATE-MARKER"}'):
            with self.subTest(result=result), self.assertRaisesRegex(ValueError, 'ladbare Host-libclang') as error:
                self.probe(result)
            self.assertNotIn('PRIVATE-MARKER', str(error.exception))
            self.assertEqual(self.env['LIBCLANG_PATH'], '/untrusted')

    def test_timeout_and_failed_loading_stop_with_fixed_error(self):
        for failure in (subprocess.TimeoutExpired(['PRIVATE-MARKER'], 20),
                        subprocess.CalledProcessError(1, ['PRIVATE-MARKER']), OSError('PRIVATE-MARKER')):
            with self.subTest(failure=type(failure).__name__), \
                    patch.object(sandbox, 'command', side_effect=failure), \
                    self.assertRaisesRegex(ValueError, 'Kein Cargo-Build') as error:
                sandbox.require_libclang('/fixture', self.env)
            self.assertNotIn('PRIVATE-MARKER', str(error.exception))

    def test_probe_uses_twenty_second_captured_command_contract(self):
        with patch.object(sandbox, 'execute', return_value='{"library":"/usr/lib/libclang.so"}') as execute, \
                patch.object(sandbox, 'Path', PurePosixPath):
            sandbox.require_libclang('/fixture', self.env)
        self.assertEqual(execute.call_args.kwargs, {'timeout': 20, 'capture': True})

    def test_dependency_decline_stops_before_probe_or_toolchain_download(self):
        with patch.object(sandbox.platform, 'system', return_value='Linux'), \
                patch.object(sandbox.platform, 'machine', return_value='x86_64'), \
                patch.object(sandbox.os, 'geteuid', return_value=1000, create=True), \
                patch.object(sandbox, 'checked', return_value=ROOT), \
                patch.object(sandbox.shutil, 'disk_usage', return_value=Mock(free=100 * 1024**3)), \
                patch.object(Path, 'read_text', return_value='MemAvailable: 16777216 kB\n'), \
                patch.object(deps, 'prepare', side_effect=ValueError('consent required')), \
                patch.object(sandbox, 'require_libclang') as probe, \
                patch.object(sandbox, 'toolchains') as toolchains:
            with self.assertRaisesRegex(ValueError, 'consent required'):
                sandbox.preflight(ROOT, self.spec, approved=False)
        probe.assert_not_called()
        toolchains.assert_not_called()

    def test_ubuntu26_dependency_setup_simulates_and_installs_only_libclang(self):
        ready = set(deps.SANDBOX_PACKAGES['firecracker']) - {'libclang-dev'}

        def execute(args, cwd, env):
            if 'install' in args and '--simulate' not in args:
                ready.add('libclang-dev')

        with patch.object(deps, 'os_release', return_value={'ID': 'ubuntu', 'VERSION_ID': '26.04'}), \
                patch.object(deps, 'ubuntu_release', return_value=False), \
                patch.object(deps, 'debian_family', return_value=True), \
                patch.object(deps.shutil, 'which', return_value='/fixture/tool'), \
                patch.object(deps.os, 'geteuid', return_value=0, create=True), \
                patch.object(deps, 'installed', side_effect=lambda package: package in ready), \
                patch.object(deps.common, 'run', side_effect=execute) as run, redirect_stdout(io.StringIO()):
            deps.prepare(self.spec, approved=True)
        commands = [call.args[0] for call in run.call_args_list]
        self.assertEqual(len(commands), 3)
        self.assertIn('--simulate', commands[1])
        self.assertEqual(commands[2][-1], 'libclang-dev')
        self.assertIn('--no-remove', commands[2])
        self.assertIn('--no-install-recommends', commands[2])

    def test_missing_library_stops_before_rust_or_cargo(self):
        with patch.object(sandbox, 'require_libclang', side_effect=ValueError('missing libclang')), \
                patch.object(sandbox, 'command') as command:
            with self.assertRaisesRegex(ValueError, 'missing libclang'):
                sandbox.toolchains('firecracker', ROOT, self.env)
        command.assert_not_called()

    def test_failed_library_preflight_stops_before_compiler_activation(self):
        with patch.object(sandbox.platform, 'system', return_value='Linux'), \
                patch.object(sandbox.platform, 'machine', return_value='x86_64'), \
                patch.object(sandbox.os, 'geteuid', return_value=1000, create=True), \
                patch.object(sandbox, 'checked', return_value=ROOT), \
                patch.object(sandbox.shutil, 'disk_usage', return_value=Mock(free=100 * 1024**3)), \
                patch.object(Path, 'read_text', return_value='MemAvailable: 16777216 kB\n'), \
                patch.object(deps, 'prepare') as prepare, \
                patch.object(sandbox, 'require_libclang', side_effect=ValueError('missing library')), \
                patch.object(sandbox, 'executable') as executable, \
                patch.object(sandbox, 'toolchains') as toolchains:
            with self.assertRaisesRegex(ValueError, 'missing library'):
                sandbox.preflight(ROOT, self.spec, approved=True)
        prepare.assert_called_once_with(self.spec, approved=True)
        executable.assert_not_called()
        toolchains.assert_not_called()


if __name__ == '__main__':
    unittest.main()
