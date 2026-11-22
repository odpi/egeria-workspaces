#!/usr/bin/env bash
# Resource Explorer (charts/trellis-re) on a kind cluster, against a quickstart Egeria platform and the test Postgres (pgvector) that
# kind_infra.sh makes, with the schema split of TR-115: the schema Job runs as an OWNER role, the pods as a RUNTIME role that holds only
# default privileges on the owner's objects (no DDL rights).
# usage: kind_re.sh <namespace> [release]        env: RE_IMAGE (default tr112-registry:5000/trellis/resource-explorer) RE_TAG (default tr115-efd55108)
#   MODE=demo (default) | production: production runs the platform with its own SAN keystore (kind_install.sh MODE=production) and the chart in the
#   production posture: image by digest, existing Secrets, tls.verify=true against the platform CA, NetworkPolicies, a separate owner role.
#   SKIP_PLATFORM=1: the platform, Postgres and Kafka are already installed.
#   A2A=1: also enable the chart's A2A role and check its public index, a signed-in call and a call for a context that does not exist.
#   PREFECT=1: also run a Prefect server (the RE image's own `prefect server start`, SQLite, test only) and enable the chart's Prefect worker.
# Secret values are generated here or read from tracked demo files and are never printed. Test infrastructure only, NOT part of any chart.
set -euo pipefail
NS=${1:?namespace}; REL=${2:-re}
HERE=$(cd "$(dirname "$(readlink -f "$0")")" && pwd); CHARTS=$(dirname "$HERE")
IMG=${RE_IMAGE:-tr112-registry:5000/trellis/resource-explorer}; TAG=${RE_TAG:-tr115-efd55108}
HELM=${HELM:-helm}; MODE=${MODE:-demo}
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT; umask 077

# 1. an Egeria platform (quickstart demo) plus the test Postgres and Kafka (SKIP_PLATFORM=1 when they are already installed)
[ "${SKIP_PLATFORM:-0}" = 1 ] || MODE=$MODE bash "$HERE/kind_install.sh" quickstart "$NS" qs

# 2. the RE database: an owner role (the schema Job) and a runtime role (the pods). The runtime role gets default privileges on what
#    the owner creates, and nothing else. The extension is the admin's (a managed Postgres often refuses it to the Job's role).
# no trailing newline: the files become Secret values
openssl rand -hex 16 | tr -d '\n' > "$W/owner-pw"; openssl rand -hex 16 | tr -d '\n' > "$W/rt-pw"
OPW=$(cat "$W/owner-pw"); RPW=$(cat "$W/rt-pw")
kubectl -n "$NS" exec -i deploy/postgres -- psql -p 5442 -U postgres -v ON_ERROR_STOP=1 -q >/dev/null <<SQL
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
kubectl -n "$NS" create secret generic re-owner-db --from-file=password="$W/owner-pw" --dry-run=client -o yaml | kubectl apply -f - >/dev/null
kubectl -n "$NS" create secret generic re-db --from-file=password="$W/rt-pw" --dry-run=client -o yaml | kubectl apply -f - >/dev/null
# RE's Egeria service account: the non-personal account from the tracked quickstart user directory
python3 -I - "$CHARTS/egeria-platform/files/quickstart/secrets/coco-user-directory.omsecrets" "$W" <<'PY'
import sys, yaml
u = yaml.safe_load(open(sys.argv[1]))["secretsCollections"]["cocoUserDirectory"]["users"]["omagspcatnpa"]["secrets"]["clearPassword"]
open(sys.argv[2] + "/egeria-pw", "w").write(u)
PY
kubectl -n "$NS" create secret generic re-egeria --from-file=password="$W/egeria-pw" --dry-run=client -o yaml | kubectl apply -f - >/dev/null

# 3. Resource Explorer
PFARGS=()
[ "${A2A:-0}" = 1 ] && PFARGS+=(--set a2a.enabled=true)
if [ "${PREFECT:-0}" = 1 ]; then
  # a test Prefect server from the RE image (its own client version): one pod, SQLite on an emptyDir. NOT part of the chart.
  kubectl -n "$NS" apply -f - >/dev/null <<YAML
apiVersion: apps/v1
kind: Deployment
metadata: {name: prefect-server}
spec:
  replicas: 1
  selector: {matchLabels: {app: prefect-server}}
  template:
    metadata: {labels: {app: prefect-server}}
    spec:
      containers:
        - name: server
          image: $IMG:$TAG
          command: ["prefect", "server", "start", "--host", "0.0.0.0", "--port", "4200"]
          env: [{name: PREFECT_HOME, value: /prefect}]
          ports: [{containerPort: 4200}]
          readinessProbe: {httpGet: {path: /api/health, port: 4200}, periodSeconds: 5, failureThreshold: 60}
          volumeMounts: [{name: prefect-home, mountPath: /prefect}]
      volumes: [{name: prefect-home, emptyDir: {}}]
---
apiVersion: v1
kind: Service
metadata: {name: prefect-server}
spec:
  selector: {app: prefect-server}
  ports: [{port: 4200, targetPort: 4200}]
