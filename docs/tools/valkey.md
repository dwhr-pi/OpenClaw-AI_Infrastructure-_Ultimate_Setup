# Valkey: nativer Server- und CLI-Build

Quelle: [valkey-io/valkey](https://github.com/valkey-io/valkey).
Stand: 16.11.2026. Version **9.1.3**, Commit
`29173b67508b2de4c0f0ed551f3b47cf19fc3ca8`.
[Originallizenz am Pin](https://github.com/valkey-io/valkey/blob/29173b67508b2de4c0f0ed551f3b47cf19fc3ca8/COPYING):
BSD-3-Clause; Lizenzen gebuendelter Bibliotheken bleiben getrennt zu beachten.

## Installation im Setup

Valkey ist jetzt **experimental / nativer Build**, nicht mehr ausschliesslich ein
gesperrter Planungseintrag. Im Tools-Menue an der bisherigen Stelle hinter XERJ
`Valkey` waehlen. Das Setup bietet fehlende Buildwerkzeuge zur bewussten Freigabe an.
Debian-/Ubuntu-Familie inklusive Ubuntu 26.04 und DietPi wird erkannt;
abweichende Paketbasen muessen zuerst die apt-Simulation bestehen.

```bash
bash scripts/tools/valkey_install.sh --dry-run
bash scripts/tools/valkey_install.sh --install-build-deps
bash scripts/tools/valkey_status.sh
bash scripts/tools/valkey_doctor.sh
```

Direkter Installationsaufruf ohne Flag fragt nur bei interaktivem Terminal nach.
Ohne Freigabe werden keine fehlenden Systempakete installiert. Benoetigt:
Git, Python >=3.10, Make, C/C++-Compiler, pkg-config und OpenSSL-Entwicklungsbibliotheken.
Paketliste: `build-essential`, `pkg-config`, `libssl-dev`; niemals das Valkey-Serverpaket.
Mindestens 4096 MiB Disk und 1024 MiB verfuegbarer RAM als Buildreserve.

Privates Ziel: `~/.openclaw_ultimate_user_data/tools/valkey/native-github/`.
Der Make-Build verwendet einen Job, eingebautes TLS und den libc-Allocator.
Kein Docker, `sudo make install`, globaler PATH-Eintrag oder Redis-Symlink.
`COPYING`, README, Makefiles und Versionsheader werden gegen feste SHA256 geprueft.
Der Build nutzt die am Commit enthaltenen Abhaengigkeiten; keine separate Versionserfindung.

Server und CLI werden nach dem Build ausschliesslich mit `--version` geprueft,
jeweils maximal 30 Sekunden. Erst danach entstehen Buildmarker und Datei-/Artefaktinventar.
Kein Serverstart, TCP-Port, PING, Providerzugriff oder Datenbanktest.
Eine erfolgreiche Installation belegt den Binary-Build, nicht produktive Betriebsbereitschaft.
**Ein echter Linux-/WSL-Build ist durch den Nutzer noch abzunehmen.**

## Nachweise und Lifecycle

`valkey-build-lock.json` erfasst Commit, gepruefte Quellhashes, den Git-Baum der
gebuendelten Abhaengigkeiten, Buildoptionen und die verwendete OpenSSL-Version.
`valkey-sbom.cdx.json` nennt Hauptkomponente/OpenSSL, nicht den vollstaendigen
OS-/Compiler-/Bibliotheksbaum. `valkey-version-probes.json` dokumentiert beide Proben.
Die erzeugten Artefakte werden lokal SHA256-inventarisiert; kein vorab versprochener Binary-Hash.

```bash
bash scripts/tools/valkey_update.sh --dry-run
bash scripts/tools/valkey_uninstall.sh --dry-run
```

Update bleibt auf dem freigegebenen Pin. Uninstall entfernt nur den unveraenderten
eigenen Build mit Besitz-/Inventarnachweis. Fremde Redis-/Valkey-Installationen,
gemeinsame Compiler, Logs und externe Daten/Configs bleiben erhalten.
Einen spaeter selbst eingerichteten Dienst vor einer Deinstallation bewusst stoppen;
der Build-Uninstaller stoppt oder entfernt keine systemd-Units automatisch.
Unbekannte oder veraenderte Bestandsordner werden nicht uebernommen oder geloescht.

## Optionaler Betrieb und Sicherheit

Die [User-systemd-Vorlage](../../config/systemd/openclaw-valkey.service.example)
ist nur ein Beispiel und wird weder installiert noch aktiviert. Sie erwartet den
Standard-Buildpfad, stellt **keinen TCP-Port** bereit und nutzt einen privaten
Unix-Socket mit Modus 0600. StateDirectory und RuntimeDirectory liegen ausserhalb
des Buildbaums; Persistenzdaten bleiben bei dessen Deinstallation erhalten.
Zusaetzliche Abhaertung und User-systemd-Funktionalitaet unter WSL separat pruefen.

Mehrbenutzerbetrieb, TCP/VPN-Zugriff oder ein Gateway erfordern eigene minimale ACLs,
TLS-Zertifikate ausserhalb Git, Speicher-/Eviction-Grenzen und Restore-Tests.
Keine anonymen externen Listener und kein automatischer Ersatz eines Redis-Backends.
TLS ist im Binary verfuegbar, durch einen Binary-Build aber noch nicht konfiguriert.
ACL-/TLS-, Last-/Persistenz-, Backup-/Restore- und Gateway-Kompatibilitaetsabnahme bleiben offen.

[Offizielle Buildanleitung am Pin](https://github.com/valkey-io/valkey/blob/29173b67508b2de4c0f0ed551f3b47cf19fc3ca8/README.md),
[Systemdiagnose](../SYSTEM_DIAGNOSTICS.md),
[Infrastruktur-Kandidaten](infrastructure-candidates.md).

<!-- BEGIN GENERATED VPS SSH -->

## VPS ueber SSH bedienen

Voraussetzung: ein bereits gepruefter Setup-Checkout und ein selbst eingerichteter
SSH-Alias `vps` (Benutzer, Host und Schluessel in deiner SSH-Konfiguration).
Alternativ `vps` durch `BENUTZER@VPS_HOST` ersetzen. Den Host-Fingerprint vorher
unabhaengig pruefen; keine Host-Key-Pruefung abschalten. Keine Zugangsdaten in Git.

Auf deinem Client (PowerShell, Linux oder macOS):

```bash
ssh -t vps
```

Danach **im Linux-Terminal des VPS**. Den Pfad bei einem Branch-Checkout anpassen;
ein Windows-/Desktop-Tool wird durch SSH nicht zu einer VPS-Anwendung:

```bash
cd "$HOME/openclaw_ultimate_setup" || exit 1
test -f scripts/tool_commands.py || exit 1
```

Zuerst nur den Offline-Plan lesen (keine Installation und kein Dienststart):

```bash
python3 -I -B scripts/tool_commands.py show valkey
```

### SSH-Aktionen: `valkey`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run valkey --action status
python3 -I -B scripts/tool_commands.py run valkey --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run valkey --action install --apply --confirm valkey:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run valkey --action update --apply --confirm valkey:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run valkey --action uninstall --apply --confirm valkey:uninstall
```

Fehlende Build-Abhaengigkeiten stoppen den Versuch. Nur fuer Install/Update
`--install-build-deps` nach separater Download-Freigabe ergaenzen. Kein Auto-Yes,
kein Docker-Fallback; Source-Build/Status ist keine erfolgreiche Runtime-Abnahme.

Das interaktive Setup bleibt nach bewusster Freigabe im SSH-Terminal erreichbar:

```bash
bash setup_ultimate.sh
```

Keine automatische Installation, kein Browser-/Modell-/Produktivdienststart durch diese Dokumentation.
Nach jedem bewusst ausgefuehrten Befehl den Exitcode unmittelbar mit `echo $?` pruefen;
zum Verlassen des VPS-Terminals `exit` verwenden.

[SSH-Voraussetzungen und Sicherheitsgrenzen](../HEADLESS_SETUP.md) | [Befehle aller registrierten Tools](../generated/HEADLESS_TOOL_COMMANDS.md)

Dieser Abschnitt wird aus der Registry erzeugt. Pflege: `python3 -I -B scripts/quality/tool_ssh_docs.py --write`.

<!-- END GENERATED VPS SSH -->
