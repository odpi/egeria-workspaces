#!/usr/bin/env bash
# Platform start-up proof: the upstream image under an arbitrary UID with GID 0, against a private
# Postgres and Kafka. Needs docker. Reads compose files, writes only to $W (a temp dir) and its own
# containers (tr112c-*) on a private network. Never touches laz or pop-os.
# TR-112c platform proof on cray. Private network, own Postgres/Kafka, never laz/pop-os.
# usage: proof112c.sh quickstart|freshstart   (run through: sg docker -c '...')
set -euo pipefail
ENV=${1:-quickstart}
SP=$(dirname "$(readlink -f "$0")")
UP=$(cd "$SP/../.." && pwd)
W=${TMPDIR:-/tmp}/tr112c-proof-$ENV
NET=tr112c-net
PREFIX=tr112c-$ENV
IMG=docker.io/odpi/egeria-platform:6.3@sha256:483726b69b9e789749995d114633eeeab0f70a9c26ec5e59ae0e3d300ebda29c
PGIMG=pgvector/pgvector:pg17
KFIMG=cleanstart/kafka@sha256:3bfad519feac67e6bd1ae2b18b3e4770cdf2fedf53ecff7b38a520a7c5d77564
UID_G=1000680000
case $ENV in
  quickstart) PROPS=$UP/runtime-volumes/quickstart-platform-data/quickstart.application.properties
              SECDIR=$UP/compose-configs/egeria-quickstart/secrets; DB=egeria; SERVERS=qs; PORT=9443; HPATH=users/garygeeke/server-platform/origin ;;
  freshstart) PROPS=$(ls $UP/runtime-volumes/freshstart-platform-data/*.application.properties | head -1)
              SECDIR=$UP/compose-configs/egeria-freshstart/secrets; DB=egeria_freshstart; SERVERS=fs; PORT=8443; HPATH=server-platform/origin ;;
esac
docker network inspect $NET >/dev/null 2>&1 || docker network create $NET >/dev/null
rm -rf "$W"; mkdir -p "$W"/{data,logs,secrets,initdb,kafka}
chmod 777 "$W"/{data,logs,secrets,kafka}
SRVDIR=$UP/compose-configs/egeria-quickstart/servers
mkdir -p "$W/data/servers"; for d in "$SRVDIR"/$SERVERS-*/; do cp -r "$d" "$W/data/servers/"; done; chmod -R a+rwX "$W/data"
cp "$SECDIR"/*.omsecrets "$W/secrets/"; chmod 666 "$W"/secrets/*
cp $UP/compose-configs/shared-infra/docker-entrypoint-initdb.d/{init_egeria.sql,init_egeria_ods.sql} "$W/initdb/"
# copy of the tracked properties, endpoints re-pointed at this private network only
sed -e 's#host.docker.internal:9194#tr112c-kafka:9192#g' \
    -e "s#host.docker.internal:5442#tr112c-pg:5442#g" "$PROPS" > "$W/application.properties"
chmod 644 "$W/application.properties"

if ! docker ps --format '{{.Names}}' | grep -qx tr112c-pg; then
  docker rm -f tr112c-pg >/dev/null 2>&1 || true
  docker run -d --name tr112c-pg --network $NET -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=egeria \
    -e PGDATA=/var/lib/postgresql/data/pgdata -v "$W/initdb":/docker-entrypoint-initdb.d:ro $PGIMG -p 5442 >/dev/null
fi
if ! docker ps --format '{{.Names}}' | grep -qx tr112c-kafka; then
  docker rm -f tr112c-kafka >/dev/null 2>&1 || true
  docker run -d --name tr112c-kafka --hostname tr112c-kafka --network $NET \
    -v $UP/compose-configs/shared-infra/kafka-entrypoint.sh:/usr/local/bin/egeria-kafka-entrypoint.sh:ro \
    --entrypoint /usr/local/bin/egeria-kafka-entrypoint.sh \
    -e KAFKA_CFG_NODE_ID=1 -e KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE=true -e KAFKA_CFG_PROCESS_ROLES=controller,broker \
    -e KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER -e KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=1@127.0.0.1:9193 \
    -e KAFKA_CFG_LISTENERS=PLAINTEXT://0.0.0.0:9192,CONTROLLER://0.0.0.0:9193 \
    -e KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://tr112c-kafka:9192,CONTROLLER://127.0.0.1:9193 \
    -e KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT \
    -e KAFKA_KRAFT_CLUSTER_ID=42 -e KAFKA_CFG_LOG_DIRS=/tmp/kraft-logs $KFIMG >/dev/null
fi
echo "waiting for postgres..."
for i in $(seq 1 60); do docker exec tr112c-pg pg_isready -U postgres -p 5442 >/dev/null 2>&1 && break; sleep 2; done
docker exec tr112c-pg psql -U postgres -p 5442 -Atc "select count(*) from pg_database where datname='$DB'" | sed 's/^/db exists (1=yes): /'

docker rm -f $PREFIX >/dev/null 2>&1 || true
T0=$(date +%s)
docker run -d --name $PREFIX --network $NET --user $UID_G:0 \
  -e server.port=$PORT -e KAFKA_BOOTSTRAP_SERVERS=tr112c-kafka:9192 -e HOST_FQDN=localhost \
  -e XTDB_ENABLE_BYTEUTILS_SHA1=True -e XTDB_DISABLE_LIBCRYPTO=True \
  -e startup.server.list="$(grep '^startup.server.list=' "$W/application.properties" | cut -d= -f2-)" \
  -e JAVA_OPTS_APPEND="-XX:MaxMetaspaceSize=512m -XX:-UseParallelGC -XX:+UseG1GC -XX:MaxRAMPercentage=60.0 -XX:MinHeapFreeRatio=20 -XX:MaxHeapFreeRatio=40 -XX:GCTimeRatio=19 -Xms2g" \
  --memory 6g --cpus 4 --add-host host.docker.internal:127.0.0.1 \
  -v "$W/data":/deployments/data -v "$W/logs":/deployments/logs -v "$W/secrets":/deployments/secrets:ro \
  -v "$W/application.properties":/deployments/application.properties:ro $IMG >/dev/null
echo "started $PREFIX; polling health (200 or 401 counts, as in compose)"
for i in $(seq 1 90); do
  code=$(docker exec $PREFIX curl -k -s -o /dev/null -w '%{http_code}' --max-time 10 \
    "https://localhost:$PORT/open-metadata/platform-services/$HPATH" 2>/dev/null || true)
  if [[ "$code" == 200 || "$code" == 401 ]]; then echo "HEALTHY http=$code after $(( $(date +%s) - T0 ))s"; break; fi
  if ! docker ps --format '{{.Names}}' | grep -qx $PREFIX; then echo "CONTAINER EXITED"; break; fi
  sleep 10
done
docker ps --filter name=$PREFIX --format '{{.Names}} {{.Status}}'
echo "waiting for all five $SERVERS-* servers (SERVER-OPS-0004)..."
for i in $(seq 1 90); do
  n=$(docker logs $PREFIX 2>&1 | grep -c "SERVER-OPS-0004" || true)
  [[ "$n" -ge 5 ]] && { echo "ALL 5 SERVERS STARTED after $(( $(date +%s) - T0 ))s"; break; }
  docker ps --format '{{.Names}}' | grep -qx $PREFIX || { echo "CONTAINER EXITED at $n/5"; break; }
  sleep 10
done
docker logs $PREFIX 2>&1 | grep -E "SERVER-OPS-0004" | sed -E 's/^.* GMT [0-9]+ ([a-z-]+) .*/started: \1/'
echo "permission errors: $(docker logs $PREFIX 2>&1 | grep -ciE "permission denied|EACCES|read-only file system|AccessDenied" || true)"
echo "error/exception lines: $(docker logs $PREFIX 2>&1 | grep -ciE "exception|error" || true)"
docker exec $PREFIX id
