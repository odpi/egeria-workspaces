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
#
# ── Compose file set (2026-08-23 incident) ──────────────────────────────────
# quick-start-local always runs against a MERGED set of compose files — never
# just egeria-quickstart.yaml alone (see its COMPOSE_FILES assembly). This
# script has to build the same set: recreating a container with a narrower
# file set doesn't error, it just silently drops whatever that container's
# entry in the missing overlay files defined. Hit for real 2026-08-23: a
# manual `docker compose -f egeria-quickstart.yaml up -d apache-web` (to pick
# up a fresh pyegeria build, same class of operation this script automates)
# recreated the container without egeria-quickstart-ssl.yaml's bind mount for
# runtime-volumes/quickstart-apache-web/ssl-define.conf — Apache's `Define
# HTTPS_REDIRECT_PORT` never ran, so the plain-HTTP vhost's redirect sent
# browsers to the literal, unresolvable "https://localhost:${HTTPS_REDIRECT_
# PORT}/" instead of the real port. Same risk applies to pyegeria-web and
# jupyter-hub's egeria-quickstart-local.yaml extra_hosts entries. Below
# mirrors quick-start-local's own COMPOSE_FILES logic so this can't recur.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUICKSTART_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Source engine detection to get $CONTAINER_ENGINE / $COMPOSE_CMD
source "${QUICKSTART_DIR}/../shared-infra/detect-engine.sh"

log() {
  echo "[quickstart-pyegeria-update] $*"
}

cd "${QUICKSTART_DIR}"

# Same assembly as quick-start-local: base + local (extra_hosts) + ssl
# (Apache HTTPS, unconditionally mounted every run, demo or not) + docker
# (service_healthy — podman-compose 1.5.0 blocks on it indefinitely) + demo
# (only if this deployment was actually started with --demo, detected the
# same way quick-start-local persists it: .env.demo existing).
COMPOSE_FILES=(-f egeria-quickstart.yaml -f egeria-quickstart-local.yaml -f egeria-quickstart-ssl.yaml)
if [[ "$CONTAINER_ENGINE" != "podman" ]]; then
  COMPOSE_FILES+=(-f egeria-quickstart-docker.yaml)
fi
if [[ -f .env.demo ]]; then
  COMPOSE_FILES+=(-f egeria-quickstart-demo.yaml)
  log "Demo mode detected (.env.demo present) — including egeria-quickstart-demo.yaml."
fi

log "Rebuilding pyegeria-web with --no-cache (forces the pip install layer to actually re-run)..."
$COMPOSE_CMD -p egeria-quickstart "${COMPOSE_FILES[@]}" build --no-cache pyegeria-web

log "Recreating the pyegeria-web container from the fresh image..."
$COMPOSE_CMD -p egeria-quickstart "${COMPOSE_FILES[@]}" up -d pyegeria-web

log "Verifying the installed version:"
$CONTAINER_ENGINE exec quickstart-pyegeria-web pip show pyegeria | grep -E '^(Name|Version):'

log "Done."
