<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Popularity and usage measures: Overview tiles, analytic functions and report specs — design note

**Status:** draft for review (2026-10-23). Nothing here is built yet except step 1 (PR #682, below).
It frames the work across the portal (`egeria-workspaces`) and pyegeria (`egeria-python`) before any
pyegeria code is written. Builds on:

- `design-docs/analytic-functions-and-metrics.md` (PR #603, open) — the contract for an analytic function
  callable from a report spec, and the Governance Metrics panel.
- `compose-configs/egeria-quickstart/PyegeriaWebHandler/OVERVIEW_REPORTING_MODEL.md` — tiles as pyegeria
  `FormatSet` report specs, placed in a `Container`; "extend `FormatSet`, don't build a parallel registry".

> **Evidence tags.** *[verified]* = run against the laz quickstart this session. *[read]* = read in code or
> docs. *[inferred]* = not checked.

## 1. The question

Egeria now records how its metadata is used. Can the portal show that, as Overview measures, and expose the
same measures as documented analytic functions and report specs, so users can build their own dashboards
from them?

It started with a report from Mandy's platform: the portal showed only the `*CountTotal` values of a
collection's `MemberPopularityProfile`, not the per-member maps.

## 2. What Egeria provides

| Where | Classification | Written by | Content |
|---|---|---|---|
| Each element | `UsageActivity` | Pepys Activity Observer (nanny daemon) | Seven counts: `explicitGetCount`, `findCount`, `updatePropertyCount`, `updateAttachmentCount`, `updateFeedbackCount`, `deleteAttachmentCount`, `deleteFeedbackCount` *[read]* |
| Root collections, glossaries, data sharing hubs, collection folders, digital product catalogs | `MemberPopularityProfile` | Lovelace "Build Member Popularity Profile" (Babbage Analytical Engine) | For each of the seven counts, a `…Total` and a `…Profile` map of **member element GUID → count**. Nested collections roll up, so totals ripple to the top. Members with no activity are left out; a map is omitted when every member is zero *[read]* |
| Governance zones | `ZoneMembershipProfile` | Lovelace "Build Zone Membership Profile" | Member counts by type: direct, anchored, combined *[read]* |
| People | `ContributionRecord` | Lovelace "Award Karma Points" | Karma points (already used by `karma_leaderboard`) *[read]* |

Points that shape the design:

- **The map keys are elements, not people.** "Member" means a collection member. The profile answers "which
  parts of this collection get used", not "who uses it". *[read]*
- **Pepys counts only people and external tools** since odpi/egeria #9375 (in the build laz runs since
  2026-10-22). Before that, most counts came from Egeria's own servers and engines. Counts collected
  before that build mean something different from counts collected after it. *[read]*
- **Counts are cumulative**, with no time stamps per count. A trend needs snapshots: `asOfTime` reads, as
  `growth_series` and `metric_trend` already do. *[inferred: whether asOfTime returns earlier classification
  values for these elements has not been checked]*
- **On laz today every profile is zero.** 12 of the 32 Coco collections carry a `MemberPopularityProfile`, all
  with zero totals and therefore no maps. *[verified]* Demo data will need real browsing first.

## 3. What the portal shows today

- **Detail pages:** classification properties are shown generically. Map-valued properties were dropped by
  every flattener, so only the totals appeared. **PR #682** keeps the maps and renders them with member GUIDs
  resolved to display names (Explorer, The Catalog, Data Mesh, Resource Browser). *[verified by unit and
  harness tests; not yet against real counts]*
- **Overview:** the "Popularity / Usage" topic filter exists, but its tiles (products, ISCs, blueprints,
  people, communities) are counts of definitions, not usage. `overview_specs.py` says so itself: "Counts product
  DEFINITIONS, not adoption -- no rating/usage signal is wired." *[read]*
- **Resource Browser home:** has a "Popular" panel that always reports "Popularity is not available yet". The
  backend hard-codes `available: False` with the reason "Egeria holds no usage measure for these resources",
  which is no longer true now that `UsageActivity` exists. *[read: `resource_browser_handler.py` `/api/resource-browser/home`]*
- **pyegeria:** 23 analytic functions; none reads `UsageActivity` or `MemberPopularityProfile`. Nearest
  neighbours: `karma_leaderboard`, `active_contributors`, `engagement_series`, `stale_assets`,
  `metric_trend`. *[verified: registry listed from pyegeria 6.2.9]*

## 4. Proposed measures

Each measure is one analytic function in pyegeria, one demo report spec, and (where it earns a place) an
Overview tile. Names are proposals.

| # | Measure | Question it answers | Source | Tile? |
|---|---|---|---|---|
| M1 | `collection_popularity` | Which collections, glossaries and catalogs get used most, and for what (read / find / update / feedback)? | `MemberPopularityProfile` totals | Yes: top-N bar, split by activity kind |
| M2 | `member_hotspots` | Within one collection, which members get the attention? | One collection's `…Profile` maps, names resolved | Drill-down from M1, not a tile |
| M3 | `element_usage` | Which individual elements are used most (or not at all), optionally by type? | `UsageActivity` | Yes: top-N list, and an "unused" count |
| M4 | `usage_mix` | What kind of use dominates: looking, finding, updating, giving feedback? | Sum of the seven totals over a scope | Yes: one stacked bar |
| M5 | `unused_but_governed` | Which governed or approved elements has nobody looked at? | `UsageActivity` absent or zero, joined with governance classifications | Candidate, pairs with `stale_assets` and `orphan_glossary_terms` |
| M6 | `usage_trend` | Is use growing? | M1 or M3 over `asOfTime` snapshots, via `metric_trend` | Later; depends on the asOfTime check in §2 |

Not proposed: anything that ranks **people** by usage. The data doesn't support it (the keys are elements), and
karma points already cover contribution.

## 5. Honest-data rules these measures must follow

These follow the Overview's existing no-sample / None-not-0 rules.

1. **"Not measured" is not "zero".** An element with no `UsageActivity`, or a collection with no
   `MemberPopularityProfile`, has not been measured. It must not be counted as unused. M3 and M5 need three
   states: used, measured-and-unused, not measured.
2. **Say when the profiler last ran.** A profile is only rewritten when counts change, so its `updateTime` is not
   a "last analysed" time. Each tile should show the Babbage/Lovelace run time, or say it is unknown.
3. **Mark the Pepys change.** Counts from before odpi/egeria #9375 include Egeria's own activity. A deployment
   upgraded across it has mixed counts until they are reset. The tile description should say so.
4. **Resolve names, keep GUIDs.** Every list shows display names, with the GUID available, as PR #682 does.

## 6. Where the code goes

| Piece | Repo | Notes |
|---|---|---|
| Analytic functions M1–M6 | `egeria-python` (`pyegeria.view`) | Registered in `analytic_registry`, each with `description`, `params`, `returns`, `resource_types`, `tags` |
| Demo report specs, one per function | `egeria-python` (`analytic_demo_specs`) | Appear automatically in Explorer's Report Specs browser |
| Overview tiles | `egeria-workspaces` (`overview_specs.py`, `egeria-overview.html`) | Under the existing Popularity / Usage topic; drift-guarded by `test_overview_specs.py` |
| Glossary entries | `egeria-workspaces` (`OVERVIEW_ANALYTICS_GLOSSARY.dr-egeria.md` via `gen_dashboard_glossary.py`) | So each measure is documented where users browse metrics |
| Resource Browser "Popular" panel | `egeria-workspaces` | Fill from M3, which removes the hard-coded "not available yet" |

The pyegeria work should be coordinated with the pyegeria session, which owns releases.

## 7. Decisions needed

1. **Scope of the first release:** M1 + M3 + M4 (the tiles), or all six?
2. **Read path for M3 and M5:** these need `UsageActivity` across many elements. Is there a classification-scoped
   find that returns only classified elements, or does this need a new pyegeria call? The repository is large
   (about 620k current entities, 2026-10-22), so a full scan is not acceptable for a tile.
3. **Pre-#9375 counts:** reset them on deployments that upgraded across the change, or only label them?
4. **Report spec authoring:** keep the demo specs hand-written in pyegeria, or author them through Dr.Egeria?
   This is the same open question as #603.

## 8. Suggested next steps

1. Merge PR #682, then check it against an element with real counts (Mandy's `coco-data-hub`, or laz after some
   browsing and a profiler run).
2. Answer decision 2 with a read-only probe: time a classification-scoped read of `UsageActivity` on laz.
3. Write M1 and M4 in pyegeria (they read only `MemberPopularityProfile` on a bounded set of collections), with
   demo report specs, and release.
4. Add the M1 and M4 tiles and glossary entries to the Overview.
5. Then M3, M5 and the Resource Browser panel, depending on decision 2. M6 last.

----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
