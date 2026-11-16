#!/usr/bin/env bash
# Official source: https://github.com/aquasecurity/kube-bench; never starts an audit.
set -euo pipefail
ROOT="$(cd "${BASH_SOURCE[0]%/*}/../.." && pwd)"
exec "${NATIVE_GITHUB_PYTHON_BIN:-python3}" -B "$ROOT/scripts/tools/helpers/native_github_tools.py" kube_bench install "$@"
