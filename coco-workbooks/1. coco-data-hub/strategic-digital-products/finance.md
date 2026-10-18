# Finance Digital Products

> **Author:** Erin Overview (Information Architect), Peter Profile (Solution Architect)
> **Version:** 1.0
> **Status:** ACTIVE
> **Date:** 2026-09-17
> **Description:** The 13 digital products owned by the Finance business system group, each with its data specification and its PostgreSQL data set.

---

## Overview

Products of the financial systems: invoices, subledger postings, ledger balances, journal approvals, consolidation, disclosures, controls evidence, supplier payments and their monitoring, expenses, and transfers of value.

| Product | Solution component | Category | Structures |
|---|---|---|---|
| Treatment Invoices | `CocoPharma::SolutionComponent::OrderToInvoice` | Transactional Record | Invoice, Revenue Recognition |
| Subledger Postings | `CocoPharma::SolutionComponent::SubledgerFeeds` | Transactional Record | Posting Batch, Posting Line |
| Manual Journal Approvals | `CocoPharma::SolutionComponent::JournalEntryReview` | Evidence Record | Journal Entry, Journal Approval |
| Consolidated Group Results | `CocoPharma::SolutionComponent::GroupConsolidation` | Insight | Entity Trial Balance, Consolidation Adjustment, Consolidated Statement Line |
| External Financial Disclosures | `CocoPharma::SolutionComponent::DisclosureReporting` | Regulatory Submission | Disclosure Statement, Disclosure Line Item |
| Financial Controls Evidence | `CocoPharma::SolutionComponent::ControlsEvidenceRepository` | Evidence Record | Control Test Evidence, Close Checklist Item |
| Supplier Payment Detail Changes | `CocoPharma::SolutionComponent::PaymentDetailChangeControl` | Evidence Record | Payment Detail Change, Verification Evidence |
| Supplier Payments | `CocoPharma::SolutionComponent::SupplierPaymentProcessing` | Transactional Record | Invoice Match, Payment Instruction |
| Payment Anomaly Findings | `CocoPharma::SolutionComponent::TransactionMonitoring` | Insight | Anomaly Finding, Monitored Transaction |
| Transfers Of Value | `CocoPharma::SolutionComponent::TransfersOfValueRegister` | Evidence Record | Transfer Of Value |
| Expense Approvals | `CocoPharma::SolutionComponent::ExpenseApprovalWorkflow` | Transactional Record | Expense Claim, Approval Decision |
| General Ledger Balances | `SolutionComponent::Accounting ledgers::V1.0` | Transactional Record | Ledger Transaction, Ledger Account Balance |
| Employee Expense Claims | `SolutionComponent::Employee Expense Tool::V1.0` | Transactional Record | Claim Submission, Claim Line, Claimant Cost Centre |

For every product this file:

1. creates the **digital product** and adds it to the `Finance` folder of the catalog;
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, its position and coverage category set on that relationship - `IDENTIFIER` for the fields that identify a row of the structure, `CORE_DETAIL` for the rest - named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, anchored to the product and a member of it, so that it is removed with the product.  The schema is named after the product, in the `coco_data_hub` database on `Coco PostgreSQL Server 1`.

13 products, 27 data structures, 174 data fields.  This file loads after `catalog.md`.

```
dr_egeria --directive process --userid erinoverview --user_pass secret finance.md
```

---

# Treatment Invoices

*Solution component:* `CocoPharma::SolutionComponent::OrderToInvoice`  
*Category:* Transactional Record

The invoices raised for fulfilled treatment orders and the revenue recognition data that accompanies them.  It is where a clinical event becomes a financial one, and where the fulfilment record and the financial record must agree.

## Create Digital Product

### Display Name
Treatment Invoices

### Product Name
Treatment Invoices

### Qualified Name
DigitalProduct::Coco::Treatment Invoices

### Description
The invoices raised for fulfilled treatment orders and the revenue recognition data that accompanies them.  It is where a clinical event becomes a financial one, and where the fulfilment record and the financial record must agree.

### Purpose
Turns confirmed fulfilment into an invoice and a revenue posting that can be traced back to the delivery evidence.

### Category
Transactional Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

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
CollectionFolder::Coco::Strategic Digital Products::Finance

### Element Id
DigitalProduct::Coco::Treatment Invoices

### Membership Rationale
Produced by the Finance group's `OrderToInvoice` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Treatment Invoices Data Spec

### Qualified Name
DataSpec::Coco::Treatment Invoices

### Description
The data structures and fields that make up the Treatment Invoices digital product.

### Purpose
Describes the data a subscriber to Treatment Invoices receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Treatment Invoices

### Collection Id
DataSpec::Coco::Treatment Invoices

### Label
data specification

___

## Create Data Structure

### Display Name
Invoice

### Qualified Name
DataStructure::Coco::Treatment Invoices::Invoice

### Description
One row per invoice raised.

### Namespace Path
coco_data_hub.treatment_invoices

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Treatment Invoices

### Element Id
DataStructure::Coco::Treatment Invoices::Invoice

### Membership Rationale
The Invoice structure is part of the Treatment Invoices data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Invoice Number

### Qualified Name
DataField::Coco::Treatment Invoices::Invoice::Invoice Number

### Description
The invoice number.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Treatment Invoices::Invoice::Invoice Number

### Data Structure
DataStructure::Coco::Treatment Invoices::Invoice

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Invoice Date

### Qualified Name
DataField::Coco::Treatment Invoices::Invoice::Invoice Date

### Description
When the invoice was raised.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Treatment Invoices::Invoice::Invoice Date

### Data Structure
DataStructure::Coco::Treatment Invoices::Invoice

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Order Identifier

### Qualified Name
DataField::Coco::Treatment Invoices::Invoice::Order Identifier

### Description
The treatment order invoiced.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Treatment Invoices::Invoice::Order Identifier

### Data Structure
DataStructure::Coco::Treatment Invoices::Invoice

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Customer Identifier

### Qualified Name
DataField::Coco::Treatment Invoices::Invoice::Customer Identifier

### Description
The organisation invoiced.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Treatment Invoices::Invoice::Customer Identifier

### Data Structure
DataStructure::Coco::Treatment Invoices::Invoice

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Invoice Total Amount

### Qualified Name
DataField::Coco::Treatment Invoices::Invoice::Invoice Total Amount

### Description
The invoiced value.

### Data Type
bigdecimal

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Treatment Invoices::Invoice::Invoice Total Amount

### Data Structure
DataStructure::Coco::Treatment Invoices::Invoice

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Invoice Currency Code

### Qualified Name
DataField::Coco::Treatment Invoices::Invoice::Invoice Currency Code

### Description
The currency of the invoice.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
3

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Treatment Invoices::Invoice::Invoice Currency Code

### Data Structure
DataStructure::Coco::Treatment Invoices::Invoice

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Invoice Due Date

### Qualified Name
DataField::Coco::Treatment Invoices::Invoice::Invoice Due Date

### Description
When payment is due.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Treatment Invoices::Invoice::Invoice Due Date

### Data Structure
DataStructure::Coco::Treatment Invoices::Invoice

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Invoice Current Status

### Qualified Name
DataField::Coco::Treatment Invoices::Invoice::Invoice Current Status

### Description
Whether the invoice is open, paid or credited.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Treatment Invoices::Invoice::Invoice Current Status

### Data Structure
DataStructure::Coco::Treatment Invoices::Invoice

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Structure

### Display Name
Revenue Recognition

### Qualified Name
DataStructure::Coco::Treatment Invoices::Revenue Recognition

### Description
One row per invoice, the revenue recognised and the evidence it rests on.

### Namespace Path
coco_data_hub.treatment_invoices

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Treatment Invoices

### Element Id
DataStructure::Coco::Treatment Invoices::Revenue Recognition

### Membership Rationale
The Revenue Recognition structure is part of the Treatment Invoices data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Invoice Number

### Qualified Name
DataField::Coco::Treatment Invoices::Revenue Recognition::Invoice Number

### Description
The invoice.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Treatment Invoices::Revenue Recognition::Invoice Number

### Data Structure
DataStructure::Coco::Treatment Invoices::Revenue Recognition

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Revenue Recognition Date

### Qualified Name
DataField::Coco::Treatment Invoices::Revenue Recognition::Revenue Recognition Date

### Description
When the revenue is recognised.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Treatment Invoices::Revenue Recognition::Revenue Recognition Date

### Data Structure
DataStructure::Coco::Treatment Invoices::Revenue Recognition

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Revenue Amount

### Qualified Name
DataField::Coco::Treatment Invoices::Revenue Recognition::Revenue Amount

### Description
The revenue recognised.

### Data Type
bigdecimal

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Treatment Invoices::Revenue Recognition::Revenue Amount

### Data Structure
DataStructure::Coco::Treatment Invoices::Revenue Recognition

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Order Delivery Date

### Qualified Name
DataField::Coco::Treatment Invoices::Revenue Recognition::Order Delivery Date

### Description
The delivery date the recognition relies on.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Treatment Invoices::Revenue Recognition::Order Delivery Date

### Data Structure
DataStructure::Coco::Treatment Invoices::Revenue Recognition

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Ledger Account Code

### Qualified Name
DataField::Coco::Treatment Invoices::Revenue Recognition::Ledger Account Code

### Description
The revenue account posted to.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Treatment Invoices::Revenue Recognition::Ledger Account Code

### Data Structure
DataStructure::Coco::Treatment Invoices::Revenue Recognition

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

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
- databaseName: coco_data_hub
- schemaName: treatment_invoices
- schemaDescription: The invoices raised for fulfilled treatment orders and the revenue recognition data that accompanies them. It is where a clinical event becomes a financial one, and where the fulfilment record and the financial record must agree.

### Anchor ID
DigitalProduct::Coco::Treatment Invoices

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Treatment Invoices

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Subledger Postings

*Solution component:* `CocoPharma::SolutionComponent::SubledgerFeeds`  
*Category:* Transactional Record

