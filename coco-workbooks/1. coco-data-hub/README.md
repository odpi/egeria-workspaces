<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# The Coco Data Hub

The `coco-data-hub` is a collection of data stores that hold the key data needed to be exchanged between different business units to support new strategic initiatives such as personalized medicine.  It is part of the [new systems architecture](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/defining-new-systems-architecture/overview/).

This directory tells the story in the order it happens.  Erin Overview and Peter Profile lay out the solution components that implement the [strategic information supply chains](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/defining-information-supply-chains/overview/).  
To map those components to real systems they need an inventory, and the only one the company has is Gary Geeke's spreadsheet — so Gary [loads it into Egeria](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/cataloguing-infrastructure/overview/).  The mapping finds gaps; Gary asks the two newly acquired sites for their systems data to see how widespread the problem is, and gets a pleasant surprise.

With the flows, the components, and the systems in one place, Erin sets the standard for naming data fields, Gary and Peter catalogue the data each system holds, the data the supply chains carry is offered as digital products described to that standard, and the Data Sharing Hub that will serve them can be scoped and built.

| | Step | Content |
|---|---|---|
| 1 | Lay out the supply chain components | [strategic-supply-chain-analysis.md](strategic-supply-chain-analysis.md) |
| 2 | Gary's systems inventory | already in Egeria — supplied by `CocoComboArchive.omarchive` at startup |
| 3 | Match components to systems, find the gaps | [strategic-supply-chain-system-matches.md](strategic-supply-chain-system-matches.md) |
| 4 | Load the acquisitions' systems | [extending-the-systems-inventory/](extending-the-systems-inventory/README.md) |
| 5 | Link components to systems, report the gaps, attach the chains to the lineage | [mapping-the-systems/](mapping-the-systems/README.md) |
| 6 | Set standards for data field names | [data-field-naming/](data-field-naming/README.md) |
| 7 | Catalog the systems' database schemas, tables and columns | [creating-system-data-layer/](creating-system-data-layer/README.md) |
| 8 | Publish the data the supply chains carry as digital products | [strategic-digital-products/](strategic-digital-products/README.md) |
| 9 | Design the Data Sharing Hub | [solution-design.md](solution-design.md) |
| 10 | Govern how it is built | [software-development-governance-program.md](software-development-governance-program.md) |
| 11 | Set up the data sharing hub | [setting-up-the-data-hub.ipynb](setting-up-the-data-hub.ipynb) |
| 12 | Receive the OpenLineage events from Airflow | [receiving-open-lineage-events.ipynb](receiving-open-lineage-events.ipynb) |
| 13 | Subscribe the systems to the digital products | [digital-product-subscriptions.md](digital-product-subscriptions.md) |

----

## Before you start

Load [`0. data-governance-program`](../0.%20data-governance-program/README.md) first: the supply chains and the
governance definitions this directory links to are created there.

This directory also needs two of the optional runtimes in
[`compose-configs/optional-associated-runtimes`](../../compose-configs/optional-associated-runtimes/README.md),
running alongside `egeria-quickstart`:

* **Unity Catalog** ([unity-catalog/](../../compose-configs/optional-associated-runtimes/unity-catalog/README.md)) -
  `setting-up-the-data-hub.ipynb` catalogues it, and adds its `clinical_trials` catalog to the data hub.
* **Airflow and Marquez** ([airflow-marquez/](../../compose-configs/optional-associated-runtimes/airflow-marquez/README.md)) -
  Airflow runs the DAGs in [`exchange-quickstart/coco-dags`](../../exchange-quickstart/coco-dags/README.md) that move
  the data along the supply chains: `coco_operations_*` simulate the company's day-to-day activity in its systems,
  `coco_feed_*` copy each change from the systems into the digital products in the hub, and `coco_subscriptions_*`
  apply what the products' subscriptions deliver to the subscribing systems.  Start `egeria-quickstart` first,
  since Airflow uses its PostgreSQL server and the databases it creates.

Airflow reports what each DAG reads and writes as OpenLineage events.  For those events to reach Egeria:

1. Point Airflow at Egeria's OpenLineage topic, from the `airflow-marquez` directory: `./switch-lineage.sh egeria`
   (or `both` to keep sending them to Marquez too).  The events go through the OpenLineage proxy in `shared-infra`
   to the Kafka topic `openlineage.events`.
