"""Read-only, allowlisted system identity for installation logs; no secrets or network."""
from pathlib import Path
import platform
import shutil
import sys


FIELDS = ('PRETTY_NAME', 'ID', 'ID_LIKE', 'VERSION_ID', 'VERSION_CODENAME')


def clean(value):
    return ''.join(c if c.isprintable() else '?' for c in str(value))[:240]


def snapshot():
    try:
        release = platform.freedesktop_os_release()
    except OSError:
        release = {}
    kernel = platform.release()
    distro = release.get('ID', '')
    relatives = release.get('ID_LIKE', '').split()
    dietpi = distro == 'dietpi' or Path('/boot/dietpi/.version').is_file()
    debian = distro in ('debian', 'ubuntu', 'dietpi') or 'debian' in relatives or 'ubuntu' in relatives
    result = {key: release.get(key, 'unbekannt') for key in FIELDS}
    result.update(System=platform.system(), Architektur=platform.machine(), Kernel=kernel,
                  WSL='ja' if 'microsoft' in kernel.lower() else 'nein/nicht erkannt',
                  Debian_Familie='ja' if debian else 'nein/unbekannt',
                  DietPi_Marker='vorhanden' if dietpi else 'nicht erkannt',
                  Python='.'.join(map(str, sys.version_info[:3])), Python_Pfad=sys.executable)
    for command in ('apt-get', 'dpkg-query', 'apt-cache'):
        result[command] = shutil.which(command) or 'nicht im PATH'
    return result


def main():
    print('--- Systemdiagnose (nur lesend) ---')
    for key, value in snapshot().items():
        print(key + '=' + clean(value))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
