<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Egeria Reporting & Dashboard Model — design

**Status:** design / discussion (2026-07-25). **P0 landed 2026-07-26** (see §9);
**P2 core landed 2026-07-26** (Container model, ahead of P1); **P1 core landed
2026-07-27** (Vega-Lite chart-engine decision + generator library + two
dashboard charts live-verified — see §5/§9). Companion to `OVERVIEW_README.md`,
`OVERVIEW_METRICS.md`, `OVERVIEW_NEXT_STEPS.md`.

**P0 shipped:** `overview_specs.py` (the single source-of-truth tile registry, 11
KPIs as real pyegeria `FormatSet` objects), served at `GET /api/overview/specs`;
`gen_overview_metrics.py` generates the KPI catalog + provenance block of
`OVERVIEW_METRICS.md` from it; `test_overview_specs.py` guards that the registry,
the frontend `METRICS`/`PERSP_KPIS`/`DRILL` maps, and the generated doc block
never silently diverge.

**P2 core shipped (ahead of P1):** `overview_containers.py` — a pyegeria-local
`Container`/`Placement` model (§4.3), per the open-decision resolution below
(storage stays local, not Egeria metadata, for now). The "Overview" dashboard is
now expressed as one `Container` (`OVERVIEW_CONTAINER`) whose placement order
mirrors `overview_specs.TILE_ORDER`. **Perspective is a real filtered/reordered
view over placements** (§6), not a separate hardcoded list — `view_for_perspective()`
derives it from each tile's own `question_spec.perspectives`, matching
`PERSP_KPIS` exactly (order included, drift-guarded). Served at
`GET /api/overview/container?perspective=<p>`. `test_overview_specs.py` (274
checks total) extended to cover container resolution + all 8 perspective views.
**Not yet built:** the Dr.Egeria markdown commands to *author* containers (§4.3's
`Create Container` proposal) — that's authoring-pipeline work in the separate
egeria-python `md_processing` repo, a distinct increment from the container model
itself, and the frontend SPA does not yet render from `/api/overview/container`
(still reads its own `PERSP_KPIS` map, now guard-locked to match). Chart-engine
work (§5, Mermaid + Vega-Lite two-tier) is P1 and not started.

The five open decisions (§10) are now **resolved** — see below.

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

