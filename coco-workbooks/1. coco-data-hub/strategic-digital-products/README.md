<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# The Strategic Digital Product Catalog

The [strategic supply chain analysis](../strategic-supply-chain-analysis.md) laid out the solution components that
carry Coco Pharmaceuticals' strategic information supply chains and drew the wires between them.  Every wire
carries data that one component produces and another consumes, and the analysis wrote down what that data is.
This directory turns that data into **digital products**: defined, described collections of data that a
consumer can find in a catalog, understand from a data specification, and read from a data set, rather than
integrations that only the two systems involved know about.

The catalog is the **Coco Pharmaceuticals Strategic Digital Product Catalog**.  It is a member of
`Egeria::DigitalProductCatalogsRoot`, the root collection every digital product catalog in Egeria hangs from, and
it is organised into one folder per **business system group** from the analysis - Master Data Management, Patient Treatment,
Finance, Procurement, Research, Warehouse, Manufacturing, Delivery, Quality Systems, People Systems and Privacy
Operations - because the group that owns the producing component owns the product.

## What a product is here

Each product is built from the data entering one solution component, and there is at least one product per
component.  A component gets more than one product where the data entering it is of different kinds or from
different sources: the treatment ordering portal receives orders and, through the same channel, clinicians'
adverse reaction reports, so it has *Treatment Orders* and *Clinician Adverse Reaction Reports*; the market
verification gateway sends identifier uploads out and receives verification traffic back, so it has *Market
Identifier Submissions* and *Market Verification Responses*; the cold chain collector holds the temperature
record and, separately, the carriers' account of the journey.

Every product has:

* a **digital product** in its group's folder, with a description, a purpose and a category (master data,
  transactional record, event stream, time series, evidence record, reference data, regulatory submission or
  insight);
* a **data spec**, attached with a `DataDescription` relationship, containing one or more **data structures**,
  each containing the **data fields** a subscriber receives.  Every field name follows the
  [Data Field Naming](../data-field-naming/README.md) standard - prime word, modifiers, class word - and every one
  of the 1,011 field names decomposes into the glossary's vocabulary.  The glossary was extended with the
  vocabulary these names needed, see below;
* a **PostgreSQL tabular data set collection** the product is read from, created with the Asset Maker
  `Create Element` command from the PostgreSQL schema template.  Each product is a schema named after it in the
  `coco_pharma` database on `Coco PostgreSQL Server 1`, and the data set is a member of the product.

The **Data Sharing Hub** has no product either, and deliberately so: it is the asset-layer component of the data
fabric that carries data between the business functions, defined in
[solution-design.md](../solution-design.md).  It originates no data of its own, so there is nothing for it to
publish that its neighbours do not already publish.

Two components have no product of their own.  The **hospital processes** are outside Coco Pharmaceuticals; the
site safety reports they send arrive in *Consolidated Safety Reports*.  The **national verification systems**,
**carrier systems** and **sanctions screening service** are also outside the company, but the data they send
*in* is valuable and is held by the component that receives it, so it is a product owned by that component's
group: *Market Verification Responses* and *Carrier Transit Events* in Manufacturing and Delivery, and *Third
Party Screening Results* in Procurement.  Data sent *out* to them is not a product.  The eight business system
group components themselves are folders, not products; the Master Data Management, Procurement and Research
groups also have products of their own because the analysis wired them directly.

## Dependencies

A wire from component A to component B means the product built from the data entering B depends on the
product A publishes.  [product-dependencies.md](product-dependencies.md) draws that `DigitalProductDependency`
for every wire in the analysis whose two ends both have a product - 117 of the 123 - with the wire's label, a
description of what is exchanged, and the qualified name of the information supply chain it implements in
`ISC Qualified Name`.  `DigitalProductDependency` is a lineage relationship carrying the same single
`iscQualifiedName` as a `DataFlow`, and it is a multi-link, so a wire that implements several chains becomes one
dependency per chain - 122 dependencies from the 117 wires, plus one between the cold chain data collector's two products and one across the carrier systems from the consignment records to the carriers' transit events - and two products that exchange several kinds of
data have one per wire.  Following the dependencies from any product therefore traces the supply chains through
the catalog, and filtering them by chain name gives that chain's product graph.  A wire that crosses from one chain into
another names no chain, so its dependency has no `ISC Qualified Name`; there are ten of these, and the handoffs they
carry are recorded as peer links between the chains in
[strategic-information-supply-chains.md](../../0.%20data-governance-program/strategic-information-supply-chains.md).

| Group | Products | Structures | Fields | Dependencies |
|---|---|---|---|---|
| Master Data Management | 3 | 7 | 41 | 5 |
| Patient Treatment | 3 | 5 | 31 | 3 |
| Finance | 13 | 27 | 173 | 23 |
| Procurement | 5 | 11 | 68 | 6 |
| Research | 2 | 5 | 29 | 1 |
| Warehouse | 4 | 9 | 60 | 8 |
| Manufacturing | 11 | 20 | 129 | 22 |
| Delivery | 7 | 10 | 73 | 12 |
| Quality Systems | 15 | 30 | 208 | 19 |
| People Systems | 11 | 18 | 123 | 16 |
| Privacy Operations | 7 | 11 | 76 | 9 |
| **Total** | **81** | **153** | **1,011** | **124** |

