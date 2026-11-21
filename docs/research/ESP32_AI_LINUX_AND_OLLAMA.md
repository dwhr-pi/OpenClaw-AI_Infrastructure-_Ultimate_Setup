# ESP32-KI verstehen: Speicher, Linux-Tests und Ollama

Stand der Quellenpruefung: **19.11.2026**. Reine Hintergrunddokumentation, keine Installationsanleitung des Setups.

**Die vier hier besprochenen ESP-Projekte sind nicht Bestandteil dieses Setups und werden nicht aufgenommen.**
Es gibt dafuer keine Installationsplanung, Menueeintraege, Registry-Rezepte oder automatischen Downloads.
Dieser Beitrag fuegt auch keine Entwicklungsumgebung, Simulatoren, Modellgewichte oder Firmware hinzu.
Ollama ist ein bereits separat behandeltes Werkzeug; daraus entsteht keine fertige ESP32-Integration.
Eine Erfassung dieser Quellen in einem Dokumentationsinventar ist keine Aufnahme als installierbares Tool.

## Zwei grundverschiedene Architekturen

| Frage | Modell direkt auf dem ESP32 | ESP32 als Client eines Modellservers |
| --- | --- | --- |
| Wo werden die Modellgewichte verarbeitet? | Auf dem Mikrocontroller | Auf Linux-PC, Mac, MiniPC oder einem anderen Server |
| Was liegt auf dem ESP32? | Firmware, Modell, Tokenizer und Inferenzpuffer | Firmware, Verbindungsdaten, begrenzter Dialog und Hardwarelogik |
| Ist WLAN fuer jeden Modellschritt notwendig? | Nicht bei vollstaendig lokalem Modell | Ja, beziehungsweise eine andere Verbindung zum Server |
| Was ist der Engpass? | RAM, Speicherbandbreite, Flash und Rechenleistung | Netzwerk, JSON-/Audiopuffer, Serverlast und Zugriffsregeln |
| Was kann Linux ohne Board pruefen? | Modellmathematik und portable Laufzeit | Anfrageformat, Agentenlogik und simulierte Werkzeuge |
| Was beweist ein solcher Linux-Test nicht? | Geschwindigkeit oder Speicherverhalten des Chips | Korrekte reale GPIO-, Audio- oder Sensorfunktion |

Ein ESP32 ist kein kleiner Linux-Rechner. ESP-IDF-Firmware arbeitet typischerweise mit FreeRTOS;
ein Linux-Host kann sie bauen, fuehrt die erzeugte Chip-Binaerdatei aber nicht einfach nativ aus.
Ein Raspberry Pi mit Linux und ein ESP32 haben deshalb grundverschiedene Software- und Speichergrenzen.

## Einordnung der vier Quellen

### DaveBben/esp32-llm: sehr kleines Modell direkt auf dem Chip

Die [Projektbeschreibung][dave-readme] nennt ein TinyStories-Modell mit 260000 Parametern,
eine angepasste `llama2.c`-Laufzeit und ein ESP32-S3-Beispiel mit 2 MB PSRAM.
Die dort genannten **19,13 Tokens/s sind eine Messangabe des Autors**, kein eigener Benchmark.
Die verwendete Boardkonfiguration ist keine universelle Mindestanforderung fuer jedes ESP-Projekt.

Der [C-Quelltext][dave-runtime] liest das Checkpoint-Abbild in einen Speicherpuffer und legt
zusaetzliche Aktivierungs- und KV-Puffer an. Display, DSP und FreeRTOS sind chipbezogene Abhaengigkeiten.
Der ESP-Port ist daher kein unveraendertes Linux-Programm. Die verwandte
[llama2.c-Referenz][llama2] kann auf einem PC als Ausgangspunkt fuer Modellversuche dienen;
Dateiformat und Tokenizer muessen zur jeweils verwendeten Laufzeit passen.

Das ist ein Lehr- und Architekturbeispiel, kein allgemeiner Chatassistent. Kleine spezialisierte Modelle
sind deswegen nicht generell nutzlos: Eine eng begrenzte Aufgabe muss separat mit passenden Daten bewertet werden.
Eine eigene `LICENSE` im betrachteten Repository-Wurzelpfad wurde nicht gefunden.
Die Lizenz eines Ursprungsprojekts ist keine pauschale Lizenzbestaetigung fuer diesen Port oder seine Gewichte.

