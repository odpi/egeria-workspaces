#!/bin/bash

# Configuration
ENV_FILE="openlineage.env"
MARQUEZ_URL="http://marquez:5050"
# Actual Egeria Asset Lineage OMAS endpoint
EGERIA_URL="http://egeria-server:9443/servers/egeria-server/open-metadata/access-services/asset-lineage/users/airflow/open-lineage"

# JSON Definitions
MARQUEZ_ONLY='{"type": "http", "url": "'$MARQUEZ_URL'", "endpoint": "api/v1/lineage"}'
EGERIA_ONLY='{"type": "http", "url": "'$EGERIA_URL'"}'
COMPOSITE='{"type": "composite", "transports": {"marquez": {"type": "http", "url": "'$MARQUEZ_URL'", "endpoint": "api/v1/lineage"}, "egeria": {"type": "http", "url": "'$EGERIA_URL'"}}}'

case $1 in
  "marquez")
    echo "Setting lineage to: MARQUEZ ONLY"
    echo "OL_TRANSPORT='$MARQUEZ_ONLY'" > $ENV_FILE
    ;;
  "egeria")
    echo "Setting lineage to: EGERIA ONLY"
    echo "OL_TRANSPORT='$EGERIA_ONLY'" > $ENV_FILE
    ;;
  "both")
    echo "Setting lineage to: MARQUEZ + EGERIA"
    echo "OL_TRANSPORT='$COMPOSITE'" > $ENV_FILE
    ;;
  *)
    echo "Usage: ./switch-lineage.sh [marquez|egeria|both]"
    exit 1
    ;;
esac

echo "Updating Airflow containers..."
docker compose up -d airflow-scheduler airflow-worker airflow-webserver
echo "Done. Current configuration in $ENV_FILE:"
cat $ENV_FILE