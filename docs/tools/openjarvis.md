# OpenJarvis: nativer CLI-/SDK-Build

Stand: 20.11.2026. Eigener Setup-Eintrag **OpenJarvis**, nicht Hermes_Agent_Jarvis,
Jarvis_Core oder das historische Till-Schaefer-Projekt.

**Installationsumfang:** gepinnter nativer Python-CLI-/SDK-Build mit Install-,
Update-, Status-, Check-, Doctor- und geschuetzten Uninstall-Skripten.
**Kein Quickstart-Autostart und keine automatischen Modelldownloads. GUI,
Desktop-Paket und Rust-Erweiterung bleiben ausdruecklich getrennte Ausbaustufen.**
Experimentell: Offline-Tests sind keine erfolgreiche Linux-/WSL-Build- oder Inferenzabnahme.

## Offizielle Quellen

- [GitHub-Organisation](https://github.com/open-jarvis).
- [Originalrepository](https://github.com/open-jarvis/OpenJarvis).
- [Offizielle Projektwebsite](https://openjarvis.stanford.edu/).
- [Offizielle Dokumentation](https://open-jarvis.github.io/OpenJarvis/).
- [Installationsanleitung am Setup-Pin][install-source].
- [Apache-2.0-Originallizenz am Pin][license-source]. Modell- und Abhaengigkeitslizenzen separat pruefen.

Quellpin: `a9e59e8770f92dd8046c2e5fcc1246eef51bb96a`.
Das ist ein gepruefter Entwicklungsstand, kein neu behaupteter stabiler Upstream-Release.
Die private Buildversion `0.0.0+openclaw.a9e59e8` kennzeichnet genau diesen Setup-Build.
Keine automatische Umstellung auf `main`, `latest` oder Desktop-Releases.

### Buildversionskorrektur vom 20.11.2026

Ein WSL-Test erreichte die vollstaendige Installation von 61 Paketen und eine erfolgreiche
Paketkompatibilitaetspruefung, scheiterte danach jedoch an der Versionsprobe. Das Wheel meldete
`0.0.1.dev1+unknown.ga9e59e877` statt der festgelegten privaten Buildversion.
Dies war ein Fehler unserer SCM-Versionsuebergabe, kein erfolgreicher Installationsnachweis.
Der [gepruefte OpenJarvis-Build][build-source] nutzt hatch-vcs;
dessen [Versionsquelle in 0.5.0][hatch-vcs-source] ruft setuptools-scm ohne Paketnamen auf.
Deshalb setzt der Installer nun auch `SETUPTOOLS_SCM_PRETEND_VERSION` ausschliesslich
in seiner privaten Buildumgebung, nicht im System oder Benutzerprofil.
Die erwartete Version und der Quellpin bleiben unveraendert.

Die Wheel-Metadaten werden unmittelbar nach dem Build auf Paketname und exakte Version
geprueft, noch vor der Aufloesung und Installation der Runtime-Abhaengigkeiten.
Die abschliessende geschuetzte Importprobe bleibt verpflichtend. Es wird weder jede beliebige
Entwicklungsversion akzeptiert noch ein fehlgeschlagener Build als installiert markiert.
Offline-Regressionstests ersetzen weiterhin keinen erfolgreichen Linux-/WSL-Gesamtlauf.

[build-source]: https://github.com/open-jarvis/OpenJarvis/blob/a9e59e8770f92dd8046c2e5fcc1246eef51bb96a/pyproject.toml
[hatch-vcs-source]: https://github.com/ofek/hatch-vcs/blob/v0.5.0/hatch_vcs/version_source.py

### Paketdownload: Timeouts und DNS-Abbruch

Ein weiterer WSL-Lauf am 20.11.2026 scheiterte zuerst an einem Netzwerk-Timeout beim
`aiohttp`-Download und im zweiten Versuch an der Namensaufloesung fuer `files.pythonhosted.org`
beim Download von `huggingface-hub`. Das ist kein Nachweis fuer defekte Modellgewichte,
eine fehlende Buildbasis oder eine erfolgreiche OpenJarvis-Installation.

Der gemeinsame Python-Installer benennt DNS-Abbrueche jetzt auch in der abschliessenden
Fehlermeldung. Ein ausdruecklich voruebergehender DNS-Fehler im ersten Versuch darf den
bereits vorgesehenen zweiten Versuch nutzen. Insgesamt bleiben es hoechstens zwei Versuche
im selben 7200-Sekunden-Budget, mit gleicher Lockdatei, gleichem Cache, Hashpflicht und TLS.
Ein DNS-Fehler im zweiten Versuch startet keinen dritten Versuch; Hash-, Zertifikats-,
Zugriffs- und Speicherfehler werden nicht als temporaere DNS-Probleme umgedeutet.
Keine automatische DNS-/WSL-Reparatur, kein Mirror, keine alternativen Paketquellen oder IP-Tricks.
Die Ursache einer anhaltend gestoerten WSL-/Host-Netzverbindung ist damit nicht behoben.

OpenJarvis ist ein Agenten-/SDK-Framework, kein mitgeliefertes LLM und kein Modellgewicht.
Es kann bestehende Inferenz-Backends wie Ollama ansprechen. Die Website nennt weitere
Engines, Werkzeuge, Speicher und Lernwege; deren vollstaendige Integration wird hier nicht behauptet.

## Setup-Installation und Lifecycle

Im Tools-Menue **OpenJarvis** auswaehlen. Fehlende freigegebene Voraussetzungen
einzeln oder ueber die einmalige Stapelfreigabe zulassen. Direkter Weg aus dem Setup-Checkout:

```bash
bash scripts/tools/openjarvis_install.sh --install-build-deps
bash scripts/tools/openjarvis_status.sh
bash scripts/tools/openjarvis_check.sh
bash scripts/tools/openjarvis_doctor.sh
```

Der aktuelle native Buildpfad ist fuer Linux/WSL vorgesehen. Ubuntu 26 mit
System-Python 3.14 nutzt bei Bedarf eine private CPython-3.12.12-Basis nach Zustimmung;
das System-Python wird nicht ersetzt. Debian-/DietPi-/ARM-Systeme brauchen passende
Ressourcen und verfuegbare Wheels; keine pauschale Plattformabnahme.
Native Windows-/macOS-Pakete sind Upstream-Optionen, nicht dieser Linux-Buildpfad.
Android/iOS sind durch diesen Eintrag weder installiert noch als mobile Runtime getestet.

Konservative Reserve: 12 GiB Disk und 2 GiB RAM, unter WSL zusaetzlich die
Host-Speicherpruefung; Modellgewichte und spaetere GUI-/Rust-Builds sind nicht enthalten.
Private Datenbasis: `~/.openclaw_ultimate_user_data/tools/openjarvis/`.
Der Build liegt darunter in `native-github/`, getrennt von Hermes und vorhandenen OpenJarvis-Daten.

Der Installer baut ein Python-Wheel aus dem Pin, installiert nur die Kernabhaengigkeiten
in einer privaten venv und erzwingt SHA256-gesperrte Paketinstallationen.
Kein `curl | bash`, `quickstart.sh`, `uv sync --all-extras` oder globaler `jarvis`-Befehl wird eingerichtet.
Kein Docker-/Compose-Fallback. Upstream-Buildcode wird ausgefuehrt: eine private venv ist keine Sandbox.
Die begrenzte Importprobe blockiert Netzwerk und Unterprozesse und erzeugt keinen Agenten.
CLI-Datei, Buildnachweis und Python-SBOM werden erfasst, keine komplette Produktivabnahme.

```bash
bash scripts/tools/openjarvis_update.sh --install-build-deps
bash scripts/tools/openjarvis_uninstall.sh
```

Update bleibt am dokumentierten Pin. Geaenderte oder fremde Dateien verhindern eine
automatische Uebernahme/Entfernung; kein Reset und keine Loeschung von `~/.openjarvis`.
Status/Check pruefen Buildnachweise, keine Dienstgesundheit. Doctor kann ohne
gesonderte Laufzeitabnahme unvollstaendig bleiben. Keine automatische systemd-/K8s-Unit:
dieser Eintrag installiert eine CLI/SDK-Basis, keinen laufenden Dienst.

## Ollama und bewusster erster Start

Ollama und ein passendes Modell separat ueber deren Setup-Wege einrichten.
Der [Ollama-Adapter am Pin][ollama-source] nutzt standardmaessig
`http://localhost:11434`; bei entfernten Backends sind Transport, Authentifizierung
und Firewall gesondert abzusichern. Eine lokale API nicht ungeprueft ins Internet veroeffentlichen.

Nach erfolgreicher Installation und eigener Freigabe kann die private CLI manuell gestartet werden:

```bash
jarvis_bin="$HOME/.openclaw_ultimate_user_data/tools/openjarvis/native-github/venv/bin/jarvis"
"$jarvis_bin" --help
```

Ein Aufruf ohne Argumente kann Upstream-Ersteinrichtung oder Chat starten.
`jarvis init`, Modellverwaltung, Agenten, E-Mail-/Kalenderverbindungen, Scans,
OAuth, Scheduler und Cloud-APIs sind **keine** Installationsschritte dieses Setups.
Das [chat-simple-Preset][chat-source] ist ein Ausgangspunkt ohne Werkzeuge;
Modellname, Datenpfade und Providerwahl vor einer bewussten Uebernahme selbst festlegen.
Keine existierende Konfiguration mit `--force` ueberschreiben.

Die [Telemetriedokumentation am Pin][telemetry-source] unterscheidet lokale
Leistungsdaten von optionaler externer Nutzungsanalyse. Vor dem ersten echten
Start `[analytics] enabled = false` pruefen, wenn keine externe Analyse gewuenscht ist.
Eine vorhandene ausdrueckliche Zustimmung wird durch diesen Installer nicht heimlich geaendert.
Cloud- und Connector-Konfiguration kann Daten nach aussen senden; local-first ist kein pauschaler Datenschutzbeweis.

## Getrennte Ausbaustufen

| Ausbau | Noch erforderliche Arbeit |
| --- | --- |
| Browser-GUI | Server-Extras, Node-/Frontend-Build, Loopback-Bindung, Authentifizierung und manueller Start; nicht mit dem CLI-Wheel ausgeliefert |
| Desktop-Paket | Eigener Tauri-/Plattformbuild oder getrennt verifiziertes Release-Paket samt Signatur-/Integritaetspruefung; nicht automatisch installiert |
| Rust-Erweiterung | Gepinnte Cargo-/Maturin-Toolchain, eigener nativer Build und Funktionsprobe; im CLI-/SDK-Basisumfang nicht gebaut |
| Inferenz und Lernen | Eigenes Backend, separat lizenzierte Gewichte, Ressourcen-/Qualitaetstest und bewusste Datenfreigabe; keine automatischen Trainings- oder Modellauftraege |

Weiter: [Hermes-Abgrenzung](jarvis-hermes-dashboard.md),
[native Python-Builds](python-reviewed-native.md),
[Installationsrichtlinie](../INSTALLATION_POLICY.md).

[install-source]: https://github.com/open-jarvis/OpenJarvis/blob/a9e59e8770f92dd8046c2e5fcc1246eef51bb96a/docs/getting-started/installation.md
[license-source]: https://github.com/open-jarvis/OpenJarvis/blob/a9e59e8770f92dd8046c2e5fcc1246eef51bb96a/LICENSE
[ollama-source]: https://github.com/open-jarvis/OpenJarvis/blob/a9e59e8770f92dd8046c2e5fcc1246eef51bb96a/src/openjarvis/engine/ollama.py
[chat-source]: https://github.com/open-jarvis/OpenJarvis/blob/a9e59e8770f92dd8046c2e5fcc1246eef51bb96a/configs/openjarvis/examples/chat-simple.toml
[telemetry-source]: https://github.com/open-jarvis/OpenJarvis/blob/a9e59e8770f92dd8046c2e5fcc1246eef51bb96a/docs/telemetry.md

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
python3 -I -B scripts/tool_commands.py show openjarvis
```

### SSH-Aktionen: `openjarvis`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run openjarvis --action status
python3 -I -B scripts/tool_commands.py run openjarvis --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run openjarvis --action install --apply --confirm openjarvis:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run openjarvis --action update --apply --confirm openjarvis:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run openjarvis --action uninstall --apply --confirm openjarvis:uninstall
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
