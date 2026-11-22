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