### slvDev/esp32-ai: Speicherhierarchie statt alles gleichzeitig im RAM

Das [TinyStories-Beispiel][slv-readme] nennt 28,9 Millionen gespeicherte Parameter,
8 MB PSRAM, 16 MB Flash und 14,9 MB Modellgroesse bei 4-Bit-Darstellung.
Die angegebenen **9,88 Tokens/s** sind ebenfalls ein Upstream-Bericht.
Der Ansatz nutzt Per-Layer Embeddings: Eine grosse Tabelle bleibt im Flash, waehrend pro Token
nur ausgewaehlte Zeilen benoetigt werden. Das ist kein auf den ESP32 portiertes vollstaendiges Gemma 3n.

Wichtig ist die Trennung der Modelle: TinyStories ist auf Geschichten ausgerichtet.
Das gesonderte [Barista-Modell][barista] hat laut Firmwaredokumentation **8,9 Millionen Parameter**,
einen begrenzten Ausgabewortschatz und eine andere Ein-/Ausgabeabbildung.
Es ist nicht einfach dasselbe 28,9-Millionen-Modell mit einem Espresso-Prompt.
Barista benoetigt neben Gewichten und Tokenizer passende Vokabular- und Layoutdateien.
Falsche Kombinationen duerfen nicht als sinnvolle Modellergebnisse bewertet werden.

Quellcode: MIT laut gelesener Lizenzdatei. Gewichte und Trainingsdaten sind getrennt zu lizenzieren.
Die ebenfalls enthaltene Fliegen-Konnektom-Demo ist kein Sprachmodell und kein Beleg fuer LLM-Faehigkeiten.

### espressif/esp-claw: Agentenlaufzeit mit externem Modell

Das [Repository unter Espressifs Organisation][claw-readme] beschreibt eine Agentenlaufzeit in C,
unterstuetzte Boards sowie OpenAI-/Anthropic-artige APIs und benutzerdefinierte Endpunkte.
Die Agentenlogik auf dem Chip ist nicht mit einem grossen Sprachmodell auf dem Chip gleichzusetzen.
Ein lokaler Ollama-Endpunkt ist ueber den passenden API-Vertrag prinzipiell ein pruefbarer Ansatz;
ein erfolgreicher Ende-zu-Ende-Test dieser Kombination wurde hier nicht durchgefuehrt.

Die gelesene Projektlizenz ist Apache-2.0. Der Name ESP-Claw bedeutet weder eine installierte
OpenClaw-Erweiterung noch eine zugesagte Integration in dieses Setup.

### lubluniky/esp32-harness: kompakter Hardware-Client

Die [Projektbeschreibung][harness-readme] trennt Agentenschleife und externes Modell:
JSON-Werkzeugaufrufe und UI laufen auf einem ESP32-S3-Cardputer; das Modell antwortet ueber
einen OpenAI-kompatiblen Endpunkt. Ollama wird ausdruecklich als moeglicher Server genannt.
Das gezeigte Board hat laut Quelle 512 KB SRAM, keinen PSRAM und 8 MB Flash.
Die Angabe von etwa 200 C++-Zeilen beschreibt den Anwendungskern, nicht den Umfang aller Bibliotheken.

Der beschriebene Weg verwendet bewusst unverschluesseltes HTTP. Das ist keine Empfehlung fuer
oeffentliche Netze oder ungeschuetzte Aktoren. Quellcode: MIT laut gelesener Lizenzdatei.
Weitere Netzwerk- und Hardwarepruefungen sind trotz kleiner Codebasis erforderlich.

## Wie der Speicher des ESP32 genutzt wird

