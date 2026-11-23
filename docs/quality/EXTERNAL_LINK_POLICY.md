# Externe Markdown-Links: Policy und PR-6-Befunde

Stand: 31.10.2026. Keine Merge- oder Produktionsfreigabe.

## PR 31: Generator-Korrektur vom 23.11.2026

Der Quellen-Auditgenerator erzeugte erneut aktive Repository-Links aus historischen,
bereits als Code dokumentierten Originaladressen und Beispiel-Platzhaltern.
Das erzeugte elf HTTP-404-Fehler im generierten Bericht. Alle erkannten Repositorynamen
und Fundstellen bleiben im Inventar, aber ausschliesslich in Code genannte Adressen
werden nicht mehr zu neuen Live-Links aufgewertet. Eine aktive Prosa-Fundstelle verhindert
diese Code-only-Darstellung; die bestehenden genehmigten Einzelklassifizierungen bleiben erhalten.
Die Herkunftstrennung ist lexikalisch, keine neue Verifikation oder vollstaendiger Markdown-Parser.
Die Originaldokumente bleiben vollstaendig im unveraenderten Link-Gate.

Ein weiterer historischer Commit-Link mit altem Repositorynamen scheiterte mit HTTP 503.
Der korrigierte Link verwendet denselben vollen Commit unter dem kanonischen Namen;
die alte Adresse und der CI-Befund bleiben im Review vom 02.11.2026 erhalten.
[Einzelbefunde, Originaladressen und Pruefgrenzen](CI_PR31_REFERENCE_REVIEW_2026-11-23.json).
Keine neue Quellenfreigabe, Domain-Ausnahme, Status-Aufweichung oder Retry-Erweiterung.

## Folgepruefung 20.11.2026: Prepaid-Hoster HTTP 404

Die beiden Linkchecks zu `f25b7fb` meldeten jeweils genau dieselbe alte Prepaid-Hoster-Testserverseite
mit HTTP 404. Der unabhaengige GET bestaetigt 404; die gelesene offizielle FAQ liefert HTTP 200 und
nennt Testserver nur noch auf Anfrage. Die Anbieteruebersicht verlinkt diese konkrete FAQ, nicht
eine beliebige Startseite. Die alte Adresse und der datierte Befund bleiben dort als Code erhalten.
Historische Sieben-Tage-Werbung aus Suchtreffern ist keine aktuelle Verfuegbarkeitszusage.
[Beide CI-Jobs, Originaladresse, Ersatzbeleg und Grenzen](PREPAID_HOSTER_REFERENCE_2026-11-20.json).
Die zuvor nachgeprueften 18 Adressen haben diese neuen Laeufe bestanden und bleiben aktiv.
Keine neue Ignore-Regel, Quellenpauschalausnahme oder Retry-Erweiterung.

## Nachpruefung 20.11.2026: kanonischer Commit und Abrufsperren

Am Commit `c88ef57` scheiterte der PR-Linkcheck an einem historischen Commit-Link mit dem alten
Repositorynamen (HTTP 503). Der aktive Link nutzt jetzt den gelesenen kanonischen Repositorynamen
und denselben vollstaendigen Commit; die Originaladresse bleibt im datierten Review erhalten.
Kein Ersatz durch `main`, keinen neueren Commit oder eine beliebige Startseite.

Der Push-Linkcheck meldete zehn GitHub-API-Adressen und acht Anbieter-/Medienseiten mit HTTP 403/429.
Alle 18 Originaladressen lieferten beim unabhaengigen Einzel-GET wieder HTTP 200 und bleiben aktive Links.
API-JSON wurde gelesen, YouTube nur auf Seitentitel geprueft. Instagram lieferte eine allgemeine
HTML-Seite: Der Reel-Inhalt bleibt unbestaetigt. Ein erfolgreicher Einzelabruf ist keine nachtraegliche
CI-Abnahme, keine Konditions-/Lizenzpruefung und kein Beweis fuer dauerhafte Erreichbarkeit.
Mangels CI-Antwortheadern ist ein ausgeschoepftes API-Limit nur eine moegliche Ursache, kein Nachweis.
[Alle 19 Einzelbefunde mit Lauf, Job, Fundstelle und Pruefgrenzen](CI_LINK_FOLLOWUP_2026-11-20.json).
Keine neue Quellenumklassifizierung, Ignore-Regel, Statusfreigabe oder Retry-Aenderung.
Die Offline-Regression desselben Commits war bei Push und PR erfolgreich; offen bleibt die erneute CI-Linkpruefung.

## Nachpruefung 19.11.2026: Microsoft- und VPS-Referenzen

