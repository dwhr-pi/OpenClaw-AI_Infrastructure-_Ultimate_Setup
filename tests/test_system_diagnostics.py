"""Offline distribution diagnostics; no WSL, packages, secrets or network."""
import importlib.util
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('system_diagnostics_fixture', ROOT / 'scripts/helpers/system_diagnostics.py')
diagnostics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diagnostics)


class SystemDiagnostics(unittest.TestCase):
    def test_ubuntu_and_wsl_are_reported_without_environment_secrets(self):
        release = {'ID': 'ubuntu', 'VERSION_ID': '24.04', 'PRETTY_NAME': 'Ubuntu 24.04.5 LTS', 'UNRELATED': 'do-not-log'}
        with patch.object(diagnostics.platform, 'freedesktop_os_release', return_value=release), \
                patch.object(diagnostics.platform, 'release', return_value='6.6-microsoft-standard-WSL2'), \
                patch.object(diagnostics.Path, 'is_file', return_value=False), \
                patch.object(diagnostics.shutil, 'which', return_value='/usr/bin/fixture'), \
                patch.dict(os.environ, {'OPENAI_API_KEY': 'not-in-report'}):
            result = diagnostics.snapshot()
        self.assertEqual(result['VERSION_ID'], '24.04')
        self.assertEqual(result['WSL'], 'ja')
        self.assertEqual(result['Debian_Familie'], 'ja')
        self.assertNotIn('UNRELATED', result)
        self.assertNotIn('not-in-report', str(result))

    def test_debian_and_dietpi_base_are_distinguished(self):
        for marker in (True, False):
            with patch.object(diagnostics.platform, 'freedesktop_os_release', return_value={
                    'ID': 'debian', 'VERSION_ID': '13', 'PRETTY_NAME': 'Debian GNU/Linux 13'}), \
                    patch.object(diagnostics.Path, 'is_file', return_value=marker):
                result = diagnostics.snapshot()
            self.assertEqual(result['ID'], 'debian')
            self.assertEqual(result['Debian_Familie'], 'ja')
            self.assertEqual(result['DietPi_Marker'], 'vorhanden' if marker else 'nicht erkannt')

    def test_derivatives_and_unknown_systems_are_not_mislabeled_ubuntu(self):
        for release, family in (({'ID': 'linuxmint', 'ID_LIKE': 'ubuntu debian'}, 'ja'), ({'ID': 'fedora'}, 'nein/unbekannt')):
            with patch.object(diagnostics.platform, 'freedesktop_os_release', return_value=release), \
                    patch.object(diagnostics.Path, 'is_file', return_value=False):
                result = diagnostics.snapshot()
            self.assertEqual(result['Debian_Familie'], family)
            self.assertNotEqual(result['ID'], 'ubuntu')

    def test_missing_release_and_tools_are_explicit(self):
        with patch.object(diagnostics.platform, 'freedesktop_os_release', side_effect=OSError('fixture')), \
                patch.object(diagnostics.Path, 'is_file', return_value=False), \
                patch.object(diagnostics.shutil, 'which', return_value=None):
            result = diagnostics.snapshot()
        self.assertEqual(result['ID'], 'unbekannt')
        self.assertEqual(result['apt-get'], 'nicht im PATH')
        self.assertEqual(result['Python_Pfad'], sys.executable)
        self.assertEqual(diagnostics.clean('Ubuntu\n\x1b[31m'), 'Ubuntu??[31m')


if __name__ == '__main__':
    unittest.main()
