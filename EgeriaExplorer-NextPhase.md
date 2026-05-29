# Egeria Explorer — Next Phase Planning

Working document. Add comments / answers inline using `<!-- your note -->` or just edit text directly.

---

## Context

The current Egeria Explorer (`type-explorer.html` + FastAPI backend) has eight tabs:
**Home → Type Explorer → Glossary → Reference Data → Digital Products → Report Specs → Valid Values → REST APIs**

All tabs are read-only. The SPA is a single self-contained HTML file (React 18 + Mermaid 11 via CDN, no build step). The backend is a set of FastAPI routers mounted in `pyegeria_handler.py`.

---

## Part A — Backlog: improvements to existing tabs

### Status

| Item | Decision | Status |
|------|----------|--------|
| **A1** Cross-section navigation | Glossary Terms and Type System first; Type System → Valid Values done; more to come | Type System → Valid Values **done** |
| **A2** Term semantic relationships | Relationships first (already rendered), then back-links, then classifications | Classifications **done** in backend + frontend |
| **A3** Glossary recursive folders | Deep nesting needed; not most immediate | Deferred |
| **A4** Pagination / truncation warning | Add warning when results are truncated | **Done** — `⚠ first N shown` in Glossary counts |
| **A5** Global search | Per-section acceptable for now; note to user that search is section-specific | Deferred |
| **A6** Report Specs question_spec + family | High priority; grouping by family, perspective/question filtering | Family grouping **done**; question_spec already rendered |
| **A7** Home reconnect button | Acceptable for now; add localStorage note | Deferred |
| **A8** Valid Values debug endpoint | Remove it | **Done** |
| **A9** freshstart/quickstart sync | Ok for now; add README note | Deferred — note to add to README |

### Remaining A-items to complete

**A1 — Cross-section navigation still needed:**
- Glossary term → Data Fields semantically linked to it (needs Phase 2 / B4)
- Reference Data value → elements that use it
- Data Field → Glossary term (bidirectional; needs Phase 2)

**A3 — Recursive glossary folder tree:**
Deep nesting likely in production. Deferred but not forgotten — same pattern as Digital Products tree. Track for Phase 2+ once data volumes make it urgent.

**A5 / A7 / A9 — Minor UX notes (low effort, deferred):**
- Add tooltip to search inputs: "Search is within this section only"
- Add note to Home tab: "Credentials stored in browser localStorage — clear via DevTools to reset"
- Add rsync note to README

---

## Part B — New tabs and capabilities

### Decisions recorded

---

### B1 + B2. Solution Architecture tab *(combined)*

**Decision**: Single combined tab (can split later if crowded). Components are navigable from Blueprint detail via links.

**Layout**:
- Left panel: sub-navigation toggle — **Blueprints** | **Components** (shared left panel like Glossary)
- Blueprint detail: small structured property panel (name, description, classifications) + mermaid diagram from `generate_solution_blueprint_output`
- Component detail: property panel + back-links to parent blueprint(s) + mermaid context diagram + implementations list

**pyegeria manager**: `SolutionArchitect`

**Backend handler**: `solution_architect_handler.py`

**API endpoints to build**:
| Endpoint | Method | Notes |
|----------|--------|-------|
| `GET /api/solution/blueprints` | `find_all_solution_blueprints()` | List all blueprints |
| `GET /api/solution/blueprints/{guid}` | `get_solution_blueprint_by_guid(guid)` | Detail + mermaid |
| `GET /api/solution/components` | `find_all_solution_components()` | List all components |
| `GET /api/solution/components/{guid}` | `get_solution_component_by_guid(guid)` + `get_component_related_elements(guid)` | Detail + relationships |
| `GET /api/solution/components/{guid}/implementations` | `get_solution_component_implementations(guid)` | Concrete implementations |

**Mermaid**: Use `generate_solution_blueprint_output(guid)` for blueprints (dedicated output method); use existing `/api/mermaid/{guid}` button for components.

**Information Supply Chains**: Separate tab (later phase — distinct concept).

