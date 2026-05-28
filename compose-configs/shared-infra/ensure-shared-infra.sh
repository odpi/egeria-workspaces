#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "${SCRIPT_DIR}/detect-engine.sh"
source "${SCRIPT_DIR}/compose-build-flags.sh"

wait_for_container_state() {
  local container_name="$1"
  local attempts="${2:-40}"
  local sleep_seconds="${3:-3}"
  local status=""

  for (( attempt=1; attempt<=attempts; attempt++ )); do
    # Try the explicit name, then try project-prefixed name (for some podman-compose versions)
    local target_name="$container_name"
    if ! $CONTAINER_ENGINE inspect "$target_name" >/dev/null 2>&1; then
        local found_name=$($CONTAINER_ENGINE ps -a --format '{{.Names}}' | grep -E "^${container_name}$|^[^_]+_${container_name#egeria-shared-}_[0-9]+$" | head -n 1)
        target_name="${found_name:-$container_name}"
    fi

    status="$($CONTAINER_ENGINE inspect -f "$INSPECT_STATUS_FORMAT" "$target_name" 2>/dev/null || true)"
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

if [[ -n "${HARDENED_KAFKA_DATA_DIR:-}" ]]; then
  prepare_runtime_dir "${HARDENED_KAFKA_DATA_DIR}"
  echo "[shared-infra] Kafka data dir: ${HARDENED_KAFKA_DATA_DIR}"
fi

if ! $CONTAINER_ENGINE network inspect egeria_network >/dev/null 2>&1; then
  $CONTAINER_ENGINE network create egeria_network >/dev/null
  echo "[shared-infra] Created $CONTAINER_ENGINE network 'egeria_network'"
else
  echo "[shared-infra] $CONTAINER_ENGINE network 'egeria_network' already exists"
fi

echo "[shared-infra] Ensuring shared Kafka, Postgres, and proxy are running..."
if ! $COMPOSE_CMD -p egeria-shared-infra -f shared-infra.yaml build "${COMPOSE_BUILD_FLAGS[@]}" proxy; then
  echo "[shared-infra] Pull-enabled build failed; retrying build without pull to use local cache..."
  $COMPOSE_CMD -p egeria-shared-infra -f shared-infra.yaml build proxy
fi

if ! $COMPOSE_CMD -p egeria-shared-infra -f shared-infra.yaml up -d ${COMPOSE_PULL_FLAGS} proxy kafka postgres; then
  echo "[shared-infra] Pull-enabled up failed; retrying up without pull to use local cache..."
  $COMPOSE_CMD -p egeria-shared-infra -f shared-infra.yaml up -d proxy kafka postgres
fi

wait_for_container_state egeria-shared-kafka
wait_for_container_state egeria-shared-postgres
wait_for_container_state egeria-shared-openlineage-proxy-backend

echo "[shared-infra] Shared Kafka, Postgres, and proxy are ready."
popd >/dev/null