The transactions carried from the operational systems into the general ledger, batched per source feed and accounting period.  Each feed is a place where a transaction can be dropped, duplicated or posted to the wrong period, so completeness is asserted per feed rather than in aggregate.

## Create Digital Product

### Display Name
Subledger Postings

### Product Name
Subledger Postings

### Qualified Name
DigitalProduct::Coco::Subledger Postings

### Description
The transactions carried from the operational systems into the general ledger, batched per source feed and accounting period.  Each feed is a place where a transaction can be dropped, duplicated or posted to the wrong period, so completeness is asserted per feed rather than in aggregate.

### Purpose
Gives the close process a complete, per-feed record of what was posted, so that a missing or duplicated posting is visible before the ledger is closed.

### Category
Transactional Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

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
CollectionFolder::Coco::Strategic Digital Products::Finance

### Element Id
DigitalProduct::Coco::Subledger Postings

### Membership Rationale
Produced by the Finance group's `SubledgerFeeds` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Subledger Postings Data Spec

### Qualified Name
DataSpec::Coco::Subledger Postings

### Description
The data structures and fields that make up the Subledger Postings digital product.

### Purpose
Describes the data a subscriber to Subledger Postings receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Subledger Postings

### Collection Id
DataSpec::Coco::Subledger Postings

### Label
data specification

___

## Create Data Structure

### Display Name
Posting Batch

### Qualified Name
DataStructure::Coco::Subledger Postings::Posting Batch

### Description
One row per batch of postings from one source feed for one period.

### Namespace Path
coco_data_hub.subledger_postings

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Subledger Postings

### Element Id
DataStructure::Coco::Subledger Postings::Posting Batch

### Membership Rationale
The Posting Batch structure is part of the Subledger Postings data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Feed Identifier

### Qualified Name
DataField::Coco::Subledger Postings::Posting Batch::Feed Identifier

### Description
The unique identifier of the batch.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Subledger Postings::Posting Batch::Feed Identifier

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Batch

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
System Identifier

### Qualified Name
DataField::Coco::Subledger Postings::Posting Batch::System Identifier

### Description
The source system the feed comes from.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
60

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Subledger Postings::Posting Batch::System Identifier

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Batch

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Accounting Period Code

### Qualified Name
DataField::Coco::Subledger Postings::Posting Batch::Accounting Period Code

### Description
The accounting period the batch belongs to.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Subledger Postings::Posting Batch::Accounting Period Code

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Batch

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Feed Posted Timestamp

### Qualified Name
DataField::Coco::Subledger Postings::Posting Batch::Feed Posted Timestamp

### Description
When the batch was posted to the ledger.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Subledger Postings::Posting Batch::Feed Posted Timestamp

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Batch

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Feed Line Count

### Qualified Name
DataField::Coco::Subledger Postings::Posting Batch::Feed Line Count

### Description
The number of postings in the batch.

### Data Type
int

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Subledger Postings::Posting Batch::Feed Line Count

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Batch

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Feed Total Amount

### Qualified Name
DataField::Coco::Subledger Postings::Posting Batch::Feed Total Amount

### Description
The control total of the batch.

### Data Type
bigdecimal

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Subledger Postings::Posting Batch::Feed Total Amount

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Batch

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Feed Current Status

### Qualified Name
DataField::Coco::Subledger Postings::Posting Batch::Feed Current Status

### Description
Whether the batch is pending, posted or rejected.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Subledger Postings::Posting Batch::Feed Current Status

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Batch

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Structure

### Display Name
Posting Line

### Qualified Name
DataStructure::Coco::Subledger Postings::Posting Line

### Description
One row per posting within a batch.

### Namespace Path
coco_data_hub.subledger_postings

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Subledger Postings

### Element Id
DataStructure::Coco::Subledger Postings::Posting Line

### Membership Rationale
The Posting Line structure is part of the Subledger Postings data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Feed Identifier

### Qualified Name
DataField::Coco::Subledger Postings::Posting Line::Feed Identifier

### Description
The batch the posting belongs to.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Subledger Postings::Posting Line::Feed Identifier

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Line

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Posting Line Number

### Qualified Name
DataField::Coco::Subledger Postings::Posting Line::Posting Line Number

### Description
The position of the posting in the batch.

### Data Type
int

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Subledger Postings::Posting Line::Posting Line Number

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Line

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Ledger Account Code

### Qualified Name
DataField::Coco::Subledger Postings::Posting Line::Ledger Account Code

### Description
The account posted to.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Subledger Postings::Posting Line::Ledger Account Code

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Line

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Legal Entity Code

### Qualified Name
DataField::Coco::Subledger Postings::Posting Line::Legal Entity Code

### Description
The legal entity the posting belongs to.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Subledger Postings::Posting Line::Legal Entity Code

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Line

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Transaction Identifier

### Qualified Name
DataField::Coco::Subledger Postings::Posting Line::Transaction Identifier

### Description
The source transaction the posting represents.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Subledger Postings::Posting Line::Transaction Identifier

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Line

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Posting Amount

### Qualified Name
DataField::Coco::Subledger Postings::Posting Line::Posting Amount

### Description
The amount posted.

### Data Type
bigdecimal

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Subledger Postings::Posting Line::Posting Amount

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Line

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Posting Currency Code

### Qualified Name
DataField::Coco::Subledger Postings::Posting Line::Posting Currency Code

### Description
The currency of the amount.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
3

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Subledger Postings::Posting Line::Posting Currency Code

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Line

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

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
- databaseName: coco_data_hub
- schemaName: subledger_postings
- schemaDescription: The transactions carried from the operational systems into the general ledger, batched per source feed and accounting period. Each feed is a place where a transaction can be dropped, duplicated or posted to the wrong period, so completeness is asserted per feed rather than in aggregate.

### Anchor ID
DigitalProduct::Coco::Subledger Postings

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Subledger Postings

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Manual Journal Approvals

*Solution component:* `CocoPharma::SolutionComponent::JournalEntryReview`  
*Category:* Evidence Record

Manual journal entries above the materiality threshold, together with the review and approval each received before it was posted.  Manual adjustment is the segment of the close least covered by system controls and most able to change a reported figure.

## Create Digital Product

### Display Name
Manual Journal Approvals

### Product Name
Manual Journal Approvals

### Qualified Name
DigitalProduct::Coco::Manual Journal Approvals

### Description
Manual journal entries above the materiality threshold, together with the review and approval each received before it was posted.  Manual adjustment is the segment of the close least covered by system controls and most able to change a reported figure.

### Purpose
Evidences that every material manual adjustment was reviewed by someone other than its author before it reached the ledger.

### Category
Evidence Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

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
CollectionFolder::Coco::Strategic Digital Products::Finance

### Element Id
DigitalProduct::Coco::Manual Journal Approvals

### Membership Rationale
Produced by the Finance group's `JournalEntryReview` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Manual Journal Approvals Data Spec

### Qualified Name
DataSpec::Coco::Manual Journal Approvals

### Description
The data structures and fields that make up the Manual Journal Approvals digital product.

### Purpose
Describes the data a subscriber to Manual Journal Approvals receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Manual Journal Approvals

### Collection Id
DataSpec::Coco::Manual Journal Approvals

### Label
data specification

___

## Create Data Structure

### Display Name
Journal Entry

### Qualified Name
DataStructure::Coco::Manual Journal Approvals::Journal Entry

### Description
One row per manual journal entry submitted for review.

### Namespace Path
coco_data_hub.manual_journal_approvals

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Manual Journal Approvals

### Element Id
DataStructure::Coco::Manual Journal Approvals::Journal Entry

### Membership Rationale
The Journal Entry structure is part of the Manual Journal Approvals data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Journal Entry Identifier

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Entry::Journal Entry Identifier

### Description
The unique identifier of the entry.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Manual Journal Approvals::Journal Entry::Journal Entry Identifier

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Entry

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Accounting Period Code

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Entry::Accounting Period Code

### Description
The period the entry adjusts.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Manual Journal Approvals::Journal Entry::Accounting Period Code

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Entry

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Legal Entity Code

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Entry::Legal Entity Code

### Description
The entity the entry belongs to.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Manual Journal Approvals::Journal Entry::Legal Entity Code

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Entry

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Journal Entry Amount

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Entry::Journal Entry Amount

### Description
The value of the adjustment.

### Data Type
bigdecimal

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Manual Journal Approvals::Journal Entry::Journal Entry Amount

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Entry

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Journal Entry Description

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Entry::Journal Entry Description

### Description
The reason for the adjustment.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Manual Journal Approvals::Journal Entry::Journal Entry Description

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Entry

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Journal Entry Preparer Identifier

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Entry::Journal Entry Preparer Identifier

### Description
The person who prepared the entry.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Manual Journal Approvals::Journal Entry::Journal Entry Preparer Identifier

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Entry

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Journal Entry Submitted Timestamp

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Entry::Journal Entry Submitted Timestamp

### Description
When the entry was submitted for review.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Manual Journal Approvals::Journal Entry::Journal Entry Submitted Timestamp

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Entry

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Structure

### Display Name
Journal Approval

### Qualified Name
DataStructure::Coco::Manual Journal Approvals::Journal Approval

### Description
One row per review decision on a journal entry.

### Namespace Path
coco_data_hub.manual_journal_approvals

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Manual Journal Approvals

### Element Id
DataStructure::Coco::Manual Journal Approvals::Journal Approval

### Membership Rationale
The Journal Approval structure is part of the Manual Journal Approvals data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Journal Entry Identifier

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Approval::Journal Entry Identifier

### Description
The entry reviewed.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Manual Journal Approvals::Journal Approval::Journal Entry Identifier

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Approval

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Journal Entry Approval Timestamp

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Approval::Journal Entry Approval Timestamp

### Description
When the decision was taken.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Manual Journal Approvals::Journal Approval::Journal Entry Approval Timestamp

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Approval

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Journal Entry Approver Identifier

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Approval::Journal Entry Approver Identifier

