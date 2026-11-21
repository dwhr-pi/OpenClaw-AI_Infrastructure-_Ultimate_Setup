"""Consent-gated Debian-family build dependencies, separate from unprivileged builds."""
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

import gap_tools as common


# Do not allow recipes to install applications or arbitrary system packages.
MOSQUITTO_PACKAGES = ("git", "cmake", "build-essential", "pkg-config", "libssl-dev",
                      "libcjson-dev", "libsqlite3-dev", "libedit-dev", "libmicrohttpd-dev")
LITELLM_PACKAGES = ("build-essential", "pkg-config")
SONGREC_PACKAGES = ('cargo', 'rustc', 'build-essential', 'pkg-config', 'gettext',
                    'libasound2-dev', 'libglib2.0-dev', 'libssl-dev')
SONGREC_COMMANDS = ('cargo', 'rustc', 'cc', 'c++', 'make', 'pkg-config', 'msgfmt')
ESPEAK_PACKAGES = ('cmake', 'build-essential')
OUTLINES_PACKAGES = ('python3.12', 'python3.12-venv')
VALKEY_PACKAGES = ('build-essential', 'pkg-config', 'libssl-dev')
VAULTWARDEN_PACKAGES = ('build-essential', 'pkg-config', 'perl', 'libssl-dev')
TESTSSL_PACKAGES = ('bash', 'openssl', 'bsdextrautils', 'coreutils', 'gawk', 'grep',
                    'sed', 'procps', 'findutils', 'util-linux')
SANDBOX_PACKAGES = {
    'gvisor': ('build-essential', 'python3', 'ca-certificates', 'bzip2'),
    'firecracker': ('build-essential', 'musl-tools', 'python3', 'ca-certificates', 'libclang-dev'),
    'kata_containers': ('build-essential', 'pkg-config', 'libseccomp-dev', 'ca-certificates'),
}


def os_release():
    # Standard parser handles shell quoting and /usr/lib/os-release fallback, without executing it.
    try:
        return platform.freedesktop_os_release()
    except OSError:
        return {}


def ubuntu_release():
    values = os_release()
    return values.get("ID") == "ubuntu" and values.get("VERSION_ID") == "24.04"


def debian_family():
    values = os_release()
    return (values.get('ID') in ('ubuntu', 'debian', 'dietpi') or
            bool({'ubuntu', 'debian'} & set(values.get('ID_LIKE', '').split())))


