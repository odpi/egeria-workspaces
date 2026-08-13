#!/usr/bin/env bash
# Obtain (or renew) a Let's Encrypt certificate via the HTTP-01 challenge and
# install it into CERT_DIR using the server.crt/server.key/server-ca.crt
# layout generate-certs.sh's self-signed certs already use — so
# fastapi-ssl.conf needs no changes regardless of which one is in CERT_DIR.
#
# Usage: ./letsencrypt-cert.sh CERT_DIR DOMAIN EMAIL WEBROOT_DIR [LE_HOME]
#   CERT_DIR    — destination dir for server.crt/server.key/server-ca.crt.
#   DOMAIN      — the public domain to request a cert for. Must already
#                 resolve (DNS A/AAAA record) to this host, and port 80 must
#                 be reachable from the internet on that domain — see
#                 egeria-quickstart-letsencrypt.yaml, which maps it.
#   EMAIL       — contact address for Let's Encrypt expiry/renewal notices.
#   WEBROOT_DIR — host directory serving /.well-known/acme-challenge over
#                 plain HTTP (mounted into apache-web by
#                 egeria-quickstart-letsencrypt.yaml). Apache must already be
#                 running and reachable on port 80 before this runs — see the
#                 --letsencrypt flow in quick-start-local for the bootstrap
#                 order (temporary self-signed cert -> start apache-web ->
#                 run this script -> restart apache-web to load the real one).
#   LE_HOME     — persistent certbot state dir (config/work/logs), default
#                 runtime-volumes/letsencrypt. Reused across renewals so
#                 certbot recognizes the existing cert/account and only
#                 reissues when actually close to expiry.
#
# Requires Docker or Podman — runs the official certbot/certbot image, so
# nothing needs installing on the host. Safe to re-run/schedule: certbot
# skips reissuing a cert that isn't close to expiry (--keep-until-expiring)
# unless deleted. See renew-certs.sh for the scheduled-renewal wrapper.
set -euo pipefail

CERT_DIR="${1:?Usage: letsencrypt-cert.sh CERT_DIR DOMAIN EMAIL WEBROOT_DIR [LE_HOME]}"
DOMAIN="${2:?Usage: letsencrypt-cert.sh CERT_DIR DOMAIN EMAIL WEBROOT_DIR [LE_HOME]}"
EMAIL="${3:?Usage: letsencrypt-cert.sh CERT_DIR DOMAIN EMAIL WEBROOT_DIR [LE_HOME]}"
WEBROOT_DIR="${4:?Usage: letsencrypt-cert.sh CERT_DIR DOMAIN EMAIL WEBROOT_DIR [LE_HOME]}"
LE_HOME="${5:-runtime-volumes/letsencrypt}"

if [[ -n "${CONTAINER_ENGINE:-}" ]]; then
  _engine="$CONTAINER_ENGINE"
elif command -v podman >/dev/null 2>&1; then
  _engine="podman"
else
  _engine="docker"
fi

mkdir -p "$LE_HOME/config" "$LE_HOME/work" "$LE_HOME/logs" "$WEBROOT_DIR" "$CERT_DIR"

echo "[letsencrypt-cert.sh] Requesting/renewing certificate for ${DOMAIN} via HTTP-01 (webroot: ${WEBROOT_DIR}, engine: ${_engine})..."

# Everything — obtaining the cert AND copying it into CERT_DIR's
# server.crt/server.key/server-ca.crt layout — happens inside the container
# as root, because certbot's privkey.pem is 0600 root-owned; copying it out
# to the host as a non-root user would fail with permission denied.
"$_engine" run --rm \
  -v "$(cd "$LE_HOME/config" && pwd)":/etc/letsencrypt \
  -v "$(cd "$LE_HOME/work" && pwd)":/var/lib/letsencrypt \
  -v "$(cd "$LE_HOME/logs" && pwd)":/var/log/letsencrypt \
  -v "$(cd "$WEBROOT_DIR" && pwd)":/webroot \
  -v "$(cd "$CERT_DIR" && pwd)":/output \
  --entrypoint /bin/sh \
  certbot/certbot -c '
    set -e
    certbot certonly --webroot -w /webroot -d "$1" --email "$2" \
      --agree-tos --non-interactive --keep-until-expiring
    cp "/etc/letsencrypt/live/$1/fullchain.pem" /output/server.crt
    cp "/etc/letsencrypt/live/$1/privkey.pem"   /output/server.key
    cp "/etc/letsencrypt/live/$1/chain.pem"     /output/server-ca.crt
    chmod 644 /output/server.crt /output/server.key /output/server-ca.crt
  ' _ "$DOMAIN" "$EMAIL"

echo "[letsencrypt-cert.sh] Installed Let's Encrypt certificate for ${DOMAIN} into ${CERT_DIR}."
