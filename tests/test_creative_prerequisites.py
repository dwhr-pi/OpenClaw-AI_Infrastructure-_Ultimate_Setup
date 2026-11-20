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
        self.assertIn('^(Outlines|eSpeak_NG|SongRec|Valkey|Kube_Bench|', dispatcher)
        for key in ('cert-manager', 'External_DNS', 'KEDA', 'Arize_Phoenix', 'Vaultwarden', 'Argo_Workflows'):
            self.assertIn('|' + key, dispatcher)
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
                result = subprocess.run([bash, '--noprofile', '--norc', '-s'], input=command,
                                        env=env, capture_output=True, text=True, timeout=10, check=True)
                self.assertEqual('--install-build-deps' in result.stdout,
                                 answer == 0 and action in ('install', 'update'))

    def prerequisite_dialog(self, language, answer, override=''):
        bash = 'C:/Program Files/Git/bin/bash.exe' if os.name == 'nt' else shutil.which('bash')
        if not bash or (os.name == 'nt' and not Path(bash).is_file()):
            self.skipTest('Bash not available for offline language fixture')
        text = (ROOT / 'setup_ultimate.sh').read_text(encoding='utf-8')
        dispatcher = 'run_tool_script() {' + text.split('run_tool_script() {', 1)[1].split('remove_tool_from_autostart_script()', 1)[0]
        stubs = '''
declare -A TOOL_SCRIPT_NAMES=([Arize_Phoenix]=phoenix)
INSTALL_DIR=/fixture
validate_tool_source_policy() { return 0; }
dialog() { printf 'DIALOG_ARG:%s\\n' "$@"; return "$ANSWER"; }
run_bash_script() { printf 'RUN_ARG:%s\\n' "$@"; }
source "scripts/lang/$1.sh"
'''
        env = {k: v for k, v in os.environ.items() if k.upper() in ('PATH', 'SYSTEMROOT', 'TEMP', 'TMP')}
        env.update(LANG='C', LC_ALL='C')
        command = stubs + dispatcher + '\n' + override + '\nANSWER=' + str(answer) + '\nrun_tool_script Arize_Phoenix install'
        result = subprocess.run([bash, '--noprofile', '--norc', '-s', '--', language], input=command,
                                cwd=ROOT, env=env, capture_output=True, encoding='utf-8', timeout=15, check=True)
        return result.stdout.splitlines()

    def batch_prerequisites(self, choice='all', menu_rc=0, queue='Outlines eSpeak_NG Other', after=''):
        bash = 'C:/Program Files/Git/bin/bash.exe' if os.name == 'nt' else shutil.which('bash')
        if not bash or (os.name == 'nt' and not Path(bash).is_file()):
            self.skipTest('Bash not available for offline batch fixture')
        text = (ROOT / 'setup_ultimate.sh').read_text(encoding='utf-8')
        batch = ('select_tool_batch_build_deps_policy() {'
                 + text.split('select_tool_batch_build_deps_policy() {', 1)[1].split('is_base_install_ready()', 1)[0])
        dispatcher = ('run_tool_script() {'
                      + text.split('run_tool_script() {', 1)[1].split('remove_tool_from_autostart_script()', 1)[0])
        stubs = '''
declare -A TOOL_SCRIPT_NAMES=([Outlines]=outlines [eSpeak_NG]=espeak_ng [Other]=other)
INSTALL_DIR=/fixture
TOOL_BATCH_BUILD_DEPS_POLICY=all
validate_tool_source_policy() { return 0; }
show_tool_action_plan_intro() { :; }
format_tool_queue_preview() { :; }
confirm_tool_batch_step() { return 0; }
uninstall_tool() { printf 'UNINSTALL:%s\\n' "$1"; }
install_tool() { run_tool_script "$1" install; }
run_bash_script() { printf 'RUN_ARG:%s\\n' "$@"; }
dialog() {
  case " $* " in
    *" --menu "*)
      printf 'MENU_ARG:%s\\n' "$@" >&2
      printf '%s\\n' "$BATCH_CHOICE"
      return "$MENU_RC"
      ;;
    *) printf 'TOOL_QUESTION\\n'; return 1 ;;
  esac
}
'''
        env = {k: v for k, v in os.environ.items() if k.upper() in ('PATH', 'SYSTEMROOT', 'TEMP', 'TMP')}
        env.update(BATCH_CHOICE=choice, MENU_RC=str(menu_rc))
        command = (stubs + batch + dispatcher + '\nuninstalls=(Old); installs=(' + queue + ')\n'
                   'rc=0; run_ordered_tool_actions fixture uninstalls installs || rc=$?\n'
                   'printf "BATCH_RC:%s\\n" "$rc"\n' + after)
        return subprocess.run([bash, '--noprofile', '--norc', '-s'], input=command, cwd=ROOT,
                              env=env, capture_output=True, encoding='utf-8', timeout=15, check=True)

    def test_batch_all_approves_only_supported_tools_without_repeated_dialogs(self):
        result = self.batch_prerequisites()
        self.assertEqual(result.stdout.count('RUN_ARG:--install-build-deps'), 2)
        self.assertNotIn('TOOL_QUESTION', result.stdout)
        self.assertIn('UNINSTALL:Old', result.stdout)
        self.assertIn('RUN_ARG:/fixture/scripts/tools/other_install.sh', result.stdout)
        self.assertIn('MENU_ARG:--stdout', result.stderr)
        self.assertIn('MENU_ARG:--default-item\nMENU_ARG:ask', result.stderr)
        self.assertEqual(result.stderr.count('MENU_ARG:--menu'), 1)
        self.assertIn('BATCH_RC:0', result.stdout)

    def test_batch_ask_keeps_individual_default_no_dialogs(self):
        result = self.batch_prerequisites(choice='ask')
        self.assertEqual(result.stdout.count('TOOL_QUESTION'), 2)
        self.assertNotIn('RUN_ARG:--install-build-deps', result.stdout)

    def test_batch_cancel_or_invalid_choice_prevents_uninstall_and_install(self):
        for choice, status in (('all', 1), ('all', 255), ('unknown', 0), ('', 0)):
            with self.subTest(choice=choice, status=status):
                result = self.batch_prerequisites(choice=choice, menu_rc=status)
                self.assertIn('BATCH_RC:1', result.stdout)
                self.assertNotIn('UNINSTALL:', result.stdout)
                self.assertNotIn('RUN_ARG:', result.stdout)

    def test_batch_consent_never_leaks_to_single_tool_or_readonly_action(self):
        result = self.batch_prerequisites(after=('run_tool_script Outlines install\n'
                                                'run_tool_script Outlines doctor\n'))
        self.assertEqual(result.stdout.count('RUN_ARG:--install-build-deps'), 2)
        self.assertEqual(result.stdout.count('TOOL_QUESTION'), 1)
        self.assertIn('RUN_ARG:/fixture/scripts/tools/outlines_doctor.sh', result.stdout)
        for queue in ('Outlines', ''):
            with self.subTest(queue=queue):
                result = self.batch_prerequisites(queue=queue)
                self.assertNotIn('MENU_ARG:', result.stderr)
                self.assertNotIn('RUN_ARG:--install-build-deps', result.stdout)

    def test_next_batch_requires_its_own_choice(self):
        result = self.batch_prerequisites(after=('BATCH_CHOICE=ask\n'
                                                'run_ordered_tool_actions next uninstalls installs\n'))
        self.assertEqual(result.stderr.count('MENU_ARG:--menu'), 2)
        self.assertEqual(result.stdout.count('RUN_ARG:--install-build-deps'), 2)
        self.assertEqual(result.stdout.count('TOOL_QUESTION'), 2)

    def test_prerequisite_buttons_follow_all_setup_languages_not_system_locale(self):
        labels = {'de': ('Ja', 'Nein'), 'en': ('Yes', 'No'), 'fr': ('Oui', 'Non'),
                  'es': ('S\u00ed', 'No'), 'eo': ('Jes', 'Ne'), 'zh': ('\u662f', '\u5426'),
                  'ja': ('\u306f\u3044', '\u3044\u3044\u3048'), 'ru': ('\u0414\u0430', '\u041d\u0435\u0442'),
                  'ar': ('\u0646\u0639\u0645', '\u0644\u0627'), 'he': ('\u05db\u05df', '\u05dc\u05d0')}
        for language, (yes, no) in labels.items():
            for answer in (0, 1, 255):
                with self.subTest(language=language, answer=answer):
                    lines = self.prerequisite_dialog(language, answer)
                    self.assertEqual(lines[lines.index('DIALOG_ARG:--yes-label') + 1], 'DIALOG_ARG:' + yes)
                    self.assertEqual(lines[lines.index('DIALOG_ARG:--no-label') + 1], 'DIALOG_ARG:' + no)
                    self.assertIn('DIALOG_ARG:--defaultno', lines)
                    self.assertEqual('RUN_ARG:--install-build-deps' in lines, answer == 0)

    def test_prerequisite_buttons_preserve_overrides_and_missing_key_fallback(self):
        for override, labels in (("TXT_YES_LABEL='Custom accept'; TXT_NO_LABEL='Custom decline'",
                                  ('Custom accept', 'Custom decline')),
                                 ('unset TXT_YES_LABEL TXT_NO_LABEL', ('Ja', 'Nein'))):
            with self.subTest(override=override):
                lines = self.prerequisite_dialog('en', 1, override)
                self.assertEqual(lines[lines.index('DIALOG_ARG:--yes-label') + 1], 'DIALOG_ARG:' + labels[0])
                self.assertEqual(lines[lines.index('DIALOG_ARG:--no-label') + 1], 'DIALOG_ARG:' + labels[1])
                self.assertNotIn('RUN_ARG:--install-build-deps', lines)

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
