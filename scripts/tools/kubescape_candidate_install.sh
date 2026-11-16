#!/usr/bin/env bash
set -euo pipefail
exec bash "${BASH_SOURCE[0]%/*}/kubescape_install.sh" "$@"
