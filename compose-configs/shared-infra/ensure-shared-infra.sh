#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

if ! docker network inspect egeria_network >/dev/null 2>&1; then
  docker network create egeria_network >/dev/null
  echo "[shared-infra] Created docker network 'egeria_network'"
else
  echo "[shared-infra] Docker network 'egeria_network' already exists"
fi

echo "[shared-infra] Ensuring shared Kafka and Postgres are running..."
docker compose -p egeria-shared-infra -f shared-infra.yaml up -d kafka postgres

wait_for_container_state egeria-shared-kafka
wait_for_container_state egeria-shared-postgres

echo "[shared-infra] Shared Kafka and Postgres are ready."
popd >/dev/null

