#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
#
# Drop and recreate an Egeria metadata-store database in the shared Postgres,
# for a clean start (e.g. after an Egeria release that needs a fresh store).
#
# Why this exists: docker-entrypoint-initdb.d/init_egeria.sql creates the
# database AND grants egeria_admin / egeria_user privileges on it -- but it only
# runs when Postgres initialises a brand-new data directory. Recreating the
# database by hand with just CREATE DATABASE skips the grant, and the platform
# then crash-loops (exit 43) with "permission denied for database egeria" when it
# tries to create its repository schema. This script does all of it in order.
#
# DESTRUCTIVE: all metadata in the database is lost, unless --backup is given.
# Other databases in the same Postgres (egeria_advisor, airflow, marquez, the
# Coco databases, ...) are not touched.
#
# Usage: reset-egeria-db.sh [--yes] [--backup] [--dry-run]
#                           [--database NAME] [--container NAME]
#                           [--postgres-container NAME] [--port PORT]
#   --database NAME            database to reset (default: egeria; use
#                              egeria_freshstart for freshstart)
#   --container NAME           Egeria platform container to stop and restart
#                              (default: quickstart-egeria-main)
#   --postgres-container NAME  shared Postgres container (default:
#                              egeria-shared-postgres)
#   --port PORT                Postgres port inside that container (default: 5442)
#   --backup                   pg_dump the database to egeria-db-backups/ (next to this
#                              script, git-ignored) first
#   --yes                      don't ask for confirmation
#   --dry-run                  print what would be done, change nothing
#
# Before running: stop anything else that writes to Egeria (e.g. the Resource
# Explorer web server on 8810) -- Egeria is empty until its bootstrap finishes.
# After running: the platform reloads its content packs on startup, and the
# portal's own bootstrap heal then repopulates the rest; do not hand-run
# Dr.Egeria documents on top of it (their link commands do not dedupe).
set -euo pipefail

database="egeria"
platform_container="quickstart-egeria-main"
pg_container="egeria-shared-postgres"
pg_port="5442"
grant_roles="egeria_admin, egeria_user"   # matches init_egeria.sql
assume_yes=0
do_backup=0
dry_run=0

usage() { sed -n '/^# Usage:/,/^# Before running/p' "$0" | sed 's/^# \{0,1\}//' | sed '$d'; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --database)           database="${2:?--database needs a value}"; shift 2 ;;
    --container)          platform_container="${2:?--container needs a value}"; shift 2 ;;
    --postgres-container) pg_container="${2:?--postgres-container needs a value}"; shift 2 ;;
    --port)               pg_port="${2:?--port needs a value}"; shift 2 ;;
    --backup)             do_backup=1; shift ;;
    --yes|-y)             assume_yes=1; shift ;;
    --dry-run)            dry_run=1; shift ;;
    -h|--help)            usage; exit 0 ;;
    *) echo "[reset-egeria-db] unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

# The name goes into SQL unquoted, so only accept a plain lowercase identifier,
# and never the maintenance databases.
if [[ ! "$database" =~ ^[a-z_][a-z0-9_]*$ ]] || [[ "$database" == postgres || "$database" == template* ]]; then
  echo "[reset-egeria-db] refusing database name: '$database'" >&2
  exit 2
fi

run() {
  if [[ "$dry_run" -eq 1 ]]; then echo "[dry-run] $*"; else "$@"; fi
}
psql_admin() {
  docker exec "$pg_container" psql -h localhost -p "$pg_port" -U postgres -v ON_ERROR_STOP=1 -Atc "$1"
}

for c in "$pg_container" "$platform_container"; do
  if ! docker inspect "$c" >/dev/null 2>&1; then
    echo "[reset-egeria-db] no such container: $c" >&2
    exit 1
  fi
done
if [[ "$(docker inspect -f '{{.State.Running}}' "$pg_container")" != "true" ]]; then
  echo "[reset-egeria-db] $pg_container is not running" >&2
  exit 1
fi

size="$(psql_admin "select pg_size_pretty(pg_database_size('${database}'))" 2>/dev/null || echo 'does not exist')"
echo "[reset-egeria-db] database '${database}' on ${pg_container}:${pg_port} (${size})"
echo "[reset-egeria-db] platform container to stop and restart: ${platform_container}"
echo "[reset-egeria-db] ALL metadata in '${database}' will be deleted$([[ $do_backup -eq 1 ]] && echo ' (after a backup)' || echo ' with NO backup')."

if [[ "$assume_yes" -ne 1 && "$dry_run" -ne 1 ]]; then
  read -r -p "Type the database name to continue: " answer
  if [[ "$answer" != "$database" ]]; then
    echo "[reset-egeria-db] aborted." >&2
    exit 1
  fi
fi

if [[ "$do_backup" -eq 1 ]]; then
  backup_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/egeria-db-backups"
  backup_file="${backup_dir}/${database}-$(date -u +%Y%m%dT%H%M%SZ).sql.gz"
  echo "[reset-egeria-db] backing up to ${backup_file}"
  if [[ "$dry_run" -eq 1 ]]; then
    echo "[dry-run] docker exec ${pg_container} pg_dump -h localhost -p ${pg_port} -U postgres ${database} | gzip > ${backup_file}"
  else
    mkdir -p "$backup_dir"
    docker exec "$pg_container" pg_dump -h localhost -p "$pg_port" -U postgres "$database" | gzip > "$backup_file"
  fi
fi

echo "[reset-egeria-db] stopping ${platform_container}"
run docker stop "$platform_container"

echo "[reset-egeria-db] dropping and recreating ${database}"
if [[ "$dry_run" -eq 1 ]]; then
  echo "[dry-run] DROP DATABASE ${database} WITH (FORCE); CREATE DATABASE ${database}; GRANT ALL PRIVILEGES ON DATABASE ${database} TO ${grant_roles};"
else
  # WITH (FORCE) disconnects anything still attached (pgAdmin, DBeaver, ...).
  psql_admin "DROP DATABASE IF EXISTS ${database} WITH (FORCE)"
  psql_admin "CREATE DATABASE ${database}"
  psql_admin "GRANT ALL PRIVILEGES ON DATABASE ${database} TO ${grant_roles}"
fi

echo "[reset-egeria-db] starting ${platform_container}"
run docker start "$platform_container"

cat <<EOF
[reset-egeria-db] done. The platform now loads its content packs; this takes a few minutes.
  Watch:  docker logs -f ${platform_container}
  Healthy once: docker inspect -f '{{.State.Health.Status}}' ${platform_container}
Anything that holds Egeria GUIDs (e.g. Resource Explorer's registry) is stale until it resyncs.
EOF