## Files and load order

| File | Content |
|---|---|
| [catalog.md](catalog.md) | The catalog, its membership of the digital product catalogs root, and the eleven group folders |
| [master-data-management.md](master-data-management.md) | Product master data, change notifications, the open metadata catalogue |
| [patient-treatment.md](patient-treatment.md) | Treatment orders, clinician reaction reports, the patient pseudonym register |
| [finance.md](finance.md) | Invoices, subledger postings, ledger balances, journal approvals, consolidation, disclosures, controls evidence, supplier payments and their monitoring, expenses, transfers of value |
| [procurement.md](procurement.md) | Supplier master data, onboarding cases, screening results, supplier certificates, purchase orders and receipts |
| [research.md](research.md) | New product definitions, hospital certifications |
| [warehouse.md](warehouse.md) | Goods receipts, quarantine dispositions, goods inventory, hazardous material holdings |
| [manufacturing.md](manufacturing.md) | Schedules, execution records, process time series, equipment status, the electronic batch record, serialisation, verification traffic |
| [delivery.md](delivery.md) | Sample consignments, delivery events, transport classifications, dangerous goods declarations, temperature readings, cold chain records, carrier events |
| [quality-systems.md](quality-systems.md) | Safety reports, cases, assessments, signals, submissions; laboratory results, deviations, certification, alert investigations, excursion assessments, market authorisations; exposure bands, monitoring, incidents |
| [people-systems.md](people-systems.md) | Worker master data, lifecycle events, access, payroll, directory, competency requirements, training, qualifications and their currency, health surveillance, the long-term archive |
| [privacy-operations.md](privacy-operations.md) | Rights requests, identity verification, the record of processing, discovery findings, fulfilment actions, retention obligations and assignments |
| [product-dependencies.md](product-dependencies.md) | The 124 dependencies, one per wire per supply chain (one per wire where it crosses between chains), grouped by the consuming product's group |

`catalog.md` loads first; the group files follow in any order; `product-dependencies.md` loads last because it
references products from every group.  The `_batch.json` manifest gives this order.  All the files are processed
as Erin Overview:

```
dr_egeria --directive process --userid erinoverview --user_pass secret catalog.md
dr_egeria --directive process --userid erinoverview --user_pass secret master-data-management.md
dr_egeria --directive process --userid erinoverview --user_pass secret patient-treatment.md
dr_egeria --directive process --userid erinoverview --user_pass secret finance.md
dr_egeria --directive process --userid erinoverview --user_pass secret procurement.md
dr_egeria --directive process --userid erinoverview --user_pass secret research.md
dr_egeria --directive process --userid erinoverview --user_pass secret warehouse.md
dr_egeria --directive process --userid erinoverview --user_pass secret manufacturing.md
dr_egeria --directive process --userid erinoverview --user_pass secret delivery.md
dr_egeria --directive process --userid erinoverview --user_pass secret quality-systems.md
dr_egeria --directive process --userid erinoverview --user_pass secret people-systems.md
dr_egeria --directive process --userid erinoverview --user_pass secret privacy-operations.md
dr_egeria --directive process --userid erinoverview --user_pass secret product-dependencies.md
```

## What must already be loaded

* `0. data-governance-program/strategic-information-supply-chains.md` and
  `1. coco-data-hub/strategic-supply-chain-analysis.md` - the products are named for, and describe the data
  of, the components and wires defined there, though nothing here references them by qualified name.
* The [data-field-naming](../data-field-naming/README.md) glossary, the standard the field names were built
  to, including `strategic-products-vocabulary.md`, which adds the 73 prime words, 161 modifiers and 6 class
  words the names needed beyond the original vocabulary - `Batch`-related manufacturing terms such as
  `ExecutionStep` and `ProcessParameter`, safety terms such as `SafetyCase` and `Signal`, finance terms such as
  `Ledger` and `JournalEntry`, and the `Timestamp`, `Duration`, `Temperature`, `Count`, `Version` and
  `Signature` class words.  The data fields do not yet link to the glossary terms by name, but the standard
  precedes the names built to it, and the check that every name decomposes into the vocabulary was made when
  the files were written.
* The PostgreSQL content pack, which supplies template `3f9a0ab3-072c-4cb1-a14f-6e0492e00dd7`, and the
  `Egeria::DigitalProductCatalogsRoot` collection from the core content pack.  Both are present in the
  quickstart platform.

The data sets point at `Coco PostgreSQL Server 1` on `host.docker.internal:5442`, the shared PostgreSQL server
of the quickstart environment, with credentials from the `PostgreSQL Server Secret` collection in
`secrets/integration.omsecrets`.  The `coco_pharma` database and its schemas do not exist yet: the products
are proposals, and the data sets describe where each will be read from once the Data Sharing Hub is built.

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
