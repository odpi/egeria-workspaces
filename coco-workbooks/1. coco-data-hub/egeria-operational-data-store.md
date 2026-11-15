# Egeria Operational Data Store

> **Author:** Peter Profile (Solution Architect)
> **Version:** 1.1
> **Status:** ACTIVE
> **Date:** 2026-11-15
> **Description:** Fills the `egeria_ods` database with Egeria's open metadata digital products - one table for each product - through a daily subscription to each of the top-level product families in the Open Metadata Digital Product Catalog.

---

# Overview

The Data Sharing Hub delivers Coco Pharmaceuticals' own digital products to the systems that subscribe to them
(see [digital-product-subscriptions.md](digital-product-subscriptions.md)).  Egeria publishes digital products too:
extracts of the open metadata ecosystem, such as the list of departments, the valid metadata values and the latest
survey reports, catalogued in the *Open Metadata Digital Product Catalog*.  Each product is a table of values.

This file builds an operational data store for them.  `egeria_ods` is a database on the hub's PostgreSQL server that
holds one table for each of Egeria's products, so that the content of the open metadata ecosystem can be queried
with SQL, joined, and used by the reporting tools alongside Coco's own data.

Egeria's products are organized into **product families**.  A subscription to a family delivers every product in
it - including the products of the families nested inside it, and products that are added later.  The families sit
in a catalog folder called *Digital Products derived from Open Metadata*.  The folder itself is not a product, so it cannot be subscribed to;
instead this file subscribes to each of the families directly beneath it:

| Product family | Schema in `egeria_ods` | What it delivers |
|---|---|---|
| Valid Metadata Value Sets | `valid_metadata_value_sets` | The valid values that Egeria accepts for the properties of open metadata elements |
| Reference Data Sets | `reference_data_sets` | The reference data sets managed in open metadata |
| Open Metadata Types | `open_metadata_types` | The open metadata types: their attributes, relationships and classifications |
| Actor, Places and Products | `actor_places_and_products` | The master data about people, teams, organizations, locations and products, including the nested Organization Structure and Organization Observability families |
| Survey Reports | `survey_reports` | The results of the surveys that Egeria has run against the organization's resources |
| Governance Observability | `governance_observability` | Insights into the activity of the governance program |
| IT Operations Observability | `it_operations_observability` | Insights into the operation of the IT infrastructure that Egeria monitors |
| Security Observability | `security_observability` | Insights into security, including the nested Secrets Observability and User Observability families |

The file has three parts:

1. **Catalogue the database.**  The `egeria_ods` database is created empty with the PostgreSQL server
   (`compose-configs/shared-infra/docker-entrypoint-initdb.d/init_egeria_ods.sql`).  A governance action process
   describes it in Egeria and attaches it to the integration connector that catalogues databases, so the schemas and
   tables that appear in it are catalogued and kept up to date.
2. **Describe the destinations.**  A subscription to a product family delivers to a collection of tables: a database
   schema that receives one table for each product.  Each family has its own schema, described from the
   *PostgreSQL Tabular Data Set Collection* template.  Egeria's provisioning services create the schema and its
   tables when they first deliver.
3. **Subscribe.**  Each destination is subscribed to its family, using the family's daily refresh subscription
   type.  A daily refresh subscription delivers the family's products once a day, starting from the time of the
   subscription.

These are the same steps that `setting-up-the-data-hub.ipynb` and `digital-product-subscriptions.md` take for Coco's
own databases and products; here they are all Dr.Egeria commands, so the whole set-up can be validated before it is
run.

Run this file once.  Its commands are actions rather than definitions.  Running the cataloguing process again is
harmless - it finds the database it has already catalogued - but the other commands do not look for what is already
there, so a second run asks for a second description of each destination and a second subscription to it.

When Egeria adds a top-level family to the catalog folder, add a section for it here.

---

# Cataloguing the database

The process is the one that `setting-up-the-data-hub.ipynb` runs for `coco_data_hub`, with the same server name, so
`egeria_ods` is catalogued as another database of *Coco PostgreSQL Server 1*.  It runs in the background.

___

## Initiate Governance Action Process

### Governance Action Process

PostgreSQLDatabase::CreateAsCatalogTargetGovernanceActionProcess

### Request Parameters

- serverName: Coco PostgreSQL Server 1
- hostIdentifier: host.docker.internal
- portNumber: 5442
- secretsStorePathName: secrets/integration.omsecrets
- secretsCollectionName: PostgreSQL Server Secret
- versionIdentifier: 1.0
- databaseName: egeria_ods
- databaseDescription: Egeria's operational data store.  It holds one table for each open metadata digital product, refreshed by subscriptions to the product families of the Open Metadata Digital Product Catalog.

### Journal Entry

Catalogue the egeria_ods database so that the tables delivered to it are described in open metadata.

___

---

# Subscribing to the product families

Each section below describes a family's destination and then subscribes the destination to the family.  The
destinations' connections use the `provisioner` database user from the *PostgreSQL Provisioning Secret*, which may
create schemas and tables in `egeria_ods`.  The subscriptions are requested by Peter Profile.

---

## Valid Metadata Value Sets

Delivers the valid values that Egeria accepts for the properties of open metadata elements.

___

## Create Element

### Element Type Name

TabularDataSetCollection

### Template GUID

3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values

- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: egeria_ods
- schemaName: valid_metadata_value_sets
- schemaDescription: The products of the Valid Metadata Value Sets product family, one table for each product, delivered by a daily subscription to the family.

___

## Initiate Subscription

