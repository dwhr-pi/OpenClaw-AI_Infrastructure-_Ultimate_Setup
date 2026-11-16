# gVisor, Kata Containers und Firecracker: ehrliche Runtime-Vorbereitung

Pruefstand: 16.11.2026. Die bisherigen Logs zeigen **gesperrte Planungseintraege**,
nicht gescheiterte Compilerlaeufe. Fuer diese drei Tools existiert weiterhin kein
freigegebener vollstaendiger nativer Installer. Die folgenden Pruefungen ersetzen ihn nicht.
Ein vorhandenes Ubuntu 26.04 oder eine kompilierte CLI ist keine Sandbox-/VM-Abnahme.

## Automatische Host-Metadaten

Die [Systemdiagnose](../SYSTEM_DIAGNOSTICS.md) erfasst jetzt auch:

- Linux-Kernel gegen die aktuelle gVisor-Mindestversion 5.6 und 64-Bit-Architektur.
- `/dev/kvm` als vorhandenes direktes Zeichengeraet und Lese-/Schreibrecht des aktuellen Benutzers.
- Sichtbare Marker fuer User-, Mount-, PID- und Netzwerk-Namespaces.
- Ausdruecklichen Hinweis: kein Runtime-, VM-, KVM- oder Sicherheitsfunktionstest.

Bei Auswahl von gVisor, Kata oder Firecracker zeigt das Hauptmenue diese Angaben
bereits im Planungshinweis. Bei normalen Installationslaeufen stehen sie im neuen
Operationslog. Es wird kein KVM-Geraet geoeffnet, kein ioctl ausgefuehrt und keine
Runtime gestartet. Kein sudo, modprobe, Gruppen-/ACL-Wechsel, Mount oder sysctl-Schreibzugriff.
Keine Kubernetes-/containerd-Konfiguration wird gelesen oder geaendert.

Optionaler eigener Diagnoseaufruf, kein Installationsbefehl:

```bash
python3 -I -B scripts/helpers/system_diagnostics.py --sandbox
```

KVM-Metadaten koennen fehlende Voraussetzungen sichtbar machen; vorhandene Rechte
beweisen weder funktionierende verschachtelte Virtualisierung noch eine sichere Sandbox.
Unter WSL ist die tatsaechliche Kernel-/Virtualisierungsumgebung entscheidend,
nicht allein `PRETTY_NAME` oder die Ubuntu-Version. Eine fehlende WSL-Kennung ist kein
Nachweis fuer Bare Metal. Auf 32-Bit-DietPi ist ein 64-Bit-Build nicht automatisch nutzbar.

## Unterschiedliche Aufgaben

| Tool | Belegter Weg / Voraussetzung | Noch offen |
| --- | --- | --- |
| gVisor | Linux amd64/arm64 und Kernel >=5.6. Nativer Bazel-Build ohne Docker ist upstream beschrieben. KVM wird nur bei Auswahl der KVM-Plattform benoetigt, nicht pauschal fuer jede gVisor-Plattform. | Exakter Toolchain-Bootstrap, vollstaendiges Releasebundle mit Sidecars, Lock-/SBOM-/Inventar-Nachweise, Runtime- und CRI-Abnahme. |
| Kata Containers | Runtime/Shim allein reichen nicht: ein passender Hypervisor, Gast-Kernel sowie initrd oder rootfs gehoeren zur Installation. | Gepinnter Gesamtbuild inklusive Gastartefakten, Hypervisor-/KVM-Vertrag, Containerd-/CRI-Abnahme, persistente Nutzerdaten und geschuetzter Uninstall. |
| Firecracker | Der hier betrachtete lokale Linux/KVM-Weg braucht passenden Gast-Kernel, rootfs und KVM-Lese-/Schreibzugriff; produktiver Betrieb erfordert einen Jailer-Vertrag. | Gepinnter Source-Build mit Jailer, Gastartefakte, sichere Ressourcen-/Netz-/Datengrenzen und echte MicroVM-Abnahme. Kein automatischer VM- oder API-Socket-Start. |

