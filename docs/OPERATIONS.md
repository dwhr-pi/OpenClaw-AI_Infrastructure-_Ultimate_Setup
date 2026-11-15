# Betrieb: Update, Wiederherstellung und Stoerungen

## Entwicklungsbranch und Release

Im Entwicklungscheckout zuerst `git status --short --branch` pruefen.
Den eigenen geprueften Arbeitsbranch fuer Entwicklung und Offline-Tests
beibehalten; keinen Branch nur wegen der Versionsnummer wechseln.
Aktueller Setup-Stand ist 11.18, Release-Ziel `v11.18.0`.
Der Menuepunkt Setup-Update ist kein Branch-Wechsel: Fuer
produktive Updates den [signierten Release-Pfad](SIGNED_RELEASES.md)
verwenden. Ein neues 11.18-Release braucht einen neuen versionierten
Tag und eine neue Signatur, nicht zwingend einen neuen Minisign-Schluessel.
Die veroeffentlichten 11.17.0-Dateien nicht ueberschreiben.
Die [neue Installationsanleitung](INSTALL_SIGNED_RELEASE.md) fuehrt Schritt fuer
Schritt durch Clone, Quellpruefung und Installation. Vorher die
[Veroeffentlichungs-Checkliste](releases/v11.18.0.md) abschliessen.

## Backup, Restore und Schluessel

Vor Updates Checkout, Tool-Zustand und Datenbanken getrennt sichern.
Backups verschluesselt und offsite ablegen; Restore in einem getrennten
Ziel testen. Die [Backup-Strategie](BACKUP_RESTORE_STRATEGY.md) und
[Schluesselhandhabung](MINISIGN_KEY_HANDLING.md) unterscheiden State,
Secrets und wiederbeschaffbare Modellcaches. Pro Dienst ein erwartetes
RPO/RTO vereinbaren und im Drill messen, keine pauschale Zusage.

## Stoerungsablauf

| Symptom | Erste Pruefung | Sichere Reaktion |
| --- | --- | --- |
| Pi offline | Strom, lokaler Reachability-Check, WoL-Relay | Kein unkontrolliertes Retry; Inferenz als nicht verfuegbar melden |
| GPU-Worker offline | Wake-Zustand, K3s-Node, Runtime und GPU | Queue begrenzen; kein stiller Cloud-Fallback |
| WireGuard unterbrochen | Beide Tunnel-Enden und private Routen pruefen | Keine privaten Ports als Ersatz oeffentlich oeffnen |
| Platte voll | Speicherort und Volumes, Modellcache gegen State abgrenzen | Erst Backup und Owner pruefen, nicht automatisch loeschen |
| Datenbank oder State fehlerhaft | Letzten konsistenten Backup-Stand feststellen | Getrennt wiederherstellen und erst nach Abnahme umschalten |

[Monitoring und GPU-Betrieb](LLMOPS_GPU_AND_OPERATIONS.md) sowie
[manuelle GitOps-Freigabe](GITOPS_DEPLOYMENT_PATH.md) weiterverwenden.
Keine Dienste, Timer oder Container allein durch diese Dokumentation
installieren oder starten.
