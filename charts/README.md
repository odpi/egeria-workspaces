# Egeria Helm charts (TR-112, phase 1)

Helm charts for the Egeria 6 OMAG Server Platform. **Compose stays the source of truth**: the charts are
additive, nothing under `compose-configs/` is changed, and `tests/drift_test.py` fails if the chart and
compose disagree.

| Chart | What it is |
|---|---|
| `egeria-common/` | Library chart: names, labels, pod and container security contexts (`global.openshift`). |
| `egeria-platform/` | One OMAG platform, one replica (the chart refuses more), for the `quickstart` or the `freshstart` environment. |
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

## Secrets

* `secrets.existingSecret`: a Secret whose keys are the file names mounted at `/deployments/secrets` (`egeria-servers.omsecrets`, ...).
* `tls.existingSecret` (required in production): `keystore.p12`, `truststore.p12`, `keystore-password`, `truststore-password`, optional `key-alias`, `rsa-key-id`.
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

`kind_install.sh` expects a running kind cluster and, with `MODE=production`, `KEYSTORE_POD=<namespace>/<pod>` (the image's own
keystore is copied out of a running platform pod to build the TLS Secret). Do not preload images with `kind load`
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
* Phase 1 covers the platform only. The Portal, Resource Explorer and Egeria Advisor charts, and the OpenShift run, are later phases.
