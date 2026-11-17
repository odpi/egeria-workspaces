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

echo "[shared-infra] Ensuring shared Kafka, Postgres, proxy, kroki, and autoheal are running..."
if ! $COMPOSE_CMD -p egeria-shared-infra -f shared-infra.yaml build "${COMPOSE_BUILD_FLAGS[@]}" proxy autoheal; then
  echo "[shared-infra] Pull-enabled build failed; retrying build without pull to use local cache..."
  $COMPOSE_CMD -p egeria-shared-infra -f shared-infra.yaml build proxy autoheal
fi

if ! $COMPOSE_CMD -p egeria-shared-infra -f shared-infra.yaml up -d ${COMPOSE_PULL_FLAGS} proxy kafka postgres kroki kroki-mermaid autoheal; then
  echo "[shared-infra] Pull-enabled up failed; retrying up without pull to use local cache..."
  $COMPOSE_CMD -p egeria-shared-infra -f shared-infra.yaml up -d proxy kafka postgres kroki kroki-mermaid autoheal
fi

wait_for_container_state egeria-shared-kafka
wait_for_container_state egeria-shared-postgres
wait_for_container_state egeria-shared-openlineage-proxy-backend
wait_for_container_state egeria-shared-kroki
wait_for_container_state egeria-shared-autoheal

# Extra safety: Wait for Postgres port to be reachable on localhost
# Container 'healthy' (pg_isready) doesn't always mean the host-mapped port is fully bound/reachable yet.
# Skip if nc is not found.
if command -v nc &> /dev/null; then
  echo "[shared-infra] Waiting for Postgres port 5442 to be reachable on localhost..."
  for i in {1..20}; do
    if nc -zv localhost 5442 >/dev/null 2>&1; then
      echo "[shared-infra] Postgres port 5442 is reachable."
      break
    fi
    [[ $i -eq 20 ]] && echo "[shared-infra] WARNING: Postgres port 5442 still not reachable on localhost."
    sleep 1
  done
fi

# Databases added to the shared Postgres after it was first released.  The scripts in docker-entrypoint-initdb.d
# run only when the server's data volume is first created, so a script listed here is run again on every start to
# bring an existing server up to date.  Each must be safe to repeat: it creates only what is missing.
SHARED_POSTGRES_UPDATE_SCRIPTS=(
  init_egeria_ods.sql
)
for update_script in "${SHARED_POSTGRES_UPDATE_SCRIPTS[@]}"; do
  # PROVISIONER_PASSWORD (exported from .env above) is passed by NAME, so its value is not on a command line:
  # init_egeria_ods.sql sets the provisioner role's password from it on every start (TR-28). It is deliberately
  # not in shared-infra.yaml's environment, so that adding it did not recreate the Postgres container.
  if $CONTAINER_ENGINE exec -e PGOPTIONS="-c client_min_messages=warning" -e PROVISIONER_PASSWORD egeria-shared-postgres \
       psql -p 5442 -U postgres -d postgres -q -v ON_ERROR_STOP=1 -f "/docker-entrypoint-initdb.d/${update_script}" >/dev/null; then
    echo "[shared-infra] Postgres is up to date with ${update_script}."
  else
    echo "[shared-infra] WARNING: could not apply ${update_script} to Postgres." >&2
    if [[ "$update_script" == init_egeria_ods.sql && -n "${PROVISIONER_PASSWORD:-}" ]]; then
      # The start scripts give Egeria's secrets and Airflow the value in .env; if this failed, the role may still
      # have its previous password, so provisioning and the coco_data_hub loads would fail to sign in (TR-28 R2).
      echo "[shared-infra] WARNING: the provisioner role's password may NOT have been set from PROVISIONER_PASSWORD in .env," >&2
      echo "[shared-infra]          but Egeria's secrets and Airflow are given that value. Fix the error above and start again." >&2
    fi
  fi
done

echo "[shared-infra] Shared Kafka, Postgres, and proxy are ready."
popd >/dev/null
