# Query

Query is the Portal's cross-cutting governance search tool: build a faceted query against any element type's properties and classifications, run it, and optionally save it as a real Egeria `SavedQuery` element for reuse. Renamed from "Egeria Insights" to "Query" in the UI (2026-08-14) — the route and this doc's filename kept the old name for compatibility with existing bookmarks.

Access it from the portal tile (🧭 Query) or directly at `/egeria-insights`.

---

## Dashboard tab

An overview of governance-classification coverage across the catalog — counts and breakdowns for confidentiality, criticality, severity, and similar ordinal classification levels, populated live from Egeria's type system rather than hardcoded.

---

## Query tab

Build a query from a facet picker (populated live from `/api/types`, so it always reflects whatever classifications and properties actually exist on your server) plus an operator (`=`, `≠`, `>`, `≥`, `<`, `≤`, and set-membership operators) and a value. Ordinal fields — confidentiality, criticality, severity, retention basis — get numeric operators and a valid-values lookup for human-readable labels instead of raw numbers.

---

## Saved Queries tab

Queries you save here persist as real Egeria `SavedQuery` elements (previously modeled as a generic `ResultsSet` before Egeria added a dedicated type) — not local-only Portal state. A saved query with `CollectionMembership` results shows a staleness indicator if the underlying data has changed since it was last materialized.

---

## Further resources

- [Egeria Explorer](egeria-explorer.md) — for browsing a specific element's full detail once Query has found it
- [Egeria Audit](egeria-audit.md) — governance-zone-aware detail views for the same classification-level data Query's Dashboard tab summarizes
