#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

HOST_FQDN="$(hostname -f 2>/dev/null || hostname)"

read_existing_env() {
  local key="$1"
  if [[ -f .env ]]; then
    grep -E "^${key}=" .env | head -n1 | cut -d= -f2- || true
  fi
}

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

SHARED_KAFKA_IMAGE_VAL="${SHARED_KAFKA_IMAGE:-}"
if [[ -z "$SHARED_KAFKA_IMAGE_VAL" ]]; then
  SHARED_KAFKA_IMAGE_VAL="$(read_existing_env SHARED_KAFKA_IMAGE)"
fi
if [[ -z "$SHARED_KAFKA_IMAGE_VAL" ]]; then
  SHARED_KAFKA_IMAGE_VAL="bitnamilegacy/kafka@sha256:f45d5b813412e1ef7ce67b467309a84e4c6dc03d7626a0b6da867db9b69bd107"
fi

SHARED_POSTGRES_IMAGE_VAL="${SHARED_POSTGRES_IMAGE:-}"
if [[ -z "$SHARED_POSTGRES_IMAGE_VAL" ]]; then
  SHARED_POSTGRES_IMAGE_VAL="$(read_existing_env SHARED_POSTGRES_IMAGE)"
fi
if [[ -z "$SHARED_POSTGRES_IMAGE_VAL" ]]; then
  SHARED_POSTGRES_IMAGE_VAL="postgres@sha256:fbcea1bd13b6a882cd6caa6b58db3ae5c102efe50ec625b3e2a5cbc50db5bfe4"
fi

USE_HARDENED_KAFKA_VAL="${USE_HARDENED_KAFKA:-}"
if [[ -z "$USE_HARDENED_KAFKA_VAL" ]]; then
  USE_HARDENED_KAFKA_VAL="$(read_existing_env USE_HARDENED_KAFKA)"
fi
if [[ -z "$USE_HARDENED_KAFKA_VAL" ]]; then
  USE_HARDENED_KAFKA_VAL="0"
fi

KAFKA_HARDENED_IMAGE_VAL="${KAFKA_HARDENED_IMAGE:-}"
if [[ -z "$KAFKA_HARDENED_IMAGE_VAL" ]]; then
  KAFKA_HARDENED_IMAGE_VAL="$(read_existing_env KAFKA_HARDENED_IMAGE)"
fi
if [[ -z "$KAFKA_HARDENED_IMAGE_VAL" ]]; then
  KAFKA_HARDENED_IMAGE_VAL="docker.io/<vendor>/<hardened-kafka-image>:<tag-or-digest>"
fi

TMP_ENV=".env.tmp"
cat > "$TMP_ENV" <<EOF
HOST_FQDN=${HOST_FQDN}
KAFKA_CLUSTER_ID=${KAFKA_CLUSTER_ID_VAL}
KAFKA_BOOTSTRAP_SERVERS=${HOST_FQDN}:9194
SHARED_KAFKA_IMAGE=${SHARED_KAFKA_IMAGE_VAL}
SHARED_POSTGRES_IMAGE=${SHARED_POSTGRES_IMAGE_VAL}
USE_HARDENED_KAFKA=${USE_HARDENED_KAFKA_VAL}
KAFKA_HARDENED_IMAGE=${KAFKA_HARDENED_IMAGE_VAL}
EOF
mv -f "$TMP_ENV" .env

echo "[shared-infra/gen-env.sh] Wrote .env with HOST_FQDN=${HOST_FQDN}, KAFKA_CLUSTER_ID=${KAFKA_CLUSTER_ID_VAL}, USE_HARDENED_KAFKA=${USE_HARDENED_KAFKA_VAL}" >&2

