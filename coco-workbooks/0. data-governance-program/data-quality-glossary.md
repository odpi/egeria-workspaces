# Coco Pharmaceuticals Data Quality Glossary

> **Author:** Erin Overview (Information Architect), Florence Paynter, Stew Faster (Head of Manufacturing)  
> **Version:** 1.0  
> **Status:** ACTIVE  
> **Date:** 2026-09-05  
> **Description:** The vocabulary of data integrity as the regulators use it — the five ALCOA attributes, the four added by ALCOA+, the one added by ALCOA++, and the supporting terms about records, evidence and controls that those attributes depend on.

---

## Overview

The manufacturing team's `ALCOA+ Data Integrity` principle is the standard that all GMP data at Coco Pharmaceuticals
must meet, and the `ALCOA+ Data Integrity Framework` approach is how they apply it — as a design tool, an audit tool
and an investigation framework.  Both were written on the assumption that everybody involved already agrees what
*attributable*, *contemporaneous* and *original* mean.

They did not.  When the data quality analysts started turning the manufacturing quality expectations into measurable
rules, the same nine words came back with different meanings from each area: *original* meant the paper printout to
the QC laboratory and the instrument's binary file to the engineers; *complete* meant "no empty fields" to one team
and "including the tests that failed" to another.  The rules could not be written until the words were agreed.

