#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

HOST_FQDN="$(hostname -f 2>/dev/null || hostname)"

source "${SCRIPT_DIR}/../shared-infra/detect-engine.sh"

EXCHANGE_CONFIG_JSON="../../exchange-quickstart/config/config_workspaces.json"
EXCHANGE_CONFIG_TEMPLATE="${EXCHANGE_CONFIG_JSON}.template"

# HTTPS_PORT for the "Pyegeria Publishing Root" link below. quick-start-local
# writes .env.demo / .env.ssl (with the effective HTTPS_PORT) before calling
# this script, so read it from whichever exists; default to the non-demo
# self-signed default (8843) otherwise.
HTTPS_PORT_VAL=""
[[ -f .env.demo ]] && HTTPS_PORT_VAL="$(grep -E '^HTTPS_PORT=' .env.demo | head -n1 | cut -d= -f2- || true)"
[[ -z "$HTTPS_PORT_VAL" && -f .env.ssl ]] && HTTPS_PORT_VAL="$(grep -E '^HTTPS_PORT=' .env.ssl | head -n1 | cut -d= -f2- || true)"
[[ -z "$HTTPS_PORT_VAL" ]] && HTTPS_PORT_VAL="8843"

if [[ ! -f "$EXCHANGE_CONFIG_TEMPLATE" ]]; then
  echo "[gen-env.sh] WARNING: template not found at ${EXCHANGE_CONFIG_TEMPLATE}; skipping config generation" >&2
else
  cp "$EXCHANGE_CONFIG_TEMPLATE" "$EXCHANGE_CONFIG_JSON"
  if command -v python3 >/dev/null 2>&1; then
    # Substitute HOST_FQDN for localhost/127.0.0.1 and inject qs-* service names.
    python3 - "$EXCHANGE_CONFIG_JSON" "$HOST_FQDN" "$HTTPS_PORT_VAL" <<'PY'
import json
import sys

path = sys.argv[1]
host = sys.argv[2]
https_port = sys.argv[3]

