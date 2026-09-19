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
2. creates its **data spec** and attaches it with a `DataDescription` relationship, then the **data structures**, each added to the spec, and the **data fields**, each linked to its structure with a `MemberDataField` relationship, named to the [Data Field Naming](../data-field-naming/README.md) standard;
3. creates the **PostgreSQL tabular data set collection** the product is read from, using the PostgreSQL schema template, as a member of the product.  The schema is named after the product, in the `coco_pharma` database on `Coco PostgreSQL Server 1`.

13 products, 27 data structures, 173 data fields.  This file loads after `catalog.md`.

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
coco_pharma.treatment_invoices

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
InvoiceNumber

### Qualified Name
DataField::Coco::Treatment Invoices::Invoice::InvoiceNumber

### Description
The invoice number.

### Data Type
string

### Position
1

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
DataField::Coco::Treatment Invoices::Invoice::InvoiceNumber

### Data Structure
DataStructure::Coco::Treatment Invoices::Invoice

### Label
field 1

___

## Create Data Field

### Display Name
InvoiceDate

### Qualified Name
DataField::Coco::Treatment Invoices::Invoice::InvoiceDate

### Description
When the invoice was raised.

### Data Type
date

### Position
2

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
DataField::Coco::Treatment Invoices::Invoice::InvoiceDate

### Data Structure
DataStructure::Coco::Treatment Invoices::Invoice

### Label
field 2

___

## Create Data Field

### Display Name
OrderIdentifier

### Qualified Name
DataField::Coco::Treatment Invoices::Invoice::OrderIdentifier

### Description
The treatment order invoiced.

### Data Type
string

### Position
3

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
DataField::Coco::Treatment Invoices::Invoice::OrderIdentifier

### Data Structure
DataStructure::Coco::Treatment Invoices::Invoice

### Label
field 3

___

## Create Data Field

### Display Name
CustomerIdentifier

### Qualified Name
DataField::Coco::Treatment Invoices::Invoice::CustomerIdentifier

### Description
The organisation invoiced.

### Data Type
string

### Position
4

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
DataField::Coco::Treatment Invoices::Invoice::CustomerIdentifier

### Data Structure
DataStructure::Coco::Treatment Invoices::Invoice

### Label
field 4

___

## Create Data Field

### Display Name
InvoiceTotalAmount

### Qualified Name
DataField::Coco::Treatment Invoices::Invoice::InvoiceTotalAmount

### Description
The invoiced value.

### Data Type
bigdecimal

### Position
5

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
DataField::Coco::Treatment Invoices::Invoice::InvoiceTotalAmount

### Data Structure
DataStructure::Coco::Treatment Invoices::Invoice

### Label
field 5

___

## Create Data Field

### Display Name
InvoiceCurrencyCode

### Qualified Name
DataField::Coco::Treatment Invoices::Invoice::InvoiceCurrencyCode

### Description
The currency of the invoice.

### Data Type
string

### Position
6

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
DataField::Coco::Treatment Invoices::Invoice::InvoiceCurrencyCode

### Data Structure
DataStructure::Coco::Treatment Invoices::Invoice

### Label
field 6

___

## Create Data Field

### Display Name
InvoiceDueDate

### Qualified Name
DataField::Coco::Treatment Invoices::Invoice::InvoiceDueDate

### Description
When payment is due.

### Data Type
date

### Position
7

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
DataField::Coco::Treatment Invoices::Invoice::InvoiceDueDate

### Data Structure
DataStructure::Coco::Treatment Invoices::Invoice

### Label
field 7

___

## Create Data Field

### Display Name
InvoiceCurrentStatus

### Qualified Name
DataField::Coco::Treatment Invoices::Invoice::InvoiceCurrentStatus

### Description
Whether the invoice is open, paid or credited.

### Data Type
string

### Position
8

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
DataField::Coco::Treatment Invoices::Invoice::InvoiceCurrentStatus

### Data Structure
DataStructure::Coco::Treatment Invoices::Invoice

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
coco_pharma.treatment_invoices

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
InvoiceNumber

### Qualified Name
DataField::Coco::Treatment Invoices::Revenue Recognition::InvoiceNumber

### Description
The invoice.

### Data Type
string

### Position
1

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
DataField::Coco::Treatment Invoices::Revenue Recognition::InvoiceNumber

### Data Structure
DataStructure::Coco::Treatment Invoices::Revenue Recognition

### Label
field 1

___

## Create Data Field

### Display Name
RevenueRecognitionDate

### Qualified Name
DataField::Coco::Treatment Invoices::Revenue Recognition::RevenueRecognitionDate

### Description
When the revenue is recognised.

### Data Type
date

### Position
2

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
DataField::Coco::Treatment Invoices::Revenue Recognition::RevenueRecognitionDate

### Data Structure
DataStructure::Coco::Treatment Invoices::Revenue Recognition

### Label
field 2

___

## Create Data Field

### Display Name
RevenueAmount

### Qualified Name
DataField::Coco::Treatment Invoices::Revenue Recognition::RevenueAmount

### Description
The revenue recognised.

### Data Type
bigdecimal

### Position
3

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
DataField::Coco::Treatment Invoices::Revenue Recognition::RevenueAmount

### Data Structure
DataStructure::Coco::Treatment Invoices::Revenue Recognition

### Label
field 3

___

## Create Data Field

### Display Name
OrderDeliveryDate

### Qualified Name
DataField::Coco::Treatment Invoices::Revenue Recognition::OrderDeliveryDate

### Description
The delivery date the recognition relies on.

### Data Type
date

### Position
4

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
DataField::Coco::Treatment Invoices::Revenue Recognition::OrderDeliveryDate

### Data Structure
DataStructure::Coco::Treatment Invoices::Revenue Recognition

### Label
field 4

___

## Create Data Field

### Display Name
LedgerAccountCode

### Qualified Name
DataField::Coco::Treatment Invoices::Revenue Recognition::LedgerAccountCode

### Description
The revenue account posted to.

### Data Type
string

### Position
5

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
DataField::Coco::Treatment Invoices::Revenue Recognition::LedgerAccountCode

### Data Structure
DataStructure::Coco::Treatment Invoices::Revenue Recognition

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: treatment_invoices
- schemaDescription: The invoices raised for fulfilled treatment orders and the revenue recognition data that accompanies them. It is where a clinical event becomes a financial one, and where the fulfilment record and the financial record must agree.

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
coco_pharma.subledger_postings

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
FeedIdentifier

### Qualified Name
DataField::Coco::Subledger Postings::Posting Batch::FeedIdentifier

### Description
The unique identifier of the batch.

### Data Type
string

### Position
1

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
DataField::Coco::Subledger Postings::Posting Batch::FeedIdentifier

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Batch

### Label
field 1

___

## Create Data Field

### Display Name
SystemIdentifier

### Qualified Name
DataField::Coco::Subledger Postings::Posting Batch::SystemIdentifier

### Description
The source system the feed comes from.

### Data Type
string

### Position
2

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
DataField::Coco::Subledger Postings::Posting Batch::SystemIdentifier

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Batch

### Label
field 2

___

## Create Data Field

### Display Name
AccountingPeriodCode

### Qualified Name
DataField::Coco::Subledger Postings::Posting Batch::AccountingPeriodCode

### Description
The accounting period the batch belongs to.

### Data Type
string

### Position
3

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
DataField::Coco::Subledger Postings::Posting Batch::AccountingPeriodCode

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Batch

### Label
field 3

___

## Create Data Field

### Display Name
FeedPostedTimestamp

### Qualified Name
DataField::Coco::Subledger Postings::Posting Batch::FeedPostedTimestamp

### Description
When the batch was posted to the ledger.

### Data Type
date

### Position
4

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
DataField::Coco::Subledger Postings::Posting Batch::FeedPostedTimestamp

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Batch

### Label
field 4

___

## Create Data Field

### Display Name
FeedLineCount

### Qualified Name
DataField::Coco::Subledger Postings::Posting Batch::FeedLineCount

### Description
The number of postings in the batch.

