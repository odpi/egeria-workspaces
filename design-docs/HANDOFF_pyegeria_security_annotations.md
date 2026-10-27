# Hand-off: security annotations in pyegeria and Dr.Egeria

Audience: maintainers of **pyegeria** and **Dr.Egeria** (egeria-python).
Goal: support the four new annotation types added to Egeria 6.3 for the results of security testing, so that a security team can catalogue vulnerability scans and penetration tests, see the findings against the systems they affect, and follow the trend across test runs.

Status (2026-10-27): the egeria changes are merged into `main` for 6.3 (odpi/egeria#9386).  Every flow below has been exercised end to end against a platform built from them.  pyegeria 6.2.11 has also been tried against that platform - see [What already works](#what-already-works).

---

## Background

Each run of a security test is catalogued as a *SurveyReport*.  Since a survey report is a type of asset, it is created through the **Asset Maker API**; its annotations are created and linked through the **Data Discovery API**.  The report's `category` says what kind of test it was - for example `Vulnerability Scan Report` or `Penetration Test Results`.

```
SurveyReport --ReportSubject--> Asset that was tested
SurveyReport --ReportedAnnotation--> SecurityFindingAnnotation (or a subtype), one per finding
SurveyReport --ReportedAnnotation--> SecurityPostureAnnotation, the summary of the run

Asset that was tested --AssociatedAnnotation--> finding
Catalogued element named by affectedLocation or compromisedResources --AssociatedAnnotation--> finding

Finding from the previous run --AnnotationExtension--> the same finding in this run
Finding --AnnotationExtension--> a finding the tester chained onto it
```

The new types work with the existing annotation mechanisms:

- The scanner's own identifier for a finding goes in the annotation's `identifier` property, so the same finding can be recognized in later runs.
- The vulnerability type can be attached with *ReferenceValueAssignment* to a *ReferenceDataValue* from the security team's reference data.
- False positives and accepted risks are recorded with an *AnnotationReview*.
- A finding that needs someone to act on it can be raised as an incident report.

---

## The new types (model 0665)

All four are entities.  The properties classes are registered as JSON subtypes, so a request body uses the class names below.

### SecurityFindingAnnotation

- Supertype: **Annotation**.  Used directly for findings that are neither a known vulnerability nor a penetration test finding, such as an insecure configuration.
- JSON properties class: `SecurityFindingAnnotationProperties` (a subtype of `AnnotationProperties`).
- Type GUID: `6a9ac809-aee9-4785-a3b0-4be237f81c08`.

| Attribute | Type | Notes |
|---|---|---|
| `severity` | string | Use the CVSS ratings: `None`, `Low`, `Medium`, `High`, `Critical`. |
| `cvssScore` | float | CVSS base score, 0.0 to 10.0. |
| `cvssVector` | string | For example `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`. |
| `vulnerabilityIdentifiers` | array of string | For example CVE identifiers. |
| `weaknessIdentifiers` | array of string | For example CWE identifiers. |
| `affectedLocation` | string | Host and port, URL, file path or package.  If the element there is catalogued, link it with *AssociatedAnnotation* too. |
| `evidence` | string | For example the request and response that demonstrated the finding. |
| `remediation` | string | The recommended fix. |
| `exploitAvailable` | boolean | Is an exploit publicly available? |

### VulnerabilityAnnotation

- Supertype: **SecurityFindingAnnotation**.  A known vulnerability in the software used by a resource, typically from a vulnerability scan.
- JSON properties class: `VulnerabilityAnnotationProperties`.
- Type GUID: `e743e3a7-6848-4e4d-bc05-aace812aa21e`.

| Attribute | Type | Notes |
|---|---|---|
| `packageURL` | string | Package URL (purl), for example `pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1`. |
| `installedVersion` | string | |
| `fixedVersion` | string | |
| `patchAvailable` | boolean | |

### PenetrationTestFindingAnnotation

- Supertype: **SecurityFindingAnnotation**.  A weakness that a penetration test was able to exploit.
- JSON properties class: `PenetrationTestFindingAnnotationProperties`.
- Type GUID: `33b327e5-4afa-4445-8b42-5e3c36cd97a6`.

| Attribute | Type | Notes |
|---|---|---|
| `attackVector` | string | For example `Network`, `Adjacent network`, `Local`, `Physical`, `Social engineering`. |
| `attackTechniques` | array of string | For example MITRE ATT&CK technique identifiers such as `T1190`. |
| `privilegesGained` | string | |
| `compromisedResources` | array of string | Names of the resources reached or controlled.  If they are catalogued, link each with *AssociatedAnnotation* too. |
| `reproductionSteps` | string | |

### SecurityPostureAnnotation

- Supertype: **ResourceMeasureAnnotation** (so it also has `resourceProperties`).  The summary of one test run.
- JSON properties class: `SecurityPostureAnnotationProperties` (a subtype of `ResourceMeasureAnnotationProperties`).
- Type GUID: `3ef4ffc5-af73-444f-82b0-403fa2cce4ee`.

| Attribute | Type | Notes |
|---|---|---|
| `findingCountsBySeverity` | map of string to long | For example `{"Critical": 1, "High": 4}`. |
| `resourcesInScopeCount` | long | |
| `resourcesTestedCount` | long | |
| `newFindingCount` | long | Findings seen for the first time in this run. |
| `resolvedFindingCount` | long | Findings from earlier runs that are no longer detected. |

---

## The API operations

No new operations were needed: the existing Asset Maker and Data Discovery operations handle the new types.  All are `POST`, under `{{baseURL}}/servers/{{viewServer}}/api/open-metadata/`.

| Step | Operation | Path | Existing pyegeria method |
|---|---|---|---|
| Create the report | createAsset | `asset-maker/assets` with `SurveyReportProperties` | `AssetMaker.create_asset` |
| Create a finding | createAnnotation | `data-discovery/annotations` | `DataDiscovery.create_annotation` |
| Create a finding already linked to its report | createAnnotation, with `parentGUID` = report, `parentRelationshipTypeName` = `ReportedAnnotation`, `parentAtEnd1` = `true` | `data-discovery/annotations` | `DataDiscovery.create_annotation` |
| Link a finding to its report | attachAnnotationToReport | `data-discovery/survey-reports/{surveyReportGUID}/new-annotations/{annotationGUID}/attach` | `attach_annotation_to_report` |
| Link a finding to an affected element | (AssociatedAnnotation) | `data-discovery/elements/{elementGUID}/associated-annotations/{annotationGUID}/attach` | `link_annotation_to_described_element` |
| Link a finding to the same finding in the previous run | linkAnnotationToItsPredecessor (AnnotationExtension) | `data-discovery/annotations/{previousAnnotationGUID}/later-annotations/{newAnnotationGUID}/attach` | `link_annotation_to_its_predecessor` |
| List a report's findings | getNewAnnotations | `data-discovery/survey-reports/{surveyReportGUID}/new-annotations` | `get_new_annotations` |
| List an element's findings | (AssociatedAnnotation) | `data-discovery/elements/{elementGUID}/associated-annotations` | `get_annotations_for_element` |
| Retrieve, find, update, delete | | `data-discovery/annotations/...` | `get_annotation_by_guid`, `find_annotations`, `get_annotations_by_annotation_type`, `update_annotation`, `delete_annotation` |

---

## What already works

Tried with pyegeria 6.2.11 against a platform built from the branch:

- `DataDiscovery.create_annotation` with a dict body whose properties class is `VulnerabilityAnnotationProperties` creates the annotation, and every security property is stored.
- `get_annotation_by_guid(..., output_format="JSON")` returns all the security properties in `properties`, with the right `class`.

The gaps are in output and convenience, not in the calls themselves.

### Unset numbers and flags (ISSUE-166)

Fixed in Egeria 6.3 (merged into `main` on 2026-10-27), for every Open Metadata Framework property bean, not only the security annotations:

- Numeric and boolean properties are now `Integer`, `Long`, `Float` and `Boolean` with a `null` default.  A value that is not set is not stored, and is left out of the response, so `cvssScore`, `exploitAvailable`, `patchAvailable` and the posture counts are simply absent when nobody set them.
- A merge update that leaves a number or flag out no longer resets it: `update_annotation` with only `reproductionSteps` keeps the stored `cvssScore` and `exploitAvailable`.  The Dr.Egeria `SecurityFindingProcessor` workaround that copies the current values into every merge update can go.
- When a value is absent, its default is in the `defaultValue` additional property of the property's valid metadata value (category `Open Metadata Types`, set `propertyName`).  For example `exploitAvailable` and `patchAvailable` default to `false`, and `cvssScore` to `0.0`.  For a findings table, leaving an absent value blank - as the PR #495 rows already do - is still the right display; the default says what Egeria assumes, not what anyone assessed.

---

## What pyegeria needs

1. **Pydantic models** for the four properties classes, so that bodies can be built and validated as models rather than as dicts:
   - `SecurityFindingAnnotationProperties` (Annotation fields plus the table above)
   - `VulnerabilityAnnotationProperties` and `PenetrationTestFindingAnnotationProperties` (both extend it)
   - `SecurityPostureAnnotationProperties` (ResourceMeasureAnnotation fields plus the table above)
2. **Output formats.**  `_extract_annotation_properties` and the default report spec show only the common columns, so the `DICT`, `TABLE` and `MD` outputs drop every security property today.  Report specs that would be most useful:
   - **Security Findings** - one row per finding: display name, type, severity, CVSS score, CVE/CWE identifiers, affected location, exploit available, and for vulnerabilities the package URL and fixed version.  Sorted by CVSS score, highest first.  This is the triage view for one report, or for one system through `get_annotations_for_element`.
   - **Penetration Test Findings** - attack vector, ATT&CK techniques, privileges gained, compromised resources, and remediation.  This is the view the tester hands back.
   - **Security Posture** - one row per run: report name, completion time, counts by severity, resources in scope and tested, new and resolved findings.  Across a series of reports this shows whether the estate is getting more secure.
   Markdown and Excel/CSV output would both be useful; findings are often shared as spreadsheets.
3. **Convenience methods** (optional) on `DataDiscovery`, following the existing naming:
   - `create_security_finding(report_guid, properties, affected_element_guids=None)` - creates the annotation under the report and links it to each affected element in one call.
   - `get_security_findings(element_guid=None, report_guid=None, min_severity=None, ...)` - returns only the security finding subtypes, filtered by severity.
   - `get_security_posture_history(element_guid)` - the posture annotations from the reports about one element, oldest first.
4. **`delete_annotation`** makes `body` a required argument; most other delete methods default it to `None`.

---

## What Dr.Egeria needs

New commands, with templates in `templates/basic` and `templates/advanced` like the existing ones.  Scanners will normally load their results through pyegeria or an integration connector, so these commands are mainly for findings from manual penetration tests and for reviewing results.

**Create Survey Report / Update Survey Report**
- Display Name (required), Qualified Name, Description, Category (for example `Penetration Test Results`), Purpose, Start Time, Completion Time.
- Optional **Report Subjects** (reference name list): creates a *ReportSubject* relationship to each asset that was tested.

**Create Security Finding / Create Vulnerability Finding / Create Penetration Test Finding** (and the matching Update commands)
- Display Name (required), Qualified Name, Identifier, Description, plus the attributes in the tables above for the chosen type.  Severity should take the valid values `None`, `Low`, `Medium`, `High` and `Critical`.
- **Survey Report** (reference name): creates the *ReportedAnnotation* relationship.
- **Affected Elements** (reference name list): creates an *AssociatedAnnotation* relationship to each catalogued element - the tested asset, plus any catalogued element named by `affectedLocation` or `compromisedResources`.
- Optional **Previous Finding** (reference name): creates the *AnnotationExtension* relationship to the same finding in an earlier run.
- Optional **Vulnerability Type** (reference name): creates a *ReferenceValueAssignment* to a reference data value.

**Create Security Posture Summary**
- Survey Report (reference name, required), and the counts in the SecurityPostureAnnotation table.

**View Security Findings / View Security Posture**
- Report commands that produce the report specs described for pyegeria above.

---

## Example flow (Coco Pharmaceuticals)

1. Simon Burr's team runs its quarterly penetration test of the supplier portal.  Si creates a survey report `SurveyReport::Supplier Portal::2026-Q4 Penetration Test` with category `Penetration Test Results`, through Asset Maker.
2. The tester finds SQL injection in the supplier search.  Si records it as a *PenetrationTestFindingAnnotation* under the report: severity `High`, CVSS 8.6, CWE-89, attack vector `Network`, technique `T1190`, privileges gained "read access to the supplier database", compromised resources `Supplier Master Register`.
3. He links the finding with *AssociatedAnnotation* to the supplier portal asset that was tested and to the catalogued Supplier Master Register.  The finding now appears with both, and the Supplier Master Register's owner can see it.
4. A *SecurityPostureAnnotation* summarizes the run: 1 High finding, 3 resources in scope, all 3 tested, 1 new finding.
5. After the fix is deployed, the next quarter's test no longer finds the weakness.  Its posture summary records 1 resolved finding, and the trend across the two reports shows the improvement.

The Coco workbooks will get a Dr.Egeria example of this once the commands exist.
