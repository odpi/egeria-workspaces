# Strategic Supply Chain Components — Candidate System Matches

> **Author:** Erin Overview (Information Architect), Peter Profile (Solution Architect), with Gary Geeke (IT Infrastructure)  
> **Version:** 0.2  
> **Status:** DRAFT  
> **Date:** 2026-09-13  
> **Description:** Candidate `ImplementedBy` matches from the 82 solution components in `strategic-supply-chain-analysis.md` to the systems Coco Pharmaceuticals runs — across three estates, not one.  This is an analysis document, not a Dr.Egeria command file: nothing here is loaded until the matches are confirmed.

---

## Three estates, not one

Version 0.1 of this document matched the components against `CocoComboArchive.omarchive` alone and concluded that the regulated layer of the business — laboratory, quality, batch release, safety, serialisation — had no systems at all.  That conclusion was wrong, and the reason it was wrong is the most important thing in this document.

**The archive is Gary Geeke's spreadsheet, not the estate.** Its 29 `SoftwareServer`s are the servers under Gary's responsibility at each location — the inventory he kept in a spreadsheet before moving it into Egeria in the [cataloguing infrastructure](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/cataloguing-infrastructure/overview/) scenario.  Equipment that departments bought for themselves is explicitly outside it, so it is the integrated surface of the parent company rather than everything the parent runs.  Coco Pharmaceuticals grew those systems on a shoestring, buying or building each one as the function was needed; they are homegrown, COTS or SaaS, they are plural where they should be singular, and none of them is a quality system.

**Austin is an acquisition**, and so is **Bucharest**.  Both are small-batch pharmaceutical manufacturers, both were bought with their systems, and both have had minimal integration since — Bucharest's acquisition has only just closed.  Their full inventories were loaded by Gary Geeke in `extending-the-systems-inventory/` and they tell a different story: each runs a complete, modern, regulated-pharma stack.  Siemens Opcenter MES, Rockwell FactoryTalk SCADA, LabWare LIMS, Waters Empower, Veeva Vault QMS, Trackwise, IBM Maximo, SAP S/4HANA, Workday, Splunk — in both of them, almost system for system.

| Estate | Systems | Where defined | Qualified name pattern | Character |
|---|---|---|---|---|
| **Coco core** (parent) | 29 | `CocoComboArchive.omarchive` | `System::<id>` | Organic; homegrown/COTS/SaaS; the integrated surface |
| **Austin** (acquired) | 45 | `coco_austin_systems.csv` → notebook | `SoftwareServer::AUS-SYS-nnn::<serial>` | Complete regulated stack, US-facing; Cloudera data lake, Informatica MDM |
| **Bucharest / EKG** (acquired, just closed) | 30 | `ekg_systems.csv` → notebook | `SoftwareServer::SYS-nnn::<system name>` | Complete regulated stack, EU-facing; Veeva RIM, OpenText ECM, cold-chain IoT |

The acquired systems are loaded with `category: Acquired Systems` and `deployedImplementationType: Unclassified Software Server`, under `ITSubsystem::` collections per business area, in the **IT Systems Inventory**.  Their system interactions are loaded as `DataFlow` relationships — and every one of those carries an `iscQualifiedName` property currently holding the placeholder *"add qualifiedName of information supply chain here"*.  That placeholder is where this document's supply chains are meant to go.

---

## Reconciling the archive's Austin entries

Four of the archive's 29 systems are labelled Austin: `MFCTRL9482` (Austin Manufacturing Control, homegrown V1.2), `aus-inventory` (homegrown V23.2), `austin-haz-mat` (homegrown V1.2) and `procurement04` (COTS V7.2).  None of them appears in the 45-system Austin inventory, and the inventory's equivalents are different products — Siemens Opcenter rather than a homegrown control system, SAP S/4HANA and Manhattan WMS rather than a homegrown inventory, SAP Ariba rather than a generic COTS purchasing system.

Two readings are possible and the difference matters for what gets linked:

- **They are what Coco integrated with** — interface systems or legacy components that the parent connected to, standing in front of the real Austin estate.  Then they are the right target for the parent's chains and the wrong target for Austin's.
- **They are the archive's simplification** of the same systems, written before the full inventory existed.  Then they should be reconciled to the inventory entries and eventually retired.

