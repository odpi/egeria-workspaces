#!/bin/bash
# Generate self-signed certificates for Egeria Quickstart SSL

CERT_DIR="runtime-volumes/certs"
DOMAIN="egeria.pdr-associates.com"

if [ ! -d "$CERT_DIR" ]; then
    mkdir -p "$CERT_DIR"
fi

echo "Generating self-signed certificates in $CERT_DIR for $DOMAIN..."

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout "$CERT_DIR/server.key" \
    -out "$CERT_DIR/server.crt" \
    -subj "/C=US/ST=State/L=City/O=Egeria/OU=Quickstart/CN=$DOMAIN"

# For the chain file, we can just copy the crt for self-signed
cp "$CERT_DIR/server.crt" "$CERT_DIR/server-ca.crt"

chmod 644 "$CERT_DIR/server.crt" "$CERT_DIR/server.key" "$CERT_DIR/server-ca.crt"

echo "Done. Files generated:"
ls -l "$CERT_DIR"