### Data Type
int

### Position
5

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
DataField::Coco::Subledger Postings::Posting Batch::FeedLineCount

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Batch

### Label
field 5

___

## Create Data Field

### Display Name
FeedTotalAmount

### Qualified Name
DataField::Coco::Subledger Postings::Posting Batch::FeedTotalAmount

### Description
The control total of the batch.

### Data Type
bigdecimal

### Position
6

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
DataField::Coco::Subledger Postings::Posting Batch::FeedTotalAmount

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Batch

### Label
field 6

___

## Create Data Field

### Display Name
FeedCurrentStatus

### Qualified Name
DataField::Coco::Subledger Postings::Posting Batch::FeedCurrentStatus

### Description
Whether the batch is pending, posted or rejected.

### Data Type
string

### Position
7

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
DataField::Coco::Subledger Postings::Posting Batch::FeedCurrentStatus

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Batch

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
coco_pharma.subledger_postings

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
FeedIdentifier

### Qualified Name
DataField::Coco::Subledger Postings::Posting Line::FeedIdentifier

### Description
The batch the posting belongs to.

### Data Type
string

### Position
1

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
DataField::Coco::Subledger Postings::Posting Line::FeedIdentifier

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Line

### Label
field 1

___

## Create Data Field

### Display Name
PostingLineNumber

### Qualified Name
DataField::Coco::Subledger Postings::Posting Line::PostingLineNumber

### Description
The position of the posting in the batch.

### Data Type
int

### Position
2

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
DataField::Coco::Subledger Postings::Posting Line::PostingLineNumber

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Line

### Label
field 2

___

## Create Data Field

### Display Name
LedgerAccountCode

### Qualified Name
DataField::Coco::Subledger Postings::Posting Line::LedgerAccountCode

### Description
The account posted to.

### Data Type
string

### Position
3

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
DataField::Coco::Subledger Postings::Posting Line::LedgerAccountCode

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Line

### Label
field 3

___

## Create Data Field

### Display Name
LegalEntityCode

### Qualified Name
DataField::Coco::Subledger Postings::Posting Line::LegalEntityCode

### Description
The legal entity the posting belongs to.

### Data Type
string

### Position
4

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
DataField::Coco::Subledger Postings::Posting Line::LegalEntityCode

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Line

### Label
field 4

___

## Create Data Field

### Display Name
TransactionIdentifier

### Qualified Name
DataField::Coco::Subledger Postings::Posting Line::TransactionIdentifier

### Description
The source transaction the posting represents.

### Data Type
string

### Position
5

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
DataField::Coco::Subledger Postings::Posting Line::TransactionIdentifier

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Line

### Label
field 5

___

## Create Data Field

### Display Name
PostingAmount

### Qualified Name
DataField::Coco::Subledger Postings::Posting Line::PostingAmount

### Description
The amount posted.

### Data Type
bigdecimal

### Position
6

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
DataField::Coco::Subledger Postings::Posting Line::PostingAmount

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Line

### Label
field 6

___

## Create Data Field

### Display Name
PostingCurrencyCode

### Qualified Name
DataField::Coco::Subledger Postings::Posting Line::PostingCurrencyCode

### Description
The currency of the amount.

### Data Type
string

### Position
7

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
DataField::Coco::Subledger Postings::Posting Line::PostingCurrencyCode

### Data Structure
DataStructure::Coco::Subledger Postings::Posting Line

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: subledger_postings
- schemaDescription: The transactions carried from the operational systems into the general ledger, batched per source feed and accounting period. Each feed is a place where a transaction can be dropped, duplicated or posted to the wrong period, so completeness is asserted per feed rather than in aggregate.

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
coco_pharma.manual_journal_approvals

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
JournalEntryIdentifier

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Entry::JournalEntryIdentifier

### Description
The unique identifier of the entry.

### Data Type
string

### Position
1

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
DataField::Coco::Manual Journal Approvals::Journal Entry::JournalEntryIdentifier

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Entry

### Label
field 1

___

## Create Data Field

### Display Name
AccountingPeriodCode

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Entry::AccountingPeriodCode

### Description
The period the entry adjusts.

### Data Type
string

### Position
2

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
DataField::Coco::Manual Journal Approvals::Journal Entry::AccountingPeriodCode

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Entry

### Label
field 2

___

## Create Data Field

### Display Name
LegalEntityCode

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Entry::LegalEntityCode

### Description
The entity the entry belongs to.

### Data Type
string

### Position
3

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
DataField::Coco::Manual Journal Approvals::Journal Entry::LegalEntityCode

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Entry

### Label
field 3

___

## Create Data Field

### Display Name
JournalEntryAmount

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Entry::JournalEntryAmount

### Description
The value of the adjustment.

### Data Type
bigdecimal

### Position
4

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
DataField::Coco::Manual Journal Approvals::Journal Entry::JournalEntryAmount

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Entry

### Label
field 4

___

## Create Data Field

### Display Name
JournalEntryDescription

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Entry::JournalEntryDescription

### Description
The reason for the adjustment.

### Data Type
string

### Position
5

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
DataField::Coco::Manual Journal Approvals::Journal Entry::JournalEntryDescription

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Entry

### Label
field 5

___

## Create Data Field

### Display Name
JournalEntryPreparerIdentifier

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Entry::JournalEntryPreparerIdentifier

### Description
The person who prepared the entry.

### Data Type
string

### Position
6

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
DataField::Coco::Manual Journal Approvals::Journal Entry::JournalEntryPreparerIdentifier

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Entry

### Label
field 6

___

## Create Data Field

### Display Name
JournalEntrySubmittedTimestamp

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Entry::JournalEntrySubmittedTimestamp

### Description
When the entry was submitted for review.

### Data Type
date

### Position
7

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
DataField::Coco::Manual Journal Approvals::Journal Entry::JournalEntrySubmittedTimestamp

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Entry

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
coco_pharma.manual_journal_approvals

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
JournalEntryIdentifier

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Approval::JournalEntryIdentifier

### Description
The entry reviewed.

### Data Type
string

### Position
1

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
DataField::Coco::Manual Journal Approvals::Journal Approval::JournalEntryIdentifier

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Approval

### Label
field 1

___

## Create Data Field

### Display Name
JournalEntryApproverIdentifier

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Approval::JournalEntryApproverIdentifier

### Description
The reviewer.

### Data Type
string

### Position
2

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
DataField::Coco::Manual Journal Approvals::Journal Approval::JournalEntryApproverIdentifier

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Approval

### Label
field 2

___

## Create Data Field

### Display Name
JournalEntryApprovalStatus

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Approval::JournalEntryApprovalStatus

### Description
Approved, rejected or returned for change.

### Data Type
string

### Position
3

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
DataField::Coco::Manual Journal Approvals::Journal Approval::JournalEntryApprovalStatus

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Approval

### Label
field 3

___

## Create Data Field

### Display Name
JournalEntryApprovalTimestamp

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Approval::JournalEntryApprovalTimestamp

### Description
When the decision was taken.

### Data Type
date

### Position
4

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
DataField::Coco::Manual Journal Approvals::Journal Approval::JournalEntryApprovalTimestamp

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Approval

### Label
field 4

___

## Create Data Field

### Display Name
JournalEntryApprovalNotes

### Qualified Name
DataField::Coco::Manual Journal Approvals::Journal Approval::JournalEntryApprovalNotes

### Description
The reviewer's comments.

### Data Type
string

### Position
5

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
DataField::Coco::Manual Journal Approvals::Journal Approval::JournalEntryApprovalNotes

### Data Structure
DataStructure::Coco::Manual Journal Approvals::Journal Approval

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: manual_journal_approvals
- schemaDescription: Manual journal entries above the materiality threshold, together with the review and approval each received before it was posted. Manual adjustment is the segment of the close least covered by system controls and most able to change a reported figure.

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
coco_pharma.consolidated_group_results

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
LegalEntityCode

### Qualified Name
DataField::Coco::Consolidated Group Results::Entity Trial Balance::LegalEntityCode