`austin-haz-mat` is the sharpest case: nothing in the 45-system inventory holds hazardous material data at all, so either the archive entry is a Coco-side stub or the inventory is missing a system.  This document treats the archive's four as **Coco core** and matches Austin components against the full inventory, and records the question rather than answering it.

**Confidence**

| | Meaning |
|---|---|
| **Strong** | The system's description or a loaded interaction names the function; link it |
| **Probable** | The function plainly lives in this system, but nothing says so explicitly |
| **Possible** | The system *could* host it; confirm with the owner before linking |
| — | Nothing in that estate does this |

---

## Part 1: Business system groups by estate

| Group | Coco core | Austin | Bucharest / EKG |
|---|---|---|---|
| Data Hub | being built | Informatica MDM + IDMC, Cloudera data lake | — |
| Patient Treatment / Sales | `globalCRM` (SaaS) | Salesforce CRM, Oracle OMS | Veeva CRM, HubSpot |
| Finance | `coco-ledgers`, `coco-expenses` (both SaaS) | SAP S/4HANA | SAP S/4HANA, SAP Concur |
| Procurement | `procurement01`–`05` | SAP Ariba SRM, OpenText EDI | SAP S/4HANA, DocuSign |
| Research | **none** | data lake / Spark (analytics, not research) | — |
| Warehouse | `coco-inventory`, `aus-inventory`, 3 × depots | Manhattan WMS | in-house WMS |
| Manufacturing | `manufacturing-planning`, 3 × homegrown control systems | Opcenter MES, FactoryTalk SCADA, Honeywell BMS | Opcenter MES, FactoryTalk, Proact cold chain |
| Delivery | 3 × depots | Oracle TMS, OpenText EDI, ArcGIS | WMS despatch only |
| Quality and Regulatory | **none** | LabWare LIMS, Empower, Veeva QMS, Veeva EBR, Trackwise, Maximo | LabWare LIMS, Empower, Veeva QMS, Veeva RIM, Trackwise, Maximo, Aris |
| People | `coco-hrim`, UK/NL/CA payroll, `cocopages`, `sec-admin` | Workday, Cornerstone LMS, UKG, AD, Entra ID | Workday, Kronos, AD |
| Privacy Operations | **none** | Purview DLP (discovery only) | OpenText ECM (retention only) |

The parent has no quality layer; both acquisitions have a complete one.  The parent has no US payroll; Austin's Workday is it.  The parent has one candidate for a master data hub and it is not yet built; Austin has Informatica MDM pushing golden product, supplier, customer and employee records to four systems already.

---

## Part 2: Component matches

Systems are named by short id — `AUS-022` means `SoftwareServer::AUS-SYS-022::SN-MES-AU-20180601`, `EKG-003` means `SoftwareServer::SYS-003::Siemens Opcenter MES`, and core systems keep their `System::` name.

### 2.1 Data Hub

| Component | Coco core | Austin | Bucharest / EKG |
|---|---|---|---|
| Product Master Register | `cocoProducts` — Probable | AUS-043 Informatica MDM — **Strong** (golden product records) | EKG-001 SAP material master — Possible |
| Product Data Distribution | — | AUS-043 MDM → AUS-042 IDMC — **Strong** (pushes golden records to SAP, Salesforce, Ariba, WMS on change) | — |

### 2.2 Patient Treatment

| Component | Coco core | Austin | Bucharest / EKG |
|---|---|---|---|
| Treatment Ordering Portal | `globalCRM` — **Strong** | AUS-016 Salesforce CRM / AUS-011 Oracle OMS — Probable (distributor and hospital orders; nothing personalised) | EKG-006 Veeva CRM — Possible |
| Patient Identity Register | `globalCRM` — Possible ⚠ external SaaS | — (Austin sells to distributors; no patient record) | — |
| Order to Invoice Processing | `globalCRM` → `coco-ledgers` — Probable | AUS-011 OMS → AUS-009 SAP — **Strong** (order confirmation, ATP, invoicing loaded as interactions) | EKG-001 SAP → EKG-006 Veeva CRM — Probable (order status and invoice data) |

