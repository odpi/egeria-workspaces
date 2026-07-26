<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Egeria Reporting & Dashboard Model — design

**Status:** design / discussion (2026-07-25). **P0 landed 2026-07-26** (see §9).
Companion to `OVERVIEW_README.md`, `OVERVIEW_METRICS.md`, `OVERVIEW_NEXT_STEPS.md`.

**P0 shipped:** `overview_specs.py` (the single source-of-truth tile registry, 11
KPIs as real pyegeria `FormatSet` objects), served at `GET /api/overview/specs`;
`gen_overview_metrics.py` generates the KPI catalog + provenance block of
`OVERVIEW_METRICS.md` from it; `test_overview_specs.py` (242 checks) guards that
the registry, the frontend `METRICS`/`PERSP_KPIS`/`DRILL` maps, and the generated
doc block never silently diverge. The five open decisions (§10) affect P1–P4 only
and remain open. Frontend still holds its own tile maps (now guard-locked to the
registry); having the SPA render *from* `/api/overview/specs` is P1 work.

**Purpose:** define how the Egeria Overview dashboard — and dashboards/reports in
general — should be *declaratively defined* on top of the existing pyegeria
**ReportSpec / `FormatSet`** model, rather than hand-coded per app. The goal is one
model that unifies the dashboard, the Egeria Advisor's report builder, and the
Perspective/Question work, and that can eventually be governed metadata in Egeria.

---

## 1. Why (the problem)

Today a dashboard tile's definition is spread across ~6 hand-synced places
(`overview_handler.py` calc, the frontend `METRICS`/`DRILL`/`PERSP_KPIS` maps + the
`apply*` field-mapping, hardcoded provenance badges, and the hand-written
`OVERVIEW_METRICS.md`). Every drift bug we hit — wrong drill links, stale metrics
doc, provenance mismatches — came from this loose coupling. Adding one metric means
editing five files. That's the evidence the relationship between **what is
displayed / how it's computed / how it's displayed / how to drill for more** needs a
single source of truth.

## 2. The key insight

The pyegeria **`FormatSet`** (a.k.a. ReportSpec, `pyegeria/view/_output_format_models.py`)
already models most of it — including the perspective/question and drill links we
were about to reinvent:

