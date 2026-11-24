# VPS-Anbieter und begrenzter Provideradapter

Stand: 18.11.2026. **Lokale Implementierung mit Offline-Tests, keine Live-Abnahme.**
Kontoregistrierung, Ressourcenbuchung, vorhandener Host und Clusterbeitritt sind getrennte Schritte.
Die [Quellenreview](vps/PROVIDER_REVIEW_2026_11_18.md) behandelt Anbieter, Bedingungen und Lernmaterial.

## Faehigkeiten und Herkunft

| Pfad | Implementiert | Noch offen / gesperrt |
| --- | --- | --- |
| Free-VPS | Offlineimport aller 56 Angebote, Originalfelder, Dateihash und Herkunft | Originalpruefung aller Dimensionen; keine pauschale Nutzungsfreigabe |
| GCP, vorhandene VM | Offizieller GET, Besitz-/ID-/SKU-Pruefung, gepinntes SSH, Ansiblepfad hinter Autorisierung | Konto, konkrete Zielverifikation und echte API-/SSH-/Ansible-Abnahme |
| OCI und Hetzner | Anbieterreview und Katalogdaten | Kein operativer Provideradapter |
| Kontoeroeffnung | Menschliche Schritte und ungepruefte Bedingungen dokumentiert | Keine automatische Registrierung oder CAPTCHA-/KYC-Umgehung |
| `provision` | Validierter Vertrag und Sperrentscheidung | Keine VM-Buchung, auch mit `--apply`; harter Gesamt-Kosten-/Laufzeitdeckel fehlt |
| `teardown` | Nicht destruktive Vorschau | Kein Loeschen, Stoppen oder destruktiver Recoverypfad |
| K3s / WireGuard | Getrennte bestehende Setupwege und Abnahmekriterien | Kein automatischer Join, Modell-, Mining-, Handels- oder Walletstart |

Die [CLI](../scripts/vps_adapter.py) verwendet den separaten [Adapter](../tools/vps/adapter.py),
keine generische LLM-Shell oder Browserregistrierung. [Automaton](tools/automaton.md) bleibt unveraendert
gesperrt fuer Runtime, Init und Provision; Offlinepruefer und Policydatei sind keine Ausfuehrungsbruecke.
[GitOps](GITOPS_SMALL_VPS.md) und [signierte Releases](INSTALL_SIGNED_RELEASE.md) bleiben getrennt.

| Provenienz | Nachweis |
| --- | --- |
| Hauptrepo-Basis | `aae010c57a3afd675b278790d8e371019c047492`; neue Arbeit lokal und uncommittiert |
| Erste Free-VPS-Lesung | HEAD `e94cb8af66592c5fcc6e7b4895b614a81b1e8a90`; bestehende lokale Aenderungen erhalten |
| Spaetere Free-VPS-Lesung | HEAD `1a77fa567d69633a998b702b1d7208a8d8a1cfb3`; Quelle extern weiterentwickelt |
| Importierte Quelldatei | SHA256 `95efce946dfc20c890cf771906128d5a5c5ec93e09bcd58c482baa33a6c62bbd` |
| Snapshot | [catalog-2026-11-18.json](vps/catalog-2026-11-18.json), 56 Angebote, Importzeit im Dokument |

Der Snapshot nennt den zuerst erfassten Basis-HEAD; der Dateihash identifiziert seine importierten Bytes.
Ein HEAD beweist keinen sauberen Quellbaum. `source.head` ist gelieferte Provenienz, keine Signatur.
Vor Folgeimporten HEAD, Dirty-Status und Dateihash neu erfassen. Free-VPS wurde hier nicht veraendert.

## Offline verwenden

Ab dem Repositoryverzeichnis, ohne Netz-/Token-/SSH-Zugriff:

```text
python3 -I -B scripts/vps_adapter.py plan --plan examples/vps/gcp-existing.plan.json --catalog docs/vps/catalog-2026-11-18.json
```

