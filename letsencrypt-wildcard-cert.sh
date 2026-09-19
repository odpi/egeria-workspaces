#!/usr/bin/env bash
# Obtain (or renew) a wildcard Let's Encrypt certificate via DNS-01 against
# IONOS DNS, using certbot-dns-ionos (compose-configs/egeria-quickstart/
# Dockerfile-certbot-ionos). Installs into CERT_DIR using the
# server.crt/server.key/server-ca.crt layout every other cert source in this
# repo uses (generate-certs.sh's self-signed certs, letsencrypt-cert.sh's
# HTTP-01 certs) — so fastapi-ssl.conf and trellis-ssl-vhosts.conf need no
# changes regardless of which one is active in CERT_DIR.
#
# Unlike letsencrypt-cert.sh (HTTP-01), this needs no port 80, no router
# forward, and no Apache running first: DNS-01 proves domain control by
# creating a TXT record via IONOS's API, which the plugin also removes when
# done. That also means one cert can cover a wildcard (*.example.com) plus any
# number of apex/extra names in a single request, across multiple zones, as
# long as the same IONOS account manages all of them.
#
# Usage: ./letsencrypt-wildcard-cert.sh CERT_DIR DOMAINS EMAIL CREDENTIALS_FILE
#   CERT_DIR         — destination dir for server.crt/server.key/server-ca.crt.
#   DOMAINS          — comma-separated list, e.g.
#                       "pdr-associates.com,*.pdr-associates.com,home.wolfsonnet.com".
#                       First name is the primary (CN) and fixes the certbot
#                       lineage name (--cert-name), same reasoning as
#                       letsencrypt-cert.sh: keep it first and stable across
#                       calls, or a renewal spawns a parallel
#                       "<name>-0001" lineage instead of renewing in place.
#   EMAIL            — contact address for Let's Encrypt expiry/renewal notices.
#   CREDENTIALS_FILE — path to an IONOS Developer API credentials.ini with
#                       dns_ionos_prefix / dns_ionos_secret (see
#                       developer.hosting.ionos.com -> API Keys). Keep this
#                       OUTSIDE the repo entirely (e.g.
#                       ~/.config/egeria-quickstart/ionos-credentials.ini,
#                       mode 600) rather than merely gitignored inside it — a
#                       credential that grants DNS write access deserves a
#                       stronger guarantee than "not staged by accident".
#
# certbot state (account key, lineage, renewal config) lives in fixed-name
# Docker volumes, same reasoning as letsencrypt-cert.sh: bind mounts can't
# hold certbot's 0600 account key under Docker Desktop, and fixed names mean
# a renewal reuses the existing account/lineage instead of re-registering.
#
# Safe to re-run/schedule: certbot skips reissuing a cert that isn't close to
# expiry (--keep-until-expiring) unless the lineage is deleted. See
# renew-wildcard-cert.sh for the scheduled-renewal wrapper.
set -euo pipefail
cd "$(dirname "$0")"

CERT_DIR="${1:?Usage: letsencrypt-wildcard-cert.sh CERT_DIR DOMAINS EMAIL CREDENTIALS_FILE}"
DOMAINS="${2:?Usage: letsencrypt-wildcard-cert.sh CERT_DIR DOMAINS EMAIL CREDENTIALS_FILE}"
EMAIL="${3:?Usage: letsencrypt-wildcard-cert.sh CERT_DIR DOMAINS EMAIL CREDENTIALS_FILE}"
CREDENTIALS_FILE="${4:?Usage: letsencrypt-wildcard-cert.sh CERT_DIR DOMAINS EMAIL CREDENTIALS_FILE}"

if [[ -n "${CONTAINER_ENGINE:-}" ]]; then
  _engine="$CONTAINER_ENGINE"
elif command -v podman >/dev/null 2>&1; then
  _engine="podman"
else
  _engine="docker"
fi