2. Run [receiving-open-lineage-events.ipynb](receiving-open-lineage-events.ipynb) - step 12 - which makes Egeria's
   `OpenLineageKafkaListener` integration connector listen to `openlineage.events`.  It runs **after step 11**,
   `setting-up-the-data-hub.ipynb`, has catalogued the `coco_data_hub` database: Egeria then matches the OpenLineage
   events about the product tables to the tables it has catalogued, which are what the ongoing update subscriptions in
   step 13 monitor.  If the events arrive first, Egeria creates separate `DataSet` elements for the tables instead, and
   those subscriptions are not triggered.  The listener starts reading at the end of the topic, so only events
   published after it is connected are catalogued.  The notebook can be re-run safely.

   To also send Egeria's own lineage events on to Marquez, run
   [publish-to-marquez.ipynb](../../workbooks/cataloguing-and-surveys/marquez/publish-to-marquez.ipynb) once in
   JupyterLab - only its first cells are needed, since step 12 has already connected the listener.

----

## Analysing the strategic supply chains

The file [strategic-supply-chain-analysis.md](strategic-supply-chain-analysis.md) works out what actually implements the
[strategic information supply chains](../0.%20data-governance-program/strategic-information-supply-chains.md) that
Jules Keeper's team registered.  For each chain it identifies the solution components that carry the data — creating
the ones that did not exist, locating the ones that did — makes them members of the chain, and draws the solution
linking wires between them.  Every wire records which supply chains it implements, so Egeria can assemble each
chain's implementation graph from the wires rather than from a drawing somebody has to maintain.

In total it creates 82 solution components, adds 15 memberships for components that already existed, and draws
123 wires.  Ten of those wires cross from one chain into another and name no chain - the handoffs, recorded as
peer links between the chains, where a fault in one chain becomes a failure in the next - and they are the places
worth instrumenting first.

Two things it does not do.  It does not touch the **Clinical Trials** or **Sustainability Reporting** chains, which
arrive fully implemented in `CocoComboArchive.omarchive`; where another chain meets clinical trials, the wire records
it.  And it does not invent blueprints: five of the archive's seven solution blueprints were
stubs sitting exactly where a strategic supply chain needed components, so it fills those in instead.

**This file loads before `solution-design.md`.**  The seven business system groups that `solution-design.md` used to
create — patient treatment, finance, procurement, research, warehouse, manufacturing and delivery — are the
landscape every strategic supply chain runs over, so they are now created here alongside the fine-grained
components they contain, and `solution-design.md` links them to its blueprint instead.  The **Data Sharing Hub**
stays in `solution-design.md`, because it is an asset-layer component of the data fabric that carries data
between those functions rather than a group of systems: it implements no supply chain and is offered as no
digital product.

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

With all three estates in Egeria, the matching becomes metadata.  The [mapping-the-systems/](mapping-the-systems/README.md) folder holds the mapping as a spreadsheet — one row per candidate system per component, with a confidence — and a notebook that creates the `ImplementedBy` relationships from the solution components to the systems, then produces a gap report: which components have no system anywhere, which are implemented only at the acquisitions and so lie outside the scope of the original Coco operation, and where the parent's coverage is unconfirmed.  That report, by business system group and by supply chain, is what scopes the Data Sharing Hub.  A second notebook then attaches each supply chain to the `DataFlow` lineage between the systems - merging the chain's name onto the interactions Gary loaded, and cloning a relationship per chain where a hop carries several, since lineage relationships are multi-links.

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

## Cataloguing the systems' data

The digital products are filled from the systems' own data, so before they are published Gary Geeke and Peter Profile describe the data
layer of every system that supplies or receives them.  Each of those systems keeps its data in its own PostgreSQL
schema, in one database per estate - `coco_pharma`, `austin_systems` and `bucharest_systems`.  The notebook in
[creating-system-data-layer/](creating-system-data-layer/README.md) has Gary give each system a `DatabaseManager` software
capability (`SupportedSoftwareCapability`); Peter then creates a `DeployedDatabaseSchema` asset for its schema from the
PostgreSQL schema template so that it has a working connection, links the two with `CapabilityAssetUse`, and makes
the schema a catalog target of the `JDBCDatabaseCataloguer`, which catalogues its tables and columns.

----

