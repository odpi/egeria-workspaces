# Egeria Helm charts (TR-112, phases 1 and 2)

Helm charts for the Egeria 6 OMAG Server Platform. **Compose stays the source of truth**: the charts are
additive, nothing under `compose-configs/` is changed, and `tests/drift_test.py` fails if the chart and
compose disagree.

| Chart | What it is |
|---|---|
| `egeria-common/` | Library chart: names, labels, pod and container security contexts (`global.openshift`). |
| `egeria-platform/` | One OMAG platform, one replica (the chart refuses more), for the `quickstart` or the `freshstart` environment. |
| `egeria-stack/` | Umbrella: the platform (alias `core`) and the Portal (alias `portal`) as one release, so one `helm install` and one `helm test` for both. |
| `egeria-portal/` | The Portal: pyegeria-web (one pod) behind an Apache front door (Phase 2). Images from `compose-configs/egeria-quickstart/README-portal-images.md`. |
| `egeria-demo-postgres/` | **Demo only.** One PostgreSQL pod and an idempotent set-up Job (creates only, never drops). |
| `egeria-demo-kafka/` | **Demo only.** One single-node Kafka (KRaft), no persistence. |

## Install

Demo, with the bundled Postgres and Kafka:

```bash
helm dependency update charts/egeria-platform
helm install egeria charts/egeria-platform -n egeria --create-namespace \
  -f charts/egeria-platform/values-demo.yaml -f charts/egeria-platform/values-demo-infra.yaml \
  --set environment=quickstart          # or freshstart
helm test egeria -n egeria              # only "PASS: platform up, servers verified" means ready
```

Production-style posture (your own Postgres and Kafka, your own Secrets):

```bash
helm install egeria charts/egeria-platform -n egeria -f charts/egeria-platform/values-production.yaml \
  --set environment=freshstart --set postgres.host=... --set kafka.bootstrapServers=... \
  --set secrets.existingSecret=... --set tls.existingSecret=... --set canary.existingSecret=... \
  --set persistence.storageClassName=... --set resources.limits.cpu=4
```

The chart refuses to render, naming the setting, when something required is missing (see `egeria-platform/templates/_helpers.tpl`).

## Portal (Phase 2)

```bash
helm dependency update charts/egeria-portal
helm install pq charts/egeria-portal -n egeria -f charts/egeria-portal/values-demo.yaml \
  --set environment=quickstart --set platform.serviceName=<platform release>-platform \
  --set images.portal.repository=<registry>/portal-quickstart --set images.portal.tag=quickstart-6.3-<sha> \
  --set images.apache.repository=<registry>/apache-web --set images.apache.tag=6.3-<sha>
helm test pq -n egeria      # a real Egeria call through the front door; only the PASS line means ready
kubectl -n egeria port-forward svc/pq-portal-web 8085:8085
```

* One Portal pod (state is files and sqlite on one volume, strategy Recreate) and one Apache front door. The front door serves plain HTTP
  on 8085: TLS ends at the Ingress (`ingress.enabled`, `ingress.host`, `ingress.tlsSecretName`).
* `httpd.conf` and the proxy routes are compose's, copied into `files/` by `tests/gen_portal_conf.py` and checked by `drift_test.py`;
  the vhost is the chart's. Routes to services this chart does not deploy (My Profile, Trellis) stay in the config and answer 503.
* `EGERIA_ROOT_PATH` is `/app/dr-egeria`, never compose's `/` (a non-root user cannot write there); `portal_render_test.py` checks it.
* **Readiness is a plain `GET /`**, like liveness and startup: an Egeria outage must not become a 503 at the Ingress, and a probe must not
  mint tokens. Egeria reachability is proven by `helm test`, which signs in as a non-personal canary account (`canary.existingSecret`,
  keys `userId` and `password`; the demo posture makes one from the tracked files) through the front door. The Portal heals Egeria content
  itself; nothing in Helm hooks.
