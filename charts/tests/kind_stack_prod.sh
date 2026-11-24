#!/usr/bin/env bash
# Production-style install of egeria-stack (freshstart) on a kind cluster: external test Postgres and Kafka, a keystore of our own
# with SANs and random passwords (hostname checks ON, tls.verify true), existing Secrets, image digests, NetworkPolicies, then helm test.
# usage: kind_stack_prod.sh <namespace> [release]      env: PORTAL_TAG (default freshstart-6.3-a79109b7) APACHE_TAG (default 6.3-a79109b7)
#                                                      REGISTRY (default tr112-registry:5000; the kind nodes must be able to pull it)
# Secret values are generated here or read from the tracked demo files and are never printed.
set -euo pipefail
kubectl config current-context | grep -q "^kind-" || { echo "not a kind context" >&2; exit 2; }
NS=${1:?namespace}; REL=${2:-ps}
HERE=$(cd "$(dirname "$(readlink -f "$0")")" && pwd); CHARTS=$(dirname "$HERE")
REG=${REGISTRY:-tr112-registry:5000}; PTAG=${PORTAL_TAG:-freshstart-6.3-a79109b7}; ATAG=${APACHE_TAG:-6.3-a79109b7}
HELM=${HELM:-helm}
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT; umask 077

bash "$HERE/kind_infra.sh" "$NS"
bash "$HERE/make_san_keystore.sh" "$W/tls" "$NS" "$REL-platform" >/dev/null
SECDIR=$CHARTS/egeria-platform/files/freshstart/secrets
kubectl -n "$NS" create secret generic prod-secrets --from-file="$SECDIR" --dry-run=client -o yaml | kubectl apply -f - >/dev/null
kubectl -n "$NS" create secret generic prod-tls --from-file="$W/tls/keystore.p12" --from-file="$W/tls/truststore.p12" --from-file="$W/tls/ca.crt" \
  --from-file=keystore-password="$W/tls/keystore-password" --from-file=truststore-password="$W/tls/truststore-password" \
  --from-file=key-alias="$W/tls/key-alias" --dry-run=client -o yaml | kubectl apply -f - >/dev/null
kubectl -n "$NS" create secret generic prod-ca --from-file=ca.crt="$W/tls/ca.crt" --dry-run=client -o yaml | kubectl apply -f - >/dev/null
# non-personal canary account and the Portal's Egeria user, from the tracked demo user directory
python3 -I - "$SECDIR/egeria-user-directory.omsecrets" "$W" <<'PY'
import sys, yaml
u = yaml.safe_load(open(sys.argv[1]))["secretsCollections"]["userDirectory"]["users"]
w = sys.argv[2]
open(w + "/canary-user", "w").write("omagspcatnpa")
open(w + "/canary-pw", "w").write(u["omagspcatnpa"]["secrets"]["clearPassword"])
open(w + "/portal-egeria-pw", "w").write(u["bootstrap"]["secrets"]["clearPassword"])
PY
openssl rand -hex 24 > "$W/jwt"; openssl rand -hex 16 > "$W/mcp"
kubectl -n "$NS" create secret generic prod-canary --from-file=userId="$W/canary-user" --from-file=password="$W/canary-pw" --dry-run=client -o yaml | kubectl apply -f - >/dev/null
kubectl -n "$NS" create secret generic prod-portal --from-file=jwt-secret="$W/jwt" --from-file=mcp-access-token="$W/mcp" \
  --from-file=egeria-user-password="$W/portal-egeria-pw" --dry-run=client -o yaml | kubectl apply -f - >/dev/null

digest() { sg docker -c "docker image inspect localhost:5001/$1 --format '{{index .RepoDigests 0}}'" | sed 's/.*@//'; }
PD=$(digest "portal-freshstart:$PTAG"); AD=$(digest "apache-web:$ATAG")

$HELM dependency update "$CHARTS/egeria-platform" >/dev/null; $HELM dependency update "$CHARTS/egeria-portal" >/dev/null; $HELM dependency update "$CHARTS/egeria-stack" >/dev/null
$HELM upgrade --install "$REL" "$CHARTS/egeria-stack" -n "$NS" -f "$CHARTS/egeria-stack/values-production.yaml" -f "$CHARTS/egeria-stack/values-freshstart.yaml" \
  --set core.postgres.host=postgres --set core.kafka.bootstrapServers="kafka.$NS.svc.cluster.local:9192" \
  --set core.secrets.existingSecret=prod-secrets --set core.tls.existingSecret=prod-tls --set core.canary.existingSecret=prod-canary \
  --set core.persistence.storageClassName=standard --set core.resources.limits.cpu=4 \
  --set portal.secrets.existingSecret=prod-portal --set portal.tls.caSecret=prod-ca --set portal.canary.existingSecret=prod-canary \
  --set portal.platform.userDirectorySecret=prod-secrets \
  --set portal.persistence.storageClassName=standard \
  --set portal.images.portal.repository="$REG/portal-freshstart" --set portal.images.portal.tag="$PTAG" --set portal.images.portal.digest="$PD" \
  --set portal.images.apache.repository="$REG/apache-web" --set portal.images.apache.tag="$ATAG" --set portal.images.apache.digest="$AD" \
  | sed -n '/^NOTES/,$p'
echo "installed $REL in $NS; waiting for the platform (first start loads content packs for several minutes)"
for i in $(seq 1 90); do
  r=$(kubectl -n "$NS" get pod "$REL-platform-0" -o jsonpath='{.status.containerStatuses[?(@.name=="platform")].ready}' 2>/dev/null || true)
  [ "$r" = true ] && break; sleep 10
done
n=0; for i in $(seq 1 60); do n=$(kubectl -n "$NS" logs "$REL-platform-0" -c platform 2>/dev/null | grep -c SERVER-OPS-0004 || true); [ "$n" -ge 5 ] && break; sleep 10; done
echo "servers started: $n/5"
kubectl -n "$NS" get pods
$HELM test "$REL" -n "$NS" --logs 2>&1 | grep -E "^ok|^FAIL|^PASS|Phase|TEST SUITE|Error"
