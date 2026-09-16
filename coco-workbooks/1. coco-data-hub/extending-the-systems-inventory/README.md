# Extending the Systems Inventory

This folder follows [Gary Geeke](https://egeria-project.org/practices/coco-pharmaceuticals/personas/gary-geeke/) as he extends the systems inventory with the systems of two recent acquisitions, both manufacturers and experts in small batch manufacturing: one in Austin and one in Bucharest.

His own inventory is already in Egeria.  He loaded it from his spreadsheet — the [cataloguing infrastructure](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/cataloguing-infrastructure/overview/) scenario — so that the solution components of the [strategic information supply chains](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/defining-information-supply-chains/overview/) could be mapped to real systems; in the demo environment those systems are present from startup, supplied by `CocoComboArchive.omarchive`.  The mapping found that many of the components live in systems outside his responsibility, so he asked the two acquired sites for their systems data to see how widespread the problem is.  Gary has received 6 spreadsheets that are stored in the data folder:

* The Austin systems:
    * `coco_austin_subsystems.csv` - subsystems that organize the Austin systems
    * `coco_austin_systems.csv` - descriptions of the Austin systems themselves
    * `coco_austin_system_interactions.csv` - descriptions of the data exchange between the austin systems
* The Bucharest systems:
    * `ekg_subsystems.csv` - subsystems that organize the Bucharest systems
    * `ekg_systems.csv` - descriptions of the Bucharest systems themselves
    * `ekg_system_interactions.csv` - descriptions of the data exchange between the Bucharest systems

----

## Loading the files

Open the Jupyter Notebook [extending-the-systems-inventory.ipynb](extending-the-systems-inventory.ipynb) and run the cells to
load the data in the csv files into Egeria.  The notebook goes through the process step-by-step, explaining how the elements
are created and linked together.

----

## Loading the naming conventions

While Gary is working with the files he notices that both companies use a systematic naming convention for their system identifiers.  Each company's approach is slightly different of course, but it has him wondering.  Gary asks each team about their naming convention, interested in whether they are using a standard.  

They reply that there are not really well established naming conventions so they made it up.  Gary decides to capture each of their approaches in a naming standard rule cant can be found in file [naming-conventions.md](naming-conventions.md).

You can load the definitions into Egeria in one of two ways:

1. From Obsidian - open the naming-conventions.md file and click the suitcase icon labeled "Call Dr. Egeria (MCP)"
2. From the command line in JupyterLab. Make sure you are in this directory and issue the command:

    ```
    dr_egeria --directive process --userid garygeeke --user_pass secret naming-conventions.md
     
    ```


____
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.