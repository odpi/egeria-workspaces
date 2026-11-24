{{/*
trellis-re: validation, derived values and the shared pod environment. Every failure names the setting to change.
Use: {{ $cfg := include "trellis-re.cfg" . | fromYaml }}
*/}}

{{/* image reference: repository:tag[@digest] */}}
{{- define "trellis-re.image" -}}
{{- if not .img.repository -}}{{- fail "set image.repository: the Resource Explorer image is not published; build it from the trellis repo (docker/Dockerfile.resource-explorer) and push it to a registry your cluster can pull from" -}}{{- end -}}
{{- if not .img.tag -}}{{- fail "set image.tag" -}}{{- end -}}
{{- if and .prod (not .img.digest) -}}{{- fail "set image.digest: the production posture pins images by digest" -}}{{- end -}}
{{- if .img.digest -}}{{ printf "%s:%s@%s" .img.repository .img.tag .img.digest }}{{- else -}}{{ printf "%s:%s" .img.repository .img.tag }}{{- end -}}
{{- end -}}

{{- define "trellis-re.cfg" -}}
{{- $v := .Values -}}
{{- if not (has $v.posture (list "demo" "production")) -}}
{{- fail (printf "posture must be demo or production, not %q (use values-demo.yaml or values-production.yaml)" $v.posture) -}}
{{- end -}}
{{- $prod := eq $v.posture "production" -}}
{{- range $p := list (list "database.host" $v.database.host) (list "database.name" $v.database.name) (list "database.user" $v.database.user) (list "egeria.daemon.userId" $v.egeria.daemon.userId) -}}
{{- if not (index $p 1) -}}{{- fail (printf "set %s" (index $p 0)) -}}{{- end -}}
{{- end -}}
{{- /* In an umbrella (global.stack) the platform is this release's own Service; outside one it must be set. */ -}}
{{- $gtls := default (dict) (get (default (dict) $v.global) "tls") -}}
{{- $stack := eq (toString (default false (get (default (dict) $v.global) "stack"))) "true" -}}
{{- if not (has $v.environment (list "quickstart" "freshstart")) -}}{{- fail (printf "environment must be quickstart or freshstart, not %q" $v.environment) -}}{{- end -}}
{{- $platformUrl := $v.egeria.platformUrl -}}
{{- if not $platformUrl -}}
{{- if $stack -}}{{- $platformUrl = printf "https://%s-platform:%d" .Release.Name (int (default (ternary 9443 8443 (eq $v.environment "quickstart")) $v.egeria.platformPort)) -}}
{{- else -}}{{- fail "set egeria.platformUrl" -}}{{- end -}}
{{- end -}}
{{- $viewServer := default (ternary "qs-view-server" "fs-view-server" (eq $v.environment "quickstart")) $v.egeria.viewServer -}}
{{- $tlsVerify := or $v.tls.verify (eq (toString (default false $gtls.verify)) "true") -}}
{{- $caSecret := default (default "" $gtls.caSecret) $v.tls.caSecret -}}
{{- if not $v.database.existingSecret -}}
{{- fail "set database.existingSecret: a Secret with the runtime role's password (key database.passwordKey). It must exist before the install: the schema Job runs as a pre-install hook." -}}
{{- end -}}
{{- if not $v.egeria.daemon.existingSecret -}}
{{- fail "set egeria.daemon.existingSecret: a Secret with RE's Egeria service-account password (key egeria.daemon.passwordKey)" -}}
{{- end -}}
{{- if lt (int $v.web.replicas) 1 -}}{{- fail "web.replicas must be at least 1" -}}{{- end -}}
{{- if lt (int $v.worker.replicas) 1 -}}{{- fail "worker.replicas must be at least 1: the worker runs the queue and the leader-elected loops" -}}{{- end -}}
{{- if and $prod (not $v.secrets.existingSecret) -}}
{{- fail "the production posture requires secrets.existingSecret: a Secret with keys jwt-secret and db-credential-key, shared by every pod" -}}
{{- end -}}
{{- if $prod -}}
{{- if or (not $v.database.owner.user) (not $v.database.owner.existingSecret) -}}
{{- fail "the production posture requires database.owner.user and database.owner.existingSecret: the schema Job runs as a separate OWNER role and the pods as the runtime role, which must hold no DDL rights (TR-115). Without an owner the Job would run as the runtime role, and an operator would have to grant it DDL, which removes the guarantee." -}}
{{- end -}}
{{- if eq $v.database.owner.user $v.database.user -}}
{{- fail "database.owner.user is the same role as database.user: the production posture needs two roles, so that the pods' runtime role holds no DDL rights (TR-115). Make a separate owner role." -}}
{{- end -}}
{{- end -}}
{{- if and $prod (not $tlsVerify) -}}{{- fail "the production posture requires tls.verify=true (or global.tls.verify in a stack)" -}}{{- end -}}
{{- if and $tlsVerify (not $caSecret) $prod -}}
{{- fail "set tls.caSecret (or global.tls.caSecret in a stack): a Secret with key ca.crt that the platform's certificate chains to (tls.verify is true)" -}}
{{- end -}}
{{- if and $prod (not $v.persistence.storageClassName) (not $v.persistence.existingClaim) -}}
{{- fail "the production posture requires persistence.storageClassName (or persistence.existingClaim)" -}}
{{- end -}}
{{- if and $v.ingress.enabled (not $v.ingress.host) -}}{{- fail "set ingress.host (ingress.enabled is true)" -}}{{- end -}}
{{- if and $prod $v.ingress.enabled (not $v.ingress.tlsSecretName) -}}
{{- fail "set ingress.tlsSecretName: the production posture requires Ingress TLS" -}}
{{- end -}}
{{- if not (has $v.llm.backend (list "ollama" "openai" "anthropic")) -}}
{{- fail (printf "llm.backend must be ollama, openai or anthropic, not %q" $v.llm.backend) -}}
{{- end -}}
{{- if and $v.prefect.enabled (not $v.prefect.apiUrl) -}}
{{- fail "set prefect.apiUrl (prefect.enabled is true): the Prefect server's API, for example http://prefect-server:4200/api. This chart does not run a Prefect server." -}}
{{- end -}}
{{- if and $v.prefect.enabled (lt (int $v.prefect.worker.replicas) 1) -}}{{- fail "prefect.worker.replicas must be at least 1 (prefect.enabled is true)" -}}{{- end -}}
{{- if and $v.a2a.enabled (ne (int $v.a2a.replicas) 1) -}}
{{- fail "a2a.replicas must be 1: the A2A context store is in memory, so a task started on one pod is invisible on another (more replicas need sticky routing, which this chart does not set up)" -}}
{{- end -}}
{{- if and $v.a2a.enabled $prod $v.a2a.publicUrl (not (hasPrefix "https://" $v.a2a.publicUrl)) (not (hasPrefix "http://" $v.a2a.publicUrl)) -}}
{{- fail "a2a.publicUrl must start with http:// or https://" -}}
{{- end -}}
{{- $owned := list "RE_SCHEMA_MODE" "PGVECTOR_HOST" "PGVECTOR_PORT" "PGVECTOR_DBNAME" "PGVECTOR_USER" "PGVECTOR_PASSWORD" "PGVECTOR_SCHEMA" "EGERIA_PLATFORM_URL" "EGERIA_VIEW_SERVER_URL" "EGERIA_VIEW_SERVER" "RE_DAEMON_USER_ID" "RE_DAEMON_USER_PASSWORD" "RE_JWT_SECRET" "TRELLIS_DB_CREDENTIAL_KEY" "PYEGERIA_SSL_VERIFY" "PYEGERIA_CA_BUNDLE" "PREFECT_ENABLED" "EMBEDDINGS__DEVICE" "PYEGERIA_LOG_DIRECTORY" "EMBED_WORKER" "A2A_ALLOW_ANONYMOUS" "A2A_PUBLIC_URL" "PORT" "HOST" "PREFECT_API_URL" "PREFECT_WORK_POOL" "PREFECT_DISPATCH_STEPS" "PREFECT_API_KEY" -}}
{{- range $e := $v.extraEnv -}}
{{- if eq $e.name "A2A_ALLOW_ANONYMOUS" -}}{{- fail "extraEnv: A2A_ALLOW_ANONYMOUS would remove the bearer-token gate from every A2A agent; the chart never sets it (it is false) and refuses to pass it through. A2A is for signed-in callers only." -}}{{- end -}}
{{- if has $e.name $owned -}}{{- fail (printf "extraEnv: %s is set by the chart; change the chart value it comes from instead" $e.name) -}}{{- end -}}
{{- end -}}
{{- $web := include "egeria-common.name" (dict "ctx" . "component" "re-web") -}}
{{- $worker := include "egeria-common.name" (dict "ctx" . "component" "re-worker") -}}
{{- $pfworker := include "egeria-common.name" (dict "ctx" . "component" "re-prefect-worker") -}}
{{- $a2a := include "egeria-common.name" (dict "ctx" . "component" "re-a2a") -}}
{{- $job := include "egeria-common.name" (dict "ctx" . "component" "re-schema") -}}
{{- $secretName := default (include "egeria-common.name" (dict "ctx" . "component" "re-secrets")) $v.secrets.existingSecret -}}
{{- $dataClaim := default (include "egeria-common.name" (dict "ctx" . "component" "re-data")) $v.persistence.existingClaim -}}
platformUrl: {{ $platformUrl | quote }}
viewServer: {{ $viewServer | quote }}
tlsVerify: {{ $tlsVerify }}
caSecret: {{ $caSecret | quote }}
webname: {{ $web }}
workername: {{ $worker }}
jobname: {{ $job }}
a2aname: {{ $a2a }}
a2aurl: {{ default (printf "http://%s:%d" $a2a (int $v.a2a.port)) $v.a2a.publicUrl }}
prefectworkername: {{ $pfworker }}
secretName: {{ $secretName }}
createSecret: {{ not $v.secrets.existingSecret }}
dataClaim: {{ $dataClaim }}
createDataClaim: {{ not $v.persistence.existingClaim }}
image: {{ include "trellis-re.image" (dict "img" $v.image "prod" $prod) }}
ownerUser: {{ default $v.database.user $v.database.owner.user }}
ownerSecret: {{ default $v.database.existingSecret $v.database.owner.existingSecret }}
ownerKey: {{ ternary $v.database.owner.passwordKey $v.database.passwordKey (not (empty $v.database.owner.existingSecret)) }}
{{- end -}}

