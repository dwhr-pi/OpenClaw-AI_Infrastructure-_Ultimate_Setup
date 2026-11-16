# Nur signierte Setup-Updates

## Automatische Startpruefung

Bei jedem interaktiven Start oder Neustart von `setup_ultimate.sh` wird einmal nach Updates gesucht.
Die Online-Startpruefung ist auf 20 Sekunden begrenzt; der Prozessabbruch darf weitere drei Sekunden brauchen.
Sie **installiert nichts** und startet
keine Dienste, Modelle oder Cluster. Offline-/Headless-Optionen wie `--dry-run`, `--tools-json`
und `--tool-plan` fuehren diese Netzwerkpruefung nicht aus.

Ein neueres Release wird erst als signiertes Update gemeldet, nachdem Minisign und SHA256 mit
dem separat bereitgestellten lokalen Vertrauensschluessel erfolgreich geprueft wurden.
Bei fehlendem Schluessel, fehlendem Minisign, Netzwerk- oder Signaturfehler erscheint ein Hinweis;
das Menue bleibt nutzbar. Ein Fehler bedeutet **nicht**, dass der Stand aktuell ist.

Standardpfad fuer den bereits unabhaengig geprueften oeffentlichen Schluessel:

```text
~/.config/openclaw-trust/release.pub
```

Alternativer vorhandener Pfad, vor dem Start im selben Terminal gesetzt:

```bash
export OPENCLAW_RELEASE_PUBLIC_KEY='/absoluter/pfad/zur/release.pub'
bash ./setup_ultimate.sh
```

Der Schluessel wird nur gelesen, nicht geloescht, ersetzt oder aus einem Release importiert.
Der private `release.key` wird fuer Updates **niemals** benoetigt.
Windows-/WSL-Import: [vollstaendige Installationsanleitung](INSTALL_SIGNED_RELEASE.md).

Fuer einen bewusst netzwerkfreien Start:

```bash
OPENCLAW_UPDATE_CHECK=0 bash ./setup_ultimate.sh
```

## Pruefen und Aktualisieren

Im geprueften Setup-Verzeichnis zuerst nur pruefen:

```bash
bash scripts/check_setup_updates.sh
```

Erst bewusst aktualisieren, ueber das Optionen-Menue oder diesen Befehl:

```bash
bash scripts/update_setup_only.sh
```

Der Updatebefehl sucht erneut und prueft erneut; eine fruehere Startmeldung ersetzt keine
erneute Signaturpruefung. Lokale Aenderungen blockieren die Uebernahme. Vor Git-Fetch/Checkout
wird die vorhandene verifizierte Repository-Sicherung erstellt. Es gibt kein Force-Checkout,
keinen Dienstneustart und keine Loeschung von `~/.openclaw_ultimate_user_data`.
Ein Checkout ist keine Runtime-/Migrationsabnahme installierter Tools.

## Auswahl und Sicherheitsgrenzen

1. Die Suche liest hoechstens 100 aktuelle GitHub-Release-Datensaetze, nicht beliebige Branches.
2. Nur stabile `vX.Y.Z`-Tags sind Kandidaten; Drafts und Pre-Releases werden nicht ausgewaehlt.
3. Fehlt eines der vier Artefakte `install.sh`, `release.json`, `SHA256SUMS`, `SHA256SUMS.minisig`,
   wird das Release als unvollstaendig gemeldet und nicht uebernommen.
4. Der numerisch hoechste vollstaendige Kandidat wird heruntergeladen und kryptografisch geprueft.
   Fehlende oder ungueltige Signatur, falscher Hash, Tag oder Repository-Vertrag fuehren zum Abbruch.
   Bei einer ungueltigen Signatur wird nicht auf einen anderen Kandidaten ausgewichen.
5. Nur eine hoehere Version als die lokale Setup-Version bzw. der exakte lokale Release-Tag wird
   automatisch ausgewaehlt. Gleiche Version mit anderem Commit und aeltere Version bleiben unberuehrt.
6. `main` dient nur der Information. Abweichender Code ist kein Update und wird nie als Ersatz geladen.
   Die Meldung bedeutet nicht, dass jeder einzelne Git-Commit auf `main` unsigniert sein muss.

GitHub-Labels wie Latest/Verified und vorhandene Signaturdateien sind allein kein Vertrauensnachweis.
Vertrauensanker ist ausschliesslich die unabhaengig gepruefte lokale `release.pub`.
Die Signatur bestaetigt Herkunft/Integritaet, nicht Fehlerfreiheit, Aktualitaet der GitHub-Liste oder
eine vollstaendige Supply-Chain-Abnahme. Die begrenzte Liste und Netzfehler erlauben keine Aussage
ueber versteckte/aeltere Releases oder absolute Update-Frische. Ein bewusst gewaehlter manueller
Release-Tag bleibt ein eigener Verwaltungsweg, kein automatisch downgradegeschuetzter Kanal.

Die Suche setzt HTTPS, kleine Antworten, begrenzte Laufzeiten und offizielle GitHub-Downloadziele voraus.
API-Asset-URLs werden nicht ausgefuehrt oder als beliebige Downloadziele uebernommen.
Private GitHub-Repositories und Unternehmens-Proxys mit Authentifizierung sind hier nicht abgenommen.

## Vorhandene explizite Release-Auswahl

Sind `OPENCLAW_RELEASE_TAG` und `OPENCLAW_RELEASE_ARTIFACTS` gesetzt, bleibt die vorhandene explizite
Auswahl aktiv. Fuer automatische Suche diese beiden Variablen nicht setzen bzw. bewusst entfernen.
Nur eine der beiden Variablen zu setzen fuehrt zum Abbruch, nicht zur stillen Auswahl eines anderen Tags.
`OPENCLAW_RELEASE_PUBLIC_KEY` kann in beiden Wegen verwendet werden.

[Manueller signierter Updatepfad](SIGNED_RELEASES.md#standard-update).
Die historische Entwickler-Quellreparatur bleibt ein expliziter separater CLI-Weg und ist kein signiertes
Update. Sie wird im interaktiven Standardmenue nicht mehr ausgefuehrt. Keine automatische Reparatur
auf `main`, kein unsignierter Fallback und keine Neu-Signierung bestehender Releases.

## Testnachweise

`tests/test_signed_update_discovery.py` prueft Auswahl, Versionsgrenzen, fehlende/ungueltige Signaturen,
fremde Ziele, fehlende Vertrauensschluessel und den Startpruefungs-Timeout mit Offline-Fixtures.
Die HTTP-/Minisign-/Checkout-Aktionen werden dabei gemockt. Das ist kein echter GitHub-Download,
keine kryptografische Abnahme und kein produktiver Update-/Restore-Test.
