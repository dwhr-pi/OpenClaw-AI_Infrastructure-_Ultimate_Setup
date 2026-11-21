"""Reviewed source-wheel builds for Phoenix, Checkov, Ragas and OpenJarvis; no app starts."""
from email.parser import Parser
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from urllib.request import urlopen
import zipfile

import gap_tools as common
import native_uv
import native_node
import native_build_process
import webinar_releases as releases

ROOT = Path(__file__).resolve().parents[3]
CANDIDATES = ROOT / 'config/native-candidates/python-reviewed.json'
PYTHON = '3.12.12'
BUILD_REQUIREMENTS = ['build==1.3.0', 'hatchling==1.27.0', 'setuptools==80.9.0',
                      'setuptools-scm==9.2.0', 'wheel==0.45.1', 'PyYAML==6.0.3']
PNPM_SHA256 = '72f1630812107c8723eb5be4517725f3e13f09cfd8f71571cf29f23ce318bdb7'
RAGAS_COMPATIBILITY = ('langchain-community==0.3.31', 'langchain>=0.3.27,<1.0',
                       'langchain-core>=0.3.78,<1.0', 'langchain-openai>=0.3,<1.0')


def runtime_compatibility_requirements(spec):
    if spec['id'] != 'ragas':
        return []
    if spec['recipe']['version'] != '0.3.9':
        raise ValueError('Ragas-Kompatibilitaetsbereich nur fuer den geprueften Pin 0.3.9 freigegeben.')
    return list(RAGAS_COMPATIBILITY)


def frontend(outer, spec, approved=False):
    slot = common.checked(outer / 'toolchain/phoenix-frontend')
    marker = common.checked(slot / 'frontend-ready.json')
    env = environment(outer / 'toolchain/phoenix-frontend-state')
    if slot.exists():
        record = json.loads(marker.read_text(encoding='utf-8'))
        files = common.inventory(slot)
        files.pop('frontend-ready.json', None)
        if files != record['files'] or record['pnpm_sha256'] != PNPM_SHA256 or record['node'] != native_node.NODE:
            raise ValueError('Private Phoenix-Frontend-Toolchain geaendert.')
    else:
        if not approved:
            raise ValueError('Private Phoenix-Node/pnpm-Basis braucht --install-build-deps.')
        host = releases.host_key()
        if host not in native_node.ASSETS:
            raise ValueError('Phoenix-Frontend nur fuer Linux amd64/arm64.')
        arch, size, digest, _, _ = native_node.ASSETS[host]
        common.reserve(outer, {'reserve_mb': spec['recipe']['disk_mb'] + 1024})
        slot.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with tempfile.TemporaryDirectory(prefix='phoenix-frontend-', dir=slot.parent) as temporary:
            stage = Path(temporary)
            payload = stage / 'payload'
            payload.mkdir(mode=0o700)
            node_url = 'https://nodejs.org/dist/v' + native_node.NODE + '/node-v' + native_node.NODE + '-linux-' + arch + '.tar.gz'
            native_node.download_node(node_url, stage / 'node.tar.gz', size, digest)
            native_node.unpack_node(stage / 'node.tar.gz', payload / 'node', arch)
            pnpm_url = 'https://registry.npmjs.org/pnpm/-/pnpm-10.2.0.tgz'
            archive = stage / 'pnpm.tgz'
            with urlopen(pnpm_url, timeout=60) as response:
                if response.geturl() != pnpm_url:
                    raise ValueError('Unerwartete pnpm-Download-Umleitung.')
                data = response.read(4390334)
            if len(data) != 4390333 or hashlib.sha256(data).hexdigest() != PNPM_SHA256:
                raise ValueError('pnpm-Download groessen-/hashabweichend.')
            archive.write_bytes(data)
            total = 0
            with tarfile.open(archive, 'r:gz') as bundle:
                for member in bundle:
                    relative = Path(member.name)
                    if relative.is_absolute() or '..' in relative.parts or '\\' in member.name or ':' in member.name:
                        raise ValueError('Unsicherer pnpm-Archivpfad.')
                    if member.isdir():
                        continue
                    total += member.size
                    if not member.isfile() or member.size < 0 or total > 64 * 1024**2:
                        raise ValueError('pnpm-Archiv enthaelt Links/Spezialdateien oder ist zu gross.')
                    target = common.checked(payload / relative)
                    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
                    with bundle.extractfile(member) as source, target.open('xb') as output:
                        shutil.copyfileobj(source, output)
            launcher = payload / 'pnpm'
            launcher.write_text('#!/bin/sh\nexec "${0%/*}/node" "${0%/*}/package/bin/pnpm.cjs" "$@"\n', encoding='ascii')
            launcher.chmod(0o700)
            (payload / 'frontend-ready.json').write_text(json.dumps(dict(
                node=native_node.NODE, node_sha256=digest, pnpm_sha256=PNPM_SHA256,
                files=common.inventory(payload))), encoding='utf-8')
            payload.rename(slot)
    env['PATH'] = str(slot) + os.pathsep + env.get('PATH', '')
    env.update(COREPACK_ENABLE_NETWORK='0', npm_config_manage_package_manager_versions='false')
    if execute([slot / 'node', '--version'], outer, env, 30) != 'v' + native_node.NODE:
        raise ValueError('Private Phoenix-Node-Version abweichend.')
    if execute([slot / 'pnpm', '--version'], outer, env, 30) != '10.2.0':
        raise ValueError('Private Phoenix-pnpm-Version abweichend.')
    return slot


