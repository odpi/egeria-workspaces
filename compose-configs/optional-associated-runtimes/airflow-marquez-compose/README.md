<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Overview
This directory contains sample Docker Compose scripts to support the deployment of Apache Airflow with Marquez and Postgres
to simplify experimentation with OpenLineage and Egeria. A local volume is mounted in the egeria-workspaces directory to hold
dags (flows) to be executed in Airflow. There are a few sample dags provided. The pyegeria and openlineage python packages are
automatically installed for your use. Openlineage is pre-configured to work with Marquez via HTTP.

postgres at 5436
## Usage

Follow these steps to use Docker Compose.

1. Install and Configure Docker and Docker Compose.
    * Docker and Docker compose must be installed and running - see https://docs.docker.com/install/
    * Configure docker with at least 8GB memory
2. Download or clone the egeria-workspaces repo at [**egeria-workspaces**](https://github.com/odpi/egeria-workspaces.git)
3. In a terminal window, change directory to `<your path to here>/egeria-workspaces/airflow-marquez-compose`
4. At the command line issue:

`docker compose -f airflow-marquez.yaml up`

This will:
a. download the docker images for Apache Airflow and Marquez
b. create and start the containers for these technologies. This can take several minutes the first time the containers are created. Subsequent startups will be much faster.

4. Using either the **docker desktop** application or the docker command line you can see the two new containers running. To do this with the docker command line, you can issue:

`docker ps`

5. The environment is ready to be used.

6. You can control the containers with docker compose commands - see [docker compose](https://docs.docker.com/reference/cli/docker/compose/). These commands can be used to administer and use the docker containers.
7. To access Marquez, open a browser tab to `http://localhost:3000/events`. 
8. To access Apache Airflow's console, open a browser tab to `http://localhost:8070/home`.  To sign in use a userId of `airflow` and a password of `????`.





License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project.