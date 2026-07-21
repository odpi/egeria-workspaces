#!/usr/bin/env bash
set -euo pipefail

# [sync-demo-db] Move the demo Portal's user + feedback data (the demo_auth
# and demo schemas in coco_pharma) between two machines that never run the
# Portal at the same time — e.g. switching which box is the "live" demo
# machine while Egeria Advisor / Resource Explorer run elsewhere.
#
# This only handles the pg_dump/pg_restore half. Transport for 'push'/'pull'
# is plain scp/ssh — point it at a Tailscale hostname/IP once Tailscale is
# set up on both machines, and make sure key-based SSH auth works first
# (`ssh <remote-host>` with no password prompt).
#
# Because only one Portal is ever live, 'import' is a full replace
# (pg_restore --clean) of the local demo_auth schema (users, events,
# favorites, config) — there is no merge/conflict resolution there, by
# design. demo.feedback is different: feedback is independently-generated,
# append-only data that either machine can produce, so it's merged by id
# (existing rows kept, missing rows added) rather than replaced — a sync
# should never be able to lose feedback collected on either side.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUICKSTART_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

source "${QUICKSTART_DIR}/../shared-infra/detect-engine.sh"

CONTAINER_NAME="${DEMO_DB_CONTAINER:-egeria-shared-postgres}"
PGPORT="${PGPORT:-5442}"
PGUSER="${PGUSER:-postgres}"
export PGPASSWORD="${PGPASSWORD:-egeria}"
PGDATABASE="${PGDATABASE:-coco_pharma}"
SCHEMAS=(demo_auth demo)

SYNC_DIR="${SYNC_DIR:-${QUICKSTART_DIR}/../../runtime-volumes/demo-sync}"

log() { echo "[sync-demo-db] $*" >&2; }

usage() {
  cat <<'EOF'
Usage:
  sync-demo-db.sh export [outfile]
      Dump the demo_auth + demo schemas (users, feedback, config, events,
      favorites) to a pg_dump custom-format file. Defaults to
      runtime-volumes/demo-sync/demo-db_<timestamp>.dump, and always also
      refreshes runtime-volumes/demo-sync/latest.dump.

  sync-demo-db.sh import <file> [-y]
      Restore a dump produced by 'export' into this machine's
      egeria-shared-postgres: demo_auth (users, events, favorites, config)
      is REPLACED; demo.feedback is MERGED by id (existing rows kept,
      missing rows added). Prompts for confirmation unless -y is given.

  sync-demo-db.sh push <remote-host> <remote-dir>
      export, then scp the dump + latest.dump to <remote-host>:<remote-dir>.
      <remote-dir> is a path on the remote host (relative to its $HOME
      unless absolute) — e.g. egeria-workspaces/runtime-volumes/demo-sync.
      Use your Tailscale hostname/IP for <remote-host>.

  sync-demo-db.sh pull <remote-host> <remote-dir> [-y]
      scp <remote-dir>/latest.dump down from <remote-host>, then import it.

Env overrides: DEMO_DB_CONTAINER, PGPORT, PGUSER, PGPASSWORD, PGDATABASE, SYNC_DIR
EOF
}

_dump_cmd() {
  local outfile="$1"
  local schema_args=()
  for s in "${SCHEMAS[@]}"; do schema_args+=(--schema="$s"); done
  log "Dumping schemas (${SCHEMAS[*]}) from ${CONTAINER_NAME} -> ${outfile}"
  $CONTAINER_ENGINE exec -e PGPASSWORD="$PGPASSWORD" "$CONTAINER_NAME" \
    pg_dump -h localhost -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" \
      -Fc "${schema_args[@]}" \
    > "$outfile"
}

_psql() {
  $CONTAINER_ENGINE exec -i -e PGPASSWORD="$PGPASSWORD" "$CONTAINER_NAME" \
    psql -h localhost -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" "$@"
}

_restore_demo_auth() {
  local infile="$1"
  log "Replacing demo_auth (users, events, favorites, config) from ${infile}"
  $CONTAINER_ENGINE exec -i -e PGPASSWORD="$PGPASSWORD" "$CONTAINER_NAME" \
    pg_restore -h localhost -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" \
      --schema=demo_auth --clean --if-exists --no-owner \
    < "$infile"
}

