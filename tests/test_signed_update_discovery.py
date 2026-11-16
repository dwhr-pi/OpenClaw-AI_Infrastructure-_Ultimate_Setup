"""Offline discovery/startup fixtures; no real downloads, signatures, checkout or services."""
import importlib.util
import io
import json
import os
from contextlib import redirect_stdout
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('signed_discovery_test', ROOT / 'scripts/security/discover_signed_update.py')
discovery = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(discovery)
REAL_LOCAL_STATE = discovery.local_state


def release(tag, *, missing=(), **extra):
    return dict(tag_name=tag, draft=False, prerelease=False,
                assets=[{'name': name, 'browser_download_url': 'http://untrusted.invalid/ignored'}
                        for name in discovery.FILES if name not in missing], **extra)


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.key = self.root / 'release.pub'
        self.key.write_text('FIXTURE PUBLIC KEY - no cryptographic evidence')
        self.records = [release('v2.0.0')]
        self.main = {'sha': 'c' * 40}
        self.download = Mock(side_effect=self.response)
        self.manifest = dict(tag='v2.0.0', commit='b' * 40, repo=discovery.updater.REPO, schema_version=1)
        self.verifier = Mock(side_effect=self.verify_fixture)
        self.perform = Mock(return_value=dict(status='release-checked-out-not-runtime-tested', backup='fixture-backup'))
        state = patch.object(discovery, 'local_state', return_value=('v1.0.0', 'a' * 40))
        self.state = state.start()
        self.addCleanup(state.stop)

    def response(self, url, limit):
        if '/releases?' in url:
            return json.dumps(self.records).encode()
        if url.endswith('/commits/main'):
            return json.dumps(self.main).encode()
        self.assertTrue(url.startswith(discovery.DOWNLOAD + 'v2.0.0/'))
        self.assertEqual(limit, 1048576)
        return b'OFFLINE FIXTURE - not executable release data'

    def verify_fixture(self, directory, tag, key):
        self.assertEqual(tag, self.manifest['tag'])
        self.assertEqual(key, self.key)
        self.assertEqual({path.name for path in directory.iterdir()}, set(discovery.FILES))
        return self.manifest

    def run_discovery(self, **kwargs):
        return discovery.discover(self.root, self.key, self.root / 'backups', download=self.download,
                                  verifier=self.verifier, perform=self.perform, **kwargs)

    def test_check_verifies_but_never_updates_or_uses_api_asset_urls(self):
        result = self.run_discovery()
        self.assertEqual(result['status'], 'new-signed-release-available')
        self.assertTrue(result['signature_verified'])
        self.assertFalse(result['checkout'])
        self.assertTrue(result['main_outside_selected_release'])
        self.perform.assert_not_called()
        self.assertTrue(all('untrusted.invalid' not in call.args[0] for call in self.download.call_args_list))
        self.assertFalse((self.root / 'backups').exists())

    def test_apply_passes_only_verified_manifest_and_expected_local_head(self):
        result = self.run_discovery(apply=True)
        self.assertTrue(result['checkout'])
        self.verifier.assert_called_once()
        self.perform.assert_called_once_with(self.root, self.root / 'backups', self.manifest,
                                            apply=True, fetch=True, expected_head='a' * 40)

    def test_incomplete_newer_release_is_reported_not_installed(self):
        self.records.insert(0, release('v3.0.0', missing=('SHA256SUMS.minisig',)))
        result = self.run_discovery()
        self.assertEqual(result['incomplete_releases'], ['v3.0.0'])
        self.assertEqual(result['tag'], 'v2.0.0')

    def test_no_signed_candidate_never_downloads_or_calls_updater(self):
        self.records = [release('v3.0.0', missing=('SHA256SUMS.minisig',))]
        self.assertEqual(self.run_discovery(apply=True)['status'], 'no-verifiable-stable-release')
        self.assertEqual(self.download.call_count, 1)
        self.verifier.assert_not_called()
        self.perform.assert_not_called()

    def test_signature_failure_blocks_without_trying_an_older_candidate(self):
        self.records.append(release('v1.5.0'))
        self.verifier.side_effect = ValueError('invalid fixture signature')
        with self.assertRaises(ValueError):
            self.run_discovery(apply=True)
        self.verifier.assert_called_once()
        self.perform.assert_not_called()
        self.assertFalse(any('/v1.5.0/' in call.args[0] for call in self.download.call_args_list))

    def test_same_older_or_current_commit_never_updates(self):
        for current_tag, current_commit, status in (
                ('v2.0.0', 'a' * 40, 'not-newer-no-downgrade-or-same-version-replacement'),
                ('v3.0.0', 'a' * 40, 'not-newer-no-downgrade-or-same-version-replacement'),
                ('v2.0.0', 'b' * 40, 'already-at-verified-release')):
            self.state.return_value = (current_tag, current_commit)
            self.assertEqual(self.run_discovery(apply=True)['status'], status)
        self.perform.assert_not_called()

    def test_missing_trust_key_stops_before_network(self):
        self.key.unlink()
        with self.assertRaises(ValueError):
            self.run_discovery(apply=True)
        self.download.assert_not_called()

    def test_network_failure_bad_main_or_empty_asset_never_updates(self):
        self.download.side_effect = OSError('offline fixture')
        with self.assertRaises(OSError):
            self.run_discovery(apply=True)
        self.download.side_effect = self.response
        self.main = {'sha': '../not-a-commit'}
        with self.assertRaises(ValueError):
            self.run_discovery(apply=True)
        self.download.side_effect = [json.dumps(self.records).encode(), b'']
        with self.assertRaises(ValueError):
            self.run_discovery(apply=True)
        self.perform.assert_not_called()

    def test_numeric_sort_and_exclusion_of_drafts_prereleases_and_nonversions(self):
        draft = release('v99.0.0'); draft['draft'] = True
        pre = release('v98.0.0'); pre['prerelease'] = True
        complete, incomplete = discovery.candidates([
            release('v1.9.0'), release('v1.10.0'), release('main'), release('v2.0.0-rc.1'), draft, pre])
        self.assertEqual(complete, ['v1.10.0', 'v1.9.0'])
        self.assertEqual(incomplete, [])

    def test_duplicate_tags_assets_and_oversized_lists_are_rejected(self):
        duplicated = release('v2.0.0')
        duplicated['assets'].append({'name': 'SHA256SUMS'})
        for records in ([release('v2.0.0')] * 2, [duplicated], [release('v2.0.0')] * 101, {}):
            with self.assertRaises(ValueError):
                discovery.candidates(records)

    def test_only_official_https_urls_are_allowed(self):
        for url in ('http://github.com/x', 'https://evil.invalid/x', 'https://user@github.com/x',
                    'https://github.com:444/x', 'https://github.com/x#fragment'):
            with self.assertRaises(ValueError):
                discovery.allowed_url(url)
        discovery.allowed_url('https://release-assets.githubusercontent.com/x?token=fixture')

    def test_local_version_uses_exact_patch_tag_without_running_setup(self):
        (self.root / 'setup_ultimate.sh').write_text('APP_VERSION="11.18"\n')
        with patch.object(discovery.updater.safety, 'git', side_effect=[
                Mock(stdout=b'a' * 40, returncode=0), Mock(stdout=b'v11.18.2', returncode=0)]):
            self.assertEqual(REAL_LOCAL_STATE(self.root), ('v11.18.2', 'a' * 40))


class StartupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.key = self.root / 'release.pub'
        self.key.write_text('FIXTURE')
        self.process = Mock(returncode=0)
        self.process.communicate.return_value = (json.dumps(dict(status='new-signed-release-available',
                                                                 tag='v2.0.0', signature_verified=True)), '')

    def test_startup_only_checks_with_a_global_timeout_and_sanitized_environment(self):
        with patch.object(discovery.updater.subprocess, 'Popen', return_value=self.process) as start:
            with patch.dict(os.environ, {'OPENAI_API_KEY': 'fixture-never-forward', 'PYTHONPATH': 'fixture'}):
                message = discovery.startup_check(self.root, self.key)
        self.assertIn('Neues signiertes', message)
        args = start.call_args.args[0]
        self.assertIn('--check-online', args)
        self.assertNotIn('--apply', args)
        self.assertNotIn('OPENAI_API_KEY', start.call_args.kwargs['env'])
        self.process.communicate.assert_called_once_with(timeout=20)

    def test_timeout_kills_the_check_and_never_reports_up_to_date(self):
        self.process.communicate.side_effect = [subprocess.TimeoutExpired('fixture', 20), ('', '')]
        self.process.pid = 12345
        with patch.object(discovery.updater.subprocess, 'Popen', return_value=self.process):
            with patch.object(discovery.os, 'killpg', create=True) as kill:
                message = discovery.startup_check(self.root, self.key)
        self.assertIn('Status unbekannt', message)
        if os.name == 'posix':
            kill.assert_called_once_with(12345, discovery.signal.SIGKILL)
        else:
            self.process.kill.assert_called_once()

    def test_missing_key_skips_network_and_signature_failures_remain_unknown(self):
        self.key.unlink()
        with patch.object(discovery.updater.subprocess, 'Popen') as start:
            self.assertIn('Keine Online-Pruefung', discovery.startup_check(self.root, self.key))
        start.assert_not_called()
        self.key.write_text('FIXTURE')
        self.process.returncode = 1
        with patch.object(discovery.updater.subprocess, 'Popen', return_value=self.process):
            self.assertIn('nicht erfolgreich', discovery.startup_check(self.root, self.key))

    def test_current_release_is_quiet_and_cli_startup_does_not_apply(self):
        self.process.communicate.return_value = (json.dumps(dict(status='already-at-verified-release',
                                                                 signature_verified=True, tag='v2.0.0')), '')
        with patch.object(discovery.updater.subprocess, 'Popen', return_value=self.process):
            self.assertEqual(discovery.startup_check(self.root, self.key), '')
        with patch.object(discovery, 'startup_check', return_value='fixture notice'):
            with patch.object(discovery, 'discover') as apply, redirect_stdout(io.StringIO()):
                self.assertEqual(discovery.main(['--startup-check']), 0)
        apply.assert_not_called()

    def test_malformed_or_unverified_startup_report_never_claims_current(self):
        for report in ([], {}, {'status': 'already-at-verified-release', 'signature_verified': False}):
            self.process.communicate.return_value = (json.dumps(report), '')
            with patch.object(discovery.updater.subprocess, 'Popen', return_value=self.process):
                self.assertIn('nicht verfuegbar', discovery.startup_check(self.root, self.key))

    def test_headless_setup_exits_before_startup_check_and_no_unsigned_menu_repair(self):
        setup = (ROOT / 'setup_ultimate.sh').read_text(encoding='utf-8')
        self.assertLess(setup.index('exec python3 -I -B "$HEADLESS_ROOT/scripts/tool_commands.py"'),
                        setup.index('--startup-check --public-key'))
        self.assertIn('OPENCLAW_UPDATE_CHECK:-1', setup)
        self.assertNotIn('run_bash_script "$INSTALL_DIR/scripts/auto_update_hard.sh"', setup)


if __name__ == '__main__':
    unittest.main()
