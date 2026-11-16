"""Select existing Python only; no uv, Python download or model execution."""
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts/tools/helpers'))
import gap_native_build as native


class OutlinesPythonSelection(unittest.TestCase):
    def test_falls_back_from_incompatible_dispatcher(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            candidate = base / 'python3.12'
            candidate.write_text('fixture, never executed')

            def version(args, cwd, env):
                self.assertIn('-S', args)
                return json.dumps([3, 12, 8] if Path(args[0]) == candidate else [3, 14, 0])

            with patch.dict(os.environ, {}, clear=True), \
                    patch.object(native.shutil, 'which', side_effect=lambda name: str(candidate) if name == 'python3.12' else None), \
                    patch.object(native, 'probe', side_effect=version), redirect_stdout(io.StringIO()):
                self.assertEqual(native.select_outlines_python(base), str(candidate))

    def test_explicit_override_is_respected_and_secrets_excluded(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            candidate = base / 'custom-python'
            candidate.write_text('fixture, never executed')
            with patch.dict(os.environ, {'OUTLINES_PYTHON_BIN': str(candidate), 'OPENAI_API_KEY': 'fixture'}), \
                    patch.object(native.shutil, 'which') as which, \
                    patch.object(native, 'probe', return_value='[3, 11, 9]') as probe, redirect_stdout(io.StringIO()):
                self.assertEqual(native.select_outlines_python(base), str(candidate))
                which.assert_not_called()
                self.assertNotIn('OPENAI_API_KEY', probe.call_args.args[2])

    def test_incompatible_override_never_falls_back(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            candidate = base / 'python3.14'
            candidate.write_text('fixture, never executed')
            with patch.dict(os.environ, {'OUTLINES_PYTHON_BIN': str(candidate)}), \
                    patch.object(native.shutil, 'which') as which, \
                    patch.object(native, 'probe', return_value='[3, 14, 0]'):
                with self.assertRaisesRegex(ValueError, 'kein Python-Download'):
                    native.select_outlines_python(base)
                which.assert_not_called()

    def test_relative_override_rejected_without_execution(self):
        with patch.dict(os.environ, {'OUTLINES_PYTHON_BIN': './python'}), patch.object(native, 'probe') as probe:
            with self.assertRaisesRegex(ValueError, 'absoluter'):
                native.select_outlines_python(Path('.'))
            probe.assert_not_called()

    def test_missing_compatible_python_precedes_uv_bootstrap(self):
        with patch.object(native.platform, 'system', return_value='Linux'), \
                patch.object(native.os, 'geteuid', return_value=1000, create=True), \
                patch.object(native, 'select_outlines_python', side_effect=ValueError('kein Python')), \
                patch('native_uv.select') as uv:
            with self.assertRaisesRegex(ValueError, 'kein Python'):
                native.preflight('outlines', Path('.'), approved=True)
            uv.assert_not_called()

    def test_espeak_missing_build_tools_gives_actionable_ubuntu_command(self):
        with patch.object(native.platform, 'system', return_value='Linux'), \
                patch.object(native.os, 'geteuid', return_value=1000, create=True), \
                patch.object(native.common, 'executable', side_effect=ValueError('missing')):
            with self.assertRaisesRegex(ValueError, 'cmake build-essential'):
                native.preflight('espeak_ng', Path('.'))

    def test_malformed_and_failed_version_probes_are_not_accepted(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            candidate = base / 'python'
            candidate.write_text('fixture, never executed')
            for value in ('{}', '[3, true, 0]', '[3, 14, 0]', 'invalid', subprocess.TimeoutExpired('fixture', 30)):
                with self.subTest(value=value), patch.dict(os.environ, {'OUTLINES_PYTHON_BIN': str(candidate)}), \
                        patch.object(native, 'probe', side_effect=value if isinstance(value, Exception) else None,
                                     return_value=value):
                    with self.assertRaises(ValueError):
                        native.select_outlines_python(base)


if __name__ == '__main__':
    unittest.main()
