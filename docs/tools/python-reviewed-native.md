# Phoenix, Checkov, Ragas und OpenJarvis nativ installieren

[OpenJarvis](openjarvis.md) nutzt denselben geprueften Source-Wheel-Lifecycle,
aber ausschliesslich fuer die CLI-/SDK-Basis. GUI, Desktop-Paket und Rust-Erweiterung
sind getrennte Ausbaustufen; kein Quickstart-Autostart oder automatischer Modelldownload.

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
Dabei bleibt `subprocess.Popen` als Klasse erhalten, damit Typannotationen und Bibliotheksimporte funktionieren.
Ein CPython-Audit-Hook und Socket-Sperren verhindern die erfassten Prozess-/Netzwerkaufrufe;
dies ist keine Betriebssystem-Sandbox fuer nicht vertrauenswuerdigen Code.
Buildschritte zeigen laufende Ausgabe, Prozess-ID und regelmaessige Lebenszeichen statt still zu warten.
Scheitert die 45-Sekunden-Importprobe, protokolliert sie begrenzte, bereinigte Fehlerausgabe und bleibt fehlgeschlagen.
Im gemeldeten Phoenix-Versuch fehlte diese Ausgabe; die konkrete Importursache ist deshalb noch nicht belegt.
Phoenix startet keinen HTTP-/Tracing-Dienst. Auth, Datenbank, Trace-Redaction und Betrieb sind separat abzunehmen.

## Pruefung und Lifecycle

### Ragas: pyarrow-Download-Timeout (20.11.2026)

Der Lauf `20261120_163907` scheiterte beim Download des etwa 52,5 MiB grossen
`pyarrow==26.0.1`-Wheels nach dem 300s-HTTP-Lesefenster. Die verschachtelte
Extraktionsmeldung nennt ausdruecklich einen Netzwerk-Timeout, nicht einen
belegten Python-/Quellcodefehler. Ein allgemeiner I/O-Fehler reicht nicht fuer einen Retry.

Nur bei ausdruecklichem Wheel-Download-Timeout wiederholt der Installer die
hashgesperrte `uv pip install`-Phase hoechstens einmal. Der letzte Versuch nutzt
900s HTTP-Lesezeitlimit und einen statt zwei paralleler Downloads. Beide
Versuche teilen ein Installationsbudget von 7200s; die Aufloesung, der
Source-Wheel-Build und die Lockdatei werden nicht wiederholt. Derselbe private
Cache bleibt waehrend dieses Versuchs erhalten, ohne neue Persistenz ausserhalb
des bisherigen Besitz-/Rollback-Bereichs. Kein garantierter Download-Resume.
Verbindungsaufbau bleibt 30s, uv-interne HTTP-Wiederholungen bleiben auf drei begrenzt.

