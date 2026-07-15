# Egeria Explorer — Extension History and Roadmap

This document records the design decisions made when extending the original Type System Explorer into the full **Egeria Explorer**, and captures remaining open work.

---

## What was planned (original outline)

- Reference Data sets + values (ReferenceDataManager)
- Digital Product Catalog hierarchy
- Glossary (Glossaries → Folders → Terms)
- Report Spec browser

## What has been implemented

All four planned sections are live, plus many more added since. The app was renamed **Egeria Explorer** and the full section roster now spans multiple portal pages:

**Egeria Explorer** (`type-explorer.html`):
```
[ Type System ] [ Glossary ] [ Reference Data ] [ Digital Products ]
[ Collections ] [ Data Design ] [ Perspectives ] [ ISC ]
[ Solution Architect ] [ Projects ] [ Actors ] [ Locations ]
[ Communities ] [ Note Logs ] [ Governance Definitions ]
[ Report Specs ] [ Valid Values ] [ REST APIs ]
```

**Tech Catalog** (`tech-catalog.html`):
```
[ IT Infrastructure ] [ Software Capabilities ] [ Endpoints ]
[ Data Stores ] [ Data Feeds ] [ Data Sets ] [ APIs ]
[ Software Components ] [ Actions ] [ Survey Reports ]
[ Technology Types ] [ Glossary ]
```

**Lineage Explorer** (`lineage-explorer.html`): asset search with lineage graph.

### Sections and their handlers

| Section / Tab | Handler file | pyegeria manager / data source |
|---------------|-------------|-------------------------------|
| Type System | `type_system_handler.py` | `ValidMetadataManager` |
| Glossary | `glossary_handler.py` | `GlossaryManager` |
| Reference Data | `reference_data_handler.py` | `ReferenceDataManager` |
| Digital Products | `digital_products_handler.py` | `CollectionManager` |
| Collections | `collections_handler.py` | `CollectionManager` |
| Data Design | `data_design_handler.py` | `CollectionManager` / `DataDesignManager` |
| Perspectives / Questions | `perspectives_handler.py` | `CollectionManager` |
| Information Supply Chains | `isc_handler.py` | `InformationSupplyChainManager` |
| Solution Architect | `solution_architect_handler.py` | `SolutionArchitectManager` |
| Projects | `project_handler.py` | `ProjectManager` |
| Actors | `actor_handler.py` | `ActorProfileManager` |
| Locations | `location_handler.py` | `LocationManager` |
| Communities | `community_handler.py` | `CommunityManager` |
| Note Logs | `notelog_handler.py` | `CollaborationManager` |
| Governance Definitions | `governance_definitions_handler.py` | `GovernanceDefinitionManager` |
| Tech Catalog (all categories) | `tech_catalog_handler.py` | `AssetManager` / `SurveyReportManager` |
| Lineage Explorer | `lineage_handler.py` | `AssetManager` |
| Context diagrams | `mermaid_handler.py` | `MetadataExpert` |
| Report Specs | `report_specs_handler.py` | local pyegeria only |
| Valid Values | `valid_values_handler.py` | `ReferenceDataManager` |
| REST APIs | `rest_api_handler.py` | `egeria_request_body_catalog.json` (static) + Egeria `/v3/api-docs` (live) |

---

## Key decisions (final)

