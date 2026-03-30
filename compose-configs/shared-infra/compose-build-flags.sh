#!/usr/bin/env bash
set -euo pipefail

COMPOSE_BUILD_FLAGS=(--pull)

case "${NO_CACHE:-}" in
  ""|0|false|FALSE|False|no|NO|No|off|OFF|Off)
    ;;
  1|true|TRUE|True|yes|YES|Yes|on|ON|On)
    COMPOSE_BUILD_FLAGS+=(--no-cache)
    echo "[compose-build] NO_CACHE enabled: docker compose builds will bypass the local build cache."
    ;;
  *)
    echo "[compose-build] Invalid NO_CACHE value: ${NO_CACHE}. Use one of: 1, true, yes, on, 0, false, no, off." >&2
    return 1 2>/dev/null || exit 1
    ;;
esac

