# Native Go-Controller und Temporal

Diese Kandidaten ersetzen Quellen-Platzhalter durch echte Go-Buildrezepte. Ein erfolgreicher
Build bedeutet **Binaerdateien vorhanden und gehasht**, nicht Kubernetes eingerichtet oder
Produktionsbetrieb abgenommen. Kein Docker-/Compose-Fallback, kein Cluster-Apply, Dienststart,
DNS-Test, Zertifikatsauftrag, Schema-Update oder Zugriff auf Benutzer-Secrets.

## Komponenten und Pins

Offizielle GitHub-Releases und vollstaendige Commits wurden am 16.11.2026 abgefragt.
Die autoritativen SHA256-Vertraege stehen in `config/native-candidates/go-controllers.json`.
Pins sind reproduzierbare Ausgangspunkte, keine Zusage einer dauerhaft aktuellen Sicherheitslage.

| Kandidat | Version / Mindest-Go | Tatsaechliche Buildkomponenten |
| --- | --- | --- |
| cert-manager | v1.21.3 / 1.26.0 | controller, cainjector, webhook, acmesolver, startupapicheck; jeweils eigenes `cmd/NAME`-Modul, Paket `.` |
| External_DNS | v0.24.0 / 1.27.3 | `external-dns` aus dem Root-Paket `.` |
| Kyverno | v1.20.0 / 1.27.3 | `./cmd/kyverno`, background-controller, cleanup-controller, reports-controller, kyverno-init, readiness-checker |
| Gatekeeper | v3.23.1 / 1.26.0 | `gatekeeper` aus Root-Paket `.`, nicht der gator-CLI |
| KEDA | v2.21.1 / 1.27.4 | `./cmd/operator`, `./cmd/adapter`, `./cmd/webhooks` |
| Temporal | v1.32.2 / 1.26.10 | `./cmd/server`, `./cmd/tools/sql`, `./cmd/tools/cassandra`; Tag `disable_grpc_modules`, CGO=0 wie Upstream |
| Argo_Workflows | v4.1.6 / 1.26.10 | `./cmd/workflow-controller`, `./cmd/argoexec`; kein CLI-/UI-/API-Server |

Offizielle Quellen mit Build-/Versionsvertraegen:

