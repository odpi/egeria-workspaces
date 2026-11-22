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
{{- if not .img.repository -}}{{- fail (printf "set %s.repository: the Portal and Apache images are not published, build them as charts/docs/kubernetes.md#images describes (for example localhost:5001/portal-quickstart)" .name) -}}{{- end -}}
{{- if not .img.tag -}}{{- fail (printf "set %s.tag" .name) -}}{{- end -}}
{{- if and .prod (not .img.digest) -}}{{- fail (printf "set %s.digest: the production posture pins images by digest" .name) -}}{{- end -}}
{{- if .img.digest -}}{{ printf "%s:%s@%s" .img.repository .img.tag .img.digest }}{{- else -}}{{ printf "%s:%s" .img.repository .img.tag }}{{- end -}}
{{- end -}}

{{/* Refuse a trusted-proxy entry that is not narrow (call with dict "list" <comma list> "name" <value name>). A CIDR must be /24 or narrower (IPv4) or /120 or narrower
(IPv6): 256 addresses at most. On kind (10.244.0.0/16) and Calico's default (192.168.0.0/16) even a /16 is the WHOLE pod network, and any pod that can reach Apache could
then forge X-Forwarded-For and choose its own rate-limit key. Hostnames and bare IPs are not checked here. */}}
{{- define "egeria-portal.checkProxyList" -}}
{{- range $c := splitList "," (regexReplaceAll "\\s+" .list "") -}}
{{- if contains "/" $c -}}
{{- $ok := false -}}
{{- if contains ":" $c -}}{{- $ok = regexMatch "/(12[0-8])$" $c -}}{{- else if contains "." $c -}}{{- $ok = regexMatch "/(2[4-9]|3[0-2])$" $c -}}{{- end -}}
{{- if not $ok -}}
{{- fail (printf "%s entry %q is not narrow enough: a range must be /24 or narrower (IPv4) or /120 or narrower (IPv6), at most 256 addresses. The Portal believes X-Forwarded-For from every address in it, so a range that covers the pod network lets any pod that reaches Apache pick its own rate-limit key. List the controller's /24s (several for a multi-node controller), or better its exact pods: a headless Service over them, with its full name here." $.name $c) -}}
{{- end -}}
{{- end -}}
{{- end -}}
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
{{- if and $prod (eq $v.environment "quickstart") -}}
{{- fail "the production posture needs a login gate, and the quickstart environment has none (SERVER_MANAGED_AUTH is false there; only the public-demo SQLite accounts gate it). The freshstart Portal has a sign-in page, but no server-side API gate yet (PO-78), so it cannot be exposed through an Ingress either: run it behind port-forward." -}}
{{- end -}}
{{- $stack := and $v.global (eq (toString (default false $v.global.stack)) "true") -}}
{{- $platformSvc := default (ternary (printf "%s-platform" .Release.Name) "" $stack) $v.platform.serviceName -}}
{{- if not $platformSvc -}}
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
{{- if and $v.ingress.enabled (eq $v.environment "freshstart") -}}
{{- fail "the freshstart Portal has no server-side API gate yet (PO-78): requests that carry no token are answered as the Portal's service user, so it must not be exposed through an Ingress (or an OpenShift Route, which is made from the Ingress). Leave ingress.enabled false and use kubectl port-forward. The sign-in page is a screen only; it does not protect the API." -}}
{{- end -}}
{{- if and $v.ingress.enabled (not $v.ingress.host) -}}
{{- fail "set ingress.host (ingress.enabled is true)" -}}
{{- end -}}
{{- if and $prod $v.ingress.enabled (not $v.ingress.tlsSecretName) -}}
{{- fail "set ingress.tlsSecretName: the production posture requires Ingress TLS" -}}
{{- end -}}
{{- if and $v.ingress.enabled (eq $v.environment "quickstart") (not $v.demoMode) (not $v.allowUngatedPortal) -}}
{{- fail "ingress.enabled with environment=quickstart and demoMode=false would publish a Portal with no login gate (local mode: anyone reaches Egeria as the Portal's service user). Use environment=freshstart, or demoMode=true, or set allowUngatedPortal=true (demo posture only)." -}}
{{- end -}}
{{- if and $v.ingress.enabled (not $v.networkPolicy.enabled) -}}
{{- fail "set networkPolicy.enabled=true: with an Ingress, the Portal Service on 8000 must be reachable only from the Apache front door, because the login gate trusts the edge header Apache adds. A direct path to 8000 would bypass the gate." -}}
{{- end -}}
{{- if and $prod (eq $v.environment "freshstart") (not $v.platform.userDirectorySecret) -}}
{{- fail "set platform.userDirectorySecret (in egeria-stack: portal.platform.userDirectorySecret) to the platform's Secret, usually the same one as the platform's secrets.existingSecret: the freshstart Portal reads the user directory from its key egeria-user-directory.omsecrets. The default <platform>-secrets exists only in the demo posture, and the optional mount would find nothing." -}}
{{- end -}}
{{- if and $v.allowUngatedPortal $prod -}}
{{- fail "allowUngatedPortal is demo only." -}}
{{- end -}}
{{- $owned := list "EGERIA_ROOT_PATH" "EGERIA_INBOX_PATH" "EGERIA_OUTBOX_PATH" "DEMO_MODE" "SERVER_MANAGED_AUTH" "JWT_SECRET" "EGERIA_USER_PASSWORD" "MCP_ACCESS_TOKEN" "EGERIA_USER" "PORTAL_ALLOWED_PLATFORM_URLS" "PORTAL_TRUSTED_PROXIES" "EGERIA_PLATFORM_URL" -}}
{{- range $e := $v.extraEnv -}}
{{- if has $e.name $owned -}}{{- fail (printf "extraEnv may not set %s: the chart owns it (set the matching value instead)." $e.name) -}}{{- end -}}
{{- end -}}
{{- $port := int (default $d.platformPort $v.platform.port) -}}
{{- $name := include "egeria-common.name" (dict "ctx" . "component" "portal") -}}
{{- $web := include "egeria-common.name" (dict "ctx" . "component" "portal-web") -}}
{{- $webhl := include "egeria-common.name" (dict "ctx" . "component" "portal-web-hl") -}}
{{- $ctl := regexReplaceAll "\\s+" (default "" $v.ingressControllerCidr) "" -}}
{{- include "egeria-portal.checkProxyList" (dict "list" $ctl "name" "ingressControllerCidr") -}}
{{- include "egeria-portal.checkProxyList" (dict "list" (default "" $v.trustedProxies) "name" "trustedProxies") -}}
{{- $base := regexReplaceAll "\\s+" (default (printf "%s.%s.svc.cluster.local" $webhl .Release.Namespace) $v.trustedProxies) "" -}}
{{- $trusted := ternary (printf "%s,%s" $base $ctl) $base (ne $ctl "") -}}
fullname: {{ $name }}
webname: {{ $web }}
webhlname: {{ $webhl }}
trustedProxies: {{ $trusted | quote }}
prod: {{ $prod }}
platformUrl: {{ printf "https://%s:%d" $platformSvc $port | quote }}
platformHost: {{ $platformSvc | quote }}
viewServer: {{ default $d.viewServer $v.platform.viewServer | quote }}
userId: {{ default $d.userId $v.egeria.userId | quote }}
composeHost: {{ $d.composeHost | quote }}
secretName: {{ default (printf "%s-secrets" $name) $v.secrets.existingSecret }}
createSecret: {{ not $v.secrets.existingSecret }}
canarySecretName: {{ default (printf "%s-canary" $name) $v.canary.existingSecret }}
createCanarySecret: {{ and (not $v.canary.existingSecret) (not $prod) }}
hasCanary: {{ or (not (not $v.canary.existingSecret)) (not $prod) }}
managedAuth: {{ eq $v.environment "freshstart" }}
gated: {{ or (eq $v.environment "freshstart") $v.demoMode }}
portalImage: {{ include "egeria-portal.image" (dict "img" $v.images.portal "name" "images.portal" "prod" $prod) | quote }}
apacheImage: {{ include "egeria-portal.image" (dict "img" $v.images.apache "name" "images.apache" "prod" $prod) | quote }}
dataClaim: {{ default (printf "%s-data" $name) $v.persistence.existingClaim }}
createDataClaim: {{ not $v.persistence.existingClaim }}
{{- end -}}

{{/* Probe timings from values: only timing keys, so the probe's handler stays the chart's. dict "name" "probes.x.y" "t" <map> */}}
{{- define "egeria-portal.probeTiming" -}}
{{- $allowed := list "initialDelaySeconds" "periodSeconds" "timeoutSeconds" "failureThreshold" "successThreshold" -}}
{{- range $k, $_ := .t -}}
{{- if not (has $k $allowed) -}}{{- fail (printf "%s.%s is not allowed: only %s can be set (the probe's check is the chart's)" $.name $k (join ", " $allowed)) -}}{{- end -}}
{{- end -}}
{{- if .t }}{{ toYaml .t }}{{ end -}}
{{- end -}}
