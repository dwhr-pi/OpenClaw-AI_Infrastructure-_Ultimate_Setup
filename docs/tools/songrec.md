# SongRec

Optionaler Menuepunkt **SongRec**, Status `experimental` / `planned`.

## Quelle, Lizenz und Plattform

[Offizielles GitHub-Projekt](https://github.com/marin-m/SongRec).
Alter Quellen-Pin (2026-11-11): `0f677c702666448642753f0e4da2fa262da67bc8`.
Neuer nativer Linux-CLI-Pin (offizieller Tag 0.4.3):
`15da6b224297d7bf8a9c91b9f70af3d499a9636d`.
Der neuere Quellen-Pin verlangt neuere Systembibliotheken; er wird nicht
stillschweigend als Ubuntu-24.04-Build ausgegeben. Alte Quellenverwaltung
bleibt explizit mit `--source-only` erhalten.
Lizenz: GPL-3.0. README und vorhandene Lizenzdateien werden gegen
die SHA256 im Quellenmanifest geprueft.

Rust-Shazam-Client fuer Linux mit GUI und CLI, keine lokale Shazam-Datenbank. Fingerprints gehen an den externen
Shazam-Dienst. Native Rust-/Systembibliotheken und optional GTK/Audio sind separat zu bauen; ein vermeintliches
SongRec-Core-Python-SDK wird nicht erfunden. Keine Mikrofonaufnahme oder Erkennungsanfrage automatisch starten.

## Nativer CLI-Build

Python >=3.11, Git, Cargo/Rust, C-Compiler, pkg-config, gettext/msgfmt sowie
ALSA-, GLib- und OpenSSL-Entwicklungsbibliotheken erforderlich. 8192 MiB
Mindestreserve fuer den neuen Build; keine GUI, keine globale Installation.
Der CLI-Build verwendet `cargo build --release --locked --no-default-features`.
Kein Docker-Fallback. Vollstaendiger Linux-Build bleibt durch Nutzer zu pruefen.

### Cargo und Build-Voraussetzungen im Installer

Der korrigierte Installer prueft unter Ubuntu 24.04 auch die gemeinsamen
Buildpakete. Fehlendes Cargo/Rust und Entwicklungsbibliotheken werden nach
ausdruecklicher Zustimmung ueber APT eingerichtet, danach folgt der gepinnte
GitHub-Build als normaler Benutzer. Im interaktiven Setup fragt der Installer
bei fehlenden Paketen nach; `j` erlaubt die Paketphase, Enter/Nein lehnt ab.

Alternativ die Paketphase ausdruecklich freigeben:

```bash
bash scripts/tools/songrec_install.sh --install-build-deps
```

Freigegebene Buildpakete: `cargo`, `rustc`, `build-essential`, `pkg-config`,
`gettext`, `libasound2-dev`, `libglib2.0-dev`, `libssl-dev`. Bereits vorhandene
Cargo-/Rust-Binaries aus einer privaten Toolchain werden nicht durch APT ersetzt.
Gemeinsame Buildwerkzeuge bleiben bei SongRec-Deinstallation erhalten.

Ohne Zustimmung kein Paket-/Quellen-Download und kein Erfolgsmarker.
Plan, Dry-run, Status und Doctor installieren keine Pakete und fragen nicht nach
sudo. Nur die freigegebene Paketphase nutzt sudo; der eigentliche Build nicht.
Auf anderen Distributionen bleiben Buildpakete manuell bereitzustellen.
Eine nicht passende Rust-Version oder ein Compilerfehler wird nicht durch einen
anderen Quell-Pin oder einen Docker-Fallback umgangen. Echte Linux-Buildabnahme offen.

### Lifecycle-Befehle

```bash
bash scripts/tools/songrec_install.sh --dry-run
bash scripts/tools/songrec_install.sh
bash scripts/tools/songrec_status.sh
bash scripts/tools/songrec_doctor.sh
bash scripts/tools/songrec_doctor.sh --smoke
bash scripts/tools/songrec_update.sh --dry-run
bash scripts/tools/songrec_uninstall.sh --dry-run
```

Install baut die CLI, prueft `--version` und schreibt erst danach `installed: true`.
`runtime_tested: false` bleibt: kein Audio-/Shazam-Funktionstest. Doctor prueft
offline Pin, Origin, Vertragsdateien und Inventar; `--smoke` erlaubt explizit
die begrenzte Versionsprobe. Update bleibt beim Pin. Uninstall ohne Dry-run
entfernt nur unveraenderte, inventarisierte Quellen mit Besitznachweis;
geaenderte Dateien, Modelle, Datenbanken, Logs und sonstige Benutzerdaten bleiben erhalten.

Die Cargo.lock-Abhaengigkeiten werden in `native-sbom.cdx.json` verzeichnet;
das ist eine Lockfile-Inventur, kein Nachweis aller gelinkten Systembibliotheken.
Keine systemd-Unit fuer die CLI. [Voraussetzungen und Testmatrix](SOURCE_INSTALL_READINESS.md).
Der echte End-to-End-Test bleibt offen. Kein automatischer Start/Download
von Modellen, Aufnahme, Training, API-Test oder Dienst.

## Alter Quellenmodus

Mit `--source-only` bleibt die bisherige Quellenverwaltung am alten Pin erhalten.
Hier gelten weiterhin 2048 MiB Mindestreserve nur fuer Quellen, nicht fuer Builds.
Ein erfolgreicher Checkout meldet `source_prepared: true`, `installed: false`
und `runtime_tested: false`. Er ist kein Buildnachweis und wird nicht automatisch
in den neuen nativen CLI-Build umgewandelt. Dessen Mindestreserve betraegt 8192 MiB.
Bei fehlenden Voraussetzungen oder fehlgeschlagenem Build wird auch im nativen
Modus kein erfolgreicher Installationsnachweis geschrieben.

## Einsatz in der Hybrid-Plattform

[Musikerkennung und Domain-Modelle](../AUDIO_RECOGNITION_AND_DOMAIN_MODELS.md)
erlaeutert Datenfluss, Modellkarten und Sicherheitsgrenzen. Auf dem Linux-VPS kann
die native CLI gebaut werden; die GUI ist nicht Teil dieses Buildrezepts und
es wird kein Musikerkennungsserver automatisch gestartet.
GPU-Inferenz gehoert auf passende lokale Worker; private Endpunkte nur ueber
WireGuard, Authentifizierung und bewusst freigegebene Clients verwenden.

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
python3 -I -B scripts/tool_commands.py show songrec
```

### SSH-Aktionen: `songrec`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`SongRec` (ID `songrec`) waehlen und die Einzelfreigaben lesen.
Fehlt der Eintrag oder ist der native Weg gesperrt, hier stoppen: keine
Legacy-/Docker-Ausweichinstallation und kein automatischer Plattformwechsel.

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
