#!/usr/bin/env bash
# Catalog candidate only; no installer or runtime is available.
set -euo pipefail
ROOT="$(cd "${BASH_SOURCE[0]%/*}/../.." && pwd)"
printf '%s\n' 'Kube_Bench: GEPLANT / NICHT INSTALLIERBAR. Native Build- und Lifecycle-Abnahme offen.'
exec "$BASH" "$ROOT/scripts/tools/infrastructure_candidate_blocked.sh" "$@"

