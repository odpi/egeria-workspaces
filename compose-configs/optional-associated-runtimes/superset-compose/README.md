<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Overview
This directory contains sample Docker Compose script to support the deployment of 
Apache Superset to use with Egeria. 

The current script is designed to work with the 
egeria-quickstart script. It assumes that 
a docker network `egeria-network` is configured and that postgres is running
on port 5442. You can, of course, modify this script to meet your needs.

The default user for superset is admin, with password admin. Again,
you can alter this to meet your requirements.

# Running

From the superset-compose directory, issue:

`docker compose -f egeria-superset-compose.yml up`

From a browser, navigate to `http://localhost:8088` and login with user/pwd of `admin`

# Using

Please refer to the Apache Superset documentation at [Apache Superset](https://superset.apache.org/)


---
As always, your feedback and participation are welcome. 


License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project.