### 2.3 Finance

| Component | Coco core | Austin | Bucharest / EKG |
|---|---|---|---|
| Subledger Feeds | `coco-ledgers` — Possible | AUS-009 SAP — **Strong** (MES, Ariba, Workday, Maximo → SAP are loaded interactions; they *are* the feeds) | EKG-001 SAP — **Strong** (MES, Concur, Workday, Maximo, WMS → SAP) |
| Journal Entry Review | `coco-ledgers` — Probable | AUS-009 SAP — Probable | EKG-001 SAP — Probable |
| Group Consolidation Engine | `coco-ledgers` — Possible | AUS-009 SAP — Possible (plant-level only) | EKG-001 SAP — Possible ⚠ three ledgers, no consolidation flow between them |
| Disclosure and Statutory Reporting | `coco-ledgers` — Possible | AUS-041 Power BI — Possible | EKG-014 Power BI — Possible |
| Controls Evidence Repository | — | AUS-038 Splunk — Possible (SAP audit log: "critical financial transactions") | EKG-026 Splunk — Possible |
| Payment Detail Change Control | `procurement01` / `coco-ledgers` — Possible | AUS-043 MDM (golden supplier) / AUS-014 Ariba — Probable | EKG-001 SAP — Possible |
| Supplier Payment Processing | `coco-ledgers` — Probable | AUS-009 SAP ← AUS-014 Ariba (supplier invoices) — **Strong** | EKG-001 SAP — Probable |
| Transaction Monitoring | — | AUS-038 Splunk — Possible | EKG-026 Splunk — Possible |
| Transfers of Value Register | — | AUS-017 Salesforce Marketing Cloud — Possible ("HCP engagement tracking") | — |
| Expense Approval Workflow | `coco-expenses` — **Strong** | AUS-009 SAP — Possible (no expense tool) | EKG-012 SAP Concur — **Strong** |

### 2.4 Procurement

| Component | Coco core | Austin | Bucharest / EKG |
|---|---|---|---|
| Supplier Material Certificates | procurement / depots — Possible | AUS-024 LabWare LIMS — Probable; AUS-015 EDI — Possible | EKG-004 LIMS — Probable; EKG-024 OpenText ECM — Probable (CoA PDFs archived) |
| Third Party Onboarding Workflow | `procurement01` — Probable | AUS-014 SAP Ariba SRM — **Strong** ("supplier onboarding") | EKG-001 SAP — Possible; EKG-020 DocuSign (contract execution) — Possible |
| Supplier Master Register | `procurement01` — Probable ⚠ five purchasing systems | AUS-043 Informatica MDM — **Strong** (golden supplier records → SAP, Ariba) | EKG-001 SAP — Probable |

### 2.5 Warehouse

| Component | Coco core | Austin | Bucharest / EKG |
|---|---|---|---|
| Goods Receipt and Inspection | 3 × depots; both inventories — **Strong** | AUS-012 Manhattan WMS — **Strong** ("inbound receipts") | EKG-019 WMS — **Strong** (goods receipts from SAP) |
| Material Quarantine and Release Control | `coco-inventory`, `aus-inventory` — Probable | AUS-012 WMS / AUS-009 SAP — Probable; LIMS as the gate | EKG-019 WMS / EKG-001 SAP — Probable |

### 2.6 Manufacturing

| Component | Coco core | Austin | Bucharest / EKG |
|---|---|---|---|
| Personalised Order Scheduler | `manufacturing-planning` — **Strong** | AUS-009 SAP production planning — Probable | EKG-001 SAP — Probable |
| Manufacturing Execution System | 3 × control systems — **Strong** | AUS-022 Siemens Opcenter MES — **Strong** | EKG-003 Siemens Opcenter MES — **Strong** |
| Process Historian | control systems — Possible | AUS-023 SCADA → AUS-007 Kafka → AUS-001 CDP — **Strong** ("5 years of … sensor telemetry") | EKG-015 FactoryTalk — Probable (no historian or lake) |
| Equipment Qualification Register | control systems — Possible | AUS-029 IBM Maximo — **Strong** ("calibration records, equipment qualification status") | EKG-016 Maximo — **Strong** |
| Electronic Batch Record System | control systems — Probable | AUS-026 Veeva Vault EBR — **Strong** | EKG-003 Opcenter MES — Probable; signed PDFs to EKG-024 OpenText ECM |
| Serial Number Generator | — | — | — |
| Packaging Line Controller | control systems — Possible | AUS-023 FactoryTalk SCADA ("filling lines") — Probable | EKG-015 FactoryTalk — Probable |
| Case and Pallet Aggregation Recorder | control / depots — Possible | AUS-012 Manhattan WMS ("pick, pack and despatch") — Possible | EKG-019 WMS — Possible |
| Serialisation Repository | — | — | — |
| Market Verification Gateway | — | — (EDI is B2B documents, not verification) | — |