### Description
The reviewer.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Manual Journal Approvals::Journal Approval::Journal Entry Approver Identifier

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Approval

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Journal Entry Approval Status

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Approval::Journal Entry Approval Status

### Description
Approved, rejected or returned for change.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Manual Journal Approvals::Journal Approval::Journal Entry Approval Status

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Approval

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Journal Entry Approval Notes

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Approval::Journal Entry Approval Notes

### Description
The reviewer's comments.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Manual Journal Approvals::Journal Approval::Journal Entry Approval Notes

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Approval

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

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
- databaseName: coco_data_hub
- schemaName: manual_journal_approvals
- schemaDescription: Manual journal entries above the materiality threshold, together with the review and approval each received before it was posted. Manual adjustment is the segment of the close least covered by system controls and most able to change a reported figure.

### Anchor ID
DigitalProduct::Coco::Manual Journal Approvals

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Manual Journal Approvals

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Consolidated Group Results

*Solution component:* `CocoPharma::SolutionComponent::GroupConsolidation`  
*Category:* Insight

The trial balances of the US parent and the UK and EU subsidiaries, the intercompany eliminations and currency translations applied to them, and the consolidated statement lines that result.  It is where several sets of books become one set of figures.

## Create Digital Product

### Display Name
Consolidated Group Results

### Product Name
Consolidated Group Results

### Qualified Name
DigitalProduct::Coco::Consolidated Group Results

### Description
The trial balances of the US parent and the UK and EU subsidiaries, the intercompany eliminations and currency translations applied to them, and the consolidated statement lines that result.  It is where several sets of books become one set of figures.

### Purpose
Produces the single set of group figures external reporting is built from, with every adjustment between the entity ledgers and the group result recorded.

### Category
Insight

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

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
CollectionFolder::Coco::Strategic Digital Products::Finance

### Element Id
DigitalProduct::Coco::Consolidated Group Results

### Membership Rationale
Produced by the Finance group's `GroupConsolidation` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Consolidated Group Results Data Spec

### Qualified Name
DataSpec::Coco::Consolidated Group Results

### Description
The data structures and fields that make up the Consolidated Group Results digital product.

### Purpose
Describes the data a subscriber to Consolidated Group Results receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Consolidated Group Results

### Collection Id
DataSpec::Coco::Consolidated Group Results

### Label
data specification

___

## Create Data Structure

### Display Name
Entity Trial Balance

### Qualified Name
DataStructure::Coco::Consolidated Group Results::Entity Trial Balance

### Description
One row per account per legal entity per period.

### Namespace Path
coco_data_hub.consolidated_group_results

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Consolidated Group Results

### Element Id
DataStructure::Coco::Consolidated Group Results::Entity Trial Balance

### Membership Rationale
The Entity Trial Balance structure is part of the Consolidated Group Results data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Legal Entity Code

### Qualified Name
DataField::Coco::Consolidated Group Results::Entity Trial Balance::Legal Entity Code

### Description
The legal entity.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Group Results::Entity Trial Balance::Legal Entity Code

### Data Structure
DataStructure::Coco::Consolidated Group Results::Entity Trial Balance

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Accounting Period Code

### Qualified Name
DataField::Coco::Consolidated Group Results::Entity Trial Balance::Accounting Period Code

### Description
The period.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Group Results::Entity Trial Balance::Accounting Period Code

### Data Structure
DataStructure::Coco::Consolidated Group Results::Entity Trial Balance

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Ledger Account Code

### Qualified Name
DataField::Coco::Consolidated Group Results::Entity Trial Balance::Ledger Account Code

### Description
The account.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Group Results::Entity Trial Balance::Ledger Account Code

### Data Structure
DataStructure::Coco::Consolidated Group Results::Entity Trial Balance

### Position
3

### Coverage Category
IDENTIFIER

### Label
field 3

___

## Create Data Field

### Display Name
Ledger Account Balance Amount

### Qualified Name
DataField::Coco::Consolidated Group Results::Entity Trial Balance::Ledger Account Balance Amount

### Description
The closing balance in the entity's currency.

### Data Type
bigdecimal

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Group Results::Entity Trial Balance::Ledger Account Balance Amount

### Data Structure
DataStructure::Coco::Consolidated Group Results::Entity Trial Balance

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Ledger Currency Code

### Qualified Name
DataField::Coco::Consolidated Group Results::Entity Trial Balance::Ledger Currency Code

### Description
The entity's reporting currency.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
3

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Group Results::Entity Trial Balance::Ledger Currency Code

### Data Structure
DataStructure::Coco::Consolidated Group Results::Entity Trial Balance

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Structure

### Display Name
Consolidation Adjustment

### Qualified Name
DataStructure::Coco::Consolidated Group Results::Consolidation Adjustment

### Description
One row per elimination or translation adjustment applied during consolidation.

### Namespace Path
coco_data_hub.consolidated_group_results

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Consolidated Group Results

### Element Id
DataStructure::Coco::Consolidated Group Results::Consolidation Adjustment

### Membership Rationale
The Consolidation Adjustment structure is part of the Consolidated Group Results data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Consolidation Adjustment Identifier

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::Consolidation Adjustment Identifier

### Description
The unique identifier of the adjustment.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::Consolidation Adjustment Identifier

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidation Adjustment

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Accounting Period Code

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::Accounting Period Code

### Description
The period.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::Accounting Period Code

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidation Adjustment

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Consolidation Adjustment Type

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::Consolidation Adjustment Type

### Description
Intercompany elimination, currency translation or other.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::Consolidation Adjustment Type

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidation Adjustment

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Legal Entity Code

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::Legal Entity Code

### Description
The entity the adjustment applies to.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::Legal Entity Code

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidation Adjustment

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Ledger Account Code

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::Ledger Account Code

### Description
The account adjusted.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::Ledger Account Code

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidation Adjustment

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Consolidation Adjustment Amount

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::Consolidation Adjustment Amount

### Description
The adjustment in group currency.

### Data Type
bigdecimal

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::Consolidation Adjustment Amount

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidation Adjustment

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Consolidation Adjustment Description

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::Consolidation Adjustment Description

### Description
The basis of the adjustment.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::Consolidation Adjustment Description

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidation Adjustment

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Structure

### Display Name
Consolidated Statement Line

### Qualified Name
DataStructure::Coco::Consolidated Group Results::Consolidated Statement Line

### Description
One row per line of the consolidated statements per period, with segment analysis.

### Namespace Path
coco_data_hub.consolidated_group_results

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Consolidated Group Results

### Element Id
DataStructure::Coco::Consolidated Group Results::Consolidated Statement Line

### Membership Rationale
The Consolidated Statement Line structure is part of the Consolidated Group Results data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Statement Line Identifier

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidated Statement Line::Statement Line Identifier

### Description
The unique identifier of a line of the consolidated statements for a period and segment.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Group Results::Consolidated Statement Line::Statement Line Identifier

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidated Statement Line

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Accounting Period Code

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidated Statement Line::Accounting Period Code

### Description
The period.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Group Results::Consolidated Statement Line::Accounting Period Code

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidated Statement Line

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Statement Line Code

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidated Statement Line::Statement Line Code

### Description
The statement line.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Group Results::Consolidated Statement Line::Statement Line Code

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidated Statement Line

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Statement Segment Code

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidated Statement Line::Statement Segment Code

### Description
The business segment the line is analysed to.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Group Results::Consolidated Statement Line::Statement Segment Code

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidated Statement Line

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Statement Line Amount

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidated Statement Line::Statement Line Amount

### Description
The consolidated amount in group currency.

### Data Type
bigdecimal

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Consolidated Group Results::Consolidated Statement Line::Statement Line Amount

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidated Statement Line

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

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
- databaseName: coco_data_hub
- schemaName: consolidated_group_results
- schemaDescription: The trial balances of the US parent and the UK and EU subsidiaries, the intercompany eliminations and currency translations applied to them, and the consolidated statement lines that result. It is where several sets of books become one set of figures.

### Anchor ID
DigitalProduct::Coco::Consolidated Group Results

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Consolidated Group Results

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# External Financial Disclosures

*Solution component:* `CocoPharma::SolutionComponent::DisclosureReporting`  
*Category:* Regulatory Submission

The statements filed with regulators and published to the market, and the disclosures of transfers of value to healthcare professionals.  Every figure must be resolvable back through the consolidation and the ledger to the transactions it was built from.

## Create Digital Product

### Display Name
External Financial Disclosures

### Product Name
External Financial Disclosures

### Qualified Name
DigitalProduct::Coco::External Financial Disclosures

### Description
The statements filed with regulators and published to the market, and the disclosures of transfers of value to healthcare professionals.  Every figure must be resolvable back through the consolidation and the ledger to the transactions it was built from.

### Purpose
Holds what was actually filed, when, and with what supporting reconciliation, so that a published figure can be defended on demand.

### Category
Regulatory Submission

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

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
CollectionFolder::Coco::Strategic Digital Products::Finance

### Element Id
DigitalProduct::Coco::External Financial Disclosures

### Membership Rationale
Produced by the Finance group's `DisclosureReporting` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
External Financial Disclosures Data Spec

### Qualified Name
DataSpec::Coco::External Financial Disclosures

### Description
The data structures and fields that make up the External Financial Disclosures digital product.

### Purpose
Describes the data a subscriber to External Financial Disclosures receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::External Financial Disclosures

### Collection Id
DataSpec::Coco::External Financial Disclosures

### Label
data specification

___

## Create Data Structure

### Display Name
Disclosure Statement

### Qualified Name
DataStructure::Coco::External Financial Disclosures::Disclosure Statement

### Description
One row per statement or report filed.

### Namespace Path
coco_data_hub.external_financial_disclosures

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::External Financial Disclosures

### Element Id
DataStructure::Coco::External Financial Disclosures::Disclosure Statement

