# Coco Pharmaceuticals Strategic Digital Product Catalog

> **Author:** Erin Overview (Information Architect), Peter Profile (Solution Architect)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-09-17
> **Description:** Creates the catalog, places it under Egeria's digital product catalogs root, and creates one folder per business system group for the products to live in.

---

## Overview

The [strategic supply chain analysis](../strategic-supply-chain-analysis.md) identified the solution components that carry Coco Pharmaceuticals' strategic information supply chains and the wires between them.  Each wire carries data that one component produces and another consumes.  Where that data is valuable enough that other parts of the business would subscribe to it, it is a **digital product**: a defined, described collection of data with an owner, a data specification and somewhere it can be read from.

This catalog holds those products.  It is organised into one folder per business system group from the analysis, because that is who owns the component the data comes from, and therefore who owns the product.  The products themselves are in the group files in this directory; the dependencies between them, which follow the supply chains, are in `product-dependencies.md`.

This file loads first.  It creates the catalog as a member of `Egeria::DigitalProductCatalogsRoot`, the root collection every digital product catalog in Egeria hangs from, and then the 11 folders.

```
dr_egeria --directive process --userid erinoverview --user_pass secret catalog.md
```

---

# The catalog

## Create Digital Product Catalog

### Display Name
Coco Pharmaceuticals Strategic Digital Product Catalog

### Qualified Name
DigitalProductCatalog::Coco::Strategic Digital Product Catalog

### Description
The digital products that carry data between the solution components of Coco Pharmaceuticals' strategic information supply chains.  Each product is the data one component makes available to the others: defined once, described by a data specification, and readable from a data set in the Data Hub's PostgreSQL server.  The catalog is organised by the business system group that owns the producing component.

### Purpose
Turns the data exchanged along the strategic supply chains into products that can be found, understood and subscribed to, rather than integrations that only the two systems involved know about.

### Category
Strategic Digital Products

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
Egeria::DigitalProductCatalogsRoot

### Element Id
DigitalProductCatalog::Coco::Strategic Digital Product Catalog

### Membership Rationale
Every digital product catalog in Egeria is reachable from the digital product catalogs root, so that a consumer can browse all of them from one place.

### Membership Status
VALIDATED

___

# Folders

One folder per business system group, in the order the analysis introduced them.

# Data Hub

Products of the Data Hub itself and of the master data it distributes: the product master, the change notifications that keep every copy honest, the business summaries the hub assembles, and the open metadata catalogue that describes the estate.

## Create Collection Folder

### Display Name
Data Hub

### Qualified Name
CollectionFolder::Coco::Strategic Digital Products::Data Hub

### Description
Products of the Data Hub itself and of the master data it distributes: the product master, the change notifications that keep every copy honest, the business summaries the hub assembles, and the open metadata catalogue that describes the estate.

### Purpose
Holds the 4 digital products owned by the Data Hub business system group.

### Category
Strategic Digital Products

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
DigitalProductCatalog::Coco::Strategic Digital Product Catalog

### Element Id
CollectionFolder::Coco::Strategic Digital Products::Data Hub

### Membership Rationale
The Data Hub group's products are catalogued together because the same people own them.

### Membership Status
VALIDATED

___

# Patient Treatment

Products originating in the direct-to-patient channel: treatment orders, the pseudonym register that protects patient identity through the rest of the chain, and the adverse reactions clinicians report.

## Create Collection Folder

### Display Name
Patient Treatment

### Qualified Name
CollectionFolder::Coco::Strategic Digital Products::Patient Treatment

### Description
Products originating in the direct-to-patient channel: treatment orders, the pseudonym register that protects patient identity through the rest of the chain, and the adverse reactions clinicians report.

### Purpose
Holds the 3 digital products owned by the Patient Treatment business system group.

### Category
Strategic Digital Products

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
DigitalProductCatalog::Coco::Strategic Digital Product Catalog

### Element Id
CollectionFolder::Coco::Strategic Digital Products::Patient Treatment

### Membership Rationale
The Patient Treatment group's products are catalogued together because the same people own them.