| Concern | `FormatSet` field |
|---|---|
| **What is displayed** | `target_type` (OM type) + `formats[].attributes` (`Column`/`Attribute`: `name`,`key`) + `heading`/`description`/`family` |
| **How it's computed** | `action: ActionParameter{function, required_params, optional_params, spec_params}` (FROM + params). Advisor's report-spec layer adds `content_filters` (WHERE), `shape_defaults`, `performance_hints`, `master_detail`. |
| **How it's displayed** | `formats[].types` = `DICT/LIST/TABLE/REPORT/MERMAID/HTML`, **plus Vega-Lite charts** (attributes keyed `*BarGraph`/`*PieGraph`/`*VegaGraph`), **Mermaid pie charts**, and **profile/aggregation attributes** (`zoneProfile…` → distributions) |
| **How to drill (more info)** | `Column.detail_spec` (a ReportSpec for a column's detail) + `get_additional_props` (a second action) |
| **Who it's for** | `question_spec: [{perspectives, questions}]` — declares which **perspectives** and which NL **questions** the spec answers (field was migrated `roles → perspectives`) |

Decision consequence: **extend `FormatSet`, don't build a parallel dashboard
registry.** Attributes are the unit of "what" — *not* columns; the tabular framing
is dropped (both terms remain interchangeable for back-compat).

## 3. Target architecture — five layers

```
Attribute        the unit of "what" (a data field); render kind decides presentation
   ↓ (a spec projects a set of attributes)
ReportSpec       reusable element definition: attributes + action(+params) + output
(FormatSet)      format + detail_spec (drill) + question_spec (perspectives/questions)
   ↓ (a container places specs and other containers)
Container        named, nestable, reusable layout: ordered placements of specs/containers
   ↓ (a dashboard is a top-level container + bindings)
Dashboard        top-level Container + perspective bindings + default parameters
                 (as-of time, scope). "Overview" is one; users/projects/orgs define more.
   ↓ (stored & managed)
Store            pyegeria-managed today → Egeria-native metadata (endgame)
```

A tile is then: **a ReportSpec answering a Question, placed in a Container, scoped by
a Perspective, computed by its `action`, rendered by its output format, drilling via
`detail_spec`.** One model for dashboard + Advisor + Perspective/Question.

## 4. Layer detail

### 4.1 ReportSpec as the dashboard-element definition
Use `FormatSet` as-is for identity, projection (attributes), compute (`action` +
params), display (formats), drill (`detail_spec`/`get_additional_props`), and the
perspective/question binding (`question_spec`). The advisor's report-spec layer
supplies WHERE/shape/params/master-detail. **`required/optional/spec_params` is the
hook for perspective-scope parameterization** (see §6).

### 4.2 Output-format generalization (backward-compatible) — see §5.

### 4.3 Container / placement — NEW
A **Container** is a qualified-named, reusable component holding **ordered
placements**; each placement references a child (a ReportSpec *or* another Container)
plus presentation hints.
- **Layout primitive (proposed):** ordered flow + span/emphasis hints (e.g.
  `span: 1|2|full`, `emphasis: kpi|panel`) — responsive, authorable in Dr.Egeria
  markdown, matches the current dashboard, nests cleanly. (Alternatives: absolute
  grid coordinates; named slots. Ordered-flow recommended; grid can come later.)
- **Nesting + reuse:** a placement can target a Container by qualified name → a
  "People panel" or "Governance summary" is authored once and reused across
  dashboards.
- **Dr.Egeria commands (proposed):** `Create Container`, placements via an attribute
  list (or `Place Report in Container`), and **extend the report view/embed command**
  to target a container/placement. QNs enable cross-referencing — mirrors the
  Perspective/Question Dr.Egeria pattern already shipped.

### 4.4 Dashboard
A **Dashboard** = a top-level Container + perspective bindings + default parameters
(as-of time, scope, filters). The current "Overview" becomes a dashboard definition;
user/project/org dashboards are additional definitions (§7).

### 4.5 Store
`base_report_formats.py` (generated) + advisor registry today → **pyegeria-managed
spec+container store** (read/write, versioned) authored by Dr.Egeria → **Egeria
metadata** (§8). "A broader dashboard/reporting-component model in pyegeria" is the
right near-term home: a component library (reusable containers + specs) carrying
rendering instructions.

## 5. Output-format generalization

Generalize `Format` from `types: [str]` toward a **render hint** `{ kind, options }`,
mapping legacy string types onto kinds so nothing breaks (`TABLE/LIST/DICT/MERMAID/
REPORT` keep working). New kinds needed for dashboards:
- **`kpi`** — scalar + delta + sparkline (names a value attribute + optional trend attr)
- **`series` / `line`** — asOfTime trend (needs the time-series execution mode, §6)
- **`funnel`**
- first-class **`bar` / `pie`** — generalize today's `*BarGraph`/`*PieGraph`
  attribute-key convention into an explicit kind

**Chart engine: commit to Vega-Lite** (already in the renderer) — a chart Format's
`options` can compile to a Vega-Lite spec, rather than inventing a viz grammar.
Attributes stay the data; the kind decides presentation. **Backward compatibility is
a hard requirement** (per direction): existing FormatSets must render unchanged.

## 6. Perspective as a parameterized lens (facets 1–3)

Perspective is not just show/hide; it is a **named scope + selection**:
- **Selection:** a perspective shows a placement if it (or the placed spec's
  `question_spec.perspectives`) includes it.
- **Scope/parameterization:** the perspective carries parameters (e.g., a steward's
  domain, an owner's assets) injected into each spec's `action` params **and** into
  its `detail_spec` drill — so "Governed Coverage" drills to *org-wide exceptions*
  for a Governance Lead but *"ungoverned assets in my domain"* for a Steward. Same
  metric, scoped drill. This reuses the report-spec parameter model.
- **Multi-user:** counts are already user-relative (per-user `X-Egeria-Token` +
  Egeria zone security; backend cache is keyed on `user_id`). Explicit "my domain"
  scope resolves from `assignmentScope` (Person→PersonRole→scope). User preferences
  (chosen perspective, custom dashboards) must move **off `localStorage` to
  per-user server-side** at scale. Guardrails: the native **count API** (#9168) +
  page/cost limits so user-authored specs stay cheap and safe.

## 7. Multi-dashboard & user-authored (the unlock — and its dependency)

Going the ReportSpec route lets users/projects/orgs **create and modify dashboards**:
an "Overview" (system default) plus special-purpose dashboards. **Hard dependency:**
user-authored dashboards force **generic execution** — every tile runs through the
report runner (`action` function dispatch, already in the advisor's
`report_spec_agent`); you cannot hand-code a handler per user tile. So §7 depends on
§4.1 (spec-driven) + §5 (render kinds) + a stored model (§8). Payoff: dashboards
become first-class, shareable, versioned, token-scoped, reviewable artifacts — and
the Advisor could generate them conversationally (it already builds report specs).

## 8. Egeria-native endgame (facet 4)

Egeria already has the pieces to make dashboards *rendered governed metadata*:
- **`GovernanceMetric`** (governance model) — native home for a metric definition.
- **Perspective + Question** elements — already modeled (`Perspective ─ScopedBy→
  Question`); Dr.Egeria authoring shipped (`OVERVIEW_PERSPECTIVES.dr-egeria.md`).
- **ReportSpec** — the "how to compute," linkable from a Question/Metric.
- **Scope** — `assignmentScope` / `GovernanceZone` / `Collection` express scope as
  relationships.
- **Container/Dashboard** — either a new type or a `Collection` subtype for layout.

Likely Egeria extensions: relationships `GovernanceMetric → Question`, a metric →
data-source/ReportSpec link, a drill/rendering property, and Dr.Egeria commands to
author metrics/containers (same pipeline as Perspectives). Chain:
`Perspective ─ScopedBy→ Question ─answeredBy→ GovernanceMetric(+ReportSpec)
─placedIn→ Container ─drillsTo→ element/collection`, scoped by zone.

## 9. Incremental roadmap (value early, de-risked)

| Phase | Scope | Unlocks / de-risks |
|---|---|---|
| **P0 ✅** | **DONE 2026-07-26.** Each current tile formalized as a `FormatSet` in `overview_specs.py` (attributes + action + render-kind + `detail_spec` + `question_spec` + provenance), served at `/api/overview/specs`; `OVERVIEW_METRICS.md` KPI catalog + provenance generated from it (`gen_overview_metrics.py`); drift guarded by `test_overview_specs.py` (242 checks). | Kills the drift-bug class; proves the model on real pyegeria `FormatSet` objects; pays for itself in maintainability. No container/user-auth. |
| **P1** | Generalize output formats (`kpi`/`series`/`funnel`, Vega-backed `bar`/`pie`), backward-compatible. Dashboard renders from render-kind. | Display model covers dashboard widgets. |
| **P2** | Container model + Dr.Egeria commands; rebuild Overview *as* a container of specs; perspective = filter/scope over placements. | Composition + reuse; perspective becomes a real lens. |
| **P3** | Move specs + containers into pyegeria-managed storage; unify on the report runner; back with Egeria metadata (`GovernanceMetric`/Perspective/Question/Container). | Generic execution; governed storage. |
| **P4** | User/project/org-authored dashboards; sharing/governance; Advisor-generated dashboards. | The multi-dashboard vision. |

P0–P1 stand alone and are worth doing regardless of whether P3–P4 ship.

## 10. Open decisions

1. **Layout primitive:** ordered-flow + span (recommended) vs grid coordinates vs named slots?
2. **Output-format generalization:** render-hint `{kind, options}` with legacy mapping (recommended), and **commit to Vega-Lite** as the chart engine?
3. **Execution:** commit to unifying on the **report runner** at P3 (required for P4), keeping bespoke handlers only through P1–P2?
4. **Storage/ownership:** pyegeria-managed store near-term, Egeria-native metadata endgame — both, with a migration path?
5. **Container as metadata:** new `Container`/`Dashboard` type vs reuse `Collection` for layout?

## 11. Risks / caveats

- FormatSet's display vocabulary is report/table/chart-oriented — **KPI tiles,
  sparklines, funnels, and the time-machine are not yet expressible**; real extension
  work across pyegeria + advisor.
- Generic **action execution** lives in the advisor's report runner; the dashboard
  uses bespoke handlers today — unifying is the biggest architectural move.
- **Couples** the dashboard's evolution to the ReportSpec model (shared across
  pyegeria / advisor / egeria) — a governance win but a coordination cost.
- **Backward compatibility** for existing FormatSets is non-negotiable.
- Related: the load-all paging/sequencing strategy (PY-20) and the native count API
  (#9168) are prerequisites for cheap, correct, user-authored specs.

## 12. Cross-references
- `OVERVIEW_METRICS.md` — current per-metric catalog + provenance (the P0 source-of-truth candidate).
- `OVERVIEW_NEXT_STEPS.md` — R-1/R-2/R-3 metric-definition research (contextualized coverage, AI-ready, business value) that will live in this model.
- `PYEGERIA_ISSUES.md` PY-20 — load-all paging strategy; #9168 — native counting.
- pyegeria `pyegeria/view/_output_format_models.py` (`FormatSet`/`Format`/`Column`/`ActionParameter`/`QuestionSpec`), `base_report_formats.py`, `output_formatter.py`.
- egeria-advisor `advisor/report_spec_*.py`, `report_spec_agent.py` (the report runner), `report_spec_elicitor.py`.
- `OVERVIEW_PERSPECTIVES.dr-egeria.md` + `gen_perspectives.py` — the Perspective/Question authoring pattern to mirror for metrics/containers.
