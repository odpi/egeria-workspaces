<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Creating the System Data Layer

This folder follows [Gary Geeke](https://egeria-project.org/practices/coco-pharmaceuticals/personas/gary-geeke/) and [Peter Profile](https://egeria-project.org/practices/coco-pharmaceuticals/personas/peter-profile/) describing the data held by the systems that supply and receive the strategic digital products.  It runs after [mapping-the-systems](../mapping-the-systems/README.md) and [data-field-naming](../data-field-naming/README.md), and just before [strategic-digital-products](../strategic-digital-products/README.md).

Each of these systems keeps its data in its own PostgreSQL schema, and each estate has its own database on the shared PostgreSQL server (`host.docker.internal:5442`):

| Estate | Database | Systems |
|---|---|---|
| Coco core | `coco_pharma` | 22 |
| Austin | `austin_systems` | 27 |
| Bucharest | `bucharest_systems` | 17 |

The databases are created, with sample data, when `egeria-quickstart` starts (`compose-configs/egeria-quickstart/docker-entrypoint-initdb.d/init_coco_systems.sql`).

## Contents

| File | What it is |
|---|---|
| [creating-system-data-layer.ipynb](creating-system-data-layer.ipynb) | Builds the data layer of each system in Egeria with pyegeria and checks the cataloguing |
| [data/system-databases.csv](data/system-databases.csv) | One row per system schema: estate, database, schema, the system's qualified name and name, the schema's description and the number of tables it defines.  Generated from the header and `COMMENT ON SCHEMA` of each `data/coco_systems/<database>/<schema>.sql` script - regenerate it when a system schema is added |

## What the notebook does

For each system in the CSV file:

1. **Creates a `DatabaseManager` software capability** - `DatabaseManager::<system qualified name>` - and links it to the system's `SoftwareServer` with `SupportedSoftwareCapability`.
2. **Creates a `DeployedDatabaseSchema` asset** from the *PostgreSQL Relational Database Schema* template, so that it comes with the `Connection`, `ConnectorType` and `Endpoint` for `jdbc:postgresql://host.docker.internal:5442/<database>?currentSchema=<schema>` and the secrets store holding the credentials.  Its qualified name is `PostgreSQL Relational Database Schema::Coco PostgreSQL Server 1::<database>.<schema>`.  It is linked to the database manager with `CapabilityAssetUse` (use type `OWNS`).
3. **Adds the schema asset as a catalog target** of the `JDBCDatabaseCataloguer` integration connector, which catalogues the schema's tables and columns under the schema asset (`<schema qualified name>::<table>::<column>`) and keeps them up to date.
4. **Refreshes the cataloguer** and checks that every table the schema defines has been catalogued.

Each step looks for what already exists before creating anything, so the notebook can be re-run.

## Running it

Open [creating-system-data-layer.ipynb](creating-system-data-layer.ipynb) in JupyterLab and run the cells in order.  Step 1 runs as `garygeeke`, because the systems sit in governance zones only the infrastructure team may update and `SupportedSoftwareCapability` changes the system.  Everything from the creation of the schema assets onwards runs as `peterprofile`.  It needs, already in Egeria:

* the Coco core systems from `CocoComboArchive.omarchive`
* the Austin and Bucharest systems from [extending-the-systems-inventory.ipynb](../extending-the-systems-inventory/extending-the-systems-inventory.ipynb)
* the PostgreSQL content pack, which supplies the schema template and the `JDBCDatabaseCataloguer` connector.

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
