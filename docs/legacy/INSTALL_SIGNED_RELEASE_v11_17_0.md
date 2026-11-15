# Historie: signiertes Release v11.17.0

Dieses Dokument beschreibt das bisher veroeffentlichte
[Release v11.17.0](https://github.com/dwhr-pi/OpenClaw-AI_Infrastructure-_Ultimate_Setup/releases/tag/v11.17.0).
Es ist kein Installationsweg fuer Setup 11.18 und kein automatischer Fallback.
Die [aktuelle Anleitung](../INSTALL_SIGNED_RELEASE.md) zielt auf `v11.18.0`.

## Historischer Vertrauensstand

Der damalige Bootstrap-/Release-Commit lautet
`8164d68fce1700fa2de4e69baf402da4878dcc13`. Ein alter, hier dokumentierter Hash
ersetzt keine unabhaengige Vertrauenspruefung. Die vier veroeffentlichten Assets
sind `install.sh`, `release.json`, `SHA256SUMS` und `SHA256SUMS.minisig`.
Der oeffentliche Download wurde im Chat unter Ubuntu/WSL erfolgreich verifiziert;
eine vollstaendige Fresh-Host- oder Produktionsabnahme wurde damit nicht belegt.

## Bisheriger Pruefaufruf

Nur mit einem unabhaengig geprueften alten Bootstrap und separat bestaetigtem
Public Key. Pfade ersetzen; die Quelle des Public Keys wird nur gelesen:

```bash
bash /ABSOLUT/GEPRUEFTER-BOOTSTRAP/verify_release_and_install.sh --tag v11.17.0 --public-key /ABSOLUT/VERTRAUENSWUERDIG/release.pub --download --verify-only
```

Unter WSL kann der Public Key direkt ueber einen bestaetigten Pfad unter
`/mnt/c/Users/.../release.pub` gelesen werden. Eine Kopie war nicht zwingend
erforderlich. Die neuen Projektbrief-/Key-Import-Helfer fehlen in diesem alten Tag.

## Nicht nachtraeglich umetikettieren

Tag, Commit und Assets dieses Releases bleiben zusammen. Keine Aenderung von
`release.json` auf `v11.18.0`, keine Wiederverwendung seiner Signatur fuer neue
Dateien und kein Ersetzen bereits verteilter Assets. Setup 11.18 braucht einen
neuen Tag, neue Artefakte und eine neue Signatur; siehe
[Release-Checkliste](../releases/v11.18.0.md) und
[Schluesselhandhabung](../MINISIGN_KEY_HANDLING.md).
