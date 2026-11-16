#!/usr/bin/env bash
set -euo pipefail
exec bash "${BASH_SOURCE[0]%/*}/kata_containers_install.sh" "$@"
