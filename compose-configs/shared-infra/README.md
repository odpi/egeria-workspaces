<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Shared infrastructure for Egeria workspaces

This directory contains the shared Kafka, PostgreSQL, OpenLineage proxy, and Kroki (diagram rendering) infrastructure used by
both the `egeria-quickstart` and `egeria-freshstart` deployments.

The shared stack exposes:

- Kafka on `9192`, `9193`, `9194`
- PostgreSQL on `5442` (with [pgvector](https://github.com/pgvector/pgvector) extension available)
- OpenLineage proxy on `6000`, `6001`
- Kroki (`egeria-shared-kroki` + `egeria-shared-kroki-mermaid` companion) on host `6002` (container-internal `8000`)
- the external Docker network `egeria_network`

## Kroki (Mermaid diagram rendering)

pyegeria's `render_mermaid()` (used by Jupyter notebooks) previously called the public `https://kroki.io` service directly —
an unannounced external dependency subject to that service's own load (intermittent "Failed to launch the browser process"
Chromium crashes) and Mermaid version drift (inconsistent diagram colors/themes between requests). This stack now runs its
own Kroki instance instead: `egeria-shared-kroki` (core) + `egeria-shared-kroki-mermaid` (the headless-browser companion
Mermaid needs, given `shm_size: 1gb` — the standard fix for the same class of Docker/Chromium crash kroki.io's own
infrastructure was hitting).

Jupyter services in both environments set `EGERIA_KROKI_URL=http://egeria-shared-kroki:8000` (container-to-container,
on `egeria_network`) so pyegeria tries this container first. If it's absent or unreachable, pyegeria falls back to
rendering the diagram entirely client-side in the notebook's browser (no server dependency at all) — nothing
hard-depends on this container being present. Host processes not on `egeria_network` (e.g. `resource-explorer`, run
via `uv run` rather than containerized) reach it at `http://localhost:6002` instead — the published host port is
`6002`, not Kroki's own default `8000`, to avoid colliding with common local dev servers (`mkdocs serve`, etc.) that
also default to `8000`.

## PostgreSQL and pgvector

PostgreSQL runs from the `pgvector/pgvector:pg17` image, which includes the pgvector extension pre-installed. This enables
vector similarity search in any database where the extension is activated.

The `egeria_advisor` database (used by Trellis: Resource Explorer, Egeria Advisor and Studio) is created at first startup
by `docker-entrypoint-initdb.d/init_trellis.sh`, with pgvector already enabled and owned by the `egeria_advisor` user.
Its password is `PGVECTOR_PASSWORD` from `shared-infra/.env`. **There is no default password.**
- On a brand-new install, `gen-env.sh` generates a random `PGVECTOR_PASSWORD` into `.env` (mode 600).
- To choose your own instead, set `PGVECTOR_PASSWORD` in the environment or in `.env` before the first start.
- Give Trellis the same value as its `PGVECTOR_PASSWORD`. Trellis refuses to start without it.
- If it is empty at first start, the role is created without a password and cannot log in until you set one (below).
All other databases have pgvector available but not enabled — run `CREATE EXTENSION IF NOT EXISTS vector;` in any database
that needs it.

### The provisioner user
`provisioner` is the Postgres user that Egeria's provisioning services deliver digital products with (into `egeria_ods`,
`coco_data_hub` and `subscription_staging`), and that Airflow's `coco_data_hub` connection signs in with.
Its password is `PROVISIONER_PASSWORD` from `shared-infra/.env`. **There is no default password.**
- `gen-env.sh` generates a random `PROVISIONER_PASSWORD` into `.env` (mode 600) when neither the environment nor `.env`
  has one, on an existing install too.
- `ensure-shared-infra.sh` sets the role's password from it on every start (`init_egeria_ods.sql`). So to rotate it, put
  a new value in `.env` (or delete the line to have a new one generated) and run the start script again.
