# Outlines: strukturierte lokale Textausgabe

Optionales Tool **Outlines**, Status `experimental` / `planned`.
Primaerquelle [dottxt-ai/outlines](https://github.com/dottxt-ai/outlines), Apache-2.0.
Gepruefter Pin: `c52af8472c6fe8a607a733ec11b709476af77a96`.
README, LICENSE und Regex-API-Dokument werden gegen feste SHA256 geprueft.

Outlines beschraenkt Ausgabeformen, beispielsweise durch Regex oder Schemas.
Es beweist weder phonetisch perfekte Reime noch korrekte Silben oder natuerliches
Metrum. Modell, Tokenizer und Backend sind separate Voraussetzungen.

## Installation und Lifecycle

Der Setup-Installer baut jetzt eine **private Python-Basisumgebung aus GitHub**,
mit dem upstream `uv.lock`, ohne optionale Modell-Backends. Linux/WSL,
Python >=3.10 und <3.14, Git und 4096 MiB Diskreserve erforderlich.
Eine vorhandene geeignete uv-Basis wird bevorzugt. Fehlt sie, darf die bestehende
gepruefte private uv-Bereitstellung nur mit `--install-build-deps` herunterladen.
Keine Modelle, API-/Inferenz-/Dienststarts oder Docker-Fallbacks.

Der Installer-Interpreter darf neuer sein: Die Folgekorrektur waehlt fuer Outlines
ein bereits vorhandenes Python >=3.10 und <3.14. Bei ungeeignetem Dispatcher
werden die vorhandenen versionierten Interpreter (zuerst Python 3.12) geprueft.
Kein System-Python-/PATH-Umbau und kein Python-Download. Explizite Auswahl im
korrigierten Checkout: `OUTLINES_PYTHON_BIN=/usr/bin/python3.12`.
Ein inkompatibler expliziter Pfad wird nicht stillschweigend durch einen anderen ersetzt.

### Bisheriger PR-28-Checkout mit Python-Versionsfehler

Zuerst `/usr/bin/python3.12 --version` ausfuehren. Wenn der Interpreter vorhanden
ist, laesst sich im alten Checkout auch der Installer selbst damit starten:

```bash
GAP_TOOLS_PYTHON_BIN=/usr/bin/python3.12 bash scripts/tools/outlines_install.sh --install-build-deps
```

`GAP_TOOLS_PYTHON_BIN` betrifft den bestehenden Installer-Dispatcher;
`OUTLINES_PYTHON_BIN` betrifft erst die neue getrennte Runtime-Auswahl.
Der Versionsfehler ist kein Nachweis fuer ein Speicherproblem. Fehlendes uv
oder andere nachfolgende Buildfehler bleiben eigene, separat zu pruefende Schritte.

### Installation einzeln ausfuehren

```bash
bash scripts/tools/outlines_install.sh --dry-run
bash scripts/tools/outlines_install.sh
bash scripts/tools/outlines_install.sh --install-build-deps
bash scripts/tools/outlines_status.sh
bash scripts/tools/outlines_doctor.sh
bash scripts/tools/outlines_doctor.sh --smoke
bash scripts/tools/outlines_update.sh --dry-run
bash scripts/tools/outlines_uninstall.sh --dry-run
```

Die beiden Install-Befehle sind Alternativen. `installed: true` wird erst nach
Paketinstallation, Artefaktinventar und lokalem Regex-Importcheck geschrieben.
`runtime_tested: false` bleibt bestehen: keine echte Modell-/Decoding-Abnahme.
Doctor prueft offline Origin, Pin, Vertragsdateien und Inventar. Nur `--smoke`
fuehrt explizit den begrenzten lokalen Python-Importcheck aus, ohne Modellaufruf.
Update bleibt beim Pin. Uninstall ohne `--dry-run` entfernt nur unveraenderte
inventarisierte Quellen mit Besitznachweis unter
`~/.openclaw_ultimate_user_data/tools/outlines/`; eigene Aenderungen sperren
die Entfernung. Logs, Modelle und weitere Benutzerdaten bleiben erhalten.
`native-sbom.cdx.json` erfasst die installierten Python-Distributionen.
Der lokale Paket-Versionszusatz `0.0.0+git.<Pin>` ist kein upstream Release-Tag.
Keine systemd-Unit fuer diese Bibliothek. Optionale Backend-Builds und die echte
Decoding-Abnahme bleiben offen. Bestehende reine Quellen werden nicht automatisch
ersetzt; deren Lifecycle ist weiterhin mit `--source-only` erreichbar.
Nur beim alten Quellbestand bedeutet `source_prepared: true` weiterhin keine installierte Runtime.
Siehe [Testmatrix und Voraussetzungen](SOURCE_INSTALL_READINESS.md).

## Reim-/Lyric-Anwendung

[Offline-Pruefer und Outlines-Anbindung](../CREATIVE_LYRICS.md) mit AABB, ABAB,
ABBA und AAAA, IPA-Beispiellexikon und begrenzter Silben-/Betonungspruefung.
Der am Pin gepruefte API-Weg nutzt `outlines.from_transformers(...)`,
`outlines.types.Regex(...)` und `model(prompt, output_type, max_new_tokens=...)`.
Das alte `outlines.generate.regex` ist nicht als kompatibler Einstieg zugesagt.
[API am Pin](https://github.com/dottxt-ai/outlines/blob/c52af8472c6fe8a607a733ec11b709476af77a96/docs/features/core/output_types.md).
Keine automatischen Modell-Downloads; vorhandene lokale Artefakte gesondert
freigeben und nach [Modellhandbuch](../models/README.md) pruefen.

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
python3 -I -B scripts/tool_commands.py show outlines
```

### SSH-Aktionen: `outlines`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`Outlines` (ID `outlines`) waehlen und die Einzelfreigaben lesen.
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
