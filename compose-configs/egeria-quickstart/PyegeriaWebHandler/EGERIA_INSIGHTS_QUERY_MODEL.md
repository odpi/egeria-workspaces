<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Egeria Insights — Saved Query Model (design)

**Status:** design + Track A **shipped and live-verified** (2026-08-05).
Track A of Part 3's plan (A.1–A.4: query-editor searchable dropdowns,
save/load via `ResultsSet.additionalProperties`, `CollectionMembership`
materialization + staleness UI, the Saved Queries tab) is built, tested end
to end against the running qs-view-server, and about to be committed — see
the "Track A build notes" callout after §2.3 for what was learned building
it (in particular: the real Egeria type is spelled **`ResultsSet`**, not
`ResultSet`). Tracks B and C (§ Part 3) remain design-only. Companion to
`OVERVIEW_REPORTING_MODEL.md` (the sibling design doc this one converges
with — see §2).

**Trigger:** NEXT-25 built Egeria Insights into a real 3-way advanced search
(classification + relationship + property-value conditions, freely
combinable via ALL/ANY/NONE, role/direction-aware). The natural next
question — "can a user save one of these queries and re-run it?" — turned
into a design discussion about what a saved query actually *is*, and it
converges with reporting/dashboard work already underway elsewhere in this
project rather than being a new, isolated feature.

---

## Part 1 — Current thinking

### 1.1 What Egeria Insights already does, and what it's missing

Insights' `POST /api/insights/search` (`insights_handler.py`) currently
composes a query across three independent dimensions and executes it as a
single call to `MetadataExpert.find_metadata_elements` (classification +
property-value conditions, combined server-side in one `FindRequestBody`)
plus a client-side GUID-set pass for relationship conditions (Egeria's find
API has no relationship-presence filter). This is deliberately generic —
it doesn't know or care what the query is *for*, it just runs it and
renders a table.

**A review of `ClassificationExplorer`/`MetadataExpert`'s existing methods**
(2026-08-05, prompted by the question "is `find_metadata_elements` really
the best/only tool for this?") found more combined-query surface than
expected, but not a full match for what Insights' UI needs:

| Method | Combines | Limitation vs. Insights' needs |
|---|---|---|
| `MetadataExpert.find_metadata_elements` | type + N classification conditions (ALL/ANY/NONE) + N property conditions (ALL/ANY/NONE), one server call | No relationship-presence filter at all |
| `ClassificationExplorer.find_elements_by_classification_with_property_value` | **one** classification name + one property-value string + relationship-type scoping (`include_only_relationships`/`skip_relationships`) + extra classification filters + zone filter | Only one named classification, one value-search string — not N independently-combinable conditions |
| `ClassificationExplorer.find_related_elements_with_property_value` / `find_relationships_with_property_value` | relationship scoping + property-value search | Same one-condition-at-a-time shape |
| `ClassificationExplorer.find_authored_elements` (by category) | elements a given actor authored, scoped by an authoring category | Narrow, purpose-built — not a general filter, but exactly right *when* the question is "what did X author" |
| `ClassificationExplorer.find_root_elements` | elements with no incoming containment/anchor relationship (i.e. the "tops" of a hierarchy) | Narrow, purpose-built — right *when* the question is "show me the roots" |
| `MetadataExpert.find_elements_for_anchor` | all elements anchored to a given element | Narrow, purpose-built — efficient for "everything under this anchor" |
| `MetadataExpert.find_elements_for_anchor_domain` | all elements anchored within a given domain | Same shape, domain-scoped |
| `MetadataExpert.find_elements_for_anchor_scope` | all elements anchored within a given scope | Same shape, scope-scoped |

So there's real, more-efficient-than-what-Insights-uses-today capability
for the *narrow* case (one classification, one relationship type, one
value search, or an anchor/authorship/root-elements question) — worth
using directly when a query happens to fit that shape, rather than always
falling through to the generic `find_metadata_elements` + client-side
relationship pass. But none of these support the fully general "N
classification conditions AND N relationship conditions AND N value
conditions, each independently ALL/ANY/NONE" shape the UI offers. **A new,
more general query method is planned to close this gap — expected in the
order of days, not immediate.** This document's design should not block on
it: the storage/lifecycle model below is deliberately execution-method-agnostic
(§2.1), so saved queries keep working, and simply get more expressive, once
the new method lands.

**Idea (brainstorm, not designed): let the user pick "by functionality"
before building conditions.** Rather than always defaulting to the general
condition-builder path, the query editor could open with a functionality
selector — likely mutually-exclusive checkboxes/radio, e.g. "General
search" (today's builder) vs. "Elements authored by…" vs. "Root elements"
vs. "Everything under this anchor / domain / scope" — each routing to the
narrower, more efficient method above with its own (much simpler) form,
instead of forcing every question through the general N-way builder. Not
scoped yet — needs its own small design pass (which methods deserve a
dedicated form vs. staying reachable only through the general builder,
what the forms look like) before it's buildable; captured here so it isn't
lost. See Track A.5 in Part 3.

**This query builder is one way to construct a find — not the only one.**
It's a new, additional path, chosen because it's approachable for
non-programmers (visual condition rows vs. hand-writing a `FindRequestBody`
or calling a pyegeria method directly). Programmatic construction of finds
— directly in pyegeria, or via Dr.Egeria commands, or hand-built REST calls
— remains equally valid and isn't being superseded by this UI.

### 1.2 The reframe: this is the missing UI for `FormatSet.action`

The core insight from this discussion: "construct a query, execute it,
render a table" is not a new concept in this project — it's exactly what
pyegeria's `FormatSet`/`ActionParameter` model already exists for (see
`OVERVIEW_REPORTING_MODEL.md`), just missing a visual authoring tool.
`ActionParameter{function, spec_params}` is "how a report's data is
computed"; `FormatSet.formats[]` is "how it's displayed." Egeria Insights'
query builder is a natural fit for **authoring the `action` half**
interactively, where Dr.Egeria markdown commands have always been better
suited to *displaying/dashboard* definitions than to iteratively building
up a filter condition.

