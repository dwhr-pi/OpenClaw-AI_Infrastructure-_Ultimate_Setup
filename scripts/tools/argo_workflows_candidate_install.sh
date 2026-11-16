#!/usr/bin/env bash
# Catalog candidate only; no native build or lifecycle is approved.
set -euo pipefail
ROOT="$(cd "${BASH_SOURCE[0]%/*}/../.." && pwd)"
printf '%s\n' 'Argo_Workflows: GEPLANT / NICHT INSTALLIERBAR. Siehe docs/tools/infrastructure-candidates.md'
exec "$BASH" "$ROOT/scripts/tools/infrastructure_candidate_blocked.sh" "$@"
