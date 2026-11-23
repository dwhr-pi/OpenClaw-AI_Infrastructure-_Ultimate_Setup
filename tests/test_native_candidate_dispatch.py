"""Offline native installer dispatch boundaries; no upstream build acceptance."""
from contextlib import redirect_stdout
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/tools/helpers'))
import native_github_tools as engine


class CandidateDispatchTests(unittest.TestCase):
    def test_every_requested_adapter_is_wired_to_exact_reviewed_recipe(self):
        entries = []
        for path in sorted((ROOT / 'config/native-candidates').glob('*.json')):
            entries += json.loads(path.read_text(encoding='utf-8'))['tools']
        self.assertEqual(len(entries), 21)
        self.assertEqual(sum(spec['id'] == 'openjarvis' for spec in entries), 1)
        self.assertEqual({s['id'] for s in entries}, set(engine.CANDIDATE_BACKENDS))
        for spec in entries:
            self.assertEqual(engine.TOOLS[spec['id']], spec)
            module = engine.candidate_backend(spec)
            self.assertTrue(callable(module.preflight))
            self.assertTrue(callable(module.build))
            if hasattr(module, 'contract'):
                module.contract(spec)
            elif hasattr(module, 'recipe'):
                module.recipe(spec)

    def test_all_backends_reject_windows_before_packages_or_network(self):
        for key in engine.CANDIDATE_BACKENDS:
            spec = engine.TOOLS[key]
            module = engine.candidate_backend(spec)
            with self.subTest(tool=key), tempfile.TemporaryDirectory() as temp, \
                    patch.object(module.platform, 'system', return_value='Windows'), \
                    patch.object(engine.common, 'run', side_effect=AssertionError('no command')):
                with self.assertRaises(ValueError):
                    module.preflight(Path(temp), spec, approved=True)

    def test_unreviewed_adapter_path_is_never_imported(self):
        spec = copy.deepcopy(engine.TOOLS['keda'])
        spec['id'] = 'foreign'
        spec['recipe']['candidate_module'] = '../../foreign.py'
        with patch.object(engine.importlib, 'import_module') as load:
            with self.assertRaises(ValueError):
                engine.candidate_backend(spec)
        load.assert_not_called()

    def test_generic_resources_fail_before_adapter_or_download(self):
        with tempfile.TemporaryDirectory() as temp, \
                patch.object(engine.platform, 'system', return_value='Linux'), \
                patch.object(engine.common, 'reserve', side_effect=ValueError('disk budget')), \
                patch.object(engine, 'candidate_backend') as backend:
            with self.assertRaisesRegex(ValueError, 'disk budget'):
                engine.preflight(Path(temp), engine.TOOLS['gvisor'], True)
        backend.assert_not_called()

    def test_adapter_needs_real_owned_artifacts_not_a_clone_or_success_message(self):
        for names in ([], ['missing'], ['../outside'], ['/absolute'], ['a', 'a']):
            with self.subTest(artifacts=names), tempfile.TemporaryDirectory() as temp:
                prefix = Path(temp)
                module = SimpleNamespace(build=Mock(return_value=names))
                with patch.object(engine, 'candidate_backend', return_value=module):
                    with self.assertRaises((ValueError, OSError)):
                        engine.build(prefix, engine.TOOLS['keda'])
                self.assertFalse((prefix / 'build-ready.json').exists())

    def test_doctor_does_not_turn_build_receipts_into_runtime_acceptance(self):
        module = SimpleNamespace()
        with tempfile.TemporaryDirectory() as temp, \
                patch.dict(engine.os.environ, {'OPENCLAW_USER_DATA_DIR': temp}), \
                patch.object(engine, 'validate', return_value={}), \
                patch.object(engine, 'candidate_backend', return_value=module), redirect_stdout(io.StringIO()) as output:
            self.assertEqual(engine.main(['keda', 'doctor']), 3)
        data = json.loads(output.getvalue())
        self.assertTrue(data['installed'])
        self.assertFalse(data['application_tested'])
        self.assertFalse(data['activation_performed'])


if __name__ == '__main__':
    unittest.main()
