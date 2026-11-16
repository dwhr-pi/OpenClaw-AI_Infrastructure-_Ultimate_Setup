#!/usr/bin/env bash
# Only removes unchanged owned build files; not databases or system packages.
set -euo pipefail
ROOT="$(cd "${BASH_SOURCE[0]%/*}/../.." && pwd)"
exec "${NATIVE_GITHUB_PYTHON_BIN:-python3}" -B "$ROOT/scripts/tools/helpers/native_github_tools.py" valkey uninstall "$@"
