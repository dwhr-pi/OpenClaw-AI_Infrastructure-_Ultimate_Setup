"""Consent-gated private Python 3.13; never changes the system interpreter."""
import json
import os
from pathlib import Path
import shutil
import sys

import gap_tools as common
import native_uv


def select(base, approved=False):
    slot = common.checked(base / 'toolchain/outlines-python313')
    marker = common.checked(slot / 'python-ready.json')
    env = {k: v for k, v in os.environ.items() if k in ('PATH', 'LANG', 'LC_ALL')}
    env.update(UV_NO_CONFIG='1', UV_PYTHON_DOWNLOADS='never', PYTHONDONTWRITEBYTECODE='1')

    def verify(entry):
        if not isinstance(entry, str) or '\\' in entry or ':' in entry:
            raise ValueError('Outlines: ungueltiger privater Python-Pfad.')
        relative = Path(entry)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Outlines: Python-Pfad verlaesst private Toolchain oder fehlt.')
        managed = common.checked(slot / 'managed')
        candidate = slot / relative
        if not candidate.is_relative_to(managed):
            raise ValueError('Outlines: Python-Pfad liegt nicht in privater managed-Laufzeit.')
        # uv may return an internal version alias; never relax the general path guard.
        try:
            resolved = candidate.resolve(strict=True)
        except (OSError, RuntimeError) as error:
            raise ValueError('Outlines: privater Python-Verweis fehlt oder ist zyklisch.') from error
        if not resolved.is_relative_to(managed):
            raise ValueError('Outlines: Python-Verweis verlaesst private managed-Laufzeit.')
        python = common.checked(resolved)
        if not python.is_file():
            raise ValueError('Outlines: Python-Pfad verlaesst private Toolchain oder fehlt.')
        common.run([str(python), '-I', '-B', '-c',
                    'import sys,ssl,venv; assert sys.version_info[:2] == (3,13); print(sys.version)'], base, env)
        return str(python)

    if slot.exists():
        record = json.loads(marker.read_text(encoding='utf-8'))
        files = common.inventory(slot)
        files.pop('python-ready.json', None)
        if files != record['files']:
            raise ValueError('Outlines: private Python-Dateien veraendert; nichts ueberschreiben.')
        return verify(record['entry'])
    print('Outlines: kein geeignetes Python vorhanden. Private Python-3.13-Laufzeit via uv/GitHub; kein System-Python-Wechsel.')
    if not approved and sys.stdin.isatty():
        print('Private Python-Laufzeit und fehlendes uv jetzt bereitstellen? [j/N]', flush=True)
        try:
            approved = input().strip().lower() in ('j', 'ja', 'y', 'yes')
        except EOFError:
            approved = False
    if not approved:
        raise ValueError('Outlines: private Python-Einrichtung nicht freigegeben; kein Download oder Modellstart.')
    common.reserve(base, {'reserve_mb': 4096 + 1024})
    uv = native_uv.select(base, {'id': 'outlines', 'recipe': {'private_uv': '0.13.5', 'disk_mb': 4096}},
                          approved=True, allow_download=True)
    slot.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    slot.mkdir(mode=0o700)
    env.update(UV_PYTHON_INSTALL_DIR=str(slot / 'managed'), UV_CACHE_DIR=str(slot / 'cache'),
               UV_PYTHON_DOWNLOADS='manual')
    try:
        common.run([uv, 'python', 'install', '3.13', '--no-bin', '--no-config'], base, env)
        python = Path(common.run([uv, 'python', 'find', '3.13', '--managed-python',
                                  '--no-python-downloads', '--no-config'], base, env).strip())
        if not python.is_absolute() or not python.is_relative_to(slot / 'managed'):
            raise ValueError('Outlines: uv lieferte keinen privaten Python-Pfad.')
        entry = python.relative_to(slot).as_posix()
        python = Path(verify(entry))
        entry = python.relative_to(slot).as_posix()
        marker.write_text(json.dumps({'entry': entry, 'files': common.inventory(slot)}), encoding='utf-8')
    except BaseException:
        shutil.rmtree(common.checked(slot))
        raise
    print('Outlines: private Python-3.13-Basis bereit; Dateiinventar erfasst. Toolchain bleibt bei App-Deinstallation erhalten.')
    return str(python)
