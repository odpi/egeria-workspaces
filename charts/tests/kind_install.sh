#!/usr/bin/env bash
# Install egeria-platform on a kind cluster with its own test Postgres and Kafka, then time the start.
# usage: kind_install.sh <quickstart|freshstart> <namespace> [release]
#   MODE=demo (default): values-demo.yaml. MODE=production: values-production.yaml with the Secrets it requires
#   (made from the tracked demo files and the image's own keystore, so the mechanism is exercised, not real security).
#   HELM=helm3 to use Helm 3. BUNDLED=1: use the chart's demo Postgres and Kafka instead of this script's.
#   needs: kind cluster up (kubectl context kind-<cluster>), the images loaded (see kind_setup.sh), helm.
# The test Postgres and Kafka are NOT part of the chart: they exist only for this test, one pair per
# namespace (design note 16: one each is the default). Nothing here touches laz or pop-os.
set -euo pipefail
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
kubectl -n "$NS" create configmap pg-init \
  --from-file=init_egeria.sql="$SHARED/docker-entrypoint-initdb.d/init_egeria.sql" \
  --from-file=init_egeria_ods.sql="$SHARED/docker-entrypoint-initdb.d/init_egeria_ods.sql" \
  --dry-run=client -o yaml | kubectl apply -f - >/dev/null
kubectl -n "$NS" create configmap kafka-entrypoint \
  --from-file=egeria-kafka-entrypoint.sh="$SHARED/kafka-entrypoint.sh" --dry-run=client -o yaml | kubectl apply -f - >/dev/null

kubectl -n "$NS" apply -f - >/dev/null <<YAML
apiVersion: apps/v1
kind: Deployment
metadata: {name: postgres}
spec:
  replicas: 1
  selector: {matchLabels: {app: postgres}}
  template:
    metadata: {labels: {app: postgres}}
    spec:
      containers:
        - name: postgres
          image: $PGIMG
          imagePullPolicy: IfNotPresent
          args: ["-p", "5442"]
          env:
            - {name: POSTGRES_USER, value: postgres}
            - {name: POSTGRES_PASSWORD, value: egeria}
            - {name: PGDATA, value: /var/lib/postgresql/data/pgdata}
          ports: [{containerPort: 5442}]
          readinessProbe:
            exec: {command: [sh, -c, "pg_isready -U postgres -p 5442"]}
            periodSeconds: 5
          volumeMounts:
            - {name: data, mountPath: /var/lib/postgresql/data}
            - {name: init, mountPath: /docker-entrypoint-initdb.d}
      volumes:
        - {name: data, emptyDir: {}}
        - {name: init, configMap: {name: pg-init}}
---
apiVersion: v1
kind: Service
metadata: {name: postgres}
spec:
  selector: {app: postgres}
  ports: [{port: 5442, targetPort: 5442}]
---
apiVersion: apps/v1
kind: Deployment
metadata: {name: kafka}
spec:
  replicas: 1
  selector: {matchLabels: {app: kafka}}
  template:
    metadata: {labels: {app: kafka}}
    spec:
      containers:
        - name: kafka
          image: $KFIMG
          imagePullPolicy: IfNotPresent
          command: ["/usr/local/bin/egeria-kafka-entrypoint.sh"]
          env:
            - {name: KAFKA_CFG_NODE_ID, value: "1"}
            - {name: KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE, value: "true"}
            - {name: KAFKA_CFG_PROCESS_ROLES, value: "controller,broker"}
            - {name: KAFKA_CFG_CONTROLLER_LISTENER_NAMES, value: CONTROLLER}
            - {name: KAFKA_CFG_CONTROLLER_QUORUM_VOTERS, value: "1@127.0.0.1:9193"}
            - {name: KAFKA_CFG_LISTENERS, value: "PLAINTEXT://0.0.0.0:9192,CONTROLLER://0.0.0.0:9193"}
            - {name: KAFKA_CFG_ADVERTISED_LISTENERS, value: "PLAINTEXT://kafka.$NS.svc.cluster.local:9192,CONTROLLER://127.0.0.1:9193"}
            - {name: KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP, value: "CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT"}
            - {name: KAFKA_KRAFT_CLUSTER_ID, value: "42"}
            - {name: KAFKA_CFG_LOG_DIRS, value: /tmp/kraft-logs}
          ports: [{containerPort: 9192}]
          readinessProbe:
            tcpSocket: {port: 9192}
            periodSeconds: 5
          volumeMounts:
            - {name: entry, mountPath: /usr/local/bin/egeria-kafka-entrypoint.sh, subPath: egeria-kafka-entrypoint.sh}
      volumes:
        - name: entry
          configMap: {name: kafka-entrypoint, defaultMode: 0755}
---
apiVersion: v1
kind: Service
metadata: {name: kafka}
spec:
  selector: {app: kafka}
  ports: [{port: 9192, targetPort: 9192}]
YAML
kubectl -n "$NS" rollout status deploy/postgres --timeout=300s
kubectl -n "$NS" rollout status deploy/kafka --timeout=300s
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
  SRC=${KEYSTORE_POD:-}   # a running platform pod to take the image's keystores from (kubectl cp)
  [ -n "$SRC" ] || { echo "MODE=production needs KEYSTORE_POD=<namespace>/<pod> (a running platform pod)"; exit 2; }
  kubectl -n "${SRC%%/*}" cp -c platform "${SRC##*/}:/deployments/keystore.p12" "$W/keystore.p12"
  kubectl -n "${SRC%%/*}" cp -c platform "${SRC##*/}:/deployments/truststore.p12" "$W/truststore.p12"
  P=$CHART/files/$ENV/application.properties
  kubectl -n "$NS" create secret generic prod-tls --from-file="$W/keystore.p12" --from-file="$W/truststore.p12" \
    --from-literal=keystore-password="$(grep '^server.ssl.key-store-password=' "$P" | cut -d= -f2-)" \
    --from-literal=truststore-password="$(grep '^server.ssl.trust-store-password=' "$P" | cut -d= -f2-)" \
    --from-literal=key-alias="$(grep '^server.ssl.keyAlias=' "$P" | cut -d= -f2-)" --dry-run=client -o yaml | kubectl apply -f - >/dev/null
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
