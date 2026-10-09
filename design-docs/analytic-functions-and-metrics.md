<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Analytic functions, KPI metrics and the Governance Metrics panel — design note

**Status:** exploratory / for discussion (2026-10-04). A quick feasibility look, **not** a design. It
exists to frame the cross-repo decisions (portal = `egeria-workspaces`, pyegeria = `egeria-python`,
trellis = Resource Explorer and friends) before anyone writes code. Companion to, and built on:

- `compose-configs/egeria-quickstart/PyegeriaWebHandler/OVERVIEW_REPORTING_MODEL.md` — the five-layer
  dashboard model (Attribute → ReportSpec/`FormatSet` → Container → Dashboard → Store). Its decision,
  "extend `FormatSet`, don't build a parallel dashboard registry", is assumed here.
- `.../OVERVIEW_METRIC_GOVERNANCE.md` (NEXT-24) — governing the dashboard's own metrics as Egeria elements.
- `design-docs/report-rendering-plan.md`, `design-docs/perspective-question-scoping.md`.

> **How to read the evidence.** *[verified]* = I ran it or measured it against the live platform this
> session. *[read]* = I read the code. *[inferred]* = taken from grep output or a read-only survey and
> not run. The pyegeria code was read from the copy inside the `quickstart-pyegeria-web` container, so
> the installed release is the only version examined.

## 1. The question

Can the code behind the Overview's KPIs become **analytic functions callable from within a
`report_spec`**, with each function's **description** surfaced in the portal's **Governance Metrics
panel**, in a way that is **extensible** — a new function is registered in one place and neither the
page nor the panel needs editing?

**Short answer: mostly yes, and most of the machinery already exists.** What is missing is a *contract*
for what an analytic function promises (§4), a single-place registration path (§5), and a live feed from
the registry to the panel (§3). The biggest risk is not plumbing but semantics: the KPI code only became
trustworthy this month because of rules that are not yet written down anywhere a function author would
find them (§2).

## 2. What building honest KPIs taught us (requirements, not nice-to-haves)

