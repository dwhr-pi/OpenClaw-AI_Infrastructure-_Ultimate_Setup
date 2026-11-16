"""Pinned controller builds and static receipts, never controller execution."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess

import gap_tools as common
import native_build_process
import native_go
import private_go

ROOT = Path(__file__).resolve().parents[3]
FRAGMENT = ROOT / 'config/native-candidates/go-controllers.json'


def contract(spec):
    entries = json.loads(FRAGMENT.read_text(encoding='utf-8'))['tools']
    entry = next((item for item in entries if item['id'] == spec['id']), None)
    if entry is None or any(spec['recipe'].get(k) != v for k, v in entry['recipe'].items()):
        raise ValueError('Nicht freigegebener Controller-Buildvertrag.')
    return entry['recipe']


def path_under(root, relative):
    if (not isinstance(relative, str) or not relative or relative.startswith(('/', '-')) or
            any(c in relative for c in ('\\', ':', '\0')) or '..' in relative.split('/')):
        raise ValueError('Unsicherer Controller-Artefaktpfad.')
    root = common.checked(Path(root))
    result = common.checked(root / relative)
    if not result.is_relative_to(root):
        raise ValueError('Artefakt ausserhalb des Buildziels.')
    return result


def digest(path):
    value = hashlib.sha256()
    with common.checked(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def capture(args, cwd, env):
    return subprocess.run(list(map(str, args)), cwd=cwd, env=env, check=True,
                          capture_output=True, text=True, timeout=60).stdout.strip()


def clean_env(env):
    # Never forward cloud credentials, kubeconfig, GOFLAGS or user Go configuration.
    child = {k: str(v) for k, v in env.items() if k in (
        'PATH', 'LANG', 'LC_ALL', 'HOME', 'TMPDIR', 'GOPATH', 'GOCACHE', 'GOMODCACHE', 'GOROOT')}
    child.update(GOTOOLCHAIN='local', GOENV='off', GOWORK='off', GOFLAGS='',
                 GOTELEMETRY='off', CGO_ENABLED='0', GOMAXPROCS='2',
                 GOPROXY='https://proxy.golang.org', GOSUMDB='sum.golang.org',
                 GOPRIVATE='', GONOPROXY='', GONOSUMDB='',
                 GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                 GIT_TERMINAL_PROMPT='0')
    return child


def select_go(outer, recipe, env, approved=False):
    child = clean_env(env)
    binary = shutil.which('go', path=child.get('PATH'))
    if binary:
        actual = capture([binary, 'version'], outer, child)
        if native_go.version_ok(actual, recipe['go_min']):
            return binary, child, actual
    required = '.'.join(map(str, recipe['go_min']))
    bootstrap = private_go
    if recipe.get('private_go'):
        # Reuse verified extraction/receipts without mutating shared module globals.
        module_spec = importlib.util.spec_from_file_location('controller_private_go', private_go.__file__)
        bootstrap = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(bootstrap)
        bootstrap.VERSION = recipe['private_go']['version']
        bootstrap.ARCHIVES = {key: tuple(value) for key, value in recipe['private_go']['archives'].items()}
    if not native_go.version_ok('go version ' + bootstrap.VERSION + ' linux/amd64', recipe['go_min']):
        raise ValueError('Go >=' + required + ' erforderlich; vorhandener privater Pin ' +
                         bootstrap.VERSION + ' ist zu alt; kein Download.')
    key, _, _ = bootstrap.target()
    slot = common.checked(Path(outer) / 'toolchain' / (bootstrap.VERSION + '-' + key))
    if not slot.exists() and not approved:
        raise ValueError('Go >=' + required + ' fehlt; privater Download nicht freigegeben.')

    def validate(binary, root, target):
        actual = capture([binary, 'version'], outer, {**child, 'GOROOT': str(root)})
        if actual != 'go version ' + bootstrap.VERSION + ' ' + target.replace('-', '/'):
            raise ValueError('Private Go-Version/Architektur abweichend.')

    binary, root = bootstrap.ensure(Path(outer), validate)
    child.update(GOROOT=str(root), PATH=str(Path(binary).parent) + os.pathsep + child.get('PATH', ''))
    return binary, child, capture([binary, 'version'], outer, child)


def preflight(outer, spec, approved=False):
    recipe = contract(spec)
    if platform.system() != 'Linux' or platform.machine().lower() not in ('amd64', 'x86_64', 'arm64', 'aarch64'):
        raise ValueError('Controller-Builds nur nativ unter Linux amd64/arm64; kein Crossbuild.')
    if hasattr(os, 'geteuid') and os.geteuid() == 0:
        raise ValueError('Controller-Build nicht als root/sudo ausfuehren.')
    common.reserve(Path(outer), {'reserve_mb': recipe['disk_mb']})
    info = Path('/proc/meminfo')
    if info.is_file():
        available = re.search(r'^MemAvailable:\s+(\d+)', info.read_text(), re.M)
        if not available or int(available[1]) < recipe['ram_mb'] * 1024:
            raise ValueError('Zu wenig freier RAM fuer Controller-Build.')
    common.executable('git')
    select_go(outer, recipe, os.environ, approved=approved)


def verify_source(source, recipe, env):
    pin = capture(['git', 'rev-parse', 'HEAD'], source, env)
    if pin != recipe['pin']:
        raise ValueError('Controller-Commit stimmt nicht mit Pin ueberein.')
    status = capture(['git', 'status', '--porcelain', '--untracked-files=all', '--ignored'], source, env)
    if status:
        raise ValueError('Controller-Quellen enthalten lokale/unbekannte Aenderungen.')
    for name, expected in recipe['source_sha256'].items():
        if digest(path_under(source, name)) != expected:
            raise ValueError('Controller-Quellhash abweichend: ' + name)


def write_json(prefix, name, value):
    path = path_under(prefix, name)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with path.open('x', encoding='utf-8') as output:
        json.dump(value, output, indent=2, sort_keys=True)
        output.write('\n')
    return name


def components_from_buildinfo(info):
    components = []
    lines = info.splitlines()
    for index, line in enumerate(lines):
        fields = line.strip().split('\t')
        if fields[0] != 'dep' or len(fields) < 3:
            continue
        name, version = fields[1:3]
        properties = []
        if len(fields) > 3:
            properties.append({'name': 'go.sum', 'value': fields[3]})
        if index + 1 < len(lines):
            replacement = lines[index + 1].strip().split('\t')
            if replacement[0] == '=>':
                properties.append({'name': 'go.replace', 'value': '\t'.join(replacement[1:])})
        component = dict(type='library', name=name, version=version)
        if properties:
            component['properties'] = properties
        components.append(component)
    return components


def build(source, prefix, spec, env):
    recipe = contract(spec)
    source, prefix = common.checked(Path(source)), common.checked(Path(prefix))
    if source == prefix or prefix.is_relative_to(source):
        raise ValueError('Build-Ausgabe muss ausserhalb der Quellen liegen.')
    # The central engine owns the operation lock and has already run preflight.
    go, child, go_version = select_go(prefix.parent, recipe, env)
    verify_source(source, recipe, child)
    entries, commands, infos, components = [], [], {}, {}
    outputs = ['bin/' + item['binary'] for item in recipe['builds']]
    outputs += ['receipts/controller-build-lock.json', 'receipts/controller-sbom.cdx.json',
                'receipts/controller-version-probe.json']
    for name in outputs:
        if path_under(prefix, name).exists():
            raise ValueError('Buildziel bereits belegt; keine Dateien ueberschreiben.')
    lock_hashes = {}
    module_dirs = sorted({'.'} | {item['module_dir'] for item in recipe['builds']})
    for directory in module_dirs:
        for filename in ('go.mod', 'go.sum'):
            name = filename if directory == '.' else directory + '/' + filename
            path = path_under(source, name)
            if name not in recipe['source_sha256']:
                raise ValueError('Nicht gepruefte Modul-Lockdatei: ' + name)
            lock_hashes[name] = digest(path)
            target = path_under(prefix, 'locks/' + name)
            target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            with target.open('xb') as stream:
                stream.write(path.read_bytes())
            entries.append('locks/' + name)
    for name in recipe['static_files']:
        path = path_under(source, name)
        if not path.is_file() or path.stat().st_size == 0:
            raise ValueError('Statische Controller-Datei fehlt: ' + name)
        target = path_under(prefix, 'share/upstream/' + name)
        target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with target.open('xb') as stream:
            stream.write(path.read_bytes())
        entries.append('share/upstream/' + name)
    for item in recipe['builds']:
        relative = 'bin/' + item['binary']
        artifact = path_under(prefix, relative)
        artifact.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        cwd = path_under(source, item['module_dir'])
        args = [go, 'build', '-mod=readonly', '-trimpath', '-buildvcs=true', '-p=2']
        if recipe.get('tags'):
            args += ['-tags', ','.join(recipe['tags'])]
        if recipe['ldflags']:
            args += ['-ldflags', recipe['ldflags']]
        args += ['-o', str(artifact), item['package']]
        native_build_process.run(args, cwd, child, timeout=7200, label='Controller-Build')
        if not artifact.is_file() or artifact.stat().st_size == 0:
            raise ValueError('Go meldete Erfolg ohne Buildartefakt.')
        info = capture([go, 'version', '-m', str(artifact)], prefix, child)
        if (not re.search(r':\s+go\d+\.\d+', info.splitlines()[0]) or
                'vcs.revision=' + recipe['pin'] not in info or 'vcs.modified=false' not in info):
            raise ValueError('Go-Buildinfo fehlt/abweichend; kein Buildnachweis.')
        infos[relative] = info
        for component in components_from_buildinfo(info):
            components[json.dumps(component, sort_keys=True)] = component
        commands.append({'cwd': item['module_dir'], 'argv': [str(arg) for arg in args]})
        entries.append(relative)
    for directory in module_dirs:
        capture([go, 'mod', 'verify'], path_under(source, directory), child)
    verify_source(source, recipe, child)
    if any(digest(path_under(source, name)) != checksum for name, checksum in lock_hashes.items()):
        raise ValueError('Go-Lockdatei waehrend des Builds geaendert.')
    hashes = {name: digest(path_under(prefix, name)) for name in entries}
    entries.append(write_json(prefix, 'receipts/controller-version-probe.json', {
        'method': 'go version -m FILE (statische Inspektion)', 'artifacts': infos,
        'executed_artifacts': False, 'cluster_checked': False, 'service_started': False}))
    entries.append(write_json(prefix, 'receipts/controller-sbom.cdx.json', {
        'bomFormat': 'CycloneDX', 'specVersion': '1.5', 'version': 1,
        'metadata': {'properties': [{'name': 'scope', 'value':
            'Go build-info dependencies; no runtime, image or OS package completeness claim'}]},
        'components': [dict(type='application', name=spec['id'], version=recipe['version'])] +
                      list(components.values())}))
    entries.append(write_json(prefix, 'receipts/controller-build-lock.json', {
        'repo': 'https://github.com/' + recipe['repo'], 'commit': recipe['pin'],
        'version': recipe['version'], 'go_version': go_version,
        'source_sha256': recipe['source_sha256'], 'module_lock_sha256': lock_hashes,
        'artifact_sha256': hashes, 'commands': commands,
        'runtime_acceptance': False, 'deployment_applied': False}))
    return entries
