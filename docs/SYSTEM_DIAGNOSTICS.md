# Systemangaben in Installationsprotokollen

Neue vom Setup angelegte Operationslogs enthalten vor Speicherpruefung und Installerstart
eine feste, nur lesende Systemdiagnose. Alte Logs werden nicht nachtraeglich umgeschrieben.

- Distribution: `PRETTY_NAME`, `ID`, `ID_LIKE`, `VERSION_ID`, `VERSION_CODENAME`.
- Laufzeit: System, Architektur, Kernel und WSL-Erkennung anhand der Kernelkennung.
- Python: tatsaechlich fuer die Diagnose verwendete Version und Interpreterpfad.
- Paketbasis: vorhandene Pfade zu `apt-get`, `dpkg-query` und `apt-cache` oder explizit fehlend.
- Debian-Familie und erkannter DietPi-Marker werden getrennt vom zugrunde liegenden OS ausgegeben.

Der Standardparser liest `/etc/os-release` beziehungsweise den Systemfallback
`/usr/lib/os-release`, ohne Shellcode daraus auszufuehren. Bei DietPi wird zusaetzlich
das Vorhandensein von `/boot/dietpi/.version` erkannt; die Datei wird nicht ausgefuehrt.
Die gemeldete Debian-Basisversion ist nicht die DietPi-Softwareversion.
Unbekannte Werte bleiben `unbekannt`; eine nicht erkannte WSL-Kennung beweist kein natives Linux.
Keine Keys, Umgebungsvariablen-Sammlung, Hostnamen, Netzadressen oder Benutzerkonfigurationen.
Steuerzeichen werden entfernt beziehungsweise ersetzt und Feldlaengen begrenzt.

## Diagnose ohne Installation

Im bereits geprueften Setup-Verzeichnis:

```bash
python3 -I -B scripts/helpers/system_diagnostics.py
```

Dieser Befehl installiert nichts, fragt kein sudo an und startet keine Dienste,
Modelle, Provider, Cluster oder WSL-Instanzen. Ausgabe bei Rueckfragen zum Fehlerlog beifuegen.

## Debian, DietPi und andere Derivate

Debian, Ubuntu, DietPi und deklarierte Debian-/Ubuntu-Derivate werden bei der
Diagnose beruecksichtigt. `ID_LIKE=debian` bedeutet aber nicht, dass eine Ubuntu-Paketliste,
ein Compilerstand oder ein GPU-/Kernelrezept unveraendert funktioniert.
Die Paketphase erkennt die Debian-/Ubuntu-Familie statt nur eines exakten Releases.
Fuer andere Basen als Ubuntu 24.04 folgt nach Zustimmung und Aktualisierung des
Paketindex vor der Installation eine apt-Simulation mit `--no-remove`.
Fehlende Pakete, nicht aufloesbare Abhaengigkeiten oder Werkzeugfehler stoppen den Lauf.
Keine Fremd-Paketquellen, kein Entfernen bestehender Pakete oder Austausch von Standard-Python.
Unter Ubuntu 26.04 und vergleichbaren Systemen verwendet Outlines bei Bedarf eine
private Python-3.13-Basis statt Python 3.14. Auf Ubuntu 24.04 bleibt die zusaetzliche
Python-3.12-Paketbasis vorgesehen. Beides nur nach Freigabe im Setup.
Erkennung und Paketaufloesung sind keine echte Build-/Runtime-Abnahme.

## Geplante Infrastrukturwerkzeuge

Ein `GEPLANT / NICHT INSTALLIERBAR` gekennzeichneter Menueeintrag wird bereits vor
einer Installationstransaktion erklaert. Der Hinweis ist keine Installation;
es gibt keinen Installiert-Marker und keine vorgetaeuschte Runtime-Abnahme.
Insbesondere sind cert-manager, External_DNS und Kyverno noch offene Build-/Lifecycle-Aufgaben.
Siehe [Infrastruktur-Kandidaten](tools/infrastructure-candidates.md).
