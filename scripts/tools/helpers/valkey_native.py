"""Valkey source contracts and bounded version probes; no server or DNS access."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

import gap_tools as common


def prepare(prefix, spec, env):
    recipe = spec['recipe']
    source = prefix / 'source'
    hashes = recipe['source_sha256']
    expected = {'COPYING', 'README.md', 'Makefile', 'src/Makefile', 'deps/Makefile', 'src/version.h'}
    if set(hashes) != expected or any(not re.fullmatch('[0-9a-f]{64}', value) for value in hashes.values()):
        raise ValueError('Valkey: ungueltiger Quellvertrag.')
    for name, digest in hashes.items():
        if hashlib.sha256(common.checked(source / name).read_bytes()).hexdigest() != digest:
            raise ValueError('Valkey: Quellhash abweichend: ' + name)
    openssl = common.run(['pkg-config', '--modversion', 'openssl'], source, env).strip()
    lock = dict(commit=recipe['pin'], version=recipe['version'], source_sha256=hashes,
                vendored_deps_tree=common.git(source, 'rev-parse', 'HEAD:deps'),
                openssl_version=openssl, allocator='libc', tls=True,
                scope='source-contracts-and-system-openssl-not-full-os-lock')
    (prefix / 'valkey-build-lock.json').write_text(json.dumps(lock, indent=2) + '\n', encoding='utf-8')


def receipts(prefix, spec, env):
    recipe = spec['recipe']
    versions = {}
    for binary in ('valkey-server', 'valkey-cli'):
        path = common.checked(prefix / 'source/src' / binary)
        result = subprocess.run([str(path), '--version'], cwd=prefix, env=env, check=True,
                                capture_output=True, text=True, timeout=30)
        if not re.search(r'(?<![0-9])' + re.escape(recipe['version']) + r'(?![0-9.])', result.stdout):
            raise ValueError('Valkey: Versionsprobe abweichend: ' + binary)
        versions[binary] = result.stdout.strip()
    lock = json.loads((prefix / 'valkey-build-lock.json').read_text(encoding='utf-8'))
    components = [dict(type='application', name='valkey', version=recipe['version'],
                       licenses=[{'license': {'id': 'BSD-3-Clause'}}]),
                  dict(type='library', name='openssl', version=lock['openssl_version'])]
    record = dict(bomFormat='CycloneDX', specVersion='1.5', version=1, components=components,
                  metadata={'properties': [{'name': 'scope', 'value': 'main-component-and-system-openssl; bundled sources in build lock'}]})
    (prefix / 'valkey-sbom.cdx.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    (prefix / 'valkey-version-probes.json').write_text(json.dumps(versions, indent=2) + '\n', encoding='utf-8')
    return ['valkey-build-lock.json', 'valkey-sbom.cdx.json', 'valkey-version-probes.json']
