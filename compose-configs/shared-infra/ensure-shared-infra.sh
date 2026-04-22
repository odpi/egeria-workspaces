#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "${SCRIPT_DIR}/compose-build-flags.sh"

wait_for_container_state() {
  local container_name="$1"
  local attempts="${2:-40}"
  local sleep_seconds="${3:-3}"
  local status=""

  for (( attempt=1; attempt<=attempts; attempt++ )); do
    status="$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "$container_name" 2>/dev/null || true)"
    if [[ "$status" == "healthy" || "$status" == "running" ]]; then
      return 0
    fi
    sleep "$sleep_seconds"
  done

  echo "[shared-infra] Timed out waiting for ${container_name}. Last status: ${status:-missing}" >&2
  return 1
}

pushd "$SCRIPT_DIR" >/dev/null
./gen-env.sh
set -a
source ./.env
set +a

COMPOSE_FILES=(-f shared-infra.yaml)
case "${USE_HARDENED_KAFKA:-0}" in
  1|true|TRUE|True|yes|YES|Yes|on|ON|On)
    COMPOSE_FILES+=(-f shared-infra.hardened-kafka.yaml)
    echo "[shared-infra] USE_HARDENED_KAFKA enabled: using shared-infra.hardened-kafka.yaml override."
    ;;
  ""|0|false|FALSE|False|no|NO|No|off|OFF|Off)
    ;;
  *)
    echo "[shared-infra] Invalid USE_HARDENED_KAFKA value: ${USE_HARDENED_KAFKA}. Use one of: 1, true, yes, on, 0, false, no, off." >&2
    popd >/dev/null
    exit 1
    ;;
esac

if ! docker network inspect egeria_network >/dev/null 2>&1; then
  docker network create egeria_network >/dev/null
  echo "[shared-infra] Created docker network 'egeria_network'"
else
  echo "[shared-infra] Docker network 'egeria_network' already exists"
fi

echo "[shared-infra] Ensuring shared Kafka, Postgres, and proxy are running..."
if ! docker compose -p egeria-shared-infra "${COMPOSE_FILES[@]}" build "${COMPOSE_BUILD_FLAGS[@]}" proxy; then
  echo "[shared-infra] Pull-enabled build failed; retrying build without pull to use local cache..."
  docker compose -p egeria-shared-infra "${COMPOSE_FILES[@]}" build proxy
fi

if ! docker compose -p egeria-shared-infra "${COMPOSE_FILES[@]}" up -d --pull always proxy kafka postgres; then
  echo "[shared-infra] Pull-enabled up failed; retrying up without pull to use local cache..."
  docker compose -p egeria-shared-infra "${COMPOSE_FILES[@]}" up -d proxy kafka postgres
fi

wait_for_container_state egeria-shared-kafka
wait_for_container_state egeria-shared-postgres
wait_for_container_state egeria-shared-openlineage-proxy-backend

echo "[shared-infra] Shared Kafka, Postgres, and proxy are ready."
popd >/dev/null

