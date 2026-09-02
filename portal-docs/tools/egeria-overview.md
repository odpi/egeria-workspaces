# Egeria Overview

Egeria Overview is the executive / at-a-glance dashboard for the portal: scale, governance coverage, quality, AI-readiness, usage context, and the people/community behind the metadata — every number tied to a business-value lens and a drill-through into the tool that owns it. Where the other tools are task-oriented drill-down views, Egeria Overview is the one screen that answers "how are we doing, and is it improving?"

Access it from the portal tile (📊 Egeria Overview) or directly at `/egeria-overview`.

---

## Perspective and Topic

Two independent selector strips sit above the KPI band:

- **Perspective** — *who's looking* (10: Governance, Steward, Data Owner, Consumer, Engineering, Architecture, Security, App/AI Builder, Privacy, Community — reconciled against Resource Explorer's own real Egeria `Perspective` elements, not a portal-specific list). Reconfigures the whole page: which sections show, in what order, which KPI tiles, and the question set.
- **Topic** — *what domain of concern* (Any, AI/Context Intelligence, Security/Privacy, Quality, Popularity/Usage), independent of Perspective. Both narrow the KPI band and section visibility; selecting both filters to their intersection, falling back to the Topic-only view if the intersection would otherwise be empty.

Each Perspective is a real Egeria `Perspective` element, linked via `ScopedBy` to its own set of `Question` glossary terms — not portal-hardcoded copy. Browse them directly in [Egeria Explorer's Perspectives & Questions tab](egeria-explorer.md).

---

## KPI tiles and the "ⓘ" info bubble

Every KPI tile carries a summary of what it actually measures, plus usage notes covering known scoping caveats — click the small "ⓘ" on a tile to open it. This is the same content that generates the "Egeria Dashboard Analytics" Glossary (one GlossaryTerm per tile, browsable under the "Egeria Dashboard" RootCollection in [Egeria Explorer's Collections view](egeria-explorer.md)) — the dashboard isn't the only place this documentation lives, it's just the most convenient one to read it from while looking at the number itself.

Some caveats are more than cosmetic: for example, "Semantic Grounding" counts `SemanticAssignment` relationships as a proxy for AI-readiness, but in a typical dataset most of those relationships connect to governance-automation elements rather than data assets — read the tile's usage notes before treating a percentage as a literal "share of assets."

---

## Time machine and growth trends

An "as of `<date>`" picker re-queries the entire dashboard at any past date via Egeria's native bitemporal `asOfTime`; **Compare to now** shows real now-vs-then deltas on every tile. The Growth & Trends chart plots real snapshots over a selectable window (8 hours to 1 year).

---

## Data-source badges

Every section carries a provenance badge: ● live (queried from Egeria now), ◐ mixed (some live, some illustrative), or ○ illustrative (sample data, not yet wired to a live query). A badge is computed from the section's actual sub-items, not hand-maintained text, so it can't silently drift out of sync with what's really live.

---

## Further resources

- [Egeria Explorer](egeria-explorer.md) — browse the "Egeria Dashboard Analytics" Glossary and "Egeria Dashboard" RootCollection that the info bubbles are generated from
- [Egeria Audit](egeria-audit.md) — full detail views for the exceptions/certifications tiles' underlying elements