def contract(spec):
    candidates = json.loads(CANDIDATES.read_text(encoding='utf-8'))['tools']
    expected = next((item for item in candidates if item['id'] == spec['id']), None)
    if expected is None or spec['recipe'] != expected['recipe']:
        raise ValueError('Python-Quellvertrag nicht freigegeben; Kandidat und Rezept muessen identisch sein.')
    return spec['recipe']


def environment(base):
    env = {k: v for k, v in os.environ.items() if k in ('PATH', 'LANG', 'LC_ALL')}
    for name in ('home', 'tmp', 'cache'):
        common.checked(base / name).mkdir(mode=0o700, parents=True, exist_ok=True)
    env.update(HOME=str(base / 'home'), USERPROFILE=str(base / 'home'),
               TMPDIR=str(base / 'tmp'), TEMP=str(base / 'tmp'), TMP=str(base / 'tmp'),
               XDG_CONFIG_HOME=str(base / 'home/config'), XDG_CACHE_HOME=str(base / 'cache'),
               UV_CACHE_DIR=str(base / 'cache/uv'), UV_NO_CONFIG='1', UV_KEYRING_PROVIDER='disabled',
               UV_PYTHON_DOWNLOADS='never', UV_NO_PROGRESS='1', UV_CONCURRENT_BUILDS='1',
               UV_CONCURRENT_DOWNLOADS='2', UV_HTTP_TIMEOUT='300', UV_HTTP_CONNECT_TIMEOUT='30',
               UV_HTTP_RETRIES='3', PYTHONDONTWRITEBYTECODE='1',
               DO_NOT_TRACK='1', RAGAS_DO_NOT_TRACK='true', HF_HUB_OFFLINE='1',
               HF_DATASETS_OFFLINE='1', AWS_EC2_METADATA_DISABLED='true',
               PIP_CONFIG_FILE=os.devnull, PIP_DISABLE_PIP_VERSION_CHECK='1',
               npm_config_userconfig=os.devnull, npm_config_cache=str(base / 'cache/npm'), CI='1')
    return env


def failure_details(error):
    """Bound child diagnostics and remove terminal controls/credential-shaped values."""
    parts = []
    for label, value in (('stderr', error.stderr), ('stdout', error.output)):
        if isinstance(value, bytes):
            value = value.decode('utf-8', errors='replace')
        if not value:
            continue
        value = re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', value)
        value = ''.join(char for char in value if char in '\n\t' or char.isprintable())
        value = re.sub(r'(?i)(https?://)[^\s/@]+:[^\s/@]+@', r'\1[redacted]@', value)
        value = re.sub(r'(?i)(\bBearer\s+)\S+', r'\1[redacted]', value)
        value = re.sub(r'''(?ix)((?:api[_-]?key|token|password|secret|authorization)\b["']?\s*[:=]\s*)[^\s,;]+''',
                       r'\1[redacted]', value)
        parts.append(label + ':\n' + value[-6000:])
    return '\n'.join(parts) or 'Keine Kindprozess-Ausgabe vorhanden.'


def execute(args, cwd, env, timeout=7200):
    try:
        result = subprocess.run(list(map(str, args)), cwd=cwd, env=env, capture_output=True,
                                text=True, errors='replace', check=True, timeout=timeout)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        print('Python-Build/Probe fehlgeschlagen; begrenzte bereinigte Diagnose:\n' + failure_details(error),
              flush=True)
        raise
    return result.stdout.strip()