Hash-, Zertifikats-, Zugriffs- und Speicherfehler bleiben sofort blockierend,
auch wenn zusaetzlich ein Timeout genannt wird. Kein neuer Index/Mirror,
kein Hash-/TLS-Fallback, keine Paketversionsaenderung und kein dritter Versuch.
Ein Prozess-Timeout oder Benutzerabbruch wird nicht wiederholt. Ein erneuter
Fehler verhindert Probe und Erfolgsmarker; bisherige Nutzerdaten bleiben erhalten.
Die [offizielle uv-Referenz](https://docs.astral.sh/uv/reference/environment/)
beschreibt HTTP-Lesezeitlimit und Downloadparallelitaet. Offline-Fixtures
belegen die Grenzen, nicht eine erfolgreiche WSL-Installation oder Evaluation.

### Ragas 0.3.9 und LangChain-Kompatibilitaet (19.11.2026)

Der erneute WSL-Lauf konnte `hf-xet` und alle 95 Pakete laden. Erst die geschuetzte
Importprobe scheiterte: Ragas importiert `langchain_community.chat_models.vertexai`,
das im installierten Community-Paket 0.4.2 fehlt. `uv pip check` prueft deklarierte
Paketmetadaten, nicht die Existenz jedes importierten Moduls. Der
[gepruefte Ragas-Quellstand][ragas-legacy-source]
importiert diese alte API ohne passende obere LangChain-Versionsgrenzen.

Nur fuer Ragas 0.3.9 ergaenzt der Installer deshalb vor der Hash-Lock-Erzeugung:

```text
langchain-community==0.3.31
langchain>=0.3.27,<1.0
langchain-core>=0.3.78,<1.0
langchain-openai>=0.3,<1.0
```

Das [offizielle Community-Wheel 0.3.31](https://pypi.org/project/langchain-community/0.3.31/)
wurde ohne Installation oder Ausfuehrung nach Groesse und SHA256 geprueft;
es enthaelt das benoetigte Modul. SHA256:
`1c727e3ebbacd4d891b07bd440647668001cea3e39cbe732499ad655ec5cb569`.
Die Quelle von Ragas bleibt unveraendert gepinnt; kein Import-Shim, kein Ausblenden von Fehlern.
Hashes fuer die tatsaechlich aufgeloesten Pakete werden weiterhin vor Installation erzeugt
und erzwungen. Der Buildnachweis erfasst die zusaetzlichen Anforderungen; die Offline-Importprobe
bleibt 45 Sekunden begrenzt und sperrt Netzwerk-/Prozessaufrufe. Andere Tools erhalten diese Grenzen nicht.

**Legacy-Kompatibilitaet, keine Sicherheitsfreigabe:** LangChain Community ist laut PyPI archiviert.
Dieser Bereich repariert die belegte API-Unvertraeglichkeit des bestehenden experimentellen Pins,
beweist aber weder einen erfolgreichen kompletten WSL-Build noch Schwachstellenfreiheit.
Ein spaeteres Ragas-Upgrade mit gepflegten Providerpaketen und eigener Abnahme bleibt erforderlich.
Keine Evaluation, Cloudanmeldung oder LLM-Anfrage wird dabei gestartet.

### Langsame Paketdownloads (19.11.2026)

Der gemeldete Ragas-Lauf scheiterte beim Wheel-Download von `hf-xet==1.8.0`
auf `files.pythonhosted.org` durch einen HTTP-Timeout, nicht durch einen belegten
Python-Kompatibilitaetsfehler. Der gemeinsame Installer fuer Ragas, Phoenix und Checkov
setzt jetzt feste uv-Budgets: 300 Sekunden HTTP-Lesezeitlimit, 30 Sekunden Verbindungsaufbau,
hoechstens drei HTTP-Wiederholungen und zwei statt vier parallele Downloads.
Die Werte erscheinen im Installationsprotokoll; geerbte uv-Netzwerkoptionen werden nicht uebernommen.
Diese Parameter sind in der [offiziellen uv-Referenz](https://docs.astral.sh/uv/reference/environment/)
dokumentiert. Das Prozesslimit bleibt 7200 Sekunden je Python-Buildschritt, nicht je Gesamtinstallation.
Fuer Phoenix-Frontend-Schritte gilt die nachstehende Ausnahme.
Keine zusaetzliche Wiederholung des gesamten Builds, kein unsicherer Mirror, TLS-Bypass
oder Verzicht auf `--require-hashes` und reine Wheel-Abhaengigkeiten.
Ein weiterhin nicht erreichbarer Paketserver bleibt ein Fehler; die Aenderung garantiert
keinen Download bei DNS-/Netzausfall. Kein Modell-Download oder Provider-Aufruf.
Offline-Tests pruefen die Budgets, Umgebungsfilterung und den Abbruch ohne Erfolgsnachweis;
die erneute Installation unter WSL ist separat zu testen.

### Phoenix-Frontend ohne Zwei-Stunden-Abbruch (21.11.2026)

Ein gemeldeter WSL-Lauf wurde nach genau 7200 Sekunden bei
`pnpm install --frozen-lockfile --ignore-scripts` durch unser Prozesslimit beendet.
Ob der Prozess noch Fortschritt machte oder bereits hing, belegen die Heartbeats nicht.

Fuer die drei Phoenix-Frontend-Schritte `pnpm install`, `pnpm rebuild esbuild` und
`pnpm run build` gibt es jetzt kein automatisches Gesamtzeitlimit mehr.
Das Log meldet PID, Laufzeit und ausdruecklich `kein automatisches Zeitlimit`.
Ein haengender Prozess kann dadurch unbegrenzt weiterlaufen; Abbruch mit **Strg+C**
bleibt moeglich und wird nicht als Erfolg behandelt. Unter POSIX wird beim Abbruch
die gestartete Prozessgruppe beendet. Nichtnull-Exitcodes bleiben Fehler.

Unveraendert bleiben der Quellpin, das eingefrorene pnpm-Lockfile, die gezielte
esbuild-Freigabe, Integritaets-/Speicherpruefungen und der geschuetzte Rollback.
Git-, Python-Paketdownload-, Verbindungs- und Importprobe-Limits werden hierdurch
nicht entfernt; auch pnpm-interne Netzwerkfehler sind weiterhin moeglich.
Dies behebt keine DNS-Stoerung und ist keine erfolgreiche Phoenix-Laufzeitabnahme.

### Ragas: GitPython in der Offline-Importprobe (21.11.2026)

Ein WSL-Lauf installierte 92 Pakete und bestand `uv pip check`, scheiterte danach aber
beim Ragas-Import: GitPython wollte bereits bei der Initialisierung einen Git-Prozess
zur Versionspruefung starten. Das ist ein Konflikt mit unserer Prozesssperre, kein
belegter Download- oder Python-Versionsfehler.

Die Probe setzt ausschliesslich fuer Ragas und nur im kurzlebigen Pruefprozess
`GIT_PYTHON_REFRESH=quiet`. Ein versuchter `subprocess.Popen` bleibt vor dem Start
blockiert, meldet dort aber `PermissionError`: Diesen Fall behandelt die
[GitPython-3.2.1-Initialisierung][gitpython-refresh] als nicht verfuegbares Git.
Der [Modulimport][gitpython-import] kann damit ohne gestarteten Git-Prozess abschliessen.
Es werden weder GitPython/Ragas-Quellen veraendert noch Module oder Rueckgabewerte vorgetaeuscht.

Die Probe verlangt weiterhin Ragas 0.3.9, importierbare `evaluate`/`aevaluate` und
explizit `git.GIT_OK is False`. Netzwerk, Shell, andere Prozesswege und Git-Kommandos
bleiben gesperrt; `subprocess.Popen` bleibt als Klasse fuer Imports erhalten.
Die 45-Sekunden-Grenze bleibt bestehen. Der Bericht vermerkt `git_runtime_tested=false`:
Git-basierte Experimentversionierung und echte Evaluation sind nicht abgenommen.
Im spaeteren normalen Ragas-Betrieb wird dieser Probe-Schalter nicht gesetzt.
Ein erfolgreicher Gesamtlauf unter Linux/WSL ist separat nachzuweisen.

[gitpython-refresh]: https://github.com/gitpython-developers/GitPython/blob/3.2.1/git/cmd.py
[gitpython-import]: https://github.com/gitpython-developers/GitPython/blob/3.2.1/git/__init__.py

### Lifecycle-Befehle

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

[ragas-legacy-source]: https://github.com/vibrantlabsai/ragas/blob/8b4653c41abf6c8f86f63397f1a960d6411c0ca9/src/ragas/llms/base.py

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