The Overview was rebuilt in October 2026 (PRs #599–#602) so that it never shows a sample number as a
measurement. Every item below was found by running against real data, and each is a requirement on any
function that will be callable from a spec — otherwise a spec author can silently reintroduce the bug.

| # | Lesson | Concrete case | What a function must promise |
|---|---|---|---|
| 1 | **Unknown is not zero** | pyegeria's `count_elements` returns `0` on any failure and `_find` swallows exceptions into `[]`, so a failed count reads as a measured zero *[read]* | Return a distinct "not measured" state; never fold failure into `0`/`[]`. |
| 2 | **Existence is not outcome** | A failed survey still writes a `SurveyReport` and partial findings; "a report exists" counted failed surveys as coverage *[verified]* | State what the number counts and what it excludes; classify outcomes, don't infer success. |
| 3 | **Categories must not overlap** | "Processes" already contained software components and APIs (`DeployedAPI → DeployedSoftwareComponent → Process`); bars summed to 2,098 vs a true total of 2,009 *[verified]* | Declare whether categories are exclusive and whether they sum to a stated total. |
| 4 | **A capped page is a lower bound** | Egeria `find` has no total; one page is capped at `max_paging_size` *[read]* | Report `capped`, and withhold any derived figure (e.g. "never surveyed = total − surveyed") that a lower bound would corrupt. |
| 5 | **A proxy is fine if it is labelled** | "Has schema captured" = anchors of `SchemaType` elements ∪ survey schema analysis; neither is "the schema" *[verified]* | Carry a plain-language caveat and the *denominator* ("of all assets"), shown with the number. |
| 6 | **The data model surprises you** | `ReportSubject` also links connector-activity reports; the subject end is typed just `Asset`; surveys record a database's schema as annotations, not `SchemaType` elements *[verified]* | Document the types/relationships actually used so the next author can probe them. |
| 7 | **Identity and scope change the answer** | The Overview now runs as the persona picked in the Portal, so numbers follow that persona's zone access *[verified]* | Declare context sensitivity (persona/token, as-of time, `forLineage`) and put it in any cache key. |
| 8 | **Test the failure path, not just the happy path** | A render-order bug and a "no data vs stale numbers" contradiction were found only in a real browser, with a simulated failing backend *[verified]* | Ship fixtures for: success, empty, failed, capped, inconsistent counts. |

These eight are the seed of the function contract in §4.

## 3. What exists today

### 3.1 Report specs execute named functions already *[read, inferred line numbers]*

(Paths relative to `pyegeria/view/` in the container.)

- **Data model** — `_output_format_models.py`: `FormatSet` (target type, heading, description, family,
  `formats`, `action`, `question_spec`, `detail_spec` via `Column`) and `ActionParameter`, which carries
  `function` (a client method, `Class.method`) **and `analytic_function`** (a dotted path to a callable),
  plus `analytic_spec_params`.
- **Loading / registration** — `base_report_formats.py`: specs are generated Python; `load_report_specs`,
  `register_report_specs` (runtime registration; raises `ReportFormatCollision` on duplicates); extra specs
  can be loaded from a directory named by `PYEGERIA_USER_REPORT_SPECS_DIR`.
- **Execution** — `format_set_executor.py`: `_resolve_analytic_function` imports the dotted path
  (`importlib.import_module` + `getattr`, checks `callable`); `_bind_client_args` auto-binds the leading
  `mgr`/`ce` client argument; `run_analytic_action` runs *fetch → analytic*; the result is wrapped into an
  output format (no chart wrapping when the result is a raw dict).
- **A real registry** — `analytic_registry.py`: `AnalyticFunctionSpec` (name, dotted `function`,
  `description`, `returns`, `generic`, `binding_note`, `params`, optional `action`); a hand-written
  `_BUILTINS` (~23 entries); a **CONFIG tier** loaded from `PYEGERIA_ANALYTIC_FUNCTIONS_JSON` and
  `PYEGERIA_ANALYTIC_FUNCTIONS_MODULES` (`pkg.mod:func` returning a dict) — a genuine plugin hook; a
  **RUNTIME tier** (`register_analytic_functions` / `unregister_analytic_function`); collisions across tiers
  raise `AnalyticRegistryCollision`; `analytic_registry_payload()` backs `/api/analytics`.
- **Demo specs** — `analytic_demo_specs.py` holds one executable `FormatSet` per registry entry.
- **MCP** — `core/mcp_adapter.py` exposes `run_report`; the survey did not find the analytic registry exposed
  to MCP specifically *[inferred]*.

### 3.2 The Governance Metrics panel *[read]*

- Page `governance-metrics.html` (route `/governance-metrics`) fetches `/api/governance-metrics`, served by
  `governance_metrics_handler.py`, which queries **live `GovernanceMetric` elements in Egeria** (summary,
  scope, usage, implementationDescription, measurement, target) and follows their `GovernanceResults` link
  to a Report and an `InformationSupplyChain`. It is cached (`_CACHE_TTL`).
- Those elements are produced by `gen_governance_metrics.py`, which reads the **analytic registry** and
  emits Dr.Egeria markup (`OVERVIEW_GOVERNANCE_METRICS.dr-egeria.md`: one `GovernanceMetric`, `Report`,
  `GovernanceResults` link and supply chain per non-generic function). The file must be regenerated and
  loaded with Dr.Egeria `--validate` / `--process`.
- So the panel is **not static and not live from the registry**: it shows what has been *loaded into
  Egeria*. A function added to the registry does not appear until someone regenerates and loads.

### 3.3 Two parallel descriptions of the same thing *[read]*

`overview_specs._TILES` (12 tiles; `summary`/`usage`; feeds `/api/overview/specs` and the generated glossary
`OVERVIEW_ANALYTICS_GLOSSARY.dr-egeria.md`) and the registry's `description`/`binding_note`/`returns` are
separate prose sources for the same metrics. They can drift.

### 3.4 The Overview does not go through any of it *[read]*

`overview_handler.py` imports the `overview_metrics` functions directly (and the survey/schema/
confidentiality helpers added this month live in the handler itself). A new function is therefore *not*
automatically an `/api/overview/*` endpoint, a spec, or a panel entry.

## 4. A candidate contract for an analytic function

Derived from §2, not yet validated. Everything is *declared* alongside the function so a generator can
turn it into a spec entry, a panel entry and a glossary term from one source.

**Result shape** (replaces "return a number"):

```
{ value | values,                 # the measurement
  status: "measured" | "not_measured" | "partial",
  capped: bool,                   # a lower bound
  basis:  { numerator, denominator, denominator_label },   # "2 of 2,647 assets"
  caveats: [str],                 # plain language, shown with the number
  as_of:  iso8601 | null }
```

**Declared metadata:**

| Field | Why (lesson) |
|---|---|
| `name`, `summary`, `usage`, `formula_note` | what the panel/glossary shows; one source of prose (fixes §3.3) |
| `source_types` (OM types / relationships read) | #6: probe-ability; also drives "which content pack must be loaded" |
| `category_semantics`: `exclusive`/`overlapping` + `sums_to` | #3 |
| `failure_semantics`: when is it `not_measured` vs a real 0 | #1 |
| `cost`: `calls`, `cap`, `timeout`, `heavy: bool` | #4 and Postgres/Egeria load (the metadata store has been saturated by connector load) |
| `context`: `needs_persona`, `supports_as_of`, `for_lineage`, `cache_key_parts` | #7 |
| `proxy_for` (optional) | #5 |
| `fixtures` | #8: success / empty / failed / capped / inconsistent |
| `owner`, `version`, `since` | extensibility and audit |

The existing `AnalyticFunctionSpec` already has `name`, `description`, `returns`, `generic`,
`binding_note`, `params`; the new fields are additive.

## 5. Design options

**A — Decorator-driven registry in pyegeria.** `@analytic(...)` on the functions in `overview_metrics`
builds the `AnalyticFunctionSpec` (params from the signature) and a default demo `FormatSet`. *Pros:* one
place per function, no drift between code/registry/demo spec. *Cons:* egeria-python change and a release
cycle; docstrings become the prose source; portal-side helpers stay outside it.

**B — A per-column "computed" attribute in a spec** (`Column(computed="registry_name", args={…})`). *Pros:*
the literal reading of "callable within a report_spec" — a spec can mix fetched and computed columns.
*Cons:* a model and executor change in egeria-python with per-row vs per-report semantics; largest and
riskiest. Action-level `analytic_function` may already cover most needs — see question 4.

**C — Keep the registry as is; extend it from the portal.** Register portal-side functions through the
existing CONFIG tier (`PYEGERIA_ANALYTIC_FUNCTIONS_MODULES`), and make `/api/governance-metrics` **merge**
registry entries (description, returns, `binding_note`, plus the §4 fields) with the Egeria
`GovernanceMetric` elements, tagging each as "governed (in Egeria)" or "registry only". *Pros:* works with
today's pyegeria, stays in this repo, "add a function" is one module and no page edits (the page already
iterates the API response), and it proves the end-to-end flow. *Cons:* a hybrid of live registry and
Egeria state; functions outside `overview_metrics` need a module on the import path.

