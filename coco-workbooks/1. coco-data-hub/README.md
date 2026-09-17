# The Coco Data Hub

The `coco-data-hub` is a collection of data stores that hold the key data needed to be exchanged between different business units to support new strategic initiatives such as personalized medicine.  It is part of the [new systems architecture](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/defining-new-systems-architecture/overview/).

This directory tells the story in the order it happens.  Erin Overview and Peter Profile lay out the solution components that implement the [strategic information supply chains](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/defining-information-supply-chains/overview/).  To map those components to real systems they need an inventory, and the only one the company has is Gary Geeke's spreadsheet — so Gary [loads it into Egeria](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/cataloguing-infrastructure/overview/).  The mapping finds gaps; Gary asks the two newly acquired sites for their systems data to see how widespread the problem is, and gets a pleasant surprise.  With the flows, the components and the systems in one place, the Data Hub can be scoped and built - and the data the supply chains carry can be offered as digital products.

| | Step | Content |
|---|---|---|
| 1 | Lay out the supply chain components | [strategic-supply-chain-analysis.md](strategic-supply-chain-analysis.md) |
| 2 | Gary's systems inventory | already in Egeria — supplied by `CocoComboArchive.omarchive` at startup |
| 3 | Match components to systems, find the gaps | [strategic-supply-chain-system-matches.md](strategic-supply-chain-system-matches.md) |
| 4 | Load the acquisitions' systems | [extending-the-systems-inventory/](extending-the-systems-inventory/README.md) |
| 5 | Link components to systems, report the gaps, attach the chains to the lineage | [mapping-the-systems/](mapping-the-systems/README.md) |
| 6 | Design the Data Hub | [solution-design.md](solution-design.md) |
| 7 | Govern how it is built | [software-development-governance-program.md](software-development-governance-program.md) |
| 8 | Set it up | [setting-up-the-data-hub.ipynb](setting-up-the-data-hub.ipynb) |
| 9 | Name its data fields | [data-field-naming/](data-field-naming/README.md) |
| 10 | Publish the data the supply chains carry as digital products | [strategic-digital-products/](strategic-digital-products/README.md) |

----

## Analysing the strategic supply chains

The file [strategic-supply-chain-analysis.md](strategic-supply-chain-analysis.md) works out what actually implements the
[strategic information supply chains](../0.%20data-governance-program/strategic-information-supply-chains.md) that
Jules Keeper's team registered.  For each chain it identifies the solution components that carry the data — creating
the ones that did not exist, locating the ones that did — makes them members of the chain, and draws the solution
linking wires between them.  Every wire records which supply chains it implements, so Egeria can assemble each
chain's implementation graph from the wires rather than from a drawing somebody has to maintain.

In total it creates 82 solution components, adds 21 memberships for components that already existed, and draws
130 wires.  Forty-four of those wires implement more than one supply chain: they are the handovers, where a fault
in one chain becomes a failure in the next, and they are the places worth instrumenting first.

Two things it does not do.  It does not touch the **Clinical Trials** or **Sustainability Reporting** chains, which
arrive fully implemented in `CocoComboArchive.omarchive` — beyond adding handover members where another chain now
meets clinical trials.  And it does not invent blueprints: five of the archive's seven solution blueprints were
stubs sitting exactly where a strategic supply chain needed components, so it fills those in instead.

**This file loads before `solution-design.md`.**  The eight business system groups that `solution-design.md` used to
create — the Data Hub, patient treatment, finance, procurement, research, warehouse, manufacturing and delivery —
are the landscape every strategic supply chain runs over, so they are now created here alongside the fine-grained
components they contain, and `solution-design.md` links them to its blueprint instead.

    ```
    dr_egeria --directive process --userid erinoverview --user_pass secret strategic-supply-chain-analysis.md
    ```

It refers to the supply chains created in `0. data-governance-program/strategic-information-supply-chains.md`, so
load the data governance program first.

----

## Gary's systems inventory

Gary Geeke has kept a spreadsheet of the servers he is responsible for at every Coco Pharmaceuticals location.  When Erin and Peter need to map the strategic supply chain components to the systems that run them, that spreadsheet is the only inventory the company has, so Gary loads it into Egeria through the pyegeria API — the story is told in the [cataloguing infrastructure](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/cataloguing-infrastructure/overview/) scenario.  In the demo environment this step is already done: `CocoComboArchive.omarchive` is loaded at startup and supplies those systems, organised into subsystems under the **IT Systems Inventory** collection, so there is something to look at from the first connection.

----

## Mapping the components to systems

The file [strategic-supply-chain-system-matches.md](strategic-supply-chain-system-matches.md) is the result of taking the seventy-one components to Gary's inventory and trying to match them up.  It is an analysis document rather than a Dr.Egeria command file — nothing in it is loaded — and it exists for what it found rather than for the mapping itself: the inventory answered *what do we run?* when the supply chains were asking *what do we depend on?*, and the gaps clustered exactly where the regulated layer of the business ought to be.