| Decision | Choice | Notes |
|----------|--------|-------|
| App rename | **Egeria Explorer** | Done |
| Read-only | Yes, all sections | No write operations |
| Report Specs | Concept A — client-side pyegeria format specs | Not stored in Egeria |
| GlossaryProject | Omitted | Focus on Glossaries, Folders, Terms |
| Pagination strategy | Load-all per section, held in React state | Endpoints accept `start_from`/`page_size`; no UI pagination yet |
| Digital Products manager | `CollectionManager` | `ProductManager` was unavailable in installed pyegeria |
| Valid values scope | Both global (Reference Data tab) and lookup-by-property (Valid Values tab) | |
| Connection settings | Env-var only | No UI for connection settings |
| pyegeria version | Always latest | Circular-import bug in `pyegeria.core._exceptions` has been fixed upstream |
| HTML build | Inline `React.createElement()` — no JSX transpilation | File grew large; acceptable for now |
| Context diagrams | Lazy on demand via `/api/mermaid/{guid}` | `MetadataExpert.get_anchored_element_graph` |
| Context diagram toggle | Load → Show → Hide → Show cycle, no re-fetch | `code` state persists; `visible` state gates render |
| Mermaid JS version | **v11** required | Egeria uses `@{ shape: … }` syntax introduced in v11.0 |
| Tab order | Type Explorer is the **first** tab (leftmost) | Prevents it disappearing when type-system extras are hidden |
| URL alias | `/type-explorer` restored alongside `/egeria-explorer` | Two `@router.get` decorators on the same handler function |
| Template substitutes (Glossary) | Hidden by default; "Show template substitutes" checkbox filters on `isTemplateSubstitute` client-side | `TemplateSubstitute` field comes from the term's own properties, not the `Template` classification |
| Template classification filter | All list endpoints support `include_templates=true`; default excludes elements with the `Template` classification | Two paths: `skip_classified_elements` (native pyegeria) or `_is_template()` post-filter; frontend uses `inclTempl` state + checkbox |
| REST API catalog source | Extracted from Egeria's `http-client-collections` http files | OpenAPI schemas alone don't reliably describe the two-layer payload structure; the http client files do |
| REST API catalog format | Committed JSON artifact (`egeria_request_body_catalog.json`) + rebuild script | Committed so the UI works without a rebuild; script makes upgrades a one-command operation |
| REST API OpenAPI caching | In-process 1-hour TTL, explicit refresh endpoint | The spec is large (~MB); re-fetching on every request would be too slow |
| REST API properties type inference | Schema $ref → summary parsing → URL heuristic (in priority order) | Many endpoints reference generic `ElementProperties`; heuristics give a useful starting point |

---

## Significant implementation lessons

### REST API two-layer payload model

Egeria REST request bodies follow a consistent two-layer pattern that the OpenAPI schema alone does not make obvious:

**Layer 1 — outer wrapper (~44 types, stable).** Types like `NewElementRequestBody`, `UpdateElementRequestBody`, `DeleteElementRequestBody`, `NewRelationshipRequestBody`, etc. These carry governance/provenance metadata (`externalSourceGUID`, `effectiveFrom`/`To`), lifecycle linkage (`parentGUID`, `parentRelationshipTypeName`, `anchorGUID`, `isOwnAnchor`), and a single `properties` field.

**Layer 2 — inner type-specific properties (one per entity/relationship/classification type).** The `properties.class` discriminator identifies the specific type (e.g., `"class": "CollectionProperties"`). For a given create endpoint you can use the base type's properties body or any subtype's body (e.g., `CollectionProperties` or `DataStoreCollectionProperties`). All properties from the full inheritance chain are valid.

**Catalog extraction approach.** Rather than trying to parse Java source or derive the catalog from the OpenAPI spec, the `build_request_body_catalog.py` script scans Egeria's `http-client-collections` http client files. These files contain representative JSON payloads for every major operation, making them the most reliable source of ground-truth field names and structure. Running the script against a new Egeria release captures any new body types or field additions automatically.

**44 outer body types found** across 78 `.http` files in egeria-platform-6.1. They group into 11 functional families: create entity, create from template, update entity, delete entity, relationship, classification, search/query, external identifiers, governance actions, simple scalar, and admin/system.

**The `mergeUpdate` field is the key semantic switch on all update bodies.** `true` = partial update (only supplied fields change); `false` = replace all properties. The UI highlights this prominently.

**OpenAPI `$ref` resolution for properties types.** For most typed OMVS endpoints, the requestBody schema references `NewElementRequestBody`, and the `properties.properties.$ref` within that schema points to the specific properties class (e.g., `GlossaryProperties`). However, many endpoints use the generic low-level store API with `ElementProperties` — for these, the properties type is inferred from the operation summary text ("Create a GlossaryTerm" → `GlossaryTerm`) or, as a last resort, from the URL path's last segment.

