# Technology Types — Catalog Card Design Plan

## What are Technology Types?

Technology Types are **Valid Metadata Values** — not part of the Egeria Open Metadata Type System itself, but a catalogue of "recipes" for how to deploy, catalog, and govern specific technologies (PostgreSQL, Kafka, Unity Catalog, CSV files, etc.). They're definitions that live as `ValidMetadataValue` elements and are connected to:

- **Catalog Templates** — parameterised blueprints for creating the right Egeria metadata elements when you onboard a new instance of that technology
- **Governance Action Processes** — workflows that can be applied (e.g. survey-postgres-server, integrate-kafka)
- **External References** — links to project documentation
- **A hierarchy** — parent/child relationships ("Root Technology Type" → "Database Server" → "PostgreSQL Server")
- **Live instances** — actual deployed elements in your catalog that match this type

They are the authoritative source of "what does Egeria know how to do with X?" and are the entry point for provisioning new catalog entries.

---

## Key pyegeria API (`AutomatedCuration` module)

`AutomatedCuration` takes `view_server=`, `platform_url=`, `user_id=`, `user_pwd=` — same constructor pattern as `AssetMaker`.

| Method | Notes |
|---|---|
| `get_all_technology_types(output_format="JSON")` | Returns flat list of all tech type dicts. Wrapper for `find_technology_types("*")`. |
| `find_technology_types(search_string, output_format="JSON")` | Search by name fragment. Default `limit_results_by_status=["ACTIVE"]`. Returns list of summary dicts. |
| `get_tech_type_detail(filter_string=name, output_format="JSON")` | **Lookup is by name string, not GUID.** Returns a single detailed dict for the exact named type. POST to `/technology-types/by-name`. |
| `get_tech_type_hierarchy(filter_string="Root Technology Type")` | Hierarchy tree starting from the named root. Passing `"*"` defaults to `"Root Technology Type"`. |
| `get_technology_type_elements(filter_string=name)` | Returns actual deployed catalog elements of this tech type. No wildcards — exact type name required. |
| `get_tech_types_for_open_metadata_type(type_name, tech_name)` | Reverse lookup: given an Open Metadata type (e.g. `"Database"`) and tech name, returns matching tech types. Useful for cross-navigation from asset detail. |
| `get_template_guid_for_technology_type(type_name)` | Returns the GUID of the primary catalog template for a type. |

### pyegeria additions

| Method | Status | Rationale |
|---|---|---|
| `get_tech_type_detail` accepting qualifiedName | **Already works** — `get_tech_type_by_name` (the underlying call) accepts qualified names. Use this as the lookup key now. | `qualifiedName` is unique and stable; avoids any displayName collision risk. |
| `get_tech_type_by_guid(guid)` | **Planned** — needs a new pyegeria method + a new backend REST endpoint (`/api/tech-catalog/tech-types/by-guid/{guid}`). | Cleanest long-term key for URL routing, detail fetch, and feedback anchor. |

**Current approach:** use `qualifiedName` as the URL key and detail lookup key. The `technologyTypeGUID` from the list response is used as the feedback/comments anchor.

### Other quirks

- **`find_technology_types` status filter defaults to `["ACTIVE"]`** — correct for browsing; no override needed unless you want inactive/draft types.
- **`get_tech_type_hierarchy` uses POST with `{"class": "FilterRequestBody", "filter": name}`.** The Egeria endpoint is `/technology-types/hierarchy`.
- **`get_technology_type_elements` is exact-match** — no wildcards. Pass the `displayName` returned by the list call.

---

## Data Model

### List element (from `find_technology_types` / `get_all_technology_types`)

```
{
  "technologyTypeGUID": "...",
  "qualifiedName":      "DeployedImplementationType:PostgreSQL Server",
  "displayName":        "PostgreSQL Server",
  "description":        "...",
  "category":           "...",           // if present
  "mermaidGraph":       "graph ...",     // short overview diagram
  "specificationMermaidGraph": "graph ..." // structure diagram
}
```

### Detail element (from `get_tech_type_detail`)

Everything in the list element PLUS:

