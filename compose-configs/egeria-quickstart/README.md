<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Overview
This directory contains the *egeria-quickstart* docker compose script and supporting files, to support the deployment of Egeria for experimentation,
development, and learning. Rather than having to install Egeria, prerequisites and tools separately, these scripts make 
it easy to get a stack running quickly. This deployment configures and starts:

* Egeria on port 9443 and will automatically start the default servers.
* Jupyter is deployed using port 7888 so as not to interfere with other jupyter servers
* Kafka on port 9192 to support communications between Egeria servers and other sources.
* Postgres on port 5442 is configured with the *egeria* database and is dynamically configured with the needed schemas.
* Open Lineage Proxy running on ports 6000 and 6001. Details of the proxy's configuration are in the file `proxy.yml`. 
* Apache Web Server on port 8085 and configured with `httpd.conf`.


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
and started when the Egeria platform is started.  A description of these servers can be found at [sample configs](open-metadata-resources/open-metadata-deployment/sample-configs/README.md).
The pre-configured and started servers are:

  * qs-metadata-store
  * qs-engine-host
  * qs-integration-daemon
  * qs-view-server
  
   
* Mounted volumes for:
    * **distribution-hub**: an area where information created by Egeria (such as logs and survey information) can be easily exposed.
    * **egeria-platform-data**: this is a default location to hold your metadata repository when using the out of the box repository configuration. This has been externalized so that you can easily preserve your repository independently of docker.
    * **landing-area**: a convenient drop off point for files and folders you want to survey, analyze, and catalog with Egeria.
    * **landing-bay**: a place to drop files that you want to be loaded into Egeria - e.g glossary terms to import into an Egeria glossary.
  
    

## Kafka - configured for Egeria
We use the bitnami/kafka image described at [kafka](https://hub.docker.com/r/bitnami/kafka)

* Port - We use the default port of 9192 for Kafka. This port is also exposed in the host environment. Changing this port also requires corresponding changes to the Egeria configuration.
* Other configuration can be seen in the *egeria-platform.yaml* file. 

## Jupyter - configured for Egeria
A standard Jupyter data science docker image is extended to pre-install **pyegeria** and simplify using Egeria from Jupyter notebooks.

File system volumes are mounted for:
    * **landing-area**: a convenient drop off point for files and folders you want to survey, analyze and perhaps catalog with Egeria.
    * **distribution-hub**: an area where information created by Egeria (such as logs and survey information) can be easily exposed.
    * **work**: a place for you to put your code and other artifacts.
    * **workbooks**: an area where we have put some Jupyter notebooks and related information to help you complete common tasks with Egeria. 

## Postgresql - configured for Egeria

This is a standard PostgreSQL database server with a database named *egeria*. The port for postgres is set to 5442. On initialization, two user roles are created:

* egeria_admin with password 'admin4egeria'
* egeria_user with password 'user4egeria'

Egeria will automatically create database schemas in this database to support the different kinds of activities you configure and run.

## Open Lineage Proxy 
This is a standard Open Lineage Proxy running on ports 6000 and 6001. Details of the proxy's configuration are in
the file `proxy.yml`. 

----
# Usage

Follow these steps to use Docker Compose.

1. Install and Configure Docker and Docker Compose. 
   * Docker and Docker compose must be installed and running - see https://docs.docker.com/install/
   * Configure docker with at least 8GB memory
   * Create the egeria_network from a terminal window by issuing: `docker network create egeria_network`
2. Download or clone the egeria-workspaces repo at [**egeria-workspaces**](https://github.com/odpi/egeria-workspaces.git)
3. In a terminal window, change directory to `<your path to here>/egeria-workspaces/compose-configs/egeria-quickstart`
4. At the command line issue:

   `docker compose -f egeria-quickstart.yaml up --build`

   This will:

   * build a jupyter image that is pre-configured to work with Egeria 
    
   * download the docker images for Kafka, Egeria, and Postgres, and then create and start the containers. Both kafka and Egeria will then automatically configure themselves. 

   * start the jupyter container

   For Egeria, this means not only starting up the initial set of servers, but then loading the **CoreContentPack.omarchive** into the metadata repository, and then configuring all the servers. 
   This can take several minutes the first time the containers are created. Subsequent startups will be much faster.

Using either the **docker desktop** application or the docker command line you can see the two new containers running. To do this with the docker command line, you can issue:

`docker ps`

The environment is ready to be used. 

You can control the containers with docker compose commands - see [docker compose](https://docs.docker.com/reference/cli/docker/compose/). These commands can be used to manage and use the docker containers.

To access jupyter, open a browser to `http://localhost:7888`. At the password prompt, enter `egeria`. This should open up your notebook environment.

>Note: You only need to use the --build option if you want to rebuild the jupyter image.

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