Unter Windows gegebenenfalls den vorhandenen Pythonaufruf statt `python3` verwenden.
Die [Vorlagen](../examples/vps/README.md) enthalten ausschliesslich inaktive Testdaten:
Nullpreise, Dokumentations-IP und Nullschluessel sind keine echten Preise oder Vertrauensanker.
Der Beispielplan hat keine Nutzungs-/Konto-/Hostfreigabe und wird nach sieben Tagen als veraltet abgelehnt.

Eigener spaeterer Import in eine noch nicht existierende Ausgabedatei:

```text
python3 -I -B scripts/vps_adapter.py catalog --source QUELLDATEI --source-head GELESENER_HEAD --output NEUE_SNAPSHOTDATEI
```

Quelle ist die lokale `Free-VPS/data/anbieter-de.json`; Ausgabe ins Hauptrepo oder eigenen Pruefbereich,
niemals ins Schwesterrepository. Kein Ueberschreiben, keine Quellskriptausfuehrung.
Der [Importer](../tools/vps/catalog.py) begrenzt JSON auf 4 MiB und verwirft doppelte Schluessel/IDs,
nichtendliche Zahlen und ungueltige Datierungen. Alle Originalfelder bleiben unter `source_fields` erhalten.

`kind` unterscheidet VMs, Systemcontainer, App-Hosting, CI, Trials, Rueckerstattung, Brokerfinanzierung,
historische und ungepruefte Angebote. Dimensionen enthalten Quellenangaben oder `null`; alle bleiben
`unverified`. `retrieved_at` ist der lokale Import, `source_claimed_reviewed_on` die Quelldatierung,
`content_reviewed_at: null` behauptet keinen eigenen Anbieterreview. Die Markdownreview ist separat.

## Plan, Konto und Freigabe

Pflichtfelder sind Provider, Konto, Region/Zone, vorhandene Ressourcen-ID, SKU, OS-Image, Architektur,
Nutzung, Besitzer, Preisbestandteile, Budget/Laufzeit, SSH-Referenzen und Bootstrap-SHA256.
Unbekannte Felder/Preise werden nicht stillschweigend akzeptiert. Geldwerte sind Dezimalzeichenketten;
Standardvorlage: Budget null. Gesamtschaetzung: `hourly * hours + setup + extras + tax`.
IP, Egress, Backups, Steuer und alle Zusatzressourcen muessen in der geprueften Kalkulation enthalten sein.
Eine eingetragene Null beweist keine Kostenfreiheit; Schaetzung darf das Budget nicht ueberschreiten.

Preis-/AUP-Review muss hoechstens sieben Tage alt sein; Quellenfelder sind Betreiberangaben, kein
automatischer Vertragsnachweis. Einsatzzwecke trennen Monitoring, KI-Client/Inferenz/Training, Mining,
Krypto-Nodes/Validatoren, privates Trading, oeffentliche Plattform und gewerbliche Nutzung.
`unverified`/`forbidden` blockiert `configure` fuer diesen Plan, nicht die Dokumentationsarbeit.
Alle operativen Aktionen verlangen ein bereits legitim eingerichtetes Konto (`existing_account_required`).
Andere Registrierungszustaende halten vor Tokenzugriff an.

Die externe Autorisierungsdatei bindet Planhash, Aktionen, Start/Ende, Budget, Stunden und genau eine
Ressource; maximal sieben Tage gueltig. Noch gueltige Freigaben koennen fuer idempotente Folgelaeufe
wiederverwendet werden. Planaenderung verlangt eine neue Hashfreigabe. Auf POSIX: Eigentuemer und exakt
`0600`, ausserhalb des Repos, keine Links/Reparse-Pfade. Das ist keine minisign-Signatur oder Cloudkostensperre.