**Chart engine — DECIDED (2026-07-27, revised): Vega-Lite is the default/primary
engine whenever there's a choice** — it renders visibly richer output than
Mermaid and, as of this revision, covers far more chart shapes (see below).
Mermaid is not treated as a competing "markdown-native tier" for new chart
types; it remains the right choice only for the structural diagrams it
already owns (entity/relationship graphs, mind maps, its existing pie-chart
convention) — nothing about that changes. (This revises the 2026-07-26 "two-tier
Mermaid + Vega-Lite" call in §10 #2's history below; superseded per direction:
"vega-lite generates nicer graphs than mermaid — so we should use them when
there is a choice.")

Both engines already share one convention worth keeping: **rendered output is
a fenced markdown code block** (```` ```vega-lite ```` / ```` ```mermaid ````
containing the spec/graph text), auto-detected today by an attribute
key-suffix convention (`_is_vega_attribute`/`_is_mermaid_attribute` in
pyegeria's `output_formatter.py`). A chart Format's `options` compiles to
one of these — not a bespoke viz grammar. **Backward compatibility is a hard
requirement** (per direction): existing FormatSets must render unchanged.

**Landed (2026-07-27, ahead of the rest of P1):** pyegeria already shipped
`generate_vega_bar_chart`/`generate_vega_pie_chart` (`pyegeria/view/vega_utilities.py`)
plus a **generic auto-promotion pass** in `output_formatter.py` that finds any
nested `{str: number}` "categorical counts" shape in an extracted element and
auto-generates bar+pie Vega specs for it, with zero per-type configuration —
this alone covers a lot of dashboard composition needs for free. Extended
2026-07-27 with `generate_vega_line_chart`/`generate_vega_area_chart`
(multi-series via a `fold` transform over wide-format records — no reshaping
needed by callers), `generate_vega_scatter_chart`, `generate_vega_funnel_chart`
(ordered horizontal bars — Vega-Lite has no native funnel mark), and a
low-level **`generate_vega_chart(values, mark, encoding, title, ...)`
escape hatch** for any chart shape without a named generator — deliberately
open-ended, since "we don't know what kind of graphs users will want — we
know only what we currently need" (direction, 2026-07-27). 16 unit tests,
`egeria-python` commit `319b177`.

**Wired into the Overview dashboard (2026-07-27):** `overview_handler.py` now
returns ready Vega-Lite specs — `byTypeChart` (assets-by-type composition),
`feedbackChart` (people feedback-by-type), `growthChart` (multi-series growth
trend), `funnelChart` (context-readiness funnel) — and `egeria-overview.html`
renders them via a new `renderVega()` helper (loads `vega-embed`, merges a
dark-theme `config` so charts match the dashboard instead of Vega-Lite's
white-background default). **Verified live: `byTypeChart` and `feedbackChart`**
(both use only the pre-existing `generate_vega_bar_chart`, already on the
deployed pyegeria 6.0.17.2). **`growthChart`/`funnelChart` cannot be verified
yet** — the deployed pyegeria is pinned via `requirements.txt` to a PyPI
release that predates `generate_vega_line_chart`/`generate_vega_funnel_chart`;
the handler imports them defensively (`try/except ImportError` → `None`) so
the app runs fine either way, and both fields will activate automatically once
the pin is bumped to a release that includes them — no further dashboard code
changes needed. **Known gap, not yet closed:** the Vega bar charts replacing
`hbars()` rows lose the per-bar "click to drill" affordance (Vega tooltips
partially compensate); revisit once wiring `growthChart`/`funnelChart` forces
a broader look at drill-parity (both the old growth SVG and the funnel rows
are also click-drillable today and were deliberately left alone until they can
be verified, rather than guessing at replacement UX blind).

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
| **P0 ✅** | **DONE 2026-07-26.** Each current tile formalized as a `FormatSet` in `overview_specs.py` (attributes + action + render-kind + `detail_spec` + `question_spec` + provenance), served at `/api/overview/specs`; `OVERVIEW_METRICS.md` KPI catalog + provenance generated from it (`gen_overview_metrics.py`); drift guarded by `test_overview_specs.py` (242 checks at P0, 274 after P2). | Kills the drift-bug class; proves the model on real pyegeria `FormatSet` objects; pays for itself in maintainability. No container/user-auth. |
| **P1 (core ✅, `kpi`/`series` render-kind generalization not started)** | **DONE 2026-07-27 (core):** chart-engine decision revised to Vega-Lite-primary (§5/§10 #2); pyegeria `vega_utilities.py` extended with line/area/scatter/funnel generators + a generic escape hatch (16 tests, commit `319b177`); Overview wired for 4 chart fields (`byTypeChart`/`feedbackChart`/`growthChart`/`funnelChart`), 2 of 4 **live-verified** (byType, feedback — both dark-themed via a new `renderVega()` helper), 2 deferred pending a pyegeria version bump (growth, funnel — wired defensively, `None` on the current pin). **Still open:** the `{kind, options}` render-hint generalization on `Format` itself, `kpi`/`series` render kinds, and drill-click parity for the new Vega bars (known gap — see §5). | Display model covers dashboard widgets. |
| **P2 (core ✅, Dr.Egeria commands not started)** | **DONE 2026-07-26 (core):** `overview_containers.py` — pyegeria-local `Container`/`Placement` model; Overview rebuilt *as* a `Container` of the P0 specs; perspective = real filter/scope over placements (`view_for_perspective()`), served at `/api/overview/container`. **Still open:** Dr.Egeria `Create Container` authoring commands (separate egeria-python repo work); SPA rendering from the container endpoint. | Composition + reuse; perspective becomes a real lens. |
| **P3** | Move specs + containers into pyegeria-managed storage; unify on the report runner; back with Egeria metadata (`GovernanceMetric`/Perspective/Question/Container). | Generic execution; governed storage. |
| **P4** | User/project/org-authored dashboards; sharing/governance; Advisor-generated dashboards. | The multi-dashboard vision. |

P0–P1 stand alone and are worth doing regardless of whether P3–P4 ship.

## 10. Open decisions — resolved (2026-07-26)

1. **Layout primitive:** ordered-flow + span — **confirmed**, proceed as recommended.
2. **Output-format generalization / chart engine — DECIDED (revised 2026-07-27):
   Vega-Lite is the default engine whenever there's a choice; Mermaid is not a
   competing tier for new chart types.**
   *(History: on 2026-07-26 this was first decided as a Mermaid + Vega-Lite
   two-tier split — Mermaid as the "markdown-native" default for bar/line/pie,
   Vega-Lite only for funnel/KPI+sparkline/interactivity. Superseded the next
   day per direction: "vega-lite generates nicer graphs than mermaid — so we
   should use them when there is a choice," plus "we should look at adding
   more vega-lite types... we don't know what kind of graphs users will want.")*
   Mermaid remains the right choice only for what it already structurally owns
   (entity/relationship diagrams, mind maps, its existing pie-chart convention)
   — not the default for new dashboard chart types. Both engines still share
   the same fenced-markdown-block rendering convention (§5), so this isn't a
   storage-shape fork, just an engine preference. Extensibility answer: rather
   than trying to enumerate every future chart type up front, pyegeria's
   `vega_utilities.py` now has named generators for the known shapes
   (bar/pie/line/area/scatter/funnel) **plus** a generic `generate_vega_chart()`
   escape hatch for anything else — see §5 "Landed" for what shipped. Backward
   compatibility for existing FormatSets remains a hard requirement either way.
3. **Execution — P2 approved, "worth trying," may need tweaking as it's built.**
   Proceed into Container model + Dr.Egeria commands now. Full unification on the
   generic report runner stays a P3 commitment (required for P4); bespoke handlers
   are fine through P1–P2.
4. **Storage/ownership — P3 explicitly backlogged** ("will be a few weeks").
   Continue with the **current local approach pyegeria already takes** (Python/JSON-
   defined FormatSets, as `overview_specs.py` does) — no move to Egeria-native
   metadata storage yet. P2's Container model is therefore also pyegeria-local
   (a Pydantic model + Python/JSON definitions), **not** new Egeria element types —
   that step waits for the P3 storage decision.
5. **Container as metadata — deferred with P3/P4** (both backlogged); revisit
   alongside the storage decision.

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
- `LOCAL_DASHBOARDS_TUTORIAL.md` — user-facing guide to §13's Dashboard Sheet track.

## 13. Update — the Dashboard Sheet / Report track actually shipped §9's P3 goals, via a different path (2026-07-29 → 2026-07-30)

§9's roadmap framed "generic action execution" and "user-authored dashboards"
as P3/P4 work gated on migrating the **Container** model into Egeria-native
storage. What actually got built instead — driven by real user feedback, not
a planned continuation of P2 — is a **parallel, simpler track** that reaches
much of the same destination without that migration:

- **`Report`** (Dr.Egeria `Create Report`) — a real Egeria asset (not
  pyegeria-local) naming a Report Spec plus its own default execution
  parameters. Fixes the exact problem `overview_containers.py`'s pyegeria-local
  `Container`/`Placement` model never solved: a placement can finally be
  genuinely scoped/parameterized instead of a bare Report Spec reference with
  no way to carry fixed values.
- **`Dashboard Sheet`** (`pyegeria/view/_output_dashboard_sheet_models.py`,
  Dr.Egeria `Create Dashboard Sheet`/`Link Report to Dashboard Sheet`/`Add
  Text on Dashboard Sheet`) — the user-authored analog of `Container`, still
  pyegeria-local (JSON store, not Egeria-native — P3's storage question is
  still open), but real and shipping today via `local-dashboards.html`/
  `local_dashboards_handler.py` (egeria-workspaces-fs), documented in
  `LOCAL_DASHBOARDS_TUTORIAL.md`.
- **Generic analytic execution — §9 P3's "unify on the report runner" landed**,
  but via a second `ActionParameter` execution path (`analytic_function` /
  Dr.Egeria's `extra_find`) rather than migrating `action_function`'s
  client-method-call path. `format_set_executor.py`'s `exec_report_spec()` now
  runs either path per `FormatSet`, and `SERIES`/`BAR`/`PIE` output formats
  wrap an analytic function's result as a Vega-Lite chart — the `kpi`/`series`
  render-kind generalization §5 called for, achieved without touching
  `Format.types`'s string-based shape at all (dispatched before the normal
  Format-row lookup instead).
- **Analytic function registry** (`pyegeria/view/analytic_registry.py`) +
  **demo report specs** (`analytic_demo_specs.py`, 10 specs, family
  `"Analytic Function Demo"`) — a discoverable catalog of what's runnable,
  each function marked `generic` (what it counts is a parameter) or a fixed
  metric (hardcoded vocabulary), browsable in Egeria Explorer's new
  "Analytic Functions" sub-tab (under Reports) and cross-linked to its demo
  spec.
- **Config-driven, zero-registration-call visibility** — `get_report_registry()`
  auto-loads a CONFIG tier (`settings.Environment.pyegeria_report_spec_modules`
  / `PYEGERIA_REPORT_SPEC_MODULES`) on first call, so the demo specs (and any
  future extra report-spec source) are visible to `dr_egeria`, `hey_egeria`,
  the Portal, and any other pyegeria consumer without each one remembering to
  register anything.

**What this does *not* close** — the real gap list from re-assessing "is this
enough to rewrite the Overview dashboard on Dashboard Sheets" (2026-07-30):
no composite/derived metrics (`overview_handler.py`'s `assetTotal =
sum(counts_by_type(...))` has no analytic-function equivalent yet), no
perspective lens on Dashboard Sheets/Placements (§6 is still `Container`-only),
no compact KPI-tile-band rendering (Local Dashboards renders full cards, not
icon+number+sparkline tiles), no sparklines-in-tile, no drill-down (§5's
"known gap" still applies here too), and no caching (every Local Dashboards
placement re-queries live on every page load, unlike Overview's 60–900s TTLs).
Tracked as `egeria-workspaces-fs` `BACKLOG.md` NEXT-16 (rename "Usage Context
Counts") and NEXT-17 (more comprehensive metrics); the KPI-tile-band/
perspective/drill-down/caching gaps aren't backlog items yet — surfaced here,
not yet triaged.
