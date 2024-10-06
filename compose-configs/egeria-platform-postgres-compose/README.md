<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Overview
This directory contains a sample Docker Compose scripts to support the deployment of Egeria for experimentation,
development, and learning. Rather than having to install Egeria, prerequisites and tools separately, these scripts make 
it easy to get a stack running quickly. 

This compose script builds on `egeria-platform-compose` by adding a postgres database container. Postgres is automatically
configured to support collecting different kinds of data from Egeria. Enabling this requires some additional Egeria configuration.

These are not meant for production use. Please see the [Planning Guide](https://egeria-project.org/guides/planning/)
for more information about designing Egeria deployments. The Egeria community has also created samples for other 
deployment styles, such as Cloud Native approaches and the use of Helm charts to configure Kubernetes clusters. These
options may be better starting points for production deployments - depending upon your requirements.
Please feel free to engage with the community on our slack channel - we'd love your feedback and participation.

# Contents

* egeria-platform-postgres-compose - a minimalist Egeria OMAG platform standalone deployment that includes Kafka and PostgreSQL as well as Egeria.

This egeria docker compose script is called **egeria-platform-postgres.yml**. After running this script, you will have a running environment 
that consists of a single Egeria runtime platform and the Apache Kafka event system. Information about configuring 
Egeria can be found at [Configuring Egeria](https://egeria-project.org/guides/admin/configuring-the-omag-server-platform/). 
We use standard, out-of-the-box configurations for both - a minimal amount of configuration for:

## Egeria Platform - Default Configuration
We use the Egeria platform docker image - [egeria-platform](https://hub.docker.com/r/odpi/egeria-platform).

* Port - By default the platform uses port 9443 and exposes this port to the host environment, This means that Egeria requests
can be made to platform URL **https://localhost:9443** or, if your environment is configured to support it, it can use 
the domain name of your host machine. 
* SSL - By default strict SSL is set to false 
* Auto-Started Servers - by default a useful set of Egeria Operational Metadata and Governance (OMAG) servers are pre-installed
and started when the Egeria platform is started. The pre-configured and started servers are:
  * simple-metadata-store
  * active-metadata-store
  * engine-host
  * integration-daemon
  * view-server
A description of these servers can be found at [sample configs](open-metadata-resources/open-metadata-deployment/sample-configs/README.md)
* Content Packs - pre-constructed information sets that can be used to configure Egeria and pre-load metadata, reference data and glossary data. See [Content Packs](https://egeria-project.org/content-packs/).
* Out-of-the-box Connectors - descriptions of the integration connectors can be found at [Integration Connectors](https://egeria-project.org/connectors/).

## Kafka - configured for Egeria
We use the bitnami/kafka image described at [kafka](https://hub.docker.com/r/bitnami/kafka)
* Port - We use the default port of 9192 for Kafka. This port is also exposed in the host environment. Changing this port also requires corresponding changes to the Egeria configuration.
* Other configuration can be seen in the *egeria-platform.yaml* file. 

## Postgresql - configured for Egeria
This is a standard PostgreSQL database server. The port for postgres is set to 5442. On initialization, two user roles are created:
    * egeria_admin with password 'admin4egeria'
    * egeria_user with password 'user4egeria'

# Usage
Follow these steps to use this Docker Compose script.

1. Install and Configure Docker and Docker Compose. 
   * Docker and Docker compose must be installed and running - see https://docs.docker.com/install/
   * Configure docker with at least 6GB memory
2. Clone the egeria-workspaces git repository [**egeria-workspacesl**](https://github.com/odpi/egeria-workspaces.git)
3. In a terminal window, change directory to the `egeria-workspaces/compose-configs/egeria-platform-postgres-compose` and
at the command line issue:

  `docker compose -f egeria-platform-postgres-compose.yaml up`

This will download the docker images for Kafka, PostgreSQL, and Egeria, then create and start the two containers. kafka, PostgreSQL and Egeria will then automatically configure themselves. For Egeria, this means not only starting up the initial set of servers, but then loading the **CoreContentPack.omarchive** into the metadata repository, and then configuring all the servers. This can take several minutes the first time the containers are created. Subsequent startups will be much faster.

4. Using either the **docker desktop** application or the docker command line you can see the two new containers running. To do this with the docker command line, you can issue:

`docker ps`

5. The environment is ready to be used. 

6. You can control the containers with docker compose commands - see [docker compose](https://docs.docker.com/reference/cli/docker/compose/). These commands can be used to administer and use the docker containers.

## Next Steps

Now that your Egeria environment is running and configured it is waiting for you to make requests. 
Some tutorials for working with Egeria can be found at [Tutorials](https://egeria-project.org/education/tutorials/). For those that want to try the new python client, you can find a quick introduction at [pyegeria](https://getting-started-with-egeria.pdr-associates.com/recipe-6-charming-python.html). 

# Please Note
Please note that this very basic docker compose script does not externalize Egeria's repositories - so if you delete the container,
you will lose your Egeria data. This also means that you can't easily share files between Egeria and your host environment.

The more extensive `egeria-platform-jupyter-compose` and `egeria-platform-jupyter-proxy-pg-compose` do externalize the Egeria repository
and do explicitly support convenient sharing of files between the docker containers and the host environment - these may be more convenient starting
points for development environments using python.

License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project.