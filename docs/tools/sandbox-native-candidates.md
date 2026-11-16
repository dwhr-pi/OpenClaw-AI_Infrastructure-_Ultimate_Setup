# Native Sandbox-Buildkandidaten

Stand: 16.11.2026. Neuer Integrationsvorschlag in
`config/native-candidates/sandbox.json`; keine eigenstaendige Registry-Aktivierung.
Diese Seite ersetzt keine Runtime-/Sicherheitsabnahme. Ein Clone ist nie installiert.
Die Windows-Entwicklungsumgebung fuehrt keine Linux-Compiler- oder VM-Abnahme aus.

## Umfang und Quellen

| Werkzeug | Unveraenderlicher Source-Pin | Gebaute Artefakte | Abnahmegrenze |
| --- | --- | --- | --- |
| gVisor release-20261109.0 | `a0e6be6fb5e03d8ebea13592f36a097c7e9a41b9` | `runsc`, `containerd-shim-runsc-v1`, alle sieben `gvisor-bin/`-Sidecars | Vollstaendiges Releasebundle, nur Versionsprobe; kein Sandbox-/CRI-Test. |
| Firecracker 1.18.0 | `eaf83bb718a559d324613d566eaf776b31a62340` | `firecracker`, `jailer`, native musl-Release-Binaries | Nur Hostkomponenten; Gast-Kernel, rootfs, Jailer-Betriebsvertrag und MicroVM-Abnahme fehlen. |
| Kata Containers 4.3.1 | `03cf2ec06a5d302f23af811744f6bcea49988bfb` | Legacy-Go-`kata-runtime`, `containerd-shim-kata-v2` | Komponenten, **keine vollstaendige Kata-Installation**. |