### Subscription Type

ProvisioningActionProcess::Valid Metadata Value Sets::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester

Person::UK::986419

### Destination Data Set

PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::egeria_ods.valid_metadata_value_sets

### Journal Entry

The Egeria operational data store subscribes to the Valid Metadata Value Sets product family: its products are delivered to egeria_ods.valid_metadata_value_sets once a day.

___

---

## Reference Data Sets

Delivers the reference data sets managed in open metadata.

___

## Create Element

### Element Type Name

TabularDataSetCollection

### Template GUID

3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values

- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: egeria_ods
- schemaName: reference_data_sets
- schemaDescription: The products of the Reference Data Sets product family, one table for each product, delivered by a daily subscription to the family.

___

## Initiate Subscription

### Subscription Type

ProvisioningActionProcess::Reference Data Sets::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester

Person::UK::986419

### Destination Data Set

PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::egeria_ods.reference_data_sets

### Journal Entry

The Egeria operational data store subscribes to the Reference Data Sets product family: its products are delivered to egeria_ods.reference_data_sets once a day.

___

---

## Open Metadata Types

Delivers the open metadata types: their attributes, relationships and classifications.

___

## Create Element

### Element Type Name

TabularDataSetCollection

### Template GUID

3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values

- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: egeria_ods
- schemaName: open_metadata_types
- schemaDescription: The products of the Open Metadata Types product family, one table for each product, delivered by a daily subscription to the family.

___

## Initiate Subscription

### Subscription Type

ProvisioningActionProcess::Open Metadata Types::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester

Person::UK::986419

### Destination Data Set

PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::egeria_ods.open_metadata_types

### Journal Entry

The Egeria operational data store subscribes to the Open Metadata Types product family: its products are delivered to egeria_ods.open_metadata_types once a day.

___

---

## Actor, Places and Products

Delivers the master data about people, teams, organizations, locations and products, including the nested Organization Structure and Organization Observability families.

___

## Create Element

### Element Type Name

TabularDataSetCollection

### Template GUID

3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values

- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: egeria_ods
- schemaName: actor_places_and_products
- schemaDescription: The products of the Actor, Places and Products product family, one table for each product, delivered by a daily subscription to the family.

___

## Initiate Subscription

### Subscription Type

ProvisioningActionProcess::Actor, Places and Products::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester

Person::UK::986419

### Destination Data Set

PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::egeria_ods.actor_places_and_products

### Journal Entry

The Egeria operational data store subscribes to the Actor, Places and Products product family: its products are delivered to egeria_ods.actor_places_and_products once a day.

___

---

## Survey Reports

Delivers the results of the surveys that Egeria has run against the organization's resources.

___

## Create Element

### Element Type Name

TabularDataSetCollection

### Template GUID

3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values

- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: egeria_ods
- schemaName: survey_reports
- schemaDescription: The products of the Survey Reports product family, one table for each product, delivered by a daily subscription to the family.

___

## Initiate Subscription

### Subscription Type

ProvisioningActionProcess::Survey Reports::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester

Person::UK::986419

### Destination Data Set

PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::egeria_ods.survey_reports

### Journal Entry

The Egeria operational data store subscribes to the Survey Reports product family: its products are delivered to egeria_ods.survey_reports once a day.

___

---

## Governance Observability

Delivers insights into the activity of the governance program.

___

## Create Element

### Element Type Name

TabularDataSetCollection

### Template GUID

3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values

- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: egeria_ods
- schemaName: governance_observability
- schemaDescription: The products of the Governance Observability product family, one table for each product, delivered by a daily subscription to the family.

___

## Initiate Subscription

### Subscription Type

ProvisioningActionProcess::Governance Observability::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester

Person::UK::986419

### Destination Data Set

PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::egeria_ods.governance_observability

### Journal Entry

The Egeria operational data store subscribes to the Governance Observability product family: its products are delivered to egeria_ods.governance_observability once a day.

___

---

## IT Operations Observability

Delivers insights into the operation of the IT infrastructure that Egeria monitors.

___

## Create Element

### Element Type Name

TabularDataSetCollection

### Template GUID

3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values

- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: egeria_ods
- schemaName: it_operations_observability
- schemaDescription: The products of the IT Operations Observability product family, one table for each product, delivered by a daily subscription to the family.

___

## Initiate Subscription

### Subscription Type

ProvisioningActionProcess::IT Operations Observability::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester

Person::UK::986419

### Destination Data Set

PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::egeria_ods.it_operations_observability

### Journal Entry

The Egeria operational data store subscribes to the IT Operations Observability product family: its products are delivered to egeria_ods.it_operations_observability once a day.

___

---

## Security Observability

Delivers insights into security, including the nested Secrets Observability and User Observability families.

___

## Create Element

### Element Type Name

TabularDataSetCollection

### Template GUID

3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7

### Placeholder Property Values

- hostIdentifier: host.docker.internal
- serverName: Coco PostgreSQL Server 1
- portNumber: 5442
- secretsCollectionName: PostgreSQL Provisioning Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: egeria_ods
- schemaName: security_observability
- schemaDescription: The products of the Security Observability product family, one table for each product, delivered by a daily subscription to the family.

___

## Initiate Subscription

### Subscription Type

ProvisioningActionProcess::Security Observability::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester

Person::UK::986419

### Destination Data Set

PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::egeria_ods.security_observability

### Journal Entry

The Egeria operational data store subscribes to the Security Observability product family: its products are delivered to egeria_ods.security_observability once a day.

___

---

License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
