# Extending the Egeria Type Explorer → Egeria Explorer

The Egeria Type Explorer is a powerful tool for exploring the types defined in the Egeria ecosystem. It provides a
visual interface for browsing and understanding the types, their properties, and their relationships. The explorer is so
good that I want to extend it to support additional features and capabilities. In this document, I will outline some of the ways in which I plan to extend the Egeria Type Explorer.

## Original Outline

### Adding Support for the Egeria Reference data
Things of type valid metadata value — ValidMetadataManager

### Reference Data Set with members Reference Data Values
ReferenceDataManager

### Support for the Digital Product Catalog
* DigitalProducts, DigitalProductFamilies, DigitalProductCatalogs are all subtypes of Collection.
* A hierarchy of containing:
  * Digital Product Catalog containing:
    * Digital Product Families containing:
      * Digital Products

### Support for the Glossary
* Glossary, CollectionFolder, GlossaryTerm, GlossaryProject
* Glossaries and Collection Folder are subtypes of Collection, GlossaryTerm is its own type. GlossaryProject is a classification applied to a project.
* A hierarchy of containing:
  * Glossary containing:
    * Collection Folders containing:
      * Glossary Terms

### Support for listing Report_Specs and searching for reportspecs by names, by perspectives, etc

---

## Key Decisions

| Decision | Choice |
|----------|--------|
| App rename | Yes — **Egeria Explorer**, with Type System as the first tab |
| Read-only vs. read-write | **Read-only** for all new sections |
| Report Specs concept | **Concept A** — pyegeria client-side formatting specs (`base_report_formats.py`) with `perspectives` and `question_spec` fields. Not stored in Egeria. |
| GlossaryProject handling | **Omit for now** — focus on Glossaries, Categories, and Terms |
| Pagination strategy | **Load-all per section, cached in browser for the session.** API endpoints will accept `start_from`/`page_size` params from the start, but the UI will not implement pagination controls until data volumes warrant it |
| Digital Products manager | **ProductManager preferred** if available in the installed pyegeria; fall back to `CollectionManager` otherwise |
| Valid values scope | **Both** — global view of all valid values, plus drill-down by type and property |
| Connection settings UI | **Keep env-var-only approach** for now |
| pyegeria version | **Always latest** — no pinning. The circular-import bug in `pyegeria.core._exceptions` that was noted in architecture docs has been fixed |

---

## Analysis of the Current Implementation

### What the Type Explorer already does

The current explorer is built on three layers:

- **`type_system_handler.py`** — FastAPI router. On each `GET /api/types` call it creates a `ValidMetadataManager`, fetches all entity, relationship, and classification *type definitions* from Egeria, derives area numbers by walking the supertype chain, and returns a single normalised JSON payload. No server-side caching.
- **`type-explorer.html`** — A fully self-contained React 18 SPA (all JavaScript inlined, no CDN calls). It loads the full type system once per page load and does all navigation, search, and graph rendering client-side from that in-memory snapshot.
- Two views: **Type Explorer** (entity hierarchy tree, properties table, relationships list, SVG inheritance graph) and **Attribute Index** (cross-reference of every property name to every type that declares it).

### Data characteristics of the new sections

The new sections deal with instance data rather than type definitions, but the data characteristics are actually similar in practice: this is slowly-changing reference and governance data, not transactional data. Expected volumes are small — well under 1,000 items per category (valid values for a given property, terms in a given glossary, products in a given catalog). The type system itself is not as static as one might assume; it has also changed frequently as Egeria continues to develop (three new types and relationships added in recent weeks alone).

The practical consequence is that the same **load-on-demand, cache in browser** strategy used by the type system is the right starting point for instance sections too. Each tab loads its data when first opened and holds it in memory for the session. Server-side API endpoints will accept pagination parameters from day one so that adding UI-level pagination later is straightforward, but there is no need to build that UI complexity now.

| Dimension | Type System | Instance sections |
|-----------|-------------|-------------------|
| Volume | ~800 items | < 1,000 per category |
| Rate of change | Moderate (active Egeria development) | Slow (stable reference/governance data) |
| Load strategy | All at once on page load | All at once when tab is first opened |
| Freshness | Page reload sufficient | Section-level refresh button sufficient |
| Primary API | `ValidMetadataManager` type-def endpoints | `GlossaryManager`, `CollectionManager`, `ReferenceDataManager` |

---

## Proposed Features — Detailed Specification

### 1. Reference Data Explorer

Two related sub-areas that together cover Egeria's reference-data capability:

#### 1a. Valid Metadata Values (ValidMetadataManager)
Egeria allows administrators to define controlled vocabularies for metadata fields — for example, the allowed values for a `confidentiality` property or an asset `criticality` rating. These are stored as `ValidMetadataValue` instances and are surfaced in pyegeria via `ValidMetadataManager` instance methods (`find_valid_value_definitions`, `get_valid_value_definitions_by_name`, `get_valid_value_definition_by_guid`).

