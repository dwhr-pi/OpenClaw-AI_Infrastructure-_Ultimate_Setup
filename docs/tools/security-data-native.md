# Milvus, Vaultwarden und OWASP ZAP nativ

## Integrationsvertrag

Vorschlag: `config/native-candidates/security-data.json`. Keine zentrale Registry,
kein Menue und keine alten Wrapper werden durch diesen Beitrag geaendert.
Der zentrale Merger integriert die drei `candidate-native`-Rezepte.
Modul: `scripts/tools/helpers/security_data_native.py`.

- `preflight(outer, spec, approved=False)`: Linux x86_64, Disk/RAM und vorhandene
  Werkzeuge pruefen; fuer ZAP und Vaultwarden erlaubt `approved` die unten beschriebene Buildbasis.
  Milvus erhaelt dadurch keinen zusaetzlichen Downloadpfad.
- `build(source, prefix, spec, env, run=None)`: `source == prefix/source`, voller
  Git-Pin/Origin und SHA256-Quellvertraege; Rueckgabe aller prefix-relativen
  Artefakt-/Konfigurations-/Nachweispfade. Optionaler Runner: `(args,cwd,env)`
  mit geprueftem Exitcode und vollstaendigem stdout als String; keine Shell.
- `doctor(prefix,spec)`: SHA256-Pruefung und statische ELF/JAR-Probe ohne
  Anwendungsstart. Das Ergebnis enthaelt `doctor_exit=3`, `runtime_tested=false`.
  Der zentrale Dispatcher muss diesen unvollstaendigen Laufzeitstatus erhalten.

Der Default-Buildrunner beendet nach 14400 Sekunden die Prozessgruppe. Ein
injizierter Runner muss das gleiche begrenzte Fehler-/Abbruchverhalten bieten.
Builds duerfen Quell-/Paketserver kontaktieren; Diagnose und Probes nicht.
Kein Docker-, Podman-, rustup- oder Wrapper-Download-Fallback.
Die ZAP-/Vaultwarden-Buildbasis wird ausschliesslich im freigegebenen Vorbereitungsschritt eingerichtet;
der Build selbst installiert keine Systempakete und laedt keine Toolchain nach.
Git-/Paket-Zugangsdaten und geerbte Anwendungsvariablen werden nicht uebernommen.

## Pins und Umfang

### Milvus

