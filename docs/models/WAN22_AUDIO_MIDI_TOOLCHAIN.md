# Wan2.2, MIDI, Vocoder und Musikwerkzeuge

Quellenpruefung: **17.11.2026**. Statische Quellcode-/Dokumentationspruefung,
keine Installation, kein Audio-/GPU-Test. Ergaenzung zum
[eigenen Lyrics-/MIDI-Forschungsplan](SONGSAGE_MIDI_RESEARCH.md).

## Ergebnis fuer Wan2.2

**Audiokomponenten: ja. MIDI-Komposition und Harmonizer: im geprueften Stand
nicht gefunden. Vocoder: als Abhaengigkeit beziehungsweise in optionaler TTS.**
Das ist differenzierter als die Aussage, Wan habe ueberhaupt keine Audiotechnik.
Es macht Wan2.2 aber nicht zu einer MIDI-DAW oder einem eigenstaendigen Songgenerator.

Gepruefter Wan2.2-Commit: `1ea34ff48f87168174e12956e200b1d908b1c5ff`.
Der Review-Pin ersetzt keinen bestehenden Setup- oder Gewichts-Pin.

| Frage | Quellbefund | Was daraus nicht folgt |
| --- | --- | --- |
| Verarbeitet Wan Audio? | `AudioEncoder` liest Audio ueber librosa und nutzt Wav2Vec2-Merkmale fuer die Videokonditionierung | Keine MIDI-Noten oder neue Begleitmusik |
| Ist WORLD erwaehnt? | `pyworld` steht in `requirements_s2v.txt` | Kein belegter direkter WORLD-Aufruf im Wan-eigenen Python-Code |
| Gibt es einen neuronalen Vocoder? | Wan kann CosyVoice2 als TTS laden; die separat gepruefte CosyVoice-Codebasis verwendet `hift` | Kein Harmonizer und kein Gesangs-/MIDI-Modell allein durch diese Anbindung |
| Gibt es MIDI oder Harmonizer? | Keine Treffer fuer MIDI-/Mido-/MidiTok-, Harmonizer- oder Pitch-Shifting-Begriffe in den unten beschriebenen Textquellen | Kein Beweis ueber unbekannte Plugins, andere Versionen oder transitive Pakete |
| Wird Sprache synthetisiert? | Optionales `tts()` erzeugt eine WAV-Datei ueber CosyVoice; Wan verbindet Audio und Video | Keine instrumentale Komposition oder automatische Akkordbegleitung |

Primaerquellen am Wan-Review-Pin:

