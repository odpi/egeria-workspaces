<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Overview
This directory contains sample Docker Compose scripts to support the deployment of Egeria for experimentation,
development, and learning. Rather than having to install Egeria, prerequisites and tools separately, these scripts make 
it easy to get a stack running quickly. 
These are not meant for production use. Please see the [Planning Guide](https://egeria-project.org/guides/planning/)
for more information about designing Egeria deployments. The Egeria community has also created samples for other 
deployment styles, such as Cloud Native approaches and the use of Helm charts to configure Kubernetes clusters. These
options may be better starting points for production deployments - depending upon your requirements.
Please feel free to engage with the community on our slack channel - we'd love your feedback and participation.


For a quick and simple environment to explore some of Egeria's base capabilities, the **egeria-platform-compose**  Docker Compose
deployment may be a good starting point. Once this script executes successfully, you will have two docker containers running. 
One for the Egeria platform and one for Kafka. With this running configuration, you can work with any of Egeria's standard interfaces - 
java APIs, python APIs (you'll need to install pyegeria), or just plain RESTful http calls - and of course, to make use of tools and interfaces that have been built using these APIs.

The **egeria-platform-jupyter-compose** script is useful if you want to use the [**project jupyter**](https://jupyter.org/)
based browser interfaces for exploration and development. pyegeria is pre-installed along with demonstration and starter Jupyter notebooks.

The set of **Docker Compose** configurations will grow and evolve over time to cover additional scenarios. For example,
the folder `egeria-platform-postgres-compose` contains a docker compose configuration that adds a Postgres 
database along with the Egeria OMAG platform and Kafka servers. A Postgres database can be used both as an Egeria repository and as
a collection point to store and analyze additional information such as Audit logs or Survey results. 

We also provide some sample docker compose scripts for other runtimes that are often used with Egeria such as [**superset**](https://superset.apache.org/) as an
analytics dashboard, [**airflow**](https://airflow.apache.org/) for executing python based workflows and [**marquez**](https://github.com/MarquezProject/marquez) for visualizing open lineage.
Please see the embedded README.md files for more details.

Also note that you can switch between compose scripts and still maintain your Egeria repository with the default configuration.

> **Tip**: For everyday use, I use egeria-platform-jupyter-proxy-pg-compose for the broadest range of uses.

# Contents
* airflow-marquez-compose - configures an apache airflow and Marquez environment with OpenLineage for experimentation.
* egeria-platform-compose - a basic Egeria OMAG platform standalone deployment that includes Kafka as well as Egeria.
* egeria-platform-jupyter-compose - adds a jupyter server to the previous configuration.
* egeria-platform-postgres-compose - deploys and configures a Postgres relational database as well as Kafka and Egeria.
* egeria-platform-jupyter-proxy-pg-compose - adds an OpenLineage proxy and Postgres servers to egeria-platform-jupyter-compose.
* superset-compose - a simple modification of the standard Apache Superset compose script to use the same postgres database as Egeria.


Please see the README.md files in each of the sub-directories for more details.

As always, your feedback and participation are welcome. 


License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project.