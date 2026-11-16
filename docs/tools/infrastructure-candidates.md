# Infrastruktur-Kandidaten hinter XERJ

Stand: 16.11.2026. Diese Tools stehen als letzter Block **direkt hinter XERJ** im Tools-Menue.
Bestehende Eintraege werden nicht dupliziert. Der eingefrorene A-Z-Bereich bleibt erhalten;
TruffleHog wird auf ausdruecklichen Wunsch in den neuen Schlussblock verschoben.

## Status und Grenzen

**GEPLANT / NICHT INSTALLIERBAR** ist kein fertiger Installer. Die neuen Eintraege laden nichts herunter,
bauen nichts und starten weder Dienste noch Cluster, Modelle oder Sicherheitspruefungen.
Install/Update/Doctor/Uninstall enden fuer die neuen Kandidaten mit Exit 3 statt einem falschen Erfolg.
Ein expliziter `--dry-run` zeigt nur den Plan (Exit 0). Status liefert `installed: null`:
Der Host wird nicht untersucht, auch eine separat eingerichtete Installation bleibt unberuehrt.

Die GitHub-Links sind Quellenkandidaten, **keine Freigabe eines Pins oder einer Lizenz**.
Erst nach geprueftem vollen Commit, Lockfiles und Artefakthashes darf ein nativer Build folgen.
Ein Klon, eine Policy oder ein CRD-Beispiel ersetzt keine Controller-/Runtime-Abnahme.
Keine Docker-/Compose-Installation, kein Fallback und keine automatische Aktivierung.

## Werkzeuge