### Description
The legal entity.

### Data Type
string

### Position
1

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
DataField::Coco::Consolidated Group Results::Entity Trial Balance::LegalEntityCode

### Data Structure
DataStructure::Coco::Consolidated Group Results::Entity Trial Balance

### Label
field 1

___

## Create Data Field

### Display Name
AccountingPeriodCode

### Qualified Name
DataField::Coco::Consolidated Group Results::Entity Trial Balance::AccountingPeriodCode

### Description
The period.

### Data Type
string

### Position
2

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
DataField::Coco::Consolidated Group Results::Entity Trial Balance::AccountingPeriodCode

### Data Structure
DataStructure::Coco::Consolidated Group Results::Entity Trial Balance

### Label
field 2

___

## Create Data Field

### Display Name
LedgerAccountCode

### Qualified Name
DataField::Coco::Consolidated Group Results::Entity Trial Balance::LedgerAccountCode

### Description
The account.

### Data Type
string

### Position
3

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
DataField::Coco::Consolidated Group Results::Entity Trial Balance::LedgerAccountCode

### Data Structure
DataStructure::Coco::Consolidated Group Results::Entity Trial Balance

### Label
field 3

___

## Create Data Field

### Display Name
LedgerAccountBalanceAmount

### Qualified Name
DataField::Coco::Consolidated Group Results::Entity Trial Balance::LedgerAccountBalanceAmount

### Description
The closing balance in the entity's currency.

### Data Type
bigdecimal

### Position
4

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
DataField::Coco::Consolidated Group Results::Entity Trial Balance::LedgerAccountBalanceAmount

### Data Structure
DataStructure::Coco::Consolidated Group Results::Entity Trial Balance

### Label
field 4

___

## Create Data Field

### Display Name
LedgerCurrencyCode

### Qualified Name
DataField::Coco::Consolidated Group Results::Entity Trial Balance::LedgerCurrencyCode

### Description
The entity's reporting currency.

### Data Type
string

### Position
5

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
DataField::Coco::Consolidated Group Results::Entity Trial Balance::LedgerCurrencyCode

### Data Structure
DataStructure::Coco::Consolidated Group Results::Entity Trial Balance

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
coco_pharma.consolidated_group_results

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
ConsolidationAdjustmentIdentifier

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::ConsolidationAdjustmentIdentifier

### Description
The unique identifier of the adjustment.

### Data Type
string

### Position
1

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
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::ConsolidationAdjustmentIdentifier

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidation Adjustment

### Label
field 1

___

## Create Data Field

### Display Name
AccountingPeriodCode

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::AccountingPeriodCode

### Description
The period.

### Data Type
string

### Position
2

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
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::AccountingPeriodCode

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidation Adjustment

### Label
field 2

___

## Create Data Field

### Display Name
ConsolidationAdjustmentType

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::ConsolidationAdjustmentType

### Description
Intercompany elimination, currency translation or other.

### Data Type
string

### Position
3

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
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::ConsolidationAdjustmentType

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidation Adjustment

### Label
field 3

___

## Create Data Field

### Display Name
LegalEntityCode

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::LegalEntityCode

### Description
The entity the adjustment applies to.

### Data Type
string

### Position
4

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
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::LegalEntityCode

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidation Adjustment

### Label
field 4

___

## Create Data Field

### Display Name
LedgerAccountCode

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::LedgerAccountCode

### Description
The account adjusted.

### Data Type
string

### Position
5

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
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::LedgerAccountCode

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidation Adjustment

### Label
field 5

___

## Create Data Field

### Display Name
ConsolidationAdjustmentAmount

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::ConsolidationAdjustmentAmount

### Description
The adjustment in group currency.

### Data Type
bigdecimal

### Position
6

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
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::ConsolidationAdjustmentAmount

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidation Adjustment

### Label
field 6

___

## Create Data Field

### Display Name
ConsolidationAdjustmentDescription

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::ConsolidationAdjustmentDescription

### Description
The basis of the adjustment.

### Data Type
string

### Position
7

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
DataField::Coco::Consolidated Group Results::Consolidation Adjustment::ConsolidationAdjustmentDescription

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidation Adjustment

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
coco_pharma.consolidated_group_results

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
AccountingPeriodCode

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidated Statement Line::AccountingPeriodCode

### Description
The period.

### Data Type
string

### Position
1

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
DataField::Coco::Consolidated Group Results::Consolidated Statement Line::AccountingPeriodCode

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidated Statement Line

### Label
field 1

___

## Create Data Field

### Display Name
StatementLineCode

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidated Statement Line::StatementLineCode

### Description
The statement line.

### Data Type
string

### Position
2

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
DataField::Coco::Consolidated Group Results::Consolidated Statement Line::StatementLineCode

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidated Statement Line

### Label
field 2

___

## Create Data Field

### Display Name
StatementSegmentCode

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidated Statement Line::StatementSegmentCode

### Description
The business segment the line is analysed to.

### Data Type
string

### Position
3

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
DataField::Coco::Consolidated Group Results::Consolidated Statement Line::StatementSegmentCode

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidated Statement Line

### Label
field 3

___

## Create Data Field

### Display Name
StatementLineAmount

### Qualified Name
DataField::Coco::Consolidated Group Results::Consolidated Statement Line::StatementLineAmount

### Description
The consolidated amount in group currency.

### Data Type
bigdecimal

### Position
4

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
DataField::Coco::Consolidated Group Results::Consolidated Statement Line::StatementLineAmount

### Data Structure
DataStructure::Coco::Consolidated Group Results::Consolidated Statement Line

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: consolidated_group_results
- schemaDescription: The trial balances of the US parent and the UK and EU subsidiaries, the intercompany eliminations and currency translations applied to them, and the consolidated statement lines that result. It is where several sets of books become one set of figures.

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
coco_pharma.external_financial_disclosures

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
DisclosureIdentifier

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Statement::DisclosureIdentifier

### Description
The unique identifier of the filing.

### Data Type
string

### Position
1

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
DataField::Coco::External Financial Disclosures::Disclosure Statement::DisclosureIdentifier

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Statement

### Label
field 1

___

## Create Data Field

### Display Name
DisclosureType

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Statement::DisclosureType

### Description
Annual report, quarterly report, transfers of value disclosure or other.

### Data Type
string

### Position
2

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
DataField::Coco::External Financial Disclosures::Disclosure Statement::DisclosureType

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Statement

### Label
field 2

___

## Create Data Field

### Display Name
AccountingPeriodCode

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Statement::AccountingPeriodCode

### Description
The period the filing covers.

### Data Type
string

### Position
3

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
DataField::Coco::External Financial Disclosures::Disclosure Statement::AccountingPeriodCode

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Statement

### Label
field 3

___

## Create Data Field

### Display Name
DisclosureRegulatorCode

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Statement::DisclosureRegulatorCode

### Description
The regulator or body the filing was made to.

### Data Type
string

### Position
4

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
DataField::Coco::External Financial Disclosures::Disclosure Statement::DisclosureRegulatorCode

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Statement

### Label
field 4

___

## Create Data Field

### Display Name
DisclosureFiledTimestamp

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Statement::DisclosureFiledTimestamp

### Description
When the filing was made.

### Data Type
date

### Position
5

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
DataField::Coco::External Financial Disclosures::Disclosure Statement::DisclosureFiledTimestamp

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Statement

### Label
field 5

___

## Create Data Field

### Display Name
DisclosureAcknowledgedFlag

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Statement::DisclosureAcknowledgedFlag

### Description
Whether the regulator has acknowledged receipt.

### Data Type
boolean

### Position
6

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
DataField::Coco::External Financial Disclosures::Disclosure Statement::DisclosureAcknowledgedFlag

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Statement

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
coco_pharma.external_financial_disclosures

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
DisclosureIdentifier

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Line Item::DisclosureIdentifier

### Description
The filing.

### Data Type
string

### Position
1

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
DataField::Coco::External Financial Disclosures::Disclosure Line Item::DisclosureIdentifier

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Line Item

