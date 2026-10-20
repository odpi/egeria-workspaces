# Digital Product Subscriptions

> **Author:** Peter Profile (Solution Architect), Erin Overview (Information Architect)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-10-19
> **Description:** Subscribes the Coco Pharmaceuticals systems to the strategic digital products they depend on, so that the data each product receives in the Data Sharing Hub is delivered to the systems that need it.

---

# Overview

Each system that supplies a digital product copies every change it makes into the product's tables in the Data
Sharing Hub straight away (the `coco_feed_*` DAGs).  This file sets up the other half of each supply chain: the
**subscriptions** that deliver the products' data to the systems that consume it.  The subscriptions follow
[product-subscriptions.csv](mapping-the-systems/data/product-subscriptions.csv): a system subscribes to a product when
it implements a solution component whose own product depends on it, and the reporting stores `coco_ods` and
`coco_sus` subscribe to the products that fill their reports.

Egeria delivers a subscription by running a provisioning pipeline that copies the product's tables into the
subscriber's **destination** - the subscriber's own schema in the `subscription_staging` database, holding the
product's tables plus delivery columns.  The `coco_subscriptions_*` DAGs then apply what has been delivered to the
subscribing system's own tables.

## What a subscription needs

A product can be subscribed to once it has

* a **product manager** - an actor assigned to the product.  Each business system group's products are assigned to
  that group's *Digital Product Manager* role;
* **subscription types** - the ways of subscribing to it.  Each one is a governance action process,
  `ProvisioningActionProcess::<product name>::Create Subscription::<identifier>`, which `Initiate Subscription` runs;
* a **license type** and a **service level objective** for each subscription type, granted to the subscriber.  The
  products use the licenses and service level objectives from Egeria's digital products content pack: products about
  identifiable people are licensed as *Personal Information*, everything else as *Data for Internal Use*.

## Kinds of subscription

The subscriptions use five subscription types, so that each way Egeria delivers a product is exercised:

| Subscription type | Kind | Delivery | Used for | Subscriptions |
|---|---|---|---|---|
| Ongoing update subscription | `ONGOING_UPDATE` | when the product's data changes, at most every 5 minutes | operational systems that act on the data as it arrives | 129 |
| Hourly refresh subscription | `PERIODIC` | every hour | batch interfaces into the ERP, finance and people systems | 50 |
| Daily refresh subscription | `PERIODIC` | every day | the `coco_ods` and `coco_sus` reporting stores | 11 |
| Weekly refresh subscription | `PERIODIC` | every week | records, regulatory and catalogue systems | 13 |
| Evaluation subscription | `ONE_TIME` | once | EKG Pharmaceuticals (Bucharest), assessing the group's master data, privacy and patient treatment products before integrating with them | 2 |

An *ongoing update* subscription is triggered by changes to the product's **monitored resources**: here, the
product's tables as Egeria's PostgreSQL cataloguer records them when `setting-up-the-data-hub.ipynb` catalogues the
`coco_data_hub` database (`PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::<schema>::<table>`).
Each time a `coco_feed_*` DAG loads a product table, Airflow's OpenLineage event about the load resolves to that
table, its `DataScope` classification is refreshed, and Egeria's subscription manager (Baudot) runs the deliveries.
So connect OpenLineage to Egeria after the hub has been catalogued - see *Before you start* in the
[README](README.md).  Periodic and one-time subscriptions are run by Baudot on its ten-minute refresh.

## Products waiting for a source

44 of the 249 subscriptions in the list are to products that no system supplies yet - the
products classified as promises in [promises.md](strategic-digital-products/promises.md).  They are not set up here,
since there is nothing to deliver; add them when the products have a source.

| Subscriber | Product |
|---|---|
| Austin HazMat Inventory (Coco core) | Incidents And Near Misses |
| Coco HazMat Inventory (Coco core) | Incidents And Near Misses |
| Coco Product Management (Coco core) | New Product Definitions |
| Informatica MDM (Austin) | New Product Definitions |
| Microsoft Purview DLP (Austin) | Open Metadata Catalogue Holdings |
| Global Manufacturing Planning (Coco core) | Patient Pseudonym Register |
| SAP ERP S/4HANA (Bucharest) | Patient Pseudonym Register |
| SAP S/4HANA (Austin) | Patient Pseudonym Register |
| Global Manufacturing Planning (Coco core) | Patient Sample Consignments |
| Proact Cold Chain Monitor (Bucharest) | Patient Sample Consignments |
| SAP ERP S/4HANA (Bucharest) | Patient Sample Consignments |
| SAP S/4HANA (Austin) | Patient Sample Consignments |
| Siemens Opcenter MES (Bucharest) | Patient Sample Consignments |
| Coco Pharmaceuticals Procurement (Coco core) | Payment Anomaly Findings |
| Informatica MDM (Austin) | Payment Anomaly Findings |
| SAP ERP S/4HANA (Bucharest) | Payment Anomaly Findings |
| Veeva Vault RIM (Bucharest) | Pharmacovigilance Cases |
| Coco Ledgers (Coco core) | Purchase Orders And Receipts |
| Coco Pharmaceuticals Operational Data Store (Coco core) | Purchase Orders And Receipts |
| SAP Ariba SRM (Austin) | Purchase Orders And Receipts |
| SAP ERP S/4HANA (Bucharest) | Purchase Orders And Receipts |
| SAP S/4HANA (Austin) | Purchase Orders And Receipts |
| Cornerstone OnDemand LMS (Austin) | Qualification Expiry Warnings |
| Human Resources Information Manager (HRIM) (Coco core) | Rights Fulfilment Actions |
| Workday HCM (Bucharest) | Rights Fulfilment Actions |
| Workday Human Capital Management (Austin) | Rights Fulfilment Actions |
| Trackwise Digital (Bucharest) | Safety Signals |
| Veeva Vault QMS (Austin) | Safety Signals |
| Veeva Vault QMS (Bucharest) | Safety Signals |
| Veeva Vault RIM (Bucharest) | Safety Signals |
| Rockwell FactoryTalk (Bucharest) | Serial Number Allocations |
| Rockwell FactoryTalk SCADA (Austin) | Serial Number Allocations |
| Austin Inventory (Coco core) | Serialised Product Identifiers |
| Coco Inventory (Coco core) | Serialised Product Identifiers |
| Manhattan WMS (Austin) | Serialised Product Identifiers |
| Warehouse Management System (WMS) (Bucharest) | Serialised Product Identifiers |
| Austin Manufacturing Control System (Coco core) | Temperature Excursion Assessments |
| Edmonton Manufacturing Control System (Coco core) | Temperature Excursion Assessments |
| OpenText ECM (Bucharest) | Temperature Excursion Assessments |
| Siemens Opcenter MES (Bucharest) | Temperature Excursion Assessments |
| Veeva Vault EBR (Austin) | Temperature Excursion Assessments |
| Winchester Manufacturing Control System (Coco core) | Temperature Excursion Assessments |
| Coco Pharmaceuticals Procurement (Coco core) | Third Party Screening Results |
| SAP Ariba SRM (Austin) | Third Party Screening Results |

---

# Product managers

Each business system group's products are managed by the group's Digital Product Manager role, which becomes the
products' owner in each subscription.

___

## Create Person Role

### Display Name
Delivery Digital Product Manager

### Qualified Name
PersonRole::Coco::Digital Product Manager::Delivery

### Description
Manages the Delivery digital products in the Coco Pharmaceuticals Strategic Digital Product Catalog: their definitions, their subscription types and the subscriptions taken out to them.

___

## Create Person Role

### Display Name
Finance Digital Product Manager

### Qualified Name
PersonRole::Coco::Digital Product Manager::Finance

### Description
Manages the Finance digital products in the Coco Pharmaceuticals Strategic Digital Product Catalog: their definitions, their subscription types and the subscriptions taken out to them.

___

## Create Person Role

### Display Name
Manufacturing Digital Product Manager

### Qualified Name
PersonRole::Coco::Digital Product Manager::Manufacturing

### Description
Manages the Manufacturing digital products in the Coco Pharmaceuticals Strategic Digital Product Catalog: their definitions, their subscription types and the subscriptions taken out to them.

___

## Create Person Role

### Display Name
Master Data Management Digital Product Manager

### Qualified Name
PersonRole::Coco::Digital Product Manager::Master Data Management

### Description
Manages the Master Data Management digital products in the Coco Pharmaceuticals Strategic Digital Product Catalog: their definitions, their subscription types and the subscriptions taken out to them.

___

## Create Person Role

### Display Name
Patient Treatment Digital Product Manager

### Qualified Name
PersonRole::Coco::Digital Product Manager::Patient Treatment

### Description
Manages the Patient Treatment digital products in the Coco Pharmaceuticals Strategic Digital Product Catalog: their definitions, their subscription types and the subscriptions taken out to them.

___

## Create Person Role

### Display Name
People Systems Digital Product Manager

### Qualified Name
PersonRole::Coco::Digital Product Manager::People Systems

### Description
Manages the People Systems digital products in the Coco Pharmaceuticals Strategic Digital Product Catalog: their definitions, their subscription types and the subscriptions taken out to them.

___

## Create Person Role

### Display Name
Procurement Digital Product Manager

### Qualified Name
PersonRole::Coco::Digital Product Manager::Procurement

### Description
Manages the Procurement digital products in the Coco Pharmaceuticals Strategic Digital Product Catalog: their definitions, their subscription types and the subscriptions taken out to them.

___

## Create Person Role

### Display Name
Quality Systems Digital Product Manager

### Qualified Name
PersonRole::Coco::Digital Product Manager::Quality Systems

### Description
Manages the Quality Systems digital products in the Coco Pharmaceuticals Strategic Digital Product Catalog: their definitions, their subscription types and the subscriptions taken out to them.

___

## Create Person Role

### Display Name
Warehouse Digital Product Manager

### Qualified Name
PersonRole::Coco::Digital Product Manager::Warehouse

### Description
Manages the Warehouse digital products in the Coco Pharmaceuticals Strategic Digital Product Catalog: their definitions, their subscription types and the subscriptions taken out to them.

___

---

# Delivery

## Carrier Transit Events

