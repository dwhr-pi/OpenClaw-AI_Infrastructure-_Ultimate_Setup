#!/usr/bin/env bash
# Fail closed for unimplemented install, update, removal and doctor actions.
set -euo pipefail
printf '%s\n' 'GEPLANT / NICHT INSTALLIERBAR: kein freigegebenes natives Build-/Lifecycle-Rezept.'
printf '%s\n' 'Keine Dateien, Pakete, Dienste oder Cluster geaendert. Keine vorhandene Installation entfernt.'
printf '%s\n' 'Anleitung: docs/tools/infrastructure-candidates.md'
if [[ "$#" -eq 1 && "$1" == "--dry-run" ]]; then
  exit 0
fi
exit 3

