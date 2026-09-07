#!/usr/bin/env bash
# Scheduled renewal for the wildcard Let's Encrypt certificate obtained via
# letsencrypt-wildcard-cert.sh (DNS-01 against IONOS) — the
# runtime-volumes/certs-wildcard counterpart to renew-certs.sh's
# certs-letsencrypt/HTTP-01 flow.
#
# Schedule this via cron, e.g.:
#   0 3 * * * cd /path/to/egeria-workspaces && ./renew-wildcard-cert.sh >> runtime-volumes/certs-wildcard-renew.log 2>&1
#
# No cert-watch.sh equivalent needed here: DNS-01 doesn't depend on port 80
# being reachable from the internet, so unlike the HTTP-01 flow there is no
# "please open port 80" email dance — a plain nightly cron is sufficient, and
# certbot's own --keep-until-expiring makes a no-op check safe to run daily.
#
# IONOS_CREDENTIALS_FILE overrides the default credentials path if needed.
set -euo pipefail
cd "$(dirname "$0")"

ENV_DEMO="compose-configs/egeria-quickstart/.env.demo"
if [[ ! -f "$ENV_DEMO" ]]; then
  echo "[renew-wildcard-cert.sh] ${ENV_DEMO} not found — nothing to renew (this host isn't running demo mode)." >&2
  exit 1
fi

_get() { grep -E "^$1=" "$ENV_DEMO" | head -n1 | cut -d= -f2- || true; }

CERT_DIR="$(_get CERT_DIR)"
EMAIL="$(_get ADMIN_BOOTSTRAP_EMAIL)"
CREDENTIALS_FILE="${IONOS_CREDENTIALS_FILE:-$HOME/.config/egeria-quickstart/ionos-credentials.ini}"

if [[ -z "$CERT_DIR" || "$CERT_DIR" != *"/runtime-volumes/certs-wildcard" ]]; then
  echo "[renew-wildcard-cert.sh] CERT_DIR (${CERT_DIR:-unset}) isn't the wildcard cert output path — nothing to renew here." >&2
  exit 0
fi

# The wildcard itself is hardcoded, not derived from .env.demo — this script
# is specifically the pdr-associates.com wildcard renewal, not a generic
# any-domain one (that's letsencrypt-wildcard-cert.sh, called directly).
#
# Optional extra names, comma-separated, e.g. CERT_EXTRA_DOMAINS=foo.example.net
# in .env.demo, for a name the wildcard doesn't cover (different apex, like
# home.wolfsonnet.com below).
DOMAINS="pdr-associates.com,*.pdr-associates.com"
EXTRA_DOMAINS="$(_get CERT_EXTRA_DOMAINS)"
if [[ -n "$EXTRA_DOMAINS" ]]; then
  DOMAINS="${DOMAINS},${EXTRA_DOMAINS}"
fi

# Self-healing, same reasoning as renew-certs.sh: also carry over every SAN
# already on the installed cert that isn't covered above (e.g.
# home.wolfsonnet.com), so a .env.demo regression (gen-env.sh rewrites it
# every run) can't silently drop a name from the next renewal — see
# renew-certs.sh's own comment for the 2026-08-22 incident this pattern
# defends against. Skipped on a first issuance, when there's no cert yet to
# read.
if [[ -r "${CERT_DIR}/server.crt" ]]; then
  while read -r _san; do
    [[ -n "$_san" ]] || continue
    case ",${DOMAINS}," in
      *",${_san},"*) ;;                      # already present (or covered by the wildcard)
      *) DOMAINS="${DOMAINS},${_san}"
         echo "[renew-wildcard-cert.sh] Preserving existing SAN from installed cert: ${_san}" >&2 ;;
    esac
  done < <(openssl x509 -in "${CERT_DIR}/server.crt" -noout -ext subjectAltName 2>/dev/null \
             | tr ',' '\n' | sed -n 's/.*DNS://p' | tr -d ' ')
fi

if [[ -z "$EMAIL" ]]; then
  echo "[renew-wildcard-cert.sh] Could not determine EMAIL (from ADMIN_BOOTSTRAP_EMAIL) in ${ENV_DEMO}." >&2
  exit 1
fi

_before="$(cksum "$CERT_DIR/server.crt" 2>/dev/null || true)"

./letsencrypt-wildcard-cert.sh "$CERT_DIR" "$DOMAINS" "$EMAIL" "$CREDENTIALS_FILE"

_after="$(cksum "$CERT_DIR/server.crt" 2>/dev/null || true)"

if [[ "$_before" != "$_after" ]]; then
  echo "[renew-wildcard-cert.sh] Certificate renewed — reloading apache-web to pick it up..."
  source compose-configs/shared-infra/detect-engine.sh
  # Graceful reload, not a restart: httpd re-reads the cert files without
  # dropping in-flight connections, unlike renew-certs.sh's container restart
  # (that one restarts because its Let's Encrypt overlay also changes the
  # port 80 mount on the first run; this cert's vhosts have no such mount to
  # pick up, so a reload is enough).
  "$CONTAINER_ENGINE" exec quickstart-web-server httpd -k graceful
else
  echo "[renew-wildcard-cert.sh] Certificate unchanged (not yet due for renewal) — nothing to reload."
fi
