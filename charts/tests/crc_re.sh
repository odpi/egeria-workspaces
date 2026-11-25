#!/usr/bin/env bash
# Production-posture trellis-re (Resource Explorer) on OpenShift Local (crc), under restricted-v2 with global.openshift=true: a production-style
# quickstart platform with its own SAN keystore, the test Postgres (pgvector) and Kafka in <ns>-infra (anyuid, test only), and trellis-re with
# image by digest from the internal registry, existing Secrets, tls.verify against the platform CA, NetworkPolicies and a separate owner role.
# usage: crc_re.sh [namespace] [release]     env: RE_LOCAL_IMAGE (default localhost:5001/trellis/resource-explorer:tr115-efd55108)
# Memory: the VM holds one platform at a time: scale other platform releases to zero first (this script does not touch them).
# Secret values and the push token are generated here or read from tracked demo files and are never printed.
set -euo pipefail
NS=${1:-egeria-re}; REL=${2:-re}; INFRA=${NS}-infra
HERE=$(cd "$(dirname "$(readlink -f "$0")")" && pwd); CHARTS=$(dirname "$HERE")
LOCAL=${RE_LOCAL_IMAGE:-localhost:5001/trellis/resource-explorer:tr115-efd55108}; NAME=resource-explorer; TAG=${LOCAL##*:}
export KUBECONFIG=${KUBECONFIG:-$HOME/.crc/machines/crc/kubeconfig}
OC=${OC:-$HOME/.crc/bin/oc/oc}
SSH="ssh -o BatchMode=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -i $HOME/.crc/machines/crc/id_ed25519 -p 2222 core@127.0.0.1"
ROUTE=$($OC -n openshift-image-registry get route default-route -o jsonpath='{.spec.host}')
INREG=image-registry.openshift-image-registry.svc:5000
SC=crc-csi-hostpath-provisioner
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT; umask 077
PLAT=qs

$OC get project "$NS" >/dev/null 2>&1 || $OC new-project "$NS" >/dev/null
$OC get project "$INFRA" >/dev/null 2>&1 || $OC new-project "$INFRA" >/dev/null
$OC adm policy add-scc-to-user anyuid -z default -n "$INFRA" >/dev/null      # test Postgres and Kafka only
$OC -n "$NS" get sa pusher >/dev/null 2>&1 || $OC -n "$NS" create sa pusher >/dev/null
$OC -n "$NS" policy add-role-to-user system:image-builder -z pusher >/dev/null

# the RE image: into the VM's podman (about 5 GB), then the internal registry; the digest is what the registry reports
$OC -n "$NS" create token pusher --duration=2h | $SSH "sudo podman login --tls-verify=false -u pusher --password-stdin $ROUTE" >/dev/null
docker save "$LOCAL" | $SSH 'sudo podman load' >/dev/null
DIG=$($SSH "f=\$(sudo mktemp) && sudo podman tag $LOCAL $ROUTE/$NS/$NAME:$TAG && sudo podman push --tls-verify=false --digestfile \$f $ROUTE/$NS/$NAME:$TAG >/dev/null 2>&1 && sudo cat \$f; sudo rm -f \$f")
[ -n "$DIG" ] || { echo "image push failed" >&2; exit 1; }
echo "image $INREG/$NS/$NAME:$TAG@${DIG:0:19}..."

bash "$HERE/kind_infra.sh" "$INFRA"       # kubectl is oc here: same KUBECONFIG

# a production-style quickstart platform (own SAN keystore: re-runs keep the Secrets of the first run)
CHART=$CHARTS/egeria-platform; SECDIR=$CHART/files/quickstart/secrets
if ! $OC -n "$NS" get secret prod-tls >/dev/null 2>&1; then
  bash "$HERE/make_san_keystore.sh" "$W/tls" "$NS" "$PLAT-platform" >/dev/null
  $OC -n "$NS" create secret generic prod-secrets --from-file="$SECDIR" --dry-run=client -o yaml | $OC apply -f - >/dev/null
  $OC -n "$NS" create secret generic prod-tls --from-file="$W/tls/keystore.p12" --from-file="$W/tls/truststore.p12" --from-file="$W/tls/ca.crt" \
    --from-file=keystore-password="$W/tls/keystore-password" --from-file=truststore-password="$W/tls/truststore-password" \
    --from-file=key-alias="$W/tls/key-alias" --dry-run=client -o yaml | $OC apply -f - >/dev/null
  $OC -n "$NS" create secret generic re-ca --from-file=ca.crt="$W/tls/ca.crt" --dry-run=client -o yaml | $OC apply -f - >/dev/null
  CPW=$(python3 -I -c "import yaml,sys;print(yaml.safe_load(open(sys.argv[1]))['secretsCollections']['cocoUserDirectory']['users']['omagspcatnpa']['secrets']['clearPassword'], end='')" "$SECDIR/coco-user-directory.omsecrets")
  printf %s "$CPW" > "$W/egeria-pw"; unset CPW
  $OC -n "$NS" create secret generic prod-canary --from-literal=userId=omagspcatnpa --from-file=password="$W/egeria-pw" --dry-run=client -o yaml | $OC apply -f - >/dev/null
  $OC -n "$NS" create secret generic re-egeria --from-file=password="$W/egeria-pw" --dry-run=client -o yaml | $OC apply -f - >/dev/null
  openssl rand -hex 24 | tr -d '\n' > "$W/jwt"; openssl rand -hex 16 | tr -d '\n' > "$W/ckey"
  $OC -n "$NS" create secret generic re-secrets --from-file=jwt-secret="$W/jwt" --from-file=db-credential-key="$W/ckey" --dry-run=client -o yaml | $OC apply -f - >/dev/null
fi
helm dependency update "$CHART" >/dev/null
helm upgrade --install "$PLAT" "$CHART" -n "$NS" -f "$CHART/values-production.yaml" --set environment=quickstart --set global.openshift=true \
  --set postgres.host="postgres.$INFRA.svc.cluster.local" --set kafka.bootstrapServers="kafka.$INFRA.svc.cluster.local:9192" \
  --set secrets.existingSecret=prod-secrets --set tls.existingSecret=prod-tls --set canary.existingSecret=prod-canary \
  --set persistence.storageClassName=$SC --set resources.limits.cpu=4 >/dev/null
echo "platform installed; waiting for it (content packs load for several minutes)"
for i in $(seq 1 120); do
  r=$($OC -n "$NS" get pod "$PLAT-platform-0" -o jsonpath='{.status.containerStatuses[?(@.name=="platform")].ready}' 2>/dev/null || true)
  [ "$r" = true ] && break; sleep 10
done
n=0; for i in $(seq 1 60); do n=$($OC -n "$NS" logs "$PLAT-platform-0" -c platform 2>/dev/null | grep -c SERVER-OPS-0004 || true); [ "$n" -ge 5 ] && break; sleep 10; done
echo "servers started: $n/5"

# the RE database: an owner role for the schema Job, a runtime role for the pods (default privileges only)
openssl rand -hex 16 | tr -d '\n' > "$W/owner-pw"; openssl rand -hex 16 | tr -d '\n' > "$W/rt-pw"
OPW=$(cat "$W/owner-pw"); RPW=$(cat "$W/rt-pw")
$OC -n "$INFRA" exec -i deploy/postgres -- psql -p 5442 -U postgres -v ON_ERROR_STOP=1 -q >/dev/null <<SQL
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
$OC -n "$NS" create secret generic re-owner-db --from-file=password="$W/owner-pw" --dry-run=client -o yaml | $OC apply -f - >/dev/null
$OC -n "$NS" create secret generic re-db --from-file=password="$W/rt-pw" --dry-run=client -o yaml | $OC apply -f - >/dev/null

helm dependency update "$CHARTS/trellis-re" >/dev/null
T0=$(date +%s)
helm upgrade --install "$REL" "$CHARTS/trellis-re" -n "$NS" -f "$CHARTS/trellis-re/values-production.yaml" --set global.openshift=true \
  --set image.repository="$INREG/$NS/$NAME" --set image.tag="$TAG" --set image.digest="$DIG" \
  --set database.host="postgres.$INFRA.svc.cluster.local" --set database.port=5442 --set database.name=re_proof --set database.user=re_rt \
  --set database.existingSecret=re-db --set database.owner.user=re_owner --set database.owner.existingSecret=re-owner-db \
  --set egeria.platformUrl=https://$PLAT-platform:9443 --set egeria.daemon.userId=omagspcatnpa --set egeria.daemon.existingSecret=re-egeria \
  --set secrets.existingSecret=re-secrets --set tls.caSecret=re-ca \
  --set persistence.storageClassName=$SC --set 'persistence.accessModes={ReadWriteOnce}' --wait --timeout 15m | sed -n '/^NOTES/,$p'
echo "installed $REL in $NS after $(( $(date +%s) - T0 ))s"
for p in $($OC -n "$NS" get pods -o name | grep -E "re-re-(web|worker)" | sed 's#pod/##'); do
  c=$($OC -n "$NS" get pod "$p" -o jsonpath='{.spec.containers[0].name}')
  echo "$p: scc=$($OC -n "$NS" get pod "$p" -o jsonpath='{.metadata.annotations.openshift\.io/scc}') $($OC -n "$NS" exec "$p" -c "$c" -- id | cut -c1-70)"
done
helm test "$REL" -n "$NS" --logs 2>&1 | grep -E "^ok|^FAIL|^PASS|Phase|TEST SUITE|Error"