def build_execute(args, cwd, env):
    return native_build_process.run(args, cwd, env, timeout=7200, label='Python-/Frontend-Build')


def frontend_execute(args, cwd, env):
    print('Phoenix-Frontend: kein automatisches Gesamtzeitlimit; manueller Abbruch mit Strg+C. '
          'Netzwerkfehler und pnpm-interne Zeitlimits bleiben moeglich.', flush=True)
    return native_build_process.run(args, cwd, env, timeout=None, label='Phoenix-Frontend-Build')


def install_locked_wheels(args, cwd, env, run=None):
    deadline = time.monotonic() + 7200
    child = dict(env)
    for attempt in range(2):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise subprocess.TimeoutExpired(args, 7200)
        print('Hashgesperrte Wheel-Installation: Versuch', attempt + 1,
              'von 2; Restbudget:', round(remaining), 's.', flush=True)
        try:
            if run is not None:
                return run(args, cwd, child)
            return native_build_process.run(args, cwd, child, timeout=remaining,
                                            label='Hashgesperrte Wheel-Installation')
        except subprocess.CalledProcessError as error:
            output = '\n'.join(value.decode('utf-8', errors='replace') if isinstance(value, bytes) else value
                               for value in (error.output, error.stderr) if value).lower()
            permanent = any(message in output for message in (
                'hash mismatch', 'does not match the expected hash', 'certificate',
                'unauthorized', 'forbidden', '401', '403', 'no space left',
                'disk quota', 'permission denied'))
            network_timeout = 'failed to download' in output and (
                'network timeout' in output or 'timed out' in output)
            dns_failure = 'failed to download' in output and any(message in output for message in (
                'dns error', 'failed to lookup address information', 'name resolution'))
            temporary_dns = dns_failure and any(message in output for message in (
                'temporary failure in name resolution', 'eai_again', '[errno -3]'))
            if dns_failure and not permanent:
                print('DNS-/Namensaufloesung fuer die Python-Paketquelle fehlgeschlagen; '
                      'kein Modell- oder Quellbuildfehler. Keine Aenderung an DNS, WSL oder TLS.', flush=True)
            if attempt or permanent or not (network_timeout or temporary_dns) or time.monotonic() >= deadline:
                if dns_failure and not permanent:
                    raise ValueError('Python-Paketdownload wegen DNS-/Namensaufloesung abgebrochen; '
                                     'Installation unvollstaendig. Kein weiterer automatischer Versuch, '
                                     'kein Wechsel der Paketquelle oder DNS-Konfiguration.') from error
                raise
            # Retry only installation against the same lock and cache, never resolution/build.
            child = dict(child, UV_HTTP_TIMEOUT='900', UV_CONCURRENT_DOWNLOADS='1')
            reason = 'voruebergehenden DNS-Fehler' if temporary_dns else 'Netzwerk-Timeout'
            print('Wheel-Download durch ' + reason + ' abgebrochen. Ein letzter Versuch mit'
                  ' 900s HTTP-Lesefenster und einem parallelen Download im selben 7200s-Budget.'
                  ' Gleiche Lockdatei, Hashpflicht, Paketquelle und TLS-Pruefung; kein neuer Build.', flush=True)


