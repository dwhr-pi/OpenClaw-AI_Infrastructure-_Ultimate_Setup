# Systemangaben in Installationsprotokollen

Neue vom Setup angelegte Operationslogs enthalten vor Speicherpruefung und Installerstart
eine feste, nur lesende Systemdiagnose. Alte Logs werden nicht nachtraeglich umgeschrieben.

- Distribution: `PRETTY_NAME`, `ID`, `ID_LIKE`, `VERSION_ID`, `VERSION_CODENAME`.
- Laufzeit: System, Architektur, Kernel und WSL-Erkennung anhand der Kernelkennung.
- Python: tatsaechlich fuer die Diagnose verwendete Version und Interpreterpfad.
- Paketbasis: vorhandene Pfade zu `apt-get`, `dpkg-query` und `apt-cache` oder explizit fehlend.
- Debian-Familie und erkannter DietPi-Marker werden getrennt vom zugrunde liegenden OS ausgegeben.
- Sandbox-Metadaten: gVisor-Kernel-/Architekturgrenze, KVM-Geraetetyp/-Zugriffsrechte
  und sichtbare Namespace-Marker; kein Runtime- oder Virtualisierungsfunktionstest.

Der Standardparser liest `/etc/os-release` beziehungsweise den Systemfallback
`/usr/lib/os-release`, ohne Shellcode daraus auszufuehren. Bei DietPi wird zusaetzlich
das Vorhandensein von `/boot/dietpi/.version` erkannt; die Datei wird nicht ausgefuehrt.
Die gemeldete Debian-Basisversion ist nicht die DietPi-Softwareversion.
Unbekannte Werte bleiben `unbekannt`; eine nicht erkannte WSL-Kennung beweist kein natives Linux.
Keine Keys, Umgebungsvariablen-Sammlung, Hostnamen, Netzadressen oder Benutzerkonfigurationen.
Steuerzeichen werden entfernt beziehungsweise ersetzt und Feldlaengen begrenzt.

## Windows-Host-Speicher unter WSL

Die Menuepruefung liest zuerst den gemounteten Windows-Datentraeger unter
`/mnt/c` beziehungsweise das konfigurierte `WINDOWS_HOST_DRIVE` direkt mit `df`.
Nur ein nachgewiesener Mount wird verwendet, kein beliebiger Linux-Ordner dieses Namens.
Damit ist fuer den Standardfall keine funktionierende PowerShell-Interop erforderlich.
Als Fallback bleibt eine nichtinteraktive PowerShell-Abfrage mit zehn Sekunden
Zeitlimit und zwei Sekunden Abbruchfrist. Grosse Bytewerte bleiben Dezimaltext,
statt durch awk-Rundung oder wissenschaftliche Schreibweise unbrauchbar zu werden.
Null freier Speicher ist ein bekannter Wert, nicht eine fehlgeschlagene Messung.
Kann keiner der Wege messen, bleibt der Wert ausdruecklich unbekannt.

Firecracker und Kata verlangen im Menue dieselben 16 GiB Windows-Host-Reserve
wie der native Installer, gVisor dieselben 64 GiB. Im Protokoll mit 14926 MiB
freiem Host-Speicher fehlen fuer Firecracker mindestens 1458 MiB zur Reserve.
Die grosse freie virtuelle Linux-Kapazitaet ersetzt diesen Host-Speicher nicht.
Es erfolgt keine automatische Datenloeschung oder WSL-Verschiebung und keine
Absenkung der Schutzgrenze. Die Messung beweist nicht, auf welchem Laufwerk eine
verschobene WSL-VHDX tatsaechlich gespeichert ist; das muss separat geklaert werden.

## Diagnose ohne Installation

Im bereits geprueften Setup-Verzeichnis:

```bash
python3 -I -B scripts/helpers/system_diagnostics.py
```

Dieser Befehl installiert nichts, fragt kein sudo an und startet keine Dienste,
Modelle, Provider, Cluster oder WSL-Instanzen. Ausgabe bei Rueckfragen zum Fehlerlog beifuegen.
Nur Sandbox-Metadaten: `python3 -I -B scripts/helpers/system_diagnostics.py --sandbox`.
Ein KVM-Geraet wird nicht geoeffnet; Rechte oder Kernelmodule werden nicht geaendert.
Details und Grenzen: [Sandbox-Runtimes](tools/sandbox-runtimes.md).

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
