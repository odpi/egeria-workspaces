<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->
  
# Sustainability Initiative

This folder contains example Jupyter Notebooks and Dr.Egeria Markdown scripts to support the execution of the [Sustainability Initiative](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/sustainability-initiative/overview/) scenario at [Coco Pharmaceuticals](https://egeria-project.org/practices/coco-pharmaceuticals/). 

The governance definitions for the initiative are in two files.  [sustainability-governance-definitions.md](sustainability-governance-definitions.md) creates the Sustainability Reporting business imperative, the Sustainability Lead governance role held by [Tom Tally](https://egeria-project.org/practices/coco-pharmaceuticals/personas/tom-tally/), and the supporting folio.  [sustainability-governance-program.md](sustainability-governance-program.md) connects those definitions to the domain programs built since — reporting reconciliation from the corporate program, quality expectations, lineage, catalog and master data from the data governance program, and ALCOA+ integrity from manufacturing, where most of the company's emissions data originates.

The second file creates no new definitions; it exists to place the sustainability imperative inside the wider governance framework rather than alongside it.  Load the whole of `0. data-governance-program` first, then `sustainability-governance-definitions.md`, then `sustainability-governance-program.md`.

Each sample gives an explanation and code for how to perform the specific task.  You can go through them in turn if this detail is interesting.  Alternatively, if you just want the metadata loaded, then run the [run-all.ipynb](run-all.ipynb) notebook and it will choreograph the execution of them in a single run.

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.