### 2.7 Delivery

| Component | Coco core | Austin | Bucharest / EKG |
|---|---|---|---|
| Patient Sample Logistics | — | AUS-013 Oracle TMS — Possible (outbound only) | — |
| Treatment Delivery Tracking | depots / `globalCRM` — Possible | AUS-013 Oracle TMS — **Strong** ("delivery tracking of outbound orders"); AUS-044 ArcGIS | EKG-019 WMS — Possible (despatch only) |
| Transport Classification Service | HazMat inventories — Probable | AUS-013 TMS / AUS-009 SAP material master — Possible | EKG-001 SAP — Possible |
| Shipping Documentation Preparation | 3 × depots — Probable | AUS-013 TMS (BOL) + AUS-015 EDI (ASNs) — **Strong** | EKG-019 WMS — Probable |
| Temperature Monitoring Devices | — | AUS-028 Honeywell BMS — Possible (cleanrooms, static) | EKG-022 Proact Cold Chain Monitor — Probable (IoT; cold stores and cleanrooms, not yet in transit) |
| Cold Chain Data Collector | — | AUS-007 Kafka → AUS-001 CDP — Possible (environmental telemetry) | EKG-022 Proact → EKG-003 MES — Probable |

### 2.8 Quality and Regulatory

| Component | Coco core | Austin | Bucharest / EKG |
|---|---|---|---|
| Safety Intake Gateway | — | AUS-018 ServiceNow CSM → AUS-025 Veeva QMS — **Strong** (loaded interaction: "product complaint records and adverse event reports") | — |
| Product Complaint Intake | `globalCRM` — Possible | AUS-018 ServiceNow CSM — **Strong** ("product complaint intake") | EKG-006 Veeva CRM — Possible |
| Pharmacovigilance Case Management | — | AUS-025 Veeva QMS — Possible (receives AE reports; it is a QMS, not a PV system) | EKG-002 Veeva QMS — Possible |
| Medical Assessment and Coding | — | — (manual) | — |
| Safety Signal Detection | — | AUS-006 Spark on the data lake — Possible ("anomaly scores") | — |
| Regulatory Safety Submission | — | AUS-030 Trackwise — Possible (commitments, field actions) | EKG-021 Veeva Vault RIM — Probable ("submission planning … health authority tracking") |
| Laboratory Information Management System | — | AUS-024 LabWare LIMS + AUS-027 Empower — **Strong** | EKG-004 LabWare LIMS + EKG-027 Empower — **Strong** |
| Deviation and CAPA Management | — | AUS-025 Veeva Vault QMS — **Strong** | EKG-002 Veeva QMS + EKG-005 Trackwise — **Strong** |
| Batch Review and QP Certification | control systems — Possible | AUS-026 Veeva EBR ("batch review and release") + AUS-025 QMS ("QP release approvals") — **Strong** | EKG-003 MES / EKG-002 QMS — Probable |
| Serialisation Alert Triage | — | — | — |
| Temperature Excursion Assessment | — | AUS-025 Veeva QMS (as deviation) — Possible | EKG-002 QMS — Possible; EKG-022 Proact as source |
| Market Authorisation Register | `cocoProducts` — Possible | AUS-030 Trackwise — Possible | EKG-021 Veeva Vault RIM — **Strong** ("dossier authoring and health authority tracking") |
| Exposure Banding Register | HazMat inventories — Probable | AUS-025 Veeva QMS — Possible (no EHS system) | EKG-002 QMS — Possible |
| Exposure Monitoring Capture | `coco-haz-mat` — Possible | AUS-028 Honeywell BMS — Possible (environmental, not personal) | EKG-022 Proact — Possible |
| Incident and Near Miss Reporting | — | AUS-025 Veeva QMS / AUS-034 ServiceNow ITSM — Possible | EKG-002 Veeva QMS — Possible |

