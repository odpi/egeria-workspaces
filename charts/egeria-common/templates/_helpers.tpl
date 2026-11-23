{{/*
egeria-common: helpers shared by every Egeria chart.
Rules (design note section 16): every object name comes from the release name,
nothing is cluster-scoped, nothing external is fixed in a template.
Call with the root context: {{ include "egeria-common.name" (dict "ctx" . "component" "platform") }}
*/}}

{{/* <release>-<component>, at most 63 characters, trailing dash removed */}}
{{- define "egeria-common.name" -}}
{{- $n := printf "%s-%s" .ctx.Release.Name .component -}}
{{- if gt (len $n) 63 -}}
{{- fail (printf "egeria-common: the release name %q is too long: %q would exceed 63 characters. Use a shorter release name." .ctx.Release.Name $n) -}}
{{- end -}}
{{- $n -}}
{{- end -}}

{{/* Selector labels: stable across upgrades */}}
{{- define "egeria-common.selectorLabels" -}}
app.kubernetes.io/name: {{ .component }}
app.kubernetes.io/instance: {{ .ctx.Release.Name }}
{{- end -}}

{{/* Full label set */}}
{{- define "egeria-common.labels" -}}
{{ include "egeria-common.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .ctx.Release.Service }}
app.kubernetes.io/part-of: egeria
helm.sh/chart: {{ printf "%s-%s" .ctx.Chart.Name .ctx.Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end -}}

{{/* true when global.openshift is explicitly set (never auto-detected) */}}
{{- define "egeria-common.openshift" -}}
{{- if and .Values.global .Values.global.openshift -}}true{{- end -}}
{{- end -}}

{{/*
Pod security context. With global.openshift: true there is no runAsUser,
runAsGroup or fsGroup: restricted-v2 assigns an arbitrary UID with GID 0.
Call with the root context.
*/}}
{{- define "egeria-common.podSecurityContext" -}}
runAsNonRoot: true
seccompProfile:
  type: RuntimeDefault
{{- if not (include "egeria-common.openshift" .) }}
runAsUser: {{ .Values.securityContext.runAsUser }}
runAsGroup: {{ .Values.securityContext.runAsGroup }}
fsGroup: {{ .Values.securityContext.fsGroup }}
{{- end }}
{{- end -}}

{{- define "egeria-common.containerSecurityContext" -}}
allowPrivilegeEscalation: false
capabilities:
  drop:
    - ALL
{{- end -}}

{{/* A failure that says which setting to change. */}}
{{- define "egeria-common.requireValue" -}}
{{- if not .value -}}
{{- fail (printf "set %s%s" .name (default "" .hint)) -}}
{{- end -}}
{{- end -}}

{{/*
Pod identity: serviceAccountName and imagePullSecrets, for every pod (test pods too). Call with the root context.
Pull secrets are the chart's own imagePullSecrets plus global.imagePullSecrets (set once in an umbrella); each entry is
a name or {name: ...}. The ServiceAccount is never created: serviceAccountName must name one that exists.
*/}}
{{- define "egeria-common.podIdentity" -}}
{{- if .Values.serviceAccountName }}
serviceAccountName: {{ .Values.serviceAccountName }}
{{- end }}
{{- $all := list -}}
{{- range $s := (default list .Values.imagePullSecrets) }}{{ $all = append $all $s }}{{ end -}}
{{- if and .Values.global .Values.global.imagePullSecrets }}{{ range $s := .Values.global.imagePullSecrets }}{{ $all = append $all $s }}{{ end }}{{ end -}}
{{- $names := list -}}
{{- range $s := $all }}
{{- $n := "" }}
{{- if kindIs "string" $s }}{{ $n = $s }}{{ else if kindIs "map" $s }}{{ $n = get $s "name" }}{{ end }}
{{- if not $n }}{{ fail "imagePullSecrets: each entry is a Secret name or {name: <Secret>}" }}{{ end }}
{{- $names = append $names $n }}
{{- end -}}
{{- with ($names | uniq) }}
imagePullSecrets:
{{- range . }}
  - name: {{ . }}
{{- end }}
{{- end }}
{{- end -}}

{{/*
egeria-common.waitForServers: shell steps shared by the platform canary and Resource Explorer's wait. Signs in to the platform and polls
the active-servers list until every name in $SERVERS is active. The caller defines CURL, BASE, SERVERS, end (a deadline in epoch seconds)
and fail(), and exports the two environment variables named here. The password goes in on stdin, never in argv or the log.
Use: {{ include "egeria-common.waitForServers" (dict "user" "CANARY_USER" "password" "CANARY_PASSWORD" "progress" false) | nindent 10 }}
*/}}
{{- define "egeria-common.waitForServers" -}}
# 1. log in (the password is never printed)
token=
tick=$(date +%s)
while [ -z "$token" ]; do
  token=$(printf '{"userId":"%s","password":"%s"}' "${{ .user }}" "${{ .password }}" | $CURL --max-time 20 -X POST -H 'Content-Type: application/json' --data @- "$BASE/api/token" || true)
  case "$token" in eyJ*) ;; *) token=; [ "$(date +%s)" -lt "$end" ] || fail "could not get a token for account ${{ .user }} from $BASE before the deadline"
    {{- if .progress }}
    [ $(( $(date +%s) - tick )) -lt 60 ] || { echo "waiting: no token yet from $BASE"; tick=$(date +%s); }
    {{- end }}
    sleep 10 ;; esac
done
echo "ok: logged in as ${{ .user }}"
auth="Authorization: Bearer $token"
# 2. every name in SERVERS is active
while :; do
  active=$($CURL --max-time 30 -H "$auth" "$BASE/open-metadata/platform-services/server-platform/servers/active" || true)
  missing=
  for s in $SERVERS; do case "$active" in *"\"$s\""*) ;; *) missing="$missing $s" ;; esac; done
  case "$active" in *'"relatedHTTPCode":200'*) [ -z "$missing" ] && break ;; *) missing="${missing:- (no valid answer; is ${{ .user }} allowed to list active servers?)}" ;; esac
  [ "$(date +%s)" -lt "$end" ] || fail "servers not active before the deadline:$missing"
  {{- if .progress }}
  [ $(( $(date +%s) - tick )) -lt 60 ] || { echo "waiting: not active yet:$missing"; tick=$(date +%s); }
  {{- end }}
  sleep 10
done
echo "ok: all active: $SERVERS"
{{- end -}}
