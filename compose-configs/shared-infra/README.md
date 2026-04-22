<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Shared infrastructure for Egeria workspaces

This directory contains the shared Kafka, PostgreSQL, and OpenLineage proxy infrastructure used by both the `egeria-quickstart`
and `egeria-freshstart` deployments.

The shared stack exposes:

- Kafka on `9192`, `9193`, `9194`
- PostgreSQL on `5442`
- OpenLineage proxy on `6000`, `6001`
- the external Docker network `egeria_network`

Both root startup scripts (`quick-start-*` and `fresh-start-*`) call `ensure-shared-infra.sh`, which:

1. generates `.env` for the shared stack,
2. creates `egeria_network` if needed,
3. starts OpenLineage proxy, Kafka, and PostgreSQL when they are missing or stopped,
4. waits until all services are ready.

`ensure-shared-infra.sh` now also refreshes images during startup:

- it rebuilds the local proxy image with `docker compose build --pull`, and
- it starts services with `docker compose up -d --pull always` so Docker checks for newer remote images before using cached ones.

To bypass the local build cache for the proxy build, set `NO_CACHE=1` before running the script.

## Image pinning and optional hardened Kafka

`gen-env.sh` now writes image references into `compose-configs/shared-infra/.env`:

- `SHARED_KAFKA_IMAGE` (default pinned digest for the current Bitnami legacy Kafka image)
- `SHARED_POSTGRES_IMAGE` (default pinned digest for PostgreSQL)
- `USE_HARDENED_KAFKA` (`0` by default)
- `KAFKA_HARDENED_IMAGE` (placeholder value you replace with your hardened image)

By default, startup behavior is unchanged except image references are pinned. To opt into a hardened Kafka image, set:

```bash
USE_HARDENED_KAFKA=1
KAFKA_HARDENED_IMAGE=<your-compatible-hardened-kafka-image>
```

When enabled, `ensure-shared-infra.sh` adds `shared-infra.hardened-kafka.yaml` as a compose override.

> Note: the hardened image must be compatible with the current Kafka configuration (KRaft single-node and `KAFKA_CFG_*` environment variables).
> The current tested override is suitable for smoke tests: it uses a writable temporary KRaft log path because the hardened
> image runs as a non-root user and does not yet align with the existing `/bitnami/kafka` persistent-volume permissions.

You can also manage the shared stack directly from this directory:

```bash
./ensure-shared-infra.sh
NO_CACHE=1 ./ensure-shared-infra.sh
docker compose -p egeria-shared-infra -f shared-infra.yaml build --pull proxy
docker compose -p egeria-shared-infra -f shared-infra.yaml up -d --pull always proxy kafka postgres
docker compose -p egeria-shared-infra -f shared-infra.yaml ps
docker compose -p egeria-shared-infra -f shared-infra.yaml down
```

To run with a hardened Kafka override manually:

```bash
docker compose \
  -p egeria-shared-infra \
  -f shared-infra.yaml \
  -f shared-infra.hardened-kafka.yaml \
  up -d --pull always proxy kafka postgres
```

To force a clean rebuild of the proxy image when running Docker Compose manually, add `--no-cache` to the build step:

```bash
docker compose -p egeria-shared-infra -f shared-infra.yaml build --pull --no-cache proxy
```

## Validation and rollback

Smoke-check after changes:

```bash
./compose-configs/shared-infra/ensure-shared-infra.sh
docker compose -p egeria-shared-infra -f compose-configs/shared-infra/shared-infra.yaml ps
./quick-start-local
./fresh-start-local
```

Rollback to current non-hardened path:

```bash
USE_HARDENED_KAFKA=0
# Optional: keep KAFKA_HARDENED_IMAGE for later tests
./compose-configs/shared-infra/ensure-shared-infra.sh
```