### 2.9 People

| Component | Coco core | Austin | Bucharest / EKG |
|---|---|---|---|
| Worker Master Register | `coco-hrim` — **Strong** | AUS-019 Workday HCM — **Strong** | EKG-013 Workday HCM — **Strong** |
| Joiner Mover Leaver Workflow | `coco-hrim` — **Strong** | AUS-019 Workday → AUS-032 Entra ID — **Strong** (SCIM "joiner, mover and leaver events") | EKG-013 Workday → EKG-007 M365 — **Strong** |
| Identity and Access Provisioning | `sec-admin` — **Strong** | AUS-032 Entra ID + AUS-031 AD — **Strong** | EKG-008 Active Directory — **Strong** |
| Payroll System | UK/NL/CA payroll — **Strong** ⚠ no US payroll | AUS-019 Workday ("payroll") + AUS-021 UKG — **Strong** — *this is the US payroll* | EKG-013 Workday + EKG-023 Kronos — **Strong** — the Romanian payroll |
| Corporate Directory | `cocopages` — **Strong** | AUS-031 AD / AUS-033 M365 — Probable | EKG-007 M365 / EKG-008 AD — Probable |
| Competency Framework Register | `coco-hrim` — Probable | AUS-020 Cornerstone LMS ("role-based curricula") — **Strong** | EKG-013 Workday — Possible |
| Learning Management System | `coco-hrim` — Possible | AUS-020 Cornerstone OnDemand LMS ("GMP training compliance") — **Strong** | EKG-013 Workday — Possible |
| Qualification and Competency Register | `coco-hrim` — Probable | AUS-020 Cornerstone ("training record management") — **Strong** | EKG-013 Workday — Possible |
| Qualification Currency Checker | — | AUS-020 Cornerstone — Possible | — |
| Health Surveillance Records | `coco-hrim` — Possible ⚠ principle says not here | — | — |
| Long Term Health Record Archive | — | — | EKG-024 OpenText ECM — Possible (built for long-term GMP retention; right capability, different content) |

### 2.10 Privacy Operations

| Component | Coco core | Austin | Bucharest / EKG |
|---|---|---|---|
| Rights Request Intake | — | AUS-018 ServiceNow CSM — Possible | — |
| Data Subject Identity Verification | — | — | — |
| Record of Processing Activities Register | — | — | — |
| Personal Data Discovery | — | AUS-039 Microsoft Purview DLP — Probable ("data classification … sensitive manufacturing and patient data") | — |
| Rights Fulfilment Orchestrator | — | — | — |
| Retention Schedule Service | — | — | EKG-024 OpenText ECM — Possible |

### 2.11 External

National Verification Systems, Carrier Systems and Sanctions and Screening Service are external by design.  Austin's OpenText EDI (AUS-015) is the company's own end of the carrier and 3PL exchange, and is a candidate for the wire rather than for the external component.

---

## Findings

**The regulated layer exists — twice — and not at the parent.** After matching against all three estates, only **eight** internal components have no candidate anywhere: the four serialisation components, medical assessment and coding (manual by design), and three of the six privacy components — identity verification, the record of processing, and the fulfilment orchestrator.  In version 0.1 it was 28.  The difference is Austin and Bucharest.  Every LIMS, QMS, EBR, CAPA, equipment qualification and training compliance component the strategic chains need has a Strong match at one or both acquisitions, and none at Coco core.

**The acquisitions show what the target looks like.** Austin and EKG run near-identical stacks — Opcenter, FactoryTalk, LabWare, Empower, Veeva QMS, Trackwise, Maximo, S/4HANA, Workday, Splunk, vSphere, Veeam, AD — bought independently, by two different companies, in two different regulatory jurisdictions.  That convergence is not coincidence; it is what a small-batch pharmaceutical manufacturer buys when it has to pass inspection.  The parent is the outlier, and the integration question is less *how do we absorb Austin* than *which of Austin's systems becomes the group standard*.

