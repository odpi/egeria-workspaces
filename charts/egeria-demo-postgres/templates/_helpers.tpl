{{- define "egeria-demo-postgres.name" -}}
{{- $n := printf "%s-demo-postgres" .Release.Name -}}
{{- if gt (len $n) 63 -}}{{- fail (printf "release name %q is too long: %q would be over 63 characters" .Release.Name $n) -}}{{- end -}}
{{- $n -}}
{{- end -}}
{{- define "egeria-demo-postgres.labels" -}}
app.kubernetes.io/name: demo-postgres
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: egeria
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end -}}
{{- define "egeria-demo-postgres.selector" -}}
app.kubernetes.io/name: demo-postgres
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/* Pod identity (the same rules as egeria-common.podIdentity, which this demo chart does not depend on). */}}
{{- define "egeria-demo-postgres.podIdentity" -}}
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