def select_python(outer, spec, approved=False):
    slot = common.checked(outer / 'toolchain/python-reviewed-312')
    env = environment(common.checked(outer / 'toolchain/python-reviewed-state'))
    explicit = os.environ.get('NATIVE_SOURCE_PYTHON_BIN')
    candidates = [explicit] if explicit else [shutil.which('python3.12'), sys.executable]
    for candidate in candidates:
        if not candidate:
            continue
        try:
            execute([candidate, '-I', '-B', '-c',
                     'import sys,ssl,venv; assert sys.implementation.name == "cpython"; '
                     'assert sys.version_info[:2] == (3,12); print(sys.executable)'], outer, env, 30)
            return str(Path(candidate).resolve())
        except (OSError, subprocess.SubprocessError):
            if explicit:
                raise ValueError('Explizites NATIVE_SOURCE_PYTHON_BIN braucht CPython 3.12 mit SSL/venv.')
    marker = common.checked(slot / 'python-ready.json')
    if slot.exists():
        record = json.loads(marker.read_text(encoding='utf-8'))
        files = common.inventory(slot)
        files.pop('python-ready.json', None)
        relative = Path(record['entry'])
        if (relative.is_absolute() or '..' in relative.parts or ':' in str(relative)
                or '\\' in record['entry'] or files != record['files']):
            raise ValueError('Private Python-Laufzeit geaendert; keine Ersetzung.')
        python = slot / relative
        if not python.resolve().is_relative_to(slot.resolve()):
            raise ValueError('Privater Python-Pfad verlaesst Toolchain.')
        execute([python, '-I', '-B', '-c',
                 'import sys,ssl,venv; assert sys.version_info[:3] == (3,12,12)'], outer, env, 30)
        return str(python)
    if not approved:
        raise ValueError('Private CPython-3.12.12-Basis erforderlich: --install-build-deps bewusst freigeben.')
    common.reserve(outer, {'reserve_mb': spec['recipe']['disk_mb'] + 1024})
    uv = native_uv.select(outer, spec, approved=True, allow_download=True)
    slot.mkdir(mode=0o700, parents=True)
    env.update(UV_PYTHON_INSTALL_DIR=str(slot / 'managed'), UV_PYTHON_DOWNLOADS='manual')
    try:
        execute([uv, 'python', 'install', PYTHON, '--no-bin', '--no-config'], outer, env)
        python = Path(execute([uv, 'python', 'find', PYTHON, '--managed-python',
                               '--no-python-downloads', '--no-config'], outer, env))
        if not python.is_absolute() or not python.is_file() or not python.resolve().is_relative_to(slot.resolve()):
            raise ValueError('uv lieferte keine private Python-Laufzeit.')
        execute([python, '-I', '-B', '-c',
                 'import sys,ssl,venv; assert sys.version_info[:3] == (3,12,12)'], outer, env, 30)
        marker.write_text(json.dumps({'entry': python.relative_to(slot).as_posix(),
                                      'provider': 'uv-0.13.5/python-build-standalone',
                                      'files': common.inventory(slot)}), encoding='utf-8')
    except BaseException:
        shutil.rmtree(common.checked(slot))
        raise
    return str(python)


def preflight(outer, spec, approved=False):
    contract(spec)
    if platform.system() != 'Linux':
        raise ValueError('Dieses native Python-Buildrezept braucht Linux/WSL, keinen Windows-Crossbuild.')
    common.reserve(outer, {'reserve_mb': spec['recipe']['disk_mb']})
    native_uv.select(outer, spec, approved=approved, allow_download=approved)
    select_python(outer, spec, approved=approved)
    if spec['id'] == 'phoenix':
        frontend(outer, spec, approved=approved)


def verify_source(source, recipe):
    if (common.git(source, 'rev-parse', 'HEAD') != recipe['pin'] or
            common.git(source, 'remote', 'get-url', 'origin') != 'https://github.com/' + recipe['repo'] + '.git'):
        raise ValueError('Git-Quellidentitaet abweichend.')
    for name, digest in recipe['source_sha256'].items():
        path = common.checked(source / name)
        if not path.resolve().is_relative_to(source.resolve()) or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError('Quellhash abweichend: ' + name)


def inspect_wheel(wheel, recipe):
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        if recipe['distribution'] == 'arize-phoenix':
            if 'phoenix/server/static/.vite/manifest.json' not in names or not any(
                    n.startswith('phoenix/server/static/assets/') and n.endswith('.js') for n in names):
                raise ValueError('Phoenix-Wheel ohne kompiliertes Frontend.')
        if recipe['distribution'] == 'checkov' and not any(
                '/checks/graph_checks/' in n and n.endswith('.json') for n in names):
            raise ValueError('Checkov-Wheel ohne generierte Graph-Policies.')
        if recipe['distribution'] == 'ragas' and 'ragas/_version.py' not in names:
            raise ValueError('Ragas-Wheel ohne erzeugte SCM-Version.')
        if recipe['distribution'] == 'OpenJarvis' and not {
                'openjarvis/__init__.py', 'openjarvis/cli/__init__.py'}.issubset(names):
            raise ValueError('OpenJarvis-Wheel ohne CLI-/SDK-Basis.')
        if recipe['distribution'] == 'OpenJarvis':
            metadata_paths = [n for n in names if n.endswith('.dist-info/METADATA') and n.count('/') == 1]
            if len(metadata_paths) != 1:
                raise ValueError('OpenJarvis-Wheel braucht genau eine Paketmetadatei.')
            metadata = Parser().parsestr(archive.read(metadata_paths[0]).decode('utf-8'))
            if (metadata.get_all('Name') != [recipe['distribution']] or
                    metadata.get_all('Version') != [recipe['version']]):
                raise ValueError('OpenJarvis-Wheel: Paketname/Buildversion abweichend; '
                                 'keine Runtime-Abhaengigkeiten installiert.')