## Publishing the data as digital products

Every wire in the supply chain analysis carries data that one component produces and another consumes, and
the analysis wrote down what that data is.  The [strategic-digital-products](strategic-digital-products/README.md)
directory turns it into the **Coco Pharmaceuticals Strategic Digital Product Catalog**: one digital product per
solution component that originates data (more where a component receives data of different kinds), organised into a folder per
business system group, each product with a data specification whose structures and fields follow the data field
naming standard, and a PostgreSQL data set it will be read from.  The dependencies between the products follow
the wires and each names the supply chain it implements, so the supply chains can be traced through the catalog.  The products' field names follow the
data field naming standard set in step 6, and the terms they needed beyond the original vocabulary are added to the
glossary by `data-field-naming/strategic-products-vocabulary.md`, so the naming standard loads first.

The catalog is a member of `Egeria::DigitalProductCatalogsRoot`, so it appears in Egeria's web portal alongside
every other digital product catalog.

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

## Setting up the Data Sharing Hub

The file [setting-up-the-data-hub.ipynb](setting-up-the-data-hub.ipynb) is a Jupyter Notebook that performs the steps the [Peter Profile](https://egeria-project.org/practices/coco-pharmaceuticals/personas/peter-profile/) goes though to set up the data sharing hub.  You need to open the file in JupyterHub and then run each cell in turn.  There are descriptions of each command he uses throughout the file.  Once you have run the file, go to Egeria's web portal and you can see the data sharing hub in Egeria Explorer under the "Strategic Data Hubs" collection displayed from the **Collections** card.

----

## Receiving the OpenLineage events

The notebook [receiving-open-lineage-events.ipynb](receiving-open-lineage-events.ipynb) connects Egeria to the
OpenLineage events that Airflow publishes as the DAGs move the data along the supply chains.  Peter Profile runs the
`HarvestOpenLineageEvents::CreateAsCatalogTargetGovernanceActionProcess` process, which creates a `Topic` asset for
`openlineage.events` and adds it as a catalog target of the `OpenLineageKafkaListener` integration connector, and then
starts the listener.  From then on each DAG task is catalogued as a process, linked by `DataFlow` lineage to the
system tables and product tables it reads and writes.  It needs Airflow to be sending its events to Egeria - see
*Before you start* - and it must run after `setting-up-the-data-hub.ipynb`.  Since the `JDBCDatabaseCataloguer` carries
on cataloguing the tables in the background after the earlier workbooks finish, the notebook first waits - for up to 20
minutes - until every system table and every product table the `coco_feed_*` DAGs write to is catalogued, and does not
connect the listener if they are not.  If the listener is already connected, the notebook does not add a second catalog
target.

----

## Subscribing the systems to the digital products

The file [digital-product-subscriptions.md](digital-product-subscriptions.md) completes the supply chains.  Each
system that supplies a digital product already copies its changes into the product's tables in the hub; this file
sets up the **subscriptions** that deliver each product's data to the systems that depend on it, following
[product-subscriptions.csv](mapping-the-systems/data/product-subscriptions.csv).  It gives each product a product
manager and the subscription types its subscribers use, creates each subscriber's destination in the
`subscription_staging` database, and initiates the subscriptions.  The subscription types are deliberately varied -
ongoing updates, hourly, daily and weekly refreshes, and one-time evaluations - so that each way Egeria delivers a
product is exercised.  The subscriptions to products that no system supplies yet are listed in the file but not set
up.

It is generated by `compose-configs/egeria-quickstart/bin/gen-digital-product-subscriptions.py`; change the rules
there and regenerate rather than editing the file.  It needs the runtimes described in *Before you start*: the
ongoing update subscriptions are triggered by the data sets Egeria catalogues from the feed DAGs' OpenLineage
events, so it runs after OpenLineage is connected to Egeria (step 12).  It is the last file in the directory's batch
load, which runs it as Peter Profile, who builds the hub's pipelines.  To load it by hand:

    ```
    dr_egeria --directive process --userid peterprofile --user_pass secret digital-product-subscriptions.md
    ```

Each delivery lands in the subscriber's schema in `subscription_staging`, where the `coco_subscriptions_*` DAGs
apply it to the subscribing system - see [exchange-quickstart/coco-dags](../../exchange-quickstart/coco-dags/README.md).

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
