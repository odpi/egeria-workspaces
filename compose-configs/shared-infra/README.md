<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Shared infrastructure for Egeria workspaces

This directory contains the shared Kafka and PostgreSQL infrastructure used by both the `egeria-quickstart`
and `egeria-freshstart` deployments.

The shared stack exposes:

- Kafka on `9192`, `9193`, `9194`
- PostgreSQL on `5442`
- the external Docker network `egeria_network`

Both root startup scripts (`quick-start-*` and `fresh-start-*`) call `ensure-shared-infra.sh`, which:

1. generates `.env` for the shared stack,
2. creates `egeria_network` if needed,
3. starts Kafka and PostgreSQL when they are missing or stopped,
4. waits until both services are ready.

You can also manage the shared stack directly from this directory:

```bash
./ensure-shared-infra.sh
docker compose -p egeria-shared-infra -f shared-infra.yaml ps
docker compose -p egeria-shared-infra -f shared-infra.yaml down
```