{{/* The environment every RE pod gets, without the Egeria service account and without extraEnv. Call with the root context. */}}
{{- define "trellis-re.envCore" -}}
{{- $v := .Values -}}
{{- $cfg := include "trellis-re.cfg" . | fromYaml -}}
- {name: RE_SCHEMA_MODE, value: external}
- {name: PGVECTOR_HOST, value: {{ $v.database.host | quote }}}
- {name: PGVECTOR_PORT, value: {{ $v.database.port | quote }}}
- {name: PGVECTOR_DBNAME, value: {{ $v.database.name | quote }}}
- {name: PGVECTOR_USER, value: {{ $v.database.user | quote }}}
- {name: PGVECTOR_SCHEMA, value: {{ $v.database.schema | quote }}}
- {name: PGVECTOR_PASSWORD, valueFrom: {secretKeyRef: {name: {{ $v.database.existingSecret }}, key: {{ $v.database.passwordKey }}}}}
- {name: EGERIA_PLATFORM_URL, value: {{ $cfg.platformUrl | quote }}}
- {name: EGERIA_VIEW_SERVER_URL, value: {{ $cfg.platformUrl | quote }}}
- {name: EGERIA_VIEW_SERVER, value: {{ $cfg.viewServer | quote }}}
- {name: RE_JWT_SECRET, valueFrom: {secretKeyRef: {name: {{ $cfg.secretName }}, key: jwt-secret}}}
- {name: TRELLIS_DB_CREDENTIAL_KEY, valueFrom: {secretKeyRef: {name: {{ $cfg.secretName }}, key: db-credential-key}}}
- {name: PYEGERIA_SSL_VERIFY, value: {{ $cfg.tlsVerify | quote }}}
{{- if $cfg.caSecret }}
- {name: PYEGERIA_CA_BUNDLE, value: /etc/egeria-ca/ca.crt}
{{- end }}
# web, worker and the Prefect worker run one image: one RE commit per release, which RE requires before it dispatches. No MLflow or Phoenix.
{{- if $v.prefect.enabled }}
- {name: PREFECT_ENABLED, value: "true"}
- {name: PREFECT_API_URL, value: {{ $v.prefect.apiUrl | quote }}}
- {name: PREFECT_WORK_POOL, value: {{ $v.prefect.workPool | quote }}}
{{- if $v.prefect.dispatchSteps }}
- {name: PREFECT_DISPATCH_STEPS, value: {{ $v.prefect.dispatchSteps | quote }}}
{{- end }}
{{- if $v.prefect.apiKeySecret }}
- {name: PREFECT_API_KEY, valueFrom: {secretKeyRef: {name: {{ $v.prefect.apiKeySecret }}, key: api-key}}}
{{- end }}
{{- else }}
- {name: PREFECT_ENABLED, value: "false"}
{{- end }}
- {name: OBSERVABILITY__MLFLOW__ENABLED, value: "false"}
- {name: OBSERVABILITY__PHOENIX__ENABLED, value: "false"}
- {name: EMBEDDINGS__DEVICE, value: {{ $v.embeddings.device | quote }}}
- {name: PYEGERIA_LOG_DIRECTORY, value: {{ $v.logs.directory | quote }}}
- {name: LLM__BACKEND, value: {{ $v.llm.backend | quote }}}
{{- if $v.llm.ollama.baseUrl }}
- {name: LLM__OLLAMA__BASE_URL, value: {{ $v.llm.ollama.baseUrl | quote }}}
{{- end }}
{{- if $v.llm.ollama.model }}
- {name: LLM__OLLAMA__MODEL, value: {{ $v.llm.ollama.model | quote }}}
{{- end }}
{{- if $v.publicUrl }}
- {name: RE_PUBLIC_URL, value: {{ $v.publicUrl | quote }}}
{{- end }}
{{- end -}}


