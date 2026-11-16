"""Static examples and isolated proxy fixtures; no cluster/provider requests."""
import ast
import os
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'examples/kubernetes/hardened-services.yaml'
SOURCE = ROOT / 'examples/kubernetes/gemini_proxy.py'


class HardenedExamples(unittest.TestCase):
    def test_no_old_executable_path_and_every_container_is_restricted(self):
        self.assertFalse((ROOT / 'scripts/k8s_deployments.yaml').exists())
        text = MANIFEST.read_text(encoding='utf-8')
        self.assertEqual(text.count('readOnlyRootFilesystem: true'), 6)
        self.assertEqual(text.count('allowPrivilegeEscalation: false'), 6)
        self.assertEqual(text.count('capabilities: {drop: [ALL]}'), 6)
        self.assertEqual(text.count('runAsNonRoot: true'), 5)
        self.assertEqual(text.count('automountServiceAccountToken: false'), 5)
        self.assertEqual(text.count('replicas: 0'), 5)
        self.assertNotIn('LoadBalancer', text)
        self.assertNotIn(':latest', text)
        self.assertIn('registry.invalid/', text)
        self.assertIn('test "${#OPENMANUS_COMMIT}" -eq 40', text)

    def load_proxy(self):
        source = SOURCE.read_text(encoding='utf-8')
        ast.parse(source)
        app = SimpleNamespace(config={}, logger=Mock())
        app.before_request = lambda function: function
        app.route = lambda *args, **kwargs: lambda function: function
        flask = ModuleType('flask')
        flask.Flask = lambda name: app
        flask.request = SimpleNamespace(headers={}, get_json=lambda **kwargs: None)
        flask.jsonify = lambda value: value
        requests = ModuleType('requests')
        requests.post = Mock(side_effect=AssertionError('no provider call allowed'))
        requests.exceptions = SimpleNamespace(RequestException=RuntimeError)
        namespace = {'__name__': 'isolated_example'}
        env = {'GEMINI_API_KEY': 'fixture-not-a-key', 'GEMINI_MODEL': 'fixture-model',
               'PROXY_AUTH_TOKEN': 'fixture-token-' * 4, 'OLLAMA_URL': 'http://ollama:11434'}
        with patch.dict(sys.modules, {'flask': flask, 'requests': requests}), patch.dict(os.environ, env):
            exec(compile(source, '<isolated proxy fixture>', 'exec'), namespace)
        return namespace, flask, requests, app

    def test_proxy_authentication_and_non_ascii_headers_fail_closed(self):
        namespace, flask, requests, app = self.load_proxy()
        self.assertEqual(namespace['authorize']()[1], 401)
        flask.request.headers = {'Authorization': 'Bearer ' + chr(0xE4)}
        self.assertEqual(namespace['authorize']()[1], 401)
        flask.request.headers = {'Authorization': 'Bearer ' + 'fixture-token-' * 4}
        self.assertIsNone(namespace['authorize']())
        requests.post.assert_not_called()
        self.assertEqual(app.config['MAX_CONTENT_LENGTH'], 65536)

    def test_invalid_json_never_contacts_provider(self):
        namespace, flask, requests, _ = self.load_proxy()
        for value in (None, [], {'prompt': 4}, {'prompt': ' '}, {'prompt': 'a' * 16001}):
            flask.request.get_json = lambda **kwargs: value
            self.assertEqual(namespace['generate']()[1], 400)
        requests.post.assert_not_called()

    def test_credentials_are_not_in_urls_or_exception_logs(self):
        source = SOURCE.read_text(encoding='utf-8')
        self.assertNotIn('?key=', source)
        self.assertNotIn('print(', source)
        self.assertIn('"x-goog-api-key": GEMINI_API_KEY', source)
        self.assertIn('"stream": False', source)

    def test_source_is_packaged_in_image_not_embedded_as_configmap_data(self):
        text = MANIFEST.read_text(encoding='utf-8')
        self.assertNotIn('  proxy.py: |', text)
        self.assertNotIn('gemini-ollama-proxy-config', text)
        self.assertNotIn('name: proxy-code', text)
        self.assertIn('command: ["python", "/app/proxy.py"]', text)
        self.assertIn('secretKeyRef: {name: gemini-secrets, key: proxy-auth-token}', text)
        self.assertIn('secretKeyRef:', text)
        self.assertIn('key: api-key', text)
        self.assertIn('gemini_proxy.py', (MANIFEST.parent / 'README.md').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
