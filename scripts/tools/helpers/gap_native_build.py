"""Reviewed native builders for optional tools; no models, services or providers."""
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

import gap_tools as common

TOOLS = frozenset(('outlines', 'espeak_ng', 'songrec'))


def specification(key, source):
    result = dict(source)
    if key not in TOOLS:
        return result
    result.update(mode='native-build', source_status_only=False, native_tool=key,
                  reserve_mb=8192 if key == 'songrec' else 4096)
    result['contracts'] = dict(source.get('contracts', {}))
    if key == 'songrec':
        # The old source-only pin needs libraries newer than Ubuntu 24.04.
        result.update(pin='15da6b224297d7bf8a9c91b9f70af3d499a9636d', contracts={
            'README.md': '66bca26beca5c0058d5494dd37e0846f93f94eb72b9bdef296bcdb82c16106de',
            'LICENSE': '3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986',
            'Cargo.toml': '2793a5f0df90c4f84c60e6e19693fcced3fc9de213f8066bebf439bb87aea1d0',
            'Cargo.lock': '0079d5a9adf97fdac182051c720a0100f6f4b09e04b04c3c04caf9bfa03cd9ca'})
    elif key == 'outlines':
        result['contracts'].update({
            'pyproject.toml': '9f74a1dde6cca53863235c2aff2d12e96f94ec2ce7888bcd6d0cb92988097b96',
            'uv.lock': '40440e425aa7f94e356e77ca2def1138e10d981138881ad822e183bd0de082f5'})
    else:
        result['contracts']['CMakeLists.txt'] = 'f7c978ca6cb25182697729c4eb083c71547c4f93724bf259a6b654f901835425'
    if key == 'songrec':
        from native_build_deps import SONGREC_PACKAGES
        result['apt_build_deps'] = list(SONGREC_PACKAGES)
    return result


def uv_spec():
    return {'id': 'outlines', 'recipe': {'private_uv': '0.13.5', 'disk_mb': 4096}}


def songrec_dependency_spec():
    from native_build_deps import SONGREC_PACKAGES
    return {'id': 'songrec', 'recipe': {'apt_build_deps': list(SONGREC_PACKAGES)}}


def select_outlines_python(base):
    override = os.environ.get('OUTLINES_PYTHON_BIN')
    if override and not Path(override).is_absolute():
        raise ValueError('OUTLINES_PYTHON_BIN muss ein absoluter Interpreter-Pfad sein.')
    candidates = ([override] if override else [sys.executable] +
                  [shutil.which(name) for name in ('python3.12', 'python3.13', 'python3.11', 'python3.10', 'python3')])
    seen = set()
    env = {key: value for key, value in os.environ.items()
           if key.upper() in ('PATH', 'SYSTEMROOT', 'LANG', 'LC_ALL', 'TEMP', 'TMP')}
    code = 'import sys,ssl,json; assert sys.platform == "linux"; print(json.dumps(list(sys.version_info[:3])))'
    for candidate in candidates:
        if not candidate:
            continue
        try:
            path = Path(candidate).resolve()
            present = path.is_file()
        except (OSError, RuntimeError):
            continue
        if not present or str(path) in seen:
            continue
        seen.add(str(path))
        try:
            version = json.loads(probe([path, '-I', '-S', '-B', '-c', code], base, env))
        except (ValueError, OSError, subprocess.SubprocessError):
            continue
        if (isinstance(version, list) and len(version) == 3 and
                all(type(number) is int for number in version) and
                (3, 10) <= tuple(version[:2]) < (3, 14)):
            print('Outlines: vorhandenes Python', '.'.join(map(str, version)), str(path), flush=True)
            return str(path)
    raise ValueError('Outlines-Pin braucht vorhandenes Python >=3.10 und <3.14; '
                     'Installer-Python ist ' + '.'.join(map(str, sys.version_info[:3])) +
                     '. OUTLINES_PYTHON_BIN auf einen kompatiblen absoluten Pfad setzen; kein Python-Download.')


