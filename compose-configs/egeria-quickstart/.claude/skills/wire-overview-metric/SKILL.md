---
name: wire-overview-metric
description: Take a still-sample/placeholder metric on the Egeria Overview dashboard (a "Remaining app wiring" item in PyegeriaWebHandler/OVERVIEW_NEXT_STEPS.md) and wire it to real live data. Use whenever the user asks to wire up a specific Overview tile/panel, work through the next item on OVERVIEW_NEXT_STEPS.md's remaining-wiring list, or replace a hardcoded/sample number on the Overview dashboard with something real. Covers the exact multi-file sequence (pyegeria metric function, overview_handler.py, overview_specs.py, egeria-overview.html's several live-data touch points, freshstart mirror, NEXT_STEPS.md) so nothing gets missed.
---

# Wiring a real metric into the Egeria Overview dashboard

Every "Still ⚪ sample" / "Remaining app wiring" item in
`compose-configs/egeria-quickstart/PyegeriaWebHandler/OVERVIEW_NEXT_STEPS.md`
follows the same shape once it's actually done. Missing any one of the
frontend touch points below is how a metric ends up "live" in the API but
still showing `(sample)` or a stale placeholder in the browser.

## 0. Investigate before writing code

Don't guess at what's cheaply queryable. Spawn an Explore agent (or do it
inline) to answer, grounded in what's actually real:
- What does the existing tile/section currently compute (if anything) —
  read the relevant `overview_specs.py` tile dict and/or
  `overview_handler.py` endpoint function.
- What Egeria concept does this metric actually map to — check
  `digital_products_handler.py`, `pyegeria/omvs/*.py`, and the live server
  directly (a throwaway script against `MetadataExpert`/
  `ClassificationExplorer`) rather than assuming a property/relationship
  name exists.
- Is there a cheap **native count** path (`count_elements`,
  `count_relationships`, or a `searchProperties` EQ condition on
  `count_metadata_elements` — see `count_elements_by_property` in
  `overview_metrics.py` for the pattern) or does it genuinely need a
  traversal? A metric that looks traversal-blocked often has a
  single-relationship-type proxy instead (see `contextualised_coverage`'s
  own docstring for a worked example: `ImplementedBy` relationships,
  filtered and deduped, instead of walking every asset) — check relationship
  types connecting the two element types before assuming a full graph walk
  is required.
- If it's a **proxy**, not the literal metric, that's fine — this
  dashboard's established convention is honest proxies with a documented
  caveat, not fake precision. If nothing cheap exists at all, the
  established convention is to leave it `None` with a documented reason
  (see `context_readiness_funnel`'s `aiReady` field) rather than compute it
  expensively or fake it.

## 1. New function in pyegeria's overview_metrics.py

Add the function to `/Users/dwolfson/localGit/egeria-python/pyegeria/view/overview_metrics.py`,
matching the existing style: docstring explaining what's real vs. proxy,
`try/except` around any relationship/find call (never raises), returns a
plain dict. Add it to `__all__`. See the `live-patch-pyegeria-container`
skill for validating and live-testing this function before it's in a
release.

## 2. Wire into overview_handler.py

- Defensive import (the new function isn't in a published pyegeria release
  yet) — copy the exact pattern already used for `ownership_coverage` /
  `count_elements_by_property` in this file.
- Call it from the relevant endpoint function, add the new field(s) to the
  returned payload dict.

## 3. Update overview_specs.py (if it's a `_TILES` entry)

Not every metric is a `_TILES` entry (e.g. Usage Context is its own
section, not a KPI tile) — check whether the metric has a dict in `_TILES`
first. If it does, update `description`/`summary`/`usage` to describe the
real computation instead of the old placeholder text.

## 4. Frontend — egeria-overview.html, all the touch points

This is the step most likely to be incomplete. Grep for the metric's field
name (e.g. `contextualisedPct`) and check **every** hit, not just the first:

- The tile card definition (`METRICS.<key>` or similar) — the value getter.
- **Every `SECTION_VARIANTS` copy**, if the containing section has
  perspective-specific variants (e.g. Usage Context has a default + two
  named variants) — the same static markup block is duplicated per variant;
  editing only the default copy leaves the others showing stale sample
  text. `grep -c` the metric's DOM id to see how many copies exist before
  declaring the frontend done.
- Any `(sample)` / `illustrative` label spans next to the value — remove
  once it's live.
- The live-apply function (`applyUsage`/`applyPeople`/etc.) — does it write
  the new field into `store.*` as well as calling `setTxt`/`setText`? A
  field only set via `setTxt` (DOM write) but never written to `store.*`
  won't survive a perspective/variant switch, which re-renders from
  `store.*`.
- The variant-switch re-apply block (search for where `SECTION_VARIANTS` are
  swapped into the DOM) — does it re-apply this field from `LIVE.*` after a
  swap? A field newly added here needs an explicit line, same shape as the
  existing `isc`/`blueprints` reapply.
- `drillLivePatch()`, if the metric has a drill-down/detail panel — overlay
  the live value onto `d.stats[n]`/`d.list`, following the existing
  per-key `if (key === '...')` blocks. Replace fake sample list rows
  outright rather than appending real rows to them.
- The status registry (`{ name: '...', status: 'illustrative' }` list) —
  flip to `'live'`.

## 5. Mirror to egeria-freshstart

`compose-configs/egeria-freshstart/PyegeriaWebHandler/` has its own copies
of `overview_handler.py`/`overview_specs.py`/`egeria-overview.html`, already
independently drifted from quickstart's (check with `diff` against the
quickstart pre-edit committed version before assuming identical context —
don't blind-copy). Apply the same logical edits around the existing drift,
not on top of it. freshstart's container usually isn't running — this copy
stays source-only, untested live, and that's expected; say so plainly
rather than implying it was verified.

## 6. Live-verify (quickstart only)

Deploy per `deploy-pyegeria-webhandler` (app files) and
`live-patch-pyegeria-container` (the pyegeria function) together — the
`overview_handler.py` deploy's reload picks up both. Then:
```bash
curl -sk "https://localhost:8843/api/overview/<endpoint>?server=qs-view-server&user_id=erinoverview" | python3 -m json.tool
```
Confirm the new field(s) are non-placeholder and match what the
investigation step predicted. Diff-confirm every deployed file.

## 7. Update OVERVIEW_NEXT_STEPS.md

Mark the item done with what was actually verified (real numbers, not just
"wired"). If it turned out to be a proxy rather than the literal metric,
say so here too, matching the frontend's honesty. Check the "Still ⚪
sample" summary line near the top of the file — it independently lists the
same items and goes stale if only the detailed bullet below is updated.

## 8. Commit both repos, don't push without asking

`pyegeria/view/overview_metrics.py` commits in `egeria-python` (use `git
commit -s`, that repo's own convention). The `PyegeriaWebHandler` +
`OVERVIEW_NEXT_STEPS.md` changes commit in `egeria-workspaces-fs` (heredoc
commit message with `Signed-off-by` + `Co-Authored-By` trailers, per that
repo's `CLAUDE.md`). Check `git fetch` + compare against `origin` before
either commit — this repo has had commits land on the wrong branch or get
concurrently pushed by another session before. Push only when asked.
