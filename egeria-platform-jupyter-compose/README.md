<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Open Metadata Labs - Using Docker Compose

The open metadata labs contain an interactive environment that allow you to
experiment with different capabilities of Egeria.  More information about the labs can be found at:
[Overview of the Labs](https://egeria-project.org/education/open-metadata-labs/overview/).
The labs are written using Python Jupyter notebooks that
run in a Jupyter Server. The interactive exercises in the notebooks call python functions
that communicate with Egeria. An Apache Kafka server is used by Egeria for communications.

One way to easily deploy a running
Open Metadata Labs environment is by using the Docker Compose scripts contained in this directory.

A docker compose script, coco-lab-setup.yaml uses docker compose to deploy, configure and run a complete working 
environment that includes:

* Three Egeria OMAG Server Platforms 
  * egeria-core (on port 7443)
  * egeria-datalake (on port 7444)
  * egeria-dev (on port 7445)
* Kafka (on port 9192)
* Jupyter Server that is used to run the lab exercises (on port 9888)

Note that the port numbers are different from tho commonly used defaults to simplify
the coexistence of this environment in a host that may already be running Egeria, Kafka or Jupyter.
Configurations can be changed in the docker compose script `coco-lab-setup.yaml`.

# Getting Started

To get started, you need a computer with Docker installed and configured. Our experience is with running Docker on Mac and 
Linux machines, Windows machines should also work (reach out if you run into issues). Docker can be installed from 
[Docker](https://docker.com). Docker compose is installed automatically if you install Dockker Desktop.
Compatible alternatives to Docker Compose exist but have not yet been validated.

This deployment has been testing on older machines as well as current ones. Given the number of 
servers we are running, allocating at 10gb of memory for Docker is recommended. 

The startup procedure is as follows:

1. Start docker or docker desktop
2. Download or clone the git repository containing the Egeria Open Metadata Labs
   * Download - a zip file of the repository can be downloaded by pressing the green `Code` button on  [](https://github.com/odpi/egeria-jupyter-notebooks)
     * unzip the file in your directory of choice
   * Clone - If you want to fork the repo first then change the URL to your fork.
     * Ensure you have the git command line installed.
     * Change to a directory you want to use as the parent of the files
     * From a terminal window, issue: `git clone https://github.com/dwolfson/egeria-jupyter-notebooks.git`
3. In a terminal window, from the `egeria-jupyter-notebooks` folder, issue the commmand:
    `docker compose -f coco-lab-docker-compose/coco-lab-setup.yaml up --build`
    * This should produce a large amount of output as images are downloaded and started and configured. Expect the process to take a few minutes the first time and less on subsequent starts.
    * You should only need the `--build` option the first time you run this command. Subsequent startup calls would just be:
    `docker compose -f coco-lab-docker-compose/coco-lab-setup.yaml up`
4. Once everything is started and configured you can run the labs from the jupyter server by:
   * opening a web browser to:
     `http://localhost:9888/lab/tree/egeria-labs/read-me-first.ipynb`
   * Type in `egeria` into the box for token or password. This will launch Jupyter in the browser.
   * The `read-me-first` jupyter notebook should now be displayed. You are ready to start!


5. Questions, observations and other feedback are always welcome - we welcome your participation in our community:
   * https://egeria-project.org/guides/community/
   





----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
