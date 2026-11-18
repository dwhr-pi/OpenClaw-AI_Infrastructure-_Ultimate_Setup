# VPS-Anbieterreview und Quellenstand vom 18.11.2026

## 1. Auftrag, Evidenz und Grenzen

Deutschsprachige Dokumentationsrecherche, Stand **2026-11-18**. Keine Vollerfassung des Weltmarkts und keine Zusage
freier Kapazitaet, erfolgreicher Registrierung, dauerhafter Kostenfreiheit oder erlaubter Spezialnutzung. Schwerpunkt:
OCI, Google Cloud und Hetzner. Der vorhandene weltweite Katalog wird nach Angebotsart eingeordnet, nicht fuer jeden
Eintrag neu vollstaendig geprueft.

Gelesene lokale Grundlagen: `AGENTS.md` und `docs/INSTALLATION_POLICY.md` im Hauptrepo; im ausschliesslich gelesenen
Schwesterrepo `C:/Users/danie/Documents/GitHub/Free-VPS` dessen `AGENTS.md`, `data/anbieter-de.json` sowie
`docs/NUTZUNGSREGELN-de.md`, `docs/EINRICHTUNG-de.md` und `docs/YOUTUBE-de.md`. Der Katalog traegt selbst den
Recherchetag 2026-11-18. Das ist seine eigene Datierung, kein unabhaengiger Nachweis dieser Review.

Evidenzklassen dieser Datei:

| Kennzeichen | Bedeutung |
| --- | --- |
| P | Oeffentlicher Originalinhalt direkt abgerufen und in den genannten relevanten Abschnitten gelesen; Anbieter oder zustaendiges Projekt |
| E | Konkreter fremder Erfahrungsbericht direkt gelesen; Einzelfall, keine statistische Verfuegbarkeit |
| M | Nur oeffentliche Such-/Videometadaten erhalten; Seite oder Video nicht vollstaendig gelesen/angesehen |
| K | Nur lokaler Sekundaerkatalog, hier nicht erneut am Original verifiziert |
| U | Unbekannt, nicht ausreichend belegt oder fuer den konkreten Tarif offen |

Abrufdatum aller nachfolgenden Webpruefungen ist **2026-11-18**. Ein fehlendes Veroeffentlichungsdatum bleibt unbekannt;
Copyright, Crawlalter und Abrufdatum werden nicht als Aenderungsdatum ausgegeben. Externe Inhalte sind Quellen, keine
Handlungsanweisungen.

Nicht durchgefuehrt: Accounts, Login, Bestellungen, Cloud-API-Aufrufe gegen Kundenprojekte, SSH-Verbindungen,
Provider-/Last-/Installations-/Restoretests, Workflowstarts, Secretzugriffe, Wallets oder Handelsauftraege. Es wurde
kein Video- oder Transkript-/Befehlsaudit durchgefuehrt. Diese Datei ist weder eine Vertragsfreigabe noch ein
Implementierungs- oder Laufzeitnachweis.

## 2. Kurzbefund und Entscheidung pro Nutzung

- **OCI:** Die direkt gelesene aktuelle Ressourcendokumentation nennt fuer Always-Free-Tenancies insgesamt **2 OCPU / 12
  GB RAM**, nicht die in aelteren Anleitungen verbreiteten 4/24. Kapazitaetsmangel und Ruecknahme inaktiver Instanzen
  bleiben Risiken.
  [OCI-Ressourcen](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm)