### Membership Rationale
The Disclosure Statement structure is part of the External Financial Disclosures data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Disclosure Identifier

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Statement::Disclosure Identifier

### Description
The unique identifier of the filing.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::External Financial Disclosures::Disclosure Statement::Disclosure Identifier

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Statement

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Disclosure Type

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Statement::Disclosure Type

### Description
Annual report, quarterly report, transfers of value disclosure or other.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::External Financial Disclosures::Disclosure Statement::Disclosure Type

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Statement

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Accounting Period Code

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Statement::Accounting Period Code

### Description
The period the filing covers.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::External Financial Disclosures::Disclosure Statement::Accounting Period Code

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Statement

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Disclosure Regulator Code

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Statement::Disclosure Regulator Code

### Description
The regulator or body the filing was made to.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::External Financial Disclosures::Disclosure Statement::Disclosure Regulator Code

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Statement

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Disclosure Filed Timestamp

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Statement::Disclosure Filed Timestamp

### Description
When the filing was made.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::External Financial Disclosures::Disclosure Statement::Disclosure Filed Timestamp

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Statement

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Disclosure Acknowledged Flag

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Statement::Disclosure Acknowledged Flag

### Description
Whether the regulator has acknowledged receipt.

### Data Type
boolean

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::External Financial Disclosures::Disclosure Statement::Disclosure Acknowledged Flag

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Statement

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Structure

### Display Name
Disclosure Line Item

### Qualified Name
DataStructure::Coco::External Financial Disclosures::Disclosure Line Item

### Description
One row per figure in a filing, with its source.

### Namespace Path
coco_data_hub.external_financial_disclosures

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::External Financial Disclosures

### Element Id
DataStructure::Coco::External Financial Disclosures::Disclosure Line Item

### Membership Rationale
The Disclosure Line Item structure is part of the External Financial Disclosures data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Disclosure Identifier

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Line Item::Disclosure Identifier

### Description
The filing.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::External Financial Disclosures::Disclosure Line Item::Disclosure Identifier

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Line Item

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Statement Line Code

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Line Item::Statement Line Code

### Description
The statement line the figure reports.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::External Financial Disclosures::Disclosure Line Item::Statement Line Code

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Line Item

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Disclosure Line Amount

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Line Item::Disclosure Line Amount

### Description
The figure disclosed.

### Data Type
bigdecimal

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::External Financial Disclosures::Disclosure Line Item::Disclosure Line Amount

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Line Item

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Consolidation Adjustment Identifier

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Line Item::Consolidation Adjustment Identifier

### Description
The consolidation adjustment the figure depends on, if any.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::External Financial Disclosures::Disclosure Line Item::Consolidation Adjustment Identifier

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Line Item

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

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
- databaseName: coco_data_hub
- schemaName: external_financial_disclosures
- schemaDescription: The statements filed with regulators and published to the market, and the disclosures of transfers of value to healthcare professionals. Every figure must be resolvable back through the consolidation and the ledger to the transactions it was built from.

### Anchor ID
DigitalProduct::Coco::External Financial Disclosures

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::External Financial Disclosures

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Financial Controls Evidence

*Solution component:* `CocoPharma::SolutionComponent::ControlsEvidenceRepository`  
*Category:* Evidence Record

The documentation and test evidence for the internal controls over financial reporting, and the reconciliations, approvals and checklist items produced by each close.  The controls it evidences are controls over the close itself, so the repository is part of the chain rather than an audit of it.

## Create Digital Product

### Display Name
Financial Controls Evidence

### Product Name
Financial Controls Evidence

### Qualified Name
DigitalProduct::Coco::Financial Controls Evidence

### Description
The documentation and test evidence for the internal controls over financial reporting, and the reconciliations, approvals and checklist items produced by each close.  The controls it evidences are controls over the close itself, so the repository is part of the chain rather than an audit of it.

### Purpose
Gives auditors and management the evidence that each control operated in each period, attached to the close it belongs to.

### Category
Evidence Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

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
CollectionFolder::Coco::Strategic Digital Products::Finance

### Element Id
DigitalProduct::Coco::Financial Controls Evidence

### Membership Rationale
Produced by the Finance group's `ControlsEvidenceRepository` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Financial Controls Evidence Data Spec

### Qualified Name
DataSpec::Coco::Financial Controls Evidence

### Description
The data structures and fields that make up the Financial Controls Evidence digital product.

### Purpose
Describes the data a subscriber to Financial Controls Evidence receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Financial Controls Evidence

### Collection Id
DataSpec::Coco::Financial Controls Evidence

### Label
data specification

___

## Create Data Structure

### Display Name
Control Test Evidence

### Qualified Name
DataStructure::Coco::Financial Controls Evidence::Control Test Evidence

### Description
One row per test of a control in a period.

### Namespace Path
coco_data_hub.financial_controls_evidence

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Financial Controls Evidence

### Element Id
DataStructure::Coco::Financial Controls Evidence::Control Test Evidence

### Membership Rationale
The Control Test Evidence structure is part of the Financial Controls Evidence data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Control Identifier

### Qualified Name
DataField::Coco::Financial Controls Evidence::Control Test Evidence::Control Identifier

### Description
The control tested.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Financial Controls Evidence::Control Test Evidence::Control Identifier

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Control Test Evidence

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Accounting Period Code

### Qualified Name
DataField::Coco::Financial Controls Evidence::Control Test Evidence::Accounting Period Code

### Description
The period the test covers.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Financial Controls Evidence::Control Test Evidence::Accounting Period Code

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Control Test Evidence

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Control Tested Date

### Qualified Name
DataField::Coco::Financial Controls Evidence::Control Test Evidence::Control Tested Date

### Description
When the test was performed.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Financial Controls Evidence::Control Test Evidence::Control Tested Date

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Control Test Evidence

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Control Tester Identifier

### Qualified Name
DataField::Coco::Financial Controls Evidence::Control Test Evidence::Control Tester Identifier

### Description
Who performed the test.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Financial Controls Evidence::Control Test Evidence::Control Tester Identifier

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Control Test Evidence

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Control Tested Status

### Qualified Name
DataField::Coco::Financial Controls Evidence::Control Test Evidence::Control Tested Status

### Description
Whether the control operated effectively.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Financial Controls Evidence::Control Test Evidence::Control Tested Status

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Control Test Evidence

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Control Evidence Identifier

### Qualified Name
DataField::Coco::Financial Controls Evidence::Control Test Evidence::Control Evidence Identifier

### Description
The document holding the evidence.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
60

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Financial Controls Evidence::Control Test Evidence::Control Evidence Identifier

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Control Test Evidence

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Structure

### Display Name
Close Checklist Item

### Qualified Name
DataStructure::Coco::Financial Controls Evidence::Close Checklist Item

### Description
One row per step of the period-end close, its completion and approval.

### Namespace Path
coco_data_hub.financial_controls_evidence

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Financial Controls Evidence

### Element Id
DataStructure::Coco::Financial Controls Evidence::Close Checklist Item

### Membership Rationale
The Close Checklist Item structure is part of the Financial Controls Evidence data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Accounting Period Code

### Qualified Name
DataField::Coco::Financial Controls Evidence::Close Checklist Item::Accounting Period Code

### Description
The period closed.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Financial Controls Evidence::Close Checklist Item::Accounting Period Code

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Close Checklist Item

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Close Checklist Item Code

### Qualified Name
DataField::Coco::Financial Controls Evidence::Close Checklist Item::Close Checklist Item Code

### Description
The step.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Financial Controls Evidence::Close Checklist Item::Close Checklist Item Code

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Close Checklist Item

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Close Checklist Item Completed Timestamp

### Qualified Name
DataField::Coco::Financial Controls Evidence::Close Checklist Item::Close Checklist Item Completed Timestamp

### Description
When the step was completed.

### Data Type
date

### Is Nullable
true

### Minimum Cardinality
0

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Financial Controls Evidence::Close Checklist Item::Close Checklist Item Completed Timestamp

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Close Checklist Item

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Close Checklist Item Approver Identifier

### Qualified Name
DataField::Coco::Financial Controls Evidence::Close Checklist Item::Close Checklist Item Approver Identifier

### Description
Who approved completion.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Financial Controls Evidence::Close Checklist Item::Close Checklist Item Approver Identifier

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Close Checklist Item

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Close Checklist Item Status

### Qualified Name
DataField::Coco::Financial Controls Evidence::Close Checklist Item::Close Checklist Item Status

### Description
Not started, complete or approved.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Financial Controls Evidence::Close Checklist Item::Close Checklist Item Status

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Close Checklist Item

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

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
- databaseName: coco_data_hub
- schemaName: financial_controls_evidence
- schemaDescription: The documentation and test evidence for the internal controls over financial reporting, and the reconciliations, approvals and checklist items produced by each close. The controls it evidences are controls over the close itself, so the repository is part of the chain rather than an audit of it.

### Anchor ID
DigitalProduct::Coco::Financial Controls Evidence

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Financial Controls Evidence

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Supplier Payment Detail Changes

*Solution component:* `CocoPharma::SolutionComponent::PaymentDetailChangeControl`  
*Category:* Evidence Record

Every change to a supplier's bank details, treated as a controlled event with independent verification rather than as routine maintenance.  This is where the payment flow has historically been attacked.

## Create Digital Product

### Display Name
Supplier Payment Detail Changes

### Product Name
Supplier Payment Detail Changes

### Qualified Name
DigitalProduct::Coco::Supplier Payment Detail Changes

### Description
Every change to a supplier's bank details, treated as a controlled event with independent verification rather than as routine maintenance.  This is where the payment flow has historically been attacked.

### Purpose
Ensures no change to where a supplier is paid takes effect without being verified with the supplier through a channel the requester did not supply.

### Category
Evidence Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

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
CollectionFolder::Coco::Strategic Digital Products::Finance

### Element Id
DigitalProduct::Coco::Supplier Payment Detail Changes

