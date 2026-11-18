"""Render isolated UI functions only; never source or run the installer."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASH = 'C:/Program Files/Git/bin/bash.exe' if os.name == 'nt' else shutil.which('bash')
GREEN = '\033[0;32m'
NC = '\033[0m'


@unittest.skipUnless(BASH and Path(BASH).is_file(), 'Existing Bash required; no WSL fallback')
class ToolActionListTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / 'setup_ultimate.sh').read_text(encoding='utf-8')
        cls.function = re.search(r'^format_tool_action_list\(\) \{\n.*?^\}',
                                 cls.source, re.M | re.S).group(0)

    def render(self, *items):
        script = self.function + '\nGREEN="\\033[0;32m"; NC="\\033[0m"\nformat_tool_action_list "$@"'
        env = dict(os.environ, BASH_ENV='', ENV='')
        result = subprocess.run([BASH, '--noprofile', '--norc', '-c', script, 'fixture', *items],
                                cwd=ROOT, env=env, capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, '')
        return result.stdout

    def test_zero_one_two_three_and_four_tools(self):
        for items, expected in (([], '(keine)'), (['Kube_Bench'], 'Kube_Bench'),
                                (['Kube_Bench', 'Testssl'], 'Kube_Bench und Testssl'),
                                (['Kube_Bench', 'Testssl', 'Checkov'], 'Kube_Bench, Testssl und Checkov'),
                                (['A', 'B', 'C', 'D'], 'A, B, C und D')):
            with self.subTest(items=items):
                plain = re.sub(r'\x1b\[[0-9;]*m', '', self.render(*items))
                self.assertEqual(plain, expected)

    def test_only_names_are_colored_not_punctuation_or_conjunction(self):
        self.assertEqual(self.render('Kube_Bench', 'Testssl', 'Checkov'),
                         GREEN + 'Kube_Bench' + NC + ', ' + GREEN + 'Testssl' + NC
                         + ' und ' + GREEN + 'Checkov' + NC)
        self.assertEqual(self.render(), '(keine)')

    def test_names_are_literal_printf_data(self):
        name = r'Tool %s \n mit Leerzeichen'
        self.assertEqual(self.render(name), GREEN + name + NC)

    def test_both_action_rows_use_the_formatter_without_changing_order(self):
        intro = re.search(r'^show_tool_action_plan_intro\(\) \{\n.*?^\}',
                          self.source, re.M | re.S).group(0)
        self.assertIn('format_tool_action_list "${uninstall_array[@]}"', intro)
        self.assertIn('format_tool_action_list "${install_array[@]}"', intro)
        self.assertLess(intro.index('1. Deinstallationen zuerst:'), intro.index('2. Installationen danach:'))


if __name__ == '__main__':
    unittest.main()
