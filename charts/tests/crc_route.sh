#!/usr/bin/env bash
# A Route for the Portal front door on OpenShift Local, with no chart change: OpenShift turns the chart's Ingress into a Route.
# usage: crc_route.sh [namespace] [release] [host]      needs: the stack already installed by crc_stack.sh or crc_stack_prod.sh (quickstart needs demoMode)
# The Ingress needs portal.networkPolicy.enabled (the chart refuses an Ingress without it) and the annotation route.openshift.io/termination=edge
# (TLS at the router with its default certificate; plain http is redirected to https). The Route points at the Apache Service only: the Portal's
# own port 8000 stays inside the cluster behind its NetworkPolicy. Prints only status codes.
set -euo pipefail
NS=${1:-egeria-demo}; REL=${2:-qs}; HOSTN=${3:-portal-$NS.apps-crc.testing}
HERE=$(cd "$(dirname "$(readlink -f "$0")")" && pwd); CHARTS=$(dirname "$HERE")
export KUBECONFIG=${KUBECONFIG:-$HOME/.crc/machines/crc/kubeconfig}; OC=${OC:-$HOME/.crc/bin/oc/oc}
helm upgrade "$REL" "$CHARTS/egeria-stack" -n "$NS" --reuse-values --set portal.networkPolicy.enabled=true \
  --set portal.ingress.enabled=true --set portal.ingress.host="$HOSTN" \
  --set-string 'portal.ingress.annotations.route\.openshift\.io/termination=edge' | grep -E "^STATUS|Error"
for i in $(seq 1 12); do $OC -n "$NS" get route -o name 2>/dev/null | grep -q . && break; sleep 5; done
$OC -n "$NS" get route
H=https://$HOSTN
chk() { got=$(curl -sk -o /dev/null -w "%{http_code}" "$@"); echo "$got  ${*: -1}"; [ "$got" = "$WANT" ]; }
WANT=302; chk "$H/portal"                                    # the login gate redirects
WANT=200; chk "$H/login"
WANT=401; chk -X POST -H 'Content-Type: application/json' -d '{}' "$H/api/egeria-token"      # PO-68: no password, no session
WANT=401; chk "$H/api/operations/platforms"                  # an authenticated API is closed to an anonymous caller
WANT=302; chk "http://$HOSTN/portal"                         # plain http is redirected to https
helm test "$REL" -n "$NS" --logs 2>&1 | grep -E "^FAIL|^PASS"