| Speicherbereich | Typische Aufgabe | Grenze |
| --- | --- | --- |
| Internes SRAM | Haeufig benutzte Daten, Stacks, Aktivierungen und zeitkritische Puffer | Klein; Firmware, System und Kommunikation brauchen ebenfalls Platz |
| PSRAM | Groessere, veraenderliche Puffer und ausgewaehlte Gewichte | Langsamer als internes SRAM; Zugriff und Zuweisung muessen zur Plattform passen |
| Flash | Firmware, Tokenizer, Dateien und unveraenderliche Gewichtstabellen | Kein beliebig schneller RAM-Ersatz; Partitionen begrenzen den nutzbaren Platz |

Die [ESP-IDF-Dokumentation fuer externes RAM][psram] erklaert Speicherabbildung und
`MALLOC_CAP_SPIRAM`. Eine passende Zuweisungsstrategie ist notwendig; externer Speicher macht
nicht jeden Puffer automatisch kompatibel. Insbesondere Cache-, DMA- und Betriebssystemanforderungen
sind versions- und komponentenabhaengig. Der nominelle Board-Speicher ist nicht der freie Heap.

```text
On-Device-Modell, schematisch:
Flash: Firmware + Tokenizer + grosse, selten benoetigte Gewichtstabellen
                                  |
                                  v
PSRAM: ausgewaehlte Gewichte + groessere Arbeits-/Kontextpuffer
                                  |
                                  v
SRAM: haeufig benutzte Aktivierungen + kleine schnelle Arbeitspuffer
```

Eine reine Gewichts-Untergrenze laesst sich selbst berechnen:

```text
Gewichtsbytes ungefaehr = Parameterzahl * Bits_pro_Gewicht / 8
260000 Parameter * 4 Bytes bei FP32 = 1040000 Bytes
28900000 Parameter * 4 Bit / 8 = 14450000 Bytes
```

Quantisierung braucht zusaetzlich Skalen, Metadaten und eventuell nicht quantisierte Tensoren.
Ausserdem fehlen in dieser Rechnung Tokenizer, Logits, Aktivierungen, Stacks und Kontextspeicher.
MB bezeichnet hier dezimale Angaben; 1 MiB sind 1048576 Bytes. Unterschiedliche Einheiten nicht vermischen.
Flash fuer Firmware, Dateisystem und gegebenenfalls OTA-Partitionen ist ebenfalls einzuplanen;
ein 16-MB-Flash stellt nicht gleichzeitig 16 MB fuer Modell und nochmals 16 MB fuer Firmware bereit.

Fuer einen klassischen Attention-KV-Cache gilt als Naeherung:

```text
KV-Bytes = 2 * Schichten * Kontexttoken * KV-Koepfe * Kopfdimension * Bytes_pro_Element
```

Der Faktor 2 kommt von Key und Value. Rein rechnerisches Beispiel, nicht die Konfiguration der vier Projekte:
6 Schichten, 256 Token, KV-Gesamtdimension 128 und FP32 benoetigen dafuer 1572864 Bytes, also 1,5 MiB.
Laengerer Kontext kann deshalb schon ein winziges Modell ueber das RAM-Budget bringen.
Der [portable PLE-Hostpruefer][slv-verify] legt ebenfalls getrennte Key-/Value-Caches und Scratch-Puffer an.
Flash-Lesezugriffe laden unveraenderliche Daten; ein Schreiben des ganzen Modells pro Token ist nicht erforderlich.

## Was sich unter Linux testen oder simulieren laesst

### Modell und portable Laufzeit

Fuer numerische Tests ist ein Hostlauf oft aussagekraeftiger als eine komplette Chipemulation:
identischer Tokenizer, identische Gewichte, gleiche Quantisierung und feste Eingaben zuerst.
Der portable [PLE-Pruefer][slv-verify] vergleicht C-Logits mit Referenzwerten aus PyTorch.
Das untersucht Rechenergebnisse, nicht WLAN, Speicherbandbreite oder die reale Boardgeschwindigkeit.

Die [TinyStories-Forschungsdokumentation][slv-research] beschreibt Training, Sampling,
Quantisierungsbewertung und Export fuer den Host. Die gelesene [Paketdefinition][slv-package]
nennt Python ab 3.12 sowie unter anderem PyTorch. Das ist ein separater Forschungsweg,
kein Setup-Installer. Ein Linux-Host ist damit ein plausibler Testort; ausgefuehrt wurde er hier nicht.
Trainieren auf dem PC ist nicht Trainieren auf dem ESP32. Rohdaten, Tokenizer und Checkpoints
brauchen eigene Versions-/Hashnachweise; die Forschungsdokumentation nennt selbst Reproduzierbarkeitsgrenzen.

