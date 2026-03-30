<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Overview

This directory contains the *egeria-freshstart* deployment files.

The freshstart deployment is isolated from quickstart and uses:

- Egeria platform on `8443`
- Jupyter on `7889`
- Apache web on `8086`
- OpenLineage proxy on `6002` and `6003`
- FastAPI handler on `8001`

Kafka (`9192/9193/9194`) and PostgreSQL (`5442`) are shared infrastructure services managed from
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
freshstart secrets from `compose-configs/egeria-freshstart/secrets` into `/deployments/loading-bay/secrets`.

## Runtime and exchange locations

- runtime data: `runtime-volumes/freshstart-platform-data`
- apache runtime: `runtime-volumes/freshstart-apache-web`
- exchange tree: `exchange-freshstart`
- deployment-local secrets: `compose-configs/egeria-freshstart/secrets`

## Secrets Location for Freshstart

- Freshstart platform secrets are sourced from `compose-configs/egeria-freshstart/secrets`.
- They are copied into the Egeria container image at `/deployments/loading-bay/secrets` during image build.
- The freshstart image includes only these freshstart secrets files:
  - `egeria-user-directory.omsecrets`
  - `egeria-servers.omsecrets`
  - `integration.omsecrets`
- `exchange-freshstart/loading-bay/secrets` is not required for normal freshstart startup.

----
License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project.