### Membership Rationale
Produced by the Finance group's `PaymentDetailChangeControl` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Supplier Payment Detail Changes Data Spec

### Qualified Name
DataSpec::Coco::Supplier Payment Detail Changes

### Description
The data structures and fields that make up the Supplier Payment Detail Changes digital product.

### Purpose
Describes the data a subscriber to Supplier Payment Detail Changes receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Supplier Payment Detail Changes

### Collection Id
DataSpec::Coco::Supplier Payment Detail Changes

### Label
data specification

___

## Create Data Structure

### Display Name
Payment Detail Change

### Qualified Name
DataStructure::Coco::Supplier Payment Detail Changes::Payment Detail Change

### Description
One row per requested change to a supplier's payment details.

### Namespace Path
coco_data_hub.supplier_payment_detail_changes

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Supplier Payment Detail Changes

### Element Id
DataStructure::Coco::Supplier Payment Detail Changes::Payment Detail Change

### Membership Rationale
The Payment Detail Change structure is part of the Supplier Payment Detail Changes data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Payment Detail Change Identifier

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::Payment Detail Change Identifier

### Description
The unique identifier of the change request.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::Payment Detail Change Identifier

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Payment Detail Change

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Supplier Identifier

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::Supplier Identifier

### Description
The supplier.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::Supplier Identifier

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Payment Detail Change

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Payment Detail Change Requested Timestamp

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::Payment Detail Change Requested Timestamp

### Description
When the change was requested.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::Payment Detail Change Requested Timestamp

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Payment Detail Change

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Payment Detail Change Requester Identifier

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::Payment Detail Change Requester Identifier

### Description
Who requested it.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::Payment Detail Change Requester Identifier

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Payment Detail Change

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Bank Account Previous Identifier

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::Bank Account Previous Identifier

### Description
The bank account before the change, masked.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::Bank Account Previous Identifier

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Payment Detail Change

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Bank Account Current Identifier

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::Bank Account Current Identifier

### Description
The bank account after the change, masked.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::Bank Account Current Identifier

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Payment Detail Change

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Payment Detail Change Status

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::Payment Detail Change Status

### Description
Pending verification, verified, rejected.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::Payment Detail Change Status

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Payment Detail Change

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Structure

### Display Name
Verification Evidence

### Qualified Name
DataStructure::Coco::Supplier Payment Detail Changes::Verification Evidence

### Description
One row per independent verification of a change.

### Namespace Path
coco_data_hub.supplier_payment_detail_changes

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Supplier Payment Detail Changes

### Element Id
DataStructure::Coco::Supplier Payment Detail Changes::Verification Evidence

### Membership Rationale
The Verification Evidence structure is part of the Supplier Payment Detail Changes data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Payment Detail Change Identifier

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::Payment Detail Change Identifier

### Description
The change verified.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::Payment Detail Change Identifier

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Verification Evidence

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Payment Detail Change Verified Timestamp

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::Payment Detail Change Verified Timestamp

### Description
When the verification was completed.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::Payment Detail Change Verified Timestamp

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Verification Evidence

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Payment Detail Change Verifier Identifier

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::Payment Detail Change Verifier Identifier

### Description
Who carried out the verification.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::Payment Detail Change Verifier Identifier

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Verification Evidence

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Payment Detail Change Channel Type

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::Payment Detail Change Channel Type

### Description
The channel used, for example call-back to a known number.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::Payment Detail Change Channel Type

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Verification Evidence

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Payment Detail Change Verified Notes

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::Payment Detail Change Verified Notes

### Description
What was confirmed and with whom.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::Payment Detail Change Verified Notes

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Verification Evidence

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

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
- databaseName: coco_data_hub
- schemaName: supplier_payment_detail_changes
- schemaDescription: Every change to a supplier's bank details, treated as a controlled event with independent verification rather than as routine maintenance. This is where the payment flow has historically been attacked.

### Anchor ID
DigitalProduct::Coco::Supplier Payment Detail Changes

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Supplier Payment Detail Changes

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Supplier Payments

*Solution component:* `CocoPharma::SolutionComponent::SupplierPaymentProcessing`  
*Category:* Transactional Record

Supplier invoices matched to purchase orders and goods receipts, the payment authorisations that followed, and the instructions sent to the bank.  Screening status and payment details are read at the moment of authorisation, the only moment at which either of them protects anything.

## Create Digital Product

### Display Name
Supplier Payments

### Product Name
Supplier Payments

### Qualified Name
DigitalProduct::Coco::Supplier Payments

### Description
Supplier invoices matched to purchase orders and goods receipts, the payment authorisations that followed, and the instructions sent to the bank.  Screening status and payment details are read at the moment of authorisation, the only moment at which either of them protects anything.

### Purpose
Records every payment with the match, the authorisation and the supplier status it was made under.

### Category
Transactional Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

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
CollectionFolder::Coco::Strategic Digital Products::Finance

### Element Id
DigitalProduct::Coco::Supplier Payments

### Membership Rationale
Produced by the Finance group's `SupplierPaymentProcessing` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Supplier Payments Data Spec

### Qualified Name
DataSpec::Coco::Supplier Payments

### Description
The data structures and fields that make up the Supplier Payments digital product.

### Purpose
Describes the data a subscriber to Supplier Payments receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Supplier Payments

### Collection Id
DataSpec::Coco::Supplier Payments

### Label
data specification

___

## Create Data Structure

### Display Name
Invoice Match

### Qualified Name
DataStructure::Coco::Supplier Payments::Invoice Match

### Description
One row per supplier invoice, matched to the order and receipt it settles.

### Namespace Path
coco_data_hub.supplier_payments

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Supplier Payments

### Element Id
DataStructure::Coco::Supplier Payments::Invoice Match

### Membership Rationale
The Invoice Match structure is part of the Supplier Payments data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Invoice Number

### Qualified Name
DataField::Coco::Supplier Payments::Invoice Match::Invoice Number

### Description
The supplier's invoice number.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payments::Invoice Match::Invoice Number

### Data Structure
DataStructure::Coco::Supplier Payments::Invoice Match

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Supplier Identifier

### Qualified Name
DataField::Coco::Supplier Payments::Invoice Match::Supplier Identifier

### Description
The supplier.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payments::Invoice Match::Supplier Identifier

### Data Structure
DataStructure::Coco::Supplier Payments::Invoice Match

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Order Identifier

### Qualified Name
DataField::Coco::Supplier Payments::Invoice Match::Order Identifier

### Description
The purchase order matched.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payments::Invoice Match::Order Identifier

### Data Structure
DataStructure::Coco::Supplier Payments::Invoice Match

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Goods Receipt Identifier

### Qualified Name
DataField::Coco::Supplier Payments::Invoice Match::Goods Receipt Identifier

### Description
The goods receipt matched.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payments::Invoice Match::Goods Receipt Identifier

### Data Structure
DataStructure::Coco::Supplier Payments::Invoice Match

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Invoice Total Amount

### Qualified Name
DataField::Coco::Supplier Payments::Invoice Match::Invoice Total Amount

### Description
The invoiced amount.

### Data Type
bigdecimal

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payments::Invoice Match::Invoice Total Amount

### Data Structure
DataStructure::Coco::Supplier Payments::Invoice Match

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Invoice Currency Code

### Qualified Name
DataField::Coco::Supplier Payments::Invoice Match::Invoice Currency Code

### Description
The currency.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
3

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payments::Invoice Match::Invoice Currency Code

### Data Structure
DataStructure::Coco::Supplier Payments::Invoice Match

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Invoice Match Status

### Qualified Name
DataField::Coco::Supplier Payments::Invoice Match::Invoice Match Status

### Description
Matched, variance or unmatched.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payments::Invoice Match::Invoice Match Status

### Data Structure
DataStructure::Coco::Supplier Payments::Invoice Match

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Structure

### Display Name
Payment Instruction

### Qualified Name
DataStructure::Coco::Supplier Payments::Payment Instruction

### Description
One row per payment authorised and instructed to the bank.

### Namespace Path
coco_data_hub.supplier_payments

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Supplier Payments

### Element Id
DataStructure::Coco::Supplier Payments::Payment Instruction

### Membership Rationale
The Payment Instruction structure is part of the Supplier Payments data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Payment Identifier

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::Payment Identifier

### Description
The unique identifier of the payment.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payments::Payment Instruction::Payment Identifier

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Supplier Identifier

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::Supplier Identifier

### Description
The payee.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payments::Payment Instruction::Supplier Identifier

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Invoice Number

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::Invoice Number

### Description
The invoice settled.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payments::Payment Instruction::Invoice Number

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Payment Amount

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::Payment Amount

### Description
The amount paid.

### Data Type
bigdecimal

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payments::Payment Instruction::Payment Amount

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Payment Currency Code

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::Payment Currency Code

### Description
The currency.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
3

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payments::Payment Instruction::Payment Currency Code

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Payment Authoriser Identifier

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::Payment Authoriser Identifier

### Description
Who authorised the payment.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payments::Payment Instruction::Payment Authoriser Identifier

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Payment Authorised Timestamp

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::Payment Authorised Timestamp

### Description
When it was authorised.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payments::Payment Instruction::Payment Authorised Timestamp

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Supplier Screened Status

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::Supplier Screened Status

### Description
The supplier's screening status at authorisation.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payments::Payment Instruction::Supplier Screened Status

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Bank Account Current Identifier

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::Bank Account Current Identifier

### Description
The account paid, masked.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payments::Payment Instruction::Bank Account Current Identifier

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

### Position
9

### Coverage Category
CORE_DETAIL

### Label
field 9

___

## Create Data Field

### Display Name
Ledger Account Code

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::Ledger Account Code

### Description
The cost coding of the payment.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Supplier Payments::Payment Instruction::Ledger Account Code

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

### Position
10

### Coverage Category
CORE_DETAIL

