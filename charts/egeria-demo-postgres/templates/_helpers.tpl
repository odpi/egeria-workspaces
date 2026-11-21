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
