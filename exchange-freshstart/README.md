<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Summary
This folder contains freshstart exchange folders shared only with freshstart containers.

The table below shows the key mounts:

| **Docker Script** | **Docker Container**            | distribution-hub                  | landing-area                 | loading-bay                 |
|-------------------|---------------------------------|------------------------------------|-------------------------------|------------------------------|
| egeria-freshstart | **freshstart-egeria-main**      | /deployments/distribution-hub      | /deployments/landing-area     | /deployments/loading-bay    |
| egeria-freshstart | **freshstart-jupyter-work-full**| /home/jovyan/distribution-hub      | /home/jovyan/landing-area     | /home/jovyan/loading-bay    |

Note: unlike `exchange-quickstart`, this folder has no `coco-data-lake` subdirectory — freshstart does not mount one.

----
License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project.