* **Login gate:** `SERVER_MANAGED_AUTH` is set explicitly (true for freshstart, false for quickstart). The chart refuses production with
  quickstart (no gate there), refuses an Ingress with quickstart and `demoMode=false` (an ungated Portal) unless `allowUngatedPortal=true`
  (demo only; NOTES warns), and refuses an Ingress without `networkPolicy.enabled`: the gate trusts the edge header Apache adds, so the
  Portal Service on 8000 must be reachable only from the front door. The Ingress backend is always `<release>-portal-web`.
* `extraEnv` may not set names the chart owns (`EGERIA_ROOT_PATH`, `DEMO_MODE`, `SERVER_MANAGED_AUTH`, passwords, ...).
* PO-68 (Portal, HIGH): `POST /api/egeria-token` with an empty body minted the Portal's service-user token for any caller. It is fixed upstream
  (odpi/egeria-workspaces#907, c6aedd12), but the Portal images these charts were tested with (built from a79109b7) PREDATE that fix and still have
  the bug. Rebuild the Portal image from a tree that contains c6aedd12 before publishing a chart Ingress; then the canary should also assert that
  `{}` without a session gets 401.
* Demo posture creates a Secret (random `jwt-secret` and `mcp-access-token`, kept across upgrades; the public demo Egeria password).
  Production needs `secrets.existingSecret` (keys `jwt-secret`, `egeria-user-password`, `mcp-access-token`), `tls.caSecret` (key `ca.crt`),
  image digests, a StorageClass, and refuses `demoMode`.
* Freshstart mounts the platform release's `<service>-properties` ConfigMap and `<service>-secrets` Secret (optional; override with
  `platform.propertiesConfigMap`, `platform.userDirectorySecret`).
* Proven on kind (Helm 4): quickstart as UID 1001 then switched to 1000680000:0 on the same volume, and freshstart as 1000680000:0,
  both passing `helm test`. Production-style install: see the umbrella section. Not run: OpenShift, the optional content claims, demoMode.
* Images reach kind through a local registry: `docker network connect kind <registry>`, and a `hosts.toml` for it on the node (see the session notes);
  do not use `kind load` with the containerd image store.

## Umbrella (Phase 2)

```bash
helm dependency update charts/egeria-platform; helm dependency update charts/egeria-portal; helm dependency update charts/egeria-stack
helm install st charts/egeria-stack -n egeria --create-namespace -f charts/egeria-stack/values-demo.yaml -f charts/egeria-stack/values-freshstart.yaml \
  --set core.demoPostgres.enabled=true --set core.demoKafka.enabled=true --set core.persistence.storageClassName=standard \
  --set portal.images.portal.repository=<registry>/portal-freshstart --set portal.images.portal.tag=freshstart-6.3-<sha> \
  --set portal.images.apache.repository=<registry>/apache-web --set portal.images.apache.tag=6.3-<sha>
helm test st -n egeria      # both canaries
```

* Each part's values go under `core:` and `portal:` and are that chart's own values. The environment must be set for all three
  (`environment`, `core.environment`, `portal.environment`); `values-quickstart.yaml` and `values-freshstart.yaml` do it, and the chart refuses a mismatch,
  differing postures, or a `portal.platform.serviceName` that is not `<release>-platform` (inside the stack the Portal finds its platform by itself).
