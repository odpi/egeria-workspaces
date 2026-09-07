#!/usr/bin/env bash
# Mirrors generated Dr.Egeria templates from egeria-python into the
# egeria-workspaces-fs repo and the trellis monorepo. Uses `rsync --delete`
# so renamed/removed family folders don't linger as stale copies downstream.
#
# 2026-09-06: the trellis destination moved from
# packages/egeria-advisor/examples/templates to the repo-level
# config/dr-egeria-templates. Still two destinations, not three -- the
# templates are a runtime input to egeria-advisor's command keyword index
# and agents/tools.py rather than an example library, and the repo-level
# home lets resource-explorer consume them later without a third copy.
set -euo pipefail

EGERIA_PYTHON="${EGERIA_PYTHON:-/Users/dwolfson/localGit/egeria-python}"
EGERIA_WORKSPACES_FS="${EGERIA_WORKSPACES_FS:-/Users/dwolfson/localGit/egeria-v6/egeria-workspaces-fs}"
# Migrated 2026-08-09: egeria-advisor is now a package inside the trellis
# monorepo, not a standalone checkout -- see references/repo_paths.md.
# 2026-09-06: templates now land at the repo root, not in the package, so
# this points at the trellis repo itself. TRELLIS is the current name;
# EGERIA_ADVISOR is still honoured for anyone with it exported.
TRELLIS="${TRELLIS:-${EGERIA_ADVISOR:-/Users/dwolfson/localGit/egeria-v6/trellis}}"

SRC_BASIC="$EGERIA_PYTHON/sample-data/templates/basic/"
SRC_ADVANCED="$EGERIA_PYTHON/sample-data/templates/advanced/"

for src in "$SRC_BASIC" "$SRC_ADVANCED"; do
  if [ ! -d "$src" ]; then
    echo "Source directory missing: $src" >&2
    echo "Run refresh_specs in egeria-python first." >&2
    exit 1
  fi
done

WS_BASIC="$EGERIA_WORKSPACES_FS/templates/basic/"
WS_ADVANCED="$EGERIA_WORKSPACES_FS/templates/advanced/"
WS_STRAY_NESTED="$EGERIA_WORKSPACES_FS/templates/templates"

ADV_BASIC="$TRELLIS/config/dr-egeria-templates/basic/"
ADV_ADVANCED="$TRELLIS/config/dr-egeria-templates/advanced/"

sync_one () {
  local src="$1" dst="$2" label="$3"
  echo "== $label =="
  mkdir -p "$dst"
  # -rt (not -a): recursive + preserve timestamps, but NOT permissions.
  # -a propagates source file mode, which turned every destination file
  # into a mode-only diff (755->644) the first time this ran -- these are
  # plain markdown docs, mode bits shouldn't be part of the content diff.
  rsync -rt --delete "$src" "$dst"
  echo
}

if [ -d "$WS_STRAY_NESTED" ]; then
  echo "Removing accidental nested duplicate: $WS_STRAY_NESTED"
  rm -rf "$WS_STRAY_NESTED"
  echo
fi

sync_one "$SRC_BASIC"    "$WS_BASIC"    "egeria-workspaces-fs / Basic"
sync_one "$SRC_ADVANCED" "$WS_ADVANCED" "egeria-workspaces-fs / Advanced"
sync_one "$SRC_BASIC"    "$ADV_BASIC"   "trellis / Basic"
sync_one "$SRC_ADVANCED" "$ADV_ADVANCED" "trellis / Advanced"

echo "Done. Review git status in egeria-workspaces-fs and trellis before committing:"
echo "  git -C \"$EGERIA_WORKSPACES_FS\" status --short"
echo "  git -C \"$TRELLIS\" status --short"
