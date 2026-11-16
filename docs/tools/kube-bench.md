# Kube Bench: nativer Build, kein automatischer Audit

Quelle: [aquasecurity/kube-bench](https://github.com/aquasecurity/kube-bench).
Version **v0.16.0**, Commit `5c6c22d51b926020e7414e1f1e051851d1a2feff`,
geprueft am 16.11.2026. Apache-2.0 fuer den Code; CIS-Benchmark-Inhalte und ihre
Nutzungsbedingungen getrennt beachten. Originale [Lizenz am Pin][license].

## Einrichtung im Setup

Der Menueeintrag **Kube_Bench** hat jetzt einen nativen Go-Build statt des
gesperrten Platzhalters. Ein geeignetes vorhandenes Go >=1.26.3 wird bevorzugt.
Fehlt es, bietet das Setup nach Zustimmung die bestehende private, SHA256-gepruefte
Go-Bereitstellung an. Kein Wechsel des System-Go, kein globaler PATH-Eintrag.
Debian, Ubuntu und WSL/Linux sind Buildumgebungen, keine automatisch geprueften Auditziele.

```bash
bash scripts/tools/kube_bench_install.sh --dry-run
bash scripts/tools/kube_bench_install.sh --install-build-deps
bash scripts/tools/kube_bench_status.sh
bash scripts/tools/kube_bench_doctor.sh
```

Voraussetzungen: vorhandenes Python >=3.10 und Git, mindestens 8192 MiB Diskreserve
und 2048 MiB verfuegbarer RAM. Der optionale private Go-Bootstrap benoetigt weitere
Reserve; der Installer prueft diese vor dem Download. Keine apt-Installation eines Scanners,
kein Container-Fallback und kein sudo fuer den eigentlichen Build.

Privates Ziel: `~/.openclaw_ultimate_user_data/tools/kube_bench/native-github/`.
Binary: `bin/kube-bench`. Zugehoerige Benchmark-Dateien: `source/cfg/`.
Alle stammen vom selben festen Commit; keine automatisch nachgeladenen neueren Rulesets.
`go.mod`, `go.sum`, Lizenz, Versionscode und Hauptkonfiguration haben feste SHA256-Vertraege.
`go mod download` und `go mod verify` gehen dem `-mod=readonly`-Build voraus.
Die Version wird beim Linken fest auf 0.16.0 gesetzt, nicht aus einem beliebigen main abgeleitet.

## Was die Installationsprobe tut

Der Installer ruft nur den Unterbefehl **`version`** auf, maximal 30 Sekunden,
mit ausdruecklich ausgewaehlter Konfiguration aus dem neuen privaten Checkout.
Es werden keine Kubeconfig-/Cloud-Umgebungsvariablen an die Probe weitergereicht.
Wichtig: `--version` ist bei kube-bench eine Kubernetes-Zielversionsoption,
nicht derselbe Befehl wie die scanfreie Ausgabe der Programmversion.

Kein Standardaufruf ohne Unterbefehl, Host-/Cluster-Audit, kubectl, AWS-Upload,
Datenbankzugriff oder automatische Root-Freigabe. Auf dem Windows-Entwicklungssystem
wurde kein echter Linux-Build und kein CIS-Benchmark ausgefuehrt.
Ein Buildnachweis ist keine Compliance- oder Kubernetes-Sicherheitsfreigabe.

## Inventar und Lifecycle

`kube-bench-build-lock.json` dokumentiert Pin, Quellhashes und die vollstaendigen
Dateihashes von `cfg/`. Die Konfiguration wird nach dem Build erneut verglichen.
`kube-bench-sbom.cdx.json` nennt Hauptkomponente und in `go.sum` deklarierte Module;
dies ist keine vollstaendige Binary-Reachability-/OS-SBOM.
`kube-bench-version-probe.json` dokumentiert die Version und den nicht ausgefuehrten Audit.
Binary, Nachweise und Benchmark-Dateien werden im Buildmarker SHA256-inventarisiert.

```bash
bash scripts/tools/kube_bench_update.sh --dry-run
bash scripts/tools/kube_bench_uninstall.sh --dry-run
```

Update bleibt am Pin. Uninstall entfernt nur den unveraenderten eigenen Buildbaum.
Logs, externe Auditberichte, fremde Installationen und private Go-Toolchains bleiben erhalten.
Eigene Aenderungen an cfg/ erst ausserhalb des Buildbaums sichern; Doctor/Uninstall
akzeptieren keinen veraenderten Bestand als original. Keine systemd-Unit erforderlich:
Dieses Rezept installiert eine bewusst auszufuehrende CLI, keinen Dienst oder Kubernetes-Job.

## Einen echten Audit getrennt freigeben

Vor Ausfuehrung Zielmaschine/Cluster, Kubernetes-/CIS-Zuordnung, Benchmark-Profil,
benoetigte Leserechte und Aufbewahrung sensitiver Reports klaeren.
Nicht jede Kubernetes-Version entspricht genau einer CIS-Benchmark-Version.
Eine frische WSL ohne Kubernetes-Node ist kein geeignetes CIS-Node-Abnahmeziel.
Keine pauschalen Root-Rechte oder Remediationen durch den Installer.
[Offizielle Ausfuehrungsanleitung am Pin][running] und
[Benchmark-Zuordnung am Pin][platforms] lesen; reale Audits bleiben eine separate Benutzeraktion.
Die Anbindung bestehender Audit-Wrapper an den privaten Binary-/cfg-Pfad ist separat zu pruefen.

[Infrastruktur-Kandidaten](infrastructure-candidates.md),
[Systemdiagnose](../SYSTEM_DIAGNOSTICS.md).

[license]: https://github.com/aquasecurity/kube-bench/blob/5c6c22d51b926020e7414e1f1e051851d1a2feff/LICENSE
[running]: https://github.com/aquasecurity/kube-bench/blob/5c6c22d51b926020e7414e1f1e051851d1a2feff/docs/running.md
[platforms]: https://github.com/aquasecurity/kube-bench/blob/5c6c22d51b926020e7414e1f1e051851d1a2feff/docs/platforms.md

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
python3 -I -B scripts/tool_commands.py show kube_bench
```

### SSH-Aktionen: `kube_bench`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run kube_bench --action status
python3 -I -B scripts/tool_commands.py run kube_bench --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run kube_bench --action install --apply --confirm kube_bench:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run kube_bench --action update --apply --confirm kube_bench:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run kube_bench --action uninstall --apply --confirm kube_bench:uninstall
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
