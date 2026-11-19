"""Offline contracts and synthetic artifacts, never real runtime acceptance."""
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/tools/helpers'))
import security_data_native as native

SPECS = {x['id']: x for x in json.loads((ROOT / 'config/native-candidates/security-data.json').read_text())['tools']}


class CandidateTests(unittest.TestCase):
    def test_manifest_and_hooks(self):
        self.assertEqual(set(SPECS), native.IDS)
        for spec in SPECS.values():
            self.assertEqual(native.recipe(spec)['candidate_module'], 'security_data_native')
            self.assertTrue((ROOT / spec['doc']).is_file())
            self.assertTrue(spec['license'])
            self.assertNotIn('probe', spec['recipe'])
            self.assertEqual(spec['recipe']['kind'], 'candidate-native')

    def test_bad_paths(self):
        for name in ('../data', '/etc/passwd', 'C:/data', 'a\\b', '-switch', ''):
            with self.subTest(name=name), self.assertRaises(ValueError):
                native.relative(name)

    def test_missing_contract_rejected(self):
        spec = json.loads(json.dumps(SPECS['vaultwarden']))
        del spec['recipe']['source_sha256']['Cargo.lock']
        with self.assertRaises(ValueError):
            native.recipe(spec)

    def test_source_hash_failure_precedes_build(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'source'
            source.mkdir()
            spec = SPECS['vaultwarden']
            def git(_, *args):
                return spec['recipe']['pin'] if args[0] == 'rev-parse' else 'https://github.com/' + spec['repo'] + '.git'
            with patch.object(native.common, 'git', side_effect=git), self.assertRaises(ValueError):
                native.verify_source(source, spec)

    def test_version_runner_bounded_no_stdin(self):
        with patch.object(native.subprocess, 'run') as run:
            run.return_value.stdout = 'v1'
            run.return_value.stderr = ''
            self.assertEqual(native.versions(['compiler', '--version'], Path.cwd(), {}), 'v1')
            self.assertEqual(run.call_args.kwargs['timeout'], 30)
            self.assertEqual(run.call_args.kwargs['stdin'], native.subprocess.DEVNULL)

    def test_rust_no_implicit_bootstrap(self):
        with patch.dict(os.environ, {'NATIVE_SOURCE_RUST_TOOLCHAIN': ''}), self.assertRaises(ValueError):
            native.rust_environment(SPECS['vaultwarden'], {}, Path.cwd())

    def test_gradle_requires_consent_before_download(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(native.shutil, 'which', return_value=None), \
                patch.object(native.releases, 'download') as download:
            with self.assertRaisesRegex(ValueError, 'Zustimmung'):
                native.zap_gradle(Path(temp), SPECS['owasp_zap'], {}, prepare=True)
            download.assert_not_called()
            self.assertFalse((Path(temp) / 'toolchain').exists())

    def test_gradle_private_bootstrap_reuse_and_tamper(self):
        with tempfile.TemporaryDirectory() as temp:
            base, env = Path(temp), {'PATH': ''}
            def download(url, target, size, sha):
                self.assertEqual(url, native.GRADLE_URL)
                self.assertEqual(size, 232036537)
                self.assertEqual(sha, native.GRADLE_SHA256)
                with zipfile.ZipFile(target, 'w') as archive:
                    archive.writestr('gradle-8.13/bin/gradle', '#!/bin/sh\nexit 0\n')
                    archive.writestr('gradle-8.13/lib/fixture.jar', 'synthetic')
            with patch.object(native.shutil, 'which', return_value=None), \
                    patch.object(native.common, 'reserve') as reserve, \
                    patch.object(native.releases, 'download', side_effect=download) as fetch:
                native.zap_gradle(base, SPECS['owasp_zap'], env, approved=True, prepare=True)
                reserve.assert_called_once_with(base, {'reserve_mb': 13312})
                native.zap_gradle(base, SPECS['owasp_zap'], {}, prepare=False)
                self.assertEqual(fetch.call_count, 1)
                entry = base / 'toolchain/gradle-8.13/app/gradle-8.13/bin/gradle'
                self.assertEqual(env['PATH'].split(os.pathsep)[0], str(entry.parent))
                entry.write_text('modified')
                with self.assertRaises(ValueError):
                    native.zap_gradle(base, SPECS['owasp_zap'], {}, approved=True, prepare=True)
                self.assertEqual(fetch.call_count, 1)

    def test_gradle_failed_hash_does_not_publish(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(native.shutil, 'which', return_value=None), \
                patch.object(native.common, 'reserve'), \
                patch.object(native.releases, 'download', side_effect=ValueError('SHA256')):
            with self.assertRaisesRegex(ValueError, 'SHA256'):
                native.zap_gradle(Path(temp), SPECS['owasp_zap'], {}, approved=True, prepare=True)
            self.assertFalse((Path(temp) / 'toolchain/gradle-8.13').exists())
            self.assertEqual(list(Path(temp).glob('gradle-bootstrap-*')), [])

    def test_gradle_contract_change_rejected_before_download(self):
        spec = json.loads(json.dumps(SPECS['owasp_zap']))
        spec['recipe']['gradle_distribution']['sha256'] = '0' * 64
        with tempfile.TemporaryDirectory() as temp, patch.object(native.releases, 'download') as download:
            with self.assertRaisesRegex(ValueError, 'Downloadvertrag'):
                native.zap_gradle(Path(temp), spec, {}, approved=True, prepare=True)
            download.assert_not_called()

    def test_gradle_existing_exact_version_without_download(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(native.shutil, 'which', return_value='/gradle'), \
                patch.object(native, 'versions', return_value='Gradle 8.13\n'), \
                patch.object(native.releases, 'download') as download:
            native.zap_gradle(Path(temp), SPECS['owasp_zap'], {}, prepare=True)
            download.assert_not_called()

    def test_zap_java_prerequisites_use_consent_gated_package_path(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(native.shutil, 'which', return_value=None), \
                patch.object(native.Path, 'is_file', return_value=False), \
                patch.object(native.native_build_deps, 'prepare', side_effect=ValueError('no consent')) as prepare:
            with self.assertRaisesRegex(ValueError, 'no consent'):
                native.zap_java(Path(temp), SPECS['owasp_zap'], {}, prepare=True)
            prepare.assert_called_once_with(SPECS['owasp_zap'], approved=False)

    def test_zap_existing_jdk_sets_private_build_environment_only(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            compiler = base / 'jdk/bin/javac'
            compiler.parent.mkdir(parents=True)
            compiler.write_text('fixture')
            env = {'PATH': 'original', 'JAVA_HOME': 'incompatible-jdk'}
            def version(args, cwd, child):
                return 'javac 21.0.9' if args[0] == str(compiler) else 'openjdk version "21.0.9"'
            with patch.object(native.shutil, 'which', side_effect=lambda name, **_: str(compiler) if name == 'javac' else 'java'), \
                    patch.object(native, 'versions', side_effect=version), \
                    patch.object(native.native_build_deps, 'prepare') as prepare:
                native.zap_java(base, SPECS['owasp_zap'], env, approved=True, prepare=True)
                self.assertEqual(env['JAVA_HOME'], str(compiler.parent.parent))
                self.assertEqual(env['PATH'], 'original')
                prepare.assert_not_called()

    @unittest.skipIf(os.name == 'nt', 'Windows does not preserve POSIX executable permission bits')
    def test_elf_probe_no_subprocess(self):
        with tempfile.TemporaryDirectory() as temp:
            prefix = Path(temp)
            (prefix / 'bin').mkdir()
            path = prefix / 'bin/vaultwarden'
            path.write_bytes(b'\x7fELF\x02\x01' + b'\0' * 12 + b'\x3e\x00')
            path.chmod(path.stat().st_mode | stat.S_IXUSR)
            with patch.object(native.subprocess, 'run', side_effect=AssertionError('application executed')):
                result = native.probe(prefix, SPECS['vaultwarden'])
            self.assertEqual(result['doctor_exit'], 3)
            self.assertFalse(result['runtime_tested'])
            path.write_bytes(b'not an ELF')
            with self.assertRaises(ValueError):
                native.probe(prefix, SPECS['vaultwarden'])

    def test_zap_jar_probe(self):
        with tempfile.TemporaryDirectory() as temp:
            prefix = Path(temp)
            dist = prefix / 'source/zap/build/distFiles'
            dist.mkdir(parents=True)
            with zipfile.ZipFile(dist / 'zap-2.17.0.jar', 'w') as jar:
                jar.writestr('META-INF/MANIFEST.MF', 'Implementation-Version: 2.17.0\n')
                jar.writestr('org/zaproxy/zap/ZAP.class', b'fixture')
            self.assertTrue(native.probe(prefix, SPECS['owasp_zap'])['artifact_probe_passed'])

    def test_doctor_detects_modified_files(self):
        with tempfile.TemporaryDirectory() as temp:
            prefix = Path(temp)
            artifact = prefix / 'fixture'
            artifact.write_bytes(b'original')
            native.write(prefix / 'candidate-artifact-receipt.json',
                         dict(commit=SPECS['vaultwarden']['recipe']['pin'], files={'fixture': native.digest(artifact)}))
            artifact.write_bytes(b'modified')
            with self.assertRaises(ValueError):
                native.doctor(prefix, SPECS['vaultwarden'])

    @unittest.skipUnless(os.name == 'posix', 'POSIX symlinks')
    def test_external_artifact_link_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            prefix = Path(temp) / 'prefix'
            prefix.mkdir()
            outside = Path(temp) / 'outside'
            outside.write_bytes(b'do not modify')
            (prefix / 'link').symlink_to(outside)
            with self.assertRaises(ValueError):
                native.collect(prefix, prefix)
            self.assertEqual(outside.read_bytes(), b'do not modify')

    def test_write_never_overwrites(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'evidence'
            native.write(path, 'original')
            with self.assertRaises(FileExistsError):
                native.write(path, 'replacement')

    def test_vaultwarden_command_and_scope(self):
        with tempfile.TemporaryDirectory() as temp:
            prefix = Path(temp)
            source = prefix / 'source'
            source.mkdir()
            (source / '.env.template').write_text('# fixture\n')
            (source / 'Cargo.lock').write_text('version = 4\n[[package]]\nname="fixture"\nversion="1.0"\n')
            binary = prefix / '_build/cargo-target/release/vaultwarden'
            binary.parent.mkdir(parents=True)
            binary.write_bytes(b'fixture-not-runtime')
            calls = []
            entries, components = native.vaultwarden(source, prefix, SPECS['vaultwarden'], {},
                                                     lambda args, cwd, env: calls.append(args))
            self.assertEqual(entries, ['bin/vaultwarden'])
            self.assertIn('--locked', calls[0])
            self.assertEqual(calls[0][-2:], ['--bin', 'vaultwarden'])
            self.assertIn('WEB_VAULT_ENABLED=false', (prefix / 'config/vaultwarden.env.example').read_text())
            self.assertEqual(components[0]['name'], 'fixture')


if __name__ == '__main__':
    unittest.main()