{{/* RE's Egeria service account (RE_DAEMON_*): the worker loops, the Prefect steps and web need it; the A2A pod does not unless a2a.serviceAccount is set. */}}
{{- define "trellis-re.daemonEnv" -}}
{{- $v := .Values -}}
- {name: RE_DAEMON_USER_ID, value: {{ $v.egeria.daemon.userId | quote }}}
- {name: RE_DAEMON_USER_PASSWORD, valueFrom: {secretKeyRef: {name: {{ $v.egeria.daemon.existingSecret }}, key: {{ $v.egeria.daemon.passwordKey }}}}}
{{- end -}}

{{/* extraEnv: appended last, after the chart's own names were checked in trellis-re.cfg. */}}
{{- define "trellis-re.extraEnv" -}}
{{- with .Values.extraEnv }}
{{ toYaml . }}
{{- end }}
{{- end -}}

{{/* The environment of the web, worker and Prefect worker pods (the A2A pod composes its own). Call with the root context. */}}
{{- define "trellis-re.env" -}}
{{ include "trellis-re.envCore" . }}
{{ include "trellis-re.daemonEnv" . }}
{{- include "trellis-re.extraEnv" . }}
{{- end -}}

{{/* Probe timing from a values dict, every field optional */}}
{{- define "trellis-re.probeTiming" -}}
{{- range $k, $x := . }}
{{ $k }}: {{ $x }}
{{- end }}
{{- end -}}
