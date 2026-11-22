#!/usr/bin/env bash
# Production-style install of egeria-stack (freshstart) on OpenShift Local (crc): the posture of kind_stack_prod.sh (external test Postgres
# and Kafka, our own SAN keystore with random passwords, existing Secrets, image digests, NetworkPolicies, tls.verify) but under restricted-v2
# with global.openshift=true. Images are pushed to the cluster's internal registry so the digests are real registry digests.
# usage: crc_stack_prod.sh [namespace] [release]      needs: crc running, docker (for the images), helm, openssl, ssh.
# Secret values and the push token are generated here or read from tracked demo files and are never printed.
# The test Postgres and Kafka run as fixed UIDs, so they live in a separate namespace (<ns>-infra) with the anyuid SCC.
set -euo pipefail
NS=${1:-egeria-prod}; REL=${2:-ps}; INFRA=${NS}-infra
HERE=$(cd "$(dirname "$(readlink -f "$0")")" && pwd); CHARTS=$(dirname "$HERE")
TAG=${IMAGE_TAG:-6.3-a79109b7}; PTAG=${PORTAL_TAG:-freshstart-$TAG}
export KUBECONFIG=${KUBECONFIG:-$HOME/.crc/machines/crc/kubeconfig}
OC=${OC:-$HOME/.crc/bin/oc/oc}
SSH="ssh -o BatchMode=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -i $HOME/.crc/machines/crc/id_ed25519 -p 2222 core@127.0.0.1"
ROUTE=$($OC -n openshift-image-registry get route default-route -o jsonpath='{.spec.host}')   # reachable from the VM, which pushes
INREG=image-registry.openshift-image-registry.svc:5000                                         # how the pods pull
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT; umask 077
alias kubectl="$OC"; shopt -s expand_aliases

$OC get project "$NS" >/dev/null 2>&1 || $OC new-project "$NS" >/dev/null
$OC get project "$INFRA" >/dev/null 2>&1 || $OC new-project "$INFRA" >/dev/null
$OC adm policy add-scc-to-user anyuid -z default -n "$INFRA" >/dev/null      # test Postgres and Kafka only
$OC -n "$NS" get sa pusher >/dev/null 2>&1 || $OC -n "$NS" create sa pusher >/dev/null
$OC -n "$NS" policy add-role-to-user system:image-builder -z pusher >/dev/null

# images: into the VM's podman, then to the internal registry; the digest is what the registry reports
$OC -n "$NS" create token pusher --duration=1h | $SSH "sudo podman login --tls-verify=false -u pusher --password-stdin $ROUTE" >/dev/null
digest() {   # <name:tag> -> sha256:...
  docker save "docker.io/library/$1" 2>/dev/null | $SSH 'sudo podman load' >/dev/null 2>&1 || docker save "$1" | $SSH 'sudo podman load' >/dev/null
  $SSH "sudo podman tag docker.io/library/$1 $ROUTE/$NS/$1 && sudo podman push --tls-verify=false --digestfile /tmp/dg $ROUTE/$NS/$1 >/dev/null 2>&1 && cat /tmp/dg"
}
PD=$(digest "portal-freshstart:$PTAG"); AD=$(digest "apache-web:$TAG")
[ -n "$PD" ] && [ -n "$AD" ] || { echo "image push failed" >&2; exit 1; }

bash "$HERE/kind_infra.sh" "$INFRA"
bash "$HERE/make_san_keystore.sh" "$W/tls" "$NS" "$REL-platform" >/dev/null
SECDIR=$CHARTS/egeria-platform/files/freshstart/secrets
$OC -n "$NS" create secret generic prod-secrets --from-file="$SECDIR" --dry-run=client -o yaml | $OC apply -f - >/dev/null
$OC -n "$NS" create secret generic prod-tls --from-file="$W/tls/keystore.p12" --from-file="$W/tls/truststore.p12" --from-file="$W/tls/ca.crt" \
  --from-file=keystore-password="$W/tls/keystore-password" --from-file=truststore-password="$W/tls/truststore-password" \
  --from-file=key-alias="$W/tls/key-alias" --dry-run=client -o yaml | $OC apply -f - >/dev/null
