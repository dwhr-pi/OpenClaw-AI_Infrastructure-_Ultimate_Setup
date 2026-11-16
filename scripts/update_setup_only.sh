#!/usr/bin/env bash
# Standard-Update ausschliesslich ueber signierte Release-Metadaten; Repair bleibt separat.
set -Eeuo pipefail
ROOT="$(cd "${BASH_SOURCE[0]%/*}/.." && pwd)"
if (($# == 0)) || [[ $# == 1 && $1 == --dry-run ]] || [[ $# == 1 && $1 == --check-online ]] || [[ $# == 1 && $1 == --apply ]]; then
  mode=${1:---apply}
  key=${OPENCLAW_RELEASE_PUBLIC_KEY:-$HOME/.config/openclaw-trust/release.pub}
  if [[ -n ${OPENCLAW_RELEASE_TAG:-} || -n ${OPENCLAW_RELEASE_ARTIFACTS:-} ]]; then
    if [[ -z ${OPENCLAW_RELEASE_TAG:-} || -z ${OPENCLAW_RELEASE_ARTIFACTS:-} ]]; then
      printf '%s\n' 'Tag und Artefaktverzeichnis gemeinsam angeben; kein automatischer Ersatzweg.' >&2
      exit 2
    fi
    [[ "$mode" != --check-online ]] || mode=--dry-run
    set -- --tag "$OPENCLAW_RELEASE_TAG" --artifacts "$OPENCLAW_RELEASE_ARTIFACTS" --public-key "$key" "$mode"
    if [[ "$mode" == --apply ]]; then set -- "$@" --fetch; fi
  else
    [[ "$mode" == --apply ]] || mode=--check-online
    exec python3 -I -B "$ROOT/scripts/security/discover_signed_update.py" --public-key "$key" "$mode"
  fi
fi
exec python3 -I -B "$ROOT/scripts/security/update_verified_release.py" "$@"
