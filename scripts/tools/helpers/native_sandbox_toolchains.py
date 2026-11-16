"""Consent-gated private compiler assets for sandbox candidates; no global changes."""
import json
import os
from pathlib import Path
import platform
import shutil
import tarfile
import tempfile
import time
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, build_opener

from native_sandbox_candidates import checked, regular, sha256, command, write_json, BAZEL_HASHES


RUST_HASHES = {
    'x86_64': ('0a8787303c88b018af61b5c53a0c7024d516d175e623eeab35a35eab11dbcad0',
               '5c5bc94af02797b699bb7d4e85b356192eab9fb50376053a1e6edf509fcf7129',
               '0c43618128a7a6b96b0b04c04cf7b28dd52fb0991a74c9615fbd1a684ff88712',
               '9744b43bed4a89db05e83dc8054d3e92e23ddb70a6c08c54ccde9a58d7b28627'),
    'aarch64': ('06a71688ee297515ebc6a815e42c779735c09423b0bed056e0896c80c7295399',
                '71f0457abe8fdf9fc048009f867acc27b21e25c8e06a1a3e9a12c637833b6aab',
                'b6a90dab26527f17e7e395e24b2d79976e30432c41feb073fe920d3b26b709a0',
                '91b55028112e6a978386de46013820d921330f0a182d11900f117e9f0f4ef338')}


class Redirect(HTTPRedirectHandler):
    max_redirections = 3

    def __init__(self, hosts):
        self.hosts = hosts

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urlsplit(newurl)
        if parsed.scheme != 'https' or parsed.hostname not in self.hosts or parsed.username or parsed.password:
            raise ValueError('Toolchain-Redirect ausserhalb offizieller HTTPS-Hosts.')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download(url, path, digest):
    host = urlsplit(url).hostname
    if host not in ('static.rust-lang.org', 'github.com') or not url.startswith('https://'):
        raise ValueError('Nicht freigegebener Toolchain-Host.')
    hosts = {host} if host == 'static.rust-lang.org' else {host, 'release-assets.githubusercontent.com', 'objects.githubusercontent.com'}
    started, total = time.monotonic(), 0
    with build_opener(Redirect(hosts)).open(url, timeout=30) as response, checked(path).open('xb') as out:
        while True:
            if time.monotonic() - started > 600:
                raise ValueError('Toolchain-Download-Zeitbudget 600s ueberschritten.')
            block = response.read(1024**2)
            if not block:
                break
            total += len(block)
            if total > 512 * 1024**2:
                raise ValueError('Toolchain-Download groesser als 512 MiB.')
            out.write(block)
    if sha256(path) != digest:
        raise ValueError('Toolchain-SHA256 weicht ab; keine Ausfuehrung.')


def inventory(root):
    result = {}
    for path in sorted(checked(root).rglob('*')):
        checked(path)
        if path.is_dir():
            continue
        if len(result) >= 60000:
            raise ValueError('Toolchain-Dateibudget ueberschritten.')
        result[path.relative_to(root).as_posix()] = sha256(path)
    return result


def rust_assets(machine):
    host = machine + '-unknown-linux-gnu'
    target = machine + '-unknown-linux-musl'
    parts = [('rustc', host), ('cargo', host), ('rust-std', host), ('rust-std', target)]
    return [('https://static.rust-lang.org/dist/2026-07-09/' + name + '-1.97.0-' + triple + '.tar.xz', digest)
            for (name, triple), digest in zip(parts, RUST_HASHES[machine])]


def extract(archive, destination):
    total, seen = 0, set()
    with tarfile.open(regular(archive), 'r:xz') as bundle:
        for entry in bundle:
            path = Path(entry.name)
            if (path.is_absolute() or '..' in path.parts or '\\' in entry.name or ':' in entry.name or
                    not path.parts or entry.name in seen or len(seen) >= 60000 or
                    not (entry.isdir() or entry.isfile())):
                raise ValueError('Unsicheres Rust-Komponentenarchiv; keine Links/Spezialdateien.')
            seen.add(entry.name)
            total += entry.size
            if entry.size < 0 or total > 2 * 1024**3:
                raise ValueError('Rust-Entpackbudget ueberschritten.')
            target = checked(destination / path)
            if entry.isdir():
                target.mkdir(parents=True, exist_ok=True, mode=0o700)
            else:
                target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
                with bundle.extractfile(entry) as src, target.open('xb') as dst:
                    shutil.copyfileobj(src, dst)
                target.chmod(0o700 if entry.mode & 0o111 else 0o600)