if [[ ! -r "$CREDENTIALS_FILE" ]]; then
  echo "[letsencrypt-wildcard-cert.sh] Credentials file not found or unreadable: ${CREDENTIALS_FILE}" >&2
  exit 1
fi
_creds_dir="$(cd "$(dirname "$CREDENTIALS_FILE")" && pwd)"
_creds_name="$(basename "$CREDENTIALS_FILE")"

IMAGE="egeria-quickstart-certbot-ionos:latest"
echo "[letsencrypt-wildcard-cert.sh] Building ${IMAGE} (cheap/cached if Dockerfile-certbot-ionos is unchanged)..."
"$_engine" build -q -t "$IMAGE" -f compose-configs/egeria-quickstart/Dockerfile-certbot-ionos compose-configs/egeria-quickstart >/dev/null

mkdir -p "$CERT_DIR"

# Fixed names (not derived from CERT_DIR) so an existing account/lineage is
# reused across calls — mirrors letsencrypt-cert.sh's egeria-le-config/work/logs.
LE_VOL_CONFIG="egeria-le-wildcard-config"
LE_VOL_WORK="egeria-le-wildcard-work"
LE_VOL_LOGS="egeria-le-wildcard-logs"

PRIMARY_DOMAIN="${DOMAINS%%,*}"
HOST_UID="$(id -u)"
HOST_GID="$(id -g)"

echo "[letsencrypt-wildcard-cert.sh] Requesting/renewing certificate for ${DOMAINS} via DNS-01/IONOS (engine: ${_engine})..."

# Everything happens inside the container as root, same reasoning as
# letsencrypt-cert.sh — certbot's privkey.pem is 0600 root-owned. Unlike that
# script, we chown the copies to the invoking host user afterward instead of
# relying on Docker Desktop's bind-mount UID translation, so this also works
# correctly under a plain Linux dockerd, where a bind-mounted file created by
# container root is root-owned on the host too.
"$_engine" run --rm \
  -v "${LE_VOL_CONFIG}":/etc/letsencrypt \
  -v "${LE_VOL_WORK}":/var/lib/letsencrypt \
  -v "${LE_VOL_LOGS}":/var/log/letsencrypt \
  -v "${_creds_dir}/${_creds_name}":/creds/ionos-credentials.ini:ro \
  -v "$(cd "$CERT_DIR" && pwd)":/output \
  --entrypoint /bin/sh \
  "$IMAGE" -c '
    set -e
    _domains="$1"; _email="$2"; _primary="$3"; _uid="$4"; _gid="$5"
    # Expand the comma-separated list into repeated -d flags.
    _dflags=""
    _rest="$_domains"
    while [ -n "$_rest" ]; do
      _one="${_rest%%,*}"
      [ -n "$_one" ] && _dflags="$_dflags -d $_one"
      [ "$_rest" = "$_one" ] && break
      _rest="${_rest#*,}"
    done
    certbot certonly \
      --authenticator dns-ionos \
      --dns-ionos-credentials /creds/ionos-credentials.ini \
      --dns-ionos-propagation-seconds 60 \
      $_dflags --email "$_email" \
      --cert-name "$_primary" --agree-tos --non-interactive --keep-until-expiring
    cp "/etc/letsencrypt/live/$_primary/fullchain.pem" /output/server.crt
    cp "/etc/letsencrypt/live/$_primary/privkey.pem"   /output/server.key
    cp "/etc/letsencrypt/live/$_primary/chain.pem"     /output/server-ca.crt
    chmod 644 /output/server.crt /output/server-ca.crt
    chmod 600 /output/server.key
    chown "${_uid}:${_gid}" /output/server.crt /output/server.key /output/server-ca.crt
  ' _ "$DOMAINS" "$EMAIL" "$PRIMARY_DOMAIN" "$HOST_UID" "$HOST_GID"

echo "[letsencrypt-wildcard-cert.sh] Installed wildcard certificate for ${DOMAINS} into ${CERT_DIR}."
