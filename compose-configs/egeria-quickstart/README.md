<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Overview
This directory contains the *egeria-quickstart* docker compose script and supporting files, to support the deployment of Egeria for experimentation,
development, and learning. Rather than having to install Egeria, prerequisites and tools separately, these scripts make 
it easy to get a stack running quickly. This deployment configures and starts:

* Egeria on port 9443 and will automatically start the default servers.
* Jupyter is deployed using port 7888 so as not to interfere with other jupyter servers
* Apache Web Server on port 8085 and configured with `httpd.conf`.

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

PostgreSQL runs in the shared infra stack and provides the `egeria` database used by quickstart.

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
   * `./quick-start-local` — single-machine development (see [Local vs multi-host](#local-vs-multi-host))
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

The startup scripts now automatically refresh images more aggressively than before:

- local compose images are rebuilt with `docker compose build --pull`, which checks for newer base images before building, and
- containers are started with `docker compose up -d --pull always`, which checks for newer remote images before using cached ones.

If you want to force a completely clean rebuild that ignores Docker's local build cache, set `NO_CACHE=1` when starting the stack from the repository root:

```bash
NO_CACHE=1 ./quick-start-local
NO_CACHE=1 ./quick-start-multi-host
```

Accepted truthy values are `1`, `true`, `yes`, and `on`. Falsey values are unset, `0`, `false`, `no`, and `off`.

Using either the **Docker Desktop** application or the docker command line you can see the new containers running. To do this with the docker command line, you can issue:

`docker ps`

The environment is ready to be used. 

You can control the containers with docker compose commands - see [docker compose](https://docs.docker.com/reference/cli/docker/compose/). These commands can be used to manage and use the docker containers.

To access jupyter, open a browser to `http://localhost:7888`. At the password prompt, enter `egeria`. This should open up your notebook environment.

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

This environment includes support for processing Markdown files containing Dr. Egeria commands. This is primarily intended for use with Obsidian.

The `PyegeriaWebHandler` service (port 8085) handles processing requests and can be configured to work with multiple Obsidian vaults.

For more details, see [Dr. Egeria Processing](./dr-egeria-processing.md).

## Next Steps

Now that your Egeria environment is running and configured it is waiting for you to make requests. 
Some tutorials for working with Egeria can be found at [Tutorials](https://egeria-project.org/education/tutorials/). For those that want to try the new python client, you can find a quick introduction at [pyegeria](https://getting-started-with-egeria.pdr-associates.com/recipe-6-charming-python.html). 
Some short youtube videos are available on the [Egeria youtube channel](https://www.youtube.com/@egeria-project). 
In particular, there are some videos on the *hey_egeria* command line interface and *Basic Egeria Business Glossaries with hey_egeria*
that may be useful starting points.


As always, your feedback and participation are welcome. 


License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project.
   





----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
