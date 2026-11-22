{{/*
egeria-platform: environment defaults, validation and derived values.
"egeria-platform.cfg" returns YAML; consumers use: {{ $cfg := include "egeria-platform.cfg" . | fromYaml }}
Every failure names the setting to change.
*/}}

{{- define "egeria-platform.envDefaults" -}}
{{- if eq . "quickstart" -}}
port: 9443
xtdb: true
cpuLimit: "4"
database: egeria
organizationName: Coco Pharmaceuticals
userDirectoryStore: /deployments/secrets/coco-user-directory.omsecrets
userDirectoryCollection: cocoUserDirectory
servers: [qs-metadata-store, qs-engine-host, qs-integration-daemon, qs-view-server, qs-nanny-daemon]
{{- else if eq . "freshstart" -}}
port: 8443
xtdb: false
cpuLimit: ""
database: egeria_freshstart
organizationName: "null"
userDirectoryStore: /deployments/secrets/egeria-user-directory.omsecrets
userDirectoryCollection: userDirectory
servers: [fs-metadata-store, fs-engine-host, fs-integration-daemon, fs-view-server, fs-nanny-daemon]
{{- else -}}
{{- fail (printf "environment must be quickstart or freshstart, not %q (set environment)" .) -}}
{{- end -}}
{{- end -}}

{{- define "egeria-platform.cfg" -}}
{{- $v := .Values -}}
{{- $env := $v.environment -}}
{{- $d := include "egeria-platform.envDefaults" $env | fromYaml -}}

{{- if gt (int $v.replicas) 1 -}}
{{- fail (printf "replicas is %d: one OMAG platform cannot be scaled out, and a second replica would corrupt the shared metadata. Set replicas to 1, or install a second release instead." (int $v.replicas)) -}}
{{- end -}}
{{- if not (has $v.posture (list "demo" "production")) -}}
{{- fail (printf "posture must be demo or production, not %q (use values-demo.yaml or values-production.yaml)" $v.posture) -}}
{{- end -}}

{{- $port := int (default $d.port $v.platform.port) -}}
{{- if lt $port 1024 -}}
{{- fail (printf "platform.port is %d: ports below 1024 are not allowed, because the image must run under an arbitrary UID. Set platform.port to 1024 or more." $port) -}}
{{- end -}}
{{- $servers := ternary $v.platform.serverList $d.servers (gt (len $v.platform.serverList) 0) -}}
{{- if eq (len $servers) 0 -}}
{{- fail (printf "environment %s has no servers: set platform.serverList. The image's own default (port 7443, no servers) is never used." $env) -}}
{{- end -}}
{{- range $s := $servers -}}
{{- if not ($.Files.Get (printf "files/%s/servers/%s/%s.config" $env $s $s)) -}}
{{- fail (printf "server %s is in the server list but this chart has no configuration document for it (files/%s/servers/%s/%s.config). Without it the platform would exit with OMAG-ADMIN-400-011. Add the document or remove the server from platform.serverList." $s $env $s $s) -}}
{{- end -}}
{{- end -}}

{{- if and (eq $v.posture "production") (or $v.demoPostgres.enabled $v.demoKafka.enabled) -}}
{{- fail "demoPostgres and demoKafka are demo only: the production posture needs your own postgres.host and kafka.bootstrapServers." -}}
{{- end -}}
{{- $pgHost := default (ternary (printf "%s-demo-postgres" .Release.Name) "" $v.demoPostgres.enabled) $v.postgres.host -}}
{{- $pgPort := ternary 5442 (int $v.postgres.port) (and $v.demoPostgres.enabled (not $v.postgres.host)) -}}
{{- $kafka := default (ternary (printf "%s-demo-kafka.%s.svc.cluster.local:9192" .Release.Name .Release.Namespace) "" $v.demoKafka.enabled) $v.kafka.bootstrapServers -}}
{{- if not $pgHost -}}
{{- fail "set postgres.host: the platform needs an external PostgreSQL (host name of a service in or outside the cluster). The database defaults to the environment's: egeria or egeria_freshstart." -}}
{{- end -}}
{{- if not $kafka -}}
{{- fail "set kafka.bootstrapServers: the platform needs an external Kafka (host:port)." -}}
{{- end -}}

{{- if and (not $v.secrets.existingSecret) (not $v.secrets.useDemoFiles) -}}
{{- fail "set secrets.existingSecret to a Secret holding the /deployments/secrets files (egeria-servers.omsecrets and the others), or for a demo use values-demo.yaml (secrets.useDemoFiles). There is no built-in default password." -}}
{{- end -}}
{{- if and (eq $v.posture "production") $v.secrets.useDemoFiles -}}
{{- fail "secrets.useDemoFiles is demo only: the production posture requires secrets.existingSecret." -}}
{{- end -}}
{{- if eq $v.posture "production" -}}
{{- if not $v.secrets.existingSecret -}}{{- fail "the production posture requires secrets.existingSecret" -}}{{- end -}}
{{- if not $v.persistence.storageClassName -}}{{- if not $v.persistence.existingClaim -}}{{- fail "the production posture requires persistence.storageClassName (or persistence.existingClaim)" -}}{{- end -}}{{- end -}}
{{- if not (and $v.resources.limits $v.resources.limits.memory $v.resources.limits.cpu $v.resources.requests $v.resources.requests.memory $v.resources.requests.cpu) -}}
{{- fail "the production posture requires resources.requests and resources.limits for cpu and memory" -}}
{{- end -}}
{{- end -}}

