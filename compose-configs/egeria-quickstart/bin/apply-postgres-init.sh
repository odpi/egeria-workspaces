#!/usr/bin/env bash
set -euo pipefail

# [quickstart-postgres-init] Brings the quickstart PostgreSQL set-up up to date.
#
# Runs every init script below, in order, on every start.  Each script is safe to
# run again: it creates only the users, databases, schemas, tables and seed rows
# that are missing.  So a new install gets everything, an existing install picks
# up anything added since it was created, and a database that has been dropped
# (e.g. to reset the demo) is recreated on the next start.  A change to an
# existing table must therefore be written so it is also safe to repeat (e.g.
# ALTER ... TYPE, ADD COLUMN IF NOT EXISTS).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUICKSTART_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Source engine detection to get $CONTAINER_ENGINE
source "${QUICKSTART_DIR}/../shared-infra/detect-engine.sh"

SQL_DIR="${QUICKSTART_DIR}/docker-entrypoint-initdb.d"

PGHOST="${PGHOST:-localhost}"
PGPORT="${PGPORT:-5442}"
PGUSER="${PGUSER:-egeria_admin}"
# Exported so the local-psql branch of psql_cmd() (used when the host has psql
# installed) picks it up via libpq instead of prompting interactively. The
# default matches the egeria_admin role created by the postgres init SQL.
export PGPASSWORD="${PGPASSWORD:-admin4egeria}"
# The scripts rerun on every start, so hide the "already exists, skipping" notices.
export PGOPTIONS="${PGOPTIONS:--c client_min_messages=warning}"
PGDATABASE="${PGDATABASE:-postgres}"

# Init scripts in SQL_DIR, run in this order on every start.
INIT_SCRIPTS=(
  init_egeria.sql
  init_coco_data_hub.sql
  init_coco_systems.sql
  init_subscription_staging.sql
)
CONTAINER_NAME="${PG_CONTAINER:-egeria-shared-postgres}"

# Wrapper to run psql. Use local psql if available, otherwise use docker/podman exec
psql_cmd() {
  if command -v psql &> /dev/null; then
    psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" "$@"
  else
    # Use -h localhost -p 5442 inside the container because that is how it is configured
    $CONTAINER_ENGINE exec -i -e PGPASSWORD="$PGPASSWORD" "$CONTAINER_NAME" psql -h localhost -p 5442 -U "$PGUSER" -d "$PGDATABASE" "$@"
  fi
}

log() {
  echo "[quickstart-postgres-init] $*"
}

# Wait for PostgreSQL to be ready
log "Waiting for PostgreSQL at ${PGHOST}:${PGPORT}..."
MAX_ATTEMPTS=40
ATTEMPT=1

until psql_cmd -v ON_ERROR_STOP=1 -c "SELECT 1;" >/dev/null 2>&1; do
  if [ $ATTEMPT -ge $MAX_ATTEMPTS ]; then
    log "ERROR: PostgreSQL not ready after $MAX_ATTEMPTS attempts."
    # Dump some diagnostic info
    if command -v nc &> /dev/null; then
      log "Diagnostic: nc -zv $PGHOST $PGPORT"
      nc -zv "$PGHOST" "$PGPORT" 2>&1 || log "  Port $PGPORT is NOT reachable on $PGHOST"
    fi
    exit 1
  fi
  log "  attempt $ATTEMPT/$MAX_ATTEMPTS (waiting 3s...)"
  sleep 3
  ATTEMPT=$((ATTEMPT + 1))
done

run_init_script() {
  local SQL_FILE="$1"
  log "Running $SQL_FILE ..."
  if command -v psql &> /dev/null; then
    (cd "$SQL_DIR" && psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -q -v ON_ERROR_STOP=1 -f "$SQL_FILE")
  else
    # psql is not on the host: run it in the container.  The scripts include their
    # data files with \ir, so copy the whole directory in first.
    $CONTAINER_ENGINE exec -i -e PGPASSWORD="$PGPASSWORD" -e PGOPTIONS="$PGOPTIONS" "$CONTAINER_NAME" /bin/bash -c "cd $TMP_DIR && psql -h localhost -p 5442 -U $PGUSER -d $PGDATABASE -q -v ON_ERROR_STOP=1 -f $SQL_FILE"
  fi
}

TMP_DIR="/tmp/quickstart-init"
if ! command -v psql &> /dev/null; then
  $CONTAINER_ENGINE exec "$CONTAINER_NAME" rm -rf "$TMP_DIR"
  $CONTAINER_ENGINE exec "$CONTAINER_NAME" mkdir -p "$TMP_DIR"
  $CONTAINER_ENGINE cp "$SQL_DIR/." "$CONTAINER_NAME:$TMP_DIR/"
  trap '$CONTAINER_ENGINE exec "$CONTAINER_NAME" rm -rf "$TMP_DIR" >/dev/null 2>&1 || true' EXIT
fi

for sql_file in "${INIT_SCRIPTS[@]}"; do
  run_init_script "$sql_file"
done
log "PostgreSQL set-up is up to date."