| Quelle | Pruefzweck |
| --- | --- |
| [Audioencoder](https://github.com/Wan-Video/Wan2.2/blob/1ea34ff48f87168174e12956e200b1d908b1c5ff/wan/modules/s2v/audio_encoder.py) | Audioeingabe und Merkmale |
| [Speech-to-Video und TTS](https://github.com/Wan-Video/Wan2.2/blob/1ea34ff48f87168174e12956e200b1d908b1c5ff/wan/speech2video.py) | Optionale Synthese und Video |
| [S2V-Abhaengigkeiten](https://github.com/Wan-Video/Wan2.2/blob/1ea34ff48f87168174e12956e200b1d908b1c5ff/requirements_s2v.txt) | WORLD-/Audio-Pakete |

## Vocoder ist nicht gleich Vocoder

| Begriff | Aufgabe | Beispiel fuer unsere Planung |
| --- | --- | --- |
| Klassischer Effekt-Vocoder | Formant-/Spektralmerkmale eines Modulators auf einen Traeger uebertragen | Sprachaufnahme plus Synthesizer als Effekt |
| Analyse-/Synthese-Vocoder | Sprachparameter analysieren und daraus Klang rekonstruieren | WORLD/pyworld fuer F0, Spektrum und Resynthese |
| Neuronaler Vocoder | Akustische Merkmale in eine Wellenform umsetzen | HiFT-Stufe in CosyVoice |
| Harmonizer | Zusaetzliche, gezielt transponierte Stimmen erzeugen | Pitch-Shifter plus Mehrstimmen-/Akkordsteuerung |
| MIDI-Sequencer | Zeitlich geordnete Noten und Steuerdaten bearbeiten | Editor oder eigenes symbolisches Modell |

"Vocalcoder" ist kein eindeutiger Quellcodebegriff. Voice Conversion, Vocoder,
Sprachsynthese und Gesangssynthese nicht gleichsetzen.
Ein Pitch-Shifter allein entscheidet noch nicht musikalisch passende Akkorde.

CosyVoice wurde getrennt am Commit
`074ca6dc9e80a2f424f1f74b48bdd7d3fea531cc` betrachtet:

| Quelle | Pruefzweck |
| --- | --- |
| [Modellklassen mit HiFT](https://github.com/FunAudioLLM/CosyVoice/blob/074ca6dc9e80a2f424f1f74b48bdd7d3fea531cc/cosyvoice/cli/model.py) | Neuronale Audioausgabe |

Das ist **nicht** ein von Wan fest gesperrter Dependency-Commit.
Wan-eigenes `load_tts()` kann fehlende CosyVoice-Quellen und Gewichte nachladen;
der [Downloader](https://github.com/Wan-Video/Wan2.2/blob/1ea34ff48f87168174e12956e200b1d908b1c5ff/wan/utils/utils.py)
verwendet fuer den Quellclone `main` und rekursive Submodule.
Ein solcher Aufruf wurde hier nicht ausgefuehrt. Fuer eine Setup-Integration
sind getrennte Pins, Hashes, Download-Freigabe, Modell-/Stimmenrechte und eine
pruefbare Abhaengigkeitskette erforderlich. Kein ungeprueftes `--enable_tts` starten.

## Werkzeuge aus deiner Setup-Sammlung

Grundlage ist die Registry `config/tools.yml` mit den verlinkten Toolseiten.
**Registriert bedeutet nicht auf deinem Rechner installiert oder betriebsbereit.**
Es wurde kein WSL-System inventarisiert und keine Modellinferenz ausgefuehrt.

| Vorhandener Eintrag | Rolle in einer Musikpipeline | Tatsaechliche Grenze |
| --- | --- | --- |
| [ACE-Step 1.5](../tools/ace-step-15.md) | Kandidat fuer direkt erzeugte Musik/Songs | Basispaket und Runtime/Gewichte unterscheiden; kein GPU-/Musiknachweis |
| [YuE](../tools/yue.md) | Gesungene Musik aus Lyrics-/Stilvorgaben | Setup-Pin ist YuE-v1, nicht das inzwischen andere YuE2-main; Quellbereitstellung |
| [MusicGen](../tools/musicgen-source.md) | Musik aus Text, je nach Modell mit melodischer Konditionierung | Quellenweg; Code MIT, Gewichte CC-BY-NC-4.0, kein garantierter Lyrics-Gesang |
| [LeVo_2](../tools/levo-2.md) | Forschungsansatz fuer vollstaendige Songs | Quellenweg; nichtkommerzielle Forschungs-/Bildungsgrenzen beachten |
| [Stable Audio Open](../tools/stable-audio-open.md) | Audio-/Loop-/Klangbausteine je nach Checkpoint | Bibliothek ist nicht das Modell; Modelllizenz separat |
| [AudioLDM2](../tools/audioldm2.md) | Text-to-Audio und musikalische Klangentwuerfe | Basispaket ohne komplette Laufzeit; keine Songqualitaetsabnahme |
| [AudioGen](../tools/audiogen.md) | Geraeusche und Klanglandschaften | Kein allgemeiner Gesangs-/Songgenerator |
| [OpenUtau und DiffSinger](../tools/local-audio-chain.md) | Noten-/Lyrics-Arrangement und Gesangssynthese | Quellen vorhanden; Voicebanks, Runtime und Rendering separat offen |
| [RVC und Seed-VC](../tools/local-audio-chain.md) | Klangfarbe einer vorhandenen Stimme umwandeln | Keine eigenstaendige Komposition; Referenzstimme und Modellrechte klaeren |
| [UVR5 und FFmpeg](../tools/local-audio-chain.md) | Stems trennen, mischen, messen und exportieren | Separation braucht Modelle; kein autonomes Komponieren |
| [MOSS-Music](../tools/moss-music.md) | Musik beschreiben, Lyrics transkribieren, Struktur analysieren | Musikverstehen, nicht Songgenerierung |
| [SongSage](../tools/songsage.md), [Lyrics-Pruefer](../CREATIVE_LYRICS.md) | Forschungsreferenz beziehungsweise formale Textpruefung | SongSage gesperrt; Reim-/Silbenpruefung erzeugt kein Audio |
| [SongRec](../tools/songrec.md), [Dejavu](../tools/dejavu.md) | Vorhandene Aufnahmen erkennen | Fingerprinting, kein Generator und kein Originalitaetsbeweis |

Fuer einen ersten Audiovergleich **ACE-Step 1.5 und YuE-v1** als getrennte,
bewusst freizugebende Kandidaten vorsehen. Fuer bearbeitbare Noten und Lyrics
ist die bestehende OpenUtau-/DiffSinger-Kette naheliegender als Wan.
Das sind Architekturvorschlaege, keine hier gemessene Rangliste oder Zusage
kompatibler Hardware. Weitere TTS-Eintraege der Sammlung sind Sprachwerkzeuge;
Sprachsynthese allein belegt keine kontrollierte Gesangssynthese.

## Fehlende Open-Source-Bausteine ergaenzt

Die folgenden Projekte fehlen als eigenstaendige IDs in der geprueften Registry.
Sie sind hier **neu als Entwicklungskandidaten aufgenommen**, noch nicht als
installierbare Menuepunkte oder ausgefuehrte Installationen.
OpenUtau, DiffSinger, RVC, Seed-VC, UVR5 und FFmpeg werden nicht doppelt angelegt.

| Kandidat / Originalquelle | Aufgabe | Gelesener Lizenzstand | Einordnung und offene Arbeit |
| --- | --- | --- | --- |
| [MidiTok](https://github.com/Natooz/MidiTok) | MIDI-Ereignisse tokenisieren/decodieren | [MIT](https://github.com/Natooz/MidiTok/blob/main/LICENSE) | Prioritaet 1: Roundtrip und Training; Abhaengigkeiten/Pins noch festlegen |
| [Mido](https://github.com/mido/mido) | MIDI-Dateien und Nachrichten lesen/schreiben | [MIT](https://github.com/mido/mido/blob/main/LICENSE) | Prioritaet 1: Parser/Exporter, keine KI und keine Klangerzeugung |
| [FluidSynth](https://github.com/FluidSynth/fluidsynth) | MIDI mit SoundFont rendern | [LGPL-2.1](https://github.com/FluidSynth/fluidsynth/blob/master/LICENSE) | Prioritaet 1: Soundbank-Lizenz und Offline-Rendering separat pruefen |
| [WORLD](https://github.com/mmorise/World) | F0-/Spektralanalyse und Sprachresynthese | [BSD-3-Clause-Bedingungen](https://github.com/mmorise/World/blob/master/LICENSE.txt) | Vocoder-Baustein, keine automatische Gesangskomposition; Wrapper separat pinnen |
| [Rubber Band](https://github.com/breakfastquay/rubberband) | Tonhoehe und Zeit unabhaengig veraendern | [GPL-2.0-or-later; alternative kommerzielle Lizenz](https://github.com/breakfastquay/rubberband/blob/default/README.md) | Pitch-Baustein fuer Harmonizer; Mehrstimmen-/Akkordlogik fehlt noch |
| [Ardour](https://github.com/Ardour/ardour) | Audio-/MIDI-DAW, Arrangement und Plugin-Host | [GPL-2.0-or-later](https://github.com/Ardour/ardour/blob/master/COPYING) | Desktop-/Audiogeraete-Integration getrennt von WSL-Training pruefen |
| [LMMS](https://github.com/LMMS/lmms) | Piano Roll, Sequencer, Synthesizer und Arrangement | [GPL-2.0-Familie](https://github.com/LMMS/lmms/blob/master/LICENSE.txt) | Alternative DAW, kein autonomes Musikmodell |
| [Calf Studio Gear](https://github.com/calf-studio-gear/calf) | Effekt-Plugins einschliesslich [Vocoder](https://calf-studio-gear.org/doc/Vocoder.html) | LGPL-2.1/GPL-2.0-Dateien; pro Komponente pruefen | Legacy/EOL-Hinweis wegen GTK2; nicht als neue Standardbasis empfehlen |
| [CosyVoice](https://github.com/FunAudioLLM/CosyVoice) | Sprachsynthese mit neuronaler Vocoder-Stufe | [Apache-2.0-Code](https://github.com/FunAudioLLM/CosyVoice/blob/074ca6dc9e80a2f424f1f74b48bdd7d3fea531cc/LICENSE) | Optionaler Sprechtext, kein belegter Song-/MIDI-Generator; Gewichte separat |

Calf verweist selbst auf einen Nachfolger; dessen Funktions-/Lizenzabnahme ist
hier nicht durchgefuehrt. Fuer einen neuen Harmonizer zuerst Rubber Band plus
eigene, testbare Mehrstimmensteuerung untersuchen, statt eine Legacy-UI zu priorisieren.
Quellenlizenzen sind keine Lizenz fuer beliebige Voicebanks, SoundFonts,
Trainingsdaten oder Stimmen. Auch ein Open-Source-Renderer kann Rechte an
seinen geladenen Inhalten nicht stellvertretend erteilen.

## Geplanter Ausbau ohne Scheininstaller

1. MidiTok und Mido: feste Quellen-/Abhaengigkeitspins, Parsergrenzen und Roundtrip-Fixtures ausarbeiten.
2. FluidSynth: Source-Build, freigegebene Soundbank und deterministischen Render-Test vorbereiten.
3. Ardour oder LMMS: Zielplattform und Desktop-/Audioanbindung bewusst auswaehlen.
4. WORLD und Rubber Band: kontrollierte Stimme/Pitch-Tests und Mehrstimmenlogik entwerfen.
5. Erst danach eigene Installer mit Plan, Zustimmung, Status, Doctor und datenerhaltendem Lifecycle aufnehmen.

Aktuell gibt es fuer diese neun neuen Kandidaten durch diese Aenderung **keine
Installer oder Buildfreigabe**. Vor einem Menueeintrag muessen Herkunft, exakte
Pins, Hashes, Build-Lock/SBOM, Plattformvertrag und echte Runtime-Grenzen feststehen.
Native GitHub-Source-Builds bleiben Vorgabe; kein Docker-Fallback.
Kein Modell-, Plugin-, Browser-, Audio-, Trainings- oder Dienststart durch diese Seite.

## Pruefprotokoll und Grenzen

Der Wan-Commit wurde ueber die GitHub-API aufgeloest und als ZIP nur im Speicher
gelesen, ohne Checkout, Archivextraktion oder Ausfuehrung von Fremdcode.
Archivumfang: **8.522.493 Bytes**, SHA256:
`59757c3e54140a9d219432e678aa5b50fac4dd56481c91a95bfb2c923d7e4d7a`.
Der Hash dokumentiert die gelesenen Bytes, keinen unabhaengigen Vertrauensnachweis.

Gelesen wurden **66 Textdateien mit 770.140 unkomprimierten Bytes** aus
`.py`, `.txt`, `.md`, `.json`, `.yaml`, `.yml` und `.toml`.
Gesucht wurden unter anderem MIDI, Mido, MidiTok, Harmonizer, Vocoder,
Vocalcoder, pyworld und Pitch-Shifting-Begriffe. Der Treffer `pyworld` stand nur
in der oben verlinkten Requirements-Datei. Audioencoder, TTS-Steuerung und
Downloader wurden zusaetzlich im Zusammenhang gelesen.

Negative Suchtreffer sind keine formale Vollstaendigkeitsgarantie:
Modellgewichte, Binaerdateien, nicht ausgecheckte Submodule, externe Plugins und
die gesamte transitive Laufzeit wurden nicht analysiert. CosyVoice ist eine
separat betrachtete externe Quelle, nicht Teil der 66 Wan-Textdateien.
Die API-Quelle ist der vollstaendige Git-Baum:

| Quelle | Umfang |
| --- | --- |
| [Git-Baum](https://api.github.com/repos/Wan-Video/Wan2.2/git/trees/1ea34ff48f87168174e12956e200b1d908b1c5ff?recursive=1) | Dateiliste des Review-Pins |

Anbieter-Demos und Suchtreffer wurden nicht als lokale Betriebsnachweise verwendet.
