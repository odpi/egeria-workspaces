#!/usr/bin/env bash
# PO-83 on a kind cluster: the Portal's auth rate limits count per REAL client IP when the chart sets PORTAL_TRUSTED_PROXIES to the headless
# Service of the Apache pods, and everyone shares one budget when it does not. Installs egeria-portal alone (quickstart demoMode: its sign-in is local,
# so no Egeria platform is needed for the 401/429 behaviour) with the NetworkPolicy, then drives POST /api/auth/login (10/minute per client) from two pods.
# usage: kind_trusted_proxies.sh <namespace> [release]      env: PORTAL_TAG (default po83-cd4ebc84; the Portal image must contain PO-83)
#   CLIENT_IMAGE: any image with curl (default the RE image tr112-registry:5000/trellis/resource-explorer:tr112d-73b5bfcc)
# Secret values are generated here and never printed. Test only.
set -euo pipefail
NS=${1:?namespace}; REL=${2:-pt}
HERE=$(cd "$(dirname "$(readlink -f "$0")")" && pwd); CHARTS=$(dirname "$HERE")
REG=${REGISTRY:-tr112-registry:5000}; TAG=${PORTAL_TAG:-po83-cd4ebc84}
CLIENT=${CLIENT_IMAGE:-$REG/trellis/resource-explorer:tr112d-73b5bfcc}
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT; umask 077
kubectl get ns "$NS" >/dev/null 2>&1 || kubectl create ns "$NS" >/dev/null
# The Portal's demo sign-in database is Postgres in current images (demo_db.py: DEMO_DB_*, schema demo_auth in database coco_pharma): the test
# Postgres from kind_infra.sh, with a demo_user role. (Without it the sign-in answers 500, though the rate limit still counts first.)
bash "$HERE/kind_infra.sh" "$NS" >/dev/null
kubectl -n "$NS" rollout status deploy/postgres --timeout=180s >/dev/null
kubectl -n "$NS" exec -i deploy/postgres -- psql -p 5442 -U postgres -q >/dev/null 2>&1 <<SQL || true
CREATE ROLE demo_user LOGIN PASSWORD 'demo4egeria';
CREATE DATABASE coco_pharma OWNER demo_user;
SQL
openssl rand -hex 16 | tr -d '\n' > "$W/pw"
kubectl -n "$NS" create secret generic demo-admin --from-file=password="$W/pw" --dry-run=client -o yaml | kubectl apply -f - >/dev/null
cat > "$W/v.yaml" <<YAML
extraEnv:
  - {name: ADMIN_BOOTSTRAP_EMAIL, value: admin@example.test}
  - {name: ADMIN_BOOTSTRAP_PASSWORD, valueFrom: {secretKeyRef: {name: demo-admin, key: password}}}
  - {name: DEMO_DB_HOST, value: postgres}
  - {name: DEMO_DB_PORT, value: "5442"}
YAML
helm dependency update "$CHARTS/egeria-portal" >/dev/null
install() {   # extra helm args
  helm upgrade --install "$REL" "$CHARTS/egeria-portal" -n "$NS" -f "$CHARTS/egeria-portal/values-demo.yaml" -f "$W/v.yaml" \
    --set environment=quickstart --set demoMode=true --set platform.serviceName=no-platform \
    --set images.portal.repository="$REG/portal-quickstart" --set images.portal.tag="$TAG" \
    --set images.apache.repository="$REG/apache-web" --set images.apache.tag="$TAG" \
    --set networkPolicy.enabled=true "$@" --wait --timeout 5m >/dev/null
  kubectl -n "$NS" rollout status deploy/$REL-portal --timeout=180s >/dev/null
}
for c in a b; do
  kubectl -n "$NS" get pod client-$c >/dev/null 2>&1 || kubectl -n "$NS" run client-$c --image="$CLIENT" --restart=Never --command -- sleep 3600 >/dev/null
done
kubectl -n "$NS" wait --for=condition=Ready pod/client-a pod/client-b --timeout=180s >/dev/null
WEB=http://$REL-portal-web:8085
login() {   # <client> -> the HTTP status of one bad sign-in through Apache
  kubectl -n "$NS" exec "client-$1" -- curl -s -o /dev/null -m 15 -w '%{http_code}' -X POST -H 'Content-Type: application/json' \
    -d '{"email":"nobody@example.com","password":"wrong-password"}' "$WEB/api/auth/login"
}
burst() {   # <client> <n>
  local out=""; for _ in $(seq 1 "$2"); do out="$out $(login "$1")"; done; echo "$out"
}

echo "=== 1. the chart's default: PORTAL_TRUSTED_PROXIES = the headless Apache Service"
install
kubectl -n "$NS" exec deploy/$REL-portal -- sh -c 'echo PORTAL_TRUSTED_PROXIES=$PORTAL_TRUSTED_PROXIES'
echo "client A, 12 bad sign-ins:$(burst a 12)"
echo "client B, 1 bad sign-in right after: $(login b)   (not 429 = B has its own budget)"
echo "=== 2. control: a trusted-proxy list that does not include Apache (everyone shares Apache's address)"
install --set trustedProxies=127.0.0.1
kubectl -n "$NS" exec deploy/$REL-portal -- sh -c 'echo PORTAL_TRUSTED_PROXIES=$PORTAL_TRUSTED_PROXIES'
echo "client A, 12 bad sign-ins:$(burst a 12)"
echo "client B, 1 bad sign-in right after: $(login b)   (429 = B is locked out by A: the shared budget)"
echo "=== 3. the Portal on 8000 is reachable only through Apache"
echo "client B straight to the Portal Service on 8000: HTTP $(kubectl -n "$NS" exec client-b -- curl -s -o /dev/null -m 6 -w '%{http_code}' http://$REL-portal:8000/ || true)   (000 = blocked by the NetworkPolicy)"
echo "client B through Apache /portal: HTTP $(kubectl -n "$NS" exec client-b -- curl -s -o /dev/null -m 15 -w '%{http_code}' $WEB/portal)"
