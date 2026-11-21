#!/usr/bin/env bash
# TR-112a proof: the Portal and Apache images run as their default user and as an arbitrary UID with
# GID 0, with the content mounts read-only; the health route answers; every written path is writable;
# and `docker compose config` for both compose files is identical before and after the branch.
# usage: proof112a.sh [build]      (run through: sg docker -c '...')   env: BASE=<ref before the branch>
# Builds are tagged <env>-<egeria release>-<short sha>. Needs docker; nothing leaves this machine.
set -euo pipefail
UP=$(cd "$(dirname "$(readlink -f "$0")")/../.." && pwd)
CC=$UP/compose-configs
REL=${EGERIA_RELEASE:-6.3}
SHA=$(git -C "$UP" rev-parse --short HEAD)
TAG=${TAG_SUFFIX:-$REL-$SHA}
BASE=${BASE:-234006cc}
ARB=1000680000
fail=0
ok()  { echo "PASS: $*"; }
bad() { echo "FAIL: $*"; fail=1; }

if [ "${1:-}" = build ]; then
  for e in quickstart freshstart; do
    docker build -q -f "$CC/egeria-$e/PyegeriaWebHandler/Dockerfile-portal-image" -t "portal-$e:$e-$TAG" "$CC/egeria-$e/PyegeriaWebHandler" >/dev/null
  done
  docker build -q -f "$CC/egeria-quickstart/Dockerfile-apache-web-nonroot" -t "apache-web:$TAG" "$CC/egeria-quickstart" >/dev/null
fi

M=$(mktemp -d); trap 'rm -rf "$M"; docker rm -f tr112a-c >/dev/null 2>&1 || true' EXIT
# the content compose mounts, as empty read-only stand-ins (the chart mounts the real content)
for d in config work coco-workbooks design-patterns templates coco-dags loading-bay landing-area coco-data-lake distribution-hub treasury-dts-history; do mkdir -p "$M/$d"; done
chmod -R a+rX "$M"

PY='import http.client as h,sys
u=sys.argv[1].split("//")[1].split("/")[0].split(":")
c=h.HTTPConnection(u[0],int(u[1]),timeout=5); c.request("GET","/"); print(c.getresponse().status)'   # no redirect following
# listening TCP ports of the container's processes (hex local port from /proc/net/tcp*)
LISTEN='import sys
for f in ("/proc/net/tcp","/proc/net/tcp6"):
    for l in open(f).read().splitlines()[1:]:
        c=l.split()
        if c[3]=="0A": print(int(c[1].rsplit(":",1)[1],16))'
run_check() {   # image label user... : start, wait for health, write checks
  local img=$1 label=$2 kind=$3; shift 3
  docker rm -f tr112a-c >/dev/null 2>&1 || true
  if [ "$kind" = portal ]; then
    docker run -d --name tr112a-c "$@" -e EGERIA_USER_PASSWORD=test -e JWT_SECRET=test -e DEMO_MODE=false \
      -e EGERIA_PLATFORM_URL=https://127.0.0.1:1 -e EGERIA_VIEW_SERVER=none \
      -v "$M/config":/config:ro -v "$M/work":/work:ro -v "$M/coco-workbooks":/coco-workbooks:ro -v "$M/design-patterns":/design-patterns:ro \
      -v "$M/templates":/app/templates:ro -v "$M/coco-dags":/app/coco-dags:ro \
      -v "$M/loading-bay":/deployments/loading-bay:ro -v "$M/landing-area":/deployments/landing-area:ro \
      -v "$M/coco-data-lake":/deployments/coco-data-lake:ro -v "$M/distribution-hub":/deployments/distribution-hub:ro \
      -v "$M/treasury-dts-history":/deployments/treasury-dts-history:ro "$img" >/dev/null
    local url=http://127.0.0.1:8000/ writes="/home/portal/.pyegeria /app/logs /app/demo-data /app/workbench-access /app/dr-egeria /app /tmp"
  else
    docker run -d --name tr112a-c "$@" "$img" >/dev/null
    local url=http://127.0.0.1:8085/ writes="/usr/local/apache2/logs /tmp"
  fi
  local code=
  for _ in $(seq 1 60); do
    code=$(docker exec tr112a-c python3 -c "$PY" "$url" 2>/dev/null || true)
    [ -n "$code" ] && break
    docker ps -q -f name=tr112a-c | grep -q . || break
    sleep 2
  done
  if [ "$kind" = portal ]; then [ "$code" = 200 ] && ok "$label: GET / answers 200" || bad "$label: GET / gave '${code:-nothing}'"
  else [ -n "$code" ] && ok "$label: Apache answers on 8085 ($code)" || bad "$label: no answer on 8085"; fi
  for p in $(docker exec tr112a-c python3 -c "$LISTEN" | sort -un); do
    [ "$p" -ge 1024 ] && ok "$label: listens on $p" || bad "$label: listens on privileged port $p"
  done
  for p in $writes; do
    docker exec tr112a-c sh -c "f=\$(mktemp -p $p) && rm -f \$f" >/dev/null 2>&1 && ok "$label: $p writable" || bad "$label: $p not writable"
  done
  if [ "$kind" = portal ]; then
    # Dr.Egeria inbox and outbox (EGERIA_ROOT_PATH, EGERIA_INBOX_PATH, EGERIA_OUTBOX_PATH from the image)
    docker exec tr112a-c sh -c 'mkdir -p "$EGERIA_ROOT_PATH/$EGERIA_INBOX_PATH" "$EGERIA_ROOT_PATH/$EGERIA_OUTBOX_PATH" && echo x > "$EGERIA_ROOT_PATH/$EGERIA_INBOX_PATH/probe.md" && echo x > "$EGERIA_ROOT_PATH/$EGERIA_OUTBOX_PATH/probe.md"' >/dev/null 2>&1 \
      && ok "$label: Dr.Egeria inbox and outbox writable" || bad "$label: Dr.Egeria inbox or outbox not writable"
    docker exec tr112a-c sh -c "grep -q '^Umask:.0002' /proc/1/status" >/dev/null 2>&1 \
      && ok "$label: umask is 002 (files the app creates are group-writable)" || bad "$label: umask is not 002"
    # _rebuild_catalog overwrites the tracked catalog in place
    docker exec tr112a-c sh -c 'cp egeria_request_body_catalog.json /tmp/cat.json && cat /tmp/cat.json > egeria_request_body_catalog.json' >/dev/null 2>&1 \
      && ok "$label: request body catalog overwritable" || bad "$label: request body catalog not overwritable"
  fi
  docker exec tr112a-c sh -c "echo x > /config/w" >/dev/null 2>&1 && [ "$kind" = portal ] && bad "$label: read-only /config was writable" || true
  [ "$kind" = portal ] && { docker exec tr112a-c sh -c 'test -f /home/portal/.pyegeria/bootstrap.log' && ok "$label: state written under HOME/.pyegeria" || echo "note: no bootstrap.log yet"; }
  docker rm -f tr112a-c >/dev/null
}

