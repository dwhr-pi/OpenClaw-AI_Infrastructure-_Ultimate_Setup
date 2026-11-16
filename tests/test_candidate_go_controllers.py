"""Offline controller hook tests; mocks are not upstream build acceptance."""
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/tools/helpers'))
import candidate_go_controllers as controllers


class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.specs = json.loads(controllers.FRAGMENT.read_text(encoding='utf-8'))['tools']
        self.spec = copy.deepcopy(self.specs[3])
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source, self.prefix = self.base / 'source', self.base / 'prefix'
        self.source.mkdir()
        self.prefix.mkdir()

    def fixture_recipe(self):
        recipe = copy.deepcopy(self.spec['recipe'])
        recipe['source_sha256'] = {}
        recipe['static_files'] = ['deploy/gatekeeper.yaml']
        for name, data in [('go.mod', b'module fixture\ngo 1.26.0\n'),
                           ('go.sum', b'example.org/lib v1.0.0 h1:fixture\n'),
                           ('main.go', b'package main\nfunc main() {}\n'),
                           ('deploy/gatekeeper.yaml', b'kind: CustomResourceDefinition\n')]:
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            recipe['source_sha256'][name] = hashlib.sha256(data).hexdigest()
        return recipe

    def buildinfo(self, recipe):
        return ('binary: go1.27.4\n\tdep\texample.org/lib\tv1.0.0\th1:fixture\n'
                '\tbuild\tvcs.revision=' + recipe['pin'] + '\n\tbuild\tvcs.modified=false')

    def fake_compile(self, args, cwd, env, **kwargs):
        self.assertNotIn('KUBECONFIG', env)
        self.assertEqual(env['GOTOOLCHAIN'], 'local')
        self.assertIn('-mod=readonly', args)
        self.assertIn('-buildvcs=true', args)
        Path(args[args.index('-o') + 1]).write_bytes(b'fixture-not-an-executable')

    def fake_capture(self, recipe):
        def run(args, cwd, env):
            if args[:3] == ['git', 'rev-parse', 'HEAD']:
                return recipe['pin']
            if args[:2] == ['git', 'status']:
                return ''
            if args[1:3] == ['version', '-m']:
                return self.buildinfo(recipe)
            if args[1:3] == ['mod', 'verify']:
                return 'all modules verified'
            self.fail('Unexpected process: ' + repr(args))
        return run

    def build_patches(self, recipe):
        return (patch.object(controllers, 'contract', return_value=recipe),
                patch.object(controllers, 'select_go', return_value=(
                    '/checked/go', controllers.clean_env({'PATH': 'fixture', 'HOME': str(self.base)}),
                    'go version go1.27.4 linux/amd64')),
                patch.object(controllers, 'capture', side_effect=self.fake_capture(recipe)),
                patch.object(controllers.native_build_process, 'run', side_effect=self.fake_compile))

    def test_fragment_schema_and_all_pins(self):
        self.assertEqual([s['tool_key'] for s in self.specs],
                         ['cert-manager', 'External_DNS', 'Kyverno', 'Gatekeeper', 'KEDA', 'Temporal', 'Argo_Workflows'])
        for spec in self.specs:
            r = controllers.contract(spec)
            self.assertRegex(r['pin'], r'^[a-f0-9]{40}$')
            self.assertEqual(r['kind'], 'candidate-native')
            self.assertEqual(r['probe'], [])
            self.assertEqual(r['probe_mode'], 'go-buildinfo')
            self.assertTrue({'go.mod', 'go.sum', 'Makefile'} <= r['source_sha256'].keys())
            self.assertIsNone(spec['blocked_reason'])
            self.assertTrue(r['static_files'])
            for value in r['source_sha256'].values():
                self.assertRegex(value, r'^[a-f0-9]{64}$')
            self.assertTrue((ROOT / spec['doc']).is_file())

    def test_changed_recipe_rejected_before_processes(self):
        for field, value in [('pin', '0' * 40), ('ldflags', '-X bad=1'), ('go_min', [1, 1, 0]),
                             ('static_files', ['../../secret']), ('builds', [])]:
            spec = copy.deepcopy(self.spec)
            spec['recipe'][field] = value
            with patch.object(controllers, 'capture') as run, self.assertRaises(ValueError):
                controllers.build(self.source, self.prefix, spec, {})
            run.assert_not_called()

    def test_path_traversal_rejected(self):
        for name in ('../secret', '/tmp/secret', 'C:/secret', 'a\\b', 'a/../../b', '-bad', ''):
            with self.subTest(name=name), self.assertRaises(ValueError):
                controllers.path_under(self.prefix, name)

    def test_environment_drops_credentials_user_flags_and_crossbuild(self):
        env = controllers.clean_env({'PATH': 'fixture', 'KUBECONFIG': '/secret', 'AWS_PROFILE': 'secret',
                                     'GOFLAGS': '-mod=mod', 'GOOS': 'windows', 'GOARCH': 'arm',
                                     'GOTOOLCHAIN': 'auto', 'GOPROXY': 'https://private.invalid',
                                     'GOSUMDB': 'off', 'GIT_CONFIG_COUNT': '1'})
        for key in ('KUBECONFIG', 'AWS_PROFILE', 'GOOS', 'GOARCH', 'GIT_CONFIG_COUNT'):
            self.assertNotIn(key, env)
        self.assertEqual(env['GOFLAGS'], '')
        self.assertEqual(env['GOTOOLCHAIN'], 'local')
        self.assertEqual(env['GOSUMDB'], 'sum.golang.org')

    def test_missing_go_never_downloads_without_consent(self):
        with patch.object(controllers.shutil, 'which', return_value=None), \
             patch.object(controllers.private_go, 'target', return_value=('linux-amd64', 'archive', ('hash', 1))), \
             patch.object(controllers.private_go, 'ensure') as ensure:
            with self.assertRaisesRegex(ValueError, 'nicht freigegeben'):
                controllers.select_go(self.base, self.spec['recipe'], {})
        ensure.assert_not_called()

    def test_keda_has_current_private_pin_but_needs_download_consent(self):
        keda = next(s for s in self.specs if s['id'] == 'keda')
        self.assertEqual(keda['recipe']['go_min'], [1, 27, 4])
        self.assertEqual(keda['recipe']['private_go']['version'], 'go1.27.4')
        with patch.object(controllers.shutil, 'which', return_value=None), \
             patch.object(controllers.platform, 'system', return_value='Linux'), \
             patch.object(controllers.platform, 'machine', return_value='x86_64'), \
             patch.object(controllers.private_go, 'ensure') as ensure:
            with self.assertRaisesRegex(ValueError, 'nicht freigegeben'):
                controllers.select_go(self.base, keda['recipe'], {})
        ensure.assert_not_called()

    def test_existing_go_no_bootstrap(self):
        with patch.object(controllers.shutil, 'which', return_value='/checked/go'), \
             patch.object(controllers, 'capture', return_value='go version go1.27.4 linux/amd64'), \
             patch.object(controllers.private_go, 'ensure') as ensure:
            binary, env, version = controllers.select_go(self.base, self.spec['recipe'], {})
        ensure.assert_not_called()
        self.assertEqual(binary, '/checked/go')
        self.assertEqual(env['GOTOOLCHAIN'], 'local')

    def test_wrong_platform_fails_before_download(self):
        with patch.object(controllers.platform, 'system', return_value='Windows'), \
             patch.object(controllers.private_go, 'ensure') as ensure:
            with self.assertRaisesRegex(ValueError, 'Linux'):
                controllers.preflight(self.base, self.spec, approved=True)
        ensure.assert_not_called()

    def test_low_disk_fails_before_download(self):
        with patch.object(controllers.platform, 'system', return_value='Linux'), \
             patch.object(controllers.platform, 'machine', return_value='x86_64'), \
             patch.object(controllers.os, 'geteuid', return_value=1000, create=True), \
             patch.object(controllers.common, 'reserve', side_effect=ValueError('disk')), \
             patch.object(controllers, 'select_go') as select:
            with self.assertRaisesRegex(ValueError, 'disk'):
                controllers.preflight(self.base, self.spec, approved=True)
        select.assert_not_called()

    def test_build_creates_binaries_locks_static_files_and_honest_receipts(self):
        recipe = self.fixture_recipe()
        a, b, c, d = self.build_patches(recipe)
        with a, b, c as capture, d:
            entries = controllers.build(self.source, self.prefix, self.spec, {'KUBECONFIG': '/secret'})
        self.assertIn('bin/gatekeeper', entries)
        self.assertIn('share/upstream/deploy/gatekeeper.yaml', entries)
        self.assertTrue(all((self.prefix / name).is_file() for name in entries))
        for call in capture.call_args_list:
            self.assertIn(str(call.args[0][0]), ('git', '/checked/go'))
        lock = json.loads((self.prefix / 'receipts/controller-build-lock.json').read_text())
        self.assertFalse(lock['runtime_acceptance'])
        self.assertFalse(lock['deployment_applied'])
        self.assertEqual(lock['artifact_sha256']['bin/gatekeeper'],
                         controllers.digest(self.prefix / 'bin/gatekeeper'))
        sbom = json.loads((self.prefix / 'receipts/controller-sbom.cdx.json').read_text())
        self.assertEqual(sbom['components'][1]['name'], 'example.org/lib')
        probe = json.loads((self.prefix / 'receipts/controller-version-probe.json').read_text())
        self.assertFalse(probe['executed_artifacts'])

    def test_dirty_source_fails_before_compile(self):
        recipe = self.fixture_recipe()
        a, b, _, d = self.build_patches(recipe)
        with a, b, patch.object(controllers, 'capture', side_effect=[recipe['pin'], ' M main.go']), d as compile:
            with self.assertRaisesRegex(ValueError, 'Aenderungen'):
                controllers.build(self.source, self.prefix, self.spec, {})
        compile.assert_not_called()

    def test_changed_source_hash_fails_before_compile(self):
        recipe = self.fixture_recipe()
        (self.source / 'go.mod').write_bytes(b'changed')
        a, b, c, d = self.build_patches(recipe)
        with a, b, c, d as compile:
            with self.assertRaisesRegex(ValueError, 'Quellhash'):
                controllers.build(self.source, self.prefix, self.spec, {})
        compile.assert_not_called()

    def test_no_artifact_not_accepted(self):
        recipe = self.fixture_recipe()
        a, b, c, _ = self.build_patches(recipe)
        with a, b, c, patch.object(controllers.native_build_process, 'run'):
            with self.assertRaisesRegex(ValueError, 'ohne Buildartefakt'):
                controllers.build(self.source, self.prefix, self.spec, {})
        self.assertFalse((self.prefix / 'receipts/controller-build-lock.json').exists())

    def test_metadata_must_match_commit_and_clean_tree(self):
        recipe = self.fixture_recipe()
        a, b, c, d = self.build_patches(recipe)
        with a, b, c, d, patch.object(self, 'buildinfo', return_value='binary: go1.27.4\n'):
            with self.assertRaisesRegex(ValueError, 'Buildinfo'):
                controllers.build(self.source, self.prefix, self.spec, {})

    def test_existing_artifact_is_preserved(self):
        recipe = self.fixture_recipe()
        (self.prefix / 'bin').mkdir()
        binary = self.prefix / 'bin/gatekeeper'
        binary.write_bytes(b'preserve')
        a, b, c, d = self.build_patches(recipe)
        with a, b, c, d as compile:
            with self.assertRaisesRegex(ValueError, 'belegt'):
                controllers.build(self.source, self.prefix, self.spec, {})
        compile.assert_not_called()
        self.assertEqual(binary.read_bytes(), b'preserve')

    def test_output_inside_source_rejected(self):
        with self.assertRaisesRegex(ValueError, 'ausserhalb'):
            controllers.build(self.source, self.source / 'build', self.spec, {})

    def test_component_replacements_are_recorded(self):
        info = '\tdep\told.example/lib\tv1\th1:old\n\t=>\tnew.example/lib\tv2\th1:new\n'
        c = controllers.components_from_buildinfo(info)[0]
        self.assertEqual(c['properties'][1]['name'], 'go.replace')
        self.assertIn('h1:new', c['properties'][1]['value'])

    def test_cert_manager_nested_modules_and_temporal_tags(self):
        cert = self.specs[0]['recipe']
        self.assertEqual(len(cert['builds']), 5)
        for b in cert['builds']:
            self.assertEqual(b['package'], '.')
            self.assertIn(b['module_dir'] + '/go.sum', cert['source_sha256'])
        temporal = next(s for s in self.specs if s['id'] == 'temporal')['recipe']
        self.assertEqual(temporal['tags'], ['disable_grpc_modules'])
        argo = self.specs[-1]['recipe']
        self.assertEqual({b['package'] for b in argo['builds']}, {'./cmd/workflow-controller', './cmd/argoexec'})


if __name__ == '__main__':
    unittest.main()