Der Linkcheck zu `56964fe` scheiterte an 15 unterschiedlichen Originaladressen:
Microsoft Agent Framework (HTTP 404) sowie einzelne VPS-/Community-Seiten (0/403/404).
Die [datierte Einzelreferenzliste](CI_SOURCE_REFERENCES_2026-11-19.json) enthaelt Original-URLs,
betroffene Dateien, CI-Lauf/Job und den begrenzten unabhaengigen Pruefumfang.
Auf ausdrueckliche Nutzerfreigabe bleiben genau diese Adressen als Code mit Datum und Befund erhalten.
Das reduziert bewusst den Live-Link-Pruefumfang, nicht die Fehlerkriterien des Checkers.
Keine Domain-Ausnahme, kein 403/404 als Erfolg und kein Ersatz durch beliebige Startseiten.
Der Quellen-Auditgenerator darf die genehmigten Referenzen nicht wieder als aktive Links ausgeben.
Nicht erneut gelesene Inhalte, Lizenzbedingungen und VPS-Konditionen bleiben unbestaetigt.
Suchindex-Treffer belegen keine aktuelle Erreichbarkeit; die Installer-Quellenpins bleiben unveraendert.

Die Offline-Regression desselben Commits meldete genau einen Fehler: Die Cargo-Fixture erwartete
noch `verify(root, cwd)` statt des ausdruecklichen Versionsvertrags `verify(root, cwd, version=...)`.
Die korrigierte Assertion prueft diesen Pin weiterhin, statt den Mockaufruf unspezifisch zu akzeptieren.

## Nachpruefung 16.11.2026: rustfmt und AMD HIP

Am Commit `246680c` scheiterte der PR-Linkcheck an HTTP 502 fuer rustfmt in der
[Entwicklungsuebersicht](../DEVELOPMENT_TOOLS_OVERVIEW.md), der Push-Linkcheck an HTTP 429 fuer
AMD HIP Unified Memory im [Speicherleitfaden](../memory/UNIFIED_MEMORY_AND_OFFLOADING.md).
Beide Originalquellen waren separat erreichbar; das ersetzt keinen erfolgreichen CI-Abruf.
Die Quellen bleiben aktive Links, keine Ausnahmen oder Umleitung auf beliebige Ersatzseiten.

HTTP 429 behaelt zwei begrenzte Upstream-Wiederholungen und respektiert `Retry-After`.
Fehlt ein gueltiger Header, warten wir jetzt 60 statt fuenf Sekunden, entsprechend dem
[dokumentierten Upstream-Default][mlc-retries]. Fuer im zweiten Durchlauf weiterhin tote
HTTP-500/502/503/504-Ziele ist ein letzter Versuch nach 15 Sekunden vorgesehen.
Es gibt keinen vierten Wrapper-Durchlauf. Ein dauerhafter Fehler bleibt rot; bessere
Wartezeiten garantieren keine erfolgreiche Antwort. Die CI-Zeitlimits bleiben unveraendert.

[mlc-retries]: https://github.com/tcort/markdown-link-check/blob/v3.15.0/README.md

## Nachpruefung 16.11.2026: BashDB und HTTP 502

