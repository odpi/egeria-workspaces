# Egeria Helm charts

Helm charts that deploy the Egeria 6 OMAG Server Platform and the Egeria Portal on Kubernetes and on OpenShift.

The charts mirror the compose environments in `compose-configs/`. Compose stays the source of truth:
the charts copy its configuration, and `tests/drift_test.py` fails if the two drift apart.

## What's in the box

| Chart | What it is | Use it for |
|---|---|---|
| `egeria-stack/` | Umbrella chart. It installs the platform (alias `core`) and the Portal (alias `portal`) as one release, so one `helm install` and one `helm test` cover both. | **Start here.** Most installs. |
| `egeria-platform/` | One OMAG Server Platform, one replica (the chart refuses more). It runs the five servers of the `quickstart` or the `freshstart` environment. | Egeria without the Portal, or a platform that a separately installed Portal uses. |
| `egeria-portal/` | The Portal: pyegeria-web (one pod) behind an Apache front door. | A Portal installed separately from its platform. |
| `egeria-common/` | Library chart: names, labels, and pod and container security contexts (`global.openshift`). It installs nothing by itself. | Used by the others. |
| `egeria-demo-postgres/` | **Demo and test only.** One PostgreSQL pod and an idempotent set-up Job (it creates, never drops). Not supported on OpenShift. | Trying the platform chart on a laptop cluster. |
| `egeria-demo-kafka/` | **Demo and test only.** One single-node Kafka (KRaft), with no persistence, TLS or auth. | Trying the platform chart on a laptop cluster. |

The two demo charts are subcharts of `egeria-platform` (aliases `demoPostgres` and `demoKafka`, both off by default).
The production posture refuses them.

Not included yet: Resource Explorer and Egeria Advisor charts (a later phase; see [Known limits](#known-limits)).

## Two choices you make for every install

1. **Environment:** `quickstart` (the Coco Pharmaceuticals demo content, port 9443, servers `qs-*`) or `freshstart`
   (an empty Egeria with a sign-in page on the Portal (no server-side API gate until PO-78, so port-forward only), port 8443, servers `fs-*`).
   See [docs/configuration.md](docs/configuration.md#quickstart-or-freshstart).
2. **Posture:** `demo` or `production`. You pick it with a values file (`values-demo.yaml` or `values-production.yaml`).
   - **Demo** builds its Secrets from the public demo files tracked in this repository. Anyone can read those
     passwords. Use it only on a cluster you control.
   - **Production** creates no credentials. It requires your own Secrets, keystore, StorageClass, resource limits and
     image digests, turns on TLS verification and NetworkPolicies, and refuses to render without them. It is hardened
     and operable, **not highly available**: one platform pod and one Portal pod.

## Where to go next

| I want to… | Read |
|---|---|
| Try the stack on a laptop (kind or another plain Kubernetes) | [docs/kubernetes.md — Quick start](docs/kubernetes.md#quick-start-on-kind-demo) |
| Install for real on Kubernetes | [docs/kubernetes.md — Production-style install](docs/kubernetes.md#production-style-install) |
| Install on OpenShift (or OpenShift Local) | [docs/openshift.md](docs/openshift.md) |
| Run a public-demo style Portal (registration, demo login) | [docs/configuration.md — demoMode](docs/configuration.md#demomode) |
| Look up a value | [docs/configuration.md — Values reference](docs/configuration.md#values-reference) |
| Verify, upgrade, uninstall or troubleshoot | [docs/operations.md](docs/operations.md) |
| Change the charts or rerun the live tests | [docs/testing.md](docs/testing.md) |

## The shortest path

The Portal images are not published to any registry. Build them first
([docs/kubernetes.md — Images](docs/kubernetes.md#images)), then run, from the repository root:

```bash
helm dependency update charts/egeria-platform
helm dependency update charts/egeria-portal
helm dependency update charts/egeria-stack
helm install st charts/egeria-stack -n egeria --create-namespace \
  -f charts/egeria-stack/values-demo.yaml -f charts/egeria-stack/values-freshstart.yaml \
  --set core.demoPostgres.enabled=true --set core.demoKafka.enabled=true \
  --set core.persistence.storageClassName=standard \
  --set portal.images.portal.repository=<registry>/portal-freshstart --set portal.images.portal.tag=freshstart-6.3-<sha> \
  --set portal.images.apache.repository=<registry>/apache-web --set portal.images.apache.tag=6.3-<sha>
helm test st -n egeria
```

A Ready pod does **not** mean Egeria is up. The first start loads content packs for several minutes. Only the two
`PASS` lines from `helm test` mean the stack is ready.

## Known limits

- **One replica each.** The platform and the Portal refuse `replicas` above 1. There is no high availability.
- **Portal images and PO-68.** Build the Portal image from a tree that contains the PO-68 fix (c6aedd12,
  odpi/egeria-workspaces#907) before you expose a Portal through an Ingress or Route. The older images these charts
  were first tested with hand out the Portal's service-user token to anyone. On a gated Portal, `helm test` fails
  on such an image. See [docs/operations.md](docs/operations.md#helm-test-fails-the-po-68-check).
- **The demo Postgres and Kafka** have no tuning, backups or high availability, and they do not run on OpenShift's
  `restricted-v2`.
- **Resource Explorer** (phase 3) is not charted yet. It waits on TR-115: Resource Explorer's other stores still run
  their own DDL in external-schema mode.
- **Not yet run on a cluster:** the TR-123 additions (`imagePullSecrets` and `serviceAccountName`, configurable Portal
  and Apache probes, Apache tolerations and affinity, the `portal.platform.userDirectorySecret` requirement). They are
  render-tested; a kind and OpenShift Local run is still to come.
