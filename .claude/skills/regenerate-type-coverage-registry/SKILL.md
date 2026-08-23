---
name: regenerate-type-coverage-registry
description: Regenerate portal-docs/Internals/type-coverage-gap-analysis.md — a gap analysis of PyegeriaWebHandler's Egeria type coverage against the full Egeria v6 type system, with a curated, re-verified priority list of real feature gaps. Use when asked to refresh/update/regenerate the Type Coverage Registry, or periodically (it goes stale as features ship).
---

# Regenerate the Type Coverage Registry

Produces `portal-docs/Internals/type-coverage-gap-analysis.md`: a mechanical
diff of every Egeria v6 type against what `PyegeriaWebHandler` actually
references, plus a hand-curated, individually-re-verified list of real
feature gaps ranked by value. First built 2026-07-15, regenerated fresh
2026-08-19 after going stale (several "open" gaps had quietly been built).

## 0. Locate the two things this diffs

- **The type source**: `OpenMetadataType.java` in the local `odpi/egeria`
  checkout — find it with `find <egeria-checkout-root> -iname
  OpenMetadataType.java`. On this machine that's
  `~/localGit/egeria-v6/egeria/open-metadata-implementation/frameworks/open-metadata-framework/src/main/java/org/odpi/openmetadata/frameworks/openmetadata/types/OpenMetadataType.java`
  — confirm it still exists there before assuming the path; the local
  checkout can move.
- **The scan target**: `compose-configs/egeria-quickstart/PyegeriaWebHandler/*.py`
  and `*.html` in `egeria-workspaces-fs`. Quickstart only, matching the
  original's scope — freshstart shares most of the same handler code via
  the divergent-copy pattern (see project memory `share_codebase`), so
  scanning quickstart is representative.

## 1. Extract types, classified by Area

Each enum entry in `OpenMetadataType.java` looks like:

```java
GOVERNANCE_METRIC("9ada8e7b-...",
                  "GovernanceMetric",
                  OpenMetadataWikiPages.MODEL_0450_GOVERNANCE_ROLLOUT,
                  ...
```

Extract the type name (2nd string literal) and classify its Area from the
model number's **second digit** — `MODEL_0450` → Area 4, `MODEL_0010` →
Area 0, `MODEL_0135` → Area 1. (Not the first digit — every model number
starts with `0`.) A regex like
`[A-Z][A-Z0-9_]*\(\s*"[0-9a-f-]{36}",\s*\n\s*"([A-Za-z0-9]+)",\s*\n\s*OpenMetadataWikiPages\.MODEL_(\d{4})`
across the whole file works; expect ~620-625 matches, close to but not
necessarily exactly matching the previous run's count (the type model
itself grows between Egeria releases — a count that moved slightly since
last time is expected, not a bug in the extraction).

Area labels (fixed, from Egeria's own model organization):
0 = Basic definitions & Infrastructure, 1 = Collaboration, 2 = Assets,
3 = Glossary, 4 = Governance, 5 = Schemas, 6 = Metadata Surveys,
7 = Lineage & Usage.

## 2. Scan for presence — and mind the self-scan trap

For each type name, whole-word-match it (word boundaries, not substring —
`SecurityRole` shouldn't match inside `SecurityRoleAppointment`) across
every `.py`/`.html` file in `PyegeriaWebHandler`.

**The gotcha that actually bit the first regeneration**: the report file
itself, `type-coverage-gap-analysis.html` (if an old HTML version still
exists) or wherever the previous markdown version lives, lists every
"missing" type name in its own raw-diff appendix. Scanning it alongside
the real handlers makes almost everything look "covered" — one run hit
616/622 "referenced" this way, an obviously-wrong number that only made
sense once the report was excluded from its own scan (true number: 281/622
that same run). **Always exclude the report's own current and previous
output files from the scan glob.**

Also be honest in the doc about what this mechanical pass does *not* do:
the original 2026-07-15 version was a genuine manual per-handler read that
filtered out internal relationship plumbing, abstract base types, and
auto-riding subtypes ("checked for which Egeria types it actually queries
or renders"). A pure text scan has no such filter — a type name mentioned
only in a comment or a docstring explaining why something is *out* of
scope counts as "present." State this plainly in the regenerated doc's
Method section so the raw percentage isn't read as more precise than it
is; it's an upper bound on real coverage, not a count.

## 3. Re-verify the curated gap list item by item — don't just carry it forward

The mechanical raw diff is reference material; the curated "highest
value" / "high value" / "worth planning" / "niche" tiered list is the
part worth someone's time, and it's also the part that goes stale fastest.
For **every** item in the previous version's curated list, re-check
against current code rather than trusting its last-recorded status:

- Search for the type names it lists across `PyegeriaWebHandler` — a
  zero-hit item is still genuinely open; any hits mean investigate further
  (a passing mention in a comment is not coverage — check the surrounding
  code actually queries/renders it, e.g. via a dedicated `_handler.py` file
  or a registered route/router).
- Check `pyegeria_handler.py`'s `app.include_router(...)` calls for a
  router name matching the gap's feature area — a router that now exists
  where the old report said "zero references" means it's been built since.
- `git log --follow -- <handler_file>` on any newly-found handler file
  confirms roughly when it landed, useful for the "Built since" section's
  narrative.

Move anything now-covered into a "Built since [previous date]" section
with a one-line note on where it landed (which handler, which router).
Keep genuinely-still-open items in their tier, but re-word them against
current code rather than copying old prose verbatim — check whether the
specific detail (e.g. "zero references anywhere") is still accurate.

## 4. Write the doc and wire it in

Write to `portal-docs/Internals/type-coverage-gap-analysis.md` (create the
`Internals/` folder if this is the first regeneration in markdown form).
Follow `portal-docs/contributing.md`'s three-step process for any doc
that's new or has never been wired in:

1. The `.md` file itself, in the right subdirectory.
2. A card in `portal-docs/index.html` (check the "For maintainers" section
   — that's where this doc's card lives; no `card-tag` needed there,
   matching the existing `contributing.md` card).
3. A breadcrumb label in `portal-docs/viewer.html`'s `_LABELS` dict —
   optional in practice (there's a title-case fallback), but add one for
   any slug where the fallback would look wrong.

No deploy/reload step needed — `portal-docs/` is bind-mounted straight
into Apache; changes to `.md`/`.html` files there take effect immediately.
Verify live with `curl -sk https://localhost:8843/docs/` if the quickstart
stack is up (check `docker ps` first — it may not be, this isn't always
running); if it's down, source-review is the fallback, same as any other
portal-docs edit.

## 5. Report honestly

State the total types/referenced/gaps-tracked numbers, and explicitly
flag anything moved from "open" to "built since" with where it landed.
If the type count or referenced count moved by more than a handful from
the last run for a reason other than genuine new coverage (e.g. Egeria's
own type model grew), say so — don't let a bare number comparison imply
more regression or progress than actually happened.
