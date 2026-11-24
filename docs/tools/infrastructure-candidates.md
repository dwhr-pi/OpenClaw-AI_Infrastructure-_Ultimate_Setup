# Native Infrastruktur- und Agenten-Installer hinter XERJ

Stand: 20.11.2026. Die genannten Tools stehen weiterhin im letzten Tools-Menueabschnitt.
Valkey und Kube_Bench behalten ihre bestehenden nativen Installer; die weiteren Eintraege
verwenden jetzt tool-spezifische native Buildrezepte statt gesperrter Dokumentations-Platzhalter.

**Experimentell, echte Linux-Buildabnahme offen:** Offline-Fixtures pruefen Vertrage und Fehlerpfade,
nicht einen abgeschlossenen Ubuntu-/WSL-Build. Installation bedeutet ausschliesslich den unten
und auf der Toolseite beschriebenen Programm-/Komponentenumfang, niemals einen betriebsbereiten Cluster.

## Auswahl und Voraussetzungen

Im Setup das gewuenschte Tool auswaehlen und fehlende Buildvoraussetzungen bewusst freigeben.
Quellen werden am vollen Pin gebaut; ein Clone allein erzeugt keinen Erfolgsnachweis.
Neue Debian-/Ubuntu-Releases und DietPi werden nicht wegen einer Point-Release-Bezeichnung abgelehnt.
Architektur, Pakete, Compiler, Kernel und Ressourcen muessen trotzdem zum Rezept passen.
Bei WSL gilt auch der echte freie Windows-Backing-Speicher, nicht nur die virtuelle Linux-Kapazitaet.

Kein Docker-/Compose-Fallback und kein automatischer Dienst-, Modell-, VM- oder Clusterstart.
Keine CRD-/DNS-/Zertifikatsaenderung, kein Security-Scan oder Provideraufruf durch die Installation.

## Installer und Grenzen

