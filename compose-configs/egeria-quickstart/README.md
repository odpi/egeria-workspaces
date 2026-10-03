<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Overview
This directory contains the *egeria-quickstart* docker compose script and supporting files, to support the deployment of Egeria for experimentation,
development, and learning. Rather than having to install Egeria, prerequisites and tools separately, these scripts make 
it easy to get a stack running quickly. This deployment configures and starts:

* Egeria on port 9443 and will automatically start the default servers.
* Jupyter is deployed using port 8888 so as not to interfere with other jupyter servers
* Apache Web Server on port 8885 and configured with `httpd.conf`.

Kafka, PostgreSQL, and the OpenLineage proxy are provided by the shared infra stack in `compose-configs/shared-infra`.


This environment is not designed for enterprise-wide use. Please see the [Planning Guide](https://egeria-project.org/guides/planning/)
for more information about designing bespoke Egeria deployments, such as Cloud Native approaches and the use of
Helm charts to configure Kubernetes clusters. 
For further help and advice, please feel free to engage with the community on our [slack channel](https://lfaifoundation.slack.com/join/shared_invite/zt-o65errpw-gMTbwNr7FnNbVXNVFkmyNA%E2%80%8B#/shared-invite/email) - we'd love your feedback and participation.

 

## Egeria Platform - Default Configuration
We use the Egeria platform docker image - [egeria-platform](https://hub.docker.com/r/odpi/egeria-platform). We are now using an internal docker network called
`egeria_network` to allow postgres database to be shared with other deployments such as Superset. 

* Port - By default the platform uses port 9443 and exposes this port to the host environment, This means that Egeria requests
can be made to platform URL **https://localhost:9443** or, if your environment is configured to support it, it can use 
the domain name of your host machine. 
* SSL - By default strict SSL is set to false 
* Content Packs - pre-constructed information sets that can be used to configure Egeria and pre-load metadata, reference data and glossary data. 
You can use the pyegeria command `list-archives` from a terminal window to see available content packs. See [Content Packs](https://egeria-project.org/content-packs/).
* Out-of-the-box Connectors - descriptions of the integration connectors can be found at [Integration Connectors](https://egeria-project.org/connectors/).

* Auto-Started Servers - by default a useful set of Egeria Open Metadata and Governance (OMAG) servers are pre-installed
and started when the Egeria platform is started. A description of these servers is included in the `servers/` directory in this deployment.
The pre-configured and started servers are:

  * qs-metadata-store
  * qs-engine-host
  * qs-integration-daemon
  * qs-nanny-daemon
  * qs-view-server
  
   
* Mounted volumes for:
    * **distribution-hub**: an area where information created by Egeria (such as logs and survey information) can be easily exposed.
    * **quickstart-platform-data**: mounted to `/deployments` (read-write) and includes data, logs, secrets and local platform configuration.
    * **landing-area**: a convenient drop off point for files and folders you want to survey, analyze, and catalog with Egeria.
    * **landing-bay**: a place to drop files that you want to be loaded into Egeria - e.g glossary terms to import into an Egeria glossary.
  
    

## Shared Kafka and PostgreSQL

Quickstart uses the shared Kafka and PostgreSQL containers managed by `compose-configs/shared-infra`.
The startup scripts call `compose-configs/shared-infra/ensure-shared-infra.sh` automatically.
The shared-infra stack pins image references by default in `compose-configs/shared-infra/.env`,
including the hardened Kafka image with a persistent host-side data path.

## Jupyter - configured for Egeria
A standard Jupyter data science docker image is extended to pre-install **pyegeria** and simplify using Egeria from Jupyter notebooks.

File system volumes are mounted for:
    * **landing-area**: a convenient drop off point for files and folders you want to survey, analyze and perhaps catalog with Egeria.
    * **distribution-hub**: an area where information created by Egeria (such as logs and survey information) can be easily exposed.
    * **work**: a place for you to put your code and other artifacts.
    * **workbooks**: an area where we have put some Jupyter notebooks and related information to help you complete common tasks with Egeria. 

## Postgresql - configured for Egeria

PostgreSQL runs in the shared infra stack (port **5442**). Standard Docker PostgreSQL containers
run their initialization scripts only once, when the data volume is brand new. So Egeria Quickstart
also brings the set-up up to date on every start.

### Automatic Initialization

The root startup scripts (`./quick-start-local` and `./quick-start-multi-host`) automatically
execute `compose-configs/egeria-quickstart/bin/apply-postgres-init.sh` after the shared
infrastructure is ready. It waits for PostgreSQL and then runs these scripts from
`docker-entrypoint-initdb.d/`, in order, on every start:

1. `init_egeria.sql` - users, databases, the demo schemas and the `coco_ods` / `coco_sus` sample data
2. `init_coco_data_hub.sql` - the Data Sharing Hub, `coco_data_hub`
3. `init_coco_systems.sql` - the Coco Pharmaceuticals system databases
4. `init_subscription_staging.sql` - the digital product subscriptions, `subscription_staging`

Every script creates only what is missing, so running them again is safe and takes a few seconds.
A new install gets everything. An existing install picks up anything added since it was created.
A database that has been dropped, for example to reset the demo, is recreated on the next start.
Data already in the databases is kept: `coco_ods` and `coco_sus` are loaded only when their schema
is new, and seed rows are inserted only when missing.

To change the set-up, edit or add a script and keep it safe to rerun. A new script also needs an
entry in `INIT_SCRIPTS` in `bin/apply-postgres-init.sh`. A change to a table that already exists
on existing installs needs a statement that is also safe to repeat, for example
`ALTER TABLE ... ALTER COLUMN ... TYPE ...` or `ADD COLUMN IF NOT EXISTS`.
`init_coco_data_hub.sql` has an example.

### What `init_egeria.sql` does

The script:

1. **Creates database users** — `egeria_admin`, `egeria_user`, `airflow_user`, `marquez_user`,
   `example_user`, `uc_user`, and `mlflow_user`.
2. **Creates databases** — `egeria`, `superset`, `coco_pharma`, `airflow`, `marquez`, `examples`,
   `ucdb`, `hive_metastore`, `mlflow_db`, and `coco_ods`.
3. **Grants privileges** to the appropriate users on each database.
4. **Creates schemas** inside specific databases:
   - `demo` schema in `egeria` — the demo-mode user registry.
   - `coco_sus` schema in `coco_pharma` — Coco Pharmaceuticals supply chain / source system data.
   - `coco_ods` schema in `coco_pharma` — Coco Pharmaceuticals operational data store.
5. **Loads sample data** into each schema immediately after creating it, using the SQL files in
   `docker-entrypoint-initdb.d/data/`:
   - `data/coco_sus.sql` is loaded into `coco_sus`
   - `data/coco_ods.sql` is loaded into `coco_ods`

### What `init_coco_data_hub.sql` does

Creates the `coco_data_hub` database — the Coco Pharmaceuticals Data Sharing Hub — and loads
`docker-entrypoint-initdb.d/data/coco_data_hub.sql` into it: one schema per strategic digital product
(81), one table per data structure (153), one column per data field linked to it (1,015 columns - the
shared Product Code field is a column of three tables) with the key columns first, a primary key on the
fields whose link to their data structure has the coverage category `IDENTIFIER`, and the product,
structure and field descriptions as comments.  It also creates the `provisioner` database user
(password `provisioner4egeria`, secrets collection `PostgreSQL Provisioning Secret` in
`secrets/integration.omsecrets`), which reads and writes the rows of every product table, and gives the
cataloguer's `surveyor` user read-only access to every product table, so that the Data Sharing Hub
Manager (Liskov) can survey the hub.  The tables are empty.  `coco_pharma` keeps the existing
Coco systems (`coco_sus`, `coco_ods`).

`data/coco_data_hub.sql` is generated from the product definitions in
`coco-workbooks/1. coco-data-hub/strategic-digital-products/` — regenerate it after changing them:

```bash
# From the repository root
compose-configs/egeria-quickstart/bin/gen-coco-data-hub-sql.py \
  "coco-workbooks/1. coco-data-hub/strategic-digital-products" \
  compose-configs/egeria-quickstart/docker-entrypoint-initdb.d/data/coco_data_hub.sql
```

The SQL only creates what is missing, so once `coco_data_hub` exists a new product or data structure reaches
it on the next start, but a change to an existing column needs an `ALTER` in `init_coco_data_hub.sql`. While
the tables hold no data, you can instead drop the database and restart.

### What `init_coco_systems.sql` does

Creates a database for each of Coco Pharmaceuticals' system estates and fills it with the systems that feed the
strategic digital products. There is one schema per system, holding only the tables needed to fill the product
tables in `coco_data_hub`, plus sample data. The tables and columns are named in the style of each kind of system,
not to the data field naming standard.

| Database | Estate | Contents |
|---|---|---|
| `coco_pharma` (existing) | Coco core, the parent company | 22 systems, 109 tables |
| `austin_systems` | the acquired Austin site | 27 systems, 134 tables |
| `bucharest_systems` | the acquired EKG Pharmaceuticals S.R.L., Bucharest | 17 systems, 120 tables |

The system SQL is in `docker-entrypoint-initdb.d/data/coco_systems/<database>/<system schema>.sql`. The queries that
copy each system's data into the product tables are in
[`exchange-quickstart/coco-dags/coco-system-extracts/`](../../exchange-quickstart/coco-dags/coco-system-extracts/README.md). That README also explains how the systems were chosen.
The seed data is inserted with `ON CONFLICT DO NOTHING`, so each start adds only missing rows. A changed row
stays changed, but a deleted seed row comes back.

### What `init_subscription_staging.sql` does

Creates the `subscription_staging` database, where subscribing systems receive the data of the digital products
they subscribe to. A subscription is one subscribing system taking one digital product, and each subscription
has its own schema, named `<estate>_<system schema>__<product schema>` (estate `coco`, `aus` or `buc`; Coco
systems whose names already start with `coco` keep their name, e.g. `coco_ods__product_master_data`). So two
systems that subscribe to the same product each have their own copy of its data, which lets each take
deliveries on its own schedule and reprocess them after an error.

Each subscription schema has one table per data structure of the product, with the same columns, types,
primary key and comments as the product's table in `coco_data_hub`, followed by five delivery columns:

| Column | Meaning |
|---|---|
| `delivery_identifier` | The delivery (e.g. the pipeline run) that last wrote the row |
| `delivery_timestamp` | When the row was last delivered |
| `processing_status` | `delivered` (waiting for the subscriber), `processed` or `failed`; set back to `delivered` to reprocess |
| `processing_timestamp` | When the subscriber last processed the row |
| `processing_message` | Why processing failed, or the subscriber's note |

A delivery is an upsert on the product's primary key that resets `processing_status` to `delivered`. The
`provisioner` user reads and writes every subscription table; `surveyor` reads them.

The subscriptions (249, from 63 subscribing systems to 56 products) are listed in
`coco-workbooks/1. coco-data-hub/mapping-the-systems/data/product-subscriptions.csv`. A system subscribes to a
product when it implements a solution component whose own product depends on that product (one row per
system and product, whatever the number of dependencies), in all three estates; `coco_ods` and `coco_sus`
subscribe to the products that fill their reporting tables
(see `coco-workbooks/1. coco-data-hub/reporting-subscription-gaps.md` for what no product supplies).
`data/subscription_staging.sql` is generated from the product definitions and that list:

```bash
# From the repository root
compose-configs/egeria-quickstart/bin/gen-subscription-staging-sql.py \
  "coco-workbooks/1. coco-data-hub/strategic-digital-products" \
  "coco-workbooks/1. coco-data-hub/mapping-the-systems/data/product-subscriptions.csv" \
  compose-configs/egeria-quickstart/docker-entrypoint-initdb.d/data/subscription_staging.sql
```

As for `coco_data_hub`, the SQL only creates what is missing: a new subscription reaches an existing
install on the next start, and a change to an existing table needs an `ALTER`.

### Adding schemas to an existing Postgres deployment

If you are using an existing PostgreSQL instance that was not initialized by the quickstart
runner, run the same script yourself. It is safe to run at any time:

```bash
# From the repository root
./compose-configs/egeria-quickstart/bin/apply-postgres-init.sh
```

Older versions of the runner kept a table of applied migrations,
`quickstart_migrations.applied_migrations`, in the `postgres` database. It is no longer used and
can be dropped.

## Demo data synchronization

The Quickstart environment supports synchronizing the demo portal's user and feedback data
between machines using the `user-sync` root command or `--sync-*` flags in `./quick-start-local`.

This workflow:
1.  **Exports** the `demo_auth` and `demo` schemas from the `coco_pharma` database.
2.  **Transfers** the dump files via SSH/SCP.
3.  **Imports** the data into the target machine's PostgreSQL instance.

It requires `ssh` (and optionally `sshpass` for password-based auth) to be available on the
host machine.

Example:
```bash
./quick-start-local --sync-from demo-host:path/to/sync-dir
```

**Using the legacy schema script:**
Alternatively, if you only need the Coco Pharmaceuticals schemas:

```bash
# From the repository root (defaults: localhost:5442, egeria_admin / admin4egeria)
./compose-configs/egeria-quickstart/docker-entrypoint-initdb.d/add_coco_schemas.sh
```

Override connection settings with environment variables if needed:

```bash
PGHOST=myhost PGPORT=5442 PGUSER=egeria_admin PGPASSWORD=admin4egeria \
  ./compose-configs/egeria-quickstart/docker-entrypoint-initdb.d/add_coco_schemas.sh
```

The script is idempotent — it uses `CREATE SCHEMA IF NOT EXISTS` so it is safe to run more than once.

## Open Lineage Proxy 
This is now provided by the shared infrastructure stack and runs on ports 6000 and 6001.
Its build and runtime configuration are in `compose-configs/shared-infra/shared-infra.yaml` and `proxy.yml`.

----
# Usage

Most users should start from the repository root using one of the quick-start scripts:

1. Install and configure Docker (or Podman) and Docker Compose. 
   * Docker must be installed and running — see https://docs.docker.com/install/
   * Configure Docker with at least 8GB memory
   * A Docker network named `egeria_network` will be created automatically by the scripts if needed
2. Clone the repo: [odpi/egeria-workspaces](https://github.com/odpi/egeria-workspaces.git)
3. From the repository root, run one of:
   * `./quick-start-local` — single-machine development, HTTPS via a self-signed cert by default (see [HTTPS](#https))
   * `./quick-start-local --demo` — public demo deployment with user auth, registration, and a real-cert HTTPS on 443 (see [Demo mode](#demo-mode))
   * `./quick-start-multi-host` — reachable from other hosts on your network (see [Local vs multi-host](#local-vs-multi-host))

These scripts will:

   * copy the server configuration files from `compose-configs/egeria-quickstart/servers` to `runtime-volumes/quickstart-platform-data/data/servers`. This enables you to make local changes to the server configurations that persist across restarts and are ignored by Git.

   * build the `egeria-main` image from `Dockerfile-egeria-platform`.
   * ensure `runtime-volumes/quickstart-platform-data/data` and `runtime-volumes/quickstart-platform-data/logs` exist with write permissions.

   * build a jupyter image that is pre-configured to work with Egeria 
    
   * download the docker images for Kafka, Egeria, and Postgres, and then create and start the containers. Both kafka and Egeria will then automatically configure themselves. 

   * start the jupyter container

   For Egeria, this means not only starting up the initial set of servers, but then loading the **CoreContentPack.omarchive** into the metadata repository, and then configuring all the servers. 
   This can take several minutes the first time the containers are created. Subsequent startups will be much faster.

### Full refresh (recommended)

To stop the stack, remove locally-built images, pull the latest egeria-workspaces, rebuild, and restart in one step:

```bash
./refresh-local                  # quickstart + freshstart (if previously set up)
./refresh-local --demo           # refresh and restart in demo mode (auth, HTTPS)
./refresh-local --no-freshstart  # quickstart only
./refresh-local --infra          # also cycle Kafka / Postgres / proxy
./refresh-local --no-pull        # skip git pull (rebuild from current local code)
```

### Partial refresh

The startup scripts now automatically refresh images more aggressively than before:

- local compose images are rebuilt with `docker compose build --pull`, which checks for newer base images before building, and
- containers are started with `docker compose up -d --pull always`, which checks for newer remote images before using cached ones.

If you want to force a completely clean rebuild that ignores Docker's local build cache, set `NO_CACHE=1` when starting the stack from the repository root:

```bash
NO_CACHE=1 ./quick-start-local
NO_CACHE=1 ./quick-start-multi-host
```

Accepted truthy values are `1`, `true`, `yes`, and `on`. Falsey values are unset, `0`, `false`, `no`, and `off`.

If you want to force refresh the `egeria-main` image (even when `egeria-quickstart-platform:local` already exists), run:

```bash
./quick-start-local --refresh-platform
```

This triggers a rebuild of the platform service with `docker compose build --pull` so Docker checks for a newer
`quay.io/odpi/egeria-platform:latest` base image.

Every run installs the latest pyegeria release from PyPI into `pyegeria-web` and `jupyter`, unless a
version has been pinned. The resolved version is the cache key for pyegeria's own Docker layer, so when the
latest hasn't changed the step is a cache hit; when it has, only that layer rebuilds. An upgrade done
*inside* a running container (`pip install --upgrade pyegeria`) is lost the next time the container is
recreated (e.g. by `--refresh-platform`), so use these flags instead:

```bash
./quick-start-local --pyegeria-version 6.1.20   # pin a release; saved in .env.pyegeria, persists across re-runs
./quick-start-local --pyegeria-version latest   # clear the pin, go back to tracking the latest
./quick-start-local --no-refresh-pyegeria       # skip the PyPI check and keep the images' current version
./quick-start-local --refresh-pyegeria          # force the pyegeria layer to rebuild even if the version is unchanged
```

Using either the **Docker Desktop** application or the docker command line you can see the new containers running. To do this with the docker command line, you can issue:

`docker ps`

The environment is ready to be used. 

You can control the containers with docker compose commands - see [docker compose](https://docs.docker.com/reference/cli/docker/compose/). These commands can be used to manage and use the docker containers.

To access jupyter, open a browser to `http://localhost:8888`. At the password prompt, enter `egeria`. This should open up your notebook environment.

>Note: You only need to use the --build option if you want to rebuild the Jupyter image.

## Advanced: Manual Docker Compose

If you prefer to run Docker Compose manually instead of using the root scripts, from this directory you can run:

```bash
docker compose -f egeria-quickstart.yaml build --pull
docker compose -f egeria-quickstart.yaml up -d --pull always
```

For the local overlay (host-gateway mappings):

```bash
docker compose \
  -f egeria-quickstart.yaml \
  -f egeria-quickstart-local.yaml \
  build --pull

docker compose \
  -f egeria-quickstart.yaml \
  -f egeria-quickstart-local.yaml \
  up -d --pull always
```

For the multi-host overlay (external Kafka listeners / FQDN):

```bash
docker compose \
  -f egeria-quickstart.yaml \
  -f egeria-quickstart-cluster.yaml \
  build --pull

docker compose \
  -f egeria-quickstart.yaml \
  -f egeria-quickstart-cluster.yaml \
  up -d --pull always
```

To bypass the local build cache during the manual build step, add `--no-cache`:

```bash
docker compose -f egeria-quickstart.yaml build --pull --no-cache
```

## HTTPS

`./quick-start-local` always brings up Apache's HTTPS listener, on port 8843 by default. If no
certificate is configured, it auto-generates a self-signed one on first run (via
`generate-certs.sh`, into `runtime-volumes/certs-quickstart`) — your browser will warn once,
which is expected. To use a real certificate instead, create
`compose-configs/egeria-quickstart/.env.ssl` (gitignored) with:

```ini
CERT_DIR=/path/to/dir/containing/server.crt+server.key+server-ca.crt
```

### Demo mode

Demo mode additionally activates user registration and authentication, and moves HTTPS to port
443 with a required real certificate. Run:

```bash
./quick-start-local --demo
```

On first run it prompts for a TLS certificate directory and admin credentials, saves them to
`compose-configs/egeria-quickstart/.env.demo` (gitignored), and generates the Apache SSL
server-name config automatically. Subsequent `--demo` runs reuse the saved values.

For full details including manual configuration, see
[`PyegeriaWebHandler/demo-mode.md`](PyegeriaWebHandler/demo-mode.md).

For the full HTTPS/TLS mechanism across all deployment modes (self-signed generation,
`.env.ssl`, Let's Encrypt acquisition/renewal) and the auth model differences between
quickstart/`--demo`/freshstart, see
[`docs/SECURITY-CONFIGURATION.md`](../../docs/SECURITY-CONFIGURATION.md) at the repo root.

## Secrets Location for Quickstart

- Quickstart platform secrets are resolved at `/deployments/secrets` inside the container.
- By default, these come from the Egeria platform image — no host secrets mount is required.
- To customise secrets, add a volume mount from a host directory to `/deployments/secrets` in `egeria-quickstart.yaml`.
- `exchange-quickstart/loading-bay/secrets` is optional and not used by the default startup.

## Local vs multi-host

The two startup scripts apply different Docker Compose overlays on top of `egeria-quickstart.yaml`:

| | `./quick-start-local` | `./quick-start-multi-host` |
|---|---|---|
| Overlay file | `egeria-quickstart-local.yaml` | `egeria-quickstart-cluster.yaml` |
| Extra behaviour | Adds `extra_hosts` mapping `${HOST_FQDN} → host-gateway` inside the Egeria, Jupyter, and pyegeria-web containers | No `extra_hosts` — relies on real DNS resolution of `${HOST_FQDN}` |
| When to use | Single machine (laptop / workstation). Lets containers reach the host by its hostname without a real DNS entry. Required on Linux where `host.docker.internal` is not automatic. | When Egeria needs to be reachable from **other machines** on your network. `HOST_FQDN` must resolve via DNS on all participating hosts. |

Neither overlay changes ports, images, or volumes — the only difference is whether containers get a synthetic `/etc/hosts` entry for the host machine's hostname.

## Dr. Egeria Processing

This environment includes support for processing Markdown files containing Dr. Egeria commands. This is primarily intended for use with Obsidian but can be used by any MCP client.

The `PyegeriaWebHandler` service (host port 8800 direct / 8885 via Apache) provides both a REST API and a **Model Context Protocol (MCP)** server for interacting with Dr. Egeria.

- **Obsidian Plugins**: Use the **Call Dr. Egeria** plugin. It's MCP-based (over SSE) with a "Content-First" architecture that eliminates Docker permission issues. See the [Obsidian Plugins README](../../obsidian-plugins/call-dr-egeria/README.md) for details.
- **MCP Server**: The backend exposes Dr. Egeria commands as MCP tools via both **SSE (HTTP)** and **stdio**. This allows integration with assistants like Claude Desktop or any MCP-compatible environment.
- **Documentation**: For comprehensive setup and configuration instructions, see the [Unified Plugin Guide](../../Configuring%20and%20Using%20the%20Call%20Dr.%20Egeria%20Obsidian%20Plugin.md).

## Next Steps

Now that your Egeria environment is running and configured it is waiting for you to make requests. 
Some tutorials for working with Egeria can be found at [Tutorials](https://egeria-project.org/education/tutorials/). For those that want to try the new python client, you can find a quick introduction at [pyegeria](https://getting-started-with-egeria.pdr-associates.com/recipe-6-charming-python.html). 
Some short youtube videos are available on the [Egeria youtube channel](https://www.youtube.com/@egeria-project). 
In particular, there are some videos on the *hey_egeria* command line interface and *Basic Egeria Business Glossaries with hey_egeria*
that may be useful starting points.


As always, your feedback and participation are welcome. 


License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project.
   





## Troubleshooting

### myEgeria fails to load when accessed via hostname (not localhost)

**Symptom:** The myEgeria / My Profile page shows a blank screen or the textual app never connects when the browser URL uses a hostname other than `localhost` (e.g. `https://myserver.local:8843/my-egeria`).

**Root cause:** `textual-serve` uses the `MY_EGERIA_PUBLIC_URL` environment variable to emit same-origin WebSocket and static-asset URLs. Without it set correctly, it emits `http://0.0.0.0:8020/...` or `https://localhost:8843/...` URLs that the browser blocks under its same-origin policy.

**Fix:** Set `SITE_URL` in `compose-configs/egeria-quickstart/.env.ssl` (or `.env.demo` in `--demo` mode) to the base URL your browser uses to reach the portal (no trailing slash):

```bash
SITE_URL=https://myserver.local:8843
```

When `SITE_URL` is set, both the pyegeria-web service and the myEgeria service pick it up automatically. When `SITE_URL` is not set, the default `https://localhost:8843` is used — so no change is needed for single-machine `localhost` access.

Note: `quick-start-local` regenerates `.env` on every run — `.env.ssl` (or `.env.demo`) is the persisted file it reads `SITE_URL` from and re-appends to `.env` each time, so it survives regeneration.

---

### Proxy Error: DNS lookup failure for `quickstart-pyegeria-web`

Apache returns this when it can't resolve a container hostname — almost always because the containers are not attached to `egeria_network`.

**Root cause:** `egeria_network` is declared `external: true` in both compose files. If the quickstart stack is brought up before `ensure-shared-infra.sh` runs (or after a hard stop that left the network empty), containers attach to the default Podman network instead.

**Fix:** Podman 3.x requires a full stop/start cycle (not just restart) to activate a new network attachment, otherwise you get "address already in use" on the port rebind.

```bash
for c in quickstart-egeria-main quickstart-pyegeria-web quickstart-web-server \
          quickstart-jupyter-work-full obsidian-quickstart quickstart-my-profile \
          egeria-shared-postgres egeria-shared-kafka \
          egeria-shared-openlineage-proxy-backend; do
  podman network connect egeria_network $c 2>/dev/null
  podman stop $c && podman start $c && echo "restarted $c" || echo "failed $c"
done
```

After connecting a container to a new network, any container that proxies *to* it (e.g. `quickstart-web-server` → `quickstart-my-profile`) must also be restarted so its DNS resolver picks up the new peer:
```bash
podman stop quickstart-web-server && podman start quickstart-web-server
```

**Prevention:** always start via `compose-configs/shared-infra/ensure-shared-infra.sh` before bringing up the quickstart stack — that script creates `egeria_network` if it doesn't exist.

---

## Configuration files

### pyegeria / Jupyter config (`exchange-quickstart/config/config_workspaces.json`)

This file is **generated automatically** by `quick-start-local` on every run — do not commit it.

The template is tracked at `exchange-quickstart/config/config_workspaces.json.template`. It contains `localhost` as a placeholder for all host-dependent URLs. At startup, `gen-env.sh` copies the template and replaces `localhost` with the machine's fully-qualified hostname, then injects the correct Egeria service names (`qs-*`). The result is written to `exchange-quickstart/config/config_workspaces.json` and mounted into the Jupyter container at `/home/jovyan/config/`.

| File | Status | Purpose |
|------|--------|---------|
| `exchange-quickstart/config/config_workspaces.json.template` | Tracked in git | Pristine template with `localhost` placeholders — edit this to change defaults |
| `exchange-quickstart/config/config_workspaces.json` | Gitignored, generated at runtime | Machine-specific config read by Jupyter / pyegeria |

To change a persistent default (e.g. `console_width`, `User Profile`), edit the `.template` file. The runtime file is regenerated fresh on every startup.

---

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