### Label
field 10

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
- databaseName: coco_data_hub
- schemaName: supplier_payments
- schemaDescription: Supplier invoices matched to purchase orders and goods receipts, the payment authorisations that followed, and the instructions sent to the bank. Screening status and payment details are read at the moment of authorisation, the only moment at which either of them protects anything.

### Anchor ID
DigitalProduct::Coco::Supplier Payments

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Supplier Payments

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Payment Anomaly Findings

*Solution component:* `CocoPharma::SolutionComponent::TransactionMonitoring`  
*Category:* Insight

The patterns found across supplier payments and expense claims that no single transaction shows: duplicate payments, unusual supplier behaviour, and the concerns raised as a result.  The fraud that motivated this chain was visible only across the whole flow.

## Create Digital Product

### Display Name
Payment Anomaly Findings

### Product Name
Payment Anomaly Findings

### Qualified Name
DigitalProduct::Coco::Payment Anomaly Findings

### Description
The patterns found across supplier payments and expense claims that no single transaction shows: duplicate payments, unusual supplier behaviour, and the concerns raised as a result.  The fraud that motivated this chain was visible only across the whole flow.

### Purpose
Turns the payment and expense streams into concerns the supplier register and finance can act on.

### Category
Insight

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

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
CollectionFolder::Coco::Strategic Digital Products::Finance

### Element Id
DigitalProduct::Coco::Payment Anomaly Findings

### Membership Rationale
Produced by the Finance group's `TransactionMonitoring` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Payment Anomaly Findings Data Spec

### Qualified Name
DataSpec::Coco::Payment Anomaly Findings

### Description
The data structures and fields that make up the Payment Anomaly Findings digital product.

### Purpose
Describes the data a subscriber to Payment Anomaly Findings receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Payment Anomaly Findings

### Collection Id
DataSpec::Coco::Payment Anomaly Findings

### Label
data specification

___

## Create Data Structure

### Display Name
Anomaly Finding

### Qualified Name
DataStructure::Coco::Payment Anomaly Findings::Anomaly Finding

### Description
One row per anomaly detected.

### Namespace Path
coco_data_hub.payment_anomaly_findings

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Payment Anomaly Findings

### Element Id
DataStructure::Coco::Payment Anomaly Findings::Anomaly Finding

### Membership Rationale
The Anomaly Finding structure is part of the Payment Anomaly Findings data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Anomaly Identifier

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::Anomaly Identifier

### Description
The unique identifier of the finding.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::Anomaly Identifier

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Anomaly Finding

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Anomaly Detected Timestamp

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::Anomaly Detected Timestamp

### Description
When it was detected.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::Anomaly Detected Timestamp

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Anomaly Finding

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Anomaly Type

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::Anomaly Type

### Description
Duplicate payment, split payment, new-supplier spike, claim pattern or other.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::Anomaly Type

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Anomaly Finding

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Supplier Identifier

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::Supplier Identifier

### Description
The supplier implicated, if any.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::Supplier Identifier

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Anomaly Finding

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::Worker Pseudonym Identifier

### Description
The claimant implicated, if any.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Anomaly Finding

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Anomaly Description

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::Anomaly Description

### Description
What was observed.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::Anomaly Description

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Anomaly Finding

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Anomaly Severity

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::Anomaly Severity

### Description
The assessed seriousness.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::Anomaly Severity

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Anomaly Finding

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Anomaly Current Status

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::Anomaly Current Status

### Description
Open, under investigation, closed as false positive, confirmed.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::Anomaly Current Status

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Anomaly Finding

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Structure

### Display Name
Monitored Transaction

### Qualified Name
DataStructure::Coco::Payment Anomaly Findings::Monitored Transaction

### Description
One row per transaction contributing to a finding.

### Namespace Path
coco_data_hub.payment_anomaly_findings

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Payment Anomaly Findings

### Element Id
DataStructure::Coco::Payment Anomaly Findings::Monitored Transaction

### Membership Rationale
The Monitored Transaction structure is part of the Payment Anomaly Findings data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Anomaly Identifier

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::Anomaly Identifier

### Description
The finding.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::Anomaly Identifier

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Monitored Transaction

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Transaction Identifier

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::Transaction Identifier

### Description
The payment or claim.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::Transaction Identifier

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Monitored Transaction

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Transaction Type

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::Transaction Type

### Description
Supplier payment or expense claim.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::Transaction Type

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Monitored Transaction

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Transaction Amount

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::Transaction Amount

### Description
Its amount.

### Data Type
bigdecimal

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::Transaction Amount

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Monitored Transaction

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Transaction Date

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::Transaction Date

### Description
Its date.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::Transaction Date

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Monitored Transaction

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

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
- databaseName: coco_data_hub
- schemaName: payment_anomaly_findings
- schemaDescription: The patterns found across supplier payments and expense claims that no single transaction shows: duplicate payments, unusual supplier behaviour, and the concerns raised as a result. The fraud that motivated this chain was visible only across the whole flow.

### Anchor ID
DigitalProduct::Coco::Payment Anomaly Findings

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Payment Anomaly Findings

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Transfers Of Value

*Solution component:* `CocoPharma::SolutionComponent::TransfersOfValueRegister`  
*Category:* Evidence Record

Payments and benefits provided to healthcare professionals and organisations, from whichever flow they originate, identified and recorded so that they can be disclosed.  Reconstructing this afterwards from a general ledger is the failure it exists to prevent.

## Create Digital Product

### Display Name
Transfers Of Value

### Product Name
Transfers Of Value

### Qualified Name
DigitalProduct::Coco::Transfers Of Value

### Description
Payments and benefits provided to healthcare professionals and organisations, from whichever flow they originate, identified and recorded so that they can be disclosed.  Reconstructing this afterwards from a general ledger is the failure it exists to prevent.

### Purpose
Provides the disclosure process with a complete register of transfers of value built as they happen.

### Category
Evidence Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

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
CollectionFolder::Coco::Strategic Digital Products::Finance

### Element Id
DigitalProduct::Coco::Transfers Of Value

### Membership Rationale
Produced by the Finance group's `TransfersOfValueRegister` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Transfers Of Value Data Spec

### Qualified Name
DataSpec::Coco::Transfers Of Value

### Description
The data structures and fields that make up the Transfers Of Value digital product.

### Purpose
Describes the data a subscriber to Transfers Of Value receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Transfers Of Value

### Collection Id
DataSpec::Coco::Transfers Of Value

### Label
data specification

___

## Create Data Structure

### Display Name
Transfer Of Value

### Qualified Name
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Description
One row per payment or benefit to a healthcare professional or organisation.

### Namespace Path
coco_data_hub.transfers_of_value

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Transfers Of Value

### Element Id
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Membership Rationale
The Transfer Of Value structure is part of the Transfers Of Value data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Transfer Of Value Identifier

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::Transfer Of Value Identifier

### Description
The unique identifier of the transfer.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Transfers Of Value::Transfer Of Value::Transfer Of Value Identifier

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Transfer Of Value Recipient Identifier

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::Transfer Of Value Recipient Identifier

### Description
The healthcare professional or organisation.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Transfers Of Value::Transfer Of Value::Transfer Of Value Recipient Identifier

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Transfer Of Value Recipient Type

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::Transfer Of Value Recipient Type

### Description
Individual professional or organisation.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Transfers Of Value::Transfer Of Value::Transfer Of Value Recipient Type

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Transfer Of Value Type

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::Transfer Of Value Type

### Description
Fee, hospitality, travel, grant or other.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Transfers Of Value::Transfer Of Value::Transfer Of Value Type

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Transfer Of Value Description

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::Transfer Of Value Description

### Description
The purpose of the transfer.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Transfers Of Value::Transfer Of Value::Transfer Of Value Description

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Transfer Of Value Amount

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::Transfer Of Value Amount

### Description
The value transferred.

### Data Type
bigdecimal

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Transfers Of Value::Transfer Of Value::Transfer Of Value Amount

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Transfer Of Value Currency Code

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::Transfer Of Value Currency Code

### Description
The currency.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
3

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Transfers Of Value::Transfer Of Value::Transfer Of Value Currency Code

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Transfer Of Value Date

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::Transfer Of Value Date

### Description
When it was provided.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Transfers Of Value::Transfer Of Value::Transfer Of Value Date

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Transaction Identifier

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::Transaction Identifier

### Description
The payment or expense claim it originated from.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Transfers Of Value::Transfer Of Value::Transaction Identifier

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Position
9

### Coverage Category
CORE_DETAIL

### Label
field 9

___

## Create Data Field

### Display Name
Transfer Of Value Disclosed Flag

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::Transfer Of Value Disclosed Flag

### Description
Whether it has been included in a disclosure.

### Data Type
boolean

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Transfers Of Value::Transfer Of Value::Transfer Of Value Disclosed Flag

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Position
10

### Coverage Category
CORE_DETAIL

### Label
field 10

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
- databaseName: coco_data_hub
- schemaName: transfers_of_value
- schemaDescription: Payments and benefits provided to healthcare professionals and organisations, from whichever flow they originate, identified and recorded so that they can be disclosed. Reconstructing this afterwards from a general ledger is the failure it exists to prevent.

### Anchor ID
DigitalProduct::Coco::Transfers Of Value

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Transfers Of Value

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Expense Approvals

*Solution component:* `CocoPharma::SolutionComponent::ExpenseApprovalWorkflow`  
*Category:* Transactional Record

Expense claims routed for approval, the approver each was sent to and the decision taken, carried forward to payment.  The approval is only worth anything if it is still attached to the claim when the payment is made.

## Create Digital Product

### Display Name
Expense Approvals

### Product Name
Expense Approvals

### Qualified Name
DigitalProduct::Coco::Expense Approvals

### Description
Expense claims routed for approval, the approver each was sent to and the decision taken, carried forward to payment.  The approval is only worth anything if it is still attached to the claim when the payment is made.

### Purpose
Keeps the approval and the claim together from submission to posting.

