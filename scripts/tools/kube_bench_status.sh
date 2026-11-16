#!/usr/bin/env bash
# Build receipt only; no audit or Kubernetes API access.
set -euo pipefail
ROOT="$(cd "${BASH_SOURCE[0]%/*}/../.." && pwd)"
exec "${NATIVE_GITHUB_PYTHON_BIN:-python3}" -B "$ROOT/scripts/tools/helpers/native_github_tools.py" kube_bench status "$@"
