{{/* Pod identity (the same rules as egeria-common.podIdentity, which this demo chart does not depend on). */}}
{{- define "egeria-demo-kafka.podIdentity" -}}
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
