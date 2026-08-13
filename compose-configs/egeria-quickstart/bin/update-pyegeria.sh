#!/usr/bin/env bash
set -euo pipefail

# [quickstart-pyegeria-update] Force-rebuild the pyegeria-web image so a new
# pyegeria release actually gets picked up.
#
# Why this exists: the FastAPI image's `pip install pyegeria>=X --upgrade`
# line runs at BUILD time (see PyegeriaWebHandler/Dockerfile-fast-api), and
# Docker caches that RUN layer by instruction text, not by "did PyPI publish
# something new." A plain `docker compose build` (no `--no-cache`) reuses the
# cached layer and silently keeps whatever version was resolved the first
# time the image was built — this is what "pip install --upgrade inside a
# shell in the container" runs into too: it updates the *running* container's
# filesystem, which is fine until the next `build`/`up --build` recreates it
# from the (still-stale) image, at which point the manual upgrade is gone.
# Only ./PyegeriaWebHandler:/app is bind-mounted — site-packages is not.
#
# This script always does a real --no-cache rebuild, so it's the reliable
# way to pick up a new release regardless of what's cached.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUICKSTART_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Source engine detection to get $CONTAINER_ENGINE / $COMPOSE_CMD
source "${QUICKSTART_DIR}/../shared-infra/detect-engine.sh"

log() {
  echo "[quickstart-pyegeria-update] $*"
}

cd "${QUICKSTART_DIR}"

log "Rebuilding pyegeria-web with --no-cache (forces the pip install layer to actually re-run)..."
$COMPOSE_CMD -f egeria-quickstart.yaml build --no-cache pyegeria-web

log "Recreating the pyegeria-web container from the fresh image..."
$COMPOSE_CMD -f egeria-quickstart.yaml up -d pyegeria-web

log "Verifying the installed version:"
$CONTAINER_ENGINE exec quickstart-pyegeria-web pip show pyegeria | grep -E '^(Name|Version):'

log "Done."
