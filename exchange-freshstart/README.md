<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Summary
This folder contains freshstart exchange folders shared only with freshstart containers.

The table below shows the key mounts:

| **Docker Script** | **Docker Container**            | coco-data-lake                 | distribution-hub                  | landing-area                 | loading-bay                 |
|-------------------|---------------------------------|--------------------------------|-----------------------------------|------------------------------|-----------------------------|
| egeria-freshstart | **freshstart-egeria-main**      | /deployments/coco-data-lake    | /deployments/distribution-hub      | /deployments/landing-area    | /deployments/loading-bay    |
| egeria-freshstart | **freshstart-jupyter-work-full**| /home/jovyan/coco-data-lake    | /home/jovyan/distribution-hub      | /home/jovyan/landing-area    | /home/jovyan/loading-bay    |

----
License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project.