---

### B3. Perspectives & Questions tab *(standalone)*

**Decision**: Standalone tab. Used with both Digital Products and Report Specs. Important enough to stand alone.

**Egeria types** (confirmed):
- `Question` = GlossaryTerm with a **Question classification**
- `Perspective` = subtype of **Actor**

**Backend approach**: Perspectives — use `ActorManager.find_perspectives()`; Questions — use `GlossaryManager.find_glossary_terms()` with `include_only_classified_elements=["Question"]` (the same `spec_params` pattern used in the B8 report spec for Questions). Raw OpenMetadata format parsing required for Perspectives.

**Open question remaining**:
> Q-B3a: Are there existing `Perspective` instances in your demo/quickstart data we can test against? What's the full Egeria type name for Perspective (e.g., `Perspective`, `ActorProfile` subtype)?
<!-- ANSWER: -->
Yes - I added one Perspective:Architect. Type of Perspective - a subtype of Actor. 
> Q-B3b: For Questions — do they appear in the glossary hierarchy (browsable via `GlossaryManager`) or only discoverable via `find_metadata_elements`?
<!-- ANSWER: -->
No - you can find_perspectives method in actor_manager, or one of the generic methods in classification manager or metadata expert. 
**API endpoints to build**:
| Endpoint | Notes |
|----------|-------|
| `GET /api/perspectives` | `ActorManager.find_perspectives()` |
| `GET /api/perspectives/{guid}` | Full perspective detail |
| `GET /api/questions` | `GlossaryManager.find_glossary_terms()` with `include_only_classified_elements=["Question"]` |
| `GET /api/questions/{guid}` | Full question detail |

---

### B4 + B5. Data Design tab *(combined — Specs / Structures / Fields / Grains)*

**Decision**: One combined tab. Sub-navigation within the tab between: **Data Specs** | **Data Structures** | **Data Fields** | **Data Grains**.

**Entry points**: Both standalone browse and cross-navigation from Digital Products (product → data spec).

**Relationships to surface**: Data Scope, Data Classes, Glossary terms (all cross-links wanted).

**pyegeria manager**: `DataDesigner`

**Backend handler**: `data_design_handler.py`

**API endpoints to build**:
| Endpoint | Method | Notes |
|----------|--------|-------|
| `GET /api/data-design/specs` | `find_data_value_specifications("*")` | List all specs |
| `GET /api/data-design/specs/{guid}` | `get_data_value_specification_by_guid` + `get_data_value_specification_rel_elements` | Detail + linked structures/classes |
| `GET /api/data-design/structures` | `find_all_data_structures()` | List all structures |
| `GET /api/data-design/structures/{guid}` | `get_data_structure_by_guid` + `get_data_memberships_with_dict` | Detail + member fields |
| `GET /api/data-design/fields` | `find_all_data_fields()` | List all fields |
| `GET /api/data-design/fields/{guid}` | `get_data_field_by_guid` + `get_data_field_rel_elements` | Detail + relationships + glossary links |
| `GET /api/data-design/grains` | `MetadataExpert.find_metadata_elements` with `DataGrain` type | No `find_all_data_grains()` on `DataDesigner` |
| `GET /api/data-design/grains/{guid}` | `get_data_grain_by_guid` + `get_data_grain_rel_elements` | Detail |

**Data Grains**: Browsable list in left panel of Data Design tab; also shown as linked items on field/structure detail panels (primary use case is navigation from field/structure, but standalone browse is also supported).

**Cross-links**:
- Data Field → Glossary term (semantic definition) *(A1)*
- Data Spec → Digital Product *(B6)*
- Data Field → Valid Values *(A1 extension)*

---

### B6. Digital Products — enhanced detail

**Decision**: Pull forward in phases (user wants this early, after Phase 1).

**What changes**:
- Product detail panel expands to show **all collection members** grouped by type: Data Spec, Tabular Data Sets, License, etc.
- Identify `TabularDataSetCollection` and `TabularDataSet` members specifically
- Cross-link Data Spec members to the Data Design tab (B4)
- Cross-link Tabular Data Sets to their schema if available

