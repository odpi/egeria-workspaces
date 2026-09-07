# The Coco Data Hub

The `coco-data-hub` is a collection of data stores that hold the key data needed to be exchanged between different business units to support new strategic initiatives such as personalized medicine.  It is part of the [new systems architecture](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/defining-new-systems-architecture/overview/).

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
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
