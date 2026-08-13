#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

HOST_FQDN="$(hostname -f 2>/dev/null || hostname)"

source "${SCRIPT_DIR}/../shared-infra/detect-engine.sh"

EXCHANGE_CONFIG_JSON="../../exchange-freshstart/config/config_workspaces.json"
EXCHANGE_CONFIG_TEMPLATE="${EXCHANGE_CONFIG_JSON}.template"

# HTTPS_PORT for the "Pyegeria Publishing Root" link below. fresh-start-local
# writes .env.ssl (with the effective HTTPS_PORT) before calling this script,
# so read it from there; default to the self-signed default (7843) otherwise.
HTTPS_PORT_VAL=""
[[ -f .env.ssl ]] && HTTPS_PORT_VAL="$(grep -E '^HTTPS_PORT=' .env.ssl | head -n1 | cut -d= -f2- || true)"
[[ -z "$HTTPS_PORT_VAL" ]] && HTTPS_PORT_VAL="7843"

if [[ ! -f "$EXCHANGE_CONFIG_TEMPLATE" ]]; then
  echo "[gen-env.sh] WARNING: template not found at ${EXCHANGE_CONFIG_TEMPLATE}; skipping config generation" >&2
else
  cp "$EXCHANGE_CONFIG_TEMPLATE" "$EXCHANGE_CONFIG_JSON"
  if command -v python3 >/dev/null 2>&1; then
    # Substitute HOST_FQDN for localhost/127.0.0.1 and inject fs-* service names.
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
    env["Egeria Engine Host"] = "fs-engine-host"
    env["Egeria Integration Daemon"] = "fs-integration-daemon"
    env["Egeria Metadata Store"] = "fs-metadata-store"
    env["Egeria View Server"] = "fs-view-server"
    env["Egeria Platform URL"] = f"https://{host}:8443"
    env["Egeria Integration Daemon URL"] = f"https://{host}:8443"
    env["Egeria View Server URL"] = f"https://{host}:8443"
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

CONFIG_JSON_RAW=""
if [[ -f "$EXCHANGE_CONFIG_JSON" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    CONFIG_JSON_RAW="$({ python3 -c 'import json; print(json.dumps(json.load(open("'"$EXCHANGE_CONFIG_JSON"'")), separators=(",", ":")))'; })"
  else
    CONFIG_JSON_RAW="$(tr -d '\n\r' < "$EXCHANGE_CONFIG_JSON")"
  fi
fi

CONFIG_JSON_ESCAPED="$(printf '%s' "$CONFIG_JSON_RAW" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g')"

KAFKA_CLUSTER_ID_VAL="${KAFKA_CLUSTER_ID:-}"
if [[ -z "$KAFKA_CLUSTER_ID_VAL" && -f .env ]]; then
  EXISTING_ID="$(grep -E '^KAFKA_CLUSTER_ID=' .env | head -n1 | cut -d= -f2- || true)"
  if [[ -n "$EXISTING_ID" && "$EXISTING_ID" != "<stable-cluster-id>" && "$EXISTING_ID" =~ ^[0-9A-Za-z_.-]+$ ]]; then
    KAFKA_CLUSTER_ID_VAL="$EXISTING_ID"
  fi
fi
if [[ -z "$KAFKA_CLUSTER_ID_VAL" || "$KAFKA_CLUSTER_ID_VAL" == "<stable-cluster-id>" ]]; then
  KAFKA_CLUSTER_ID_VAL="42"
fi

# Determine EGERIA_MEM_LIMIT (freshstart-egeria-main's mem_limit — see
# egeria-freshstart.yaml, mirrored from quickstart). Same priority as
# KAFKA_CLUSTER_ID above: already-exported env var (set by
# ./fresh-start-local --egeria-memory) > existing .env value (so a value set
# once persists across plain re-runs without the flag) > default 6g.
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

TMP_ENV=".env.tmp"
cat > "$TMP_ENV" <<EOF
HOST_FQDN=${HOST_FQDN}
KAFKA_CLUSTER_ID=${KAFKA_CLUSTER_ID_VAL}
KAFKA_BOOTSTRAP_SERVERS=${HOST_FQDN}:9194
HOST_GATEWAY_IP=${HOST_GATEWAY_IP}
EGERIA_MEM_LIMIT=${EGERIA_MEM_LIMIT_VAL}
CONFIG_JSON="${CONFIG_JSON_ESCAPED}"
EOF
mv -f "$TMP_ENV" .env

echo "[gen-env.sh] Wrote .env with HOST_FQDN=${HOST_FQDN}, KAFKA_CLUSTER_ID=${KAFKA_CLUSTER_ID_VAL}, EGERIA_MEM_LIMIT=${EGERIA_MEM_LIMIT_VAL}" >&2

