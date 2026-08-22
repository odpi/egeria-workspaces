#!/usr/bin/env bash
# Scheduled renewal for a Let's Encrypt certificate obtained via
# quick-start-local --demo's automatic Let's Encrypt fallback (see
# letsencrypt-cert.sh — CERT_DIR pointing at runtime-volumes/certs-letsencrypt
# is what marks a demo deployment as using Let's Encrypt rather than a
# manually-supplied cert).
#
# Schedule this via cron or a systemd timer on the demo host, e.g.:
#   0 3 * * * cd /path/to/egeria-workspaces && ./renew-certs.sh >> runtime-volumes/letsencrypt/renew.log 2>&1
#
# Safe to run as often as daily: certbot only actually reissues a cert once
# it's within 30 days of its 90-day expiry (--keep-until-expiring in
# letsencrypt-cert.sh), and this script only restarts apache-web when the
# certificate file on disk actually changed — a no-op renewal check causes
# no service interruption.
set -euo pipefail
cd "$(dirname "$0")"

ENV_DEMO="compose-configs/egeria-quickstart/.env.demo"
if [[ ! -f "$ENV_DEMO" ]]; then
  echo "[renew-certs.sh] ${ENV_DEMO} not found — nothing to renew (this host isn't running demo mode)." >&2
  exit 1
fi

_get() { grep -E "^$1=" "$ENV_DEMO" | head -n1 | cut -d= -f2- || true; }

CERT_DIR="$(_get CERT_DIR)"
SITE_URL="$(_get SITE_URL)"
EMAIL="$(_get ADMIN_BOOTSTRAP_EMAIL)"

if [[ -z "$CERT_DIR" || "$CERT_DIR" != *"/runtime-volumes/certs-letsencrypt" ]]; then
  echo "[renew-certs.sh] CERT_DIR (${CERT_DIR:-unset}) isn't the Let's Encrypt output path — this demo is using a manually-supplied cert; nothing to renew here." >&2
  exit 0
fi

DOMAIN="${SITE_URL#https://}"
DOMAIN="${DOMAIN%%/*}"
DOMAIN="${DOMAIN%%:*}"

# Optional extra names to carry on the same cert, comma-separated, e.g.
#   CERT_EXTRA_DOMAINS=home.example.net
# Each must resolve to this host and pass its own HTTP-01 challenge. Without
# this, a renewal silently reissues with only SITE_URL's name and drops any
# additional SANs the current cert carries.
EXTRA_DOMAINS="$(_get CERT_EXTRA_DOMAINS)"
if [[ -n "$EXTRA_DOMAINS" ]]; then
  DOMAIN="${DOMAIN},${EXTRA_DOMAINS}"
fi

if [[ -z "$DOMAIN" || -z "$EMAIL" ]]; then
  echo "[renew-certs.sh] Could not determine DOMAIN (from SITE_URL) / EMAIL (from ADMIN_BOOTSTRAP_EMAIL) in ${ENV_DEMO}." >&2
  exit 1
fi

_before="$(cksum "$CERT_DIR/server.crt" 2>/dev/null || true)"

./letsencrypt-cert.sh "$CERT_DIR" "$DOMAIN" "$EMAIL" \
  "runtime-volumes/quickstart-apache-web/acme-challenge" \
  "runtime-volumes/letsencrypt"

_after="$(cksum "$CERT_DIR/server.crt" 2>/dev/null || true)"

if [[ "$_before" != "$_after" ]]; then
  echo "[renew-certs.sh] Certificate renewed — restarting apache-web to load it..."
  source compose-configs/shared-infra/detect-engine.sh
  "$CONTAINER_ENGINE" restart quickstart-web-server
else
  echo "[renew-certs.sh] Certificate unchanged (not yet due for renewal) — nothing to restart."
fi