* Proven on kind (Helm 4):
  * freshstart demo with the bundled Postgres and Kafka: both canaries pass.
  * **Production-style** (`tests/kind_stack_prod.sh <namespace> [release]`): external test Postgres and Kafka, a keystore of our own made by
    `tests/make_san_keystore.sh` (random passwords, SANs for the Service names, so `strict.ssl=true` and the Portal's `tls.verify=true` check
    hostnames), existing Secrets, image digests, NetworkPolicies; both canaries pass.
  * **Ingress** (ingress-nginx v1.15.1 on kind): the front door answers through TLS and a direct request to the Portal on 8000 is blocked by
    the NetworkPolicy. It also showed PO-68: an empty-body `POST /api/egeria-token` through the Ingress returns a token (that image predates the
    upstream fix c6aedd12), so do not publish a Portal Ingress with an image built before it.
  * **OpenShift Local (crc 2.65.0, OpenShift 5.0.0)** (`tests/crc_stack.sh`): freshstart demo stack with `global.openshift=true`; the platform,
    the Portal and Apache were admitted under **restricted-v2** with an assigned UID (here 1000670000), GID 0 and no `runAsUser`/`fsGroup` in
    our manifests; both canaries pass. The test Postgres and Kafka run as fixed UIDs, so they are in a separate namespace with the `anyuid` SCC
    (the demo Postgres chart is not supported on OpenShift). The VM needs more than crc's defaults (20 GB RAM, 8 CPUs, 70 GB disk: the default
    31 GB disk reached kubelet disk-pressure and stopped scheduling the test pod). Images were loaded into the node over SSH (`podman load`).
  * **Production-style on OpenShift Local** (`tests/crc_stack_prod.sh`): the kind production posture (own SAN keystore with random passwords,
    existing Secrets, `tls.verify`, NetworkPolicies, images pinned by digest) with `global.openshift=true`. The images are pushed to the cluster's
    internal registry so the digests are real registry digests. All three pods ran under **restricted-v2** (UID 1000680000, GID 0), 5/5 servers
    started and both canaries passed. The test infrastructure is in `<namespace>-infra` under `anyuid`, as above.
  * **Re-run with the PO-68 fix:** the Portal image rebuilt from this branch plus c6aedd12 (`freshstart-6.3-c6aedd12`, merged in a throwaway
    worktree, the branch itself is unchanged) passed both canaries again, and `{}` posted to `/api/egeria-token` without a session now returns 401.
    A wrong password still returns 500 (not changed by that fix). `crc_stack_prod.sh` keeps the first run's Secrets on a re-run: a new random CA
    would not match the keystore a running platform already loaded (the platform canary then hangs on TLS verification).
  * **Portal canary: PO-68 check.** On a gated Portal (freshstart, or demoMode) the canary also posts `{}` with no session and requires 401. On OpenShift
    it passes with the image built with c6aedd12 and FAILS (HTTP 200) with the a79109b7 image, so it catches a Portal image that predates the fix.
  * Not run: demoMode, Ingress/Route on OpenShift.
