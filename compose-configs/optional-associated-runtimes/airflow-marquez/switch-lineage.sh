#!/bin/bash
# Chooses where Airflow sends its OpenLineage events, and recreates the Airflow containers to pick it up.
#
#   ./switch-lineage.sh marquez   - to Marquez only (the default)
#   ./switch-lineage.sh egeria    - to Egeria only, through the OpenLineage proxy backend in shared-infra, which
#                                   publishes the events to the Kafka topic openlineage.events.  Egeria's
#                                   OpenLineageKafkaListener integration connector must be listening on that topic:
#                                   see workbooks/cataloguing-and-surveys/apache-kafka/kafka-open-lineage-events.ipynb.
#   ./switch-lineage.sh both      - to both
#
# The choice is written to openlineage.env (AIRFLOW__OPENLINEAGE__TRANSPORT), which every Airflow container loads,
# so it stays in force across restarts and rebuilds until it is switched again.
set -euo pipefail
cd "$(dirname "$0")"

ENV_FILE="openlineage.env"
MARQUEZ='{"type": "http", "url": "http://marquez:5050", "endpoint": "api/v1/lineage"}'
EGERIA='{"type": "http", "url": "http://host.docker.internal:6000", "endpoint": "api/v1/lineage"}'

case "${1:-}" in
  marquez) echo "Setting lineage to: MARQUEZ ONLY";    TRANSPORT="$MARQUEZ" ;;
  egeria)  echo "Setting lineage to: EGERIA ONLY";     TRANSPORT="$EGERIA" ;;
  both)    echo "Setting lineage to: MARQUEZ + EGERIA"
           TRANSPORT='{"type": "composite", "transports": {"marquez": '"$MARQUEZ"', "egeria": '"$EGERIA"'}}' ;;
  *)       echo "Usage: ./switch-lineage.sh [marquez|egeria|both]"; exit 1 ;;
esac

# Replace (or add) the transport line, keeping the rest of the file.
grep -v '^AIRFLOW__OPENLINEAGE__TRANSPORT=' "$ENV_FILE" > "$ENV_FILE.tmp" || true
echo "AIRFLOW__OPENLINEAGE__TRANSPORT=$TRANSPORT" >> "$ENV_FILE.tmp"
mv "$ENV_FILE.tmp" "$ENV_FILE"

echo "Recreating the Airflow containers..."
docker compose -f airflow-marquez.yaml up -d --no-deps \
  airflow-apiserver airflow-scheduler airflow-dag-processor airflow-worker airflow-triggerer
echo "Done. Lineage transport in $ENV_FILE:"
grep '^AIRFLOW__OPENLINEAGE__TRANSPORT=' "$ENV_FILE"