Primaerquellen:
[gVisor-Installation](https://gvisor.dev/docs/user_guide/install/),
[gVisor-Plattformen](https://gvisor.dev/docs/user_guide/platforms/),
[gVisor-Buildanleitung](https://github.com/google/gvisor/blob/release-20261109.0/README.md),
[Kata Developer Guide](https://github.com/kata-containers/kata-containers/blob/main/docs/Developer-Guide.md),
[Firecracker Getting Started](https://github.com/firecracker-microvm/firecracker/blob/main/docs/getting-started.md).
Die gesonderte AWS-Nitro-Sandbox ist kein hier implementierter lokaler Firecracker-Weg.

## Konkreter gVisor-Baustein fuer das naechste Buildrezept

Originalrelease: `release-20261109.0`, annotierter Tag auf Commit
`a0e6be6fb5e03d8ebea13592f36a097c7e9a41b9`.
Die gelesene Datei `images/default/bazelversion` verlangt **Bazel 9.3.1**,
nicht das bereits fuer andere SDKs vorhandene Bazel 9.2.0.
Upstream-Ziel fuer den nativen Build: `//debian:gvisor-release-tar-bz2`.
Das Bundle muss `runsc`, `containerd-shim-runsc-v1` und `gvisor-bin/`-Sidecars zusammen enthalten.
Nur `go build` oder eine einzelne runsc-Binary ist kein gleichwertiges Rezept.

| Gelesene Quelldatei am Commit | SHA256 |
| --- | --- |
| LICENSE | `0fbab5c58efbdf6d31e8085214f2dd821659c03d73cff3ed2b08e98826ea1cd9` |
| README.md | `0164b6a864027e506c90185bb3c8b5bc0d70e51dc6e872b2b1d8719364dfcba3` |
| images/default/bazelversion | `10ba73729037af18a205cb7f273f8676ef03aec9610e248d138c8f385457cda8` |
| MODULE.bazel | `4b8f3ca647e66eb0bcf39f7289dedb13fe572ab4cd3dd7d02d42454c19f20be4` |
| debian/BUILD | `87e52587227ab5d801ee55a56e8d5c61afd57bd96f3514cb2f3cd62982da6669` |
| tools/release.bzl | `5b8f5d651f2473ba94aa173827be2fc7a54062917ecf99374f2d692a82bb9eda` |

Die oeffentliche Bazel-Release-API nennt fuer 9.3.1 folgende Buildwerkzeug-Artefakte;
kein Download oder Ausfuehren dieser Artefakte in dieser Pruefung:

| GitHub-Asset | Bytes | SHA256 laut Release-Metadaten |
| --- | --- | --- |
| bazel-9.3.1-linux-x86_64 | 77022209 | `7f775b54bbec487efaf0f49ccda1d2ed02cd34f582edfdd6aeeec76e39ef585c` |
| bazel-9.3.1-linux-arm64 | 74883684 | `10ba9cb76d4ee748d274dcc2981992bb12b74a203dc41a9c2eceeb8f29359366` |

Original: [Bazel 9.3.1](https://github.com/bazelbuild/bazel/releases/tag/9.3.1).
`MODULE.bazel.lock` konnte am gVisor-Pin nicht bestaetigt werden. Vor Freigabe muss
der Aufloesungs-/Lock-Erzeugungspfad fuer heruntergeladene Go-/LLVM-/Python-/Bazel-Abhaengigkeiten
festgelegt und dokumentiert werden. Diese Tabelle ist noch kein genehmigter Downloadvertrag im Installer.
Paketlisten, Ressourcenbudgets und Artefaktpfade sind vor einem echten Build zu pruefen;
die bisherige pauschale 4-GiB-Menuevorlage ist keine gemessene Groessenfreigabe.

## Sichere Aktivierungsgrenze

Kein automatischer Docker-/Compose-Fallback, RuntimeClass-Apply, CRI-Rewrite,
containerd-Neustart oder GPU-Zugriff. Gastimages werden weder geladen noch eingebunden.
Erst ein geprueftes Buildbundle samt Besitz-/Hashnachweisen, eine begrenzte Versionsprobe
und ein separat freigegebener Runtime-Test erlauben eine entsprechende Erfolgsaussage.
[Zurueck zu den Infrastruktur-Kandidaten](infrastructure-candidates.md).

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