**Product → Data Spec link**: Through an intermediate `DataSpecCollection` node already visible in the current tree. We need to detect `DataSpecCollection` type members and expose them with a "View Data Spec →" link.

**Relevant Egeria types for product members**:
- `DataSpecCollection` — container pointing to the data spec
- `TabularDataSetCollection` — collection of tabular data sets
- `TabularDataSet` — individual tabular data set
- License, governance classifications, etc.

**Implementation note**: The current `_serialize_node` in `digital_products_handler.py` already returns `typeName`. The change is: in the product detail frontend panel, group the tree children by `typeName` and add navigation buttons for `DataSpecCollection` and `TabularDataSet*` members.

---

### B7. Dr. Egeria Commands tab

**Decision**: Start with reference catalog + markdown template display. Execution (via MCP) is a follow-on once the catalog is in place.

**Phase 1 (reference)**: Browsable catalog of Dr. Egeria commands — verb, parameters, description, and the associated markdown template displayed inline (syntax-highlighted). Similar to REST APIs tab.

**Phase 2 (execution, later)**: Pick command, fill form, run via MCP (`dr_egeria_run_block`). Output = rendered markdown with raw toggle; markdown tables and mermaid diagrams supported.

**Open question — template storage**:
> Q-B7: Where should the canonical copy of Dr. Egeria command templates live so they are accessible to: (a) the Explorer web UI, (b) Jupyter notebook users, (c) MCP tool users, (d) other tools? Options: a shared volume mount, a git-tracked directory under egeria-workspaces, inside the pyegeria package, or a combination. What's your preference?
<!-- ANSWER: -->
for now I created a top-level directory for templates. Note that there are two sub-directories - one for basic templates and a second for advanced.
Advanced templates offer more parameters than basic but the same commands should be in either. Choosing the template to show could be through a selector button in the tab.
I think that we will need to move this to another location later.
**Backend approach for reference catalog**: Enumerate templates from `templates/basic/` and `templates/advanced/` at repo root. For each command, return both the basic and advanced template content. The UI shows them with a **Basic / Advanced toggle** — same command, swapped template. No Egeria connection needed. Return shape per command: `{name, family, verb, parameters, description, basicTemplate, advancedTemplate}`.

---

### B8. Report Specs — execution

**Decision**: Yes — pick spec, supply parameters, click Run, see formatted output inline.

**Model spec**: Full dataclass definitions in `pyegeria/view/_output_format_models.py` (egeria-python repo). Broader description at `docs/output-formats-and-report-specs.md` in the same repo. Report specs are loaded from `pyegeria/view/base_report_formats.py`; that module also provides methods to look up specs by perspective and question.

**`ActionParameter` structure** (from `_output_format_models.py`):
```python
action=ActionParameter(
    function="ManagerClass.method_name",   # dotted path; split on "." to dispatch
    required_params=["search_string"],      # user must supply these in the run form
    optional_params=OPTIONAL_FILTER_PARAMS + TIME_PARAMETERS,  # user may supply
    spec_params={"include_only_classified_elements": ["Question"]},  # fixed; passed automatically
)
```

**Example — Questions spec**:
```python
"Questions": FormatSet(
    target_type="GlossaryTerm",
    heading="Questions",
    description="GlossaryTerms classified as Questions",
    family="GlossaryManager",
    formats=[Format(types=["ALL"], attributes=COMMON_COLUMNS + [...])],
    action=ActionParameter(
        function="GlossaryManager.find_glossary_terms",
        optional_params=OPTIONAL_FILTER_PARAMS + TIME_PARAMETERS,
        required_params=["search_string"],
        spec_params={"include_only_classified_elements": ["Question"]},
    ),
)
```

`spec_params` are fixed values injected automatically by the backend — they never appear in the user-facing form.