### Label
field 1

___

## Create Data Field

### Display Name
StatementLineCode

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Line Item::StatementLineCode

### Description
The statement line the figure reports.

### Data Type
string

### Position
2

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
DataField::Coco::External Financial Disclosures::Disclosure Line Item::StatementLineCode

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Line Item

### Label
field 2

___

## Create Data Field

### Display Name
DisclosureLineAmount

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Line Item::DisclosureLineAmount

### Description
The figure disclosed.

### Data Type
bigdecimal

### Position
3

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
DataField::Coco::External Financial Disclosures::Disclosure Line Item::DisclosureLineAmount

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Line Item

### Label
field 3

___

## Create Data Field

### Display Name
ConsolidationAdjustmentIdentifier

### Qualified Name
DataField::Coco::External Financial Disclosures::Disclosure Line Item::ConsolidationAdjustmentIdentifier

### Description
The consolidation adjustment the figure depends on, if any.

### Data Type
string

### Position
4

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
DataField::Coco::External Financial Disclosures::Disclosure Line Item::ConsolidationAdjustmentIdentifier

### Data Structure
DataStructure::Coco::External Financial Disclosures::Disclosure Line Item

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: external_financial_disclosures
- schemaDescription: The statements filed with regulators and published to the market, and the disclosures of transfers of value to healthcare professionals. Every figure must be resolvable back through the consolidation and the ledger to the transactions it was built from.

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
coco_pharma.financial_controls_evidence

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
ControlIdentifier

### Qualified Name
DataField::Coco::Financial Controls Evidence::Control Test Evidence::ControlIdentifier

### Description
The control tested.

### Data Type
string

### Position
1

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
DataField::Coco::Financial Controls Evidence::Control Test Evidence::ControlIdentifier

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Control Test Evidence

### Label
field 1

___

## Create Data Field

### Display Name
AccountingPeriodCode

### Qualified Name
DataField::Coco::Financial Controls Evidence::Control Test Evidence::AccountingPeriodCode

### Description
The period the test covers.

### Data Type
string

### Position
2

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
DataField::Coco::Financial Controls Evidence::Control Test Evidence::AccountingPeriodCode

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Control Test Evidence

### Label
field 2

___

## Create Data Field

### Display Name
ControlTestedDate

### Qualified Name
DataField::Coco::Financial Controls Evidence::Control Test Evidence::ControlTestedDate

### Description
When the test was performed.

### Data Type
date

### Position
3

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
DataField::Coco::Financial Controls Evidence::Control Test Evidence::ControlTestedDate

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Control Test Evidence

### Label
field 3

___

## Create Data Field

### Display Name
ControlTesterIdentifier

### Qualified Name
DataField::Coco::Financial Controls Evidence::Control Test Evidence::ControlTesterIdentifier

### Description
Who performed the test.

### Data Type
string

### Position
4

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
DataField::Coco::Financial Controls Evidence::Control Test Evidence::ControlTesterIdentifier

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Control Test Evidence

### Label
field 4

___

## Create Data Field

### Display Name
ControlTestedStatus

### Qualified Name
DataField::Coco::Financial Controls Evidence::Control Test Evidence::ControlTestedStatus

### Description
Whether the control operated effectively.

### Data Type
string

### Position
5

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
DataField::Coco::Financial Controls Evidence::Control Test Evidence::ControlTestedStatus

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Control Test Evidence

### Label
field 5

___

## Create Data Field

### Display Name
ControlEvidenceIdentifier

### Qualified Name
DataField::Coco::Financial Controls Evidence::Control Test Evidence::ControlEvidenceIdentifier

### Description
The document holding the evidence.

### Data Type
string

### Position
6

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
DataField::Coco::Financial Controls Evidence::Control Test Evidence::ControlEvidenceIdentifier

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Control Test Evidence

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
coco_pharma.financial_controls_evidence

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
AccountingPeriodCode

### Qualified Name
DataField::Coco::Financial Controls Evidence::Close Checklist Item::AccountingPeriodCode

### Description
The period closed.

### Data Type
string

### Position
1

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
DataField::Coco::Financial Controls Evidence::Close Checklist Item::AccountingPeriodCode

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Close Checklist Item

### Label
field 1

___

## Create Data Field

### Display Name
CloseChecklistItemCode

### Qualified Name
DataField::Coco::Financial Controls Evidence::Close Checklist Item::CloseChecklistItemCode

### Description
The step.

### Data Type
string

### Position
2

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
DataField::Coco::Financial Controls Evidence::Close Checklist Item::CloseChecklistItemCode

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Close Checklist Item

### Label
field 2

___

## Create Data Field

### Display Name
CloseChecklistItemCompletedTimestamp

### Qualified Name
DataField::Coco::Financial Controls Evidence::Close Checklist Item::CloseChecklistItemCompletedTimestamp

### Description
When the step was completed.

### Data Type
date

### Position
3

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
DataField::Coco::Financial Controls Evidence::Close Checklist Item::CloseChecklistItemCompletedTimestamp

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Close Checklist Item

### Label
field 3

___

## Create Data Field

### Display Name
CloseChecklistItemApproverIdentifier

### Qualified Name
DataField::Coco::Financial Controls Evidence::Close Checklist Item::CloseChecklistItemApproverIdentifier

### Description
Who approved completion.

### Data Type
string

### Position
4

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
DataField::Coco::Financial Controls Evidence::Close Checklist Item::CloseChecklistItemApproverIdentifier

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Close Checklist Item

### Label
field 4

___

## Create Data Field

### Display Name
CloseChecklistItemStatus

### Qualified Name
DataField::Coco::Financial Controls Evidence::Close Checklist Item::CloseChecklistItemStatus

### Description
Not started, complete or approved.

### Data Type
string

### Position
5

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
DataField::Coco::Financial Controls Evidence::Close Checklist Item::CloseChecklistItemStatus

### Data Structure
DataStructure::Coco::Financial Controls Evidence::Close Checklist Item

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: financial_controls_evidence
- schemaDescription: The documentation and test evidence for the internal controls over financial reporting, and the reconciliations, approvals and checklist items produced by each close. The controls it evidences are controls over the close itself, so the repository is part of the chain rather than an audit of it.

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
coco_pharma.supplier_payment_detail_changes

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
PaymentDetailChangeIdentifier

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::PaymentDetailChangeIdentifier

### Description
The unique identifier of the change request.

### Data Type
string

### Position
1

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
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::PaymentDetailChangeIdentifier

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Payment Detail Change

### Label
field 1

___

## Create Data Field

### Display Name
SupplierIdentifier

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::SupplierIdentifier

### Description
The supplier.

### Data Type
string

### Position
2

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
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::SupplierIdentifier

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Payment Detail Change

### Label
field 2

___

## Create Data Field

### Display Name
PaymentDetailChangeRequestedTimestamp

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::PaymentDetailChangeRequestedTimestamp

### Description
When the change was requested.

### Data Type
date

### Position
3

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
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::PaymentDetailChangeRequestedTimestamp

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Payment Detail Change

### Label
field 3

___

## Create Data Field

### Display Name
PaymentDetailChangeRequesterIdentifier

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::PaymentDetailChangeRequesterIdentifier

### Description
Who requested it.

### Data Type
string

### Position
4

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
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::PaymentDetailChangeRequesterIdentifier

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Payment Detail Change

### Label
field 4

___

## Create Data Field

### Display Name
BankAccountPreviousIdentifier

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::BankAccountPreviousIdentifier

### Description
The bank account before the change, masked.

### Data Type
string

### Position
5

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
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::BankAccountPreviousIdentifier

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Payment Detail Change

### Label
field 5

___

## Create Data Field

### Display Name
BankAccountCurrentIdentifier

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::BankAccountCurrentIdentifier

### Description
The bank account after the change, masked.

### Data Type
string

### Position
6

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
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::BankAccountCurrentIdentifier

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Payment Detail Change

### Label
field 6

___

## Create Data Field

### Display Name
PaymentDetailChangeStatus

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::PaymentDetailChangeStatus

