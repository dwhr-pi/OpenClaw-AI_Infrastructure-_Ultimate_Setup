# Setup 11.18 installieren: Schritt fuer Schritt

Diese Anleitung fuehrt dich von GitHub bis zum Setup-Menue. Sie ist fuer
**Ubuntu, Linux und Ubuntu unter WSL** geschrieben. Arbeite die Schritte der
Reihe nach ab. Kopiere nur den Inhalt der Codebloecke, niemals das Promptzeichen `$`.

## 1. Version und Ziel verstehen

**Aktueller Setup-Stand: 11.18.** Ziel fuer das neue signierte Release: `v11.18.0`.
Das Setup-Menue sowie Tool- und Profilkataloge tragen bereits 11.18.
Die dreiteilige Tag-Nummer ist fuer den Release-Pruefer erforderlich.

Stand 12.11.2026 wurde oeffentlich nur `v11.17.0` mit den vier signierten
Assets gefunden. **`v11.18.0` ist noch nicht veroeffentlicht.** Schritte 2-4
kannst du zum Beziehen der Quellen verwenden. Fuer Schritt 5 brauchst du einen
unabhaengig geprueften Commit; ab Schritt 7 muss das neue signierte Release
tatsaechlich bereitstehen. Ein angekuendigtes Release ist noch kein Download.
Der Maintainer folgt vorher der [Release-Checkliste fuer v11.18.0](releases/v11.18.0.md).

Die alte [Anleitung fuer v11.17.0](legacy/INSTALL_SIGNED_RELEASE_v11_17_0.md)
bleibt als Historie erhalten. Alte Tags, Dateien und Signaturen werden nicht
umbenannt oder ueberschrieben. Es gibt keinen automatischen unsignierten Ersatzweg.

Du bekommst zwei getrennte Ordner:

| Ordner | Zweck |
| --- | --- |
| `~/OpenClaw-Quellpruefung` | Quellen herunterladen, geprueften Bootstrap bereitstellen |
| `~/openclaw_ultimate_setup-v11.18` | Neues Installationsziel fuer das signierte Setup 11.18 |

