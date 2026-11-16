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
