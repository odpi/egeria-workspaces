#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

HOST_FQDN="$(hostname -f 2>/dev/null || hostname)"

source "${SCRIPT_DIR}/detect-engine.sh"

read_existing_env() {
  local key="$1" val
  if [[ -f .env ]]; then
    val="$(grep -E "^${key}=" .env | head -n1 | cut -d= -f2- || true)"
    # The alerting values below are written single-quoted so this file stays
    # safe to `source` (ensure-shared-infra.sh does). Strip that quoting on the
    # way back in — otherwise each regeneration would wrap the value in another
    # layer of quotes.
    val="${val%\'}"; val="${val#\'}"
    val="${val%\"}"; val="${val#\"}"
    printf '%s' "$val"
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
if [[ "$SHARED_KAFKA_IMAGE_VAL" == bitnamilegacy/kafka* || "$SHARED_KAFKA_IMAGE_VAL" == cleanstart/kafka* ]]; then
  SHARED_KAFKA_IMAGE_VAL=""
fi
if [[ -z "$SHARED_KAFKA_IMAGE_VAL" ]]; then
  SHARED_KAFKA_IMAGE_VAL="docker.io/cleanstart/kafka@sha256:3bfad519feac67e6bd1ae2b18b3e4770cdf2fedf53ecff7b38a520a7c5d77564"
fi

SHARED_POSTGRES_IMAGE_VAL="${SHARED_POSTGRES_IMAGE:-}"
if [[ -z "$SHARED_POSTGRES_IMAGE_VAL" ]]; then
  SHARED_POSTGRES_IMAGE_VAL="$(read_existing_env SHARED_POSTGRES_IMAGE)"
fi
# Migrate away from plain postgres images to pgvector
if [[ "$SHARED_POSTGRES_IMAGE_VAL" == postgres:* || "$SHARED_POSTGRES_IMAGE_VAL" == "postgres@sha256:"* || "$SHARED_POSTGRES_IMAGE_VAL" == "pgvector/pgvector"* ]]; then
  SHARED_POSTGRES_IMAGE_VAL=""
fi
if [[ -z "$SHARED_POSTGRES_IMAGE_VAL" ]]; then
  SHARED_POSTGRES_IMAGE_VAL="docker.io/pgvector/pgvector:pg17"
fi

HARDENED_KAFKA_DATA_DIR_VAL="${HARDENED_KAFKA_DATA_DIR:-}"
if [[ -z "$HARDENED_KAFKA_DATA_DIR_VAL" ]]; then
  HARDENED_KAFKA_DATA_DIR_VAL="$(read_existing_env HARDENED_KAFKA_DATA_DIR)"
fi
if [[ -z "$HARDENED_KAFKA_DATA_DIR_VAL" ]]; then
  HARDENED_KAFKA_DATA_DIR_VAL="${REPO_ROOT}/runtime-volumes/shared-infra-hardened-kafka"
fi

HARDENED_KAFKA_LOG_DIR_VAL="${HARDENED_KAFKA_LOG_DIR:-}"
if [[ -z "$HARDENED_KAFKA_LOG_DIR_VAL" ]]; then
  HARDENED_KAFKA_LOG_DIR_VAL="$(read_existing_env HARDENED_KAFKA_LOG_DIR)"
fi
if [[ -z "$HARDENED_KAFKA_LOG_DIR_VAL" ]]; then
  HARDENED_KAFKA_LOG_DIR_VAL="/var/lib/kafka-data/kraft-logs"
fi

# Alerting credentials for the autoheal service. These have no sensible
# default and are deliberately not generated — they are carried through from
# the environment or from the existing .env so that regenerating this file
# (which happens on every startup) does not silently wipe them. Left empty,
# autoheal still heals; it just logs instead of emailing.
RESEND_API_KEY_VAL="${RESEND_API_KEY:-}"
if [[ -z "$RESEND_API_KEY_VAL" ]]; then
  RESEND_API_KEY_VAL="$(read_existing_env RESEND_API_KEY)"
fi

RESEND_FROM_VAL="${RESEND_FROM:-}"
if [[ -z "$RESEND_FROM_VAL" ]]; then
  RESEND_FROM_VAL="$(read_existing_env RESEND_FROM)"
fi

ALERT_EMAIL_TO_VAL="${ALERT_EMAIL_TO:-}"
if [[ -z "$ALERT_EMAIL_TO_VAL" ]]; then
  ALERT_EMAIL_TO_VAL="$(read_existing_env ALERT_EMAIL_TO)"
fi

TMP_ENV=".env.tmp"
cat > "$TMP_ENV" <<EOF
HOST_FQDN=${HOST_FQDN}
KAFKA_CLUSTER_ID=${KAFKA_CLUSTER_ID_VAL}
KAFKA_BOOTSTRAP_SERVERS=${HOST_FQDN}:9194
SHARED_KAFKA_IMAGE=${SHARED_KAFKA_IMAGE_VAL}
SHARED_POSTGRES_IMAGE=${SHARED_POSTGRES_IMAGE_VAL}
HARDENED_KAFKA_DATA_DIR=${HARDENED_KAFKA_DATA_DIR_VAL}
HARDENED_KAFKA_LOG_DIR=${HARDENED_KAFKA_LOG_DIR_VAL}
HOST_GATEWAY_IP=${HOST_GATEWAY_IP}
RESEND_API_KEY='${RESEND_API_KEY_VAL}'
RESEND_FROM='${RESEND_FROM_VAL}'
ALERT_EMAIL_TO='${ALERT_EMAIL_TO_VAL}'
EOF
mv -f "$TMP_ENV" .env
# This file can now hold a Resend API key, so it must not be world-readable.
# The temp file above is created under the caller's umask (typically 0664), so
# the mode has to be set explicitly after the move — same reasoning as
# quick-start-local's `chmod 600` on .env.demo.
chmod 600 .env

echo "[shared-infra/gen-env.sh] Wrote .env with HOST_FQDN=${HOST_FQDN}, KAFKA_CLUSTER_ID=${KAFKA_CLUSTER_ID_VAL}" >&2

