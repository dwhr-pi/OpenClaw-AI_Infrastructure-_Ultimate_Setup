"""Style policy is explicit; no security or link scanner is disabled."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FormattingPolicy(unittest.TestCase):
    def test_markdown_defaults_and_only_justified_overrides(self):
        policy = json.loads((ROOT / '.markdownlint.json').read_text(encoding='utf-8'))
        self.assertEqual(set(policy), {'default', 'MD013', 'MD024'})
        self.assertIs(policy['default'], True)
        self.assertEqual(policy['MD013'], {'line_length': 120, 'code_blocks': False, 'tables': False})
        self.assertEqual(policy['MD024'], {'siblings_only': True})
        prettier = json.loads((ROOT / '.prettierrc.json').read_text(encoding='utf-8'))
        self.assertEqual(prettier['embeddedLanguageFormatting'], 'off')

    def test_shell_formatters_use_the_same_options(self):
        for filename in ('ci.yml', 'repo-health.yml'):
            text = (ROOT / '.github/workflows' / filename).read_text(encoding='utf-8')
            self.assertIn('shfmt -d -i 2 -ci', text)
        editor = (ROOT / '.editorconfig').read_text(encoding='utf-8')
        self.assertIn('indent_size = 2', editor)
        self.assertIn('switch_case_indent = true', editor)

    def test_translation_exception_is_narrow_and_documented(self):
        for language in ('ar', 'de', 'en', 'eo', 'es', 'fr', 'he', 'ja', 'ru', 'zh'):
            text = (ROOT / 'scripts/lang' / (language + '.sh')).read_text(encoding='utf-8')
            self.assertIn('variables are a sourced public interface', text)
            directives = [line for line in text.splitlines() if 'shellcheck disable=' in line]
            self.assertEqual(directives, ['# shellcheck disable=SC2034'])
        global_settings = (ROOT / '.shellcheckrc').read_text(encoding='utf-8')
        self.assertNotIn('disable=', global_settings)


    def test_infrastructure_candidate_scripts_have_one_final_newline(self):
        checked = []
        directory = ROOT / 'scripts/tools'
        paths = [*directory.glob('*_candidate_install.sh'),
                 directory / 'infrastructure_candidate_blocked.sh',
                 directory / 'infrastructure_candidate_status.sh']
        for path in paths:
            text = path.read_text(encoding='utf-8')
            if ('infrastructure_candidate_blocked.sh' not in text and
                    path.name not in ('infrastructure_candidate_blocked.sh', 'infrastructure_candidate_status.sh')):
                continue
            self.assertTrue(text.endswith('\n'), path.name)
            self.assertFalse(text.endswith('\n\n'), path.name)
            checked.append(path.name)
        self.assertGreaterEqual(len(checked), 24)


if __name__ == '__main__':
    unittest.main()