def probe_script(recipe):
    # Keep Popen a real class: imports can subclass it or use Popen[str] annotations.
    return '''import importlib, importlib.metadata as m, json, os, socket, subprocess, sys
%s
def denied(*args, **kwargs):
    raise RuntimeError("Runtime-Probe erlaubt kein Netzwerk/Unterprozess")
def audit_runtime(event, args):
    if event in {"subprocess.Popen", "os.system", "os.posix_spawn", "os.fork", "os.forkpty",
                 "socket.connect", "socket.bind", "socket.getaddrinfo", "socket.gethostbyname",
                 "socket.gethostbyaddr", "socket.sendto", "socket.sendmsg"}:
        if event == "subprocess.Popen" and %r:
            # GitPython handles a denied executable in its documented quiet refresh mode.
            raise PermissionError("Runtime-Probe blockiert Audit-Ereignis: " + event)
        raise RuntimeError("Runtime-Probe blockiert Audit-Ereignis: " + event)
sys.addaudithook(audit_runtime)
socket.socket.connect = denied
socket.socket.connect_ex = denied
socket.create_connection = denied
socket.getaddrinfo = denied
socket.socket.bind = denied
assert sys.prefix != sys.base_prefix
module = importlib.import_module(%r)
assert m.version(%r) == %r
%s
rows = sorted([{"name": d.metadata["Name"], "version": d.version} for d in m.distributions()], key=lambda d: d["name"].lower())
print(json.dumps({"version": m.version(%r), "module": module.__name__, "distributions": rows,
                  "application_tested": False, "network_allowed": False, "process_allowed": False,
                  "git_runtime_tested": False,
                  "guard": "cpython-audit-hook-and-socket-guards", "scan_performed": False}))
''' % ('os.environ["GIT_PYTHON_REFRESH"] = "quiet"' if recipe['distribution'] == 'ragas' else '',
       recipe['distribution'] == 'ragas', recipe['import_module'], recipe['distribution'], recipe['version'],
       {'ragas': 'assert callable(module.evaluate) and callable(module.aevaluate)\n'
                 'assert importlib.import_module("git").GIT_OK is False',
        'arize-phoenix': 'assert callable(module.launch_app)',
        'checkov': 'importlib.import_module("checkov.common.util.type_forcers")',
        'OpenJarvis': 'assert any(e.name == "jarvis" and e.value == "openjarvis.cli:main" '
                     'for e in m.distribution("OpenJarvis").entry_points)'}[recipe['distribution']],
       recipe['distribution'])


