# trellis-re

Resource Explorer: the web role, one worker and a schema Job. It needs an Egeria platform and a Postgres with the pgvector
extension that you run yourself. The image is built from the trellis repo (`docker/Dockerfile.resource-explorer`); it is not published.

```bash
helm install re charts/trellis-re -n <ns> -f charts/trellis-re/values-demo.yaml \
  --set image.repository=<registry>/trellis/resource-explorer --set image.tag=<tag> \
  --set database.host=<host> --set database.name=<db> --set database.user=<runtime role> --set database.existingSecret=<secret> \
  --set egeria.platformUrl=https://<platform>:9443 --set egeria.daemon.userId=<account> --set egeria.daemon.existingSecret=<secret>
```

Tested: `charts/tests/re_render_test.py` (no cluster) and `charts/tests/kind_re.sh` (kind). See `charts/docs/testing.md`.

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

Then set `database.user=re_rt` and `database.owner.user=re_owner` (with `database.owner.existingSecret`).

## A new resource needs a schema apply

In `external` mode a vector collection that the schema Job has not created is refused. Adding a resource (a repository) means running
`helm upgrade` (or the Job) before its first ingest. The reindex swap and collection rename/drop are refused in external mode too.
