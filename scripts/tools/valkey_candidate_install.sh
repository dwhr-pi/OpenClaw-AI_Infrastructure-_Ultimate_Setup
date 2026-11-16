#!/usr/bin/env bash
# Compatibility entry for the reviewed native installer.
set -euo pipefail
ROOT="$(cd "${BASH_SOURCE[0]%/*}/../.." && pwd)"
exec "$BASH" "$ROOT/scripts/tools/valkey_install.sh" "$@"
