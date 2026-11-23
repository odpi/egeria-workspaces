#!/usr/bin/env bash
# NEEDS the freshstart Ingress refusal lifted (branch tr112-lift-freshstart-ingress-refusal) and the egeria-stack re.enabled option (tr112-re-in-stack): on either branch alone the install is refused.
# One freshstart demo stack on kind, with Resource Explorer enabled in the umbrella (re.enabled) and the Portal behind ingress-nginx.
# Also proves PO-83 (a separate 429 budget per client; needs a Portal image with #914) and prints the worker's Egeria errors in full.
# Proves: (1) the freshstart Ingress is allowed and a Portal image with PO-78 answers an anonymous read with 401, a page with 302 /login,
# and a signed-in read with 200; helm test (with its PO-78 canary step) passes; (2) the umbrella derives RE's platform URL, view server
# and CA settings so RE reaches the platform and `helm test` passes for it.
# usage: kind_stack_re_ingress.sh <namespace> [release]
#   env: PORTAL_TAG (portal-freshstart + apache-web tag), RE_TAG, REGISTRY (default tr112-registry:5000), INGRESS_PORT (local port, default 18080)
# Secret values are generated here or read from tracked demo files and are never printed. Test infrastructure only, NOT part of any chart.
set -euo pipefail
kubectl config current-context | grep -q "^kind-" || { echo "not a kind context" >&2; exit 2; }
NS=${1:?namespace}; REL=${2:-st}
HERE=$(cd "$(dirname "$(readlink -f "$0")")" && pwd); CHARTS=$(dirname "$HERE")
REG=${REGISTRY:-tr112-registry:5000}; PTAG=${PORTAL_TAG:-odpi-f62b5baa}; RTAG=${RE_TAG:-main-4867b7b0}
HOST=portal.test; LP=${INGRESS_PORT:-18080}
W=$(mktemp -d); trap 'rm -rf "$W"; [ -n "${PF:-}" ] && kill "$PF" 2>/dev/null || true' EXIT; umask 077

bash "$HERE/kind_infra.sh" "$NS" >/dev/null
kubectl -n "$NS" rollout status deploy/postgres --timeout=180s >/dev/null

# RE database: owner role (schema Job) and runtime role (pods); the admin creates the extension
openssl rand -hex 16 | tr -d '\n' > "$W/owner-pw"; openssl rand -hex 16 | tr -d '\n' > "$W/rt-pw"
OPW=$(cat "$W/owner-pw"); RPW=$(cat "$W/rt-pw")
kubectl -n "$NS" exec -i deploy/postgres -- psql -p 5442 -U postgres -v ON_ERROR_STOP=1 -q >/dev/null <<SQL
DROP DATABASE IF EXISTS re_proof;
DROP ROLE IF EXISTS re_rt; DROP ROLE IF EXISTS re_owner;
CREATE ROLE re_owner LOGIN PASSWORD '$OPW';
CREATE ROLE re_rt LOGIN PASSWORD '$RPW';
CREATE DATABASE re_proof OWNER re_owner;
\c re_proof
CREATE EXTENSION IF NOT EXISTS vector;
ALTER DEFAULT PRIVILEGES FOR ROLE re_owner GRANT USAGE ON SCHEMAS TO re_rt;
ALTER DEFAULT PRIVILEGES FOR ROLE re_owner GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO re_rt;
ALTER DEFAULT PRIVILEGES FOR ROLE re_owner GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO re_rt;
SQL
unset OPW RPW
kubectl -n "$NS" create secret generic re-owner-db --from-file=password="$W/owner-pw" --dry-run=client -o yaml | kubectl apply -f - >/dev/null
kubectl -n "$NS" create secret generic re-db --from-file=password="$W/rt-pw" --dry-run=client -o yaml | kubectl apply -f - >/dev/null
# RE's Egeria service account (and the sign-in account used below): the non-personal account of the tracked freshstart user directory
python3 -I - "$CHARTS/egeria-platform/files/freshstart/secrets/egeria-user-directory.omsecrets" "$W" <<'PY'
import sys, yaml
u = yaml.safe_load(open(sys.argv[1]))["secretsCollections"]["userDirectory"]["users"]["omagspcatnpa"]["secrets"]["clearPassword"]
open(sys.argv[2] + "/egeria-pw", "w").write(u)
PY
kubectl -n "$NS" create secret generic re-egeria --from-file=password="$W/egeria-pw" --dry-run=client -o yaml | kubectl apply -f - >/dev/null

for c in egeria-platform egeria-portal trellis-re; do helm dependency update "$CHARTS/$c" >/dev/null; done
helm dependency update "$CHARTS/egeria-stack" >/dev/null
T0=$(date +%s)
helm upgrade --install "$REL" "$CHARTS/egeria-stack" -n "$NS" -f "$CHARTS/egeria-stack/values-demo.yaml" -f "$CHARTS/egeria-stack/values-freshstart.yaml" \
  --set core.postgres.host=postgres --set core.kafka.bootstrapServers="kafka.$NS.svc.cluster.local:9192" \
  --set core.persistence.storageClassName=standard --set portal.persistence.storageClassName=standard \
  --set portal.images.portal.repository="$REG/portal-freshstart" --set portal.images.portal.tag="$PTAG" \
  --set portal.images.apache.repository="$REG/apache-web" --set portal.images.apache.tag="$PTAG" \
  --set portal.ingress.enabled=true --set portal.ingress.className=nginx --set portal.ingress.host=$HOST --set portal.networkPolicy.enabled=true \
  --set re.enabled=true --set re.image.repository="$REG/trellis/resource-explorer" --set re.image.tag="$RTAG" \
  --set re.database.host=postgres --set re.database.port=5442 --set re.database.name=re_proof --set re.database.user=re_rt --set re.database.existingSecret=re-db \
  --set re.database.owner.user=re_owner --set re.database.owner.existingSecret=re-owner-db \
  --set re.egeria.daemon.userId=omagspcatnpa --set re.egeria.daemon.existingSecret=re-egeria \
  --set re.persistence.storageClassName=standard --set 're.persistence.accessModes={ReadWriteOnce}' >/dev/null