### Description
Pending verification, verified, rejected.

### Data Type
string

### Position
7

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
DataField::Coco::Supplier Payment Detail Changes::Payment Detail Change::PaymentDetailChangeStatus

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Payment Detail Change

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
coco_pharma.supplier_payment_detail_changes

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
PaymentDetailChangeIdentifier

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::PaymentDetailChangeIdentifier

### Description
The change verified.

### Data Type
string

### Position
1

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
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::PaymentDetailChangeIdentifier

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Verification Evidence

### Label
field 1

___

## Create Data Field

### Display Name
PaymentDetailChangeVerifierIdentifier

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::PaymentDetailChangeVerifierIdentifier

### Description
Who carried out the verification.

### Data Type
string

### Position
2

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
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::PaymentDetailChangeVerifierIdentifier

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Verification Evidence

### Label
field 2

___

## Create Data Field

### Display Name
PaymentDetailChangeChannelType

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::PaymentDetailChangeChannelType

### Description
The channel used, for example call-back to a known number.

### Data Type
string

### Position
3

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
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::PaymentDetailChangeChannelType

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Verification Evidence

### Label
field 3

___

## Create Data Field

### Display Name
PaymentDetailChangeVerifiedTimestamp

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::PaymentDetailChangeVerifiedTimestamp

### Description
When the verification was completed.

### Data Type
date

### Position
4

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
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::PaymentDetailChangeVerifiedTimestamp

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Verification Evidence

### Label
field 4

___

## Create Data Field

### Display Name
PaymentDetailChangeVerifiedNotes

### Qualified Name
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::PaymentDetailChangeVerifiedNotes

### Description
What was confirmed and with whom.

### Data Type
string

### Position
5

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
DataField::Coco::Supplier Payment Detail Changes::Verification Evidence::PaymentDetailChangeVerifiedNotes

### Data Structure
DataStructure::Coco::Supplier Payment Detail Changes::Verification Evidence

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: supplier_payment_detail_changes
- schemaDescription: Every change to a supplier's bank details, treated as a controlled event with independent verification rather than as routine maintenance. This is where the payment flow has historically been attacked.

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
coco_pharma.supplier_payments

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
InvoiceNumber

### Qualified Name
DataField::Coco::Supplier Payments::Invoice Match::InvoiceNumber

### Description
The supplier's invoice number.

### Data Type
string

### Position
1

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
DataField::Coco::Supplier Payments::Invoice Match::InvoiceNumber

### Data Structure
DataStructure::Coco::Supplier Payments::Invoice Match

### Label
field 1

___

## Create Data Field

### Display Name
SupplierIdentifier

### Qualified Name
DataField::Coco::Supplier Payments::Invoice Match::SupplierIdentifier

### Description
The supplier.

### Data Type
string

### Position
2

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
DataField::Coco::Supplier Payments::Invoice Match::SupplierIdentifier

### Data Structure
DataStructure::Coco::Supplier Payments::Invoice Match

### Label
field 2

___

## Create Data Field

### Display Name
OrderIdentifier

### Qualified Name
DataField::Coco::Supplier Payments::Invoice Match::OrderIdentifier

### Description
The purchase order matched.

### Data Type
string

### Position
3

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
DataField::Coco::Supplier Payments::Invoice Match::OrderIdentifier

### Data Structure
DataStructure::Coco::Supplier Payments::Invoice Match

### Label
field 3

___

## Create Data Field

### Display Name
GoodsReceiptIdentifier

### Qualified Name
DataField::Coco::Supplier Payments::Invoice Match::GoodsReceiptIdentifier

### Description
The goods receipt matched.

### Data Type
string

### Position
4

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
DataField::Coco::Supplier Payments::Invoice Match::GoodsReceiptIdentifier

### Data Structure
DataStructure::Coco::Supplier Payments::Invoice Match

### Label
field 4

___

## Create Data Field

### Display Name
InvoiceTotalAmount

### Qualified Name
DataField::Coco::Supplier Payments::Invoice Match::InvoiceTotalAmount

### Description
The invoiced amount.

### Data Type
bigdecimal

### Position
5

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
DataField::Coco::Supplier Payments::Invoice Match::InvoiceTotalAmount

### Data Structure
DataStructure::Coco::Supplier Payments::Invoice Match

### Label
field 5

___

## Create Data Field

### Display Name
InvoiceCurrencyCode

### Qualified Name
DataField::Coco::Supplier Payments::Invoice Match::InvoiceCurrencyCode

### Description
The currency.

### Data Type
string

### Position
6

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
DataField::Coco::Supplier Payments::Invoice Match::InvoiceCurrencyCode

### Data Structure
DataStructure::Coco::Supplier Payments::Invoice Match

### Label
field 6

___

## Create Data Field

### Display Name
InvoiceMatchStatus

### Qualified Name
DataField::Coco::Supplier Payments::Invoice Match::InvoiceMatchStatus

### Description
Matched, variance or unmatched.

### Data Type
string

### Position
7

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
DataField::Coco::Supplier Payments::Invoice Match::InvoiceMatchStatus

### Data Structure
DataStructure::Coco::Supplier Payments::Invoice Match

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
coco_pharma.supplier_payments

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
PaymentIdentifier

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::PaymentIdentifier

### Description
The unique identifier of the payment.

### Data Type
string

### Position
1

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
DataField::Coco::Supplier Payments::Payment Instruction::PaymentIdentifier

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

### Label
field 1

___

## Create Data Field

### Display Name
SupplierIdentifier

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::SupplierIdentifier

### Description
The payee.

### Data Type
string

### Position
2

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
DataField::Coco::Supplier Payments::Payment Instruction::SupplierIdentifier

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

### Label
field 2

___

## Create Data Field

### Display Name
InvoiceNumber

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::InvoiceNumber

### Description
The invoice settled.

### Data Type
string

### Position
3

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
DataField::Coco::Supplier Payments::Payment Instruction::InvoiceNumber

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

### Label
field 3

___

## Create Data Field

### Display Name
PaymentAmount

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::PaymentAmount

### Description
The amount paid.

### Data Type
bigdecimal

### Position
4

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
DataField::Coco::Supplier Payments::Payment Instruction::PaymentAmount

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

### Label
field 4

___

## Create Data Field

### Display Name
PaymentCurrencyCode

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::PaymentCurrencyCode

### Description
The currency.

### Data Type
string

### Position
5

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
DataField::Coco::Supplier Payments::Payment Instruction::PaymentCurrencyCode

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

### Label
field 5

___

## Create Data Field

### Display Name
PaymentAuthoriserIdentifier

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::PaymentAuthoriserIdentifier

### Description
Who authorised the payment.

### Data Type
string

### Position
6

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
DataField::Coco::Supplier Payments::Payment Instruction::PaymentAuthoriserIdentifier

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

### Label
field 6

___

## Create Data Field

### Display Name
PaymentAuthorisedTimestamp

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::PaymentAuthorisedTimestamp

### Description
When it was authorised.

### Data Type
date

### Position
7

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
DataField::Coco::Supplier Payments::Payment Instruction::PaymentAuthorisedTimestamp

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

### Label
field 7

___

## Create Data Field

### Display Name
SupplierScreenedStatus

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::SupplierScreenedStatus

### Description
The supplier's screening status at authorisation.

### Data Type
string

### Position
8

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
DataField::Coco::Supplier Payments::Payment Instruction::SupplierScreenedStatus

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

### Label
field 8

___

## Create Data Field

### Display Name
BankAccountCurrentIdentifier

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::BankAccountCurrentIdentifier

### Description
The account paid, masked.

### Data Type
string

### Position
9

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
DataField::Coco::Supplier Payments::Payment Instruction::BankAccountCurrentIdentifier

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

### Label
field 9

___

## Create Data Field

### Display Name
LedgerAccountCode

### Qualified Name
DataField::Coco::Supplier Payments::Payment Instruction::LedgerAccountCode

### Description
The cost coding of the payment.

### Data Type
string

