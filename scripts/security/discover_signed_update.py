"""Explicit online discovery; only independently Minisign-verified newer releases may update."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import signal
import sys
import tempfile
import time
from urllib.parse import urlsplit
from urllib.request import build_opener, HTTPRedirectHandler, ProxyHandler, Request

SPEC = importlib.util.spec_from_file_location('discovery_verified_updater', Path(__file__).with_name('update_verified_release.py'))
updater = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(updater)

ROOT = Path(__file__).resolve().parents[2]
PROJECT = 'dwhr-pi/OpenClaw-AI_Infrastructure-_Ultimate_Setup'
API = 'https://api.github.com/repos/' + PROJECT
DOWNLOAD = 'https://github.com/' + PROJECT + '/releases/download/'
FILES = ('SHA256SUMS', 'SHA256SUMS.minisig', 'release.json', 'install.sh')
STABLE = re.compile(r'v(0|[1-9][0-9]{0,8})\.(0|[1-9][0-9]{0,8})\.(0|[1-9][0-9]{0,8})')
HOSTS = {'api.github.com', 'github.com', 'release-assets.githubusercontent.com', 'objects.githubusercontent.com'}


def version(tag):
    match = STABLE.fullmatch(tag) if isinstance(tag, str) else None
    if not match:
        raise ValueError('Stabiler vX.Y.Z-Tag erforderlich.')
    return tuple(map(int, match.groups()))


def allowed_url(url):
    parsed = urlsplit(url)
    if (parsed.scheme != 'https' or parsed.hostname not in HOSTS or parsed.username or parsed.password
            or parsed.port not in (None, 443) or parsed.fragment):
        raise ValueError('Nicht freigegebenes Release-Downloadziel.')


class SecureRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        allowed_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url, limit):
    allowed_url(url)
    # Do not inherit proxy credentials or accept arbitrary asset URLs from API metadata.
    opener = build_opener(ProxyHandler({}), SecureRedirect())
    accept = 'application/vnd.github+json' if url.startswith(API + '/') else 'application/octet-stream'
    request = Request(url, headers={'User-Agent': 'OpenClaw-signed-update-check', 'Accept': accept})
    deadline = time.monotonic() + 30
    with opener.open(request, timeout=15) as response:
        if response.status != 200:
            raise ValueError('Release-HTTP-Antwort nicht erfolgreich.')
        result = bytearray()
        while len(result) <= limit:
            if time.monotonic() > deadline:
                raise ValueError('Release-Download-Zeitlimit erreicht.')
            block = response.read(min(65536, limit + 1 - len(result)))
            if not block:
                return bytes(result)
            result.extend(block)
        raise ValueError('Release-Datei oder API-Antwort zu gross.')


def candidates(records):
    if not isinstance(records, list) or len(records) > 100:
        raise ValueError('Ungueltige oder zu grosse Release-Liste.')
    complete, incomplete, seen = [], [], set()
    for row in records:
        if not isinstance(row, dict):
            raise ValueError('Ungueltiger Release-Datensatz.')
        if row.get('draft') is not False or row.get('prerelease') is not False:
            continue
        tag = row.get('tag_name')
        if not isinstance(tag, str) or not STABLE.fullmatch(tag):
            continue
        if tag in seen:
            raise ValueError('Doppelter Release-Tag; keine automatische Auswahl.')
        seen.add(tag)
        assets = row.get('assets')
        if not isinstance(assets, list):
            raise ValueError('Release-Assetliste fehlt.')
        names = [asset.get('name') for asset in assets if isinstance(asset, dict)]
        if any(names.count(name) > 1 for name in FILES):
            raise ValueError('Mehrdeutige Release-Artefakte.')
        if any(name not in names for name in FILES):
            incomplete.append(tag)
        else:
            complete.append(tag)
    return sorted(complete, key=version, reverse=True), sorted(incomplete, key=version, reverse=True)


def local_state(repo):
    commit = updater.safety.git(repo, 'rev-parse', 'HEAD').stdout.decode().strip()
    if not re.fullmatch('[0-9a-f]{40}', commit):
        raise ValueError('Lokaler Git-Commit nicht bestimmbar.')
    setup = repo / 'setup_ultimate.sh'
    if setup.is_symlink() or not setup.is_file() or setup.stat().st_size > 1048576:
        raise ValueError('Lokale Setup-Version nicht sicher lesbar.')
    matches = re.findall(r'^APP_VERSION="([0-9]+\.[0-9]+(?:\.[0-9]+)?)"$', setup.read_text(encoding='utf-8'), re.M)
    if len(matches) != 1:
        raise ValueError('Lokale Setup-Version nicht eindeutig.')
    tag = 'v' + matches[0] + ('.0' if matches[0].count('.') == 1 else '')
    # A patch-level release tag takes precedence over the legacy major.minor APP_VERSION.
    described = updater.safety.git(repo, 'describe', '--tags', '--exact-match', 'HEAD', allowed=(0, 128))
    exact = described.stdout.decode().strip() if described.returncode == 0 else ''
    if STABLE.fullmatch(exact):
        tag = exact if version(exact) >= version(tag) else tag
    return tag, commit


def discover(repo, key, backup_root, *, apply=False, download=fetch, verifier=None, perform=None):
    # Never import a trust key from a release, and fail before any network request if it is missing.
    updater.manifest_module.regular(key)
    current_tag, current_commit = local_state(repo)
    records = json.loads(download(API + '/releases?per_page=100', 2097152),
                         object_pairs_hook=updater.manifest_module.unique)
    complete, incomplete = candidates(records)
    report = dict(status='no-verifiable-stable-release', current_tag=current_tag, current_commit=current_commit,
                  incomplete_releases=incomplete, signature_verified=False, checkout=False,
                  policy='minisign-only-no-main-fallback', discovery_limit=100)
    if not complete:
        return report
    tag = complete[0]
    with tempfile.TemporaryDirectory(prefix='openclaw-update-discovery-') as directory:
        artifacts = Path(directory)
        for name in FILES:
            data = download(DOWNLOAD + tag + '/' + name, 1048576)
            if not data or len(data) > 1048576:
                raise ValueError('Leeres oder zu grosses Release-Artefakt.')
            (artifacts / name).write_bytes(data)
        manifest = (verifier or updater.verify)(artifacts, tag, key)
        report.update(tag=tag, commit=manifest['commit'], signature_verified=True)
        # main is informational only. Its code, files or URLs are never used for an update.
        main = json.loads(download(API + '/commits/main', 524288),
                          object_pairs_hook=updater.manifest_module.unique)
        sha = main.get('sha') if isinstance(main, dict) else None
        if not isinstance(sha, str) or not re.fullmatch('[0-9a-f]{40}', sha):
            raise ValueError('GitHub-main-Metadaten ungueltig; kein Update.')
        report.update(main_commit=sha, main_outside_selected_release=sha != manifest['commit'])
        if manifest['commit'] == current_commit:
            report['status'] = 'already-at-verified-release'
        elif version(tag) <= version(current_tag):
            report['status'] = 'not-newer-no-downgrade-or-same-version-replacement'
        elif not apply:
            report['status'] = 'new-signed-release-available'
        else:
            result = (perform or updater.update)(repo, backup_root, manifest, apply=True, fetch=True,
                                                  expected_head=current_commit)
            report.update(status=result['status'], checkout=True, backup=result['backup'])
        return report


def startup_check(repo, key):
    try:
        updater.manifest_module.regular(key)
    except (ValueError, OSError):
        return ('Update-Hinweis: keine unabhaengige release.pub gefunden. Keine Online-Pruefung.\n'
                'Schluessel importieren oder OPENCLAW_RELEASE_PUBLIC_KEY setzen; siehe docs/SIGNED_UPDATES.md.')
    command = [sys.executable, '-I', '-B', str(Path(__file__).resolve()), '--check-online',
               '--repo', str(repo), '--public-key', str(key)]
    env = {name: value for name, value in os.environ.items()
           if name in ('PATH', 'HOME', 'LANG', 'LC_ALL', 'SYSTEMROOT')}
    process = None
    try:
        process = updater.subprocess.Popen(command, env=env, stdout=updater.subprocess.PIPE,
                                           stderr=updater.subprocess.PIPE, text=True,
                                           start_new_session=os.name == 'posix')
        try:
            stdout, _ = process.communicate(timeout=20)
        except updater.subprocess.TimeoutExpired:
            if os.name == 'posix':
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            else:
                process.kill()
            process.communicate(timeout=3)
            return 'Update-Pruefung nach 20 Sekunden beendet. Status unbekannt; kein Update ausgefuehrt.'
        if process.returncode != 0:
            return 'Update-Pruefung nicht erfolgreich (Netzwerk, Minisign oder Release). Kein Update ausgefuehrt.'
        report = json.loads(stdout.splitlines()[-1])
        if report.get('status') == 'new-signed-release-available' and report.get('signature_verified') is True:
            return ('Neues signiertes Setup-Update verfuegbar: ' + report['tag'] + '\n'
                    'Minisign und SHA256 mit deiner release.pub geprueft.\n'
                    'Installation nur bewusst ueber Optionen: Jetzt nur das Setup aktualisieren.')
        if report.get('main_outside_selected_release'):
            return ('GitHub-main weicht vom verifizierten Release ab. Diese Quellen werden nicht automatisch uebernommen.\n'
                    'Kein neueres signiertes Setup-Update verfuegbar.')
        return ''
    except (ValueError, OSError, IndexError, updater.subprocess.SubprocessError):
        if process is not None and process.poll() is None:
            process.kill()
        return 'Update-Pruefung derzeit nicht verfuegbar. Kein Update ausgefuehrt.'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--public-key', type=Path, default=Path.home() / '.config/openclaw-trust/release.pub')
    parser.add_argument('--backup-root', type=Path, default=Path.home() / '.openclaw_ultimate_user_data/repo_update_backups')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check-online', action='store_true')
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--startup-check', action='store_true')
    args = parser.parse_args(argv)
    if args.startup_check:
        notice = startup_check(args.repo, args.public_key)
        if notice:
            print(notice)
        return 0
    try:
        report = discover(args.repo, args.public_key, args.backup_root, apply=args.apply)
        if report['signature_verified']:
            print('Minisign-Signatur und SHA256 geprueft:', report['tag'])
        print('Unvollstaendige Releases und main werden nicht als Update uebernommen.')
        print(json.dumps(report, ensure_ascii=True))
        return 3 if report['status'] == 'no-verifiable-stable-release' else 0
    except (ValueError, OSError, updater.safety.SafetyError, updater.subprocess.SubprocessError):
        print('Signierte Update-Suche abgebrochen: Netzwerk, Minisign, lokalen Stand und separat bereitgestellte release.pub pruefen. Kein unsignierter Fallback.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