echo "installed $REL in $NS at $(date -u +%T)"
POD=$REL-platform-0
for i in $(seq 1 120); do
  r=$(kubectl -n "$NS" get pod "$POD" -o jsonpath='{.status.containerStatuses[?(@.name=="platform")].ready}' 2>/dev/null || true)
  [ "$r" = true ] && break; sleep 10
done
n=0; for i in $(seq 1 60); do n=$(kubectl -n "$NS" logs "$POD" -c platform 2>/dev/null | grep -c SERVER-OPS-0004 || true); [ "$n" -ge 5 ] && break; sleep 10; done
echo "platform ready after $(( $(date +%s) - T0 ))s; servers started: $n"
kubectl -n "$NS" rollout status deploy/$REL-portal --timeout=300s >/dev/null || true
kubectl -n "$NS" get pods
kubectl -n "$NS" get ingress
echo "=== RE environment (derived by the umbrella)"
kubectl -n "$NS" exec deploy/$REL-re-web -- sh -c 'echo EGERIA_PLATFORM_URL=$EGERIA_PLATFORM_URL EGERIA_VIEW_SERVER=$EGERIA_VIEW_SERVER PYEGERIA_SSL_VERIFY=$PYEGERIA_SSL_VERIFY' 2>&1 | tail -1

echo "=== helm test (platform, Portal canary with the PO-78 step, Resource Explorer)"
helm test "$REL" -n "$NS" --logs 2>&1 | grep -E "^ok|^FAIL|^PASS|Phase|TEST SUITE|Error" || true

echo "=== through ingress-nginx (Host: $HOST), freshstart"
kubectl -n ingress-nginx port-forward svc/ingress-nginx-controller $LP:80 >/dev/null 2>&1 & PF=$!
sleep 4
IN=http://127.0.0.1:$LP
code() { curl -s -o /dev/null -m 20 -w '%{http_code}' -H "Host: $HOST" "$@"; }
echo "anonymous GET /api/operations/platforms: HTTP $(code $IN/api/operations/platforms)   (401 expected)"
echo "anonymous GET /portal: HTTP $(curl -s -o /dev/null -m 20 -w '%{http_code} -> %{redirect_url}' -H "Host: $HOST" $IN/portal | sed "s#http://$HOST##")   (302 -> /login expected)"
python3 -I - "$W" <<'PY'
import json, sys
w = sys.argv[1]
open(w + "/login.json", "w").write(json.dumps({"user_id": "omagspcatnpa", "password": open(w + "/egeria-pw").read()}))
PY
# The password goes in a file (umask 077), never in curl's argv. An Egeria token alone is not a Portal session (PO-78): sign in at /api/auth/login and keep the demo_token cookie.
LOGIN=$(curl -s -m 30 -o /dev/null -w '%{http_code}' -c "$W/jar" -H "Host: $HOST" -H 'Content-Type: application/json' --data @"$W/login.json" $IN/api/auth/login)
echo "sign-in (POST /api/auth/login): HTTP $LOGIN"
echo "signed-in GET /api/operations/platforms: HTTP $(code -b "$W/jar" $IN/api/operations/platforms)   (200 expected)"
echo "signed-in GET /portal: HTTP $(code -b "$W/jar" $IN/portal)   (200 expected)"
echo "=== PO-83: separate sign-in budget per client (two pods, straight to the Apache front door, bad password, 10/minute per client)"
for c in a b; do
  kubectl -n "$NS" get pod client-$c >/dev/null 2>&1 || kubectl -n "$NS" run client-$c --image="$REG/trellis/resource-explorer:$RTAG" --restart=Never --command -- sleep 3600 >/dev/null
done
kubectl -n "$NS" wait --for=condition=Ready pod/client-a pod/client-b --timeout=180s >/dev/null
bad() { kubectl -n "$NS" exec "client-$1" -- curl -s -o /dev/null -m 15 -w '%{http_code}' -X POST -H 'Content-Type: application/json' \
  -d '{"user_id":"nobody","password":"wrong-password"}' http://$REL-portal-web:8085/api/auth/login; }
OUT=""; for _ in $(seq 1 12); do OUT="$OUT $(bad a)"; done
echo "client A, 12 bad sign-ins:$OUT   (401s, then 429)"
echo "client B, 1 bad sign-in right after: $(bad b)   (401 = B has its own budget)"
kubectl -n "$NS" exec deploy/$REL-portal -- sh -c 'echo PORTAL_TRUSTED_PROXIES=$PORTAL_TRUSTED_PROXIES' 2>&1 | tail -1
echo "=== RE worker: any Egeria error (full text)"
kubectl -n "$NS" logs deploy/$REL-re-worker 2>&1 | grep -n -B2 -A14 "Egeria detected error" | head -60 || true
echo "=== Resource Explorer: the schema Job and its pods"
kubectl -n "$NS" get job,pods 2>&1 | grep -i "re-" || true
