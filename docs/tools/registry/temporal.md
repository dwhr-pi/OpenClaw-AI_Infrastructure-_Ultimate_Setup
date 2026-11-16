# Temporal: SSH-Einstieg

Tool-ID: `temporal`. Diese Einstiegsseite ergaenzt die bisher fehlende
Dokumentationszuordnung. Sie ist **keine vollstaendige Lifecycle-Anleitung** und
kein Build-, Inferenz-, Sicherheits- oder Produktionsnachweis.

## Vor der Installation

Die Details aus `config/tools.yml` und dem lokalen Offline-Plan pruefen.
Reifegrad: `planned`; Bereitschaft: `unknown`.
Fehlende Reifegradangaben werden nicht als Freigabe interpretiert.
Nur Git-Quellen verwenden; kein Docker-/Compose-Installationsfallback.
Plattform, Lizenz, benoetigte Hardware, Speichervorrat und Quell-Pins vorab pruefen.
Keine Modelle, Cloud-Anfragen oder Produktivdienste ungefragt starten.

Registrierter Sicherheitshinweis: Workflow Engine, schwer.

Registrierte Quelle (hier nicht erneut online verifiziert): `https://github.com/temporalio/temporal`.

## Registrierte Lifecycle-Pfade

Die Links zeigen Repository-Code zur Pruefung, **keine Ausfuehrungsfreigabe**.
Fehlende Update-/Doctor-/Statuspfade bleiben offene Implementierungsaufgaben.

- `install`: [registriertes Skript](../../../scripts/tools/planned_tool_stub_install.sh).
- `update`: kein Skript in der Registry hinterlegt.
- `uninstall`: [registriertes Skript](../../../scripts/tools/planned_tool_stub_uninstall.sh).
- `doctor`: kein Skript in der Registry hinterlegt.
- `status`: kein Skript in der Registry hinterlegt.

Secrets und Daten bleiben unter `~/.openclaw_ultimate_user_data`.
Vor Updates und Deinstallation ein verschluesseltes Backup und die
tool-spezifischen Erhaltungsregeln pruefen; keine Verzeichnisse pauschal loeschen.

## Weitere Orientierung

[SSH-Verfahren und Freigaben](../../HEADLESS_SETUP.md),
[Installationsrichtlinie](../../INSTALLATION_POLICY.md) und
[Backup/Wiederherstellung](../../INSTALLATION_STATUS_BACKUP.md).

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
python3 -I -B scripts/tool_commands.py show temporal
```

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

[SSH-Voraussetzungen und Sicherheitsgrenzen](../../HEADLESS_SETUP.md) | [Befehle aller registrierten Tools](../../generated/HEADLESS_TOOL_COMMANDS.md)

Dieser Abschnitt wird aus der Registry erzeugt. Pflege: `python3 -I -B scripts/quality/tool_ssh_docs.py --write`.

<!-- END GENERATED VPS SSH -->