### Membership Status
VALIDATED

___

# Finance

Products of the financial systems: invoices, subledger postings, ledger balances, journal approvals, consolidation, disclosures, controls evidence, supplier payments and their monitoring, expenses, and transfers of value.

## Create Collection Folder

### Display Name
Finance

### Qualified Name
CollectionFolder::Coco::Strategic Digital Products::Finance

### Description
Products of the financial systems: invoices, subledger postings, ledger balances, journal approvals, consolidation, disclosures, controls evidence, supplier payments and their monitoring, expenses, and transfers of value.

### Purpose
Holds the 13 digital products owned by the Finance business system group.

### Category
Strategic Digital Products

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
DigitalProductCatalog::Coco::Strategic Digital Product Catalog

### Element Id
CollectionFolder::Coco::Strategic Digital Products::Finance

### Membership Rationale
The Finance group's products are catalogued together because the same people own them.

### Membership Status
VALIDATED

___

# Procurement

Products of the sourcing function: supplier master data, onboarding cases, third party screening results, supplier certificates, and the purchase orders and receipts that payment is matched against.

## Create Collection Folder

### Display Name
Procurement

### Qualified Name
CollectionFolder::Coco::Strategic Digital Products::Procurement

### Description
Products of the sourcing function: supplier master data, onboarding cases, third party screening results, supplier certificates, and the purchase orders and receipts that payment is matched against.

### Purpose
Holds the 5 digital products owned by the Procurement business system group.

### Category
Strategic Digital Products

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
DigitalProductCatalog::Coco::Strategic Digital Product Catalog

### Element Id
CollectionFolder::Coco::Strategic Digital Products::Procurement

### Membership Rationale
The Procurement group's products are catalogued together because the same people own them.

### Membership Status
VALIDATED

___

# Research

Products of drug development that other chains consume: new product definitions and the certification of hospitals as trial sites.

## Create Collection Folder

### Display Name
Research

### Qualified Name
CollectionFolder::Coco::Strategic Digital Products::Research

### Description
Products of drug development that other chains consume: new product definitions and the certification of hospitals as trial sites.

### Purpose
Holds the 2 digital products owned by the Research business system group.

### Category
Strategic Digital Products

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
DigitalProductCatalog::Coco::Strategic Digital Product Catalog

### Element Id
CollectionFolder::Coco::Strategic Digital Products::Research

### Membership Rationale
The Research group's products are catalogued together because the same people own them.

### Membership Status
VALIDATED

___

# Warehouse

Products of physical stock handling: goods receipts, quarantine dispositions, the goods inventory and the hazardous material holdings.

## Create Collection Folder

### Display Name
Warehouse

### Qualified Name
CollectionFolder::Coco::Strategic Digital Products::Warehouse

### Description
Products of physical stock handling: goods receipts, quarantine dispositions, the goods inventory and the hazardous material holdings.

### Purpose
Holds the 4 digital products owned by the Warehouse business system group.

### Category
Strategic Digital Products

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
DigitalProductCatalog::Coco::Strategic Digital Product Catalog

### Element Id
CollectionFolder::Coco::Strategic Digital Products::Warehouse

### Membership Rationale
The Warehouse group's products are catalogued together because the same people own them.

### Membership Status
VALIDATED

___

# Manufacturing

Products of production and serialisation: schedules, execution records, process time series, equipment status, the electronic batch record, serial number allocations, commissioned packs, aggregation, the serialisation repository and the market verification traffic.

## Create Collection Folder

### Display Name
Manufacturing

### Qualified Name
CollectionFolder::Coco::Strategic Digital Products::Manufacturing

### Description
Products of production and serialisation: schedules, execution records, process time series, equipment status, the electronic batch record, serial number allocations, commissioned packs, aggregation, the serialisation repository and the market verification traffic.

### Purpose
Holds the 11 digital products owned by the Manufacturing business system group.

### Category
Strategic Digital Products

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
DigitalProductCatalog::Coco::Strategic Digital Product Catalog

