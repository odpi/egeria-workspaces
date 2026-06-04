<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project 2024. -->

# Overview

This **egeria-workspaces** repository provides a runtime environment for learning, experimenting and using Egeria. 
The default configuration sets up a full Egeria system and provides pre-built content to help you get started. 

This environment is not designed for enterprise-wide use. Please see the [Planning Guide](https://egeria-project.org/guides/planning/)
for more information about designing bespoke Egeria deployments, such as Cloud Native approaches and the use of
Helm charts to configure Kubernetes clusters. 
For further help and advice, please feel free to engage with the community on our [slack channel](https://lfaifoundation.slack.com/join/shared_invite/zt-o65errpw-gMTbwNr7FnNbVXNVFkmyNA%E2%80%8B#/shared-invite/email) - we'd love your feedback and participation.

## Requirements

**Egeria Workspaces** uses Docker compose to deploy docker containers, creating a usable environment. So, at a minimum,
you need to have docker and docker compose compatible software installed. We test **Egeria Workspaces** using
[Docker Desktop](https://www.docker.com/get-started/) but **podman** and **podman-compose** should also work 
[Podman](https://podman.io/). See [Monitoring Podman with PyCharm](Monitoring%20Podman%20with%20PyCharm.md) for IDE integration steps.

>Note: The minimum level of Egeria (egeria-platform) required is 6.0. If you have older images you should either remove these old images or modify 
 the docker compose yaml scripts to use the image tag 'stable' (referring to 6.0 production release) or a specific post 6.0 release.


## Quickstart and Freshstart

This repository provides two isolated flavors of Egeria deployment that share a common Kafka, PostgreSQL, and OpenLineage proxy infrastructure stack.

[Egeria Quickstart](https://egeria-project.org/egeria-workspaces/quick-start/overview/) is a docker-based deployment that runs on port `9443` and provides a single [platform deployment of Egeria](https://egeria-project.org/guides/admin/configuring-the-omag-server-platform/).  It is populated with users and data for the [Coco Pharmaceuticals](https://egeria-project.org/practices/coco-pharmaceuticals/) training scenarios. This is the environment to use if you want to explore Egeria's capabilities and learn how to use them.

[Freshstart](https://egeria-project.org/egeria-workspaces/fresh-start/overview/) is also a docker-based deployment that runs on port `8443`, providing a single platform deployment of Egeria.  It is populated with clean defaults so you can set up your own environment.  This environment could support your own work, or a small team.  Freshstart is a secure environment that can host private data.  It does not have, however, the ability to scale to support a large organization.  This would require a different deployment architecture using multiple platforms and probably Kubernettes.  Details of setting up a larger company deployment can be found in Egeria's [planning guide](https://egeria-project.org/guides/planning/). 

The following table summarizes the differences between the two deployments.  The `local` scripts are for single-machine use, while the `multi-host` scripts enable Egeria to be called from other machines on your network (see [section on local vs multi-host](#local-vs-multi-host) below).

|                            | **egeria-quickstart**                                            | **egeria-freshstart**                                                                                                                   |
|----------------------------|------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| Start script (single host) | `./quick-start-local`                                            | `./fresh-start-local`                                                                                                                   |
| Start script (multi-host)  | `./quick-start-multi-host`                                       | `./fresh-start-multi-host`                                                                                                              |
| Egeria platform            | `https://localhost:9443`                                         | `https://localhost:8443`                                                                                                                |
| Jupyter                    | `http://localhost:8888` (password: `egeria`)                     | `http://localhost:7888` (password: `egeria`)                                                                                            |
| Web                        | `http://localhost:8885`                                          | `http://localhost:7885`                                                                                                                 |
| Servers                    | `qs-*` (Coco Pharmaceuticals defaults)                           | `fs-*` (clean defaults)                                                                                                                 |
| Platform secrets           | Image-bundled (no host mount required)                           | Seeded from `compose-configs/egeria-freshstart/secrets/` templates into `runtime-volumes/freshstart-platform-data/secrets` on first run |
| Exchange tree              | `exchange-quickstart/`                                           | `exchange-freshstart/`                                                                                                                  |
| Runtime data               | `runtime-volumes/quickstart-platform-data/`                      | `runtime-volumes/freshstart-platform-data/`                                                                                             |
| Further Information        | [Quickstart README](compose-configs/egeria-quickstart/README.md) | [Freshstart README](compose-configs/egeria-freshstart/README.md)                                                                        |

All four scripts automatically ensure the shared infrastructure stack in `compose-configs/shared-infra/` is running.
This shared stack provides Kafka, PostgreSQL, and the OpenLineage proxy used by both deployments.
Shared-infra image references are pinned in `compose-configs/shared-infra/.env` by default, including the hardened
Kafka image and a persistent host-side Kafka data path.

## Host port allocation

Host (published) ports follow a consistent scheme so the two environments can run side by side
without colliding, and to keep clear of ports commonly used by other applications (notably `8000`):

- **Quickstart → `88xx`**, **Freshstart → `78xx`**, with the **same last two digits = same function**
  in both environments.
- Only the **published host port** follows this scheme; **container-internal ports are unchanged**
  (the Apache reverse proxy reaches services container-to-container, so it is unaffected).
- The platform, Kafka and PostgreSQL ports are intentionally **left as-is** (well-established defaults).

| Function | Quickstart | Freshstart | Container | Notes |
|----------|------------|------------|-----------|-------|
| Egeria platform (+ JVM debug) | `9443` / `5005` | `8443` / `5006` | same | **fixed — not renumbered** |
| Apache web portal | **`8885`** | **`7885`** | `8085` | main entry point |
| Jupyter (notebook / debug) | **`8888`** / `8889` | **`7888`** / `7889` | `7888` / `5678` | password `egeria` |
| pyegeria-web (FastAPI/MCP) | **`8800`** | **`7800`** | `8000` | moved off host `8000` |
| my-egeria (`my-profile` TUI) | **`8820`** | *`7820`* (reserved) | `8020` | textual-serve via Apache `/my-egeria/` |
| Egeria Advisor | **`8880`** | **`7880`** | external | not in compose; portal links to `EGERIA_ADVISOR_URL` (was `8080`) |
| ProjectExplorer | *`8830`* (planned) | *`7830`* (reserved) | tbd | see BACKLOG `PORT-7` |
| Obsidian (web / https) | **`8860`** / `8861` | — | `3000` / `3001` | optional |
| Shared Kafka | `9192`–`9194` | `9192`–`9194` | same | **fixed — shared-infra** |
| Shared PostgreSQL | `5442` | `5442` | same | **fixed — shared-infra** |
| Shared OpenLineage proxy | `6000` / `6001` | `6000` / `6001` | same | shared-infra |

> One caveat: quickstart Jupyter uses `8888`, which is also Jupyter's own default port — it will
> collide only if you run another Jupyter server on the host. See `BACKLOG.md` → *Ports & Networking*
> for the full rationale and the migration items (`PORT-1` … `PORT-8`).

## Servers

There are four [servers](https://egeria-project.org/concepts/omag-server/) configured and running on Egeria's platform:

| Server Type                                                                         | Quickstart Server Name  | Freshstart Server Name  | Description                                                                                                                                                                                    |
|-------------------------------------------------------------------------------------|-------------------------|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [View Server](https://egeria-project.org/concepts/view-server/)                     | `qs-view-server`        | `fs-view-server`        | The server that supports Egeria's REST API.  This is the name of the server to use when configuring `pyegeria`.                                                                                |
| [Integration Daemon](https://egeria-project.org/concepts/integration-daemon/)       | `qs-integration-daemon` | `fs-integration-daemon` | The server that hosts the [integration connectors](https://egeria-project.org/concepts/integration-connector/).  This are the long-running services that synchronize metadata between systems. |
| [Engine Host](https://egeria-project.org/concepts/engine-host/)                     | `qs-engine-host`        | `fs-engine-host`        | The server that runs [governance services](https://egeria-project.org/concepts/governance-service/).                                                                                           |
| [Metadata Access Store](https://egeria-project.org/concepts/metadata-access-store/) | `qs-metadata-store`     | `fs-metadata-store`     | The server that hosts the metadata repository.                                                                                                                                                 |

### Using the Dr. Egeria Obsidian Plugins

Dr. Egeria commands can be executed directly from your Obsidian vault using one of the available plugins:

1.  **Calling the Dr. (MCP) - RECOMMENDED**: A next-generation plugin using the Model Context Protocol (MCP). It features dynamic command discovery, hot-reloading of specifications, and rich diagnostic feedback. This plugin uses a "Content-First" architecture where note content is sent to the backend and the results are written directly to the vault via the Obsidian API, eliminating Docker permission issues.
    - **Source**: `obsidian-plugins/calling-the-dr/`
    - **Documentation**: [Calling the Dr. (MCP) Guide](Configuring and Using the Calling Dr. Egeria Obsidian Plug-in.md)

2.  **Call Dr. Egeria (Legacy)**: The original plugin using a direct REST API.
    - **Source**: `obsidian-plugins/call-dr-egeria/`
    - **Documentation**: [Call Dr. Egeria README](obsidian-plugins/call-dr-egeria/README.md)

- **Detailed Profiles**: For specific configuration profiles aligned with this workspace (e.g., for `work/Work-Obsidian` or `coco-workbooks`), see [OBSIDIAN_PROFILES.md](compose-configs/egeria-quickstart/OBSIDIAN_PROFILES.md).

### Using both MCP servers together

You can configure the `pyegeria` MCP server and the Dr. Egeria MCP server from `PyegeriaWebHandler` in the same MCP client configuration. The recommended client-side aliases are `pyegeria` for the pyegeria package server and `dr-egeria` for the Dr. Egeria server; these names only need to be unique within the `mcpServers` block.

See `exchange-quickstart/claude_desktop_config.json.md` for a combined example configuration that includes both servers. For Dr. Egeria MCP details, tool descriptions, and environment settings, see `compose-configs/egeria-quickstart/PyegeriaWebHandler/README.md` or `compose-configs/egeria-freshstart/PyegeriaWebHandler/README.md`.

The quickstart examples use `https://localhost:9443` and `qs-view-server`; if you are using freshstart, switch those values to the appropriate freshstart platform URL and server names.

#### Quick Example

After configuring both servers in `~/.config/Claude/claude_desktop_config.json`, you can interact with Egeria like this:

```
User: "Using the Dr. Egeria MCP server, create a new glossary called 'Product Catalog' 
       and then list all glossaries to confirm it was created."

Claude: I'll create the glossary using Dr. Egeria commands and then list all glossaries.

[Calls dr_egeria_run_block with Create Glossary command]
✓ Glossary 'Product Catalog' created successfully

[Calls egeria_list_glossaries]
Available glossaries:
• Data Assets (id: glossary-001)
• Product Catalog (id: glossary-002)  [newly created]
• Business Concepts (id: glossary-003)
```

You can also switch to the `pyegeria` server for lower-level metadata queries:

```
User: "Using the pyegeria MCP server, what are the available metadata stores?"

Claude: I'll query the available metadata stores.

[Calls pyegeria tools]
Available metadata stores:
• qs-metadata-store (primary store, type: metaverse)
• qs-archive-store (archive store, type: archive)
```

## Local vs multi-host

The `-local` scripts add a synthetic `/etc/hosts` entry inside each container that maps your machine's hostname to Docker's `host-gateway` address, so containers can resolve the host by name without a real DNS entry. This is required on Linux (where `host.docker.internal` is not automatic) and the right choice for any single-machine setup.

The `-multi-host` scripts omit that mapping and expect `HOST_FQDN` to resolve via real DNS — use these only when Egeria needs to be reachable from other machines on your network.

The startup scripts now always:

- rebuild local compose images with `docker compose build --pull`, so Docker checks for newer base images such as `quay.io/odpi/egeria-platform:latest`, and
- start containers with `docker compose up -d --pull always`, so Docker checks for newer remote images before using cached ones.

If you want a completely clean rebuild that ignores Docker's local build cache, set `NO_CACHE=1` when starting either deployment:

```bash
NO_CACHE=1 ./quick-start-local
NO_CACHE=1 ./fresh-start-local
```

Accepted truthy values are `1`, `true`, `yes`, and `on`. Falsey values are unset, `0`, `false`, `no`, and `off`.

If you specifically want to force-refresh the quickstart or freshstart platform image base (even when a local platform
image already exists), run:

```bash
./quick-start-local --refresh-platform
./fresh-start-local --refresh-platform
```

## Contents of this repository

**egeria-workspaces** consists of a number of artifacts reflected by the folder structure itself. Here is a quick tour:
### compose-configs
Subdirectories contain artifacts for different deployments of Egeria along with optional runtimes often used with Egeria.
The deployments provide **docker compose** scripts to orchestrate the building, configuration and startup of the components needed.
Here is the break-down of the configurations:

#### shared-infra
This compose stack provides the shared Kafka and PostgreSQL services used by both deployments. It is managed
automatically by the start scripts, and can also be managed directly in `compose-configs/shared-infra/`.

#### egeria-quickstart
This provides the Coco Pharmaceuticals quickstart deployment and runs on port `9443`.

#### egeria-freshstart
This provides the freshstart deployment and runs on port `8443`.

#### optional-associated-runtimes
This folder contains some sample docker compose scripts to start some other runtimes
that we often use with Egeria. Currently this includes:
* airflow & marquez - Apache Airflow is a popular open source workflow runtime and marquez offers
some very nice visualization of open lineage graphs.
* superset - Apache Superset is an open source reporting and dashboard tool.
* unity-catalog - Open source catalog for managing physical artifacts in a lakehouse environment.
* deltalake-spark - Open source lakehouse runtime for managing data in a lakehouse environment.
* milvus—Open source vector database for efficient similarity search and clustering of large datasets.
* mlflow—Open source platform for managing the end-to-end machine learning lifecycle.

### exchange-quickstart / exchange-freshstart
These folders support file-based exchange between Egeria containers, Jupyter, and the host file-system for each deployment.
Quickstart and freshstart each have an isolated exchange tree.
#### coco-data-lake
A file location supporting Coco Pharmaceuticals scenarios.
#### distribution-hub
The distribution hub is where Egeria can place information and results that it generates so that they are
easily visible to the users and Jupyter, This information currently includes:
- logs - Egeria audit logs (if file based event logging has been configured)
- surveys - Survey reports generated by Egeria based on user request or automation.
#### landing-area
The *landing-area* directory (or any of its subdirectories) are monitored by the *qs-integration-daemon* server.
If you add files under this directory, they will be automatically classified using their file name and file extension,
and then catalogued into the *qs-metadata-store* metadata repository as [assets](https://egeria-project.org/concepts/asset/).

#### loading-bay
The *loading-bay* directory is where users place information to be ingested by Egeria.
There are sub-directories for different kinds of information:

- glossary - for importing and exporting glossary terms
- open-metadata-archives - for importing open-metadata-archives
- secrets - optional host-side secrets location for custom workflows in exchange trees.
  Runtime platform secrets are resolved at `/deployments/secrets` inside the container:
  - quickstart: image-bundled default secrets (no host secrets mount by default)
  - freshstart: seeded from `compose-configs/egeria-freshstart/secrets/` templates into
    `runtime-volumes/freshstart-platform-data/secrets` on first run; customise in place thereafter

### runtime-volumes
The information in these folders are used by the Runtimes. They are not for the general
user to use. Externalizing runtime information here, rather than embedded within the containers,
means that if containers are upgraded or destroyed, the environment can still be recovered.
Currently there are sub-directories here for:
* airflow-volumes
* quickstart-platform-data
* quickstart-apache-web
* freshstart-platform-data
* freshstart-apache-web
* unity-coco
* unitycatalog2

### work
This folder is meant for you to put your own private working files for use with Egeria and
Jupyter. The directory is mounted and visible within both Egeria and Jupyter runtimes. 
Your additions are ignored by Git.

----
License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project. of of this 