#!/usr/bin/env bash
set -euo pipefail

HOST_FQDN="$(hostname -f 2>/dev/null || hostname)"

EXCHANGE_CONFIG_JSON="../../exchange/config/config.json"

if [[ -f "$EXCHANGE_CONFIG_JSON" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    # Update exchange/config.json: replace "localhost" and "127.0.0.1" with the host FQDN
    # in all string values. Creates a one-time backup (config.json.bak) if it doesn't exist.
    python3 - "$EXCHANGE_CONFIG_JSON" "$HOST_FQDN" <<'PY'
import json
import os
import shutil
import sys

path = sys.argv[1]
host = sys.argv[2]

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

backup_path = path + ".bak"
if not os.path.exists(backup_path):
    shutil.copy2(path, backup_path)

tmp_path = path + ".tmp"
with open(tmp_path, "w", encoding="utf-8") as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)
    f.write("\n")

os.replace(tmp_path, path)
PY
  else
    echo "python3 not found; skipping update of ${EXCHANGE_CONFIG_JSON}" >&2
  fi
else
  echo "Config file not found: ${EXCHANGE_CONFIG_JSON} (skipping update)" >&2
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

# Write .env atomically
TMP_ENV=".env.tmp"
cat > "$TMP_ENV" <<EOF
HOST_FQDN=${HOST_FQDN}
KAFKA_NODE_ID=1
KAFKA_CLUSTER_ID=${KAFKA_CLUSTER_ID_VAL}
KAFKA_CONTROLLER_QUORUM_VOTERS=1@${HOST_FQDN}:9193
KAFKA_BOOTSTRAP_SERVERS=${HOST_FQDN}:9194
CONFIG_JSON="${CONFIG_JSON_ESCAPED}"
EOF
mv -f "$TMP_ENV" .env

echo "[gen-env.sh] Wrote .env with HOST_FQDN=${HOST_FQDN}, KAFKA_CLUSTER_ID=${KAFKA_CLUSTER_ID_VAL}" >&2