def preflight(key, base, approved=False):
    if key not in TOOLS or platform.system() != 'Linux':
        raise ValueError('Nativer Build nur unter Linux/WSL; kein Windows-/macOS-Crossbuild.')
    if hasattr(os, 'geteuid') and os.geteuid() == 0:
        raise ValueError('Nativen Tool-Build als normaler Benutzer starten, nicht mit sudo/root.')
    if key == 'songrec':
        if sys.version_info < (3, 11):
            raise ValueError('SongRec-Buildnachweis braucht Python >=3.11 (tomllib).')
        import native_build_deps
        native_build_deps.prepare(songrec_dependency_spec(), approved=approved)
    tools = {'outlines': (), 'espeak_ng': ('cmake', 'make', 'cc'),
             'songrec': ('cargo', 'rustc', 'cc', 'pkg-config', 'msgfmt')}
    for name in tools[key]:
        try:
            common.executable(name)
        except ValueError as error:
            if key == 'espeak_ng':
                raise ValueError('eSpeak NG: ' + name + ' fehlt. Unter Ubuntu separat ausfuehren: '
                                 'sudo apt-get install --no-install-recommends cmake build-essential. '
                                 'Danach erneut installieren; kein Download/Build gestartet.') from error
            raise
    if key == 'outlines':
        python = select_outlines_python(base)
        import native_uv
        native_uv.select(base, uv_spec(), approved=approved, allow_download=approved)
        return python
    if key == 'songrec':
        probe(['pkg-config', '--exists', 'alsa', 'glib-2.0', 'openssl'], base, None)


def probe(args, cwd, env):
    # No audio recording, provider request or model loading in these commands.
    return subprocess.run(list(map(str, args)), cwd=cwd, env=env, check=True,
                          capture_output=True, text=True, timeout=30).stdout


def smoke_command(key, runtime):
    if key == 'outlines':
        return [str(runtime / '.venv/bin/python'), '-I', '-B', '-c',
                'import outlines; from outlines.types import Regex; assert Regex("[a-z]+") is not None']
    if key == 'songrec':
        return [str(runtime / 'target/release/songrec'), '--version']
    if key == 'espeak_ng':
        return [str(runtime / 'install/bin/espeak-ng'), '--version']
    raise ValueError('Unbekanntes natives Tool.')


def build(runtime, env, spec, python=None):
    key = spec['native_tool']
    common.source_contracts(runtime, spec)
    env['NATIVE_BUILD_STREAM'] = 'gap-native'
    run = lambda args: common.run(args, runtime, env)
    if key == 'outlines':
        python = python or select_outlines_python(runtime)
        import native_uv
        native_uv.activate(runtime.parent, uv_spec(), env)
        env.update(UV_NO_CONFIG='1', UV_PYTHON_DOWNLOADS='never',
                   UV_PROJECT_ENVIRONMENT=str(runtime / '.venv'),
                   SETUPTOOLS_SCM_PRETEND_VERSION_FOR_OUTLINES='0.0.0+git.' + spec['pin'][:12],
                   HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1')
        run(['uv', 'sync', '--frozen', '--no-dev', '--no-default-groups', '--no-editable',
             '--no-python-downloads', '--python', python])
        entries = ['.venv/pyvenv.cfg', 'uv.lock']
        python = runtime / '.venv/bin/python'
        components = json.loads(probe([python, '-I', '-B', '-c',
            'import importlib.metadata as m,json; print(json.dumps([dict(type="library",'
            'name=d.metadata["Name"],version=d.version) for d in m.distributions()]))'], runtime, env))
    elif key == 'songrec':
        run(['cargo', 'build', '--release', '--locked', '--no-default-features', '--jobs', '1'])
        entries = ['target/release/songrec', 'Cargo.lock']
        # Record the locked dependency set without running Cargo metadata/network.
        import tomllib
        packages = tomllib.loads((runtime / 'Cargo.lock').read_text(encoding='utf-8'))['package']
        components = [dict(type='library', name=p['name'], version=p['version']) for p in packages]
    elif key == 'espeak_ng':
        run(['cmake', '-S', '.', '-B', 'build', '-DCMAKE_INSTALL_PREFIX=' + str(runtime / 'install'),
             '-DCMAKE_BUILD_TYPE=Release', '-DBUILD_SHARED_LIBS=OFF', '-DENABLE_TESTS=OFF',
             '-DUSE_LIBPCAUDIO=OFF', '-DUSE_LIBSONIC=OFF', '-DUSE_MBROLA=OFF', '-DUSE_SPEECHPLAYER=OFF'])
        run(['cmake', '--build', 'build', '--parallel', '1'])
        run(['cmake', '--install', 'build'])
        entries = ['install/bin/espeak-ng', 'CMakeLists.txt']
        components = [dict(type='application', name='espeak-ng', version='1.53.0')]
    else:
        raise ValueError('Kein freigegebenes natives Buildrezept.')
    probe(smoke_command(key, runtime), runtime, env)
    sbom = runtime / 'native-sbom.cdx.json'
    sbom.write_text(json.dumps(dict(bomFormat='CycloneDX', specVersion='1.5', version=1,
                                   components=components), indent=2) + '\n', encoding='utf-8')
    return entries + ['native-sbom.cdx.json']