**Recommended path (for discussion):** C first, then A once the contract has been exercised, and defer B.
Independently, harden the resolver (§6) — that is the one item that should not wait.

## 6. Risks

- **Callable-by-name is arbitrary-callable-by-name.** `_resolve_analytic_function` imports and calls any
  dotted path a spec supplies; no allowlist was evident *[read, not exercised]*. A spec authored by a user
  or by Dr.Egeria can name anything importable. Resolve only names present in the registry, or enforce a
  module-prefix allowlist. Decide who may author specs that name callables.
- **Semantics drift.** Without §4, a function written next month will reintroduce `0`-for-failure. A shared
  result type and the fixtures are the mitigation, not documentation.
- **Cost.** Functions need declared caps/timeouts; the registry has none. The Overview already uses a
  non-blocking background-cache pattern for slow aggregations (Survey Types, Integration Connectors); the
  registry/panel should reuse it rather than invent another cache.
- **Context.** Today only the client and an `as_of` argument reach a function. Persona/token, zone
  visibility and `forLineage` are not modelled; the Overview's caches must already include `lineage_key()`.
- **Two prose sources and two stores of truth** (registry vs Egeria `GovernanceMetric` elements) unless §5-C
  is done deliberately.
- **Version coupling.** Whether the pyegeria release in a given deployment contains the registry module
  must be pinned; only one container copy was examined.

## 7. Cross-repo implications

