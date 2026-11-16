"""Isolated candidate-native hooks. Build only; never launch applications."""
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import stat
import subprocess
import tomllib
import zipfile

import gap_tools as common
import native_build_process

IDS = {'milvus', 'vaultwarden', 'owasp_zap'}
REQUIRED = {
    'milvus': {'go.mod', 'go.sum', 'internal/core/conanfile.py',
               'internal/core/CMakeLists.txt', 'scripts/3rdparty_build.sh',
               'internal/http/webui/index.html', 'configs/milvus.yaml'},
    'vaultwarden': {'Cargo.toml', 'Cargo.lock', 'rust-toolchain.toml', 'src/main.rs', 'build.rs', '.env.template'},
    'owasp_zap': {'zap/zap.gradle.kts', 'zap/gradle.properties', 'gradle/wrapper/gradle-wrapper.properties',
                  'buildSrc/src/main/kotlin/org/zaproxy/zap/distributions.gradle.kts'},
}


def recipe(spec):
    if spec.get('id') not in IDS or spec['recipe'].get('kind') != 'candidate-native':
        raise ValueError('Unbekannter candidate-native Vertrag.')
    value = spec['recipe']
    if not re.fullmatch('[0-9a-f]{40}', value.get('pin', '')):
        raise ValueError('Voller Commit-Pin fehlt.')
    hashes = value.get('source_sha256', {})
    if not REQUIRED[spec['id']] <= hashes.keys():
        raise ValueError('Quellvertraege unvollstaendig.')
    for name, digest in hashes.items():
        relative(name)
        if not re.fullmatch('[0-9a-f]{64}', digest):
            raise ValueError('Ungueltiger SHA256.')
    return value


def relative(name):
    if (not isinstance(name, str) or not name or name.startswith(('/', '-')) or
            '\\' in name or ':' in name or '..' in Path(name).parts):
        raise ValueError('Unsicherer relativer Pfad.')
    return Path(name)


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()


