# Coco Pharmaceuticals Employee Glossary

> **Author:** Erin Overview (Information Analyst), Faith Broker (Director of Human Resources)  
> **Version:** 1.0  
> **Status:** DRAFT  
> **Date:** 2026-08-18  
> **Description:** The first draft of the glossary for the Employee subject area, produced by Erin Overview and Faith Broker in a working session described in [Defining a glossary](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/defining-a-glossary/overview/).

---

## Overview

[Erin Overview](https://egeria-project.org/practices/coco-pharmaceuticals/personas/erin-overview/) had already created an
initial list of [subject areas for Coco Pharmaceuticals](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/defining-subject-areas/overview/).
In this session she worked with [Faith Broker](https://egeria-project.org/practices/coco-pharmaceuticals/personas/faith-broker/),
the director for human resources, on the **employee data** subject area.  This file captures the result of that session.

![Erin and Faith working together](https://raw.githubusercontent.com/odpi/egeria-docs/main/site/docs/practices/coco-pharmaceuticals/scenarios/defining-a-glossary/erin-and-faith-defining-employee-subject-area.png)

Building a glossary is iterative and collaborative.  It switches between sketching an overview of the content and
drilling down into the specifics — increasing the precision — before returning to review the overall consistency of
the definitions.  Erin and Faith's session followed exactly that rhythm, and the parts of this file follow it too:

1. **The glossary itself**, linked to the `Person: Employee` subject area.
2. **Categories** to organize the terms — in the same way that files are organized into folders on a disk.
3. **The initial list of terms** ([Figure 1](https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/defining-a-glossary/overview/)) —
   key concepts with a short description each.  Writing the descriptions revealed new concepts that needed explaining.
4. **Drilling down into Work Location** (Figure 2) — expanding one concept with the detail of the data likely to be
   associated with it.  Term relationships begin to appear here.
5. **Redefining Postal Address** (Figure 3) — the concept originally called *Address* was renamed and promoted to a
   common core type once Erin and Faith noticed the same substructure appearing in several places.
6. **Defining Manager** (Figure 4) — a specialization linked into a type hierarchy.
7. **The term relationships** that emerged from steps 4 to 6.
8. **The terms added in the follow-on sessions**, as the team expanded and each area was filled out in
   more depth - including the terms that answer the questions the first session left open.
9. **The expanded set of term relationships** connecting those new terms to each other and to the originals.

Two conventions are worth noting before loading this file:

* Every definition is created with a **content status of `DRAFT`**.  After a few hours' work Erin and Faith had a
  usable skeleton, not a finished vocabulary.  The next step is to bring in more people, walk them through the work
  so far, and incorporate their feedback.
* The **notes** column of the working sheets — the points to investigate and expand on, such as *"Includes
  contractors?"* — is carried into each definition as a **Journal Entry**, so the open questions stay attached to the
  term they belong to rather than being lost when the session ended.

`Employee Home Address`, `Supplier Address` and `Delivery Address` are included because they appear in Figure 3 as
evidence that Postal Address is reused well beyond employee data.  Only enough of each is defined here to record that
reuse; their full definitions belong to the person, supplier and distribution subject areas.

**Prerequisite:** the `SubjectArea::Person:Employee` collection must already exist in Egeria.  The subject area
collections are loaded from `CocoComboArchive.omarchive` when the metadata server starts up.

---

## Part 1: The Glossary

___

## Create Glossary

### Display Name
Employee Glossary

### Qualified Name
Glossary::EmployeeGlossary

### Description
The vocabulary used to describe the people who work for Coco Pharmaceuticals: their identity, their role, where they work and how they are paid.  It is the semantic definition of the Employee subject area.

### Language
English

### Usage
Reference this glossary when defining, sourcing or reporting on employee data, so that terms such as Employee, Manager, Work Location and Compensation Plan carry the same meaning in every system and every conversation.

### Purpose
To establish agreed, precise definitions for the concepts used in employee data, as the foundation for consistent human resources data across Coco Pharmaceuticals.

### Search Keywords
- Employee
- Human Resources
- Subject Area

### URL
https://egeria-project.org/practices/coco-pharmaceuticals/scenarios/defining-a-glossary/overview/

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Add Member to Collection

### Element Id
Glossary::EmployeeGlossary

### Membership Rationale
Links the Employee subject area to the glossary that defines its vocabulary.

### Membership Status
PROPOSED

### Collection Id
SubjectArea::Person:Employee

___

---

## Part 2: Organizing the Glossary

As new terms are defined, Erin organizes them into categories, in a similar way to organizing files into directories
on a disk.  A term can appear in more than one category — in fact it can appear in categories belonging to other
glossaries, which is how a common core type such as Postal Address gets shared.

___

## Create Collection Folder

### Display Name
Employment

### Qualified Name
CollectionFolder::EmployeeGlossary::Employment

### Description
The concepts describing a person's employment by Coco Pharmaceuticals — who they are, how they are identified and what they do.

### Purpose
Groups the terms that identify an employee and describe their role.

### Parent ID
Glossary::EmployeeGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Erin Overview
- Faith Broker

### Content Status
DRAFT

___

---

___

## Create Collection Folder

### Display Name
Compensation

### Qualified Name
CollectionFolder::EmployeeGlossary::Compensation

### Description
The concepts describing what an employee receives in exchange for their time and effort working for the organization.

### Purpose
Groups the terms covering pay, salary and additional payments.

### Parent ID
Glossary::EmployeeGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Erin Overview
- Faith Broker

### Content Status
DRAFT

___

---

___

## Create Collection Folder

### Display Name
Work Locations

### Qualified Name
CollectionFolder::EmployeeGlossary::WorkLocations

### Description
The concepts describing where an employee is based, and how the organization's work locations are identified and classified.

### Purpose
Groups the terms produced when Work Location was expanded in detail.

### Parent ID
Glossary::EmployeeGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Erin Overview
- Faith Broker

### Content Status
DRAFT

___

---

___

## Create Collection Folder

### Display Name
Addresses

### Qualified Name
CollectionFolder::EmployeeGlossary::Addresses

### Description
Postal Address and the concepts that make it up, together with the different kinds of address that are defined by it.  These are common core definitions, reused well beyond employee data.

### Purpose
Groups the common address definitions that emerged when the same substructure was found in several places.

### Parent ID
Glossary::EmployeeGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Erin Overview
- Faith Broker

### Content Status
DRAFT

___

---

___

## Create Collection Folder

### Display Name
Personal Details

### Qualified Name
CollectionFolder::EmployeeGlossary::PersonalDetails

### Description
The concepts describing an employee as a person rather than as a job holder - their name, their date of birth, the identifiers issued to them by government, and how to contact them.

### Purpose
Groups the terms that are personal data, so that the privacy controls they need can be applied to the whole folder.

### Parent ID
Glossary::EmployeeGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Erin Overview
- Faith Broker

### Content Status
DRAFT

___

---
___

## Create Collection Folder

### Display Name
Working Time and Absence

### Qualified Name
CollectionFolder::EmployeeGlossary::WorkingTime

### Description
The concepts describing when an employee is expected to work, when they actually worked, and the periods when they are away from work.

### Purpose
Groups the terms covering working patterns, recorded time, leave and absence.

### Parent ID
Glossary::EmployeeGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Erin Overview
- Faith Broker

### Content Status
DRAFT

___

---
___

## Create Collection Folder

### Display Name
Performance and Development

### Qualified Name
CollectionFolder::EmployeeGlossary::PerformanceDevelopment

### Description
The concepts describing how an employee's performance is assessed, what they are expected to be able to do, and how those capabilities are developed and evidenced.

### Purpose
Groups the terms covering reviews, objectives, competencies, qualifications and training.

### Parent ID
Glossary::EmployeeGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Erin Overview
- Faith Broker

### Content Status
DRAFT

___

---
## Part 3: The Initial List of Key Concepts

Erin and Faith began by identifying the key concepts and writing a short description for each one.  Each of these
concepts is recorded here as a glossary term.  Writing the descriptions was harder than expected — being precise
about words used every day takes effort — but it got easier as the core concepts already defined could be reused in
the definitions of new terms.

___

## Create Glossary Term

### Display Name
Employee

### Summary
A person who works for the organization under an employment contract.

### Description
A person who works for the organization.  They have an employment contract.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::Employee

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Journal Entry
Open question from the first working session: does this term include contractors?  Contractors work for Coco Pharmaceuticals but not under an employment contract, so either the description needs to broaden or a separate term is needed.

### Is Abstract Concept
False

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Manager

### Summary
An employee who is responsible for managing other employees.

### Description
A person that is responsible for managing other employees.  All employees have a manager except founders.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::Manager

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Journal Entry
Open question from the first working session: what about team leaders?  They direct the day-to-day work of others without the formal responsibilities of a manager, so it is not yet clear whether they are Managers, a specialization of Manager, or a separate concept.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Employee Id

### Summary
A unique identifier for an employee.

### Description
A unique identifier for an employee.  It is needed because two employees may have the same name, or an employee may change their name.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::EmployeeId

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Journal Entry
Open question from the first working session: is this really an identifier for the person, or for the employment contract?  Need to check what happens when someone leaves and is later re-hired — do they keep their original Employee Id?

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Employee Name

### Summary
The name that an employee wants to be known as.

### Description
The name that an employee wants to be known as.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::EmployeeName

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Journal Entry
Open question from the first working session: this needs to be split up into first name, middle names and last name.  The structure seems common to all people, not just employees, so it may belong in a shared core definition.  Also need to distinguish legal name from known name.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Job Title

### Summary
A short description of an employee's responsibilities.

### Description
A short description of an employee's responsibilities.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::JobTitle

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Compensation Plan

### Summary
The agreed benefits given to an employee in exchange for their work.

### Description
The agreed benefits that will be given to an employee in exchange for their time and effort working for the organization.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::CompensationPlan

### Folders
- CollectionFolder::EmployeeGlossary::Compensation

### Is Abstract Concept
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Annual Salary

### Summary
A type of compensation paid as one twelfth of an annual amount each month.

### Description
A type of compensation where an employee is paid 1/12th of an annual amount for each month they work.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::AnnualSalary

### Folders
- CollectionFolder::EmployeeGlossary::Compensation

### Journal Entry
Noted in the first working session: most employees are compensated this way.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Hourly Pay Rate

### Summary
A type of compensation where the employee is paid for every hour they work.

### Description
A type of compensation where the employee is paid for every hour they work.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::HourlyPayRate

### Folders
- CollectionFolder::EmployeeGlossary::Compensation

### Journal Entry
Noted in the first working session: used in manufacturing.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Bonus

### Summary
An additional payment made to an employee for service beyond their core role.

### Description
Additional payment made to an employee for additional service beyond their core role.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::Bonus

### Folders
- CollectionFolder::EmployeeGlossary::Compensation

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

## Part 4: Drilling Down — Work Location

Taking each concept in turn, Erin and Faith fleshed out more detail.  Work Location was the first to be expanded with
the detail of the data likely to be associated with it, and this is where term relationships started to appear.  As
more detail was created, new related concepts emerged — Work Location Code, Work Location Type and Work Location
Address are all children of this exercise.

___

## Create Glossary Term

### Display Name
Work Location

### Summary
The place where an employee is based.

### Description
The office where an employee is based.  They may visit, or work from, other locations.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::WorkLocation

### Folders
- CollectionFolder::EmployeeGlossary::WorkLocations

### Journal Entry
Refined in the first working session: work locations have a code and an address.  Not all work locations are offices, and some employees work at home — so the description above is too narrow and needs revisiting.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Work Location Code

### Summary
Unique identifier for one of the organization's work locations.

### Description
Unique identifier for one of the organization's work locations.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::WorkLocationCode

### Folders
- CollectionFolder::EmployeeGlossary::WorkLocations

### Journal Entry
Noted in the first working session: the code set includes codes for business partners — hospitals, for example — where Coco Pharmaceuticals employees may be based.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Work Location Type

### Summary
Unique identifier for the type of a work location.

### Description
Unique identifier for the type of work location.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::WorkLocationType

### Folders
- CollectionFolder::EmployeeGlossary::WorkLocations

### Example
Office, manufacturing plant, warehouse, hospital, home.

### Journal Entry
Noted in the first working session: the value set includes codes for offices, manufacturing plant, warehouse, hospital and home.  The full set should become a valid value set.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Work Location Address

### Summary
The postal address of a specific work location.

### Description
The postal address of a specific work location.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::WorkLocationAddress

### Folders
- CollectionFolder::EmployeeGlossary::WorkLocations
- CollectionFolder::EmployeeGlossary::Addresses

### Journal Entry
Noted in the first working session: the detailed definition of the address content is held in the Postal Address term, not repeated here.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

## Part 5: Redefining Postal Address

Working through Work Location surfaced the same address substructure that had already appeared elsewhere.  The
concept originally listed simply as *Address* was renamed **Postal Address**, given a precise definition, broken down
into its parts, and promoted to a common core type that the specific kinds of address are defined by.  This is the
point at which the glossary started to pay for itself: the addresses used for employees' homes, for suppliers and
for deliveries no longer each need their own structural definition.

___

## Create Glossary Term

### Display Name
Postal Address

### Aliases
- Address

### Summary
The description of a location that can be used to find it, or to send post to it.

### Description
The description of a location that can be used to locate the place — to visit it, for example, or to send a letter or parcel to it using the postal services.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::PostalAddress

### Folders
- CollectionFolder::EmployeeGlossary::Addresses

### Usage
Use Postal Address as the common definition of address structure.  A specific kind of address — a work location's address, an employee's home address, a supplier's address, a delivery address — is defined by this term rather than restating its content.

### Journal Entry
This term began the first working session as "Address", with the note that there are lots of different types of addresses.  It was renamed to Postal Address and promoted to a common core type once the same substructure was found in several places.

### Is Abstract Concept
False

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Building Name

### Summary
The name identifying a building within a postal address.

### Description
The name of the building that a postal address refers to, where the building is identified by name rather than, or in addition to, a street number.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::BuildingName

### Folders
- CollectionFolder::EmployeeGlossary::Addresses

### Journal Entry
Identified when Postal Address was broken down in the first working session.  The description here is provisional and needs review with the teams that already hold address data.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Street Number

### Summary
The number identifying a property along a street.

### Description
The number that identifies a particular property along a street, within a postal address.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::StreetNumber

### Folders
- CollectionFolder::EmployeeGlossary::Addresses

### Journal Entry
Identified when Postal Address was broken down in the first working session.  The description here is provisional and needs review with the teams that already hold address data.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Street Name

### Summary
The name of the street that a postal address is located on.

### Description
The name of the street that the property identified by a postal address is located on.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::StreetName

### Folders
- CollectionFolder::EmployeeGlossary::Addresses

### Journal Entry
Identified when Postal Address was broken down in the first working session.  The description here is provisional and needs review with the teams that already hold address data.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Employee Home Address

### Summary
The postal address of the place where an employee lives.

### Description
The postal address of the place where an employee lives.  Its content is defined by Postal Address.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::EmployeeHomeAddress

### Folders
- CollectionFolder::EmployeeGlossary::Addresses
- CollectionFolder::EmployeeGlossary::Employment

### Journal Entry
Recorded in the first working session as one of the kinds of address that reuse Postal Address.  This is personal data and will need a confidentiality classification before the term is finalized.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Supplier Address

### Summary
The postal address of a supplier to Coco Pharmaceuticals.

### Description
The postal address of a supplier to Coco Pharmaceuticals.  Its content is defined by Postal Address.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::SupplierAddress

### Folders
- CollectionFolder::EmployeeGlossary::Addresses

### Journal Entry
Recorded in the first working session only as evidence that Postal Address is reused outside employee data.  The full definition belongs to the Organization: Supplier subject area and should be moved there when that glossary is built.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Delivery Address

### Summary
The postal address that goods are to be delivered to.

### Description
The postal address that goods are to be delivered to.  Its content is defined by Postal Address.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::DeliveryAddress

### Folders
- CollectionFolder::EmployeeGlossary::Addresses

### Journal Entry
Recorded in the first working session only as evidence that Postal Address is reused outside employee data.  The full definition belongs to the Service Quality: Distribution subject area and should be moved there when that glossary is built.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

## Part 6: Term Relationships

The relationships below are the ones that emerged while drilling down.  They were not visible in the initial flat
list of concepts — they only appeared once Erin and Faith started expanding individual terms.  Three kinds are used:

* **Is A Type Of** — a specialization linked into a type hierarchy, as when Manager was recognized as a kind of Employee.
* **Has A** — a term that is made up of other terms, as when Work Location and Postal Address were broken down.
* **Typed By** — a specific term whose content is defined by a common core type, as when the various kinds of address were defined by Postal Address.

All of these are created with a relationship status of `DRAFT`, matching the terms they connect.

### 6.1 Defining Manager

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::Manager

### Term 2
Glossary::EmployeeGlossary::Employee

### Source
Erin Overview and Faith Broker, employee subject area working session — Figure 4, Defining Manager.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

### 6.2 Refining Work Location

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::WorkLocation

### Term 2
Glossary::EmployeeGlossary::WorkLocationAddress

### Source
Erin Overview and Faith Broker, employee subject area working session — Figure 2, Refining Work Location.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::WorkLocation

### Term 2
Glossary::EmployeeGlossary::WorkLocationCode

### Source
Erin Overview and Faith Broker, employee subject area working session — Figure 2, Refining Work Location.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::WorkLocation

### Term 2
Glossary::EmployeeGlossary::WorkLocationType

### Source
Erin Overview and Faith Broker, employee subject area working session — Figure 2, Refining Work Location.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermTYPEDBYRelationship

### Term 1
Glossary::EmployeeGlossary::WorkLocationAddress

### Term 2
Glossary::EmployeeGlossary::PostalAddress

### Source
Erin Overview and Faith Broker, employee subject area working session — Figure 2, Refining Work Location.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

### 6.3 Redefining Postal Address

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::PostalAddress

### Term 2
Glossary::EmployeeGlossary::BuildingName

### Source
Erin Overview and Faith Broker, employee subject area working session — Figure 3, Redefining Postal Address.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::PostalAddress

### Term 2
Glossary::EmployeeGlossary::StreetNumber

### Source
Erin Overview and Faith Broker, employee subject area working session — Figure 3, Redefining Postal Address.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::PostalAddress

### Term 2
Glossary::EmployeeGlossary::StreetName

### Source
Erin Overview and Faith Broker, employee subject area working session — Figure 3, Redefining Postal Address.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermTYPEDBYRelationship

### Term 1
Glossary::EmployeeGlossary::EmployeeHomeAddress

### Term 2
Glossary::EmployeeGlossary::PostalAddress

### Source
Erin Overview and Faith Broker, employee subject area working session — Figure 3, Redefining Postal Address.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermTYPEDBYRelationship

### Term 1
Glossary::EmployeeGlossary::SupplierAddress

### Term 2
Glossary::EmployeeGlossary::PostalAddress

### Source
Erin Overview and Faith Broker, employee subject area working session — Figure 3, Redefining Postal Address.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermTYPEDBYRelationship

### Term 1
Glossary::EmployeeGlossary::DeliveryAddress

### Term 2
Glossary::EmployeeGlossary::PostalAddress

### Source
Erin Overview and Faith Broker, employee subject area working session — Figure 3, Redefining Postal Address.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

## Part 7: Filling Out the Glossary

Erin and Faith's own conclusion was that a glossary is not the work of a committee: two or three experts lay out the
core concepts, and only then do you bring in more people, take them through the work so far, and expand it with them.
This part is the result of doing that. The terms below were added in the follow-on sessions, as members of the human
resources, payroll, facilities and learning teams were brought in and worked on the sections they know best.

They are still authored by Erin and Faith - Erin as the information analyst holding the glossary together, Faith as
the subject matter authority - and they are still `DRAFT`. Several of them exist specifically to answer questions the
first session left open:

* **Worker** answers *"Includes contractors?"* - it is the broader concept that covers employees and contractors
  alike, which lets Employee keep its precise definition.
* **Team Leader** answers *"What about team leaders?"* - the proposal being that a team leader is a type of employee
  but not a type of manager.
* **Legal Name**, **Known Name**, **First Name**, **Middle Name** and **Last Name** answer *"Need to split up into
  first name, middle names, last name... Legal name vs known name?"*.
* **Employment Contract** is what makes the Employee Id question answerable: a person may hold more than one
  employment contract over time, which is exactly what happens when someone leaves and is re-hired.
* **Office**, **Manufacturing Plant**, **Warehouse** and **Home Working Location** answer the note that not all work
  locations are offices and that some employees work at home.
* **Address Line**, **City**, **Region**, **Postal Code** and **Country** complete the breakdown of Postal Address
  that Figure 3 started.

Notice how many of the new journal entries are about privacy and about country-by-country variation. Neither was
visible in the first session; both surfaced as soon as the definitions got specific enough to be argued with.

### 7.1 Employment

___

## Create Glossary Term

### Display Name
Worker

### Summary
A person who performs work for Coco Pharmaceuticals, whether or not they are employed by it.

### Description
A person who performs work for Coco Pharmaceuticals. This covers employees, who work under an employment contract, and contractors, who work under a contract for services. It is deliberately broader than Employee so that the data describing the people doing the work can be defined once.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::Worker

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Journal Entry
Proposed in a follow-on session as the answer to the open question recorded against Employee - "Includes contractors?". Introducing Worker as the broader concept lets Employee keep its precise definition (a person with an employment contract) while still giving the organization a single term for everyone who does its work. Needs confirmation with HR and with the supplier management team.

### Is Abstract Concept
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Contractor

### Summary
A person who works for Coco Pharmaceuticals under a contract for services rather than an employment contract.

### Description
A person who performs work for Coco Pharmaceuticals under a contract for services rather than an employment contract. Contractors are usually engaged for a defined piece of work or a fixed period, often through an agency or through their own company, and are not entitled to employee benefits.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::Contractor

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Journal Entry
Much contractor data is held in supplier and procurement systems rather than in the HR systems, so the authoritative source for a contractor is not the same as for an employee. This needs working through with the supplier management team.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Team Leader

### Summary
An employee who directs the day-to-day work of a team without full line management responsibility.

### Description
An employee who directs the day-to-day work of a team - allocating tasks, setting priorities and reporting progress - without holding the formal line management responsibilities for pay, performance assessment, hiring and discipline that a manager holds.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::TeamLeader

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Journal Entry
This term is the proposed answer to the open question recorded against Manager - "What about team leaders?". The proposal is that a team leader is a type of employee but NOT a type of manager, because they do not hold the responsibilities that define a manager. Faith Broker to confirm with the HR policy team before this is settled.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Founder

### Summary
One of the people who founded Coco Pharmaceuticals.

### Description
One of the people who founded Coco Pharmaceuticals. Founders are the exception to the rule that every employee has a manager.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::Founder

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Journal Entry
Identified from the note on Manager that all employees have a manager except founders. Needs checking against the current board structure - a founder who is also an executive may in practice report to the board rather than to no one at all.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Employment Contract

### Summary
The agreement between Coco Pharmaceuticals and an employee that sets out the terms of their employment.

### Description
The agreement between Coco Pharmaceuticals and an employee that sets out the terms on which they are employed: the job title and job grade they are engaged at, when the employment starts and ends, the compensation plan that applies, the working pattern expected and the notice either party must give to end it.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::EmploymentContract

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Journal Entry
Emerged directly from the description of Employee - "they have an employment contract". Making the contract a term of its own is what allows the open question on Employee Id to be resolved: an employee may hold more than one employment contract over time if they leave and are re-hired.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Employment Type

### Summary
The nature of an employment contract.

### Description
The nature of an employment contract - whether it is open-ended or runs for a defined period, and whether it is a training arrangement.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::EmploymentType

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Example
Permanent, fixed term, apprenticeship, internship, secondment.

### Journal Entry
The full set of values should become a valid value set once agreed.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Employment Status

### Summary
The current standing of a person's employment with Coco Pharmaceuticals.

### Description
The current standing of a person's employment with Coco Pharmaceuticals, used to determine which HR processes apply to them and whether they should have access to systems and buildings.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::EmploymentStatus

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Example
Applicant, offer accepted, probation, active, on leave, notice period, left.

### Journal Entry
The security team have an interest in this term: access revocation is driven from the transition to "notice period" and "left". Needs review with them before the value set is fixed.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Employment Start Date

### Summary
The date on which a person's employment with Coco Pharmaceuticals begins.

### Description
The date on which a person's employment with Coco Pharmaceuticals begins, as recorded on their employment contract.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::EmploymentStartDate

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Journal Entry
Needs to be distinguished from a continuous service date. Where someone leaves and is later re-hired they have two employment start dates, but their entitlements may be calculated from the first. This is the same underlying issue as the open question on Employee Id.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Employment End Date

### Summary
The date on which a person's employment with Coco Pharmaceuticals ends.

### Description
The date on which a person's employment with Coco Pharmaceuticals ends, whether because the employee resigned, the contract reached its end, or the employment was terminated.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::EmploymentEndDate

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Journal Entry
This date starts a number of retention clocks - payroll records, personal data, and access logs are all retained for different periods after it. Needs review with the privacy team.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Notice Period

### Summary
The warning either party must give before ending an employment contract.

### Description
The amount of warning that Coco Pharmaceuticals or the employee must give the other before ending the employment contract. It usually lengthens with job grade and with length of service.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::NoticePeriod

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Probation Period

### Summary
An initial period of employment during which suitability for the role is assessed.

### Description
An initial period at the start of an employment contract during which the employee's suitability for the role is assessed and either party may end the contract at shorter notice than normal.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::ProbationPeriod

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Business Unit

### Summary
One of the operating divisions of Coco Pharmaceuticals that an employee is assigned to.

### Description
One of the operating divisions of Coco Pharmaceuticals. Every employee is assigned to a business unit, which determines much of the reporting, budgeting and access control that applies to them.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::BusinessUnit

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Example
Research, clinical trials, manufacturing, distribution, sales, finance, information technology.

### Journal Entry
A business unit is an organizational concept rather than a purely employee one, so this term probably belongs in a shared organization glossary. Recorded here because employee data cannot be described without it.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Team

### Summary
A group of employees who work together on a shared set of responsibilities.

### Description
A group of employees within a business unit who work together on a shared set of responsibilities, under a single team leader or manager.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::Team

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Job Grade

### Summary
The level assigned to a job, used to compare roles of similar scope.

### Description
The level assigned to a job, used to compare roles of similar scope and responsibility across the organization, to set the pay range that applies to the role, and to determine entitlements such as notice period and annual leave.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::JobGrade

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Direct Report

### Summary
An employee whose work is managed directly by a particular manager.

### Description
An employee whose work is managed by a particular manager, and who reports to that manager directly rather than through another manager. The set of a manager's direct reports, followed recursively, gives the organization structure beneath them.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::DirectReport

### Folders
- CollectionFolder::EmployeeGlossary::Employment

### Journal Entry
This describes a relationship between two employees rather than a property of one. It is recorded as a term so that reports and access rules can refer to it consistently, but how it is represented in data still needs designing.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---
### 7.2 Personal Details

This folder answers the open question recorded against Employee Name, and in doing so
collects the terms that are unambiguously personal data. Grouping them makes it straightforward to apply a single
set of privacy controls, and makes it obvious when a system is asking for more personal data than it needs.

___

## Create Glossary Term

### Display Name
Legal Name

### Summary
The name recorded on a person's official identity documents.

### Description
The name recorded on a person's official identity documents. It is the name that must be used on the employment contract, on payroll submissions and in any dealings with government bodies.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::LegalName

### Folders
- CollectionFolder::EmployeeGlossary::PersonalDetails

### Journal Entry
Recorded in answer to the open question on Employee Name - "Legal name vs known name?". Note that Employee Name is currently described as the name the employee wants to be known as, which is the Known Name rather than the Legal Name. The two definitions need reconciling at the next review.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Known Name

### Aliases
- Preferred Name

### Summary
The name that an employee wants to be known as at work.

### Description
The name that an employee wants to be known as at work. It may differ from their legal name for many reasons, and it is the name that should appear in directories, on email addresses, on badges and in everyday correspondence.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::KnownName

### Folders
- CollectionFolder::EmployeeGlossary::PersonalDetails

### Journal Entry
Recorded in answer to the open question on Employee Name - "Legal name vs known name?". Using the known name wherever the legal name is not strictly required is a matter of respect as well as accuracy, and should be stated as a usage rule once the term is settled.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
First Name

### Aliases
- Given Name

### Summary
The part of a person's name that identifies them within their family.

### Description
The part of a person's name that identifies them as an individual within their family.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::FirstName

### Folders
- CollectionFolder::EmployeeGlossary::PersonalDetails

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Middle Name

### Summary
An additional given name recorded between a person's first name and last name.

### Description
Any additional given name recorded between a person's first name and last name. A person may have none, one, or several.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::MiddleName

### Folders
- CollectionFolder::EmployeeGlossary::PersonalDetails

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Last Name

### Aliases
- Family Name
- Surname

### Summary
The part of a person's name that is shared with their family.

### Description
The part of a person's name that is shared with the rest of their family.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::LastName

### Folders
- CollectionFolder::EmployeeGlossary::PersonalDetails

### Journal Entry
The first name / middle name / last name structure is not universal - naming conventions differ between cultures, and some people have a single name. Coco Pharmaceuticals employs people in many countries, so this breakdown must be reviewed before it is fixed into any system design.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Date of Birth

### Summary
The date on which an employee was born.

### Description
The date on which an employee was born. It is needed to establish eligibility for pension arrangements and certain benefits, and to distinguish between employees with the same name.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::DateOfBirth

### Folders
- CollectionFolder::EmployeeGlossary::PersonalDetails

### Journal Entry
Personal data. It should be held only where there is a specific need for it and must carry a confidentiality classification. The privacy team should review any use of it for identification, since Employee Id exists for that purpose.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
National Identifier

### Summary
The identifier issued to a person by their national government for tax and social security purposes.

### Description
The identifier issued to a person by their national government for tax and social security purposes. Payroll must report against it, so it is held for every employee, and its format differs from country to country.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::NationalIdentifier

### Folders
- CollectionFolder::EmployeeGlossary::PersonalDetails

### Example
National Insurance number (United Kingdom), Social Security number (United States).

### Journal Entry
Highly sensitive personal data. It needs a confidentiality classification, a retention rule and restricted access before any system is allowed to hold it. Must never be used as a general-purpose identifier for an employee - that is what Employee Id is for.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Work Email Address

### Summary
The email address issued to an employee by Coco Pharmaceuticals.

### Description
The email address issued to an employee by Coco Pharmaceuticals, used for all work correspondence and as their identity in many internal systems.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::WorkEmailAddress

### Folders
- CollectionFolder::EmployeeGlossary::PersonalDetails

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Personal Email Address

### Summary
An employee's own email address, held for use outside work systems.

### Description
An employee's own email address, held so that they can be contacted before their work account is created, when work systems are unavailable, and after they have left.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::PersonalEmailAddress

### Folders
- CollectionFolder::EmployeeGlossary::PersonalDetails

### Journal Entry
Personal data belonging to the employee rather than to the organization. It should never be used for routine work correspondence, and the retention rule after an employee leaves needs to be agreed with the privacy team.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Work Telephone Number

### Summary
The telephone number on which an employee can be reached at work.

### Description
The telephone number on which an employee can be reached at work, whether a desk extension at their work location or a number for a device issued to them.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::WorkTelephoneNumber

### Folders
- CollectionFolder::EmployeeGlossary::PersonalDetails

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Personal Telephone Number

### Summary
An employee's own telephone number, held for use outside work systems.

### Description
An employee's own telephone number, held so that they can be contacted when work systems and work devices are not available to them.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::PersonalTelephoneNumber

### Folders
- CollectionFolder::EmployeeGlossary::PersonalDetails

### Journal Entry
Personal data belonging to the employee. Access should be restricted to the HR team and to whatever emergency processes genuinely need it.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Emergency Contact

### Summary
The person an employee nominates to be contacted on their behalf in an emergency.

### Description
The person an employee nominates to be contacted on their behalf if they are taken ill or involved in an accident at work.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::EmergencyContact

### Folders
- CollectionFolder::EmployeeGlossary::PersonalDetails

### Journal Entry
This is personal data about a third party who is not an employee and who has not given their consent to Coco Pharmaceuticals directly. The privacy team need to review what may be held, for how long, and who may see it.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---
### 7.3 Compensation

The first session captured how an employee is paid. These terms cover what actually reaches
them, what is taken from it, and the non-cash parts of the deal.

___

## Create Glossary Term

### Display Name
Pay Grade

### Summary
The pay range that applies to a job grade.

### Description
The range of pay that applies to a job grade, giving the minimum and maximum that an employee in a role at that grade may be paid. It is reviewed periodically against market rates.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::PayGrade

### Folders
- CollectionFolder::EmployeeGlossary::Compensation

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Payroll Number

### Summary
The identifier used by the payroll system to identify an employee's pay record.

### Description
The identifier used by the payroll system to identify an employee's pay record.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::PayrollNumber

### Folders
- CollectionFolder::EmployeeGlossary::Compensation

### Journal Entry
It is not yet confirmed whether this is the same value as Employee Id or a separate identifier issued by the payroll system. Different business units appear to answer this differently, which is exactly the kind of ambiguity this glossary exists to remove.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Pay Period

### Summary
The recurring period of time that a payment to an employee covers.

### Description
The recurring period of time that a single payment to an employee covers. It determines how often the employee is paid and what period each payslip reports on.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::PayPeriod

### Folders
- CollectionFolder::EmployeeGlossary::Compensation

### Example
Monthly, four-weekly, weekly.

### Journal Entry
Employees paid by Hourly Pay Rate are generally on a shorter pay period than those on an Annual Salary. Needs confirming with payroll.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Gross Pay

### Summary
The total amount due to an employee for a pay period, before deductions.

### Description
The total amount due to an employee for a pay period under their compensation plan, before any deductions are taken from it.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::GrossPay

### Folders
- CollectionFolder::EmployeeGlossary::Compensation

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Deduction

### Summary
An amount subtracted from an employee's gross pay.

### Description
An amount subtracted from an employee's gross pay before it is paid to them - for example income tax, social security contributions, pension contributions, or repayments the employee has agreed to.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::Deduction

### Folders
- CollectionFolder::EmployeeGlossary::Compensation

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Net Pay

### Summary
The amount actually paid to an employee for a pay period, after deductions.

### Description
The amount actually paid to an employee for a pay period: their gross pay less the total of all deductions taken from it.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::NetPay

### Folders
- CollectionFolder::EmployeeGlossary::Compensation

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Overtime Rate

### Summary
The rate at which an employee is paid for hours worked beyond their contracted hours.

### Description
The rate at which an employee is paid for hours worked beyond their contracted hours. It is usually expressed as a multiple of their hourly pay rate.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::OvertimeRate

### Folders
- CollectionFolder::EmployeeGlossary::Compensation

### Journal Entry
Used alongside Hourly Pay Rate in manufacturing. Whether employees on an Annual Salary can receive overtime at all is a policy question for Faith Broker.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Commission

### Summary
A type of compensation calculated as a proportion of the value of sales made.

### Description
A type of compensation where an employee receives an amount calculated as a proportion of the value of the sales they have made.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::Commission

### Folders
- CollectionFolder::EmployeeGlossary::Compensation

### Journal Entry
Used for the sales team. The rules that determine when a sale counts towards commission are held by the sales operations team and will need their own definitions.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Pension Contribution

### Summary
An amount paid into an employee's pension.

### Description
An amount paid into an employee's pension, either by the employee out of their gross pay, by Coco Pharmaceuticals on their behalf, or by both.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::PensionContribution

### Folders
- CollectionFolder::EmployeeGlossary::Compensation

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Employee Benefit

### Summary
A non-cash element of an employee's compensation plan.

### Description
A non-cash element of an employee's compensation plan - something of value provided to them rather than paid to them.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::EmployeeBenefit

### Folders
- CollectionFolder::EmployeeGlossary::Compensation

### Example
Private medical cover, life assurance, a company car, subsidised meals, additional annual leave.

### Journal Entry
Some benefits are taxable and therefore appear in payroll data as well as in the compensation plan. Which ones differs by country. Needs review with payroll and with the finance team.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Expense Claim

### Summary
A request from an employee to be reimbursed for costs they paid personally.

### Description
A request from an employee for reimbursement of costs they have paid personally while carrying out their work, such as travel, accommodation or materials.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::ExpenseClaim

### Folders
- CollectionFolder::EmployeeGlossary::Compensation

### Journal Entry
An expense reimbursement is not compensation - it repays a cost rather than rewarding work - but it is paid through payroll, so it is defined here to make the distinction explicit.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Compensation Review

### Summary
The periodic assessment of an employee's compensation plan.

### Description
The periodic assessment of an employee's compensation plan against their performance, their job grade and the pay grade that applies to their role, resulting in a decision on whether their compensation changes.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::CompensationReview

### Folders
- CollectionFolder::EmployeeGlossary::Compensation

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---
### 7.4 Work Locations

The kinds of work location that sit behind the Work Location Type code set. Defining them as
terms in their own right is what allows the note on Work Location - that not all work locations are offices - to be
resolved rather than just recorded.

___

## Create Glossary Term

### Display Name
Office

### Summary
A work location whose primary purpose is desk-based work.

### Description
A work location whose primary purpose is desk-based work, providing workspaces, meeting rooms and the facilities that support them.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::Office

### Folders
- CollectionFolder::EmployeeGlossary::WorkLocations

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Manufacturing Plant

### Summary
A work location where Coco Pharmaceuticals manufactures its products.

### Description
A work location where Coco Pharmaceuticals manufactures its products. Employees based at a manufacturing plant work under the controlled conditions that pharmaceutical manufacturing requires.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::ManufacturingPlant

### Folders
- CollectionFolder::EmployeeGlossary::WorkLocations

### Journal Entry
Access to a manufacturing plant depends on current certification for the work being done, so the employee data held about people based here connects to the Certification term.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Warehouse

### Summary
A work location used to store products and materials.

### Description
A work location used to store products and materials before they are used in manufacturing or distributed to customers.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::Warehouse

### Folders
- CollectionFolder::EmployeeGlossary::WorkLocations

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Home Working Location

### Summary
An employee's own home, recorded as a place they regularly work from.

### Description
An employee's own home, when it is recorded as a place they regularly work from. Its address is the employee's home address rather than an address belonging to Coco Pharmaceuticals.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::HomeWorkingLocation

### Folders
- CollectionFolder::EmployeeGlossary::WorkLocations

### Journal Entry
Recorded in answer to the note on Work Location that not all work locations are offices and some employees work at home. Because the address of a home working location is personal data belonging to the employee, it must not be published in the location directory in the way that office addresses are.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Time Zone

### Summary
The local time that applies at a work location.

### Description
The local time that applies at a work location, needed so that working hours, meetings and shift patterns can be interpreted correctly across a business that operates in several countries.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::TimeZone

### Folders
- CollectionFolder::EmployeeGlossary::WorkLocations

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---
### 7.5 Addresses

The rest of the breakdown of Postal Address. Figure 3 captured the parts of an address that
identify a property; these are the parts that locate it. They are the terms most likely to be adopted by other
subject areas, since every address in the organization is built from them.

___

## Create Glossary Term

### Display Name
Address Line

### Summary
A line of free text within a postal address.

### Description
A single line of free text within a postal address, used for the parts of the address that do not fit the named components - a district, an estate, a floor, or a care-of line.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::AddressLine

### Folders
- CollectionFolder::EmployeeGlossary::Addresses

### Journal Entry
Needed because address structure varies considerably between countries. How many address lines to allow, and whether their order is significant, still needs deciding.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
City

### Aliases
- Town

### Summary
The city or town that a postal address is located in.

### Description
The city or town that a postal address is located in.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::City

### Folders
- CollectionFolder::EmployeeGlossary::Addresses

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Region

### Aliases
- State
- Province
- County

### Summary
The state, province or county that a postal address is located in.

### Description
The administrative area larger than a city that a postal address is located in.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::Region

### Folders
- CollectionFolder::EmployeeGlossary::Addresses

### Journal Entry
Both the name of this component and whether it is required at all differ by country, which is why it is defined by the general term Region rather than by any one country's name for it.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Postal Code

### Aliases
- Post Code
- Zip Code

### Summary
The code used by the postal service to identify the delivery area of an address.

### Description
The code used by the postal service to identify the delivery area that a postal address falls within.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::PostalCode

### Folders
- CollectionFolder::EmployeeGlossary::Addresses

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Country

### Summary
The country that a postal address is located in.

### Description
The country that a postal address is located in.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::Country

### Folders
- CollectionFolder::EmployeeGlossary::Addresses

### Journal Entry
Should be recorded using the ISO 3166 country codes rather than free text. A valid value set needs to be created for this, and it will be reused far beyond employee data.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---
### 7.6 Working Time and Absence

When an employee is expected to work, when they actually worked, and when they are
away. This section connects employee data to payroll, to manufacturing batch records and to clinical trial evidence,
which is why the terms need to be precise.

___

## Create Glossary Term

### Display Name
Working Pattern

### Summary
The days and hours that an employee is contracted to work.

### Description
The days and hours that an employee is contracted to work, and where those hours are worked. It sets the expectation against which attendance, absence and overtime are measured.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::WorkingPattern

### Folders
- CollectionFolder::EmployeeGlossary::WorkingTime

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Contracted Hours

### Summary
The number of hours per week that an employee is contracted to work.

### Description
The number of hours per week that an employee is contracted to work under their working pattern.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::ContractedHours

### Folders
- CollectionFolder::EmployeeGlossary::WorkingTime

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Full Time

### Summary
A working pattern covering the standard number of hours for the role.

### Description
A working pattern in which the employee works the organization's standard number of hours for their role and location.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::FullTime

### Folders
- CollectionFolder::EmployeeGlossary::WorkingTime

### Journal Entry
The standard number of hours differs by country, so "full time" does not mean the same number of hours everywhere. This needs stating explicitly wherever the term is used in a calculation.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Part Time

### Summary
A working pattern covering fewer than the standard number of hours.

### Description
A working pattern in which the employee works fewer than the standard number of hours for their role and location. Entitlements such as annual leave are usually calculated in proportion to the hours worked.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::PartTime

### Folders
- CollectionFolder::EmployeeGlossary::WorkingTime

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Timesheet

### Summary
The record of the hours an employee has actually worked in a period.

### Description
The record of the hours an employee has actually worked in a period, and of what they worked on.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::Timesheet

### Folders
- CollectionFolder::EmployeeGlossary::WorkingTime

### Journal Entry
Required wherever compensation is calculated from an Hourly Pay Rate, and also for clinical trial and manufacturing work where the effort has to be attributable to a specific study or batch. The two uses may have different accuracy requirements.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Annual Leave Entitlement

### Summary
The amount of paid holiday an employee may take in a leave year.

### Description
The amount of paid holiday an employee may take in a leave year, established by their employment contract and by the law of the country they work in.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::AnnualLeaveEntitlement

### Folders
- CollectionFolder::EmployeeGlossary::WorkingTime

### Journal Entry
Varies by country, by job grade and by length of service, and is proportioned for part-time employees. When the leave year starts is also not the same everywhere.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Absence

### Summary
A period during which an employee is not at work when they would normally be expected to be.

### Description
A period during which an employee is not at work when their working pattern says they would be expected to be, whether the absence is planned or unplanned, paid or unpaid.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::Absence

### Folders
- CollectionFolder::EmployeeGlossary::WorkingTime

### Is Abstract Concept
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Sick Leave

### Summary
An absence caused by the employee's illness or injury.

### Description
An absence caused by the employee's own illness or injury.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::SickLeave

### Folders
- CollectionFolder::EmployeeGlossary::WorkingTime

### Journal Entry
Data about sick leave reveals information about a person's health, which is special category personal data under GDPR. It must not be held alongside general HR data without a confidentiality classification and restricted access. The privacy team must review this term before any system design uses it.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Parental Leave

### Summary
An absence taken following the birth or adoption of a child, or to care for one.

### Description
An absence taken by an employee following the birth or adoption of a child, or in order to care for a child.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::ParentalLeave

### Folders
- CollectionFolder::EmployeeGlossary::WorkingTime

### Journal Entry
Entitlement, pay and notice rules differ substantially between the countries Coco Pharmaceuticals operates in. Whether these are variations of one term or genuinely different terms needs deciding.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Public Holiday

### Summary
A day on which a work location is closed and employees there are not expected to work.

### Description
A day on which a work location is closed, and the employees based there are not expected to work, because it is a public holiday in that country.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::PublicHoliday

### Folders
- CollectionFolder::EmployeeGlossary::WorkingTime

### Journal Entry
Public holidays follow the work location rather than the employee, which matters for employees who work across locations and for anyone with a home working location in a different country from their team.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---
### 7.7 Performance and Development

What an employee is expected to be able to do, how well they do it, and how
those capabilities are developed and evidenced. Certification in particular reaches well outside human resources -
regulated work has to be done by people whose certification was current at the time.

___

## Create Glossary Term

### Display Name
Performance Review

### Summary
The periodic assessment of an employee's performance against their objectives.

### Description
The periodic discussion between an employee and their manager in which performance against the agreed objectives is assessed, development needs are identified, and objectives for the next period are agreed.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::PerformanceReview

### Folders
- CollectionFolder::EmployeeGlossary::PerformanceDevelopment

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Performance Objective

### Summary
A specific outcome an employee agrees to achieve within a review period.

### Description
A specific, measurable outcome that an employee and their manager agree the employee will achieve within a review period.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::PerformanceObjective

### Folders
- CollectionFolder::EmployeeGlossary::PerformanceDevelopment

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Competency

### Summary
A skill, area of knowledge or behaviour expected of an employee in a role.

### Description
A skill, area of knowledge or behaviour that Coco Pharmaceuticals expects an employee working in a given role to be able to demonstrate.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::Competency

### Folders
- CollectionFolder::EmployeeGlossary::PerformanceDevelopment

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Proficiency Level

### Summary
The degree to which an employee demonstrates a competency.

### Description
The degree to which an employee is able to demonstrate a competency, used to identify development needs and to find the right people for a piece of work.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::ProficiencyLevel

### Folders
- CollectionFolder::EmployeeGlossary::PerformanceDevelopment

### Example
Awareness, working, practitioner, expert.

### Is Data Value
True

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Qualification

### Summary
A formal award held by an employee.

### Description
A formal academic or vocational award held by an employee, granted by an educational institution or a professional body.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::Qualification

### Folders
- CollectionFolder::EmployeeGlossary::PerformanceDevelopment

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Certification

### Summary
A qualification confirming that a person is competent to perform a regulated activity.

### Description
A qualification awarded by an external body confirming that a person is competent to perform a specific regulated activity. Certifications are usually valid only for a fixed period and must be renewed.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::Certification

### Folders
- CollectionFolder::EmployeeGlossary::PerformanceDevelopment

### Journal Entry
Certification matters far beyond HR. Manufacturing and clinical trial work must be performed by people whose certification was current at the time the work was done, so this data is needed for regulatory evidence and not only for personnel records. Needs review with the manufacturing and clinical trial governance teams.

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Training Course

### Summary
A structured learning activity provided or funded to develop an employee's competencies.

### Description
A structured learning activity provided or funded by Coco Pharmaceuticals in order to develop an employee's competencies, or to obtain or renew a certification they need for their role.

### Glossary Name
Glossary::EmployeeGlossary

### Qualified Name
Glossary::EmployeeGlossary::TrainingCourse

### Folders
- CollectionFolder::EmployeeGlossary::PerformanceDevelopment

### Authors
- Erin Overview
- Faith Broker

### Version Identifier
1.0

### Content Status
DRAFT

___

---
## Part 8: The Expanded Term Relationships

The relationships below connect the terms added in Part 7 to each other and to the terms from the original session.
They use the same three kinds of relationship that emerged from the first drill-down, plus one more:

* **Is A Type Of** - the type hierarchies. Some of these were implied by the original descriptions all along:
  Annual Salary and Hourly Pay Rate were both described as *"a type of compensation where..."*, so they are
  specializations of Compensation Plan.
* **Has A** - the terms that are made up of other terms. Employee itself is broken down here, which the first
  session's flat list of concepts had not yet done.
* **Related Term** - a connection that is real but is not composition or specialization. The Expression on each one
  records what the connection actually is, including the two that record open questions rather than settled facts.

### 8.1 Type Hierarchies

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::Employee

### Term 2
Glossary::EmployeeGlossary::Worker

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::Contractor

### Term 2
Glossary::EmployeeGlossary::Worker

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::TeamLeader

### Term 2
Glossary::EmployeeGlossary::Employee

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::Founder

### Term 2
Glossary::EmployeeGlossary::Employee

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::LegalName

### Term 2
Glossary::EmployeeGlossary::EmployeeName

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::KnownName

### Term 2
Glossary::EmployeeGlossary::EmployeeName

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::AnnualSalary

### Term 2
Glossary::EmployeeGlossary::CompensationPlan

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::HourlyPayRate

### Term 2
Glossary::EmployeeGlossary::CompensationPlan

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::Bonus

### Term 2
Glossary::EmployeeGlossary::CompensationPlan

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::Commission

### Term 2
Glossary::EmployeeGlossary::CompensationPlan

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::EmployeeBenefit

### Term 2
Glossary::EmployeeGlossary::CompensationPlan

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::Office

### Term 2
Glossary::EmployeeGlossary::WorkLocation

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::ManufacturingPlant

### Term 2
Glossary::EmployeeGlossary::WorkLocation

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::Warehouse

### Term 2
Glossary::EmployeeGlossary::WorkLocation

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::HomeWorkingLocation

### Term 2
Glossary::EmployeeGlossary::WorkLocation

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::SickLeave

### Term 2
Glossary::EmployeeGlossary::Absence

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::ParentalLeave

### Term 2
Glossary::EmployeeGlossary::Absence

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::FullTime

### Term 2
Glossary::EmployeeGlossary::WorkingPattern

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::PartTime

### Term 2
Glossary::EmployeeGlossary::WorkingPattern

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermISATYPEOFRelationship

### Term 1
Glossary::EmployeeGlossary::Certification

### Term 2
Glossary::EmployeeGlossary::Qualification

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---
### 8.2 Composition

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::Employee

### Term 2
Glossary::EmployeeGlossary::EmployeeId

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::Employee

### Term 2
Glossary::EmployeeGlossary::EmployeeName

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::Employee

### Term 2
Glossary::EmployeeGlossary::JobTitle

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::Employee

### Term 2
Glossary::EmployeeGlossary::EmploymentContract

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::Employee

### Term 2
Glossary::EmployeeGlossary::WorkLocation

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::Employee

### Term 2
Glossary::EmployeeGlossary::BusinessUnit

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::Employee

### Term 2
Glossary::EmployeeGlossary::EmployeeHomeAddress

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::Employee

### Term 2
Glossary::EmployeeGlossary::WorkEmailAddress

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::Employee

### Term 2
Glossary::EmployeeGlossary::DateOfBirth

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::Employee

### Term 2
Glossary::EmployeeGlossary::NationalIdentifier

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::Employee

### Term 2
Glossary::EmployeeGlossary::EmergencyContact

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::EmployeeName

### Term 2
Glossary::EmployeeGlossary::FirstName

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::EmployeeName

### Term 2
Glossary::EmployeeGlossary::MiddleName

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::EmployeeName

### Term 2
Glossary::EmployeeGlossary::LastName

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::EmploymentContract

### Term 2
Glossary::EmployeeGlossary::EmploymentType

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::EmploymentContract

### Term 2
Glossary::EmployeeGlossary::EmploymentStartDate

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::EmploymentContract

### Term 2
Glossary::EmployeeGlossary::EmploymentEndDate

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::EmploymentContract

### Term 2
Glossary::EmployeeGlossary::NoticePeriod

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::EmploymentContract

### Term 2
Glossary::EmployeeGlossary::ProbationPeriod

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::EmploymentContract

### Term 2
Glossary::EmployeeGlossary::CompensationPlan

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::EmploymentContract

### Term 2
Glossary::EmployeeGlossary::WorkingPattern

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::WorkingPattern

### Term 2
Glossary::EmployeeGlossary::ContractedHours

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::CompensationPlan

### Term 2
Glossary::EmployeeGlossary::PayPeriod

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::PostalAddress

### Term 2
Glossary::EmployeeGlossary::AddressLine

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::PostalAddress

### Term 2
Glossary::EmployeeGlossary::City

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::PostalAddress

### Term 2
Glossary::EmployeeGlossary::Region

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::PostalAddress

### Term 2
Glossary::EmployeeGlossary::PostalCode

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::PostalAddress

### Term 2
Glossary::EmployeeGlossary::Country

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::WorkLocation

### Term 2
Glossary::EmployeeGlossary::TimeZone

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::Team

### Term 2
Glossary::EmployeeGlossary::TeamLeader

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::Manager

### Term 2
Glossary::EmployeeGlossary::DirectReport

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::PerformanceReview

### Term 2
Glossary::EmployeeGlossary::PerformanceObjective

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---
___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::Employee

### Term 2
Glossary::EmployeeGlossary::EmploymentStatus

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---
___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::Employee

### Term 2
Glossary::EmployeeGlossary::WorkTelephoneNumber

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---
___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::Employee

### Term 2
Glossary::EmployeeGlossary::PersonalEmailAddress

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---
___

## Link Term-Term Relationship

### Relationship Type
TermHASARelationship

### Term 1
Glossary::EmployeeGlossary::Employee

### Term 2
Glossary::EmployeeGlossary::PersonalTelephoneNumber

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---
### 8.3 Related Terms

Two of these record disagreements rather than facts. Payroll Number and Employee Id are linked because nobody in the
session could say for certain whether they hold the same value, and Manager and Team Leader are linked because
whether one is a kind of the other is still open. Recording the uncertainty as a relationship with an expression on
it is better than recording a guess as a definition.

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::EmployeeGlossary::PayrollNumber

### Term 2
Glossary::EmployeeGlossary::EmployeeId

### Expression
Both identify an employee. Whether they hold the same value, or are separate identifiers issued by different systems, is an open question.

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::EmployeeGlossary::NetPay

### Term 2
Glossary::EmployeeGlossary::GrossPay

### Expression
Net pay is gross pay after deductions have been taken from it.

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::EmployeeGlossary::NetPay

### Term 2
Glossary::EmployeeGlossary::Deduction

### Expression
Net pay is gross pay less the total of all deductions.

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::EmployeeGlossary::PensionContribution

### Term 2
Glossary::EmployeeGlossary::Deduction

### Expression
An employee's own pension contribution is taken as a deduction from gross pay.

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::EmployeeGlossary::PayGrade

### Term 2
Glossary::EmployeeGlossary::JobGrade

### Expression
The pay grade that applies to an employee is determined by the job grade of their role.

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::EmployeeGlossary::Timesheet

### Term 2
Glossary::EmployeeGlossary::HourlyPayRate

### Expression
Where an employee is paid by hourly pay rate, the timesheet supplies the hours the payment is calculated from.

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::EmployeeGlossary::Timesheet

### Term 2
Glossary::EmployeeGlossary::ContractedHours

### Expression
Hours recorded on a timesheet beyond the contracted hours are the hours paid at the overtime rate.

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::EmployeeGlossary::OvertimeRate

### Term 2
Glossary::EmployeeGlossary::HourlyPayRate

### Expression
The overtime rate is usually expressed as a multiple of the employee's hourly pay rate.

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::EmployeeGlossary::HomeWorkingLocation

### Term 2
Glossary::EmployeeGlossary::EmployeeHomeAddress

### Expression
The address of a home working location is the employee's own home address, so it is personal data rather than organization data.

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::EmployeeGlossary::CompensationReview

### Term 2
Glossary::EmployeeGlossary::PerformanceReview

### Expression
The outcome of a performance review is one of the inputs to a compensation review.

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::EmployeeGlossary::Certification

### Term 2
Glossary::EmployeeGlossary::Competency

### Expression
A certification is external evidence that an employee holds a competency.

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::EmployeeGlossary::TrainingCourse

### Term 2
Glossary::EmployeeGlossary::Competency

### Expression
A training course is provided in order to develop a competency.

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::EmployeeGlossary::AnnualLeaveEntitlement

### Term 2
Glossary::EmployeeGlossary::Absence

### Expression
Annual leave entitlement is the amount of one particular kind of planned, paid absence an employee may take.

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::EmployeeGlossary::PublicHoliday

### Term 2
Glossary::EmployeeGlossary::WorkLocation

### Expression
Public holidays apply to a work location rather than to an employee, so which ones an employee observes follows from where they are based.

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::EmployeeGlossary::Manager

### Term 2
Glossary::EmployeeGlossary::TeamLeader

### Expression
Both direct the work of others. Whether a team leader is a kind of manager is the open question recorded against both terms.

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---
___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::EmployeeGlossary::Competency

### Term 2
Glossary::EmployeeGlossary::ProficiencyLevel

### Expression
A competency is always recorded together with the proficiency level at which the employee demonstrates it - the competency alone does not say how well.

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---
___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::EmployeeGlossary::ExpenseClaim

### Term 2
Glossary::EmployeeGlossary::CompensationPlan

### Expression
An expense claim is paid through payroll alongside compensation but is not part of it: it repays a cost the employee has already borne rather than rewarding their work.

### Source
Employee glossary follow-on sessions - expanding the Employee subject area with the wider human resources team.

### Steward
Erin Overview

### Term Relationship Status
DRAFT

___

---
## Reflecting on the process

Erin and Faith reviewed how the session had gone.  It was hard work at first to be precise about the definition of
words they use every day, but it got easier as the core concepts they had already defined could be reused in the
definitions of new ones.  They also concluded that building a glossary is not the work of a committee: it takes the
focus of two or three experts to lay out the core concepts.  Only then do you bring in new people, take them through
the work so far, incorporate their feedback, and work with them on the additional terms they care about.  Through
that process the team and the knowledge expand together, subteams form to fill out different sections, and there is
constant review that the terms stay consistent and discrete.

The open questions recorded in the Journal Entries above are the agenda for the next session.

---
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
