# Hand-off: statements of applicability in pyegeria and Dr.Egeria

Audience: maintainers of **pyegeria** and **Dr.Egeria** (egeria-python).
Goal: support the new statement of applicability types and Security Officer API operations added to Egeria 6.3, so that a security team can record which controls of a standard such as ISO/IEC 27001 apply to them, why, and how far each one has been implemented.

Status (2026-10-26): the egeria changes are on the `oak2026` branch, not yet committed.  They compile, the framework and content pack tests pass, and every operation below has been exercised end to end against a platform built from the branch, with controls loaded from the Security Content Pack.

---

## Background

A *statement of applicability* (SoA) is the record an organization keeps of which controls from a standard apply to it.  For ISO/IEC 27001 it lists every Annex A control with:

- whether the control applies,
- why it is included or excluded,
- how far it has been implemented, and
- how it is implemented.

It is one of the main documents reviewed in a certification audit, and it is versioned and approved like any other authored document.

In open metadata:

```
CertificationType --GovernedBy--> StatementOfApplicability --ControlApplicability--> GovernanceDefinition (a control from the standard)
                                         |
                                         +--ScopedBy--> Referenceable (organization, site, system...)
```

The organization's own controls are linked to the standard's controls with the existing *GovernanceControlLink* relationship, and to the risks they treat with *GovernanceMechanism*.

---

## The new types

### StatementOfApplicability entity

- Supertype: **AuthoredReferenceable**.  It carries `authors`, `contentStatus` (for example DRAFT, then APPROVED) and `versionIdentifier`, plus the usual Referenceable properties.
- New attributes:
  - `scope` (string): the part of the organization that the statement covers, such as the scope of the ISMS.
  - `reviewDate` (date): when the statement was last reviewed.
- JSON properties class: `StatementOfApplicabilityProperties` (a subtype of `AuthoredReferenceableProperties`).
- Type GUID: `57f60046-aa59-4f0e-bc09-08714d40d4f5`.

### ControlApplicability relationship

- End 1: **StatementOfApplicability** (attribute name `statementsOfApplicability`).
- End 2: **GovernanceDefinition** (attribute name `assessedControls`).  This is any governance definition describing a control, typically a *GovernanceControl*, but a *RegulationArticle* works too.
- Not multi-link: there is one relationship per control per statement.
- Attributes:

  | Attribute | Type | Notes |
  |---|---|---|
  | `isApplicable` | boolean | A control is treated as applicable unless this is `false`. |
  | `justification` | string | Why the control is included or excluded. |
  | `inclusionReasons` | array of string | Free text.  Suggested values: `Risk Treatment`, `Legal or Regulatory Requirement`, `Contractual Obligation`, `Business Requirement`, `Best Practice`. |
  | `implementationStatus` | enum *ControlImplementationStatus* | See below. |
  | `implementationDescription` | string | How the control is implemented within the scope of the statement. |
  | `reviewDate` | date | When this control's applicability was last reviewed. |
  | `label` | string | Suggested use: the control's number in the standard, such as `8.25`. |
  | `description` | string | Notes. |

- JSON properties class: `ControlApplicabilityProperties` (a subtype of `LabeledRelationshipProperties`).
- Type GUID: `92562d3e-1838-4a86-9295-8b39d80c3773`.

### ControlImplementationStatus enumeration

`NOT_STARTED` (default), `PLANNED`, `PARTIALLY_IMPLEMENTED`, `IMPLEMENTED`, `OTHER`.

These values are registered as valid metadata values for the `implementationStatus` property in the Core Content Pack.

### Core Content Pack

The Core Content Pack now contains a *CertificationType* for ISO/IEC 27001:2022:

- qualified name `CertificationType::ISO/IEC 27001:2022`
- GUID `f51e1e11-62c7-4148-8104-4477551e446d`

It does not contain the Annex A controls themselves.  The text of the standard belongs to ISO, so organizations load the controls from their own licensed copy.

### Security Content Pack

A new, separately loaded **SecurityContentPack** contains the NIST CSF 2.0 and NIST SP 800-53 Rev. 5 catalogs.  Each control is a *GovernanceControl* that can be linked straight to a statement of applicability, so this pack makes it possible to test the new APIs without any licensed content:

- 106 CSF subcategories, such as `NIST CSF 2.0::GV.OC-01`;
- 300 SP 800-53 controls, such as `NIST SP 800-53 Rev 5::AC-2`;
- 714 control enhancements, such as `NIST SP 800-53 Rev 5::AC-2(1)`, each linked to its base control with *GovernanceControlLink*.

The Core Content Pack also now has the six STRIDE threats, such as `Threat::STRIDE::Spoofing`.

---

## New Security Officer API operations

URL marker `security-officer`.  Every path below follows `{{baseURL}}/servers/{{viewServer}}/api/open-metadata/security-officer`.  All operations are `POST`.

