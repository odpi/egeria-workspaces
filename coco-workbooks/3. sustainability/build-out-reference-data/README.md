<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Building out Reference Data describing Coco Pharmaceuticals

The two notebooks in this folder extend the description of Coco Pharmaceuticals' organization to cover its two acquisitions - Austin Pharmaceuticals, Inc. (the Austin Site) and EKG Pharmaceuticals S.R.L. (the Bucharest Site) - and set up Procurement as a business area of its own.  Run them in this order, after `1. coco-data-hub`, which creates the Bucharest Site and the acquired systems in the IT Systems Inventory:

1. [adding-acquisition-employees.ipynb](adding-acquisition-employees.ipynb)
2. [adding-procurement.ipynb](adding-procurement.ipynb)

Both notebooks check for each element before creating it, so they can be rerun.

## Acquisition Employees

[adding-acquisition-employees.ipynb](adding-acquisition-employees.ipynb) follows the pattern of the existing Coco employee profiles, such as Gary Geeke's:

* **Reference data** - Tom Tally adds Romania (`RO`) to the *CountryCode* reference data set and Bucharest (`12`) to the *WorkLocation* reference data set, each as a reference data value and as a valid metadata value.  The Bucharest work location values are linked to the Bucharest Site location with the *MoreInformation* relationship.
* **Teams** - Faith Broker creates the Bucharest Site team (`Department::9991`) and its Factory, Office and Information Technology departments (`0025`-`0027`), each with a team leader role and a team member role.  The Austin teams already exist.
* **Employees** - Faith adds an actor profile, user identity and work email contact details for each employee, and appoints them to their team.
* **System owners** - Gary Geeke creates an *asset-owner* role for each subsystem of the Austin and Bucharest estates and appoints the business owner named in the system inventory.

The employees come from these files in [data](data):

| File | Contents |
|---|---|
| [austin_employees.csv](data/austin_employees.csv) | 35 Austin employees: the staff in Austin's Workday HCM system, plus the business owners named in the Austin system inventory, with their team, job level and employee type. |
| [ekg_romanian_employees.csv](data/ekg_romanian_employees.csv) | The 50 EKG employees on the staff list provided at the acquisition (see below). |
| [ekg_additional_employees.csv](data/ekg_additional_employees.csv) | 16 more EKG employees: factory and laboratory staff from EKG's Workday HCM system who are not on the staff list, and Carmen Iliescu, who looks after procurement at Bucharest. |
| [ekg_employee_assignments.csv](data/ekg_employee_assignments.csv) | The team, team role, job level and employee type of each EKG employee. |
| [bucharest_teams.csv](data/bucharest_teams.csv) | The Bucharest teams and the business areas that own them. |

### EKG (Bucharest) staff list

Data in file [data/ekg_romanian_employees.csv](data/ekg_romanian_employees.csv) has 50 employees. Here's a summary of what's in it:

- **Names** — authentic Romanian first names, surnames, and diacritics (ă, â, î, ș, ț) throughout
- **Courtesy titles** — Romanian conventions: `Dl.` (Domnul, Mr.) and `Dna.` (Doamna, Ms.)
- **Ages** — range from 23 (born 2001) to 57 (born 1968), spread across generations
- **Pronouns** — Romanian forms: `el/lui` (he/him) and `ea/ei` (she/her)
- **Preferred language** — `Română` for all
- **Email** — `firstname.surname@ekg.ro` pattern, with a `2` suffix where surnames clash (e.g. two Ionescus)
- **Job titles** — a realistic mix across engineering, finance, HR, legal, operations, sales, and leadership (including C-suite roles)

The date of birth is not loaded into Egeria.

## Procurement Business Capability

[adding-procurement.ipynb](adding-procurement.ipynb) adds Procurement to the *Coco Pharmaceuticals Business Areas*, following the supplier fraud.  Its only member is the existing Procurement Team, managed by Sally Counter.  The notebook creates the Procurement Sustainability Champion role by copying the Finance Sustainability Champion, appoints Sally to it, and adds Ethan Park (Austin) and Carmen Iliescu (Bucharest) to the Procurement Team so that, together, they can consolidate the supplier lists.

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
