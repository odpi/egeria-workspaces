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
{{- range $p := list (list "database.host" $v.database.host) (list "database.name" $v.database.name) (list "database.user" $v.database.user) (list "egeria.platformUrl" $v.egeria.platformUrl) (list "egeria.daemon.userId" $v.egeria.daemon.userId) -}}
{{- if not (index $p 1) -}}{{- fail (printf "set %s" (index $p 0)) -}}{{- end -}}
{{- end -}}
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
{{- if and $prod (not $v.tls.verify) -}}{{- fail "the production posture requires tls.verify=true" -}}{{- end -}}
{{- if and $v.tls.verify (not $v.tls.caSecret) $prod -}}
{{- fail "set tls.caSecret: a Secret with key ca.crt that the platform's certificate chains to (tls.verify is true)" -}}
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
{{- $owned := list "RE_SCHEMA_MODE" "PGVECTOR_HOST" "PGVECTOR_PORT" "PGVECTOR_DBNAME" "PGVECTOR_USER" "PGVECTOR_PASSWORD" "PGVECTOR_SCHEMA" "EGERIA_PLATFORM_URL" "EGERIA_VIEW_SERVER_URL" "EGERIA_VIEW_SERVER" "RE_DAEMON_USER_ID" "RE_DAEMON_USER_PASSWORD" "RE_JWT_SECRET" "TRELLIS_DB_CREDENTIAL_KEY" "PYEGERIA_SSL_VERIFY" "PYEGERIA_CA_BUNDLE" "PREFECT_ENABLED" "EMBEDDINGS__DEVICE" "PYEGERIA_LOG_DIRECTORY" "EMBED_WORKER" "PREFECT_API_URL" "PREFECT_WORK_POOL" "PREFECT_DISPATCH_STEPS" "PREFECT_API_KEY" -}}
{{- range $e := $v.extraEnv -}}
{{- if has $e.name $owned -}}{{- fail (printf "extraEnv: %s is set by the chart; change the chart value it comes from instead" $e.name) -}}{{- end -}}
{{- end -}}
{{- $web := include "egeria-common.name" (dict "ctx" . "component" "re-web") -}}
{{- $worker := include "egeria-common.name" (dict "ctx" . "component" "re-worker") -}}
{{- $pfworker := include "egeria-common.name" (dict "ctx" . "component" "re-prefect-worker") -}}
{{- $job := include "egeria-common.name" (dict "ctx" . "component" "re-schema") -}}
{{- $secretName := default (include "egeria-common.name" (dict "ctx" . "component" "re-secrets")) $v.secrets.existingSecret -}}
{{- $dataClaim := default (include "egeria-common.name" (dict "ctx" . "component" "re-data")) $v.persistence.existingClaim -}}
webname: {{ $web }}
workername: {{ $worker }}
jobname: {{ $job }}
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

{{/* The environment shared by the web and worker pods. Call with the root context. */}}
{{- define "trellis-re.env" -}}
{{- $v := .Values -}}
{{- $cfg := include "trellis-re.cfg" . | fromYaml -}}
- {name: RE_SCHEMA_MODE, value: external}
- {name: PGVECTOR_HOST, value: {{ $v.database.host | quote }}}
- {name: PGVECTOR_PORT, value: {{ $v.database.port | quote }}}
- {name: PGVECTOR_DBNAME, value: {{ $v.database.name | quote }}}
- {name: PGVECTOR_USER, value: {{ $v.database.user | quote }}}
- {name: PGVECTOR_SCHEMA, value: {{ $v.database.schema | quote }}}
- {name: PGVECTOR_PASSWORD, valueFrom: {secretKeyRef: {name: {{ $v.database.existingSecret }}, key: {{ $v.database.passwordKey }}}}}
- {name: EGERIA_PLATFORM_URL, value: {{ $v.egeria.platformUrl | quote }}}
- {name: EGERIA_VIEW_SERVER_URL, value: {{ $v.egeria.platformUrl | quote }}}
- {name: EGERIA_VIEW_SERVER, value: {{ $v.egeria.viewServer | quote }}}
- {name: RE_DAEMON_USER_ID, value: {{ $v.egeria.daemon.userId | quote }}}
- {name: RE_DAEMON_USER_PASSWORD, valueFrom: {secretKeyRef: {name: {{ $v.egeria.daemon.existingSecret }}, key: {{ $v.egeria.daemon.passwordKey }}}}}
- {name: RE_JWT_SECRET, valueFrom: {secretKeyRef: {name: {{ $cfg.secretName }}, key: jwt-secret}}}
- {name: TRELLIS_DB_CREDENTIAL_KEY, valueFrom: {secretKeyRef: {name: {{ $cfg.secretName }}, key: db-credential-key}}}
- {name: PYEGERIA_SSL_VERIFY, value: {{ $v.tls.verify | quote }}}
{{- if $v.tls.caSecret }}
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
{{- with $v.extraEnv }}
{{ toYaml . }}
{{- end }}
{{- end -}}

{{/* Probe timing from a values dict, every field optional */}}
{{- define "trellis-re.probeTiming" -}}
{{- range $k, $x := . }}
{{ $k }}: {{ $x }}
{{- end }}
{{- end -}}
