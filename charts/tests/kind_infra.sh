#!/usr/bin/env bash
# A test Postgres and Kafka in one namespace of a kind cluster (the same ones kind_install.sh uses): NOT part of any chart.
# They exist so a chart can be installed with external infrastructure, the production-style way.
# usage: kind_infra.sh <namespace>        (Services: postgres:5442, kafka.<ns>.svc.cluster.local:9192)
set -euo pipefail
kubectl config current-context | grep -q "^kind-" || { echo "not a kind context" >&2; exit 2; }
NS=${1:?namespace}
REPO=$(cd "$(dirname "$(readlink -f "$0")")/../.." && pwd)
SHARED=$REPO/compose-configs/shared-infra
PGIMG=${PGIMG:-pgvector/pgvector:pg17}
KFIMG=${KFIMG:-cleanstart/kafka@sha256:3bfad519feac67e6bd1ae2b18b3e4770cdf2fedf53ecff7b38a520a7c5d77564}
kubectl get ns "$NS" >/dev/null 2>&1 || kubectl create ns "$NS" >/dev/null
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