### Element Id
CollectionFolder::Coco::Strategic Digital Products::Manufacturing

### Membership Rationale
The Manufacturing group's products are catalogued together because the same people own them.

### Membership Status
VALIDATED

___

# Delivery

Products of inbound and outbound logistics: sample consignments, therapy delivery events, transport classifications, dangerous goods declarations, temperature readings, cold chain records and carrier events.

## Create Collection Folder

### Display Name
Delivery

### Qualified Name
CollectionFolder::Coco::Strategic Digital Products::Delivery

### Description
Products of inbound and outbound logistics: sample consignments, therapy delivery events, transport classifications, dangerous goods declarations, temperature readings, cold chain records and carrier events.

### Purpose
Holds the 7 digital products owned by the Delivery business system group.

### Category
Strategic Digital Products

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
DigitalProductCatalog::Coco::Strategic Digital Product Catalog

### Element Id
CollectionFolder::Coco::Strategic Digital Products::Delivery

### Membership Rationale
The Delivery group's products are catalogued together because the same people own them.

### Membership Status
VALIDATED

___

# Quality Systems

Products of quality, regulatory affairs and safety: safety reports and cases, assessments, signals and submissions; laboratory results, deviations and CAPAs, batch certification, serialisation alert investigations, excursion assessments, market authorisations; exposure bands, monitoring results and incidents.

## Create Collection Folder

### Display Name
Quality Systems

### Qualified Name
CollectionFolder::Coco::Strategic Digital Products::Quality Systems

### Description
Products of quality, regulatory affairs and safety: safety reports and cases, assessments, signals and submissions; laboratory results, deviations and CAPAs, batch certification, serialisation alert investigations, excursion assessments, market authorisations; exposure bands, monitoring results and incidents.

### Purpose
Holds the 15 digital products owned by the Quality Systems business system group.

### Category
Strategic Digital Products

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
DigitalProductCatalog::Coco::Strategic Digital Product Catalog

### Element Id
CollectionFolder::Coco::Strategic Digital Products::Quality Systems

### Membership Rationale
The Quality Systems group's products are catalogued together because the same people own them.

### Membership Status
VALIDATED

___

# People Systems

Products of the worker record and everything derived from it: lifecycle events, access entitlements, payroll, the directory, competency requirements, training, qualifications and their currency, and the health surveillance records that outlive employment.

## Create Collection Folder

### Display Name
People Systems

### Qualified Name
CollectionFolder::Coco::Strategic Digital Products::People Systems

### Description
Products of the worker record and everything derived from it: lifecycle events, access entitlements, payroll, the directory, competency requirements, training, qualifications and their currency, and the health surveillance records that outlive employment.

### Purpose
Holds the 11 digital products owned by the People Systems business system group.

### Category
Strategic Digital Products

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
DigitalProductCatalog::Coco::Strategic Digital Product Catalog

### Element Id
CollectionFolder::Coco::Strategic Digital Products::People Systems

### Membership Rationale
The People Systems group's products are catalogued together because the same people own them.

### Membership Status
VALIDATED

___

# Privacy Operations

Products of the privacy function: rights requests, identity verifications, the record of processing, personal data discovery findings, fulfilment actions, retention obligations and the retention periods set on catalogued assets.

## Create Collection Folder

### Display Name
Privacy Operations

### Qualified Name
CollectionFolder::Coco::Strategic Digital Products::Privacy Operations

### Description
Products of the privacy function: rights requests, identity verifications, the record of processing, personal data discovery findings, fulfilment actions, retention obligations and the retention periods set on catalogued assets.

### Purpose
Holds the 7 digital products owned by the Privacy Operations business system group.

### Category
Strategic Digital Products

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Add Member to Collection

### Collection Id
DigitalProductCatalog::Coco::Strategic Digital Product Catalog

### Element Id
CollectionFolder::Coco::Strategic Digital Products::Privacy Operations

### Membership Rationale
The Privacy Operations group's products are catalogued together because the same people own them.

### Membership Status
VALIDATED

___


----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