def build(source, prefix, spec, env, run=None):
    recipe = contract(spec)
    source, prefix = common.checked(Path(source)), common.checked(Path(prefix))
    if source != prefix / 'source':
        raise ValueError('Buildquelle muss im eigenen nativen Praefix liegen.')
    verify_source(source, recipe)
    runner = run or build_execute
    child = environment(common.checked(prefix / '_python-build'))
    uv = native_uv.select(prefix.parent, spec, allow_download=False)
    python = select_python(prefix.parent, spec)
    wheelhouse = common.checked(prefix / 'wheels')
    wheelhouse.mkdir(mode=0o700)
    build_python = prefix / 'build-venv/bin/python'
    vpython = prefix / 'venv/bin/python'
    for venv in ('build-venv', 'venv'):
        runner([uv, 'venv', '--python', python, '--no-python-downloads', str(prefix / venv)], prefix, child)
    build_input = prefix / 'build-requirements.in'
    requirements = BUILD_REQUIREMENTS + (['hatch-vcs==0.5.0'] if spec['id'] == 'openjarvis' else [])
    build_input.write_text('\n'.join(requirements) + '\n', encoding='ascii')
    index = ['--index-url', 'https://pypi.org/simple', '--no-config', '--keyring-provider', 'disabled']

    def locked_install(input_file, lock, target):
        print('uv-Downloadbudget: HTTP-Lesen 300s, Verbindung 30s, hoechstens 3 HTTP-Wiederholungen, '
              '2 parallele Downloads; Prozesslimit weiterhin 7200s. Kein Index-/TLS-/Hash-Fallback.', flush=True)
        runner([uv, 'pip', 'compile', str(input_file), '--python', str(target),
                '--generate-hashes', '--only-binary', ':all:', '--output-file', str(lock), *index], prefix, child)
        install_locked_wheels([uv, 'pip', 'install', '--python', str(target), '--require-hashes',
                               '--only-binary', ':all:', '-r', str(lock), *index], prefix, child, run=run)

    locked_install(build_input, prefix / 'build-requirements.lock', build_python)
    if spec['id'] == 'phoenix':
        frontend_runner = run or frontend_execute
        slot = frontend(prefix.parent, spec)
        child['PATH'] = str(slot) + os.pathsep + child.get('PATH', '')
        child.update(COREPACK_ENABLE_NETWORK='0', npm_config_manage_package_manager_versions='false',
                     PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD='1')
        # Skip the npx preinstall hook: the pinned pnpm is already selected directly.
        frontend_runner([slot / 'pnpm', 'install', '--frozen-lockfile', '--ignore-scripts'], source / 'app', child)
        frontend_runner([slot / 'pnpm', 'rebuild', 'esbuild'], source / 'app', child)
        frontend_runner([slot / 'pnpm', 'run', 'build'], source / 'app', child)
        if not (source / 'src/phoenix/server/static/.vite/manifest.json').is_file():
            raise ValueError('Phoenix-UI-Build lieferte kein Vite-Manifest.')
    if spec['id'] == 'ragas':
        child['SETUPTOOLS_SCM_PRETEND_VERSION_FOR_RAGAS'] = recipe['version']
    elif spec['id'] == 'openjarvis':
        # hatch-vcs calls get_version without dist_name, so the generic override is required.
        child['SETUPTOOLS_SCM_PRETEND_VERSION'] = recipe['version']
        child['SETUPTOOLS_SCM_PRETEND_VERSION_FOR_OPENJARVIS'] = recipe['version']
    runner([build_python, '-I', '-B', '-m', 'build', '--wheel', '--no-isolation',
            '--outdir', str(wheelhouse), str(source)], source, child)
    wheels = list(wheelhouse.glob('*.whl'))
    if len(wheels) != 1:
        raise ValueError('Genau ein lokales Source-Wheel erforderlich.')
    wheel = common.checked(wheels[0])
    inspect_wheel(wheel, recipe)
    runtime_input = prefix / 'runtime-requirements.in'
    compatibility = runtime_compatibility_requirements(spec)
    runtime_input.write_text('\n'.join([str(wheel), *compatibility]) + '\n', encoding='utf-8')
    locked_install(runtime_input, prefix / 'runtime-requirements.lock', vpython)
    runner([uv, 'pip', 'check', '--python', str(vpython), '--no-config'], prefix, child)
    cli = common.checked(prefix / 'venv/bin' / recipe['cli'])
    if not cli.is_file():
        raise ValueError('Installierter CLI-Einstieg fehlt.')
    # The bounded probe always uses the local executor, never a long-running build runner.
    print(spec['name'] + ': begrenzte Offline-Importprobe (45s); kein Dienst-/Modellstart.', flush=True)
    report = json.loads(execute([vpython, '-I', '-B', '-c', probe_script(recipe)], prefix, child, 45))
    verify_source(source, recipe)
    wheel_name = wheel.relative_to(prefix).as_posix()
    receipt = dict(commit=recipe['pin'], source_sha256=recipe['source_sha256'],
                   wheel=wheel_name, wheel_sha256=hashlib.sha256(wheel.read_bytes()).hexdigest(),
                   python=python, probe=report, application_tested=False,
                   runtime_compatibility_requirements=compatibility,
                   dependency_scope='resolved-at-install; hashes enforced; not an upstream audited dependency lock')
    (prefix / 'python-build-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    components = [dict(type='library', name=row['name'], version=row['version'],
                       purl='pkg:pypi/' + row['name'].lower().replace('_', '-') + '@' + row['version'])
                  for row in report['distributions']]
    sbom = dict(bomFormat='CycloneDX', specVersion='1.5', version=1, components=components,
                metadata={'properties': [{'name': 'scope', 'value': 'installed Python distributions; not source reachability or security scan'}]})
    (prefix / 'python-sbom.cdx.json').write_text(json.dumps(sbom, indent=2) + '\n', encoding='utf-8')
    return [wheel_name, 'venv/pyvenv.cfg', 'venv/bin/' + recipe['cli'],
            'build-requirements.in', 'build-requirements.lock', 'runtime-requirements.in',
            'runtime-requirements.lock', 'python-build-receipt.json', 'python-sbom.cdx.json']