### Category
Transactional Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

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
CollectionFolder::Coco::Strategic Digital Products::Finance

### Element Id
DigitalProduct::Coco::Expense Approvals

### Membership Rationale
Produced by the Finance group's `ExpenseApprovalWorkflow` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Expense Approvals Data Spec

### Qualified Name
DataSpec::Coco::Expense Approvals

### Description
The data structures and fields that make up the Expense Approvals digital product.

### Purpose
Describes the data a subscriber to Expense Approvals receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Expense Approvals

### Collection Id
DataSpec::Coco::Expense Approvals

### Label
data specification

___

## Create Data Structure

### Display Name
Expense Claim

### Qualified Name
DataStructure::Coco::Expense Approvals::Expense Claim

### Description
One row per claim submitted for approval.

### Namespace Path
coco_data_hub.expense_approvals

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Expense Approvals

### Element Id
DataStructure::Coco::Expense Approvals::Expense Claim

### Membership Rationale
The Expense Claim structure is part of the Expense Approvals data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Claim Identifier

### Qualified Name
DataField::Coco::Expense Approvals::Expense Claim::Claim Identifier

### Description
The unique identifier of the claim.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Expense Approvals::Expense Claim::Claim Identifier

### Data Structure
DataStructure::Coco::Expense Approvals::Expense Claim

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Expense Approvals::Expense Claim::Worker Pseudonym Identifier

### Description
The claimant.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Expense Approvals::Expense Claim::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Expense Approvals::Expense Claim

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Claim Submitted Timestamp

### Qualified Name
DataField::Coco::Expense Approvals::Expense Claim::Claim Submitted Timestamp

### Description
When it was submitted.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Expense Approvals::Expense Claim::Claim Submitted Timestamp

### Data Structure
DataStructure::Coco::Expense Approvals::Expense Claim

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Claim Total Amount

### Qualified Name
DataField::Coco::Expense Approvals::Expense Claim::Claim Total Amount

### Description
The value claimed.

### Data Type
bigdecimal

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Expense Approvals::Expense Claim::Claim Total Amount

### Data Structure
DataStructure::Coco::Expense Approvals::Expense Claim

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Claim Currency Code

### Qualified Name
DataField::Coco::Expense Approvals::Expense Claim::Claim Currency Code

### Description
The currency.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
3

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Expense Approvals::Expense Claim::Claim Currency Code

### Data Structure
DataStructure::Coco::Expense Approvals::Expense Claim

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Ledger Account Code

### Qualified Name
DataField::Coco::Expense Approvals::Expense Claim::Ledger Account Code

### Description
The cost coding.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Expense Approvals::Expense Claim::Ledger Account Code

### Data Structure
DataStructure::Coco::Expense Approvals::Expense Claim

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Claim Approver Identifier

### Qualified Name
DataField::Coco::Expense Approvals::Expense Claim::Claim Approver Identifier

### Description
The approver it was routed to.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Expense Approvals::Expense Claim::Claim Approver Identifier

### Data Structure
DataStructure::Coco::Expense Approvals::Expense Claim

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Structure

### Display Name
Approval Decision

### Qualified Name
DataStructure::Coco::Expense Approvals::Approval Decision

### Description
One row per decision on a claim.

### Namespace Path
coco_data_hub.expense_approvals

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Expense Approvals

### Element Id
DataStructure::Coco::Expense Approvals::Approval Decision

### Membership Rationale
The Approval Decision structure is part of the Expense Approvals data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Claim Identifier

### Qualified Name
DataField::Coco::Expense Approvals::Approval Decision::Claim Identifier

### Description
The claim.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Expense Approvals::Approval Decision::Claim Identifier

### Data Structure
DataStructure::Coco::Expense Approvals::Approval Decision

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Claim Approval Timestamp

### Qualified Name
DataField::Coco::Expense Approvals::Approval Decision::Claim Approval Timestamp

### Description
When.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Expense Approvals::Approval Decision::Claim Approval Timestamp

### Data Structure
DataStructure::Coco::Expense Approvals::Approval Decision

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Claim Approver Identifier

### Qualified Name
DataField::Coco::Expense Approvals::Approval Decision::Claim Approver Identifier

### Description
Who decided.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Expense Approvals::Approval Decision::Claim Approver Identifier

### Data Structure
DataStructure::Coco::Expense Approvals::Approval Decision

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Claim Approval Status

### Qualified Name
DataField::Coco::Expense Approvals::Approval Decision::Claim Approval Status

### Description
Approved, rejected or returned.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Expense Approvals::Approval Decision::Claim Approval Status

### Data Structure
DataStructure::Coco::Expense Approvals::Approval Decision

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Claim Approval Notes

### Qualified Name
DataField::Coco::Expense Approvals::Approval Decision::Claim Approval Notes

### Description
The approver's comments.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Expense Approvals::Approval Decision::Claim Approval Notes

### Data Structure
DataStructure::Coco::Expense Approvals::Approval Decision

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

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
- databaseName: coco_data_hub
- schemaName: expense_approvals
- schemaDescription: Expense claims routed for approval, the approver each was sent to and the decision taken, carried forward to payment. The approval is only worth anything if it is still attached to the claim when the payment is made.

### Anchor ID
DigitalProduct::Coco::Expense Approvals

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Expense Approvals

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# General Ledger Balances

*Solution component:* `SolutionComponent::Accounting ledgers::V1.0`  
*Category:* Transactional Record

The general ledger of each legal entity: the transactions posted from every feed, adjustment and payment, and the account balances that result.  It is the source of the entity trial balances that consolidation starts from and of the manual entries that review examines.

## Create Digital Product

### Display Name
General Ledger Balances

### Product Name
General Ledger Balances

### Qualified Name
DigitalProduct::Coco::General Ledger Balances

### Description
The general ledger of each legal entity: the transactions posted from every feed, adjustment and payment, and the account balances that result.  It is the source of the entity trial balances that consolidation starts from and of the manual entries that review examines.

### Purpose
Provides the authoritative accounting record each entity's figures are drawn from.

### Category
Transactional Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

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
CollectionFolder::Coco::Strategic Digital Products::Finance

### Element Id
DigitalProduct::Coco::General Ledger Balances

### Membership Rationale
Produced by the Finance group's `Accounting ledgers` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
General Ledger Balances Data Spec

### Qualified Name
DataSpec::Coco::General Ledger Balances

### Description
The data structures and fields that make up the General Ledger Balances digital product.

### Purpose
Describes the data a subscriber to General Ledger Balances receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::General Ledger Balances

### Collection Id
DataSpec::Coco::General Ledger Balances

### Label
data specification

___

## Create Data Structure

### Display Name
Ledger Transaction

### Qualified Name
DataStructure::Coco::General Ledger Balances::Ledger Transaction

### Description
One row per transaction posted to the ledger.

### Namespace Path
coco_data_hub.general_ledger_balances

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::General Ledger Balances

### Element Id
DataStructure::Coco::General Ledger Balances::Ledger Transaction

### Membership Rationale
The Ledger Transaction structure is part of the General Ledger Balances data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Transaction Identifier

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Transaction::Transaction Identifier

### Description
The unique identifier of the ledger transaction.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::General Ledger Balances::Ledger Transaction::Transaction Identifier

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Transaction

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Legal Entity Code

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Transaction::Legal Entity Code

### Description
The entity.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::General Ledger Balances::Ledger Transaction::Legal Entity Code

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Transaction

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Accounting Period Code

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Transaction::Accounting Period Code

### Description
The period.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::General Ledger Balances::Ledger Transaction::Accounting Period Code

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Transaction

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Ledger Account Code

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Transaction::Ledger Account Code

### Description
The account.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::General Ledger Balances::Ledger Transaction::Ledger Account Code

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Transaction

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Transaction Amount

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Transaction::Transaction Amount

### Description
The amount.

### Data Type
bigdecimal

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::General Ledger Balances::Ledger Transaction::Transaction Amount

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Transaction

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Transaction Currency Code

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Transaction::Transaction Currency Code

### Description
The currency.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
3

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::General Ledger Balances::Ledger Transaction::Transaction Currency Code

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Transaction

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Transaction Posted Timestamp

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Transaction::Transaction Posted Timestamp

### Description
When posted.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::General Ledger Balances::Ledger Transaction::Transaction Posted Timestamp

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Transaction

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Feed Identifier

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Transaction::Feed Identifier

### Description
The feed batch it arrived in, if from a feed.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::General Ledger Balances::Ledger Transaction::Feed Identifier

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Transaction

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Field

### Display Name
Journal Entry Identifier

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Transaction::Journal Entry Identifier

### Description
The manual journal it arrived in, if manual.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::General Ledger Balances::Ledger Transaction::Journal Entry Identifier

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Transaction

### Position
9

### Coverage Category
CORE_DETAIL

### Label
field 9

___

## Create Data Structure

### Display Name
Ledger Account Balance

### Qualified Name
DataStructure::Coco::General Ledger Balances::Ledger Account Balance

### Description
One row per account per entity per period.

### Namespace Path
coco_data_hub.general_ledger_balances

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::General Ledger Balances

### Element Id
DataStructure::Coco::General Ledger Balances::Ledger Account Balance

### Membership Rationale
The Ledger Account Balance structure is part of the General Ledger Balances data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Legal Entity Code

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Account Balance::Legal Entity Code

### Description
The entity.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::General Ledger Balances::Ledger Account Balance::Legal Entity Code

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Account Balance

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Accounting Period Code

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Account Balance::Accounting Period Code

### Description
The period.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
10

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::General Ledger Balances::Ledger Account Balance::Accounting Period Code

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Account Balance

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Ledger Account Code

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Account Balance::Ledger Account Code

### Description
The account.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::General Ledger Balances::Ledger Account Balance::Ledger Account Code

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Account Balance

### Position
3

### Coverage Category
IDENTIFIER

### Label
field 3

___

## Create Data Field

### Display Name
Ledger Account Name

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Account Balance::Ledger Account Name