### graph_query_depth and duplicates

Egeria's `graph_query_depth=1` parameter causes the API to traverse one relationship hop from each primary search hit. Any element that is a neighbor of *multiple* primary hits appears in the result list multiple times — once as a primary hit and once per neighbor that links to it. In a glossary folder with N terms, every term appears up to N times in the raw API response.

**Fix:** Deduplicate by GUID immediately after every `graph_query_depth=1` response, before any filtering or serialisation.

**Why depth=1 is still needed:** `memberOfCollections` (glossary terms) and `memberOfValidValueSets` (reference data values) are only populated at depth=1. Without them, folder-level filtering and the Reference Data tree are impossible.

**Rule of thumb:** Use `graph_query_depth=0` for list/search endpoints that only need element properties. Use `graph_query_depth=1` only when relationship data is required, and always deduplicate.

### mermaidGraph is at the container level, not in properties

Egeria places the mermaid diagram string at the response container level (`element["mermaidGraph"]`), not inside `element["properties"]`. Serialisers that read `props.get("mermaidGraph")` will always find an empty string. The correct approach is the dedicated `/api/mermaid/{guid}` endpoint, which calls `MetadataExpert.get_anchored_element_graph(guid, mermaid_only=True)`.

### Mermaid must be v11

Egeria generates diagram code using the `@{ shape: … }` node syntax introduced in mermaid v11.0. Mermaid v10 accepts the code without errors but returns empty SVG. Loading `mermaid@11` from CDN fixes this.

### TemplateSubstitute classification location

The `TemplateSubstitute` classification is **not** in `elementHeader["classifications"]`. It is stored as a sibling key directly on `elementHeader`:

```python
is_template_substitute = bool(element_header.get("templateSubstitute"))
```

Code that looks in the `classifications` list will always find `False`. Similarly, `sourcedFromTemplate` (indicating the element was copied from a template) is a top-level key on the element, not inside `elementHeader`.

In the Egeria demo dataset, template substitute terms have the same display name as real terms; they are separate Egeria entities, not duplicates. They should be hidden from normal browsing (the Glossary view hides them by default) but exposable for template management tasks.

### CollectionManager for Digital Products

`ProductManager` was not available in the installed pyegeria version. `CollectionManager` provides the same underlying `find_collections` and `get_collection_members` methods needed for the digital products hierarchy, so it was used throughout.

### graph_query_depth=0 for Digital Products performance

`find_collections` with `graph_query_depth=1` was taking 25–30 seconds per page. Switching to `graph_query_depth=0` reduced it to under 0.5 seconds. The tree is built by explicit recursive calls to `get_collection_members`, each also with depth=0.

---

## Remaining open work

### Cross-section navigation

Currently only **Digital Products → Glossary** cross-navigation is implemented (the "View in Glossary →" button on a Digital Products detail panel). Planned but not yet done:

- Type System property row → Valid Values lookup for that property name
- Reference Data value → any metadata elements that use it

~~Glossary term → any assets semantically linked to the term~~ — **already
done, verified 2026-07-15.** `SemanticAssignment` (term → data element, e.g. a
schema attribute) and `SemanticDefinition` (term → Data Design element, e.g. a
DataStructure) both already render via `_extract_extra_rels()`'s generic
fallback in `glossary_handler.py` — as "Meaning For Data Elements" and
"Semantically Associated Definitions" respectively. Verified live by seeding
both relationship types (`ClassificationExplorer.setup_semantic_assignment`,
`DataDesigner.link_semantic_definition`) against real qs demo data and
confirming the API response, then cleaning up. No code changes were needed —
this item was listed as open but had actually been working all along.

### Semantic relationship display on glossary terms — done (2026-07-15)

