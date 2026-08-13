#!/bin/bash
# Generate a self-signed TLS certificate (server.crt/server.key/server-ca.crt)
# for Apache's fastapi-ssl.conf vhost.
#
# Usage: ./generate-certs.sh [CERT_DIR] [DOMAIN]
#   CERT_DIR — output directory (default: runtime-volumes/certs)
#   DOMAIN   — certificate CN / subject (default: egeria.pdr-associates.com)
#
# Called automatically by quick-start-local / fresh-start-local to provision
# a fallback self-signed cert when no CERT_DIR is configured (non-demo mode).
# Can also be run manually for ad hoc local HTTPS testing.
set -euo pipefail

CERT_DIR="${1:-runtime-volumes/certs}"
DOMAIN="${2:-egeria.pdr-associates.com}"

mkdir -p "$CERT_DIR"

echo "[generate-certs.sh] Generating self-signed certificate in ${CERT_DIR} for ${DOMAIN}..."

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout "$CERT_DIR/server.key" \
    -out "$CERT_DIR/server.crt" \
    -subj "/C=US/ST=State/L=City/O=Egeria/OU=Quickstart/CN=$DOMAIN"

# For the chain file, we can just copy the crt for self-signed
cp "$CERT_DIR/server.crt" "$CERT_DIR/server-ca.crt"

chmod 644 "$CERT_DIR/server.crt" "$CERT_DIR/server.key" "$CERT_DIR/server-ca.crt"

echo "[generate-certs.sh] Done. Files generated:"
ls -l "$CERT_DIR"
