# Deploying on OpenShift

Everything in [kubernetes.md](kubernetes.md) applies. This page covers what is different on OpenShift.

What ran live, on **OpenShift Local (crc 2.65.0, OpenShift 5.0.0)**:

| Run | Script | Result |
|---|---|---|
| Freshstart demo stack | `charts/tests/crc_stack.sh` | All pods under `restricted-v2`, 5/5 servers started, both `helm test` checks PASS |
| Production-style freshstart stack | `charts/tests/crc_stack_prod.sh` | Same, with an own keystore, existing Secrets, `tls.verify`, NetworkPolicies and image digests |
| Quickstart stack with `demoMode` | `ENVIRONMENT=quickstart DEMO_MODE=true charts/tests/crc_stack.sh egeria-demo qs` | Same, including the PO-68 check |
| Route for the Portal | `charts/tests/crc_route.sh` | Edge Route with the router's certificate; http redirected to https |

Not run: a full OpenShift cluster (only OpenShift Local), a Route on the production-style stack, and a Route with a
certificate of its own.

## Set `global.openshift=true`

```bash
--set global.openshift=true
```

The charts never detect OpenShift; set it yourself. With it, no `runAsUser`, `runAsGroup` or `fsGroup` is rendered, so
the `restricted-v2` SCC assigns a UID from the namespace's range, with GID 0. Every pod keeps `runAsNonRoot: true`, the
`RuntimeDefault` seccomp profile, no privilege escalation, and all capabilities dropped.

The images are built for this: every path they write is group 0 with group write. In the live runs the platform, the
Portal and Apache all ran under `restricted-v2` with assigned UIDs (for example 1000680000) and GID 0.

Without `global.openshift=true` the charts set fixed UIDs (185 for the platform, 1001 for the Portal and Apache), which
`restricted-v2` rejects.

In the umbrella, `global.openshift` reaches both parts. When you install `egeria-platform` or `egeria-portal` on
their own, set it on each.

## Postgres and Kafka