- The start scripts put the same value into the Egeria secrets as they copy them into `runtime-volumes`
  (`install-secrets.py`: collection `PostgreSQL Provisioning Secret` in `integration.omsecrets`, whose template holds
  the placeholder `__PROVISIONER_PASSWORD__`) and into Airflow's connection (`export-provisioner-password.sh`).
  After a rotation, restart Airflow the same way (`quick-start-local --with-airflow-marquez`, or `switch-lineage.sh`),
  or its `coco_data_hub` loads fail to sign in.
- `airflow-marquez.yaml` refuses to run without `PROVISIONER_PASSWORD` in the environment, so EVERY compose command on
  that file (`up`, `down`, `ps`, `config`, …) needs it exported first: `source ../../shared-infra/export-provisioner-password.sh`.
- Use letters and digits only (as the generated value is). The value is written as it is into YAML and into Airflow's
  connection URI, where other characters can break them.
- **Re-running a start script keeps the password.** `quick-start-local`, `fresh-start-local` and `gen-env.sh` take
  `PROVISIONER_PASSWORD` from the environment first, then from the existing `.env`, and write the value they used
  back into `.env`. They generate a new one only when neither has a value. So a redeploy that leaves the databases
  alone keeps the same password, and nothing loses access.
- **A new password comes only from:**
  - a missing `.env`, or a missing or empty `PROVISIONER_PASSWORD` line in it: for example a fresh clone, a
    cleaned-up checkout, or a deleted `shared-infra/.env`. Keep that file, or keep a copy, if you want the password
    to stay the same;
  - a different `PROVISIONER_PASSWORD` exported in the shell you start from. It replaces the value in `.env`, so
    don't leave a different value exported when you start.

  If a new password does come in:
  - The next start applies it to the role and to the Egeria secrets **of the stack you start** (for a freshstart with
    `--keep-existing`, its placeholder secrets), so that stack's provisioning services keep working.
  - The role is shared. On a host that runs both the quickstart and a freshstart, re-run the start script of the other
    one too (`quick-start-local` or `fresh-start-local`). Until then its Egeria secrets keep the old password, and its
    provisioning connectors fail to sign in (HTTP 500, `PostgresTabularDataSetCollectionConnector` and
    `password authentication failed for user "provisioner"` in the platform log).
  - No data is lost. Changing a role's password doesn't drop or empty anything: `egeria_ods`, `coco_data_hub`,
    `subscription_staging` and Egeria's metadata store keep their contents. Egeria's own metadata store doesn't sign
    in as `provisioner` at all.
  - Airflow picks up the new value only when its containers are recreated. A `quick-start-local` run that starts
    Airflow (`--with-airflow-marquez`, or by default under `--demo`) does this itself. Otherwise recreate them as
    after a rotation (above). Until then its `coco_data_hub` loads fail with a sign-in error, visibly.
- Before this change the role had a well-known password. The first start after it rotates that password, together
  with the Egeria secrets of the stack you start and the Airflow connection if that start brings Airflow up. If the
  host also runs the other stack, re-run its start script straight after (see above). Writing to the shared Postgres
  affects other users, so tell them first.

### Egeria operational data store (egeria_ods)

The `egeria_ods` database receives Egeria's open metadata digital products - one table per product - so that the
content of the open metadata ecosystem can be queried with SQL. Both the quickstart and the freshstart environments
use it. It is created empty by `docker-entrypoint-initdb.d/init_egeria_ods.sql`, along with the `provisioner` user
that Egeria's provisioning services deliver the products with. Cataloguing the database and taking out the
subscriptions that fill it - one for each top-level product family, each with its own schema - is done by `workbooks/subscribing-to-digital-products/build-egeria-ods.ipynb` in
freshstart, and by `coco-workbooks/1. coco-data-hub/egeria-operational-data-store.md` in quickstart.

The scripts in `docker-entrypoint-initdb.d` run only when the server's data volume is first created, so
`ensure-shared-infra.sh` runs `init_egeria_ods.sql` again on every start to add the database to a server that
predates it. The script creates only what is missing. To add another database later, write its script the same way
and add it to `SHARED_POSTGRES_UPDATE_SCRIPTS` in `ensure-shared-infra.sh`.