### Description
The account's name.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
120

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::General Ledger Balances::Ledger Account Balance::Ledger Account Name

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Account Balance

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Ledger Account Balance Amount

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Account Balance::Ledger Account Balance Amount

### Description
The closing balance.

### Data Type
bigdecimal

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::General Ledger Balances::Ledger Account Balance::Ledger Account Balance Amount

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Account Balance

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Ledger Currency Code

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Account Balance::Ledger Currency Code

### Description
The currency.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
3

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::General Ledger Balances::Ledger Account Balance::Ledger Currency Code

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Account Balance

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

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
- databaseName: coco_data_hub
- schemaName: general_ledger_balances
- schemaDescription: The general ledger of each legal entity: the transactions posted from every feed, adjustment and payment, and the account balances that result. It is the source of the entity trial balances that consolidation starts from and of the manual entries that review examines.

### Anchor ID
DigitalProduct::Coco::General Ledger Balances

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::General Ledger Balances

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___

# Employee Expense Claims

*Solution component:* `SolutionComponent::Employee Expense Tool::V1.0`  
*Category:* Transactional Record

The claims employees submit for expenses incurred, line by line with their supporting evidence, and the record of which workers may claim against which cost centres.  It is the entry point of the expense payment chain and a source of transfers of value that disclosure must catch.

## Create Digital Product

### Display Name
Employee Expense Claims

### Product Name
Employee Expense Claims

### Qualified Name
DigitalProduct::Coco::Employee Expense Claims

### Description
The claims employees submit for expenses incurred, line by line with their supporting evidence, and the record of which workers may claim against which cost centres.  It is the entry point of the expense payment chain and a source of transfers of value that disclosure must catch.

### Purpose
Captures each expense with enough detail for approval, cost coding and disclosure screening.

### Category
Transactional Record

### Maturity
Proposed

### Service Life
Life of the supply chain it serves

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
CollectionFolder::Coco::Strategic Digital Products::Finance

### Element Id
DigitalProduct::Coco::Employee Expense Claims

### Membership Rationale
Produced by the Finance group's `Employee Expense Tool` component.

### Membership Status
VALIDATED

___

## Create Data Spec

### Display Name
Employee Expense Claims Data Spec

### Qualified Name
DataSpec::Coco::Employee Expense Claims

### Description
The data structures and fields that make up the Employee Expense Claims digital product.

### Purpose
Describes the data a subscriber to Employee Expense Claims receives, structure by structure and field by field, using the Data Field Naming standard.

### Version Identifier
1.0

### Content Status
ACTIVE

### Authors
- Erin Overview
- Peter Profile

___

## Link Data Description

### Element Id
DigitalProduct::Coco::Employee Expense Claims

### Collection Id
DataSpec::Coco::Employee Expense Claims

### Label
data specification

___

## Create Data Structure

### Display Name
Claim Submission

### Qualified Name
DataStructure::Coco::Employee Expense Claims::Claim Submission

### Description
One row per claim as submitted by the claimant.

### Namespace Path
coco_data_hub.employee_expense_claims

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Employee Expense Claims

### Element Id
DataStructure::Coco::Employee Expense Claims::Claim Submission

### Membership Rationale
The Claim Submission structure is part of the Employee Expense Claims data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Claim Identifier

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Submission::Claim Identifier

### Description
The unique identifier of the claim.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Employee Expense Claims::Claim Submission::Claim Identifier

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Submission

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Submission::Worker Pseudonym Identifier

### Description
The claimant.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Employee Expense Claims::Claim Submission::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Submission

### Position
2

### Coverage Category
CORE_DETAIL

### Label
field 2

___

## Create Data Field

### Display Name
Claim Submitted Timestamp

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Submission::Claim Submitted Timestamp

### Description
When submitted.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Employee Expense Claims::Claim Submission::Claim Submitted Timestamp

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Submission

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Claim Total Amount

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Submission::Claim Total Amount

### Description
The total claimed.

### Data Type
bigdecimal

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Employee Expense Claims::Claim Submission::Claim Total Amount

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Submission

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Claim Currency Code

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Submission::Claim Currency Code

### Description
The currency.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
3

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Employee Expense Claims::Claim Submission::Claim Currency Code

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Submission

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Claim Current Status

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Submission::Claim Current Status

### Description
Draft, submitted, approved, paid or rejected.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Employee Expense Claims::Claim Submission::Claim Current Status

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Submission

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Structure

### Display Name
Claim Line

### Qualified Name
DataStructure::Coco::Employee Expense Claims::Claim Line

### Description
One row per expense within a claim.

### Namespace Path
coco_data_hub.employee_expense_claims

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Employee Expense Claims

### Element Id
DataStructure::Coco::Employee Expense Claims::Claim Line

### Membership Rationale
The Claim Line structure is part of the Employee Expense Claims data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Claim Identifier

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Line::Claim Identifier

### Description
The claim.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Employee Expense Claims::Claim Line::Claim Identifier

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Line

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Claim Line Number

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Line::Claim Line Number

### Description
The position of the line in the claim.

### Data Type
int

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Employee Expense Claims::Claim Line::Claim Line Number

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Line

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Claim Line Type

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Line::Claim Line Type

### Description
Travel, hospitality, accommodation or other.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Employee Expense Claims::Claim Line::Claim Line Type

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Line

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Claim Line Date

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Line::Claim Line Date

### Description
When the expense was incurred.

### Data Type
date

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Employee Expense Claims::Claim Line::Claim Line Date

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Line

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

___

## Create Data Field

### Display Name
Claim Line Amount

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Line::Claim Line Amount

### Description
The amount.

### Data Type
bigdecimal

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Employee Expense Claims::Claim Line::Claim Line Amount

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Line

### Position
5

### Coverage Category
CORE_DETAIL

### Label
field 5

___

## Create Data Field

### Display Name
Claim Line Description

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Line::Claim Line Description

### Description
What the expense was for.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Employee Expense Claims::Claim Line::Claim Line Description

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Line

### Position
6

### Coverage Category
CORE_DETAIL

### Label
field 6

___

## Create Data Field

### Display Name
Claim Line Recipient Identifier

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Line::Claim Line Recipient Identifier

### Description
The healthcare professional entertained, if any.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Employee Expense Claims::Claim Line::Claim Line Recipient Identifier

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Line

### Position
7

### Coverage Category
CORE_DETAIL

### Label
field 7

___

## Create Data Field

### Display Name
Claim Line Evidence Identifier

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Line::Claim Line Evidence Identifier

### Description
The receipt or other evidence attached.

### Data Type
string

### Is Nullable
true

### Minimum Cardinality
0

### Length
60

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Employee Expense Claims::Claim Line::Claim Line Evidence Identifier

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Line

### Position
8

### Coverage Category
CORE_DETAIL

### Label
field 8

___

## Create Data Structure

### Display Name
Claimant Cost Centre

### Qualified Name
DataStructure::Coco::Employee Expense Claims::Claimant Cost Centre

### Description
One row per worker per cost centre they may claim against, with the approver and spending authority.

### Namespace Path
coco_data_hub.employee_expense_claims

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Add Member to Collection

### Collection Id
DataSpec::Coco::Employee Expense Claims

### Element Id
DataStructure::Coco::Employee Expense Claims::Claimant Cost Centre

### Membership Rationale
The Claimant Cost Centre structure is part of the Employee Expense Claims data specification.

### Membership Status
VALIDATED

___

## Create Data Field

### Display Name
Worker Pseudonym Identifier

### Qualified Name
DataField::Coco::Employee Expense Claims::Claimant Cost Centre::Worker Pseudonym Identifier

### Description
The worker.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Employee Expense Claims::Claimant Cost Centre::Worker Pseudonym Identifier

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claimant Cost Centre

### Position
1

### Coverage Category
IDENTIFIER

### Label
field 1

___

## Create Data Field

### Display Name
Cost Centre Code

### Qualified Name
DataField::Coco::Employee Expense Claims::Claimant Cost Centre::Cost Centre Code

### Description
The cost centre.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
20

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Employee Expense Claims::Claimant Cost Centre::Cost Centre Code

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claimant Cost Centre

### Position
2

### Coverage Category
IDENTIFIER

### Label
field 2

___

## Create Data Field

### Display Name
Claim Approver Identifier

### Qualified Name
DataField::Coco::Employee Expense Claims::Claimant Cost Centre::Claim Approver Identifier

### Description
The approver for the worker's claims.

### Data Type
string

### Is Nullable
false

### Minimum Cardinality
1

### Length
40

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Employee Expense Claims::Claimant Cost Centre::Claim Approver Identifier

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claimant Cost Centre

### Position
3

### Coverage Category
CORE_DETAIL

### Label
field 3

___

## Create Data Field

### Display Name
Claim Maximum Amount

### Qualified Name
DataField::Coco::Employee Expense Claims::Claimant Cost Centre::Claim Maximum Amount

### Description
The spending authority applying to the worker.

### Data Type
bigdecimal

### Is Nullable
true

### Minimum Cardinality
0

### Version Identifier
1.0

### Content Status
ACTIVE

___

## Link Data Field to Data Structure

### Data Field
DataField::Coco::Employee Expense Claims::Claimant Cost Centre::Claim Maximum Amount

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claimant Cost Centre

### Position
4

### Coverage Category
CORE_DETAIL

### Label
field 4

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
- databaseName: coco_data_hub
- schemaName: employee_expense_claims
- schemaDescription: The claims employees submit for expenses incurred, line by line with their supporting evidence, and the record of which workers may claim against which cost centres. It is the entry point of the expense payment chain and a source of transfers of value that disclosure must catch.

### Anchor ID
DigitalProduct::Coco::Employee Expense Claims

### Is Own Anchor
false

### Parent ID
DigitalProduct::Coco::Employee Expense Claims

### Parent Relationship Type Name
CollectionMembership

### Parent at End1
true

___


----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
