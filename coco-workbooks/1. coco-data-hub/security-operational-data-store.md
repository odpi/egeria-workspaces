# Security Operational Data Store

> **Author:** Ivor Padlock (Chief Security Officer)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-11-17
> **Description:** Fills the `security_ods` database with Egeria's security observability digital products - one table for each product - through a daily subscription to the Security Observability product family in the Open Metadata Digital Product Catalog.

---

# Overview

Egeria publishes digital products of its own: extracts of the open metadata ecosystem, each a table of values,
catalogued in the *Open Metadata Digital Product Catalog*.  Peter Profile's
[egeria-operational-data-store.md](egeria-operational-data-store.md) subscribes to most of them, and delivers them
to the `egeria_ods` database.

The products of the **Security Observability** family are the exception.  They describe the secrets that the
platform uses and the activity of its users, so they are in the security governance zone: only the security team
can see them.  Peter cannot see the family, so he cannot subscribe to it, and its products do not belong in
`egeria_ods`, which every user of the catalogue may read.

This file builds a separate operational data store for them.  `security_ods` is a database on the hub's PostgreSQL
server that holds one table for each of the security observability products, so that the security team can query
them with SQL.  The subscription is taken out by Ivor Padlock, the Chief Security Officer.

| Product family | Schema in `security_ods` | What it delivers |
|---|---|---|
| Security Observability | `security_observability` | Insights into security, including the nested Secrets Observability and User Observability families |

A subscription to a family delivers every product in it - including the products of the families nested inside it,
and products that are added later.

The file has three parts:

1. **Catalogue the database.**  The `security_ods` database is created empty with the PostgreSQL server
   (`compose-configs/shared-infra/docker-entrypoint-initdb.d/init_security_ods.sql`).  A governance action process
   describes it in Egeria and attaches it to the integration connector that catalogues databases, so the schema and
   tables that appear in it are catalogued and kept up to date.
2. **Describe the destination.**  A subscription to a product family delivers to a collection of tables: a database
   schema that receives one table for each product.  It is described from the
   *PostgreSQL Tabular Data Set Collection* template.  Egeria's provisioning services create the schema and its
   tables when they first deliver.
3. **Subscribe.**  The destination is subscribed to the family, using the family's daily refresh subscription
   type.  A daily refresh subscription delivers the family's products once a day, starting from the time of the
   subscription.

Run this file once, as Ivor Padlock.  Its commands are actions rather than definitions.  Running the cataloguing
process again is harmless - it finds the database it has already catalogued - but the other commands do not look
for what is already there, so a second run asks for a second description of the destination and a second
subscription to it.

In PostgreSQL, only two database users may connect to `security_ods`: `provisioner`, which delivers the products,
and `surveyor`, which the cataloguing connector uses.  The users that read `egeria_ods` have no access to it.

---

# Cataloguing the database

The process is the one that `setting-up-the-data-hub.ipynb` runs for `coco_data_hub`, with the same server name, so
`security_ods` is catalogued as another database of *Coco PostgreSQL Server 1*.  It runs in the background.

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
- databaseName: security_ods
- databaseDescription: The security team's operational data store.  It holds one table for each open metadata digital product of the Security Observability product family, refreshed by a subscription to the family in the Open Metadata Digital Product Catalog.

### Journal Entry

Catalogue the security_ods database so that the tables delivered to it are described in open metadata.

___

---

# Subscribing to the product family

The section below describes the family's destination and then subscribes the destination to the family.  The
destination's connection uses the `provisioner` database user from the *PostgreSQL Provisioning Secret*, which may
create schemas and tables in `security_ods`.  The subscription is requested by Ivor Padlock.

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
- databaseName: security_ods
- schemaName: security_observability
- schemaDescription: The products of the Security Observability product family, one table for each product, delivered by a daily subscription to the family.

___

## Initiate Subscription

### Subscription Type

ProvisioningActionProcess::Security Observability::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester

Person::USA::499888

### Destination Data Set

PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::security_ods.security_observability

### Journal Entry

The security operational data store subscribes to the Security Observability product family: its products are delivered to security_ods.security_observability once a day.

___

---

License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