Proposed UI features:
- **Global view**: searchable list of all valid value definitions, grouped by the property they apply to (`typeName`/`propertyName` dimensions). Gives administrators an overview of all controlled vocabularies.
- **Drill-down view**: pick a type, then a property, to see only the valid values for that context. Integrates with a cross-link from the Type System tab — clicking a property row in the Type Explorer can open the corresponding valid-values drill-down.
- Detail panel for a selected value: name, display name, description, usage, scope, data type, is-deprecated flag.
- Filter by property name, type name, or category.

#### 1b. Reference Data Sets (ReferenceDataManager)
Reference data sets are `ReferenceDataSet` entities containing `ReferenceDataValue` members. The `ReferenceDataManager` exposes `find_valid_value_definitions` with `element_type="ReferenceDataSet"` and member-walking via containment relationships.

Proposed UI features:
- Collapsible tree: Reference Data Set → Reference Data Values (members).
- Detail panel for a selected set: description, GUID, usage.
- Detail panel for a selected value: symbolic name, display name, additional properties (encoded as `additionalProperties` map).
- Search across sets and values simultaneously.

---

### 2. Digital Product Catalog Explorer

Digital products in Egeria are all subtypes of `Collection`, arranged in a strict three-level containment hierarchy. The preferred manager is `ProductManager` (richer API, purpose-built for the three-level hierarchy); fall back to `CollectionManager` if `ProductManager` is not available in the installed pyegeria.

**Hierarchy tree (left panel)**
```
Digital Product Catalog  [badge: catalog]
  └── Digital Product Family  [badge: family]
        ├── Digital Product  [badge: product]
        └── Digital Product  [badge: product]
```

- Load all catalogs when the tab is opened (`find_digital_product_catalogs` / `find_digital_products` with catalog filter).
- Expand family and product nodes on click.
- Click any node to show its detail panel.

**Detail panel (right)**
- For a **Catalog**: name, description, GUID, creation date, custom properties.
- For a **Family**: same as catalog plus breadcrumb link to containing catalog.
- For a **Product**: full `DigitalProductProperties` — `productStatus`, `productType`, `introductionDate`, `maturity`, `serviceLife`, `currentVersion`, `nextVersionDate`, `withdrawDate`, additional properties; relationship links to assets, glossary terms, and data specifications.

**Search**: free-text search across all products, filtering by `productStatus`, `productType`, or maturity level.

---

### 3. Glossary Explorer

Egeria's glossary model: `Glossary` and `GlossaryCategory` (the collection-folder level) are both subtypes of `Collection`; `GlossaryTerm` is its own type. `GlossaryProject` (a classification on a `Project` entity) is out of scope for this phase.

The pyegeria `GlossaryManager` provides: `find_glossaries`, `get_glossaries_by_name`, `get_glossary_by_guid`, `find_glossary_terms`, `get_terms_by_name`, `get_term_by_guid`, plus relationship management methods.

**Hierarchy tree (left panel)**
```
Glossary  [e.g. "Coco Pharmaceuticals Glossary"]
  └── Category Folder  [e.g. "Medical Terms"]
        ├── Category Folder  [nested]
        │     └── Glossary Term
        └── Glossary Term
```

- Top level: all glossaries loaded when tab is opened.
- Expand to show categories; expand categories to show terms.
- Click a term to show its detail panel.

**Term detail panel**
- All term properties: `displayName`, `summary`, `description`, `examples`, `usage`, `abbreviation`, `formula`, `publishVersionIdentifier`, term status.
- Term status badge (Draft / Proposed / Active / Deprecated / etc.).
- Semantic relationships to other terms (IsA, PreferredTerm, Synonym, Translation, etc.) — each shown as a clickable link that navigates to the related term.
- Classifications applied to the term (e.g., `AbstractConcept`, `DataValue`, `ActivityDescription`, `ContextDefinition`).
- Back-links: which assets or data fields are semantically linked to this term.

**Glossary search**
- Text search across all terms in a glossary or across all glossaries.
- Filter by term status, by category, by classification type.
- Results list with direct navigation to term detail.

---

### 4. Report Spec Browser

This section surfaces pyegeria's **client-side formatting specifications** — Python objects defined in `base_report_formats.py` (and any user-defined specs). These are not stored in Egeria; they live in the pyegeria package and define how API responses are formatted into tables, dicts, JSON, or Markdown. Each spec carries a `perspectives` list (e.g., "Data Steward", "Business Analyst") and a `question_spec` list describing what questions it can answer.

The `find_report_specs(perspective, question)` and `report_spec_list()` functions both operate on this same underlying data structure. The implementation will use a single `GET /api/report-specs` endpoint that returns the full list; all filtering and search happens client-side.

**No Egeria connection is required** for this section.

Proposed UI features:
- Searchable sidebar list of all report specs, showing name and family.
- Filter dropdown by perspective.
- Free-text search by name or by question text.
- Detail panel for a selected spec: name, description, family, perspectives, available output formats (TABLE / JSON / DICT / MARKDOWN), and the full question spec (what questions this format can answer).