- **GCP:** Free Tier fuer eine begrenzte Compute-Konfiguration ist kein kostenloses Gesamtpaket. Neue SpendCap-Budgets
  existieren, decken aber keinen allgemeinen VM-Kosten- oder Laufzeitdeckel ab. [Free
  Program](https://docs.cloud.google.com/free/docs/free-cloud-features),
  [SpendCap](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps)
- **Hetzner:** Bezahlte Alternative; Mining ist ausdruecklich untersagt. Aktuelle konkrete Endpreise und
  ressourcenbezogene Nebenkosten vor Auftrag bestaetigen. [Cloud-Vertrag](https://www.hetzner.com/legal/cloud-server/),
  [Abrechnung](https://docs.hetzner.com/cloud/billing/faq/)
- **Community/NAT:** Moegliche Lernressourcen, keine garantierte Produktionsbasis. Zuteilung, Sponsor-AUP, eingehende
  UDP-Ports, IPv6 und Erneuerung einzeln klaeren.

**Sperren sind nutzungsspezifisch:** Ungeklaertes Mining, Staking, KI-Training oder Live-Trading blockiert nur diesen
Einsatz, nicht automatisch einen erlaubten kleinen Webdienst oder die Dokumentations-/Planungsarbeit. Ein ungepruefter
Kernelpfad blockiert K3s/WireGuard, nicht automatisch SSH. Eine fehlende harte Kosten-/Laufzeitbegrenzung blockiert hier
unbeaufsichtigte Neuprovisionierung, nicht pauschal den bewusst genehmigten Umgang mit vorhandenen Ressourcen. Ein
generelles Go fuer Produktion wird keinem Anbieter erteilt.

## 3. OCI, GCP und Hetzner im Detail

### 3.1 Kosten, Registrierung und Ressourcen

| Dimension | OCI Always Free | GCP Compute Engine Free Tier | Hetzner Cloud |
| --- | --- | --- | --- |
| Angebotsklasse | Begrenztes Dauerkontingent; Trial separat | Begrenztes monatliches Kontingent; Trial separat | Regulaer bezahlt; kein dauerhaft kostenloser VPS nachgewiesen |
| Compute, RAM, Architektur | A1 ARM64 insgesamt 2 OCPU/12 GB; genaue Kombination mit AMD-Micro pruefen [O1] | `e2-micro`-Zeitkontingent; nicht eine freie VM je Region [G1]; Katalog nennt AMD64/1 GB, hier RAM nicht separat an Shape-Dokumentation bestaetigt (K) | CX/CAX laut Katalog AMD64-/ARM-Optionen; konkretes bestellbares CPU-/RAM-Paket hier U (K) |
| Disk | 200 GB gemeinsamer Blockspeicher einschliesslich Bootvolumes [O1] | 30 GB-Monate **Standard Persistent Disk** [G1]; SSD/balanced nicht gleichsetzen | Inklusivdisk/Volumes anhand konkreter SKU U; keine Mengen aus alter Generation zusagen |
| GPU | Kein kostenloser GPU-Anspruch in diesen gelesenen Compute-Angeboten | GPU/TPU nicht Teil dieses Free Tier [G1] | GPU in diesem Cloud-VPS-Tarif nicht nachgewiesen; andere Produktlinie separat |
| Region | Heimatregion, Shape-Kapazitaet nicht garantiert [O1] | `us-west1`, `us-central1`, `us-east1` fuer dieses Compute-Kontingent [G1] | Katalog: DE/FI, weitere Serien USA/SG; jeweilige SKU-Verfuegbarkeit hier U (K) |
| Basispreis und Trial | Innerhalb freier Grenzen 0; 300 USD/30 Tage Trial separat [O2] | Innerhalb Grenzen 0; 300 USD/90 Tage Trial separat [G1] | Katalog/Index: CX23 DE/FI ab 15.06.2026 5,49 EUR netto/Monat ohne IPv4; rechnerisch ca. 6,53 EUR mit 19% USt. **Nicht direkt nachbestaetigter Endpreis** [H4] |
| Nebenkosten | PAYG-Mehrverbrauch und Zusatzprodukte getrennt pruefen; kein pauschaler Gesamtkostendeckel belegt | IPv4, Cloud NAT, Mehr-Egress, falsche Disks, Snapshots und weitere Dienste kostenpflichtig moeglich [G2] | Primary IPv4, Volumes, Backups, Snapshots, Egress und Steuer separat; konkrete Gesamtsumme U [H2] |
| Karte, Identitaet | Geeignete Kredit-/Debitkarte zur Verifikation; virtuelle/Prepaid-Karten laut FAQ nicht akzeptiert [O2] | Gueltiges Zahlungsmittel/Identitaetspruefung, je Land auch Bankverifikation [G1] | Vollstaendige korrekte Daten, Nachweise auf Anforderung [H3]; fuer diesen Nutzer erforderliches Zahlungsmittel/KYC hier U |
| Mehrfachkonten | Maximal ein Free-Trial-/Always-Free-Konto pro Person; auch Versuche mehrerer freier Konten untersagt [O2] | Keine Konto-/Projektaufteilung zur Umgehung von Gebuehren/Limits [G3] | Konkrete Mehrfachkontenregel U; keine Freigabe daraus ableiten |
| Agentenregistrierung | Vollautonome Erstregistrierung nicht belegt | Vollautonome Erstregistrierung nicht belegt | Vollautonome Erstregistrierung nicht belegt |
| API/Automatisierung | Katalog nennt OCI CLI/API/Terraform (K); hier keine API-Abnahme | Bestehende Ressourcen: vom Auftraggeber beschriebener Adapterumfang, siehe 3.3; hier kein API-Test | Katalog nennt Verwaltungsautomatisierung (K); hier keine API-/Token-/Adapterabnahme |
| Laufzeit/Erneuerung | Kein fester Always-Free-Ablauf laut FAQ; inaktive Ressourcen/Konten koennen entfallen [O1/O2] | Trialende und Paid-Billing unterscheiden; Free Tier kein unbedingter Dauerbetriebsanspruch [G1] | Abrechnung solange Server existiert, auch ausgeschaltet; Loeschen beendet nur betroffene Ressource [H2] |
| OS/Root | Gelistete Always-Free-Linux-Images, ARM/AMD passend waehlen [O1]; Windowsanspruch U | Trial schliesst Windows-Server-Images aus [G1]; konkretes Image/Root/sudo pruefen | Konkretes Linux-/Windowsimage, Lizenzkosten und Rootzugang U fuer ungewaehlten Tarif |
| SLA/Support | Kein Free-Tier-SLA, eingeschraenkter Support [O2] | Konkrete Free-Tier-SLA-/Supportdeckung hier U | Cloud-SLA 99,9% monatlich mit Ausschluessen und Credit-Verfahren, keine Backup-/Anwendungs-SLA [H1] |
| Backup/Restore | Externen Restore selbst planen; keine Probe erfolgt | Snapshotpreise und externe Sicherung selbst planen; keine Probe erfolgt | Eigenverantwortliche externe Backups [H3]; kostenpflichtige Anbieterbackups ersetzen keine Restoreprobe |

Der Hetzner-Preis ist bewusst nur K/M: Die verlinkte Preisanpassungsseite liefert im Suchindex eine Tabelle, direkte
Abrufe der englischen/deutschen Seite scheiterten hier. Das ist **keine gelesene aktuelle Preisliste**. Keine
Kaufentscheidung auf dieser Zahl allein aufbauen. [Index-Fundstelle der
Preisanpassung](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/)

### 3.2 Netz, Traffic und technische Eignung

| Dimension | OCI | GCP | Hetzner |
| --- | --- | --- | --- |
| Traffic | Katalog nennt 10 TB/Monat ausgehend (K); Egressabschnitt hier nicht separat vollstaendig nachgeprueft | 1 GB/Monat aus Nordamerika, China/Australien ausgenommen [G1]; weitere Pfade nach Preisliste | Nur ausgehender Mehrtraffic wird laut FAQ berechnet; konkrete Inklusivmenge der gewaehlten SKU hier U [H2] |
| Bandbreite/Fair Share | AMD-Micro laut [O1] bis 50 Mbit/s Internet; A1 shapeabhaengig, keine dedizierte Mindestleistung behauptet | Port-/Sustained-CPU-Leistung fuer konkrete VM hier U | Geteilte/dedizierte CPU und konkrete Portgeschwindigkeit hier U |
| IPv4 | Micro-Dokumentation nennt oeffentliche IP; nicht jedem Host zwingend zuweisen [O1]; Zusatz-IP-Kosten U | Standard-VM IPv4 aktuell 0,005 USD/Stunde, nur 1 Stunde/Monat frei laut [G2]; nicht als dauergratis buchen | Primary IPv4 separat berechnet, auch unzugewiesen; konkreter Preis U [H2] |
| IPv6 | Region/Subnetz/VNIC/Firewall fuer konkretes Setup U | Konkrete IPv6-only-/Dual-Stack-Konfiguration und Erreichbarkeit U; IPv6 ersetzt nicht jede IPv4-Abhaengigkeit | Primary IPv6 laut FAQ kostenlos [H2]; Clientroute und konkretes Praefix U |
| NAT/UDP/Ports | Sicherheitslisten/Hostfirewall und erlaubte UDP-Pfade konkret U | Cloud NAT ist kostenpflichtig und kein kostenloser eingehender Portweiterleitungsdienst [G2] | NAT-/Port-/UDP-Pfad im gewaehlten Netz konkret U |
| TUN/Kernel/cgroups | Nicht mit SSH oder Rootnachweis gleichsetzen; konkret U | Konkret U, nicht durch Free-Tier-Label belegt | Konkret U, insbesondere nicht aus Preis ableiten |
| K3s | A1 fuer kleines Labor nach Ressourcenpruefung plausibel; keine Laufzeitabnahme | Ein 1-GB-Host laut Katalog kein empfohlener K3s-Server; Agent nur nach Pruefung | Ausreichend dimensionierte SKU plausibel; Architektur/CRI/Netz/Backup erst nachweisen |
| Ollama/OpenClaw | Schlanke Koordination eher als grosses Modelltraining; ARM-Builds pruefen | Eher kleiner Dienst/Koordination, nicht GPU-/Trainingshost | Kleine Koordination moeglich; Inferenzleistung/CPU-Dauerlast und Spezial-AUP offen |

Die letzten beiden Zeilen sind **eigene Planungsableitungen**, keine Anbieterfreigaben. K3s dokumentiert als Minimum 2
Kerne/2 GB fuer Server und 1 Kern/512 MB fuer Agenten; Anwendungsreserve, schnelle Disk und cgroups kommen hinzu. API
6443 nur fuer berechtigte Peers; CNI-/etcd-Pfade passend zum gewaelten Backend, VXLAN nicht ins offene Internet stellen.
[K3s-Voraussetzungen](https://docs.k3s.io/installation/requirements)

### 3.3 GCP: Budgetalarm, SpendCap und Adapter getrennt halten

Die aktuelle Originalseite **Manage spend cap budgets**, zuletzt aktualisiert **2026-11-10 UTC**, wurde direkt gelesen.
SpendCap ist nicht dasselbe wie ein reines Alarmbudget:

- SpendCaps gelten je **einem Projekt und einem berechtigten Dienst**, monatlich: Gemini API, Gemini Enterprise Agent
  Platform (vormals Vertex AI), Cloud Run und Cloud Run functions.
- Bei Durchsetzung werden neue Nutzungen dieses Dienstes pausiert; laufende Anfragen werden beendet und abgerechnet.
- **Persistente Compute-/Storage-Ressourcen bleiben aktiv und verursachen weiter Kosten.** Andere Dienste/Projekte
  werden nicht generell gestoppt.
- Durchsetzung ist nicht sofortig; **Overages werden regulaer berechnet**. Der naechste Budgetzeitraum hebt die Sperre
  automatisch auf.

Daher weder pauschal "GCP hat keine SpendCaps" noch "SpendCap garantiert ein hartes VM-Limit" schreiben. [Originalquelle
und Einschraenkungen](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps)

**Adapterabgrenzung nach Mitteilung des Auftraggebers am 18.11.2026, nicht eigenstaendig am Code verifiziert:** Der
Hauptadapter arbeitet mit `GCP existing resources GET` sowie SSH-Verifikation/`configure`. Diese Review aendert ihn
nicht und setzt vorhandene Ressourcen nicht mit Neuprovisionierung gleich. Solange kein wirklich harter, fuer alle neu
angelegten Ressourcen belegter Kosten- **und** Laufzeitabschluss vorhanden ist, bleibt **Neuprovisionierung
fail-closed**. Ein Alarm, verzoegerter SpendCap, Best-effort-Timer oder freies VM-Zeitkontingent genuegt dafuer nicht.
Vorhandene Ressourcen koennen bereits Kosten verursachen; `configure` ist eine bewusste Aenderung und nicht durch einen
lesenden GET automatisch genehmigt. Kein API-/SSH-Aufruf wurde fuer diese Review ausgefuehrt.

Zusaetzlicher datierter Befund: Die aktuell gelesene Free-Program-Seite nennt fuer Anmeldungen/Upgrades ab
**16.11.2026** einen Ausschluss des 300-USD-Guthabens fuer Gemini-Plattformdienste (frueher Vertex AI); auch Gemini API
in AI Studio ist nicht pauschal davon bezahlt. Kein generisches "300 USD fuer beliebige KI" versprechen.
[Free-Program-Original](https://docs.cloud.google.com/free/docs/free-cloud-features)

### 3.4 AUP und Nutzung: keine pauschale Krypto-/KI-Freigabe

`U` bedeutet in jeder Zelle ausdruecklich **unbekannt fuer die konkrete Nutzung und den konkreten Tarif**. Vor genau
dieser kritischen Nutzung aktuelle Vertragsfassung und gegebenenfalls schriftliche Anbieterbestaetigung beschaffen. Aus
fehlendem Verbot wird keine Erlaubnis. Hostingvertrag und technische Moeglichkeit ersetzen keine rechtliche Zulassung.

| Nutzung | OCI | GCP | Hetzner Cloud |
| --- | --- | --- | --- |
| Allgemeine AUP / Missbrauch | Passenden Landesvertrag und Service Policies noch bestimmen; Vertragsportal gelesen, vollstaendige AUP-Pruefung U [O3] | AUP gelesen: u. a. illegale Nutzung, Betrug, Spam, unberechtigte Zugriffe untersagt; gilt auch fuer Agenten [G4] | AGB/Cloud-Vertrag gelesen; Missbrauch/illegale Inhalte untersagt [H1/H3] |
| CPU-/GPU-Mining | U | Im Free Trial untersagt [G1]; allgemein nur mit vorheriger schriftlicher Google-Genehmigung [G3] | Ausdruecklich untersagt [H1/H3] |
| Farming/Plotting | U | U separat; Miningregel nicht blind auf jeden Algorithmus uebertragen | AGB nennen Farming/Plotting ausdruecklich im Verbot [H3] |
| KI-API-Client / Agentenkoordination | Kleine Anwendungen beschrieben [O1]; konkrete Inhalte/Agentenrechte U | AUP gilt; API-Tarif und Rechte gesondert pruefen [G4] | Kein spezifisches Freigabeurteil; konkrete Last/Inhalte U |
| Eigene KI-Inferenz | Workloadfreigabe U; keine Gratis-GPU nachgewiesen | Workloadfreigabe U; Compute-/API-/Modelllizenz getrennt | Workloadfreigabe U; Cloud-VPS nicht mit eigener Inference API gleichsetzen |
| KI-Training / Dauer-Volllast | U | U; kein allgemeiner Trainingsanspruch aus Trial/KI-Marketing | U; Shared-CPU-/Systemregeln vor Dauerlast klaeren |
| Krypto-Analyse / Walletsoftware | U | U | U; nicht automatisch Mining, aber keine Freigabe belegt |
| Blockchain-Full-/RPC-Node | U | U | U; kein aktuelles Totalverbot aller Blockchain-Nutzungen aus Miningklausel ableiten |
| Staking / Validator | U, getrennt von Mining | U, getrennt von Mining | U, getrennt von Mining; vor Einsatz schriftlich klaeren |
| Offlineanalyse / Paper-Trading | Konkrete Vertragsdeckung U | Konkrete Vertragsdeckung U | Konkrete Vertragsdeckung U; nicht gleich Live-Kryptohandel |
| Live-Trading-Bot, privat | U; Broker-/Boersenregeln zusaetzlich | U; Broker-/Boersenregeln zusaetzlich | U; keine Erlaubnis aus fehlender Miningaktivitaet ableiten |
| Oeffentliche Tradingplattform / Exchange | U; Vertrags-/Compliancepruefung erforderlich | U; Vertrags-/Compliancepruefung erforderlich | U; Vertrags-/Compliancepruefung erforderlich |
| Privates WireGuard / Tunnel | Konkrete Nutzung/Netzrechte U | Konkrete Nutzung/Netzrechte U | Konkrete Nutzung/Netzrechte U |
| Oeffentliches VPN / Proxy / TOR / P2P | Jeweils U | Jeweils U | Jeweils U |
| Kommerzielle Anwendung / Weiterverkauf | Konkreter Tarif-/Nutzungsumfang U; nicht gleichsetzen | Allgemeine Anwendungsnutzung im Vertrag, Weiterverkauf eingeschraenkt [G3]; konkrete Dienstleistung U | Drittbenutzung in AGB geregelt, Verantwortung bleibt beim Kunden [H3]; konkrete Weiterverkaufsform U |
| Automatisierte Kontoanlage / Kontingentumgehung | Keine autonome Registrierung belegt; freie Mehrfachkonten untersagt [O2] | Umgehung von Gebuehren/Quoten untersagt [G3]; autonome Registrierung U | Autonome Registrierung/Mehrfachkonten U |

## 4. Weltweiter Bestand: 56 Katalogeintraege, keine 56 bestaetigten Gratisanbieter

Quelle dieses Abschnitts ist ausschliesslich **K**, soweit nicht ausdruecklich P genannt. Grundlage: lokale Datei
`C:/Users/danie/Documents/GitHub/Free-VPS/data/anbieter-de.json` (Schema 1, eigene Datierung 2026-11-18). Ihre einzelnen
Recherchebehauptungen werden nicht als eigene Originalpruefung uebernommen. Anbieterstandorte sind keine Garantie, dass
jeder Tarif weltweit bestellbar ist. Sponsoren/Nodes werden nicht als weitere Gratisanbieter gezaehlt; OVH Trial/VPS und
Azure/Students sind getrennte Angebote desselben Konzerns.

| Kategorie | Bestand mit Angebotslinks | Geografischer Rahmen laut Katalog / Bedeutung |
| --- | --- | --- |
| Begrenztes Cloud-Freikontingent (2) | [OCI](https://www.oracle.com/cloud/free/), [GCP](https://cloud.google.com/free/) | OCI Heimatregion; GCP-Compute nur drei US-Regionen. P-Vertiefung oben, keine Kapazitaetsgarantie |
| Community-/Sponsorangebote (2) | [FreeVPS.org](https://www.freevps.org/), [FOSSVPS](https://fossvps.org/) | Europa, Nordamerika und APAC je Sponsor; P-Stichprobe unten |
| Verlaengerungs-/IPv6-/historisch unsichere Gratisgruppe (4) | [EUserv VS2-free](https://www.euserv.com/en/virtual-private-server/root-vserver/v2/vs2-free.php), [HAX](https://hax.co.id/), [Woiden](https://woiden.id/), [Openworld](https://openworld.eu.org/) | EUserv DE, sonst nodeabhaengig; heutige Zuteilung/Erneuerung/Kosten U. Kataloglabel `gratis` ist keine Bestaetigung |
| Unbestaetigte bzw. eingeschraenkte Kandidaten (8) | [VPSFree.io](https://vpsfree.io/), [TheUltraHost](https://theultrahost.com/free-vps), [vyce.cloud](https://vyce.cloud/), [Verta Cloud](https://portal.vertacloud.biz/index.php?rp=/store/free-vps), [GratisVPS](https://gratisvps.net/), [AlaVPS](https://alavps.com/vps.html), [FreeVPS.edu.pl](https://freevps.edu.pl/), [FreeVPSHostings](https://freevpshostings.com/) | Standort/Berechtigung/Root/Bestand/Vertrag jeweils U; keine Bestellung empfohlen, nur Kandidatenstatus |
| Befristete Trials / Credits (11) | [AWS](https://aws.amazon.com/free/), [Azure](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account), [Azure Students](https://azure.microsoft.com/en-us/free/students/), [DigitalOcean](https://www.digitalocean.com/products/droplets), [Vultr](https://docs.vultr.com/platform/create-an-account), [Akamai/Linode](https://www.akamai.com/cloud/pricing), [Kamatera](https://www.kamatera.com/free-trial/), [Alibaba](https://www.alibabacloud.com/en/free), [OVH Public Cloud](https://www.ovhcloud.com/asia/public-cloud/free-trial/), [Prepaid-Hoster](https://www.prepaid-hoster.de/vserver/vserver-testen-neu.html), [1Free.eu](https://www.1free.eu/en) | Grosse Clouds international, einzelne Tarife/Identitaeten/Regionen eingeschraenkt; Laufzeit, Credits und Folgekosten hier U, keine alten Trialzahlen als aktuelle Garantie |
| Geld-zurueck, nicht gratis (2) | [IONOS](https://www.ionos.de/server/free-vps), [dogado](https://www.dogado.de/vps/vserver-bei-dogado/vserver-kostenlos-testen) | Erstattungsvertrag mit Zahlung/Kuendigung/Fristen; konkrete aktuelle Bedingungen U |
| Bezahlte VPS (12) | [Hetzner](https://www.hetzner.com/cloud/), [netcup](https://www.netcup.com/de/server/vps), [Contabo](https://contabo.com/en/vps/), [OVH VPS](https://www.ovhcloud.com/de/vps/), [Time4VPS](https://www.time4vps.com/Linux-vps/), [AlphaVPS](https://alphavps.com/uk-vps/), [BuyVM](https://buyvm.net/kvm-dedicated-server-slices), [WebHorizon NAT](https://my.webhorizon.net/order/main/index/nat), [GreenCloud](https://greencloudvps.com/budget-kvm-vps.php), [HostHatch](https://hosthatch.com/products), [RackNerd](https://www.racknerd.com/kvm-vps), [Sakura](https://vps.sakura.ad.jp/) | Europa/USA/APAC, Katalog nennt bei WebHorizon auch Chile/Suedafrika; Sakura Japan. Geografische Einordnung K, keine Standortabnahme. Hetzner P-Vertiefung oben |
| PaaS / Shared Hosting statt allgemeinem Root-VPS (6) | [Render](https://render.com/docs/free), [Koyeb](https://www.koyeb.com/docs), [Railway](https://docs.railway.com/pricing/plans), [Fly.io](https://fly.io/docs/about/free-trial/), [serv00](https://www.serv00.com/), [HelioHost](https://heliohost.org/) | Plattform-/Accountregionen; Root, Kernel und persistente Disk nicht unterstellen. Nicht automatisch K3s-/Ansible-Bootstrap-Ziele |
| Entwicklungs-/CI-Umgebungen (2) | [github-vps](https://github.com/dwhr-pi/github-vps), [FreeVPS_by_Github-Action](https://github.com/dwhr-pi/FreeVPS_by_Github-Action) | Keine Dauer-VPS; separate P-Pruefung der GitHub-Grenzen in Abschnitt 6 |
| Broker-/Tradingzweckgebunden (4) | [ForexVPS](https://www.forexvps.net/free-forex-vps), [RoboForex](https://roboforex.com/clients/services/forex-vps/), [Orbex](https://www.orbex.com/en/trading-tools/free-vps), [Admirals](https://admiralmarkets.com/trading-platforms/forex-vps) | Konto-/Laender-/Equity-/Volumenvorgaben; Handelskosten/Verluste mitrechnen. Keine Empfehlung, Handelsvolumen fuer VPS zu erzeugen; Linux/Root/K3s U |
| Historisch (2) | [FreeMach](https://freemach.rowe.sh/), [FreeLiVPS](https://freelivps.com/) | Laut Katalog alte/ausgelaufene Angebote bzw. Domainwechsel; aktuelles Hosting U, nicht als verfuegbar gezaehlt |
| Als eigener Gratis-VPS ausgeschlossen (1) | [VPSWala](https://vpswala.org/blog/get/free-vps) | Katalog berichtet Affiliateweiterleitung zu Kamatera; hier nicht erneut geoeffnet, kein eigener Zuteilungsnachweis |

**Dimensionsabdeckung fuer alle K-only-Eintraege:** Die Kategorie liefert keine aktuelle Einzelpruefung. Je Angebot
bleiben aktuelle CPU/RAM/Disk/Architektur/OS/Root/GPU, Region/Kapazitaet, Karte/KYC,
Einrichtung/Steuer/IPv4/Traffic/Backup-/Overagekosten, Verlaengerung/Kuendigung/Erstattung, SLA/Restore, Bandbreite/Fair
Share, IPv4/IPv6/NAT/UDP/TUN/cgroups, API/Ansible, Erstregistrierung/Mehrfachkonten, kommerzielle Nutzung/Weiterverkauf
sowie Mining/Farming, KI-API/Inferenz/Training, Krypto-Tools/Full Nodes/Validatoren, privates Live-Trading/oeffentliche
Tradingplattform und VPN/Proxy/TOR/P2P **U, hier nicht am Original geprueft**. Das ist kein pauschales Verbot der
sonstigen Nutzung. Keine unkritisch fortgeschriebene Regelmatrix aus Sekundaerdaten.

### 4.1 Zwei direkt gelesene Community-Stichproben

**FreeVPS.org (P, undatiert, Abruf 18.11.2026):** Aktive LET-/LES-Mitgliedschaft, mindestens 3 Monate, 50 substantielle
Beitraege und 25 Thanks; auch Spenden umgehen diese Voraussetzungen nicht. Keine Karte laut Seite. Sponsor-AUP
zusaetzlich verbindlich; oeffentliche VPNs, TOR, Torrents, Mailrelays und Weiterverkauf/kommerzielle Weitergabe
untersagt. Kein SLA oder feste Bestandsdauer. Privates WireGuard wird dadurch nicht automatisch freigegeben;
Sponsorregel/UDP-Zuteilung offen. Registrierung ist keine belastbar vollautonome Sofortzuteilung. Die Flottenseite nennt
selbst unterschiedliche Nodezaehlungen; daraus keine belastbare freie Kapazitaetszahl bilden.
[Anbieterseite](https://www.freevps.org/)

**FOSSVPS (P, undatiert, Abruf 18.11.2026):** FOSS-Entwickler mit Forumreputation; nicht kommerziell, keine exzessive
CPU-/Disk-/Netzlast, kein SLA. Seite nennt 2 vCPU/4 GiB/64 GiB HDD, NAT plus IPv6 /128 oder /96 und
Debian/Ubuntu/Alpine. Die Standortliste enthaelt auch einen bereits vergangenen Sponsoringtermin (Bukarest 17.10.2026)
sowie Buffalo 22.11.2026; gelisteter Standort ist kein aktueller Zuteilungsbeleg. Das Katalogsignal einer erneuten
Bewerbung/Frist wurde hier nicht am Betreiberthread bestaetigt und bleibt K, nicht eigener Fristnachweis.
[Anbieterseite](https://fossvps.org/)

## 5. Registrierung und Einrichtung: dokumentierter Pruefpfad, nicht ausgefuehrt

1. Offizielle Anbieterquelle oeffnen, Vertragspartner/Land/Tarif und konkrete Nutzung bestimmen. Menschlichen
  Kontoinhaber mit echten Angaben, Vertragsannahme, MFA und erforderlichen Identitaets-/Zahlungsnachweisen vorsehen.
  Keine automatisierten Scheinbeitraege, CAPTCHA-Umgehungen, Kontingentvervielfachung oder Keepalive-Tricks.
2. Bei OCI Heimatregion/Always-Free-Label und **Summen** fuer Compute/Boot-/Blockvolumes pruefen. Bei GCP Billingstatus,
  Region, Disktyp und alle Zusatzressourcen betrachten. Bei Hetzner den gesamten Bruttopreis samt IPv4/Backups/Egress
  bestaetigen. Keine automatische Buchung aufgrund eines Kataloglabels.
3. Vor Einrichtung genehmigtes Bestandsziel bestimmen. Hostfingerprint ueber unabhaengigen Kanal abgleichen, privaten
  SSH-Schluessel und Inventory ausserhalb Git halten. Bei NAT externen SSH-Port vom internen Dienstport unterscheiden.
  Ein IPv6-only-Ziel erfordert einen passenden Clientpfad; NAT64/Proxy ist keine eingehende IPv4-Adresse.
4. Erst nach eigener Freigabe Architektur, OS, sudo, freien RAM/Disk, cgroups/Kernel und Netzzuteilung lesen. Root in
  einem Systemcontainer beweist keinen eigenen Kernel oder TUN. Fuer WireGuard UDP-Erreichbarkeit, Gegenstelle, Routing
  und MTU pruefen; beide Enden hinter ungeeignetem NAT bekommen nicht durch einen Einzeiler einen oeffentlichen Eingang.
  [WireGuard Quick Start](https://www.wireguard.com/quickstart/)
5. Geprueften Git-/nativen Buildpfad gemaess [Installationsrichtlinie](../INSTALLATION_POLICY.md) verwenden; keine
  Docker-/Compose-Neuinstallation und kein Docker-Fallback. Pins/Hashes, Besitz/Pfad/Ressourcen beachten. Fehlendes
  Buildrezept bleibt offen. Keine Dienst-, Tunnel-, Modell- oder Clusterstarts durch diese Dokumentation.
6. Ansible-Plan zuerst statisch/syntaktisch und hinsichtlich Seiteneffekten pruefen. `--check` ist Simulation, **keine
  garantierte Nichtaenderung beliebiger Playbooks**: Tasks mit `check_mode: false` koennen trotzdem aendern; `--diff`
  kann sensible Inhalte offenlegen. Freigabe, Secretschutz und Idempotenztest gesondert.
  [Ansible-Originaldokumentation](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_checkmode.html)
7. Erst nach genehmigter Einrichtung Zugang nach Neustart, kleinen erlaubten Dienst, Kostenbeobachtung und getrennten
  Restore testen. Trial/Erneuerung/Kuendigung dokumentieren. Stoppen ist nicht Loeschen; vorhandene Nutzdaten/Volumes
  nicht pauschal entfernen.

## 6. Pflichtreferenzen: GitHub ist kein Gratis-Dauer-VPS

Beide Repos wurden oeffentlich geoeffnet und in ihren sichtbaren README-Abschnitten gelesen, **nicht** geforkt,
gestartet oder vollstaendig sicherheitsgeprueft:

- [dwhr-pi/github-vps](https://github.com/dwhr-pi/github-vps): Codespaces-/Kali-/Docker-/Remotezugangsbeispiel; das
  "lifetime"-Versprechen ist nicht durch den Plattformvertrag gedeckt. Docker-basierter Weg ist keine freigegebene
  native Installation dieses Hauptrepos. Keine Passwort-/Root-/Tunnelbeispiele ungeprueft uebernehmen.
- [dwhr-pi/FreeVPS_by_Github-Action](https://github.com/dwhr-pi/FreeVPS_by_Github-Action): README beschreibt
  Remote-VM/SSH ueber Actions und selbst eine 6-Stunden-Grenze. Angaben zu alter Runnerhardware sind keine aktuelle
  Ressourcenzusage. Keine Workflows oder darin referenzierten Skripte ausgefuehrt.

**Codespaces:** GitHub Free fuer persoenliche Konten beinhaltet aktuell 120 Core-Stunden und 15 GB-Monate; 2 Kerne
verbrauchen den Stundenanteil mit Faktor 2 (rechnerisch 60 Laufzeitstunden, wenn sonst nichts genutzt wird). Speicher
zaehlt solange die Umgebung existiert, auch gestoppt. Organisationen haben nicht automatisch persoenliche
Freikontingente. Nach Freimengen gelten Zahlungs-/Budgetregeln; kein 24/7-Vertrag, keine garantierte feste oeffentliche
IP oder Produktions-SLA aus dem Repo ableiten. [GitHub Codespaces
Billing](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces)

**Actions:** GitHub-hosted Jobs haben aktuell maximal 6 Stunden; Speicher, Gleichzeitigkeit und Compute-Kontingente sind
planabhaengig. Die gelesene aktuelle Limits-Tabelle nennt fuer GitHub Free 12 USD eingeschlossene monatliche
Compute-Nutzung und 500 MB Artefaktspeicher, nicht pauschal die historisch oft genannten 2.000 Minuten. Self-hosted
Runner stellen keine kostenlose GitHub-Hardware bereit. [Actions
Limits](https://docs.github.com/en/actions/reference/limits)

**Zweckbindung:** Zusatzbedingungen, wirksam **27.08.2026**, untersagen Actions-Cryptomining und zweckfremde Last auf
GitHub-hosted Runnern; sie binden Nutzung an Softwareentwicklung/-tests und begrenzen weitere kommerzielle Dienstformen.
Auch Codespaces untersagt ausdruecklich Cryptomining, produktionsgerichtetes Hosting und entwicklungs-/testfremde
Nutzung. Ein Repo macht externen Dauerbetrieb oder Live-Trading nicht zulaessig. Keine automatischen Job-Neustarts,
Idle-Umgehungen oder Kontenwechsel zur Limitumgehung.
[GitHub-Zusatzbedingungen](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features)

## 7. Konkrete Erfahrungsquellen, getrennt von Anbieterangaben

| Quelle / Datierung | Tatsaechlich gelesener Befund | Aussagegrenze |
| --- | --- | --- |
| [Tutorial on how to setup an always-free server?](https://www.reddit.com/r/oraclecloud/comments/1nnjx3d/tutorial_on_how_to_setup_an_alwaysfree_server/) (E; Reddit zeigt nur relative Altersangaben, exaktes Datum hier U) | Ein Nutzer berichtet gescheiterte Kartenregistrierung, der Fragesteller dagegen erfolgreichen Zugang und Kostenverwirrung. Kommentare nennen alte 4/24-Werte | Einzelne widerspruechliche Erfahrungen, kein Beleg fuer globale Registrierungsquote; 4/24 nicht als aktuelles Limit uebernehmen. Hinweise auf Buchungs-Wiederholskripte nicht als Empfehlung |
| [Enable IPv4 Access in EUserv IPv6-only VS2-free](https://yoursunny.com/t/2020/EUserv-IPv4/) (E; Junxiao Shi, **10.12.2020**) | Autor dokumentiert damaligen Containerbetrieb mit nur IPv6 /128 und fehlendem direktem IPv4/NAT-Zugang; behandelt einen zusaetzlichen IPv4-Zugangsweg | Konkreter technischer Erfahrungsbericht, keine Neubestellbarkeit oder Kostenfreiheit 2026. Nicht als aktuelle Installationsfreigabe/Befehlspruefung verstanden |
| [VPN com WireGuard: O Guia Definitivo](https://otaviomiranda.com.br/2026/vpn-com-wireguard-o-guia-definitivo/) (E; Otavio Miranda, **14.03.2026**) | Autor beschreibt eigenes Netz mit sieben Nodes und verlinkt sein Video; Hub/Mesh, IPv4/IPv6 und NAT sind relevante Lernpunkte | Anbieterexterner Praxisbericht, **nicht wirtschaftlich neutral**: Hostinger-Werbung/Coupon vorhanden. Keine unabhaengige Provider-AUP-/Gratis-/Performanceabnahme |

Fuer GCP-Free-Tier und den konkreten aktuellen Hetzner-Tarif wurde in diesem begrenzten Review **kein hinreichend
passender unabhaengiger Langzeitbericht direkt geprueft**. Keine erfundene Nutzerzufriedenheitsbewertung. Anbieterforen
und Betreiberankuendigungen sind fuer Stoerungen interessant, aber nicht automatisch unabhaengige Erfahrungen.

## 8. YouTube: belegte Metadaten und offene Sichtung

Alle Eintraege sind **Fundstellen/Lernideen**, kein Nachweis ueber vollstaendig gesehene Videos, Transkripte, sichere
Befehle oder heutige Tarifgueltigkeit. Suchmetadaten werden ausdruecklich als M angegeben. Direkte Watch-Abrufe waren
teilweise nicht moeglich; daraus keine Sichtung ableiten. Uploaddatum und Blogdatum nicht gleichsetzen.

| Thema | Belegte Fundstelle und Metadaten | Nutzen / Evidenzgrenze |
| --- | --- | --- |
| Registrierung OCI, offizielle Einfuehrung | [Getting Started with Oracle Cloud Free Tier](https://www.youtube.com/watch?v=YnsN52hB8EY), **Oracle Developers**, **13.11.2023** (Titel/Kanal/Datum M aus YouTube-Suchergebnis) | Historischer Einstieg. Beschreibung nennt alte A1-Mengen; aktuelle 2/12-Dokumentation hat Vorrang. Kein Formularablauf von 2026 nachgeprueft |
| Registrierung OCI, weiterer Kandidat | [Getting Started with Oracle Cloud Free Tier](https://www.youtube.com/watch?v=So0OCWLRvzk), **ThinkOCI**, **14.08.2025** (M) | Beschreibung kuendigt Anmeldung und erste Dienste an; kein Konto-/Karten-/Gratisnachweis fuer den Leser |
| Ansible und K3s | [Raspberry Pi Cluster Ep 3 - Installing Kubernetes (K3s) on the Turing Pi](https://www.youtube.com/watch?v=N4bfNefjBSw), **Jeff Geerling**, **21.05.2020** (M) | Beschreibung/Kapitel nennen SSH, K3s und k3s-ansible. Pi-Labor, nicht VPS-/AUP-/NAT-Abnahme; alter Stand gegen heutige K3s-Dokumentation pruefen |
| WireGuard / NAT / IPv4-Ende | [Create Your Own VPN With WireGuard on Real Servers](https://www.youtube.com/watch?v=yqsLvVz0Y44), Titel und **19.03.2026** nur M; exakter Kanalname hier **U**. Autorblog verlinkt exakt dieselbe Video-ID (E, 14.03.2026) | Blog bestaetigt Bezug zu sieben Nodes und NAT; abweichendes Blog-/Uploaddatum offen benennen. Kein Kanalname aus Autorenname erraten; kein Transkript gelesen |
| IPv6 / deutscher Anschluss | [VPN trotz IPv6: WireGuard & UniFi Guide (Deutsche Glasfaser)!](https://www.youtube.com/watch?v=XeAZI4io5t8), Titel M; **Kanal und exaktes Uploaddatum U**, Watch-Abruf gedrosselt | Beschreibung nennt IPv6/WireGuard/UniFi. Reine Fundstelle, keine validierte Architektur- oder Befehlsanleitung; Proxyhinweise insbesondere nicht als WireGuard-UDP-Nachweis |

Technische Schlussfolgerungen fuer dieses Repo kommen aus den **Originaldokumentationen**, nicht aus behaupteten
Videoinhalten: kleiner Koordinator statt GPU-Versprechen; private Peer-Verbindungen statt oeffentlicher Managementports;
Ansible erst nach Ziel-/Kostenfreigabe; K3s nur mit belegten Kernel-/Netz-/Ressourcenrechten. Video-Lernpfade sind keine
Ausnahme von der nativen Installationsrichtlinie.

## 9. Datierter Originalquellen-Nachweis

Die IDs gelten fuer die Tabellen oben. Alle Quellen wurden am **18.11.2026** geprueft, mit folgendem tatsaechlichen
Umfang; P bedeutet keine vollstaendige juristische Vertragspruefung.

| ID | Originalquelle | Sichtbare Datierung / Pruefumfang |
| --- | --- | --- |
| O1 | [OCI Always Free Resources](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm) | Veroeffentlichungsdatum U; Compute/Shapes/Block-/Bootspeicher/Idle/IP-Abschnitte P |
| O2 | [OCI Free Tier FAQ](https://www.oracle.com/cloud/free/faq/) | Aenderungsdatum U; Registrierung/Karte/Ein-Konto-Regel/Trial/Support P |
| O3 | [Oracle Cloud Services Contracts](https://www.oracle.com/contracts/cloud-services/) | Datum U; Vertragsmodell/Land-/Produktauswahl P, konkreter Landesvertrag/AUP noch U |
| G1 | [Free Google Cloud features and trial offer](https://docs.cloud.google.com/free/docs/free-cloud-features) | Signup/Trial/Paid-Billing/Compute-Tabelle P; ausdruecklicher Stichtag 16.11.2026 fuer KI-Guthabenausschluss. Allgemeines Seitenaenderungsdatum hier U |
| G2 | [GCP Network pricing](https://cloud.google.com/vpc/network-pricing) | Datum U; IPv4-/NAT-/Transferpreisabschnitte P, keine komplette SKU-Kalkulation |
| G3 | [Google Cloud Terms of Service](https://cloud.google.com/terms/) | Konkretes Vertragsannahmedatum U; Restrictions/Mining/Kontingentumgehung/Anwendungsnutzung P |
| G4 | [Google Cloud AUP](https://cloud.google.com/terms/aup) | Versionsbereich nennt Last modified **12.10.2026**; allgemeine Verbote/Agentenbezug P |
| G5 | [Manage spend cap budgets](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps) | Last updated **10.11.2026 UTC**; Dienste, Grenzen, Weiterabrechnung, Overages und Reset P |
| H1 | [Hetzner Cloud and vServer Service Agreement](https://www.hetzner.com/legal/cloud-server/) | Aenderungsdatum U; SLA/Ausschluesse/Miningverbot P |
| H2 | [Hetzner Cloud Billing FAQ](https://docs.hetzner.com/cloud/billing/faq/) | Seitenkopf nennt Last change **07.07.2020**, Created 02.07.2020; aktuell ausgelieferte Abschnitte Abrechnung/Traffic/Primary-IP/Backups P. Kopfdatum nicht als Datum jeder Tarifregel verstehen |
| H3 | [Hetzner Terms and Conditions](https://www.hetzner.com/legal/terms-and-conditions/) | Versionsdatum U, Suchindexalter nicht als Vertragsdatum verwendet; Identitaet/Inhalte/Mining-Farming-Plotting/Backup/Drittnutzung P |
| H4 | Hetzner Price Adjustment 15 June 2026; historische Abruf-URL: `https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/` | **Nur M/K**: Index nennt erstellt 15.06.2026, geaendert 08.07.2026 und CX23-Preis. Direktabruf 404/nicht verfuegbar; kein aktiver Quellenlink und kein P |
| C1 | [FreeVPS.org](https://www.freevps.org/) | Datum U; Berechtigung/Regeln/Flottenliste P; keine Sponsor-AUP-Vollpruefung |
| C2 | [FOSSVPS](https://fossvps.org/) | Datum U; Regeln/Ressourcen/OS/Standorttermine P, Endtermine sind keine Zuteilungspruefung |
| T1 | [K3s Requirements](https://docs.k3s.io/installation/requirements) | Aenderungsdatum hier U; Hardware/cgroups/Netz P |
| T2 | [WireGuard Quick Start](https://www.wireguard.com/quickstart/) | Datum U; Peer-/NAT-/Keepalive-Konzept P; keine Befehlsausfuehrung |
| T3 | [Ansible check/diff mode](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_checkmode.html) | Dynamische `latest`-Doku, Datum U; Check-Ausnahmen/Diff-Risiko P |
| GH1 | [GitHub Codespaces Billing](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces) | Datum U; Freimengen/Core-Multiplikatoren/Speicher/Abrechnung P |
| GH2 | [GitHub Actions Limits](https://docs.github.com/en/actions/reference/limits) | Datum U; 6-Stunden-Jobs, planabhaengige Compute-/Speichergrenzen P |
| GH3 | [GitHub Terms for Additional Products and Features](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features) | Version Effective Date **27.08.2026**; Actions-/Codespaces-Abschnitte, insbesondere Zweckbindung P |
| GH4 | [github-vps](https://github.com/dwhr-pi/github-vps) und [FreeVPS_by_Github-Action](https://github.com/dwhr-pi/FreeVPS_by_Github-Action) | Datierung/Commit-Pin hier U; sichtbare README-Teile P, kein Workflow-/Skriptaudit und keine Nutzung |

**Fehlgeschlagene bzw. nicht inhaltlich abgenommene Abrufe:** Hetzner-Preisanpassung EN/DE; ein aelterer
Oracle-CSA-PDF-Link (404); veralteter GitHub-Zusatzbedingungen-Pfad (ersetzt durch GH3); mehrere direkte
YouTube-Watch-URLs (Fehler/Drosselung). Suchtreffer ersetzen diese Luecken nicht. Ein Vertragsportal ist nicht der
Inhalt aller darin verlinkten Vertraege.

**Sekundaerquelle separat:** Der lokale Free-VPS-Katalog und seine deutschen Begleittexte dienten der Inventarisierung
und als Recherchehinweise. Dessen Regeln/Preise/Erfahrungslinks sind nur dort P/E geworden, wo diese Review den
Originalinhalt selbst geoeffnet hat. Keine Dateien im Schwesterrepo geaendert und keine dortigen Pruefzeitstempel
fortgeschrieben.

## 10. Offene Punkte und naechste Freigaben

| Prioritaet / betroffener Einsatz | Erforderlicher Nachweis | Bis dahin |
| --- | --- | --- |
| Kritisch: unbeaufsichtigte Neuprovisionierung | Verbindliche und technisch durchgesetzte Gesamt-Kosten- und Laufzeitgrenze inkl. Disk/IP/Egress und Fehlerfaellen | Fail-closed fuer neue Ressourcen; vorhandene GET-/SSH-/configure-Pfade nicht pauschal sperren |
| Kritisch: Mining/Krypto/Validator/Live-Trading/oeffentliche Plattform | Aktuelle passende AUP/Landesvertrag, schriftliche Klaerung bei U und gesonderte regulatorische Pruefung | Nur die betroffene kritische Nutzung nicht starten; keine Wallet-/Boersenschluessel beschaffen |
| Kritisch: KI-Training/Dauerlast | Konkrete Tarif-/Lastfreigabe, Architektur, Modelllizenz, Ressourcen-/Kostenrahmen | Training nicht aus KI-Marketing ableiten; erlaubte Koordination separat behandeln |
| Hoch: WireGuard/K3s auf NAT-/Systemcontainern | Sponsor-AUP, UDP/IPv6/Clientpfad, Kernel/TUN/cgroups, Ports/MTU und Persistenz | Kein Tunnel-/Clusterstart aus blossem Root-/SSH-Label |
| Hoch: aktuelle Beschaffung | OCI-Kapazitaet, GCP-Billing-/SKU-Gesamtkalkulation, Hetzner-Endpreis inkl. Steuer/Nebenkosten | Keine Zusage zur Zuteilung oder kostenlosen Gesamtnutzung |
| Hoch: Produktionsdaten | Externes Backup, Restore, Neustart-/Zugangsabnahme und Ausfallplan | Keine alleinige Ablage auf fluechtigen Gratis-/Trialressourcen |
| Mittel: Katalogrest | Anbieter-Originale pro Angebot und pro Dimension nachpruefen; historische Kandidaten bereinigen nur in gesondertem Auftrag | K bleibt K; keine pauschale weltweite Angebots-/Erlaubnisbehauptung |
| Mittel: Lernmaterial | Watch-Seiten/Kanal/Datum nachpruefen; danach ggf. Video/Transkript und einzeln freigegebene native Befehle pruefen | M bleibt Fundstelle, nicht Befehlsreview |

Ergebnis dieser Arbeit ist ausschliesslich diese neue Dokumentation. Keine Anbieterfreigabe, kein Commit/Push, keine
Anpassung am Adapter, an Skripten oder am Free-VPS-Katalog.