* **Public demo keystore password:** when `tls.existingSecret` holds the public demo password (the image's own keystore), the demo posture prints a
  WARNING in NOTES, and the **production posture refuses to install or upgrade** (`fail`, naming `tls.existingSecret`), in the platform chart and in the
  umbrella (`core.tls.existingSecret`). Both use `lookup`, so they act only against a real cluster (not `helm template` or `--dry-run=client`);
  proven on kind with `--dry-run=server`. Two limits: `lookup` sees only a Secret that exists at install or upgrade time (a Secret created or
  changed later is not checked until the next `helm upgrade`), and the check reads only the `keystore-password` key (a demo `truststore-password`
  or a keystore that was re-encrypted elsewhere is not recognised). `egeria-stack/files/demo-keystore-password` is that public demo value, kept only so the chart can recognise it
  (`drift_test.py` checks it against the properties files; `stack_render_test.py` checks it never appears in a production manifest, and in a demo
  one only inside the platform's demo TLS Secret).

## Secrets

* `secrets.existingSecret`: a Secret whose keys are the file names mounted at `/deployments/secrets` (`egeria-servers.omsecrets`, ...).
* `tls.existingSecret` (required in production): `keystore.p12`, `truststore.p12`, `keystore-password`, `truststore-password`, optional `key-alias`, `rsa-key-id`, and `ca.crt` (PEM CA or server certificate, required for `helm test` in production, which verifies TLS and never uses `-k`; set `canary.tlsServerName` if the certificate is not valid for the Service name).
  TLS passwords never appear in a ConfigMap; they reach the platform as environment overrides from this Secret.
  `strict.ssl` is `true` in production, and `tls.strictSsl=false` is refused there.
* `canary.existingSecret` (needed for `helm test` in production): keys `userId` and `password` of a non-personal account that may list active servers and read metadata.
* The demo posture builds all three from the tracked **public** demo files. The production posture never renders them (`tests/render_test.py` checks this).

## Tests

```bash
export PATH=$HOME/.local/bin:$PATH
python3 charts/tests/render_test.py                 # render tests, no cluster needed
python3 charts/tests/drift_test.py                  # compose <-> chart drift
ct lint --config charts/ct.yaml --all               # chart-testing lint
HELM=helm3 python3 charts/tests/render_test.py      # the same on Helm 3 (also drift_test.py)
bash charts/tests/kind_install.sh freshstart fs-one            # kind install; MODE=production, BUNDLED=1, HELM=helm3 supported
```

`kind_install.sh` expects a running kind cluster. With `MODE=production` it makes a keystore of its own (`make_san_keystore.sh`: random
passwords, SANs for the Service names). Do not preload images with `kind load`
on a Docker that uses the containerd image store: it leaves a broken import. Let the nodes pull the public images.

## Tool versions used (installed user-local in `~/.local/bin`, Python tools in a venv)

| Tool | Version | SHA-256 of the downloaded file |
|---|---|---|
| kubectl | v1.37.2 | `c04487523e7aa7d1493f7808174c899db93d7a9cf57531420cd76b9bd415f8f4` (binary) |
| kind | v0.33.0 | `aee6151561422756b764a4ae28e7f44cda5af5a9eead3cc9985112b1de8d8e0d` (binary) |
| helm (4) | v4.3.2 | `d1c0278d46beab79582d7e50f5b3dc206944ba8e577cde618513fd07daa53983` (`helm-v4.3.2-linux-amd64.tar.gz`) |
| helm3 | v3.22.1 | `896cf63684a42a723d61c980369d6e588330927deb13676ca0d85006dd6da0ea` (`helm-v3.22.1-linux-amd64.tar.gz`) |
| chart-testing (ct) | v3.15.0 | `467561730f25fe09d5e6cd09a3e1f6aa759871c657a57602947c716d9be2c583` (`chart-testing_3.15.0_linux_amd64.tar.gz`) |
| yamale | 6.1.0 | `7e109c9d83e3a7e42703516cb2b70b9c7aa5b7a738019c4a6c202b6b0b9096c5` (wheel) |
| yamllint | 1.38.0 | `fc394a5b3be980a4062607b8fdddc0843f4fa394152b6da21722f5d59013c220` (wheel) |
| kind node image | kindest/node v1.37.0 | kind's default for v0.33.0 (pulled by kind; digest not recorded) |

The platform image is `docker.io/odpi/egeria-platform:6.3@sha256:483726b69b9e789749995d114633eeeab0f70a9c26ec5e59ae0e3d300ebda29c`
(the same image as the compose Dockerfiles; the drift test compares them). It runs as uid 185, gid 0.
On OpenShift set `global.openshift=true`: no `runAsUser`, `runAsGroup` or `fsGroup` is rendered, so restricted-v2 assigns the UID (GID 0).
The demo Postgres needs uid 999 and is not supported there: use your own database.

## Known limits

* Readiness: a Ready pod means the platform process answers (200 or 401 on the origin endpoint, as in compose). The servers load
  content packs for a few more minutes. `helm test` is what proves the servers are up.
* The demo Postgres and Kafka are not tuned like compose's shared-infra and have no backups or high availability.
* The umbrella chart, Resource Explorer and Egeria Advisor charts, and the OpenShift run are later phases.