Operative Aufrufe brauchen zusaetzlich `--apply --authorization DATEI`; `configure` braucht auch
`--state-dir EXTERNES_PRIVATES_VERZEICHNIS`. Ohne `--apply` keine API-/SSH-Verbindung.
Fehlerausgaben geben keine Argumentwerte, Tokens oder Providerantworten aus.

**Buchung bleibt gesperrt:** GCP-SpendCaps existieren fuer bestimmte API-Dienste, stoppen aber laufende
Compute-/Storagekosten nicht allgemein. Warnbudget, ablaufendes Token oder SSH-Timer ist kein harter
VM-Gesamtkostendeckel. `provision --apply` stoppt vor Tokenzugriff, auch bei Budget null.
Bereits laufende Kontokosten werden dadurch nicht limitiert.
[Offizielle Grenzen](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps).

## Vorhandenen GCP-Host einrichten

1. Konto, Identitaet, Land/Zahlungsmittel und AUP legitim klaeren; keine Signup-API unterstellen.
2. Vorhandene konkrete Instanz und Gesamtkosten freigeben. Token auf den benoetigten Compute-Lesezugriff
   begrenzen; keine Admin-/Billing-/Wallet-Schluessel bereitstellen.
3. Labels `openclaw-owner` und `openclaw-plan` bewusst beim Provider setzen: Letzteres sind die ersten
   32 Zeichen des freigegebenen Planhashs. Der Adapter setzt keine Providerlabels.
4. Hostfingerprint unabhaengig per Providerkonsole pruefen. Eigene Known-Hosts-Datei nur mit exaktem
   IP-/Ed25519-Eintrag, ohne Wildcards, CA-Regeln oder zusaetzliche Schluessel vorbereiten.
5. Zwei getrennte administrative SSH-Zugaenge mit getrennten Schluesseldateien extern testen.
   Unterschiedliche Dateien allein beweisen keine kryptografisch verschiedenen Schluessel.
6. Externen Plan/Freigabe, Backup, Rettungszugang und frischen dedizierten Host bewusst bestaetigen.
7. Fuer genau diesen Auftrag erst `status`, dann `verify`, zuletzt `configure` autorisieren.

`OPENCLAW_VPS_...`-Referenzen fuer SSH und Known Hosts enthalten externe absolute Dateipfade;
`api_token_env` benennt dagegen die Umgebungsvariable mit dem Bearer-Token, keinen Dateipfad.
Keine Geheimnisse in Plan, Prompt oder Logs. Hier wurden keine realen Zugangsdaten verwendet.

