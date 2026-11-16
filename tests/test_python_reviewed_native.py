"""Offline contracts only; these fixtures are not Linux runtime acceptance."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/tools/helpers'))
import python_reviewed_native as helper


class ReviewedPythonTests(unittest.TestCase):
    def specs(self):
        return json.loads(helper.CANDIDATES.read_text())['tools']

    def test_exact_candidate_contracts(self):
        self.assertEqual({s['id'] for s in self.specs()}, {'phoenix', 'checkov', 'ragas'})
        for spec in self.specs():
            self.assertEqual(helper.contract(spec), spec['recipe'])
            self.assertRegex(spec['recipe']['pin'], '^[a-f0-9]{40}$')
            for digest in spec['recipe']['source_sha256'].values():
                self.assertRegex(digest, '^[a-f0-9]{64}$')
            changed = copy.deepcopy(spec)
            changed['recipe']['pin'] = '0' * 40
            with self.assertRaises(ValueError):
                helper.contract(changed)

    def test_environment_drops_credentials_and_python_injection(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {'OPENAI_API_KEY': 'not-a-key', 'AWS_PROFILE': 'not-read',
                                         'PYTHONPATH': '/not-read', 'UV_INDEX_URL': 'https://not-used'}, clear=False):
                env = helper.environment(Path(directory))
            for key in ('OPENAI_API_KEY', 'AWS_PROFILE', 'PYTHONPATH', 'UV_INDEX_URL'):
                self.assertNotIn(key, env)
            self.assertEqual(env['UV_PYTHON_DOWNLOADS'], 'never')
            self.assertEqual(env['RAGAS_DO_NOT_TRACK'], 'true')

    def test_source_mismatch_prevents_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / 'pyproject.toml').write_bytes(b'fixture')
            recipe = {'pin': 'a' * 40, 'repo': 'owner/repo',
                      'source_sha256': {'pyproject.toml': hashlib.sha256(b'other').hexdigest()}}
            with patch.object(helper.common, 'git', side_effect=[recipe['pin'], 'https://github.com/owner/repo.git']):
                with self.assertRaisesRegex(ValueError, 'Quellhash'):
                    helper.verify_source(source, recipe)

    def test_incomplete_wheels_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            wheel = Path(directory) / 'fixture.whl'
            with zipfile.ZipFile(wheel, 'w') as archive:
                archive.writestr('placeholder', 'not-a-runtime')
            for spec in self.specs():
                with self.assertRaises(ValueError):
                    helper.inspect_wheel(wheel, spec['recipe'])

    def test_probe_is_bounded_and_never_cli_execution(self):
        result = subprocess.CompletedProcess([], 0, stdout='ok')
        with patch.object(helper.subprocess, 'run', return_value=result) as run:
            self.assertEqual(helper.execute(['/python', '-I', '-c', 'pass'], ROOT, {}, 45), 'ok')
        self.assertEqual(run.call_args.kwargs['timeout'], 45)
        self.assertTrue(run.call_args.kwargs['check'])
        for spec in self.specs():
            script = helper.probe_script(spec['recipe'])
            compile(script, '<probe>', 'exec')
            self.assertIn('socket.socket.bind = denied', script)
            self.assertIn('subprocess.Popen = denied', script)
            self.assertNotIn('launch_app(', script)
            self.assertNotIn('evaluate(', script)

    def test_explicit_unsupported_python_never_downloads(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {'NATIVE_SOURCE_PYTHON_BIN': '/explicit-python'}):
                with patch.object(helper, 'execute', side_effect=subprocess.CalledProcessError(1, 'probe')):
                    with patch.object(helper.native_uv, 'select') as uv:
                        with self.assertRaisesRegex(ValueError, 'Explizites'):
                            helper.select_python(Path(directory), self.specs()[0], approved=True)
                        uv.assert_not_called()

    def test_missing_python_requires_explicit_consent(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {}, clear=True), patch.object(helper.shutil, 'which', return_value=None):
                with patch.object(helper, 'execute', side_effect=subprocess.CalledProcessError(1, 'probe')):
                    with self.assertRaisesRegex(ValueError, 'freigeben'):
                        helper.select_python(Path(directory), self.specs()[0])

    def test_build_rejects_wrong_source_layout(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, 'Buildquelle'):
                helper.build(Path(directory) / 'elsewhere', Path(directory), self.specs()[0], {})


if __name__ == '__main__':
    unittest.main()