| Menue | Quellenkandidat | Zweck | Noch offen |
| --- | --- | --- | --- |
| cert-manager | [GitHub](https://github.com/cert-manager/cert-manager) | TLS-Zertifikatsverwaltung | Issuer vorhanden; nativer Controller-Build und CRD-Abnahme offen. |
| External_DNS | [GitHub](https://github.com/kubernetes-sigs/external-dns) | DNS-Automatisierung | Zonenrechte, TXT-Owner und nativer Build offen. |
| Kyverno | [GitHub](https://github.com/kyverno/kyverno) | Kubernetes-Admission | Policies vorhanden; Controller und Admission-Abnahme offen. |
| Gatekeeper | [GitHub](https://github.com/open-policy-agent/gatekeeper) | Alternative zu Kyverno | Nicht parallel als Default; Controller-Build und Rego-Abnahme offen. |
| KEDA | [GitHub](https://github.com/kedacore/keda) | Queue-basierte Skalierung | CRDs, Auth, nativer Build und Kapazitaetstest offen. |
| Arize_Phoenix | [GitHub](https://github.com/arize-ai/phoenix) | Alternative zu Langfuse | Native Installation, Persistenz, Auth und Trace-Redaction offen. |
| Valkey | [GitHub](https://github.com/valkey-io/valkey) | Cache und Betriebsabhaengigkeit | Nativer Build, ACL/TLS und Gateway-Kompatibilitaet offen. |
| gVisor | [GitHub](https://github.com/google/gvisor) | Sandbox-Runtime | runsc-/CRI-Integration, Kernel- und GPU-Vertrag offen. |
| Kata_Containers | [GitHub](https://github.com/kata-containers/kata-containers) | VM-basierte Sandbox | Virtualisierung, CRI und native Runtime-Abnahme offen. |
| Firecracker | [GitHub](https://github.com/firecracker-microvm/firecracker) | MicroVM-Baustein | KVM, Jailer und Kubernetes-Runtime-Anbindung offen. |
| Milvus | [GitHub](https://github.com/milvus-io/milvus) | Alternative Vektordatenbank | Nativer Gesamtbuild, Abhaengigkeiten und Restore offen. |
| Kube_Bench | [GitHub](https://github.com/aquasecurity/kube-bench) | CIS-Audit | Audit-Wrapper vorhanden; gepinnter Build und Benchmark-Abnahme offen. |
| Kubescape | [GitHub](https://github.com/kubescape/kubescape) | Cluster-Sicherheitspruefung | Nativer Build, minimale Leserechte und Ruleset-Abnahme offen. |
| Nuclei | [GitHub](https://github.com/projectdiscovery/nuclei) | Autorisierte Sicherheitstests | Nativer Build und separat gepruefte Templates offen; keine automatischen Scans. |
| Testssl | [GitHub](https://github.com/testssl/testssl.sh) | TLS-Audit | Quellenpin, OpenSSL-Vertrag und Smoke-Test offen; keine automatischen Netztests. |
| OWASP_ZAP | [GitHub](https://github.com/zaproxy/zaproxy) | Autorisierte Web-Sicherheitstests | Nativer Build, JDK und Add-on-Vertrag offen; keine automatischen Scans. |
| Checkov | [GitHub](https://github.com/bridgecrewio/checkov) | IaC-Pruefung | Nativer Python-Build, Rulesets und Offline-Verhalten offen. |
| Ragas | [GitHub](https://github.com/vibrantlabsai/ragas) | RAG-Evaluation | Quellenpin und nativer Build offen; keine LLM-Judge-/Provider-Aufrufe. |
| Temporal | [GitHub](https://github.com/temporalio/temporal) | Persistente Workflows | Vorhandener Registry-Platzhalter; Build, Persistenz und Lifecycle offen. |
| TruffleHog | [GitHub](https://github.com/trufflesecurity/trufflehog) | Secret-Pruefung | Vorhandener Registry-Platzhalter; nativer Build und sichere Scanvorgaben offen. |
| Vaultwarden | [GitHub](https://github.com/dani-garcia/vaultwarden) | Passwortverwaltung | Vorhandener Registry-Platzhalter; Build, TLS, Backup und Restore offen. |
| Argo_Workflows | [GitHub](https://github.com/argoproj/argo-workflows) | Kubernetes-Workflows | Vorhandener Registry-Platzhalter; Controller, CRDs und RBAC offen. |

Die vier bisherigen Platzhalter bleiben bestehende Katalogeintraege, keine neuen Installer.
Ihre Installationspfade verweigern nun ebenfalls mit Exit 3 einen falschen Erfolg.
Bestehende individuelle Registry-Anleitungen bleiben erhalten; fuer alle 22 Eintraege gelten diese Grenzen.

## Schrittweise Umsetzung

1. Quellenpin, Lizenz am Pin, Plattform, Ressourcenbedarf und nativen Buildvertrag pruefen.
2. Lockfiles und SBOM-Erzeugung, private Installationspfade und Artifact-Hashes festlegen.
3. Status, Doctor, begrenzten Smoke-Test und idempotente Deinstallation implementieren.
4. Offline-Fehlerpfade testen, danach bewusst freigegebenen Ubuntu-/WSL-Build abnehmen.
5. Erst danach den Status anheben; Dienst-/Clusterstarts bleiben getrennte Opt-in-Aktionen.

Kyverno und Gatekeeper sowie Langfuse und Phoenix sind Alternativen, keine gemeinsamen Defaults.
KEDA ersetzt keine GPU-Kapazitaet; Firecracker allein ist keine fertige Kubernetes-Sandbox.
Kube-bench hat bereits einen [Audit-Wrapper](../../scripts/security/kube-bench-audit.sh), aber keinen Buildinstaller.

Weiter: [Enterprise-Roadmap](../architecture/ENTERPRISE_HARDENING_ROADMAP.md),
[Installationsrichtlinie](../INSTALLATION_POLICY.md), [Tool-Lifecycle](../TOOL_LIFECYCLE_STANDARD.md).

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
python3 -I -B scripts/tool_commands.py show cert_manager
python3 -I -B scripts/tool_commands.py show checkov
python3 -I -B scripts/tool_commands.py show external_dns
python3 -I -B scripts/tool_commands.py show firecracker
python3 -I -B scripts/tool_commands.py show gatekeeper
python3 -I -B scripts/tool_commands.py show gvisor
python3 -I -B scripts/tool_commands.py show kata_containers
python3 -I -B scripts/tool_commands.py show keda
python3 -I -B scripts/tool_commands.py show kube_bench
python3 -I -B scripts/tool_commands.py show kubescape
python3 -I -B scripts/tool_commands.py show kyverno
python3 -I -B scripts/tool_commands.py show milvus
python3 -I -B scripts/tool_commands.py show nuclei
python3 -I -B scripts/tool_commands.py show owasp_zap
python3 -I -B scripts/tool_commands.py show phoenix
python3 -I -B scripts/tool_commands.py show ragas
python3 -I -B scripts/tool_commands.py show testssl
python3 -I -B scripts/tool_commands.py show valkey
```

### SSH-Aktionen: `cert_manager`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`cert-manager` (ID `cert_manager`) waehlen und die Einzelfreigaben lesen.
Fehlt der Eintrag oder ist der native Weg gesperrt, hier stoppen: keine
Legacy-/Docker-Ausweichinstallation und kein automatischer Plattformwechsel.

### SSH-Aktionen: `checkov`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`Checkov` (ID `checkov`) waehlen und die Einzelfreigaben lesen.
Fehlt der Eintrag oder ist der native Weg gesperrt, hier stoppen: keine
Legacy-/Docker-Ausweichinstallation und kein automatischer Plattformwechsel.

### SSH-Aktionen: `external_dns`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`External_DNS` (ID `external_dns`) waehlen und die Einzelfreigaben lesen.
Fehlt der Eintrag oder ist der native Weg gesperrt, hier stoppen: keine
Legacy-/Docker-Ausweichinstallation und kein automatischer Plattformwechsel.

### SSH-Aktionen: `firecracker`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`Firecracker` (ID `firecracker`) waehlen und die Einzelfreigaben lesen.
Fehlt der Eintrag oder ist der native Weg gesperrt, hier stoppen: keine
Legacy-/Docker-Ausweichinstallation und kein automatischer Plattformwechsel.

### SSH-Aktionen: `gatekeeper`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`Gatekeeper` (ID `gatekeeper`) waehlen und die Einzelfreigaben lesen.
Fehlt der Eintrag oder ist der native Weg gesperrt, hier stoppen: keine
Legacy-/Docker-Ausweichinstallation und kein automatischer Plattformwechsel.

### SSH-Aktionen: `gvisor`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`gVisor` (ID `gvisor`) waehlen und die Einzelfreigaben lesen.
Fehlt der Eintrag oder ist der native Weg gesperrt, hier stoppen: keine
Legacy-/Docker-Ausweichinstallation und kein automatischer Plattformwechsel.

### SSH-Aktionen: `kata_containers`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`Kata_Containers` (ID `kata_containers`) waehlen und die Einzelfreigaben lesen.
Fehlt der Eintrag oder ist der native Weg gesperrt, hier stoppen: keine
Legacy-/Docker-Ausweichinstallation und kein automatischer Plattformwechsel.

### SSH-Aktionen: `keda`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`KEDA` (ID `keda`) waehlen und die Einzelfreigaben lesen.
Fehlt der Eintrag oder ist der native Weg gesperrt, hier stoppen: keine
Legacy-/Docker-Ausweichinstallation und kein automatischer Plattformwechsel.

### SSH-Aktionen: `kube_bench`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`Kube_Bench` (ID `kube_bench`) waehlen und die Einzelfreigaben lesen.
Fehlt der Eintrag oder ist der native Weg gesperrt, hier stoppen: keine
Legacy-/Docker-Ausweichinstallation und kein automatischer Plattformwechsel.

### SSH-Aktionen: `kubescape`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`Kubescape` (ID `kubescape`) waehlen und die Einzelfreigaben lesen.
Fehlt der Eintrag oder ist der native Weg gesperrt, hier stoppen: keine
Legacy-/Docker-Ausweichinstallation und kein automatischer Plattformwechsel.

### SSH-Aktionen: `kyverno`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`Kyverno` (ID `kyverno`) waehlen und die Einzelfreigaben lesen.
Fehlt der Eintrag oder ist der native Weg gesperrt, hier stoppen: keine
Legacy-/Docker-Ausweichinstallation und kein automatischer Plattformwechsel.

### SSH-Aktionen: `milvus`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`Milvus` (ID `milvus`) waehlen und die Einzelfreigaben lesen.
Fehlt der Eintrag oder ist der native Weg gesperrt, hier stoppen: keine
Legacy-/Docker-Ausweichinstallation und kein automatischer Plattformwechsel.

### SSH-Aktionen: `nuclei`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`Nuclei` (ID `nuclei`) waehlen und die Einzelfreigaben lesen.
Fehlt der Eintrag oder ist der native Weg gesperrt, hier stoppen: keine
Legacy-/Docker-Ausweichinstallation und kein automatischer Plattformwechsel.

### SSH-Aktionen: `owasp_zap`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`OWASP_ZAP` (ID `owasp_zap`) waehlen und die Einzelfreigaben lesen.
Fehlt der Eintrag oder ist der native Weg gesperrt, hier stoppen: keine
Legacy-/Docker-Ausweichinstallation und kein automatischer Plattformwechsel.

### SSH-Aktionen: `phoenix`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`Arize_Phoenix` (ID `phoenix`) waehlen und die Einzelfreigaben lesen.
Fehlt der Eintrag oder ist der native Weg gesperrt, hier stoppen: keine
Legacy-/Docker-Ausweichinstallation und kein automatischer Plattformwechsel.

### SSH-Aktionen: `ragas`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`Ragas` (ID `ragas`) waehlen und die Einzelfreigaben lesen.
Fehlt der Eintrag oder ist der native Weg gesperrt, hier stoppen: keine
Legacy-/Docker-Ausweichinstallation und kein automatischer Plattformwechsel.

### SSH-Aktionen: `testssl`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`Testssl` (ID `testssl`) waehlen und die Einzelfreigaben lesen.
Fehlt der Eintrag oder ist der native Weg gesperrt, hier stoppen: keine
Legacy-/Docker-Ausweichinstallation und kein automatischer Plattformwechsel.

### SSH-Aktionen: `valkey`

Kein freigegebener unbeaufsichtigter Docker-freier Adapter. Der Plan nennt
vorhandene Skriptpfade; diese nicht ungeprueft ausfuehren. Die
tool-spezifischen Plattform-, Lizenz- und Laufzeitgrenzen oben gelten weiterhin.

Fuer die interaktive Installation nach Pruefung `bash setup_ultimate.sh` im
VPS-Terminal oeffnen, dort im Tool-Management das gewuenschte Tool
`Valkey` (ID `valkey`) waehlen und die Einzelfreigaben lesen.
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
