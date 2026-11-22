# Configuring the charts

- [How values are laid out](#how-values-are-laid-out)
- [Quickstart or freshstart](#quickstart-or-freshstart)
- [Demo or production posture](#demo-or-production-posture)
- [demoMode](#demomode)
- [Values reference](#values-reference): [egeria-stack](#egeria-stack), [egeria-platform](#egeria-platform), [egeria-portal](#egeria-portal), [demo charts](#egeria-demo-postgres-and-egeria-demo-kafka)
- [Resources and probes](#resources-and-probes)
- [Storage](#storage)
- [Images and pull secrets](#images-and-pull-secrets)
- [Scheduling and extra environment](#scheduling-and-extra-environment)

## How values are laid out

Each chart's `values.yaml` holds every default, with a comment. The tables below list the keys a user is expected
to set; the defaults are copied from those files.

The umbrella `egeria-stack` passes values to its parts by prefix:

- `core.<key>` is the `egeria-platform` value `<key>`;
- `portal.<key>` is the `egeria-portal` value `<key>`;
- `global.openshift` reaches both.

A Helm umbrella cannot copy one of its values into a subchart, so a few settings must be given three times. The
shipped values files do this for you:

| File | Sets |
|---|---|
| `egeria-stack/values-quickstart.yaml`, `values-freshstart.yaml` | `environment`, `core.environment`, `portal.environment` |
| `egeria-stack/values-demo.yaml` | `posture`, `core.posture`, `portal.posture` = `demo`, and `core.secrets.useDemoFiles: true` |
| `egeria-stack/values-production.yaml` | `posture`, `core.posture`, `portal.posture` = `production`, NetworkPolicies on for both, `portal.tls.verify: true` |

The umbrella refuses a mismatch in environment or posture, naming the values. Always pass one posture file and one
environment file, then your own values file or `--set` flags.

When you install a part on its own, use that chart's own files: `egeria-platform/values-demo.yaml`,
`values-demo-infra.yaml` (adds the demo Postgres and Kafka) and `values-production.yaml`;
`egeria-portal/values-demo.yaml` and `values-production.yaml`.

Every refusal is a Helm `fail` with a message that names the setting to change.

## Quickstart or freshstart

| | quickstart | freshstart |
|---|---|---|
| What it is | The Coco Pharmaceuticals demo: personas and content | A fresh Egeria with no demo organisation |
| Platform port | 9443 | 8443 |
| Servers | `qs-metadata-store`, `qs-engine-host`, `qs-integration-daemon`, `qs-view-server`, `qs-nanny-daemon` | the same with `fs-` |
| Database (default) | `egeria` | `egeria_freshstart` |
| Organization name | `Coco Pharmaceuticals` | none (`"null"`) |
| User directory file | `coco-user-directory.omsecrets` | `egeria-user-directory.omsecrets` |
| Platform CPU limit (default) | 4 | none |
| Portal's Egeria user | `erinoverview` | `bootstrap` |
| Portal login gate | **None** (`SERVER_MANAGED_AUTH=false`): anyone who reaches the Portal uses Egeria as its service user, unless `demoMode` is on | A sign-in page only (`SERVER_MANAGED_AUTH=true`; `bootstrap` is the Portal admin). **No server-side API gate until PO-78**: a request with no token is answered as the service user |
| Portal image | `portal-quickstart` | `portal-freshstart` |
| Production posture | Platform: allowed. Portal (and so the stack): **refused** | Allowed |
| Ingress (and an OpenShift Route made from it) | Only with `demoMode: true` (or `allowUngatedPortal` in a demo) | **Refused** until PO-78 (no server-side API gate): use `port-forward` |

Each environment's configuration comes from `charts/egeria-platform/files/<environment>/`: `application.properties`,
one configuration document per server under `servers/`, and the demo secrets under `secrets/`. These are copies of
compose's files, checked by `charts/tests/drift_test.py`. Do not edit them to configure an install; use values.

## Demo or production posture

| | demo | production |
|---|---|---|
| Platform secrets | From the tracked public files (`secrets.useDemoFiles`) | `secrets.existingSecret` |
| Platform keystore | The image's built-in demo keystore, its passwords in a chart-made Secret | `tls.existingSecret`; the public demo password is refused |
| `strict.ssl` | `false` (override with `tls.strictSsl`) | `true`; `false` is refused |
| Portal secrets | Chart-made: random `jwt-secret` and `mcp-access-token` (kept across upgrades), public demo Egeria password | `secrets.existingSecret` |
| Portal checks the platform's certificate | No | Yes (`tls.verify`, `tls.caSecret`) |
| Canary account | Chart-made, `omagspcatnpa` from the public files | `canary.existingSecret` |
| Image digests (Portal, Apache) | Optional | Required |
| StorageClass, resource limits | Optional | Required |
| NetworkPolicies | Off | On |
| Demo Postgres and Kafka, `demoMode`, `allowUngatedPortal` | Allowed | Refused |

`tests/render_test.py` checks that the production posture never renders the demo files.

## demoMode

`portal.demoMode: true` turns on the login gate and self-registration of the public Egeria demo sites. It is a Portal
feature (the Portal's `DEMO_MODE`); the chart only sets it. It is what makes a **quickstart** Portal safe to put behind
an Ingress: without it, quickstart has no login at all.

- **Use it** for a public or shared demo of the quickstart content, where visitors register and then pick a Coco
  persona.
- **Never use it** for a real deployment. The chart refuses it in the production posture. Use freshstart for a real
  install: its gate is Egeria's own user directory.

What the chart does **not** do: it creates no Portal accounts. To sign in for the first time you need a bootstrap
admin, which the Portal makes from two environment variables. This is how `charts/tests/crc_stack.sh` did it, with the
password in a Secret so it never appears on a command line:

```bash
openssl rand -hex 12 > /tmp/admin-pw
kubectl -n egeria-demo create secret generic demo-admin --from-file=password=/tmp/admin-pw
cat > demo-values.yaml <<'YAML'
portal:
  demoMode: true
  extraEnv:
    - {name: ADMIN_BOOTSTRAP_EMAIL, value: admin@example.test}
    - {name: ADMIN_BOOTSTRAP_PASSWORD, valueFrom: {secretKeyRef: {name: demo-admin, key: password}}}
YAML
helm upgrade --install qs charts/egeria-stack -n egeria-demo \
  -f charts/egeria-stack/values-demo.yaml -f charts/egeria-stack/values-quickstart.yaml -f demo-values.yaml \
  ...   # Postgres, Kafka and image values as in the demo install
```

The admin signs in at `/login`. The Coco personas (`peterprofile` and the others) are Egeria personas picked after
signing in; they exist in the quickstart metadata, not in the freshstart user directory.

Under `demoMode`, `helm test` sends its token checks to the Portal Service on port 8000 directly, because the Apache
edge header trips the demo gate. The Portal NetworkPolicy admits the test pod for that.

Tested live on OpenShift Local (quickstart, demo posture, with a Route). Not run on kind.

## Values reference

### egeria-stack

| Key | Default | What |
|---|---|---|
| `global.openshift` | `false` | `true` on OpenShift: no fixed UIDs anywhere ([openshift.md](openshift.md)) |
| `global.imagePullSecrets` | `[]` | Pull Secrets for every pod of every part, demo infra and test pods included ([below](#images-and-pull-secrets)) |
| `global.stack` | `true` | Tells the Portal its platform is `<release>-platform`. Do not change. |
| `environment` | `quickstart` | Must equal `core.environment` and `portal.environment`. Use `values-<environment>.yaml`. |
| `posture` | `demo` | Must equal `core.posture` and `portal.posture`. Use `values-<posture>.yaml`. |
| `core.enabled` | `true` | Install the platform |
| `portal.enabled` | `true` | Install the Portal |
| `core.*` | | Any [egeria-platform](#egeria-platform) value |
| `portal.*` | | Any [egeria-portal](#egeria-portal) value. Leave `portal.platform.serviceName` empty. |

### egeria-platform

**Environment and posture**

| Key | Default | What |
|---|---|---|
| `global.openshift` | `false` | No `runAsUser`/`runAsGroup`/`fsGroup` when `true` |
| `global.imagePullSecrets` | `[]` | Pull Secrets for every pod, added to `imagePullSecrets` |
| `environment` | `quickstart` | `quickstart` or `freshstart` |
| `posture` | `demo` | `demo` or `production`; set by `values-demo.yaml` / `values-production.yaml` |
| `replicas` | `1` | Only 1 is accepted |

**Platform**

| Key | Default | What |
|---|---|---|
| `platform.port` | `""` | Empty means 9443 (quickstart) or 8443 (freshstart). Must be 1024 or more. |
| `platform.serverList` | `[]` | Empty means the environment's five servers. Each server needs a configuration document in the chart's `files/<environment>/servers/`. |
| `platform.organizationName` | `""` | Empty means the environment's (`Coco Pharmaceuticals` / none). The string `"null"` means none. |
| `platform.configs.overwrite` | `false` | Server configuration documents are copied into the data volume only when missing, because the admin API rewrites them. `true` overwrites them on every pod start. |
| `platform.healthPath` | `/open-metadata/platform-services/server-platform/origin` | The probes' URL; 200 or 401 counts as healthy |
| `jvm.javaOptsAppend` | G1GC, `-XX:MaxRAMPercentage=60.0`, `-Xms2g`, heap dumps to `/deployments/logs`, ... | `JAVA_OPTS_APPEND`; compose's default |

**Postgres and Kafka**

| Key | Default | What |
|---|---|---|
| `postgres.host` | `""` | Required unless `demoPostgres.enabled` |
| `postgres.port` | `5442` | Ignored when the demo Postgres is used and `postgres.host` is empty |
| `postgres.database` | `""` | Empty means `egeria` / `egeria_freshstart` |
| `kafka.bootstrapServers` | `""` | `host:port` (comma-separated allowed). Required unless `demoKafka.enabled`. |
| `demoPostgres.enabled` | `false` | Demo only. Install the bundled Postgres; `postgres.host` then defaults to it. |
| `demoKafka.enabled` | `false` | Demo only. Install the bundled Kafka; `kafka.bootstrapServers` then defaults to it. |

The Postgres user and password are not values: they are in `egeria-servers.omsecrets` in the platform Secret.

**Secrets and TLS**

| Key | Default | What |
|---|---|---|
| `secrets.existingSecret` | `""` | Secret whose keys are the files for `/deployments/secrets`. Required in production. |
| `secrets.useDemoFiles` | `false` | Demo only; `values-demo.yaml` sets it `true` |
| `tls.existingSecret` | `""` | Keystore Secret ([keys](kubernetes.md#2-keystore-tlsexistingsecret)). Required in production. Empty in demo means the image's demo keystore. |
| `tls.strictSsl` | `""` | Empty means `false` in demo, `true` in production. `false` is refused in production. |

**helm test (canary)**

| Key | Default | What |
|---|---|---|
| `canary.existingSecret` | `""` | Keys `userId`, `password` of a non-personal account. Needed for `helm test` in production. |
| `canary.demoUserId` | `omagspcatnpa` | Demo only: the account taken from the tracked user directory |
| `canary.tlsServerName` | `""` | The name the platform certificate is valid for, if not the Service name |
| `canary.timeoutSeconds` | `600` | How long each test step keeps retrying |
| `canary.viewServer` | `""` | Empty means the environment's `*-view-server` |
| `canary.guid`, `canary.name` | `2648e33f-...`, `Egeria:IntegrationGroup:Default` | The element the test reads (from the core content pack) |

**Image**

| Key | Default | What |
|---|---|---|
| `image.repository` | `docker.io/odpi/egeria-platform` | |
| `image.tag` | `"6.3"` | |
| `image.digest` | `sha256:483726b6...ebda29c` | The reference is `repository:tag@digest`; with an empty digest it is `repository:tag`, with an empty tag `repository@digest`. One of the two is required. |
| `image.pullPolicy` | `IfNotPresent` | |

**Resources, probes, storage and network**

| Key | Default | What |
|---|---|---|
| `resources.requests` | `cpu: "1"`, `memory: 3Gi` | |
| `resources.limits.cpu` | `""` | Empty means 4 (quickstart) or none (freshstart). Required in production. |
| `resources.limits.memory` | `6Gi` | |
| `probes.startup` | period 10, failures 60, timeout 15 | failureThreshold × periodSeconds must be at least 600 |
| `probes.readiness` | period 15, failures 4, timeout 15 | |
| `probes.liveness` | period 30, failures 10, timeout 15 | |
| `persistence.size` | `20Gi` | One PVC with subPaths `data`, `logs`, `security-logs` |
| `persistence.storageClassName` | `""` | Required in production (or `existingClaim`) |
| `persistence.existingClaim` | `""` | Use an existing PVC instead of the StatefulSet's claim |
| `exchange.<name>` | `{enabled: false, existingClaim: "", size: 5Gi}` | Optional folders mounted at `/deployments/<name>`: `landing-area`, `distribution-hub`, `surveys`, `loading-bay`, `coco-data-lake`, `treasury-dts-history`, `work` |
| `securityContext` | `runAsUser: 185`, `runAsGroup: 0`, `fsGroup: 0` | Ignored when `global.openshift` is `true` |
| `networkPolicy.enabled` | `false` | `values-production.yaml` sets `true` |
| `networkPolicy.clientLabel` | `egeria.odpi.org/client` | Pods labelled `<clientLabel>: "true"` may reach the platform |
| `serviceAccountName` | `""` | An existing ServiceAccount for the platform pod and its test pod; the chart creates none. Empty means the namespace's `default`. |
| `imagePullSecrets` | `[]` | Pull Secrets (names or `{name: ...}`) for the platform pod and its test pod |
| `nodeSelector`, `tolerations`, `affinity` | `{}`, `[]`, `{}` | Passed to the pod |

### egeria-portal

**Environment, posture and platform**

| Key | Default | What |
|---|---|---|
| `global.openshift` | `false` | No `runAsUser`/`runAsGroup`/`fsGroup` when `true` |
| `global.imagePullSecrets` | `[]` | Pull Secrets for every pod, added to `imagePullSecrets` |
| `environment` | `quickstart` | Must match the platform's. Production requires `freshstart`. |
| `posture` | `demo` | |
| `replicas` | `1` | Only 1 is accepted |
| `platform.serviceName` | `""` | Required outside the umbrella: the platform release's Service, `<release>-platform` |
| `platform.port` | `""` | Empty means 9443 / 8443 |
| `platform.viewServer` | `""` | Empty means `qs-view-server` / `fs-view-server` |
| `platform.propertiesConfigMap` | `""` | Freshstart only. Empty means `<platform.serviceName>-properties`. Optional mount. |
| `platform.userDirectorySecret` | `""` | Freshstart only. The Secret with the key `egeria-user-directory.omsecrets`, usually the platform's `secrets.existingSecret`. **Required in a production freshstart Portal** (the chart refuses without it). In demo, empty means `<platform.serviceName>-secrets`, the platform chart's demo Secret. |
| `egeria.userId` | `""` | Empty means `erinoverview` / `bootstrap` |

**Login and site**

| Key | Default | What |
|---|---|---|
| `trustedProxies` | `""` | `PORTAL_TRUSTED_PROXIES` (PO-83): the peers whose `X-Forwarded-For` the Portal believes, so its auth rate limits count per real client IP. Comma-separated IPs, CIDRs and hostnames, re-resolved every 60 s. Empty means the chart's headless Service for the Apache pods (`<release>-portal-web-hl.<namespace>.svc.cluster.local`): the Portal's peer is the Apache pod, whose IP no template can know. Setting it **replaces** that default. Never `0.0.0.0/0`: a NetworkPolicy gap would become a rate-limit bypass. A new Apache pod is untrusted for up to 60 s after a rollout, which falls back safely to one shared budget. Another cluster domain than `cluster.local`? Set it here. |
| `demoMode` | `false` | [demoMode](#demomode). Refused in production. |
| `allowUngatedPortal` | `false` | Allows an Ingress on a quickstart Portal without `demoMode`. Demo only; NOTES warns. |
| `siteUrl` | `""` | `SITE_URL`: the external URL, for links in e-mails |
| `extraEnv` | `[]` | Extra container env entries ([below](#scheduling-and-extra-environment)) |

**Secrets and TLS**

| Key | Default | What |
|---|---|---|
| `secrets.existingSecret` | `""` | Keys `jwt-secret`, `egeria-user-password`, `mcp-access-token`. Required in production. |
| `tls.verify` | `false` | Check the platform's certificate. `values-production.yaml` sets `true`; `false` is refused in production. |
| `tls.caSecret` | `""` | Secret with `ca.crt` to verify against. Required when `tls.verify` is `true` in production. |
| `canary.existingSecret` | `""` | Keys `userId`, `password`. Needed for `helm test` in production. |

**Images**

| Key | Default | What |
|---|---|---|
| `images.portal.repository`, `images.portal.tag` | `""` | Required. `portal-quickstart` or `portal-freshstart`. |
| `images.portal.digest` | `""` | Required in production |
| `images.apache.repository`, `images.apache.tag` | `""` | Required. `apache-web`. |
| `images.apache.digest` | `""` | Required in production |
| `images.*.pullPolicy` | `IfNotPresent` | |

**Ingress and network**

| Key | Default | What |
|---|---|---|
| `ingress.enabled` | `false` | [Ingress](kubernetes.md#ingress) |
| `ingress.host` | `""` | Required when enabled |
| `ingress.className` | `""` | |
| `ingress.tlsSecretName` | `""` | Required in production with an Ingress |
| `ingress.annotations` | `{}` | For example `route.openshift.io/termination: edge` |
| `networkPolicy.enabled` | `false` | Required with an Ingress; `values-production.yaml` sets `true` |
| `networkPolicy.platformClientLabel` | `egeria.odpi.org/client` | Label put on the Portal pod; must match the platform's `networkPolicy.clientLabel` |

**Resources, storage and scheduling**

| Key | Default | What |
|---|---|---|
| `resources.portal` | requests `cpu: 250m`, `memory: 512Mi`; limits `memory: 2Gi` | |
| `resources.apache` | requests `cpu: 50m`, `memory: 64Mi`; limits `memory: 256Mi` | |
| `persistence.size` | `2Gi` | One PVC: Portal state, demo-data (sqlite), Dr.Egeria inbox and outbox |
| `persistence.storageClassName` | `""` | Required in production (or `existingClaim`) |
| `persistence.existingClaim` | `""` | |
| `content.<name>.existingClaim` | `""` | `config`, `work`, `cocoWorkbooks`, `designPatterns`, `templates`, `cocoDags`. An existing PVC; empty means an empty directory. |
| `exchange.<name>.existingClaim` | `""` | `loadingBay`, `landingArea`, `cocoDataLake`, `distributionHub`, `treasuryDtsHistory`: the platform's exchange claims, mounted read-only |
| `securityContext` | `runAsUser: 1001`, `runAsGroup: 0`, `fsGroup: 0` | Ignored when `global.openshift` is `true` |
| `probes.portal.startup` | `periodSeconds: 10`, `failureThreshold: 60` | Timings of the Portal's `GET /` probes ([Resources and probes](#resources-and-probes)) |
| `probes.portal.readiness` | `periodSeconds: 10`, `timeoutSeconds: 5`, `failureThreshold: 3` | |
| `probes.portal.liveness` | `periodSeconds: 30`, `timeoutSeconds: 10`, `failureThreshold: 5` | |
| `probes.apache.readiness` | `periodSeconds: 10` | Timings of Apache's TCP probes on 8085 |
| `probes.apache.liveness` | `periodSeconds: 30`, `failureThreshold: 5` | |
| `serviceAccountName` | `""` | An existing ServiceAccount for the Portal, Apache and test pods; the chart creates none |
| `imagePullSecrets` | `[]` | Pull Secrets (names or `{name: ...}`) for the Portal, Apache and test pods |
| `nodeSelector`, `tolerations`, `affinity` | `{}`, `[]`, `{}` | Applied to both the Portal pod and the Apache pod |

### egeria-demo-postgres and egeria-demo-kafka

Demo only. As subcharts of the platform, set them under `demoPostgres.` and `demoKafka.` (in the umbrella,
`core.demoPostgres.` and `core.demoKafka.`).

| Key | Default | What |
|---|---|---|
| `demoPostgres.image` | `pgvector/pgvector:pg17` | |
| `demoPostgres.persistence.enabled` | `true` | `false` means an emptyDir: data is lost when the pod moves |
| `demoPostgres.persistence.size` | `5Gi` | |
| `demoPostgres.persistence.storageClassName` | `""` | |
| `demoPostgres.resources` | requests `200m` / `512Mi`, limits `memory: 2Gi` | |
| `demoPostgres.initJob.enabled` | `true` | A post-install and post-upgrade Job that creates missing roles and databases (never drops) |
| `demoPostgres.securityContext` | UID, GID and fsGroup `999` | Fixed: not supported on OpenShift |
| `demoKafka.image` | `cleanstart/kafka`, pinned by digest | |
| `demoKafka.retention` | `hours: "24"`, `bytes: "536870912"`, `segmentBytes: "107374182"` | Same as compose |
| `demoKafka.heap` | `-Xmx1G -Xms1G` | |
| `demoKafka.resources` | requests `200m` / `1536Mi`, limits `memory: 2560Mi` | |
| `demoPostgres.serviceAccountName`, `demoKafka.serviceAccountName` | `""` | An existing ServiceAccount (the Postgres one also runs its set-up Job) |
| `demoPostgres.imagePullSecrets`, `demoKafka.imagePullSecrets` | `[]` | Added to `global.imagePullSecrets` |

Postgres listens on 5442 and Kafka on 9192, as in compose. Both use the public demo passwords.

## Resources and probes

**Platform.** Requests and limits are values. In production all four (CPU and memory, request and limit) are
required; the empty default `limits.cpu` makes you choose. The JVM sizes its heap from the memory limit
(`-XX:MaxRAMPercentage=60.0`), so raise `resources.limits.memory` rather than adding `-Xmx`.

The three platform probes run the same check as compose: `curl` to `https://localhost:<port><healthPath>`, where 200
or 401 counts as healthy. The startup probe must allow at least 600 seconds (failureThreshold × periodSeconds); the
chart refuses less, because the first start loads content packs. On a slow cluster raise
`probes.startup.failureThreshold`.

A Ready platform pod means the platform process answers. It does not mean the servers are up; that is what
`helm test` proves.

**Portal and Apache.** Their requests and limits are values (`resources.portal`, `resources.apache`), and so are their
probe timings (`probes.portal.*`, `probes.apache.*`; the defaults are the numbers the live runs used). The checks
themselves are fixed: the Portal's startup, readiness and liveness probes are a plain `GET /`, on purpose (an Egeria
outage must not turn into a 503 at the Ingress, and a probe must not mint tokens), and Apache's are TCP checks on 8085.
Only `initialDelaySeconds`, `periodSeconds`, `timeoutSeconds`, `failureThreshold` and `successThreshold` may be set;
the chart refuses any other key. For example, to give a slow node more time:
`--set portal.probes.portal.startup.failureThreshold=120`. Overriding them is render-tested only (TR-123), not yet run on a cluster.

## Storage

| Volume | Made by | Default size | Kept on `helm uninstall`? |
|---|---|---|---|
| Platform data (`data` claim of the StatefulSet, `data-<release>-platform-0`) | StatefulSet `volumeClaimTemplates`, or `persistence.existingClaim` | 20Gi | Yes (Kubernetes keeps StatefulSet claims) |
| Platform exchange folders (`exchange.<name>`) | The chart, when enabled without `existingClaim` | 5Gi each | No |
| Portal data (`<release>-portal-data`) | The chart, or `persistence.existingClaim` | 2Gi | Yes (`helm.sh/resource-policy: keep`) |
| Demo Postgres | Its StatefulSet | 5Gi | Yes |

All claims are `ReadWriteOnce`. The Portal uses one volume with sub-directories, and its Deployment uses the
`Recreate` strategy so two pods never write it at once.

The size of a StatefulSet claim cannot be changed by `helm upgrade` (Kubernetes refuses changes to
`volumeClaimTemplates`). Pick `persistence.size` before the first install, or use `persistence.existingClaim` with a
claim you manage yourself.

The Portal's content directories (`content.*`) and the read-only exchange folders (`exchange.*`) are empty
directories unless you point them at existing claims. To share the platform's exchange folders with the Portal, turn
them on in the platform (`core.exchange.loading-bay.enabled: true`, ...) and give their claim names
(`<release>-platform-<name>`) to the Portal (`portal.exchange.loadingBay.existingClaim`, ...). As `ReadWriteOnce`
claims, two pods can share them only on one node. This sharing was not part of the live runs.

## Images and pull secrets

| Value | Image |
|---|---|
| `core.image.*` | Platform; pinned by digest by default |
| `portal.images.portal.*` | Portal: `portal-quickstart` or `portal-freshstart`, built by you |
| `portal.images.apache.*` | Apache front door: `apache-web`, built by you. The Portal's `helm test` pod also uses it. |

Building them: [kubernetes.md — Images](kubernetes.md#images). Production requires a digest for the Portal and
Apache images; set the platform's digest whenever you change its repository or tag.

**Private registry.** Create a pull Secret and name it in `imagePullSecrets`. In the umbrella, `global.imagePullSecrets`
reaches every pod at once: the platform, the Portal, Apache, both test pods, and the demo Postgres (with its set-up Job)
and Kafka. Each chart's own `imagePullSecrets` is added to the global list for that chart's pods only. An entry is a
Secret name or `{name: ...}`.

```bash
kubectl -n egeria create secret generic regcred --type=kubernetes.io/dockerconfigjson --from-file=.dockerconfigjson=<path to a docker config.json>
helm install st charts/egeria-stack ... --set 'global.imagePullSecrets[0]=regcred'
```

**ServiceAccounts.** By default pods use the namespace's `default` ServiceAccount. `serviceAccountName` (per chart:
`core.serviceAccountName`, `portal.serviceAccountName`, `core.demoPostgres.serviceAccountName`,
`core.demoKafka.serviceAccountName`) names an existing one for that chart's pods, test pods included. The charts never
create a ServiceAccount. On OpenShift the ServiceAccount also decides which SCCs a pod may use; keep the Egeria ones
under `restricted-v2`.

Render-tested only (TR-123); not yet run on a cluster. The live runs used a local registry (kind) or the internal registry (OpenShift), with no pull
Secret.

## Scheduling and extra environment

`nodeSelector`, `tolerations` and `affinity` exist in both the platform and the Portal chart. In the Portal chart all
three apply to both the Portal pod and the Apache front door's pod (tolerations and affinity on Apache are new in
TR-123: render-tested only).

`portal.extraEnv` adds container environment entries to the Portal, in Kubernetes `env` form (`value` or
`valueFrom`). The chart refuses names it owns: `EGERIA_ROOT_PATH`, `EGERIA_INBOX_PATH`, `EGERIA_OUTBOX_PATH`,
`DEMO_MODE`, `SERVER_MANAGED_AUTH`, `JWT_SECRET`, `EGERIA_USER_PASSWORD`, `MCP_ACCESS_TOKEN`, `EGERIA_USER`,
`PORTAL_ALLOWED_PLATFORM_URLS` and `EGERIA_PLATFORM_URL`. Set the matching value instead. The platform chart has
no `extraEnv`.