{{- if eq $v.posture "production" -}}
{{- if not $v.tls.existingSecret -}}{{- fail "the production posture requires tls.existingSecret: a Secret with keystore.p12, truststore.p12, keystore-password and truststore-password. The demo keystore built into the image is demo only." -}}{{- end -}}
{{- if eq (toString $v.tls.strictSsl) "false" -}}{{- fail "tls.strictSsl=false is demo only: the production posture checks TLS certificates (strict.ssl=true)." -}}{{- end -}}
{{- end -}}

{{- $startup := mul (int $v.probes.startup.failureThreshold) (int $v.probes.startup.periodSeconds) -}}
{{- if lt $startup 600 -}}
{{- fail (printf "probes.startup allows %d seconds (failureThreshold x periodSeconds): it must be at least 600, because the first start loads content packs. Raise probes.startup.failureThreshold." $startup) -}}
{{- end -}}

{{- $org := default $d.organizationName $v.platform.organizationName -}}
{{- $fullname := include "egeria-common.name" (dict "ctx" . "component" "platform") -}}
{{- $headless := include "egeria-common.name" (dict "ctx" . "component" "platform-hl") -}}
{{- $self := printf "https://%s.%s.svc.cluster.local:%d" $headless .Release.Namespace $port -}}
{{- $pairs := list
  (list "organizationName" (ternary "null" (printf "%q" $org) (eq $org "null")))
  (list "kafkaEndpoint" (printf "%q" $kafka))
  (list "egeriaEndpoint" (printf "%q" $self))
  (list "egeriaLocalEndpoint" (printf "%q" (printf "https://localhost:%d" $port)))
  (list "secretsStoreProvider" (printf "%q" "org.odpi.openmetadata.adapters.connectors.secretsstore.yaml.YAMLSecretsStoreProvider"))
  (list "egeriaServersSecretsStore" (printf "%q" "/deployments/secrets/egeria-servers.omsecrets"))
  (list "egeriaServersSecretsCollection" (printf "%q" "EgeriaServers"))
  (list "repositoryDatabaseURL" (printf "%q" (printf "jdbc:postgresql://%s:%d/%s" $pgHost (int $pgPort) (default $d.database $v.postgres.database))))
  (list "repositorySecretCollectionName" (printf "%q" "PostgreSQLRepository"))
  (list "userDirectorySecretsStore" (printf "%q" $d.userDirectoryStore))
  (list "userDirectorySecretsCollectionName" (printf "%q" $d.userDirectoryCollection))
-}}
{{- $lines := list -}}
{{- range $p := $pairs -}}
{{- $lines = append $lines (printf "    %q : %s" (index $p 0) (index $p 1)) -}}
{{- end -}}
{{- $block := printf "platform.placeholder.variables=\\\n  {\\\n%s\\\n  }" (join ",\\\n" $lines) -}}
fullname: {{ $fullname }}
headless: {{ $headless }}
port: {{ $port }}
healthPath: {{ $v.platform.healthPath | quote }}
servers: {{ toJson $servers }}
xtdb: {{ $d.xtdb }}
kafka: {{ $kafka | quote }}
pgHost: {{ $pgHost | quote }}
pgPort: {{ $pgPort }}
cpuLimit: {{ default $d.cpuLimit $v.resources.limits.cpu | quote }}
secretName: {{ default (printf "%s-secrets" $fullname) $v.secrets.existingSecret }}
createSecret: {{ not $v.secrets.existingSecret }}
viewServer: {{ default (index (without (mustRegexFindAll "[a-z-]+-view-server" (join " " $servers) -1) "") 0) $v.canary.viewServer | quote }}
canarySecretName: {{ default (printf "%s-canary" $fullname) $v.canary.existingSecret }}
createCanarySecret: {{ and (not $v.canary.existingSecret) (eq $v.posture "demo") }}
hasCanary: {{ or (not (not $v.canary.existingSecret)) (eq $v.posture "demo") }}
tlsSecretName: {{ default (printf "%s-tls" $fullname) $v.tls.existingSecret }}
createTlsSecret: {{ not $v.tls.existingSecret }}
strictSsl: {{ ternary (eq (toString $v.tls.strictSsl) "true") (eq $v.posture "production") (ne (toString $v.tls.strictSsl) "") }}
placeholderBlock: {{ $block | toJson }}
{{- end -}}

{{/* The same health check compose uses: curl, 200 or 401 counts as healthy. */}}
{{- define "egeria-platform.healthCommand" -}}
- sh
- -c
- >-
  code=$(curl -k -s -o /dev/null -w '%{http_code}' --max-time 10 "https://localhost:{{ .port }}{{ .healthPath }}");
  [ "$code" = 200 ] || [ "$code" = 401 ]
{{- end -}}

{{/* Value of one property line in a properties file: dict "name" "props". */}}
{{- define "egeria-platform.prop" -}}
{{- regexFind (printf "(?m)^%s=.*$" (regexQuoteMeta .name)) .props | trimPrefix (printf "%s=" .name) -}}
{{- end }}

{{/* Image reference: repository:tag, repository@digest, or repository:tag@digest (an empty digest is left out). */}}
{{- define "egeria-platform.image" -}}
{{- $i := .Values.image -}}
{{- if not $i.repository -}}{{- fail "set image.repository" -}}{{- end -}}
{{- if not (or $i.tag $i.digest) -}}{{- fail "set image.tag or image.digest" -}}{{- end -}}
{{- $i.repository -}}{{- if $i.tag -}}:{{ $i.tag }}{{- end -}}{{- if $i.digest -}}@{{ $i.digest }}{{- end -}}
{{- end -}}
