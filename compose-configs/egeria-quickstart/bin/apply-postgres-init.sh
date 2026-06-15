#!/usr/bin/env bash
set -euo pipefail

# [quickstart-postgres-init] Migration runner for quickstart PostgreSQL setup

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUICKSTART_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
SQL_DIR="${QUICKSTART_DIR}/docker-entrypoint-initdb.d"
INIT_SQL="${SQL_DIR}/init_egeria.sql"

PGHOST="${PGHOST:-localhost}"
PGPORT="${PGPORT:-5442}"
PGUSER="${PGUSER:-egeria_admin}"
PGPASSWORD="${PGPASSWORD:-admin4egeria}"
PGDATABASE="${PGDATABASE:-postgres}"

export PGPASSWORD

MIGRATION_ID="egeria-quickstart-init-egeria-v1"

log() {
  echo "[quickstart-postgres-init] $*"
}

# Wait for PostgreSQL to be ready
log "Waiting for PostgreSQL at ${PGHOST}:${PGPORT}..."
MAX_ATTEMPTS=40
ATTEMPT=1
until psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -v ON_ERROR_STOP=1 -c "SELECT 1;" >/dev/null 2>&1; do
  if [ $ATTEMPT -ge $MAX_ATTEMPTS ]; then
    log "ERROR: PostgreSQL not ready after $MAX_ATTEMPTS attempts."
    exit 1
  fi
  log "  attempt $ATTEMPT/$MAX_ATTEMPTS (waiting 3s...)"
  sleep 3
  ATTEMPT=$((ATTEMPT + 1))
done

# Ensure marker table exists
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -v ON_ERROR_STOP=1 <<EOF >/dev/null
CREATE SCHEMA IF NOT EXISTS quickstart_migrations;
CREATE TABLE IF NOT EXISTS quickstart_migrations.applied_migrations (
  migration_id text PRIMARY KEY,
  applied_at timestamptz NOT NULL DEFAULT now()
);
EOF

# Check if migration already applied
ALREADY_APPLIED=$(psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -v ON_ERROR_STOP=1 -t -c "SELECT 1 FROM quickstart_migrations.applied_migrations WHERE migration_id = '$MIGRATION_ID';" | xargs)

if [ "$ALREADY_APPLIED" = "1" ]; then
  log "Migration $MIGRATION_ID already applied; skipping."
  exit 0
fi

# Apply migration
log "Applying migration $MIGRATION_ID ..."
cd "$SQL_DIR"
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -v ON_ERROR_STOP=1 -f "$INIT_SQL"

# Record success
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -v ON_ERROR_STOP=1 <<EOF >/dev/null
INSERT INTO quickstart_migrations.applied_migrations (migration_id)
VALUES ('$MIGRATION_ID')
ON CONFLICT (migration_id) DO NOTHING;
EOF

log "Migration $MIGRATION_ID applied successfully."