The production posture needs your own PostgreSQL and Kafka, as on Kubernetes
([kubernetes.md — Prerequisites](kubernetes.md#postgresql-and-kafka-for-production)).

**The bundled demo charts are not supported on OpenShift.** `egeria-demo-postgres` runs as fixed UID 999 and ignores
`global.openshift`. Do not set `core.demoPostgres.enabled` or `core.demoKafka.enabled` there.

For a test install, the live runs put a test Postgres and Kafka in a **separate namespace** with the `anyuid` SCC, so
the Egeria namespace stays under `restricted-v2`:

```bash
oc new-project egeria
oc new-project egeria-infra
oc adm policy add-scc-to-user anyuid -z default -n egeria-infra     # test Postgres and Kafka only
bash charts/tests/kind_infra.sh egeria-infra                         # postgres:5442 and kafka:9192 in egeria-infra
```

`kind_infra.sh` is a test script, not a product: no persistence (emptyDir), public demo passwords. Then point the
platform at it:

```bash
--set core.postgres.host=postgres.egeria-infra.svc.cluster.local \
--set core.kafka.bootstrapServers=kafka.egeria-infra.svc.cluster.local:9192
```

Never grant `anyuid` in the Egeria namespace itself: that would no longer test, or enforce, `restricted-v2`.

## Images

The Portal and Apache images must be in a registry the cluster can pull from ([kubernetes.md — Images](kubernetes.md#images)).

- **Demo runs** loaded the images straight into the crc node (`docker save ... | ssh ... sudo podman load`), so the
  pods used `docker.io/library/portal-<environment>:<tag>` and `docker.io/library/apache-web:<tag>`.
- **The production-style run** pushed them to the cluster's internal registry, so the digests are real registry
  digests. Pods pull them as `image-registry.openshift-image-registry.svc:5000/<namespace>/<image>`. See
  `charts/tests/crc_stack_prod.sh` for the push (a `pusher` ServiceAccount with `system:image-builder`).

For an external private registry, create a pull Secret and set `global.imagePullSecrets`
([configuration.md — Images and pull secrets](configuration.md#images-and-pull-secrets)); that is render-tested only.

A pod in another namespace can pull from the internal registry once it is allowed to:

```bash
oc policy add-role-to-group system:image-puller system:serviceaccounts:<pulling namespace> -n <namespace that holds the images>
```

## Demo install

```bash
helm dependency update charts/egeria-platform
helm dependency update charts/egeria-portal
helm dependency update charts/egeria-stack
helm upgrade --install st charts/egeria-stack -n egeria \
  -f charts/egeria-stack/values-demo.yaml -f charts/egeria-stack/values-freshstart.yaml \
  --set global.openshift=true \
  --set core.postgres.host=postgres.egeria-infra.svc.cluster.local \
  --set core.kafka.bootstrapServers=kafka.egeria-infra.svc.cluster.local:9192 \
  --set portal.images.portal.repository=<registry>/portal-freshstart --set portal.images.portal.tag=<tag> \
  --set portal.images.apache.repository=<registry>/apache-web --set portal.images.apache.tag=<tag>
helm test st -n egeria --logs
```

The demo run left `persistence.storageClassName` empty, so the cluster's default StorageClass was used.

To see which SCC admitted each pod:

```bash
oc -n egeria get pod st-platform-0 -o jsonpath='{.metadata.annotations.openshift\.io/scc}'
```

It should print `restricted-v2`.

## Production-style install

Create the Secrets as in [kubernetes.md — Production-style install](kubernetes.md#production-style-install), with `oc`
instead of `kubectl`, then:

```bash
helm upgrade --install ps charts/egeria-stack -n egeria-prod \
  -f charts/egeria-stack/values-production.yaml -f charts/egeria-stack/values-freshstart.yaml \
  --set global.openshift=true \
  --set core.postgres.host=<postgres host> --set core.kafka.bootstrapServers=<host:port> \
  --set core.secrets.existingSecret=prod-secrets --set core.tls.existingSecret=prod-tls --set core.canary.existingSecret=prod-canary \
  --set core.persistence.storageClassName=<class> --set core.resources.limits.cpu=4 \
  --set portal.secrets.existingSecret=prod-portal --set portal.tls.caSecret=prod-ca --set portal.canary.existingSecret=prod-canary \
  --set portal.persistence.storageClassName=<class> --set portal.platform.userDirectorySecret=prod-secrets \
  --set portal.images.portal.repository=image-registry.openshift-image-registry.svc:5000/egeria-prod/portal-freshstart \
  --set portal.images.portal.tag=<tag> --set portal.images.portal.digest=sha256:<digest> \
  --set portal.images.apache.repository=image-registry.openshift-image-registry.svc:5000/egeria-prod/apache-web \
  --set portal.images.apache.tag=<tag> --set portal.images.apache.digest=sha256:<digest>
helm test ps -n egeria-prod --logs
```

On OpenShift Local the StorageClass was `crc-csi-hostpath-provisioner`.

## Routes

OpenShift turns an Ingress into a Route, so the chart's own Ingress is enough; there is no Route template. This is
what `charts/tests/crc_route.sh` adds to an installed stack:

```bash
helm upgrade qs charts/egeria-stack -n egeria-demo --reuse-values \
  --set portal.networkPolicy.enabled=true \
  --set portal.ingress.enabled=true --set portal.ingress.host=portal-egeria-demo.apps-crc.testing \
  --set-string 'portal.ingress.annotations.route\.openshift\.io/termination=edge'
oc -n egeria-demo get route
```

- `route.openshift.io/termination=edge` ends TLS at the router, with its default certificate. Plain http is
  redirected to https.
- The Route points at the Apache Service only. The Portal's port 8000 stays inside the cluster behind its
  NetworkPolicy, which the chart requires with any Ingress.
- The host must be under your cluster's apps domain (`*.apps-crc.testing` on OpenShift Local).
- The same Ingress rules as on Kubernetes apply: quickstart needs `demoMode: true` (or `allowUngatedPortal` in a
  demo), and production needs `ingress.tlsSecretName`.

`crc_route.sh` checked, through the Route, on the quickstart demoMode stack: `/portal` redirects (302) to the login
page, `/login` answers 200, `POST {}` to `/api/egeria-token` gets 401 (the PO-68 gate), an authenticated API gets 401
for an anonymous caller, plain http is redirected to an `https://` location, and `helm test` passes.

Not run: a Route on the production-style stack (where `ingress.tlsSecretName` is required), and how the router treats
`spec.tls` from the Ingress. Check both on your cluster before relying on them.

## OpenShift Local sizing

crc's defaults are too small. The settings that worked:

```bash
crc config set memory 20480
crc config set cpus 8
crc config set disk-size 70
```

With the default 31 GB disk the node reached kubelet disk-pressure and stopped scheduling the test pod.

## Known quirk: an image by name after a registry push

After `crc_stack_prod.sh` had pushed an image to the internal registry, the node no longer resolved the same
`docker.io/library/apache-web:<tag>` by name: kubelet tried to pull it and was refused. The cause was not found. A later
demo install then had to take Apache from the internal registry by digest:

```bash
--set portal.images.apache.repository=image-registry.openshift-image-registry.svc:5000/<ns>/apache-web \
--set portal.images.apache.digest=sha256:<digest>
```

with `oc policy add-role-to-group system:image-puller system:serviceaccounts:<demo ns> -n <ns>`. Running the demo
install before the production one also avoids it.
