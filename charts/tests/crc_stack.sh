#!/usr/bin/env bash
# egeria-stack (freshstart, demo posture, global.openshift=true) on OpenShift Local (crc), then helm test.
# usage: crc_stack.sh [namespace] [release]        needs: crc running, docker (for the images), helm, ssh.
# env: ENVIRONMENT=freshstart|quickstart (default freshstart), DEMO_MODE=true (quickstart public-demo login: registration + a bootstrap admin whose
#      random password is kept in the Secret demo-admin of the namespace, read it with: oc -n <ns> get secret demo-admin -o jsonpath='{.data.password}' | base64 -d),
#      PORTAL_TAG (default <ENVIRONMENT>-<IMAGE_TAG>).
# Why the steps: the Portal and Apache images are not in a registry the crc VM can reach (it only reaches the host's non-loopback
# addresses), so they are loaded into the node over SSH (podman load). The test Postgres and Kafka run as fixed UIDs, so they live in a
# SEPARATE namespace with the anyuid SCC; the Egeria pods stay under restricted-v2 (arbitrary UID, GID 0), which is what is being proved.
# Sizing that worked: crc config set memory 20480, cpus 8, disk-size 70 (the 31 GB default disk hits kubelet disk-pressure).
set -euo pipefail
NS=${1:-egeria}; REL=${2:-st}; INFRA=${NS}-infra
HERE=$(cd "$(dirname "$(readlink -f "$0")")" && pwd); CHARTS=$(dirname "$HERE")
ENVR=${ENVIRONMENT:-freshstart}; DEMO=${DEMO_MODE:-false}
TAG=${IMAGE_TAG:-6.3-a79109b7}; PTAG=${PORTAL_TAG:-$ENVR-$TAG}
export KUBECONFIG=${KUBECONFIG:-$HOME/.crc/machines/crc/kubeconfig}
OC=${OC:-$HOME/.crc/bin/oc/oc}
SSH="ssh -o BatchMode=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -i $HOME/.crc/machines/crc/id_ed25519 -p 2222 core@127.0.0.1"

for i in "portal-$ENVR:$PTAG" "apache-web:$TAG"; do
  docker save "$i" | $SSH 'sudo podman load' | tail -1
done
$OC get project "$NS" >/dev/null 2>&1 || $OC new-project "$NS" >/dev/null
$OC get project "$INFRA" >/dev/null 2>&1 || $OC new-project "$INFRA" >/dev/null
$OC adm policy add-scc-to-user anyuid -z default -n "$INFRA"      # test Postgres and Kafka only
bash "$HERE/kind_infra.sh" "$INFRA"
DEMOARGS=()
if [ "$DEMO" = true ]; then   # the public-demo login: registration, and a bootstrap admin so the first sign-in is possible
  $OC -n "$NS" get secret demo-admin >/dev/null 2>&1 || $OC -n "$NS" create secret generic demo-admin --from-literal=password="$(openssl rand -hex 12)" >/dev/null
  DV=$(mktemp); trap 'rm -f "$DV"' EXIT
  cat > "$DV" <<YAML
portal:
  demoMode: true
  extraEnv:
    - {name: ADMIN_BOOTSTRAP_EMAIL, value: admin@example.test}
    - {name: ADMIN_BOOTSTRAP_PASSWORD, valueFrom: {secretKeyRef: {name: demo-admin, key: password}}}
YAML
  DEMOARGS=(-f "$DV")
fi
helm dependency update "$CHARTS/egeria-platform" >/dev/null; helm dependency update "$CHARTS/egeria-portal" >/dev/null; helm dependency update "$CHARTS/egeria-stack" >/dev/null
helm upgrade --install "$REL" "$CHARTS/egeria-stack" -n "$NS" -f "$CHARTS/egeria-stack/values-demo.yaml" -f "$CHARTS/egeria-stack/values-$ENVR.yaml" "${DEMOARGS[@]}" \
  --set global.openshift=true \
  --set core.postgres.host="postgres.$INFRA.svc.cluster.local" --set core.kafka.bootstrapServers="kafka.$INFRA.svc.cluster.local:9192" \
  --set portal.images.portal.repository=docker.io/library/portal-$ENVR --set portal.images.portal.tag="$PTAG" \
  --set portal.images.apache.repository=docker.io/library/apache-web --set portal.images.apache.tag="$TAG" | sed -n '/^NOTES/,$p'
echo "waiting for the platform (several minutes the first time)"
for i in $(seq 1 90); do
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
