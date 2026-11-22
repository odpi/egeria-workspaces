# Verifying, upgrading, uninstalling and troubleshooting

The examples use the release `st` in the namespace `egeria`.

## Verify with `helm test`

```bash
helm test st -n egeria --logs
```

A Ready pod is not proof. The platform pod is Ready once the platform process answers; its servers then spend several
minutes loading content packs. Only the `PASS` lines mean the stack is ready.

| Test pod | What it does | Success line |
|---|---|---|
| `<release>-platform-canary` | Signs in to the platform as the canary account; waits until every server in the server list is active; reads the canary element (`Egeria:IntegrationGroup:Default`) through the view server. In production it verifies TLS against `ca.crt` and never uses `-k`. | `PASS: platform up, servers verified` |
| `<release>-portal-canary` | Requests `/portal` through the Apache front door (a gated Portal may redirect to its login page); gets an Egeria token as the canary account; on a gated Portal (freshstart, or `demoMode`) also checks that a token request with no password and no session is refused with 401 (the PO-68 check). | `PASS: portal up, front door and Egeria token verified` |

Each platform test step retries for up to `canary.timeoutSeconds` (600 by default). Run `helm test` again if the first
start has not finished. The test pods are kept after a run, so you can read them later:

```bash
kubectl -n egeria logs st-platform-canary
kubectl -n egeria logs st-portal-canary
```

Watching the servers start, as the test scripts do:

```bash
kubectl -n egeria logs st-platform-0 -c platform | grep -c SERVER-OPS-0004     # one line per started server; 5 expected
```

The Portal heals missing Egeria content by itself and reports it at `GET /api/bootstrap/status` through the front door
(and in a banner in the UI). It stays Ready while it heals.

## Upgrade

Pass the same values files and settings again, or reuse the stored ones:

```bash
helm upgrade st charts/egeria-stack -n egeria -f charts/egeria-stack/values-demo.yaml -f charts/egeria-stack/values-freshstart.yaml -f my-values.yaml
helm upgrade st charts/egeria-stack -n egeria --reuse-values --set portal.siteUrl=https://egeria.example.com
```

Run `helm dependency update` on the three charts first when the charts themselves changed. Then run `helm test`.

What to know:

- **Server configuration documents are seeded once.** The platform's init container copies each server's
  configuration document into the data volume only when it is missing, because Egeria's admin API rewrites them.
  A changed document in a new chart version is not applied to an existing volume unless `platform.configs.overwrite`
  is `true`. With `true` it is copied on every pod start, overwriting changes made through the admin API, so set it
  back to `false` afterwards.
- **`application.properties` changes restart the platform.** The pod template carries a checksum of the properties
  ConfigMap.
