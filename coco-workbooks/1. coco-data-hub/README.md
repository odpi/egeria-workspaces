# The Coco Data Hub

The `coco-data-hub` is a collection of data stores that hold the key data needed to be exchanged between different business units to support new strategic initiatives such as personalized medicine.  It is part of the [new systems architecture](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/defining-new-systems-architecture/overview/).

----

## The solution blueprint

The file [solution-design.md](solution-design.md) contains a series of Dr. Egeria commands that loads the solution blueprint describing the design of the data hub.

![Erin and Peter designing the data hub](https://raw.githubusercontent.com/odpi/egeria-docs/main/site/docs/practices/coco-pharmaceuticals/scenarios/defining-new-systems-architecture/erin-peter-designing-new-architecture.png)

You can load the definitions into Egeria on one of two ways:

1. From Obsidian - open the solution-design.md file and click the the suitcase icon labeled "Call Dr. Egeria (MCP)"
2. From the command line in JupyterLab. Make sure you are in this directory and issue the command:

    ```
    dr_egeria --directive process solution-design.md
     
    ```

The solutions design is called "Data-Driven Systems Architecture".  

Once the solution design is loaded, go to Egeria's web portal and you can see the solution design in Egeria Explorer under the "Strategic Solutions" collection displayed from the **Collections** card.

![Viewing solution blueprint](https://raw.githubusercontent.com/odpi/egeria-docs/main/site/docs/practices/coco-pharmaceuticals/scenarios/defining-new-systems-architecture/viewing-solution-blueprint.png)


----

## Defining governance for AI software development

The file [software-development-governance.md](software-development-governance-program.md) contains a series of Dr. Egeria commands that loads the governance definitions defined by the IT team to govern their new AI-driven software development process.

![Discussion how to use AI in their build out of the Coco Data Hub](https://raw.githubusercontent.com/odpi/egeria-docs/main/site/docs/practices/coco-pharmaceuticals/scenarios/defining-new-systems-architecture/it-team-disussing-ai-development-process.png)

The software development governance definitions link to definitions in the [Data Governance Program](../0.%20data-governance-program/README.md) so make sure the data governance program is loaded before the software development definitions.

Again you can load the definitions into Egeria on one of two ways:

1. From Obsidian - open the software-development-governance.md file and click the the suitcase icon labeled "Call Dr. Egeria (MCP)"
2. From the command line in JupyterLab. Make sure you are in this directory and issue the command:

    ```
    dr_egeria --directive process software-development-governance-program.md
     
    ```

----

## Setting up the Data Hub

The file [setting-up-the-data-hub.ipynb](setting-up-the-data-hub.ipynb) is a Jupyter Notebook that performs the steps the [Peter Profile](https://egeria-project.org/practices/coco-pharmaceuticals/personas/peter-profile/) goes though to set up the data hub.  You need to open the file in JupyterHub and then run each cell in turn.  There are descriptions of each command he uses throughout the file.  Once you have run the file, go to Egeria's web portal and you can see the data hub in Egeria Explorer under the "Strategic Data Hubs" collection displayed from the **Collections** card.

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
