ZZ<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Overview
This directory contains sample Docker Compose scripts to support the deployment of Apache Airflow with Marquez and Postgres
to simplify experimentation with OpenLineage and Egeria. A local volume is mounted in the egeria-workspaces directory to hold
dags (flows) to be executed in Airflow. There are a few sample dags provided. The pyegeria and openlineage python packages are
automatically installed for your use. Openlineage is pre-configured to work with Marquez via HTTP.



License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project.