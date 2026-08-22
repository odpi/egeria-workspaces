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
#                 May be a comma-separated list to put several names on one
#                 cert (e.g. "egeria.example.com,home.example.net"); EVERY
#                 name must independently resolve here and pass its own
#                 HTTP-01 challenge, or certbot fails the whole request. The
#                 first name is the primary (CN) and fixes the certbot
#                 lineage name, so renewals stay on one lineage instead of
#                 spawning "<domain>-0001" when the name list changes.
#   EMAIL       — contact address for Let's Encrypt expiry/renewal notices.
#   WEBROOT_DIR — host directory serving /.well-known/acme-challenge over
#                 plain HTTP (mounted into apache-web by
#                 egeria-quickstart-letsencrypt.yaml). NOTE: this is the
#                 challenge directory itself, not a document root, so it is
#                 mounted at /webroot/.well-known/acme-challenge inside the
#                 certbot container — certbot appends that suffix to -w and
#                 mounting it at plain /webroot instead makes it write to
#                 .well-known/acme-challenge/.well-known/acme-challenge/,
#                 which the CA then gets a 404 for. Apache must already be
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

# certbot's state (account key, lineage) CANNOT live on a bind mount under
# Docker Desktop: registering an account fails with "[Errno 95] Not supported"
# writing accounts/.../private_key.json, because that filesystem doesn't
# support the operations certbot uses. Named volumes sit on the VM's real
# filesystem and work everywhere, and they persist across runs — which is
# required, or every renewal would re-register and reissue from scratch.
# Fixed names (not derived from LE_HOME) so an existing account/lineage is
# reused; LE_HOME is still created above and used for the renew.log.
LE_VOL_CONFIG="egeria-le-config"
LE_VOL_WORK="egeria-le-work"
LE_VOL_LOGS="egeria-le-logs"

PRIMARY_DOMAIN="${DOMAIN%%,*}"

echo "[letsencrypt-cert.sh] Requesting/renewing certificate for ${DOMAIN} via HTTP-01 (webroot: ${WEBROOT_DIR}, engine: ${_engine})..."

# Everything — obtaining the cert AND copying it into CERT_DIR's
# server.crt/server.key/server-ca.crt layout — happens inside the container
# as root, because certbot's privkey.pem is 0600 root-owned; copying it out
# to the host as a non-root user would fail with permission denied.
"$_engine" run --rm \
  -v "${LE_VOL_CONFIG}":/etc/letsencrypt \
  -v "${LE_VOL_WORK}":/var/lib/letsencrypt \
  -v "${LE_VOL_LOGS}":/var/log/letsencrypt \
  -v "$(cd "$WEBROOT_DIR" && pwd)":/webroot/.well-known/acme-challenge \
  -v "$(cd "$CERT_DIR" && pwd)":/output \
  --entrypoint /bin/sh \
  certbot/certbot -c '
    set -e
    _domains="$1"; _email="$2"; _primary="$3"
    # Expand the comma-separated list into repeated -d flags.
    _dflags=""
    _rest="$_domains"
    while [ -n "$_rest" ]; do
      _one="${_rest%%,*}"
      [ -n "$_one" ] && _dflags="$_dflags -d $_one"
      [ "$_rest" = "$_one" ] && break
      _rest="${_rest#*,}"
    done
    # --cert-name pins the lineage to the primary name so adding/removing a
    # SAN renews in place rather than creating a parallel "<domain>-0001".
    certbot certonly --webroot -w /webroot $_dflags --email "$_email" \
      --cert-name "$_primary" --agree-tos --non-interactive --keep-until-expiring
    cp "/etc/letsencrypt/live/$_primary/fullchain.pem" /output/server.crt
    cp "/etc/letsencrypt/live/$_primary/privkey.pem"   /output/server.key
    cp "/etc/letsencrypt/live/$_primary/chain.pem"     /output/server-ca.crt
    # Non-fatal: bind mounts under Docker Desktop reject chmod with
    # "Not supported", and the copies are already usable there. Apache reads
    # all three as root at startup before dropping to its runtime user, so the
    # key never needs to be group/world-readable.
    chmod 644 /output/server.crt /output/server-ca.crt 2>/dev/null || true
    chmod 600 /output/server.key 2>/dev/null || true
  ' _ "$DOMAIN" "$EMAIL" "$PRIMARY_DOMAIN"

echo "[letsencrypt-cert.sh] Installed Let's Encrypt certificate for ${DOMAIN} into ${CERT_DIR}."