### Position
10

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
DataField::Coco::Supplier Payments::Payment Instruction::LedgerAccountCode

### Data Structure
DataStructure::Coco::Supplier Payments::Payment Instruction

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: supplier_payments
- schemaDescription: Supplier invoices matched to purchase orders and goods receipts, the payment authorisations that followed, and the instructions sent to the bank. Screening status and payment details are read at the moment of authorisation, the only moment at which either of them protects anything.

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
coco_pharma.payment_anomaly_findings

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
AnomalyIdentifier

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::AnomalyIdentifier

### Description
The unique identifier of the finding.

### Data Type
string

### Position
1

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
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::AnomalyIdentifier

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Anomaly Finding

### Label
field 1

___

## Create Data Field

### Display Name
AnomalyDetectedTimestamp

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::AnomalyDetectedTimestamp

### Description
When it was detected.

### Data Type
date

### Position
2

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
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::AnomalyDetectedTimestamp

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Anomaly Finding

### Label
field 2

___

## Create Data Field

### Display Name
AnomalyType

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::AnomalyType

### Description
Duplicate payment, split payment, new-supplier spike, claim pattern or other.

### Data Type
string

### Position
3

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
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::AnomalyType

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Anomaly Finding

### Label
field 3

___

## Create Data Field

### Display Name
SupplierIdentifier

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::SupplierIdentifier

### Description
The supplier implicated, if any.

### Data Type
string

### Position
4

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
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::SupplierIdentifier

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Anomaly Finding

### Label
field 4

___

## Create Data Field

### Display Name
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::WorkerPseudonymIdentifier

### Description
The claimant implicated, if any.

### Data Type
string

### Position
5

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
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Anomaly Finding

### Label
field 5

___

## Create Data Field

### Display Name
AnomalyDescription

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::AnomalyDescription

### Description
What was observed.

### Data Type
string

### Position
6

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
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::AnomalyDescription

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Anomaly Finding

### Label
field 6

___

## Create Data Field

### Display Name
AnomalySeverity

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::AnomalySeverity

### Description
The assessed seriousness.

### Data Type
string

### Position
7

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
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::AnomalySeverity

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Anomaly Finding

### Label
field 7

___

## Create Data Field

### Display Name
AnomalyCurrentStatus

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::AnomalyCurrentStatus

### Description
Open, under investigation, closed as false positive, confirmed.

### Data Type
string

### Position
8

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
DataField::Coco::Payment Anomaly Findings::Anomaly Finding::AnomalyCurrentStatus

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Anomaly Finding

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
coco_pharma.payment_anomaly_findings

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
AnomalyIdentifier

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::AnomalyIdentifier

### Description
The finding.

### Data Type
string

### Position
1

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
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::AnomalyIdentifier

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Monitored Transaction

### Label
field 1

___

## Create Data Field

### Display Name
TransactionIdentifier

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::TransactionIdentifier

### Description
The payment or claim.

### Data Type
string

### Position
2

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
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::TransactionIdentifier

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Monitored Transaction

### Label
field 2

___

## Create Data Field

### Display Name
TransactionType

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::TransactionType

### Description
Supplier payment or expense claim.

### Data Type
string

### Position
3

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
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::TransactionType

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Monitored Transaction

### Label
field 3

___

## Create Data Field

### Display Name
TransactionAmount

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::TransactionAmount

### Description
Its amount.

### Data Type
bigdecimal

### Position
4

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
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::TransactionAmount

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Monitored Transaction

### Label
field 4

___

## Create Data Field

### Display Name
TransactionDate

### Qualified Name
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::TransactionDate

### Description
Its date.

### Data Type
date

### Position
5

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
DataField::Coco::Payment Anomaly Findings::Monitored Transaction::TransactionDate

### Data Structure
DataStructure::Coco::Payment Anomaly Findings::Monitored Transaction

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: payment_anomaly_findings
- schemaDescription: The patterns found across supplier payments and expense claims that no single transaction shows: duplicate payments, unusual supplier behaviour, and the concerns raised as a result. The fraud that motivated this chain was visible only across the whole flow.

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
coco_pharma.transfers_of_value

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
TransferOfValueIdentifier

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::TransferOfValueIdentifier

### Description
The unique identifier of the transfer.

### Data Type
string

### Position
1

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
DataField::Coco::Transfers Of Value::Transfer Of Value::TransferOfValueIdentifier

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Label
field 1

___

## Create Data Field

### Display Name
TransferOfValueRecipientIdentifier

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::TransferOfValueRecipientIdentifier

### Description
The healthcare professional or organisation.

### Data Type
string

### Position
2

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
DataField::Coco::Transfers Of Value::Transfer Of Value::TransferOfValueRecipientIdentifier

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Label
field 2

___

## Create Data Field

### Display Name
TransferOfValueRecipientType

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::TransferOfValueRecipientType

### Description
Individual professional or organisation.

### Data Type
string

### Position
3

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
DataField::Coco::Transfers Of Value::Transfer Of Value::TransferOfValueRecipientType

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Label
field 3

___

## Create Data Field

### Display Name
TransferOfValueType

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::TransferOfValueType

### Description
Fee, hospitality, travel, grant or other.

### Data Type
string

### Position
4

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
DataField::Coco::Transfers Of Value::Transfer Of Value::TransferOfValueType

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Label
field 4

___

## Create Data Field

### Display Name
TransferOfValueDescription

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::TransferOfValueDescription

### Description
The purpose of the transfer.

### Data Type
string

### Position
5

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
DataField::Coco::Transfers Of Value::Transfer Of Value::TransferOfValueDescription

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Label
field 5

___

## Create Data Field

### Display Name
TransferOfValueAmount

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::TransferOfValueAmount

### Description
The value transferred.

### Data Type
bigdecimal

### Position
6

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
DataField::Coco::Transfers Of Value::Transfer Of Value::TransferOfValueAmount

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Label
field 6

___

## Create Data Field

### Display Name
TransferOfValueCurrencyCode

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::TransferOfValueCurrencyCode

### Description
The currency.

### Data Type
string

### Position
7

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
DataField::Coco::Transfers Of Value::Transfer Of Value::TransferOfValueCurrencyCode

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Label
field 7

___

## Create Data Field

### Display Name
TransferOfValueDate

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::TransferOfValueDate

### Description
When it was provided.

### Data Type
date

### Position
8

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
DataField::Coco::Transfers Of Value::Transfer Of Value::TransferOfValueDate

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Label
field 8

___

## Create Data Field

### Display Name
TransactionIdentifier

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::TransactionIdentifier

### Description
The payment or expense claim it originated from.

### Data Type
string

### Position
9

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
DataField::Coco::Transfers Of Value::Transfer Of Value::TransactionIdentifier

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

### Label
field 9

___

## Create Data Field

### Display Name
TransferOfValueDisclosedFlag

### Qualified Name
DataField::Coco::Transfers Of Value::Transfer Of Value::TransferOfValueDisclosedFlag

### Description
Whether it has been included in a disclosure.

### Data Type
boolean

### Position
10

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
DataField::Coco::Transfers Of Value::Transfer Of Value::TransferOfValueDisclosedFlag

### Data Structure
DataStructure::Coco::Transfers Of Value::Transfer Of Value

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: transfers_of_value
- schemaDescription: Payments and benefits provided to healthcare professionals and organisations, from whichever flow they originate, identified and recorded so that they can be disclosed. Reconstructing this afterwards from a general ledger is the failure it exists to prevent.

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
coco_pharma.expense_approvals

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
ClaimIdentifier

### Qualified Name
DataField::Coco::Expense Approvals::Expense Claim::ClaimIdentifier

### Description
The unique identifier of the claim.

### Data Type
string

### Position
1

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
DataField::Coco::Expense Approvals::Expense Claim::ClaimIdentifier

### Data Structure
DataStructure::Coco::Expense Approvals::Expense Claim

### Label
field 1

___

## Create Data Field

### Display Name
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Expense Approvals::Expense Claim::WorkerPseudonymIdentifier

### Description
The claimant.

