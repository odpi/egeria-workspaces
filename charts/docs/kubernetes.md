# Deploying on Kubernetes

This page covers plain Kubernetes (kind, or any conformant cluster). For OpenShift, read this page for the
concepts, then [openshift.md](openshift.md) for what is different.

All commands run from the repository root. `<release>` is your Helm release name; object names are derived from it
(`<release>-platform`, `<release>-portal`, `<release>-portal-web`, ...), so keep it short (the chart refuses a name
that makes an object name longer than 63 characters).

- [Prerequisites](#prerequisites)
- [Images](#images)
- [Quick start on kind (demo)](#quick-start-on-kind-demo)
- [Production-style install](#production-style-install)
- [Ingress](#ingress)
- [Installing the platform or the Portal alone](#installing-the-platform-or-the-portal-alone)

## Prerequisites

### Tools

| Tool | Versions the charts were tested with |
|---|---|
| Helm | 4 (v4.3.2) and 3 (v3.22.1) |
| kubectl | v1.37.2 |
| kind (for the quick start) | v0.33.0, node image kindest/node v1.37.0 |
| Docker or another image builder | to build the Portal and Apache images |
| openssl | to make a keystore (production) |

Other versions probably work, but these are the ones that ran.

### Cluster size

These figures are the charts' default requests and limits (from each chart's `values.yaml`), added up. They are not
measured minimums.

| Pod | CPU request | Memory request | Memory limit | Storage (PVC) |
|---|---|---|---|---|
| Platform | 1 | 3Gi | 6Gi (quickstart also has a 4-CPU limit) | 20Gi |
| Portal | 250m | 512Mi | 2Gi | 2Gi |
| Apache front door | 50m | 64Mi | 256Mi | none |
| Demo Postgres (demo only) | 200m | 512Mi | 2Gi | 5Gi |
| Demo Kafka (demo only) | 200m | 1536Mi | 2560Mi | none (emptyDir) |
| **Total, demo with bundled Postgres and Kafka** | **1.7** | **about 5.6Gi** | **about 12.8Gi** | **27Gi** |

Plan for the limits, not the requests: the platform's JVM starts with a 2 GB heap (`-Xms2g`) and grows during the
first start. Leave room for the images on the node's disk as well. On OpenShift Local, a 31 GB disk was not enough
(see [openshift.md](openshift.md#openshift-local-sizing)).

You also need a StorageClass that provides `ReadWriteOnce` volumes. For NetworkPolicies to have any effect, your
cluster's network plugin must enforce them.

### PostgreSQL and Kafka for production

The production posture refuses the demo Postgres and Kafka. Bring your own.

**PostgreSQL.** The platform stores its metadata in one database:

- The database is `egeria` (quickstart) or `egeria_freshstart` (freshstart). Override it with `postgres.database`.
- The login role needs all privileges on that database. The role name and password are not chart values; they
  live in the platform Secret, in `egeria-servers.omsecrets`, collection `PostgreSQLRepository`
  (see [Platform Secret](#1-platform-secret-secretsexistingsecret)).
- `charts/egeria-demo-postgres/files/init-egeria-demo.sql` is the minimal set-up the platform needs (roles,
  databases, grants, the `pg_stat_statements` extension in `egeria`). Use it as a reference, with your own passwords.
- The default port is **5442** (the compose shared-infra port), not PostgreSQL's usual 5432. Set `postgres.port`
  for a standard server.

**Kafka.** Set `kafka.bootstrapServers` to `host:port`. You can give a comma-separated list; the platform's start-up
check waits until at least one of them accepts connections. The charts have no values for Kafka TLS or SASL. The tested
Kafka was plaintext with no authentication and automatic topic creation turned on.

The platform pod waits up to 600 seconds for both to accept TCP connections before it starts (init container
`wait-for-dependencies`), so it is fine to install them at the same time.

## Images

| Image | Where it comes from |
|---|---|
| Platform | `docker.io/odpi/egeria-platform:6.3`, pinned by digest in `charts/egeria-platform/values.yaml`. Public; nothing to build. |
| Portal (`portal-quickstart` or `portal-freshstart`) | **Build it yourself.** It is not published. |
| Apache front door (`apache-web`, one image for both environments) | **Build it yourself.** It is not published. |

The Dockerfiles and their rules are in `compose-configs/egeria-quickstart/README-portal-images.md`. The build that the
tests use is in `charts/tests/proof112a.sh`; it is equivalent to:

```bash
cd compose-configs
docker build -f egeria-freshstart/PyegeriaWebHandler/Dockerfile-portal-image -t portal-freshstart:freshstart-6.3-<sha> egeria-freshstart/PyegeriaWebHandler
docker build -f egeria-quickstart/PyegeriaWebHandler/Dockerfile-portal-image -t portal-quickstart:quickstart-6.3-<sha> egeria-quickstart/PyegeriaWebHandler
docker build -f egeria-quickstart/Dockerfile-apache-web-nonroot -t apache-web:6.3-<sha> egeria-quickstart
```

`<sha>` is the short commit you built from (the tag convention, not a requirement). Push the images to a registry
your cluster can pull from.

> **Build from a tree that contains the PO-68 fix** (commit c6aedd12, odpi/egeria-workspaces#907). A Portal image
> built before it hands out its service-user token to anyone, and `helm test` fails on it when the Portal is gated.

**kind:** the tests pushed the images to a local registry container joined to kind's network
(`docker network connect kind <registry>`) and added a `hosts.toml` for it on the node. Do not use `kind load` on a
Docker that uses the containerd image store: it leaves a broken import.

## Quick start on kind (demo)

This is the freshstart demo stack with the bundled Postgres and Kafka, as it ran on kind. It uses the public demo
passwords. Use it only on a cluster you control.

```bash
kind create cluster
helm dependency update charts/egeria-platform
helm dependency update charts/egeria-portal
helm dependency update charts/egeria-stack
helm install st charts/egeria-stack -n egeria --create-namespace \
  -f charts/egeria-stack/values-demo.yaml -f charts/egeria-stack/values-freshstart.yaml \
  --set core.demoPostgres.enabled=true --set core.demoKafka.enabled=true \
  --set core.persistence.storageClassName=standard \
  --set portal.images.portal.repository=<registry>/portal-freshstart --set portal.images.portal.tag=freshstart-6.3-<sha> \
  --set portal.images.apache.repository=<registry>/apache-web --set portal.images.apache.tag=6.3-<sha>
```

Then wait for the platform and verify:

```bash
kubectl -n egeria get pods -w                        # st-platform-0 takes minutes to become Ready
helm test st -n egeria --logs                         # wait for both PASS lines
kubectl -n egeria port-forward svc/st-portal-web 8085:8085
```

Open `http://localhost:8085/portal`. Freshstart has a login gate: sign in with an account from the freshstart user
directory (`charts/egeria-platform/files/freshstart/secrets/egeria-user-directory.omsecrets`).

Notes:

- `standard` is kind's StorageClass. Use your cluster's.
- For **quickstart**, use `values-quickstart.yaml` and the `portal-quickstart` image instead. A quickstart Portal has
  **no login gate**: anyone who reaches it uses Egeria as the Portal's service user. Keep it behind `port-forward`.
- `helm test` passes only once all five servers have started. If it fails because the servers are not active yet,
  run it again (each test waits up to `canary.timeoutSeconds`, 600 by default).

## Production-style install

This is the posture of `charts/tests/kind_stack_prod.sh`, which passed on kind with an external test Postgres and
Kafka. The production posture works only with **freshstart**: the chart refuses a production Portal on quickstart,
because quickstart has no login gate.

What production requires, and the chart refuses to render without:

| Part | Required |
|---|---|
| Platform (`core.` in the stack) | `postgres.host`, `kafka.bootstrapServers`, `secrets.existingSecret`, `tls.existingSecret`, `persistence.storageClassName` (or `persistence.existingClaim`), CPU and memory in both `resources.requests` and `resources.limits` (the default `limits.cpu` is empty, so set it). `canary.existingSecret` is needed for `helm test`. |
| Portal (`portal.` in the stack) | `secrets.existingSecret`, `tls.caSecret`, `canary.existingSecret` (for `helm test`), `images.portal.digest`, `images.apache.digest`, `persistence.storageClassName` (or `persistence.existingClaim`). With an Ingress: `ingress.tlsSecretName`. |

`values-production.yaml` also turns on `networkPolicy.enabled` for both parts and `tls.verify` for the Portal.
It refuses `demoPostgres`, `demoKafka`, `secrets.useDemoFiles`, `tls.strictSsl=false`, `demoMode` and
`allowUngatedPortal`.

Create the namespace and the Secrets first (`kubectl create namespace egeria`). The examples use the namespace
`egeria` and the release `st`.

### 1. Platform Secret (`secrets.existingSecret`)

The keys are file names, mounted at `/deployments/secrets`:

| Environment | Keys |
|---|---|
| freshstart | `egeria-servers.omsecrets`, `egeria-user-directory.omsecrets`, `integration.omsecrets` |
| quickstart | `egeria-servers.omsecrets`, `coco-user-directory.omsecrets`, `integration.omsecrets` |

Start from the tracked files in `charts/egeria-platform/files/<environment>/secrets/` and replace **every** password
in them. They are public. `egeria-servers.omsecrets` holds the PostgreSQL role (`PostgreSQLRepository`); the user
directory holds the Egeria accounts, including the ones the Portal and the canary sign in as.

```bash
kubectl -n egeria create secret generic egeria-secrets --from-file=<directory with your three files>
```

> The live tests used the tracked files unchanged, to prove the wiring. They did not prove a production credential
> set.

### 2. Keystore (`tls.existingSecret`)

The platform serves HTTPS with this keystore. The Secret holds:

| Key | Required | What |
|---|---|---|
| `keystore.p12` | yes | PKCS12 keystore with the server key and certificate |
| `truststore.p12` | yes | PKCS12 truststore |
| `keystore-password`, `truststore-password` | yes | Their passwords. They reach the platform as environment overrides, never through a ConfigMap. |
| `key-alias` | no | The key's alias in the keystore |
| `rsa-key-id` | no | The token-signing key id |
| `ca.crt` | for `helm test` | PEM CA (or the server certificate). The platform test verifies TLS against it and never uses `-k`. |

The certificate must be valid for the names clients use: `<release>-platform`, `<release>-platform.<namespace>.svc.cluster.local`,
and the headless `<release>-platform-hl.<namespace>.svc.cluster.local` (the platform's own servers call it there). If it is
valid for another name only, set `canary.tlsServerName` to that name.

`charts/tests/make_san_keystore.sh` shows how such a keystore is made (a throwaway CA, valid for 3 days, random
passwords). It is a test tool; use your own CA for a real install:

```bash
bash charts/tests/make_san_keystore.sh /tmp/tls egeria st-platform
kubectl -n egeria create secret generic egeria-tls \
  --from-file=/tmp/tls/keystore.p12 --from-file=/tmp/tls/truststore.p12 --from-file=/tmp/tls/ca.crt \
  --from-file=keystore-password=/tmp/tls/keystore-password --from-file=truststore-password=/tmp/tls/truststore-password \
  --from-file=key-alias=/tmp/tls/key-alias
kubectl -n egeria create secret generic egeria-ca --from-file=ca.crt=/tmp/tls/ca.crt
```

**The production posture refuses the public demo keystore password.** If `keystore-password` in this Secret is the
password of the image's built-in demo keystore, `helm install` and `helm upgrade` fail and name the value. This check
uses `lookup`, so it runs only against a real cluster (not under `helm template` or `--dry-run=client`). It sees the
Secret as it is at install or upgrade time, and it reads only `keystore-password`.

With `tls.existingSecret` set, `strict.ssl` is `true` in production. The demo posture defaults it to `false`.

### 3. Portal Secrets

| Secret (value) | Keys |
|---|---|
| `portal.secrets.existingSecret` | `jwt-secret` (signs Portal sessions), `egeria-user-password` (the password of the Portal's Egeria user: `bootstrap` in freshstart, or `portal.egeria.userId`), `mcp-access-token` |
| `portal.tls.caSecret` | `ca.crt`: the CA the platform's certificate chains to. With `tls.verify: true` the Portal checks the platform's certificate against it. |

```bash
kubectl -n egeria create secret generic portal-secrets \
  --from-file=jwt-secret=<file> --from-file=egeria-user-password=<file> --from-file=mcp-access-token=<file>
```

### 4. Canary account (`canary.existingSecret`)

`helm test` signs in as a **non-personal** account, never as a person and never as the Portal's own user. The Secret
has the keys `userId` and `password`. The account must exist in the platform's user directory and be allowed to list
the active servers and read metadata. The tests used `omagspcatnpa` from the tracked user directory.
One Secret can serve both parts (`core.canary.existingSecret` and `portal.canary.existingSecret`).

```bash
kubectl -n egeria create secret generic egeria-canary --from-file=userId=<file> --from-file=password=<file>
```

Pass values by file, as above, so passwords do not land in your shell history.

### 5. Image digests

Production pins the Portal and Apache images by digest and refuses to render without one. Take the digest your
registry reports for the pushed image (for example `docker image inspect <image> --format '{{index .RepoDigests 0}}'`).
The platform image is already pinned in `charts/egeria-platform/values.yaml`; if you override `core.image.repository`
or `core.image.tag`, set `core.image.digest` too.

### 6. Install

```bash
helm install st charts/egeria-stack -n egeria \
  -f charts/egeria-stack/values-production.yaml -f charts/egeria-stack/values-freshstart.yaml \
  --set core.postgres.host=<postgres host> --set core.postgres.port=<port> \
  --set core.kafka.bootstrapServers=<host:port> \
  --set core.secrets.existingSecret=egeria-secrets --set core.tls.existingSecret=egeria-tls \
  --set core.canary.existingSecret=egeria-canary \
  --set core.persistence.storageClassName=<class> --set core.resources.limits.cpu=4 \
  --set portal.secrets.existingSecret=portal-secrets --set portal.tls.caSecret=egeria-ca \
  --set portal.canary.existingSecret=egeria-canary --set portal.persistence.storageClassName=<class> \
  --set portal.images.portal.repository=<registry>/portal-freshstart --set portal.images.portal.tag=freshstart-6.3-<sha> \
  --set portal.images.portal.digest=sha256:<digest> \
  --set portal.images.apache.repository=<registry>/apache-web --set portal.images.apache.tag=6.3-<sha> \
  --set portal.images.apache.digest=sha256:<digest>
helm test st -n egeria --logs
```

For a long list like this, a values file of your own is easier to review than `--set` flags; put it after the two
`-f` files above.

**The Portal and the platform's user directory (freshstart).** The freshstart Portal mounts the platform's
`application.properties` and user directory. By default it looks for `<release>-platform-properties` (a ConfigMap
the platform chart always creates) and `<release>-platform-secrets` (the Secret the platform chart creates **only in
the demo posture**). Both mounts are optional, so with `core.secrets.existingSecret` the Portal starts without the
user directory, with no error. To give it the directory, set `portal.platform.userDirectorySecret` to your platform
Secret (it reads the key `egeria-user-directory.omsecrets`). This setting was not part of the live runs.

### NetworkPolicies

With `networkPolicy.enabled` (on in production):

- **Platform:** only pods in the same namespace labelled `egeria.odpi.org/client: "true"` (the `networkPolicy.clientLabel`
  value), and the platform's own pod, may reach the platform port. The Portal pod and the platform's `helm test` pod
  carry that label. Label any other client (your own tools, a Resource Explorer) the same way.
- **Portal:** the Portal's port 8000 accepts traffic only from its Apache front door and its `helm test` pod. The
  front door itself (8085) is open to anything that can reach its Service; tighten it for your Ingress controller if
  you need to.

The Portal's login gate trusts a header that Apache adds, so a direct path to port 8000 would bypass the gate. That is
why the chart refuses an Ingress without `networkPolicy.enabled`. On kind, a direct request to port 8000 was shown to
be blocked.

Only `Ingress` rules are rendered. Egress is not restricted.

## Ingress

The Ingress always points at the Apache front door, `<release>-portal-web`, port 8085. Apache serves plain HTTP:
TLS ends at the Ingress.

```bash
--set portal.ingress.enabled=true --set portal.ingress.host=egeria.example.com \
--set portal.ingress.className=<your controller's class> --set portal.ingress.tlsSecretName=<tls secret> \
--set portal.networkPolicy.enabled=true
```

| Value | Default | What |
|---|---|---|
| `ingress.enabled` | `false` | Render an Ingress |
| `ingress.host` | `""` | Required when enabled |
| `ingress.className` | `""` | `ingressClassName`; empty means the cluster default |
| `ingress.tlsSecretName` | `""` | A `kubernetes.io/tls` Secret for the host. Required in production. |
| `ingress.annotations` | `{}` | Passed through, for example for your controller or for OpenShift Routes |

The chart refuses an Ingress:

- without `networkPolicy.enabled` (see above);
- on quickstart with `demoMode: false`, because that Portal has no login gate. Use freshstart or `demoMode: true`,
  or, in the demo posture only, set `allowUngatedPortal: true` (NOTES then prints a warning).

Set `portal.siteUrl` to the external URL so links in e-mails are right.

Tested: ingress-nginx v1.15.1 on kind, with the production-style stack: the front door answered through TLS, and a
direct request to the Portal on 8000 was blocked by the NetworkPolicy. On OpenShift, see
[openshift.md — Routes](openshift.md#routes).

## Installing the platform or the Portal alone

The umbrella is the tested and simplest path. The parts also install on their own.

**Platform alone** (demo, with the bundled Postgres and Kafka):

```bash
helm dependency update charts/egeria-platform
helm install egeria charts/egeria-platform -n egeria --create-namespace \
  -f charts/egeria-platform/values-demo.yaml -f charts/egeria-platform/values-demo-infra.yaml \
  --set environment=freshstart
helm test egeria -n egeria          # only "PASS: platform up, servers verified" means ready
```

For production use `-f charts/egeria-platform/values-production.yaml` and the platform values from step 6 without
the `core.` prefix.

**Portal alone**, pointing at a platform release in the same namespace:

```bash
helm dependency update charts/egeria-portal
helm install pq charts/egeria-portal -n egeria -f charts/egeria-portal/values-demo.yaml \
  --set environment=quickstart --set platform.serviceName=<platform release>-platform \
  --set images.portal.repository=<registry>/portal-quickstart --set images.portal.tag=quickstart-6.3-<sha> \
  --set images.apache.repository=<registry>/apache-web --set images.apache.tag=6.3-<sha>
helm test pq -n egeria
```

Outside the umbrella, `platform.serviceName` is required, and the Portal's `environment` must match the platform's.
Inside the umbrella the Portal finds its platform by itself, and the umbrella refuses a `portal.platform.serviceName`
other than `<release>-platform`.
