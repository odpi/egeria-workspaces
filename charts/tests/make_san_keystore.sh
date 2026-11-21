#!/usr/bin/env bash
# Makes a throwaway CA and a server certificate with SANs for an egeria-platform release, as PKCS12 keystore and truststore
# with random passwords (never the public demo ones). For tests only: it proves the production TLS path with hostname checks on.
# usage: make_san_keystore.sh <outdir> <namespace> <platform-service-name> [key-alias]
# writes: keystore.p12 truststore.p12 ca.crt keystore-password truststore-password key-alias   (passwords are files; never printed)
set -euo pipefail
OUT=${1:?outdir}; NS=${2:?namespace}; SVC=${3:?service name}; ALIAS=${4:-egeriaserverchassis}
umask 077; mkdir -p "$OUT"; cd "$OUT"
KPW=$(openssl rand -hex 16); TPW=$(openssl rand -hex 16)
printf %s "$KPW" > keystore-password; printf %s "$TPW" > truststore-password; printf %s "$ALIAS" > key-alias
openssl req -x509 -newkey rsa:2048 -nodes -keyout ca.key -out ca.crt -days 3 -subj "/CN=egeria-test-ca" 2>/dev/null
openssl req -newkey rsa:2048 -nodes -keyout server.key -out server.csr -subj "/CN=$SVC" 2>/dev/null
cat > san.cnf <<CNF
subjectAltName=DNS:$SVC,DNS:$SVC.$NS,DNS:$SVC.$NS.svc,DNS:$SVC.$NS.svc.cluster.local,DNS:$SVC-hl,DNS:$SVC-hl.$NS.svc.cluster.local,DNS:localhost,IP:127.0.0.1
extendedKeyUsage=serverAuth,clientAuth
CNF
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 3 -extfile san.cnf 2>/dev/null
cat server.crt ca.crt > chain.crt
openssl pkcs12 -export -inkey server.key -in chain.crt -name "$ALIAS" -out keystore.p12 -passout "pass:$KPW" 2>/dev/null
# the truststore holds the CA, so the platform trusts what it signed
openssl pkcs12 -export -nokeys -in ca.crt -name egeria-test-ca -out truststore.p12 -passout "pass:$TPW" -jdktrust anyExtendedKeyUsage 2>/dev/null || \
  openssl pkcs12 -export -nokeys -in ca.crt -name egeria-test-ca -out truststore.p12 -passout "pass:$TPW" 2>/dev/null
rm -f ca.key server.key server.csr san.cnf chain.crt server.crt ca.srl
ls keystore.p12 truststore.p12 ca.crt >/dev/null
echo "made keystore.p12, truststore.p12 and ca.crt in $OUT (SANs: $SVC, $SVC.$NS.svc.cluster.local, $SVC-hl.$NS.svc.cluster.local, localhost)"
