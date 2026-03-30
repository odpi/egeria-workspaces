<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Summary
This folder contains quickstart exchange folders shared by quickstart containers and selected optional runtimes.

The table below shows the key mounts:

| **Docker Script** | **Docker Container**         | coco-data-lake                 | distribution-hub                  | landing-area                 | loading-bay                 |
|-------------------|------------------------------|--------------------------------|-----------------------------------|------------------------------|-----------------------------|
| egeria-quickstart | **egeria-main**              | /deployments/coco-data-lake    | /deployments/distribution-hub      | /deployments/landing-area    | /deployments/loading-bay    |
| egeria-quickstart | **quickstart-jupyter-work-full** | /home/jovyan/coco-data-lake | /home/jovyan/distribution-hub      | /home/jovyan/landing-area    | /home/jovyan/loading-bay    |
| egeria-quickstart | **egeria-shared-postgres**   | /var/data/coco-data-lake       |                                   |                              |                             |
| airflow-marquez   | **airflow-x**                | /opt/airflow/data/coco-data-lake |                                 |                              |                             |
| uc-ui-compose     | **server1 (Unity Catalog)**  | /mnt/coco-data-lake            |                                   |                              |                             |
| uc-ui-compose     | **server2 (Unity Catalog)**  | /mnt/coco-data-lake            |                                   |                              |                             |

----
License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project.