### Security operational data store (security_ods)

The `security_ods` database receives the open metadata digital products of Egeria's *Security Observability* product
family. Those products are in the security governance zone, so they are delivered to a database of their own rather
than to `egeria_ods`: only `provisioner` (to deliver) and `surveyor` (to catalogue) may connect to it. It is created
empty by `docker-entrypoint-initdb.d/init_security_ods.sql`, which `ensure-shared-infra.sh` also runs on every start.
Cataloguing the database and taking out the subscription is done by
`coco-workbooks/1. coco-data-hub/security-operational-data-store.md` in quickstart, run as Ivor Padlock.

### Query statistics (pg_stat_statements)

PostgreSQL starts with `pg_stat_statements` preloaded and `track_activity_query_size=16384`, so slow or frequent
statements can be found without sampling, and `pg_stat_activity` shows Egeria's long generated SQL in full. A new data
directory gets the extension in the `egeria` database from `init_egeria.sql`. On an existing container, the settings
take effect at the next restart of `egeria-shared-postgres` (this briefly interrupts every service that uses it); then
run, once per database you want to inspect:

```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
-- busiest statements by total time
SELECT calls, round(total_exec_time) AS ms, rows, left(query, 120)
FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 20;
```

Both root startup scripts (`quick-start-*` and `fresh-start-*`) call `ensure-shared-infra.sh`, which:

1. generates `.env` for the shared stack,
2. creates `egeria_network` if needed,
3. starts OpenLineage proxy, Kafka, PostgreSQL, and Kroki when they are missing or stopped,
4. waits until all services are ready.

`ensure-shared-infra.sh` now also refreshes images during startup:

- it rebuilds the local proxy image with `docker compose build --pull`, and
- it starts services with `docker compose up -d --pull always` so Docker checks for newer remote images before using cached ones.

To bypass the local build cache for the proxy build, set `NO_CACHE=1` before running the script.

### Resetting an Egeria metadata database

To start Egeria from a clean metadata store, use `reset-egeria-db.sh` rather than a bare `DROP/CREATE DATABASE`.
`docker-entrypoint-initdb.d/init_egeria.sql` grants `egeria_admin` and `egeria_user` privileges on the database, but it only
runs when Postgres initialises a new data directory, so a hand-recreated database has no grants and the platform crash-loops
with `permission denied for database egeria`. The script stops the platform container, drops and recreates the database,
re-applies the grant, and restarts the platform:

```bash
./reset-egeria-db.sh --dry-run            # show what would happen
./reset-egeria-db.sh --backup             # pg_dump to egeria-db-backups/ first, then reset (asks you to type the database name)
./reset-egeria-db.sh --database egeria_freshstart --container <freshstart platform container>
```

All metadata in that database is lost. Stop anything else that writes to Egeria first, and do not hand-run Dr.Egeria documents
afterwards; the portal's bootstrap heal repopulates the content.

**After any egeria-main restart: re-sync report specs** (Egeria Explorer → Report Specs → **Sync from Egeria**, as an administrator, or `POST /api/report-specs/sync`), or wait for the Portal's self-heal: while the consumer index is "not read" it syncs again at most every 2 minutes, on the next Report Specs or publish request. A sync that ran while Egeria was restarting leaves **Used by** "not read" (2026-11-12).