def write(path, value):
    common.checked(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        stream.write(value if isinstance(value, str) else json.dumps(value, indent=2) + '\n')


def versions(args, cwd, env):
    result = subprocess.run(list(map(str, args)), cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                            capture_output=True, text=True, check=True, timeout=30)
    return (result.stdout + result.stderr).strip()


def rust_environment(spec, env, cwd):
    root = Path(os.environ.get('NATIVE_SOURCE_RUST_TOOLCHAIN', ''))
    if not root.is_absolute() or not (root / 'bin/rustc').is_file() or not (root / 'bin/cargo').is_file():
        raise ValueError('NATIVE_SOURCE_RUST_TOOLCHAIN: vorhandene absolute Rust-Toolchain erforderlich; kein rustup-Download.')
    env.update(RUSTUP_TOOLCHAIN=str(root), RUSTUP_AUTO_INSTALL='0',
               PATH=str(root / 'bin') + os.pathsep + env.get('PATH', ''))
    observed = versions([root / 'bin/rustc', '--version'], cwd, env)
    if observed.split()[1] != spec['recipe']['rust_exact']:
        raise ValueError('Rust-Pin abweichend: ' + observed)
    return observed


def tool_versions(outer, spec, env):
    value = recipe(spec)
    observed = {}
    for name in value['tools']:
        executable = shutil.which(name, path=env.get('PATH', ''))
        if not executable:
            raise ValueError('Buildbasis fehlt: ' + name + '; separat bereitstellen, kein apt/Fallback.')
        flag = '-version' if name == 'java' else '--version'
        if name == 'go':
            flag = 'version'
        observed[name] = versions([executable, flag], outer, env)
    if spec['id'] in ('milvus', 'vaultwarden'):
        observed['rustc'] = rust_environment(spec, env, outer)
    if spec['id'] == 'milvus':
        if 'Conan version 2.25.1' != observed['conan']:
            raise ValueError('Conan 2.25.1 erforderlich.')
        match = re.search(r'go(\d+)\.(\d+)\.(\d+)', observed['go'])
        if not match or tuple(map(int, match.groups())) < (1, 26, 9):
            raise ValueError('Go >=1.26.9 erforderlich; GOTOOLCHAIN=local, kein Download.')
        match = re.search(r'cmake version (\d+)\.(\d+)', observed['cmake'])
        if not match or tuple(map(int, match.groups())) < (3, 26):
            raise ValueError('CMake >=3.26 erforderlich.')
        if not re.search(r'\b(?:1[2-9]|[2-9][0-9])\.\d', observed['gcc']):
            raise ValueError('GCC >=12 erforderlich.')
    elif spec['id'] == 'owasp_zap':
        if not re.search(r'Gradle 8\.13(?:\s|$)', observed['gradle']):
            raise ValueError('Vorhandenes Gradle 8.13 erforderlich; Wrapper wird nicht ausgefuehrt.')
        if not re.search(r'(?:version |javac )"?21(?:\.|\s|\")', observed['java']):
            raise ValueError('JDK 21 erforderlich (Gradle/Error Prone); kein JDK-Download.')
        if not observed['javac'].startswith('javac 21'):
            raise ValueError('javac 21 erforderlich.')
    return observed


def preflight(outer, spec, approved=False):
    value = recipe(spec)
    if platform.system() != 'Linux' or platform.machine() != 'x86_64':
        raise ValueError('Dieser Kandidatenvertrag gilt nur fuer Linux x86_64, kein Crossbuild.')
    outer = common.checked(Path(outer))
    existing = outer
    while not existing.exists():
        existing = existing.parent
    if shutil.disk_usage(existing).free < value['disk_mb'] * 1024**2:
        raise ValueError('Diskreserve unterschritten: ' + str(value['disk_mb']) + ' MiB.')
    # WSL virtual free space does not represent the backing Windows volume.
    if Path('/mnt/c').is_dir() and shutil.disk_usage('/mnt/c').free < value['disk_mb'] * 1024**2:
        raise ValueError('Windows-Backing-Volume hat nicht genug Diskreserve.')
    memory = dict(line.split(':', 1) for line in Path('/proc/meminfo').read_text().splitlines())
    if int(memory['MemAvailable'].split()[0]) < value['ram_mb'] * 1024:
        raise ValueError('RAM-Reserve unterschritten.')
    if spec['id'] == 'milvus' and not re.search(r'\bavx\b', Path('/proc/cpuinfo').read_text()):
        raise ValueError('Dieser Milvus-x86_64-Build benoetigt AVX.')
    env = {k: v for k, v in os.environ.items() if k in ('PATH', 'LANG', 'LC_ALL')}
    env.update(GOTOOLCHAIN='local', GOENV='off', RUSTUP_AUTO_INSTALL='0')
    return tool_versions(existing, spec, env)


def verify_source(source, spec):
    value = recipe(spec)
    if (common.git(source, 'rev-parse', 'HEAD') != value['pin'] or
            common.git(source, 'remote', 'get-url', 'origin') != 'https://github.com/' + value['repo'] + '.git'):
        raise ValueError('Quell-Pin/Origin abweichend.')
    for name, expected in value['source_sha256'].items():
        path = common.checked(source / relative(name))
        if not path.is_file() or digest(path) != expected:
            raise ValueError('Quellvertrag abweichend: ' + name)


def collect(prefix, root):
    results = []
    for parent, directories, files in os.walk(root, followlinks=False):
        for name in directories:
            common.checked(Path(parent) / name)
        for name in files:
            path = Path(parent) / name
            # Materialize only links wholly inside the private install tree.
            if path.is_symlink():
                target = path.resolve(strict=True)
                if not target.is_relative_to(prefix.resolve()) or not target.is_file():
                    raise ValueError('Externes Artefaktlinkziel; keine Runtime-Freigabe.')
                content = target.read_bytes()
                path.unlink()
                path.write_bytes(content)
            common.checked(path)
            info = path.stat()
            if not stat.S_ISREG(info.st_mode) or info.st_size == 0:
                raise ValueError('Leeres/Spezial-Artefakt: ' + str(path))
            results.append(path.relative_to(prefix).as_posix())
    return sorted(results)


def cargo_components(lock):
    components = []
    for package in tomllib.loads(lock.read_text(encoding='utf-8'))['package']:
        entry = dict(type='library', name=package['name'], version=package['version'])
        if package.get('checksum'):
            entry['hashes'] = [{'alg': 'SHA-256', 'content': package['checksum']}]
        if package.get('source'):
            entry['properties'] = [{'name': 'source', 'value': package['source']}]
        components.append(entry)
    return components


def vaultwarden(source, prefix, spec, env, run):
    env.update(VW_VERSION=spec['recipe']['version'], CARGO_BUILD_JOBS='2',
               CARGO_TARGET_DIR=str(prefix / '_build/cargo-target'))
    run(['cargo', 'build', '--locked', '--release', '--no-default-features', '--features', 'sqlite',
         '--bin', 'vaultwarden'], source, env)
    binary = common.checked(prefix / '_build/cargo-target/release/vaultwarden')
    destination = prefix / 'bin/vaultwarden'
    destination.parent.mkdir(exist_ok=True)
    shutil.copy2(binary, destination)
    write(prefix / 'config/vaultwarden.env.example',
          'WEB_VAULT_ENABLED=false\nSIGNUPS_ALLOWED=false\nROCKET_ADDRESS=127.0.0.1\n'
          'ROCKET_PORT=8000\nDATA_FOLDER=@DATA@\n')
    write(prefix / 'config/upstream.env.example', (source / '.env.template').read_text(encoding='utf-8'))
    write(prefix / 'locks/Cargo.lock', (source / 'Cargo.lock').read_text(encoding='utf-8'))
    return ['bin/vaultwarden'], cargo_components(source / 'Cargo.lock')


def milvus(source, prefix, spec, env, run):
    env.update(CONAN_HOME=str(prefix / '_build/conan-home'), CONAN_CPU_COUNT='2', jobs='2',
               CARGO_BUILD_JOBS='2', GOTOOLCHAIN='local', GOENV='off', GOWORK='off', CGO_ENABLED='1',
               CMAKE_BUILD_PARALLEL_LEVEL='2', CMAKE_POLICY_VERSION_MINIMUM='3.5')
    core = source / 'internal/core'
    output = core / 'output'
    cmake = source / 'cmake_build'
    cmake.mkdir()
    # Reuse only the reviewed upstream shared-library hook, not its installer script.
    text = (source / 'scripts/3rdparty_build.sh').read_text(encoding='utf-8')
    hook = text.split("cat > \"$CONAN_HOME_DIR/extensions/hooks/hook_fix_shared_lib_env.py\" << 'HOOK_EOF'\n", 1)[1].split('\nHOOK_EOF', 1)[0]
    write(prefix / '_build/conan-home/extensions/hooks/hook_fix_shared_lib_env.py', hook)
    run(['conan', 'profile', 'detect'], source, env)
    run(['conan', 'remote', 'add', 'milvus', spec['recipe']['conan_remote'], '--index', '0'], source, env)
    settings = ['-s', 'build_type=Release', '-s', 'compiler.cppstd=20', '-s:b', 'compiler.cppstd=20']
    lock = prefix / 'locks/conan.lock'
    lock.parent.mkdir(exist_ok=True)
    run(['conan', 'lock', 'create', str(core), *settings, '--lockfile-out=' + str(lock)], source, env)
    run(['conan', 'install', str(core), *settings, '--lockfile=' + str(lock), '--build=*',
         '--output-folder=' + str(cmake / 'conan')], source, env)
    graph = run(['conan', 'graph', 'info', str(core), *settings, '--lockfile=' + str(lock), '--format=json'], source, env)
    write(prefix / 'locks/conan-graph.json', json.loads(graph))
    run(['cmake', '-S', str(core), '-B', str(cmake),
         '-DCMAKE_TOOLCHAIN_FILE=' + str(cmake / 'conan/conan_toolchain.cmake'),
         '-DCMAKE_INSTALL_PREFIX=' + str(output), '-DCMAKE_BUILD_TYPE=Release',
         '-DBUILD_UNIT_TEST=OFF', '-DMILVUS_GPU_VERSION=OFF', '-DBUILD_DISK_ANN=OFF',
         '-DUSE_DYNAMIC_SIMD=ON', '-DCPU_ARCH=avx', '-DWITH_SVS=OFF',
         '-DMILVUS_USE_PCH=OFF', '-DMAKE_BUILD_ARGS=-j2'], source, env)
    run(['cmake', '--build', str(cmake), '--parallel', '2'], source, env)
    run(['cmake', '--install', str(cmake)], source, env)
    libraries = [output / 'lib', output / 'lib64', cmake / 'lib']
    libpath = ':'.join(map(str, libraries))
    env.update(PKG_CONFIG_PATH=':'.join(str(p / 'pkgconfig') for p in libraries[:2]),
               LIBRARY_PATH=libpath, LD_LIBRARY_PATH=libpath, GOFLAGS='-mod=readonly')
    run(['go', 'mod', 'download'], source, env)
    run(['go', 'mod', 'verify'], source, env)
    flags = '-checklinkname=0 -r ' + libpath
    flags += ' -X github.com/milvus-io/milvus/cmd/milvus.MilvusVersion=' + spec['recipe']['version']
    flags += ' -X github.com/milvus-io/milvus/cmd/milvus.GitCommit=' + spec['recipe']['pin']
    (prefix / 'bin').mkdir(exist_ok=True)
    run(['go', 'build', '-mod=readonly', '-trimpath', '-p=2', '-ldflags', flags,
         '-tags', 'dynamic,sonic,with_jemalloc,bytedance_tango', '-o', str(prefix / 'bin/milvus'), './cmd/main.go'], source, env)
    modules = run(['go', 'list', '-m', '-json', 'all'], source, env)
    write(prefix / 'locks/go-modules.jsonstream', modules)
    write(prefix / 'locks/go.sum', (source / 'go.sum').read_text())
    write(prefix / 'config/milvus.yaml.example', (source / 'configs/milvus.yaml').read_text())
    entries = ['bin/milvus']
    entries += collect(prefix, output)
    entries += collect(prefix, cmake / 'lib')
    if not any(Path(x).name == 'libmilvus_core.so' for x in entries):
        raise ValueError('Milvus Core-Library fehlt.')
    nodes = json.loads(graph)['graph']['nodes'].values()
    components = [dict(type='library', name=n['ref'].split('/')[0], version=n['ref'].split('/', 1)[1],
                       properties=[{'name': 'scope', 'value': 'conan-resolved-recipe-reference'}])
                  for n in nodes if n.get('ref')]
    lockfiles = sorted(source.glob('internal/core/**/Cargo.lock'))
    for index, item in enumerate(lockfiles):
        write(prefix / ('locks/rust-' + str(index) + '.lock'), item.read_text())
        components += cargo_components(item)
    decoder = json.JSONDecoder()
    remaining = modules.strip()
    while remaining:
        item, end = decoder.raw_decode(remaining)
        components.append(dict(type='library', name=item['Path'], version=item.get('Version', 'local')))
        remaining = remaining[end:].lstrip()
    return entries, components


GRADLE_LOCKS = '''allprojects {
    dependencyLocking { lockAllConfigurations() }
}
'''


def zap(source, prefix, spec, env, run):
    init = prefix / 'locks/candidate-locks.gradle'
    write(init, GRADLE_LOCKS)
    args = ['gradle', '--no-daemon', '--max-workers=2', '--console=plain',
            '-Dorg.gradle.java.installations.auto-download=false', '-I', str(init)]
    run(args + ['--write-locks', '--write-verification-metadata', 'sha256', ':zap:distFiles'], source, env)
    dist = source / 'zap/build/distFiles'
    jar = dist / ('zap-' + spec['recipe']['version'] + '.jar')
    if not jar.is_file() or not (dist / 'lib').is_dir() or not (dist / 'xml/config.xml').is_file():
        raise ValueError('ZAP Core-Distribution unvollstaendig.')
    bom = source / 'zap/build/reports/bom-runtime/bom.json'
    upstream = json.loads(bom.read_text(encoding='utf-8'))
    write(prefix / 'locks/upstream-runtime-sbom.json', upstream)
    for index, lock in enumerate(sorted(source.rglob('gradle.lockfile'))):
        write(prefix / ('locks/gradle-' + str(index) + '.lockfile'), lock.read_text())
    if not list((prefix / 'locks').glob('gradle-*.lockfile')):
        raise ValueError('Gradle-Abhaengigkeitslock fehlt.')
    write(prefix / 'locks/gradle-verification-metadata.xml', (source / 'gradle/verification-metadata.xml').read_text())
    if list(dist.rglob('*.zap')):
        raise ValueError('Unerwartetes Add-on im Core-Vertrag.')
    entries = collect(prefix, dist)
    return entries, upstream['components']


def probe(prefix, spec):
    """Offline artifact inspection, deliberately not a running-service test."""
    prefix = common.checked(Path(prefix))
    key = spec['id']
    if key not in IDS:
        raise ValueError('Unbekanntes Probe-Ziel.')
    if key == 'owasp_zap':
        path = common.checked(prefix / ('source/zap/build/distFiles/zap-' + spec['recipe']['version'] + '.jar'))
        with zipfile.ZipFile(path) as jar:
            if len(jar.infolist()) > 100000 or sum(x.file_size for x in jar.infolist()) > 512 * 1024**2:
                raise ValueError('JAR-Pruefbudget ueberschritten.')
            if jar.testzip() or 'org/zaproxy/zap/ZAP.class' not in jar.namelist():
                raise ValueError('ZAP-JAR defekt.')
            manifest = jar.read('META-INF/MANIFEST.MF').decode()
            if 'Implementation-Version: ' + spec['recipe']['version'] not in manifest:
                raise ValueError('ZAP-Version abweichend.')
    else:
        path = common.checked(prefix / 'bin' / key)
        with path.open('rb') as stream:
            header = stream.read(20)
        if len(header) != 20 or header[:6] != b'\x7fELF\x02\x01' or header[18:20] != b'\x3e\x00':
            raise ValueError('Kein Linux-x86_64-ELF-Artefakt.')
        if not path.stat().st_mode & stat.S_IXUSR:
            raise ValueError('Ausfuehrungsbit fehlt.')
    return dict(artifact_probe_passed=True, runtime_tested=False, service_started=False,
                network_probe=False, doctor_exit=3)


def build(source, prefix, spec, env, run=None):
    source, prefix = common.checked(Path(source)), common.checked(Path(prefix))
    if source != prefix / 'source':
        raise ValueError('Erwartet source == prefix/source.')
    verify_source(source, spec)
    env = {k: v for k, v in env.items() if k in {
        'PATH', 'HOME', 'USERPROFILE', 'TEMP', 'TMP', 'TMPDIR', 'LANG', 'LC_ALL',
        'CARGO_HOME', 'RUSTUP_HOME', 'GOPATH', 'GOCACHE', 'GOMODCACHE', 'GRADLE_USER_HOME'}}
    env.update(GOTOOLCHAIN='local', GOENV='off', RUSTUP_AUTO_INSTALL='0', CI='1',
               GIT_TERMINAL_PROMPT='0', GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1',
               GIT_LFS_SKIP_SMUDGE='1', CARGO_NET_GIT_FETCH_WITH_CLI='false')
    observed = tool_versions(prefix, spec, env)
    executor = run or (lambda args, cwd, env: native_build_process.run(args, cwd, env, timeout=14400))
    entries, components = {'milvus': milvus, 'vaultwarden': vaultwarden, 'owasp_zap': zap}[spec['id']](
        source, prefix, spec, env, executor)
    verify_source(source, spec)
    result = probe(prefix, spec)
    if spec['id'] != 'owasp_zap':
        key = spec['id']
        write(prefix / ('config/' + key + '.service.example'),
              '[Unit]\nDescription=' + key + ' (manuell konfigurieren)\n'
              '[Service]\nType=simple\nWorkingDirectory=@DATA@\n'
              'EnvironmentFile=@ENV_FILE@\nExecStart=@PREFIX@/bin/' + key +
              (' run standalone' if key == 'milvus' else '') + '\n'
              'NoNewPrivileges=true\nPrivateTmp=true\nProtectSystem=strict\n'
              'ProtectHome=read-only\nReadWritePaths=@DATA@\nUMask=0077\n'
              '[Install]\nWantedBy=default.target\n')
    components.insert(0, dict(type='application', name=spec['id'], version=spec['recipe']['version']))
    write(prefix / 'candidate-sbom.cdx.json', dict(bomFormat='CycloneDX', specVersion='1.5', version=1,
          metadata={'properties': [{'name': 'scope', 'value': spec['recipe']['scope']},
                                   {'name': 'limitations', 'value': 'OS/toolchain/build-plugin closure not complete; not a vulnerability audit'}]},
          components=components))
    write(prefix / 'candidate-build-lock.json', dict(commit=spec['recipe']['pin'], source_sha256=spec['recipe']['source_sha256'],
          tool_versions=observed, scope=spec['recipe']['scope'], reproducible_build_claim=False))
    entries += collect(prefix, prefix / 'locks') + collect(prefix, prefix / 'config')
    entries += ['candidate-sbom.cdx.json', 'candidate-build-lock.json']
    write(prefix / 'candidate-artifact-receipt.json', dict(**result, commit=spec['recipe']['pin'],
          scope=spec['recipe']['scope'], files={name: digest(common.checked(prefix / relative(name))) for name in entries}))
    return sorted(set(entries + ['candidate-artifact-receipt.json']))


def doctor(prefix, spec):
    """Validate immutable returned artifacts without executing any application."""
    value = recipe(spec)
    prefix = common.checked(Path(prefix))
    receipt = json.loads(common.checked(prefix / 'candidate-artifact-receipt.json').read_text())
    if receipt.get('commit') != value['pin'] or not receipt.get('files'):
        raise ValueError('Unbekannter Artefaktnachweis.')
    for name, expected in receipt['files'].items():
        if digest(common.checked(prefix / relative(name))) != expected:
            raise ValueError('Artefakt veraendert: ' + name)
    return probe(prefix, spec)
