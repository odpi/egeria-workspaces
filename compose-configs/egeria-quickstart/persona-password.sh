#!/usr/bin/env bash
# Sourced by gen-env.sh (PO-45, Architect ruling option (a), 2026-11-17).
#
# The Portal (pyegeria-web) and my-profile sign in to Egeria with QUICKSTART_PERSONA_PASSWORD, and the
# compose file has no default for it any more (a missing value refuses to start). quick-start-local
# therefore makes sure .env carries one, without ever printing it:
#   1. an exported QUICKSTART_PERSONA_PASSWORD wins (and is written back to .env);
#   2. else an existing, non-empty value in .env is kept;
#   3. else the Coco demo persona password is written: the quickstart is the Coco demo, and its
#      personas all share that password (PyegeriaWebHandler/personas.json, the user directory).
# To change it, change it together with the user directory (personas.json and the .omsecrets files), and
# use letters and digits only: .env is unquoted and compose interpolates it (a warning says so otherwise).

# resolve_persona_password ENV_FILE PERSONAS_JSON
# Sets QUICKSTART_PERSONA_PASSWORD_VAL (never echoed). Returns 1, saying why on stderr, when there is
# nothing to use.
resolve_persona_password() {
  local env_file="$1" personas="$2" existing=""
  QUICKSTART_PERSONA_PASSWORD_VAL="${QUICKSTART_PERSONA_PASSWORD:-}"
  QUICKSTART_PERSONA_PASSWORD_SOURCE="exported"
  if [[ -z "$QUICKSTART_PERSONA_PASSWORD_VAL" && -f "$env_file" ]]; then
    existing="$(grep -E '^QUICKSTART_PERSONA_PASSWORD=' "$env_file" | head -n1 | cut -d= -f2- || true)"
    QUICKSTART_PERSONA_PASSWORD_VAL="$existing"
    QUICKSTART_PERSONA_PASSWORD_SOURCE="kept from .env"
  fi
  if [[ -z "$QUICKSTART_PERSONA_PASSWORD_VAL" ]]; then
    if [[ -f "$personas" ]] && command -v python3 >/dev/null 2>&1; then
      QUICKSTART_PERSONA_PASSWORD_VAL="$(python3 -c 'import json,sys; p=json.load(open(sys.argv[1])); print((p.get("erinoverview") or next(iter(p.values()), {})).get("password", ""))' "$personas" 2>/dev/null || true)"
      QUICKSTART_PERSONA_PASSWORD_SOURCE="the Coco demo persona password (personas.json)"
    fi
  fi
  if [[ -z "$QUICKSTART_PERSONA_PASSWORD_VAL" ]]; then
    echo "[gen-env.sh] ERROR: no QUICKSTART_PERSONA_PASSWORD: export it, or set it in ${env_file}" >&2
    return 1
  fi
  # .env is written unquoted and docker compose interpolates it: a "$", a quote, a space or a "#" would
  # reach the Portal as a different password. Warn in words (never the value); letters and digits only.
  if [[ ! "$QUICKSTART_PERSONA_PASSWORD_VAL" =~ ^[A-Za-z0-9]+$ ]]; then
    echo "[gen-env.sh] WARNING: QUICKSTART_PERSONA_PASSWORD (${QUICKSTART_PERSONA_PASSWORD_SOURCE}) has characters other than letters and digits; docker compose reads .env unquoted and treats \$, quotes, spaces and # specially, so the Portal may sign in with a different password. Use letters and digits only (value not shown)." >&2
  fi
  return 0
}
