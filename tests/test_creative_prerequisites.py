"""Offline prerequisite integration; no package manager, download or runtime."""
from contextlib import redirect_stdout
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/tools/helpers'))
import native_build_deps as deps
import gap_tools as tools


class CreativePrerequisites(unittest.TestCase):
    def test_missing_packages_need_consent_and_install_only_allowlist(self):
        for key, packages in (('espeak_ng', deps.ESPEAK_PACKAGES), ('outlines', deps.OUTLINES_PACKAGES),
                              ('valkey', deps.VALKEY_PACKAGES)):
            spec = {'id': key, 'recipe': {'apt_build_deps': list(packages)}}
            state = {'installed': False}

            def run(args, cwd, env):
                self.assertNotIn('OPENAI_API_KEY', env)
                if 'install' in args:
                    self.assertEqual(args[-len(packages):], list(packages))
                    self.assertIn('--no-remove', args)
                    state['installed'] = True

            with self.subTest(key=key), patch.object(deps, 'ubuntu_release', return_value=True), \
                    patch.object(deps.shutil, 'which', return_value='fixture'), \
                    patch.object(deps, 'installed', side_effect=lambda p: state['installed']), \
                    patch.object(deps.sys, 'stdin', Mock(isatty=Mock(return_value=False))), \
                    patch.object(deps.os, 'geteuid', return_value=1000, create=True), \
                    patch.object(deps.common, 'run', side_effect=run) as calls, redirect_stdout(io.StringIO()):
                with self.assertRaisesRegex(ValueError, 'Zustimmung'):
                    deps.prepare(spec)
                calls.assert_not_called()
                deps.prepare(spec, approved=True)
                self.assertEqual(calls.call_count, 2)
                deps.prepare(spec, approved=True)
                self.assertEqual(calls.call_count, 2)

    def test_unapproved_package_lists_rejected(self):
        for key in ('outlines', 'espeak_ng', 'valkey'):
            with self.subTest(key=key), patch.object(deps.common, 'run') as run:
                with self.assertRaisesRegex(ValueError, 'Nicht freigegebene'):
                    deps.prepare({'id': key, 'recipe': {'apt_build_deps': ['untrusted']}}, approved=True)
                run.assert_not_called()

    def test_unsupported_os_and_package_failure_stop(self):
        spec = {'id': 'espeak_ng', 'recipe': {'apt_build_deps': list(deps.ESPEAK_PACKAGES)}}
        with patch.object(deps, 'ubuntu_release', return_value=False), patch.object(deps, 'debian_family', return_value=False), patch.object(deps.common, 'run') as run:
            with self.assertRaisesRegex(ValueError, 'Keine Systemaenderung'):
                deps.prepare(spec, approved=True)
            run.assert_not_called()
        with patch.object(deps, 'ubuntu_release', return_value=True), \
                patch.object(deps.shutil, 'which', return_value='fixture'), \
                patch.object(deps, 'installed', return_value=False), \
                patch.object(deps.os, 'geteuid', return_value=1000, create=True), \
                patch.object(deps.common, 'run', side_effect=subprocess.CalledProcessError(100, 'fixture')), \
                redirect_stdout(io.StringIO()):
            with self.assertRaises(subprocess.CalledProcessError):
                deps.prepare(spec, approved=True)

    def test_espeak_plan_accepts_flag_without_apt(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch.dict(os.environ, {'OPENCLAW_USER_DATA_DIR': directory}), \
                patch.object(deps, 'prepare') as prepare, redirect_stdout(io.StringIO()):
            self.assertEqual(tools.main(['espeak_ng', 'plan', '--install-build-deps']), 0)
            self.assertEqual(list(Path(directory).iterdir()), [])
            prepare.assert_not_called()

    def test_setup_consent_and_songsage_guard_precede_transaction(self):
        text = (ROOT / 'setup_ultimate.sh').read_text(encoding='utf-8')
        dispatcher = text.split('run_tool_script() {', 1)[1].split('remove_tool_from_autostart_script()', 1)[0]
        self.assertIn('^(Outlines|eSpeak_NG|SongRec|Valkey|Kube_Bench)$', dispatcher)
        self.assertIn('tool_args+=(--install-build-deps)', dispatcher)
        self.assertIn('--defaultno', dispatcher)
        install = text.split('install_tool() {', 1)[1].split('uninstall_tool() {', 1)[0]
        self.assertLess(install.index('SongSage'), install.index('begin_operation_measurement'))
        self.assertIn('Kein Installationslauf gestartet', install)

    def test_menu_forwards_consent_only_for_approved_mutations(self):
        bash = shutil.which('bash')
        if os.name == 'nt' and Path('C:/Program Files/Git/bin/bash.exe').is_file():
            bash = 'C:/Program Files/Git/bin/bash.exe'
        if not bash:
            self.skipTest('Bash not available for offline menu fixture')
        text = (ROOT / 'setup_ultimate.sh').read_text(encoding='utf-8')
        dispatcher = 'run_tool_script() {' + text.split('run_tool_script() {', 1)[1].split('remove_tool_from_autostart_script()', 1)[0]
        stubs = '''
declare -A TOOL_SCRIPT_NAMES=([Outlines]=outlines [eSpeak_NG]=espeak_ng [SongRec]=songrec [Valkey]=valkey [Kube_Bench]=kube_bench)
INSTALL_DIR=/fixture
validate_tool_source_policy() { return 0; }
dialog() { return "$DIALOG_RESULT"; }
run_bash_script() { printf '%s\\n' "$@"; }
'''
        env = {k: v for k, v in os.environ.items() if k.upper() in ('PATH', 'SYSTEMROOT', 'TEMP', 'TMP')}
        for tool in ('Outlines', 'eSpeak_NG', 'SongRec', 'Valkey', 'Kube_Bench'):
            for action, answer in (('install', 0), ('install', 1), ('update', 0), ('doctor', 0)):
                command = stubs + dispatcher + '\nDIALOG_RESULT=' + str(answer) + '\nrun_tool_script ' + tool + ' ' + action
                result = subprocess.run([bash, '--noprofile', '--norc', '-c', command],
                                        env=env, capture_output=True, text=True, timeout=10, check=True)
                self.assertEqual('--install-build-deps' in result.stdout,
                                 answer == 0 and action in ('install', 'update'))

    def test_planned_infrastructure_is_rejected_before_installer_or_log(self):
        bash = 'C:/Program Files/Git/bin/bash.exe' if os.name == 'nt' else shutil.which('bash')
        if not bash or (os.name == 'nt' and not Path(bash).is_file()):
            self.skipTest('Bash not available for offline menu fixture')
        text = (ROOT / 'setup_ultimate.sh').read_text(encoding='utf-8')
        install = 'install_tool() {' + text.split('install_tool() {', 1)[1].split('\nuninstall_tool() {', 1)[0]
        stubs = '''
declare -A TOOLS=([cert-manager]='GEPLANT / NICHT INSTALLIERBAR: fixture' [External_DNS]='GEPLANT / NICHT INSTALLIERBAR: fixture' [Kyverno]='GEPLANT / NICHT INSTALLIERBAR: fixture' [gVisor]='GEPLANT / NICHT INSTALLIERBAR: fixture' [Kata_Containers]='GEPLANT / NICHT INSTALLIERBAR: fixture' [Firecracker]='GEPLANT / NICHT INSTALLIERBAR: fixture')
INSTALL_DIR=/fixture
python3() { printf 'Sandbox_Pruefumfang=fixture-only\\n'; }
LAST_OPERATION_LOG_FILE=OLD_LOG
ACTIVE_OPERATION_LOG_FILE=OLD_LOG
dialog() { printf '%s\\n' "$@"; }
begin_operation_measurement() { echo UNEXPECTED-LOG; exit 90; }
run_tool_script() { echo UNEXPECTED-INSTALLER; exit 90; }
'''
        env = {k: v for k, v in os.environ.items() if k.upper() in ('PATH', 'SYSTEMROOT', 'TEMP', 'TMP')}
        for tool in ('cert-manager', 'External_DNS', 'Kyverno', 'gVisor', 'Kata_Containers', 'Firecracker'):
            with tempfile.TemporaryDirectory() as directory:
                script = Path(directory) / 'menu-fixture.sh'
                call = ('\nrc=0; install_tool ' + tool + ' || rc=$?\n'
                        '[[ -z "$LAST_OPERATION_LOG_FILE" && -z "$ACTIVE_OPERATION_LOG_FILE" ]] || exit 92\nexit "$rc"\n')
                script.write_text(stubs + install + call, encoding='utf-8', newline='\n')
                result = subprocess.run([bash, '--noprofile', '--norc', script.as_posix()],
                                        env=env, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 3, result.stderr)
            self.assertIn('kein Installer', result.stdout)
            self.assertNotIn('UNEXPECTED-', result.stdout)
            if tool in ('gVisor', 'Kata_Containers', 'Firecracker'):
                self.assertIn('Sandbox_Pruefumfang=fixture-only', result.stdout)


if __name__ == '__main__':
    unittest.main()