[Offizieller Release v3.0.6](https://github.com/milvus-io/milvus/releases/tag/v3.0.6),
Commit `63100f8f5b4b675a12fe78fc9673b005ee318731`, Apache-2.0.
[Quell-Buildvertrag](https://github.com/milvus-io/milvus/blob/63100f8f5b4b675a12fe78fc9673b005ee318731/scripts/3rdparty_build.sh)
und [Conan-Abhaengigkeiten](https://github.com/milvus-io/milvus/blob/63100f8f5b4b675a12fe78fc9673b005ee318731/internal/core/conanfile.py).

CPU-Server aus Go plus C++/Rust-Core, SIMD/AVX und den bereits versionierten,
eingebetteten `internal/http/webui`-Assets. Kein erneuter Frontend-Download.
GPU, DiskANN, SVS und C++-Tests sind deaktiviert. Kein Ersatz durch Milvus Lite.
Buildbasis: Go >=1.26.9, Rust 1.92.0, Conan 2.25.1, GCC >=12/C++20,
CMake >=3.26, make, pkg-config, Perl, NASM, protoc; 64 GiB freie Disk,
8 GiB verfuegbarer RAM, zwei Jobs. Auch WSL-Backing-Volume wird geprueft.
`NATIVE_SOURCE_RUST_TOOLCHAIN` muss eine bereits installierte absolute Toolchain
mit `bin/rustc` und `bin/cargo` bezeichnen; kein globaler Toolchain-Wechsel.

Conan verwendet ein privates HOME und das im offiziellen Skript benannte
oeffentliche Milvus-JFrog-Remote. Lock-Erzeugung vor `conan install --build=*`;
auch C++-Abhaengigkeiten werden damit gebaut, nicht als fertige Milvus-Runtime
geladen. Nur der gepruefte Shared-Library-Buildhook wird aus dem Upstream-Skript
uebernommen. Das gesamte Installationsskript und das globale `make` werden nicht
ausgefuehrt. Native Shared Libraries verbleiben unter `source/internal/core/output`
und `source/cmake_build/lib`; diese sind KEIN entfernbarer Buildcache.

Artefakte: `bin/milvus`, Core-Libraries/Includes, Conan-Libraries,
`config/milvus.yaml.example`. Die Unit-Vorlage braucht manuell eine eigene
Konfiguration und `LD_LIBRARY_PATH` mit diesen privaten Library-Verzeichnissen.
**Kein vollstaendiges Deployment:** etcd, S3/MinIO und ggf. Pulsar/Kafka werden
weder installiert noch gestartet. Fuer den Betrieb existieren keine erfundenen
Pins/Nachweise dieser externen Dienste. Auth, TLS, Persistenz, Backup/Restore,
Runtime-Linker und produktive Standalone-Konfiguration bleiben separat abzunehmen.

### Vaultwarden

[Offizieller Release 1.37.5](https://github.com/dani-garcia/vaultwarden/releases/tag/1.37.5),
Commit `6ed6921cc2b0e03b4d74189574d2a5e71c512e97`, AGPL-3.0-only.
[Rust-Pin](https://github.com/dani-garcia/vaultwarden/blob/6ed6921cc2b0e03b4d74189574d2a5e71c512e97/rust-toolchain.toml)
und [Features](https://github.com/dani-garcia/vaultwarden/blob/6ed6921cc2b0e03b4d74189574d2a5e71c512e97/Cargo.toml).

Rust 1.99.1, C-Compiler, pkg-config, Perl, OpenSSL-Entwicklung und System-C-Laufzeit;
12 GiB Disk und 4 GiB verfuegbarer RAM. Seit 19.11.2026 richtet der Installer fehlende
Buildvoraussetzungen nach Zustimmung im Setup-Dialog selbst ein. CLI-Freigabe:
`bash scripts/tools/vaultwarden_install.sh --install-build-deps`.
Debian-/Ubuntu-Familie einschliesslich Ubuntu 26 und DietPi: ausschliesslich
`build-essential`, `pkg-config`, `perl`, `libssl-dev` aus vorhandenen apt-Quellen;
abweichende Basen erhalten vor der Installation eine Paketaufloesungssimulation.

Ein vorhandenes passendes Rust wird bevorzugt. Sonst installiert der private Bootstrap
Rust 1.99.1 unter `toolchain/rust-1.99.1-linux-amd64`, getrennt von Rust 1.98.0 anderer Tools.
Quelle ist ausschliesslich `static.rust-lang.org`; der bestehende Bootstrap prueft
Dateigroesse/SHA256 von `rustup-init` 1.29.2 vor Ausfuehrung, danach rustc-/Cargo-Version,
sysroot und das lokale Dateiinventar. Rustup prueft die Distributionskomponenten beim Download;
dies ersetzt keinen eigenen, vollstaendig vendorten Toolchain-Lock.
Zusaetzliche Speicherreserve: 2 GiB, also 14 GiB vor dem Rust-Bootstrap, auch auf dem WSL-Host.

Nachtrag 20.11.2026: Der gemeldete Lauf hatte auf C: 13946 MiB frei. Die
12-GiB-Basispruefung bestand, fuer den erforderlichen Rust-Bootstrap galten
jedoch 14336 MiB; es fehlten mindestens 390 MiB. Der Abbruch war korrekt,
kein Rust-/Python-Buildfehler. Ein Setup-Update schafft keinen freien Host-Speicher.
Menue-Vorpruefung, Voraussetzungen-Dialog und Plan nennen jetzt diesen
bedingten Zusatzbedarf. Die Menueanzeige behauptet nicht, dass Rust fehlt;
die verbindliche Toolchain-/Speicherpruefung bleibt im Installer.
Eine passende vorhandene Basis wird weiterhin ohne neuen Bootstrap bevorzugt.
Reserven werden nicht gesenkt, Daten nicht automatisch geloescht und ein
Speicherabbruch nicht durch `--install-build-deps` umgangen. Der Mindestwert
ist keine Garantie fuer den gesamten spaeteren Betrieb oder andere parallele Installationen.
Kein System-Rust-/Default-/Shell-PATH-Wechsel; `--no-modify-path` und private Cargo-/Rustup-Verzeichnisse.
Ein explizites `NATIVE_SOURCE_RUST_TOOLCHAIN` muss gueltig sein und wird nie still ersetzt.
Ohne Zustimmung, bei Hash-/Versionsfehlern oder veraendertem privatem Bestand wird abgebrochen.
Buildwerkzeuge bleiben bei App-Deinstallation erhalten; vorhandene Daten werden nicht entfernt.
Offline-Fixtures ersetzen keinen erfolgreichen WSL-Quellbuild.

`cargo build --locked --release
--no-default-features --features sqlite --bin vaultwarden`; SQLite wird gebuendelt.
Kein PostgreSQL/MySQL, keine Datenbankanlage oder Migration.

**Bewusster Backend-Komponentenumfang:** kein Web-Vault enthalten.
Die eigene ENV-Vorlage setzt deshalb `WEB_VAULT_ENABLED=false`, deaktiviert
Registrierungen und bindet spaeter nur Loopback. Upstream `.env.template` wird als
separate Referenz kopiert und nicht geladen. Das gepinnte Upstream-Rezept nennt
Web-Vault v2026.10.1; dessen gepatchter Webclient hat einen getrennten
[Buildprozess](https://github.com/dani-garcia/bw_web_builds). Ein ungeprueftes
Webarchiv, ein ungepatchter Bitwarden-Client oder Container-Extraktion werden
nicht als Ersatz eingebaut. Browser-Webvault, TLS/Reverse Proxy, Clientkompatibilitaet
und Restore bleiben offen. Keine Passwort-/Token-/Schluesselerzeugung.

Artefakte: `bin/vaultwarden`, ENV-Vorlagen, Cargo-Lock und Unit-Vorlage.
Selbst `--version` wird nicht benutzt, da der Quellpfad Web-Vault-Konfiguration
liest. Die Probe inspiziert ausschliesslich ELF-Header und Ausfuehrungsbit.

### OWASP ZAP

[Offizieller Release v2.17.0](https://github.com/zaproxy/zaproxy/releases/tag/v2.17.0),
Commit `8a1bff313f4d183dba5aa154ecbe89ad751c9153`, Apache-2.0.
[Buildanleitung](https://github.com/zaproxy/zaproxy/blob/8a1bff313f4d183dba5aa154ecbe89ad751c9153/BUILDING.md)
und [Distributionstasks](https://github.com/zaproxy/zaproxy/blob/8a1bff313f4d183dba5aa154ecbe89ad751c9153/buildSrc/src/main/kotlin/org/zaproxy/zap/distributions.gradle.kts).

JDK 21 (Compiler/Error Prone) und Gradle 8.13, 12 GiB Disk/4 GiB RAM.
Seit der Installerkorrektur vom 19.11.2026 werden fehlende Voraussetzungen nach
Zustimmung im Voraussetzungen-Dialog bereitgestellt. Ohne Zustimmung kein Download.
CLI-Freigabe: `bash scripts/tools/owasp_zap_install.sh --install-build-deps`.
Debian-/Ubuntu-Familie einschliesslich neuer Releases und DietPi: fehlendes JDK 21
via `openjdk-21-jdk-headless`, ausschliesslich aus vorhandenen apt-Quellen, mit
Paketaufloesungssimulation auf abweichenden Basen. apt kann gemeinsame Abhaengigkeiten
und Java-Alternativen aktualisieren; kein erzwungenes `update-alternatives`.
Ein passendes vorhandenes JDK wird bevorzugt, sonst wird JDK 21 nur fuer diesen Build
per `JAVA_HOME`/Prozess-PATH ausgewaehlt. Keine Fremdquelle und kein Versions-Bypass.

Fehlendes oder unpassendes Gradle wird privat unter `toolchain/gradle-8.13` eingerichtet:
[offizielle Gradle-Distribution](https://github.com/gradle/gradle-distributions/releases/tag/v8.13.0),
Archiv `gradle-8.13-all.zip`, 232036537 Bytes, SHA256
`fba8464465835e74f7270bbf43d6d8a8d7709ab0a43ce1aa3323f73e9aa0c612`.
Der Hash wurde gegen die
[offizielle Gradle-Pruefsumme](https://services.gradle.org/distributions/gradle-8.13-all.zip.sha256)
abgeglichen. Begrenztes Entpacken
verwirft Links und unsichere Pfade; Wiederverwendung prueft das gesamte Dateiinventar.
Ein beschaedigtes vorhandenes Ziel wird nicht ueberschrieben. Der Bootstrap verlangt
zusaetzlich 1 GiB Speicherreserve und hinterlaesst bei Downloadfehlern keinen fertigen
Installationsnachweis. Gemeinsame Buildwerkzeuge bleiben bei Deinstallation erhalten.
Offline-Fixtures pruefen Zustimmung, Paketfreigabe, Hashfehler und Manipulation;
ein erfolgreicher Linux-/WSL-Quellbuild ist damit noch nicht nachgewiesen.
Wrapper und automatische Gradle-JDK-Provisionierung werden nicht benutzt.
`:zap:distFiles` baut `zap-2.17.0.jar`, Runtime-JARs und
vollstaendige Core-Ressourcen (`xml`, `lang`, `db`, Startskripte).
Der upstream Runtime-CycloneDX-BOM wird ueber `jarWithBom` erzeugt.
`--write-locks --write-verification-metadata sha256` erzeugt die lokalen
Dependency-Locks/Checksum-Metadaten. Dies ist Erstaufloesung/TOFU fuer transitive
Maven-Artefakte, KEIN vorab unabhaengig gepruefter Supply-Chain-Lock.

**Core ohne Add-ons:** kein `distCore`/`distLinux`, weil diese Tasks automatisch
Add-ons laden. Keine Add-on-Downloads, Browser, JRE, install4j oder Lizenzschluessel.
Damit kein vollstaendiges Scannerprofil und keine Gleichsetzung mit der normalen
ZAP-Distribution. Die JAR-Probe liest ZIP-Integritaet, Main-Klasse und Version
mit begrenztem Entpackbudget. Kein Java-Anwendungsprozess, Port, Session-DB,
API-Key, Ziel-URL oder Scan. Eine systemd-Unit ist fuer diesen Desktop/Core-
Komponentenumfang nicht anwendbar und wird nicht erstellt.

## Nachweise und Entfernung

`candidate-build-lock.json` speichert Quellvertraege und beobachtete Toolversionen.
`locks/` enthaelt Cargo-/Conan-/Go-/Gradle-Nachweise und ZAPs Runtime-BOM.
`candidate-sbom.cdx.json` wird aus Cargo-Packages/Checksums, Conan-Graph und
Go-Modulliste bzw. dem ZAP-Runtime-BOM erzeugt. Er deckt die jeweilige Komponente
ab, nicht die komplette OS-/Compiler-/Buildplugin-Lieferkette. Keine Aussage ueber
CVE-Freiheit oder bitidentische Reproduzierbarkeit. Artefakt-SHA256 werden erst
nach erfolgreichem Build generiert, nicht als erfundene Vorab-Pruefsummen.
`candidate-artifact-receipt.json` inventarisiert alle zurueckgegebenen Payloads;
die zentrale Engine muss auch diesen Nachweis in ihrem Besitzinventar schuetzen.

Die zentrale Engine bleibt alleiniger Besitzer von Installationslock, atomarem
Ready-Marker, kompletter Bestandspruefung, Rollback und idempotentem Uninstall.
Dieser Hook loescht weder Installation noch Benutzerdaten. Entfernen nur bei
passendem Pin/Rezepthash und unveraendertem Gesamtinventar; neue/geaenderte Dateien
blockieren Uninstall. Nutzdaten, ENV-Dateien mit Secrets, Logs und manuell
installierte Units gehoeren ausserhalb von `native-github`, z.B. nach
`~/.openclaw_ultimate_user_data/data/TOOL`. Keine automatisch aktivierte Unit.
Vorlagen mit `@PREFIX@`, `@DATA@`, `@ENV_FILE@` sind absichtlich nicht startfaehig.
Vor manueller Aktivierung Pfade ersetzen, Optionen pruefen und Daten sichern.

## SSH und Abnahme

Zuerst Host-Fingerprint unabhaengig pruefen und dann `ssh -t vps` verwenden.
Im bereits geprueften Repository auf dem Linux-VPS nach zentraler Integration:

```bash
python3 -I -B scripts/tools/helpers/native_github_tools.py milvus plan
python3 -I -B scripts/tools/helpers/native_github_tools.py vaultwarden plan
python3 -I -B scripts/tools/helpers/native_github_tools.py owasp_zap plan
```

Installationsaktionen erst nach Sichtpruefung der jeweiligen Buildbasis und des
Komponentenumfangs bewusst ausfuehren; keine Dienststarts in dieser Anleitung.
Vor zentraler Integration erkennt die Engine diese Vorschlaege noch nicht.
Tests: `python3 -B -m unittest discover -s tests -p test_security_data_native.py`.
Die Tests verwenden synthetische ELF/JAR-/Cargo-Fixtures und Mocks. Sie beweisen
Sicherheits-/Befehlsvertraege, keinen echten Build oder produktiven Betrieb.
Linux-Builds, dynamische Linkaufloesung, Funktion, TLS, Client-/Add-on-Kompatibilitaet
und Restore sind nicht abgenommen und duerfen nicht als erfolgreich erscheinen.

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
python3 -I -B scripts/tool_commands.py show milvus
python3 -I -B scripts/tool_commands.py show owasp_zap
python3 -I -B scripts/tool_commands.py show vaultwarden
```

### SSH-Aktionen: `milvus`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run milvus --action status
python3 -I -B scripts/tool_commands.py run milvus --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run milvus --action install --apply --confirm milvus:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run milvus --action update --apply --confirm milvus:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run milvus --action uninstall --apply --confirm milvus:uninstall
```

Fehlende Build-Abhaengigkeiten stoppen den Versuch. Nur fuer Install/Update
`--install-build-deps` nach separater Download-Freigabe ergaenzen. Kein Auto-Yes,
kein Docker-Fallback; Source-Build/Status ist keine erfolgreiche Runtime-Abnahme.

### SSH-Aktionen: `owasp_zap`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run owasp_zap --action status
python3 -I -B scripts/tool_commands.py run owasp_zap --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run owasp_zap --action install --apply --confirm owasp_zap:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run owasp_zap --action update --apply --confirm owasp_zap:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run owasp_zap --action uninstall --apply --confirm owasp_zap:uninstall
```

Fehlende Build-Abhaengigkeiten stoppen den Versuch. Nur fuer Install/Update
`--install-build-deps` nach separater Download-Freigabe ergaenzen. Kein Auto-Yes,
kein Docker-Fallback; Source-Build/Status ist keine erfolgreiche Runtime-Abnahme.

### SSH-Aktionen: `vaultwarden`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run vaultwarden --action status
python3 -I -B scripts/tool_commands.py run vaultwarden --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run vaultwarden --action install --apply --confirm vaultwarden:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run vaultwarden --action update --apply --confirm vaultwarden:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run vaultwarden --action uninstall --apply --confirm vaultwarden:uninstall
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
