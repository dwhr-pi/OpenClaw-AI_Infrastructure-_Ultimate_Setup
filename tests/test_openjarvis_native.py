"""Offline OpenJarvis contracts; no upstream code, installer, service or model runs."""
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/tools/helpers'))
import native_github_tools as native
import python_reviewed_native as python


class OpenJarvisNative(unittest.TestCase):
    def spec(self):
        return native.TOOLS['openjarvis']

    def test_exact_source_website_and_independent_identity(self):
        spec = self.spec()
        self.assertEqual(spec['tool_key'], 'OpenJarvis')
        self.assertEqual(spec['repo'], 'open-jarvis/OpenJarvis')
        self.assertEqual(spec['website'], 'https://openjarvis.stanford.edu/')
        self.assertEqual(spec['license'], 'Apache-2.0')
        self.assertEqual(spec['recipe']['pin'], 'a9e59e8770f92dd8046c2e5fcc1246eef51bb96a')
        self.assertEqual(spec['recipe']['version'], '0.0.0+openclaw.a9e59e8')
        self.assertEqual(python.contract(spec), spec['recipe'])
        self.assertIs(native.candidate_backend(spec), python)
        self.assertEqual(set(spec['recipe']['source_sha256']), {
            'README.md', 'LICENSE', 'pyproject.toml',
            'src/openjarvis/__init__.py', 'src/openjarvis/cli/__init__.py'})
        registry = json.loads((ROOT / 'config/tools.yml').read_text(encoding='utf-8'))['tools']
        row, = [r for r in registry if r['id'] == 'openjarvis']
        self.assertEqual(row['website'], spec['website'])
        self.assertEqual(row['source_commit'], spec['recipe']['pin'])
        self.assertFalse(row['auto_install'])
        self.assertEqual(row['ports'], [])
        self.assertNotEqual(row['id'], 'hermes_agent_jarvis')

    def test_lifecycle_wrappers_and_menu_include_prerequisite_consent(self):
        for action in ('install', 'update', 'status', 'check', 'doctor', 'uninstall'):
            text = (ROOT / ('scripts/tools/openjarvis_' + action + '.sh')).read_text(encoding='utf-8')
            self.assertIn('native_github_tools.py" openjarvis ' + action + ' "$@"', text)
            self.assertNotIn('quickstart.sh', text)
        setup = (ROOT / 'setup_ultimate.sh').read_text(encoding='utf-8')
        self.assertIn('TOOL_SCRIPT_NAMES["OpenJarvis"]="openjarvis"', setup)
        self.assertIn('|OpenJarvis|', setup)
        menu = (ROOT / 'scripts/helpers/native_github_menu.sh').read_text(encoding='utf-8')
        self.assertIn('"OpenJarvis"', menu)

    def test_actual_uv_contract_accepts_openjarvis_and_reuses_existing_uv_under_denial(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch.dict(os.environ, {'OPENCLAW_BUILD_DEPS_DENY': '1'}), \
                patch.object(python.native_uv.shutil, 'which', return_value='/existing/uv'), \
                patch.object(python.native_uv.common, 'run', return_value='uv 0.13.5'), \
                patch.object(python.native_uv.releases, 'download') as download, \
                redirect_stdout(io.StringIO()):
            result = python.native_uv.select(Path(directory), self.spec(), approved=True, allow_download=True)
            self.assertEqual(result, '/existing/uv')
            download.assert_not_called()
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_actual_uv_contract_rejects_new_bootstrap_under_explicit_denial(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch.dict(os.environ, {'OPENCLAW_BUILD_DEPS_DENY': '1'}), \
                patch.object(python.native_uv.shutil, 'which', return_value=None), \
                patch.object(python.native_uv.releases, 'host_key', return_value='linux-amd64'), \
                patch.object(python.native_uv.sys.stdin, 'isatty', return_value=True), \
                patch('builtins.input', side_effect=AssertionError('No repeated question')) as question, \
                patch.object(python.native_uv.releases, 'download') as download, \
                redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, 'nicht freigegeben'):
                python.native_uv.select(Path(directory), self.spec(), approved=True, allow_download=True)
            question.assert_not_called()
            download.assert_not_called()
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_plan_status_are_offline_and_create_no_workspace(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch.dict(os.environ, {'OPENCLAW_USER_DATA_DIR': directory}), \
                patch.object(native.common, 'git') as git, patch.object(native, 'preflight') as preflight, \
                patch.object(native, 'build') as build, redirect_stdout(io.StringIO()):
            self.assertEqual(native.main(['openjarvis', 'install', '--dry-run']), 0)
            self.assertEqual(native.main(['openjarvis', 'status']), 0)
            self.assertEqual(list(Path(directory).iterdir()), [])
            git.assert_not_called()
            preflight.assert_not_called()
            build.assert_not_called()

    def test_core_source_wheel_build_never_installs_extras_or_runs_jarvis(self):
        spec = self.spec()
        with tempfile.TemporaryDirectory() as directory:
            prefix = Path(directory) / 'native-github'
            source = prefix / 'source'
            source.mkdir(parents=True)
            calls = []

            def run(args, cwd, env):
                args = list(map(str, args))
                calls.append(args)
                self.assertNotIn('--all-extras', args)
                self.assertNotIn('sync', args)
                self.assertNotIn('maturin', args)
                self.assertNotIn('quickstart.sh', args)
                if '-m' in args and 'build' in args:
                    self.assertEqual(env['SETUPTOOLS_SCM_PRETEND_VERSION_FOR_OPENJARVIS'],
                                     spec['recipe']['version'])
                    with zipfile.ZipFile(prefix / 'wheels/openjarvis-fixture.whl', 'w') as wheel:
                        wheel.writestr('openjarvis/__init__.py', '# fixture, never imported')
                        wheel.writestr('openjarvis/cli/__init__.py', '# fixture, never imported')
                if args[1:3] == ['pip', 'install']:
                    self.assertIn('--require-hashes', args)
                    self.assertIn('--only-binary', args)
                    self.assertIn('https://pypi.org/simple', args)
                    cli = prefix / 'venv/bin/jarvis'
                    cli.parent.mkdir(parents=True, exist_ok=True)
                    cli.write_text('fixture, never executed', encoding='ascii')

            report = {'distributions': [{'name': 'OpenJarvis', 'version': spec['recipe']['version']}]}
            with patch.object(python, 'verify_source'), \
                    patch.object(python.native_uv, 'select', return_value='/uv'), \
                    patch.object(python, 'select_python', return_value='/python'), \
                    patch.object(python, 'execute', return_value=json.dumps(report)) as probe, \
                    redirect_stdout(io.StringIO()):
                artifacts = python.build(source, prefix, spec, {}, run=run)
                self.assertEqual(probe.call_args.args[-1], 45)
                script = probe.call_args.args[0][-1]
                self.assertIn('sys.addaudithook(audit_runtime)', script)
                self.assertIn('openjarvis.cli:main', script)
            self.assertIn('hatch-vcs==0.5.0', (prefix / 'build-requirements.in').read_text())
            receipt = json.loads((prefix / 'python-build-receipt.json').read_text())
            self.assertFalse(receipt['application_tested'])
            self.assertEqual(receipt['commit'], spec['recipe']['pin'])
            self.assertIn('venv/bin/jarvis', artifacts)
            self.assertEqual(sum(a[1:3] == ['pip', 'install'] for a in calls), 2)
            self.assertFalse(any(Path(a[0]).name == 'jarvis' for a in calls))

    def test_docs_state_exact_scope_and_link_both_official_websites(self):
        text = (ROOT / 'docs/tools/openjarvis.md').read_text(encoding='utf-8')
        compact = ' '.join(text.split())
        for value in ('https://github.com/open-jarvis/OpenJarvis', 'https://openjarvis.stanford.edu/',
                      'https://open-jarvis.github.io/OpenJarvis/', 'Python-CLI-/SDK-Build',
                      'kein Quickstart-Autostart', 'Rust-Erweiterung', 'getrennte Ausbaustufen'):
            self.assertIn(value.lower(), compact.lower())
        self.assertIn('tools/openjarvis.md', (ROOT / 'docs/readme.md').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