### Hosttests, UI-Simulation und QEMU sind verschiedene Dinge

| Pruefweg | Belegter Ansatz | Was offen bleibt |
| --- | --- | --- |
| Portable C-/Python-Inferenz | PLE-Hostpruefer oder passende llama2.c-Laufzeit | ESP-DSP, Cache, reale Latenz und Strombedarf |
| ESP-Claw-Hosttests | GCC/cJSON-Tests fuer Endpoint-/Runtime-Komponenten | Vollstaendiger Agent auf realem Board und echter Modellserver |
| ESP-Claw-Websimulator | Lua-/Display-/LVGL-Anwendungen mit simulierten Peripheriewerten | Vollstaendige Chipemulation und echte Sensor-/GPIO-Eigenschaften |
| ESP-IDF-Linux-Hostziel | Experimentelle, teilweise portierte Komponenten mit Mocks | Nicht jede ESP-API ist auf Linux vorhanden |
| Espressif-QEMU | ESP32-S3-CPU, Speicher und ausgewaehlte Peripherie | Boardbibliotheken, WLAN, PSRAM-/SIMD-Leistung und Timing einzeln pruefen |
| Reales Board | Firmware, Speicherbelegung, USB, Sensoren und Energiebedarf | Muss gesondert aufgebaut und gemessen werden |

Quellen: [ESP-Claw-Hosttests][claw-host], [Websimulator][claw-sim],
[native Emscripten-Beschreibung][claw-wasm], [ESP-IDF-Hostanwendungen][host-apps]
und [offizielle QEMU-Dokumentation fuer ESP32-S3][qemu].

Die aktuelle QEMU-Dokumentation nennt ausdruecklich ESP32-S3-Unterstuetzung.
Die pauschale Aussage, ESP32-S3 lasse sich unter Linux ueberhaupt nicht emulieren, waere daher falsch.
Das normale Cross-Kompilieren mit `idf.py build` ist trotzdem noch kein solcher Emulatorlauf.
Eine begrenzte Host-Speicherzuteilung oder `ulimit` allein bildet SRAM, PSRAM, Flash und Buslatenzen nicht nach.

Der ESP-Claw-Websimulator ist insbesondere kein Browser-LLM fuer die On-Device-Gewichte.
Sein dokumentierter Komfort-Startweg nutzt unter anderem Docker; dieser Weg wird hier nicht uebernommen.
Upstream dokumentiert auch einen separaten Emscripten-Build. Beides bleibt ausserhalb des Setups.
Dieser Beitrag startet weder Simulator, Browser, Firmwarebuild noch Hardware-Flashvorgang.

## Koennen die Modelle selbst in Ollama laufen?

**Nicht direkt aus den betrachteten ESP-Dateien; aber auch kein generelles Verbot fuer kleine Modelle.**
Ollama ist eine Inferenzlaufzeit mit unterstuetzten Architekturen und Importformaten,
kein allgemeiner Ausfuehrer beliebiger C-Inferenzprogramme. Die Modellgroesse allein entscheidet nicht.

| Fall | Einordnung |
| --- | --- |
| DaveBben-Checkpoint im llama2.c-Binaerformat | Kein direkt nachgewiesener Ollama-Import. Eine Konvertierung braucht exakte Architektur-, Tensor- und Tokenizer-Unterstuetzung. |
| slvDev-PLE-`model.bin` | Projektspezifische Architektur und Layout. Kein hier belegter GGUF-Konverter oder Ollama-Backendpfad. |
| Umbenennen von `.bin` nach `.gguf` | Keine Konvertierung; das Dateiformat und die Modelloperationen aendern sich dadurch nicht. |
| Eigenes kompatibles GGUF-/Safetensors-Modell | Prinzipiell ein anderer Importweg, sofern das aktuelle Backend Architektur und Tokenizer unterstuetzt. Kein Nachweis fuer die obigen Artefakte. |
| ESP32 als HTTP-Client eines vorhandenen Ollama-Modells | Ein API-/Netzwerktest, keine Ausfuehrung dieses Ollama-Modells auf dem ESP32. |

