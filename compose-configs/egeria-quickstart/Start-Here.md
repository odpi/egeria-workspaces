<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->
# Using the Egeria Quickstart Environment

If you are viewing this file in a Jupyter server then now you are ready to explore and use this basic Egeria environment.

If you are running Jupyter, on the left hand navigation panel you should see a number of folders:
* coco-data-lake
* distribution-hub
* landing-area
* loading-bay
* work - for your own notebooks.
* workbooks - contains some starter jupyter notebooks and demos.

These folders reside outside of the container and by default located in the `egeria-workspaces` directory that contains the scripts used to start up this environment. These locations can be changed by altering the **Docker Compose** script 
`egeria-quickstart.yaml` using a text editor.

A good way to get started is by opening the `egeria-workbooks` Notebook iun the `workbooks` folder.

For more information, please see [Egeria Docker Compose](https://egeria-project.org/education/open-metadata-labs/overview)