This reframing surfaces four real use cases for a *saved* query, not just
an ephemeral one:

- **(a) Basic search/drill-down** — the current use case, ephemeral,
  nothing saved.
- **(b) Saved queries as the basis for new `ReportSpec`/`FormatSet`s** —
  once a query is proven useful, its `action` (what to fetch) can be paired
  with formatting/columns to become a real, reusable report definition.
- **(c) Report specs feed dashboard elements** — since `FormatSet.action`
  already has both a `function` (element-query) path and an
  `analytic_function` path, and Local Dashboards / the Overview dashboard
  already consume `FormatSet`s as placements, a saved Insights query
  becomes usable as a dashboard tile's data source close to for-free once
  it's `ActionParameter`-shaped.
- **(d) Open → refine → save-as** — load a named query into the builder,
  edit conditions, save as a new query (or update in place). Standard
  "load, edit, save" UX, not a new pattern.

None of (b)/(c)/(d) require new machinery *beyond* what's described below —
they fall out once a query is represented in a storable, re-executable
shape.

---

## Part 2 — Design

### 2.1 What gets stored: the raw wire payload, not a pyegeria-specific shape

**Correction from the first pass at this design:** the stored unit is
**not** "a pyegeria method name" as the primary identifier. The intent is
that a saved query can be executed either (a) via pyegeria, calling a
named client method, or (b) directly against Egeria's REST API — by
Egeria itself, or by any other caller that isn't pyegeria at all.
Storing only a pyegeria method name would make (b) impossible, since it's
pyegeria-specific.

**So the primary artifact is: `{url, httpMethod, body}` — the literal,
wire-format REST payload**, exactly as it would be sent over HTTP. This is
mechanism-agnostic by construction: anything that can POST/GET to Egeria's
REST API can execute it. A pyegeria-specific convenience — `{clientClass,
methodName}` — can be stored **alongside** this as optional metadata for
callers (like Egeria Insights itself) that prefer to go through pyegeria
rather than construct the raw HTTP call themselves, but it is not the
thing being persisted; the JSON body is.

This also directly resolves §1.1's "which execution method" question
cleanly: the same stored query works whether the new combined-query method
exists yet or not, whether it's called via pyegeria or raw REST, and
whether it's Egeria's own report-running mechanism invoking it or a portal
app — because what's stored is just the request, not an abstraction over
one particular way of issuing it.

### 2.2 Fixed conditions vs. override-able execution parameters

A saved query's *filter logic* (which classifications, which
relationships, which property conditions, and how they combine) should be
fixed — that's the point of saving it. But some fields in the body are
execution parameters, not filter logic — `graphQueryDepth`, `pageSize`,
`asOfTime`, `sequencingOrder` and similar — and the user should be able to
override these **at the point of use**, per the explicit requirement: "the
user decides what they want at point of use," not what was baked in when
the query was saved.

