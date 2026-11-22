#!/usr/bin/env bash
# Resource Explorer (charts/trellis-re) on a kind cluster, against a quickstart Egeria platform and the test Postgres (pgvector) that
# kind_infra.sh makes, with the schema split of TR-115: the schema Job runs as an OWNER role, the pods as a RUNTIME role that holds only
# default privileges on the owner's objects (no DDL rights).
# usage: kind_re.sh <namespace> [release]        env: RE_IMAGE (default tr112-registry:5000/trellis/resource-explorer) RE_TAG (default tr115-efd55108)
# Secret values are generated here or read from tracked demo files and are never printed. Test infrastructure only, NOT part of any chart.
set -euo pipefail
NS=${1:?namespace}; REL=${2:-re}
HERE=$(cd "$(dirname "$(readlink -f "$0")")" && pwd); CHARTS=$(dirname "$HERE")
IMG=${RE_IMAGE:-tr112-registry:5000/trellis/resource-explorer}; TAG=${RE_TAG:-tr115-efd55108}
HELM=${HELM:-helm}
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT; umask 077

# 1. an Egeria platform (quickstart demo) plus the test Postgres and Kafka (SKIP_PLATFORM=1 when they are already installed)
[ "${SKIP_PLATFORM:-0}" = 1 ] || bash "$HERE/kind_install.sh" quickstart "$NS" qs

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
$HELM dependency update "$CHARTS/trellis-re" >/dev/null
T0=$(date +%s)
$HELM upgrade --install "$REL" "$CHARTS/trellis-re" -n "$NS" -f "$CHARTS/trellis-re/values-demo.yaml" \
  --set image.repository="$IMG" --set image.tag="$TAG" \
  --set database.host=postgres --set database.port=5442 --set database.name=re_proof --set database.user=re_rt --set database.existingSecret=re-db \
  --set database.owner.user=re_owner --set database.owner.existingSecret=re-owner-db \
  --set egeria.platformUrl=https://qs-platform:9443 --set egeria.daemon.userId=omagspcatnpa --set egeria.daemon.existingSecret=re-egeria \
  --set persistence.storageClassName=standard --set 'persistence.accessModes={ReadWriteOnce}' --wait --timeout 15m | sed -n '/^NOTES/,$p'
echo "installed $REL in $NS after $(( $(date +%s) - T0 ))s"
kubectl -n "$NS" get pods
echo "--- schema Job (hook; deleted before the next hook run, so read it from the install log if gone)"
$HELM test "$REL" -n "$NS" --logs 2>&1 | grep -E "^ok|^FAIL|^PASS|Phase|TEST SUITE|Error"
