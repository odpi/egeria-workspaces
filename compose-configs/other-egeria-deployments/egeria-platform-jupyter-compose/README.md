<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Overview
This directory contains sample Docker Compose scripts to support the deployment of Egeria for experimentation,
development, and learning. Rather than having to install Egeria, prerequisites and tools separately, these scripts make 
it easy to get a stack running quickly. This deployment extends the **egeria-platform-compose** deployment by adding a Jupyter 
container[Project Jupyter](https://jupyter.org/) where users can use the **pyegeria** python client to work with Egeria.

The git repo is called **egeria-workspaces** because in addition to the core configuration, it contains sample and demonstration content and a place for you
to do your own experimentation. We've found it convenient to define a number of external mount points for your
docker volumes to simplify loading sample data, viewing sample results and sharing code. It is easy to tailor the 
configuration for your own needs.

These are not meant for production use. Please see the [Planning Guide](https://egeria-project.org/guides/planning/)
for more information about designing Egeria deployments. The Egeria community has also created samples for other 
deployment styles, such as Cloud Native approaches and the use of Helm charts to configure Kubernetes clusters. These
options may be better starting points for production deployments - depending upon your requirements.
Please feel free to engage with the community on our slack channel - we'd love your feedback and participation.

For a quick and simple environment to explore some of Egeria's base capabilities, the **egeria-platform-jupyter.yaml**  Docker Compose
deployment may be a good starting point. Once this script executes successfully, you will have three docker containers running. 
One for the Egeria platform, one for Kafka and one for Jupyter. With this running configuration, you can work with any of Egeria's standard interfaces 
- java APIs, python APIs, or just plain RESTful http calls - and of course, to make use of tools and interfaces that have been built using these APIs.

The set of **Docker Compose** configurations will grow and evolve over time to cover additional scenarios. For example,
the folder `egeria-platform-postgres-compose` contains a docker compose configuration that adds a Postgres 
database along with the Egeria OMAG platform and Kafka servers. This sets the stage emerging scenarios that
utilize a relational database to collect Egeria derived information such as Audit logs for additional analysis and dashboarding.
Please see the embedded README.md files for more details.

The docker compose script is called **egeria-platform-jupyter-compose.yaml**. After running this script, you will have a running environment 
that consists of a single Egeria runtime platform,the Apache Kafka event system and a Jupyter server. Information about configuring 
Egeria can be found at [Configuring Egeria](https://egeria-project.org/guides/admin/configuring-the-omag-server-platform/). 
We use standard, out-of-the-box configurations for both - a minimal amount of configuration for:

## Egeria Platform - Default Configuration
We use the Egeria platform docker image - [egeria-platform](https://hub.docker.com/r/odpi/egeria-platform).

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

# Usage
Follow these steps to use Docker Compose.

1. Install and Configure Docker and Docker Compose. 
   * Docker and Docker compose must be installed and running - see https://docs.docker.com/install/
   * Configure docker with at least 8GB memory
2. Download or clone the egeria-workspaces repo at [**egeria-workspaces**](https://github.com/odpi/egeria-workspaces.git)
3. In a terminal window, change directory to `<your path to here>/egeria-workspaces/egeria-platform-jupyter-compose`
4. At the command line issue:

  `docker compose -f egeria-platform-jupyter-compose.yaml up --build`

This will:
    a. build a jupyter image that is pre-configured to work with Egeria
    b. download the docker images for Kafka and Egeria, and then create and start the two containers. Both kafka and Egeria will then automatically configure themselves. 
For Egeria, this means not only starting up the initial set of servers, but then loading the **CoreContentPack.omarchive** into the metadata repository, and then configuring all the servers. This can take several minutes the first time the containers are created. Subsequent startups will be much faster.
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