**Implementation**:
1. Backend: expose `action` fields via `_serialize()` in `report_specs_handler.py` — return `{function, required_params, optional_params}` (omit `spec_params` from the API response; they are applied server-side at run time)
2. Frontend: show **Run** button only when `action` is non-null
3. Frontend run form: render `required_params` as mandatory inputs, `optional_params` as collapsible optional inputs
4. Add `POST /api/report-specs/run` endpoint: receives `{spec_name, user_params}`; backend looks up the spec, splits `function` on `.` to get manager class + method, merges `user_params` + `spec_params`, calls the method, returns formatted markdown
5. Frontend: render markdown output below the spec detail (reuse the existing markdown renderer)I ge
---

## Revised phase plan

| Phase | Items | Status | Notes |
|-------|-------|--------|-------|
| **0** | A2, A4, A6, A8, A1 (Type→VV) | **done** | Completed 2026-05-21 |
| **1** | B1+B2 Solution Architecture tab | **done** | Blueprints + Components; cross-nav |
| **2** | B6 Digital Products enhancement | **done** | Members grouped by type; Data Spec cross-link |
| **3** | B4+B5 Data Design tab | **done** | Specs/Structures/Fields/Grains; `graph_query_depth=0` required |
| **4** | A1 remaining cross-nav | **done** | Term→DataField, DataField→Glossary wired |
| **5** | B3 Perspectives & Questions | **done** | Standalone Perspectives tab; Questions tab |
| **6** | B7 Dr. Egeria Commands (reference) | **done** | Basic/Advanced toggle; template browser |
| **7** | B8 Report Spec execution | **done** | `ActionParameter` dispatch; run form; formatted output |
| **—** | ISC (Information Supply Chains) | **done** | Separate tab; segments + implementations |
| **—** | Governance Definitions | **done** | Full definition tree + relationships |
| **—** | Feedback/Comments (FB-1, FB-3) | **done** | Likes/ratings/comments on all major detail panes (both envs) |
| **8** | B7 execution (MCP) | open | Render markdown + tables + mermaid via MCP |
| **Later** | A3 folder tree, A5 global search, report rendering (RR-1–5) | open | See BACKLOG.md |

> **Note:** BACKLOG.md at repo root is now the canonical work list. This file is a historical planning record.

---

## Architectural decisions

| Decision | Choice | Notes |
|----------|--------|-------|
| Solution tab | Combined Blueprints + Components | Can split later |
| Data Design tab | Combined Specs/Structures/Fields/Grains | Sub-navigation within tab |
| Perspectives/Questions | Standalone tab | Used with both Digital Products and Report Specs |
| HTML file strategy | **Dual-file (SHARE-1 in backlog to unify)** | Currently separate freshstart/quickstart copies; env-gating proposed |
| Nav bar style | NavGroup dropdown groups (Reference/Review/Act) | Both envs now match; added to freshstart 2026-05-29 |
| Feedback widget position | In element title row, far right (`marginLeft: auto`) | Disambiguates from Comments section below |
| Dr. Egeria execution path | MCP (`dr_egeria_run_block`) | When execution is added in Phase 8 |
| Report Spec execution | `action` field dispatches to manager method | Execution only when `action` is non-null |

---

## Open questions blocking implementation

All previously open questions are resolved. Details are recorded in the relevant sections above.

| ID | Resolution | See |
|----|-----------|-----|
| Q-B3a | `Perspective` is an Actor subtype; one test instance (`Architect`) exists in quickstart data | B3 backend approach |
| Q-B3b | Questions found via `GlossaryManager.find_glossary_terms()` with `include_only_classified_elements=["Question"]` | B3 API endpoints |
| Q-B7 | Templates at `templates/basic/` + `templates/advanced/` in repo root; Basic/Advanced toggle in UI | B7 backend approach |
| Q-B8 | `action` is an `ActionParameter` with `function` (dotted path), `required_params`, `optional_params`, `spec_params` | B8 implementation |

---

*Last updated: 2026-05-29 — phases 1–7 + ISC/GovDef/Feedback all complete; see BACKLOG.md for open items*
