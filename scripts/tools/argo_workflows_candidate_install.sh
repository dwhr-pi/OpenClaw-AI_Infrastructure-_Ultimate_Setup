#!/usr/bin/env bash
set -euo pipefail
exec bash "${BASH_SOURCE[0]%/*}/argo_workflows_install.sh" "$@"