Ein vorhandenes `~/openclaw_ultimate_setup` bleibt erhalten. Wenn du dieses
aktualisieren willst, verwende den [signierten Updatepfad](SIGNED_RELEASES.md#standard-update)
statt einer Neuinstallation. Kein Ordner und keine Benutzerdaten muessen geloescht werden.

## 2. Ubuntu-Terminal oeffnen und Werkzeuge pruefen

Dein Prompt `ubuntu@Letsung-MiniPC1:~/openclaw_ultimate_setup$` ist bereits
richtig: **Bash unter Ubuntu**. Unter Windows das Ubuntu-/WSL-Terminal oeffnen,
nicht PowerShell. Auf einem Linux-Rechner oder nach SSH dieselben Bash-Bloecke verwenden.
Nicht als root arbeiten. Du kannst im jetzigen Ordner bleiben; die Ziele sind absolute Home-Pfade.

```bash
command -v bash git python3 curl tar minisign
```

Erwartet: Fuer jedes Werkzeug erscheint ein Pfad. Wenn etwas fehlt, auf
Ubuntu/Debian bewusst die benoetigten System-/Pruefwerkzeuge einrichten:

```bash
sudo apt-get update && sudo apt-get install --no-install-recommends bash git python3 curl tar minisign
```

Danach den ersten Pruefbefehl wiederholen. APT ist hier die dokumentierte
System-/Pruefwerkzeug-Ausnahme, keine Docker- oder Tool-Fallback-Installation.

## 3. Repository von GitHub klonen

### Ubuntu, Linux und WSL: Bash

Diesen ganzen Block einmal kopieren. Er startet **keinen Installer**:

```bash
(
  set -euo pipefail
  target="$HOME/OpenClaw-Quellpruefung"
  if [ -e "$target" ] || [ -L "$target" ]; then
    printf '%s\n' 'Ziel existiert bereits. Nicht loeschen; anderen neuen Zielnamen waehlen.' >&2
    exit 1
  fi
  git -c core.hooksPath=/dev/null clone --template= --no-checkout --no-recurse-submodules https://github.com/dwhr-pi/OpenClaw-AI_Infrastructure-_Ultimate_Setup.git "$target"
  git -C "$target" log -1 --format="%H %s"
)
```

Erwartet: Git meldet den Clone und zeigt danach einen langen Commit-Hash samt
Kurzbeschreibung. Das sind heruntergeladene Git-Objekte, noch keine gepruefte
Installation. Der angezeigte neueste Commit ist nicht automatisch vertrauenswuerdig.

Bei "Ziel existiert bereits" stoppen. Entweder den vorhandenen Clone bewusst
pruefen oder einen anderen neuen Namen waehlen und die folgenden Pfade entsprechend
anpassen. Kein `reset`, `clean` oder Loeschen erforderlich.

## 4. In den heruntergeladenen Ordner wechseln

```bash
cd "$HOME/OpenClaw-Quellpruefung" && pwd
```

Bei deinem Ubuntu-Benutzer lautet die Ausgabe normalerweise
`/home/ubuntu/OpenClaw-Quellpruefung`. Dass dort noch keine normalen
Projektdateien liegen, ist gewollt: `--no-checkout` hat sie noch nicht ausgecheckt.
Dein bisheriger Setup-Ordner wurde nicht veraendert.

## 5. Einen unabhaengig geprueften Quellstand auschecken

Lass dir den **vollstaendigen geprueften 40-stelligen Commit fuer den
11.18-Bootstrap** vom Maintainer ueber einen bereits vertrauenswuerdigen Kanal
bestaetigen. Nicht einfach den zuletzt angezeigten Hash als geprueft ausgeben.
Maintainer bedeutet die Person, die Repository und Releases freigibt. Bei
deinem eigenen Repository bist du das selbst: Der Hash muss aus deiner
dokumentierten Quellpruefung/Freigabe stammen, nicht nur aus der Clone-Ausgabe.
Wenn kein solcher Commit vorliegt, hier stoppen. Keine Skripte aus einem
ungeprueften Download ausfuehren.

Der folgende Block fragt nach diesem Commit. Er startet weiterhin kein Setup:

```bash
(
  set -euo pipefail
  cd "$HOME/OpenClaw-Quellpruefung"
  read -r -p 'Unabhaengig geprueften vollstaendigen 11.18-Commit eingeben: ' pin
  [[ "$pin" =~ ^[0-9a-f]{40}$ ]] || { printf '%s\n' 'Ungueltiger Commit; Abbruch.' >&2; exit 1; }
  env -i PATH="$PATH" HOME="$HOME" GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NOREPLACE_OBJECTS=1 GIT_LFS_SKIP_SMUDGE=1 git -c core.hooksPath=/dev/null -c core.fsmonitor=false checkout --detach "$pin"
  test "$(git rev-parse HEAD)" = "$pin"
  test -f verify_release_and_install.sh
  test -f scripts/security/import_release_public_key.py
  grep -qx 'APP_VERSION="11.18"' setup_ultimate.sh
  printf '%s\n' 'Gepruefter 11.18-Quellstand bereit. Noch kein Installer gestartet.'
)
```

Jetzt sind die Projektdateien sichtbar. "Detached HEAD" ist bei einem bewusst
gepinnten Commit normal. Ein fehlender Commit wird nicht durch `main`, einen
anderen Branch oder einen alten Release ersetzt.

## 6. release.pub importieren und Fingerprint bestaetigen

Du brauchst nur den **oeffentlichen** Schluessel `release.pub`, niemals
`release.key` oder dessen Passwort. Schluessel und SHA256-Fingerprint getrennt
vom Release-Download ueber einen vertrauenswuerdigen Maintainer-Kanal beziehen.
Ein selbst berechneter Hash einer unbekannten Datei beweist noch keine Herkunft.

Im jetzt geprueften Checkout ausfuehren:

```bash
cd "$HOME/OpenClaw-Quellpruefung" && python3 -I -B scripts/security/import_release_public_key.py --interactive --apply
```

Der Helfer fragt nacheinander:

1. **Genauer absoluter Pfad zur release.pub:** einen vorhandenen Dateipfad eingeben.
2. **Unabhaengig bestaetigter SHA256:** den separat bestaetigten 64-stelligen Fingerprint eingeben.

| Wo liegt deine Public-Key-Datei? | Eingabe im Ubuntu-Terminal |
| --- | --- |
| Windows-Datei, Zugriff aus WSL | `/mnt/c/Users/DEIN_WINDOWS_NAME/Documents/OpenClaw-Vertrauensschluessel/release.pub` |
| Bereits im Linux-Home abgelegt | `/home/ubuntu/OpenClaw-Vertrauensschluessel/release.pub` |

Den tatsaechlichen Pfad einsetzen; dies sind Beispiele. Unter nativem Linux
existiert `/mnt/c` normalerweise nicht. In WSL ist das `c` klein. Kein
`C:\...` und kein `$HOME` als wortwoertliche Pfadeingabe im Helfer verwenden.

Erwartet: "Public Key bytegleich importiert" oder "Bereits bytegleich vorhanden".
Das Ziel ist `~/.config/openclaw-trust/release.pub`. Die Quelle bleibt unveraendert.
Ein anderes vorhandenes Ziel wird nicht ueberschrieben. Bei Fehlern stoppen,
nicht die Pruefung abschalten. [Schluesselhandhabung und Rotation](MINISIGN_KEY_HANDLING.md).

### Wenn Python den Importhelfer nicht findet

Bei `can't open file .../scripts/security/import_release_public_key.py` ist
der Helfer in diesem Checkout nicht vorhanden. Insbesondere im alten Tag
`v11.17.0` fehlt er. Eine neue Anleitung aktualisiert nicht automatisch die
Dateien auf deinem Ubuntu-Rechner. Nicht blind `main` nachladen oder einen
ungeprueften Helfer starten; erst den richtigen geprueften Checkout aus Schritt 5 verwenden.

Der Import ist nicht zwingend: Ein bereits unabhaengig bestaetigter Public Key
kann auch direkt von seinem vorhandenen Windows-/WSL-Pfad gelesen werden.
Den absoluten Pfad anpassen:

```bash
key='/ABSOLUTER/PFAD/ZUR/release.pub'
test -f "$key" && test ! -L "$key" && sha256sum "$key"
```

Das kopiert, loescht und ueberschreibt nichts. Beim Release-Pruefer dann
`--public-key "$key"` statt des Import-Zielpfads verwenden. Die unabhaengige
Fingerprint-Pruefung und die Release-Voraussetzung aus Schritt 7 bleiben erforderlich.

### Git-Commit und Public-Key-Fingerprint unterscheiden

| Wert | Laenge | Verwendung |
| --- | --- | --- |
| Git-Commit wie `8164d68fce1700fa2de4e69baf402da4878dcc13` | 40 Hex-Zeichen | Geprueften Quellstand identifizieren, nicht `--expected-sha256` |
| SHA256 der Datei `release.pub` | 64 Hex-Zeichen | `--expected-sha256`, separat bestaetigen |

`sha256sum "$key"` zeigt den Datei-Fingerprint, nicht den Commit.
Nicht den Hash von `install.sh`, `release.json` oder `SHA256SUMS` einsetzen.
Eine passende Laenge allein beweist noch nicht, dass der Schluessel vertrauenswuerdig ist.

## 7. Veroeffentlichung von v11.18.0 kontrollieren

Oeffne die [GitHub-Releases](https://github.com/dwhr-pi/OpenClaw-AI_Infrastructure-_Ultimate_Setup/releases)
und suche **`v11.18.0`**, nicht nur den Hinweis "Latest". Dazu muessen diese
vier vom Maintainer hochgeladenen Assets gehoeren:

- `install.sh`
- `release.json`
- `SHA256SUMS`
- `SHA256SUMS.minisig`

Die automatisch erzeugten Source-code-Archive reichen nicht aus.
**Solange nur v11.17.0 vorhanden ist, hier stoppen.** Der Maintainer muss
zuerst das neue Release erstellen und signieren. Ein Tag allein reicht nicht.

## 8. Signiertes Release herunterladen und nur pruefen

Erst nach Schritt 7, im Ubuntu-Terminal:

```bash
cd "$HOME/OpenClaw-Quellpruefung" && bash ./verify_release_and_install.sh --tag v11.18.0 --public-key "$HOME/.config/openclaw-trust/release.pub" --download --verify-only
```

Der Pruefer laedt die vier Assets selbst. Du musst sie nicht einzeln im
Browser speichern. Erfolgreich ist die Meldung
"Signatur, SHA256, Tag und Commit geprueft. Kein Clone/Installer gestartet."
Sie bestaetigt Signatur, Integritaet und signierte Metadaten; der echte
Git-Tag-Abgleich erfolgt zusaetzlich beim Installieren. Bei 404, falschem Key
oder Signaturfehler nicht fortfahren und nicht auf einen unsignierten Weg wechseln.

## 9. Bewusst in einen neuen Ordner installieren

Das Ziel darf noch nicht existieren. Fuer dich ist absichtlich ein neuer
Versionsordner vorgesehen, damit `~/openclaw_ultimate_setup` erhalten bleibt:

```bash
cd "$HOME/OpenClaw-Quellpruefung" && bash ./verify_release_and_install.sh --tag v11.18.0 --public-key "$HOME/.config/openclaw-trust/release.pub" --download --install --destination "$HOME/openclaw_ultimate_setup-v11.18"
```

Jetzt werden Assets erneut geprueft, der Release-Tag geklont, dessen Commit und
Installer abgeglichen und erst danach das interaktive Setup geoeffnet.
Der Quellpruefungsordner bleibt davon getrennt. Tool-Installationen sind
bewusste Menueentscheidungen; keine pauschalen Dienst-/Modell-/Clusterstarts.
Ein anderer Checkout isoliert nicht automatisch die gemeinsamen Benutzerdaten
unter `~/.openclaw_ultimate_user_data`. Fuer isolierte Tests eine separate Umgebung verwenden.

## 10. Setup spaeter erneut oeffnen

Nach einer erfolgreichen Installation aus Schritt 9:

```bash
cd "$HOME/openclaw_ultimate_setup-v11.18" && bash ./setup_ultimate.sh
```

Nicht einfach das Setup aus dem Quellpruefungsordner starten und dies als
signierte Installation bezeichnen. Fuer Updates einer bestehenden Installation
gilt weiterhin der gesonderte [Updatepfad](SIGNED_RELEASES.md#standard-update).

## Anhang: Windows-Quellansicht und Shell-Unterschiede

### Windows: Nur PowerShell, nicht Ubuntu/WSL

Dieser optionale Block ist nur fuer einen Windows-Prompt wie `PS C:\Users\DEIN_NAME>`.
Er ersetzt nicht die Ubuntu-Schritte und installiert das Linux-Setup nicht auf Windows:

```powershell
$target = Join-Path $HOME 'OpenClaw-Quellpruefung'
if (Test-Path -LiteralPath $target) { throw 'Ziel existiert bereits; anderen neuen Zielnamen waehlen.' }
git -c core.hooksPath=NUL clone --template= --no-checkout --no-recurse-submodules https://github.com/dwhr-pi/OpenClaw-AI_Infrastructure-_Ultimate_Setup.git $target
if ($LASTEXITCODE -ne 0) { throw 'Clone fehlgeschlagen. Nicht fortfahren.' }
git -C $target log -1 --format="%H %s"
```

PowerShell-Backticks sind keine Bash-Zeilenfortsetzungen: Bash interpretiert
sie als Befehlsersetzung und versucht dann gegebenenfalls eine URL auszufuehren.
Bash verwendet `/dev/null`, Windows PowerShell `NUL`. Die Hauptanleitung
verwendet deshalb einzeilige Aufrufe ohne Zeilenfortsetzungen. Bestehende
Windows-Repositories, WSL-Checkouts und Benutzerdaten nicht loeschen.
