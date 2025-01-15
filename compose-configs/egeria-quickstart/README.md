<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Overview
This directory contains sample Docker Compose scripts to support the deployment of Egeria for experimentation,
development, and learning. Rather than having to install Egeria, prerequisites and tools separately, these scripts make 
it easy to get a stack running quickly. This deployment extends the **egeria-platform-jupyter-compose** deployment by adding a PostgreSQL
database container and an Open Lineage Proxy that routes HTTP requests to Kafka Open Lineage messages.

These are not meant for production use. Please see the [Planning Guide](https://egeria-project.org/guides/planning/)
for more information about designing Egeria deployments. The Egeria community has also created samples for other 
deployment styles, such as Cloud Native approaches and the use of Helm charts to configure Kubernetes clusters. These
options may be better starting points for production deployments - depending upon your requirements.
Please feel free to engage with the community on our slack channel - we'd love your feedback and participation.

The docker compose script is called **egeria-platform-jupyter-proxy-pg-compose.yaml**. After running this script, you will have a running environment 
that consists of a single Egeria runtime platform,the Apache Kafka event system, Jupyter server, PostgreSQL server, 
and an Open Lineage proxy. 

## Egeria Platform - Default Configuration
We use the Egeria platform docker image - [egeria-platform](https://hub.docker.com/r/odpi/egeria-platform). We are now using an internal docker network called
`egeria_network` to allow postgres database to be shared with other deployments such as Superset. 

* Port - By default the platform uses port 9443 and exposes this port to the host environment, This means that Egeria requests
can be made to platform URL **https://localhost:9443** or, if your environment is configured to support it, it can use 
the domain name of your host machine. 
* SSL - By default strict SSL is set to false 
* Content Packs - pre-constructed information sets that can be used to configure Egeria and pre-load metadata, reference data and glossary data. See [Content Packs](https://egeria-project.org/content-packs/).
* Out-of-the-box Connectors - descriptions of the integration connectors can be found at [Integration Connectors](https://egeria-project.org/connectors/).

* Auto-Started Servers - by default a useful set of Egeria Open Metadata and Governance (OMAG) servers are pre-installed
and started when the Egeria platform is started.  A description of these servers can be found at [sample configs](open-metadata-resources/open-metadata-deployment/sample-configs/README.md).
The pre-configured and started servers are:

  * simple-metadata-store
  * active-metadata-store
  * engine-host
  * integration-daemon
  * view-server
  
   
* Mounted volumes for:
    * **distribution-hub**: an area where information created by Egeria (such as logs and survey information) can be easily exposed.
    * **egeria-platform-data**: this is a default location to hold your metadata repository when using the out of the box repository configuration. This has been externalized so that you can easily preserve your repository independently of docker.
    * **landing-area**: a convenient drop off point for files and folders you want to survey, analyze and perhaps catalog with Egeria.
    * **landing-bay**: 
  
    

## Kafka - configured for Egeria
We use the bitnami/kafka image described at [kafka](https://hub.docker.com/r/bitnami/kafka)
* Port - We use the default port of 9192 for Kafka. This port is also exposed in the host environment. Changing this port also requires corresponding changes to the Egeria configuration.
* Other configuration can be seen in the *egeria-platform.yaml* file. 

## Jupyter - configured for Egeria
A standard Jupyter data science docker image is extended to pre-install **pyegeria** and simplify using Egeria from Jupyter notebooks.
* Mounted volumes for:
    * **landing-area**: a convenient drop off point for files and folders you want to survey, analyze and perhaps catalog with Egeria.
    * **distribution-hub**: an area where information created by Egeria (such as logs and survey information) can be easily exposed.
    * **work**: a place for you to put your code and other artifacts.
    * **workbooks**: an area where we have put some Jupyter notebooks and related information to help you complete common tasks with Egeria. 

## Postgresql - configured for Egeria
This is a standard PostgreSQL database server. The port for postgres is set to 5442. On initialization, two user roles are created:
    * egeria_admin with password 'admin4egeria'
    * egeria_user with password 'user4egeria'

In addition, a default database, **egeria_observations** is created along with a default database schema to support 
Egeria surveys, monitoring and analysis. This will be described further in accompanying jupyter notebooks.

## Open Lineage Proxy 
This is a standard Open Lineage Proxy running on ports 6000 and 6001. Details of the proxy's configuration are in
the file `proxy.yml`. 


# Usage
Follow these steps to use Docker Compose.

1. Install and Configure Docker and Docker Compose. 
   * Docker and Docker compose must be installed and running - see https://docs.docker.com/install/
   * Configure docker with at least 8GB memory
   * Create the egeria_network from a terminal window by issuing: `docker network create egeria_network`
2. Download or clone the egeria-workspaces repo at [**egeria-workspaces**](https://github.com/odpi/egeria-workspaces.git)
3. In a terminal window, change directory to `<your path to here>/egeria-workspaces/egeria-platform-jupyter-proxy-pg-compose`
4. At the command line issue:

  `docker compose -f egeria-platform-jupyter-proxy-pg-compose.yaml up --build`

This will:
    a. build a jupyter image that is pre-configured to work with Egeria
    b. download the docker images for Kafka, Egeria, and Postgres, and then create and start the containers. Both kafka and Egeria will then automatically configure themselves. 
For Egeria, this means not only starting up the initial set of servers, but then loading the **CoreContentPack.omarchive** into the metadata repository, and then configuring all the servers. 
This can take several minutes the first time the containers are created. Subsequent startups will be much faster.
    c. start the jupyter container
4. Using either the **docker desktop** application or the docker command line you can see the two new containers running. To do this with the docker command line, you can issue:

`docker ps`

5. The environment is ready to be used. 

6. You can control the containers with docker compose commands - see [docker compose](https://docs.docker.com/reference/cli/docker/compose/). These commands can be used to administer and use the docker containers.
7. To access jupyter, open a browser to `http://localhost:8888`. At the password prompt, enter `egeria`. This should open up your notebook environment.

## Next Steps

Now that your Egeria environment is running and configured it is waiting for you to make requests. 
Some tutorials for working with Egeria can be found at [Tutorials](https://egeria-project.org/education/tutorials/). For those that want to try the new python client, you can find a quick introduction at [pyegeria](https://getting-started-with-egeria.pdr-associates.com/recipe-6-charming-python.html). 

As always, your feedback and participation are welcome. 


License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project.
   





----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