For the quickstart, prefer `compose-configs/egeria-quickstart/bin/egeria-upgrade-reset`: it also upgrades the platform image,
backs up and verifies the dump, recreates the container on the new image (this script's `docker start` keeps the old one),
waits for the heal and checks the result. Both use the same SQL, `reset-egeria-db.sql`. See
[Upgrading or resetting the quickstart Egeria](../../portal-docs/Internals/upgrading-or-resetting-egeria.md).

## Image pinning and hardened Kafka defaults

`gen-env.sh` writes image references into `compose-configs/shared-infra/.env`:

- `SHARED_KAFKA_IMAGE` (default pinned reference for the hardened Kafka image)
- `SHARED_POSTGRES_IMAGE` (default pinned digest for PostgreSQL)
- `HARDENED_KAFKA_DATA_DIR` (host path used for persistent hardened Kafka data)
- `HARDENED_KAFKA_LOG_DIR` (container path used for KRaft logs in hardened mode)

Kafka runs on the hardened image by default. Startup behavior remains the same while image references are pinned.
To change the hardened image reference, set:

```bash
SHARED_KAFKA_IMAGE=<your-compatible-hardened-kafka-image>
```

> Note: the hardened image must be compatible with the current Kafka configuration (KRaft single-node and `KAFKA_CFG_*` environment variables).
> Kafka persistence uses a dedicated host directory (`HARDENED_KAFKA_DATA_DIR`) prepared by
> `ensure-shared-infra.sh`, so it does not depend on the legacy `/bitnami/kafka` volume permissions.

### Kafka image versions: layout and user

The default image is `cleanstart/kafka` 4.4.0. It is laid out differently from the 4.1.1 image used before it:

| | 4.1.1 | 4.4.0 |
|---|---|---|
| Kafka home (`bin/`, `config/`, `libs/`) | `/usr/lib/kafka` | `/opt/kafka` |
| Broker's own server logs | `/usr/lib/kafka/logs` | `/opt/kafka/logs` |
| Runs as | uid 65532, gid 65532 | uid 1000, gid 1000 (`kafka`) |

Nothing in this directory depends on which one is in use:

- `kafka-entrypoint.sh` looks for Kafka in `/opt/kafka` and then `/usr/lib/kafka` (set `KAFKA_HOME` to override), so the
  same script starts either image.
- `kafka-log4j2.yaml` is mounted at `/etc/egeria-kafka/log4j2.yaml`, outside Kafka home, and the entrypoint passes it to
  the broker. The Kafka command line tools keep the image's own logging configuration.
- To run a Kafka command in the container, use the path for the image, for example
  `docker exec egeria-shared-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9192 --list`.

**Moving an existing installation from 4.1.1 to 4.4.0 on Linux.** The files in `HARDENED_KAFKA_DATA_DIR` were written
by uid 65532 and the 4.4.0 broker runs as uid 1000. `ensure-shared-infra.sh` tries to open up the permissions, but
with Docker it cannot change files that the container's user owns, and prints
`Warning: Could not fully set permissions`. Stop Kafka and change the owner before starting the new image:

```bash
docker stop egeria-shared-kafka
sudo chown -R 1000:1000 runtime-volumes/shared-infra-hardened-kafka
./compose-configs/shared-infra/ensure-shared-infra.sh
```

If this step is missed, the broker does not start: the entrypoint exits with
`ERROR: /var/lib/kafka-data/kraft-logs is not writable by uid 1000` and the same `chown` command. Docker Desktop on
macOS maps the ownership of bind-mounted files, so no change is needed there. A new installation needs no change on
any platform.

`gen-env.sh` moves an existing `.env` from the 4.1.1 digest to the 4.4.0 one the next time it runs, unless
`SHARED_KAFKA_IMAGE` is set in the environment.

> Do not stay on Kafka 4.1.1. Its group coordinator can stop serving a `__consumer_offsets` partition when the
> container's clock steps backwards (`Histogram recorded value cannot be negative` in the broker log). Every consumer
> group on that partition then rebalances every five seconds and receives no events until the broker is restarted.
> This is fixed in Kafka 4.1.2 and later.

You can also manage the shared stack directly from this directory:

```bash
./ensure-shared-infra.sh
NO_CACHE=1 ./ensure-shared-infra.sh
docker compose -p egeria-shared-infra -f shared-infra.yaml build --pull proxy
docker compose -p egeria-shared-infra -f shared-infra.yaml up -d --pull always proxy kafka postgres kroki kroki-mermaid
docker compose -p egeria-shared-infra -f shared-infra.yaml ps
docker compose -p egeria-shared-infra -f shared-infra.yaml down
```

To force a clean rebuild of the proxy image when running Docker Compose manually, add `--no-cache` to the build step:

```bash
docker compose -p egeria-shared-infra -f shared-infra.yaml build --pull --no-cache proxy
```

## Upgrading an existing installation to pgvector

If you already have a running `egeria-shared-postgres` container (using `postgres:17.x-bookworm`), the image will be updated
automatically the next time `ensure-shared-infra.sh` runs — your existing data is preserved because it lives in the
`egeria-shared-infra_shared_postgres_data` Docker volume, which is independent of the container image.

However, the `egeria_advisor` database is not created automatically on an existing volume (init scripts only run on first
start).

#### Creating egeria_advisor on an existing volume
Run the same init script once, with the password in your shell's environment. `-e PGVECTOR_PASSWORD` with no value
passes it through, so it never appears on a command line:

```bash
read -rs PGVECTOR_PASSWORD && export PGVECTOR_PASSWORD   # typed, not echoed, not in shell history
# or: set -a; . compose-configs/shared-infra/.env; set +a
docker exec -e PGVECTOR_PASSWORD -e PGPORT=5442 egeria-shared-postgres \
  bash /docker-entrypoint-initdb.d/init_trellis.sh
```

The script is idempotent. It creates only what is missing, and it never changes the password of a role that already
exists.

#### Setting or changing the egeria_advisor password
For example, a role created with no password, or one still on the old `advisor` default:

```bash
docker exec -i -e PGVECTOR_PASSWORD egeria-shared-postgres psql -U postgres -p 5442 -d postgres <<'EOSQL'
\getenv p PGVECTOR_PASSWORD
ALTER ROLE egeria_advisor WITH PASSWORD :'p';
EOSQL
```

Set `PGVECTOR_PASSWORD` first the same way (`read -rs PGVECTOR_PASSWORD && export PGVECTOR_PASSWORD`).
Then put the same value in `shared-infra/.env` (`PGVECTOR_PASSWORD=`) and in Trellis's environment, and restart Trellis.
If your Trellis keeps its password in a separate secrets file, leave `PGVECTOR_PASSWORD` in `shared-infra/.env` empty:
it is used only when the volume is first created, and one source is easier to rotate.
Installs made before this change created the role with the password `advisor`. Change it this way.

## Validation and rollback

Smoke-check after changes:

```bash
./compose-configs/shared-infra/ensure-shared-infra.sh
docker compose -p egeria-shared-infra -f shared-infra.yaml ps
./quick-start-local
./fresh-start-local
```

If a provisioning connector fails after a start with `password authentication failed for user "provisioner"`, the
provisioner password was rotated by the other stack's start. Re-run this stack's start script (`quick-start-local` or
`fresh-start-local`) so its Egeria secrets get the current value from `shared-infra/.env`.

Rollback to a previous Kafka or Postgres image reference:

```bash
SHARED_KAFKA_IMAGE=<previous-kafka-image-ref> ./compose-configs/shared-infra/ensure-shared-infra.sh
SHARED_POSTGRES_IMAGE=<previous-postgres-image-ref> ./compose-configs/shared-infra/ensure-shared-infra.sh
```

Rolling Kafka back from 4.4.0 to 4.1.1 works only while the cluster's `metadata.version` is still the 4.1 one, which
it is unless someone has raised it with `kafka-features.sh upgrade`. The 4.1.1 reference is
`docker.io/cleanstart/kafka@sha256:3bfad519feac67e6bd1ae2b18b3e4770cdf2fedf53ecff7b38a520a7c5d77564`. On Linux, also
return the data directory to the 4.1.1 image's user first (`sudo chown -R 65532:65532 <HARDENED_KAFKA_DATA_DIR>`). See
[Kafka image versions: layout and user](#kafka-image-versions-layout-and-user) for why 4.1.1 is only a stopgap.

