#!/usr/bin/env bash
# Explicit menu check discovers signed releases without checkout or service changes.
set -Eeuo pipefail
ROOT="$(cd "${BASH_SOURCE[0]%/*}/.." && pwd)"
exec bash "$ROOT/scripts/update_setup_only.sh" --dry-run "$@"