### Data Type
string

### Position
2

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
DataField::Coco::Expense Approvals::Expense Claim::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Expense Approvals::Expense Claim

### Label
field 2

___

## Create Data Field

### Display Name
ClaimSubmittedTimestamp

### Qualified Name
DataField::Coco::Expense Approvals::Expense Claim::ClaimSubmittedTimestamp

### Description
When it was submitted.

### Data Type
date

### Position
3

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
DataField::Coco::Expense Approvals::Expense Claim::ClaimSubmittedTimestamp

### Data Structure
DataStructure::Coco::Expense Approvals::Expense Claim

### Label
field 3

___

## Create Data Field

### Display Name
ClaimTotalAmount

### Qualified Name
DataField::Coco::Expense Approvals::Expense Claim::ClaimTotalAmount

### Description
The value claimed.

### Data Type
bigdecimal

### Position
4

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
DataField::Coco::Expense Approvals::Expense Claim::ClaimTotalAmount

### Data Structure
DataStructure::Coco::Expense Approvals::Expense Claim

### Label
field 4

___

## Create Data Field

### Display Name
ClaimCurrencyCode

### Qualified Name
DataField::Coco::Expense Approvals::Expense Claim::ClaimCurrencyCode

### Description
The currency.

### Data Type
string

### Position
5

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
DataField::Coco::Expense Approvals::Expense Claim::ClaimCurrencyCode

### Data Structure
DataStructure::Coco::Expense Approvals::Expense Claim

### Label
field 5

___

## Create Data Field

### Display Name
LedgerAccountCode

### Qualified Name
DataField::Coco::Expense Approvals::Expense Claim::LedgerAccountCode

### Description
The cost coding.

### Data Type
string

### Position
6

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
DataField::Coco::Expense Approvals::Expense Claim::LedgerAccountCode

### Data Structure
DataStructure::Coco::Expense Approvals::Expense Claim

### Label
field 6

___

## Create Data Field

### Display Name
ClaimApproverIdentifier

### Qualified Name
DataField::Coco::Expense Approvals::Expense Claim::ClaimApproverIdentifier

### Description
The approver it was routed to.

### Data Type
string

### Position
7

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
DataField::Coco::Expense Approvals::Expense Claim::ClaimApproverIdentifier

### Data Structure
DataStructure::Coco::Expense Approvals::Expense Claim

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
coco_pharma.expense_approvals

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
ClaimIdentifier

### Qualified Name
DataField::Coco::Expense Approvals::Approval Decision::ClaimIdentifier

### Description
The claim.

### Data Type
string

### Position
1

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
DataField::Coco::Expense Approvals::Approval Decision::ClaimIdentifier

### Data Structure
DataStructure::Coco::Expense Approvals::Approval Decision

### Label
field 1

___

## Create Data Field

### Display Name
ClaimApproverIdentifier

### Qualified Name
DataField::Coco::Expense Approvals::Approval Decision::ClaimApproverIdentifier

### Description
Who decided.

### Data Type
string

### Position
2

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
DataField::Coco::Expense Approvals::Approval Decision::ClaimApproverIdentifier

### Data Structure
DataStructure::Coco::Expense Approvals::Approval Decision

### Label
field 2

___

## Create Data Field

### Display Name
ClaimApprovalStatus

### Qualified Name
DataField::Coco::Expense Approvals::Approval Decision::ClaimApprovalStatus

### Description
Approved, rejected or returned.

### Data Type
string

### Position
3

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
DataField::Coco::Expense Approvals::Approval Decision::ClaimApprovalStatus

### Data Structure
DataStructure::Coco::Expense Approvals::Approval Decision

### Label
field 3

___

## Create Data Field

### Display Name
ClaimApprovalTimestamp

### Qualified Name
DataField::Coco::Expense Approvals::Approval Decision::ClaimApprovalTimestamp

### Description
When.

### Data Type
date

### Position
4

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
DataField::Coco::Expense Approvals::Approval Decision::ClaimApprovalTimestamp

### Data Structure
DataStructure::Coco::Expense Approvals::Approval Decision

### Label
field 4

___

## Create Data Field

### Display Name
ClaimApprovalNotes

### Qualified Name
DataField::Coco::Expense Approvals::Approval Decision::ClaimApprovalNotes

### Description
The approver's comments.

### Data Type
string

### Position
5

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
DataField::Coco::Expense Approvals::Approval Decision::ClaimApprovalNotes

### Data Structure
DataStructure::Coco::Expense Approvals::Approval Decision

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: expense_approvals
- schemaDescription: Expense claims routed for approval, the approver each was sent to and the decision taken, carried forward to payment. The approval is only worth anything if it is still attached to the claim when the payment is made.

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
coco_pharma.general_ledger_balances

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
TransactionIdentifier

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Transaction::TransactionIdentifier

### Description
The unique identifier of the ledger transaction.

### Data Type
string

### Position
1

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
DataField::Coco::General Ledger Balances::Ledger Transaction::TransactionIdentifier

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Transaction

### Label
field 1

___

## Create Data Field

### Display Name
LegalEntityCode

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Transaction::LegalEntityCode

### Description
The entity.

### Data Type
string

### Position
2

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
DataField::Coco::General Ledger Balances::Ledger Transaction::LegalEntityCode

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Transaction

### Label
field 2

___

## Create Data Field

### Display Name
AccountingPeriodCode

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Transaction::AccountingPeriodCode

### Description
The period.

### Data Type
string

### Position
3

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
DataField::Coco::General Ledger Balances::Ledger Transaction::AccountingPeriodCode

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Transaction

### Label
field 3

___

## Create Data Field

### Display Name
LedgerAccountCode

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Transaction::LedgerAccountCode

### Description
The account.

### Data Type
string

### Position
4

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
DataField::Coco::General Ledger Balances::Ledger Transaction::LedgerAccountCode

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Transaction

### Label
field 4

___

## Create Data Field

### Display Name
TransactionAmount

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Transaction::TransactionAmount

### Description
The amount.

### Data Type
bigdecimal

### Position
5

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
DataField::Coco::General Ledger Balances::Ledger Transaction::TransactionAmount

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Transaction

### Label
field 5

___

## Create Data Field

### Display Name
TransactionCurrencyCode

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Transaction::TransactionCurrencyCode

### Description
The currency.

### Data Type
string

### Position
6

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
DataField::Coco::General Ledger Balances::Ledger Transaction::TransactionCurrencyCode

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Transaction

### Label
field 6

___

## Create Data Field

### Display Name
TransactionPostedTimestamp

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Transaction::TransactionPostedTimestamp

### Description
When posted.

### Data Type
date

### Position
7

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
DataField::Coco::General Ledger Balances::Ledger Transaction::TransactionPostedTimestamp

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Transaction

### Label
field 7

___

## Create Data Field

### Display Name
FeedIdentifier

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Transaction::FeedIdentifier

### Description
The feed batch it arrived in, if from a feed.

### Data Type
string

### Position
8

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
DataField::Coco::General Ledger Balances::Ledger Transaction::FeedIdentifier

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Transaction

### Label
field 8

___

## Create Data Field

### Display Name
JournalEntryIdentifier

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Transaction::JournalEntryIdentifier

### Description
The manual journal it arrived in, if manual.

### Data Type
string

### Position
9

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
DataField::Coco::General Ledger Balances::Ledger Transaction::JournalEntryIdentifier

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Transaction

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
coco_pharma.general_ledger_balances

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
LegalEntityCode

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Account Balance::LegalEntityCode

### Description
The entity.

### Data Type
string

### Position
1

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
DataField::Coco::General Ledger Balances::Ledger Account Balance::LegalEntityCode

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Account Balance

### Label
field 1

___

## Create Data Field

### Display Name
AccountingPeriodCode

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Account Balance::AccountingPeriodCode

### Description
The period.

### Data Type
string

### Position
2

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
DataField::Coco::General Ledger Balances::Ledger Account Balance::AccountingPeriodCode

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Account Balance

### Label
field 2

___

## Create Data Field

