# GitHub-Installierbarkeit: MiniMax bis Cloudflare

Stand: 15.11.2026. Keine nativen Linux-Builds auf diesem Windows-Arbeitsplatz
ausgefuehrt. Offline-Fixtures sind keine Build-, GPU-, Modell- oder Dienstabnahme.
Das veroeffentlichte signierte Release v11.18.0 wird nicht nachtraeglich veraendert.
Diese Aenderungen brauchen Review, Commit und ein eigenes spaeteres signiertes Release.

## Umfang und Grenzen

Der bestaetigte Auftrag umfasst auch Musik-/Poesie-Tools. Der vollstaendige
bekannte Abschnitt ist maschinenlesbar in
[`config/source_install_readiness.json`](../../config/source_install_readiness.json)
erfasst. Ein GitHub-Checkout ist kein installierter Modellserver. Nicht oeffentlich
verfuegbare Quellen oder ungeklaerte Lizenzen werden nicht erfunden oder umgangen.

| Tools | Aktueller Installationsumfang / verbleibender Blocker |
| --- | --- |
| Outlines | Neuer nativer Python-Basisbuild, upstream uv.lock, keine Modelle/Backend-Extras |
| eSpeak NG | Neuer privater CMake-Build mit Sprachdaten, ohne Audiostart |
| SongRec | Neuer nativer CLI-Build aus Tag 0.4.3 mit Cargo.lock, keine GUI/Shazam-Anfrage |
| Cloudflared | Bestehender nativer Go-CLI-Build; Cloudflare selbst ist kein lokal installierbarer Cloud-Dienst |
| MiniMax M3, DeepSeek R1, Qwen Coder, Qwen3 235B, QwQ 32B, GPT OSS 120B | Modellquellen; Gewichte, Lizenz, Quantisierung und Backend/Hardware noch separat freizugeben |
| Obot | Pin verlangt Go 1.27.0 und UI-Build; kein freigegebener nativer Gesamtserver |
| SongSage | Offizielle baubare GitHub-Quelle und Lizenz unbestaetigt; gesperrt |
| Dejavu | Alte NumPy-/SciPy-/PyAudio-Pins passen nicht unveraendert zu Ubuntu/Python 3.12 |
| LeVo 2, MOSS Music | Forschungs-/Lizenz-/Gewichts-/GPU- und Dependency-Freigabe offen |
| PoeLM, PoeTone, CoPoet, CTGS | Lizenz-/Dependency-/Modell- bzw. Desktop-/Headless-Abnahme offen; nur Quellen |
| Audile | Android-App, kein Linux-VPS-Dienst; SDK/JDK/Gradle/APK-Signierung noch offen |
| Mousai | Desktop-/GTK-/GStreamer-/Rust-/Meson-Build und echte Desktop-Abnahme offen |
| MusicGen / AudioCraft | Code- und Gewichtslizenz trennen; nativer Torch-/Codec-/Modellpfad noch offen |

**Nicht alles in diesem Abschnitt ist damit bereits installierbar.** Die neuen
Buildrezepte sind Testkandidaten. Die bisherige Bezeichnung source-only wird
nicht durch ein pauschales gruenes Installationslabel ersetzt.

Offline-Uebersicht, keine Downloads und keine Credential-Zugriffe:

```bash
python3 -I -B scripts/quality/source_install_readiness.py
```

## Ubuntu 24.04 und WSL: bewusst vorbereiten

Nur auf dem kuenftigen Testrechner ausfuehren, nicht als automatische Aktion.
APT wird nur fuer System-/Build-Abhaengigkeiten verwendet, nicht fuer diese Apps:

```bash
sudo apt-get update
sudo apt-get install --no-install-recommends \
  build-essential cmake pkg-config gettext libasound2-dev \
  libglib2.0-dev libssl-dev python3-venv
```

Fuer SongRec wird zusaetzlich eine bereits eingerichtete Rust-/Cargo-Basis
benoetigt. Kein unkontrolliertes curl-pipe-shell oder Docker-Fallback.
Outlines bevorzugt vorhandenes uv >=0.13.5. Fehlt es, darf der bestehende
private GitHub-uv-Bootstrap nur nach ausdruecklicher Zustimmung verwendet werden.
Keine Python-Laufzeit, Modelle oder CUDA-Pakete werden dabei automatisch geladen.

Pruefe sowohl freien Linux-Zielspeicher als auch Windows-Host-Speicher. Die
WSL-VHDX kann nur wachsen, soweit ihr physischer Datentraeger Platz hat.
Die Mindestreserven 4/4/8 GiB sind Untergrenzen, keine zugesagte Groessenmessung.
Vor grossen Builds ausreichend zusaetzliche Windows-Reserve schaffen.

