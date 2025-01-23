<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->


# Summary
This folder contains folders intended to be shared by different runtimes within the Egeria Workspaces environment.
The table below shows how each of the folders is mounted (and thus visible) in the different containers.





| **Docker Script** | **Docker Container** 	      | coco-data-lake              	    | distribution-hub              	 | landing-area              	 | loading-bay              	 |
|-------------------|-----------------------------|----------------------------------|---------------------------------|-----------------------------|----------------------------|
| egeria-quickstart | **egeria-main**          	  | /deployments/coco-data-lake 	    | /deployments/distribution-hub 	 | /deployments/landing-area   | /deployments/loading-bay   |
| egeria-quickstart | **postgres**             	  | /var/data/coco-data-lake    	    | 	                               | 	                           | 	                          |
| egeria-quickstart | **jupyter**              	  | /home/jovyan/coco-data-lake 	    | /home/jovyan/distribution-hub   | /home/jovyan/landing-area   | /home/jovyan/loading-bay   |
| airflow-marquez   | **airflow-x**               | /opt/airflow/data/coco-data-lake |                                 |                             |                            |
| uc-ui-compose     | **server1 (Unity Catalog)** | /mnt/coco-data-lake              |                                 |                             |                            |
| uc-ui-compose     | **server2 (Unity Catalog)** | /mnt/coco-data-lake              |                                 |                             |                            |
