<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project 2024. -->

# Overview

This **egeria-workspaces** repository provides a runtime environment for learning, experimenting and using Egeria. 
The default configuration sets up a full Egeria system and provides pre-built content to help you get started. 

This environment is not designed for enterprise-wide use. Please see the [Planning Guide](https://egeria-project.org/guides/planning/)
for more information about designing bespoke Egeria deployments, such as Cloud Native approaches and the use of
Helm charts to configure Kubernetes clusters. 
For further help and advice, please feel free to engage with the community on our [slack channel](https://lfaifoundation.slack.com/join/shared_invite/zt-o65errpw-gMTbwNr7FnNbVXNVFkmyNA%E2%80%8B#/shared-invite/email) - we'd love your feedback and participation.

# Requirements

**Egeria Workspaces** uses Docker compose to deploy docker containers, creating a usable environment. So, at a minimum,
you need to have docker and docker compose compatible software installed. We test **Egeria Workspaces** using
[Docker Desktop](https://www.docker.com/get-started/) but **podmand** and **podman-compose** should also work 
[Podman](https://podman.io/). 

>Note: The minimum level of Egeria (egeria-platform) required is 6.0. If you have older images you should either remove these old images or modify 
 the docker compose yaml scripts to use the image tag 'stable' (referring to 6.0 production release) or a specific post 6.0 release.


# Quick Start (recommended)
This repository now provides two isolated deployment flavors with shared Kafka and PostgreSQL infrastructure.

## Quickstart deployment (Coco Pharmaceuticals defaults)

- `./quick-start-local`
- `./quick-start-multi-host`

After startup, use:

- Egeria platform: `https://localhost:9443`
- Jupyter: `http://localhost:7888` (password: `egeria`)
- Web: `http://localhost:8085`

## Freshstart deployment (clean fs-* defaults)

- `./fresh-start-local`
- `./fresh-start-multi-host`

After startup, use:

- Egeria platform: `https://localhost:8443`
- Jupyter: `http://localhost:7889` (password: `egeria`)
- Web: `http://localhost:8086`

All four scripts automatically ensure the shared infrastructure stack in `compose-configs/shared-infra/` is running.
This shared stack now includes Kafka, PostgreSQL, and the OpenLineage proxy.

# Contents
**egeria-workspaces** consists of a number of artifacts reflected by the folder structure itself. Here is a quick tour:
## compose-configs
Subdirectories contain artifacts for different deployments of Egeria along with optional runtimes often used with Egeria.
The deployments provide **docker compose** scripts to orchestrate the building, configuration and startup of the components needed.
Here is the break-down of the configurations:

### shared-infra
This compose stack provides the shared Kafka and PostgreSQL services used by both deployments. It is managed
automatically by the start scripts, and can also be managed directly in `compose-configs/shared-infra/`.

### egeria-quickstart
This provides the Coco Pharmaceuticals quickstart deployment and runs on port `9443`.

### egeria-freshstart
This provides the freshstart deployment and runs on port `8443`.

### optional-associated-runtimes
This folder contains some sample docker compose scripts to start some other runtimes
that we often use with Egeria. Currently this includes:
* airflow & marquez - Apache Airflow is a popular open source workflow runtime and marquez offers
some very nice visualization of open lineage graphs.
* superset - Apache Superset is an open source reporting and dashboard tool.
* unity-catalog - Open source catalog for managing physical artifacts in a lakehouse environment.
* deltalake-spark - Open source lakehouse runtime for managing data in a lakehouse environment.
* milvus—Open source vector database for efficient similarity search and clustering of large datasets.
* mlflow—Open source platform for managing the end-to-end machine learning lifecycle.

### other-egeria-deployments
While the egeria-quickstart environment is a good starting point for most folk, we've also included
some other docker scripts to support some simpler deployments. The available deployments are:

* egeria-platform-compose - deploys Egeria with an XTDB file based repository along with Kafka.
* egeria-platform-jupyter-compose - additionally adds a Jupyter server
* egeria-platform-postgres-compose - deploys the postgres database for use with Egeria, and Kafka.
* coco-labs-compose - an environment for working with the Egeria Coco Pharmaceuticals training scenarios (under construction)

These simpler configurations do not externalize 
their configurations and only share a subset of the folders. They provide configurations for these servers:
* active-metadata-store
* simple-metadata-store
* integration-daemon
* engine-host
* view-server

More details can be found in the README.md files within this folder.
## exchange-quickstart / exchange-freshstart
These folders support file-based exchange between Egeria containers, Jupyter, and the host file-system for each deployment.
Quickstart and freshstart each have an isolated exchange tree.
### coco-data-lake
A file location supporting Coco Pharmaceuticals scenarios.
### distribution-hub
The distribution hub is where Egeria can place information and results that it generates so that they are
easily visible to the users and Jupyter, This information currently includes:
- logs - Egeria audit logs (if file based event logging has been configured)
- surveys - Survey reports generated by Egeria based on user request or automation.
### landing-area
The *landing-area* directory (or any of its subdirectories) are monitored by the *qs-integration-daemon* server.
If you add files under this directory, they will be automatically classified using their file name and file extension,
and then catalogued into the *qs-metadata-store* metadata repository as [assets](https://egeria-project.org/concepts/asset/).

### loading-bay
The *landing-bay* directory is where users place information to be ingested by Egeria.
There are sub-directories for different kinds of information:

- glossary - for importing and exporting glossary terms
- open-metadata-archives - for importing open-metadata-archives
- secrets - optional host-side secrets location for custom workflows in exchange trees.
  Runtime platform secrets now live under each deployment runtime volume at
  `/deployments/secrets` inside the container:
  - quickstart: `runtime-volumes/quickstart-platform-data/secrets`
  - freshstart: `runtime-volumes/freshstart-platform-data/secrets`

## runtime-volumes
The information in these folders are used by the Runtimes. They are not for the general
user to use. Externalizing runtime information here, rather than embedded within the containers,
means that if containers are upgraded or destroyed, the environment can still be recovered.
Currently there are sub-directories here for:
* airflow-volumes
* quickstart-platform-data
* quickstart-apache-web
* freshstart-platform-data
* freshstart-apache-web
* unitycatalog1 
* unitycatalog2

## work
This folder is meant for you to put your own private working files for use with Egeria and
Jupyter. The directory is mounted and visible within both Egeria and Jupyter runtimes. 
It is ignored by Git.

## workspaces
This set of folders contains examples, samples, utilities and other artifacts useful to 
getting started with Egeria. Please explore. Extend if desired, and if you want to contribute
your own content to the community feel free to contact us via Slack or email.

----
License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project.