GET ist auf `compute.googleapis.com` und Projekt/Zone/Instanz beschraenkt; ID, Besitzer und SKU werden
geprueft. Maximal zwei Versuche mit kleinem Backoff und begrenztem Zeitbudget; keine Redirects oder Buchungen.
Vertrag: [offizielles Compute-REST-GET](https://docs.cloud.google.com/compute/docs/reference/rest/v1/instances/get).
SSH prueft die zur Instanz gehoerende IP, striktes Pinning, Batchmodus und deaktivierten Agent/Fallback.
Linux-/Architektur-, CPU-/RAM-/Disk- und cgroups/TUN-Metadaten sind keine Bootimage-, KVM-, VPN-,
Neustart- oder Restore-Abnahme. Plan-`os_image` beweist das tatsaechliche Bootimage nicht.

## Konfiguration und Datenerhalt

`configure` verlangt POSIX-Controller, vorhandene Ansible-Collections und passenden Bootstrap-Dateihash.
Kein automatischer Collection-/Toolchaindownload. Der [bestehende Bootstrap](../ansible/vps_bootstrap.yml)
unterstuetzt dedizierte Ubuntu-22.04-/24.04-Hosts, **nicht pauschal Ubuntu 26.04 oder alle Debian-Derivate**.
Er installiert kein Docker. Bestehende Container/Volumes und Daten werden nicht entfernt.

Vor erstem Apply muss `llmops` nachweislich noch fehlen: Der Bootstrap verwaltet Servicegruppen und
Keys exklusiv. Ein bestehender Serviceaccount ist ein Migrationsfall, keine automatische Uebernahme.
Ablauf: Ansible-Check, Apply, weiterer Check mit null Aenderungen und erneutes SSH/Recovery.
Dies ist durch Fixtures, **nicht auf einem realen frischen Host**, geprueft. Insbesondere Checkmodus
bei neuer Benutzeranlage, Collectionversionen, Paketupdates und sshd/UFW brauchen noch eine reale Abnahme.
Bei Checkfehlern kein ungepruefter Apply-Fallback.

Globale SSH-/Firewallaenderungen und SSH-Reload sind moeglich; kein seiteneffektfreier Diagnosepfad.
Kein automatisches Rollback von Paket-/SSH-/Firewallaenderungen. Ein Fehler nach Apply kann einen
bereits veraenderten Host hinterlassen; extern getestete Rettungswege bleiben notwendig.

Privates Journal und Lock erfassen `intent` vor Apply, `configured` erst nach Nachpruefung.
Erfolgreiche Wiederholung prueft erneut, wendet aber nicht blind erneut an. Unvollstaendiges Journal,
fremder Plan oder verbliebener Lock blockiert; nicht zum Umgehen loeschen. Bestandsklaerung statt
destruktivem Rollback. Journal ist kein Backup und kein vollstaendiges Pakettransaktionslog.

`k3s_join_allowed` bleibt false. Vor separatem Join CPU/RAM/SSD, Kernelrechte/cgroups, Architektur,
WireGuard/NAT/UDP, MTU/CNI, privaten API-Zugang und Latenz praktisch pruefen. Keine 192-MB-Container oder
CI-Jobs als Control Plane und keine globale etcd-Mehrheitsgruppe ueber unzuverlaessige Gratisnodes.
Lokale GPU-Worker fuer Modelle bevorzugen.

## Wochenpflege und offene Abnahmen

[Wochenprompt](vps/WEEKLY_REVIEW_PROMPT.md) vorbereitet, **neuer Hauptrepo-Job nicht aktiviert**:
Das Automationstool meldete Nichtverfuegbarkeit. Dienstag 09:30 `Europe/Berlin` ist nur vorgeschlagen.
Bestehender API-Heartbeat Montag 09:00 wurde in seiner Automation gelesen. Der separate Windowsjob
`Free-VPS-Wochenpflege` ist im vorhandenen Statusbericht fuer Montag 09:00 als Ready dokumentiert.
Das beweist noch keinen semantischen Wochenlauf. Beide bestehenden Auftraege blieben unveraendert.

Kuenftige Hauptrepo-Recherche liest Free-VPS nur und pflegt Berichte; sie darf keine Adapter-, Policy-
oder Betriebsfreigaben erweitern. Keine Doppeljobs, Konto-/API-/SSH-/Clusteraktionen oder Veroeffentlichung.

Offline-Tests: `test_vps_catalog.py`, `test_vps_adapter.py`, `test_vps_cli.py`.
[CI](../.github/workflows/vps-adapter.yml) fuehrt nur diese Fixtures aus. POSIX-/Symlink-Tests muessen
auf Linux/macOS separat bestaetigt werden. Kein Provider gebucht, kein signiertes Release veraendert,
kein Commit/Push. Reale Konto-, API-, SSH-, Ansible-, Reboot-, VPN- und Restoretests bleiben offen.

Pflichtquellen: [Free-VPS](https://github.com/dwhr-pi/Free-VPS),
[github-vps](https://github.com/dwhr-pi/github-vps) und
[FreeVPS_by_Github-Action](https://github.com/dwhr-pi/FreeVPS_by_Github-Action).
Actions/Codespaces sind begrenzte Entwicklungs-/CI-Umgebungen, keine allgemeinen Dauer-VPS;
kein Mining, Keepalive, Kontenrotation oder Quotenvervielfachung. Originalbedingungen siehe Quellenreview.
