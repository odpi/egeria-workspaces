<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Governing the Dashboard's Own Metrics: Glossary, Collections, and an Audit

Written 2026-08-01, raised as **NEXT-24** in `BACKLOG.md`. Prompted by a live
finding while investigating the Semantic Grounding drill-down (see §1.1) —
this document is the design + plan for fixing the underlying class of
problem, not just that one metric.

> **Status (2026-08-02): Phases A, B, and C are done.** All 12 tiles carry
> `summary`/`usage`; `gen_dashboard_glossary.py` exists and generates
> `OVERVIEW_ANALYTICS_GLOSSARY.dr-egeria.md` from `overview_specs.py`'s
> `_TILES` (Create/Update-idempotent — Terms already created get an Update
> pass, not a duplicate Create); it has been run and validated/processed
> against a live server (Glossary "Egeria Dashboard Analytics", RootCollection
> "Egeria Dashboard", 4 sub-collections, 12 Terms — all confirmed browsable in
> Egeria Explorer's Collections view via `/api/collections/roots` +
> `/{guid}/tree`). The `test_overview_specs.py` §2.6 guards are in (every
> tile must carry non-empty `summary`/`usage`; the generated `.dr-egeria.md`
> has its own `--check` staleness guard) — 373 checks total. The "ⓘ" info
> bubble is live on the dashboard, fetching `summary`/`usage` from
> `/api/overview/specs` (a click popover, not a hover tooltip — see Phase C
> notes below for why). §2's "exact command syntax to confirm" caveat is
> resolved: `Create Root Collection`/`Create Collection`/`Add Member to
> Collection`/`Create Glossary Term` all matched the design as written, no
> syntax surprises. Only **Phase D** (illustrative-tile usage notes +
> Topic/Perspective sub-collections) remains.

---

## Part 1 — Rationale

### 1.1 What triggered this

Drilling into "Semantic Grounding" (21% — `groundingLinks: 397`,
`SemanticAssignment` relationship count) to list *which Assets* have term
links surfaced a live-data finding, not a UI bug: of 397
`SemanticAssignment` relationships in this dataset, **348 (87.7%) connect
to `GovernanceActionProcess`** elements (subscription-workflow governance
automation — e.g. `"Create Subscription::WEEKLY-REFRESH-SUBSCRIPTION"`), not
data assets. The remainder are schema-level elements (`DataField`,
`TabularColumn`, `APIParameter`, ...) which aren't `Asset`-typed
themselves either. **Zero of the 397 relationships connect directly to an
`Asset`.** The tile's own label — "the meaning layer that grounds AI" /
"share of assets linked to glossary terms" — doesn't match what's actually
being counted.

This isn't a one-off. It's the general risk every metric on this dashboard
carries: a number can be technically well-computed and still measure
something different from what its label claims, and nobody finds out until
someone drills in far enough (as happened here, by accident, while
answering an unrelated question).

### 1.2 The existing precedent this builds on

