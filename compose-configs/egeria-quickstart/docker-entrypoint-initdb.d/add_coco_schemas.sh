#!/usr/bin/env bash
# Run this script when coco_sus and coco_ods schemas need to be added
# to an existing coco_pharma database (i.e. Postgres was already deployed
# before these schemas were introduced).
#
# Usage:
#   ./add_coco_schemas.sh
#
# Override defaults with environment variables:
#   PGHOST=... PGPORT=... PGUSER=... PGPASSWORD=... ./add_coco_schemas.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data"

# Source engine detection to get $CONTAINER_ENGINE
source "${SCRIPT_DIR}/../../shared-infra/detect-engine.sh"

PGHOST="${PGHOST:-localhost}"
PGPORT="${PGPORT:-5442}"
PGUSER="${PGUSER:-egeria_admin}"
PGPASSWORD="${PGPASSWORD:-admin4egeria}"
# Use coco_pharma as default database for this script
PGDATABASE="${PGDATABASE:-coco_pharma}"

CONTAINER_NAME="egeria-shared-postgres"

# Wrapper to run psql. Use local psql if available, otherwise use docker/podman exec
psql_cmd() {
  if command -v psql &> /dev/null; then
    psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -v ON_ERROR_STOP=1 "$@"
  else
    # Use -h localhost -p 5442 inside the container because that is how it is configured
    $CONTAINER_ENGINE exec -e PGPASSWORD="$PGPASSWORD" "$CONTAINER_NAME" psql -h localhost -p 5442 -U "$PGUSER" -d "$PGDATABASE" -v ON_ERROR_STOP=1 "$@"
  fi
}

log() {
  echo "[add-coco-schemas] $*"
}

log "Starting coco schema addition..."

# 1. Create coco_sus
log "Creating coco_sus schema..."
psql_cmd -c "CREATE SCHEMA IF NOT EXISTS coco_sus; GRANT ALL ON SCHEMA coco_sus TO egeria_admin, egeria_user, airflow_user;"

log "Loading coco_sus data..."
if command -v psql &> /dev/null; then
    psql_cmd -f <(cat <(printf 'SET search_path TO coco_sus;\n') "$DATA_DIR/coco_sus.sql")
else
    # Copy data to container and run psql -f
    $CONTAINER_ENGINE exec "$CONTAINER_NAME" mkdir -p /tmp/coco-data
    $CONTAINER_ENGINE cp "$DATA_DIR/coco_sus.sql" "$CONTAINER_NAME:/tmp/coco-data/coco_sus.sql"
    $CONTAINER_ENGINE exec -i -e PGPASSWORD="$PGPASSWORD" "$CONTAINER_NAME" psql -h localhost -p 5442 -U "$PGUSER" -d "$PGDATABASE" -v ON_ERROR_STOP=1 -c "SET search_path TO coco_sus;" -f /tmp/coco-data/coco_sus.sql
fi

# 2. Create coco_ods
log "Creating coco_ods schema..."
psql_cmd -c "CREATE SCHEMA IF NOT EXISTS coco_ods; GRANT ALL ON SCHEMA coco_ods TO egeria_admin, egeria_user, airflow_user;"

log "Loading coco_ods data..."
if command -v psql &> /dev/null; then
    psql_cmd -f <(cat <(printf 'SET search_path TO coco_ods;\n') "$DATA_DIR/coco_ods.sql")
else
    # Copy data to container and run psql -f
    $CONTAINER_ENGINE exec "$CONTAINER_NAME" mkdir -p /tmp/coco-data
    $CONTAINER_ENGINE cp "$DATA_DIR/coco_ods.sql" "$CONTAINER_NAME:/tmp/coco-data/coco_ods.sql"
    $CONTAINER_ENGINE exec -i -e PGPASSWORD="$PGPASSWORD" "$CONTAINER_NAME" psql -h localhost -p 5442 -U "$PGUSER" -d "$PGDATABASE" -v ON_ERROR_STOP=1 -c "SET search_path TO coco_ods;" -f /tmp/coco-data/coco_ods.sql
fi

log "Done. coco_sus and coco_ods schemas are ready in coco_pharma."
# Cleanup
if ! command -v psql &> /dev/null; then
  $CONTAINER_ENGINE exec "$CONTAINER_NAME" rm -rf /tmp/coco-data
fi