Im [Lauf 43787138722](https://github.com/dwhr-pi/OpenClaw-AI_Infrastructure-_Ultimate_Setup/actions/runs/43787138722)
scheiterte der Verweis auf [BashDB](https://github.com/Trepan-Debuggers/bashdb) mit HTTP 502 nach
dem vorhandenen begrenzten Retry. Das offizielle Repository war bei der separaten Nachpruefung
erreichbar und zeigte den Bash-Debugger. Das ist kein Nachweis, dass der fehlgeschlagene CI-Abruf
erfolgreich war. Keine Ignore-Regel, kein behandeltes 502 als Erfolg und keine abgeschaltete Pruefung.
Ein erneuter CI-Lauf muss die Adresse wirklich erfolgreich abrufen; ein dauerhafter Fehler bleibt rot.

## Verbindlicher Check

Weiterer Nachtrag PR 27 nach Commit `05abbed` vom 12.11.2026: Die PR- und
Push-Linkchecks scheiterten an HTTP 502 bei zwei unterschiedlichen, weiterhin
erreichbaren GitHub-Repositories. Beide Originaladressen wurden danach mit
HTTP 200 gelesen und bleiben aktive Quellen. Der gemeinsame Runner wiederholt
jetzt auch ausgewaehlte temporaere HTTP-Fehler genau einmal; 5xx werden nicht
als erfolgreich akzeptiert. Befunde, abgebrochene macOS-Push-Jobs und die
standalone Trivy-Patchkorrektur stehen im
[Folgebericht](PR27_CI_FOLLOWUP_2026-11-12.json). Fruehere Berichte bleiben erhalten.

Nachtrag PR 27 vom 12.11.2026: Der Push-Lauf `43207287611`, Job `131145567743`,
meldete Google HTTP 500 und beim Beautiful-Soup-Source-Ziel Transportstatus 0.
Die Google-Mitteilung wurde anschliessend vollstaendig mit HTTP 200 gelesen;
der aktive Link bleibt erhalten. Launchpad lief auch beim anonymen Einzelabruf
in ein Timeout. Die offizielle Beautiful-Soup-Website bestaetigt das Source-Ziel,
nicht dessen aktuelle Erreichbarkeit. Im
[Werkzeugvergleich](../tutorials/grok-development-tooling.md) bleibt die exakte
Launchpad-Adresse deshalb mit datiertem Befund als Code erhalten; die gelesene
offizielle Projektwebsite bleibt der aktive Beleg.
[Pruefbericht und Grenzen](PR27_CI_REFERENCE_REVIEW_2026-11-12.json).
Keine neue Ignore-Regel, keine Status-Aufweichung und keine Retry-Erweiterung.

Nachtrag PR 26 vom 12.11.2026: Die vLLM-Metrik-Webfassung lieferte im Push-Linkcheck wiederholt HTTP 429,
auch nach den bereits konfigurierten begrenzten 429-Retries. Die Originaladresse bleibt im
[Haertungsplan](../architecture/ENTERPRISE_HARDENING_ROADMAP.md#vllm-quellennachweis-vom-12112026)
als Code mit Befund erhalten. Aktive Belege sind zwei gelesene offizielle GitHub-Dateien am gleichen vollen Commit:
Dokumentation plus Metrikdefinitionen, weil die Markdown-Quelle generierte Tabellen einbindet.
[Pruefumfang, Quellpositionen und SHA256](VLLM_METRICS_REFERENCE_2026-11-12.json).
Kein Nachweis dauerhafter Unerreichbarkeit, kein Versionsupgrade und keine Lockerung der Link-Pruefung.

Nachtrag PR 10 vom 05.11.2026: Der Push-Lauf `41978791716`, Job `127083798023`,
scheiterte ausschliesslich an der FFmpeg-Filter-Webfassung mit Transportstatus 0;
der PR-Linkcheck desselben Commits `f72af3a9` war erfolgreich. Der unabhaengige
Abruf der Webfassung lieferte ebenfalls ein Timeout. Im
[Karaoke-Leitfaden](../media_studio/KARAOKE_SUBTITLES_GUIDE.md) bleibt die exakte
Originaladresse daher ausdruecklich unverifiziert erhalten. Der aktive Beleg
verweist auf den gelesenen offiziellen FFmpeg-GitHub-Quelltext an Commit
`0893feba652894f836cb76617936da52570d20a5`, insbesondere `ass` und `subtitles`.
Keine Domain-/Status-Ausnahme, kein abgeschalteter Check und keine Aenderung des
Link-Checkers. Ein beantragter Job-Neustart wurde von der Integration mit HTTP 403
abgewiesen; die dokumentierte Quellenkorrektur erhaelt einen neuen normalen Commit.

Im selben Commit scheiterte Repo Health, Job `127083809804`, ausschliesslich an
einem 51CTO-Community-Beitrag (Transportstatus 0 nach Retry). Ein Einzelabruf
lieferte keinen lesbaren Artikel. Die vollstaendige Originaladresse und die schon
zuvor eingeschraenkte Aussagekraft bleiben im
[token8341-Quellenabschnitt](../_API-Keys/OnlineOnKeyServices/token8341.md#was-ausserhalb-der-betreiberwebsite-gefunden-wurde)
explizit unverifiziert erhalten. Kein Ersatz durch eine beliebige Startseite,
keine Aufwertung einer Betreiberangabe zum unabhaengigen Test, keine Domain-Regel.

Alle Markdown-Dateien bleiben im bestehenden Link-Gate. In jedem Workflow muss die Konfiguration
explizit angegeben werden; sie wird nicht automatisch gefunden:

```sh
export NODE_PATH="$(npm root -g)"
node --test tests/test_markdown_link_retry.cjs
node scripts/quality/link_checker_contract.cjs "$(command -v markdown-link-check)"
node scripts/quality/check_markdown_links.cjs -c .github/markdown-link-check.json readme.md
set -euo pipefail
find docs -type f -name '*.md' -print0 | xargs -0 -r node scripts/quality/check_markdown_links.cjs -c .github/markdown-link-check.json
```

Verbindliche Bibliothek/CLI: `markdown-link-check@3.15.0`. Die zuvor verwendete CLI 3.13.7 gab bei
toten Links faelschlich Exitcode 0 zurueck. Deshalb prueft jeder der drei Workflows vor dem
Netzwerkcheck den echten installierten Checker mit `scripts/quality/link_checker_contract.cjs`:
vorhandene lokale Datei muss 0 liefern, fehlende Datei und gemischte Eingaben jeweils 1. Dieser
Regressionstest verwendet keine HTTP-Anfragen. Die
[offizielle korrigierte CLI](https://github.com/tcort/markdown-link-check/blob/v3.15.0/markdown-link-check)
wirft bei `dead` wieder einen Fehler. Ein alter gruener Job mit `ERROR: dead links` ist keine
Link-Abnahme. Der dedizierte Workflow prueft weiterhin alle Markdown-Dateien, nicht nur Aenderungen.

Der gemeinsame Runner verwendet weiterhin diese unveraenderte Upstream-Bibliothek mit ihrer
vollstaendigen Markdown-Auswertung und derselben JSON-Konfiguration. Ausschliesslich bei
HTTP(S)-Transportstatus 0 oder HTTP 500/502/503/504 wird nach fuenf Sekunden
genau einmal dasselbe Dokument erneut geprueft. Nur die urspruenglichen
wiederholbaren Fehler duerfen durch neue echte Pruefergebnisse ersetzt werden.
HTTP-202/401/403/404/501/505-Fehler, lokale Dateifehler und sonstige Fehler bleiben
fehlgeschlagen, auch wenn ein anderer Link den Wiederholungsversuch ausloest. Keine Endlosschleife,
keine Domain-Ausnahme, kein `continue-on-error`. Fehlende oder nachtraeglich ignorierte Ergebnisse
loeschen keinen Fehler; Parser-/Ergebnisfehler scheitern geschlossen. Beide echten Programme
(Upstream-CLI und Runner) durchlaufen denselben Offline-Datei-Exitcode-Test.
HTTP 429 behaelt ausschliesslich die begrenzte Upstream-Retry-Regel mit zwei Wiederholungen;
der Wrapper fuegt dafuer keinen weiteren Versuch hinzu. Ohne gueltiges `Retry-After` gilt eine
Wartezeit von 60 Sekunden.
Meldet der zweite Durchlauf fuer einen urspruenglich wiederholbaren HTTP(S)-Fehler erneut
HTTP 500/502/503/504, folgt genau ein letzter Durchlauf nach 15 Sekunden. Nur diese weiterhin
vorhandenen 5xx-Fehler koennen dadurch ersetzt werden; fehlende oder ignorierte Ergebnisse
erhalten keinen zusaetzlichen Versuch. Wiederholte Transportfehler mit Status 0 allein bleiben
nach zwei Durchlaeufen rot. Alle urspruenglichen permanenten Fehler bleiben erhalten.
Auch nach dem letzten Durchlauf tote Ziele bleiben Fehler. Es werden weder
zusaetzliche erfolgreiche HTTP-Statuscodes noch Domain-Ausnahmen eingefuehrt.

Die zusaetzliche Einzelpruefung unter `scripts/quality/external_link_probe.py` ersetzt diesen Parser
und seine vollstaendige Markdown-Abdeckung nicht. Sie untersucht explizite Markdown-Ziele mit GET,
vier parallelen Anfragen, zehn Sekunden Timeout und hoechstens zwei Versuchen. Nur 200/206 gelten
nach Weiterleitungen als erreichbar. 202, 429, temporaere 5xx und Transportfehler erhalten einen
zweiten Versuch nach einer Sekunde; 403/404 bleiben Fehler. Keine Cookies, Tokens oder privaten
Kontodaten.

```sh
python -B scripts/quality/external_link_probe.py --markdown docs/quality/EXTERNAL_LINK_POLICY.md
python -B -m unittest discover -s tests -p test_external_link_policy.py
```

Der Zusatzcheck prueft Erreichbarkeit, nicht fachliche Richtigkeit. Ein HTTP 200 allein beweist
weder Lizenz, Rechtsstand noch die Existenz eines bestimmten Inhalts. Ein gescheiterter Abruf darf
nicht durch eine beliebige erreichbare Startseite ersetzt werden. Historische Quellen bleiben mit
unveraenderter URL und explizitem Befund als Inline-Code erhalten, nicht als angeblich aktuelle
Empfehlung.

## Weitere Quellenbefunde vom 31.10.2026

Nachtrag 31.10.2026: Die
[einzeln protokollierte suedafrikanische Behoerdenadresse](UNVERIFIED_GOV_REFERENCE_2026-10-31.json)
scheiterte im CI auch nach dem begrenzten Transport-Retry. Lokal kam HTTP 200 zurueck; das ist keine
Inhalts-/Rechtsstandsverifikation. Die Originaladresse bleibt unverifiziert erhalten, die vorigen
Evidenzlisten bleiben unveraendert. Damit sind 26 exakte Originalreferenzen protokolliert, keine
pauschale Domain-Regel.

Zwei Godot-Exportseiten lieferten HTTP 429. Die inhaltlich gelesenen Originaldateien im offiziellen
Dokumentationsrepository sind deshalb auf einen geprueften Commit gepinnt und als aktive Belege
verknuepft; alte HTML-Adressen bleiben erhalten. Bei Pinokio bleibt die gesperrte API-Adresse als
Originalreferenz erhalten. Der erreichbare offizielle Release-Link belegt nur Version und
Assetliste, nicht allein die Digests. Installer-Integritaetspruefungen bleiben unveraendert.

## Exakte Auth-Klassifikation

Nur diese vier persoenlichen Kontoeinstiege sind in der Konfiguration exakt verankert. Sie werden
als AUTH/ausgenommen bezeichnet, niemals als verifizierter Inhalt. Die oeffentlichen Anleitungen in
den jeweiligen Registrierungsdokumenten bleiben aktiv geprueft. Andere Pfade, Query-Parameter,
Subdomains oder 401/403-Antworten sind damit nicht freigegeben.

| Kontoeinstieg                                        | Klassifikation                                                     |
| ---------------------------------------------------- | ------------------------------------------------------------------ |
| [Zotero Keys](https://www.zotero.org/settings/keys)  | Login erforderlich; gemeldeter Abruf 403; Inhalt nicht verifiziert |
| [Mistral Studio](https://console.mistral.ai/)        | Konto-Dashboard; gemeldeter Abruf 403; Inhalt nicht verifiziert    |
| [Cloudflare Dashboard](https://dash.cloudflare.com/) | Konto-Dashboard; gemeldeter Abruf 403; Inhalt nicht verifiziert    |
| [DeepSeek Platform](https://platform.deepseek.com/)  | Konto-Dashboard; gemeldeter Abruf 202; Inhalt nicht verifiziert    |

Die Beispiele `http://127.0.0.1:7860` und `http://127.0.0.1:4200` sind lokale Browseradressen, keine
oeffentlichen Quellen. Sie stehen als Code in den Anleitungen; Offline-Tests pruefen Scheme,
Loopback-Adresse und Port, ohne Dienste zu kontaktieren. Es gibt keine pauschale
localhost-/IP-/Domain-Ausnahme im Link-Gate.

## Quellenhistorie und Korrekturen

Die Alt-URLs stehen weiterhin an ihren urspruenglichen Fundstellen. Das duplizierte Setup-Audit ist
ein Quelleninventar, keine Liste funktionierender Installationen.

| Alte URL oder Klasse                                                                                           | Entscheidung und belegte Primaerquelle                                                                                                                                           |
| -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `https://github.com/kubernetes-sigs/kustomize/releases/tag/kustomize%2Fv5.8.2`                                 | 404; [Release mit unkodiertem Slash](https://github.com/kubernetes-sigs/kustomize/releases/tag/kustomize/v5.8.2) inhaltlich abgerufen                                            |
| `https://hg.reportlab.com/hg-public/reportlab`                                                                 | 403; [ReportLab-Dokumentation](https://docs.reportlab.com/) inhaltlich abgerufen; kein Nachweis, dass das alte Repository geloescht ist                                          |
| `https://docs.n8n.io/sustainable-use-license/`                                                                 | 404; [Lizenz im offiziellen Repository](https://github.com/n8n-io/n8n/blob/master/LICENSE.md) inhaltlich abgerufen                                                               |
| `https://docs.mistral.ai/getting-started/models/weights/`                                                      | 404; [Modellkatalog](https://docs.mistral.ai/models) inhaltlich abgerufen; Lizenzen pro Modell pruefen                                                                           |
| `https://ai.google.dev/gemma/docs/core.md`                                                                     | Abruf 0; [HTML-Modelluebersicht](https://ai.google.dev/gemma/docs/core) inhaltlich abgerufen; kein pauschaler Nachweis fuer einen Markdown-Export                                |
| `modelcontextprotocol/server-filesystem`, `modelcontextprotocol/server-git`                                    | Alte Reponamen 404; Verzeichnisse im [offiziellen Monorepo](https://github.com/modelcontextprotocol/servers)                                                                     |
| `modelcontextprotocol/server-sqlite`, `modelcontextprotocol/server-postgres`, `servers/tree/main/src/sqlite`   | Alte Pfade 404; [offizielles Archiv](https://github.com/modelcontextprotocol/servers-archived); nicht mehr gepflegt, keine Produktionsfreigabe                                   |
| `https://codeberg.org/forgejo/forgejo.git`                                                                     | Clone-URL, Abruf 403; als Code erhalten, [offizielle Projektdokumentation](https://forgejo.org/docs/latest/) inhaltlich abgerufen; kein erfolgreicher Repository-Abruf behauptet |
| `https://github.com/bminor/bash`                                                                               | 404; GNU-Originaladresse bleibt im gesonderten Nachtrag unverifiziert erhalten; keine erfolgreiche Inhaltspruefung behauptet                                                     |
| `https://github.com/canonical/ufw`                                                                             | 404; keine stillschweigende Behauptung eines existierenden GitHub-Repositories                                                                                                   |
| `https://github.com/flowiseai/flowisechatbot`                                                                  | 404; historischer Inventareintrag, nicht automatisch mit einem anderen Produkt gleichgesetzt                                                                                     |
| `https://github.com/openclaw/clawbake`                                                                         | 404; historisch, bestehender Clawbake-Leitfaden dokumentiert die separate Nutzerquelle                                                                                           |
| `https://github.com/till-schaefer/jarvis`                                                                      | 404; Nutzerquelle bleibt unverifiziert; keine Gleichsetzung mit Hermes                                                                                                           |
| `https://github.com/Microsoft/TypeScript-Node-Starter`, `https://github.com/microsoft/typescript-node-starter` | 404; historische Vorlage, keine aktuelle Sicherheitsempfehlung                                                                                                                   |
| `https://github.com/cheahjs/free-llm-api-resources`                                                            | 404; datierte Reviews bleiben erhalten; kein Nachweis dauerhafter Loeschung                                                                                                      |
| `https://github.com/dwhr-pi/content-multiplier`, `https://github.com/dwhr-pi/content-multiplier.git`           | 404; keine oeffentlich bestaetigte Quelle, keine Freigabe                                                                                                                        |
| `https://github.com/deinname/fingpt`, `https://github.com/username/huginn`                                     | Beispiel-/Fork-Platzhalter, keine Live-Repositories                                                                                                                              |
| `https://huggingface.co/datasets/ontocord/VALID/blob/1758855b0f16da2ba0edda156099cc5a78405a94/README.md`       | 401; historische Kartenrevision nicht erneut verifiziert, keine Auth-Ausnahme und keine aktuelle Lizenzbestaetigung                                                              |

## Oeffentliche Quellen mit gemeldeten Fehlern

Diese Liste umfasst alle uebrigen unterschiedlichen URLs aus dem gemeldeten Lauf; Mehrfachvorkommen
wurden zusammengefasst. Status 0 bedeutet Transportfehler, nicht HTTP. Die Spalte ist der
**gemeldete CI-Befund**, keine Behauptung eines erfolgreichen aktuellen Abrufs. Google Veo konnte im
Recherchewerkzeug inhaltlich abgerufen werden; ein solcher Browserabruf ersetzt keinen erfolgreichen
anonymen CI-Abruf. Bei Rechtstexten bleiben Zuordnung, Originalfassung, Konsolidierung und zeitliche
Gueltigkeit separat zu pruefen.

### Ausdrueckliche Quellenfreigabe vom 30.10.2026

Der Nutzer hat die einzeln belegte Umklassifizierung nicht automatisch pruefbarer Originaladressen
genehmigt. Die [datierte Evidenzliste](UNVERIFIED_SOURCE_REFERENCES_2026-10-30.json) enthaelt exakt
23 Adressen aus den fehlgeschlagenen Runs fuer `6e11a77`, Status und betroffene Dateien. Sie ist
Dokumentation, keine vom Checker eingelesene Ignore-Liste. Die Originaladressen bleiben an ihren
Fundstellen als Code mit Datum und unverifiziertem CI-Befund erhalten. Das aendert bewusst den
Live-Link-Pruefumfang, nicht die Erfolgskriterien. Keine Aussage, die Seiten seien geloescht,
veraltet, fachlich aktuell oder generell unerreichbar. Einige lieferten lokal 200, aus GitHub aber
0/403/406/502/503; andere scheiterten an beiden Orten. Oeffentliche aktive Links mit solchen
Antworten bleiben Fehler. Neue Fundstellen werden nicht automatisch umklassifiziert.

Erreichbare offizielle Zusatzbelege:

GNU-Nachtrag fuer `fe1d3a8`: Die
[zwei gesondert belegten GNU-Adressen](UNVERIFIED_GNU_REFERENCES_2026-10-30.json) scheiterten im
Push- und PR-Linklauf wiederholt mit Transportstatus 0. Lokal kam HTTP 200 zurueck, das bestaetigt
aber keinen Projektinhalt. Auch die geprueften Savannah-Alternativen lieferten keinen belastbar
bestaetigten Ersatzinhalt und werden deshalb nicht als neue Belege verwendet. Beide Originaladressen
bleiben mit Datum und Befund erhalten. Die erste Evidenzliste mit 23 Adressen bleibt unveraendert;
insgesamt sind damit 25 exakte Referenzen dokumentiert, keine Domain-Regel.

- [Perplexity Quickstart](https://docs.perplexity.ai/docs/getting-started/quickstart): Anlegen eines
  API-Keys in der Console; kein Kontozugriff, Tarif-/KYC-Nachweis oder Comet-Downloadnachweis.
- [CISA-Bulletin vom Maerz 2022](https://content.govdelivery.com/accounts/USDHSCISA/bulletins/30ef592):
  historischer Kontext der gemeinsamen Kubernetes-Guidance, kein Ersatz des gesperrten PDFs 1.2 vom
  August 2022 und keine neue Konformitaetsbescheinigung.

Beide Inhalte wurden gelesen und anonym mit HTTP 200 abgerufen. Vor einer fachlichen Nutzung
unverifizierter Originalreferenzen ist eine erneute Inhaltspruefung erforderlich. Eine spaetere
Wiederaufnahme als aktiver Link braucht einen nachvollziehbaren erfolgreichen Abruf und Review.

| Quelle                                                                                                                                                                                                                | Gemeldeter CI-Befund                          |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| `https://amtliche-handbuecher.bundesfinanzministerium.de/ao/2026/Datenschutz-Grundverordnung/inhalt.html` (BMF DSGVO; unverifizierte Originalreferenz, CI HTTP 503, 30.10.2026)                                       | 503                                           |
| `https://www.gesetze-im-internet.de/bdsg_2018/__26.html` (BDSG 26; unverifizierte Originalreferenz, CI Transportfehler, 30.10.2026)                                                                                   | 0                                             |
| `https://amtliche-handbuecher.bundesfinanzministerium.de/ao/2026/Anhaenge/BMF-Schreiben-und-gleichlautende-Laendererlasse/Anhang-33/inhalt.html` (BMF GoBD; unverifizierte Originalreferenz, CI HTTP 503, 30.10.2026) | 503                                           |
| `https://www.gnu.org/software/gdb/` (GNU GDB; unverifizierte Originalreferenz, CI Transportfehler, 30.10.2026)                                                                                                        | 0                                             |
| `https://www.gnu.org/software/bash/` (GNU Bash; unverifizierte Originalreferenz, CI Transportfehler, 30.10.2026)                                                                                                      | 0                                             |
| [DSGVO DE ELI - Quellstatus, nicht verifiziert](PR24_LINKCHECK_2026-11-11.md#dsgvo)                                                                                             | 202                                           |
| `https://www.gesetze-im-internet.de/urhg/__69d.html` (UrhG 69d; unverifizierte Originalreferenz, CI Transportfehler, 30.10.2026)                                                                                      | 0                                             |
| `https://www.gesetze-im-internet.de/urhg/__69e.html` (UrhG 69e; unverifizierte Originalreferenz, CI Transportfehler, 30.10.2026)                                                                                      | 0                                             |
| [Veo](https://ai.google.dev/gemini-api/docs/veo)                                                                                                                                                                      | 0                                             |
| [AI Act - Quellstatus, nicht verifiziert](PR24_LINKCHECK_2026-11-11.md#ai-act)                                                                                                   | 202                                           |
| `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202601744` (OJ 2026/1744; unverifizierte Originalreferenz, CI HTTP 202, 30.10.2026)                                                                         | 202; Zuordnung zu AI Omnibus nicht bestaetigt |
| [DSGVO ELI - Quellstatus, nicht verifiziert](PR24_LINKCHECK_2026-11-11.md#dsgvo)                                                                                                | 202                                           |
| [DSM - Quellstatus, nicht verifiziert](PR24_LINKCHECK_2026-11-11.md#dsm)                                                                                                      | 202                                           |
| [NIS-2 - Quellstatus, nicht verifiziert](PR24_LINKCHECK_2026-11-11.md#nis-2)                                                                                                    | 202                                           |
| `https://www.gesetze-im-internet.de/` (Gesetze im Internet; unverifizierte Originalreferenz, CI Transportfehler, 30.10.2026)                                                                                          | 0                                             |
| `https://www.law.go.kr/` (Korea; unverifizierte Originalreferenz, CI Transportfehler, 30.10.2026)                                                                                                                     | 0                                             |
| `https://www.pdpc.gov.sg/` (Singapur; unverifizierte Originalreferenz, CI HTTP 202, 30.10.2026)                                                                                                                       | 202                                           |
| `https://ndpc.gov.ng/` (Nigeria; unverifizierte Originalreferenz, CI HTTP 403, 30.10.2026)                                                                                                                            | 403                                           |
| `https://uaelegislation.gov.ae/` (VAE; unverifizierte Originalreferenz, CI HTTP 403, 30.10.2026)                                                                                                                      | 403                                           |
| `https://pravo.gov.ru/` (Russland; unverifizierte Originalreferenz, CI Transportfehler, 30.10.2026)                                                                                                                   | 0                                             |
| `https://publication.pravo.gov.ru/` (Russland Publikation; unverifizierte Originalreferenz, CI Transportfehler, 30.10.2026)                                                                                           | 0                                             |
| `https://zakon.rada.gov.ua/laws/main?lang=en` (Ukraine; unverifizierte Originalreferenz, CI Transportfehler, 30.10.2026)                                                                                              | 0                                             |
| [Paperless API](https://github.com/paperless-ngx/paperless-ngx/blob/main/docs/api.md)                                                                                                                                 | 403; oeffentliche Doku, keine Auth-Ausnahme   |
| [Google Preise](https://ai.google.dev/gemini-api/docs/pricing)                                                                                                                                                        | 0                                             |
| [Google Billing](https://ai.google.dev/gemini-api/docs/billing)                                                                                                                                                       | 0                                             |
| [Google Einstieg](https://ai.google.dev/)                                                                                                                                                                             | 0                                             |
| [DSGVO CELEX - Quellstatus, nicht verifiziert](PR24_LINKCHECK_2026-11-11.md#dsgvo)                                                                                              | 202                                           |
| [AI Act CELEX - Quellstatus, nicht verifiziert](PR24_LINKCHECK_2026-11-11.md#ai-act)                                                                                             | 202                                           |
| [Google API Key](https://ai.google.dev/gemini-api/docs/api-key)                                                                                                                                                       | 0                                             |
| `https://media.defense.gov/2022/Aug/29/2003066362/1/1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF` (NSA/CISA Kubernetes 1.2; unverifizierte Originalreferenz, CI HTTP 403, 30.10.2026)                       | 403                                           |

## CI-Quellenabgleich (30.10.2026)

Die Alt-Adressen bleiben als Herkunftsbeleg erhalten. Die neuen Nachweise wurden anonym mit HTTP 200
abgerufen und anhand von Titel und CELEX bzw. offizieller Projektquelle zugeordnet.
EU-Metadatensaetze belegen die jeweilige Originalveroeffentlichung, nicht eine aktuelle
konsolidierte Rechtspruefung. Keine Anmeldung und keine Provider-Inferenz.

| Alt-Adresse (Abruf fehlgeschlagen)                                     | Damaliger Nachweis und aktueller Quellstatus                                                                                 |
| ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `https://eur-lex.europa.eu/eli/reg/2016/679/oj?locale=de`              | [Quellstatus, nicht verifiziert](PR24_LINKCHECK_2026-11-11.md#dsgvo) |
| `https://eur-lex.europa.eu/eli/reg/2016/679/oj`                        | [Quellstatus, nicht verifiziert](PR24_LINKCHECK_2026-11-11.md#dsgvo) |
| `https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32016R0679` | [Quellstatus, nicht verifiziert](PR24_LINKCHECK_2026-11-11.md#dsgvo) |
| `https://eur-lex.europa.eu/eli/reg/2024/1689/oj`                       | [Quellstatus, nicht verifiziert](PR24_LINKCHECK_2026-11-11.md#ai-act) |
| `https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32024R1689` | [Quellstatus, nicht verifiziert](PR24_LINKCHECK_2026-11-11.md#ai-act) |
| `https://eur-lex.europa.eu/eli/dir/2019/790/oj`                        | [Quellstatus, nicht verifiziert](PR24_LINKCHECK_2026-11-11.md#dsm) |
| `https://eur-lex.europa.eu/eli/dir/2022/2555/oj`                       | [Quellstatus, nicht verifiziert](PR24_LINKCHECK_2026-11-11.md#nis-2) |
| `https://docs.paperless-ngx.com/api/`                                  | [Primaerquelle](https://github.com/paperless-ngx/paperless-ngx/blob/main/docs/api.md)                                      |

## Nachpruefung der EU-Metadaten am 11.11.2026

Die folgenden Originalreferenzen bleiben erhalten, sind nach CI-Transportfehlern bzw. HTTP 502
und separatem HTTP 502 derzeit nicht inhaltsverifiziert. Der fruehere Quellenstand bleibt historisch,
keine neue konsolidierte Rechtspruefung wird behauptet. Einzelbelege und Abrufgrenzen:
[PR-24-Quellenbericht](PR24_LINKCHECK_2026-11-11.md). Keine Domain-/Status-Ausnahme im Linkchecker.

| Historische Metadatenadresse | Nachpruefung |
| --- | --- |
| `https://op.europa.eu/en/publication-detail/-/publication/3e485e15-11bd-11e6-ba9a-01aa75ed71a1/language-de` | unverifizierte Originalreferenz; 11.11.2026, HTTP 502 |
| `https://op.europa.eu/en/publication-detail/-/publication/dc8116a1-3fe6-11ef-865a-01aa75ed71a1/language-de` | unverifizierte Originalreferenz; 11.11.2026, HTTP 502 |
| `https://op.europa.eu/en/publication-detail/-/publication/214471fe-786e-11e9-9f05-01aa75ed71a1/language-de` | unverifizierte Originalreferenz; 11.11.2026, HTTP 502 |
| `https://op.europa.eu/en/publication-detail/-/publication/9b84d482-85bd-11ed-9887-01aa75ed71a1/language-de` | unverifizierte Originalreferenz; 11.11.2026, HTTP 502 |
