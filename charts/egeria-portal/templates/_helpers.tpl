{{/*
egeria-portal: environment defaults, validation and derived values. Every failure names the setting to change.
Use: {{ $cfg := include "egeria-portal.cfg" . | fromYaml }}
*/}}

{{- define "egeria-portal.envDefaults" -}}
{{- if eq . "quickstart" -}}
platformPort: 9443
viewServer: qs-view-server
userId: erinoverview
composeHost: quickstart-pyegeria-web
{{- else if eq . "freshstart" -}}
platformPort: 8443
viewServer: fs-view-server
userId: bootstrap
composeHost: freshstart-pyegeria-web
{{- else -}}
{{- fail (printf "environment must be quickstart or freshstart, not %q (set environment)" .) -}}
{{- end -}}
{{- end -}}

{{/* image reference: repository:tag[@digest]; dict "img" <values.images.x> "name" "images.portal" "prod" bool */}}
{{- define "egeria-portal.image" -}}
{{- if not .img.repository -}}{{- fail (printf "set %s.repository (the image from charts/README: for example localhost:5001/portal-quickstart)" .name) -}}{{- end -}}
{{- if not .img.tag -}}{{- fail (printf "set %s.tag" .name) -}}{{- end -}}
{{- if and .prod (not .img.digest) -}}{{- fail (printf "set %s.digest: the production posture pins images by digest" .name) -}}{{- end -}}
{{- if .img.digest -}}{{ printf "%s:%s@%s" .img.repository .img.tag .img.digest }}{{- else -}}{{ printf "%s:%s" .img.repository .img.tag }}{{- end -}}
{{- end -}}

{{- define "egeria-portal.cfg" -}}
{{- $v := .Values -}}
{{- $d := include "egeria-portal.envDefaults" $v.environment | fromYaml -}}
{{- if gt (int $v.replicas) 1 -}}
{{- fail (printf "replicas is %d: the Portal keeps its state in files and sqlite on one volume, so it runs as one pod. Set replicas to 1." (int $v.replicas)) -}}
{{- end -}}
{{- if not (has $v.posture (list "demo" "production")) -}}
{{- fail (printf "posture must be demo or production, not %q (use values-demo.yaml or values-production.yaml)" $v.posture) -}}
{{- end -}}
{{- $prod := eq $v.posture "production" -}}
{{- if not $v.platform.serviceName -}}
{{- fail "set platform.serviceName to the Service of the egeria-platform release in this namespace (usually <release>-platform)" -}}
{{- end -}}
{{- if and $prod (not $v.secrets.existingSecret) -}}
{{- fail "the production posture requires secrets.existingSecret: a Secret with keys jwt-secret, egeria-user-password and mcp-access-token. There is no built-in password." -}}
{{- end -}}
{{- if and $prod (not $v.tls.verify) -}}
{{- fail "tls.verify=false is demo only: the production posture checks the platform's certificate (set tls.verify=true and tls.caSecret)." -}}
{{- end -}}
{{- if and $prod $v.tls.verify (not $v.tls.caSecret) -}}
{{- fail "set tls.caSecret: a Secret with key ca.crt that the platform's certificate chains to (tls.verify is true)" -}}
{{- end -}}
{{- if and $prod (not $v.persistence.storageClassName) (not $v.persistence.existingClaim) -}}
{{- fail "the production posture requires persistence.storageClassName (or persistence.existingClaim)" -}}
{{- end -}}
{{- if and $prod $v.demoMode -}}
{{- fail "demoMode is demo only (it enables registration and the login gate of the public demos)." -}}
{{- end -}}
{{- if and $v.ingress.enabled (not $v.ingress.host) -}}
{{- fail "set ingress.host (ingress.enabled is true)" -}}
{{- end -}}
{{- if and $prod $v.ingress.enabled (not $v.ingress.tlsSecretName) -}}
{{- fail "set ingress.tlsSecretName: the production posture requires Ingress TLS" -}}
{{- end -}}
{{- $port := int (default $d.platformPort $v.platform.port) -}}
{{- $name := include "egeria-common.name" (dict "ctx" . "component" "portal") -}}
{{- $web := include "egeria-common.name" (dict "ctx" . "component" "portal-web") -}}
fullname: {{ $name }}
webname: {{ $web }}
prod: {{ $prod }}
platformUrl: {{ printf "https://%s:%d" $v.platform.serviceName $port | quote }}
platformHost: {{ $v.platform.serviceName | quote }}
viewServer: {{ default $d.viewServer $v.platform.viewServer | quote }}
userId: {{ default $d.userId $v.egeria.userId | quote }}
composeHost: {{ $d.composeHost | quote }}
secretName: {{ default (printf "%s-secrets" $name) $v.secrets.existingSecret }}
createSecret: {{ not $v.secrets.existingSecret }}
portalImage: {{ include "egeria-portal.image" (dict "img" $v.images.portal "name" "images.portal" "prod" $prod) | quote }}
apacheImage: {{ include "egeria-portal.image" (dict "img" $v.images.apache "name" "images.apache" "prod" $prod) | quote }}
dataClaim: {{ default (printf "%s-data" $name) $v.persistence.existingClaim }}
createDataClaim: {{ not $v.persistence.existingClaim }}
{{- end -}}