### Display Name
LedgerAccountCode

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Account Balance::LedgerAccountCode

### Description
The account.

### Data Type
string

### Position
3

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
DataField::Coco::General Ledger Balances::Ledger Account Balance::LedgerAccountCode

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Account Balance

### Label
field 3

___

## Create Data Field

### Display Name
LedgerAccountName

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Account Balance::LedgerAccountName

### Description
The account's name.

### Data Type
string

### Position
4

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
DataField::Coco::General Ledger Balances::Ledger Account Balance::LedgerAccountName

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Account Balance

### Label
field 4

___

## Create Data Field

### Display Name
LedgerAccountBalanceAmount

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Account Balance::LedgerAccountBalanceAmount

### Description
The closing balance.

### Data Type
bigdecimal

### Position
5

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
DataField::Coco::General Ledger Balances::Ledger Account Balance::LedgerAccountBalanceAmount

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Account Balance

### Label
field 5

___

## Create Data Field

### Display Name
LedgerCurrencyCode

### Qualified Name
DataField::Coco::General Ledger Balances::Ledger Account Balance::LedgerCurrencyCode

### Description
The currency.

### Data Type
string

### Position
6

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
DataField::Coco::General Ledger Balances::Ledger Account Balance::LedgerCurrencyCode

### Data Structure
DataStructure::Coco::General Ledger Balances::Ledger Account Balance

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: general_ledger_balances
- schemaDescription: The general ledger of each legal entity: the transactions posted from every feed, adjustment and payment, and the account balances that result. It is the source of the entity trial balances that consolidation starts from and of the manual entries that review examines.

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
coco_pharma.employee_expense_claims

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
ClaimIdentifier

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Submission::ClaimIdentifier

### Description
The unique identifier of the claim.

### Data Type
string

### Position
1

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
DataField::Coco::Employee Expense Claims::Claim Submission::ClaimIdentifier

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Submission

### Label
field 1

___

## Create Data Field

### Display Name
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Submission::WorkerPseudonymIdentifier

### Description
The claimant.

### Data Type
string

### Position
2

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
DataField::Coco::Employee Expense Claims::Claim Submission::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Submission

### Label
field 2

___

## Create Data Field

### Display Name
ClaimSubmittedTimestamp

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Submission::ClaimSubmittedTimestamp

### Description
When submitted.

### Data Type
date

### Position
3

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
DataField::Coco::Employee Expense Claims::Claim Submission::ClaimSubmittedTimestamp

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Submission

### Label
field 3

___

## Create Data Field

### Display Name
ClaimTotalAmount

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Submission::ClaimTotalAmount

### Description
The total claimed.

### Data Type
bigdecimal

### Position
4

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
DataField::Coco::Employee Expense Claims::Claim Submission::ClaimTotalAmount

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Submission

### Label
field 4

___

## Create Data Field

### Display Name
ClaimCurrencyCode

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Submission::ClaimCurrencyCode

### Description
The currency.

### Data Type
string

### Position
5

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
DataField::Coco::Employee Expense Claims::Claim Submission::ClaimCurrencyCode

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Submission

### Label
field 5

___

## Create Data Field

### Display Name
ClaimCurrentStatus

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Submission::ClaimCurrentStatus

### Description
Draft, submitted, approved, paid or rejected.

### Data Type
string

### Position
6

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
DataField::Coco::Employee Expense Claims::Claim Submission::ClaimCurrentStatus

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Submission

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
coco_pharma.employee_expense_claims

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
ClaimIdentifier

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Line::ClaimIdentifier

### Description
The claim.

### Data Type
string

### Position
1

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
DataField::Coco::Employee Expense Claims::Claim Line::ClaimIdentifier

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Line

### Label
field 1

___

## Create Data Field

### Display Name
ClaimLineNumber

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Line::ClaimLineNumber

### Description
The position of the line in the claim.

### Data Type
int

### Position
2

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
DataField::Coco::Employee Expense Claims::Claim Line::ClaimLineNumber

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Line

### Label
field 2

___

## Create Data Field

### Display Name
ClaimLineType

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Line::ClaimLineType

### Description
Travel, hospitality, accommodation or other.

### Data Type
string

### Position
3

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
DataField::Coco::Employee Expense Claims::Claim Line::ClaimLineType

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Line

### Label
field 3

___

## Create Data Field

### Display Name
ClaimLineDate

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Line::ClaimLineDate

### Description
When the expense was incurred.

### Data Type
date

### Position
4

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
DataField::Coco::Employee Expense Claims::Claim Line::ClaimLineDate

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Line

### Label
field 4

___

## Create Data Field

### Display Name
ClaimLineAmount

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Line::ClaimLineAmount

### Description
The amount.

### Data Type
bigdecimal

### Position
5

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
DataField::Coco::Employee Expense Claims::Claim Line::ClaimLineAmount

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Line

### Label
field 5

___

## Create Data Field

### Display Name
ClaimLineDescription

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Line::ClaimLineDescription

### Description
What the expense was for.

### Data Type
string

### Position
6

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
DataField::Coco::Employee Expense Claims::Claim Line::ClaimLineDescription

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Line

### Label
field 6

___

## Create Data Field

### Display Name
ClaimLineRecipientIdentifier

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Line::ClaimLineRecipientIdentifier

### Description
The healthcare professional entertained, if any.

### Data Type
string

### Position
7

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
DataField::Coco::Employee Expense Claims::Claim Line::ClaimLineRecipientIdentifier

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Line

### Label
field 7

___

## Create Data Field

### Display Name
ClaimLineEvidenceIdentifier

### Qualified Name
DataField::Coco::Employee Expense Claims::Claim Line::ClaimLineEvidenceIdentifier

### Description
The receipt or other evidence attached.

### Data Type
string

### Position
8

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
DataField::Coco::Employee Expense Claims::Claim Line::ClaimLineEvidenceIdentifier

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claim Line

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
coco_pharma.employee_expense_claims

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
WorkerPseudonymIdentifier

### Qualified Name
DataField::Coco::Employee Expense Claims::Claimant Cost Centre::WorkerPseudonymIdentifier

### Description
The worker.

### Data Type
string

### Position
1

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
DataField::Coco::Employee Expense Claims::Claimant Cost Centre::WorkerPseudonymIdentifier

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claimant Cost Centre

### Label
field 1

___

## Create Data Field

### Display Name
CostCentreCode

### Qualified Name
DataField::Coco::Employee Expense Claims::Claimant Cost Centre::CostCentreCode

### Description
The cost centre.

### Data Type
string

### Position
2

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
DataField::Coco::Employee Expense Claims::Claimant Cost Centre::CostCentreCode

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claimant Cost Centre

### Label
field 2

___

## Create Data Field

### Display Name
ClaimApproverIdentifier

### Qualified Name
DataField::Coco::Employee Expense Claims::Claimant Cost Centre::ClaimApproverIdentifier

### Description
The approver for the worker's claims.

### Data Type
string

### Position
3

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
DataField::Coco::Employee Expense Claims::Claimant Cost Centre::ClaimApproverIdentifier

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claimant Cost Centre

### Label
field 3

___

## Create Data Field

### Display Name
ClaimMaximumAmount

### Qualified Name
DataField::Coco::Employee Expense Claims::Claimant Cost Centre::ClaimMaximumAmount

### Description
The spending authority applying to the worker.

### Data Type
bigdecimal

### Position
4

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
DataField::Coco::Employee Expense Claims::Claimant Cost Centre::ClaimMaximumAmount

### Data Structure
DataStructure::Coco::Employee Expense Claims::Claimant Cost Centre

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
- secretsCollectionName: PostgreSQL Server Secret
- secretsStorePathName: secrets/integration.omsecrets
- versionIdentifier: V1.0
- databaseName: coco_pharma
- schemaName: employee_expense_claims
- schemaDescription: The claims employees submit for expenses incurred, line by line with their supporting evidence, and the record of which workers may claim against which cost centres. It is the entry point of the expense payment chain and a source of transfers of value that disclosure must catch.

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