| Repo | Owns today | Under this note |
|---|---|---|
| **egeria-workspaces (portal)** | Overview/handlers, `/api/overview/*`, Governance Metrics page + handler, `gen_governance_metrics.py`, generated Dr.Egeria files | Option C lives here: merged panel API, CONFIG-tier module for portal-side functions (survey outcome/coverage, exclusive composition, confidentiality, schema coverage), contract fixtures in the existing test style |
| **egeria-python (pyegeria)** | `FormatSet`/`ActionParameter`, executor, `analytic_registry`, `overview_metrics`, `base_report_formats` | Contract fields on `AnalyticFunctionSpec`, resolver allowlist, the `count_elements`/`_find` None-vs-0 fix (already a known issue), possibly the decorator (A) and computed columns (B) |
| **trellis (Resource Explorer & co.)** | Creates surveys (`Survey: <name>` reports), runs them via a Prefect worker, holds Egeria GUIDs in its own registry, publishes/heals definitions | **Open — needs trellis owners.** (a) Agree a *survey outcome* convention (see §8). (b) Does Resource Explorer want KPIs of its own (run queue, outbox dead-letters, resync health) registered through the same CONFIG-tier hook? (c) The persona/identity story (§2 #7) applies to anything it surfaces |

## 8. Related findings from the same session (not part of the design, but they bound it)

1. **Surveys have no standard outcome field.** Today the outcome is inferred from two conventions:
   engine-run surveys carry a `completionMessage` (`OMES-SURVEY-ACTION-0019` "has completed…" vs `-0018`
   "…threw…"), tool-created reports carry `error_count` in `additionalProperties`, and some database surveys
   record only table/column counts and are therefore *unknown*. A standard completion status on
   `SurveyReport` (or a documented convention for tools that create them) would remove the inference.
2. **Scheduled insight jobs fail every cycle** on the rebuilt platform: the three open-lineage jobs cannot find
   an OpenLineage log store (`directory: <null>`; defined in the platform's Organization Insight content pack,
   not in this repo) and the zone-membership profile throws a null-property error (suspected: membership of a
   template placeholder zone with no `GovernanceZone` element — unconfirmed). Relevant here because a
   "pipeline health" metric would currently read ~60 failed of 63.
3. **The PostgreSQL server survey fails** on the one database examined with
   `relation "treasury.public.dts_opcashdpst" does not exist`, at SQL position 22 — consistent with the
   three-part name being quoted as a single identifier (suspected survey-service bug; unconfirmed without the
   database credentials).

## 9. Decisions needed

1. Should the Governance Metrics panel stay **backed by Egeria `GovernanceMetric` elements** (governed, with
   lineage) or show the **registry directly**? Is the merged view of §5-C acceptable?
2. Which prose wins — `overview_specs._TILES` or the registry's description — and should one be generated
   from the other?
3. Do generic functions (`count_elements`, `counts_by_type`, …) get panel entries, perhaps one per
   parameterised use?
4. Is **action-level** `analytic_function` enough, or is a per-column computed type (B) really required?
5. Where do new functions live: pyegeria (shared, release cycle) or the portal (CONFIG-tier module)? Where
   do trellis-side functions live?
6. Adopt the §4 result type and declared metadata? Which fields are mandatory, and who reviews a function's
   `failure_semantics` and `category_semantics` before it ships?
7. Who may author specs that name callables, and is a registry-name-only resolver (no free dotted paths)
   acceptable?
8. Defaults for caps/timeouts, and should `heavy` functions be excluded from synchronous requests?
9. What is the single standard for **survey outcome** that Resource Explorer and the engine surveys will both
   write?
10. How should persona-dependent metrics be presented on a shared panel — per-viewer numbers, or a declared
    "as seen by" scope?

## 10. Suggested next steps (small, in order)

1. Agree the contract (§4) and the survey-outcome convention (§8.1) — a short conversation, not code.
2. Resolver allowlist in pyegeria (independent, small).
3. Option C as a thin vertical slice: register **two** existing portal helpers (survey coverage and exclusive
   composition) through the CONFIG tier with full §4 metadata; extend `/api/governance-metrics` to merge and
   tag them; confirm a third function can be added without touching the page.
4. Revisit A and B with that experience.

## Appendix — the current KPI functions and their contracts today

| Function | Where | Reads | Failure behaviour today | Notes |
|---|---|---|---|---|
| `count_elements` | pyegeria `overview_metrics` | native count / `find` | **returns 0** *[read]* | generic; the root of lesson #1 |
| `counts_by_type` | pyegeria | `count_elements` per type | 0 per failed type | buckets overlap (lesson #3); portal now de-overlaps in `_exclusive_by_type` |
| `governed_coverage` | pyegeria | one capped classification find | best-effort; capped | PY-15 server caveat on multi-condition matches |
| `certifications_summary` | pyegeria | `Certification`/`License`/`Exception` relationships | `None` fields on failure | `soon[]` = next 5 within 90 days |
| `orphan_glossary_terms`, `stale_assets` | pyegeria | glossary terms / assets | `None` fields | `stale` uses a 180-day cutoff |
| `context_readiness_funnel`, `ai_ready_assets`, `semantic_grounding`, `ownership_coverage`, `business_value_signals` | pyegeria | several capped finds | mixed | funnel stages are proxies; samples are capped (e.g. "8 of 500 checked") |
| `people_counts`, `feedback_summary`, `usage_context_counts` | pyegeria | `count_elements`, relationships | **0 on failure** (via `count_elements`) | |
| `contextualised_coverage` | pyegeria | `ImplementedBy` distinct assets | `None` on failure | a proxy, documented as such |
| `growth_series` | pyegeria | `asOfTime` snapshots | `None` per failed point | page keeps gaps as gaps |
| `_survey_outcome`, `_survey_coverage` | portal `overview_handler.py` | `SurveyReport`, `ReportSubject`, `ReportedAnnotation`, `DataStore` | `None` per step; outcome `unknown` never counted as success | completed-survey coverage; failed surveys reported separately |
| `_exclusive_by_type`, `_confidentiality_levels`, `_schema_coverage` | portal `overview_handler.py` | type counts, `Confidentiality` classification, `SchemaType` anchors | `None`; capped → withheld | the reference implementations of lessons #3–#5 |