YAML
  kubectl -n "$NS" rollout status deploy/prefect-server --timeout=300s
  PFARGS=(--set prefect.enabled=true --set prefect.apiUrl=http://prefect-server:4200/api)
fi
$HELM dependency update "$CHARTS/trellis-re" >/dev/null
T0=$(date +%s)
POSTURE=(-f "$CHARTS/trellis-re/values-demo.yaml")
if [ "$MODE" = production ]; then
  # secrets the production posture requires (values never printed): the shared JWT and credential key, and the platform's CA
  openssl rand -hex 24 | tr -d '\n' > "$W/jwt"; openssl rand -hex 16 | tr -d '\n' > "$W/ckey"
  kubectl -n "$NS" create secret generic re-secrets --from-file=jwt-secret="$W/jwt" --from-file=db-credential-key="$W/ckey" --dry-run=client -o yaml | kubectl apply -f - >/dev/null
  kubectl -n "$NS" get secret prod-tls -o jsonpath='{.data.ca\.crt}' | base64 -d > "$W/ca.crt"
  kubectl -n "$NS" create secret generic re-ca --from-file=ca.crt="$W/ca.crt" --dry-run=client -o yaml | kubectl apply -f - >/dev/null
  DIG=$(sg docker -c "docker image inspect localhost:5001/trellis/resource-explorer:$TAG --format '{{index .RepoDigests 0}}'" | sed 's/.*@//')
  POSTURE=(-f "$CHARTS/trellis-re/values-production.yaml" --set image.digest="$DIG" --set secrets.existingSecret=re-secrets --set tls.caSecret=re-ca)
  echo "production posture; image $IMG:$TAG@${DIG:0:19}..."
fi
$HELM upgrade --install "$REL" "$CHARTS/trellis-re" -n "$NS" "${POSTURE[@]}" \
  --set image.repository="$IMG" --set image.tag="$TAG" \
  --set database.host=postgres --set database.port=5442 --set database.name=re_proof --set database.user=re_rt --set database.existingSecret=re-db \
  --set database.owner.user=re_owner --set database.owner.existingSecret=re-owner-db \
  --set egeria.platformUrl=https://qs-platform:9443 --set egeria.daemon.userId=omagspcatnpa --set egeria.daemon.existingSecret=re-egeria \
  --set persistence.storageClassName=standard --set 'persistence.accessModes={ReadWriteOnce}' "${PFARGS[@]}" --wait --timeout 15m | sed -n '/^NOTES/,$p'
echo "installed $REL in $NS after $(( $(date +%s) - T0 ))s"
kubectl -n "$NS" get pods
$HELM test "$REL" -n "$NS" --logs 2>&1 | grep -E "^ok|^FAIL|^PASS|Phase|TEST SUITE|Error"
if [ "${PREFECT:-0}" = 1 ]; then
  echo "--- Prefect: the worker's deployment and pool, as the server sees them"
  kubectl -n "$NS" exec -i deploy/${REL}-re-web -- python - <<'PY'
import json, os, urllib.request
api = os.environ["PREFECT_API_URL"].rstrip("/"); pool = os.environ["PREFECT_WORK_POOL"]
def post(path, body):
    req = urllib.request.Request(api + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=15))
print("pool:", [p["name"] + "/" + p["type"] for p in post("/work_pools/filter", {}) if p["name"] == pool])
print("deployments:", [d["name"] for d in post("/deployments/filter", {})])
print("workers:", [(w["name"][:28], w["status"]) for w in post("/work_pools/%s/workers/filter" % pool, {})])
PY
fi
if [ "${A2A:-0}" = 1 ]; then
  echo "--- A2A: the public index, a signed-in call, a context that does not exist"
  kubectl -n "$NS" exec -i deploy/${REL}-re-web -- python - <<PY
import json, os, ssl, urllib.error, urllib.request
base = "http://${REL}-re-a2a:8100"
ca = os.environ.get("PYEGERIA_CA_BUNDLE")
ctx = ssl.create_default_context(cafile=ca) if ca else ssl._create_unverified_context()
def get(url, token=None, data=None, ssl_ctx=None):
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", **({"Authorization": "Bearer " + token} if token else {})})
    try:
        r = urllib.request.urlopen(req, timeout=20, context=ssl_ctx)
        return r.status, r.read().decode()[:2000]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]
st, body = get(base + "/.well-known/agents.json")
idx = json.loads(body)
print("agents.json:", st, "base_url=", idx["base_url"], "egeria=", idx.get("egeria"), "agents=", [a["name"] for a in idx["agents"]])
user, pw, plat = os.environ["RE_DAEMON_USER_ID"], os.environ["RE_DAEMON_USER_PASSWORD"], os.environ["EGERIA_PLATFORM_URL"]
st, tok = get(plat + "/servers/" + os.environ["EGERIA_VIEW_SERVER"] + "/api/v1/users/" + user + "/token", data=json.dumps({"userId": user, "password": pw}).encode(), ssl_ctx=ctx)
tok = tok.strip().strip('"')
print("egeria token:", st, "len>0" if len(tok) > 20 else "none")
print("whoami with an Egeria token:", get(base + "/whoami", tok)[0])
print("whoami with a bogus token:", get(base + "/whoami", "not-a-token")[0])
st, body = get(base + "/agents/docs/v1/tasks/00000000-0000-0000-0000-000000000000", tok)
print("task that does not exist:", st, body[:160].replace("\n", " "))
PY
fi