def ensure(base, key, approved=False):
    """Called under the central operation lock; never adopts or overwrites unknown trees."""
    base = checked(base)
    parent = checked(base / 'toolchain')
    machine = platform.machine()
    label = 'bazel-9.3.1' if key == 'gvisor' else 'rust-1.97.0-musl'
    slot = checked(parent / (label + '-' + machine))
    assets = ([('https://github.com/bazelbuild/bazel/releases/download/9.3.1/bazel-9.3.1-linux-' +
                ('x86_64' if machine == 'x86_64' else 'arm64'), BAZEL_HASHES[machine])]
              if key == 'gvisor' else rust_assets(machine))
    if slot.exists():
        marker = regular(slot / 'toolchain-ready.json')
        data = json.loads(marker.read_text())
        files = inventory(slot / 'root')
        if data != dict(assets=assets_as_json(assets), files=files):
            raise ValueError('Private Sandbox-Toolchain veraendert; keine Reparatur/Loeschung.')
        return slot / 'root'
    if not approved:
        raise ValueError('Privater ' + label + '-Download benoetigt --install-build-deps; keine Aenderung.')
    parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with tempfile.TemporaryDirectory(prefix='sandbox-toolchain-', dir=parent) as temporary:
        stage = checked(temporary)
        root = stage / 'root'
        root.mkdir(mode=0o700)
        env = {k: v for k, v in os.environ.items() if k in ('PATH', 'LANG', 'LC_ALL')}
        home = stage / 'home'
        home.mkdir(mode=0o700)
        env.update(HOME=str(home), RUSTUP_AUTO_INSTALL='0')
        for index, (url, digest) in enumerate(assets):
            archive = stage / ('asset-' + str(index))
            download(url, archive, digest)
            if key == 'gvisor':
                (root / 'bin').mkdir(mode=0o700)
                shutil.copyfile(archive, root / 'bin/bazel')
                (root / 'bin/bazel').chmod(0o700)
            else:
                unpack = stage / ('unpack-' + str(index))
                unpack.mkdir(mode=0o700)
                extract(archive, unpack)
                dirs = list(unpack.iterdir())
                if len(dirs) != 1 or not dirs[0].is_dir():
                    raise ValueError('Rust-Archivwurzel unerwartet.')
                installer = regular(dirs[0] / 'install.sh')
                command(['sh', installer, '--prefix=' + str(root), '--disable-ldconfig'], dirs[0], env)
        # Publish only the installed root and immutable ownership record, not temporary archives.
        payload = stage / 'payload'
        payload.mkdir(mode=0o700)
        root.rename(payload / 'root')
        write_json(payload / 'toolchain-ready.json', dict(assets=assets_as_json(assets), files=inventory(payload / 'root')))
        if slot.exists():
            raise ValueError('Toolchain-Ziel inzwischen belegt.')
        payload.rename(slot)
    return slot / 'root'


def assets_as_json(assets):
    return [{'url': url, 'sha256': digest} for url, digest in assets]


def activate(base, key, env, approved=False):
    if key == 'kata_containers':
        import private_go
        import native_go
        def validate(binary, root, target):
            actual = command([binary, 'version'], base, {**env, 'GOROOT': str(root), 'GOTOOLCHAIN': 'local'}, probe=True)
            if not native_go.version_ok(actual, [1, 26, 9]):
                raise ValueError('Go >=1.26.9 erforderlich.')
        current = shutil.which('go', path=env.get('PATH', ''))
        if current and native_go.version_ok(command([current, 'version'], base, {**env, 'GOTOOLCHAIN': 'local'}, probe=True), [1, 26, 9]):
            return
        slot = checked(base / 'toolchain' / (private_go.VERSION + '-' + private_go.target()[0]))
        if not slot.exists() and not approved:
            raise ValueError('Private Go-Basis benoetigt --install-build-deps.')
        binary, root = private_go.ensure(base, validate)
        env.update(PATH=str(Path(binary).parent) + os.pathsep + env.get('PATH', ''), GOROOT=str(root))
    else:
        if key == 'gvisor':
            current = shutil.which('bazel', path=env.get('PATH', ''))
            if current and sha256(Path(current).resolve()) == BAZEL_HASHES[platform.machine()]:
                return
        if key == 'firecracker' and (env.get('NATIVE_SOURCE_RUST_TOOLCHAIN') or os.environ.get('NATIVE_SOURCE_RUST_TOOLCHAIN')):
            return  # An explicit user override is verified by the builder; never replaced.
        root = ensure(base, key, approved)
        env['PATH'] = str(root / 'bin') + os.pathsep + env.get('PATH', '')
        if key == 'firecracker':
            env['NATIVE_SOURCE_RUST_TOOLCHAIN'] = str(root)
