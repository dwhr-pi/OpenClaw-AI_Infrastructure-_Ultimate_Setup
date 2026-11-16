# Kubescape, Nuclei, TruffleHog und testssl nativ

Die Installer bauen CLIs aus gepinnten Originalquellen. Kein automatischer Scan,
kein Zielsystem, Credential-Check, Template-Download oder Dienststart wird ausgewaehlt.
Der [Quellvertrag](../../config/native-candidates/security.json) enthaelt Pins,
Lizenzen, Go-Anforderungen, Source-SHA256 und die scanfreien Probe-Argumente.

## Installation im Setup

```bash
bash scripts/tools/kubescape_install.sh --install-build-deps
bash scripts/tools/nuclei_install.sh --install-build-deps
bash scripts/tools/trufflehog_install.sh --install-build-deps
bash scripts/tools/testssl_install.sh --install-build-deps
```

Nur gewuenschte Tools auswaehlen; diese Befehle sind keine Empfehlung, alle Scanner gleichzeitig auszufuehren.
Der Menueweg fragt vor fehlenden gemeinsamen Buildvoraussetzungen nach Zustimmung.
Go wird bei Bedarf privat und mit gepruefter Archiv-SHA256 eingerichtet.
testssl verwendet das System-OpenSSL, keine ungepruefte beiliegende OpenSSL-Binary.
Die Werkzeugdateien liegen unter `~/.openclaw_ultimate_user_data/tools/TOOL/native-github/`.

Die begrenzten Versionsproben laufen ohne Benutzerdaten in einem neuen Netzwerk-Namespace.
Falls `unshare --user --map-root-user --net` vom Host untersagt ist, bricht die Vorpruefung ab;
der Installer schaltet keine Kernel-/AppArmor-Schutzmassnahmen ab und weicht nicht auf einen Netzwerktest aus.
WSL, Ubuntu, DietPi und andere Debian-Derivate sind nicht allein durch ihren Namen kompatibel:
Architektur, Compiler, Pakete, User-Namespaces, RAM und echter Backing-Speicher werden getrennt geprueft.

## Nachweise und Deinstallation

Build-Locks, CycloneDX-SBOM, Artefakt-Hashes und Versionsproben werden erst nach erfolgreichem Build geschrieben.
Die echte Linux-Build-/Scanabnahme steht aus; Templates und Autorisierung sind gesondert zu pruefen.

```bash
bash scripts/tools/nuclei_status.sh
bash scripts/tools/nuclei_doctor.sh
bash scripts/tools/nuclei_update.sh --install-build-deps
bash scripts/tools/nuclei_uninstall.sh
```

Analog den Toolnamen ersetzen. Uninstall bleibt auf unveraenderte eigene Dateien begrenzt;
kein Scanergebnis, fremder Binary-Pfad oder Benutzerbestand wird geloescht.
Bei SSH im geprueften Ziel-Checkout arbeiten, Host-Fingerprint unabhaengig pruefen und keine Secrets in Git ablegen.

Originalquellen: [Kubescape](https://github.com/kubescape/kubescape),
[Nuclei](https://github.com/projectdiscovery/nuclei),
[TruffleHog](https://github.com/trufflesecurity/trufflehog), [testssl.sh](https://github.com/testssl/testssl.sh).

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
python3 -I -B scripts/tool_commands.py show kubescape
python3 -I -B scripts/tool_commands.py show nuclei
python3 -I -B scripts/tool_commands.py show testssl
python3 -I -B scripts/tool_commands.py show trufflehog
```

### SSH-Aktionen: `kubescape`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run kubescape --action status
python3 -I -B scripts/tool_commands.py run kubescape --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run kubescape --action install --apply --confirm kubescape:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run kubescape --action update --apply --confirm kubescape:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run kubescape --action uninstall --apply --confirm kubescape:uninstall
```

Fehlende Build-Abhaengigkeiten stoppen den Versuch. Nur fuer Install/Update
`--install-build-deps` nach separater Download-Freigabe ergaenzen. Kein Auto-Yes,
kein Docker-Fallback; Source-Build/Status ist keine erfolgreiche Runtime-Abnahme.

### SSH-Aktionen: `nuclei`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run nuclei --action status
python3 -I -B scripts/tool_commands.py run nuclei --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run nuclei --action install --apply --confirm nuclei:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run nuclei --action update --apply --confirm nuclei:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run nuclei --action uninstall --apply --confirm nuclei:uninstall
```

Fehlende Build-Abhaengigkeiten stoppen den Versuch. Nur fuer Install/Update
`--install-build-deps` nach separater Download-Freigabe ergaenzen. Kein Auto-Yes,
kein Docker-Fallback; Source-Build/Status ist keine erfolgreiche Runtime-Abnahme.

### SSH-Aktionen: `testssl`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run testssl --action status
python3 -I -B scripts/tool_commands.py run testssl --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run testssl --action install --apply --confirm testssl:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run testssl --action update --apply --confirm testssl:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run testssl --action uninstall --apply --confirm testssl:uninstall
```

Fehlende Build-Abhaengigkeiten stoppen den Versuch. Nur fuer Install/Update
`--install-build-deps` nach separater Download-Freigabe ergaenzen. Kein Auto-Yes,
kein Docker-Fallback; Source-Build/Status ist keine erfolgreiche Runtime-Abnahme.

### SSH-Aktionen: `trufflehog`

Status und Diagnose lesen den privaten Tool-Zustand auf dem VPS:

```bash
python3 -I -B scripts/tool_commands.py run trufflehog --action status
python3 -I -B scripts/tool_commands.py run trufflehog --action doctor
```

Die folgenden Befehle **einzeln und nur nach Freigabe** ausfuehren, nicht als
gemeinsamen Ablauf: Installation, spaeter Update oder bewusst Deinstallation.
Vorher Quellen, Lizenz, Ressourcen und Daten-Erhaltungsregeln dieser Anleitung pruefen.

Installieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run trufflehog --action install --apply --confirm trufflehog:install
```

Aktualisieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run trufflehog --action update --apply --confirm trufflehog:update
```

Deinstallieren (separate Entscheidung):

```bash
python3 -I -B scripts/tool_commands.py run trufflehog --action uninstall --apply --confirm trufflehog:uninstall
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
