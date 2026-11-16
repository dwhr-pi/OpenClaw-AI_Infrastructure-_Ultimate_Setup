"""Native security CLI artifacts; no scan, service or credential probe."""
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import stat
import subprocess
import tempfile

import gap_tools as common
import native_build_deps
import native_go

TOOLS = {
    'kubescape': ('kubescape/kubescape', [1, 27, 0], '.', ['version', '--format', 'json']),
    'nuclei': ('projectdiscovery/nuclei', [1, 26, 0], './cmd/nuclei', ['-disable-update-check', '-version']),
    'trufflehog': ('trufflesecurity/trufflehog', [1, 26, 0], '.', ['--no-update', '--version']),
    'testssl': ('testssl/testssl.sh', None, None, ['--version']),
}
TESTSSL_PACKAGES = ('bash', 'openssl', 'bsdextrautils', 'coreutils', 'gawk', 'grep',
                    'sed', 'procps', 'findutils', 'util-linux')
TESTSSL_COMMANDS = ('bash', 'openssl', 'hexdump', 'dd', 'grep', 'awk', 'tr', 'sed',
                    'wc', 'date', 'cat', 'ps', 'kill', 'head', 'tail', 'dirname',
                    'mktemp', 'uname', 'readlink', 'sort', 'find', 'rm')
SYSTEM_PATH = '/usr/bin:/bin'
RECEIPTS = ('security-dependency-lock.json', 'security-sbom.cdx.json',
            'security-version-probe.json', 'security-artifacts.json')


def relative(name):
    if (not isinstance(name, str) or not name or name.startswith(('/', '-', '.git/'))
            or '\\' in name or ':' in name or any(p in ('', '.', '..') for p in name.split('/'))):
        raise ValueError('Unsicherer relativer Artefakt-/Quellpfad.')
    return name


def checked_file(path):
    path = common.checked(path)
    info = path.lstat()
    if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1
            or (hasattr(os, 'geteuid') and info.st_uid != os.geteuid())):
        raise ValueError('Datei fremd, verlinkt oder nicht regulaer: ' + str(path))
    return path


