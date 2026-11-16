"""Offline Valkey source-build contracts; no compiler, network or server execution."""
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
import native_github_tools as tools
import native_build_deps as deps
import valkey_native as valkey


class ValkeyNative(unittest.TestCase):
    def fixture(self, base):
        spec = copy.deepcopy(tools.TOOLS['valkey'])
        for name in spec['recipe']['source_sha256']:
            path = base / 'source' / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(('fixture:' + name).encode())
            spec['recipe']['source_sha256'][name] = hashlib.sha256(path.read_bytes()).hexdigest()
        return spec

    def test_recipe_is_pinned_tls_native_and_has_no_service_start(self):
        recipe = tools.TOOLS['valkey']['recipe']
        self.assertEqual(recipe['pin'], '29173b67508b2de4c0f0ed551f3b47cf19fc3ca8')
        self.assertEqual(recipe['version'], '9.1.3')
        args = recipe['steps'][0]['args']
        self.assertIn('BUILD_TLS=yes', args)
        self.assertIn('MALLOC=libc', args)
        self.assertIn('-j1', args)
        self.assertNotIn('install', args)
        self.assertEqual(tuple(recipe['apt_build_deps']), deps.VALKEY_PACKAGES)
        self.assertNotIn('valkey', recipe['apt_build_deps'])
        for digest in recipe['source_sha256'].values():
            self.assertRegex(digest, r'^[0-9a-f]{64}$')

    def test_source_hash_failure_precedes_any_build_probe(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            spec = self.fixture(base)
            (base / 'source/COPYING').write_bytes(b'changed')
            with patch.object(valkey.common, 'run') as run, patch.object(valkey.common, 'git') as git:
                with self.assertRaisesRegex(ValueError, 'Quellhash'):
                    valkey.prepare(base, spec, {})
                run.assert_not_called()
                git.assert_not_called()

    def test_receipts_only_probe_versions_with_timeout_and_record_scope(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            spec = self.fixture(base)
            with patch.object(valkey.common, 'run', return_value='3.0.0'), \
                    patch.object(valkey.common, 'git', return_value='a' * 40):
                valkey.prepare(base, spec, {})
            for name in ('valkey-server', 'valkey-cli'):
                (base / 'source/src' / name).write_bytes(b'fixture-binary-never-executed')
            result = subprocess.CompletedProcess([], 0, stdout='Valkey v=9.1.3 fixture', stderr='')
            with patch.object(valkey.subprocess, 'run', return_value=result) as run:
                artifacts = valkey.receipts(base, spec, {})
            self.assertEqual(run.call_count, 2)
            for call in run.call_args_list:
                self.assertEqual(call.args[0][-1], '--version')
                self.assertEqual(call.kwargs['timeout'], 30)
            self.assertIn('valkey-sbom.cdx.json', artifacts)
            self.assertEqual(json.loads((base / artifacts[0]).read_text())['allocator'], 'libc')

    def test_wrong_version_does_not_create_receipts(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            (base / 'source/src').mkdir(parents=True)
            result = subprocess.CompletedProcess([], 0, stdout='Valkey v=9.0.0', stderr='')
            with patch.object(valkey.subprocess, 'run', return_value=result):
                with self.assertRaisesRegex(ValueError, 'Versionsprobe'):
                    valkey.receipts(base, tools.TOOLS['valkey'], {})
            self.assertFalse((base / 'valkey-sbom.cdx.json').exists())

    def test_plan_and_missing_status_never_fetch_or_install_dependencies(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {'OPENCLAW_USER_DATA_DIR': directory}), \
                patch.object(tools, 'preflight') as preflight, patch.object(tools.common, 'git') as git, \
                patch.object(deps, 'prepare') as prepare, redirect_stdout(io.StringIO()):
            self.assertEqual(tools.main(['valkey', 'plan', '--install-build-deps']), 0)
            self.assertEqual(tools.main(['valkey', 'status']), 0)
            self.assertEqual(list(Path(directory).iterdir()), [])
            preflight.assert_not_called()
            git.assert_not_called()
            prepare.assert_not_called()

    def test_unit_and_menu_keep_runtime_activation_explicit(self):
        unit = (ROOT / 'config/systemd/openclaw-valkey.service.example').read_text()
        self.assertIn('--port 0', unit)
        self.assertIn('--unixsocketperm 600', unit)
        self.assertIn('StateDirectory=openclaw-valkey', unit)
        menu = (ROOT / 'setup_ultimate.sh').read_text(encoding='utf-8')
        self.assertIn('TOOL_SCRIPT_NAMES["Valkey"]="valkey"', menu)
        for action in ('install', 'update', 'uninstall', 'status', 'doctor', 'check'):
            wrapper = (ROOT / ('scripts/tools/valkey_' + action + '.sh')).read_text()
            self.assertIn('native_github_tools.py" valkey ' + action, wrapper)
            self.assertNotIn('systemctl', wrapper)


if __name__ == '__main__':
    unittest.main()