Perspectives and Questions are **already real Egeria elements**, not just
Python data: `gen_perspectives.py` reads `PERSPECTIVES` out of
`egeria-overview.html` and generates `OVERVIEW_PERSPECTIVES.dr-egeria.md` —
a loadable Dr.Egeria document creating each Perspective and its Questions
(`GlossaryTerm`s classified `IsQuestion`) as real, queryable elements,
linked via `ScopedBy`. The KPI tiles themselves (`overview_specs.py`'s
`_TILES`) are the one piece of "what does this dashboard show" that never
got the same treatment — deliberately deferred to a later phase
(`OVERVIEW_REPORTING_MODEL.md`'s P3/P4). This document proposes doing for
metrics exactly what already exists for Perspectives/Questions, using the
same mechanism, not a new one.

### 1.3 Why generate, not hand-author

The direct risk in "add a Glossary of metric definitions" is the same
class of problem the section-provenance-badge fix (same day, see
`OVERVIEW_NEXT_STEPS.md` history) just solved: **two sources of truth that
silently drift**. Someone changes what a metric computes (as happened
today for grounding/lineage/aiReady) and forgets to update its Term.

The fix is the same pattern already proven for Perspectives/Questions:
`overview_specs.py` stays the single source of truth; a generator script
produces the Glossary/Term/Collection Dr.Egeria commands *from* it. The
Glossary becomes a generated downstream artifact, not a second thing to
maintain by hand — extending the exact drift-immunity
`test_overview_specs.py` already gives the tile↔frontend relationship one
hop further.

---

## Part 2 — Design

### 2.1 Richer tile schema — three fields, not one

Today's `description` field is a single-line UI sub-label. Egeria
`GlossaryTerm`s natively support `summary` / `description` / `usage` /
`abbreviation` / `examples` — use that shape properly instead of cramming
everything into one string. Add to each `_TILES` entry:

| Field | Maps to | Purpose |
|---|---|---|
| `summary` | Term `summary` | What the info bubble shows inline — one sentence |
| `description` | Term `description` | The fuller definition (today's field, kept) |
| `usage` | Term `usage` | Caveats, known scope mismatches, what it does NOT measure — **this is where the grounding finding lives**, structurally, not as a Python comment |

Example, applied to the `grounding` tile (illustrating what the audit
in §2.4 actually produces):

```python
{
    "key": "grounding", "label": "Semantic Grounding", ...,
    "summary": "Share of assets linked to glossary terms via SemanticAssignment.",
    "description": "Count and percentage of SemanticAssignment relationships, "
                    "as a proxy for the meaning layer that grounds AI context.",
    "usage": "CAVEAT (confirmed live 2026-08-01): SemanticAssignment is not "
             "Asset-scoped. In this dataset, 87.7% of SemanticAssignment "
             "relationships connect to GovernanceActionProcess elements "
             "(governance workflow automation), not data assets; the "
             "remainder connect to schema-level elements (DataField, "
             "TabularColumn, ...), not Assets directly. Zero connect to an "
             "Asset element directly. Treat this percentage as an upper "
             "bound on asset grounding, not a measured asset-grounding "
             "rate, until NEXT-24's audit resolves the scoping.",
}
```

### 2.2 Glossary + Collection structure

**Glossary**: one new Glossary, e.g. `"Egeria Dashboard Analytics"`, holding
one `GlossaryTerm` per metric (tile). Mirrors the existing `dr-egeria` help
Glossary's role — the canonical place someone (or an AI agent) looks up
"what does this number actually mean."

**Collections** — per your steering: a **RootCollection**, `"Egeria
Dashboard"`, with sub-collections underneath, taking advantage of Egeria's
multi-membership (one Term/metric can belong to several collections at
once, so this is additive, not a forced single categorization):

```
RootCollection: Egeria Dashboard
├── Overview KPIs                    (by dashboard app — today's only member;
│                                      future: Local Dashboards Analytics, etc.)
├── Live Metrics                     (by provenance — directly serves "what
├── Mixed Metrics                     am I really looking at")
├── Illustrative Metrics
```

Every metric Term is a member of exactly one **app** sub-collection
(`Overview KPIs` today) and exactly one **provenance** sub-collection
(computed from the tile's own `provenance` field — already exists, already
accurate per today's badge work). That's the v1 scope.

**Natural, cheap follow-ons** (not v1, but the multi-membership model makes
them additive later, not a restructure): sub-collections by **Topic**
(mirrors `TOPIC_KPIS` — "AI / Context Intelligence Metrics", "Security /
Privacy Metrics", ...) and by **Perspective** or **Section**. Since a Term
just gains an additional `Add Member to Collection` link, these can be
layered in incrementally once the base pattern is proven, without touching
anything already built.

This directly gives Egeria Explorer's Collections view (the "collections
without a parent" default I built earlier this session) a real, browsable
answer to "show me every metric this dashboard claims, grouped a few
different ways" — for anyone, not just Overview's own UI.

### 2.3 The generator script

`gen_dashboard_glossary.py`, mirroring `gen_perspectives.py` exactly:
reads `overview_specs._TILES` (not scraped HTML this time — the Python
registry is already the source of truth, no regex-scraping needed),
writes `OVERVIEW_ANALYTICS_GLOSSARY.dr-egeria.md`:

```
## Create Glossary          (once, "Egeria Dashboard Analytics")
## Create Root Collection   (once, "Egeria Dashboard")
## Create Collection        (x2 for v1: "Overview KPIs"; "Live Metrics" / 
                              "Mixed Metrics" / "Illustrative Metrics" x3)
--- per tile ---
## Create Term              (Display Name = label, Summary/Description/Usage
                              from §2.1's three fields, Qualified Name =
                              stable "Term::overview-kpi-<key>")
## Add Member to Collection (Term -> "Overview KPIs")
## Add Member to Collection (Term -> its provenance collection)
```

Idempotent by the same mechanism `gen_perspectives.py` already relies on
(`### Qualified Name` + `### Version Identifier`, Create→Update upsert) —
re-running after a tile's definition changes just updates the Term in
place.

**Exact command syntax to confirm before finalizing the script**: `Create
Root Collection` / `Create Collection` / `Add Member to Collection`'s
precise attribute names should be checked against the live compact command
specs (`validate_compact_specs`, or `dr_egeria --validate` against a small
hand-written probe file) before writing the generator — the shape above is
right conceptually, not verified letter-for-letter this session.

### 2.4 The audit itself

Scope by risk, not by tile count — prioritize tiles claiming to be `live`
today, since those are the ones a user reasonably trusts (illustrative
tiles aren't claiming reality yet, so there's nothing to correct, just
document as "not yet wired" in their `usage` field):

1. **`live`-tagged tiles first**: `assets`, `terms`, `governed`, `certs`,
   `products`, `exceptions`, `people`, `communities`, `isc`, `blueprints`,
   `grounding`, `ownership`. For each: does the numerator's actual
   population match what the label/denominator claims? (Exactly the check
   that caught grounding.)
2. **`mixed`-tagged tiles' live sub-parts** — same check, narrower scope.
3. **`illustrative`-tagged tiles** — no correction needed, just an honest
   `usage` note.

### 2.5 The info bubble

Once Terms exist, the info bubble is a small addition, not new
infrastructure: `/api/overview/specs` (already serves the tile registry,
already cached) is the natural place to also carry each tile's
`summary`/`usage` text directly — no separate live Egeria fetch needed at
dashboard-render time (the Term *is* generated from this same Python data,
so the Python data is already authoritative; fetching it back from Egeria
on every page load would be a slower, redundant round-trip of the same
content). The Glossary/Collection's value is discoverability and
governance (a real, browsable, queryable artifact other tools and Egeria
Explorer can find), not the live data path for the bubble itself.

Frontend: a small "ⓘ" affordance per KPI tile (`METRICS[k]` already has
`label`/`ico`/`color` — add `summary`/`usage`, rendered as a tooltip or a
small popover on click, not yet designed pixel-for-pixel — a quick mockup
pass before building is worth it, not scoped here).

### 2.6 Keeping this honest long-term

Extend `test_overview_specs.py`'s drift-guard philosophy: a check that
every `_TILES` entry has non-empty `summary`/`usage` fields (so a new tile
can't ship without them), and — once the generator exists — a check that
`OVERVIEW_ANALYTICS_GLOSSARY.dr-egeria.md` is not stale relative to
`_TILES` (same shape as the existing `OVERVIEW_METRICS.md` staleness check
`gen_overview_metrics.py --check` already does).

---

## Part 3 — Plan

### Phase A — Prove the pattern on a small slice (do this first, per 2026-08-01 discussion) — ✅ done

1. ✅ Add `summary`/`usage` fields to `_TILES` for **5 tiles**: `grounding`
   (the one with the real finding — do this one properly, it's the
   motivating case), `governed`, `ownership`, `assets`, `people`. Mix of
   simple/clean metrics and one with a genuine caveat, to prove the schema
   handles both.
2. ✅ Confirm exact Dr.Egeria command syntax for `Create Root Collection` /
   `Create Collection` / `Add Member to Collection` (validate against live
   compact specs before writing the generator).
3. ✅ Write `gen_dashboard_glossary.py` for just those 5 tiles + the
   Collection structure (§2.2, v1 scope: app + provenance sub-collections).
4. ✅ Run it, `--validate` then `--process` against a live server, confirm
   the Glossary/Collections/Terms actually land and are browsable in
   Egeria Explorer's Collections view.
5. ✅ Do NOT build the info bubble UI yet — confirm the data model first.

### Phase B — Complete the audit + generator for all `live`/`mixed` tiles — ✅ done

6. ✅ Extend `_TILES`' `summary`/`usage` fields to the remaining `live` tiles
   (`terms`, `certs`, `products`, `exceptions`, `communities`, `isc`,
   `blueprints` — all 12 tiles are `live` provenance today; no `mixed` tiles
   exist yet, so that half of §2.4's ordering didn't apply).
7. ✅ Regenerate the full Glossary/Collection doc; re-run against the live
   server.
8. ✅ Add the `test_overview_specs.py` guards from §2.6.

### Phase C — The info bubble UI — ✅ done

9. ✅ Design pass: a **click popover**, not a hover tooltip — usage notes run
   to several sentences, too long to read comfortably in a hover-triggered
   box that disappears if the cursor drifts. Popover is appended to
   `<body>` with fixed positioning (the `.kpi` tile has `overflow:hidden`
   for its sparkline, which would clip an absolutely-positioned child).
10. ✅ Wire `/api/overview/specs`' existing payload to carry `summary`/`usage`
    per tile (added to `_build()`'s `annotations` dict, alongside the
    existing `icon`/`color` pattern).
11. ✅ Build the frontend affordance, verified live. Fetched once per page
    load into a `TILE_INFO` JS object (not hand-duplicated into `METRICS`
    the way `label`/`icon` are — these are long free-text caveats, and a
    second hand-synced copy of paragraph-length text is a worse drift risk
    than the short fields `METRICS` already carries). Uses
    `stopImmediatePropagation` to avoid also triggering the tile's
    drill-down click handler, since the ⓘ button sits inside the same
    `data-drill`-bearing `.kpi` div.

### Phase D — Illustrative tiles + follow-on sub-collections

12. `usage` notes for `illustrative`-tagged tiles (lower urgency — see §2.4).
13. Topic/Perspective sub-collections (§2.2's "natural, cheap follow-ons") —
    additive `Add Member to Collection` links only, no restructuring.

### Sequencing notes

- Phase A is small and deliberately proves the riskiest new piece (the
  generator + Collection structure + live Egeria round-trip) before
  investing in the full audit or any UI work.
- Phase C (UI) is independent of Phase B's audit completeness — the info
  bubble mechanism can be built once Phase A's pattern is proven, then
  just picks up more tiles as Phase B fills them in.
- Phase D is explicitly lowest priority — nice-to-have breadth, not
  blocking anything.
