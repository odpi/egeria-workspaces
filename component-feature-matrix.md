# Component Feature Matrix — Classifications / Raw JSON / Relationships

Tracks, per Detail view/component across the portal apps, which of the
"every element gets this generically" features are wired up:

- **Classifications** — foldable `Collapsible` section (closed by default),
  rendered only when the element actually has classifications (empty →
  nothing rendered). Shared implementation: `ClassificationsAndRawJson`
  (`static/egeria-shared-ui.js`). Data comes from `elementHeader` — see
  `common_serialize.py`'s `_classifications()` (AssetCatalog/GlossaryManager
  JSON shape) / `_classifications_from_metadata_expert()` (MetadataExpert raw
  shape) on the backend, or `_classificationsFromHeader()` in
  `egeria-shared-ui.js` for call sites that only have a raw `elementHeader`
  client-side (e.g. Audit).
- **Raw JSON** — the "Copy raw JSON (debug)" affordance (`RawJsonViewer`),
  bundled into `ClassificationsAndRawJson`. Copies `{fetch_method, raw}` —
  `fetch_method` names the actual pyegeria call that produced the payload
  (from `/api/debug/raw/{guid}`, `tech_catalog_handler.py`).
- **Relationships** — generic foldable relationship sections, one per
  backend-returned key, via `RelationshipSection`/`GenericRelationshipsSection`
  + `onNavigateToElement` cross-link dispatch (`type-explorer.html`).

Quickstart and freshstart (`compose-configs/egeria-{quickstart,freshstart}/PyegeriaWebHandler/`)
share the same file names and are kept in sync line-for-line except where a
component genuinely doesn't exist in one env (noted below). Rows apply to
both unless flagged otherwise.

**Keep this updated** whenever a Detail view is added, or a gap here is
closed — that's the whole point of tracking it instead of re-discovering it
each time.

## Egeria Explorer (`type-explorer.html`)

| Component | Classifications | Raw JSON | Notes |
|---|---|---|---|
| ReferenceDataDetail | ✅ | ✅ | via `ClassificationsAndRawJson` |
| ExternalReferenceDetail | ✅ | ✅ | quickstart only — no freshstart equivalent |
| ExternalIdentifierDetail | ✅ | ✅ | quickstart only |
| AgreementDetail | ✅ | ✅ | quickstart only |
| DigitalProductDetail | ✅ | ✅ | |
| ValidValueDetail | ✅ | ✅ | |
| SolutionBlueprintDetail | ✅ | ✅ | |
| SolutionComponentDetail | ✅ | ✅ | |
| ISCDetail | ✅ | ✅ | |
| LocationDetail | ✅ | ✅ | |
| ActorDetail | ✅ | ✅ | Also: synthetic `communities` relationship key added 2026-07-22 (see `actor_handler.py`'s `_enrich_person_communities`) — resolves the `Person→performsRoles→"Community Member" role→assignmentScope→Community` 2-hop chain that `graph_query_depth=1` doesn't reach on its own. Cross-links via the existing `Community`/actor-kind entries in `_elementIsLinkable`/`onNavigateToElement` — no new frontend plumbing needed. |
| CommunityDetail | ✅ | ✅ | Member actors surface via generic `assignedActors` relationship key (points to the "Community Member" `PersonRole`, itself cross-linkable) |
| InformalTagDetail | ✅ | ✅ | |
| ActionDetail | ✅ | ✅ | |
| BusinessCapabilityDetail | ✅ | ✅ | |
| NoteLogDetail | ✅ | ✅ | |
| GovDefDetail | ✅ | ✅ | |
| ProjectDetail | ✅ (fixed 2026-07-22) | ✅ (bare `RawJsonViewer`, not the shared bundle) | Has its own richer per-kind color-coded classification badges (`ProjectKindBadge`) shown always-visible at the top — kept as-is (genuinely useful summary). The properties-table "Classification Details" section below was previously always-open; now wrapped in `Collapsible`/`defaultOpen:false` for consistency with every other view. |
| TypeDetail / ClassifDetail / RelDetail / ReportSpecDetail | N/A | N/A | Type-system / report-spec definitions, not element instances — no `elementHeader`/classifications concept applies |

## Tech Catalog (`tech-catalog.html`)

| Component | Classifications | Raw JSON | Notes |
|---|---|---|---|
| Asset detail pane (main render) | ✅ (fixed 2026-07-22) | ✅ | Was a hand-duplicated copy of the shared markup; now calls `ClassificationsAndRawJson` directly |
| `SchemaRow` (schema-tree nodes: RelationalTable/Column, etc.) | ⚠️ own inline impl | ❌ | Renders its own `FoldTriangle` + classification-card markup — a third, separate implementation. Table-row context (not a full detail panel) so a straight swap-in isn't 1:1, but worth revisiting if it drifts further from the shared styling. Not yet fixed. |

## Egeria Audit (`egeria-audit.html`)

| Component | Classifications | Raw JSON | Notes |
|---|---|---|---|
| `ElementPropertiesPane` (Exceptions / Certifications / Licenses tabs, end1 + end2) | ✅ (added 2026-07-22) | ✅ (added 2026-07-22) | Backend (`audit_handler.py`'s `get_audit_element`, `ClassificationExplorer.get_element_by_guid` at depth 0) already returned the full raw `elementHeader` with classification keys — just wasn't being extracted client-side. Added `_classificationsFromHeader()` (JS port of `common_serialize._classifications`) in `egeria-shared-ui.js` and wired it + `ClassificationsAndRawJson` into `ElementPropertiesPane`. One shared component feeds all three tabs, so this covers all of them. Verified live: a Confidentiality-classified element now surfaces via `/api/audit/element/{guid}`. |

## Egeria Operations (`egeria-operations.html`)

| Component | Classifications | Raw JSON | Notes |
|---|---|---|---|
| `DetailPanel` (Servers / Integration Connectors / Governance Engines) | ❌ — deliberately deferred | ❌ | Backend calls (`get_server_report` etc.) return runtime/status DTOs, not metadata elements — no `elementHeader` present. Getting classifications would need an *extra* `ClassificationExplorer.get_element_by_guid` round-trip per row. Every row already has a working "Open in Catalog" cross-link where classifications are visible today, so this was assessed 2026-07-22 as low value for the added latency — intentionally out of scope unless the ops console specifically needs it without leaving. |

## Query (`egeria-insights.html`, formerly "Egeria Insights" in the UI)

| Component | Classifications | Raw JSON | Notes |
|---|---|---|---|
| Search results table | ⚠️ different pattern, not a gap | ❌ | No per-element detail view exists (row click navigates away via `crossAppNavigate`, doesn't open an inline pane) — nothing to attach a foldable section to. Classification names/zones are already shown inline as table columns, suited to a search-results view. Backend (`insights_handler.py`'s `_extract_classifications`) returns a dict-of-classification-name shape, not the `[{typeName, properties}]` array `ClassificationsAndRawJson` expects — would need a small adapter if a detail modal is ever added. Assessed 2026-07-22 as out of scope for now. |

## Not yet audited

These apps/views haven't been reviewed for classification/raw-JSON coverage
yet — don't assume either presence or absence until checked:

- Lineage Explorer (`lineage-explorer.html`)
- Egeria Overview (`egeria-overview.html`, `overview_handler.py`) — in-progress feature, not yet merged
- my-egeria integration (Textual TUI portal tile)
- Resource Explorer
- Action Center (`action_center_handler.py`) — known to use `_classifications_from_metadata_expert` per `common_serialize.py`'s docstring, but its frontend view hasn't been checked against this matrix
