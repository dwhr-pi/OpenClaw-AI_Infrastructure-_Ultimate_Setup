# eSpeak NG: optionale Aussprache- und IPA-Hilfe

Optionales Tool **eSpeak_NG**, Status `experimental` / `planned`.
Primaerquelle [espeak-ng/espeak-ng](https://github.com/espeak-ng/espeak-ng),
Pin `688cb60368d6e0998f3632af8d1c3c2ad4191fc2`.
GPL-3.0-or-later; weitere Daten-/Komponentenlizenzen getrennt pruefen.
README und COPYING werden gegen feste SHA256 geprueft.

## Installation und Lifecycle

Jetzt **nativer CMake-Build mit Sprachdaten im privaten Tool-Verzeichnis**.
Linux/WSL, Python 3, Git, CMake, Make und C-Compiler erforderlich; 4096 MiB
Mindestreserve, keine gemessene Runtime-Groesse. Keine globale Installation,
Audiowiedergabe, Docker oder automatischer Dienststart. Optionale pcaudiolib-,
Sonic-, MBROLA- und SpeechPlayer-Anbindungen bleiben deaktiviert.

Bei `cmake fehlt` oder fehlendem Make/C-Compiler zuerst nur die Ubuntu-
Build-Voraussetzungen einrichten, nicht eSpeak aus einem anderen Paket installieren:

```bash
sudo apt-get update
sudo apt-get install --no-install-recommends cmake build-essential
```

Danach den folgenden Installationsbefehl erneut ausfuehren. Diese APT-Schritte
installieren Buildwerkzeuge und starten keinen eSpeak-Dienst.

```bash
bash scripts/tools/espeak_ng_install.sh --dry-run
bash scripts/tools/espeak_ng_install.sh
bash scripts/tools/espeak_ng_status.sh
bash scripts/tools/espeak_ng_doctor.sh
bash scripts/tools/espeak_ng_doctor.sh --smoke
bash scripts/tools/espeak_ng_update.sh --dry-run
bash scripts/tools/espeak_ng_uninstall.sh --dry-run
```

`installed: true` folgt erst nach Build, privater Installation und `--version`-Probe.
`runtime_tested: false` bedeutet weiterhin: keine Aussprache-/Audio-Abnahme.
Doctor prueft Pin/Origin/Hashvertraege/Inventar; nur `--smoke` startet explizit
die begrenzte `--version`-Probe, keine Audiowiedergabe.
Update bleibt beim Pin. Uninstall ohne `--dry-run` entfernt nur unveraenderte
Quellen mit Besitznachweis unter `~/.openclaw_ultimate_user_data/tools/espeak_ng/`.
Bei eigenen Aenderungen Abbruch; Logs, Modelle und andere Benutzerdaten bleiben.
Keine systemd-Unit fuer die CLI. `native-sbom.cdx.json` erfasst die Hauptkomponente,
nicht den vollstaendigen Compiler-/Systembibliothekenbaum. Compiler-/OS-Versionen
und echte Aussprache-Abnahme sind im Linux-Testprotokoll zu erfassen.
Alte reine Quellen sind separat mit `--source-only` verwaltbar und werden nicht
stillschweigend ersetzt. Siehe [Testmatrix](SOURCE_INSTALL_READINESS.md).
Beim alten Quellbestand ist `source_prepared: true` weiterhin kein Buildnachweis.

## Nutzung nach gesondertem nativem Build

Eine bewusst bereitgestellte native Binary kann IPA lautlos ausgeben:

```bash
espeak-ng -q -v de --ipa 'Nacht Pracht Licht Pflicht'
```

`-q` unterdrueckt Sprachausgabe; `--ipa` gibt Lautschrift aus.
[Manpage am Pin](https://github.com/espeak-ng/espeak-ng/blob/688cb60368d6e0998f3632af8d1c3c2ad4191fc2/src/espeak-ng.1.ronn).
Der Befehl wurde hier nicht ausgefuehrt. Aussprachevorschlaege sind keine
verbindliche Reim-/Metrik-Abnahme: Dialekt, Mehrdeutigkeit und Kontext pruefen.
Ausgabe nicht ungeprueft in ein autoritatives Reimlexikon uebernehmen.
[Lyrics-Workflow](../CREATIVE_LYRICS.md) nutzt standardmaessig nur ein kleines
lokales Beispiellexikon, keine externe Phonetik- oder Cloud-API.

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
python3 -I -B scripts/tool_commands.py show espeak_ng
```

### SSH-Aktionen: `espeak_ng`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`eSpeak_NG` (ID `espeak_ng`) waehlen und die Einzelfreigaben lesen.
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
