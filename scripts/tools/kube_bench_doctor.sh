#!/usr/bin/env bash
# Source/config/binary inventory only; no benchmark run.
set -euo pipefail
ROOT="$(cd "${BASH_SOURCE[0]%/*}/../.." && pwd)"
exec "${NATIVE_GITHUB_PYTHON_BIN:-python3}" -B "$ROOT/scripts/tools/helpers/native_github_tools.py" kube_bench doctor "$@"
