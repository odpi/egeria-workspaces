#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

HOST_FQDN="$(hostname -f 2>/dev/null || hostname)"

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

TMP_ENV=".env.tmp"
cat > "$TMP_ENV" <<EOF
HOST_FQDN=${HOST_FQDN}
KAFKA_CLUSTER_ID=${KAFKA_CLUSTER_ID_VAL}
KAFKA_BOOTSTRAP_SERVERS=${HOST_FQDN}:9194
EOF
mv -f "$TMP_ENV" .env

echo "[shared-infra/gen-env.sh] Wrote .env with HOST_FQDN=${HOST_FQDN}, KAFKA_CLUSTER_ID=${KAFKA_CLUSTER_ID_VAL}" >&2

