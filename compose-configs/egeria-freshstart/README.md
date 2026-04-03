<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Overview

This directory contains the *egeria-freshstart* deployment files.

The freshstart deployment is isolated from quickstart and uses:

- Egeria platform on `8443`
- Jupyter on `7889`
- Apache web on `8086`
- FastAPI handler on `8001`

Kafka (`9192/9193/9194`), PostgreSQL (`5442`), and the OpenLineage proxy (`6000/6001`) are shared infrastructure services managed from
`compose-configs/shared-infra`.

## Usage

From the repository root:

- `./fresh-start-local`
- `./fresh-start-multi-host`

These scripts:

1. copy `fs-*` server configurations to `runtime-volumes/freshstart-platform-data/data/servers`,
2. ensure shared Kafka/PostgreSQL are running,
3. generate `.env` in this directory,
4. start the freshstart compose stack.

They also build `freshstart-egeria-main` from `Dockerfile-egeria-platform`, which copies
no deployment-specific secrets into the image. Runtime secrets are mounted from the runtime volume.

The startup scripts now automatically refresh images during startup:

- local compose images are rebuilt with `docker compose build --pull`, which checks for newer base images before building, and
- containers are started with `docker compose up -d --pull always`, which checks for newer remote images before using cached ones.

If you want to force a completely clean rebuild that ignores Docker's local build cache, set `NO_CACHE=1` when starting the stack from the repository root:

```bash
NO_CACHE=1 ./fresh-start-local
NO_CACHE=1 ./fresh-start-multi-host
```

Accepted truthy values are `1`, `true`, `yes`, and `on`. Falsey values are unset, `0`, `false`, `no`, and `off`.

If you prefer to run Docker Compose manually from this directory, use:

```bash
docker compose -f egeria-freshstart.yaml build --pull
docker compose -f egeria-freshstart.yaml -f egeria-freshstart-local.yaml up -d --pull always
```

For the multi-host overlay:

```bash
docker compose -f egeria-freshstart.yaml build --pull
docker compose -f egeria-freshstart.yaml -f egeria-freshstart-cluster.yaml up -d --pull always
```

To bypass the local build cache during the manual build step, add `--no-cache`:

```bash
docker compose -f egeria-freshstart.yaml build --pull --no-cache
```

## Local vs multi-host

The two startup scripts apply different Docker Compose overlays on top of `egeria-freshstart.yaml`:

| | `./fresh-start-local` | `./fresh-start-multi-host` |
|---|---|---|
| Overlay file | `egeria-freshstart-local.yaml` | `egeria-freshstart-cluster.yaml` |
| Extra behaviour | Adds `extra_hosts` mapping `${HOST_FQDN} → host-gateway` inside the Egeria, Jupyter, and pyegeria-web containers | No `extra_hosts` — relies on real DNS resolution of `${HOST_FQDN}` |
| When to use | Single machine (laptop / workstation). Lets containers reach the host by its hostname without a real DNS entry. Required on Linux where `host.docker.internal` is not automatic. | When Egeria needs to be reachable from **other machines** on your network. `HOST_FQDN` must resolve via DNS on all participating hosts. |

Neither overlay changes ports, images, or volumes — the only difference is whether containers get a synthetic `/etc/hosts` entry for the host machine's hostname.

## Runtime and exchange locations

- runtime data: `runtime-volumes/freshstart-platform-data`
- runtime secrets: `runtime-volumes/freshstart-platform-data/secrets` (mounted to `/deployments/secrets`)
- apache runtime: `runtime-volumes/freshstart-apache-web`
- exchange tree: `exchange-freshstart`

## Secrets Location for Freshstart

- Freshstart platform secrets are resolved at `/deployments/secrets` inside the container.
- The runtime source is `runtime-volumes/freshstart-platform-data/secrets` (read-write mounted — not tracked by Git).
- **Template files** are kept in `compose-configs/egeria-freshstart/secrets/` (tracked by Git) and provide a starting point:
  - `egeria-user-directory.omsecrets` — user accounts, security groups, roles, and access controls
  - `egeria-servers.omsecrets` — NPA credentials and database passwords for the `fs-*` servers
  - `integration.omsecrets` — integration connector secrets (empty by default)
- The startup scripts (`fresh-start-local`, `fresh-start-multi-host`) automatically seed the runtime secrets directory from the templates on each run, **copying only files that do not already exist**. Customised files are never overwritten.
- To reset to defaults, delete `runtime-volumes/freshstart-platform-data/secrets/` and restart.
- `exchange-freshstart/loading-bay/secrets` is optional and not used by the default startup.

----
License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project.

