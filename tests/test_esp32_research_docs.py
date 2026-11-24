"""Read-only documentation boundaries; never import or execute ESP project code."""
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOC = 'docs/research/ESP32_AI_LINUX_AND_OLLAMA.md'
PROJECTS = ('DaveBben/esp32-llm', 'slvDev/esp32-ai', 'espressif/esp-claw', 'lubluniky/esp32-harness')


class Esp32ResearchDocumentation(unittest.TestCase):
    def test_documentation_is_linked_and_explicitly_excluded_from_setup(self):
        text = (ROOT / DOC).read_text(encoding='utf-8')
        self.assertIn('nicht Bestandteil dieses Setups und werden nicht aufgenommen', text)
        self.assertIn('keine Installationsplanung', text)
        self.assertIn(DOC, (ROOT / 'readme.md').read_text(encoding='utf-8'))
        self.assertIn('research/ESP32_AI_LINUX_AND_OLLAMA.md',
                      (ROOT / 'docs/readme.md').read_text(encoding='utf-8'))
        for project in PROJECTS:
            self.assertIn(project, text)

    def test_research_projects_are_not_registered_as_installers(self):
        for catalog in ('config/tools.yml', 'config/docker_to_github.json'):
            data = json.loads((ROOT / catalog).read_text(encoding='utf-8'))
            serialized = json.dumps(data).lower()
            for project in PROJECTS:
                self.assertNotIn(project.lower(), serialized)

    def test_host_emulator_model_and_client_boundaries_remain_explicit(self):
        text = (ROOT / DOC).read_text(encoding='utf-8')
        for phrase in ('KV-Bytes', 'MALLOC_CAP_SPIRAM', 'QEMU', 'Emscripten',
                       'kein generelles Verbot fuer kleine Modelle', 'Keine Konvertierung',
                       'bereits vorhandenem lokalem Modell', 'Nicht durchgefuehrt',
                       '9,88 Tokens/s', '8,9 Millionen Parameter'):
            self.assertIn(phrase, text)


if __name__ == '__main__':
    unittest.main()
