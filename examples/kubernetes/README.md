# Gehaertete Kubernetes-Beispiele

Die Beispiele aus dem erneut hinzugefuegten `scripts/k8s_deployments.yaml` bleiben erhalten,
werden aber unter [hardened-services.yaml](hardened-services.yaml) **getrennt** weitergehaertet.
Das [urspruengliche Gesamtmanifest](../../docs/legacy/K8S_DEPLOYMENTS_LEGACY.md) bleibt unveraendert archiviert.
Der bestehende reine Anzeige-Wrapper verwendet weiterhin das Archiv und fuehrt kein `kubectl apply` aus.

## Sicherheitsvorgaben

- Alle Pod- und Init-Container laufen Non-Root mit RuntimeDefault-Seccomp, ohne Capabilities oder Privilegieneskalation.
- Root-Dateisysteme sind schreibgeschuetzt. Modelle/Daten und begrenzte temporaere Schreibverzeichnisse sind eigene Volumes.
- Keine automatisch eingebundenen ServiceAccount-Tokens und kein oeffentlicher LoadBalancer fuer den Proxy.
- OpenManus-Source verlangt eine separat bereitgestellte GitHub-URL und einen vollstaendigen geprueften Commit.
- Der Proxy verlangt einen separaten Bearer-Token; Provider-Schluessel sind Header, keine URL-Parameter oder Log-Ausgaben.
- JSON-Eingaben sind begrenzt und validiert; Ollama wird fuer die JSON-Antwort explizit ohne Streaming aufgerufen.

## Vor einer Aktivierung

**Kein fertiges Deployment und kein neuer Container-Installationsweg des Setups.**
Die Beispiele sind aus Sicherheitsgruenden auf `replicas: 0` gesetzt. Die Image-Namen unter
`registry.invalid` sind absichtlich nicht aufloesbare Platzhalter, **keine verifizierten Digests**.
Ein Administrator muss passende, rechtlich und technisch gepruefte Images mit Digest ueber
ein privates Overlay bereitstellen. Es werden keine erfundenen SHA256-Pins als geprueft ausgegeben.
Das Setup baut oder startet diese Images nicht; die nativen Installer bleiben der Installationsweg.

Vor dem Erhoehen der Replikazahl sind insbesondere abzunehmen:

1. Image-Inhalt, UID/GID 10001, benoetigte Bibliotheken und schreibbare Pfade fuer jedes Programm testen.
2. Bestehende PVC-Daten sichern und UID-/Migrationsvertrag pruefen; nichts automatisch chownen oder loeschen.
3. MongoDB-Benutzer, Auth/TLS, Secret-Provisionierung und Zenbot-Zugang getrennt einrichten.
4. OpenManus-Abhaengigkeiten und Entrypoint pruefen; `openmanus-reviewed-source` enthaelt `repository` und `commit`.
5. [Proxy-Quelltext](gemini_proxy.py) als `/app/proxy.py` ins gepruefte Image aufnehmen, nicht als ConfigMap.
   Flask/Requests und eigenen Produktions-WSGI-Server bereitstellen, kein Flask-Entwicklungsserver.
6. `gemini-secrets` mit `api-key` und `proxy-auth-token` sowie `gemini-reviewed-config` mit `model` bereitstellen.
7. Interne Ollama-Service-Aufloesung, TLS/Authentifizierung, NetworkPolicies und minimale Egress-Ziele festlegen.
8. Ressourcenlimits, Probes, Backup/Restore, autorisierte Provider-Datenuebermittlung und Monitoring abnehmen.

Die mitgelieferte Proxy-Pythonreferenz ersetzt keinen Produktions-Gateway-Vertrag.
Insbesondere sind Modellverfuegbarkeit, Quoten, Tokenbudgets und Abrechnung hier nicht getestet.
Es wurde kein Provider, Cluster oder Dienst gestartet.

Fuer einen bereits abgenommenen Plattformaufbau siehe die
[Kustomize-Basis](../../k8s/base/kustomization.yml),
[Produktions-Baseline](../../docs/PRODUCTION_BASELINE.md) und
[GitOps-Anleitung](../../docs/GITOPS_SMALL_VPS.md).
