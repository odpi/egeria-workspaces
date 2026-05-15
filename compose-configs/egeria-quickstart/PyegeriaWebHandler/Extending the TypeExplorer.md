# Egeria Explorer — Extension History and Roadmap

This document records the design decisions made when extending the original Type System Explorer into the full **Egeria Explorer**, and captures remaining open work.

---

## What was planned (original outline)

- Reference Data sets + values (ReferenceDataManager)
- Digital Product Catalog hierarchy
- Glossary (Glossaries → Folders → Terms)
- Report Spec browser

## What has been implemented

All four planned sections are live. The app was renamed **Egeria Explorer** and the tab bar now reads:

```
[ Type System ] [ Reference Data ] [ Digital Products ] [ Glossary ] [ Report Specs ] [ Valid Values ]
```

A sixth tab, **Valid Values**, was added to surface Egeria's controlled vocabulary registry (property-name → allowed values lookups), which is distinct from the Reference Data sets.

### Sections and their handlers

| Tab | Handler file | pyegeria manager |
|-----|-------------|-----------------|
| Type System | `type_system_handler.py` | `ValidMetadataManager` |
| Reference Data | `reference_data_handler.py` | `ReferenceDataManager` |
| Digital Products | `digital_products_handler.py` | `CollectionManager` |
| Glossary | `glossary_handler.py` | `GlossaryManager` |
| Report Specs | `report_specs_handler.py` | local pyegeria only |
| Valid Values | `valid_values_handler.py` | `ReferenceDataManager` |
| Context diagrams | `mermaid_handler.py` | `MetadataExpert` |

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
| Template substitutes | Hidden by default in Glossary; checkbox + amber badge | `TemplateSubstitute` is stored in `elementHeader.templateSubstitute`, not in the classifications list |

---

## Significant implementation lessons

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
- Glossary term → any assets semantically linked to the term
- Reference Data value → any metadata elements that use it

### Semantic relationship display on glossary terms

The term detail panel shows all term properties but does not yet show:
- Semantic relationships to other terms (IsA, Synonym, PreferredTerm, Translation, etc.)
- Classifications applied to the term (AbstractConcept, DataValue, etc.)
- Back-links to assets or data fields

These require additional pyegeria calls (e.g., `get_related_elements` or `get_term_relationships`) and frontend components.

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
