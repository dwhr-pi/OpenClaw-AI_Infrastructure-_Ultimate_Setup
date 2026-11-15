#!/usr/bin/env bash
# Upstream: https://github.com/espeak-ng/espeak-ng; native build lifecycle, no model/service start.
set -euo pipefail
ROOT="$(cd "${BASH_SOURCE[0]%/*}/../.." && pwd)"
exec "${GAP_TOOLS_PYTHON_BIN:-python3}" -B "$ROOT/scripts/tools/helpers/gap_tools.py" espeak_ng doctor "$@"
