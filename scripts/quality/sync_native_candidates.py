"""Synchronize reviewed native recipes with catalog, wrappers and menu (offline)."""
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
FRAGMENTS = ROOT / 'config/native-candidates'
ACTIONS = ('install', 'update', 'uninstall', 'status', 'doctor', 'check')
ALLOWED = {
    'cert_manager': 'cert-manager', 'external_dns': 'External_DNS',
    'kyverno': 'Kyverno', 'gatekeeper': 'Gatekeeper', 'keda': 'KEDA',
    'phoenix': 'Arize_Phoenix', 'gvisor': 'gVisor',
    'kata_containers': 'Kata_Containers', 'firecracker': 'Firecracker',
    'milvus': 'Milvus', 'kubescape': 'Kubescape', 'nuclei': 'Nuclei',
    'testssl': 'Testssl', 'owasp_zap': 'OWASP_ZAP', 'checkov': 'Checkov',
    'ragas': 'Ragas', 'temporal': 'Temporal', 'trufflehog': 'TruffleHog',
    'vaultwarden': 'Vaultwarden', 'argo_workflows': 'Argo_Workflows',
}


def entries():
    result = []
    seen = set()
    for path in sorted(FRAGMENTS.glob('*.json')):
        for item in json.loads(path.read_text(encoding='utf-8'))['tools']:
            key = item['id']
            if key not in ALLOWED or key in seen or item['tool_key'] != ALLOWED[key]:
                raise ValueError('Unknown/duplicate candidate: ' + key)
            recipe = item['recipe']
            if (not re.fullmatch(r'[a-f0-9]{40}', recipe['pin']) or
                    not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', recipe['repo']) or
                    recipe['repo'] != item['repo'] or item.get('blocked_reason') is not None):
                raise ValueError('Invalid reviewed source contract: ' + key)
            doc = Path(item['doc'])
            if doc.is_absolute() or '..' in doc.parts or not (ROOT / doc).is_file():
                raise ValueError('Missing candidate documentation: ' + key)
            seen.add(key)
            result.append(item)
    return result


