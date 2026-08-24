<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Data Field Naming Glossary

This directory contains the Dr.Egeria markdown files that build the **Data Field Naming** glossary for
Coco Pharmaceuticals: the vocabulary of prime words, modifiers and class words used to construct
consistent data field names, organized by subject area (see `CocoSubjectAreaDefinition`).

Each subject area has its own file, with a Prime Words, Modifiers and Class Words sub-folder. Modifiers
and class words that are generic enough to be reused across many subject areas live in
`common-modifiers.md` and `common-class-words.md` instead of being repeated in every subject area. Both of
those folders sit under a top-level `common.md` folder, alongside the subject area folders.

Once all the terms exist, `classify-prime-words.md`, `classify-modifiers.md` and `classify-class-words.md`
run the `Classify Prime Word` / `Classify Modifier` / `Classify Class Word` commands against them, attaching
the `PrimeWord`, `Modifier` and `ClassWord` classifications from
[0438 Naming Standards](https://egeria-project.org/types/4/0438-Naming-Standards/). The folder a term sits in
says where it belongs in the vocabulary; the classification says the same thing on the term itself, so tools
can tell an anchor noun from a qualifier from a value-type suffix without walking the collection hierarchy.

Each subject-area file also adds the new `CollectionFolder::DataFieldNaming:<name>` folder as a member of the
corresponding `SubjectArea::<name>` collection (see `CocoSubjectAreaDefinition.java`, which defines the
`SubjectArea::` qualified name pattern), so the governance subject area and its data field naming vocabulary
are linked. This means the `SubjectArea::*` collections must already be loaded into Egeria - they are loaded
from `CocoComboArchive.omarchive` at server start up - before any of these files are processed.

## Load order

Process `glossary.md` first - every other file references the glossary it creates. Within a subject
area's family, a parent must be processed before its children (e.g. `organization.md` before
`organization-hospital.md`). The order below satisfies all dependencies:

```
dr_egeria --directive process --userid erinoverview --user_pass secret glossary.md
dr_egeria --directive process --userid erinoverview --user_pass secret organization.md
dr_egeria --directive process --userid erinoverview --user_pass secret organization-hospital.md
dr_egeria --directive process --userid erinoverview --user_pass secret organization-supplier.md
dr_egeria --directive process --userid erinoverview --user_pass secret person.md
dr_egeria --directive process --userid erinoverview --user_pass secret person-patient.md
dr_egeria --directive process --userid erinoverview --user_pass secret person-clinician.md
dr_egeria --directive process --userid erinoverview --user_pass secret person-employee.md
dr_egeria --directive process --userid erinoverview --user_pass secret person-collaborator.md
dr_egeria --directive process --userid erinoverview --user_pass secret clinical.md
dr_egeria --directive process --userid erinoverview --user_pass secret clinical-symptom.md
dr_egeria --directive process --userid erinoverview --user_pass secret clinical-measurement.md
dr_egeria --directive process --userid erinoverview --user_pass secret clinical-prescription.md
dr_egeria --directive process --userid erinoverview --user_pass secret clinical-outcome.md
dr_egeria --directive process --userid erinoverview --user_pass secret treatment.md
dr_egeria --directive process --userid erinoverview --user_pass secret treatment-product.md
dr_egeria --directive process --userid erinoverview --user_pass secret treatment-order.md
dr_egeria --directive process --userid erinoverview --user_pass secret treatment-recipe.md
dr_egeria --directive process --userid erinoverview --user_pass secret service-quality.md
dr_egeria --directive process --userid erinoverview --user_pass secret service-quality-contract.md
dr_egeria --directive process --userid erinoverview --user_pass secret service-quality-stock.md
dr_egeria --directive process --userid erinoverview --user_pass secret service-quality-distribution.md
dr_egeria --directive process --userid erinoverview --user_pass secret service-quality-invoice.md
dr_egeria --directive process --userid erinoverview --user_pass secret governance.md
dr_egeria --directive process --userid erinoverview --user_pass secret product-development.md
dr_egeria --directive process --userid erinoverview --user_pass secret product-development-clinical-trial.md
dr_egeria --directive process --userid erinoverview --user_pass secret common.md
dr_egeria --directive process --userid erinoverview --user_pass secret common-modifiers.md
dr_egeria --directive process --userid erinoverview --user_pass secret common-class-words.md
dr_egeria --directive process --userid erinoverview --user_pass secret classify-prime-words.md
dr_egeria --directive process --userid erinoverview --user_pass secret classify-modifiers.md
dr_egeria --directive process --userid erinoverview --user_pass secret classify-class-words.md
```