----

## Extending the systems inventory

Gary's response to the gaps is to ask how widespread the problem is.  The two newly acquired sites, in Austin and in Bucharest, are not in his spreadsheet at all, so he asks each of them for their systems data.  The [extending-the-systems-inventory/](extending-the-systems-inventory/README.md) folder holds the six spreadsheets that come back and the notebook that loads them, together with the [naming conventions](extending-the-systems-inventory/naming-conventions.md) each site turned out to have invented for its system identifiers.

The pleasant surprise is in the matches document: both acquisitions run a complete, modern stack for regulated manufacturing that the parent company has no equivalent of, and most of the gaps the mapping found are already closed there.  Version 0.2 of the analysis re-matches every component across all three estates.

----

## Mapping the systems

With all three estates in Egeria, the matching becomes metadata.  The [mapping-the-systems/](mapping-the-systems/README.md) folder holds the mapping as a spreadsheet — one row per candidate system per component, with a confidence — and a notebook that creates the `ImplementedBy` relationships from the solution components to the systems, then produces a gap report: which components have no system anywhere, which are implemented only at the acquisitions and so lie outside the scope of the original Coco operation, and where the parent's coverage is unconfirmed.  That report, by business system group and by supply chain, is what scopes the Data Hub.  A second notebook then attaches each supply chain to the `DataFlow` lineage between the systems - merging the chain's name onto the interactions Gary loaded, and cloning a relationship per chain where a hop carries several, since lineage relationships are multi-links.

----

## The solution blueprint

The file [solution-design.md](solution-design.md) contains a series of Dr. Egeria commands that loads the solution blueprint describing the design of the data hub.  Its eight components are created by [strategic-supply-chain-analysis.md](strategic-supply-chain-analysis.md), so load that file first.

![Erin and Peter designing the data hub](https://raw.githubusercontent.com/odpi/egeria-docs/main/site/docs/practices/coco-pharmaceuticals/scenarios/defining-new-systems-architecture/erin-peter-designing-new-architecture.png)

You can load the definitions into Egeria on one of two ways:

1. From Obsidian - open the solution-design.md file and click the the suitcase icon labeled "Call Dr. Egeria (MCP)"
2. From the command line in JupyterLab. Make sure you are in this directory and issue the command:

    ```
    dr_egeria --directive process --userid erinoverview --user_pass secret solution-design.md
     
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
    dr_egeria --directive process --userid pollytasker --user_pass secret software-development-governance-program.md
     
    ```

----

## Setting up the Data Hub

The file [setting-up-the-data-hub.ipynb](setting-up-the-data-hub.ipynb) is a Jupyter Notebook that performs the steps the [Peter Profile](https://egeria-project.org/practices/coco-pharmaceuticals/personas/peter-profile/) goes though to set up the data hub.  You need to open the file in JupyterHub and then run each cell in turn.  There are descriptions of each command he uses throughout the file.  Once you have run the file, go to Egeria's web portal and you can see the data hub in Egeria Explorer under the "Strategic Data Hubs" collection displayed from the **Collections** card.

----

## Naming the data fields

The [data-field-naming](data-field-naming/README.md) directory builds the **Data Field Naming** glossary: the
vocabulary of prime words, modifiers and class words used to construct consistent data field names across the
data hub, following the `prime word + modifier(s) + class word` convention - for example `PatientAdmittingDate`
= `Patient` (prime word) + `Admitting` (modifier) + `Date` (class word).

The glossary is organized into a folder per subject area, mirroring `CocoSubjectAreaDefinition`, and each folder
is linked to the matching `SubjectArea::` collection loaded from `CocoComboArchive.omarchive`. The final three
files classify every term as a `PrimeWord`, `Modifier` or `ClassWord`
(see [0438 Naming Standards](https://egeria-project.org/types/4/0438-Naming-Standards/)).

There are around thirty files to process and the order matters, so follow the load order given in
[data-field-naming/README.md](data-field-naming/README.md) rather than processing them ad hoc.

----

## Publishing the data as digital products

Every wire in the supply chain analysis carries data that one component produces and another consumes, and
the analysis wrote down what that data is.  The [strategic-digital-products](strategic-digital-products/README.md)
directory turns it into the **Coco Pharmaceuticals Strategic Digital Product Catalog**: one digital product per
solution component (more where a component receives data of different kinds), organised into a folder per
business system group, each product with a data specification whose structures and fields follow the data field
naming standard, and a PostgreSQL data set it will be read from.  The dependencies between the products follow
the wires, so the supply chains can be traced through the catalog.  The products' field names needed
vocabulary the naming glossary did not have, so `data-field-naming/strategic-products-vocabulary.md` extends it,
and the naming glossary must be loaded first.

The catalog is a member of `Egeria::DigitalProductCatalogsRoot`, so it appears in Egeria's web portal alongside
every other digital product catalog.

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