```
{
  "catalogTemplates": [
    {
      "displayName": "Create PostgreSQL Server",
      "description": "...",
      "guid":        "...",
      "resourceUse": "create-catalog-entry",
      "specification": {
        "placeholderProperty": [
          {
            "name":        "serverName",
            "dataType":    "string",
            "description": "...",
            "example":     "MyPostgresServer",
            "required":    true
          },
          ...
        ]
      },
      "relatedElement": {
        "properties": { "displayName": "...", "qualifiedName": "..." }
      }
    }
  ],
  "governanceActionProcesses": [
    {
      "relatedElement": {
        "properties": { "displayName": "survey-postgres-server", "description": "...", "qualifiedName": "..." }
      },
      "resourceUse": "survey",
      "specification": {
        "supportedRequestParameter": [
          { "name": "serverGUID", "dataType": "string", "description": "...", "required": true }
        ]
      }
    }
  ],
  "externalReferences": [
    {
      "relatedElement": {
        "properties": { "displayName": "PostgreSQL Project", "qualifiedName": "...", "description": "..." }
      },
      "url": "https://www.postgresql.org"
    }
  ]
}
```

---

## UI Design

### Card placement

New tile in the Catalog splash screen alongside Glossary, Infrastructure, Data Assets, APIs, Processes. Icon: `⚙` or `🔧`.

Route: `#tech-types`

### Layout

Same two-column `SidebarDetail` layout as every other section (resizable divider, left sidebar + right detail pane).

### Sidebar (left)

**Filter/search bar** at the top — calls `find_technology_types(search_string)`.

**View toggle**: Flat List | Hierarchy Tree

- **Flat list** (default): items sorted by `displayName`. Show `displayName` as the primary label, `category` or parent type as a dim sub-label. Small badge showing template count (`catalogTemplates.length`) if > 0.
- **Hierarchy tree** (toggle): calls `get_tech_type_hierarchy("Root Technology Type")`, renders a collapsible tree. Clicking a node loads its detail.

**Item format**:
```
⚙ PostgreSQL Server                    [2 templates]
    Database Server
```

### Detail pane (right)

Triggered by clicking a sidebar item. Calls `get_tech_type_detail(filter_string=qualifiedName)`.

The detail pane is organised around **what the user can do with this tech type**, not just what data it carries. The central concept is *Resources* — each resource is something actionable: create a catalog entry, run a survey, link to documentation.

#### Rendering order

1. **Header**: displayName (h2) + EgeriaFeedbackWidget (far right)
2. **Qualified name** in dim monospace
3. **Description** (rendered as markdown via `renderMd`)
4. **Mermaid diagrams** — `AvailableMermaidDiagrams` over `mermaidGraph` and `specificationMermaidGraph`

5. **Resources** section — the heart of the detail pane, grouped by resource type:

   **5a. Catalog Templates** ("How to onboard a new instance")
   One card per template. Each card has:
   - Template name (bold) + `resourceUse` badge (e.g. `create-catalog-entry`)
   - Description
   - **Placeholder Properties table** — the key onboarding information:

     | Name | Type | Required | Example | Description |
     |---|---|---|---|---|
     | serverName | string | ✓ | MyPostgresServer | The name of the server host |
     | portNumber | int | | 5432 | Listening port |
     | … | | | | |

     Sorted: required properties first, then optional. Visually distinguish required rows (bold name or coloured indicator).
   - Link to the related template element (if GUID is available)

   **5b. Governance Processes** ("What Egeria can do automatically")
   One card per process. Each card has:
   - Process name (bold) + `resourceUse` badge (e.g. `survey`, `catalog`, `provision`)
   - Description
   - **Request Parameters table** (from `supportedRequestParameter`):

     | Name | Type | Required | Description | Example |
     |---|---|---|---|---|
     | serverGUID | string | ✓ | GUID of the server asset to survey | … |
     | … | | | | |

   - **Process Steps** — if step data is available in the response, show a numbered list of step names and descriptions. If steps require a separate fetch (full `GovernanceActionProcess` detail), make it a lazy-loaded sub-section (expand button). *(Needs live data inspection — see TT-Q8.)*

   **5c. External References** ("Documentation and project links")
   Simple card with a list of labelled, clickable links:
   - `displayName` as the link label (e.g. "PostgreSQL Project")
   - `url` as the href, opened in a new tab
   - `description` shown as a dim sub-line if present