| Operation | Path | Request body | Response |
|---|---|---|---|
| createStatementOfApplicability | `/statements-of-applicability` | NewElementRequestBody | GUIDResponse |
| createStatementOfApplicabilityFromTemplate | `/statements-of-applicability/from-template` | TemplateRequestBody | GUIDResponse |
| updateStatementOfApplicability | `/statements-of-applicability/{statementOfApplicabilityGUID}/update` | UpdateElementRequestBody | BooleanResponse |
| deleteStatementOfApplicability | `/statements-of-applicability/{statementOfApplicabilityGUID}/delete` | DeleteElementRequestBody | VoidResponse |
| getStatementsOfApplicabilityByName | `/statements-of-applicability/by-name` | FilterRequestBody | OpenMetadataRootElementsResponse |
| findStatementsOfApplicability | `/statements-of-applicability/by-search-string` | SearchStringRequestBody | OpenMetadataRootElementsResponse |
| getStatementOfApplicabilityByGUID | `/statements-of-applicability/{statementOfApplicabilityGUID}/retrieve` | GetRequestBody | OpenMetadataRootElementResponse |
| linkControlApplicability | `/statements-of-applicability/{statementOfApplicabilityGUID}/control-applicability/{controlGUID}/attach` | NewRelationshipRequestBody | VoidResponse |
| detachControlApplicability | `/statements-of-applicability/{statementOfApplicabilityGUID}/control-applicability/{controlGUID}/detach` | DeleteRelationshipRequestBody | VoidResponse |

Things to watch:

- **The relationship is identified by its two ends.**  ControlApplicability is not multi-link, so link and detach both take the statement GUID and the control GUID, and link returns void like the other non-multi-link `attach` operations.  There is no separate update operation: **calling link again for a control that is already linked updates the properties of the existing relationship**.
- **The controls come back in `otherRelatedElements`.**  `getStatementOfApplicabilityByGUID` returns the statement with each ControlApplicability relationship, and the control at its other end, in the element's `otherRelatedElements` list.  The relationship properties are in `relationshipProperties`, with `class` set to `ControlApplicabilityProperties`.
- **CRUD follows the DevOps Pipeline API.**  The create, update, delete, get and find operations behave exactly like the storage volume operations in the DevOps Pipeline API, so existing pyegeria patterns for those carry over unchanged.
- **Sample requests** are at the end of `open-metadata-implementation/view-services/security-officer/Egeria-api-security-officer.http` in the egeria repo.

---

## What pyegeria needs

Add sync and async methods to the `SecurityOfficer` client, following the existing naming:

- `create_statement_of_applicability(body)` and `create_statement_of_applicability_from_template(body)`
- `update_statement_of_applicability(soa_guid, body)`
- `delete_statement_of_applicability(soa_guid, body=None, cascade=False)`
- `get_statements_of_applicability_by_name(filter_string, body=None, ...)`
- `find_statements_of_applicability(search_string="*", ...)`
- `get_statement_of_applicability_by_guid(soa_guid, body=None)`
- `link_control_applicability(soa_guid, control_guid, body=None)`
- `detach_control_applicability(soa_guid, control_guid, body=None)`

The Pydantic models need:

- `StatementOfApplicabilityProperties` (AuthoredReferenceable fields plus `scope` and `reviewDate`)
- `ControlApplicabilityProperties` (the attributes in the table above)
- a `ControlImplementationStatus` enum

The **report specs and output formats** would be most useful as a table of the controls for one statement, with columns for:

- control label and display name
- `isApplicable`
- `implementationStatus`
- `justification`
- `inclusionReasons`
- `reviewDate`

That is the view an auditor asks for.  A summary row would also help, giving the count of applicable controls by implementation status, which is the input to the *ISO 27001 Annex A Control Implementation Rate* metric in the Coco Pharmaceuticals security program.  Both Markdown and Excel/CSV output would be useful, since the SoA is often handed to auditors as a spreadsheet.

---

## What Dr.Egeria needs

New commands, with templates in `templates/basic` and `templates/advanced` like the existing ones:

**Create Statement of Applicability / Update Statement of Applicability**
- Display Name (required), Qualified Name, Description, Version Identifier, Scope, Review Date, Authors, Content Status.
- Optional **Certification Type** (reference name): creates a *GovernedBy* relationship from the certification type to the statement.
- Optional **Scope Elements** (reference name list): creates *ScopedBy* relationships from the statement to each element.

**Link Control Applicability / Unlink Control Applicability**
- Statement of Applicability (reference name, required) and Control (reference name, required).
- Is Applicable (bool, default true), Justification, Inclusion Reasons (list), Implementation Status (valid values from the enum), Implementation Description, Review Date, Label, Description.
- Re-running a Link command for the same statement and control updates the existing relationship, because the link operation updates the properties of a relationship that already exists.

**View Statement of Applicability**
- A report command that produces the control table described for pyegeria above.

---

## Example flow (Coco Pharmaceuticals)

1. Simon Burr (CISO) creates `StatementOfApplicability::Coco Pharmaceuticals ISMS` with status DRAFT, governed by `CertificationType::ISO/IEC 27001:2022` and scoped by the Coco Pharmaceuticals organization.
2. He loads the Annex A controls from Coco's licensed copy of the standard as governance controls.
3. For each control he links it to the statement with *ControlApplicability*:
   - control 8.20 (network security) is applicable, included for `Risk Treatment` (ransomware disruption to manufacturing), with status `PARTIALLY_IMPLEMENTED`;
   - control 8.25 (secure development life cycle) is applicable, included for `Business Requirement`, with status `PLANNED`.
4. As implementation progresses he links each control again with its new status and review date, which updates its existing relationship.  Before the certification audit he sets the statement's content status to APPROVED.

The Coco workbooks will get a Dr.Egeria example of this once the commands exist.
