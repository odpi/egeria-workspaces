<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->
  
# Sustainability Initiative

This folder contains example Jupyter Notebooks and Dr.Egeria Markdown scripts to support the execution of the [Sustainability Initiative](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/sustainability-initiative/overview/) scenario at [Coco Pharmaceuticals](https://egeria-project.org/practices/coco-pharmaceuticals/). 

The governance definitions for the initiative are in two files.  [sustainability-governance-definitions.md](sustainability-governance-definitions.md) creates the Sustainability Reporting business imperative, the Sustainability Lead governance role held by [Tom Tally](https://egeria-project.org/practices/coco-pharmaceuticals/personas/tom-tally/), and the supporting folio.  [sustainability-governance-program.md](sustainability-governance-program.md) connects those definitions to the domain programs built since — reporting reconciliation from the corporate program, quality expectations, lineage, catalog and master data from the data governance program, and ALCOA+ integrity from manufacturing, where most of the company's emissions data originates.

The second file creates no new definitions; it exists to place the sustainability imperative inside the wider governance framework rather than alongside it.

Two subfolders of notebooks follow:

* [build-out-reference-data](build-out-reference-data/README.md) adds the employees of the acquired Austin and Bucharest sites, extends the reference data for Bucharest, and sets up Procurement as a business area with its own sustainability champion.
* [going-cfc-free](going-cfc-free/README.md) runs the CFC-Free Initiative: new open metadata types for equipment and refrigeration units, the refrigeration units at each site, and the New York Lab's replacement of its CFC unit.

The load order is:

1. The whole of `0. data-governance-program`, and `1. coco-data-hub` - the notebooks here use the Bucharest Site and the acquired systems that `1. coco-data-hub` adds to the IT Systems Inventory.
2. [sustainability-governance-definitions.md](sustainability-governance-definitions.md)
3. [sustainability-governance-program.md](sustainability-governance-program.md)
4. [build-out-reference-data/adding-acquisition-employees.ipynb](build-out-reference-data/adding-acquisition-employees.ipynb)
5. [build-out-reference-data/adding-procurement.ipynb](build-out-reference-data/adding-procurement.ipynb)
6. [going-cfc-free/load-refrigeration-units.ipynb](going-cfc-free/load-refrigeration-units.ipynb)
7. [going-cfc-free/ny-refrigeration-unit-replacement.ipynb](going-cfc-free/ny-refrigeration-unit-replacement.ipynb)

Each `_batch.json` follows this order.  The notebooks check for each element before creating it, so they can be rerun.

Each sample gives an explanation and code for how to perform the specific task.  You can go through them in turn if this detail is interesting.  Otherwise use the batch loading found under the Admin card of the portal (Data Initialization Tab).

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.