Die [Ollama-Importdokumentation][ollama-import] beschreibt GGUF und Safetensors.
Auch ein formal gueltiger Container beweist keine Unterstuetzung aller Modelloperationen.
Fuer PLE waere gegebenenfalls echte Backend-/Konverterentwicklung noetig, nicht nur ein `Modelfile`.
Fuer einen Vergleich derselben winzigen Gewichte ist die passende Linux-Referenzlaufzeit daher
der naheliegendere Forschungsweg; fuer einen ESP-Client kann Ollama ein anderes Modell bereitstellen.

## Ollama-Vertrag zuerst ohne ESP pruefen

Nur als manuell freizugebendes Laborbeispiel mit **bereits laufendem lokalem Ollama** und
**bereits vorhandenem lokalem Modell**, ohne Cloudroute. Hier wird nichts ausgefuehrt oder eingerichtet.
Zuerst Modellnamen nachsehen, danach den Platzhalter im zweiten Aufruf ersetzen:

```bash
curl --fail --silent --show-error --connect-timeout 5 --max-time 15 \
  http://127.0.0.1:11434/api/tags
```

```bash
curl --fail --silent --show-error --connect-timeout 5 --max-time 60 \
  http://127.0.0.1:11434/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"BEREITS_LOKAL_VORHANDENES_MODELL","messages":[{"role":"user","content":"Antworte kurz mit Hallo."}],"stream":false,"max_tokens":32}'
```

Der zweite Aufruf fuehrt nach manueller Freigabe eine echte lokale Inferenz aus.
Er startet keinen Ollama-Dienst und enthaelt keinen Modell-Pull. Das curl-Zeitlimit begrenzt den Client,
nicht zwingend die gesamte weitere Serverarbeit. Ein Server ohne freigegebenes lokales Modell ist kein fertiger Test.
Die [OpenAI-Kompatibilitaetsdokumentation][ollama-api] beschreibt nur einen Teil der API.
Ein erfolgreicher Textaufruf beweist deshalb noch kein korrektes Tool-Calling oder Streaming.

Auf dem ESP32 bezeichnet `127.0.0.1` den Chip selbst, nicht den Linux-Rechner.
Fuer ein spaeteres externes Labor braucht es einen kontrollierten Netzwerkpfad zum Server oder Gateway.
Basis-URL wie `http://SERVER-IP:11434/v1` und vollstaendige Request-URL mit `/chat/completions`
nicht verwechseln: Ob der Client den Pfad anhaengt, ist im jeweiligen Quellstand zu pruefen.
Keine pauschale Oeffnung von Port 11434 oder Bindung an alle Interfaces wird hier eingerichtet.

## Speicher und Sicherheit beim Clientweg

Das Modell bleibt auf dem Server; deshalb benoetigt der ESP32 nicht dessen Gewichts- oder KV-Speicher.
Trotzdem wachsen Nachrichtenhistorie, JSON, TLS, Audio und Displaypuffer. Antwortgroesse und Kontext
messen und begrenzen; Streaming oder gefiltertes Parsing spart nicht automatisch jeden Zwischenpuffer.
Ein kleines Clientprogramm ist keine Sicherheitsfreigabe.

Ein spaeteres eigenes Labor sollte IoT-Netz und Serverzugriff trennen, TLS und authentifizierte
Gateways pruefen und keine Provider-Schluessel in Git oder Firmwarebeispiele uebernehmen.
Tool-Calling braucht feste lokale Allowlists, Wertebereiche, Zeitlimits und begrenzte Schleifen.
Unbekannte Toolnamen und ungueltiges JSON ablehnen; keine Modellantwort als freien Shell-/Lua-Auftrag behandeln.
Sicherheitskritische Aktoren nicht allein von probabilistischen Modellentscheidungen abhaengig machen.
Netzausfall, Neustart und wiederholte Antwort muessen definierte, sichere Zustaende haben.

## Was hier tatsaechlich geprueft wurde

