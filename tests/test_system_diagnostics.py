"""Offline distribution diagnostics; no WSL, packages, secrets or network."""
import importlib.util
import os
from pathlib import Path
import sys
import stat
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('system_diagnostics_fixture', ROOT / 'scripts/helpers/system_diagnostics.py')
diagnostics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diagnostics)


class SystemDiagnostics(unittest.TestCase):
    def test_gvisor_kernel_check_does_not_require_kvm_or_claim_runtime_success(self):
        with patch.object(diagnostics.platform, 'system', return_value='Linux'), \
                patch.object(diagnostics.platform, 'release', return_value='6.6-microsoft-standard-WSL2'), \
                patch.object(diagnostics.platform, 'machine', return_value='x86_64'), \
                patch.object(diagnostics.os, 'stat', side_effect=FileNotFoundError), \
                patch.object(diagnostics.os, 'access') as access, \
                patch.object(diagnostics.Path, 'exists', return_value=False):
            result = diagnostics.sandbox_snapshot()
        self.assertEqual(result['gVisor_Kernel_ab_5_6'], 'ja')
        self.assertEqual(result['KVM_Geraet'], 'nicht vorhanden')
        self.assertEqual(result['Sandbox_64bit_Architektur'], 'ja')
        self.assertIn('kein Runtime-', result['Sandbox_Pruefumfang'])
        access.assert_not_called()

    def test_kvm_permissions_are_only_metadata_never_opened(self):
        with patch.object(diagnostics.os, 'stat', return_value=SimpleNamespace(st_mode=stat.S_IFCHR | 0o660)), \
                patch.object(diagnostics.os, 'access', return_value=True) as access, \
                patch.object(diagnostics.Path, 'exists', return_value=False), \
                patch('builtins.open', side_effect=AssertionError('No device/file opening')):
            result = diagnostics.sandbox_snapshot()
        self.assertEqual(result['KVM_Geraet'], 'Zeichengeraet')
        self.assertEqual(result['KVM_Lese_Schreibrecht'], 'ja')
        access.assert_called_once_with('/dev/kvm', os.R_OK | os.W_OK)

    def test_old_kernel_or_unreadable_kvm_is_not_assumed_ready(self):
        with patch.object(diagnostics.platform, 'system', return_value='Linux'), \
                patch.object(diagnostics.platform, 'release', return_value='4.4-microsoft'), \
                patch.object(diagnostics.os, 'stat', side_effect=PermissionError), \
                patch.object(diagnostics.os, 'access') as access, \
                patch.object(diagnostics.Path, 'exists', return_value=False):
            result = diagnostics.sandbox_snapshot()
        self.assertEqual(result['gVisor_Kernel_ab_5_6'], 'nein')
        self.assertEqual(result['KVM_Geraet'], 'Metadaten nicht lesbar')
        access.assert_not_called()

    def test_non_linux_or_32bit_is_not_assumed_compatible(self):
        for system, machine in (('Windows', 'AMD64'), ('Linux', 'armv7l')):
            with patch.object(diagnostics.platform, 'system', return_value=system), \
                    patch.object(diagnostics.platform, 'machine', return_value=machine), \
                    patch.object(diagnostics.os, 'stat', side_effect=FileNotFoundError), \
                    patch.object(diagnostics.Path, 'exists', return_value=False):
                result = diagnostics.sandbox_snapshot()
            self.assertEqual(result['Sandbox_64bit_Architektur'], 'nein/unbekannt')

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
