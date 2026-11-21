"""Native sandbox candidate hooks. No activation, guest execution or CRI changes."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import signal
import stat
import subprocess
import sys
import tarfile
import tempfile

import native_build_process


SIDECARS = ('gvisor_sentry', 'checkpointgofer', 'runsc-metric-server',
            'runsc-netgofer', 'runsc-fd-parking', 'gvisor-sentry-prewarmer',
            'gvisor-proc-umounter')
GVISOR_FILES = ('runsc', 'containerd-shim-runsc-v1') + tuple('gvisor-bin/' + x for x in SIDECARS)
PINS = {'gvisor': 'a0e6be6fb5e03d8ebea13592f36a097c7e9a41b9',
        'firecracker': 'eaf83bb718a559d324613d566eaf776b31a62340',
        'kata_containers': '03cf2ec06a5d302f23af811744f6bcea49988bfb'}
BAZEL_HASHES = {'x86_64': '7f775b54bbec487efaf0f49ccda1d2ed02cd34f582edfdd6aeeec76e39ef585c',
                'aarch64': '10ba9cb76d4ee748d274dcc2981992bb12b74a203dc41a9c2eceeb8f29359366'}
KATA_TIMEOUTS = {
    'download': ('KATA_GO_DOWNLOAD_TIMEOUT_SECONDS', 1800, 30, 7200),
    'verify': ('KATA_GO_VERIFY_TIMEOUT_SECONDS', 300, 30, 1800),
    'build': ('KATA_GO_BUILD_TIMEOUT_SECONDS', 7200, 300, 21600),
}


class KataPhaseError(ValueError):
    """Fixed phase codes, without process output, paths or environment values."""


def kata_timeouts(env):
    result = {}
    for phase, (name, default, minimum, maximum) in KATA_TIMEOUTS.items():
        value = env.get(name, os.environ.get(name, str(default)))
        if (not isinstance(value, str) or re.fullmatch(r'[0-9]{1,5}', value) is None
                or not minimum <= int(value) <= maximum):
            raise KataPhaseError('kata_go_' + phase + '_timeout_invalid')
        result[phase] = int(value)
    return result


def kata_go_phases(module, prefix, item, env, run=None):
    """Stream bounded Go phases; a tail buffer is not a complete JSON document."""
    timeouts = kata_timeouts(env)
    env = dict(env)
    env.update(GOTOOLCHAIN='local', GOENV='off', GOWORK='off', GOFLAGS='-mod=readonly -p=2')
    commands = {
        'download': ['go', 'mod', 'download', '-json'],
        'verify': ['go', 'mod', 'verify'],
        'build': ['make', '-j2', 'runtime', 'containerd-shim-v2',
                  'VERSION=' + item['version'], 'PREFIX=' + str(prefix)],
    }
    for phase, args in commands.items():
        try:
            def check_locks():
                for name in ('go.mod', 'go.sum'):
                    expected = item['source_sha256']['src/runtime/' + name]
                    if sha256(module / name) != expected:
                        raise KataPhaseError('kata_go_' + phase + '_source_contract_changed')

            check_locks()
            print('Kata Go Phase:', phase, 'Zeitbudget:', timeouts[phase],
                  's; Heartbeat ist kein Fortschrittsnachweis.', flush=True)
            if run is None:
                native_build_process.run(args, module, env, timeout=timeouts[phase],
                                         heartbeat=30, label='Kata-Go-' + phase)
            else:
                # Preserve the existing three-argument test-runner contract.
                run(args, Path(module), env)
            check_locks()
        except KataPhaseError:
            raise
        except subprocess.TimeoutExpired:
            raise KataPhaseError('kata_go_' + phase + '_timeout') from None
        except KeyboardInterrupt:
            raise KataPhaseError('kata_go_' + phase + '_interrupted') from None
        except Exception:
            raise KataPhaseError('kata_go_' + phase + '_failed') from None


def checked(path):
    path = Path(path).absolute()
    for part in (path, *path.parents):
        if part.is_symlink() or (part.exists() and getattr(part.lstat(), 'st_file_attributes', 0) & 0x400):
            raise ValueError('Symlink/Reparse-Punkt im verwalteten Pfad: ' + str(part))
    return path


def regular(path):
    path = checked(path)
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise ValueError('Nur regulaere, einfach verlinkte Dateien: ' + str(path))
    return path


def sha256(path):
    digest = hashlib.sha256()
    with regular(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def execute(args, cwd, env, timeout=7200, capture=False):
    """Bound process lifetime and captured output; kill the whole native process group."""
    with tempfile.TemporaryFile() as output:
        proc = subprocess.Popen(list(map(str, args)), cwd=cwd, env=env,
                                stdout=output if capture else None,
                                stderr=subprocess.STDOUT, start_new_session=os.name == 'posix')
        try:
            code = proc.wait(timeout=timeout)
        except BaseException:
            if os.name == 'posix':
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            else:
                proc.kill()
            proc.wait()
            raise
        if code:
            raise subprocess.CalledProcessError(code, args)
        if capture:
            if output.tell() > 65536:
                raise ValueError('Probe-Ausgabe ueberschreitet 64 KiB.')
            output.seek(0)
            return output.read().decode('utf-8', errors='replace').strip()
    return ''


def command(args, cwd, env, run=None, probe=False):
    if run is not None:
        result = run(list(map(str, args)), Path(cwd), env)
        if probe and (not isinstance(result, str) or len(result.encode()) > 65536):
            raise ValueError('Injected Runner muss begrenzten Text zurueckgeben.')
        return result
    return execute(args, cwd, env, timeout=20 if probe else 7200, capture=probe)


def recipe(spec):
    key = spec['id']
    result = spec['recipe']
    if key not in PINS or result['pin'] != PINS[key] or result['kind'] != 'candidate-native':
        raise ValueError('Nicht freigegebener Sandbox-Buildvertrag.')
    return key, result


def executable(name, env):
    value = shutil.which(name, path=env.get('PATH', ''))
    if not value:
        raise ValueError('Vorhandenes Buildwerkzeug fehlt: ' + name)
    return str(Path(value).resolve())


LIBCLANG_PROBE = '''import ctypes,glob,json,pathlib,re,sys
patterns = ('/usr/lib/llvm-*/lib/libclang.so*',
            '/usr/lib/*-linux-gnu/libclang-*.so*',
            '/usr/lib/libclang*.so*', '/usr/lib64/libclang*.so*')
candidates = sorted(set(p for pattern in patterns for p in glob.glob(pattern)),
                    key=lambda p: tuple(map(int,re.findall(r'[0-9]+',p))), reverse=True)
for name in candidates[:64]:
    path = pathlib.Path(name).resolve()
    if not any(path.is_relative_to(root) for root in ('/usr/lib','/usr/lib64')):
        continue
    try:
        library = ctypes.CDLL(str(path))
        for symbol in ('clang_getClangVersion','clang_createIndex','clang_disposeIndex'):
            getattr(library,symbol)
    except (OSError,AttributeError):
        continue
    print(json.dumps({'library':str(path)}))
    sys.exit(0)
sys.exit(1)
'''


def require_libclang(cwd, env, run=None):
    # Load only a host library in a time-bounded child, never inside the installer.
    child = {key: value for key, value in env.items() if key in ('PATH', 'LANG', 'LC_ALL')}
    try:
        result = command([sys.executable, '-I', '-B', '-c', LIBCLANG_PROBE], cwd, child, run, True)
        value = json.loads(result)
        if not isinstance(value, dict) or set(value) != {'library'} or not isinstance(value['library'], str):
            raise ValueError('invalid probe')
        path = Path(value['library'])
        if (not path.is_absolute() or '..' in path.parts
                or not any(path.is_relative_to(root) for root in (Path('/usr/lib'), Path('/usr/lib64')))
                or not re.fullmatch(r'libclang(?:-[0-9.]+)?\.so(?:\.[0-9.]+)?', path.name)):
            raise ValueError('invalid library')
    except Exception:
        raise ValueError('Firecracker: ladbare Host-libclang mit Clang-C-API fehlt; '
                         'Buildabhaengigkeit libclang-dev im Voraussetzungen-Dialog freigeben. '
                         'Kein Cargo-Build gestartet.') from None
    env['LIBCLANG_PATH'] = str(path.parent)
    return str(path)


def toolchains(key, cwd, env, run=None):
    versions = {}
    if key == 'gvisor':
        bazel = executable('bazel', env)
        if sha256(bazel) != BAZEL_HASHES[platform.machine()]:
            raise ValueError('Offizielle Bazel-9.3.1-Binary mit gepinntem SHA256 erforderlich; kein Bazelisk.')
        versions['bazel'] = command([bazel, '--version'], cwd, env, run, True)
        if versions['bazel'] != 'bazel 9.3.1':
            raise ValueError('Bazel 9.3.1 erforderlich.')
    elif key == 'firecracker':
        versions['libclang'] = require_libclang(cwd, env, run)
        # Resolve rustup proxies to an already installed sysroot before invoking Cargo.
        selected = env.get('NATIVE_SOURCE_RUST_TOOLCHAIN') or os.environ.get('NATIVE_SOURCE_RUST_TOOLCHAIN')
        if not selected or not Path(selected).is_absolute():
            raise ValueError('NATIVE_SOURCE_RUST_TOOLCHAIN auf vorhandene Rust-1.97.0-Toolchain setzen.')
        root = checked(selected)
        for name in ('cargo', 'rustc'):
            regular(root / 'bin' / name)
        env.update(PATH=str(root / 'bin') + os.pathsep + env.get('PATH', ''),
                   RUSTUP_TOOLCHAIN=str(root), RUSTUP_AUTO_INSTALL='0')
        versions['rustc'] = command([root / 'bin/rustc', '--version'], cwd, env, run, True)
        if not re.match(r'^rustc 1\.97\.0(?: |$)', versions['rustc']):
            raise ValueError('Rust 1.97.0 erforderlich.')
        target = platform.machine() + '-unknown-linux-musl'
        if not checked(root / 'lib/rustlib' / target / 'lib').is_dir():
            raise ValueError('Vorhandene Rust-musl-Standardbibliothek fehlt: ' + target)
        versions['cargo'] = command([root / 'bin/cargo', '--version'], cwd, env, run, True)
        env['CC'] = executable('musl-gcc', env)
        env['CARGO_TARGET_' + target.upper().replace('-', '_') + '_LINKER'] = env['CC']
    else:
        env.update(GOTOOLCHAIN='local', GOENV='off', GOWORK='off', GOFLAGS='-mod=readonly -p=2')
        versions['go'] = command(['go', 'version'], cwd, env, run, True)
        from native_go import version_ok
        if not version_ok(versions['go'], [1, 26, 9]):
            raise ValueError('Go >=1.26.9 erforderlich; GOTOOLCHAIN=local.')
    return versions


def preflight(outer, spec, approved=False):
    """Consent-gated shared dependencies/private compilers, never runtime activation."""
    key, item = recipe(spec)
    if key == 'kata_containers':
        kata_timeouts({})
    if platform.system() != 'Linux' or platform.machine() not in BAZEL_HASHES:
        raise ValueError('Nur natives Linux x86_64/aarch64; kein Crossbuild.')
    if os.geteuid() == 0:
        raise ValueError('Build als normaler Benutzer, nicht root.')
    path = checked(outer)
    while not path.exists():
        path = path.parent
    if shutil.disk_usage(path).free < item['disk_mb'] * 1024**2:
        raise ValueError('Nicht genug freier Speicher fuer den Sandbox-Build.')
    memory = dict(line.split(':', 1) for line in Path('/proc/meminfo').read_text().splitlines())
    if int(memory['MemAvailable'].split()[0]) < item['ram_mb'] * 1024:
        raise ValueError('Nicht genug verfuegbarer RAM fuer den Sandbox-Build.')
    import native_build_deps
    native_build_deps.prepare(spec, approved=approved)
    env = {name: value for name, value in os.environ.items() if name in ('PATH', 'LANG', 'LC_ALL')}
    if key == 'firecracker':
        require_libclang(path, env)
    for name in set(item['tools']) - {'go', 'bazel'}:
        executable(name, env)
    if not Path(outer).exists():
        if not approved:
            raise ValueError('Privates Ziel fehlt; Einrichtung benoetigt --install-build-deps.')
        checked(outer).mkdir(parents=True, mode=0o700)
    from native_sandbox_toolchains import activate
    activate(checked(outer), key, env, approved)
    return toolchains(key, path, env)


def verify_source(source, spec, env, run=None):
    _, item = recipe(spec)
    if command(['git', 'rev-parse', 'HEAD'], source, env, run, True) != item['pin']:
        raise ValueError('Source-Commit weicht ab.')
    origin = command(['git', 'remote', 'get-url', 'origin'], source, env, run, True)
    if origin.removesuffix('.git') != 'https://github.com/' + item['repo']:
        raise ValueError('Source-Origin weicht ab.')
    command(['git', 'diff', '--exit-code', 'HEAD', '--'], source, env, run)
    hashes = item['source_sha256']
    if not hashes:
        raise ValueError('Leerer Quellvertrag.')
    for name, digest in hashes.items():
        if PurePosixPath(name).is_absolute() or '..' in PurePosixPath(name).parts or '\\' in name:
            raise ValueError('Unsicherer Quellvertragspfad.')
        if not re.fullmatch('[0-9a-f]{64}', digest) or sha256(source / name) != digest:
            raise ValueError('Quellhash weicht ab: ' + name)


def copy_binary(source, destination):
    source = regular(source)
    with source.open('rb') as stream:
        header = stream.read(20)
    machine = {'x86_64': 62, 'aarch64': 183}[platform.machine()]
    if len(header) != 20 or header[:6] != b'\x7fELF\x02\x01' or int.from_bytes(header[18:20], 'little') != machine:
        raise ValueError('Kein passendes natives 64-Bit-ELF-Artefakt: ' + str(source))
    destination = checked(destination)
    destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with source.open('rb') as src, destination.open('xb') as dst:
        shutil.copyfileobj(src, dst)
    destination.chmod(0o755)


def extract_gvisor(bundle, prefix):
    """Never use extractall: reject traversal, links, devices and incomplete bundles."""
    seen, total, outputs = set(), 0, []
    with tarfile.open(regular(bundle), 'r:bz2') as archive:
        for index, member in enumerate(archive):
            if index >= 64:
                raise ValueError('Zu viele Release-Tar-Eintraege.')
            name = member.name.removeprefix('./')
            if member.isdir() and name.rstrip('/') in ('', '.', 'gvisor-bin'):
                continue
            if name not in GVISOR_FILES or name in seen or not member.isfile():
                raise ValueError('Unerwarteter/unsicherer Release-Tar-Eintrag: ' + name)
            total += member.size
            if member.size <= 0 or member.size > 1024**3 or total > 2 * 1024**3:
                raise ValueError('Release-Tar-Groessenbudget ueberschritten.')
            seen.add(name)
            target = checked(prefix / 'bin' / name)
            target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            with archive.extractfile(member) as src, tempfile.TemporaryDirectory(dir=prefix) as temporary:
                candidate = Path(temporary) / 'binary'
                with candidate.open('xb') as dst:
                    shutil.copyfileobj(src, dst)
                copy_binary(candidate, target)
            outputs.append(target.relative_to(prefix).as_posix())
    if seen != set(GVISOR_FILES):
        raise ValueError('Unvollstaendiges gVisor-Bundle; Sidecars/Shim fehlen.')
    return sorted(outputs)


def write_json(path, value):
    with checked(path).open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(value, indent=2, sort_keys=True) + '\n')


def probe(prefix, spec, env, run=None):
    """Only explicit --version invocations, with 20s/64KiB limits in the default runner."""
    key, item = recipe(spec)
    names = {'gvisor': ('runsc', 'containerd-shim-runsc-v1'),
             'firecracker': ('firecracker', 'jailer'),
             'kata_containers': ('kata-runtime', 'containerd-shim-kata-v2')}[key]
    result = {}
    for name in names:
        binary = regular(Path(prefix) / 'bin' / name)
        output = command([binary, '--version'], prefix, env, run, True)
        if not output or (key != 'gvisor' and item['version'] not in output):
            raise ValueError('Versionsprobe fehlgeschlagen: ' + name)
        result[name] = output
    return result


def build(source, prefix, spec, env, run=None):
    """Return prefix-relative owned artifacts. Caller supplies fresh private staging tree."""
    key, item = recipe(spec)
    if key == 'kata_containers':
        kata_timeouts(env)
    source, prefix = checked(source), checked(prefix)
    if not source.is_relative_to(prefix):
        raise ValueError('Source muss im privaten Prefix liegen.')
    env = dict(env)
    verify_source(source, spec, env, run)
    if run is None:
        from native_sandbox_toolchains import activate
        activate(prefix.parent, key, env)
    versions = toolchains(key, prefix, env, run)
    work = checked(prefix / '_sandbox-build')
    work.mkdir(mode=0o700)
    receipts = checked(prefix / 'sandbox-receipts')
    receipts.mkdir(mode=0o700)
    components, locks = [], []
    if key == 'gvisor':
        bazel = executable('bazel', env)
        args = [bazel, '--nosystem_rc', '--nohome_rc', '--batch',
                '--output_user_root=' + str(work / 'bazel'), 'build',
                '--config=' + platform.machine(), '--compilation_mode=opt', '--jobs=2',
                '--lockfile_mode=update', '--repository_cache=' + str(work / 'repository-cache'),
                '//debian:gvisor-release-tar-bz2']
        command(args, source, env, run)
        bundle = source / 'bazel-bin/debian/gvisor.tar.bz2'
        # bazel-bin is an upstream output symlink: only its resolved owned target is accepted.
        bundle = bundle.resolve(strict=True)
        if not bundle.is_relative_to(work):
            raise ValueError('Bazel-Bundle liegt ausserhalb des privaten Buildcaches.')
        artifacts = extract_gvisor(bundle, prefix)
        lock = regular(source / 'MODULE.bazel.lock')
        if not json.loads(lock.read_text()).get('lockFileVersion'):
            raise ValueError('Erzeugter Bazel-Aufloesungslock fehlt.')
        shutil.copyfile(lock, receipts / 'MODULE.bazel.lock')
        locks.append('sandbox-receipts/MODULE.bazel.lock')
        # Preserve the original generated bundle for independent checksum/replay inspection.
        shutil.copyfile(bundle, receipts / 'gvisor.tar.bz2')
        artifacts.append('sandbox-receipts/gvisor.tar.bz2')
    elif key == 'firecracker':
        target = platform.machine() + '-unknown-linux-musl'
        env.update(CARGO_TARGET_DIR=str(work / 'cargo-target'), CARGO_BUILD_JOBS='2')
        command(['cargo', 'build', '--release', '--locked', '--target', target,
                 '-p', 'firecracker', '-p', 'jailer', '--jobs', '2'], source, env, run)
        artifacts = []
        for name in ('firecracker', 'jailer'):
            copy_binary(work / 'cargo-target' / target / 'release' / name, prefix / 'bin' / name)
            artifacts.append('bin/' + name)
        import tomllib
        for package in tomllib.loads((source / 'Cargo.lock').read_text())['package']:
            component = dict(type='library', name=package['name'], version=package['version'])
            if package.get('checksum'):
                component['hashes'] = [{'alg': 'SHA-256', 'content': package['checksum']}]
            components.append(component)
        shutil.copyfile(source / 'Cargo.lock', receipts / 'Cargo.lock')
        locks.append('sandbox-receipts/Cargo.lock')
    else:
        module = source / 'src/runtime'
        kata_go_phases(module, prefix, item, env, run)
        artifacts = []
        for name in ('kata-runtime', 'containerd-shim-kata-v2'):
            copy_binary(module / name, prefix / 'bin' / name)
            artifacts.append('bin/' + name)
        # go.sum is a checksum catalogue, not proof of the entire resolved module graph.
        for name in ('go.mod', 'go.sum'):
            shutil.copyfile(module / name, receipts / name)
            locks.append('sandbox-receipts/' + name)
    # Dependency locks are immutable for Cargo/Go; Bazel's new resolution is recorded, not pre-approved.
    for name, digest in item['source_sha256'].items():
        if sha256(source / name) != digest:
            raise ValueError('Build hat gepinnten Quellvertrag veraendert: ' + name)
    versions['artifacts'] = probe(prefix, spec, env, run)
    artifacts += locks
    hashes = {name: sha256(prefix / name) for name in artifacts}
    for name, digest in hashes.items():
        components.append(dict(type='file', name=name, hashes=[{'alg': 'SHA-256', 'content': digest}]))
    scope = item['acceptance']
    write_json(receipts / 'build-lock.json', dict(source='https://github.com/' + item['repo'],
               commit=item['pin'], source_sha256=item['source_sha256'], artifact_sha256=hashes,
               toolchains=versions, acceptance=scope, runtime_tested=False,
               dependency_scope='Cargo.lock packages or Go checksum catalogue or generated Bazel resolution; not a hermetic OS/toolchain lock'))
    write_json(receipts / 'sbom.cdx.json', dict(bomFormat='CycloneDX', specVersion='1.5', version=1,
               components=components, metadata={'properties': [
                   {'name': 'scope', 'value': 'partial: artifact files, dependency locks; Cargo package catalogue only for Firecracker'},
                   {'name': 'acceptance', 'value': scope}]}))
    write_json(receipts / 'version-probes.json', versions)
    return artifacts + ['sandbox-receipts/build-lock.json', 'sandbox-receipts/sbom.cdx.json',
                        'sandbox-receipts/version-probes.json']
