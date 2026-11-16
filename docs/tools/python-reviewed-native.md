# Phoenix, Checkov und Ragas nativ installieren

Die drei Menueeintraege erhalten private Source-Wheel-Installer statt Dokumentations-Platzhalter.
Quellen, vollstaendige Pins, Lizenz und SHA256-Vertraege stehen im
[Quellenmanifest](../../config/native-candidates/python-reviewed.json).
Phoenix ist unter Elastic-2.0 lizenziert; das ist keine pauschale Open-Source-/SaaS-Freigabe.

## Installation

Im geprueften Setup-Verzeichnis einen der folgenden Installer auswaehlen:

```bash
bash scripts/tools/phoenix_install.sh --install-build-deps
bash scripts/tools/checkov_install.sh --install-build-deps
bash scripts/tools/ragas_install.sh --install-build-deps
```

Das gleiche Zustimmungsfenster erscheint im Setup-Menue. Vorhandenes kompatibles Python wird bevorzugt;
bei Bedarf wird eine private Python-3.12-Laufzeit angelegt, ohne das System-Python zu ersetzen.
uv sowie die Phoenix-Frontend-Basis werden getrennt und mit Integritaetsnachweisen eingerichtet.
Abhaengigkeiten werden beim Installieren aufgeloest und mit Hashes gesperrt, danach mit Hashpruefung installiert.
Dies ist kein vorab vollstaendig auditierter Upstream-Dependency-Lock.
Phoenix wird einschliesslich seines Frontends gebaut, nicht als unsichtbares Backend-only-Paket.

Installationsziel: `~/.openclaw_ultimate_user_data/tools/TOOL/native-github/`.
Die `venv`, Source-Wheels, Hash-Locks, SBOM und Importprobe bleiben im privaten Toolverzeichnis.
Checkov startet keinen IaC-Scan; Ragas ruft weder LLM-Judges noch Provider auf.
Die begrenzte Python-Probe blockiert Netzwerk-/Unterprozessaufrufe vor dem Import.
Phoenix startet keinen HTTP-/Tracing-Dienst. Auth, Datenbank, Trace-Redaction und Betrieb sind separat abzunehmen.

## Pruefung und Lifecycle

```bash
bash scripts/tools/phoenix_status.sh
bash scripts/tools/phoenix_doctor.sh
bash scripts/tools/phoenix_update.sh --install-build-deps
bash scripts/tools/phoenix_uninstall.sh
```

Analog `phoenix` durch `checkov` oder `ragas` ersetzen. Update bleibt am geprueften Pin;
kein stilles Wechseln auf einen aktuellen Branch. Deinstallation entfernt nur unveraenderte,
belegte eigene Programmdateien, keine fremden Installationen, Laufzeitdaten oder gemeinsame Toolchains.
Ein bestandener Offline-Test ist kein erfolgreicher Ubuntu-/WSL-Build und kein Betriebsnachweis.
Die echte Linux-Build- und Dienstabnahme steht noch aus.

Quellen: [Phoenix](https://github.com/Arize-ai/phoenix),
[Checkov](https://github.com/bridgecrewio/checkov), [Ragas](https://github.com/vibrantlabsai/ragas).

Fuer SSH gilt dieselbe Installation in einem geprueften Checkout auf dem Zielhost;
keine Zugangsdaten in Git und kein automatisches Port-Forwarding oder Dienst-Enable.

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
python3 -I -B scripts/tool_commands.py show checkov
python3 -I -B scripts/tool_commands.py show phoenix
python3 -I -B scripts/tool_commands.py show ragas
```

### SSH-Aktionen: `checkov`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run checkov --action status
python3 -I -B scripts/tool_commands.py run checkov --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run checkov --action install --apply --confirm checkov:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run checkov --action update --apply --confirm checkov:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run checkov --action uninstall --apply --confirm checkov:uninstall
```

Fehlende Build-Abhaengigkeiten stoppen den Versuch. Nur fuer Install/Update
`--install-build-deps` nach separater Download-Freigabe ergaenzen. Kein Auto-Yes,
kein Docker-Fallback; Source-Build/Status ist keine erfolgreiche Runtime-Abnahme.

### SSH-Aktionen: `phoenix`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run phoenix --action status
python3 -I -B scripts/tool_commands.py run phoenix --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run phoenix --action install --apply --confirm phoenix:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run phoenix --action update --apply --confirm phoenix:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run phoenix --action uninstall --apply --confirm phoenix:uninstall
```

Fehlende Build-Abhaengigkeiten stoppen den Versuch. Nur fuer Install/Update
`--install-build-deps` nach separater Download-Freigabe ergaenzen. Kein Auto-Yes,
kein Docker-Fallback; Source-Build/Status ist keine erfolgreiche Runtime-Abnahme.

### SSH-Aktionen: `ragas`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run ragas --action status
python3 -I -B scripts/tool_commands.py run ragas --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run ragas --action install --apply --confirm ragas:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run ragas --action update --apply --confirm ragas:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run ragas --action uninstall --apply --confirm ragas:uninstall
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
