# VPS Oracle Cloud Free Guide

## Ziel

Oracle Free VPS kann fuer leichte Remote-Dienste, Monitoring, Tunnels, Backups und kleine
Automationen dienen. Schwere KI-/GPU-/Kubernetes-Pfade sind nicht automatisch geeignet.

## Anbieterrecherche vor dem Setup

[Free-VPS von dwhr-pi](https://github.com/dwhr-pi/Free-VPS) bietet eine externe
Sammlung als Einstieg in die Recherche kostenloser VPS-Angebote und Testkontingente,
auch ausserhalb von Oracle. Link am **18.11.2026** geprueft; die einzelnen
Anbieterangebote wurden hier nicht auf aktuelle Gueltigkeit verifiziert.

Vor Registrierung die offiziellen Anbieterbedingungen zu Laufzeit, Kontingenten,
Zahlungsmitteln, automatischer Abrechnung, Regionen und Datenverwendung pruefen.
Free Tier und befristetes Testguthaben unterscheiden; keine Garantie dauerhafter
Kostenfreiheit, verfuegbarer Kapazitaeten oder Eignung fuer K3s/GPU-Workloads.
Das Setup registriert kein Konto und startet oder bucht dadurch keinen Server.

## Geeignet

- Tailscale/cloudflared
- UFW/Fail2ban
- Uptime Kuma/Healthchecks
- leichte n8n/Huginn-Workflows
- rclone/restic Backup-Ziel

## Nicht als Default

- offene Admin-Ports
- grosse Docker-Stacks
- Airbyte/kind
- ComfyUI/Video-KI
- offene Datenbanken

## Mindesthardening

- SSH Key-Login
- Passwortlogin deaktivieren
- UFW aktivieren
- Updates planen
- Backups testen
- Ports dokumentieren