So [Erin Overview](https://egeria-project.org/practices/coco-pharmaceuticals/personas/erin-overview/) sat down with
Florence Paynter and the manufacturing quality team and defined them.  This file is the result.  It is not a Coco
Pharmaceuticals invention — the definitions follow the regulators' own, from the EMA, FDA, MHRA, WHO and PIC/S
guidance — but it records the reading that Coco Pharmaceuticals applies, which is what makes them usable in a rule.

The three framework names in the title are three successive versions of the same idea:

* **ALCOA** — the original five attributes, coined by the FDA in the 1990s for Good Laboratory Practice records.
* **ALCOA+** — the same five plus four more, added by the EU and PIC/S in the 2010s to cover the record over its
  whole life rather than just at the moment it is written.  This is the version the manufacturing program adopted.
* **ALCOA++** — ALCOA+ plus **Traceable**, introduced by the EMA in its 2023 guideline on computerised systems and
  electronic data in clinical trials.  Coco Pharmaceuticals defines it here because drug development will be held to
  it, and because it names something the other nine attributes only imply.

The glossary is governed by the manufacturing definitions rather than owning a standard of its own.  A term here
explains what the principle requires; it does not decide it.  Where a definition has been narrowed for Coco
Pharmaceuticals — as with **Original** for hybrid instrument systems — that is stated in the term's usage.

**Prerequisites:** `manufacturing-governance-program.md` must already be loaded, because this file links the glossary
to the `ALCOA+ Data Integrity` principle and the `ALCOA+ Data Integrity Framework` approach defined there.  The
`SubjectArea::Governance` collection must also already exist — the subject area collections are loaded from
`CocoComboArchive.omarchive` when the metadata server starts up.

---

## Part 1: The Glossary

___

## Create Glossary

### Display Name
Data Quality Glossary

### Qualified Name
Glossary::DataQualityGlossary

### Description
The vocabulary of data integrity and data quality used across Coco Pharmaceuticals: the ALCOA, ALCOA+ and ALCOA++ attributes, and the terms about records, evidence and controls that those attributes are expressed in.

### Language
English

### Usage
Reference this glossary whenever a data quality expectation, monitoring rule, deviation report or inspection response uses one of the ALCOA attributes, so that the word carries the same meaning in the rule as it does in the regulation it came from.

### Purpose
To make the ALCOA, ALCOA+ and ALCOA++ attributes precise enough to be turned into measurable data quality rules, and to give every governance domain a single agreed reading of the words the regulators use.

### Search Keywords
- Data Integrity
- Data Quality
- ALCOA
- ALCOA+
- ALCOA++
- GMP
- Good Documentation Practice

### URL
https://egeria-project.org/practices/coco-pharmaceuticals/

### Authors
- Erin Overview
- Florence Paynter
- Stew Faster

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

### 1.1 A member of the Governance subject area

Subject areas highlight the topics the company has decided are important enough to be curated deliberately.  Data integrity is one of them, so the glossary joins the existing `Governance` subject area as a member of that collection.

___

## Add Member to Collection

### Element Id
Glossary::DataQualityGlossary

### Membership Rationale
Links the Governance subject area to the vocabulary that defines data integrity for it. Data integrity is a governance topic before it is a manufacturing one — every domain that sets a quality expectation states it in these words.

### Membership Status
VALIDATED

### Collection Id
SubjectArea::Governance

___

---

### 1.2 Governed by the manufacturing data integrity definitions

The glossary does not set the standard — it explains the one the manufacturing team set.  Both links are recorded, because the principle is what the terms must satisfy and the framework is the method the terms are used within.

___

## Link Governed By

### Governance Definition
CocoPharma::GovernancePrinciple::ALCOAPlusDataIntegrity

### Referenceable
Glossary::DataQualityGlossary

### Label
defines the vocabulary of

### Description
The principle states that all manufacturing data must satisfy the ALCOA+ attributes. This glossary is the agreed definition of each of those attributes, so that the principle can be applied consistently and measured.

___

---

___

## Link Governed By

### Governance Definition
CocoPharma::GovernanceApproach::ALCOAPlusFramework

### Referenceable
Glossary::DataQualityGlossary

### Label
supports

### Description
The framework is used as a design tool, an audit tool and an investigation framework. Each of those uses works through the attributes defined here, so the glossary is the reference the framework is applied against.

___

---

## Part 2: Organizing the Glossary

The categories follow the shape of the frameworks themselves — the original five, the four that ALCOA+ adds, and the one that ALCOA++ adds — with two further categories for the supporting terms that the attributes are written in terms of.

___

## Create Collection Folder

### Display Name
Data Integrity Frameworks

### Qualified Name
CollectionFolder::DataQualityGlossary::Frameworks

### Description
The frameworks themselves and the overarching concepts they serve — data integrity, good documentation practice, the data lifecycle and the governance system that maintains them.

### Purpose
Groups the terms that name the frameworks and set the context the individual attributes sit in.

### Parent ID
Glossary::DataQualityGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Erin Overview
- Florence Paynter

### Content Status
ACTIVE

___

---

___

## Create Collection Folder

### Display Name
ALCOA Core Attributes

### Qualified Name
CollectionFolder::DataQualityGlossary::ALCOACore

### Description
The five original ALCOA attributes: Attributable, Legible, Contemporaneous, Original and Accurate. Every later version of the framework retains all five unchanged.

### Purpose
Groups the five attributes that describe the record at the moment it is created.

### Parent ID
Glossary::DataQualityGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Erin Overview
- Florence Paynter

### Content Status
ACTIVE

___

---

___

## Create Collection Folder

### Display Name
ALCOA+ Additional Attributes

### Qualified Name
CollectionFolder::DataQualityGlossary::ALCOAPlus

### Description
The four attributes ALCOA+ adds to ALCOA: Complete, Consistent, Enduring and Available. They describe the record over its whole retention life rather than at the moment it is written.

### Purpose
Groups the four attributes that concern the record after creation.

### Parent ID
Glossary::DataQualityGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Erin Overview
- Florence Paynter

### Content Status
ACTIVE

___

---

___

## Create Collection Folder

### Display Name
ALCOA++ Additional Attribute

### Qualified Name
CollectionFolder::DataQualityGlossary::ALCOAPlusPlus

### Description
The single attribute ALCOA++ adds to ALCOA+: Traceable. Introduced by the EMA in 2023 for computerised systems and electronic data in clinical trials.

### Purpose
Groups the attribute that ALCOA++ adds, kept separate so that the version of the framework a requirement cites remains visible.

### Parent ID
Glossary::DataQualityGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Erin Overview
- Florence Paynter

### Content Status
ACTIVE

___

---

___

## Create Collection Folder

### Display Name
Records and Data

### Qualified Name
CollectionFolder::DataQualityGlossary::RecordsAndData

### Description
The kinds of data and record the attributes are applied to — raw data, source data, metadata, static and dynamic records, copies, backups and archives.

### Purpose
Groups the terms that name what is being governed, so that an attribute can be stated about a specific thing rather than about data in general.

### Parent ID
Glossary::DataQualityGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Erin Overview
- Florence Paynter

### Content Status
ACTIVE

___

---

___

## Create Collection Folder

### Display Name
Controls and Evidence

### Qualified Name
CollectionFolder::DataQualityGlossary::ControlsAndEvidence

### Description
The mechanisms that make the attributes demonstrable to an inspector — audit trails and their review, electronic signatures, unique user identity, time synchronisation, access control and second person review.

### Purpose
Groups the terms describing how an attribute is achieved and how it is evidenced.

### Parent ID
Glossary::DataQualityGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Erin Overview
- Florence Paynter

### Content Status
ACTIVE

___

---

## Part 3: The Frameworks

These are the terms that name the frameworks and the ideas they serve.  They are defined first because every attribute below is defined as belonging to one of them.

___

## Create Glossary Term

### Display Name
Data Integrity

### Summary
The property of data being complete, consistent and accurate throughout its lifecycle, so that it can be relied on as a record of what actually happened.

### Description
Data integrity is the degree to which data are complete, consistent, accurate, trustworthy and reliable, and to which those characteristics are maintained throughout the data lifecycle. It is a property of the whole system that produces and keeps the data — the people, the procedures, the instruments and the computerised systems — not a property of an individual value. Regulators assess data integrity because every quality decision, every batch release and every clinical conclusion rests on records being a faithful account of what was done.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::DataIntegrity

### Folders
- CollectionFolder::DataQualityGlossary::Frameworks

### Usage
Use when referring to the overall property. Where a specific aspect is meant, use the ALCOA attribute that names it, so that a requirement can be tested.

### Example
A batch record whose entries were all made at the time of the activity by the person who performed it, and which has not been altered since without a recorded reason, has data integrity. One reconstructed from memory at the end of the shift does not, however accurate the numbers happen to be.

### Is Abstract Concept
True

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
ALCOA

### Abbreviation
ALCOA

### Summary
The original five-attribute data integrity framework: Attributable, Legible, Contemporaneous, Original and Accurate.

### Description
ALCOA is an acronym for the five attributes a record must have to be considered reliable: Attributable, Legible, Contemporaneous, Original and Accurate. It was coined by the FDA in the 1990s for Good Laboratory Practice records and is now used across GxP. The five attributes describe the record at the point at which it is made — who made it, whether it can be read, when it was written, whether it is the first capture, and whether it says what actually happened.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::ALCOA

### Folders
- CollectionFolder::DataQualityGlossary::Frameworks

### Usage
Cite ALCOA only where the five core attributes are meant. Coco Pharmaceuticals applies ALCOA+ to GMP data, so a requirement that says "ALCOA" and means all nine attributes should say ALCOA+ instead.

### Aliases
- ALCOA principles

### Is Abstract Concept
True

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
ALCOA+

### Abbreviation
ALCOA+

### Summary
ALCOA extended with four further attributes — Complete, Consistent, Enduring and Available — covering the record over its whole retention life.

### Description
ALCOA+ retains the five ALCOA attributes and adds Complete, Consistent, Enduring and Available. The additions were introduced in EU and PIC/S data integrity guidance during the 2010s in response to a recurring inspection finding: records that were unimpeachable at the moment they were made, but incomplete as a set, inconsistent with the records around them, degraded in storage, or no longer retrievable when an inspector asked for them. ALCOA+ is the version Coco Pharmaceuticals applies to all GMP-regulated data, as stated in the ALCOA+ Data Integrity principle.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::ALCOAPlus

### Folders
- CollectionFolder::DataQualityGlossary::Frameworks

### Usage
This is the company standard for GMP data. Quality expectations and monitoring rules for manufacturing data should be written against the nine ALCOA+ attributes.

### Aliases
- ALCOA Plus

### Is Abstract Concept
True

### Authors
- Erin Overview
- Florence Paynter
- Stew Faster

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
ALCOA++

### Abbreviation
ALCOA++

### Summary
ALCOA+ extended with a tenth attribute, Traceable, introduced by the EMA in 2023 for computerised systems and electronic data in clinical trials.

### Description
ALCOA++ is ALCOA+ with Traceable added as a tenth attribute. It was introduced in the EMA's 2023 guideline on computerised systems and electronic data in clinical trials, which took effect in September of that year. Traceability was previously treated as an implication of the other attributes — particularly Original and Complete — but the EMA made it explicit because a value that is accurate, attributable and complete can still be impossible to follow back to the source it was derived from once it has passed through several systems. ALCOA++ is the framework Coco Pharmaceuticals applies to clinical trial data.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::ALCOAPlusPlus

### Folders
- CollectionFolder::DataQualityGlossary::Frameworks

### Usage
Cite ALCOA++ for clinical trial data and any computerised system supporting it. Manufacturing data is held to ALCOA+; the Traceable attribute is nonetheless expected of manufacturing systems through the batch traceability principle.

### Aliases
- ALCOA Plus Plus

### Is Abstract Concept
True

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Good Documentation Practice

### Abbreviation
GDP

### Summary
The set of working practices that produce records satisfying the ALCOA attributes — how entries are made, corrected, signed and dated.

### Description
Good Documentation Practice is the operational discipline through which the ALCOA attributes are achieved by the people making the records. It covers the mechanics: entries made in indelible ink at the time of the activity; no blank fields, with not-applicable entries struck through and initialled; corrections made with a single line through the original value so that it remains readable, with the new value, the reason, the initials and the date; no overwriting, no correction fluid, no back-dating, and no signing for work performed by someone else.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::GoodDocumentationPractice

### Folders
- CollectionFolder::DataQualityGlossary::Frameworks

### Usage
Use when referring to the behaviour expected of the person making the record. The abbreviation GDP is ambiguous in a pharmaceutical company — it also means Good Distribution Practice — so write the term in full in any document that touches distribution.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Data Lifecycle

### Summary
The whole life of a record, from generation through processing, review, reporting and retention to eventual destruction.

### Description
The data lifecycle covers generation and capture, processing and transformation, review and reporting, retention and archiving, retrieval, and authorised destruction at the end of the retention period. The ALCOA+ attributes apply across all of it, which is the reason four attributes were added to ALCOA — the original five say nothing about what happens after the entry is made. Data integrity controls have to be designed at each stage, and a break at any stage invalidates the record regardless of how well the other stages were controlled.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::DataLifecycle

### Folders
- CollectionFolder::DataQualityGlossary::Frameworks

### Usage
Use when scoping a data integrity risk assessment. An assessment that stops at the point of capture has assessed ALCOA, not ALCOA+.

### Is Abstract Concept
True

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Data Criticality

### Summary
The degree of influence a data item has on a decision about product quality or patient safety, used to set the level of control it needs.

### Description
Data criticality is judged by what the data are used to decide. Data that support a batch release decision, a specification conformance judgement, or a clinical safety conclusion are critical; data used for process monitoring or trending are not, though they may become critical if a decision is later based on them. Criticality drives the strength of the controls applied: the most critical data justify direct instrument capture, second person review and full audit trail review, which would be disproportionate elsewhere. Criticality is a property of the use, not of the value, so the same measurement can be critical in one process and not in another.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::DataCriticality

### Folders
- CollectionFolder::DataQualityGlossary::Frameworks

### Usage
Assess criticality before assessing risk. A data integrity risk assessment that has not first established criticality cannot rank its findings.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Data Integrity Risk

### Summary
The likelihood that a data item is deleted, amended, excluded or fabricated without detection, combined with the impact if that happened.

### Description
Data integrity risk combines the vulnerability of a data process to undetected alteration, omission or fabrication with the criticality of the data involved. The vulnerability side depends on how the data are captured and handled: manual transcription, shared logins, disabled audit trails, the ability to re-run a test and report only the passing result, and paper printouts standing in for dynamic electronic data all raise it. Assessing the risk is what the ALCOA+ framework is used for when applied as a design or audit tool.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::DataIntegrityRisk

### Folders
- CollectionFolder::DataQualityGlossary::Frameworks

### Usage
Record the assessment for every GMP-critical data process, and reassess whenever the process or its supporting system changes.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 4: The ALCOA Core Attributes

The five original attributes, in the order the acronym gives them.  Each is defined by what the record must show, and by the failure mode it exists to prevent.

___

## Create Glossary Term

### Display Name
Attributable

### Summary
It must be clear who created or amended the record, and when they did so.

### Description
Attributable means that every data entry, amendment and approval can be traced to the individual who made it and to the time at which it was made. On paper this is achieved by initials or a signature with a date; in a computerised system by a unique user account and an audit trail. Attribution is to a named person, not to a role, a team or a shared account, because the purpose is to identify who can be asked what happened. It is the first ALCOA attribute and the reason batch records carry names at all — a consequence the privacy team records as a distinct processing purpose, since the identity cannot be removed without destroying the attribution that makes the record compliant.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::Attributable

### Folders
- CollectionFolder::DataQualityGlossary::ALCOACore

### Usage
Attribution must identify a person. A record attributed to a shared login, an instrument's default account or a job title does not satisfy this attribute.

### Example
An in-process weight recorded in the electronic batch record shows the operator's user identity and the system timestamp. If a supervisor later corrects it, the audit trail shows the original value, the new value, the supervisor's identity, the time and the stated reason.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Legible

### Summary
The record must be readable and permanent, and must remain so for its full retention period.

### Description
Legible means that the record can be read and understood by someone other than its author, both now and at the end of the retention period. On paper this requires handwriting that others can read, indelible ink, and corrections that leave the original entry visible rather than obliterating it. In electronic systems it extends to the format the data are kept in: a file that can only be read by a version of an application that is no longer supported is not legible, however intact the bytes are. Legibility also covers the meaning — abbreviations and codes used in a record must be defined somewhere the reader can reach.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::Legible

### Folders
- CollectionFolder::DataQualityGlossary::ALCOACore

### Usage
For electronic records, assess legibility against the end of the retention period, not against today. This is what makes format obsolescence a data integrity issue rather than an IT one.

### Example
A correction on a paper batch record is made with a single line through the original entry so that the original value remains readable, with the new value, initials, date and reason written alongside. Correction fluid would make the record illegible in the sense this attribute means.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Contemporaneous

### Summary
The record must be made at the time the activity takes place.

### Description
Contemporaneous means the entry is made as the work is done, not before it and not from memory afterwards. Pre-recording — filling in an expected value ahead of the step — and post-recording from a scrap note at the end of a shift are both violations, even when the value written down is correct, because neither is evidence that the step happened as described. For electronic records this depends on the system's clock being synchronised and on the recorded time being the time of the activity rather than the time the data were later transferred. Where a delay is unavoidable, the record must show both times and the reason.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::Contemporaneous

### Folders
- CollectionFolder::DataQualityGlossary::ALCOACore

### Usage
A monitoring rule for this attribute compares the recorded activity time with the record creation time. A systematic gap is the signal, not an individual late entry.

### Example
An operator records a temperature reading in the batch record at the moment the reading is taken. Writing it on a glove and transcribing it into the record an hour later breaks the attribute, even if the number is right.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Original

### Summary
The first capture of the data, or a verified true copy of it, must be the record that is retained and reviewed.

### Description
Original means the first place a value was recorded — the instrument's own data file, the operator's entry in the batch record, the raw chromatogram — rather than a later transcription or summary of it. The original must be retained, and any decision must be traceable back to it. Where the original cannot practically be kept in its native form, a true copy verified as complete and accurate may take its place, and the verification must itself be recorded. For dynamic electronic data, a printed page is not a true copy, because printing discards the ability to reprocess, to see the audit trail and to inspect the metadata.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::Original

### Folders
- CollectionFolder::DataQualityGlossary::ALCOACore

### Usage
At Coco Pharmaceuticals the original for any instrument capable of producing an electronic data file is that file, not the printout. Hybrid processes that retain only the paper output do not satisfy this attribute and are recorded as data integrity risks pending remediation.

### Example
For an HPLC analysis the original is the acquired chromatographic data file with its processing method and audit trail, not the integrated results summary that is pasted into the laboratory notebook.

### Authors
- Erin Overview
- Florence Paynter
- Stew Faster

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Accurate

### Summary
The record must be correct, truthful, and a faithful account of what was actually observed.

### Description
Accurate means the data are free from error and reflect what genuinely happened. It covers arithmetic and transcription correctness, but its substance is truthfulness: the record must not be edited to show a better outcome, and results must not be selectively reported. Accuracy depends on the instruments being calibrated, the methods being validated, the calculations being verified, and the people being trained — none of which can be inferred from the value itself, which is why accuracy is evidenced by the controls around the measurement as much as by the measurement. Deliberate inaccuracy is falsification, and is treated as misconduct rather than as a quality deviation.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::Accurate

### Folders
- CollectionFolder::DataQualityGlossary::ALCOACore

### Usage
Accuracy cannot be measured directly by a data quality rule. Rules test the conditions it depends on — calibration currency, calculation verification, and the absence of unexplained repeat testing.

### Example
A result is reported as obtained. Re-running a test until it passes and reporting only the passing run is inaccurate reporting even though every individual number is correct.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 5: The Attributes ALCOA+ Adds

These four describe the record after it has been made.  Each of them was added because inspectors kept finding records that satisfied all five core attributes and were still not usable as evidence.

___

## Create Glossary Term

### Display Name
Complete

### Summary
The record must include all the data generated by the activity, including repeat tests, failures and the audit trail.

### Description
Complete means nothing generated by the activity has been left out. It includes the tests that failed, the runs that were repeated and the reason for repeating them, all in-process checks, any deviations, and the metadata and audit trail that give the data their context. The attribute exists because selective omission is the most common and the least visible integrity failure: a record showing only successful results is entirely accurate, entirely attributable and entirely contemporaneous, and completely misleading. A record is not complete if part of it can be deleted without leaving evidence that it existed.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::Complete

### Folders
- CollectionFolder::DataQualityGlossary::ALCOAPlus

### Usage
Completeness includes the audit trail and the metadata. A data set exported without them is not a complete record, whatever its content.

### Example
A dissolution test that was run three times because of an equipment fault is reported with all three runs, the fault, the investigation and the justification for which result is used.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Consistent

### Summary
The record must be internally coherent and must agree with the other records of the same activity.

### Description
Consistent means the record does not contradict itself or the records around it. Events must appear in a chronological sequence that the process could actually have followed; the same batch, lot or sample identifier must be used the same way in every system that references it; the same units, formats and conventions must be applied throughout; and the values in the batch record must reconcile with those in the laboratory system, the equipment logs and the warehouse records. Inconsistency between systems is usually the first observable symptom of a deeper integrity problem, which is why it is worth measuring even when no single record is wrong.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::Consistent

### Folders
- CollectionFolder::DataQualityGlossary::ALCOAPlus

### Usage
This is the most readily automated of the nine attributes. Cross-system reconciliation rules are the practical test for it.

### Example
The material quantity recorded as dispensed in the warehouse system matches the quantity recorded as charged in the batch record, and both are timestamped in an order the process allows.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Enduring

### Summary
The record must survive intact, in a readable form, for the whole of its required retention period.

### Description
Enduring means the record does not degrade, become corrupt or become unreadable during retention. For paper it concerns the medium — indelible ink, paper that does not fade, storage conditions that do not destroy it, and not recording on anything that was never meant to be kept, such as a scrap of paper or the back of a glove. For electronic records it concerns the storage: validated backup, verified restoration, migration ahead of format or platform obsolescence, and protection against silent corruption. Retention periods in this industry run to decades, which is longer than most of the systems that hold the data will exist.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::Enduring

### Folders
- CollectionFolder::DataQualityGlossary::ALCOAPlus

### Usage
Endurance is demonstrated by tested restoration, not by the existence of a backup. An untested backup is evidence of intent, not of the attribute.

### Example
Batch records are archived in a validated repository with periodic restoration testing, and the format is migrated when the originating system is decommissioned rather than when the retention period ends.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Available

### Summary
The record must be retrievable for review or inspection throughout its retention period.

### Description
Available means the record can be produced when it is needed — for batch review, for investigation, or for a regulatory inspection — within a reasonable time and in a readable form, at any point in the retention period. It is distinct from Enduring: a record can be perfectly preserved and still unavailable if nobody knows where it is, if the system holding it has been decommissioned, if the only person who could retrieve it has left, or if a contracted archive cannot deliver it to the timescale an inspector expects. Availability is therefore as much about indexing, access and retrieval procedures as about storage.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::Available

### Folders
- CollectionFolder::DataQualityGlossary::ALCOAPlus

### Usage
The practical test is retrieval time. Record the time taken to produce a sample of archived records each year, including any held by third parties.

### Example
An inspector asks for the batch record of a product made eleven years ago. It is retrieved from the archive, complete with its audit trail, within the same inspection.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 6: The Attribute ALCOA++ Adds

___

## Create Glossary Term

### Display Name
Traceable

### Summary
It must be possible to follow a reported value back through every transformation to the source data it came from.

### Description
Traceable means the path from a reported result to the raw data behind it is visible and unbroken. Every derivation, aggregation, transfer between systems and manual intervention along the way must be recorded, so that a value in a summary report can be followed back to the observation it originated in and to the processing applied to it. The EMA added it as the tenth attribute in 2023 because modern data flows pass through several systems before reaching a report, and each transfer is a point at which the connection to the source can be lost without any of the other nine attributes being violated. Coco Pharmaceuticals treats lineage capture as the technical means of satisfying it.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::Traceable

### Folders
- CollectionFolder::DataQualityGlossary::ALCOAPlusPlus

### Usage
Traceability is demonstrated by lineage, not by documentation of the intended flow. A described data flow that cannot be evidenced for a specific value does not satisfy the attribute.

### Example
A stability trend point in a regulatory submission can be followed back through the summary table, the statistical analysis, the laboratory result and the instrument data file to the injection that produced it.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 7: Records and Data

The attributes above are stated about something.  These terms name the somethings, and several of the arguments the team had turned out to be about these rather than about the attributes.

___

## Create Glossary Term

### Display Name
Raw Data

### Summary
The original capture of an observation, in the form and detail in which the instrument or person first recorded it.

### Description
Raw data are the first recorded observation together with everything needed to reconstruct and evaluate the reported result: the acquired values, the acquisition parameters, the processing method and the audit trail. For an instrument that produces an electronic data file, the raw data are that file — not the integrated result, not the summary and not the printout. For a manual observation, the raw data are the entry made at the time of the activity. Raw data must be retained for the full retention period, because any reported result must remain reconstructable from them.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::RawData

### Folders
- CollectionFolder::DataQualityGlossary::RecordsAndData

### Usage
If a result cannot be reconstructed from what has been kept, what was kept was not the raw data.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Source Data

### Summary
The clinical equivalent of raw data: the original records of clinical findings and observations from which trial data are derived.

### Description
Source data are the information in original records, and certified copies of them, that describes the clinical findings, observations and activities in a trial and is necessary for its reconstruction and evaluation. They live in source documents — hospital records, laboratory reports, diaries, dispensing records and device outputs — which may be held by the investigator site rather than by the sponsor. The concept parallels raw data in manufacturing and carries the same obligations, and drug development uses the two terms in the senses their own regulations define.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::SourceData

### Folders
- CollectionFolder::DataQualityGlossary::RecordsAndData

### Usage
Use source data for clinical records and raw data for manufacturing and laboratory records. They are the same idea in two regulatory vocabularies, and neither should be substituted for the other in a document that cites a regulation.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Metadata

### Summary
The contextual data that give a value its meaning — what it measures, in what units, when, by whom, and under which method.

### Description
Metadata are the data that describe other data: units, instrument identity, acquisition parameters, processing method, calibration status, operator identity, timestamps and the audit trail. Without them a value is a number and cannot be evaluated. Regulators treat metadata as an inseparable part of the record, which has a direct consequence for how records are exported, copied and archived — a transfer that carries only the values has not transferred the record. Metadata are covered by all ten attributes exactly as the values are.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::Metadata

### Folders
- CollectionFolder::DataQualityGlossary::RecordsAndData

### Usage
Any requirement about retaining, copying or archiving data applies to its metadata. State this explicitly, because system vendors frequently do not implement it.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Electronic Record

### Summary
Any combination of data in digital form that is created, modified, maintained, archived or retrieved by a computerised system.

### Description
An electronic record is a GxP record held in digital form, comprising its values, its metadata and its audit trail. Where an electronic record is the original, it — and not a printout of it — is the record that must be reviewed, retained and produced on inspection. Electronic records are subject to specific regulatory requirements for validation, access control, audit trail and signature, set out in EU GMP Annex 11 and in the FDA's 21 CFR Part 11.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::ElectronicRecord

### Folders
- CollectionFolder::DataQualityGlossary::RecordsAndData

### Is Abstract Concept
True

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Static Record

### Summary
An electronic record whose content is fixed once created, such as a scanned document or a photograph.

### Description
A static record is fixed at the moment of creation and is not reprocessed or reinterpreted afterwards. A paper record, a scan of one, or an image are static. The distinction matters because a printout can be an acceptable true copy of a static record, whereas it cannot be for a dynamic one. Classifying each GxP record as static or dynamic is therefore a prerequisite for deciding what has to be retained.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::StaticRecord

### Folders
- CollectionFolder::DataQualityGlossary::RecordsAndData

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Dynamic Record

### Summary
An electronic record that can be reprocessed or interrogated, so that a printout of it is never a complete copy.

### Description
A dynamic record allows the reviewer to interact with its content — to reprocess a chromatogram with different integration parameters, to expand a spectrum, to query an underlying data set, or to inspect the audit trail. Printing it produces one fixed view and discards that capability, so a printout of a dynamic record is not a true copy and cannot be the retained original. Chromatography data, spectral data and any queryable data set are dynamic. Where a laboratory has historically kept only printouts of dynamic records, that is a data integrity finding.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::DynamicRecord

### Folders
- CollectionFolder::DataQualityGlossary::RecordsAndData

### Usage
Whether a record is dynamic decides whether paper retention is acceptable. Make the classification explicitly and record it; do not leave it to be inferred.

### Authors
- Erin Overview
- Florence Paynter
- Stew Faster

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Hybrid System

### Summary
A process in which part of the record is electronic and part is paper, most often an electronic capture signed on paper.

### Description
A hybrid system splits a single record across electronic and paper media — typically an instrument or system that captures data electronically while the review and approval signatures are applied to a printout. Hybrids are permitted but carry higher data integrity risk, because the link between the signature and the specific electronic data it approves is maintained by procedure rather than by the system, and because it is easy for the electronic original to be modified after the paper has been signed. Where a hybrid is used, the link must be documented and the electronic data must still be retained as the original.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::HybridSystem

### Folders
- CollectionFolder::DataQualityGlossary::RecordsAndData

### Usage
Every hybrid process requires a documented data integrity risk assessment describing how the signature is bound to the electronic data it approves.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
True Copy

### Summary
A verified reproduction of an original record, complete with its metadata, that may be retained in place of the original.

### Description
A true copy is a copy of an original record — paper or electronic, and in either medium — that has been verified as a complete and accurate reproduction, preserving the content, the meaning and the metadata of the original. The verification must itself be recorded, identifying who performed it and when. A true copy may replace the original for retention purposes. A printout of a dynamic electronic record is not a true copy, because it does not preserve the ability to reprocess or to inspect the audit trail.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::TrueCopy

### Folders
- CollectionFolder::DataQualityGlossary::RecordsAndData

### Aliases
- Certified Copy

### Usage
The verification is what makes a copy true. An unverified copy is just a copy, and cannot replace the original.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Backup

### Summary
A copy of current records taken for recovery purposes, held separately from the live system.

### Description
A backup is a copy of live data, metadata and audit trail, taken to allow recovery after loss or corruption. Backups must be secured against alteration, held separately from the system they protect, and — critically — restored and verified periodically, since an untested backup is an assumption rather than a control. A backup is not an archive: it holds current data for recovery, is overwritten on a cycle, and is not intended to satisfy the retention obligation.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::Backup

### Folders
- CollectionFolder::DataQualityGlossary::RecordsAndData

### Usage
Do not describe a backup as meeting a retention requirement. Confusing the two is a recurring inspection finding.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Archive

### Summary
Protected long-term storage of records that are no longer in active use, held for the whole retention period.

### Description
An archive holds completed records for the remainder of their retention period in a form that is secure, indexed and retrievable. Archived records must be protected from alteration and deletion, retain their metadata and audit trail, and remain readable as systems and formats change — which usually means planned migration rather than passive storage. Access to the archive is controlled and its own activity is recorded. The archive is where the Enduring and Available attributes are principally satisfied.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::Archive

### Folders
- CollectionFolder::DataQualityGlossary::RecordsAndData

### Usage
Archiving is a controlled process with its own records, not a location. Moving files to cheaper storage is not archiving.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Retention Period

### Summary
The length of time a record must be kept, set by the regulation that requires it and by the life of the product it concerns.

### Description
The retention period is determined by the applicable regulation and by the product, not by storage cost or system lifetime. GMP batch records are retained for at least one year beyond the product's expiry date, and longer where national law or the product's own lifecycle requires; clinical trial records and pharmacovigilance records carry their own, often longer, periods. The retention period sets the horizon against which the Legible, Enduring and Available attributes are assessed, and it routinely outlives the systems that produced the data.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::RetentionPeriod

### Folders
- CollectionFolder::DataQualityGlossary::RecordsAndData

### Usage
State the retention period for every category of GxP record, and assess system replacement plans against it rather than against the system's supported life.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 8: Controls and Evidence

An attribute that cannot be demonstrated to an inspector has not been achieved.  These are the mechanisms through which the attributes are both achieved and evidenced.

___

## Create Glossary Term

### Display Name
Audit Trail

### Summary
A secure, computer-generated, time-stamped record of who did what to a record, and why.

### Description
An audit trail records the creation, modification and deletion of data, capturing the original value, the new value, the identity of the person responsible, the date and time, and — where the change is to previously entered GxP data — the reason. It must be generated by the system rather than by the user, must not be alterable or disableable by ordinary users, and must be retained for as long as the record it describes. The audit trail is part of the record: it is what makes Attributable, Complete and Traceable demonstrable rather than merely asserted.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::AuditTrail

### Folders
- CollectionFolder::DataQualityGlossary::ControlsAndEvidence

### Usage
The ability of any user to disable the audit trail is a critical finding. Verify it during system qualification and confirm it periodically thereafter.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Audit Trail Review

### Summary
The documented examination of audit trail entries as part of the routine review of the data they relate to.

### Description
An audit trail is only a control if somebody reads it. Audit trail review is the examination of the relevant entries — changes to results, aborted or repeated runs, altered acquisition parameters, deletions, and access outside normal working patterns — carried out as part of the routine review of the record, at a frequency and depth based on the criticality of the data. The review is itself recorded, so that the fact of it and its outcome can be shown. Reviewing only when a problem is already suspected is not audit trail review.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::AuditTrailReview

### Folders
- CollectionFolder::DataQualityGlossary::ControlsAndEvidence

### Usage
Define what is reviewed, by whom and how often, for each system holding GxP-critical data. Risk-based scoping is expected; absence of scoping is not.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Electronic Signature

### Summary
A computer-generated signing of a record that is the legally binding equivalent of a handwritten signature.

### Description
An electronic signature is applied by an identified individual through a system that verifies who they are, and is permanently bound to the specific record it signs so that it cannot be transferred, copied or repudiated. The signature record must capture the signatory's printed name, the date and time, and the meaning of the signing. Regulations set the requirements: EU GMP Annex 11 in Europe and 21 CFR Part 11 in the United States. An electronic signature that can be applied without re-authentication, or that is not bound to the specific record, does not meet them.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::ElectronicSignature

### Folders
- CollectionFolder::DataQualityGlossary::ControlsAndEvidence

### Usage
Verify the binding between the signature and the exact data signed during qualification. This is the point at which hybrid processes most often fail.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Meaning of Signature

### Summary
The stated reason a record was signed — performed, checked, reviewed or approved.

### Description
Every signature, handwritten or electronic, must state what the signatory is attesting to: that they performed the work, that they checked it, that they reviewed it, or that they approve it. A signature without a stated meaning does not identify what responsibility has been taken, and is not acceptable for a GxP record. The distinction matters in practice because performing and checking a step must be different people, and only the meaning of the signature shows which of them each signatory was.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::MeaningOfSignature

### Folders
- CollectionFolder::DataQualityGlossary::ControlsAndEvidence

### Usage
Design signature fields with an explicit meaning rather than a bare signature box, in both electronic systems and paper forms.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Second Person Review

### Summary
Independent verification by a second qualified person that a critical step was performed and recorded correctly.

### Description
Second person review is the check applied to critical steps — material dispensing, calculation of a reported result, transcription between systems, and changes to critical process parameters. The reviewer must be qualified to judge the work and independent of the person who performed it, and their check is recorded with a signature whose meaning identifies it as a check rather than as performance of the step. It is a control on Accurate, but it produces evidence for Attributable as well, because it names two people rather than one.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::SecondPersonReview

### Folders
- CollectionFolder::DataQualityGlossary::ControlsAndEvidence

### Usage
Independence is the requirement. A review signed by someone who participated in the step is not a second person review, however senior they are.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Unique User Identity

### Summary
An account belonging to exactly one named individual, which is what makes attribution to a person possible.

### Description
Every user of a GxP computerised system must have an account that identifies them individually, with credentials that are not shared and access rights matched to their role. Unique identity is the mechanism through which the Attributable attribute is achieved in electronic systems: without it, the audit trail records an account rather than a person and cannot answer who did the work. Accounts are created, modified and removed under a controlled process, and are removed promptly when someone changes role or leaves.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::UniqueUserIdentity

### Folders
- CollectionFolder::DataQualityGlossary::ControlsAndEvidence

### Usage
Periodic review of active accounts against current employment and role is the routine check. Orphaned accounts break attribution retrospectively as well as prospectively.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Shared Login

### Summary
A single account used by more than one person — a prohibited practice, because it destroys attribution.

### Description
A shared login is an account whose credentials are known to several people, including generic operator accounts and default instrument accounts. Where one is used, the audit trail records the account and not the individual, so no entry made through it can be attributed to a person and every ALCOA attribute that depends on attribution fails with it. Shared logins are prohibited for GxP systems at Coco Pharmaceuticals. Legacy instruments incapable of supporting individual accounts are recorded on the data integrity risk register with a documented compensating control and a remediation date.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::SharedLogin

### Folders
- CollectionFolder::DataQualityGlossary::ControlsAndEvidence

### Usage
The term names a practice to be eliminated, not one to be managed. It is defined here so that findings and remediation plans can refer to it precisely.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Time Synchronisation

### Summary
Keeping the clocks of all GxP systems aligned to a single trusted time source.

### Description
Timestamps are only evidence if the clocks that produced them agree. All GxP computerised systems and instruments must take their time from a common trusted source, users must not be able to alter the system clock, and the time zone must be recorded so that entries made across sites remain comparable. Without synchronisation the Contemporaneous attribute cannot be demonstrated, and cross-system Consistent checks produce sequences of events that the process could not have followed.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::TimeSynchronisation

### Folders
- CollectionFolder::DataQualityGlossary::ControlsAndEvidence

### Usage
Include clock source, user privilege over the clock, and time zone handling in system qualification. Legacy standalone instruments are the usual gap.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Access Control

### Summary
Restricting what each user can see and do in a system to what their role requires.

### Description
Access control assigns privileges by role, so that the ability to modify data, to alter configuration, to change acquisition or processing methods, and to administer the system is held only by those who need it. Administrator rights, which typically include the ability to alter or delete data and to change audit trail settings, must not be held by the people who generate or review the data in the ordinary course of their work. Access rights are granted under a controlled process and reviewed periodically.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::AccessControl

### Folders
- CollectionFolder::DataQualityGlossary::ControlsAndEvidence

### Usage
Separation of the administrator role from the data generator role is the specific expectation. Analysts holding administrator rights on their own instrument is the most frequently cited example of its absence.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Data Integrity Deviation

### Summary
A departure from the required data integrity controls, raised, investigated and remediated through the quality system.

### Description
A data integrity deviation is any instance where the required controls were not met — a missing or late entry, an unexplained change, an unreviewed audit trail, a shared login, a record that cannot be located, or an inconsistency between systems that cannot be reconciled. It is raised in the quality system like any other deviation, and its investigation maps the concern against the ALCOA+ attributes to identify which control failed and why. The outcome distinguishes a training gap from a system defect from an expectation that was never achievable as written, and drives corrective and preventive action accordingly.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::DataIntegrityDeviation

### Folders
- CollectionFolder::DataQualityGlossary::ControlsAndEvidence

### Usage
Where an investigation concludes that a record was altered or omitted deliberately, the matter ceases to be a deviation and is handled as falsification.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

___

## Create Glossary Term

### Display Name
Falsification

### Summary
The deliberate creation, alteration, omission or destruction of a record so that it misrepresents what happened.

### Description
Falsification is the intentional misrepresentation of a record: fabricating a result, altering one after the fact to make it pass, back-dating an entry, signing for work performed by someone else, deleting an inconvenient run, or reporting selectively from repeated tests. It is distinguished from error and from a control failure by intent, and it is treated as misconduct rather than as a quality deviation. Regulators treat evidence of falsification as a finding about the organisation's culture rather than about the individual record, which is why an environment where people feel pressured to produce a passing result is itself a data integrity risk.

### Glossary Name
Glossary::DataQualityGlossary

### Qualified Name
Glossary::DataQualityGlossary::Falsification

### Folders
- CollectionFolder::DataQualityGlossary::ControlsAndEvidence

### Usage
Handled under the human resources disciplinary process alongside the quality investigation. The term is defined here so that the two routes can be named separately and neither is used to stand in for the other.

### Authors
- Erin Overview
- Florence Paynter

### Version Identifier
1.0

### Content Status
ACTIVE

___

---

## Part 9: Term Relationships

The relationships record two things: how the three framework versions relate to each other and to their attributes, and which supporting term each attribute is achieved or evidenced through.  The second of these is what makes the glossary usable when writing a rule — it answers *what would I have to measure to test this attribute?*

### 9.1 The frameworks and their attributes

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::ALCOAPlus

### Term 2
Glossary::DataQualityGlossary::ALCOA

### Expression
extends

### Source
EU and PIC/S data integrity guidance.

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::ALCOAPlusPlus

### Term 2
Glossary::DataQualityGlossary::ALCOAPlus

### Expression
extends

### Source
EMA guideline on computerised systems and electronic data in clinical trials, 2023.

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::ALCOA

### Term 2
Glossary::DataQualityGlossary::DataIntegrity

### Expression
is a framework for assessing

### Steward
Erin Overview

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Attributable

### Term 2
Glossary::DataQualityGlossary::ALCOA

### Expression
is an attribute of

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Legible

### Term 2
Glossary::DataQualityGlossary::ALCOA

### Expression
is an attribute of

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Contemporaneous

### Term 2
Glossary::DataQualityGlossary::ALCOA

### Expression
is an attribute of

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Original

### Term 2
Glossary::DataQualityGlossary::ALCOA

### Expression
is an attribute of

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Accurate

### Term 2
Glossary::DataQualityGlossary::ALCOA

### Expression
is an attribute of

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Complete

### Term 2
Glossary::DataQualityGlossary::ALCOAPlus

### Expression
is an attribute added by

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Consistent

### Term 2
Glossary::DataQualityGlossary::ALCOAPlus

### Expression
is an attribute added by

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Enduring

### Term 2
Glossary::DataQualityGlossary::ALCOAPlus

### Expression
is an attribute added by

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Available

### Term 2
Glossary::DataQualityGlossary::ALCOAPlus

### Expression
is an attribute added by

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Traceable

### Term 2
Glossary::DataQualityGlossary::ALCOAPlusPlus

### Expression
is the attribute added by

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

### 9.2 How each attribute is achieved and evidenced

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Attributable

### Term 2
Glossary::DataQualityGlossary::UniqueUserIdentity

### Expression
is achieved in electronic systems by

### Steward
Erin Overview

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Attributable

### Term 2
Glossary::DataQualityGlossary::AuditTrail

### Expression
is evidenced by

### Steward
Erin Overview

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
Antonym

### Term 1
Glossary::DataQualityGlossary::SharedLogin

### Term 2
Glossary::DataQualityGlossary::UniqueUserIdentity

### Expression
a shared login is the absence of unique user identity, and defeats attribution entirely

### Source
Data integrity working session, Erin Overview with the manufacturing quality team.

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Contemporaneous

### Term 2
Glossary::DataQualityGlossary::TimeSynchronisation

### Expression
cannot be demonstrated without

### Steward
Erin Overview

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Original

### Term 2
Glossary::DataQualityGlossary::RawData

### Expression
is satisfied by retaining

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::TrueCopy

### Term 2
Glossary::DataQualityGlossary::Original

### Expression
may be retained in place of

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::SourceData

### Term 2
Glossary::DataQualityGlossary::RawData

### Expression
is the clinical equivalent of — same obligations, different regulatory vocabulary

### Source
Agreed with drug development when the two glossaries were compared.

### Steward
Erin Overview

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
Antonym

### Term 1
Glossary::DataQualityGlossary::Falsification

### Term 2
Glossary::DataQualityGlossary::Accurate

### Expression
falsification is the deliberate defeat of accuracy, and is handled as misconduct rather than as a quality deviation

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Complete

### Term 2
Glossary::DataQualityGlossary::AuditTrail

### Expression
includes

### Steward
Erin Overview

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Complete

### Term 2
Glossary::DataQualityGlossary::Metadata

### Expression
includes

### Steward
Erin Overview

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Enduring

### Term 2
Glossary::DataQualityGlossary::Archive

### Expression
is principally satisfied in

### Steward
Erin Overview

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Available

### Term 2
Glossary::DataQualityGlossary::Archive

### Expression
is principally satisfied in

### Steward
Erin Overview

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Enduring

### Term 2
Glossary::DataQualityGlossary::RetentionPeriod

### Expression
is assessed against

### Steward
Erin Overview

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Traceable

### Term 2
Glossary::DataQualityGlossary::Metadata

### Expression
is carried by

### Steward
Erin Overview

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::Accurate

### Term 2
Glossary::DataQualityGlossary::SecondPersonReview

### Expression
is controlled for critical steps by

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

### 9.3 The supporting terms

___

## Link Term-Term Relationship

### Relationship Type
ISARelationship

### Term 1
Glossary::DataQualityGlossary::StaticRecord

### Term 2
Glossary::DataQualityGlossary::ElectronicRecord

### Steward
Erin Overview

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
ISARelationship

### Term 1
Glossary::DataQualityGlossary::DynamicRecord

### Term 2
Glossary::DataQualityGlossary::ElectronicRecord

### Steward
Erin Overview

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
Antonym

### Term 1
Glossary::DataQualityGlossary::DynamicRecord

### Term 2
Glossary::DataQualityGlossary::StaticRecord

### Expression
the distinction decides whether a printout can be retained in place of the electronic original

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::HybridSystem

### Term 2
Glossary::DataQualityGlossary::ElectronicSignature

### Expression
the binding between the paper signature and the electronic data is where a hybrid is at risk

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::MeaningOfSignature

### Term 2
Glossary::DataQualityGlossary::ElectronicSignature

### Expression
is a required part of

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::AuditTrailReview

### Term 2
Glossary::DataQualityGlossary::AuditTrail

### Expression
is what makes an audit trail a control rather than a log

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
Antonym

### Term 1
Glossary::DataQualityGlossary::Backup

### Term 2
Glossary::DataQualityGlossary::Archive

### Expression
a backup exists to recover current data and is overwritten; an archive exists to satisfy retention and is not — confusing the two is a recurring inspection finding

### Source
Data integrity working session, Erin Overview with the manufacturing quality team.

### Steward
Erin Overview

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::DataIntegrityRisk

### Term 2
Glossary::DataQualityGlossary::DataCriticality

### Expression
is assessed from

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::DataIntegrityDeviation

### Term 2
Glossary::DataQualityGlossary::DataIntegrity

### Expression
is raised when the controls protecting

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::GoodDocumentationPractice

### Term 2
Glossary::DataQualityGlossary::ALCOA

### Expression
is how the attributes of

### Steward
Florence Paynter

### Term Relationship Status
ACTIVE

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::DataQualityGlossary::DataLifecycle

### Term 2
Glossary::DataQualityGlossary::ALCOAPlus

### Expression
is the scope over which

### Steward
Erin Overview

### Term Relationship Status
ACTIVE

___

---

## What the glossary is for

The point of writing these definitions down was to make the quality expectations measurable.  With the words agreed,
the data quality analysts could write rules that name an attribute and mean something specific by it: a
contemporaneous rule comparing activity time with entry time, a consistent rule reconciling dispensed quantity across
the warehouse and batch record systems, a complete rule looking for repeat runs that appear in the audit trail but
not in the reported result.

Three of the attributes resisted that treatment and are worth naming as such.  **Accurate** cannot be tested directly
— rules can only test the conditions it depends on.  **Legible** and **Enduring** are assessed against the end of the
retention period rather than against today, so the measurement is of the controls rather than of the record.  Those
three are audited rather than monitored, which is the distinction between the framework used as an audit tool and the
framework used as a design tool.

The rest of the glossary — the records, the controls and the evidence — exists because an attribute stated on its own
is not actionable.  *Original* becomes actionable only once **Dynamic Record** and **True Copy** are defined, because
the two of them together are what decides whether the laboratory can keep the printout.  That question had been
argued about for a year before it was written down.