def render(items):
    outputs = {}
    manifest_path = ROOT / 'config/docker_to_github.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    additions = {item['id']: item for item in items}
    manifest['tools'] = [item for item in manifest['tools'] if item['id'] not in additions] + items
    outputs[manifest_path] = json.dumps(manifest, ensure_ascii=False, indent=2) + '\n'
    registry_path = ROOT / 'config/tools.yml'
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    rows = {row['id']: row for row in registry['tools']}
    for item in items:
        key = item['id']
        row = rows[key]
        row.update(status='experimental', readiness='planned', auto_install=False,
                   install_mode='github-native-build', check_type='path',
                   check_value='~/.openclaw_ultimate_user_data/tools/' + key + '/native-github/build-ready.json',
                   source='https://github.com/' + item['repo'] + '.git', source_verified=True,
                   source_commit=item['recipe']['pin'], license=item['license'],
                   description=item['recipe']['note'], doc=item['doc'])
        for action in ACTIONS:
            row[action + '_script'] = 'scripts/tools/' + key + '_' + action + '.sh'
            outputs[ROOT / row[action + '_script']] = (
                '#!/usr/bin/env bash\nset -euo pipefail\n'
                'ROOT="$(cd "${BASH_SOURCE[0]%/*}/../.." && pwd)"\n'
                'exec "${NATIVE_GITHUB_PYTHON_BIN:-python3}" -B '
                '"$ROOT/scripts/tools/helpers/native_github_tools.py" ' + key + ' ' + action + ' "$@"\n')
        outputs[ROOT / ('scripts/tools/' + key + '_candidate_install.sh')] = (
            '#!/usr/bin/env bash\nset -euo pipefail\n'
            'exec bash "${BASH_SOURCE[0]%/*}/' + key + '_install.sh" "$@"\n')
    outputs[registry_path] = json.dumps(registry, ensure_ascii=False, indent=2) + '\n'
    names = [item['tool_key'] for item in items]
    menu_path = ROOT / 'scripts/helpers/native_github_menu.sh'
    menu = menu_path.read_text(encoding='utf-8')
    marker = '# Generated reviewed candidate keys; see sync_native_candidates.py.'
    menu = re.sub(re.escape(marker) + r'\nNATIVE_GITHUB_TOOL_KEYS\+=\([^\n]*\)\n', '', menu)
    registration = marker + '\nNATIVE_GITHUB_TOOL_KEYS+=(' + ' '.join('"' + name + '"' for name in names) + ')\n'
    prefix, function = menu.split('\nregister_native_github_tool_keys()', 1)
    outputs[menu_path] = prefix.rstrip() + '\n\n' + registration + '\nregister_native_github_tool_keys()' + function
    status_path = ROOT / 'scripts/helpers/native_tool_status.sh'
    status = status_path.read_text(encoding='utf-8')
    status = re.sub(r'    # BEGIN NATIVE CANDIDATES\n.*?    # END NATIVE CANDIDATES\n', '', status, flags=re.S)
    block = '    # BEGIN NATIVE CANDIDATES\n' + ''.join(
        '    "' + item['tool_key'] + '") marker=' + item['id'] + '/native-github/build-ready.json ;;\n'
        for item in items) + '    # END NATIVE CANDIDATES\n'
    outputs[status_path] = status.replace('  case "$1" in\n', '  case "$1" in\n' + block, 1)
    setup_path = ROOT / 'setup_ultimate.sh'
    setup = setup_path.read_text(encoding='utf-8')
    for item in items:
        name, key = item['tool_key'], item['id']
        setup = re.sub(r'^TOOL_SCRIPT_NAMES\["' + re.escape(name) + r'"\]="[^"\n]*"$',
                       'TOOL_SCRIPT_NAMES["' + name + '"]="' + key + '"', setup, flags=re.M)
        label = 'Nativer GitHub-Installer (experimentell); keine automatische Aktivierung. ' + item['doc']
        setup = re.sub(r'^TOOLS\["' + re.escape(name) + r'"\]="[^"\n]*"$',
                       'TOOLS["' + name + '"]="' + label + '"', setup, flags=re.M)
    # Registration already inserts promoted names, so retain only unresolved candidates here.
    def remaining(match):
        original = re.findall(r'"([^"]+)"', match.group(1))
        return 'TOOL_KEYS+=(' + ' '.join('"' + name + '"' for name in original if name not in names) + ')'
    setup = re.sub(r'^TOOL_KEYS\+=\(("[^\n]*)\)$', remaining, setup, flags=re.M)
    setup = re.sub(r'    # BEGIN CANDIDATE BUDGETS\n.*?    # END CANDIDATE BUDGETS\n', '', setup, flags=re.S)
    budget = '    # BEGIN CANDIDATE BUDGETS\n' + ''.join(
        '    "' + item['tool_key'] + '") printf \'' + str(item['recipe']['disk_mb']) + '\' ;;\n'
        for item in items) + '    # END CANDIDATE BUDGETS\n'
    function = 'get_tool_install_fallback_min_free_mb() {'
    before, after = setup.split(function, 1)
    setup = before + function + after.replace('  case "$tool_key" in\n', '  case "$tool_key" in\n' + budget, 1)
    outputs[setup_path] = setup
    overview_path = ROOT / 'docs/tools/infrastructure-candidates.md'
    overview = [
        '# Native Infrastruktur-Installer hinter XERJ', '',
        'Stand: 16.11.2026. Alle 22 genannten Tools stehen weiterhin am Ende des Tools-Menues.',
        'Valkey und Kube_Bench behalten ihre bestehenden nativen Installer; die 20 weiteren Eintraege',
        'verwenden jetzt tool-spezifische native Buildrezepte statt gesperrter Dokumentations-Platzhalter.', '',
        '**Experimentell, echte Linux-Buildabnahme offen:** Offline-Fixtures pruefen Vertrage und Fehlerpfade,',
        'nicht einen abgeschlossenen Ubuntu-/WSL-Build. Installation bedeutet ausschliesslich den unten',
        'und auf der Toolseite beschriebenen Programm-/Komponentenumfang, niemals einen betriebsbereiten Cluster.', '',
        '## Auswahl und Voraussetzungen', '',
        'Im Setup das gewuenschte Tool auswaehlen und fehlende Buildvoraussetzungen bewusst freigeben.',
        'Quellen werden am vollen Pin gebaut; ein Clone allein erzeugt keinen Erfolgsnachweis.',
        'Neue Debian-/Ubuntu-Releases und DietPi werden nicht wegen einer Point-Release-Bezeichnung abgelehnt.',
        'Architektur, Pakete, Compiler, Kernel und Ressourcen muessen trotzdem zum Rezept passen.',
        'Bei WSL gilt auch der echte freie Windows-Backing-Speicher, nicht nur die virtuelle Linux-Kapazitaet.', '',
        'Kein Docker-/Compose-Fallback und kein automatischer Dienst-, Modell-, VM- oder Clusterstart.',
        'Keine CRD-/DNS-/Zertifikatsaenderung, kein Security-Scan oder Provideraufruf durch die Installation.', '',
        '## Installer und Grenzen', '',
        '| Tool | Anleitung | Gebauter Umfang und offene Betriebsabnahme |',
        '| --- | --- | --- |',
    ]
    requested = {'valkey', 'kube_bench', *additions}
    for item in manifest['tools']:
        if item['id'] not in requested:
            continue
        row = rows[item['id']]
        target = Path(row['doc']).name
        note = item['recipe'].get('scope', item['recipe']['note']).replace('|', '/')
        overview.append('| ' + item['tool_key'] + ' | [' + target + '](' + target + ') | ' + note + ' |')
    overview += ['', '## Lifecycle und Nachweise', '',
                 'Jedes Tool besitzt Install, Update, Status, Check, Doctor und geschuetzten Uninstall.',
                 'Update bleibt am freigegebenen Quellenpin; keine stillen Downloads von main/latest.',
                 'Artefakte, Lockfiles und SBOM werden im privaten Buildverzeichnis erfasst.',
                 'Status prueft Buildnachweise, nicht Dienstgesundheit. Doctor ist ohne gesonderte',
                 'Laufzeitabnahme unvollstaendig; keine automatischen Netztests oder Credential-Zugriffe.',
                 'Geaenderte oder fremde Dateien werden nicht automatisch ueberschrieben oder geloescht.', '',
                 'Die verlinkten Toolseiten benennen insbesondere die noch erforderlichen Voraussetzungen',
                 'und Komponenten: Kata-Gaeste/Hypervisor, Milvus-Betriebsdienste, Vaultwarden-Web-Vault,',
                 'ZAP-Add-ons und Argo-API/UI sind nicht durch einen einzelnen Host-Binary-Build erledigt.', '',
                 'Weiter: [Installationsrichtlinie](../INSTALLATION_POLICY.md),',
                 '[Systemdiagnose](../SYSTEM_DIAGNOSTICS.md), [Tool-Lifecycle](../TOOL_LIFECYCLE_STANDARD.md).', '']
    old_overview = overview_path.read_text(encoding='utf-8')
    ssh_marker = '<!-- BEGIN GENERATED VPS SSH -->'
    ssh_section = ssh_marker + old_overview.split(ssh_marker, 1)[1] if ssh_marker in old_overview else ''
    outputs[overview_path] = '\n'.join(overview) + '\n' + ssh_section
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    items = entries()
    if not items:
        raise ValueError('No reviewed fragments; refusing empty synchronization.')
    changed = []
    for path, content in render(items).items():
        if path.exists() and path.read_text(encoding='utf-8') == content:
            continue
        changed.append(path.relative_to(ROOT).as_posix())
        if args.write:
            path.write_text(content, encoding='utf-8', newline='\n')
    print(json.dumps(dict(tools=len(items), changed=changed, written=args.write)))
    return 0 if args.write or not changed else 1


if __name__ == '__main__':
    raise SystemExit(main())
