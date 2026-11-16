"""Offline kube-bench installation fixtures; no compiler, cluster, keys or audit."""
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

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/tools/helpers'))
import kube_bench_native as bench
import native_github_tools as tools
import native_go


class KubeBenchNative(unittest.TestCase):
    def fixture(self, base):
        spec = copy.deepcopy(tools.TOOLS['kube_bench'])
        for name in spec['recipe']['source_sha256']:
            path = base / 'source' / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(('fixture:' + name).encode())
            spec['recipe']['source_sha256'][name] = hashlib.sha256(path.read_bytes()).hexdigest()
        (base / 'source/cfg/check.yaml').write_text('fixture-not-executed')
        return spec

    def test_native_pin_go_and_version_contract(self):
        spec = tools.TOOLS['kube_bench']
        recipe = spec['recipe']
        self.assertEqual(recipe['pin'], '5c6c22d51b926020e7414e1f1e051851d1a2feff')
        self.assertEqual(recipe['go_min'], native_go.CONTRACTS['kube_bench'][0])
        self.assertEqual(recipe['probe'], ['version'])
        self.assertIn('cmd.KubeBenchVersion=0.16.0', recipe['ldflags'])
        self.assertGreaterEqual(recipe['disk_mb'], 8192)
        for digest in recipe['source_sha256'].values():
            self.assertRegex(digest, r'^[a-f0-9]{64}$')

    def test_source_failure_prevents_success_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            spec = self.fixture(base)
            (base / 'source/go.sum').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'Quellhash'):
                bench.prepare(base, spec, {})
            self.assertFalse((base / 'kube-bench-build-lock.json').exists())

    def test_only_version_with_reviewed_config_and_without_credentials(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            spec = self.fixture(base)
            bench.prepare(base, spec, {})
            result = subprocess.CompletedProcess([], 0, stdout='0.16.0\n', stderr='')
            with patch.object(bench.subprocess, 'run', return_value=result) as run:
                artifacts = bench.receipts(base, spec, {'HOME': str(base), 'KUBECONFIG': '/not-read',
                                                       'AWS_SECRET_ACCESS_KEY': 'fixture', 'KUBE_BENCH_CONFIG': '/not-read'})
            args = run.call_args.args[0]
            self.assertEqual(args[1], 'version')
            self.assertEqual(args[2:], ['--config', str(base / 'source/cfg/config.yaml'), '--config-dir', str(base / 'source/cfg')])
            self.assertEqual(run.call_args.kwargs['timeout'], 30)
            self.assertEqual(run.call_args.kwargs['env'], {'HOME': str(base)})
            self.assertIn('source/cfg/check.yaml', artifacts)
            probe = json.loads((base / 'kube-bench-version-probe.json').read_text())
            self.assertFalse(probe['audit_performed'])
            self.assertFalse(probe['credentials_passed'])

    def test_config_change_blocks_binary_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            spec = self.fixture(base)
            bench.prepare(base, spec, {})
            (base / 'source/cfg/check.yaml').write_text('changed')
            with patch.object(bench.subprocess, 'run') as run:
                with self.assertRaisesRegex(ValueError, 'Benchmark-Dateien'):
                    bench.receipts(base, spec, {})
                run.assert_not_called()

    def test_go_lock_change_blocks_binary_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            spec = self.fixture(base)
            bench.prepare(base, spec, {})
            (base / 'source/go.sum').write_text('changed')
            with patch.object(bench.subprocess, 'run') as run:
                with self.assertRaisesRegex(ValueError, 'Go-Lockdatei'):
                    bench.receipts(base, spec, {})
                run.assert_not_called()

    def test_wrong_version_cannot_claim_installed(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            spec = self.fixture(base)
            bench.prepare(base, spec, {})
            with patch.object(bench.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, stdout='other')):
                with self.assertRaisesRegex(ValueError, 'Versionsprobe'):
                    bench.receipts(base, spec, {})
            self.assertFalse((base / 'kube-bench-version-probe.json').exists())

    def test_plans_and_status_never_download_or_scan(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {'OPENCLAW_USER_DATA_DIR': directory}), \
                patch.object(tools, 'preflight') as preflight, patch.object(tools.common, 'git') as git, \
                patch.object(bench.subprocess, 'run') as run, redirect_stdout(io.StringIO()):
            self.assertEqual(tools.main(['kube_bench', 'plan', '--install-build-deps']), 0)
            self.assertEqual(tools.main(['kube_bench', 'status']), 0)
            self.assertEqual(list(Path(directory).iterdir()), [])
            preflight.assert_not_called()
            git.assert_not_called()
            run.assert_not_called()

    def test_all_wrappers_delegate_to_safe_native_lifecycle(self):
        for action in ('install', 'update', 'uninstall', 'status', 'doctor', 'check'):
            text = (ROOT / ('scripts/tools/kube_bench_' + action + '.sh')).read_text()
            self.assertIn('native_github_tools.py" kube_bench ' + action, text)
            self.assertNotIn('sudo ', text)
            self.assertNotIn('kubectl ', text)


if __name__ == '__main__':
    unittest.main()