This section was stale — classifications and term-to-term relationships were
already being fetched and rendered (`glossary_handler.py`'s `_serialize_term`,
`GlossaryTermDetail` in `egeria-shared-ui.js`) by the time this was re-checked.
One real bug was found and fixed: `_TERM_REL_KEYS` assumed Egeria exposes each
relationship type (Synonym, Antonym, ISARelationship, etc.) as its own
top-level key (`synonyms`, `classifies`/`isA`, ...), based on reading
`OpenMetadataTypesArchive1_2.java`'s per-type end-attribute names. **Live
testing disproved this**: `get_term_by_guid(output_format="JSON")` puts ALL
term-to-term relationships into a single `relatedTerms` list — every one of
them was silently falling through to the generic-extra-keys fallback under one
undifferentiated "Related Terms" label, with no way to tell a Synonym from an
ISARelationship link. Fixed by grouping `relatedTerms` entries by each one's
actual `relationshipHeader.type.typeName` (and, for the asymmetric
ISARelationship, the `relatedElementAtEnd1` boolean → "Is A" vs "Classifies")
— see `_group_related_terms()`. Verified end-to-end against a live
qs-view-server with seeded Synonym + ISARelationship test data (see
`egeria-python/tests/functional-tests/test_glossary_manager_omvs.py::test_term_relationship_keys_synonym_and_isa`).

Still open, separately: "Glossary term → any assets semantically linked" (see
Cross-section navigation above) — that's semantic *assignment* to
DataFields/assets, a different relationship from the term-to-term ones fixed
here.

### Glossary hierarchy tree

The current Glossary view shows a flat list of glossaries on the left, with folders loaded when a glossary is selected. The original design called for a full tree (Glossary → Folders → Terms). Implementing full recursive folder nesting is deferred; the current two-level (glossary / folder) navigation is functional.

### UI-level pagination

All API endpoints accept `start_from` and `page_size`. The UI currently fetches `page_size=500` (or 200 for terms) and displays all results. If a deployment has more items, pagination controls will be needed.

### Global search across sections

Search is currently per-section. A top-level search bar that queries across Type System, Glossary, and Reference Data simultaneously is desirable but not yet implemented.

### GlossaryProject

`GlossaryProject` is a classification applied to a `Project` entity — not a type in the glossary hierarchy. Deferred; may not be needed.

### Report Specs detail improvement

The Report Specs tab currently shows name, description, and perspectives. The `question_spec` field (a list of questions a spec can answer) is not yet displayed in the UI.

---

## Extension guide: adding a new section

1. **Create the handler:** `<section>_handler.py` with `router = APIRouter(tags=["<section>"])`. Follow the `_get_manager()` / `_props()` / `_header()` pattern used in all existing handlers. Return `JSONResponse` from all endpoints.

2. **Register the router** in `pyegeria_handler.py`:
   ```python
   from <section>_handler import router as <section>_router
   app.include_router(<section>_router)
   ```

3. **Add the frontend component** in `type-explorer.html`. The component goes in the main script block, before the `App` component. Use `React.createElement()` throughout — no JSX. Use the existing hooks (`useState`, `useEffect`, `useMemo`, `useCallback`) destructured from `React` or via the `const { useState, ... } = React` pattern at the top of App.

4. **Wire up the tab** in the `App` component: add a state value to `section`, a tab button in the tab bar `<div>`, and a conditional render in the section selector at the bottom of App's return.

5. **Add a `MermaidSection` call** in any detail panel that shows a single Egeria element — this gives the user a "Load Context Diagram" button for free.

6. **Update docs:** `README.md` (user-facing features and API), `type-explorer-architecture.md` (internals), and this file.

## Keeping the REST API catalog current after Egeria upgrades

Run the build script against the new distribution's http-client-collections, then commit the updated JSON:

```bash
python3 build_request_body_catalog.py \
  /path/to/egeria-platform-X.Y/assembly/opt/http-client-collections
```

The script is idempotent — re-running against the same version produces the same output. The `_meta.source` field in the JSON records which directory was used and the `howToRebuild` field documents the command, so the JSON is self-documenting.
