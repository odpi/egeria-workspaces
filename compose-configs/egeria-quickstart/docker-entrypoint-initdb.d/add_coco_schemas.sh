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

PGHOST="${PGHOST:-localhost}"
PGPORT="${PGPORT:-5442}"
PGUSER="${PGUSER:-egeria_admin}"
PGPASSWORD="${PGPASSWORD:-admin4egeria}"

export PGPASSWORD

PSQL="psql -h $PGHOST -p $PGPORT -U $PGUSER -d coco_pharma -v ON_ERROR_STOP=1"

echo "Creating coco_sus schema and loading data..."
$PSQL -c "CREATE SCHEMA IF NOT EXISTS coco_sus; GRANT ALL ON SCHEMA coco_sus TO egeria_admin, egeria_user, airflow_user;"
$PSQL -f <(cat <(printf 'SET search_path TO coco_sus;\n') "$DATA_DIR/coco_sus.sql")

echo "Creating coco_ods schema and loading data..."
$PSQL -c "CREATE SCHEMA IF NOT EXISTS coco_ods; GRANT ALL ON SCHEMA coco_ods TO egeria_admin, egeria_user, airflow_user;"
$PSQL -f <(cat <(printf 'SET search_path TO coco_ods;\n') "$DATA_DIR/coco_ods.sql")

echo "Done. coco_sus and coco_ods schemas are ready in coco_pharma."