- **Secret changes do not.** The keystore passwords and the secrets files are read when the pod starts. After you
  change `tls.existingSecret` or `secrets.existingSecret`, restart the platform:
  `kubectl -n egeria rollout restart statefulset/st-platform`. Change the keystore and the CA (`ca.crt`, and the
  Portal's `tls.caSecret`) together: a new CA that does not match the keystore the running platform loaded makes the
  platform test hang on TLS verification.
- **The demo Portal Secret keeps its random values** (`jwt-secret`, `mcp-access-token`) across upgrades, so sessions
  survive. It uses `lookup`, which `helm template` and `--dry-run=client` cannot do, so those always show new values.
- **The public-demo keystore check runs again** on every production upgrade.
- **Volume sizes are fixed.** Kubernetes refuses changes to a StatefulSet's `volumeClaimTemplates`, so
  `persistence.size` of the platform cannot be changed by an upgrade.

## Uninstall

```bash
helm uninstall st -n egeria
```

This keeps the data volumes on purpose:

| Claim | Why it stays |
|---|---|
| `data-st-platform-0` | Kubernetes keeps StatefulSet claims |
| `st-portal-data` | `helm.sh/resource-policy: keep` |
| The demo Postgres claim | Kubernetes keeps StatefulSet claims |

Secrets you created yourself also stay. A later install with the same release name finds the old volumes again. To
remove everything, delete the claims (`kubectl -n egeria get pvc`, then `kubectl -n egeria delete pvc <name>`), or the
namespace. Deleting a claim deletes the metadata it holds; there is no undo.

Your external PostgreSQL keeps its database. A fresh install against it sees the old metadata.

## Troubleshooting

### `helm install` fails with a message

Every refusal names the value to change, for example
`set postgres.host: the platform needs an external PostgreSQL ...` or
`the production posture requires tls.existingSecret ...`. Set the value and run the command again. Common ones:

| Message starts with | Cause |
|---|---|
| `core.environment is ... but environment is ...` | Pass `values-<environment>.yaml` instead of `--set environment=...` |
| `posture is ..., core.posture is ... and portal.posture is ...` | Pass `values-<posture>.yaml` instead of `--set posture=...` |
| `the production posture needs a login gate, and the quickstart environment has none` | Production requires freshstart |
| `ingress.enabled with environment=quickstart and demoMode=false ...` | See [kubernetes.md — Ingress](kubernetes.md#ingress) |
| `set networkPolicy.enabled=true: with an Ingress ...` | An Ingress always needs the Portal NetworkPolicy |
| `... holds the PUBLIC demo keystore password ...` | Make a keystore of your own ([kubernetes.md](kubernetes.md#2-keystore-tlsexistingsecret)) |
| `set images.portal.digest: the production posture pins images by digest` | [Image digests](kubernetes.md#5-image-digests) |
| `extraEnv may not set ...` | Set the matching chart value instead |

### The platform pod stays in `Init`

The init container `wait-for-dependencies` waits up to 600 seconds for PostgreSQL and Kafka:

```bash
kubectl -n egeria logs st-platform-0 -c wait-for-dependencies
```

`ERROR: PostgreSQL ... not reachable after 600 s` or `ERROR: Kafka ... not reachable` names the value to check
(`postgres.host`, `postgres.port`, `kafka.bootstrapServers`). Remember the default Postgres port is 5442. With
NetworkPolicies of your own in the database's namespace, allow the platform pod.

If `seed-config-documents` fails, a server in `platform.serverList` has no configuration document in the chart.

### The platform pod is Running but not Ready for a long time

That is normal on the first start: the startup probe allows 600 seconds by default (`probes.startup`). If the pod is
restarted by the startup probe on a slow cluster, raise `probes.startup.failureThreshold`. Check memory: the platform
needs its 6Gi limit, and an `OOMKilled` status means the limit is too low (a heap dump goes to `/deployments/logs`).

### `helm test` fails

| Output | Cause and fix |
|---|---|
| `FAIL: servers not active after 600s: ...` | The servers are still starting. Wait and run `helm test` again; check the `SERVER-OPS-0004` count. |
| `FAIL: could not get a token for account ...` | The canary account or password is wrong, or the account is not in the user directory. Check `canary.existingSecret`. |
| `FAIL: set canary.existingSecret ...` | Production has no canary account; create the Secret ([kubernetes.md](kubernetes.md#4-canary-account-canaryexistingsecret)) |
| `FAIL: production verifies TLS: add a ca.crt key ...` | Add `ca.crt` to the TLS Secret |
| The platform test hangs, then times out, in production | TLS verification fails: the certificate is not valid for the Service name (set `canary.tlsServerName`), or `ca.crt` does not match the keystore the platform loaded (restart the platform after changing either) |
| `FAIL: the canary account gets a bearer token ... (HTTP 500)` from the Portal test | The Portal could not sign in to Egeria as the canary. A wrong password returns 500, not 401. Check the canary Secret and that the platform test passes. |

### `helm test` fails the PO-68 check

```
FAIL: a request with no password and no session is refused (HTTP 200; 200 would mean PO-68: the Portal image predates the fix)
```

The Portal image was built before the PO-68 fix (c6aedd12, odpi/egeria-workspaces#907). Such a Portal hands out its
service-user token to any caller. Rebuild the Portal image from a tree that contains the fix
([kubernetes.md — Images](kubernetes.md#images)) and upgrade. Do not expose that Portal through an Ingress or Route
until the check passes.

### Pods are refused on OpenShift

- `unable to validate against any security context constraint` for the Egeria pods: set `global.openshift=true`.
- The demo Postgres or Kafka is refused: they need fixed UIDs. Run them in a separate namespace with `anyuid`, or
  use your own ([openshift.md](openshift.md#postgres-and-kafka)).
- Pods stay Pending on OpenShift Local, or the test pod is not scheduled: the node may be under disk pressure.
  Give crc a bigger disk ([openshift.md](openshift.md#openshift-local-sizing)).
- `ImagePullBackOff` for an image you loaded into the node by name, after pushing images to the internal registry:
  see [openshift.md — Known quirk](openshift.md#known-quirk-an-image-by-name-after-a-registry-push).

### Images on kind

`ErrImagePull` after `kind load` on a Docker that uses the containerd image store: the import is broken. Push the
images to a registry the kind node can reach instead ([kubernetes.md — Images](kubernetes.md#images)).

### Resource Explorer

There is no Resource Explorer chart yet. It is phase 3 of this work and waits on TR-115 (Resource Explorer's other
stores still run their own DDL in external-schema mode). Platform clients other than the Portal need the
`egeria.odpi.org/client: "true"` label when the platform NetworkPolicy is on.