for e in quickstart freshstart; do
  run_check "portal-$e:$e-$TAG" "portal-$e default user" portal
  run_check "portal-$e:$e-$TAG" "portal-$e --user $ARB:0" portal --user $ARB:0
  if [ "$e" = quickstart ]; then   # one environment-neutral Apache image
    run_check "apache-web:$TAG" "apache-web default user" apache
    run_check "apache-web:$TAG" "apache-web --user $ARB:0" apache --user $ARB:0
  fi
  u=$(docker run --rm --entrypoint id "portal-$e:$e-$TAG" -u); [ "$u" != 0 ] && ok "portal-$e default user is not root (uid $u)" || bad "portal-$e runs as root"
  g=$(docker run --rm --entrypoint id "portal-$e:$e-$TAG" -g); [ "$g" = 0 ] && ok "portal-$e default group is 0" || bad "portal-$e group is $g"
done

# nothing from a developer machine lands in the image: build from a copy of the context that has junk in it
for e in quickstart freshstart; do
  X=$M/ctx-$e; cp -r "$CC/egeria-$e/PyegeriaWebHandler" "$X"
  mkdir -p "$X/logs" "$X/tests/browser/.venv" "$X/.hypothesis"; : > "$X/logs/x.log"; : > "$X/debug_log.log"; : > "$X/tests/browser/.venv/x"; : > "$X/.hypothesis/x"; : > "$X/junit.xml"; : > "$X/stray.db"
  docker build -q -f "$X/Dockerfile-portal-image" -t "portal-$e:ctxcheck" "$X" >/dev/null
  left=$(docker run --rm --entrypoint sh "portal-$e:ctxcheck" -c 'cd /app; ls -d logs/x.log debug_log.log tests/browser/.venv .hypothesis junit.xml stray.db .git 2>/dev/null; true')
  [ -z "$left" ] && ok "portal-$e: no logs, debug log, .venv, .hypothesis, result XML or .db baked in" || bad "portal-$e: baked in: $left"
  docker rmi -f "portal-$e:ctxcheck" >/dev/null
done

# every EXPOSEd port of the Portal images is >= 1024
# (the Apache image also inherits EXPOSE 80 from the httpd base image: metadata only, it never listens there; run_check proves that)
for i in "portal-quickstart:quickstart-$TAG" "portal-freshstart:freshstart-$TAG"; do
  for p in $(docker image inspect "$i" --format '{{range $k,$v := .Config.ExposedPorts}}{{$k}} {{end}}' | sed "s#/tcp##g"); do
    [ "$p" -ge 1024 ] && ok "$i exposes $p" || bad "$i exposes privileged port $p"
  done
done

# compose unchanged: the resolved config for both compose files, before (BASE) and after (working tree)
cfg() {   # root file -> normalised config
  (cd "$1/compose-configs/$2" && JWT_SECRET=x QUICKSTART_PERSONA_PASSWORD=x EGERIA_ADMIN_CALLER_PASSWORD=x HOST_FQDN=h \
     docker compose -f "$3" config 2>&1) | sed "s#$1#ROOT#g"
}
git -C "$UP" archive "$BASE" compose-configs | tar -x -C "$M" && mkdir -p "$M/after" "$M/before" && mv "$M/compose-configs" "$M/before/"
mkdir -p "$M/after" && tar -C "$UP" --exclude=runtime-volumes -cf - compose-configs | tar -x -C "$M/after"
for pair in "egeria-quickstart egeria-quickstart.yaml" "egeria-freshstart egeria-freshstart.yaml"; do
  set -- $pair
  b=$(cfg "$M/before" "$1" "$2"); a=$(cfg "$M/after" "$1" "$2")
  [ -n "$a" ] && [ "$a" = "$b" ] && ok "docker compose config for $2 is identical to $BASE" || bad "docker compose config for $2 differs from $BASE"
done
[ "$fail" = 0 ] && echo "ALL PASS" || { echo "FAILURES"; exit 1; }