- [cert-manager am Pin](https://github.com/cert-manager/cert-manager/tree/925c22283de556172d48d96a165dc2fa27f7a6ff):
  `make/server.mk`, `cmd/*/go.mod`, `pkg/util/version.go`.
- [ExternalDNS am Pin](https://github.com/kubernetes-sigs/external-dns/tree/c40894ac060e0920b2b49035df18005954f83a7a):
  `Makefile`, `main.go`, `pkg/apis/externaldns/types.go`.
- [Kyverno am Pin](https://github.com/kyverno/kyverno/tree/f666af06e9bd310c7e730f1523c0430e90371a89):
  `Makefile`, `cmd/internal/version.go`, `pkg/version/version.go`.
- [Gatekeeper am Pin](https://github.com/open-policy-agent/gatekeeper/tree/2d0b6ad97cf3a8b8436a00a1f4b07b3a56b92ca0):
  `Makefile`, `main.go`.
- [KEDA am Pin](https://github.com/kedacore/keda/tree/43b5dfcd7a0a8a08e328b65667464986f60ee12c):
  `Makefile`, `go.mod`, `cmd/*/main.go`, `version/version.go`.
- [Temporal am Pin](https://github.com/temporalio/temporal/tree/6d085822273f4336796e6959c73ab1d14a23eb77):
  `Makefile`, `cmd/server/main.go`, `go.mod`.
- [Argo Workflows am Pin](https://github.com/argoproj/argo-workflows/tree/43021573c5a35cbafae009043c132dfcef43a112):
  `Makefile`, `cmd/workflow-controller/main.go`, `cmd/argoexec/main.go`.

## Hook-Vertrag fuer die Integration

Nur neue Dateien dieses Arbeitsbereichs integrieren; Registry, Menue, Wrapper und zentrales
Buildsystem werden separat gepflegt. Das Fragment hat das Format `{"tools":[...]}` und
die Rezeptart `candidate-native`, Helper `candidate_go_controllers`.

```python
backend.preflight(outer, spec, approved=install_build_deps)
artifacts = backend.build(source, prefix, spec, env)
```

`outer`, `source` und `prefix` sind absolute `Path`-Objekte. `source` ist der saubere Checkout
des vollstaendigen Pins, ueblicherweise `prefix/source`; Ausgabe liegt ausserhalb von `source`.
Die Rueckgabe ist eine Liste relativer regulaerer Dateien unter `prefix`, einschliesslich
Binaerdateien, statischer Dateien, kopierter Go-Locks und Receipts. Die zentrale Engine besitzt
Operation-Lock, Eigentums-/Pfadpruefung, Quellenbeschaffung und -Herkunftskontrolle, generelle
Disk-/RAM-Gates, Logs, Transaktion/Rollback, SHA256-Buildmarker, Status und Uninstall.

Integrationsanforderungen:

- Helper nur fuer die sieben IDs dieses Fragments freigeben, keine frei waehlbaren Python-Imports oder
  Shell-Schritte. `contract()` vergleicht alle vorgeschlagenen Rezeptfelder gegen das lokale Fragment.
- `candidate-native` vor `native_go.prepare/activate` behandeln: deren gemeinsame ID-Allowlist wird nicht
  veraendert. Der Helper prueft Go selbst und nutzt den geprueften privaten Bootstrap.
- Subprozess-Allowlist: `git` fuer HEAD/Status und das ausgewaehlte `go` fuer `version`, `build`, `mod verify`,
  `version -m`. Keine Ausfuehrung von `bin/*`, kein `go run`, `make`, Helm oder kubectl.
- Paket-Allowlist und Modulverzeichnisse entsprechen exakt `recipe.builds`; cert-manager hat fuenf verschachtelte
  Module. `recipe.ldflags` uebernimmt die jeweiligen Upstream-Versionvariablen, Argo einschliesslich Git-Metadaten.
- Kein generischer Binaer-Probe-Fallback bei leerem `recipe.probe`. `probe_mode=go-buildinfo` ist ausschliesslich
  statische Go-Tool-Inspektion, nicht `binary --version` oder `binary` ohne Argumente.
- Zurueckgegebene Artefakte inklusive Receipts in die zentrale Hash-/Besitzpruefung aufnehmen; erst danach
  Buildmarker schreiben. `check` prueft offline diese Hashes. `doctor`/Smoke ohne explizite Runtime-Abnahme bleibt
  unvollstaendig (Exit 3), kein Controllerstart als Diagnose.
- Idempotenter Uninstall entfernt nur belegte eigene Buildartefakte gemaess zentralem Besitzmarker. Kein
  Namespace-/CRD-/Datenbank-/DNS-/Zertifikat-Loeschen; bei geaenderten oder unbekannten Dateien Vorschau/Exit 3
  statt destruktiver Entfernung.

## Toolchain, Locks und Receipts

Vorhandenes passendes Go hat Vorrang. Fehlt es, ist ein neuer privater Download nur mit
explizitem `approved=True` erlaubt; ein bereits verifiziertes privates Go kann erneut genutzt
werden. Keine apt-Go-Installation und kein globaler PATH-/GOROOT-Wechsel. KEDA erhaelt einen
isolierten Go-1.27.4-Bootstrap; gemeinsame `private_go.VERSION`/`ARCHIVES` bleiben unveraendert.
[Offizielle Go-Metadaten](https://go.dev/dl/?mode=json&include=all) liefern diese festen Archive:

| Plattform | Bytes | SHA256 |
| --- | --- | --- |
| Linux amd64 | 70680823 | `7226736c2339719cda28fbf3a54d71aa63bcefe376e98cef00034268dab24840` |
| Linux arm64 | 67129258 | `3392582988a273a87ab5043ee1b2c9c17a2c3c00580bf9326c47a2e0aaaeac92` |

Der isolierte Bootstrap nutzt dieselben geprueften Download-, Groessen-, SHA256-, Entpack-,
Inventar- und Eigentumspruefungen wie `private_go.py`. Fuer andere Kandidaten bleibt der
vorhandene private 1.27.3-Pin ausreichend. Seine Metadaten stehen im gemeinsamen Helper.

Builds laufen mit `-mod=readonly -trimpath -buildvcs=true -p=2`, `CGO_ENABLED=0`,
`GOTOOLCHAIN=local`, `GOENV=off`, `GOWORK=off`, fester oeffentlicher Go-Proxy/SumDB und
maximal 7200 Sekunden je Komponente. Benutzer-GOFLAGS, Crossbuild-Variablen, kubeconfig und
Provider-Zugangsdaten werden nicht weitergereicht. Die zentrale Engine muss ein isoliertes
Build-HOME/GOCACHE/GOMODCACHE bereitstellen; keine Benutzerdaten als Build-HOME waehlen.

Vor und nach dem Build: voller Git-Pin, sauberer Checkout einschliesslich untracked/ignored
Dateien sowie SHA256 der primaeren Quellenvertraege. Root- und Untermodul-`go.mod`/`go.sum`
werden unveraendert nach `locks/` kopiert; abschliessend prueft `go mod verify` den Modulcache.
Ein Clone allein, eine leere Ausgabe oder ein geaenderter Lock wird nicht akzeptiert.

- `receipts/controller-build-lock.json`: Repo, Pin, Version, Go-Version, Buildbefehle,
  Quell-/Lock-/Artefakt-SHA256; Runtime-/Deployment-Abnahme ausdruecklich false.
- `receipts/controller-version-probe.json`: Ausgaben von `go version -m FILE`, passende VCS-Revision und sauberer
  VCS-Status; keine ausgefuehrte Anwendungsdatei.
- `receipts/controller-sbom.cdx.json`: CycloneDX 1.5 aus den im gebauten Binary eingebetteten Go-Abhaengigkeiten
  einschliesslich Replacement-Hinweisen. Keine Behauptung ueber Images, OS-Pakete, Cluster oder vollstaendige
  Runtime-Abhaengigkeiten.

Upstream-Versionsschnittstellen wurden nicht blind vereinheitlicht: ExternalDNS registriert
`--version`; Temporal verwendet urfave/cli mit `app.Version` (`--version`); Argo-Controller hat
ein `version`-Unterkommando. Kyverno protokolliert die Version waehrend des Starts, Gatekeeper
und KEDA haben keine hier freigegebene einheitliche Versions-Exit-Schnittstelle. Deshalb
fuehrt **keiner** dieser Build-/Diagnosepfade eine Anwendungs-Versionsprobe aus.

## Deployment bleibt separat

`share/upstream/` enthaelt ausschliesslich gepinnte statische Upstream-Dateien, keine gerenderten
oder angewendeten Ressourcen. Helm-Templates sind keine direkt anwendbaren YAML-Manifeste.
CRD-Vollstaendigkeit, Kubernetes-Kompatibilitaet, RBAC, Webhook-TLS und Namespace-Zuordnung
muessen vor einem bewusst separaten Deployment geprueft werden. Enthaltene Image-Verweise
sind Referenzen, keine Freigabe fuer Docker-Installation oder automatische Image-Pulls.

| Kandidat | Statische Dateien und noch offene Betriebsabnahme |
| --- | --- |
| cert-manager | CRDs, Chart, Manifestvorlagen; Webhook-CA, RBAC, Erreichbarkeit und Solver-Pod-Image separat. Keine Issuer-/ACME-Anfrage. |
| External_DNS | Standard-CRDs und Chart; Provider, minimale Zonenrechte, Domain-Filter, explizite Policy und TXT-Owner separat. Auch `--dry-run` ist keine sichere Diagnosefreigabe fuer alle Provider. |
| Kyverno | CRDs und Chart; Admission-/Background-/Cleanup-/Report-Rollen und Webhook-Zertifikate separat. Policy-Wirksamkeit nicht getestet. |
| Gatekeeper | `deploy/gatekeeper.yaml` und Chart/CRDs; ConstraintTemplates, Rego, Audit und Webhook-CA separat. Nicht ungeprueft parallel zu Kyverno als Default. |
| KEDA | CRDs, Default-/RBAC-/Manager-/Metrics-/Webhook-Dateien; Scaler-Zugang, APIService-TLS, Auth, Kapazitaet und Scale-to-zero separat. |
| Temporal | SQL-/Cassandra-Schemas und PostgreSQL-/Dynamicconfig-Beispiele; externe Datenbank, Schema-Migration, Visibility, TLS, Auth und gesicherte Produktionskonfiguration separat. Entwicklungskonfiguration ist keine Produktionsfreigabe. |
| Argo Workflows | Basis-/Cluster-Manifeste und CRDs; CRI, Workflow-RBAC, freigegebenes Executor-Image und Workflow-Pods separat. UI/API-Server nicht Bestandteil dieses Builds. |

Fuer Temporal liegt eine **inaktive** native Unit-Vorlage unter
`docs/tools/examples/temporal-native.service.example`. Sie wird weder kopiert noch aktiviert.
Alle anderen Kandidaten liefern Upstream-Kubernetes-Manifeste statt eines irrefuehrenden
Host-Dienstes. Ein Host-Binary allein ersetzt keinen Kubernetes-Deploymentplan.

## SSH und Pruefung

Nach zentraler Integration von einem geprueften Checkout, als normaler Benutzer unter Linux:

```bash
ssh -t vps
cd "$HOME/openclaw_ultimate_setup" || exit 1
python3 -I -B scripts/tool_commands.py show cert_manager
bash scripts/tools/cert_manager_install.sh --dry-run
# Nur nach expliziter Freigabe: Build samt benoetigter privater Toolchain.
bash scripts/tools/cert_manager_install.sh --install-build-deps
echo $?
```

Andere IDs: `external_dns`, `kyverno`, `gatekeeper`, `keda`, `temporal`, `argo_workflows`.
Wrapper werden zentral generiert, nicht von diesem Helper. Vor Integration sind diese Befehle
kein Nachweis eines bereits verfuegbaren Installationspfads. Kein Dienststart folgt auf den Build.

Offline-Tests (keine Downloads, Compiler- oder Controllerstarts):

```bash
python3 -I -B tests/test_candidate_go_controllers.py
```

Diese Tests pruefen Vertraege, Umgebungsfilter, Pfadgrenzen, Consent und Fehlerszenarien mit
Fixtures. Sie sind keine tatsaechliche Upstream-Build-, Cluster- oder Runtime-Abnahme.

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
python3 -I -B scripts/tool_commands.py show argo_workflows
python3 -I -B scripts/tool_commands.py show cert_manager
python3 -I -B scripts/tool_commands.py show external_dns
python3 -I -B scripts/tool_commands.py show gatekeeper
python3 -I -B scripts/tool_commands.py show keda
python3 -I -B scripts/tool_commands.py show kyverno
python3 -I -B scripts/tool_commands.py show temporal
```

### SSH-Aktionen: `argo_workflows`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run argo_workflows --action status
python3 -I -B scripts/tool_commands.py run argo_workflows --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run argo_workflows --action install --apply --confirm argo_workflows:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run argo_workflows --action update --apply --confirm argo_workflows:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run argo_workflows --action uninstall --apply --confirm argo_workflows:uninstall
```

Fehlende Build-Abhaengigkeiten stoppen den Versuch. Nur fuer Install/Update
`--install-build-deps` nach separater Download-Freigabe ergaenzen. Kein Auto-Yes,
kein Docker-Fallback; Source-Build/Status ist keine erfolgreiche Runtime-Abnahme.

### SSH-Aktionen: `cert_manager`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run cert_manager --action status
python3 -I -B scripts/tool_commands.py run cert_manager --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run cert_manager --action install --apply --confirm cert_manager:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run cert_manager --action update --apply --confirm cert_manager:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run cert_manager --action uninstall --apply --confirm cert_manager:uninstall
```

Fehlende Build-Abhaengigkeiten stoppen den Versuch. Nur fuer Install/Update
`--install-build-deps` nach separater Download-Freigabe ergaenzen. Kein Auto-Yes,
kein Docker-Fallback; Source-Build/Status ist keine erfolgreiche Runtime-Abnahme.

### SSH-Aktionen: `external_dns`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run external_dns --action status
python3 -I -B scripts/tool_commands.py run external_dns --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run external_dns --action install --apply --confirm external_dns:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run external_dns --action update --apply --confirm external_dns:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run external_dns --action uninstall --apply --confirm external_dns:uninstall
```

Fehlende Build-Abhaengigkeiten stoppen den Versuch. Nur fuer Install/Update
`--install-build-deps` nach separater Download-Freigabe ergaenzen. Kein Auto-Yes,
kein Docker-Fallback; Source-Build/Status ist keine erfolgreiche Runtime-Abnahme.

### SSH-Aktionen: `gatekeeper`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run gatekeeper --action status
python3 -I -B scripts/tool_commands.py run gatekeeper --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run gatekeeper --action install --apply --confirm gatekeeper:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run gatekeeper --action update --apply --confirm gatekeeper:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run gatekeeper --action uninstall --apply --confirm gatekeeper:uninstall
```

Fehlende Build-Abhaengigkeiten stoppen den Versuch. Nur fuer Install/Update
`--install-build-deps` nach separater Download-Freigabe ergaenzen. Kein Auto-Yes,
kein Docker-Fallback; Source-Build/Status ist keine erfolgreiche Runtime-Abnahme.

### SSH-Aktionen: `keda`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run keda --action status
python3 -I -B scripts/tool_commands.py run keda --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run keda --action install --apply --confirm keda:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run keda --action update --apply --confirm keda:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run keda --action uninstall --apply --confirm keda:uninstall
```

Fehlende Build-Abhaengigkeiten stoppen den Versuch. Nur fuer Install/Update
`--install-build-deps` nach separater Download-Freigabe ergaenzen. Kein Auto-Yes,
kein Docker-Fallback; Source-Build/Status ist keine erfolgreiche Runtime-Abnahme.

### SSH-Aktionen: `kyverno`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run kyverno --action status
python3 -I -B scripts/tool_commands.py run kyverno --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run kyverno --action install --apply --confirm kyverno:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run kyverno --action update --apply --confirm kyverno:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run kyverno --action uninstall --apply --confirm kyverno:uninstall
```

Fehlende Build-Abhaengigkeiten stoppen den Versuch. Nur fuer Install/Update
`--install-build-deps` nach separater Download-Freigabe ergaenzen. Kein Auto-Yes,
kein Docker-Fallback; Source-Build/Status ist keine erfolgreiche Runtime-Abnahme.

### SSH-Aktionen: `temporal`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run temporal --action status
python3 -I -B scripts/tool_commands.py run temporal --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run temporal --action install --apply --confirm temporal:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run temporal --action update --apply --confirm temporal:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run temporal --action uninstall --apply --confirm temporal:uninstall
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
