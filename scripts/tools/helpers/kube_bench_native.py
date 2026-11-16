"""Pinned kube-bench build receipts; never starts a host/cluster benchmark."""
import hashlib
import json
import re
import subprocess

import gap_tools as common


def configuration_hashes(prefix):
    root = common.checked(prefix / 'source/cfg')
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_file():
            path = common.checked(path)
            result[path.relative_to(prefix).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    if 'source/cfg/config.yaml' not in result or len(result) < 2:
        raise ValueError('Kube Bench: Benchmark-Konfiguration fehlt oder ist unvollstaendig.')
    return result


def prepare(prefix, spec, env):
    hashes = spec['recipe']['source_sha256']
    expected = {'LICENSE', 'go.mod', 'go.sum', 'cmd/version.go', 'cfg/config.yaml'}
    if set(hashes) != expected or any(not re.fullmatch('[0-9a-f]{64}', value) for value in hashes.values()):
        raise ValueError('Kube Bench: ungueltiger Quellvertrag.')
    for name, digest in hashes.items():
        if hashlib.sha256(common.checked(prefix / 'source' / name).read_bytes()).hexdigest() != digest:
            raise ValueError('Kube Bench: Quellhash abweichend: ' + name)
    lock = dict(commit=spec['recipe']['pin'], source_sha256=hashes,
                config_sha256=configuration_hashes(prefix),
                scope='pinned-go-mod-sum-and-benchmark-configs-not-host-audit')
    (prefix / 'kube-bench-build-lock.json').write_text(json.dumps(lock, indent=2) + '\n', encoding='utf-8')


def receipts(prefix, spec, env):
    lock = json.loads((prefix / 'kube-bench-build-lock.json').read_text(encoding='utf-8'))
    for name, digest in lock['source_sha256'].items():
        if hashlib.sha256(common.checked(prefix / 'source' / name).read_bytes()).hexdigest() != digest:
            raise ValueError('Kube Bench: Quell-/Go-Lockdatei waehrend des Builds geaendert: ' + name)
    if configuration_hashes(prefix) != lock['config_sha256']:
        raise ValueError('Kube Bench: Benchmark-Dateien waehrend des Builds geaendert.')
    child = {key: value for key, value in env.items() if key in ('PATH', 'LANG', 'LC_ALL', 'HOME')}
    command = [str(prefix / 'bin/kube-bench'), 'version', '--config',
               str(prefix / 'source/cfg/config.yaml'), '--config-dir', str(prefix / 'source/cfg')]
    result = subprocess.run(command, cwd=prefix, env=child, capture_output=True, text=True, check=True, timeout=30)
    if result.stdout.strip() != spec['recipe']['version']:
        raise ValueError('Kube Bench: Versionsprobe abweichend; kein Installiert-Nachweis.')
    modules = {}
    for line in (prefix / 'source/go.sum').read_text(encoding='utf-8').splitlines():
        parts = line.split()
        if len(parts) == 3 and not parts[1].endswith('/go.mod'):
            modules[(parts[0], parts[1])] = parts[2]
    components = [dict(type='application', name='kube-bench', version=spec['recipe']['version'])]
    components += [dict(type='library', name=name, version=version,
                       properties=[{'name': 'go.sum.hash', 'value': digest}])
                   for (name, version), digest in sorted(modules.items())]
    sbom = dict(bomFormat='CycloneDX', specVersion='1.5', version=1, components=components,
                metadata={'properties': [{'name': 'scope', 'value': 'declared-go.sum-modules; not binary reachability or host compliance'}]})
    (prefix / 'kube-bench-sbom.cdx.json').write_text(json.dumps(sbom, indent=2) + '\n', encoding='utf-8')
    (prefix / 'kube-bench-version-probe.json').write_text(json.dumps(dict(
        version=result.stdout.strip(), audit_performed=False, credentials_passed=False)), encoding='utf-8')
    return list(lock['config_sha256']) + ['kube-bench-build-lock.json', 'kube-bench-sbom.cdx.json', 'kube-bench-version-probe.json']