6. **Live Instances sub-pane** (lazy-loaded, expand button)
   Calls `/api/tech-catalog/tech-types/{qualifiedName}/elements`. Shows deployed catalog elements of this type. Each row shows name + type badge + "View →" cross-nav button (via `TYPE_TO_NAV`). Empty state: "No catalog entries of this type yet."

7. **EgeriaCommentsSection** — uses `technologyTypeGUID` as the GUID anchor

#### Resource grouping rationale

The three resource groups map to the three actions a user cares about:
- **Catalog Templates** → "I want to register a new instance of this technology"
- **Governance Processes** → "I want Egeria to do something with an existing instance"
- **External References** → "I want to learn more about this technology"

Keeping them visually distinct (separate section headers, different accent colours) prevents the user from confusing a template placeholder with a process parameter.

### Handling the name-not-GUID problem

**Current path (qualifiedName):** The list API returns both `displayName` and `qualifiedName`. The SPA passes `qualifiedName` URL-encoded to the detail route; the backend calls `get_tech_type_detail(filter_string=qualifiedName)`. `qualifiedName` is unique and stable — no collision risk. `technologyTypeGUID` from the list is used for feedback/comments.

**Future path (GUID):** Once `get_tech_type_by_guid` is available in pyegeria, the backend will add a `/by-guid/{guid}` endpoint and the SPA can switch to GUID-keyed routing (TT-8).

- List API returns `{ name, guid, qualifiedName, description, ... }`
- SPA stores the selected item's `name` and calls `GET /api/tech-catalog/tech-types/{encodedName}`
- Backend calls `ac.get_tech_type_detail(filter_string=name)`
- The `technologyTypeGUID` from the list can be used as the key for EgeriaFeedbackWidget / EgeriaCommentsSection

---

## Backend Design

### New handler: `tech_type_handler.py`

Or extend `tech_catalog_handler.py` with new routes under `/api/tech-catalog/tech-types/...`.

| Route | Call | Notes |
|---|---|---|
| `GET /api/tech-catalog/tech-types?q=` | `ac.find_technology_types(search_string=q)` | List/search |
| `GET /api/tech-catalog/tech-types/hierarchy?root=` | `ac.get_tech_type_hierarchy(filter_string=root)` | Tree from root |
| `GET /api/tech-catalog/tech-types/{qualifiedName}` | `ac.get_tech_type_detail(filter_string=qualifiedName)` | Detail by qualifiedName (URL-decoded). `qualifiedName` is unique — no collision risk. |
| `GET /api/tech-catalog/tech-types/{qualifiedName}/elements` | `ac.get_technology_type_elements(filter_string=displayName)` | Live instances. **Note:** `get_technology_type_elements` needs the `displayName` not the qualifiedName — extract from the already-loaded detail. |
| `GET /api/tech-catalog/tech-types/by-guid/{guid}` _(planned)_ | `ac.get_tech_type_by_guid(guid)` _(planned pyegeria method)_ | Future GUID-keyed route (TT-8). Add once pyegeria method available. |

### `_automated_curation` helper

```python
def _automated_curation(url, server, user_id, user_pwd):
    from pyegeria import AutomatedCuration
    u, s, uid, pwd = _creds(url, server, user_id, user_pwd)
    ac = AutomatedCuration(view_server=s, platform_url=u, user_id=uid, user_pwd=pwd)
    ac.create_egeria_bearer_token()
    return ac
```

### `_serialize_tech_type` for list items

Extract from the list response:
- `technologyTypeGUID` → `guid`
- `displayName`, `qualifiedName`, `description`
- `category` (if present)
- Template count from `catalogTemplates` length

### `_serialize_tech_type_detail` for detail

