#!/usr/bin/env bash
# Install egeria-platform on a kind cluster with its own test Postgres and Kafka, then time the start.
# usage: kind_install.sh <quickstart|freshstart> <namespace> [release]
#   MODE=demo (default): values-demo.yaml. MODE=production: values-production.yaml with the Secrets it requires
#   (the keystore is made by make_san_keystore.sh: our own, with SANs, so TLS checks are real; the secrets are the tracked demo files).
#   HELM=helm3 to use Helm 3. BUNDLED=1: use the chart's demo Postgres and Kafka instead of this script's.
#   needs: kind cluster up (kubectl context kind-<cluster>), the images loaded (see kind_setup.sh), helm.
# The test Postgres and Kafka are NOT part of the chart: they exist only for this test, one pair per
# namespace (design note 16: one each is the default). Nothing here touches laz or pop-os.
set -euo pipefail
kubectl config current-context | grep -q "^kind-" || { echo "not a kind context" >&2; exit 2; }
ENV=${1:?environment}; NS=${2:?namespace}; REL=${3:-$ENV}
HELM=${HELM:-helm}
MODE=${MODE:-demo}
BUNDLED=${BUNDLED:-0}
REPO=$(cd "$(dirname "$(readlink -f "$0")")/../.." && pwd)
CHART=$REPO/charts/egeria-platform
SHARED=$REPO/compose-configs/shared-infra
PGIMG=${PGIMG:-pgvector/pgvector:pg17}
KFIMG=${KFIMG:-cleanstart/kafka@sha256:3bfad519feac67e6bd1ae2b18b3e4770cdf2fedf53ecff7b38a520a7c5d77564}
case $ENV in quickstart) PORT=9443; PFX=qs ;; freshstart) PORT=8443; PFX=fs ;; *) echo "environment?"; exit 2 ;; esac

kubectl get ns "$NS" >/dev/null 2>&1 || kubectl create ns "$NS" >/dev/null
if [ "$BUNDLED" != 1 ]; then
  PGIMG=$PGIMG KFIMG=$KFIMG bash "$(dirname "$(readlink -f "$0")")/kind_infra.sh" "$NS"
fi

T0=$(date +%s)
ARGS=(--set environment="$ENV")
if [ "$BUNDLED" = 1 ]; then
  ARGS+=(-f "$CHART/values-demo-infra.yaml")
else
  ARGS+=(--set postgres.host=postgres --set kafka.bootstrapServers=kafka.$NS.svc.cluster.local:9192)
fi
if [ "$MODE" = production ]; then
  W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
  # secrets the production posture requires (values are never printed)
  kubectl -n "$NS" create secret generic prod-secrets --from-file="$CHART/files/$ENV/secrets" --dry-run=client -o yaml | kubectl apply -f - >/dev/null
  # a keystore of our own (random passwords, SANs for this release's Service names): the production posture refuses the public demo one
  bash "$(dirname "$(readlink -f "$0")")/make_san_keystore.sh" "$W/tls" "$NS" "$REL-platform" >/dev/null
  kubectl -n "$NS" create secret generic prod-tls --from-file="$W/tls/keystore.p12" --from-file="$W/tls/truststore.p12" --from-file="$W/tls/ca.crt" \
    --from-file=keystore-password="$W/tls/keystore-password" --from-file=truststore-password="$W/tls/truststore-password" \
    --from-file=key-alias="$W/tls/key-alias" --dry-run=client -o yaml | kubectl apply -f - >/dev/null
  DIRF=$(python3 -c "import sys;print({'quickstart':'coco-user-directory','freshstart':'egeria-user-directory'}['$ENV'])")
  COL=$(python3 -c "print({'quickstart':'cocoUserDirectory','freshstart':'userDirectory'}['$ENV'])")
  CPW=$(python3 -I -c "import yaml,sys;print(yaml.safe_load(open(sys.argv[1]))['secretsCollections'][sys.argv[2]]['users']['omagspcatnpa']['secrets']['clearPassword'])" "$CHART/files/$ENV/secrets/$DIRF.omsecrets" "$COL")
  kubectl -n "$NS" create secret generic prod-canary --from-literal=userId=omagspcatnpa --from-literal=password="$CPW" --dry-run=client -o yaml | kubectl apply -f - >/dev/null
  unset CPW
  $HELM upgrade --install "$REL" "$CHART" -n "$NS" -f "$CHART/values-production.yaml" "${ARGS[@]}" \
    --set secrets.existingSecret=prod-secrets --set tls.existingSecret=prod-tls --set canary.existingSecret=prod-canary \
    --set persistence.storageClassName="${STORAGE_CLASS:-standard}" --set resources.limits.cpu=4 ${EXTRA_HELM_ARGS:-} >/dev/null
else
  $HELM upgrade --install "$REL" "$CHART" -n "$NS" -f "$CHART/values-demo.yaml" "${ARGS[@]}" ${EXTRA_HELM_ARGS:-} >/dev/null
fi
POD=$REL-platform-0
echo "[$ENV/$NS] installed release $REL at $(date -u +%T); waiting for $POD"
for i in $(seq 1 120); do
  ready=$(kubectl -n "$NS" get pod "$POD" -o jsonpath='{.status.containerStatuses[?(@.name=="platform")].ready}' 2>/dev/null || true)
  [ "$ready" = true ] && { echo "[$ENV/$NS] READY (startup+readiness probes passed) after $(( $(date +%s) - T0 ))s"; break; }
  phase=$(kubectl -n "$NS" get pod "$POD" -o jsonpath='{.status.phase}' 2>/dev/null || true)
  [ "$phase" = Failed ] && { echo "[$ENV/$NS] POD FAILED"; break; }
  sleep 5
done
n=0
for i in $(seq 1 60); do
  n=$(kubectl -n "$NS" logs "$POD" -c platform 2>/dev/null | grep -c SERVER-OPS-0004 || true)
  [ "$n" -ge 5 ] && break; sleep 5
done
echo "[$ENV/$NS] servers completed start-up: $n/5 after $(( $(date +%s) - T0 ))s"
kubectl -n "$NS" logs "$POD" -c platform 2>/dev/null | grep SERVER-OPS-0004 | sed -E "s/^.* GMT [0-9]+ ([a-z-]+) .*/[$ENV\/$NS] started: \1/"
echo "[$ENV/$NS] probe (inside pod): $(kubectl -n "$NS" exec "$POD" -c platform -- sh -c "curl -k -s -o /dev/null -w '%{http_code}' https://localhost:$PORT/open-metadata/platform-services/server-platform/origin")"
echo "[$ENV/$NS] uid: $(kubectl -n "$NS" exec "$POD" -c platform -- id)"
echo "[$ENV/$NS] pod restarts: $(kubectl -n "$NS" get pod "$POD" -o jsonpath='{.status.containerStatuses[0].restartCount}')"
[ "$n" -ge 5 ]
