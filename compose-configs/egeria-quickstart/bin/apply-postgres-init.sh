#!/usr/bin/env bash
set -euo pipefail

# [quickstart-postgres-init] Migration runner for quickstart PostgreSQL setup

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUICKSTART_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Source engine detection to get $CONTAINER_ENGINE
source "${QUICKSTART_DIR}/../shared-infra/detect-engine.sh"

SQL_DIR="${QUICKSTART_DIR}/docker-entrypoint-initdb.d"
INIT_SQL="${SQL_DIR}/init_egeria.sql"

PGHOST="${PGHOST:-localhost}"
PGPORT="${PGPORT:-5442}"
PGUSER="${PGUSER:-egeria_admin}"
# Exported so the local-psql branch of psql_cmd() (used when the host has psql
# installed) picks it up via libpq instead of prompting interactively. The
# default matches the egeria_admin role created by the postgres init SQL.
export PGPASSWORD="${PGPASSWORD:-admin4egeria}"
PGDATABASE="${PGDATABASE:-postgres}"

MIGRATION_ID="egeria-quickstart-init-egeria-v1"
CONTAINER_NAME="egeria-shared-postgres"

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

# Ensure marker table exists
psql_cmd -v ON_ERROR_STOP=1 <<EOF >/dev/null
CREATE SCHEMA IF NOT EXISTS quickstart_migrations;
CREATE TABLE IF NOT EXISTS quickstart_migrations.applied_migrations (
  migration_id text PRIMARY KEY,
  applied_at timestamptz NOT NULL DEFAULT now()
);
EOF

# Check if migration already applied
ALREADY_APPLIED=$(psql_cmd -v ON_ERROR_STOP=1 -t -c "SELECT 1 FROM quickstart_migrations.applied_migrations WHERE migration_id = '$MIGRATION_ID';" 2>/dev/null | xargs)

if [ "$ALREADY_APPLIED" = "1" ]; then
  log "Migration $MIGRATION_ID already applied; skipping."
  exit 0
fi

# Apply migration
log "Applying migration $MIGRATION_ID ..."
if command -v psql &> /dev/null; then
  cd "$SQL_DIR"
  psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -v ON_ERROR_STOP=1 -f "$INIT_SQL"
else
  # If psql is not on host, we must run it in the container.
  # We use 'docker cp' to copy the SQL files to the container so that '\ir' works correctly.
  # We copy them to /tmp/quickstart-init/
  TMP_DIR="/tmp/quickstart-init"
  $CONTAINER_ENGINE exec "$CONTAINER_NAME" mkdir -p "$TMP_DIR"
  $CONTAINER_ENGINE cp "$SQL_DIR/." "$CONTAINER_NAME:$TMP_DIR/"
  
  $CONTAINER_ENGINE exec -i -e PGPASSWORD="$PGPASSWORD" "$CONTAINER_NAME" /bin/bash -c "cd $TMP_DIR && psql -h localhost -p 5442 -U $PGUSER -d $PGDATABASE -v ON_ERROR_STOP=1 -f init_egeria.sql"
  
  # Cleanup
  $CONTAINER_ENGINE exec "$CONTAINER_NAME" rm -rf "$TMP_DIR"
fi

# Record success
psql_cmd -v ON_ERROR_STOP=1 <<EOF >/dev/null
INSERT INTO quickstart_migrations.applied_migrations (migration_id)
VALUES ('$MIGRATION_ID')
ON CONFLICT (migration_id) DO NOTHING;
EOF

log "Migration $MIGRATION_ID applied successfully."
