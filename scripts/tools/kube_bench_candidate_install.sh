#!/usr/bin/env bash
# Compatibility entry for the pinned native build, without an audit.
set -euo pipefail
ROOT="$(cd "${BASH_SOURCE[0]%/*}/../.." && pwd)"
exec "$BASH" "$ROOT/scripts/tools/kube_bench_install.sh" "$@"