$OC -n "$NS" create secret generic prod-ca --from-file=ca.crt="$W/tls/ca.crt" --dry-run=client -o yaml | $OC apply -f - >/dev/null
python3 -I - "$SECDIR/egeria-user-directory.omsecrets" "$W" <<'PY'
import sys, yaml
u = yaml.safe_load(open(sys.argv[1]))["secretsCollections"]["userDirectory"]["users"]
w = sys.argv[2]
open(w + "/canary-user", "w").write("omagspcatnpa")
open(w + "/canary-pw", "w").write(u["omagspcatnpa"]["secrets"]["clearPassword"])
open(w + "/portal-egeria-pw", "w").write(u["bootstrap"]["secrets"]["clearPassword"])
PY
openssl rand -hex 24 > "$W/jwt"; openssl rand -hex 16 > "$W/mcp"
$OC -n "$NS" create secret generic prod-canary --from-file=userId="$W/canary-user" --from-file=password="$W/canary-pw" --dry-run=client -o yaml | $OC apply -f - >/dev/null
$OC -n "$NS" create secret generic prod-portal --from-file=jwt-secret="$W/jwt" --from-file=mcp-access-token="$W/mcp" \
  --from-file=egeria-user-password="$W/portal-egeria-pw" --dry-run=client -o yaml | $OC apply -f - >/dev/null

for c in egeria-platform egeria-portal egeria-stack; do helm dependency update "$CHARTS/$c" >/dev/null; done
helm upgrade --install "$REL" "$CHARTS/egeria-stack" -n "$NS" -f "$CHARTS/egeria-stack/values-production.yaml" -f "$CHARTS/egeria-stack/values-freshstart.yaml" \
  --set global.openshift=true \
  --set core.postgres.host="postgres.$INFRA.svc.cluster.local" --set core.kafka.bootstrapServers="kafka.$INFRA.svc.cluster.local:9192" \
  --set core.secrets.existingSecret=prod-secrets --set core.tls.existingSecret=prod-tls --set core.canary.existingSecret=prod-canary \
  --set core.persistence.storageClassName=crc-csi-hostpath-provisioner --set core.resources.limits.cpu=4 \
  --set portal.secrets.existingSecret=prod-portal --set portal.tls.caSecret=prod-ca --set portal.canary.existingSecret=prod-canary \
  --set portal.persistence.storageClassName=crc-csi-hostpath-provisioner \
  --set portal.images.portal.repository="$INREG/$NS/portal-freshstart" --set portal.images.portal.tag="$PTAG" --set portal.images.portal.digest="$PD" \
  --set portal.images.apache.repository="$INREG/$NS/apache-web" --set portal.images.apache.tag="$TAG" --set portal.images.apache.digest="$AD" \
  | sed -n '/^NOTES/,$p'
echo "installed $REL in $NS; waiting for the platform (first start loads content packs for several minutes)"
for i in $(seq 1 120); do
  r=$($OC -n "$NS" get pod "$REL-platform-0" -o jsonpath='{.status.containerStatuses[?(@.name=="platform")].ready}' 2>/dev/null || true)
  [ "$r" = true ] && break; sleep 10
done
n=0; for i in $(seq 1 60); do n=$($OC -n "$NS" logs "$REL-platform-0" -c platform 2>/dev/null | grep -c SERVER-OPS-0004 || true); [ "$n" -ge 5 ] && break; sleep 10; done
echo "servers started: $n/5"
for p in $($OC -n "$NS" get pods -o name | grep -v canary | sed 's#pod/##'); do
  c=$($OC -n "$NS" get pod "$p" -o jsonpath='{.spec.containers[0].name}')
  echo "$p: scc=$($OC -n "$NS" get pod "$p" -o jsonpath='{.metadata.annotations.openshift\.io/scc}') $($OC -n "$NS" exec "$p" -c "$c" -- id | cut -c1-70)"
done
helm test "$REL" -n "$NS" --logs 2>&1 | grep -E "^ok|^FAIL|^PASS|Phase|TEST SUITE|Error"