def sha256(path):
    digest = hashlib.sha256()
    with checked_file(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def contract(spec):
    key, recipe = spec['id'], spec['recipe']
    if key not in TOOLS:
        raise ValueError('Unbekanntes Security-CLI.')
    repo, minimum, package, probe = TOOLS[key]
    if (recipe['kind'] != 'candidate-native' or recipe['repo'] != repo
            or recipe.get('go_min') != minimum or recipe.get('package') != package
            or recipe.get('binary') != key or recipe.get('probe') != probe
            or not re.fullmatch('[0-9a-f]{40}', recipe['pin'])
            or not re.fullmatch(r'\d+\.\d+\.\d+', recipe['version'])):
        raise ValueError('Nicht freigegebener Security-Buildvertrag.')
    if tuple(recipe.get('apt_build_deps', [])) != (TESTSSL_PACKAGES if key == 'testssl' else ()):
        raise ValueError('Nicht freigegebene Security-Systempakete.')
    hashes = recipe['source_sha256']
    required = {'testssl.sh', 'LICENSE', 'etc/openssl.cnf', 'etc/cipher-mapping.txt'} if key == 'testssl' else {'go.mod', 'go.sum'}
    if not required <= hashes.keys() or len(hashes) > 64:
        raise ValueError('Unvollstaendiger Quellvertrag.')
    for name, digest in hashes.items():
        relative(name)
        if not re.fullmatch('[0-9a-f]{64}', digest):
            raise ValueError('Ungueltiger Quellhash.')
    return recipe


def recipe_hash(spec):
    return hashlib.sha256(json.dumps(spec['recipe'], sort_keys=True).encode()).hexdigest()


def source_contracts(source, spec):
    recipe = contract(spec)
    for name, digest in recipe['source_sha256'].items():
        if sha256(source / name) != digest:
            raise ValueError('Quell-/Lockhash abweichend: ' + name)


def execute(args, cwd, env):
    import native_build_process
    return native_build_process.run(list(map(str, args)), cwd, env, timeout=7200)


def command(name):
    path = shutil.which(name, path=SYSTEM_PATH)
    if not path:
        raise ValueError('Systemabhaengigkeit fehlt: ' + name)
    return path


def isolated(args, cwd):
    # A new empty HOME and network namespace are mandatory, never a best-effort flag.
    with tempfile.TemporaryDirectory(prefix='security-probe-') as directory:
        home = Path(directory)
        env = dict(PATH=SYSTEM_PATH, HOME=directory, TMPDIR=directory, LANG='C', LC_ALL='C',
                   XDG_CONFIG_HOME=str(home / 'config'), XDG_CACHE_HOME=str(home / 'cache'),
                   XDG_DATA_HOME=str(home / 'data'), NO_COLOR='1', TERM='dumb',
                   GOTOOLCHAIN='local', GOENV='off', GOWORK='off', GOTELEMETRY='off')
        args = [command('unshare'), '--user', '--map-root-user', '--net', '--fork',
                '--kill-child=KILL', '--'] + list(map(str, args))
        result = subprocess.run(args, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                capture_output=True, text=True, errors='replace',
                                check=True, timeout=30)
        if len(result.stdout) + len(result.stderr) > 1024 * 1024:
            raise ValueError('Versionsausgabe zu gross.')
        return result


def preflight(outer, spec, approved=False):
    recipe = contract(spec)
    if platform.system() != 'Linux' or os.geteuid() == 0:
        raise ValueError('Security-Build nur als normaler Benutzer unter Linux/WSL.')
    common.checked(outer)
    common.reserve(outer, {'reserve_mb': recipe['disk_mb']})
    memory = dict(line.split(':', 1) for line in Path('/proc/meminfo').read_text().splitlines())
    if int(memory['MemAvailable'].split()[0]) < recipe['ram_mb'] * 1024:
        raise ValueError('Zu wenig freier RAM fuer Security-Build.')
    native_build_deps.prepare(spec, approved=approved)
    command('git')
    isolated([command('true')], outer)
    if spec['id'] == 'testssl':
        for name in TESTSSL_COMMANDS:
            command(name)
        isolated([command('bash'), '--noprofile', '--norc', '-c',
                  'test "${BASH_VERSINFO[0]}" -ge 4'], outer)
    else:
        native_go.prepare(outer, spec, approved=approved)


def git_identity(source, spec, env, run):
    recipe = spec['recipe']
    args = [command('git'), '-c', 'core.hooksPath=' + os.devnull, '-c', 'credential.helper=',
            '-c', 'core.fsmonitor=false', '-C', str(source)]
    child = {**env, 'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_NOSYSTEM': '1',
             'GIT_NOREPLACE_OBJECTS': '1', 'GIT_TERMINAL_PROMPT': '0'}
    if (run(args + ['rev-parse', 'HEAD'], source, child).strip() != recipe['pin']
            or run(args + ['remote', 'get-url', 'origin'], source, child).strip()
            != 'https://github.com/' + recipe['repo'] + '.git'
            or run(args + ['status', '--porcelain', '--untracked-files=all'], source, child).strip()):
        raise ValueError('Quellidentitaet oder sauberer Git-Bestand abweichend.')


def json_stream(text):
    decoder, result = json.JSONDecoder(), []
    text = text.lstrip()
    while text:
        value, end = decoder.raw_decode(text)
        result.append(value)
        text = text[end:].lstrip()
    return result


def go_components(modules):
    components = []
    for module in modules:
        if module.get('Main'):
            continue
        selected = module.get('Replace', module)
        if not selected.get('Version') or not selected.get('Sum', '').startswith('h1:'):
            raise ValueError('Go-Abhaengigkeit ohne feste Version/Pruefsumme; lokale Ersetzungen verboten.')
        components.append(dict(type='library', name=selected['Path'], version=selected['Version'],
                               properties=[dict(name='go.module.h1', value=selected['Sum'])]))
    if not components:
        raise ValueError('Leerer Go-Abhaengigkeitsnachweis.')
    return components


def write_json(path, value):
    common.checked(path)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')
    path.chmod(0o600)


def version_probe(prefix, spec):
    recipe = contract(spec)
    binary = checked_file(prefix / 'bin' / spec['id'])
    result = isolated([binary] + recipe['probe'], prefix)
    stdout = result.stdout.strip()
    combined = stdout + '\n' + result.stderr.strip()
    version = recipe['version']
    if spec['id'] == 'kubescape':
        info = json.loads(stdout)
        valid = info.get('version') == 'v' + version and info.get('commit') == recipe['pin']
    elif spec['id'] == 'nuclei':
        valid = bool(re.search(r'Nuclei Engine Version: v' + re.escape(version) + r'(?![\w.\-])', combined))
    elif spec['id'] == 'trufflehog':
        valid = combined.strip() == 'trufflehog ' + version
    else:
        plain = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', combined)
        valid = bool(re.search(r'(?<![\d.])' + re.escape(version) + r'(?![\w.\-])', plain))
    if not valid:
        raise ValueError('Versionsprobe stimmt nicht mit Buildpin ueberein.')
    return dict(version=version, argv=['bin/' + spec['id']] + recipe['probe'],
                network_isolation='unshare-user-net; fail-closed', timeout_seconds=30,
                credentials_passed=False, scan_performed=False, application_tested=False,
                output_sha256=hashlib.sha256(combined.encode()).hexdigest())


def build(source, prefix, spec, env, run=None):
    recipe = contract(spec)
    prefix, source = common.checked(prefix), common.checked(source)
    if source != prefix / 'source':
        raise ValueError('Quellen muessen im privaten prefix/source liegen.')
    run = run or execute
    source_contracts(source, spec)
    for name in RECEIPTS:
        if (prefix / name).exists():
            raise ValueError('Vorhandene Receipts nicht ueberschreiben.')
    work = common.checked(prefix / '_build/security')
    work.mkdir(parents=True, mode=0o700)
    home = work / 'home'
    home.mkdir(mode=0o700)
    child = dict(PATH=env.get('PATH', SYSTEM_PATH), HOME=str(home), TMPDIR=str(work),
                 LANG='C', LC_ALL='C', GOTOOLCHAIN='local', GOENV='off', GOWORK='off',
                 GOTELEMETRY='off', GOFLAGS='', CGO_ENABLED='0', GOMAXPROCS='1',
                 GOMEMLIMIT='1536MiB', GOPATH=str(work / 'go'), GOCACHE=str(work / 'go-cache'),
                 GOMODCACHE=str(work / 'go-mod'), GOPROXY='https://proxy.golang.org',
                 GOSUMDB='sum.golang.org', GIT_TERMINAL_PROMPT='0',
                 GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1')
    git_identity(source, spec, child, run)
    binary = common.checked(prefix / 'bin' / spec['id'])
    binary.parent.mkdir(exist_ok=True, mode=0o700)
    if binary.exists():
        raise ValueError('Vorhandenes Binary nicht ueberschreiben.')
    artifacts = ['bin/' + spec['id']]
    lock = dict(commit=recipe['pin'], repo=recipe['repo'], recipe_sha256=recipe_hash(spec),
                source_sha256=recipe['source_sha256'], application_tested=False)
    if spec['id'] == 'testssl':
        destination = common.checked(prefix / 'share/testssl')
        destination.mkdir(parents=True, mode=0o700)
        for name in recipe['source_sha256']:
            output = common.checked(destination / name)
            output.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            with output.open('xb') as stream:
                stream.write(checked_file(source / name).read_bytes())
            output.chmod(0o700 if name == 'testssl.sh' else 0o600)
            artifacts.append(output.relative_to(prefix).as_posix())
        with binary.open('x', encoding='ascii', newline='\n') as stream:
            stream.write('#!/bin/bash\nexec /bin/bash --noprofile --norc "${BASH_SOURCE[0]%/*}/../share/testssl/testssl.sh" "$@"\n')
        binary.chmod(0o700)
        # No upstream bin/openssl.* is copied. Only system dependencies are referenced.
        system = []
        for name in TESTSSL_COMMANDS:
            path = Path(command(name)).resolve()
            info = path.stat()
            if not stat.S_ISREG(info.st_mode):
                raise ValueError('Systemabhaengigkeit nicht regulaer.')
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            system.append(dict(name=name, path=str(path), sha256=digest))
        lock.update(scope='pinned-shell-data-and-observed-system-tools; not a reproducible OS lock',
                    system_dependencies=system,
                    system_versions={name: isolated([command(name), flag], prefix).stdout.strip()
                                     for name, flag in [('bash', '--version'), ('openssl', 'version')]})
        components = [dict(type='file', name='testssl/' + name,
                           hashes=[dict(alg='SHA-256', content=digest)])
                      for name, digest in recipe['source_sha256'].items()]
        components += [dict(type='file', name='system/' + item['name'],
                            hashes=[dict(alg='SHA-256', content=item['sha256'])]) for item in system]
    else:
        native_go.activate(prefix.parent, spec, child)
        compiler = run(['go', 'version'], source, child).strip()
        if not native_go.version_ok(compiler, recipe['go_min']):
            raise ValueError('Go-Version ausserhalb des Buildvertrags.')
        run(['go', 'mod', 'download', 'all'], source, child)
        source_contracts(source, spec)
        run(['go', 'mod', 'verify'], source, child)
        offline = {**child, 'GOPROXY': 'off', 'GOSUMDB': 'off', 'GOFLAGS': '-mod=readonly'}
        modules = json_stream(run(['go', 'list', '-m', '-json', 'all'], source, offline))
        components = go_components(modules)
        flags = '-s -w'
        if spec['id'] == 'kubescape':
            flags += ' -X main.version=v' + recipe['version'] + ' -X main.commit=' + recipe['pin']
            flags += ' -X main.date=unknown'
        if spec['id'] == 'trufflehog':
            flags += ' -X github.com/trufflesecurity/trufflehog/v3/pkg/version.BuildVersion=' + recipe['version']
        run(['go', 'build', '-mod=readonly', '-trimpath', '-buildvcs=false', '-p=1',
             '-ldflags', flags, '-o', str(binary), recipe['package']], source, offline)
        checked_file(binary)
        binary.chmod(0o700)
        build_info = run(['go', 'version', '-m', str(binary)], source, offline)
        lock.update(scope='resolved-go-module-graph; not binary reachability', compiler=compiler,
                    compiler_path=shutil.which('go', path=child['PATH']),
                    modules=modules, binary_build_info=build_info,
                    build_argv=['go', 'build', '-mod=readonly', '-trimpath', '-buildvcs=false',
                                '-p=1', '-ldflags', flags, '-o', 'bin/' + spec['id'], recipe['package']])
    source_contracts(source, spec)
    git_identity(source, spec, child, run)
    probe = version_probe(prefix, spec)
    write_json(prefix / RECEIPTS[0], lock)
    write_json(prefix / RECEIPTS[1], dict(bomFormat='CycloneDX', specVersion='1.5', version=1,
               metadata={'properties': [dict(name='scope', value=lock['scope'])]},
               components=[dict(type='application', name=spec['id'], version=recipe['version'])] + components))
    write_json(prefix / RECEIPTS[2], probe)
    artifacts += list(RECEIPTS[:3])
    # The engine's inventory must additionally bind this receipt and all checkout files.
    write_json(prefix / RECEIPTS[3], dict(recipe_sha256=recipe_hash(spec),
               files={name: sha256(prefix / name) for name in artifacts}, application_tested=False))
    return artifacts + [RECEIPTS[3]]


def doctor(prefix, spec):
    """Read-only supplemental check; engine marker/full inventory remains authoritative."""
    contract(spec)
    prefix = common.checked(prefix)
    record = json.loads(checked_file(prefix / RECEIPTS[3]).read_text(encoding='utf-8'))
    if record.get('recipe_sha256') != recipe_hash(spec) or record.get('application_tested') is not False:
        raise ValueError('Security-Receipt passt nicht zum Rezept.')
    files = record.get('files', {})
    if not {'bin/' + spec['id'], *RECEIPTS[:3]} <= files.keys():
        raise ValueError('Security-Artefakte/Receipts unvollstaendig.')
    for name, expected in files.items():
        if sha256(prefix / relative(name)) != expected:
            raise ValueError('Security-Artefakt veraendert: ' + name)
    source_contracts(prefix / 'source', spec)
    return dict(installed=True, scope='native-cli-build-and-local-version-only',
                application_tested=False, scan_performed=False, credentials_passed=False)