# Merge demo.feedback by id instead of replacing it: rename the live 'demo'
# schema aside (if present), restore the dump's 'demo' schema under its
# normal name, then fold the old rows back in with ON CONFLICT DO NOTHING
# so rows unique to either side survive. Safe even when one side has no
# 'demo' schema at all yet (fresh installs never submitted feedback).
_merge_feedback() {
  local infile="$1"
  log "Merging demo.feedback from ${infile} (existing rows kept, missing rows added)"

  local pre_sql post_sql
  pre_sql="$(mktemp)"
  post_sql="$(mktemp)"

  # pg_restore --schema=demo only restores objects *inside* the schema — the
  # CREATE SCHEMA statement itself isn't part of that selection, so it fails
  # to create demo.feedback unless the schema already exists. Pre-create it
  # empty so pg_restore only has to add the table/data. Also self-heals a
  # leftover demo_sync_old from a previous crashed run.
  cat > "$pre_sql" <<'SQL'
DROP SCHEMA IF EXISTS demo_sync_old CASCADE;
DO $do$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'demo') THEN
    EXECUTE 'ALTER SCHEMA demo RENAME TO demo_sync_old';
  END IF;
END
$do$;
CREATE SCHEMA IF NOT EXISTS demo;
SQL

  # Merge old rows back in by id if the dump brought its own feedback table;
  # if the dump had none, just move the old table back into place untouched.
  cat > "$post_sql" <<'SQL'
DO $do$
BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.tables
    WHERE table_schema = 'demo_sync_old' AND table_name = 'feedback'
  ) THEN
    IF to_regclass('demo.feedback') IS NULL THEN
      EXECUTE 'ALTER TABLE demo_sync_old.feedback SET SCHEMA demo';
    ELSE
      EXECUTE 'INSERT INTO demo.feedback SELECT * FROM demo_sync_old.feedback ON CONFLICT (id) DO NOTHING';
    END IF;
  END IF;
  IF EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'demo_sync_old') THEN
    EXECUTE 'DROP SCHEMA demo_sync_old CASCADE';
  END IF;
END
$do$;
SQL

  _psql < "$pre_sql"
  $CONTAINER_ENGINE exec -i -e PGPASSWORD="$PGPASSWORD" "$CONTAINER_NAME" \
    pg_restore -h localhost -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" \
      --schema=demo --no-owner \
    < "$infile" || true
  _psql < "$post_sql"
  rm -f "$pre_sql" "$post_sql"
}

cmd_export() {
  mkdir -p "$SYNC_DIR"
  local outfile="${1:-${SYNC_DIR}/demo-db_$(date +%Y%m%dT%H%M%S).dump}"
  _dump_cmd "$outfile"
  cp "$outfile" "${SYNC_DIR}/latest.dump"
  log "Export complete: ${outfile} (latest.dump updated)"
  echo "$outfile"
}

cmd_import() {
  local infile="${1:?usage: sync-demo-db.sh import <file> [-y]}"
  local auto_yes="${2:-}"
  [[ -f "$infile" ]] || { echo "[sync-demo-db] No such file: $infile" >&2; exit 1; }
  if [[ "$auto_yes" != "-y" ]]; then
    read -r -p "[sync-demo-db] This will REPLACE local demo_auth (users, events, favorites, config) and MERGE demo.feedback with the contents of ${infile}. Continue? [y/N] " _confirm
    [[ "$_confirm" =~ ^[Yy]$ ]] || { log "Aborted."; exit 1; }
  fi
  _restore_demo_auth "$infile"
  _merge_feedback "$infile"
  log "Import complete."
}

cmd_push() {
  local remote_host="${1:?usage: sync-demo-db.sh push <remote-host> <remote-dir>}"
  local remote_dir="${2:?usage: sync-demo-db.sh push <remote-host> <remote-dir>}"
  local outfile
  outfile="$(cmd_export)"
  ssh "$remote_host" "mkdir -p '${remote_dir}'"
  log "Copying $(basename "$outfile") and latest.dump -> ${remote_host}:${remote_dir}/"
  scp "$outfile" "${SYNC_DIR}/latest.dump" "${remote_host}:${remote_dir}/"
  log "Pushed. On ${remote_host}, run: sync-demo-db.sh import ${remote_dir}/latest.dump"
}

cmd_pull() {
  local remote_host="${1:?usage: sync-demo-db.sh pull <remote-host> <remote-dir> [-y]}"
  local remote_dir="${2:?usage: sync-demo-db.sh pull <remote-host> <remote-dir> [-y]}"
  local auto_yes="${3:-}"
  mkdir -p "$SYNC_DIR"
  local local_file="${SYNC_DIR}/pulled_latest.dump"
  log "Copying ${remote_host}:${remote_dir}/latest.dump -> ${local_file}"
  scp "${remote_host}:${remote_dir}/latest.dump" "$local_file"
  cmd_import "$local_file" "$auto_yes"
}

case "${1:-}" in
  export) shift; cmd_export "$@" ;;
  import) shift; cmd_import "$@" ;;
  push)   shift; cmd_push "$@" ;;
  pull)   shift; cmd_pull "$@" ;;
  *) usage; exit 1 ;;
esac