The three `classify-*.md` files must come last: they classify terms rather than create them, so every
term they reference has to exist first.

## Files

| File | Subject area | Parent |
|------|---------------|--------|
| [glossary.md](glossary.md) | *(creates the glossary itself)* | - |
| [organization.md](organization.md) | Organization (`Organization`) | - |
| [organization-hospital.md](organization-hospital.md) | Hospital (`Organization:Hospital`) | Organization |
| [organization-supplier.md](organization-supplier.md) | Supplier (`Organization:Supplier`) | Organization |
| [person.md](person.md) | Person (`Person`) | - |
| [person-patient.md](person-patient.md) | Patient (`Person:Patient`) | Person |
| [person-clinician.md](person-clinician.md) | Clinician (`Person:Clinician`) | Person |
| [person-employee.md](person-employee.md) | Employee (`Person:Employee`) | Person |
| [person-collaborator.md](person-collaborator.md) | Collaborator (`Person:Collaborator`) | Person |
| [clinical.md](clinical.md) | Clinical (`Clinical`) | - |
| [clinical-symptom.md](clinical-symptom.md) | Symptom (`Clinical:Symptom`) | Clinical |
| [clinical-measurement.md](clinical-measurement.md) | Measurement (`Clinical:Measurement`) | Clinical |
| [clinical-prescription.md](clinical-prescription.md) | Prescription (`Clinical:Prescription`) | Clinical |
| [clinical-outcome.md](clinical-outcome.md) | Outcome (`Clinical:Outcome`) | Clinical |
| [treatment.md](treatment.md) | Treatment (`Treatment`) | - |
| [treatment-product.md](treatment-product.md) | Product (`Treatment:Product`) | Treatment |
| [treatment-order.md](treatment-order.md) | Order (`Treatment:Order`) | Treatment |
| [treatment-recipe.md](treatment-recipe.md) | Recipe (`Treatment:Recipe`) | Treatment |
| [service-quality.md](service-quality.md) | Service Quality (`ServiceQuality`) | - |
| [service-quality-contract.md](service-quality-contract.md) | Contract (`ServiceQuality:Contract`) | Service Quality |
| [service-quality-stock.md](service-quality-stock.md) | Stock (`ServiceQuality:Stock`) | Service Quality |
| [service-quality-distribution.md](service-quality-distribution.md) | Distribution (`ServiceQuality:Distribution`) | Service Quality |
| [service-quality-invoice.md](service-quality-invoice.md) | Invoice (`ServiceQuality:Invoice`) | Service Quality |
| [governance.md](governance.md) | Governance (`Governance`) | - |
| [product-development.md](product-development.md) | Product Development (`ProductDevelopment`) | - |
| [product-development-clinical-trial.md](product-development-clinical-trial.md) | Clinical Trial (`ProductDevelopment:ClinicalTrial`) | Product Development |
| [common.md](common.md) | *(top-level folder for shared terms)* | - |
| [common-modifiers.md](common-modifiers.md) | *(shared across subject areas)* | Common |
| [common-class-words.md](common-class-words.md) | *(shared across subject areas)* | Common |
| [classify-prime-words.md](classify-prime-words.md) | *(`PrimeWord` on 56 terms)* | - |
| [classify-modifiers.md](classify-modifiers.md) | *(`Modifier` on 44 terms)* | - |
| [classify-class-words.md](classify-class-words.md) | *(`ClassWord` on 46 terms)* | - |