Gelesen wurden die unten verlinkten Projektbeschreibungen und ausgewaehlte Quell-/Hostpruefdateien
sowie offizielle ESP-IDF-/Ollama-Dokumentation. Die angegebenen Quellpins identifizieren den Lesestand,
nicht einen geprueften Installer. Geschwindigkeiten und Modellangaben sind Upstream-Aussagen.

**Nicht durchgefuehrt:** Installation, Training, Modell-Download, Inferenz, Emulatorlauf,
Boardzugriff, Flashen, GPIO-Aktion oder Verbindung zu einem Modellanbieter.
Ein kuenftiger externer Test muesste Gewichte/Tokenizer, numerische Ergebnisse, Peak-RAM,
Flashpartitionen, Zeit bis zum ersten Token, Tokens/s und Energiebedarf getrennt nachweisen.
Diese Erlaeuterung ist keine Zusage, solche Tests oder Tools in das Setup aufzunehmen.

| Projekt | Gelesener Commit | Lizenzpruefung des Codes |
| --- | --- | --- |
| DaveBben/esp32-llm | `934dab4d242d259abd88678488ea3b62d4fca601` | Eigene LICENSE am gelesenen Wurzelpfad nicht nachgewiesen |
| slvDev/esp32-ai | `52ebcbbd905270592c1d415efd1128d04d0fa365` | MIT |
| espressif/esp-claw | `50072775cfa20d7ce25a9b27591d9d7c8b9dbab5` | Apache-2.0 |
| lubluniky/esp32-harness | `dfd7cc6fac7a387130d5997a81edddab845ab892` | MIT |

Weiter: [Speicher und Offloading im Linux-Cluster](../memory/UNIFIED_MEMORY_AND_OFFLOADING.md),
[Hardware-Entscheidungsbaum](../HARDWARE_DECISION_TREE.md), [Dokumentationswegweiser](../readme.md).

[dave-readme]: https://github.com/DaveBben/esp32-llm/blob/934dab4d242d259abd88678488ea3b62d4fca601/README.md
[dave-runtime]: https://github.com/DaveBben/esp32-llm/blob/934dab4d242d259abd88678488ea3b62d4fca601/main/llm.c
[slv-readme]: https://github.com/slvDev/esp32-ai/blob/52ebcbbd905270592c1d415efd1128d04d0fa365/README.md
[barista]: https://github.com/slvDev/esp32-ai/blob/52ebcbbd905270592c1d415efd1128d04d0fa365/firmware/esp32_barista/README.md
[slv-verify]: https://github.com/slvDev/esp32-ai/blob/52ebcbbd905270592c1d415efd1128d04d0fa365/runtime/host_verify/verify.c
[slv-research]: https://github.com/slvDev/esp32-ai/blob/52ebcbbd905270592c1d415efd1128d04d0fa365/research/tinystories/README.md
[slv-package]: https://github.com/slvDev/esp32-ai/blob/52ebcbbd905270592c1d415efd1128d04d0fa365/pyproject.toml
[claw-readme]: https://github.com/espressif/esp-claw/blob/50072775cfa20d7ce25a9b27591d9d7c8b9dbab5/README.md
[claw-host]: https://github.com/espressif/esp-claw/blob/50072775cfa20d7ce25a9b27591d9d7c8b9dbab5/components/claw_modules/claw_endpoint/test_host/run_tests.py
[claw-sim]: https://github.com/espressif/esp-claw/blob/50072775cfa20d7ce25a9b27591d9d7c8b9dbab5/pages/simulator/README.md
[claw-wasm]: https://github.com/espressif/esp-claw/blob/50072775cfa20d7ce25a9b27591d9d7c8b9dbab5/tools/lua_lvgl_web_sim/README.md
[harness-readme]: https://github.com/lubluniky/esp32-harness/blob/dfd7cc6fac7a387130d5997a81edddab845ab892/README.md
[llama2]: https://github.com/karpathy/llama2.c
[psram]: https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/external-ram.html
[host-apps]: https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/host-apps.html
[qemu]: https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/tools/qemu.html
[ollama-import]: https://docs.ollama.com/import
[ollama-api]: https://docs.ollama.com/api/openai-compatibility
