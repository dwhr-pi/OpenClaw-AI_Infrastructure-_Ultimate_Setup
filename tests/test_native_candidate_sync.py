"""Offline synchronization contracts; never downloads or installs a tool."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('candidate_sync', ROOT / 'scripts/quality/sync_native_candidates.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class NativeCandidateSyncTests(unittest.TestCase):
    def test_allowlist_covers_every_remaining_requested_tool_once(self):
        self.assertEqual(len(sync.ALLOWED), 20)
        self.assertEqual(len(set(sync.ALLOWED.values())), 20)
        self.assertNotIn('valkey', sync.ALLOWED)
        self.assertNotIn('kube_bench', sync.ALLOWED)

    def test_unknown_fragment_cannot_change_catalog(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            (path / 'bad.json').write_text(json.dumps({'tools': [{'id': 'foreign'}]}))
            with patch.object(sync, 'FRAGMENTS', path):
                with self.assertRaisesRegex(ValueError, 'Unknown/duplicate'):
                    sync.entries()

    def test_render_is_read_only_and_wrappers_use_native_lifecycle(self):
        items = sync.entries()
        self.assertTrue(items)
        outputs = sync.render(items)
        setup = outputs[ROOT / 'setup_ultimate.sh']
        for item in items:
            key, name = item['id'], item['tool_key']
            self.assertIn('TOOL_SCRIPT_NAMES["' + name + '"]="' + key + '"', setup)
            for action in sync.ACTIONS:
                text = outputs[ROOT / ('scripts/tools/' + key + '_' + action + '.sh')]
                self.assertIn('native_github_tools.py" ' + key + ' ' + action, text)
                self.assertNotIn('blocked.sh', text)
        self.assertEqual(len({item['id'] for item in items}), len(items))


if __name__ == '__main__':
    unittest.main()
