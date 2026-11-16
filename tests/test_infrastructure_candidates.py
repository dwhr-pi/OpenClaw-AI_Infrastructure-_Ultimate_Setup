"""Offline catalog and fail-closed checks; no downloads, host probes or services."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('candidate_order', ROOT / 'scripts/helpers/tool_menu_order.py')
ordering = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ordering)
BASH = 'C:/Program Files/Git/bin/bash.exe' if sys.platform == 'win32' else shutil.which('bash')


class CandidateCatalog(unittest.TestCase):
    def test_unique_registry_and_complete_trailing_block(self):
        rows = json.loads((ROOT / 'config/tools.yml').read_text(encoding='utf-8'))['tools']
        self.assertEqual(len(rows), len({row['id'] for row in rows}))
        normalized = lambda value: value.lower().replace('-', '_').replace(' ', '_')
        for name in ordering.AFTER_XERJ:
            matches = [row for row in rows if normalized(row['name']) == normalized(name)]
            self.assertEqual(len(matches), 1, name)
            row = matches[0]
            if row['id'] == 'valkey':
                self.assertEqual(row['status'], 'experimental')
                self.assertEqual(row['install_mode'], 'github-native-build')
                self.assertEqual(row['status_script'], 'scripts/tools/valkey_status.sh')
                continue
            self.assertEqual(row['status'], 'planned')
            self.assertFalse(row['auto_install'])
            self.assertEqual(row['status_script'], 'scripts/tools/infrastructure_candidate_status.sh')
            for action in ('install', 'update', 'uninstall', 'doctor', 'status'):
                self.assertTrue((ROOT / row[action + '_script']).is_file())

    def test_tail_is_after_xerj_and_stable_without_duplicates(self):
        keys = ['Ollama', 'TruffleHog', 'Zotero', 'XERJ', 'Other_Future'] + [
            key for key in ordering.AFTER_XERJ if key != 'TruffleHog']
        result = ordering.ordered(keys, {'Zotero', 'TruffleHog'})
        self.assertEqual(result[-23:], ['XERJ'] + ordering.AFTER_XERJ)
        self.assertCountEqual(result, keys)
        self.assertEqual(ordering.ordered(result, {'Zotero', 'TruffleHog'}), result)

    @unittest.skipUnless(BASH and Path(BASH).is_file(), 'Native Bash unavailable')
    def test_blocked_actions_and_status_do_not_touch_user_data(self):
        env = {key: value for key, value in os.environ.items()
               if key not in ('BASH_ENV', 'ENV', 'SHELLOPTS', 'BASHOPTS')}
        with tempfile.TemporaryDirectory() as directory:
            env.update(HOME=directory, OPENCLAW_USER_DATA_DIR=directory)
            sentinel = Path(directory) / 'keep.txt'
            sentinel.write_text('keep', encoding='utf-8')
            scripts = list((ROOT / 'scripts/tools').glob('*_candidate_install.sh'))
            scripts = [path for path in scripts if 'infrastructure_candidate_blocked.sh' in path.read_text()]
            self.assertEqual(len(scripts), 21)
            for path in scripts:
                result = subprocess.run([BASH, '--noprofile', '--norc', path.as_posix()],
                                        env=env, capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 3, path.name)
                self.assertIn('NICHT INSTALLIERBAR', result.stdout)
            blocked = ROOT / 'scripts/tools/infrastructure_candidate_blocked.sh'
            result = subprocess.run([BASH, '--noprofile', '--norc', blocked.as_posix(), '--dry-run'],
                                    env=env, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0)
            status = ROOT / 'scripts/tools/infrastructure_candidate_status.sh'
            result = subprocess.run([BASH, '--noprofile', '--norc', status.as_posix()],
                                    env=env, capture_output=True, text=True, timeout=15, check=True)
            data = json.loads(result.stdout)
            self.assertIsNone(data['installed'])
            self.assertFalse(data['host_inspected'])
            self.assertFalse(data['performed'])
            self.assertEqual(sentinel.read_text(), 'keep')
            self.assertEqual(list(Path(directory).iterdir()), [sentinel])


if __name__ == '__main__':
    unittest.main()
