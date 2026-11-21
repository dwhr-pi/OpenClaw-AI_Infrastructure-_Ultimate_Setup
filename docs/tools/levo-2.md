# LeVo 2

Vollstaendige Songs aus strukturierten Lyrics und Stilvorgaben; LLM-/Diffusions-Forschung, kein CPU-TTS.

Optionaler Menuepunkt **LeVo_2**, Bereitschaft `planned`, keine fertige Runtime.
Primaerquelle: [levo-demo/LeVo](https://github.com/levo-demo/LeVo).
Gepruefter Pin: `653cbcf4716101834900c75b7d5da43b07e15d5b`.
README und vorhandene Lizenzdateien werden gegen die SHA256 im Quellenmanifest geprueft.

## Lizenz und Risiken

Die LICENSE am Pin erlaubt nur akademische, Forschungs- und Bildungszwecke und schliesst kommerzielle sowie
produktive Nutzung aus. "Commercial-grade" in der README ist keine kommerzielle Lizenzfreigabe.

Der dokumentierte Docker-Einstieg wird nicht uebernommen. Checkpoints, Codec, GPU-Runtime und
Musik-/Stimmenrechte sind separat zu pruefen; kein automatischer Wechsel auf andere SongGeneration-Versionen.

## Native Quellenverwaltung

Python 3 und Git erforderlich; 2048 MiB Reserve nur fuer Quellen, nicht fuer
Modelle oder GPU-Builds. Kein Docker-Fallback. Keine Pakete, Gewichte, GUI,
Modelle, Audio, Trainingslaeufe, APIs oder Dienste automatisch starten.

### Git-Download bei Verbindungsstillstand

Der gemeldete Abbruch bei etwa 62 Prozent entstand vor Checkout und Build durch
das Git-Zeitlimit, nicht durch eine belegte Python-/GPU-Inkompatibilitaet.
Die genaue Netzwerk-/Hostursache ist aus dem Log nicht bestimmbar.
Der gemeinsame Downloader verwendet HTTP/1.1 und erkennt HTTP-Transfers unter
1 KiB/s ueber 120 Sekunden als Stillstand. Bei Timeout oder erkannten transienten
Transportfehlern folgt hoechstens ein Neuversuch desselben Fetch-Befehls und Pins.
Standard bleibt ein Gesamtbudget von 900 Sekunden; ein laufender erster Versuch
darf es ausnutzen. Ein Neuversuch erhaelt nur die Restzeit. Kein Spiegelserver,
kein anderer Branch und kein Abschalten der TLS-/Pin-/Hashpruefung.
Authentifizierungs-, Zertifikats- und unbekannte Fehler bleiben ohne Neuversuch
blockierend. Abbruch durch den Benutzer wird nicht wiederholt.
Schlaegt auch der zweite Versuch fehl, bleiben Installation und Erfolgsmarker aus;
die bestehende begrenzte Bereinigung und die Logs bleiben erhalten.
Diese Transportkorrektur ist kein erfolgreicher Download-/Runtime-Nachweis unter WSL.

```bash
bash scripts/tools/levo_2_install.sh --dry-run
bash scripts/tools/levo_2_install.sh
bash scripts/tools/levo_2_status.sh
bash scripts/tools/levo_2_doctor.sh
bash scripts/tools/levo_2_update.sh --dry-run
bash scripts/tools/levo_2_uninstall.sh --dry-run
```

`source_prepared` ist kein Buildnachweis: `installed: false`, `runtime_tested: false`.
Doctor prueft Origin, Pin, Vertragsdateien und Inventar; kein Modelltest.
Update bleibt beim Pin. Uninstall ohne `--dry-run` entfernt nur unveraenderte,
inventarisierte Quellen mit Besitznachweis unter
`~/.openclaw_ultimate_user_data/tools/levo_2/`. Geaenderte Dateien sperren die
Entfernung. Logs, Modelle und sonstige Benutzerdateien bleiben erhalten.
Keine systemd-Unit fuer reine Quellenverwaltung. Vollstaendiger nativer
Runtime-Build, Dependency-Lock/SBOM, Gewichtsrechte und End-to-End-Test offen.

## Verwendung im Setup

[Musik-/Lyrics-Katalog](../MUSIC_LYRICS_MODEL_CATALOG.md),
[Reim-/Lyric-Pruefung](../CREATIVE_LYRICS.md),
[Open Weights und Einrichtung](../models/README.md).
Keine automatische Uebernahme von Modellantworten als gepruefte Reime,
Musikrechte oder Fine-Tuning-Daten. Lyrics und Audio brauchen eigene Freigaben.

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
python3 -I -B scripts/tool_commands.py show levo_2
```

### SSH-Aktionen: `levo_2`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`LeVo_2` (ID `levo_2`) waehlen und die Einzelfreigaben lesen.
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