Die konkreten Primaerquellen sind das
[gVisor-Bundlerezept](https://github.com/google/gvisor/blob/a0e6be6fb5e03d8ebea13592f36a097c7e9a41b9/debian/BUILD),
die [Sidecar-Liste](https://github.com/google/gvisor/blob/a0e6be6fb5e03d8ebea13592f36a097c7e9a41b9/tools/release.bzl),
das [Firecracker-Workspace](https://github.com/firecracker-microvm/firecracker/blob/eaf83bb718a559d324613d566eaf776b31a62340/Cargo.toml),
der [Seccomp-Build](https://github.com/firecracker-microvm/firecracker/blob/eaf83bb718a559d324613d566eaf776b31a62340/src/firecracker/build.rs)
und das [Kata-Makefile](https://github.com/kata-containers/kata-containers/blob/03cf2ec06a5d302f23af811744f6bcea49988bfb/src/runtime/Makefile).
Source-SHA256s fuer Lizenz, Builddateien und vorhandene Locks stehen im Fragment.
Die Auswahl benutzt keine beweglichen `latest`-Referenzen beim Installieren.

Kata: Der Go-Hostbuild liefert weder den aktuellen Rust-Standardruntime noch
`kata-agent`, Gast-Kernel, initrd/rootfs, QEMU/anderen Hypervisor oder passende
Konfiguration. Dafuer waeren eigene gepinnte Quellen, Toolchains, native
Kernel-/Rootfs-Rezepte, ein passendes Agent-ABI und ein separat freigegebener
Gastartefaktvertrag erforderlich. Der hier implementierte Go-Makefile-Build
erzeugt diese Artefakte nicht. Es wird weder ein Docker-basierter Builder noch
eine unbewiesene Gastimage-Abkuerzung verwendet. Siehe
[Gastartefakte](https://github.com/kata-containers/kata-containers/blob/03cf2ec06a5d302f23af811744f6bcea49988bfb/docs/design/architecture/guest-assets.md).

## Voraussetzungen und Freigabe

Nur Linux x86_64/aarch64, unprivilegierter Benutzer, kein Crossbuild. Startbudgets:
gVisor mindestens 64 GiB freie Disk und 8 GiB verfuegbarer RAM; andere Kandidaten
16 GiB/4 GiB. Das sind konservative Eingangsschranken, keine gemessenen
Obergrenzen oder Zusage eines erfolgreichen Builds. Zwei Buildjobs, maximal
7200 Sekunden je Buildkommando. Der Hauptprozess muss seine Operationssperre halten.

Die zentrale Engine installiert nach Zustimmung ausschliesslich die im Fragment
genannten apt-**Buildabhaengigkeiten**. Keine Runtime wird ueber apt installiert.
Der Hook selbst fuehrt weder apt noch sudo aus. Fehlende private Toolchains
werden nur mit `approved=True` (`--install-build-deps`) heruntergeladen:

- gVisor: offizielle Bazel-9.3.1-Linux-Binary, SHA256 fuer beide Architekturen
  im Fragment und Helper. Kein Bazelisk, kein einzelnes `go build`.
- Firecracker: Rust 1.97.0, Cargo, GNU-Host-Stdlib und native musl-Stdlib aus den
  datierten offiziellen Archiven vom 09.07.2026. Jede Komponente hat einen
  festen SHA256 im Fragment und Helper. Die geprueften nativen `install.sh`
  laufen nur mit privatem Prefix und `--disable-ldconfig`; kein rustup-Defaultwechsel.
- Kata: Go >=1.26.9 entsprechend `go.mod`, kein Exact-Zwang. Falls erforderlich
  wird der bestehende private SHA256-gepinnte Go-1.27.3-Bootstrap verwendet.
  `GOTOOLCHAIN=local`, keine automatische Go-Toolchain-Aufloesung.

Toolchain-Basen liegen ausserhalb des App-Prefix unter `outer/toolchain/`.
Vor Wiederverwendung wird ihr Datei-Inventar geprueft. Unbekannte oder veraenderte
Basen werden nicht ueberschrieben. `NATIVE_SOURCE_RUST_TOOLCHAIN` ist nur ein
optionaler expliziter Override, keine Pflicht zur manuellen Bereitstellung.
Eine gewaehlte falsche Toolchain wird nicht still ersetzt.
Originale: [Bazel 9.3.1](https://github.com/bazelbuild/bazel/releases/tag/9.3.1),
[Rust-Distributionsmanifest](https://static.rust-lang.org/dist/channel-rust-1.97.0.toml),
[Firecracker-Toolchain](https://github.com/firecracker-microvm/firecracker/blob/eaf83bb718a559d324613d566eaf776b31a62340/rust-toolchain.toml),
[Kata-Go-Minimum](https://github.com/kata-containers/kata-containers/blob/03cf2ec06a5d302f23af811744f6bcea49988bfb/src/runtime/go.mod).

## Hook-Vertrag

Import: `scripts/tools/helpers/native_sandbox_candidates.py`, Art `candidate-native`.

```python
preflight(outer, spec, approved=False)
build(source, prefix, spec, env, run=None)  # list[str], prefix-relative paths
probe(prefix, spec, env, run=None)         # dict of bounded --version output
```

`spec` ist der komplette Fragment-Tool-Eintrag, nicht nur `recipe`.
`outer` ist der verwaltete Toolordner, `prefix=outer/native-github`,
`source=prefix/source`. Build braucht einen frischen privaten Staging-Prefix.
Die Engine prueft Besitz, Operationssperre und freien Speicher erneut, aktiviert
die apt-Buildabhaengigkeiten vor dem Hook und publiziert erst nach Inventarpruefung.
Der Hook aktiviert private Toolchains selbst, da der Custom-Dispatch zentrale
Standard-Go-/Rust-Aktivierungen umgehen kann.

Der optionale Runner hat exakt `run(argv: list[str], cwd: Path, env: dict) -> str`.
Er muss Fehler werfen und Prozessgruppen-/Zeit-/Ausgabebudgets selbst erzwingen.
Ohne Injection nutzt der Hook 20s/64 KiB fuer Probes und 7200s fuer Builds;
Buildausgabe wird geerbt statt unbegrenzt im RAM gesammelt. Nur Tests sollten
Runner injizieren. Eine Simulation ist kein realer Buildnachweis.
Doctor/Check darf nur `probe` fuer bereits inventarisierte Artefakte verwenden,
niemals `preflight` oder `build` und damit niemals Download/Compiler starten.

## Nachweise und Grenzen

gVisor baut exakt `//debian:gvisor-release-tar-bz2`, optimiert mit nativer
Architekturkonfiguration. Nur das komplette Bundle mit sieben Sidecars wird
akzeptiert. Es wird ohne `extractall` entpackt; Links, Traversal, Duplikate,
Spezialdateien und uebergrosse Archive werden abgewiesen. Die ELF-Klasse und
Architektur muessen zum Host passen. Die Sidecars bleiben neben `runsc` in
`bin/gvisor-bin/`, der Shim in `bin/`.

Firecracker baut explizit beide Cargo-Pakete mit `--locked --release --target
ARCH-unknown-linux-musl`. Ein GNU-/Debugbuild kann fehlende Seccomp-Policies durch
leere Policies ersetzen und ist kein gleichwertiger Weg. Die beiden nativen
musl-Seccomp-Quelldateien stehen deshalb im Quellvertrag.

Unter `sandbox-receipts/` entstehen erst nach Build und Versionsproben:

- `build-lock.json`: Source-Pin, Source-SHA256, Compiler-/Versionsbelege und
  SHA256 aller primaeren Artefakte und kopierten Dependency-Locks.
- `Cargo.lock` oder `go.mod`/`go.sum`, bei gVisor erzeugtes `MODULE.bazel.lock`
  und Original-`gvisor.tar.bz2` mit SHA256 im Build-Lock.
- `sbom.cdx.json`: partielles CycloneDX-1.5-Inventar mit Artefakthashes und
  bei Firecracker Paketnamen/-versionen/Checksums aus `Cargo.lock`.
- `version-probes.json`: nur `--version`, kein VM-, Netzwerk- oder Appstart.

Wichtig: Der gVisor-Pin liefert keinen bestaetigten vorab gepinnten
`MODULE.bazel.lock`. Bazel erzeugt ihn mit `--lockfile_mode=update`; seine
Aufloesung ist **nachtraeglich dokumentiert**, nicht vorab hermetisch freigegeben.
Die upstream gepinnten Modul-/Repository-Regeln koennen Go-, LLVM- und
Python-Buildwerkzeuge beziehen. Der erzeugte Lock, nicht ein erfundener SHA256,
wird inventarisiert. Go-Summen sind ein Checksum-Katalog, keine vollstaendige
transitive SBOM. Diese SBOM behauptet weder vollstaendige OS-/Compiler-Abdeckung
noch Bitreproduzierbarkeit oder einen Sicherheits-/Schwachstellen-Scan.

Der Hook ruft kein `/dev/kvm` auf, startet keine VM, keinen API-Socket und keinen
Dienst, schreibt kein CRI/containerd, erstellt keine RuntimeClass und mountet
keine Gastimages. Fuer diese CLI-/Buildkomponenten ist eine systemd-Unit nicht
anwendbar. Keine automatische Sandbox-/Produktionsfreigabe.

## SSH und Lifecycle

Nach zentraler Integration, ueber einen selbst geprueften SSH-Alias:

```bash
ssh -t vps
cd "$HOME/openclaw_ultimate_setup" || exit 1
bash scripts/tools/gvisor_install.sh --install-build-deps
bash scripts/tools/firecracker_install.sh --install-build-deps
bash scripts/tools/kata_containers_install.sh --install-build-deps
bash scripts/tools/gvisor_doctor.sh
bash scripts/tools/firecracker_check.sh
bash scripts/tools/kata_containers_status.sh
```

Jeweils nur das gewuenschte Tool auswaehlen und Exitcode sofort pruefen. Vor
Integration sind diese Wrapper kein zugesicherter Bestandteil dieses Fragments.
Offline-Plan/Status darf keinen Compiler-/Downloadhook ausloesen.

Managed-Uninstall-Vorschlag fuer die Engine: unter derselben Operationssperre
Inventar inklusive Sidecars und Receipts validieren, nur den bewiesenen privaten
`native-github`-Baum entfernen; fehlender Prefix idempotent. Bei Hashabweichung,
Symlink oder unklarer Herkunft stoppen und nicht rekursiv fremde Daten entfernen.
`outer/toolchain` separat behalten, keine apt-Deinstallation. Gastdaten,
MicroVM-Disks, Quellen ausserhalb des Prefix, Container und Benutzerdateien bleiben
unangetastet. Keine eigene rekursive Loeschroutine im Kandidatenhook.

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
python3 -I -B scripts/tool_commands.py show firecracker
python3 -I -B scripts/tool_commands.py show gvisor
python3 -I -B scripts/tool_commands.py show kata_containers
```

### SSH-Aktionen: `firecracker`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run firecracker --action status
python3 -I -B scripts/tool_commands.py run firecracker --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run firecracker --action install --apply --confirm firecracker:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run firecracker --action update --apply --confirm firecracker:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run firecracker --action uninstall --apply --confirm firecracker:uninstall
```

Fehlende Build-Abhaengigkeiten stoppen den Versuch. Nur fuer Install/Update
`--install-build-deps` nach separater Download-Freigabe ergaenzen. Kein Auto-Yes,
kein Docker-Fallback; Source-Build/Status ist keine erfolgreiche Runtime-Abnahme.

### SSH-Aktionen: `gvisor`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run gvisor --action status
python3 -I -B scripts/tool_commands.py run gvisor --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run gvisor --action install --apply --confirm gvisor:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run gvisor --action update --apply --confirm gvisor:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run gvisor --action uninstall --apply --confirm gvisor:uninstall
```

Fehlende Build-Abhaengigkeiten stoppen den Versuch. Nur fuer Install/Update
`--install-build-deps` nach separater Download-Freigabe ergaenzen. Kein Auto-Yes,
kein Docker-Fallback; Source-Build/Status ist keine erfolgreiche Runtime-Abnahme.

### SSH-Aktionen: `kata_containers`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run kata_containers --action status
python3 -I -B scripts/tool_commands.py run kata_containers --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run kata_containers --action install --apply --confirm kata_containers:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run kata_containers --action update --apply --confirm kata_containers:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run kata_containers --action uninstall --apply --confirm kata_containers:uninstall
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