Pass through the full detail dict with normalised sub-structures:
- `catalogTemplates`: list with normalised placeholder names (`name`/`dataType`/`required`/`example`/`description`)
- `governanceActionProcesses`: list with `displayName`/`description`/`resourceUse`/`parameters`
- `externalReferences`: list with `displayName`/`url`
- `mermaidGraph`, `specificationMermaidGraph` passed through for `AvailableMermaidDiagrams`

---

## Open Questions

| # | Question | Impact |
|---|---|---|
| TT-Q1 | Does `get_tech_type_hierarchy` return a recursive tree or a flat parent-child list? Need to inspect live response to decide if we build a React tree or a flat grouped list. | UI architecture for hierarchy mode |
| TT-Q2 | What's the `category` field in the list response? Is it reliably populated, or should we derive grouping from the hierarchy? | Sidebar grouping |
| TT-Q3 | Can `get_technology_type_elements` be called with partial/wildcard names? The docstring says "no wildcards" — confirm against live data. | Elements sub-pane feasibility |
| TT-Q4 | Is `specificationMermaidGraph` meaningfully different from `mermaidGraph`? Need to see live examples to decide whether both are worth surfacing. | Diagram section design |
| TT-Q5 | Should the UI allow initiating a survey/governance process directly from the detail pane? This would call `initiate_gov_action_process(qualifiedName, targets=[{targetGUID}])` where the user provides a target GUID. | Scope creep vs. high value — defer to TT-7+ |
| TT-Q6 | `get_tech_type_detail` returns a single `element` (not a list). Confirm it never returns a list when multiple types share the same displayName. Will become moot once `get_tech_type_by_guid` is available. | Edge-case handling |
| TT-Q8 | Are governance process steps included in the `governanceActionProcesses` list returned by `get_tech_type_detail`, or do they require a separate call to get the full `GovernanceActionProcess` element? | Determines whether Process Steps are inline or lazy-loaded |

**Resolved:**
- TT-Q7 (feedback anchor): `technologyTypeGUID` is the `ValidMetadataValue` element GUID — confirmed by `_extract_tech_type_properties` which reads it from `element.get("technologyTypeGUID")`. Safe to use as the `EgeriaFeedbackWidget` / `EgeriaCommentsSection` GUID anchor.

---

## Phased Implementation

| Phase | Items | Dependency |
|---|---|---|
| **TT-1** | Backend: `_automated_curation` helper + list endpoint + detail endpoint (by qualifiedName). Serialize list and detail. | None |
| **TT-2** | Frontend: Catalog splash tile + flat sidebar list + basic detail pane (properties, description, external refs, mermaid) | TT-1 |
| **TT-3** | Frontend: Catalog Templates section (placeholder properties table) | TT-2 |
| **TT-4** | Frontend: Governance Processes section | TT-2 |
| **TT-5** | Frontend: EgeriaFeedbackWidget + EgeriaCommentsSection using `technologyTypeGUID` | TT-2 |
| **TT-6** | Frontend: Live Instances sub-pane (lazy-loaded, cross-nav to catalog sections) | TT-2 + live data test of `get_technology_type_elements` (TT-Q3) |
| **TT-7** | Frontend: Hierarchy tree view toggle | TT-2 + TT-Q1 answered from live data |
| **TT-8** | pyegeria: add `get_tech_type_by_guid(guid)`. Backend: add `/by-guid/{guid}` route. Frontend: switch routing to GUID. | pyegeria upstream change |


==> Othe considerations
A given tech type has a number of resources. For example, a "PostgreSQL Server" tech type has resources to create a catalog entry (catalog template), to survey an existing server (governance action process), and to link to the PostgreSQL project website (external reference). 
The UI should surface these resources in a way that makes it clear what actions the user can take with this tech type, and how to use the associated templates and processes. 
The placeholder properties in the catalog templates are especially important, as they provide the key information needed to onboard a new instance of that technology. Placeholder properties are best displayed as a table.
Similarly for Process properties, tables make a very clear format for showing the parameters needed to execute a process as well as process steps.

----

Egeria supports and renders many kinds of lineage.

You come in from an asset. From the asset you can:

