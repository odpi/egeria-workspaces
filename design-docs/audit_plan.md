The egeria-audit tile in the portal provides easy access to auditors and owners on the status of the exceptions, certifications and licenses in use in the organization, plus details of who has access to egeria.  It has four tabs:

- Exceptions
- Certifications
- Licenses
- Users

Include asof time where sensible (I don't think it is useful for the users tab)

<!-- ───────────────────────── REVIEW COMMENTS (Claude, 2026-06-22) ─────────────────────────
> 💬 **Architecture.** This is a new standalone SPA (like `tech-catalog.html` / `type-explorer.html`),
> so it needs: `egeria-audit.html` + an `audit_handler.py` router + a portal tile in
> `demo-portal.html` + an Apache `<Location>` proxy route — all in **both** quickstart and
> freshstart (dual-file convention; pick a `78xx`/`88xx` route, e.g. `/egeria-audit`). Reuse
> `egeria-shared-ui.js`: `egeriaFetch` + `CredContext` (token auth), `TimeSlider`, `renderMd`,
> and the cross-link pattern (`TYPE_TO_NAV` → `/egeria-explorer?guid=…&kind=…#<tab>` via
> `handleNavigate`) that the Catalog already uses.
>
> 💬 **Build the 3 relationship tabs as ONE shared component.** Exceptions / Certifications /
> Licenses are ~95% identical: a sortable/filterable relationship table + a 3-section foldable
> detail panel + actor resolution + cross-links. Parameterise a single `AuditRelationshipTab`
> by `{ relationshipType, columns, actorRoles }` instead of triplicating (the modularization
> lesson from MOD-2/3). `actorRoles` = `['steward']` / `['certifiedBy','custodian','recipient']`
> / `['licensedBy','custodian','licensee']`.
>
> 💬 **Backend verified (deployed pyegeria 6.0.15.x).** `ClassificationExplorer.get_relationships`,
> `.get_element_by_guid`, `.get_element_by_unique_name`, `RuntimeManager.get_platforms_by_type`,
> and `SecurityOfficer` (`get_user_list` / `get_user_account` / `set_user_account`) all exist.
> **Note:** `SecurityOfficer` isn't in the top-level `pyegeria` namespace — it lives in
> `pyegeria.egeria_tech_client` / `security_officer.py`; verify the import path in the handler.
>
> 💬 **Demo data (quickstart, today).** `Exception` → 5 relationships, `License` → 2,
> `Certification` → **0** (returns the "no elements" string). So the Certifications tab will be
> empty until cert data is loaded — design the empty state, and flag whether demo certs are
> expected (cf. HV-1/2/3 "built; no data").
>
> 💬 **as_of_time.** Agreed: the 3 relationship tabs, not Users. BUT `get_relationships` /
> `get_element_by_guid` have **no `as_of_time` param** — they take a `body`. Per the LE-3 audit,
> passing `as_of_time` as a kwarg is a **silent no-op**; `asOfTime` must go **in the request
> body** (`body={… , "asOfTime": iso}`). Reuse the shared `TimeSlider`, and runtime-verify it
> actually filters before relying on it (some Egeria endpoints accept but ignore it).
─────────────────────────────────────────────────────────────────────────────────────────── -->

## Exceptions tab

The Exceptions tab displays relationships of type Exception.  These relationships can be retrieved using ClassificationExplorer.get_relationships(relationship_type="Exception").  This returns a list of MetadataRelationshipSummary objects.  A MetadataRelationshipSummary object has 4 parts to it:

- relationshipHeader - containing the unique identifier, the users that have created/updated the relationship and other useful information about the origin of the relationship
- relationshipProperties - these properties describe the exception.
- end1 - this is a stub describing the element that the exception has been noted against.  It includes the header information for the element (useful for retrieving the type and guid of the element) and an optional unique name (typically this is the qualifiedName property of the element).
- end2 - this is a stub of the ExceptionType element that describes the type of exception that have been noted for the element at end1.

By default, the full list of retrieved exception relationships is displayed in a table.  The table has the following columns.  

- Affected Element Name - from end1.uniqueName - if this is null then use the GUID from end1.guid
- Affected Element Type - from end1.type.typeName
- Creation Time - from relationshipHeader.versions.createTime
- Created by - from relationshipHeader.versions.createdBy
- Last Updated - from relationshipHeader.versions.updateTime - may be null in which case use relationshipHeader.versions.createTime
- Label - from relationshipProperties.label
- Description - from relationshipProperties.description
- Steward - from relationshipProperties.steward
- Exception Type - from end2.uniqueName - if this is null then use the GUID from end2.guid

The user can sort the rows by each column.  The user may also want to filter the exceptions listed in the  table by any of the column values. 

When a row in the table is selected, a details panel shows three sets of details - each once should be foldable.

- the properties of the element at end 1
- all the properties from relationshipProperties plus extra details of the steward
- the properties of the exception type at end 2

Use ClassificationExplorer.get_element_by_guid(guid=end1.guid, graph_query_depth=0) to retrieve the properties for the element at end1.  Display all of the values returned.  If the element's type is displayable through another part of the portal, add a button to jump to the full display for that element.

The relationship properties include 3 properties called steward, stewardTypeName and stewardPropertyName.  Together they uniquely identify an actor.  By default, steward contains the guid of the actor in which case, use ClassificationExplorer.get_element_by_guid(guid=steward, graph_query_depth=0).  However, if stewardPropertyName is specified, use ClassificationExplorer.get_element_by_unique_name(body={"propertyValue": steward, "propertyName": stewardPropertyName, "metadataElementTypeName": stewardTypeName, "graphQueryDepth": 0).  Display all of the values returned including header properties.  Add a button to jump to the full display of the actor in egeria-explorer's actors panel.

Use ClassificationExplorer.get_element_by_guid(guid=end2.guid, graph_query_depth=0) to retrieve the properties for the exception type at end1.  Display all of the values returned including header properties.  Add a button to jump to the full display of the exception type in egeria-explorer's governance definition panel.

<!-- ───────────────────────── REVIEW COMMENTS — Exceptions (applies to all 3 tabs) ─────────
> 💬 **Lazy-load the detail panel.** Fetch the three detail sets (end1, end2, steward) **only
> when a row is selected**, not for every row up front — otherwise it's an N+1 query storm on
> large tables (cf. the catalog-tree perf fix, 28s → 0.4s). The table itself needs only the
> data already in each `MetadataRelationshipSummary`, so the list renders from one
> `get_relationships` call; detail fetches are on-select.
>
> 💬 **Shared actor resolver.** The `steward` / `stewardTypeName` / `stewardPropertyName`
> tri-property pattern repeats for `certifiedBy`/`custodian`/`recipient` and
> `licensedBy`/`custodian`/`licensee`. Write **one** `resolveActor(name, propertyName, typeName)`
> helper: GUID path → `get_element_by_guid`; unique-name path → `get_element_by_unique_name`.
>
> 💬 **Spec typo.** The `get_element_by_unique_name` body is missing a closing brace and uses a
> positional API that differs from the deployed signature. Verified signature is
> `get_element_by_unique_name(name, property_name, …, body=…)`. Intended body:
> `{"propertyValue": steward, "propertyName": stewardPropertyName,
> "metadataElementTypeName": stewardTypeName, "graphQueryDepth": 0}` — note the closing `}`.
>
> 💬 **Cross-links verified.** "Jump to actors panel" →
> `/egeria-explorer?guid=<actorGuid>&kind=<roles|profiles|identities>#actors` — ✅ `ActorsView`
> reads `?guid`/`?kind` on cold load, so it selects on arrival. "Governance definition panel" →
> `…?guid=<guid>#governance` — ✅ `GovernanceView` reads `?guid` on cold load. For the end1
> element "if displayable elsewhere" button, reuse the Catalog/Explorer `TYPE_TO_NAV` +
> `_elementIsLinkable` resolver so it routes generically by typeName (don't hand-roll per type).
─────────────────────────────────────────────────────────────────────────────────────────── -->

## Certifications tab

The Certifications tab displays relationships of type Certification.  These relationships can be retrieved using ClassificationExplorer.get_relationships(relationship_type="Certification").  This returns a list of MetadataRelationshipSummary objects.  A MetadataRelationshipSummary object has 4 parts to it:

- relationshipHeader - containing the unique identifier, the users that have created/updated the relationship and other useful information about the origin of the relationship
- relationshipProperties - these properties describe the certification.
- end1 - this is a stub describing the element that the certification has been awarded to.  It includes the header information for the element (useful for retrieving the type and guid of the element) and an optional unique name (typically this is the qualifiedName property of the element).
- end2 - this is a stub of the CertificationType element that describes the type of certification that have been awarded for the element at end1.

By default, the full list of retrieved certification relationships is displayed in a table.  The table has the following columns.  

- Certified Element Name - from end1.uniqueName - if this is null then use the GUID from end1.guid
- Certified Element Type - from end1.type.typeName
- Creation Time - from relationshipHeader.versions.createTime
- Created by - from relationshipHeader.versions.createdBy
- Last Updated - from relationshipHeader.versions.updateTime - may be null in which case use relationshipHeader.versions.createTime
- Certificate Id - from relationshipProperties.certificateId
- Certified By - from relationshipProperties.certifiedBy
- Coverage Start  - from relationshipProperties.coverageStart - may be null
- Coverage End  - from relationshipProperties.coverageEnd - may be null
- Certification Type - from end2.uniqueName - if this is null then use the GUID from end2.guid

The user can sort the rows by each column.  The user may also want to filter the certifications listed in the  table by any of the column values. 

When a row in the table is selected, a details panel shows three sets of details - each once should be foldable.

- the properties of the element at end 1
- all the properties from relationshipProperties plus extra details of the certifiedBy, custodian and recipient actors
- the properties of the certification type at end 2

Use ClassificationExplorer.get_element_by_guid(guid=end1.guid, graph_query_depth=0) to retrieve the properties for the element at end1.  Display all of the values returned.  If the element's type is displayable through another part of the portal, add a button to jump to the full display for that element.

The relationship properties include properties for three actors associated with the certification: certifiedBy, custodian and recipient.  Where they are specified, details of these actors should be displayed:

- Each actor has 3 properties called, for example,  certifiedBy, certifiedByTypeName and certifiedByPropertyName.  These are referred to as xxx, xxxPropertyName and xxxTypeName below.  Together they uniquely identify an actor.  By default, xxx contains the guid of the actor in which case, use ClassificationExplorer.get_element_by_guid(guid=xxx, graph_query_depth=0).  However, if the xxxPropertyName is specified, use ClassificationExplorer.get_element_by_unique_name(body={"propertyValue": xxx, "propertyName": xxxPropertyName, "metadataElementTypeName": xxxTypeName, "graphQueryDepth": 0).  Display all of the values returned including header properties.  Add a button to jump to the full display of the actor in egeria-explorer's actors panel.

Use ClassificationExplorer.get_element_by_guid(guid=end2.guid, graph_query_depth=0) to retrieve the properties for the certification type at end1.  Display all of the values returned.  Add a button to jump to the full display of the certification type in egeria-explorer's governance definition panel.

<!-- REVIEW COMMENT — Certifications
> 💬 Same shared `AuditRelationshipTab` as Exceptions — only `columns` and `actorRoles`
> (`certifiedBy`/`custodian`/`recipient`) differ. Minor clarity point: `Certified By` /
> `Licensed By` appear **both** as a raw relationship-property column **and** as an actor to
> resolve in the detail panel — keep the column showing the raw stored value and resolve the
> actor only in the foldable detail, so the table stays cheap.
-->

## Licenses tab

The Licenses tab displays relationships of type License.  These relationships can be retrieved using ClassificationExplorer.get_relationships(relationship_type="License").  This returns a list of MetadataRelationshipSummary objects.  A MetadataRelationshipSummary object has 4 parts to it:

- relationshipHeader - containing the unique identifier, the users that have created/updated the relationship and other useful information about the origin of the relationship
- relationshipProperties - these properties describe the license.
- end1 - this is a stub describing the element that the license has been awarded to.  It includes the header information for the element (useful for retrieving the type and guid of the element) and an optional unique name (typically this is the qualifiedName property of the element).
- end2 - this is a stub of the LicenseType element that describes the type of license that have been awarded for the element at end1.

By default, the full list of retrieved license relationships is displayed in a table.  The table has the following columns. 

- Licensed Element Name - from end1.uniqueName - if this is null then use the GUID from end1.guid
- Licensed Element Type - from end1.type.typeName
- Creation Time - from relationshipHeader.versions.createTime
- Created by - from relationshipHeader.versions.createdBy
- Last Updated - from relationshipHeader.versions.updateTime - may be null in which case use relationshipHeader.versions.createTime
- License Id - from relationshipProperties.licenseId
- Licensed By - from relationshipProperties.licensedBy
- Coverage Start  - from relationshipProperties.coverageStart - may be null
- Coverage End  - from relationshipProperties.coverageEnd - may be null
- License Type - from end2.uniqueName - if this is null then use the GUID from end2.guid

The user can sort the rows by each column.  The user may also want to filter the license listed in the table by any of the column values. 

When a row in the table is selected, a details panel shows three sets of details - each once should be foldable.

- the properties of the element at end 1
- all the properties from relationshipProperties plus extra details of the licensedBy, custodian and licensee actors
- the properties of the license type at end 2

Use ClassificationExplorer.get_element_by_guid(guid=end1.guid, graph_query_depth=0) to retrieve the properties for the element at end1.  Display all of the values returned.  If the element's type is displayable through another part of the portal, add a button to jump to the full display for that element.

The relationship properties include properties for three actors associated with the license: licensedBy, custodian and licensee.  Where they are specified, details of these actors should be displayed:

- Each actor has 3 properties called, for example,  licensedBy, licensedByTypeName and licensedByPropertyName.  These are referred to as xxx, xxxPropertyName and xxxTypeName below.  Together they uniquely identify an actor.  By default, xxx contains the guid of the actor in which case, use ClassificationExplorer.get_element_by_guid(guid=xxx, graph_query_depth=0).  However, if the xxxPropertyName is specified, use ClassificationExplorer.get_element_by_unique_name(body={"propertyValue": xxx, "propertyName": xxxPropertyName, "metadataElementTypeName": xxxTypeName, "graphQueryDepth": 0).  Display all of the values returned including header properties.  Add a button to jump to the full display of the actor in egeria-explorer's actors panel.

Use ClassificationExplorer.get_element_by_guid(guid=end2.guid, graph_query_depth=0) to retrieve the properties for the license type at end1.  Display all of the values returned.  Add a button to jump to the full display of the license type in egeria-explorer's governance definition panel.

## Users tab

The users tab displays the user accounts defined for each platform there are options to change the user's account status.  The list of platforms can be retrieved using RuntimeManager.get_platforms_by_type(body={"filter" : "OMAG Server Platform", "graphQueryDepth" : 0}).  For each platform extract:

- the guid (from the elementHeader.guid)
- the display name (from properties.displayName - or if this is null use properties.qualifiedName)

The user is able to select the platform they are interested in from a dropdown.  Then the list of users is displayed.

This is retrieved using SecurityOfficer.get_user_list(platform_guid=guid of selected platform).  This returns the list of user names.  For each name returned use SecurityOfficer.get_user_account(platform_guid=guid of selected platform, user_id=user name).

The users are displayed in a table with the following columns:

- User Name - from userAccount.userName
- Account Type - from userAccount.userAccountType.  This is an enum
- Display Name - from userAccount.displayName
- Account Status - from userAccount.userAccountStatus.  This is an enum

It is possible to update the account status of a particular user using SecurityOfficer.set_user_account().
It is possible to display all of the properties returned for a user in their userAccount.

<!-- ───────────────────────── REVIEW COMMENTS — Users tab ─────────────────────────
> ⚠️ **🔒 Security — the big one.** `set_user_account` **mutates** account status — a privileged
> admin action, and the rest of this tile is read-only audit. This must be: (1) **role-gated**
> (an "auditor/owner" audience is read-mostly — only an admin role should see/use the status
> control; tie into the freshstart `SERVER_MANAGED_AUTH`/admin model and demo-mode gating);
> (2) behind a **confirm dialog** (irreversible-ish, outward-facing); (3) ideally the change is
> itself **logged/audited**. Per the harness safety rules, an account-status change is an
> "access control / account settings" mutation — do not let any logged-in portal user flip it.
>
> 💬 **SecurityOfficer exists** (`get_user_list(platform_name|platform_guid, status, user_type)`,
> `get_user_account(…, user_id)`, `set_user_account(…, body)`) but lives in
> `pyegeria.egeria_tech_client` / `security_officer.py`, not the top-level namespace — import
> accordingly. `set_user_account` takes a **body**; confirm what fields a status-only change
> needs (likely `userAccountStatus` + identifiers).
>
> 💬 **N+1 load.** `get_user_list` → then `get_user_account` **per user** is a serial fan-out
> (same shape as the catalog-tree perf issue). For a platform with many users this is slow —
> either show the list first and **lazy-load each account on expand**, or fetch with a clear
> loading state + spinner. `get_user_list` already takes `status` / `user_type` filters — push
> filtering server-side where possible.
>
> 💬 **Enums.** `userAccountType` and `userAccountStatus` are enums — need value→label maps and
> the valid-status set for the change control's dropdown. Pull the allowed values from the
> Egeria enum if exposed, else hard-code with a comment to keep in sync.
>
> 💬 **`get_platforms_by_type` signature.** Deployed param is `filter_string` (it also accepts a
> `body`). The spec's `body={"filter": "OMAG Server Platform", …}` — verify the body key is
> `filter` vs `filterString`/`metadataElementTypeName`; simplest is `filter_string="OMAG Server Platform"`.
>
> 💬 No as_of_time here — agreed (live account state). Good call.
─────────────────────────────────────────────────────────────────────────── -->





