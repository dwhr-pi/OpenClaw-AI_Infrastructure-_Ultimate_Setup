"""Read-only, allowlisted system identity for installation logs; no secrets or network."""
from pathlib import Path
import argparse
import os
import platform
import re
import shutil
import stat
import sys


FIELDS = ('PRETTY_NAME', 'ID', 'ID_LIKE', 'VERSION_ID', 'VERSION_CODENAME')


def clean(value):
    return ''.join(c if c.isprintable() else '?' for c in str(value))[:240]


def sandbox_snapshot():
    # Metadata only: never open /dev/kvm, issue ioctls, execute runtimes or change permissions.
    system, kernel, arch = platform.system(), platform.release(), platform.machine().lower()
    match = re.match(r'^(\d+)\.(\d+)', kernel)
    minimum = 'unbekannt'
    if system != 'Linux':
        minimum = 'kein Linux-Host'
    elif match:
        minimum = 'ja' if tuple(map(int, match.groups())) >= (5, 6) else 'nein'
    device = 'unbekannt'
    accessible = 'nicht geprueft'
    try:
        info = os.stat('/dev/kvm', follow_symlinks=False)
        device = 'Zeichengeraet' if stat.S_ISCHR(info.st_mode) else 'kein direktes Zeichengeraet'
        if stat.S_ISCHR(info.st_mode):
            accessible = 'ja' if os.access('/dev/kvm', os.R_OK | os.W_OK) else 'nein'
    except FileNotFoundError:
        device = 'nicht vorhanden'
    except OSError:
        device = 'Metadaten nicht lesbar'
    namespaces = []
    for name in ('user', 'mnt', 'pid', 'net'):
        try:
            if Path('/proc/self/ns', name).exists():
                namespaces.append(name)
        except OSError:
            pass  # Restricted /proc access is not proof of usable namespace support.
    return dict(Sandbox_Pruefumfang='nur Metadaten; kein Runtime-/VM-/KVM-Funktionstest',
                gVisor_Kernel_ab_5_6=minimum,
                Sandbox_64bit_Architektur='ja' if system == 'Linux' and arch in ('x86_64', 'amd64', 'aarch64', 'arm64') else 'nein/unbekannt',
                KVM_Geraet=device, KVM_Lese_Schreibrecht=accessible,
                Sichtbare_Namespace_Marker=','.join(namespaces) or 'keine/unbekannt',
                Runtime_Hinweis='gVisor: KVM nur fuer KVM-Plattform; Kata/Firecracker: Hypervisor-/Gast-/KVM-Vertrag separat offen')


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
    result.update(sandbox_snapshot())
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sandbox', action='store_true', help='Only read sandbox host metadata; no runtime execution')
    args = parser.parse_args(argv)
    print('--- Systemdiagnose (nur lesend) ---')
    for key, value in (sandbox_snapshot() if args.sandbox else snapshot()).items():
        print(key + '=' + clean(value))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