def installed(package):
    result = subprocess.run(["dpkg-query", "-W", "-f=${Status}", package],
                            capture_output=True, text=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == "install ok installed"


def prepare(spec, approved=False):
    denied = os.environ.get('OPENCLAW_BUILD_DEPS_DENY') == '1'
    if denied:
        approved = False
    packages = spec["recipe"].get("apt_build_deps", [])
    if spec['id'] == 'vaultwarden' and not packages:
        packages = VAULTWARDEN_PACKAGES
    name, slug = "Mosquitto", "mosquitto"
    extra = {
        'testssl': ('testssl', TESTSSL_PACKAGES, ('bash', 'openssl', 'hexdump', 'unshare')),
        'valkey': ('Valkey', VALKEY_PACKAGES, ('make', 'cc', 'c++', 'pkg-config')),
        'espeak_ng': ('eSpeak NG', ESPEAK_PACKAGES, ('cmake', 'make', 'cc')),
        'outlines': ('Outlines', OUTLINES_PACKAGES, ()),
        'vaultwarden': ('Vaultwarden', VAULTWARDEN_PACKAGES, ('cc', 'pkg-config', 'perl')),
    }
    extra.update({key: (key, packages, ('cc', 'make')) for key, packages in SANDBOX_PACKAGES.items()})
    if spec['id'] == 'owasp_zap':
        if packages and tuple(packages) != ('openjdk-21-jdk-headless',):
            raise ValueError('Nicht freigegebene ZAP-Systempaketliste; keine apt-Aktion.')
        name, slug, packages = 'OWASP ZAP', 'owasp_zap', ('openjdk-21-jdk-headless',)
    if spec['id'] in extra:
        name, expected, commands = extra[spec['id']]
        if tuple(packages) != expected:
            raise ValueError('Nicht freigegebene Systempaketliste; keine apt-Aktion.')
        slug = spec['id']
    if spec['id'] == 'songrec':
        if packages and tuple(packages) != SONGREC_PACKAGES:
            raise ValueError('Nicht freigegebene SongRec-Systempaketliste; keine apt-Aktion.')
        name, slug, packages = 'SongRec', 'songrec', SONGREC_PACKAGES
    if spec["id"] == "litellm":
        if packages and tuple(packages) != LITELLM_PACKAGES:
            raise ValueError("Nicht freigegebene LiteLLM-Systempaketliste; keine apt-Aktion.")
        name, slug, packages = "LiteLLM", "litellm", LITELLM_PACKAGES
        if all(shutil.which(tool) for tool in ("cc", "c++", "make", "pkg-config")):
            print("LiteLLM: C/C++-Buildwerkzeuge bereits vorhanden; keine apt-Aktion.")
            return
    if not packages:
        return
    if (spec["id"] not in ("mosquitto", "litellm", "songrec", "espeak_ng", "outlines", "valkey", 'testssl', 'owasp_zap', 'vaultwarden', *SANDBOX_PACKAGES) or
            (spec["id"] == "mosquitto" and tuple(packages) != MOSQUITTO_PACKAGES)):
        raise ValueError("Nicht freigegebene Systempaketliste; keine apt-Aktion.")
    release = os_release()
    supported = ubuntu_release() or debian_family()
    missing_managers = [tool for tool in ('apt-get', 'dpkg-query') if not shutil.which(tool)]
    if not supported or missing_managers:
        details = ('ID=' + str(release.get('ID', 'unbekannt')) +
                   ', VERSION_ID=' + str(release.get('VERSION_ID', 'unbekannt')))
        reason = ('Paketwerkzeuge fehlen im PATH: ' + ', '.join(missing_managers)
                  if supported else 'Distribution nicht als Debian-/Ubuntu-Familie erkannt')
        message = (name + ': ' + reason + ' (' + details + '). '
                   'Gefuehrter apt-Weg erfordert Debian-/Ubuntu-Familie und passende Pakete. Siehe docs/tools/' + slug + '.md.')
        if approved or (slug == 'songrec' and not all(shutil.which(tool) for tool in SONGREC_COMMANDS)):
            raise ValueError(message + " Keine Systemaenderung.")
        print(message)
        return
    def available(package):
        # Respect an existing rustup/private compiler instead of replacing it with APT.
        if slug == 'songrec' and package in ('cargo', 'rustc') and shutil.which(package):
            return True
        return installed(package)

    missing = [package for package in packages if not available(package)]
    if not missing:
        print(name + ": Basis-Buildpakete bereits vorhanden; keine apt-Aktion.")
        if slug == "litellm":
            raise ValueError("LiteLLM: Pakete installiert, aber cc/c++/make/pkg-config fehlen im PATH; PATH/Paketinstallation separat reparieren.")
        if slug == 'songrec' and not all(shutil.which(tool) for tool in SONGREC_COMMANDS):
            raise ValueError('SongRec: Pakete installiert, aber Buildwerkzeuge fehlen im PATH; '
                             'PATH/Paketinstallation separat reparieren. Kein Quellen-Download.')
        if slug in extra and not all(shutil.which(tool) for tool in commands):
            raise ValueError(name + ': Pakete installiert, aber Buildwerkzeuge fehlen im PATH; kein Quellen-Download.')
        return
    print(name + ": fehlende gemeinsame Buildpakete: " + " ".join(missing))
    print("Nur freigegebene Basiswerkzeuge/Bibliotheken via apt; " + name + " selbst aus GitHub. "
          "apt kann Abhaengigkeiten aktualisieren. Basiswerkzeuge bleiben bei Deinstallation erhalten.")
    print("Gezielt erneut starten: bash scripts/tools/" + slug + "_install.sh --install-build-deps")
    if not approved and not denied and sys.stdin.isatty():
        try:
            print("Fehlende Buildpakete jetzt mit apt installieren? [j/N]", flush=True)
            print("Warte auf Ihre Eingabe und Enter. Nur [j/ja/y/yes] erlaubt die Aktion; Nur [Enter] bedeutet: Nein.", flush=True)
            approved = input().strip().lower() in ("j", "ja", "y", "yes")
        except EOFError:
            approved = False
    if not approved:
        raise ValueError(name + ": Buildabhaengigkeiten fehlen; Zustimmung nicht erteilt. "
                         "Kein Download/Build, kein Erfolgsmarker. Siehe docs/tools/" + slug + ".md.")
    # Privilege escalation is confined to the explicitly approved apt phase.
    prefix = [] if os.geteuid() == 0 else [common.executable("sudo"), "--"]
    env = {key: value for key, value in os.environ.items() if key in ("PATH", "LANG", "LC_ALL", "TERM")}
    env["DEBIAN_FRONTEND"] = "noninteractive"
    options = ["-o", "DPkg::Lock::Timeout=300"]
    common.run(prefix + ["apt-get"] + options + ["update"], Path.cwd(), env)
    if not ubuntu_release():
        print(name + ': abweichende Debian-/Ubuntu-Basis; Paketaufloesung vor Installation simulieren.')
        common.run(prefix + ['apt-get'] + options + ['--simulate', 'install', '--no-remove',
                   '--no-install-recommends'] + missing, Path.cwd(), env)
    common.run(prefix + ["apt-get"] + options + ["install", "--no-remove", "--no-install-recommends", "-y"] + missing, Path.cwd(), env)
    if any(not available(package) for package in packages):
        raise ValueError(name + ": Buildpakete nach apt unvollstaendig; kein Quellen-Download.")
    if slug == "litellm" and not all(shutil.which(tool) for tool in ("cc", "c++", "make", "pkg-config")):
        raise ValueError("LiteLLM: Compiler/Linker nach apt nicht im PATH; kein Quellen-Download.")
    if slug == 'songrec' and not all(shutil.which(tool) for tool in SONGREC_COMMANDS):
        raise ValueError('SongRec: Cargo/Rust/Buildwerkzeuge nach apt nicht im PATH; kein Quellen-Download.')
    if slug in extra and not all(shutil.which(tool) for tool in commands):
        raise ValueError(name + ': Buildwerkzeuge nach apt nicht im PATH; kein Quellen-Download.')
    print(name + ": Buildabhaengigkeiten eingerichtet; GitHub-Build folgt ohne sudo/Docker.")