## Einzeln testen, nicht alle gleichzeitig installieren

Vom geprueften neuen Checkout aus, als normaler Benutzer, ohne sudo:

```bash
bash scripts/tools/outlines_install.sh --dry-run
bash scripts/tools/outlines_install.sh --install-build-deps
bash scripts/tools/outlines_doctor.sh --smoke
bash scripts/tools/espeak_ng_install.sh --dry-run
bash scripts/tools/espeak_ng_install.sh
bash scripts/tools/espeak_ng_doctor.sh --smoke
bash scripts/tools/songrec_install.sh --dry-run
bash scripts/tools/songrec_install.sh
bash scripts/tools/songrec_doctor.sh --smoke
bash scripts/tools/cloudflared_install.sh --dry-run
```

Jeden Befehl einzeln ausfuehren; bei Fehlern stoppen und das Installationslog
sichern. Bei vorhandenem reinem Quellbestand wird nicht automatisch migriert:
zuerst `*_doctor.sh --source-only` und `*_uninstall.sh --source-only --dry-run`
pruefen. Entfernen nur nach Sicherung eigener Aenderungen und ausdruecklicher Freigabe.
Logs, Modelle und andere Benutzerdaten unter `~/.openclaw_ultimate_user_data`
bleiben erhalten. CLI/Bibliotheken benoetigen keine automatisch gestartete Unit.

Der Installations-Smoke-Check ist auf 30 Sekunden begrenzt. Er prueft nur
Outlines-Import/Regex-Typ bzw. CLI-Version. Status/Doctor ohne `--smoke` starten
keinen Code aus den Tool-Runtimes. Kein Provider-, Mikrofon-, Modell- oder Diensttest.

## Nachweise und naechste Schritte

Source-Pins sowie SHA256 von Lizenz-/Build-/Lockdateien stehen im Builder.
Die volle Besitz-/Dateiinventur schuetzt Updates und Deinstallation.
`native-sbom.cdx.json` dokumentiert Python-Distributionen bzw. Cargo-Lockpakete;
bei eSpeak nur die Hauptkomponente. Dies ist keine vollstaendige transitive
OS-/Compiler-SBOM. Upstream-Buildabhaengigkeiten koennen Registry-Downloads
brauchen; GitHub-Quelleninstallation bedeutet nicht, dass jede Abhaengigkeit aus Git stammt.

- P1: Drei neue Builds auf Ubuntu 24.04/WSL mit Betriebssystem-, Compiler-, Zeit-, Speicher- und Lognachweis abnehmen.
- P1: Fuer SongSage eine autoritative lizenzierte Quelle beschaffen.
- P1: Fuer Dejavu einen separaten getesteten Python-3.12-Port entwickeln.
- P2: Obot-Toolchain/UI, Audile-APK und Mousai-Desktop jeweils als eigene native Buildauftraege abnehmen.
- P2: Forschungsprojekte auf Code-/Daten-/Gewichtslizenz und reproduzierbare Abhaengigkeiten pruefen.
- P3: Modellkarten, Gewichtshashes und Hardwareprofile explizit freigeben; erst danach getrennte Modell-/Inferenztests.

## Originalquellen der Buildpruefung

- [Outlines pyproject][outlines-project] und [uv.lock][outlines-lock].
- [eSpeak Buildanleitung][espeak-build].
- [SongRec Cargo.toml fuer 0.4.3][songrec-cargo].
- [Dejavu requirements][dejavu-requirements].
- [Obot go.mod][obot-go].

[outlines-project]: https://github.com/dottxt-ai/outlines/blob/c52af8472c6fe8a607a733ec11b709476af77a96/pyproject.toml
[outlines-lock]: https://github.com/dottxt-ai/outlines/blob/c52af8472c6fe8a607a733ec11b709476af77a96/uv.lock
[espeak-build]: https://github.com/espeak-ng/espeak-ng/blob/688cb60368d6e0998f3632af8d1c3c2ad4191fc2/docs/building.md
[songrec-cargo]: https://github.com/marin-m/SongRec/blob/15da6b224297d7bf8a9c91b9f70af3d499a9636d/Cargo.toml
[dejavu-requirements]: https://github.com/worldveil/dejavu/blob/e56a4a221ad204654a191d217f92aebf3f058b62/requirements.txt
[obot-go]: https://github.com/obot-platform/obot/blob/251f96eb1ddae99d61e78a15b7a96115fc45630b/go.mod

Die Metadatendateien wurden am 15.11.2026 vollstaendig ueber ihre originalen
raw.githubusercontent.com-URLs gelesen, nicht aus Suchsnippets uebernommen.
Diese Pruefung ist keine neue Lizenz-/Runtime-Freigabe der gesamten uebrigen Matrix.

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