2 subscriber(s): Siemens Opcenter MES (Bucharest, ongoing update subscription), Proact Cold Chain Monitor (Bucharest, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Delivery

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Carrier Transit Events

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Carrier Transit Events

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::carrier_transit_events::transit_event

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: buc_opcenter_mes__carrier_transit_events
- schemaDescription: Siemens Opcenter MES (Bucharest) copy of the Carrier Transit Events digital product.  Cold Chain Transit Records depends on it (carrier journey events).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Carrier Transit Events::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opcenter_mes__carrier_transit_events

### Journal Entry
Siemens Opcenter MES subscribes to Carrier Transit Events: Cold Chain Transit Records depends on it (carrier journey events).

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
- databaseName: subscription_staging
- schemaName: buc_proact_cold_chain__carrier_transit_events
- schemaDescription: Proact Cold Chain Monitor (Bucharest) copy of the Carrier Transit Events digital product.  Cold Chain Transit Records depends on it (carrier journey events).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Carrier Transit Events::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_proact_cold_chain__carrier_transit_events

### Journal Entry
Proact Cold Chain Monitor subscribes to Carrier Transit Events: Cold Chain Transit Records depends on it (carrier journey events).

___

## Dangerous Goods Consignment Records

4 subscriber(s): Siemens Opcenter MES (Bucharest, ongoing update subscription), Proact Cold Chain Monitor (Bucharest, ongoing update subscription), Austin HazMat Inventory (Coco core, ongoing update subscription), Coco HazMat Inventory (Coco core, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Delivery

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Dangerous Goods Consignment Records

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Dangerous Goods Consignment Records

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::dangerous_goods_consignment_records::consignment_declaration
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::dangerous_goods_consignment_records::consignment_document

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: buc_opcenter_mes__dangerous_goods_consignment_records
- schemaDescription: Siemens Opcenter MES (Bucharest) copy of the Dangerous Goods Consignment Records digital product.  Carrier Transit Events depends on it (consigned to carrier).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Dangerous Goods Consignment Records::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opcenter_mes__dangerous_goods_consignment_records

### Journal Entry
Siemens Opcenter MES subscribes to Dangerous Goods Consignment Records: Carrier Transit Events depends on it (consigned to carrier).

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
- databaseName: subscription_staging
- schemaName: buc_proact_cold_chain__dangerous_goods_consignment_records
- schemaDescription: Proact Cold Chain Monitor (Bucharest) copy of the Dangerous Goods Consignment Records digital product.  Carrier Transit Events depends on it (consigned to carrier).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Dangerous Goods Consignment Records::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_proact_cold_chain__dangerous_goods_consignment_records

### Journal Entry
Proact Cold Chain Monitor subscribes to Dangerous Goods Consignment Records: Carrier Transit Events depends on it (consigned to carrier).

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
- databaseName: subscription_staging
- schemaName: coco_austin_haz_mat__dangerous_goods_consignment_records
- schemaDescription: Austin HazMat Inventory (Coco core) copy of the Dangerous Goods Consignment Records digital product.  Hazardous Material Holdings depends on it (consignment record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Dangerous Goods Consignment Records::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_austin_haz_mat__dangerous_goods_consignment_records

### Journal Entry
Austin HazMat Inventory subscribes to Dangerous Goods Consignment Records: Hazardous Material Holdings depends on it (consignment record).

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
- databaseName: subscription_staging
- schemaName: coco_haz_mat__dangerous_goods_consignment_records
- schemaDescription: Coco HazMat Inventory (Coco core) copy of the Dangerous Goods Consignment Records digital product.  Hazardous Material Holdings depends on it (consignment record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Dangerous Goods Consignment Records::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_haz_mat__dangerous_goods_consignment_records

### Journal Entry
Coco HazMat Inventory subscribes to Dangerous Goods Consignment Records: Hazardous Material Holdings depends on it (consignment record).

___

## In-Transit Temperature Readings

2 subscriber(s): Siemens Opcenter MES (Bucharest, ongoing update subscription), Proact Cold Chain Monitor (Bucharest, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Delivery

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::In-Transit Temperature Readings

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::In-Transit Temperature Readings

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::in_transit_temperature_readings::temperature_reading

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: buc_opcenter_mes__in_transit_temperature_readings
- schemaDescription: Siemens Opcenter MES (Bucharest) copy of the In-Transit Temperature Readings digital product.  Cold Chain Transit Records depends on it (transit temperature record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::In-Transit Temperature Readings::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opcenter_mes__in_transit_temperature_readings

### Journal Entry
Siemens Opcenter MES subscribes to In-Transit Temperature Readings: Cold Chain Transit Records depends on it (transit temperature record).

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
- databaseName: subscription_staging
- schemaName: buc_proact_cold_chain__in_transit_temperature_readings
- schemaDescription: Proact Cold Chain Monitor (Bucharest) copy of the In-Transit Temperature Readings digital product.  Cold Chain Transit Records depends on it (transit temperature record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::In-Transit Temperature Readings::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_proact_cold_chain__in_transit_temperature_readings

### Journal Entry
Proact Cold Chain Monitor subscribes to In-Transit Temperature Readings: Cold Chain Transit Records depends on it (transit temperature record).

___

## Therapy Delivery Events

5 subscriber(s): Oracle Order Management (Austin, ongoing update subscription), SAP S/4HANA (Austin, hourly refresh subscription), SAP ERP S/4HANA (Bucharest, hourly refresh subscription), Global customer ordering system (Coco core, ongoing update subscription), Coco Ledgers (Coco core, hourly refresh subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Delivery

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Therapy Delivery Events

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Therapy Delivery Events

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::therapy_delivery_events::administration_confirmation
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::therapy_delivery_events::delivery_event

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Therapy Delivery Events

### Subscription Kind
PERIODIC

### Display Name
Hourly refresh subscription

### Identifier
HOURLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination every hour.

### Subscription Notification Interval
60

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: aus_oracle_oms__therapy_delivery_events
- schemaDescription: Oracle Order Management (Austin) copy of the Therapy Delivery Events digital product.  Treatment Invoices depends on it (fulfilment confirmed).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Therapy Delivery Events::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_oracle_oms__therapy_delivery_events

### Journal Entry
Oracle Order Management subscribes to Therapy Delivery Events: Treatment Invoices depends on it (fulfilment confirmed).

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
- databaseName: subscription_staging
- schemaName: aus_sap_s4hana__therapy_delivery_events
- schemaDescription: SAP S/4HANA (Austin) copy of the Therapy Delivery Events digital product.  Treatment Invoices depends on it (fulfilment confirmed).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Therapy Delivery Events::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_sap_s4hana__therapy_delivery_events

### Journal Entry
SAP S/4HANA subscribes to Therapy Delivery Events: Treatment Invoices depends on it (fulfilment confirmed).

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
- databaseName: subscription_staging
- schemaName: buc_sap_s4hana__therapy_delivery_events
- schemaDescription: SAP ERP S/4HANA (Bucharest) copy of the Therapy Delivery Events digital product.  Treatment Invoices depends on it (fulfilment confirmed).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Therapy Delivery Events::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_sap_s4hana__therapy_delivery_events

### Journal Entry
SAP ERP S/4HANA subscribes to Therapy Delivery Events: Treatment Invoices depends on it (fulfilment confirmed).

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
- databaseName: subscription_staging
- schemaName: coco_global_crm__therapy_delivery_events
- schemaDescription: Global customer ordering system (Coco core) copy of the Therapy Delivery Events digital product.  Treatment Invoices depends on it (fulfilment confirmed).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Therapy Delivery Events::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_global_crm__therapy_delivery_events

### Journal Entry
Global customer ordering system subscribes to Therapy Delivery Events: Treatment Invoices depends on it (fulfilment confirmed).

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
- databaseName: subscription_staging
- schemaName: coco_ledgers__therapy_delivery_events
- schemaDescription: Coco Ledgers (Coco core) copy of the Therapy Delivery Events digital product.  Treatment Invoices depends on it (fulfilment confirmed).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Therapy Delivery Events::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ledgers__therapy_delivery_events

### Journal Entry
Coco Ledgers subscribes to Therapy Delivery Events: Treatment Invoices depends on it (fulfilment confirmed).

___

## Transport Classifications

6 subscriber(s): OpenText Trading Grid EDI (Austin, ongoing update subscription), Oracle TMS (Austin, ongoing update subscription), Warehouse Management System (WMS) (Bucharest, ongoing update subscription), Edmonton Depot Management System (Coco core, ongoing update subscription), Kansas City Depot Management System (Coco core, ongoing update subscription), Winchester Depot Management System (Coco core, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Delivery

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Transport Classifications

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Transport Classifications

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::transport_classifications::transport_classification

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: aus_opentext_edi__transport_classifications
- schemaDescription: OpenText Trading Grid EDI (Austin) copy of the Transport Classifications digital product.  Dangerous Goods Consignment Records depends on it (classification and requirements).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Transport Classifications::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_opentext_edi__transport_classifications

### Journal Entry
OpenText Trading Grid EDI subscribes to Transport Classifications: Dangerous Goods Consignment Records depends on it (classification and requirements).

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
- databaseName: subscription_staging
- schemaName: aus_oracle_tms__transport_classifications
- schemaDescription: Oracle TMS (Austin) copy of the Transport Classifications digital product.  Dangerous Goods Consignment Records depends on it (classification and requirements).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Transport Classifications::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_oracle_tms__transport_classifications

### Journal Entry
Oracle TMS subscribes to Transport Classifications: Dangerous Goods Consignment Records depends on it (classification and requirements).

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
- databaseName: subscription_staging
- schemaName: buc_ekg_wms__transport_classifications
- schemaDescription: Warehouse Management System (WMS) (Bucharest) copy of the Transport Classifications digital product.  Dangerous Goods Consignment Records depends on it (classification and requirements).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Transport Classifications::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_ekg_wms__transport_classifications

### Journal Entry
Warehouse Management System (WMS) subscribes to Transport Classifications: Dangerous Goods Consignment Records depends on it (classification and requirements).

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
- databaseName: subscription_staging
- schemaName: coco_eddepot01__transport_classifications
- schemaDescription: Edmonton Depot Management System (Coco core) copy of the Transport Classifications digital product.  Dangerous Goods Consignment Records depends on it (classification and requirements).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Transport Classifications::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_eddepot01__transport_classifications

### Journal Entry
Edmonton Depot Management System subscribes to Transport Classifications: Dangerous Goods Consignment Records depends on it (classification and requirements).

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
- databaseName: subscription_staging
- schemaName: coco_kcdepot01__transport_classifications
- schemaDescription: Kansas City Depot Management System (Coco core) copy of the Transport Classifications digital product.  Dangerous Goods Consignment Records depends on it (classification and requirements).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Transport Classifications::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_kcdepot01__transport_classifications

### Journal Entry
Kansas City Depot Management System subscribes to Transport Classifications: Dangerous Goods Consignment Records depends on it (classification and requirements).

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
- databaseName: subscription_staging
- schemaName: coco_winchdepot01__transport_classifications
- schemaDescription: Winchester Depot Management System (Coco core) copy of the Transport Classifications digital product.  Dangerous Goods Consignment Records depends on it (classification and requirements).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Transport Classifications::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_winchdepot01__transport_classifications

### Journal Entry
Winchester Depot Management System subscribes to Transport Classifications: Dangerous Goods Consignment Records depends on it (classification and requirements).

___

---

# Finance

## Employee Expense Claims

5 subscriber(s): SAP S/4HANA (Austin, hourly refresh subscription), SAP Concur (Bucharest, hourly refresh subscription), SAP ERP S/4HANA (Bucharest, hourly refresh subscription), Coco Expenses (Coco core, hourly refresh subscription), Coco Pharmaceuticals Sustainability Data Marts (Coco core, daily refresh subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Finance

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Employee Expense Claims

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Employee Expense Claims

### Subscription Kind
PERIODIC

### Display Name
Hourly refresh subscription

### Identifier
HOURLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination every hour.

### Subscription Notification Interval
60

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-PERSONAL-DATA::Personal Information

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Employee Expense Claims

### Subscription Kind
PERIODIC

### Display Name
Daily refresh subscription

### Identifier
DAILY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a day.

### Subscription Notification Interval
1440

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-PERSONAL-DATA::Personal Information

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-DAILY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each day

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
- databaseName: subscription_staging
- schemaName: aus_sap_s4hana__employee_expense_claims
- schemaDescription: SAP S/4HANA (Austin) copy of the Employee Expense Claims digital product.  Subledger Postings depends on it (expense postings).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Employee Expense Claims::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_sap_s4hana__employee_expense_claims

### Journal Entry
SAP S/4HANA subscribes to Employee Expense Claims: Subledger Postings depends on it (expense postings).

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
- databaseName: subscription_staging
- schemaName: buc_sap_concur__employee_expense_claims
- schemaDescription: SAP Concur (Bucharest) copy of the Employee Expense Claims digital product.  Expense Approvals depends on it (submit for approval).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Employee Expense Claims::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_sap_concur__employee_expense_claims

### Journal Entry
SAP Concur subscribes to Employee Expense Claims: Expense Approvals depends on it (submit for approval).

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
- databaseName: subscription_staging
- schemaName: buc_sap_s4hana__employee_expense_claims
- schemaDescription: SAP ERP S/4HANA (Bucharest) copy of the Employee Expense Claims digital product.  Subledger Postings depends on it (expense postings).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Employee Expense Claims::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_sap_s4hana__employee_expense_claims

### Journal Entry
SAP ERP S/4HANA subscribes to Employee Expense Claims: Subledger Postings depends on it (expense postings).

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
- databaseName: subscription_staging
- schemaName: coco_expenses__employee_expense_claims
- schemaDescription: Coco Expenses (Coco core) copy of the Employee Expense Claims digital product.  Expense Approvals depends on it (submit for approval).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Employee Expense Claims::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_expenses__employee_expense_claims

### Journal Entry
Coco Expenses subscribes to Employee Expense Claims: Expense Approvals depends on it (submit for approval).

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
- databaseName: subscription_staging
- schemaName: coco_sus__employee_expense_claims
- schemaDescription: Coco Pharmaceuticals Sustainability Data Marts (Coco core) copy of the Employee Expense Claims digital product.  reporting: fills ghg_emissions.biz_travel, customer_travel.

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Employee Expense Claims::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_sus__employee_expense_claims

### Journal Entry
Coco Pharmaceuticals Sustainability Data Marts subscribes to Employee Expense Claims: reporting: fills ghg_emissions.biz_travel, customer_travel.

___

## Expense Approvals

2 subscriber(s): SAP Concur (Bucharest, hourly refresh subscription), Coco Expenses (Coco core, hourly refresh subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Finance

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Expense Approvals

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Expense Approvals

### Subscription Kind
PERIODIC

### Display Name
Hourly refresh subscription

### Identifier
HOURLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination every hour.

### Subscription Notification Interval
60

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: buc_sap_concur__expense_approvals
- schemaDescription: SAP Concur (Bucharest) copy of the Expense Approvals digital product.  Employee Expense Claims depends on it (approval decision).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Expense Approvals::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_sap_concur__expense_approvals

### Journal Entry
SAP Concur subscribes to Expense Approvals: Employee Expense Claims depends on it (approval decision).

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
- databaseName: subscription_staging
- schemaName: coco_expenses__expense_approvals
- schemaDescription: Coco Expenses (Coco core) copy of the Expense Approvals digital product.  Employee Expense Claims depends on it (approval decision).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Expense Approvals::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_expenses__expense_approvals

### Journal Entry
Coco Expenses subscribes to Expense Approvals: Employee Expense Claims depends on it (approval decision).

___

## General Ledger Balances

3 subscriber(s): SAP S/4HANA (Austin, hourly refresh subscription), SAP ERP S/4HANA (Bucharest, hourly refresh subscription), Coco Ledgers (Coco core, hourly refresh subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Finance

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::General Ledger Balances

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::General Ledger Balances

### Subscription Kind
PERIODIC

### Display Name
Hourly refresh subscription

### Identifier
HOURLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination every hour.

### Subscription Notification Interval
60

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: aus_sap_s4hana__general_ledger_balances
- schemaDescription: SAP S/4HANA (Austin) copy of the General Ledger Balances digital product.  Manual Journal Approvals depends on it (material entries for review).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::General Ledger Balances::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_sap_s4hana__general_ledger_balances

### Journal Entry
SAP S/4HANA subscribes to General Ledger Balances: Manual Journal Approvals depends on it (material entries for review).

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
- databaseName: subscription_staging
- schemaName: buc_sap_s4hana__general_ledger_balances
- schemaDescription: SAP ERP S/4HANA (Bucharest) copy of the General Ledger Balances digital product.  Manual Journal Approvals depends on it (material entries for review).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::General Ledger Balances::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_sap_s4hana__general_ledger_balances

### Journal Entry
SAP ERP S/4HANA subscribes to General Ledger Balances: Manual Journal Approvals depends on it (material entries for review).

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
- databaseName: subscription_staging
- schemaName: coco_ledgers__general_ledger_balances
- schemaDescription: Coco Ledgers (Coco core) copy of the General Ledger Balances digital product.  Manual Journal Approvals depends on it (material entries for review).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::General Ledger Balances::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ledgers__general_ledger_balances

### Journal Entry
Coco Ledgers subscribes to General Ledger Balances: Manual Journal Approvals depends on it (material entries for review).

___

## Manual Journal Approvals

3 subscriber(s): SAP S/4HANA (Austin, hourly refresh subscription), SAP ERP S/4HANA (Bucharest, hourly refresh subscription), Coco Ledgers (Coco core, hourly refresh subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Finance

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Manual Journal Approvals

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Manual Journal Approvals

### Subscription Kind
PERIODIC

### Display Name
Hourly refresh subscription

### Identifier
HOURLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination every hour.

### Subscription Notification Interval
60

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: aus_sap_s4hana__manual_journal_approvals
- schemaDescription: SAP S/4HANA (Austin) copy of the Manual Journal Approvals digital product.  General Ledger Balances depends on it (approved adjustments).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Manual Journal Approvals::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_sap_s4hana__manual_journal_approvals

### Journal Entry
SAP S/4HANA subscribes to Manual Journal Approvals: General Ledger Balances depends on it (approved adjustments).

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
- databaseName: subscription_staging
- schemaName: buc_sap_s4hana__manual_journal_approvals
- schemaDescription: SAP ERP S/4HANA (Bucharest) copy of the Manual Journal Approvals digital product.  General Ledger Balances depends on it (approved adjustments).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Manual Journal Approvals::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_sap_s4hana__manual_journal_approvals

### Journal Entry
SAP ERP S/4HANA subscribes to Manual Journal Approvals: General Ledger Balances depends on it (approved adjustments).

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
- databaseName: subscription_staging
- schemaName: coco_ledgers__manual_journal_approvals
- schemaDescription: Coco Ledgers (Coco core) copy of the Manual Journal Approvals digital product.  General Ledger Balances depends on it (approved adjustments).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Manual Journal Approvals::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ledgers__manual_journal_approvals

### Journal Entry
Coco Ledgers subscribes to Manual Journal Approvals: General Ledger Balances depends on it (approved adjustments).

___

## Subledger Postings

3 subscriber(s): SAP S/4HANA (Austin, hourly refresh subscription), SAP ERP S/4HANA (Bucharest, hourly refresh subscription), Coco Ledgers (Coco core, hourly refresh subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Finance

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Subledger Postings

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Subledger Postings

### Subscription Kind
PERIODIC

### Display Name
Hourly refresh subscription

### Identifier
HOURLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination every hour.

### Subscription Notification Interval
60

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: aus_sap_s4hana__subledger_postings
- schemaDescription: SAP S/4HANA (Austin) copy of the Subledger Postings digital product.  General Ledger Balances depends on it (post transactions).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Subledger Postings::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_sap_s4hana__subledger_postings

### Journal Entry
SAP S/4HANA subscribes to Subledger Postings: General Ledger Balances depends on it (post transactions).

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
- databaseName: subscription_staging
- schemaName: buc_sap_s4hana__subledger_postings
- schemaDescription: SAP ERP S/4HANA (Bucharest) copy of the Subledger Postings digital product.  General Ledger Balances depends on it (post transactions).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Subledger Postings::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_sap_s4hana__subledger_postings

### Journal Entry
SAP ERP S/4HANA subscribes to Subledger Postings: General Ledger Balances depends on it (post transactions).

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
- databaseName: subscription_staging
- schemaName: coco_ledgers__subledger_postings
- schemaDescription: Coco Ledgers (Coco core) copy of the Subledger Postings digital product.  General Ledger Balances depends on it (post transactions).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Subledger Postings::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ledgers__subledger_postings

### Journal Entry
Coco Ledgers subscribes to Subledger Postings: General Ledger Balances depends on it (post transactions).

___

## Supplier Payment Detail Changes

3 subscriber(s): Informatica MDM (Austin, ongoing update subscription), SAP ERP S/4HANA (Bucharest, hourly refresh subscription), Coco Pharmaceuticals Procurement (Coco core, hourly refresh subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Finance

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Supplier Payment Detail Changes

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Supplier Payment Detail Changes

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::supplier_payment_detail_changes::payment_detail_change
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::supplier_payment_detail_changes::verification_evidence

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Supplier Payment Detail Changes

### Subscription Kind
PERIODIC

### Display Name
Hourly refresh subscription

### Identifier
HOURLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination every hour.

### Subscription Notification Interval
60

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: aus_informatica_mdm__supplier_payment_detail_changes
- schemaDescription: Informatica MDM (Austin) copy of the Supplier Payment Detail Changes digital product.  Supplier Master Data depends on it (verified bank details).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Payment Detail Changes::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_informatica_mdm__supplier_payment_detail_changes

### Journal Entry
Informatica MDM subscribes to Supplier Payment Detail Changes: Supplier Master Data depends on it (verified bank details).

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
- databaseName: subscription_staging
- schemaName: buc_sap_s4hana__supplier_payment_detail_changes
- schemaDescription: SAP ERP S/4HANA (Bucharest) copy of the Supplier Payment Detail Changes digital product.  Supplier Master Data depends on it (verified bank details).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Payment Detail Changes::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_sap_s4hana__supplier_payment_detail_changes

### Journal Entry
SAP ERP S/4HANA subscribes to Supplier Payment Detail Changes: Supplier Master Data depends on it (verified bank details).

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
- databaseName: subscription_staging
- schemaName: coco_procurement01__supplier_payment_detail_changes
- schemaDescription: Coco Pharmaceuticals Procurement (Coco core) copy of the Supplier Payment Detail Changes digital product.  Supplier Master Data depends on it (verified bank details).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Payment Detail Changes::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_procurement01__supplier_payment_detail_changes

### Journal Entry
Coco Pharmaceuticals Procurement subscribes to Supplier Payment Detail Changes: Supplier Master Data depends on it (verified bank details).

___

## Supplier Payments

4 subscriber(s): SAP S/4HANA (Austin, hourly refresh subscription), SAP ERP S/4HANA (Bucharest, hourly refresh subscription), Coco Pharmaceuticals Operational Data Store (Coco core, daily refresh subscription), Coco Pharmaceuticals Sustainability Data Marts (Coco core, daily refresh subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Finance

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Supplier Payments

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Supplier Payments

### Subscription Kind
PERIODIC

### Display Name
Hourly refresh subscription

### Identifier
HOURLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination every hour.

### Subscription Notification Interval
60

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Supplier Payments

### Subscription Kind
PERIODIC

### Display Name
Daily refresh subscription

### Identifier
DAILY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a day.

### Subscription Notification Interval
1440

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-DAILY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each day

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
- databaseName: subscription_staging
- schemaName: aus_sap_s4hana__supplier_payments
- schemaDescription: SAP S/4HANA (Austin) copy of the Supplier Payments digital product.  Subledger Postings depends on it (payment postings).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Payments::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_sap_s4hana__supplier_payments

### Journal Entry
SAP S/4HANA subscribes to Supplier Payments: Subledger Postings depends on it (payment postings).

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
- databaseName: subscription_staging
- schemaName: buc_sap_s4hana__supplier_payments
- schemaDescription: SAP ERP S/4HANA (Bucharest) copy of the Supplier Payments digital product.  Subledger Postings depends on it (payment postings).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Payments::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_sap_s4hana__supplier_payments

### Journal Entry
SAP ERP S/4HANA subscribes to Supplier Payments: Subledger Postings depends on it (payment postings).

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
- databaseName: subscription_staging
- schemaName: coco_ods__supplier_payments
- schemaDescription: Coco Pharmaceuticals Operational Data Store (Coco core) copy of the Supplier Payments digital product.  reporting: fills supplier_invoices.

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Payments::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ods__supplier_payments

### Journal Entry
Coco Pharmaceuticals Operational Data Store subscribes to Supplier Payments: reporting: fills supplier_invoices.

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
- databaseName: subscription_staging
- schemaName: coco_sus__supplier_payments
- schemaDescription: Coco Pharmaceuticals Sustainability Data Marts (Coco core) copy of the Supplier Payments digital product.  reporting: fills ghg_emissions.power and transport (energy and fuel invoices).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Payments::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_sus__supplier_payments

### Journal Entry
Coco Pharmaceuticals Sustainability Data Marts subscribes to Supplier Payments: reporting: fills ghg_emissions.power and transport (energy and fuel invoices).

___

## Treatment Invoices

3 subscriber(s): SAP S/4HANA (Austin, hourly refresh subscription), SAP ERP S/4HANA (Bucharest, hourly refresh subscription), Coco Pharmaceuticals Operational Data Store (Coco core, daily refresh subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Finance

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Treatment Invoices

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Treatment Invoices

### Subscription Kind
PERIODIC

### Display Name
Hourly refresh subscription

### Identifier
HOURLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination every hour.

### Subscription Notification Interval
60

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Treatment Invoices

### Subscription Kind
PERIODIC

### Display Name
Daily refresh subscription

### Identifier
DAILY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a day.

### Subscription Notification Interval
1440

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-DAILY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each day

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
- databaseName: subscription_staging
- schemaName: aus_sap_s4hana__treatment_invoices
- schemaDescription: SAP S/4HANA (Austin) copy of the Treatment Invoices digital product.  Subledger Postings depends on it (revenue postings).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Treatment Invoices::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_sap_s4hana__treatment_invoices

### Journal Entry
SAP S/4HANA subscribes to Treatment Invoices: Subledger Postings depends on it (revenue postings).

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
- databaseName: subscription_staging
- schemaName: buc_sap_s4hana__treatment_invoices
- schemaDescription: SAP ERP S/4HANA (Bucharest) copy of the Treatment Invoices digital product.  Subledger Postings depends on it (revenue postings).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Treatment Invoices::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_sap_s4hana__treatment_invoices

### Journal Entry
SAP ERP S/4HANA subscribes to Treatment Invoices: Subledger Postings depends on it (revenue postings).

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
- databaseName: subscription_staging
- schemaName: coco_ods__treatment_invoices
- schemaDescription: Coco Pharmaceuticals Operational Data Store (Coco core) copy of the Treatment Invoices digital product.  reporting: fills orders (invoiced values).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Treatment Invoices::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ods__treatment_invoices

### Journal Entry
Coco Pharmaceuticals Operational Data Store subscribes to Treatment Invoices: reporting: fills orders (invoiced values).

___

---

# Manufacturing

## Batch Execution Records

9 subscriber(s): Veeva Vault EBR (Austin, ongoing update subscription), Veeva Vault QMS (Austin, ongoing update subscription), Siemens Opcenter MES (Bucharest, ongoing update subscription), OpenText ECM (Bucharest, weekly refresh subscription), Trackwise Digital (Bucharest, ongoing update subscription), Veeva Vault QMS (Bucharest, ongoing update subscription), Edmonton Manufacturing Control System (Coco core, ongoing update subscription), Austin Manufacturing Control System (Coco core, ongoing update subscription), Winchester Manufacturing Control System (Coco core, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Manufacturing

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Batch Execution Records

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Batch Execution Records

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::batch_execution_records::equipment_usage
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::batch_execution_records::execution_step
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::batch_execution_records::material_usage

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Batch Execution Records

### Subscription Kind
PERIODIC

### Display Name
Weekly refresh subscription

### Identifier
WEEKLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a week.

### Subscription Notification Interval
10080

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WEEKLY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each week

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
- databaseName: subscription_staging
- schemaName: aus_veeva_ebr__batch_execution_records
- schemaDescription: Veeva Vault EBR (Austin) copy of the Batch Execution Records digital product.  Electronic Batch Records depends on it (execution record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Batch Execution Records::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_veeva_ebr__batch_execution_records

### Journal Entry
Veeva Vault EBR subscribes to Batch Execution Records: Electronic Batch Records depends on it (execution record).

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
- databaseName: subscription_staging
- schemaName: aus_veeva_qms__batch_execution_records
- schemaDescription: Veeva Vault QMS (Austin) copy of the Batch Execution Records digital product.  Deviations And CAPAs depends on it (raise deviation).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Batch Execution Records::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_veeva_qms__batch_execution_records

### Journal Entry
Veeva Vault QMS subscribes to Batch Execution Records: Deviations And CAPAs depends on it (raise deviation).

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
- databaseName: subscription_staging
- schemaName: buc_opcenter_mes__batch_execution_records
- schemaDescription: Siemens Opcenter MES (Bucharest) copy of the Batch Execution Records digital product.  Electronic Batch Records depends on it (execution record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Batch Execution Records::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opcenter_mes__batch_execution_records

### Journal Entry
Siemens Opcenter MES subscribes to Batch Execution Records: Electronic Batch Records depends on it (execution record).

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
- databaseName: subscription_staging
- schemaName: buc_opentext_ecm__batch_execution_records
- schemaDescription: OpenText ECM (Bucharest) copy of the Batch Execution Records digital product.  Electronic Batch Records depends on it (execution record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Batch Execution Records::Create Subscription::WEEKLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opentext_ecm__batch_execution_records

### Journal Entry
OpenText ECM subscribes to Batch Execution Records: Electronic Batch Records depends on it (execution record).

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
- databaseName: subscription_staging
- schemaName: buc_trackwise__batch_execution_records
- schemaDescription: Trackwise Digital (Bucharest) copy of the Batch Execution Records digital product.  Deviations And CAPAs depends on it (raise deviation).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Batch Execution Records::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_trackwise__batch_execution_records

### Journal Entry
Trackwise Digital subscribes to Batch Execution Records: Deviations And CAPAs depends on it (raise deviation).

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
- databaseName: subscription_staging
- schemaName: buc_veeva_qms__batch_execution_records
- schemaDescription: Veeva Vault QMS (Bucharest) copy of the Batch Execution Records digital product.  Deviations And CAPAs depends on it (raise deviation).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Batch Execution Records::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_veeva_qms__batch_execution_records

### Journal Entry
Veeva Vault QMS subscribes to Batch Execution Records: Deviations And CAPAs depends on it (raise deviation).

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
- databaseName: subscription_staging
- schemaName: coco_ed_mfg_control__batch_execution_records
- schemaDescription: Edmonton Manufacturing Control System (Coco core) copy of the Batch Execution Records digital product.  Electronic Batch Records depends on it (execution record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Batch Execution Records::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ed_mfg_control__batch_execution_records

### Journal Entry
Edmonton Manufacturing Control System subscribes to Batch Execution Records: Electronic Batch Records depends on it (execution record).

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
- databaseName: subscription_staging
- schemaName: coco_mfctrl9482__batch_execution_records
- schemaDescription: Austin Manufacturing Control System (Coco core) copy of the Batch Execution Records digital product.  Electronic Batch Records depends on it (execution record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Batch Execution Records::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_mfctrl9482__batch_execution_records

### Journal Entry
Austin Manufacturing Control System subscribes to Batch Execution Records: Electronic Batch Records depends on it (execution record).

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
- databaseName: subscription_staging
- schemaName: coco_winch_mfg_control__batch_execution_records
- schemaDescription: Winchester Manufacturing Control System (Coco core) copy of the Batch Execution Records digital product.  Electronic Batch Records depends on it (execution record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Batch Execution Records::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_winch_mfg_control__batch_execution_records

### Journal Entry
Winchester Manufacturing Control System subscribes to Batch Execution Records: Electronic Batch Records depends on it (execution record).

___

## Electronic Batch Records

4 subscriber(s): Veeva Vault EBR (Austin, ongoing update subscription), Veeva Vault QMS (Austin, ongoing update subscription), Siemens Opcenter MES (Bucharest, ongoing update subscription), Veeva Vault QMS (Bucharest, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Manufacturing

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Electronic Batch Records

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Electronic Batch Records

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::electronic_batch_records::batch_record
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::electronic_batch_records::batch_record_section
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::electronic_batch_records::release_authorisation

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: aus_veeva_ebr__electronic_batch_records
- schemaDescription: Veeva Vault EBR (Austin) copy of the Electronic Batch Records digital product.  Batch Certification Decisions depends on it (batch record for review).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Electronic Batch Records::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_veeva_ebr__electronic_batch_records

### Journal Entry
Veeva Vault EBR subscribes to Electronic Batch Records: Batch Certification Decisions depends on it (batch record for review).

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
- databaseName: subscription_staging
- schemaName: aus_veeva_qms__electronic_batch_records
- schemaDescription: Veeva Vault QMS (Austin) copy of the Electronic Batch Records digital product.  Batch Certification Decisions depends on it (batch record for review).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Electronic Batch Records::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_veeva_qms__electronic_batch_records

### Journal Entry
Veeva Vault QMS subscribes to Electronic Batch Records: Batch Certification Decisions depends on it (batch record for review).

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
- databaseName: subscription_staging
- schemaName: buc_opcenter_mes__electronic_batch_records
- schemaDescription: Siemens Opcenter MES (Bucharest) copy of the Electronic Batch Records digital product.  Batch Certification Decisions depends on it (batch record for review).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Electronic Batch Records::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opcenter_mes__electronic_batch_records

### Journal Entry
Siemens Opcenter MES subscribes to Electronic Batch Records: Batch Certification Decisions depends on it (batch record for review).

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
- databaseName: subscription_staging
- schemaName: buc_veeva_qms__electronic_batch_records
- schemaDescription: Veeva Vault QMS (Bucharest) copy of the Electronic Batch Records digital product.  Batch Certification Decisions depends on it (batch record for review).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Electronic Batch Records::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_veeva_qms__electronic_batch_records

### Journal Entry
Veeva Vault QMS subscribes to Electronic Batch Records: Batch Certification Decisions depends on it (batch record for review).

___

## Equipment Qualification Status

5 subscriber(s): Siemens Opcenter MES (Austin, ongoing update subscription), Siemens Opcenter MES (Bucharest, ongoing update subscription), Edmonton Manufacturing Control System (Coco core, ongoing update subscription), Austin Manufacturing Control System (Coco core, ongoing update subscription), Winchester Manufacturing Control System (Coco core, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Manufacturing

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Equipment Qualification Status

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Equipment Qualification Status

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::equipment_qualification_status::equipment
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::equipment_qualification_status::qualification_status

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: aus_opcenter_mes__equipment_qualification_status
- schemaDescription: Siemens Opcenter MES (Austin) copy of the Equipment Qualification Status digital product.  Batch Execution Records depends on it (qualification status).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Equipment Qualification Status::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_opcenter_mes__equipment_qualification_status

### Journal Entry
Siemens Opcenter MES subscribes to Equipment Qualification Status: Batch Execution Records depends on it (qualification status).

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
- databaseName: subscription_staging
- schemaName: buc_opcenter_mes__equipment_qualification_status
- schemaDescription: Siemens Opcenter MES (Bucharest) copy of the Equipment Qualification Status digital product.  Batch Execution Records depends on it (qualification status).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Equipment Qualification Status::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opcenter_mes__equipment_qualification_status

### Journal Entry
Siemens Opcenter MES subscribes to Equipment Qualification Status: Batch Execution Records depends on it (qualification status).

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
- databaseName: subscription_staging
- schemaName: coco_ed_mfg_control__equipment_qualification_status
- schemaDescription: Edmonton Manufacturing Control System (Coco core) copy of the Equipment Qualification Status digital product.  Batch Execution Records depends on it (qualification status).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Equipment Qualification Status::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ed_mfg_control__equipment_qualification_status

### Journal Entry
Edmonton Manufacturing Control System subscribes to Equipment Qualification Status: Batch Execution Records depends on it (qualification status).

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
- databaseName: subscription_staging
- schemaName: coco_mfctrl9482__equipment_qualification_status
- schemaDescription: Austin Manufacturing Control System (Coco core) copy of the Equipment Qualification Status digital product.  Batch Execution Records depends on it (qualification status).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Equipment Qualification Status::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_mfctrl9482__equipment_qualification_status

### Journal Entry
Austin Manufacturing Control System subscribes to Equipment Qualification Status: Batch Execution Records depends on it (qualification status).

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
- databaseName: subscription_staging
- schemaName: coco_winch_mfg_control__equipment_qualification_status
- schemaDescription: Winchester Manufacturing Control System (Coco core) copy of the Equipment Qualification Status digital product.  Batch Execution Records depends on it (qualification status).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Equipment Qualification Status::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_winch_mfg_control__equipment_qualification_status

### Journal Entry
Winchester Manufacturing Control System subscribes to Equipment Qualification Status: Batch Execution Records depends on it (qualification status).

___

## Personalised Manufacturing Schedule

6 subscriber(s): Veeva Vault EBR (Austin, ongoing update subscription), Siemens Opcenter MES (Bucharest, ongoing update subscription), OpenText ECM (Bucharest, weekly refresh subscription), Edmonton Manufacturing Control System (Coco core, ongoing update subscription), Austin Manufacturing Control System (Coco core, ongoing update subscription), Winchester Manufacturing Control System (Coco core, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Manufacturing

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Personalised Manufacturing Schedule

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Personalised Manufacturing Schedule

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::personalised_manufacturing_schedule::manufacturing_slot
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::personalised_manufacturing_schedule::patient_material_receipt

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-PERSONAL-DATA::Personal Information

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Personalised Manufacturing Schedule

### Subscription Kind
PERIODIC

### Display Name
Weekly refresh subscription

### Identifier
WEEKLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a week.

### Subscription Notification Interval
10080

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-PERSONAL-DATA::Personal Information

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WEEKLY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each week

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
- databaseName: subscription_staging
- schemaName: aus_veeva_ebr__personalised_manufacturing_schedule
- schemaDescription: Veeva Vault EBR (Austin) copy of the Personalised Manufacturing Schedule digital product.  Electronic Batch Records depends on it (open batch).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Personalised Manufacturing Schedule::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_veeva_ebr__personalised_manufacturing_schedule

### Journal Entry
Veeva Vault EBR subscribes to Personalised Manufacturing Schedule: Electronic Batch Records depends on it (open batch).

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
- databaseName: subscription_staging
- schemaName: buc_opcenter_mes__personalised_manufacturing_schedule
- schemaDescription: Siemens Opcenter MES (Bucharest) copy of the Personalised Manufacturing Schedule digital product.  Electronic Batch Records depends on it (open batch).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Personalised Manufacturing Schedule::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opcenter_mes__personalised_manufacturing_schedule

### Journal Entry
Siemens Opcenter MES subscribes to Personalised Manufacturing Schedule: Electronic Batch Records depends on it (open batch).

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
- databaseName: subscription_staging
- schemaName: buc_opentext_ecm__personalised_manufacturing_schedule
- schemaDescription: OpenText ECM (Bucharest) copy of the Personalised Manufacturing Schedule digital product.  Electronic Batch Records depends on it (open batch).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Personalised Manufacturing Schedule::Create Subscription::WEEKLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opentext_ecm__personalised_manufacturing_schedule

### Journal Entry
OpenText ECM subscribes to Personalised Manufacturing Schedule: Electronic Batch Records depends on it (open batch).

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
- databaseName: subscription_staging
- schemaName: coco_ed_mfg_control__personalised_manufacturing_schedule
- schemaDescription: Edmonton Manufacturing Control System (Coco core) copy of the Personalised Manufacturing Schedule digital product.  Electronic Batch Records depends on it (open batch).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Personalised Manufacturing Schedule::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ed_mfg_control__personalised_manufacturing_schedule

### Journal Entry
Edmonton Manufacturing Control System subscribes to Personalised Manufacturing Schedule: Electronic Batch Records depends on it (open batch).

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
- databaseName: subscription_staging
- schemaName: coco_mfctrl9482__personalised_manufacturing_schedule
- schemaDescription: Austin Manufacturing Control System (Coco core) copy of the Personalised Manufacturing Schedule digital product.  Electronic Batch Records depends on it (open batch).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Personalised Manufacturing Schedule::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_mfctrl9482__personalised_manufacturing_schedule

### Journal Entry
Austin Manufacturing Control System subscribes to Personalised Manufacturing Schedule: Electronic Batch Records depends on it (open batch).

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
- databaseName: subscription_staging
- schemaName: coco_winch_mfg_control__personalised_manufacturing_schedule
- schemaDescription: Winchester Manufacturing Control System (Coco core) copy of the Personalised Manufacturing Schedule digital product.  Electronic Batch Records depends on it (open batch).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Personalised Manufacturing Schedule::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_winch_mfg_control__personalised_manufacturing_schedule

### Journal Entry
Winchester Manufacturing Control System subscribes to Personalised Manufacturing Schedule: Electronic Batch Records depends on it (open batch).

___

## Process Parameter Time Series

6 subscriber(s): Veeva Vault EBR (Austin, ongoing update subscription), Siemens Opcenter MES (Bucharest, ongoing update subscription), OpenText ECM (Bucharest, weekly refresh subscription), Edmonton Manufacturing Control System (Coco core, ongoing update subscription), Austin Manufacturing Control System (Coco core, ongoing update subscription), Winchester Manufacturing Control System (Coco core, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Manufacturing

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Process Parameter Time Series

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Process Parameter Time Series

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::process_parameter_time_series::process_parameter_reading

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Process Parameter Time Series

### Subscription Kind
PERIODIC

### Display Name
Weekly refresh subscription

### Identifier
WEEKLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a week.

### Subscription Notification Interval
10080

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WEEKLY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each week

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
- databaseName: subscription_staging
- schemaName: aus_veeva_ebr__process_parameter_time_series
- schemaDescription: Veeva Vault EBR (Austin) copy of the Process Parameter Time Series digital product.  Electronic Batch Records depends on it (process parameters).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Process Parameter Time Series::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_veeva_ebr__process_parameter_time_series

### Journal Entry
Veeva Vault EBR subscribes to Process Parameter Time Series: Electronic Batch Records depends on it (process parameters).

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
- databaseName: subscription_staging
- schemaName: buc_opcenter_mes__process_parameter_time_series
- schemaDescription: Siemens Opcenter MES (Bucharest) copy of the Process Parameter Time Series digital product.  Electronic Batch Records depends on it (process parameters).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Process Parameter Time Series::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opcenter_mes__process_parameter_time_series

### Journal Entry
Siemens Opcenter MES subscribes to Process Parameter Time Series: Electronic Batch Records depends on it (process parameters).

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
- databaseName: subscription_staging
- schemaName: buc_opentext_ecm__process_parameter_time_series
- schemaDescription: OpenText ECM (Bucharest) copy of the Process Parameter Time Series digital product.  Electronic Batch Records depends on it (process parameters).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Process Parameter Time Series::Create Subscription::WEEKLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opentext_ecm__process_parameter_time_series

### Journal Entry
OpenText ECM subscribes to Process Parameter Time Series: Electronic Batch Records depends on it (process parameters).

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
- databaseName: subscription_staging
- schemaName: coco_ed_mfg_control__process_parameter_time_series
- schemaDescription: Edmonton Manufacturing Control System (Coco core) copy of the Process Parameter Time Series digital product.  Electronic Batch Records depends on it (process parameters).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Process Parameter Time Series::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ed_mfg_control__process_parameter_time_series

### Journal Entry
Edmonton Manufacturing Control System subscribes to Process Parameter Time Series: Electronic Batch Records depends on it (process parameters).

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
- databaseName: subscription_staging
- schemaName: coco_mfctrl9482__process_parameter_time_series
- schemaDescription: Austin Manufacturing Control System (Coco core) copy of the Process Parameter Time Series digital product.  Electronic Batch Records depends on it (process parameters).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Process Parameter Time Series::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_mfctrl9482__process_parameter_time_series

### Journal Entry
Austin Manufacturing Control System subscribes to Process Parameter Time Series: Electronic Batch Records depends on it (process parameters).

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
- databaseName: subscription_staging
- schemaName: coco_winch_mfg_control__process_parameter_time_series
- schemaDescription: Winchester Manufacturing Control System (Coco core) copy of the Process Parameter Time Series digital product.  Electronic Batch Records depends on it (process parameters).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Process Parameter Time Series::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_winch_mfg_control__process_parameter_time_series

### Journal Entry
Winchester Manufacturing Control System subscribes to Process Parameter Time Series: Electronic Batch Records depends on it (process parameters).

___

---

# Master Data Management

## Product Master Data

9 subscriber(s): Informatica IDMC (Austin, weekly refresh subscription), Informatica MDM (Austin, ongoing update subscription), Veeva Vault EBR (Austin, ongoing update subscription), Veeva Vault QMS (Austin, ongoing update subscription), Siemens Opcenter MES (Bucharest, evaluation subscription), Veeva Vault QMS (Bucharest, evaluation subscription), Austin HazMat Inventory (Coco core, ongoing update subscription), Coco HazMat Inventory (Coco core, ongoing update subscription), Coco Pharmaceuticals Operational Data Store (Coco core, daily refresh subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Master Data Management

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Product Master Data

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Product Master Data

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::product_master_data::authorised_market_assignment
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::product_master_data::handling_requirement
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::product_master_data::pack_configuration
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::product_master_data::product_definition

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Product Master Data

### Subscription Kind
PERIODIC

### Display Name
Daily refresh subscription

### Identifier
DAILY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a day.

### Subscription Notification Interval
1440

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-DAILY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each day

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Product Master Data

### Subscription Kind
PERIODIC

### Display Name
Weekly refresh subscription

### Identifier
WEEKLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a week.

### Subscription Notification Interval
10080

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WEEKLY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each week

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Product Master Data

### Subscription Kind
ONE_TIME

### Display Name
Evaluation subscription

### Identifier
EVALUATION-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination just once, so that the subscriber can evaluate it.

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-ONCE-ONLY::A complete copy of the product data is delivered to the product data's destination just once

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
- databaseName: subscription_staging
- schemaName: aus_informatica_idmc__product_master_data
- schemaDescription: Informatica IDMC (Austin) copy of the Product Master Data digital product.  Product Change Notifications depends on it (publish change).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Product Master Data::Create Subscription::WEEKLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_informatica_idmc__product_master_data

### Journal Entry
Informatica IDMC subscribes to Product Master Data: Product Change Notifications depends on it (publish change).

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
- databaseName: subscription_staging
- schemaName: aus_informatica_mdm__product_master_data
- schemaDescription: Informatica MDM (Austin) copy of the Product Master Data digital product.  Product Change Notifications depends on it (publish change).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Product Master Data::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_informatica_mdm__product_master_data

### Journal Entry
Informatica MDM subscribes to Product Master Data: Product Change Notifications depends on it (publish change).

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
- databaseName: subscription_staging
- schemaName: aus_veeva_ebr__product_master_data
- schemaDescription: Veeva Vault EBR (Austin) copy of the Product Master Data digital product.  Batch Certification Decisions depends on it (product and market requirements).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Product Master Data::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_veeva_ebr__product_master_data

### Journal Entry
Veeva Vault EBR subscribes to Product Master Data: Batch Certification Decisions depends on it (product and market requirements).

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
- databaseName: subscription_staging
- schemaName: aus_veeva_qms__product_master_data
- schemaDescription: Veeva Vault QMS (Austin) copy of the Product Master Data digital product.  Batch Certification Decisions depends on it (product and market requirements).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Product Master Data::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_veeva_qms__product_master_data

### Journal Entry
Veeva Vault QMS subscribes to Product Master Data: Batch Certification Decisions depends on it (product and market requirements).

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
- databaseName: subscription_staging
- schemaName: buc_opcenter_mes__product_master_data
- schemaDescription: Siemens Opcenter MES (Bucharest) copy of the Product Master Data digital product.  Batch Certification Decisions depends on it (product and market requirements).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Product Master Data::Create Subscription::EVALUATION-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opcenter_mes__product_master_data

### Journal Entry
Siemens Opcenter MES subscribes to Product Master Data: Batch Certification Decisions depends on it (product and market requirements).

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
- databaseName: subscription_staging
- schemaName: buc_veeva_qms__product_master_data
- schemaDescription: Veeva Vault QMS (Bucharest) copy of the Product Master Data digital product.  Batch Certification Decisions depends on it (product and market requirements).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Product Master Data::Create Subscription::EVALUATION-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_veeva_qms__product_master_data

### Journal Entry
Veeva Vault QMS subscribes to Product Master Data: Batch Certification Decisions depends on it (product and market requirements).

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
- databaseName: subscription_staging
- schemaName: coco_austin_haz_mat__product_master_data
- schemaDescription: Austin HazMat Inventory (Coco core) copy of the Product Master Data digital product.  Transport Classifications depends on it (product handling requirements).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Product Master Data::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_austin_haz_mat__product_master_data

### Journal Entry
Austin HazMat Inventory subscribes to Product Master Data: Transport Classifications depends on it (product handling requirements).

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
- databaseName: subscription_staging
- schemaName: coco_haz_mat__product_master_data
- schemaDescription: Coco HazMat Inventory (Coco core) copy of the Product Master Data digital product.  Transport Classifications depends on it (product handling requirements).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Product Master Data::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_haz_mat__product_master_data

### Journal Entry
Coco HazMat Inventory subscribes to Product Master Data: Transport Classifications depends on it (product handling requirements).

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
- databaseName: subscription_staging
- schemaName: coco_ods__product_master_data
- schemaDescription: Coco Pharmaceuticals Operational Data Store (Coco core) copy of the Product Master Data digital product.  reporting: fills products, categories.

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Product Master Data::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ods__product_master_data

### Journal Entry
Coco Pharmaceuticals Operational Data Store subscribes to Product Master Data: reporting: fills products, categories.

___

---

# Patient Treatment

## Clinician Adverse Reaction Reports

2 subscriber(s): ServiceNow Customer Service Management (Austin, ongoing update subscription), Veeva Vault QMS (Austin, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Patient Treatment

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Clinician Adverse Reaction Reports

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Clinician Adverse Reaction Reports

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::clinician_adverse_reaction_reports::clinician_reaction_report

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-PERSONAL-DATA::Personal Information

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: aus_servicenow_csm__clinician_adverse_reaction_reports
- schemaDescription: ServiceNow Customer Service Management (Austin) copy of the Clinician Adverse Reaction Reports digital product.  Consolidated Safety Reports depends on it (clinician report).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Clinician Adverse Reaction Reports::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_servicenow_csm__clinician_adverse_reaction_reports

### Journal Entry
ServiceNow Customer Service Management subscribes to Clinician Adverse Reaction Reports: Consolidated Safety Reports depends on it (clinician report).

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
- databaseName: subscription_staging
- schemaName: aus_veeva_qms__clinician_adverse_reaction_reports
- schemaDescription: Veeva Vault QMS (Austin) copy of the Clinician Adverse Reaction Reports digital product.  Consolidated Safety Reports depends on it (clinician report).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Clinician Adverse Reaction Reports::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_veeva_qms__clinician_adverse_reaction_reports

### Journal Entry
Veeva Vault QMS subscribes to Clinician Adverse Reaction Reports: Consolidated Safety Reports depends on it (clinician report).

___

## Treatment Orders

1 subscriber(s): Coco Pharmaceuticals Operational Data Store (Coco core, daily refresh subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Patient Treatment

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Treatment Orders

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Treatment Orders

### Subscription Kind
PERIODIC

### Display Name
Daily refresh subscription

### Identifier
DAILY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a day.

### Subscription Notification Interval
1440

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-PERSONAL-DATA::Personal Information

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-DAILY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each day

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
- databaseName: subscription_staging
- schemaName: coco_ods__treatment_orders
- schemaDescription: Coco Pharmaceuticals Operational Data Store (Coco core) copy of the Treatment Orders digital product.  reporting: fills orders, order_details.

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Treatment Orders::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ods__treatment_orders

### Journal Entry
Coco Pharmaceuticals Operational Data Store subscribes to Treatment Orders: reporting: fills orders, order_details.

___

---

# People Systems

## Corporate Directory Entries

1 subscriber(s): Coco Pharmaceuticals Operational Data Store (Coco core, daily refresh subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::People Systems

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Corporate Directory Entries

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Corporate Directory Entries

### Subscription Kind
PERIODIC

### Display Name
Daily refresh subscription

### Identifier
DAILY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a day.

### Subscription Notification Interval
1440

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-PERSONAL-DATA::Personal Information

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-DAILY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each day

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
- databaseName: subscription_staging
- schemaName: coco_ods__corporate_directory_entries
- schemaDescription: Coco Pharmaceuticals Operational Data Store (Coco core) copy of the Corporate Directory Entries digital product.  reporting: fills employees (names, titles, phones), units_by_location.

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Corporate Directory Entries::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ods__corporate_directory_entries

### Journal Entry
Coco Pharmaceuticals Operational Data Store subscribes to Corporate Directory Entries: reporting: fills employees (names, titles, phones), units_by_location.

___

## Payroll Results

2 subscriber(s): SAP S/4HANA (Austin, hourly refresh subscription), SAP ERP S/4HANA (Bucharest, hourly refresh subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::People Systems

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Payroll Results

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Payroll Results

### Subscription Kind
PERIODIC

### Display Name
Hourly refresh subscription

### Identifier
HOURLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination every hour.

### Subscription Notification Interval
60

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-PERSONAL-DATA::Personal Information

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: aus_sap_s4hana__payroll_results
- schemaDescription: SAP S/4HANA (Austin) copy of the Payroll Results digital product.  Subledger Postings depends on it (payroll postings).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Payroll Results::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_sap_s4hana__payroll_results

### Journal Entry
SAP S/4HANA subscribes to Payroll Results: Subledger Postings depends on it (payroll postings).

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
- databaseName: subscription_staging
- schemaName: buc_sap_s4hana__payroll_results
- schemaDescription: SAP ERP S/4HANA (Bucharest) copy of the Payroll Results digital product.  Subledger Postings depends on it (payroll postings).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Payroll Results::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_sap_s4hana__payroll_results

### Journal Entry
SAP ERP S/4HANA subscribes to Payroll Results: Subledger Postings depends on it (payroll postings).

___

## Role Competency Requirements

1 subscriber(s): Cornerstone OnDemand LMS (Austin, weekly refresh subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::People Systems

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Role Competency Requirements

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Role Competency Requirements

### Subscription Kind
PERIODIC

### Display Name
Weekly refresh subscription

### Identifier
WEEKLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a week.

### Subscription Notification Interval
10080

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-PERSONAL-DATA::Personal Information

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WEEKLY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each week

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
- databaseName: subscription_staging
- schemaName: aus_cornerstone_lms__role_competency_requirements
- schemaDescription: Cornerstone OnDemand LMS (Austin) copy of the Role Competency Requirements digital product.  Training Completions depends on it (required competencies).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Role Competency Requirements::Create Subscription::WEEKLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_cornerstone_lms__role_competency_requirements

### Journal Entry
Cornerstone OnDemand LMS subscribes to Role Competency Requirements: Training Completions depends on it (required competencies).

___

## Training Completions

2 subscriber(s): Cornerstone OnDemand LMS (Austin, weekly refresh subscription), Human Resources Information Manager (HRIM) (Coco core, hourly refresh subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::People Systems

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Training Completions

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Training Completions

### Subscription Kind
PERIODIC

### Display Name
Hourly refresh subscription

### Identifier
HOURLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination every hour.

### Subscription Notification Interval
60

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-PERSONAL-DATA::Personal Information

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Training Completions

### Subscription Kind
PERIODIC

### Display Name
Weekly refresh subscription

### Identifier
WEEKLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a week.

### Subscription Notification Interval
10080

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-PERSONAL-DATA::Personal Information

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WEEKLY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each week

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
- databaseName: subscription_staging
- schemaName: aus_cornerstone_lms__training_completions
- schemaDescription: Cornerstone OnDemand LMS (Austin) copy of the Training Completions digital product.  Worker Qualifications depends on it (completion and assessment).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Training Completions::Create Subscription::WEEKLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_cornerstone_lms__training_completions

### Journal Entry
Cornerstone OnDemand LMS subscribes to Training Completions: Worker Qualifications depends on it (completion and assessment).

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
- databaseName: subscription_staging
- schemaName: coco_hrim__training_completions
- schemaDescription: Human Resources Information Manager (HRIM) (Coco core) copy of the Training Completions digital product.  Worker Qualifications depends on it (completion and assessment).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Training Completions::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_hrim__training_completions

### Journal Entry
Human Resources Information Manager (HRIM) subscribes to Training Completions: Worker Qualifications depends on it (completion and assessment).

___

## Worker Lifecycle Events

3 subscriber(s): Workday Human Capital Management (Austin, hourly refresh subscription), Workday HCM (Bucharest, hourly refresh subscription), Human Resources Information Manager (HRIM) (Coco core, hourly refresh subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::People Systems

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Worker Lifecycle Events

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Worker Lifecycle Events

### Subscription Kind
PERIODIC

### Display Name
Hourly refresh subscription

### Identifier
HOURLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination every hour.

### Subscription Notification Interval
60

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-PERSONAL-DATA::Personal Information

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: aus_workday_hcm__worker_lifecycle_events
- schemaDescription: Workday Human Capital Management (Austin) copy of the Worker Lifecycle Events digital product.  Worker Master Data depends on it (worker event).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Lifecycle Events::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_workday_hcm__worker_lifecycle_events

### Journal Entry
Workday Human Capital Management subscribes to Worker Lifecycle Events: Worker Master Data depends on it (worker event).

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
- databaseName: subscription_staging
- schemaName: buc_workday_hcm__worker_lifecycle_events
- schemaDescription: Workday HCM (Bucharest) copy of the Worker Lifecycle Events digital product.  Worker Master Data depends on it (worker event).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Lifecycle Events::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_workday_hcm__worker_lifecycle_events

### Journal Entry
Workday HCM subscribes to Worker Lifecycle Events: Worker Master Data depends on it (worker event).

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
- databaseName: subscription_staging
- schemaName: coco_hrim__worker_lifecycle_events
- schemaDescription: Human Resources Information Manager (HRIM) (Coco core) copy of the Worker Lifecycle Events digital product.  Worker Master Data depends on it (worker event).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Lifecycle Events::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_hrim__worker_lifecycle_events

### Journal Entry
Human Resources Information Manager (HRIM) subscribes to Worker Lifecycle Events: Worker Master Data depends on it (worker event).

___

## Worker Master Data

19 subscriber(s): Microsoft Active Directory (Austin, ongoing update subscription), Cornerstone OnDemand LMS (Austin, weekly refresh subscription), Microsoft Entra ID (Austin, ongoing update subscription), Microsoft 365 (Austin, weekly refresh subscription), UKG Dimensions (Austin, hourly refresh subscription), Workday Human Capital Management (Austin, hourly refresh subscription), Active Directory (Bucharest, ongoing update subscription), Kronos Workforce (Bucharest, hourly refresh subscription), Microsoft 365 (Bucharest, weekly refresh subscription), SAP Concur (Bucharest, hourly refresh subscription), Workday HCM (Bucharest, hourly refresh subscription), Canadian payroll (Coco core, hourly refresh subscription), Coco Expenses (Coco core, hourly refresh subscription), Human Resources Information Manager (HRIM) (Coco core, hourly refresh subscription), Netherlands payroll (Coco core, hourly refresh subscription), Coco Pharmaceuticals Operational Data Store (Coco core, daily refresh subscription), SecAdmin (Coco core, ongoing update subscription), UK payroll (Coco core, hourly refresh subscription), CocoPages (Coco core, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::People Systems

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Worker Master Data

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Worker Master Data

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::worker_master_data::worker
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::worker_master_data::worker_assignment

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-PERSONAL-DATA::Personal Information

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Worker Master Data

### Subscription Kind
PERIODIC

### Display Name
Hourly refresh subscription

### Identifier
HOURLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination every hour.

### Subscription Notification Interval
60

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-PERSONAL-DATA::Personal Information

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Worker Master Data

### Subscription Kind
PERIODIC

### Display Name
Daily refresh subscription

### Identifier
DAILY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a day.

### Subscription Notification Interval
1440

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-PERSONAL-DATA::Personal Information

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-DAILY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each day

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Worker Master Data

### Subscription Kind
PERIODIC

### Display Name
Weekly refresh subscription

### Identifier
WEEKLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a week.

### Subscription Notification Interval
10080

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-PERSONAL-DATA::Personal Information

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WEEKLY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each week

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
- databaseName: subscription_staging
- schemaName: aus_active_directory__worker_master_data
- schemaDescription: Microsoft Active Directory (Austin) copy of the Worker Master Data digital product.  Access Entitlements depends on it (provision or revoke); Corporate Directory Entries depends on it (directory entry).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Master Data::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_active_directory__worker_master_data

### Journal Entry
Microsoft Active Directory subscribes to Worker Master Data: Access Entitlements depends on it (provision or revoke); Corporate Directory Entries depends on it (directory entry).

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
- databaseName: subscription_staging
- schemaName: aus_cornerstone_lms__worker_master_data
- schemaDescription: Cornerstone OnDemand LMS (Austin) copy of the Worker Master Data digital product.  Training Completions depends on it (worker and role); Worker Qualifications depends on it (new worker record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Master Data::Create Subscription::WEEKLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_cornerstone_lms__worker_master_data

### Journal Entry
Cornerstone OnDemand LMS subscribes to Worker Master Data: Training Completions depends on it (worker and role); Worker Qualifications depends on it (new worker record).

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
- databaseName: subscription_staging
- schemaName: aus_entra_id__worker_master_data
- schemaDescription: Microsoft Entra ID (Austin) copy of the Worker Master Data digital product.  Access Entitlements depends on it (provision or revoke).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Master Data::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_entra_id__worker_master_data

### Journal Entry
Microsoft Entra ID subscribes to Worker Master Data: Access Entitlements depends on it (provision or revoke).

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
- databaseName: subscription_staging
- schemaName: aus_microsoft_365__worker_master_data
- schemaDescription: Microsoft 365 (Austin) copy of the Worker Master Data digital product.  Corporate Directory Entries depends on it (directory entry).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Master Data::Create Subscription::WEEKLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_microsoft_365__worker_master_data

### Journal Entry
Microsoft 365 subscribes to Worker Master Data: Corporate Directory Entries depends on it (directory entry).

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
- databaseName: subscription_staging
- schemaName: aus_ukg_dimensions__worker_master_data
- schemaDescription: UKG Dimensions (Austin) copy of the Worker Master Data digital product.  Payroll Results depends on it (payroll record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Master Data::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_ukg_dimensions__worker_master_data

### Journal Entry
UKG Dimensions subscribes to Worker Master Data: Payroll Results depends on it (payroll record).

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
- databaseName: subscription_staging
- schemaName: aus_workday_hcm__worker_master_data
- schemaDescription: Workday Human Capital Management (Austin) copy of the Worker Master Data digital product.  Payroll Results depends on it (payroll record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Master Data::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_workday_hcm__worker_master_data

### Journal Entry
Workday Human Capital Management subscribes to Worker Master Data: Payroll Results depends on it (payroll record).

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
- databaseName: subscription_staging
- schemaName: buc_active_directory__worker_master_data
- schemaDescription: Active Directory (Bucharest) copy of the Worker Master Data digital product.  Access Entitlements depends on it (provision or revoke); Corporate Directory Entries depends on it (directory entry).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Master Data::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_active_directory__worker_master_data

### Journal Entry
Active Directory subscribes to Worker Master Data: Access Entitlements depends on it (provision or revoke); Corporate Directory Entries depends on it (directory entry).

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
- databaseName: subscription_staging
- schemaName: buc_kronos_workforce__worker_master_data
- schemaDescription: Kronos Workforce (Bucharest) copy of the Worker Master Data digital product.  Payroll Results depends on it (payroll record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Master Data::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_kronos_workforce__worker_master_data

### Journal Entry
Kronos Workforce subscribes to Worker Master Data: Payroll Results depends on it (payroll record).

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
- databaseName: subscription_staging
- schemaName: buc_microsoft_365__worker_master_data
- schemaDescription: Microsoft 365 (Bucharest) copy of the Worker Master Data digital product.  Corporate Directory Entries depends on it (directory entry).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Master Data::Create Subscription::WEEKLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_microsoft_365__worker_master_data

### Journal Entry
Microsoft 365 subscribes to Worker Master Data: Corporate Directory Entries depends on it (directory entry).

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
- databaseName: subscription_staging
- schemaName: buc_sap_concur__worker_master_data
- schemaDescription: SAP Concur (Bucharest) copy of the Worker Master Data digital product.  Employee Expense Claims depends on it (expense access); Expense Approvals depends on it (approver and cost centre).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Master Data::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_sap_concur__worker_master_data

### Journal Entry
SAP Concur subscribes to Worker Master Data: Employee Expense Claims depends on it (expense access); Expense Approvals depends on it (approver and cost centre).

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
- databaseName: subscription_staging
- schemaName: buc_workday_hcm__worker_master_data
- schemaDescription: Workday HCM (Bucharest) copy of the Worker Master Data digital product.  Payroll Results depends on it (payroll record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Master Data::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_workday_hcm__worker_master_data

### Journal Entry
Workday HCM subscribes to Worker Master Data: Payroll Results depends on it (payroll record).

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
- databaseName: subscription_staging
- schemaName: coco_ca_payroll__worker_master_data
- schemaDescription: Canadian payroll (Coco core) copy of the Worker Master Data digital product.  Payroll Results depends on it (payroll record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Master Data::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ca_payroll__worker_master_data

### Journal Entry
Canadian payroll subscribes to Worker Master Data: Payroll Results depends on it (payroll record).

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
- databaseName: subscription_staging
- schemaName: coco_expenses__worker_master_data
- schemaDescription: Coco Expenses (Coco core) copy of the Worker Master Data digital product.  Employee Expense Claims depends on it (expense access); Expense Approvals depends on it (approver and cost centre).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Master Data::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_expenses__worker_master_data

### Journal Entry
Coco Expenses subscribes to Worker Master Data: Employee Expense Claims depends on it (expense access); Expense Approvals depends on it (approver and cost centre).

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
- databaseName: subscription_staging
- schemaName: coco_hrim__worker_master_data
- schemaDescription: Human Resources Information Manager (HRIM) (Coco core) copy of the Worker Master Data digital product.  Worker Qualifications depends on it (new worker record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Master Data::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_hrim__worker_master_data

### Journal Entry
Human Resources Information Manager (HRIM) subscribes to Worker Master Data: Worker Qualifications depends on it (new worker record).

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
- databaseName: subscription_staging
- schemaName: coco_nl_payroll__worker_master_data
- schemaDescription: Netherlands payroll (Coco core) copy of the Worker Master Data digital product.  Payroll Results depends on it (payroll record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Master Data::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_nl_payroll__worker_master_data

### Journal Entry
Netherlands payroll subscribes to Worker Master Data: Payroll Results depends on it (payroll record).

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
- databaseName: subscription_staging
- schemaName: coco_ods__worker_master_data
- schemaDescription: Coco Pharmaceuticals Operational Data Store (Coco core) copy of the Worker Master Data digital product.  reporting: fills employees (employment details).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Master Data::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ods__worker_master_data

### Journal Entry
Coco Pharmaceuticals Operational Data Store subscribes to Worker Master Data: reporting: fills employees (employment details).

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
- databaseName: subscription_staging
- schemaName: coco_sec_admin__worker_master_data
- schemaDescription: SecAdmin (Coco core) copy of the Worker Master Data digital product.  Access Entitlements depends on it (provision or revoke).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Master Data::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_sec_admin__worker_master_data

### Journal Entry
SecAdmin subscribes to Worker Master Data: Access Entitlements depends on it (provision or revoke).

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
- databaseName: subscription_staging
- schemaName: coco_uk_payroll__worker_master_data
- schemaDescription: UK payroll (Coco core) copy of the Worker Master Data digital product.  Payroll Results depends on it (payroll record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Master Data::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_uk_payroll__worker_master_data

### Journal Entry
UK payroll subscribes to Worker Master Data: Payroll Results depends on it (payroll record).

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
- databaseName: subscription_staging
- schemaName: cocopages__worker_master_data
- schemaDescription: CocoPages (Coco core) copy of the Worker Master Data digital product.  Corporate Directory Entries depends on it (directory entry).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Master Data::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.cocopages__worker_master_data

### Journal Entry
CocoPages subscribes to Worker Master Data: Corporate Directory Entries depends on it (directory entry).

___

## Worker Qualifications

13 subscriber(s): Siemens Opcenter MES (Austin, ongoing update subscription), OpenText Trading Grid EDI (Austin, ongoing update subscription), Oracle TMS (Austin, ongoing update subscription), Veeva Vault EBR (Austin, ongoing update subscription), Warehouse Management System (WMS) (Bucharest, ongoing update subscription), Siemens Opcenter MES (Bucharest, ongoing update subscription), OpenText ECM (Bucharest, weekly refresh subscription), Edmonton Manufacturing Control System (Coco core, ongoing update subscription), Edmonton Depot Management System (Coco core, ongoing update subscription), Kansas City Depot Management System (Coco core, ongoing update subscription), Austin Manufacturing Control System (Coco core, ongoing update subscription), Winchester Manufacturing Control System (Coco core, ongoing update subscription), Winchester Depot Management System (Coco core, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::People Systems

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Worker Qualifications

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Worker Qualifications

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::worker_qualifications::worker_qualification

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-PERSONAL-DATA::Personal Information

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Worker Qualifications

### Subscription Kind
PERIODIC

### Display Name
Weekly refresh subscription

### Identifier
WEEKLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a week.

### Subscription Notification Interval
10080

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-PERSONAL-DATA::Personal Information

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WEEKLY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each week

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
- databaseName: subscription_staging
- schemaName: aus_opcenter_mes__worker_qualifications
- schemaDescription: Siemens Opcenter MES (Austin) copy of the Worker Qualifications digital product.  Batch Execution Records depends on it (operator qualification).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Qualifications::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_opcenter_mes__worker_qualifications

### Journal Entry
Siemens Opcenter MES subscribes to Worker Qualifications: Batch Execution Records depends on it (operator qualification).

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
- databaseName: subscription_staging
- schemaName: aus_opentext_edi__worker_qualifications
- schemaDescription: OpenText Trading Grid EDI (Austin) copy of the Worker Qualifications digital product.  Dangerous Goods Consignment Records depends on it (certificated signatory).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Qualifications::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_opentext_edi__worker_qualifications

### Journal Entry
OpenText Trading Grid EDI subscribes to Worker Qualifications: Dangerous Goods Consignment Records depends on it (certificated signatory).

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
- databaseName: subscription_staging
- schemaName: aus_oracle_tms__worker_qualifications
- schemaDescription: Oracle TMS (Austin) copy of the Worker Qualifications digital product.  Dangerous Goods Consignment Records depends on it (certificated signatory).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Qualifications::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_oracle_tms__worker_qualifications

### Journal Entry
Oracle TMS subscribes to Worker Qualifications: Dangerous Goods Consignment Records depends on it (certificated signatory).

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
- databaseName: subscription_staging
- schemaName: aus_veeva_ebr__worker_qualifications
- schemaDescription: Veeva Vault EBR (Austin) copy of the Worker Qualifications digital product.  Electronic Batch Records depends on it (signature authority).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Qualifications::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_veeva_ebr__worker_qualifications

### Journal Entry
Veeva Vault EBR subscribes to Worker Qualifications: Electronic Batch Records depends on it (signature authority).

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
- databaseName: subscription_staging
- schemaName: buc_ekg_wms__worker_qualifications
- schemaDescription: Warehouse Management System (WMS) (Bucharest) copy of the Worker Qualifications digital product.  Dangerous Goods Consignment Records depends on it (certificated signatory).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Qualifications::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_ekg_wms__worker_qualifications

### Journal Entry
Warehouse Management System (WMS) subscribes to Worker Qualifications: Dangerous Goods Consignment Records depends on it (certificated signatory).

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
- databaseName: subscription_staging
- schemaName: buc_opcenter_mes__worker_qualifications
- schemaDescription: Siemens Opcenter MES (Bucharest) copy of the Worker Qualifications digital product.  Batch Execution Records depends on it (operator qualification); Electronic Batch Records depends on it (signature authority).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Qualifications::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opcenter_mes__worker_qualifications

### Journal Entry
Siemens Opcenter MES subscribes to Worker Qualifications: Batch Execution Records depends on it (operator qualification); Electronic Batch Records depends on it (signature authority).

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
- databaseName: subscription_staging
- schemaName: buc_opentext_ecm__worker_qualifications
- schemaDescription: OpenText ECM (Bucharest) copy of the Worker Qualifications digital product.  Electronic Batch Records depends on it (signature authority).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Qualifications::Create Subscription::WEEKLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opentext_ecm__worker_qualifications

### Journal Entry
OpenText ECM subscribes to Worker Qualifications: Electronic Batch Records depends on it (signature authority).

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
- databaseName: subscription_staging
- schemaName: coco_ed_mfg_control__worker_qualifications
- schemaDescription: Edmonton Manufacturing Control System (Coco core) copy of the Worker Qualifications digital product.  Batch Execution Records depends on it (operator qualification); Electronic Batch Records depends on it (signature authority).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Qualifications::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ed_mfg_control__worker_qualifications

### Journal Entry
Edmonton Manufacturing Control System subscribes to Worker Qualifications: Batch Execution Records depends on it (operator qualification); Electronic Batch Records depends on it (signature authority).

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
- databaseName: subscription_staging
- schemaName: coco_eddepot01__worker_qualifications
- schemaDescription: Edmonton Depot Management System (Coco core) copy of the Worker Qualifications digital product.  Dangerous Goods Consignment Records depends on it (certificated signatory).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Qualifications::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_eddepot01__worker_qualifications

### Journal Entry
Edmonton Depot Management System subscribes to Worker Qualifications: Dangerous Goods Consignment Records depends on it (certificated signatory).

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
- databaseName: subscription_staging
- schemaName: coco_kcdepot01__worker_qualifications
- schemaDescription: Kansas City Depot Management System (Coco core) copy of the Worker Qualifications digital product.  Dangerous Goods Consignment Records depends on it (certificated signatory).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Qualifications::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_kcdepot01__worker_qualifications

### Journal Entry
Kansas City Depot Management System subscribes to Worker Qualifications: Dangerous Goods Consignment Records depends on it (certificated signatory).

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
- databaseName: subscription_staging
- schemaName: coco_mfctrl9482__worker_qualifications
- schemaDescription: Austin Manufacturing Control System (Coco core) copy of the Worker Qualifications digital product.  Batch Execution Records depends on it (operator qualification); Electronic Batch Records depends on it (signature authority).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Qualifications::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_mfctrl9482__worker_qualifications

### Journal Entry
Austin Manufacturing Control System subscribes to Worker Qualifications: Batch Execution Records depends on it (operator qualification); Electronic Batch Records depends on it (signature authority).

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
- databaseName: subscription_staging
- schemaName: coco_winch_mfg_control__worker_qualifications
- schemaDescription: Winchester Manufacturing Control System (Coco core) copy of the Worker Qualifications digital product.  Batch Execution Records depends on it (operator qualification); Electronic Batch Records depends on it (signature authority).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Qualifications::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_winch_mfg_control__worker_qualifications

### Journal Entry
Winchester Manufacturing Control System subscribes to Worker Qualifications: Batch Execution Records depends on it (operator qualification); Electronic Batch Records depends on it (signature authority).

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
- databaseName: subscription_staging
- schemaName: coco_winchdepot01__worker_qualifications
- schemaDescription: Winchester Depot Management System (Coco core) copy of the Worker Qualifications digital product.  Dangerous Goods Consignment Records depends on it (certificated signatory).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Worker Qualifications::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_winchdepot01__worker_qualifications

### Journal Entry
Winchester Depot Management System subscribes to Worker Qualifications: Dangerous Goods Consignment Records depends on it (certificated signatory).

___

---

# Procurement

## Supplier Master Data

15 subscriber(s): LabWare Enterprise LIMS (Austin, ongoing update subscription), Manhattan WMS (Austin, ongoing update subscription), SAP Ariba SRM (Austin, hourly refresh subscription), SAP S/4HANA (Austin, hourly refresh subscription), Warehouse Management System (WMS) (Bucharest, ongoing update subscription), LIMS LabWare Enterprise (Bucharest, ongoing update subscription), OpenText ECM (Bucharest, weekly refresh subscription), SAP ERP S/4HANA (Bucharest, hourly refresh subscription), Austin Inventory (Coco core, ongoing update subscription), Edmonton Depot Management System (Coco core, ongoing update subscription), Coco Inventory (Coco core, ongoing update subscription), Kansas City Depot Management System (Coco core, ongoing update subscription), Coco Ledgers (Coco core, hourly refresh subscription), Coco Pharmaceuticals Operational Data Store (Coco core, daily refresh subscription), Winchester Depot Management System (Coco core, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Procurement

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Supplier Master Data

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Supplier Master Data

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::supplier_master_data::supplier
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::supplier_master_data::supplier_payment_details
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::supplier_master_data::supplier_risk_status

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Supplier Master Data

### Subscription Kind
PERIODIC

### Display Name
Hourly refresh subscription

### Identifier
HOURLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination every hour.

### Subscription Notification Interval
60

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Supplier Master Data

### Subscription Kind
PERIODIC

### Display Name
Daily refresh subscription

### Identifier
DAILY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a day.

### Subscription Notification Interval
1440

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-DAILY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each day

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Supplier Master Data

### Subscription Kind
PERIODIC

### Display Name
Weekly refresh subscription

### Identifier
WEEKLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a week.

### Subscription Notification Interval
10080

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WEEKLY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each week

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
- databaseName: subscription_staging
- schemaName: aus_labware_lims__supplier_master_data
- schemaDescription: LabWare Enterprise LIMS (Austin) copy of the Supplier Master Data digital product.  Supplier Material Certificates depends on it (supplier documentation).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Master Data::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_labware_lims__supplier_master_data

### Journal Entry
LabWare Enterprise LIMS subscribes to Supplier Master Data: Supplier Material Certificates depends on it (supplier documentation).

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
- databaseName: subscription_staging
- schemaName: aus_manhattan_wms__supplier_master_data
- schemaDescription: Manhattan WMS (Austin) copy of the Supplier Master Data digital product.  Goods Receipts depends on it (approved supplier).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Master Data::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_manhattan_wms__supplier_master_data

### Journal Entry
Manhattan WMS subscribes to Supplier Master Data: Goods Receipts depends on it (approved supplier).

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
- databaseName: subscription_staging
- schemaName: aus_sap_ariba__supplier_master_data
- schemaDescription: SAP Ariba SRM (Austin) copy of the Supplier Master Data digital product.  Supplier Payments depends on it (supplier and payment details).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Master Data::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_sap_ariba__supplier_master_data

### Journal Entry
SAP Ariba SRM subscribes to Supplier Master Data: Supplier Payments depends on it (supplier and payment details).

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
- databaseName: subscription_staging
- schemaName: aus_sap_s4hana__supplier_master_data
- schemaDescription: SAP S/4HANA (Austin) copy of the Supplier Master Data digital product.  Supplier Payments depends on it (supplier and payment details).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Master Data::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_sap_s4hana__supplier_master_data

### Journal Entry
SAP S/4HANA subscribes to Supplier Master Data: Supplier Payments depends on it (supplier and payment details).

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
- databaseName: subscription_staging
- schemaName: buc_ekg_wms__supplier_master_data
- schemaDescription: Warehouse Management System (WMS) (Bucharest) copy of the Supplier Master Data digital product.  Goods Receipts depends on it (approved supplier).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Master Data::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_ekg_wms__supplier_master_data

### Journal Entry
Warehouse Management System (WMS) subscribes to Supplier Master Data: Goods Receipts depends on it (approved supplier).

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
- databaseName: subscription_staging
- schemaName: buc_labware_lims__supplier_master_data
- schemaDescription: LIMS LabWare Enterprise (Bucharest) copy of the Supplier Master Data digital product.  Supplier Material Certificates depends on it (supplier documentation).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Master Data::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_labware_lims__supplier_master_data

### Journal Entry
LIMS LabWare Enterprise subscribes to Supplier Master Data: Supplier Material Certificates depends on it (supplier documentation).

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
- databaseName: subscription_staging
- schemaName: buc_opentext_ecm__supplier_master_data
- schemaDescription: OpenText ECM (Bucharest) copy of the Supplier Master Data digital product.  Supplier Material Certificates depends on it (supplier documentation).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Master Data::Create Subscription::WEEKLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opentext_ecm__supplier_master_data

### Journal Entry
OpenText ECM subscribes to Supplier Master Data: Supplier Material Certificates depends on it (supplier documentation).

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
- databaseName: subscription_staging
- schemaName: buc_sap_s4hana__supplier_master_data
- schemaDescription: SAP ERP S/4HANA (Bucharest) copy of the Supplier Master Data digital product.  Supplier Payments depends on it (supplier and payment details).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Master Data::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_sap_s4hana__supplier_master_data

### Journal Entry
SAP ERP S/4HANA subscribes to Supplier Master Data: Supplier Payments depends on it (supplier and payment details).

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
- databaseName: subscription_staging
- schemaName: coco_aus_inventory__supplier_master_data
- schemaDescription: Austin Inventory (Coco core) copy of the Supplier Master Data digital product.  Goods Receipts depends on it (approved supplier).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Master Data::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_aus_inventory__supplier_master_data

### Journal Entry
Austin Inventory subscribes to Supplier Master Data: Goods Receipts depends on it (approved supplier).

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
- databaseName: subscription_staging
- schemaName: coco_eddepot01__supplier_master_data
- schemaDescription: Edmonton Depot Management System (Coco core) copy of the Supplier Master Data digital product.  Goods Receipts depends on it (approved supplier).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Master Data::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_eddepot01__supplier_master_data

### Journal Entry
Edmonton Depot Management System subscribes to Supplier Master Data: Goods Receipts depends on it (approved supplier).

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
- databaseName: subscription_staging
- schemaName: coco_inventory__supplier_master_data
- schemaDescription: Coco Inventory (Coco core) copy of the Supplier Master Data digital product.  Goods Receipts depends on it (approved supplier).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Master Data::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_inventory__supplier_master_data

### Journal Entry
Coco Inventory subscribes to Supplier Master Data: Goods Receipts depends on it (approved supplier).

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
- databaseName: subscription_staging
- schemaName: coco_kcdepot01__supplier_master_data
- schemaDescription: Kansas City Depot Management System (Coco core) copy of the Supplier Master Data digital product.  Goods Receipts depends on it (approved supplier).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Master Data::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_kcdepot01__supplier_master_data

### Journal Entry
Kansas City Depot Management System subscribes to Supplier Master Data: Goods Receipts depends on it (approved supplier).

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
- databaseName: subscription_staging
- schemaName: coco_ledgers__supplier_master_data
- schemaDescription: Coco Ledgers (Coco core) copy of the Supplier Master Data digital product.  Supplier Payments depends on it (supplier and payment details).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Master Data::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ledgers__supplier_master_data

### Journal Entry
Coco Ledgers subscribes to Supplier Master Data: Supplier Payments depends on it (supplier and payment details).

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
- databaseName: subscription_staging
- schemaName: coco_ods__supplier_master_data
- schemaDescription: Coco Pharmaceuticals Operational Data Store (Coco core) copy of the Supplier Master Data digital product.  reporting: fills suppliers.

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Master Data::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ods__supplier_master_data

### Journal Entry
Coco Pharmaceuticals Operational Data Store subscribes to Supplier Master Data: reporting: fills suppliers.

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
- databaseName: subscription_staging
- schemaName: coco_winchdepot01__supplier_master_data
- schemaDescription: Winchester Depot Management System (Coco core) copy of the Supplier Master Data digital product.  Goods Receipts depends on it (approved supplier).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Master Data::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_winchdepot01__supplier_master_data

### Journal Entry
Winchester Depot Management System subscribes to Supplier Master Data: Goods Receipts depends on it (approved supplier).

___

## Supplier Material Certificates

7 subscriber(s): Manhattan WMS (Austin, ongoing update subscription), Warehouse Management System (WMS) (Bucharest, ongoing update subscription), Austin Inventory (Coco core, ongoing update subscription), Edmonton Depot Management System (Coco core, ongoing update subscription), Coco Inventory (Coco core, ongoing update subscription), Kansas City Depot Management System (Coco core, ongoing update subscription), Winchester Depot Management System (Coco core, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Procurement

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Supplier Material Certificates

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Supplier Material Certificates

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::supplier_material_certificates::certificate_of_analysis
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::supplier_material_certificates::certificate_test_result

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: aus_manhattan_wms__supplier_material_certificates
- schemaDescription: Manhattan WMS (Austin) copy of the Supplier Material Certificates digital product.  Goods Receipts depends on it (certificate of analysis).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Material Certificates::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_manhattan_wms__supplier_material_certificates

### Journal Entry
Manhattan WMS subscribes to Supplier Material Certificates: Goods Receipts depends on it (certificate of analysis).

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
- databaseName: subscription_staging
- schemaName: buc_ekg_wms__supplier_material_certificates
- schemaDescription: Warehouse Management System (WMS) (Bucharest) copy of the Supplier Material Certificates digital product.  Goods Receipts depends on it (certificate of analysis).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Material Certificates::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_ekg_wms__supplier_material_certificates

### Journal Entry
Warehouse Management System (WMS) subscribes to Supplier Material Certificates: Goods Receipts depends on it (certificate of analysis).

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
- databaseName: subscription_staging
- schemaName: coco_aus_inventory__supplier_material_certificates
- schemaDescription: Austin Inventory (Coco core) copy of the Supplier Material Certificates digital product.  Goods Receipts depends on it (certificate of analysis).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Material Certificates::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_aus_inventory__supplier_material_certificates

### Journal Entry
Austin Inventory subscribes to Supplier Material Certificates: Goods Receipts depends on it (certificate of analysis).

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
- databaseName: subscription_staging
- schemaName: coco_eddepot01__supplier_material_certificates
- schemaDescription: Edmonton Depot Management System (Coco core) copy of the Supplier Material Certificates digital product.  Goods Receipts depends on it (certificate of analysis).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Material Certificates::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_eddepot01__supplier_material_certificates

### Journal Entry
Edmonton Depot Management System subscribes to Supplier Material Certificates: Goods Receipts depends on it (certificate of analysis).

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
- databaseName: subscription_staging
- schemaName: coco_inventory__supplier_material_certificates
- schemaDescription: Coco Inventory (Coco core) copy of the Supplier Material Certificates digital product.  Goods Receipts depends on it (certificate of analysis).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Material Certificates::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_inventory__supplier_material_certificates

### Journal Entry
Coco Inventory subscribes to Supplier Material Certificates: Goods Receipts depends on it (certificate of analysis).

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
- databaseName: subscription_staging
- schemaName: coco_kcdepot01__supplier_material_certificates
- schemaDescription: Kansas City Depot Management System (Coco core) copy of the Supplier Material Certificates digital product.  Goods Receipts depends on it (certificate of analysis).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Material Certificates::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_kcdepot01__supplier_material_certificates

### Journal Entry
Kansas City Depot Management System subscribes to Supplier Material Certificates: Goods Receipts depends on it (certificate of analysis).

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
- databaseName: subscription_staging
- schemaName: coco_winchdepot01__supplier_material_certificates
- schemaDescription: Winchester Depot Management System (Coco core) copy of the Supplier Material Certificates digital product.  Goods Receipts depends on it (certificate of analysis).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Supplier Material Certificates::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_winchdepot01__supplier_material_certificates

### Journal Entry
Winchester Depot Management System subscribes to Supplier Material Certificates: Goods Receipts depends on it (certificate of analysis).

___

## Third Party Onboarding Cases

3 subscriber(s): Informatica MDM (Austin, ongoing update subscription), SAP ERP S/4HANA (Bucharest, hourly refresh subscription), Coco Pharmaceuticals Procurement (Coco core, hourly refresh subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Procurement

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Third Party Onboarding Cases

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Third Party Onboarding Cases

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::third_party_onboarding_cases::onboarding_case
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::third_party_onboarding_cases::screening_request

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Third Party Onboarding Cases

### Subscription Kind
PERIODIC

### Display Name
Hourly refresh subscription

### Identifier
HOURLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination every hour.

### Subscription Notification Interval
60

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: aus_informatica_mdm__third_party_onboarding_cases
- schemaDescription: Informatica MDM (Austin) copy of the Third Party Onboarding Cases digital product.  Supplier Master Data depends on it (create supplier record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Third Party Onboarding Cases::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_informatica_mdm__third_party_onboarding_cases

### Journal Entry
Informatica MDM subscribes to Third Party Onboarding Cases: Supplier Master Data depends on it (create supplier record).

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
- databaseName: subscription_staging
- schemaName: buc_sap_s4hana__third_party_onboarding_cases
- schemaDescription: SAP ERP S/4HANA (Bucharest) copy of the Third Party Onboarding Cases digital product.  Supplier Master Data depends on it (create supplier record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Third Party Onboarding Cases::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_sap_s4hana__third_party_onboarding_cases

### Journal Entry
SAP ERP S/4HANA subscribes to Third Party Onboarding Cases: Supplier Master Data depends on it (create supplier record).

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
- databaseName: subscription_staging
- schemaName: coco_procurement01__third_party_onboarding_cases
- schemaDescription: Coco Pharmaceuticals Procurement (Coco core) copy of the Third Party Onboarding Cases digital product.  Supplier Master Data depends on it (create supplier record).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Third Party Onboarding Cases::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_procurement01__third_party_onboarding_cases

### Journal Entry
Coco Pharmaceuticals Procurement subscribes to Third Party Onboarding Cases: Supplier Master Data depends on it (create supplier record).

___

---

# Quality Systems

## Batch Certification Decisions

2 subscriber(s): Esri ArcGIS Enterprise (Austin, ongoing update subscription), Oracle TMS (Austin, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Quality Systems

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Batch Certification Decisions

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Batch Certification Decisions

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::batch_certification_decisions::certification_decision

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: aus_arcgis__batch_certification_decisions
- schemaDescription: Esri ArcGIS Enterprise (Austin) copy of the Batch Certification Decisions digital product.  Therapy Delivery Events depends on it (therapy released).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Batch Certification Decisions::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_arcgis__batch_certification_decisions

### Journal Entry
Esri ArcGIS Enterprise subscribes to Batch Certification Decisions: Therapy Delivery Events depends on it (therapy released).

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
- databaseName: subscription_staging
- schemaName: aus_oracle_tms__batch_certification_decisions
- schemaDescription: Oracle TMS (Austin) copy of the Batch Certification Decisions digital product.  Therapy Delivery Events depends on it (therapy released).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Batch Certification Decisions::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_oracle_tms__batch_certification_decisions

### Journal Entry
Oracle TMS subscribes to Batch Certification Decisions: Therapy Delivery Events depends on it (therapy released).

___

## Deviations And CAPAs

6 subscriber(s): Veeva Vault EBR (Austin, ongoing update subscription), Siemens Opcenter MES (Bucharest, ongoing update subscription), OpenText ECM (Bucharest, weekly refresh subscription), Edmonton Manufacturing Control System (Coco core, ongoing update subscription), Austin Manufacturing Control System (Coco core, ongoing update subscription), Winchester Manufacturing Control System (Coco core, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Quality Systems

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Deviations And CAPAs

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Deviations And CAPAs

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::deviations_and_capas::corrective_action
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::deviations_and_capas::deviation
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::deviations_and_capas::investigation

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Deviations And CAPAs

### Subscription Kind
PERIODIC

### Display Name
Weekly refresh subscription

### Identifier
WEEKLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a week.

### Subscription Notification Interval
10080

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WEEKLY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each week

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
- databaseName: subscription_staging
- schemaName: aus_veeva_ebr__deviations_and_capas
- schemaDescription: Veeva Vault EBR (Austin) copy of the Deviations And CAPAs digital product.  Electronic Batch Records depends on it (deviation disposition).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Deviations And CAPAs::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_veeva_ebr__deviations_and_capas

### Journal Entry
Veeva Vault EBR subscribes to Deviations And CAPAs: Electronic Batch Records depends on it (deviation disposition).

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
- databaseName: subscription_staging
- schemaName: buc_opcenter_mes__deviations_and_capas
- schemaDescription: Siemens Opcenter MES (Bucharest) copy of the Deviations And CAPAs digital product.  Electronic Batch Records depends on it (deviation disposition).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Deviations And CAPAs::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opcenter_mes__deviations_and_capas

### Journal Entry
Siemens Opcenter MES subscribes to Deviations And CAPAs: Electronic Batch Records depends on it (deviation disposition).

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
- databaseName: subscription_staging
- schemaName: buc_opentext_ecm__deviations_and_capas
- schemaDescription: OpenText ECM (Bucharest) copy of the Deviations And CAPAs digital product.  Electronic Batch Records depends on it (deviation disposition).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Deviations And CAPAs::Create Subscription::WEEKLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opentext_ecm__deviations_and_capas

### Journal Entry
OpenText ECM subscribes to Deviations And CAPAs: Electronic Batch Records depends on it (deviation disposition).

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
- databaseName: subscription_staging
- schemaName: coco_ed_mfg_control__deviations_and_capas
- schemaDescription: Edmonton Manufacturing Control System (Coco core) copy of the Deviations And CAPAs digital product.  Electronic Batch Records depends on it (deviation disposition).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Deviations And CAPAs::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ed_mfg_control__deviations_and_capas

### Journal Entry
Edmonton Manufacturing Control System subscribes to Deviations And CAPAs: Electronic Batch Records depends on it (deviation disposition).

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
- databaseName: subscription_staging
- schemaName: coco_mfctrl9482__deviations_and_capas
- schemaDescription: Austin Manufacturing Control System (Coco core) copy of the Deviations And CAPAs digital product.  Electronic Batch Records depends on it (deviation disposition).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Deviations And CAPAs::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_mfctrl9482__deviations_and_capas

### Journal Entry
Austin Manufacturing Control System subscribes to Deviations And CAPAs: Electronic Batch Records depends on it (deviation disposition).

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
- databaseName: subscription_staging
- schemaName: coco_winch_mfg_control__deviations_and_capas
- schemaDescription: Winchester Manufacturing Control System (Coco core) copy of the Deviations And CAPAs digital product.  Electronic Batch Records depends on it (deviation disposition).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Deviations And CAPAs::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_winch_mfg_control__deviations_and_capas

### Journal Entry
Winchester Manufacturing Control System subscribes to Deviations And CAPAs: Electronic Batch Records depends on it (deviation disposition).

___

## Laboratory Test Results

13 subscriber(s): Manhattan WMS (Austin, ongoing update subscription), Siemens Opcenter MES (Austin, ongoing update subscription), SAP S/4HANA (Austin, hourly refresh subscription), Veeva Vault EBR (Austin, ongoing update subscription), Warehouse Management System (WMS) (Bucharest, ongoing update subscription), Siemens Opcenter MES (Bucharest, ongoing update subscription), OpenText ECM (Bucharest, weekly refresh subscription), SAP ERP S/4HANA (Bucharest, hourly refresh subscription), Austin Inventory (Coco core, ongoing update subscription), Edmonton Manufacturing Control System (Coco core, ongoing update subscription), Coco Inventory (Coco core, ongoing update subscription), Austin Manufacturing Control System (Coco core, ongoing update subscription), Winchester Manufacturing Control System (Coco core, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Quality Systems

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Laboratory Test Results

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Laboratory Test Results

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::laboratory_test_results::certificate_of_analysis
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::laboratory_test_results::sample
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::laboratory_test_results::test_result

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Laboratory Test Results

### Subscription Kind
PERIODIC

### Display Name
Hourly refresh subscription

### Identifier
HOURLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination every hour.

### Subscription Notification Interval
60

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Laboratory Test Results

### Subscription Kind
PERIODIC

### Display Name
Weekly refresh subscription

### Identifier
WEEKLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a week.

### Subscription Notification Interval
10080

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WEEKLY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each week

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
- databaseName: subscription_staging
- schemaName: aus_manhattan_wms__laboratory_test_results
- schemaDescription: Manhattan WMS (Austin) copy of the Laboratory Test Results digital product.  Material Quarantine Dispositions depends on it (test results).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Laboratory Test Results::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_manhattan_wms__laboratory_test_results

### Journal Entry
Manhattan WMS subscribes to Laboratory Test Results: Material Quarantine Dispositions depends on it (test results).

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
- databaseName: subscription_staging
- schemaName: aus_opcenter_mes__laboratory_test_results
- schemaDescription: Siemens Opcenter MES (Austin) copy of the Laboratory Test Results digital product.  Batch Execution Records depends on it (in-process results).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Laboratory Test Results::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_opcenter_mes__laboratory_test_results

### Journal Entry
Siemens Opcenter MES subscribes to Laboratory Test Results: Batch Execution Records depends on it (in-process results).

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
- databaseName: subscription_staging
- schemaName: aus_sap_s4hana__laboratory_test_results
- schemaDescription: SAP S/4HANA (Austin) copy of the Laboratory Test Results digital product.  Material Quarantine Dispositions depends on it (test results).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Laboratory Test Results::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_sap_s4hana__laboratory_test_results

### Journal Entry
SAP S/4HANA subscribes to Laboratory Test Results: Material Quarantine Dispositions depends on it (test results).

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
- databaseName: subscription_staging
- schemaName: aus_veeva_ebr__laboratory_test_results
- schemaDescription: Veeva Vault EBR (Austin) copy of the Laboratory Test Results digital product.  Electronic Batch Records depends on it (finished product results).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Laboratory Test Results::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_veeva_ebr__laboratory_test_results

### Journal Entry
Veeva Vault EBR subscribes to Laboratory Test Results: Electronic Batch Records depends on it (finished product results).

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
- databaseName: subscription_staging
- schemaName: buc_ekg_wms__laboratory_test_results
- schemaDescription: Warehouse Management System (WMS) (Bucharest) copy of the Laboratory Test Results digital product.  Material Quarantine Dispositions depends on it (test results).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Laboratory Test Results::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_ekg_wms__laboratory_test_results

### Journal Entry
Warehouse Management System (WMS) subscribes to Laboratory Test Results: Material Quarantine Dispositions depends on it (test results).

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
- databaseName: subscription_staging
- schemaName: buc_opcenter_mes__laboratory_test_results
- schemaDescription: Siemens Opcenter MES (Bucharest) copy of the Laboratory Test Results digital product.  Batch Execution Records depends on it (in-process results); Electronic Batch Records depends on it (finished product results).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Laboratory Test Results::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opcenter_mes__laboratory_test_results

### Journal Entry
Siemens Opcenter MES subscribes to Laboratory Test Results: Batch Execution Records depends on it (in-process results); Electronic Batch Records depends on it (finished product results).

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
- databaseName: subscription_staging
- schemaName: buc_opentext_ecm__laboratory_test_results
- schemaDescription: OpenText ECM (Bucharest) copy of the Laboratory Test Results digital product.  Electronic Batch Records depends on it (finished product results).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Laboratory Test Results::Create Subscription::WEEKLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opentext_ecm__laboratory_test_results

### Journal Entry
OpenText ECM subscribes to Laboratory Test Results: Electronic Batch Records depends on it (finished product results).

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
- databaseName: subscription_staging
- schemaName: buc_sap_s4hana__laboratory_test_results
- schemaDescription: SAP ERP S/4HANA (Bucharest) copy of the Laboratory Test Results digital product.  Material Quarantine Dispositions depends on it (test results).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Laboratory Test Results::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_sap_s4hana__laboratory_test_results

### Journal Entry
SAP ERP S/4HANA subscribes to Laboratory Test Results: Material Quarantine Dispositions depends on it (test results).

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
- databaseName: subscription_staging
- schemaName: coco_aus_inventory__laboratory_test_results
- schemaDescription: Austin Inventory (Coco core) copy of the Laboratory Test Results digital product.  Material Quarantine Dispositions depends on it (test results).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Laboratory Test Results::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_aus_inventory__laboratory_test_results

### Journal Entry
Austin Inventory subscribes to Laboratory Test Results: Material Quarantine Dispositions depends on it (test results).

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
- databaseName: subscription_staging
- schemaName: coco_ed_mfg_control__laboratory_test_results
- schemaDescription: Edmonton Manufacturing Control System (Coco core) copy of the Laboratory Test Results digital product.  Batch Execution Records depends on it (in-process results); Electronic Batch Records depends on it (finished product results).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Laboratory Test Results::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ed_mfg_control__laboratory_test_results

### Journal Entry
Edmonton Manufacturing Control System subscribes to Laboratory Test Results: Batch Execution Records depends on it (in-process results); Electronic Batch Records depends on it (finished product results).

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
- databaseName: subscription_staging
- schemaName: coco_inventory__laboratory_test_results
- schemaDescription: Coco Inventory (Coco core) copy of the Laboratory Test Results digital product.  Material Quarantine Dispositions depends on it (test results).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Laboratory Test Results::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_inventory__laboratory_test_results

### Journal Entry
Coco Inventory subscribes to Laboratory Test Results: Material Quarantine Dispositions depends on it (test results).

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
- databaseName: subscription_staging
- schemaName: coco_mfctrl9482__laboratory_test_results
- schemaDescription: Austin Manufacturing Control System (Coco core) copy of the Laboratory Test Results digital product.  Batch Execution Records depends on it (in-process results); Electronic Batch Records depends on it (finished product results).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Laboratory Test Results::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_mfctrl9482__laboratory_test_results

### Journal Entry
Austin Manufacturing Control System subscribes to Laboratory Test Results: Batch Execution Records depends on it (in-process results); Electronic Batch Records depends on it (finished product results).

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
- databaseName: subscription_staging
- schemaName: coco_winch_mfg_control__laboratory_test_results
- schemaDescription: Winchester Manufacturing Control System (Coco core) copy of the Laboratory Test Results digital product.  Batch Execution Records depends on it (in-process results); Electronic Batch Records depends on it (finished product results).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Laboratory Test Results::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_winch_mfg_control__laboratory_test_results

### Journal Entry
Winchester Manufacturing Control System subscribes to Laboratory Test Results: Batch Execution Records depends on it (in-process results); Electronic Batch Records depends on it (finished product results).

___

## Market Authorisations

2 subscriber(s): Informatica MDM (Austin, ongoing update subscription), Coco Product Management (Coco core, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Quality Systems

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Market Authorisations

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Market Authorisations

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::market_authorisations::authorisation_condition
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::market_authorisations::market_authorisation

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: aus_informatica_mdm__market_authorisations
- schemaDescription: Informatica MDM (Austin) copy of the Market Authorisations digital product.  Product Master Data depends on it (authorised markets).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Market Authorisations::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_informatica_mdm__market_authorisations

### Journal Entry
Informatica MDM subscribes to Market Authorisations: Product Master Data depends on it (authorised markets).

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
- databaseName: subscription_staging
- schemaName: coco_products__market_authorisations
- schemaDescription: Coco Product Management (Coco core) copy of the Market Authorisations digital product.  Product Master Data depends on it (authorised markets).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Market Authorisations::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_products__market_authorisations

### Journal Entry
Coco Product Management subscribes to Market Authorisations: Product Master Data depends on it (authorised markets).

___

## Occupational Exposure Bands

2 subscriber(s): Austin HazMat Inventory (Coco core, ongoing update subscription), Coco HazMat Inventory (Coco core, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Quality Systems

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Occupational Exposure Bands

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Occupational Exposure Bands

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::occupational_exposure_bands::band_containment_requirement
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::occupational_exposure_bands::substance_exposure_band

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: coco_austin_haz_mat__occupational_exposure_bands
- schemaDescription: Austin HazMat Inventory (Coco core) copy of the Occupational Exposure Bands digital product.  Transport Classifications depends on it (shared substance classification).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Occupational Exposure Bands::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_austin_haz_mat__occupational_exposure_bands

### Journal Entry
Austin HazMat Inventory subscribes to Occupational Exposure Bands: Transport Classifications depends on it (shared substance classification).

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
- databaseName: subscription_staging
- schemaName: coco_haz_mat__occupational_exposure_bands
- schemaDescription: Coco HazMat Inventory (Coco core) copy of the Occupational Exposure Bands digital product.  Transport Classifications depends on it (shared substance classification).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Occupational Exposure Bands::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_haz_mat__occupational_exposure_bands

### Journal Entry
Coco HazMat Inventory subscribes to Occupational Exposure Bands: Transport Classifications depends on it (shared substance classification).

___

## Product Complaints

2 subscriber(s): ServiceNow Customer Service Management (Austin, ongoing update subscription), Veeva Vault QMS (Austin, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Quality Systems

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Product Complaints

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Product Complaints

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::product_complaints::complaint
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::product_complaints::complaint_safety_assessment

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: aus_servicenow_csm__product_complaints
- schemaDescription: ServiceNow Customer Service Management (Austin) copy of the Product Complaints digital product.  Consolidated Safety Reports depends on it (complaint with safety content).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Product Complaints::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_servicenow_csm__product_complaints

### Journal Entry
ServiceNow Customer Service Management subscribes to Product Complaints: Consolidated Safety Reports depends on it (complaint with safety content).

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
- databaseName: subscription_staging
- schemaName: aus_veeva_qms__product_complaints
- schemaDescription: Veeva Vault QMS (Austin) copy of the Product Complaints digital product.  Consolidated Safety Reports depends on it (complaint with safety content).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Product Complaints::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_veeva_qms__product_complaints

### Journal Entry
Veeva Vault QMS subscribes to Product Complaints: Consolidated Safety Reports depends on it (complaint with safety content).

___

---

# Warehouse

## Goods Inventory Stock

8 subscriber(s): Siemens Opcenter MES (Austin, ongoing update subscription), Siemens Opcenter MES (Bucharest, ongoing update subscription), Austin HazMat Inventory (Coco core, ongoing update subscription), Edmonton Manufacturing Control System (Coco core, ongoing update subscription), Coco HazMat Inventory (Coco core, ongoing update subscription), Austin Manufacturing Control System (Coco core, ongoing update subscription), Coco Pharmaceuticals Operational Data Store (Coco core, daily refresh subscription), Winchester Manufacturing Control System (Coco core, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Warehouse

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Goods Inventory Stock

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Goods Inventory Stock

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::goods_inventory_stock::material_issue
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::goods_inventory_stock::stock_movement
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::goods_inventory_stock::stock_position

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Goods Inventory Stock

### Subscription Kind
PERIODIC

### Display Name
Daily refresh subscription

### Identifier
DAILY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a day.

### Subscription Notification Interval
1440

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-DAILY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each day

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
- databaseName: subscription_staging
- schemaName: aus_opcenter_mes__goods_inventory_stock
- schemaDescription: Siemens Opcenter MES (Austin) copy of the Goods Inventory Stock digital product.  Batch Execution Records depends on it (issue material).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Goods Inventory Stock::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_opcenter_mes__goods_inventory_stock

### Journal Entry
Siemens Opcenter MES subscribes to Goods Inventory Stock: Batch Execution Records depends on it (issue material).

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
- databaseName: subscription_staging
- schemaName: buc_opcenter_mes__goods_inventory_stock
- schemaDescription: Siemens Opcenter MES (Bucharest) copy of the Goods Inventory Stock digital product.  Batch Execution Records depends on it (issue material).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Goods Inventory Stock::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_opcenter_mes__goods_inventory_stock

### Journal Entry
Siemens Opcenter MES subscribes to Goods Inventory Stock: Batch Execution Records depends on it (issue material).

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
- databaseName: subscription_staging
- schemaName: coco_austin_haz_mat__goods_inventory_stock
- schemaDescription: Austin HazMat Inventory (Coco core) copy of the Goods Inventory Stock digital product.  Hazardous Material Holdings depends on it (hazardous holdings).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Goods Inventory Stock::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_austin_haz_mat__goods_inventory_stock

### Journal Entry
Austin HazMat Inventory subscribes to Goods Inventory Stock: Hazardous Material Holdings depends on it (hazardous holdings).

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
- databaseName: subscription_staging
- schemaName: coco_ed_mfg_control__goods_inventory_stock
- schemaDescription: Edmonton Manufacturing Control System (Coco core) copy of the Goods Inventory Stock digital product.  Batch Execution Records depends on it (issue material).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Goods Inventory Stock::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ed_mfg_control__goods_inventory_stock

### Journal Entry
Edmonton Manufacturing Control System subscribes to Goods Inventory Stock: Batch Execution Records depends on it (issue material).

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
- databaseName: subscription_staging
- schemaName: coco_haz_mat__goods_inventory_stock
- schemaDescription: Coco HazMat Inventory (Coco core) copy of the Goods Inventory Stock digital product.  Hazardous Material Holdings depends on it (hazardous holdings).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Goods Inventory Stock::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_haz_mat__goods_inventory_stock

### Journal Entry
Coco HazMat Inventory subscribes to Goods Inventory Stock: Hazardous Material Holdings depends on it (hazardous holdings).

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
- databaseName: subscription_staging
- schemaName: coco_mfctrl9482__goods_inventory_stock
- schemaDescription: Austin Manufacturing Control System (Coco core) copy of the Goods Inventory Stock digital product.  Batch Execution Records depends on it (issue material).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Goods Inventory Stock::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_mfctrl9482__goods_inventory_stock

### Journal Entry
Austin Manufacturing Control System subscribes to Goods Inventory Stock: Batch Execution Records depends on it (issue material).

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
- databaseName: subscription_staging
- schemaName: coco_ods__goods_inventory_stock
- schemaDescription: Coco Pharmaceuticals Operational Data Store (Coco core) copy of the Goods Inventory Stock digital product.  reporting: fills products (stock levels), supplies (stock levels).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Goods Inventory Stock::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ods__goods_inventory_stock

### Journal Entry
Coco Pharmaceuticals Operational Data Store subscribes to Goods Inventory Stock: reporting: fills products (stock levels), supplies (stock levels).

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
- databaseName: subscription_staging
- schemaName: coco_winch_mfg_control__goods_inventory_stock
- schemaDescription: Winchester Manufacturing Control System (Coco core) copy of the Goods Inventory Stock digital product.  Batch Execution Records depends on it (issue material).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Goods Inventory Stock::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_winch_mfg_control__goods_inventory_stock

### Journal Entry
Winchester Manufacturing Control System subscribes to Goods Inventory Stock: Batch Execution Records depends on it (issue material).

___

## Goods Receipts

7 subscriber(s): Manhattan WMS (Austin, ongoing update subscription), SAP S/4HANA (Austin, hourly refresh subscription), Warehouse Management System (WMS) (Bucharest, ongoing update subscription), SAP ERP S/4HANA (Bucharest, hourly refresh subscription), Austin Inventory (Coco core, ongoing update subscription), Coco Inventory (Coco core, ongoing update subscription), Coco Pharmaceuticals Operational Data Store (Coco core, daily refresh subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Warehouse

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Goods Receipts

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Goods Receipts

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::goods_receipts::goods_receipt
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::goods_receipts::receipt_inspection

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Goods Receipts

### Subscription Kind
PERIODIC

### Display Name
Hourly refresh subscription

### Identifier
HOURLY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination every hour.

### Subscription Notification Interval
60

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Goods Receipts

### Subscription Kind
PERIODIC

### Display Name
Daily refresh subscription

### Identifier
DAILY-REFRESH-SUBSCRIPTION

### Description
Delivers the product's data to the subscriber's destination once a day.

### Subscription Notification Interval
1440

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-DAILY-REFRESH::A complete refresh of the product data is delivered to the product data's destination each day

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
- databaseName: subscription_staging
- schemaName: aus_manhattan_wms__goods_receipts
- schemaDescription: Manhattan WMS (Austin) copy of the Goods Receipts digital product.  Material Quarantine Dispositions depends on it (place in quarantine).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Goods Receipts::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_manhattan_wms__goods_receipts

### Journal Entry
Manhattan WMS subscribes to Goods Receipts: Material Quarantine Dispositions depends on it (place in quarantine).

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
- databaseName: subscription_staging
- schemaName: aus_sap_s4hana__goods_receipts
- schemaDescription: SAP S/4HANA (Austin) copy of the Goods Receipts digital product.  Material Quarantine Dispositions depends on it (place in quarantine).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Goods Receipts::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_sap_s4hana__goods_receipts

### Journal Entry
SAP S/4HANA subscribes to Goods Receipts: Material Quarantine Dispositions depends on it (place in quarantine).

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
- databaseName: subscription_staging
- schemaName: buc_ekg_wms__goods_receipts
- schemaDescription: Warehouse Management System (WMS) (Bucharest) copy of the Goods Receipts digital product.  Material Quarantine Dispositions depends on it (place in quarantine).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Goods Receipts::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_ekg_wms__goods_receipts

### Journal Entry
Warehouse Management System (WMS) subscribes to Goods Receipts: Material Quarantine Dispositions depends on it (place in quarantine).

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
- databaseName: subscription_staging
- schemaName: buc_sap_s4hana__goods_receipts
- schemaDescription: SAP ERP S/4HANA (Bucharest) copy of the Goods Receipts digital product.  Material Quarantine Dispositions depends on it (place in quarantine).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Goods Receipts::Create Subscription::HOURLY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_sap_s4hana__goods_receipts

### Journal Entry
SAP ERP S/4HANA subscribes to Goods Receipts: Material Quarantine Dispositions depends on it (place in quarantine).

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
- databaseName: subscription_staging
- schemaName: coco_aus_inventory__goods_receipts
- schemaDescription: Austin Inventory (Coco core) copy of the Goods Receipts digital product.  Material Quarantine Dispositions depends on it (place in quarantine).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Goods Receipts::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_aus_inventory__goods_receipts

### Journal Entry
Austin Inventory subscribes to Goods Receipts: Material Quarantine Dispositions depends on it (place in quarantine).

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
- databaseName: subscription_staging
- schemaName: coco_inventory__goods_receipts
- schemaDescription: Coco Inventory (Coco core) copy of the Goods Receipts digital product.  Material Quarantine Dispositions depends on it (place in quarantine).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Goods Receipts::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_inventory__goods_receipts

### Journal Entry
Coco Inventory subscribes to Goods Receipts: Material Quarantine Dispositions depends on it (place in quarantine).

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
- databaseName: subscription_staging
- schemaName: coco_ods__goods_receipts
- schemaDescription: Coco Pharmaceuticals Operational Data Store (Coco core) copy of the Goods Receipts digital product.  reporting: fills supplier_invoice_details (delivery dates and quantities received).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Goods Receipts::Create Subscription::DAILY-REFRESH-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_ods__goods_receipts

### Journal Entry
Coco Pharmaceuticals Operational Data Store subscribes to Goods Receipts: reporting: fills supplier_invoice_details (delivery dates and quantities received).

___

## Hazardous Material Holdings

2 subscriber(s): Austin HazMat Inventory (Coco core, ongoing update subscription), Coco HazMat Inventory (Coco core, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Warehouse

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Hazardous Material Holdings

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Hazardous Material Holdings

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::hazardous_material_holdings::substance_hazard_data
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::hazardous_material_holdings::substance_holding

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: coco_austin_haz_mat__hazardous_material_holdings
- schemaDescription: Austin HazMat Inventory (Coco core) copy of the Hazardous Material Holdings digital product.  Occupational Exposure Bands depends on it (substance holdings); Transport Classifications depends on it (substance identity).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Hazardous Material Holdings::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_austin_haz_mat__hazardous_material_holdings

### Journal Entry
Austin HazMat Inventory subscribes to Hazardous Material Holdings: Occupational Exposure Bands depends on it (substance holdings); Transport Classifications depends on it (substance identity).

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
- databaseName: subscription_staging
- schemaName: coco_haz_mat__hazardous_material_holdings
- schemaDescription: Coco HazMat Inventory (Coco core) copy of the Hazardous Material Holdings digital product.  Occupational Exposure Bands depends on it (substance holdings); Transport Classifications depends on it (substance identity).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Hazardous Material Holdings::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_haz_mat__hazardous_material_holdings

### Journal Entry
Coco HazMat Inventory subscribes to Hazardous Material Holdings: Occupational Exposure Bands depends on it (substance holdings); Transport Classifications depends on it (substance identity).

___

## Material Quarantine Dispositions

8 subscriber(s): LabWare Enterprise LIMS (Austin, ongoing update subscription), Manhattan WMS (Austin, ongoing update subscription), Waters Empower 3 (Austin, ongoing update subscription), Warehouse Management System (WMS) (Bucharest, ongoing update subscription), Empower Chromatography (Bucharest, ongoing update subscription), LIMS LabWare Enterprise (Bucharest, ongoing update subscription), Austin Inventory (Coco core, ongoing update subscription), Coco Inventory (Coco core, ongoing update subscription).

___

## Link Assignment Scope

### Assigned Actor
PersonRole::Coco::Digital Product Manager::Warehouse

### Assignment Type
Product Manager

### Scope Element
DigitalProduct::Coco::Material Quarantine Dispositions

___

## Create Subscription Type

### Digital Product
DigitalProduct::Coco::Material Quarantine Dispositions

### Subscription Kind
ONGOING_UPDATE

### Display Name
Ongoing update subscription

### Identifier
ONGOING-UPDATE-SUBSCRIPTION

### Description
Delivers the changes to the product's data to the subscriber's destination as they arrive in the Data Sharing Hub, at most every five minutes.

### Subscription Notification Interval
5

### Monitored Resources
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::material_quarantine_dispositions::quarantine_record
- PostgreSQL Relational Database::Coco PostgreSQL Server 1::coco_data_hub::material_quarantine_dispositions::release_disposition

### Subscription License Type
LicenseType::Jacquard::LICENSE-TYPE-IOU::Data for Internal Use

### Subscription Service Level Objective
ServiceLevelObjective::Jacquard::SLO-WITHIN-HOUR::Updates are delivered within 1 hour of receipt

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
- databaseName: subscription_staging
- schemaName: aus_labware_lims__material_quarantine_dispositions
- schemaDescription: LabWare Enterprise LIMS (Austin) copy of the Material Quarantine Dispositions digital product.  Laboratory Test Results depends on it (request incoming testing).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Material Quarantine Dispositions::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_labware_lims__material_quarantine_dispositions

### Journal Entry
LabWare Enterprise LIMS subscribes to Material Quarantine Dispositions: Laboratory Test Results depends on it (request incoming testing).

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
- databaseName: subscription_staging
- schemaName: aus_manhattan_wms__material_quarantine_dispositions
- schemaDescription: Manhattan WMS (Austin) copy of the Material Quarantine Dispositions digital product.  Goods Inventory Stock depends on it (release for use).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Material Quarantine Dispositions::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_manhattan_wms__material_quarantine_dispositions

### Journal Entry
Manhattan WMS subscribes to Material Quarantine Dispositions: Goods Inventory Stock depends on it (release for use).

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
- databaseName: subscription_staging
- schemaName: aus_waters_empower__material_quarantine_dispositions
- schemaDescription: Waters Empower 3 (Austin) copy of the Material Quarantine Dispositions digital product.  Laboratory Test Results depends on it (request incoming testing).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Material Quarantine Dispositions::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.aus_waters_empower__material_quarantine_dispositions

### Journal Entry
Waters Empower 3 subscribes to Material Quarantine Dispositions: Laboratory Test Results depends on it (request incoming testing).

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
- databaseName: subscription_staging
- schemaName: buc_ekg_wms__material_quarantine_dispositions
- schemaDescription: Warehouse Management System (WMS) (Bucharest) copy of the Material Quarantine Dispositions digital product.  Goods Inventory Stock depends on it (release for use).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Material Quarantine Dispositions::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_ekg_wms__material_quarantine_dispositions

### Journal Entry
Warehouse Management System (WMS) subscribes to Material Quarantine Dispositions: Goods Inventory Stock depends on it (release for use).

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
- databaseName: subscription_staging
- schemaName: buc_empower_cds__material_quarantine_dispositions
- schemaDescription: Empower Chromatography (Bucharest) copy of the Material Quarantine Dispositions digital product.  Laboratory Test Results depends on it (request incoming testing).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Material Quarantine Dispositions::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_empower_cds__material_quarantine_dispositions

### Journal Entry
Empower Chromatography subscribes to Material Quarantine Dispositions: Laboratory Test Results depends on it (request incoming testing).

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
- databaseName: subscription_staging
- schemaName: buc_labware_lims__material_quarantine_dispositions
- schemaDescription: LIMS LabWare Enterprise (Bucharest) copy of the Material Quarantine Dispositions digital product.  Laboratory Test Results depends on it (request incoming testing).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Material Quarantine Dispositions::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.buc_labware_lims__material_quarantine_dispositions

### Journal Entry
LIMS LabWare Enterprise subscribes to Material Quarantine Dispositions: Laboratory Test Results depends on it (request incoming testing).

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
- databaseName: subscription_staging
- schemaName: coco_aus_inventory__material_quarantine_dispositions
- schemaDescription: Austin Inventory (Coco core) copy of the Material Quarantine Dispositions digital product.  Goods Inventory Stock depends on it (release for use).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Material Quarantine Dispositions::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_aus_inventory__material_quarantine_dispositions

### Journal Entry
Austin Inventory subscribes to Material Quarantine Dispositions: Goods Inventory Stock depends on it (release for use).

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
- databaseName: subscription_staging
- schemaName: coco_inventory__material_quarantine_dispositions
- schemaDescription: Coco Inventory (Coco core) copy of the Material Quarantine Dispositions digital product.  Goods Inventory Stock depends on it (release for use).

___

## Initiate Subscription

### Subscription Type
ProvisioningActionProcess::Material Quarantine Dispositions::Create Subscription::ONGOING-UPDATE-SUBSCRIPTION

### Subscription Requester
Person::UK::986419

### Destination Data Set
PostgreSQL Tabular Data Set Collection::Coco PostgreSQL Server 1::subscription_staging.coco_inventory__material_quarantine_dispositions

### Journal Entry
Coco Inventory subscribes to Material Quarantine Dispositions: Goods Inventory Stock depends on it (release for use).

___

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