---

## Architectural Considerations

### App rename and navigation

Proposed top-level tab bar:
```
[ Type System ] [ Reference Data ] [ Digital Products ] [ Glossary ] [ Report Specs ]
```

The Type System tab is unchanged from today. Each new tab is a separate SPA view that shares the same connection settings and dark/light theme.

### Backend: new handlers and endpoints

One FastAPI router file per section, mounted in `pyegeria_handler.py` via `app.include_router()`:

```
PyegeriaWebHandler/
  type_system_handler.py        # existing, unchanged
  reference_data_handler.py     # new
  digital_products_handler.py   # new
  glossary_handler.py           # new
  report_specs_handler.py       # new
  egeria_explorer.html          # renamed/extended SPA
```

| Section | Endpoint(s) | pyegeria manager |
|---------|-------------|-----------------|
| Type System | `GET /api/types` (existing) | `ValidMetadataManager` |
| Reference Data — valid values | `GET /api/valid-values?q=&type=&property=&start_from=&page_size=` | `ValidMetadataManager` (instance methods) |
| Reference Data — ref data sets | `GET /api/reference-data?q=&start_from=&page_size=` | `ReferenceDataManager` |
| Digital Products | `GET /api/digital-products?q=&start_from=&page_size=` | `ProductManager` (fallback: `CollectionManager`) |
| Glossary | `GET /api/glossary?q=&start_from=&page_size=`, `GET /api/glossary/{guid}/terms?q=&start_from=&page_size=` | `GlossaryManager` |
| Report Specs | `GET /api/report-specs` | Local pyegeria package only |

All instance endpoints accept `start_from` and `page_size` parameters from the start (Egeria's default page limit is 1,000). The UI will use load-all initially; the pagination wire-up is ready when we need it.

### pyegeria version

Always use the latest pyegeria release — no version pinning. The circular-import bug in `pyegeria.core._exceptions` that was previously noted has been fixed. Before building Phase 2 onward, verify `from pyegeria import GlossaryManager, CollectionManager, ProductManager` all import cleanly in the Docker container. If `ProductManager` is absent, fall back to `CollectionManager`.

### HTML file size

`type-explorer.html` is already large (~2,500 lines of inlined JS). Adding four more sections in the same file will make it unmanageable. Before Phase 1, evaluate a lightweight Babel CLI build step that compiles separate JSX files into the single inlined HTML — preserving the no-CDN, no-build-at-runtime property while making the source maintainable.

---

## Implementation Plan

### Phase 0 — Navigation scaffold
- Rename the SPA title and header to "Egeria Explorer".
- Add the top-level tab bar: Type System | Reference Data | Digital Products | Glossary | Report Specs.
- New tabs show a "Coming soon" placeholder.
- Keep all existing Type System functionality unchanged.
- Evaluate and set up the Babel CLI build pipeline for the HTML.

### Phase 1 — Report Spec Browser
- New `report_specs_handler.py` with `GET /api/report-specs`.
- Returns full `report_spec_list()` as JSON; client handles search and filtering.
- UI: searchable sidebar, perspective filter dropdown, detail panel (name, description, family, perspectives, output formats, question spec).
- Validates the new tab architecture with zero Egeria connectivity risk.

### Phase 2 — Glossary Explorer
- New `glossary_handler.py`.
- Endpoints: `GET /api/glossary` (all glossaries), `GET /api/glossary/{guid}/terms`.
- Load all glossaries on tab open; load terms when a glossary is selected.
- Term detail panel: all properties, status badge, semantic relationship links.

### Phase 3 — Reference Data Explorer
- New `reference_data_handler.py`.
- Endpoints: `GET /api/valid-values` (global + drill-down via `?type=&property=`) and `GET /api/reference-data` (sets + members).
- Global valid-values view grouped by type/property; drill-down view filtered by type and property.
- Reference data sets shown as expandable tree.
- Cross-link: a type name in the valid-values view navigates to that type in the Type System tab.

### Phase 4 — Digital Product Catalog Explorer
- New `digital_products_handler.py`.
- Endpoint: `GET /api/digital-products` (full catalog→family→product hierarchy).
- Three-level tree reusing the existing tree component from the Type System view.
- Product detail panel with full `DigitalProductProperties` fields.

### Phase 5 — Polish and integration
- Global search across all sections.
- Cross-section navigation (e.g., from a property in Type System → to its valid values in Reference Data).
- Update README and architecture docs.
- Revisit GlossaryProject if needed.

---

## Remaining Technical Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| `ProductManager` unavailable in installed pyegeria | Low | Fall back to `CollectionManager`; check import before Phase 4 |
| Instance data volume eventually exceeds load-all performance threshold | Low | API pagination params are wired from day one; add UI controls when needed |
| `type-explorer.html` becomes unmaintainable at current size | Medium | Evaluate Babel CLI build step in Phase 0 before adding more JS |