def rewrite(obj):
    if isinstance(obj, dict):
        return {k: rewrite(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [rewrite(v) for v in obj]
    if isinstance(obj, str):
        return obj.replace("127.0.0.1", host).replace("localhost", host)
    return obj

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

new_data = rewrite(data)

env = new_data.get("Environment")
if isinstance(env, dict):
    env["Egeria Engine Host"] = "qs-engine-host"
    env["Egeria Integration Daemon"] = "qs-integration-daemon"
    env["Egeria Metadata Store"] = "qs-metadata-store"
    env["Egeria View Server"] = "qs-view-server"
    env["Egeria Platform URL"] = f"https://{host}:9443"
    env["Egeria Integration Daemon URL"] = f"https://{host}:9443"
    env["Egeria View Server URL"] = f"https://{host}:9443"
    env["Egeria Kafka Endpoint"] = "host.docker.internal:9194"
    port_suffix = "" if https_port == "443" else f":{https_port}"
    env["Pyegeria Publishing Root"] = f"https://{host}{port_suffix}/dr-egeria-outbox"

tmp_path = path + ".tmp"
with open(tmp_path, "w", encoding="utf-8") as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)
    f.write("\n")

import os
os.replace(tmp_path, path)
PY
  else
    echo "[gen-env.sh] python3 not found; skipping host substitution in ${EXCHANGE_CONFIG_JSON}" >&2
  fi
fi

# Prepare CONFIG_JSON as a compact single line
CONFIG_JSON_RAW=""
if [[ -f "$EXCHANGE_CONFIG_JSON" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    CONFIG_JSON_RAW="$(
      python3 -c 'import json; print(json.dumps(json.load(open("'"$EXCHANGE_CONFIG_JSON"'")), separators=(",", ":")))' \
    )"
  else
    CONFIG_JSON_RAW="$(tr -d '\n\r' < "$EXCHANGE_CONFIG_JSON")"
  fi
fi

# Escape for .env usage (single-line, safe quoting)
CONFIG_JSON_ESCAPED="$(
  printf '%s' "$CONFIG_JSON_RAW" \
    | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g'
)"

# Determine KAFKA_CLUSTER_ID
# Priority: already exported env var > existing .env numeric value (not placeholder) > default 42
KAFKA_CLUSTER_ID_VAL="${KAFKA_CLUSTER_ID:-}"
if [[ -z "$KAFKA_CLUSTER_ID_VAL" && -f .env ]]; then
  # shellcheck disable=SC2002
  EXISTING_ID="$(grep -E '^KAFKA_CLUSTER_ID=' .env | head -n1 | cut -d= -f2- || true)"
  # Treat placeholder or empty/non-numeric as invalid
  if [[ -n "$EXISTING_ID" && "$EXISTING_ID" != "<stable-cluster-id>" && "$EXISTING_ID" =~ ^[0-9A-Za-z_.-]+$ ]]; then
    KAFKA_CLUSTER_ID_VAL="$EXISTING_ID"
  fi
fi
if [[ -z "$KAFKA_CLUSTER_ID_VAL" || "$KAFKA_CLUSTER_ID_VAL" == "<stable-cluster-id>" ]]; then
  KAFKA_CLUSTER_ID_VAL="42"
fi

# Determine EGERIA_MEM_LIMIT (egeria-main's mem_limit — see egeria-quickstart.yaml).
# Same priority as KAFKA_CLUSTER_ID above: already-exported env var (set by
# ./quick-start-local --egeria-memory) > existing .env value (so a value set
# once persists across plain re-runs without the flag) > default 6g. A
# 2026-09-08 fix briefly raised this default to 10g to paper over GC-thrash-
# induced 401s/timeouts under the JVM's old MaxRAMPercentage=80 flags; the
# JVM retuning in egeria-quickstart.yaml (G1GC, MaxRAMPercentage=60) fixes
# that thrash directly, so 6g is a safe default again. 10g (or higher)
# remains a reasonable EGERIA_MEM_LIMIT override on a host still seeing
# pressure — it's just no longer the default.
EGERIA_MEM_LIMIT_VAL="${EGERIA_MEM_LIMIT:-}"
if [[ -z "$EGERIA_MEM_LIMIT_VAL" && -f .env ]]; then
  EXISTING_MEM="$(grep -E '^EGERIA_MEM_LIMIT=' .env | head -n1 | cut -d= -f2- || true)"
  if [[ -n "$EXISTING_MEM" ]]; then
    EGERIA_MEM_LIMIT_VAL="$EXISTING_MEM"
  fi
fi
if [[ -z "$EGERIA_MEM_LIMIT_VAL" ]]; then
  EGERIA_MEM_LIMIT_VAL="6g"
fi

# Determine EGERIA_CPU_LIMIT (egeria-main's cpus — see egeria-quickstart.yaml).
# Same priority/persistence pattern as EGERIA_MEM_LIMIT above. This caps CPU,
# not memory: an unbounded egeria-main can starve every other container (and
# the Docker Desktop VM's own kernel threads) on CPU alone, badly enough to
# crash them even with plenty of free memory — see the 2026-08-23 incident
# where Postgres crashed because a checkpoint couldn't get scheduled.
EGERIA_CPU_LIMIT_VAL="${EGERIA_CPU_LIMIT:-}"
if [[ -z "$EGERIA_CPU_LIMIT_VAL" && -f .env ]]; then
  EXISTING_CPU="$(grep -E '^EGERIA_CPU_LIMIT=' .env | head -n1 | cut -d= -f2- || true)"
  if [[ -n "$EXISTING_CPU" ]]; then
    EGERIA_CPU_LIMIT_VAL="$EXISTING_CPU"
  fi
fi
if [[ -z "$EGERIA_CPU_LIMIT_VAL" ]]; then
  EGERIA_CPU_LIMIT_VAL="4"
fi

# QUICKSTART_PERSONA_PASSWORD (PO-45): the Portal's and my-profile's Egeria password. The compose file
# has no default for it; exported > existing .env > the Coco demo persona password. Never printed.
source "${SCRIPT_DIR}/persona-password.sh"
resolve_persona_password .env "${SCRIPT_DIR}/PyegeriaWebHandler/personas.json"

# JWT_SECRET (PO-46b, as RK-24b for freshstart): signs the Portal's session cookies. This script rewrites .env every
# run, which used to drop it outside --demo, so the compose default (a value published in the repo) signed every
# quickstart's sessions. An exported value wins, else .env.demo's (quick-start-local --demo writes it before calling
# this script), else the one already in .env, else a random one is generated on this first run. A published value is
# never kept. Never printed.
_PUBLIC_JWT_DEFAULTS=("change-me-before-going-public" "change-me-before-going-public-meow")
_is_public_jwt() { local v="$1" p; for p in "${_PUBLIC_JWT_DEFAULTS[@]}"; do [[ "$v" == "$p" ]] && return 0; done; return 1; }
if [[ -n "${JWT_SECRET:-}" ]] && _is_public_jwt "$JWT_SECRET"; then
  # An exported value wins at compose too, so it can't be replaced here: stop rather than start a Portal that
  # refuses every sign-in.
  echo "[gen-env.sh] STOP: the exported JWT_SECRET is a published example value, which anyone could use to forge sessions." >&2
  echo "[gen-env.sh]   Unset it (unset JWT_SECRET) and re-run: a random one is generated into .env and kept." >&2
  exit 1
fi
JWT_SECRET_VAL="${JWT_SECRET:-}"
for _jwt_file in .env.demo .env; do
  if [[ -z "$JWT_SECRET_VAL" && -f "$_jwt_file" ]]; then
    JWT_SECRET_VAL="$(grep -E '^JWT_SECRET=' "$_jwt_file" | head -n1 | cut -d= -f2- || true)"
    JWT_SECRET_VAL="${JWT_SECRET_VAL%\"}"; JWT_SECRET_VAL="${JWT_SECRET_VAL#\"}"
    if _is_public_jwt "$JWT_SECRET_VAL"; then JWT_SECRET_VAL=""; fi
  fi
done
if [[ -z "$JWT_SECRET_VAL" ]]; then
  if command -v openssl >/dev/null 2>&1; then
    JWT_SECRET_VAL="$(openssl rand -hex 32)"
  else
    JWT_SECRET_VAL="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
  fi
  echo "[gen-env.sh] JWT_SECRET: generated a new random value into .env (kept on later runs)." >&2
fi

# Write .env atomically (mode 600: it now carries a password)
TMP_ENV=".env.tmp"
( umask 077; : > "$TMP_ENV" )
cat > "$TMP_ENV" <<EOF
HOST_FQDN=${HOST_FQDN}
KAFKA_NODE_ID=1
KAFKA_CLUSTER_ID=${KAFKA_CLUSTER_ID_VAL}
KAFKA_CONTROLLER_QUORUM_VOTERS=1@${HOST_FQDN}:9193
KAFKA_BOOTSTRAP_SERVERS=${HOST_FQDN}:9194
HOST_GATEWAY_IP=${HOST_GATEWAY_IP}
EGERIA_MEM_LIMIT=${EGERIA_MEM_LIMIT_VAL}
EGERIA_CPU_LIMIT=${EGERIA_CPU_LIMIT_VAL}
CONFIG_JSON="${CONFIG_JSON_ESCAPED}"
QUICKSTART_PERSONA_PASSWORD=${QUICKSTART_PERSONA_PASSWORD_VAL}
EOF
printf 'JWT_SECRET=%s\n' "$JWT_SECRET_VAL" >> "$TMP_ENV"
mv -f "$TMP_ENV" .env
chmod 600 .env

echo "[gen-env.sh] Wrote .env with HOST_FQDN=${HOST_FQDN}, KAFKA_CLUSTER_ID=${KAFKA_CLUSTER_ID_VAL}, EGERIA_MEM_LIMIT=${EGERIA_MEM_LIMIT_VAL}, EGERIA_CPU_LIMIT=${EGERIA_CPU_LIMIT_VAL}, QUICKSTART_PERSONA_PASSWORD ${QUICKSTART_PERSONA_PASSWORD_SOURCE} (not shown), JWT_SECRET (kept or generated, not shown)" >&2