| Tool | Anleitung | Gebauter Umfang und offene Betriebsabnahme |
| --- | --- | --- |
| Kube_Bench | [kube-bench.md](kube-bench.md) | Gepinnter nativer Go-Build mit cfg-Benchmarks; Go-Basis nur nach Zustimmung. Nur version-Probe mit eigener gepruefter Konfiguration. Kein Host-/Cluster-Audit, kubectl, Kubeconfig-, AWS-, Datenbank- oder Root-Zugriff. Linux-/Benchmark-Abnahme offen. |
| Valkey | [valkey.md](valkey.md) | Valkey 9.1.3 mit TLS und libc-Allocator, privater GitHub-Source-Build. Nur Versionsproben, kein Serverstart/Port/Redis-Ersatz. Gemeinsame Buildpakete nach Zustimmung; ACL/TLS-Konfiguration, Persistenz und Gateway-Abnahme separat. |
| cert-manager | [native-go-controllers.md](native-go-controllers.md) | Native Komponenten und statische Upstream-Dateien; keine Cluster-/Dienstabnahme. CRDs/Chart-/Konfigurationsdateien werden nur kopiert, nicht angewendet. |
| External_DNS | [native-go-controllers.md](native-go-controllers.md) | Native Komponenten und statische Upstream-Dateien; keine Cluster-/Dienstabnahme. CRDs/Chart-/Konfigurationsdateien werden nur kopiert, nicht angewendet. |
| Kyverno | [native-go-controllers.md](native-go-controllers.md) | Native Komponenten und statische Upstream-Dateien; keine Cluster-/Dienstabnahme. CRDs/Chart-/Konfigurationsdateien werden nur kopiert, nicht angewendet. |
| Gatekeeper | [native-go-controllers.md](native-go-controllers.md) | Native Komponenten und statische Upstream-Dateien; keine Cluster-/Dienstabnahme. CRDs/Chart-/Konfigurationsdateien werden nur kopiert, nicht angewendet. |
| KEDA | [native-go-controllers.md](native-go-controllers.md) | Native Komponenten und statische Upstream-Dateien; keine Cluster-/Dienstabnahme. CRDs/Chart-/Konfigurationsdateien werden nur kopiert, nicht angewendet. |
| Temporal | [native-go-controllers.md](native-go-controllers.md) | Native Komponenten und statische Upstream-Dateien; keine Cluster-/Dienstabnahme. Server und SQL-/Cassandra-Werkzeuge; Datenbank, Schema-Migration, TLS/Auth und Deployment separat. |
| Argo_Workflows | [native-go-controllers.md](native-go-controllers.md) | Native Komponenten und statische Upstream-Dateien; keine Cluster-/Dienstabnahme. Nur Controller und Executor, kein UI-/API-Server; Workflow-Pods brauchen separate freigegebene CRI-Images. |
| OpenJarvis | [openjarvis.md](openjarvis.md) | Gepinnter nativer Python-CLI-/SDK-Basisbuild mit Lifecycle; ohne Quickstart-Autostart oder automatische Modelldownloads. GUI, Desktop-Paket und Rust-Erweiterung sind getrennte Ausbaustufen. Linux-/WSL-Buildabnahme offen; keine Inferenz oder Agentenausfuehrung. |
| Arize_Phoenix | [python-reviewed-native.md](python-reviewed-native.md) | Source-Wheel einschliesslich kompiliertem Frontend, private CPython-3.12-venv. Importprobe ohne launch_app/Dienststart. Elastic-2.0 vorher pruefen. Keine Laufzeit-/Datenbankabnahme; Linux-End-to-End-Build noch ausstehend. |
| Checkov | [python-reviewed-native.md](python-reviewed-native.md) | Echtes Source-Wheel mit generierten JSON-Graph-Policies und Checkov-CLI in eigener venv; keine Scans/Providerkontakte. Python-docker ist deklarierte Bibliotheksabhaengigkeit, keine Engine/Containerinstallation. Linux-End-to-End-Build noch ausstehend. |
| Ragas | [python-reviewed-native.md](python-reviewed-native.md) | Source-Wheel mit expliziter gepinnter SCM-Version, CLI und evaluate/aevaluate-Importprobe. Keine Evaluation, Inferenz, Modell-Downloads oder Providerkontakte; keine all/dev-Extras. Linux-End-to-End-Build noch ausstehend. |
| gVisor | [sandbox-native-candidates.md](sandbox-native-candidates.md) | Vollstaendiges gVisor-Releasebundle nativ mit Bazel 9.3.1; nur Versionsprobe, keine Sandbox-/CRI-Abnahme. |
| Firecracker | [sandbox-native-candidates.md](sandbox-native-candidates.md) | Native Firecracker-/Jailer-Hostkomponenten mit Rust 1.97.0 und musl; kein Gast-Kernel/rootfs und keine VM-Abnahme. |
| Kata_Containers | [sandbox-native-candidates.md](sandbox-native-candidates.md) | Nur native Legacy-Go-Hostkomponenten kata-runtime und Shim; KEINE vollstaendige Kata-Installation ohne Agent, Gast-Kernel/rootfs und Hypervisor. |
| Milvus | [security-data-native.md](security-data-native.md) | Milvus CPU Server/Core mit eingebetteten versionierten Web-UI-Assets; ohne etcd/MinIO/Pulsar, GPU, DiskANN oder Betriebsabnahme |
| Vaultwarden | [security-data-native.md](security-data-native.md) | Vaultwarden SQLite-Backend, gebuendelte SQLite; ausdruecklich ohne Web-Vault, WEB_VAULT_ENABLED=false; keine vollstaendige Browser-Installation |
| OWASP_ZAP | [security-data-native.md](security-data-native.md) | ZAP Core-JAR mit Runtime-JARs, xml/lang/db-Konfiguration und Startskripten; ohne Add-ons/Browser/Installer/JRE; kein vollstaendiges Scanprofil |
| Kubescape | [native-security-candidates.md](native-security-candidates.md) | Nur lokale CLI-Artefakte; keine Dienste, Scans, Templates, Browser, Cluster-/Providerzugriffe oder Updates. Netzwerklose Versionsprobe braucht unshare/User-Netzwerk-Namespace. Reale Linux/WSL-Buildabnahme noch offen. |
| Nuclei | [native-security-candidates.md](native-security-candidates.md) | Nur lokale CLI-Artefakte; keine Dienste, Scans, Templates, Browser, Cluster-/Providerzugriffe oder Updates. Netzwerklose Versionsprobe braucht unshare/User-Netzwerk-Namespace. Reale Linux/WSL-Buildabnahme noch offen. |
| TruffleHog | [native-security-candidates.md](native-security-candidates.md) | Nur lokale CLI-Artefakte; keine Dienste, Scans, Templates, Browser, Cluster-/Providerzugriffe oder Updates. Netzwerklose Versionsprobe braucht unshare/User-Netzwerk-Namespace. Reale Linux/WSL-Buildabnahme noch offen. |
| Testssl | [native-security-candidates.md](native-security-candidates.md) | Nur lokale CLI-Artefakte; keine Dienste, Scans, Templates, Browser, Cluster-/Providerzugriffe oder Updates. Netzwerklose Versionsprobe braucht unshare/User-Netzwerk-Namespace. Reale Linux/WSL-Buildabnahme noch offen. |

## Lifecycle und Nachweise

Jedes Tool besitzt Install, Update, Status, Check, Doctor und geschuetzten Uninstall.
Update bleibt am freigegebenen Quellenpin; keine stillen Downloads von main/latest.
Artefakte, Lockfiles und SBOM werden im privaten Buildverzeichnis erfasst.
Status prueft Buildnachweise, nicht Dienstgesundheit. Doctor ist ohne gesonderte
Laufzeitabnahme unvollstaendig; keine automatischen Netztests oder Credential-Zugriffe.
Geaenderte oder fremde Dateien werden nicht automatisch ueberschrieben oder geloescht.

Die verlinkten Toolseiten benennen insbesondere die noch erforderlichen Voraussetzungen
und Komponenten: Kata-Gaeste/Hypervisor, Milvus-Betriebsdienste, Vaultwarden-Web-Vault,
ZAP-Add-ons und Argo-API/UI sind nicht durch einen einzelnen Host-Binary-Build erledigt.

Weiter: [Installationsrichtlinie](../INSTALLATION_POLICY.md),
[Systemdiagnose](../SYSTEM_DIAGNOSTICS.md), [Tool-Lifecycle](../TOOL_LIFECYCLE_STANDARD.md).

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
python3 -I -B scripts/tool_commands.py list
```

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