**Each acquisition has something the other lacks.** Austin has the electronic batch record (Veeva EBR), master data management (Informatica MDM), a five-year data lake, transport management and a learning management system.  EKG has regulatory information management (Veeva RIM), a long-term GMP archive (OpenText ECM), cold-chain IoT and electronic signature.  Between them they cover almost the whole strategic register; neither covers it alone.

**Nothing serialises, and nothing does pharmacovigilance.** Not the parent, not Austin, not EKG.  Both acquisitions have product complaint intake and both can route an adverse event into a QMS, but a QMS is not a pharmacovigilance system and cannot run the statutory reporting clock.  Serialisation is absent entirely, across all three estates — the serialisation program's *Centralised Serialisation Data Management* approach describes a capability the group does not have.

**There are now three ledgers and no consolidation.** FinMagic (SaaS) for the parent, SAP S/4HANA at Austin, SAP S/4HANA at EKG.  No loaded interaction connects any of them.  For a US-listed group the consolidated statements are being produced somewhere, and that somewhere is not in any inventory.

**Master data is fragmented differently in each estate.** The parent has five purchasing systems and two inventories with no master data hub.  Austin has one hub (Informatica MDM) pushing golden records to four systems.  EKG has SAP as its de facto master.  Three different answers to *which record is authoritative* is a harder problem than one bad answer.

**The archive's Austin entries do not reconcile to the Austin inventory.** See above; `austin-haz-mat` in particular has no counterpart.  This should be settled before any `ImplementedBy` link is drawn to those four.

**The inventory's own gaps have moved.** No US payroll turned out to mean *Austin's Workday runs it*.  The Kansas City depot is still unexplained.  Research systems are still absent everywhere — the clinical trials chain, the best-modelled in the archive, runs on components that no inventory lists as systems.

---

## What this makes possible

**`ImplementedBy` per estate.** One solution component may be implemented by three systems, one per estate.  That is not a modelling compromise; it is the integration debt made visible.  A component with three implementations and no wire between them is a supply chain that runs three times in parallel.

**The `iscQualifiedName` placeholder.** The 120 `DataFlow` relationships loaded by the inventory notebook — 75 for Austin, 45 for EKG — each carry `iscQualifiedName: "add qualifiedName of information supply chain here"`.  Twenty-one of them correspond directly to wires in `strategic-supply-chain-analysis.md` — the appendix lists each one.  MES → Veeva EBR is *execution record*, ServiceNow CSM → Veeva QMS is *complaint with safety content*, Workday → Entra ID is *provision or revoke*, Ariba → SAP is *payment postings*.  Filling the placeholder with the strategic chain's qualified name is what connects a designed supply chain to the real lineage beneath it — and it is a change to the CSV files and the notebook, not to this document.

**The Strong and Probable rows are linked** by the notebook in [mapping-the-systems/](mapping-the-systems/README.md), which carries this table forward as `data/component-system-mapping.csv` and creates the `ImplementedBy` relationships from it.  The Possible rows are reported there rather than linked, until an owner confirms them.  The eight with nothing are the shopping list — and it is a much shorter list than it was this morning.

---

## Appendix: Loaded interactions that are strategic wires

The `DataFlow` relationships below, already loaded by the inventory notebook, carry the same flow as a wire in `strategic-supply-chain-analysis.md`.  Each is a candidate for having its `iscQualifiedName` placeholder replaced with the supply chain named.  Fourteen are Austin's, seven are EKG's.  Interactions that are authentication plumbing (Active Directory → everything), instrument feeds (Empower → LIMS) or analytics extracts (→ Power BI, → data lake) are not listed: they are real, but they are not supply chain handovers.