**Mechanism (leaning toward, not yet decided):** invocation takes an
optional `overrides` dict, shallow-merged onto the stored body immediately
before the request is sent (`{**storedBody, **overrides}`). This needs no
per-query declaration of which fields are override-able — any top-level
body key can be overridden by a caller who chooses to. The risk (a caller
accidentally overriding something that was meant to be part of the fixed
filter logic, e.g. `metadataElementTypeName`) is a UI-level concern more
than a storage-level one — the query editor can visually distinguish
"filter conditions" fields from "execution parameters" fields even though
both live in the same stored JSON body, so a re-user of the query isn't
tempted to touch the wrong section. This is an **open decision** (§ below)
— the alternative is a per-query declared allowlist of override-able keys,
which is more explicit but requires the query author to think about it up
front rather than it being available by default.

**This isn't unique to Insights — the same override-at-point-of-use idea
extends to Local Dashboards.** If a dashboard widget's data source is a
saved query (§1.2 c), the widget itself may want its own override
properties (e.g. "this widget's copy always shows `graphQueryDepth: 2`
regardless of what the saved query's default is") — the override dict
travels with the *placement*, not just an ad hoc one-off invocation.
Also worth noting: pyegeria already has a **generic "execute report"
command that takes optional parameters** at call time — the same
override-dict shape this section proposes for saved queries is not a new
mechanism being invented from scratch, it's the same pattern that command
already establishes for `ReportSpec`/`FormatSet` execution, applied here
to queries specifically.

### 2.3 Storage location: a new `Query` element, related to `ResultsSet` — `ResultsSet.additionalProperties` is the short-term stopgap only

> **Naming trap (found building Track A, 2026-08-05):** the real Egeria
> entity type is spelled **`ResultsSet`** (with an "s"), confirmed live
> against qs-view-server's `/api/types` entity catalog — description:
> "Defines that a collection is a set of results from an activity, query,
> ...". pyegeria's `base_report_formats.py` FormatSet alias list spells it
> `ResultSet` (no "s"); that's a pyegeria-side alias typo, not an
> alternative real type — `createMetadataElementInStore` rejects
> `"ResultSet"` outright (`OMAG-COMMON-400-018`, "type name ... not
> recognized"). This doc now uses the real spelling throughout.

Egeria already has a `ResultsSet` type (`Collection` subtype, alongside
`RootCollection`/`Folder`/`RecentAccess`/`WorkItemList`) — but its name and
position in that family say "a collection whose members are the elements
a query *returned*," not "a place to store the query itself." Storing the
spec in `ResultsSet.additionalProperties` works mechanically but overloads
the type's own semantic — confirmed with the user this is understood and
deliberate as a **short-term workaround only**.

**Target design:** a new element type (name TBD — "Query", "SavedQuery",
"QuerySpecification" are candidates, not decided) holds the
`{url, httpMethod, body}` payload as its own properties, and a
**new, purpose-built relationship type** (expected — not a reuse of an
existing generic relationship) binds that `Query` element to a
`ResultsSet`, whose `CollectionMembership` holds the currently-materialized
results (re-run → diff membership → update). This cleanly separates "the
question" (`Query`) from "the answer" (`ResultsSet`), each in the
element/relationship shape Egeria already models this kind of thing with,
rather than conflating both into one overloaded type. The relationship's
exact name/properties still need real design work (§ Open Decisions) —
"new relationship type" is the expected shape, not yet the finished
design.

**Interim state (Track A, shipped 2026-08-05):** `ResultsSet` alone,
`additionalProperties` holding the query spec (as the literal
`{url, httpMethod, body}` JSON, per §2.1 — not a pyegeria-specific
shape, so nothing has to change when the real `Query` type exists,
just where the spec is read from), `CollectionMembership` used for
materialized results from day one. See the build notes below for what
else this surfaced.

This mirrors the same trajectory `Dashboard Sheet` already went through —
pyegeria-local model first, explicit plan to converge onto a real Egeria
Collection-family type later (`OVERVIEW_REPORTING_MODEL.md` §10.4's
`Collection Base` note). Worth watching for where these two efforts might
eventually meet — a Dashboard Sheet placement pointing at a `Query`-backed
result set is a natural pairing once both exist properly.

**Track A build notes (2026-08-05, live-verified against qs-view-server):**
- `CollectionManager.create_collection(body={...typeName: "ResultsSet",
  additionalProperties: {...}})` works exactly as designed — the additional
  properties round-trip losslessly through `get_collection_by_guid`/
  `find_collections`.
- Adding a materialized result to the ResultsSet's `CollectionMembership`
  needs `"class": "NewRelationshipRequestBody"` — pyegeria's own docstring
  examples for `add_to_collection` say `"RelationshipRequestBody"`, which
  the server rejects (`class` is a Pydantic `Literal`). A stale docstring,
  not a behavioral bug — one line to fix once found, not worth a
  `PYEGERIA_ISSUES.md` entry.
- **Deleting a saved query needs its members unlinked first.** Egeria's
  collection `cascade` delete only removes elements the collection *owns*
  (`isOwnAnchor`) — every real search result is independently anchored, so
  `delete_collection(guid, cascade=True)` still 403s
  (`OMAG-GENERIC-HANDLERS-403-005`, "still has a dependent ... element")
  until each `CollectionMembership` link is removed via
  `remove_from_collection` first. The shipped delete endpoint does this
  automatically; worth remembering for the eventual Dr.Egeria `Delete
  Query` command too.
- **Performance caveat, not yet addressed — and NOT fixed by Track B alone.**
  Materializing a 200-element result set takes ~20s live. It's important to
  be precise about *which* half of "run the query" this slowness is in,
  since it's easy to conflate the two:
  - **Finding the results** (the search itself) is already fast — real
    body-based paging (ISSUE-34's fix), and the upcoming combined-query
    method (§1.1, Track B) will mostly improve *correctness* here
    (relationship conditions move server-side) plus some speed on
    relationship-heavy queries.
  - **Writing the results into `CollectionMembership`** is the actual
    bottleneck, and it's a completely separate code path: one
    `add_to_collection` HTTP round-trip per result guid, because pyegeria
    has no bulk-membership endpoint. Track B's better search method doesn't
    touch this loop at all.
  So the real fix is Track C, not Track B: once `Query` is a first-class
  Egeria element with a relationship to its `ResultsSet`, the natural design
  has Egeria itself execute the query *and* populate membership server-side
  in one operation (most likely a governance action service) — eliminating
  our app's N-round-trip loop entirely, not just speeding it up. Until then,
  a cheaper interim mitigation (client-side concurrency on the
  `add_to_collection` loop) is possible but not yet done.

### 2.4 Lifecycle

Create / Update / Refresh / Delete over the query+result-set pair — a real
Dr.Egeria command family once the storage model is settled, same shape as
`Dashboard Sheet`'s (`md_processing/v2/dashboard_sheet.py` is the closest
existing template: local-store-backed processors subclassing
`AsyncBaseCommandProcessor`, overriding just the Egeria-touching
primitives). Not yet designed in command-attribute detail.

**Staleness UI:** viewing a saved query shows its last-materialized
results (from `CollectionMembership`) with a visible "as of \<time\>" badge
and an explicit refresh action — not a live re-run on every view. Agreed
as acceptable "as long as it's clear" — same staleness-badge convention
Overview's own time-machine/provenance UI already uses elsewhere in this
project, reused rather than inventing a new pattern.

### 2.5 Query editor investment (independent of the storage work)

Separately identified as needing real investment regardless of when saved
queries land: **searchable dropdowns for element types, classification
names, and relationship types** in the condition builder, replacing the
current free-text/plain-`<select>` inputs. The data for this already
exists (`/api/types`'s classification/relationship/entity catalogs, plus
`GET /api/insights/relationships`'s live-usage-count list already built
for the Relationship tree) — this is a UI-only improvement, doesn't depend
on the new combined-query method or the storage model, and can be picked
up independently.

### 2.6 Output shapes: not just tables

A saved query's *results* need to support the same range of output formats
`FormatSet`/`Format` already defines — DICT/LIST/TABLE/REPORT/MERMAID/HTML,
plus Vega-Lite charts — not just the tabular rendering Insights' search
page uses today. Which output shape makes sense is use-case dependent: an
ad hoc drill-down search (§1.2 a) wants a table; a query feeding a
dashboard tile (§1.2 c) likely wants a KPI/chart shape; a query embedded in
a generated report (§1.2 b) might want REPORT/HTML. Not every shape is
relevant to every use case, and this document isn't proposing that saved
queries pick or declare one shape up front — the same stored `{url,
httpMethod, body}` (§2.1) should be renderable through whichever `Format`
a given consumer pairs it with, same as any other `FormatSet.action`
result is today. No new mechanism needed here — this is a reminder to keep
the full output-format range in view when Track A/B build out rendering,
not just default to a table because that's what Insights' current UI does.

---

## Part 3 — Plan (phased, not yet started)

Two tracks that don't block each other:

**Track A — doesn't wait on the new combined-query method:**
- A.1: Query editor UX investment (§2.5) — searchable type-aheads for
  types/classifications/relationships.
- A.2: Save/load prototype using `ResultsSet.additionalProperties` (§2.3
  interim state) — store the literal `{url, httpMethod, body}` payload
  (§2.1) even while it's only ever `find_metadata_elements`-shaped, so
  nothing about the storage shape needs to change once the new method
  exists.
- A.3: `CollectionMembership`-based result materialization + the
  staleness/refresh UI (§2.4).
- A.4: "Saved Queries" as a third tab in Egeria Insights (browse/search
  over `ResultsSet`s, same pattern as any other `find_collections`-style
  browse), "open in builder" reusing the deep-link-seeding mechanism
  already built for `?type=&rel=`.
- A.5: functionality-selector brainstorm (§1.1) — scope which of
  `find_authored_elements`/`find_root_elements`/`find_elements_for_anchor*`
  deserve a dedicated simple form in the query editor, and design those
  forms; independent of the general-builder work.
- A.6 **(shipped 2026-08-05):** "Exclude types" condition — client-side
  post-filter (`exclude_types`), the interim workaround `PYEGERIA_ISSUES.md`
  ISSUE-46 names. Matches a result's `typeName` OR any `superTypeNames`
  entry, so excluding a base type (e.g. `Action`) drops every subtype
  (`ToDo`/`Meeting`/`Review`/`Notification`) at once. Applied before
  aggregates/relationship-annotation/sorting, so excluded elements are
  treated as never having been fetched, not just hidden at the last step.
  Persists through Track A save/load like any other spec field. Prompted
  by trying (and disproving, see ISSUE-45) whether Egeria's documented
  `metadataElementSubtypeNames` allow-list could do this server-side —
  confirmed live it has no effect at all, so this stays a client-side,
  fetched-page-only filter until Egeria ships real exclude semantics.

**Track B — depends on the new combined-query method landing. Improves
correctness and read-side speed, does NOT fix the materialization
performance caveat (see the Track A build notes above) — that needs C.1.**
- B.1: wire Insights to prefer the new method when a query's shape needs
  genuine N-way classification+relationship+value combination; keep using
  the narrower pairwise methods (§1.1's table) or `find_metadata_elements`
  where they already suffice.

**Track C — later, Egeria-native:**
- C.1: design + build the real `Query` element type + its relationship to
  `ResultsSet`, migrate off `additionalProperties`. **This is where the
  refresh-performance fix actually belongs** — Egeria executing the query
  and populating `CollectionMembership` server-side in one operation
  (likely a governance action service), eliminating the N-round-trip
  `add_to_collection` loop Track A's refresh currently does client-side.
- C.2: Dr.Egeria lifecycle commands (Create/Update/Refresh/Delete) for the
  real type.
- C.3: connect saved queries to the `FormatSet`/dashboard model (§1.2 b/c)
  — a saved query becomes a usable `ActionParameter` for a report spec /
  dashboard placement.

---

## Open decisions

- **Naming** for the new `Query`/`SavedQuery` element type — not decided.
- **Override mechanism** (§2.2): shallow-merge `overrides` dict at
  invocation time (simple, no per-query declaration) vs. a per-query
  declared allowlist of override-able body keys (more explicit, more
  authoring overhead). Leaning toward the former; not decided.
- **Relationship shape** between `Query` and `ResultsSet` (§2.3) — a new,
  purpose-built relationship type is expected (not reuse of an existing
  generic one), but its name/properties need the same kind of Egeria-side
  type design `Dashboard Sheet` went through — not scoped yet.
- **Functionality-selector UI** (§1.1 brainstorm) — which narrower methods
  (`find_authored_elements`, `find_root_elements`,
  `find_elements_for_anchor`/`_anchor_domain`/`_anchor_scope`) get a
  dedicated simple form vs. staying reachable only through the general
  builder, and what those forms look like — not designed.
- **Output-format selection at the point a query is consumed** (§2.6) —
  how a saved query's `{url, httpMethod, body}` gets paired with a
  `Format` (table/KPI/chart/report/etc.) per consumer — not designed, just
  flagged as a requirement to keep in view.
- **Whether `Query` needs to be a genuinely new Egeria type**, or can be
  modeled as another `Referenceable` with a classification (mirroring how
  `Dashboard Sheet`'s eventual `Collection Base` convergence was framed) —
  open, likely needs to be resolved alongside whatever Egeria-side design
  work produces the new combined-query method, since both are moving in
  the same timeframe.
- **How "which fields are filter conditions vs. execution parameters" is
  surfaced in the editor UI** (§2.2) — not yet designed at the UI level,
  only at the storage level (both live in the same JSON body regardless of
  the answer).
