# trellis-re

Resource Explorer: the web role, one worker and a schema Job. It needs an Egeria platform and a Postgres with the pgvector
extension that you run yourself. The image is built from the trellis repo (`docker/Dockerfile.resource-explorer`); it is not published.

```bash
helm install re charts/trellis-re -n <ns> -f charts/trellis-re/values-demo.yaml \
  --set image.repository=<registry>/trellis/resource-explorer --set image.tag=<tag> \
  --set database.host=<host> --set database.name=<db> --set database.user=<runtime role> --set database.existingSecret=<secret> \
  --set egeria.platformUrl=https://<platform>:9443 --set egeria.daemon.userId=<account> --set egeria.daemon.existingSecret=<secret>
```

Tested: `charts/tests/re_render_test.py` (no cluster) and `charts/tests/kind_re.sh` (kind, demo and `MODE=production`). With `tls.verify=true` the platform's CA must pass strict verification (the image runs Python 3.13: a CA needs `keyUsage` with `keyCertSign` and key identifiers). See `charts/docs/testing.md`.

## How the schema is handled

A pre-install/pre-upgrade Job runs `resource-explorer schema apply`: it creates and migrates the registry and the metrics,
feedback, vector-store and artifact-tree schemas and writes the version markers. The web and worker pods run
`RE_SCHEMA_MODE=external`: they send no DDL and refuse to start when a marker is missing or for other code. The Job needs
the **owner** role; the pods need only the **runtime** role.

The Secrets you name in `database.*` must exist before `helm install` (hooks run before the chart's own objects).

## What the database admin sets up

The runtime role gets default privileges on what the owner creates, and nothing else. Run this once, before the first install
(the extension is the admin's too: a managed Postgres often refuses it to the Job's role, and the Job then says so):

```sql
CREATE ROLE re_owner LOGIN PASSWORD '...';
CREATE ROLE re_rt LOGIN PASSWORD '...';
CREATE DATABASE re_db OWNER re_owner;
\c re_db
CREATE EXTENSION IF NOT EXISTS vector;
ALTER DEFAULT PRIVILEGES FOR ROLE re_owner GRANT USAGE ON SCHEMAS TO re_rt;
ALTER DEFAULT PRIVILEGES FOR ROLE re_owner GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO re_rt;
ALTER DEFAULT PRIVILEGES FOR ROLE re_owner GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO re_rt;
```

Then set `database.user=re_rt` and `database.owner.user=re_owner` (with `database.owner.existingSecret`). In the production posture the chart **refuses** unless the owner role and its Secret are set and differ from the runtime role: with one role the Job would run as the runtime role, and giving that role DDL rights voids the split. The demo posture may use one role.

## A new resource needs the schema Job

In `external` mode the pods send no DDL, so a vector collection the schema Job has not created is refused, with a message that says
**a new resource needs the schema Job: `helm upgrade`, or run `resource-explorer schema apply`**. What counts as a new resource:

- a new project (its `<slug>_<type>` collections);
- a project whose `homepage_url` or `docs_url` points at a new host (website ingestion writes `web_docs_<host>`, keyed on the host, not on a repository);
- a collection name a project has recorded (a site shared with a sibling repository).

`resource-explorer schema apply` declares and creates all of them on every run (a no-op when nothing is new, apart from reading the
projects), so `helm upgrade` (which runs the Job as a hook) or running that command is enough; the pods need no restart. There is no
automatic trigger: ingesting a new resource before the Job has run fails loudly, by design. The reindex swap and collection
rename/drop are refused in external mode too.

## Prefect (optional)

`prefect.enabled=true` adds a Prefect worker (the image's `prefect-worker` role) and turns Prefect dispatch on for web and worker. You run the
Prefect server; set `prefect.apiUrl` (and `prefect.apiKeySecret`, a Secret with key `api-key`, if your server wants one). web, worker and the Prefect
worker are one image, so one commit, which RE requires before it dispatches (otherwise it warns and runs the steps itself). An init step creates the
`process` work pool when it is missing. The worker is a `process` worker: each step runs as a subprocess of its pod, with the pod's environment and
the shared data volume. `prefect.dispatchSteps` chooses which steps go to Prefect (empty: the image default).

## A2A (optional)

`a2a.enabled=true` adds the `a2a` role: every Resource Explorer agent on **one port** (`a2a.port`, 8100: the image's own `PORT` is 8810, so the chart sets it
explicitly) behind a bearer token. It is a ClusterIP Service only; there is no Ingress for it. The cards and `/.well-known/agents.json` are public by design;
every agent call needs a token, either a trellis app JWT (verified with the shared `jwt-secret`, so a web login's token works) or a raw Egeria token (validated
against the platform; the result is cached for the token's own lifetime, keyed on a hash of the token). There is no static A2A token, and
`A2A_ALLOW_ANONYMOUS` is never set by the chart and is refused through `extraEnv`.

- **Who may reach it:** the NetworkPolicy lets anything that can reach the Service in, on the A2A port only, as for web. Narrow it for your Ingress controller or Portal if you need to.
- **Credentials:** the same runtime database role and Secrets as web, and the same LLM settings and `extraEnvFrom` (provider API keys). It does **not** get RE's Egeria
  service account unless you set `a2a.serviceAccount=true` (the agents make no service-account Egeria call today).
- **One replica.** The conversation context is held in memory: a restart or a rollout loses the conversations that are open, and the chart refuses more than one
  replica (a task started on one pod is invisible on another).
- **`A2A_PUBLIC_URL`** is the URL written into the cards; it defaults to the in-cluster Service URL. Set `a2a.publicUrl` when callers reach it another way.