| Estate | Loaded interaction | Strategic wire | Supply chain |
|---|---|---|---|
| Austin | Opcenter MES → Veeva Vault EBR | Manufacturing Execution → Electronic Batch Record: *execution record* | Batch Manufacturing and Release |
| Austin | Opcenter MES → Veeva Vault QMS | Manufacturing Execution → Deviation and CAPA: *raise deviation* | Batch Manufacturing and Release |
| Austin | Opcenter MES → SAP S/4HANA | Subledger Feeds → ledger: *post transactions* (production confirmations) | Financial Close and External Reporting |
| Austin | Veeva Vault QMS → Veeva Vault EBR | Deviation and CAPA → Electronic Batch Record: *deviation disposition* | Batch Manufacturing and Release |
| Austin | Informatica MDM → SAP S/4HANA | Product Data Distribution → Data Hub: *product master feed* | New Drug Product Details |
| Austin | Salesforce CRM → Oracle OMS | Treatment Ordering Portal → Patient Identity Register: *register order* | Personalised Treatment Ordering |
| Austin | Manhattan WMS → Oracle TMS | Shipping Documentation → Carrier Systems: *consign* | Cold Chain and Dangerous Goods Consignment |
| Austin | Oracle TMS → OpenText EDI | Shipping Documentation → Carrier Systems: *consign* | Cold Chain and Dangerous Goods Consignment |
| Austin | SAP Ariba SRM → SAP S/4HANA | Supplier Payment Processing → ledger: *payment instruction* | Third Party Onboarding and Payment |
| Austin | ServiceNow CSM → Veeva Vault QMS | Product Complaint Intake → Safety Intake Gateway: *complaint with safety content* | Adverse Event and Safety Reporting |
| Austin | Workday HCM → SAP S/4HANA | Payroll System → Subledger Feeds: *payroll postings* | Financial Close; New Employee Onboarding |
| Austin | Workday HCM → Cornerstone LMS | Worker Master Register → Learning Management: *worker and role* | Workforce Competency and Qualification |
| Austin | Workday HCM → Entra ID | Worker Master Register → Identity and Access Provisioning: *provision or revoke* | New Employee Onboarding |
| Austin | IBM Maximo → SAP S/4HANA | Subledger Feeds → ledger: *post transactions* (work order costs, depreciation) | Financial Close and External Reporting |
| EKG | Proact Cold Chain Monitor → Opcenter MES | Temperature Monitoring Devices → Cold Chain Data Collector: *transit temperature record* | Cold Chain and Dangerous Goods Consignment |
| EKG | Opcenter MES → Veeva Vault QMS | Manufacturing Execution → Deviation and CAPA: *raise deviation* | Batch Manufacturing and Release |
| EKG | Opcenter MES → SAP S/4HANA | Subledger Feeds → ledger: *post transactions* | Financial Close and External Reporting |
| EKG | SAP S/4HANA → Workday HCM | Payroll System → Subledger Feeds: *payroll postings* | Financial Close; New Employee Onboarding |
| EKG | SAP S/4HANA → SAP Concur | Expense tool → Subledger Feeds: *expense postings* | Employee Expense Payment |
| EKG | SAP S/4HANA → Maximo | Subledger Feeds → ledger: *post transactions* | Financial Close and External Reporting |
| EKG | Workday HCM → Microsoft 365 | Worker Master Register → Identity and Access Provisioning: *provision or revoke* | New Employee Onboarding |

Two loaded interactions have no strategic wire and probably should: **LIMS → Veeva QMS** (out-of-specification results raising a deviation) exists at both sites and is a flow the batch release chain depends on, and **Maximo → Veeva QMS** (overdue calibration raising a quality event) is the equipment qualification gate actually enforcing itself.  Both are wires the analysis should gain, not interactions to ignore.

---

## Appendix: Related Resources

| Resource | Relevance |
|---|---|
| [strategic-supply-chain-analysis.md](strategic-supply-chain-analysis.md) | The 82 components and 130 wires this document matches |
| [`0. data-governance-program/strategic-information-supply-chains.md`](../0.%20data-governance-program/strategic-information-supply-chains.md) | The sixteen supply chains |
| [`extending-the-systems-inventory/`](extending-the-systems-inventory/README.md) | Austin and EKG inventories, subsystems and interactions, and the notebook that loads them |
| `extending-the-systems-inventory/data/*_system_interactions.csv` | The `DataFlow` relationships carrying the `iscQualifiedName` placeholder |
| `CocoComboArchive.omarchive` | The 29 core systems and their existing `ImplementedBy` links |

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
