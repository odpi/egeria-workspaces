# Relationship Purpose — Portal Adoption Plan

Working document. Add comments / answers inline using `<!-- your note -->` or just edit text directly.

---

## Context

Egeria has added a **relationship purpose** to every relationship type
(`OpenMetadataRelationshipPurpose`, concept page:
<https://egeria-project.org/concepts/relationship-purpose/>). It explains *why* a
relationship type exists. It also decides whether operations that start on an
anchored element (delete, copy, scope checks) follow the relationship.

The portal apps currently show relationships as flat lists, grouped (on detail
pages) by whatever response key pyegeria happened to use. Purpose gives us a
meaningful, Egeria-defined way to organise them. This document plans adoption in:

- **Egeria Explorer → Type Explorer** (`type-explorer.html`): organise relationship types by purpose.
- **Element detail pages** (every `*Detail` panel in `type-explorer.html`, plus
  `data-mesh.html` and `tech-catalog.html`): group related elements into
  collapsible **purpose families**.

### Source references (odpi/egeria, `main`)

| What | Where |
|------|-------|
| Enum | `frameworks/open-metadata-framework/.../enums/OpenMetadataRelationshipPurpose.java` |
| OMRS typedef field (string) | `repository-services-apis/.../typedefs/RelationshipDef.java` → `relationshipPurpose` |
| Framework typedef field (enum) | `open-metadata-framework/.../properties/OpenMetadataRelationshipDef.java` → `relationshipPurpose` |
| Inheritance resolution | `generic-handlers/.../RelationshipPurposeResolver.java` |
| Populated on typedef API | `omf-metadata-server/.../OpenMetadataStoreRESTServices.java` (~line 5315) |

---

## 1. The purpose model

### 1.1 The eleven purposes

| Enum constant | Display name | Meaning | Anchored graph |
|---|---|---|:-:|
| `STRUCTURAL` | Structural | Part of what the element is. | ✔ |
| `ATTACHMENT` | Attachment | Information attached to, and owned by, the element. | ✔ |
| `ASSIGNMENT` | Assignment | Links the element to independent information that describes or governs it. | |
| `MEMBERSHIP` | Membership | Groups or organizes elements without owning them. | |
| `ASSOCIATION` | Association | Relates elements that keep their own identity, often in one direction. **Enum default.** | |
| `PEER` | Peer | A purely peer link between elements of equal standing. | |
| `DEFINITION` | Definition | Links a design or specification to its implementation. | |
| `DEPLOYMENT` | Deployment | Where something runs or is stored. | |
| `DESIGN_LINEAGE` | DesignLineage | How data and control are designed to flow (`LineageRelationship` and subtypes). | |
| `ACTION` | Action | Information gathered so that action can be taken. | |
| `ACTIVITY` | Activity | A record of action that took place. | |

"Anchored graph" = `isPartOfAnchoredGraph()`. Anchor operations starting on an
anchored element follow these relationships to elements in the same anchored
graph.

### 1.2 Key facts that shape the design

1. **Purpose is a property of the relationship *type*, not of individual relationships.**
   Related-element rows on detail pages do not carry it, so the portal must map
   `relationshipType` name → purpose.
2. **Inheritance is resolved server-side** on the OMF typedef path:
   `RelationshipPurposeResolver` walks the supertype chain, using the typedef's own
   value first and then the built-in `OpenMetadataType` table. The client does not
   need to walk supertypes, but must tolerate `null` (older servers, or a type
   with no purpose anywhere in its chain).
3. **Wire format.** `OpenMetadataRelationshipPurpose` is a Java enum with no
   `@JsonFormat(shape=OBJECT)`, so Jackson should serialise it as the constant name
   (`"DESIGN_LINEAGE"`). The OMRS `RelationshipDef` stores a plain string, also the
   constant name (`fromName` compares against `purpose.name()`). Normalise
   defensively anyway (accept constant names, display names, and `{name: …}`
   objects).

   **Verified in Phase 0 (2026-11-03)** against the quickstart platform
   (`versionName` 6.3-SNAPSHOT), raw `GET …/valid-metadata/open-metadata-types/relationship-defs`:
   - The list is at `typeDefList.typeDefs`. `relationshipPurpose` is a **plain
     string holding the constant name**, e.g. `"DESIGN_LINEAGE"`. No object
     form was seen.
   - 205 relationship defs: ASSIGNMENT 37, ASSOCIATION 30, STRUCTURAL 30,
     DEFINITION 18, DEPLOYMENT 16, ATTACHMENT 15, DESIGN_LINEAGE 14,
     MEMBERSHIP 13, ACTIVITY 12, PEER 12, ACTION 7, and **1 with the field
     absent**: `BiopsySupportingEvidence`, a custom Coco type with no
     supertype. So "no purpose" does occur on current servers too, not only
     on older ones.
   - Inheritance is filled in: every `LineageRelationship` /
     `DataLineageRelationship` subtype (DataFlow, ControlFlow, ProcessCall,
     UltimateSource, …) reports `DESIGN_LINEAGE`, and `AssetConnection`
     inherits `STRUCTURAL` from `ResourceConnection`.
   - **Subtypes can override their supertype**: `ActionRequester` is
     `ACTIVITY` under `LineageRelationship` (`DESIGN_LINEAGE`), and most
     `LabeledRelationship` subtypes differ from its `ASSOCIATION`. The client
     must use each type's own reported value and never derive it from the
     supertype.
   - Not yet checked: an older server without the field (none was available).
     The code treats an absent field as `null`, and B2 reports
     `serverReportsPurpose: false` when every def lacks it.

### 1.3 The six display families

Eleven flat groups would crowd a detail panel, so the UI groups purposes into six
**families**. The Type Explorer still shows the precise purpose on every type, and
badges on detail rows show the precise purpose too. Families are only the unit
for collapsible grouping.

| # | Family | Purposes | Default on detail pages | Rationale |
|---|--------|----------|-------------------------|-----------|
| 1 | **Composition** | Structural, Attachment | folded | The element's own anchored graph: what it *is* and what it *owns*. |
| 2 | **Governance & Description** | Assignment | folded | Independent things that describe or govern it (terms, policies, owners, tags). |
| 3 | **Organization** | Membership | folded | Collections, folders, groupings it belongs to or contains. |
| 4 | **Associations** | Association, Peer | folded | Independent elements linked by an ordinary or equal-standing relationship. |
| 5 | **Design & Deployment** | Definition, Deployment, DesignLineage | folded | Spec → implementation, where it runs or is stored, designed flows. |
| 6 | **Operations** | Action, Activity | folded | Actions to take, and records of actions taken. |
| — | **Unclassified** | `null` / unknown | folded, shown last | Server does not report a purpose, or the row has no `relationshipType`. |

Notes:
- **Unclassified does not fall back to Association.** Association is the enum
  default, but showing un-purposed relationships as "Associations" would
  claim something the server never said. Older Egeria servers will put
  everything in Unclassified. The UI should then show a single hint ("This
  Egeria server doesn't report relationship purposes") rather than six empty
  families.
- Family order is fixed (table order), and empty families are not rendered.
- Fold state is per family. It defaults as above and the user's choice is
  remembered per family in `localStorage` (wrapped in try/catch, as elsewhere).

---

## 2. Current state (egeria-workspaces)

All paths under `compose-configs/egeria-quickstart/PyegeriaWebHandler/`.

| Area | File / symbol | Today |
|------|---------------|-------|
| Typedef fetch | `type_system_handler.py::get_all_types` | `ValidMetadataManager.get_all_relationship_defs()` → `/open-metadata-types/relationship-defs`. Builds `relationships[name]` with `relationshipCategory`, `propagationRule`, ends, cardinality. **Purpose not read.** |
| Type list | `type-explorer.html::Sidebar` (~l.1827) | Flat A–Z "RELATIONSHIPS (n)" section. |
| Entity → rels | `TypeDetail` Relationships tab (~l.1270), `getRels()` (l.866) | Card list; sorts: name / other end / nearest ancestor / direction. No grouping. |
| Relationship type | `RelDetail` (l.1536) | Category badge via `_relCategoryInfo`. No purpose. |
| Detail pages | `GenericRelationshipsSection` → `RelationshipSection` → `RelatedElementRow` (l.8725–8820) | One `Collapsible` per pyegeria response key (e.g. `resourceList`), from `common_serialize._generic_relationships`. Each row has `relationshipType`. ~37 call sites in `type-explorer.html`. |
| Data Mesh | `data-mesh.html` (l.476–550) | **Separate copy** of `RelationshipSection` + its own key-grouping loop. |
| Tech Catalog | `tech-catalog.html::AssetRelationships` (~l.1770–1800) | Own flat list with `relationshipType` per row and a `rel` sort. |
| Shared UI | `static/egeria-shared-ui.js` | `Collapsible`, `FoldTriangle`, `ListControls`, `useListControls`. |

---

## 3. Design

### 3.1 Backend

**B1. Surface purpose in `/api/types`.** In `get_all_types`, add to each relationship:

```python
"relationshipPurpose": _norm_purpose(td.get("relationshipPurpose")),
```

`_norm_purpose` returns the enum constant name (`"DESIGN_LINEAGE"`) or `None`.
It accepts a constant name, a display name (`"DesignLineage"` → `DESIGN_LINEAGE`),
or a dict with `name`/`displayName`. Unknown values are logged once and treated
as `None`.

**B2. Lightweight lookup endpoint.** Pages that don't load the full type system
(detail panels in other sections, `data-mesh.html`, `tech-catalog.html`) need only
the name → purpose map:

```
GET /api/types/relationship-purposes
→ { "purposes": { "Schema": "STRUCTURAL", "SemanticAssignment": "ASSIGNMENT",
                  "BiopsySupportingEvidence": null, ... },
    "serverReportsPurpose": true }
```

- Built from the same `get_all_relationship_defs()` call. Cached in-process with
  a TTL (e.g. 10 min), keyed by `url|server`. Type definitions change rarely.
- Types with no purpose are listed with `null`, so "known type, no purpose"
  stays distinguishable from "type unknown to this server".
- `serverReportsPurpose` is `false` when *no* relationship def carried a purpose.
  The UI uses it to show the "server doesn't report purposes" hint instead of
  an all-Unclassified layout.
- Same auth pattern as `get_all_types` (token first, env service account
  fallback). Use the async client factory (see CLAUDE.md async invariants).

**B3. (Optional, later) Stamp purpose on related-element rows server-side.**
`common_serialize._unwrap_relationship_item` could add `relationshipPurpose`
using the cached map, so clients need no lookup. Deferred: the client-side map
is simpler, keeps serialisation free of type-system calls, and B2 is needed
anyway for the Type Explorer-less pages.

### 3.2 Shared front-end module

Add to `static/egeria-shared-ui.js` (single source of truth for every app):

```js
// Purpose metadata — mirrors OpenMetadataRelationshipPurpose.
var REL_PURPOSES = {
  STRUCTURAL:     { label: 'Structural',     family: 'composition', anchored: true,  desc: '…' },
  ATTACHMENT:     { label: 'Attachment',     family: 'composition', anchored: true,  desc: '…' },
  ASSIGNMENT:     { label: 'Assignment',     family: 'governance',  desc: '…' },
  MEMBERSHIP:     { label: 'Membership',     family: 'organization',desc: '…' },
  ASSOCIATION:    { label: 'Association',    family: 'related',     desc: '…' },
  PEER:           { label: 'Peer',           family: 'related',     desc: '…' },
  DEFINITION:     { label: 'Definition',     family: 'design',      desc: '…' },
  DEPLOYMENT:     { label: 'Deployment',     family: 'design',      desc: '…' },
  DESIGN_LINEAGE: { label: 'Design Lineage', family: 'design',      desc: '…' },
  ACTION:         { label: 'Action',         family: 'operations',  desc: '…' },
  ACTIVITY:       { label: 'Activity',       family: 'operations',  desc: '…' },
};
var REL_PURPOSE_FAMILIES = [   // display order
  { key: 'composition',  label: 'Composition',              defaultOpen: true,  color: … },
  { key: 'governance',   label: 'Governance & Description', defaultOpen: true,  color: … },
  { key: 'organization', label: 'Organization',             defaultOpen: false, color: … },
  { key: 'related',      label: 'Associations',             defaultOpen: false, color: … },
  { key: 'design',       label: 'Design & Deployment',      defaultOpen: false, color: … },
  { key: 'operations',   label: 'Operations',               defaultOpen: false, color: … },
  { key: 'unclassified', label: 'Unclassified',             defaultOpen: false, color: … },
];

useRelationshipPurposes(creds) // hook: fetches B2 once per page load per url|server (module-level cache),
                               // returns { purposeOf(typeName), familyOf(typeName), ready, error, serverReportsPurpose }
                               // serverReportsPurpose is null (unknown) while loading or after a failed fetch;
                               // a failed lookup must not show the "server doesn't report purposes" hint
seedRelationshipPurposes(map)  // Type Explorer calls this with data it already has from /api/types,
                               // so it never makes the extra B2 request
PurposeBadge({ purpose })      // small badge, tooltip = description (+ "Part of the anchored graph" when anchored)
groupByPurposeFamily(items, getTypeName, purposeOf?) // → [{ family, items }] in display order, empty families dropped
majorityPurposeFamily(items, getTypeName, purposeOf?) // → family key for a mixed-purpose group (D1); ties → earlier family
```

Colours: one muted hue per family, used for the family header accent and for
purpose badges. Define them as CSS custom properties alongside the existing
tokens so light and dark themes both work. Purposes in the same family share
the family hue; the badge text tells them apart.

### 3.3 Type Explorer

**T1. `RelDetail` — purpose badge.** Next to the category badge: `PurposeBadge`,
plus a small "⚓ anchored graph" chip for Structural/Attachment, and a link to the
concept page. If `relationshipPurpose` is null, show nothing (no fake default).

**T2. `TypeDetail` → Relationships tab — group by purpose.**
- New control: **Group by** `Purpose family` (default) | `None`, next to the
  existing sort select. Grouped mode renders one `Collapsible` per family, all
  open (this is a reference view, so folding by default would hide information).
  The family header shows the count.
- Inside a family, cards keep the current sort, and each card shows its precise
  `PurposeBadge`.
- Add a **purpose filter** (multi-select chips of the eleven purposes) that
  composes with the existing text filter and the Show inherited toggle.
- `getRels()` already spreads the relationship object, so `relationshipPurpose`
  flows through with no change there.

**T3. Sidebar — group the RELATIONSHIPS section by family.** Under
"RELATIONSHIPS (n)", one sub-header per family (with count), foldable, folded
by default except while a search query is active, when matching families
expand. Within a family, keep A–Z order and show the purpose as a small dim
suffix only when the family has more than one purpose.

**T4. (Optional) `GraphView` — colour relationship edges by family**, with a
legend. Low cost once the colour tokens exist. Do it if the graph already
distinguishes edge kinds; otherwise defer.
**Deferred (2026-11-04):** `GraphView` draws only the inheritance tree, with no
relationship edges, so there is nothing to colour yet.

**T5. Attribute index.** No change. It indexes properties, not relationships.

### 3.4 Element detail pages

**D1. `GenericRelationshipsSection` — two-level grouping.** This one component
backs nearly every detail panel, so changing it covers the whole Explorer.

```
▸ COMPOSITION (7)                         ← family Collapsible (new)
    ▸ Schema Type (1)                     ← existing per-key RelationshipSection
    ▸ Data Fields (6)
▸ GOVERNANCE & DESCRIPTION (4)
    ▸ Meanings (2)
    ▸ Governed By (2)
▸ ORGANIZATION (1)   [folded]
▸ UNCLASSIFIED (2)   [folded]
```

- Each existing key group (`relationships[key]`) is assigned to a family by its
  rows' `relationshipType` → purpose.
- **Mixed-purpose keys.** A pyegeria key can contain rows of several relationship
  types. Assign the key to the family of the **majority** of its rows (ties: the
  family that comes first in display order). Every row shows its own
  `PurposeBadge` (D2), so a minority row stays visibly labelled and nothing is
  hidden or duplicated. Splitting a key across families was considered and
  rejected: it would show the same pyegeria label in two places.
- While the purpose map is loading, render today's flat layout so there is no
  layout flash. Once `ready`, switch to the grouped layout. If
  `serverReportsPurpose` is false, keep the flat layout and show the one-line hint.
- Family fold state: all folded by default (§1.3), remembered per family in `localStorage`.
  The per-key inner `Collapsible`s keep `defaultOpen: true`, as today.
- Opt-out prop `groupByPurpose={false}` for any panel where the grouping reads
  badly. None are expected; the prop is an escape hatch.
- *Implemented 2026-11-04:* the family header count is the number of related
  elements (rows), not key groups. Fold state is one `localStorage` entry,
  `egeria-rel-purpose-open` (`{familyKey: bool}`), shared by every panel and
  app, so opening a family once opens it everywhere. `PurposeFamilySection`,
  `usePurposeFamilyOpen` and `relPurposeBadgeWanted` live in
  `egeria-shared-ui.js` for reuse in Phase 4.

**D2. `RelatedElementRow` — purpose badge** (shown per the §5 Q3 rule:
always outside a family group, where purpose isn't visible otherwise; inside
one only for multi-purpose families or minority rows). Next to the existing amber
`relationshipType` badge, add a compact `PurposeBadge` (shown only when the
purpose is known). This also covers hand-placed `RelationshipSection` call
sites that aren't routed through `GenericRelationshipsSection`. Those keep
their curated positions and gain only the badge.

**D3. `data-mesh.html`.** *Done 2026-11-04:* `RelationshipSection`,
`GenericRelationshipsSection`, `RelatedElementRowBase`, `relTitleCase` and
`REL_SECTION_*` moved to `egeria-shared-ui.js`. The Explorer keeps its
type-aware navigation by registering `RelationshipUI.Row = RelatedElementRow`
(a thin wrapper over `RelatedElementRowBase`). Data Mesh deleted its copies
and renders through the shared `GenericRelationshipsSection`. Delete its private `RelationshipSection` copy and its
key-grouping loop, and use the shared implementation (move `RelationshipSection`,
`RelatedElementRow` and `GenericRelationshipsSection` into `egeria-shared-ui.js`
if they aren't already shareable). This removes a duplicate as well as adding
the feature.

**D4. `tech-catalog.html::AssetRelationships`.** *Done 2026-11-04:* one
filter/sort control above the families; it applies before grouping, which has
the same effect as per-family controls without repeating the filter box. Its rows are relationship-first
(`r.relationshipType` plus a related element) rather than key-grouped. Wrap the
list in family `Collapsible`s using `groupByPurposeFamily(rels, r => r.relationshipType)`,
and add `PurposeBadge` beside the relationship-type label. Keep the existing
filter/sort inside each family.

### 3.5 Things deliberately out of scope

- Writing or editing purposes. They are defined by Egeria's type system.
- Changing what anchor operations do. The portal only *explains* the anchored-graph
  flag.
- Purpose-based filtering in search / lineage explorer. Possible follow-up.
- egeria-advisor. Its RAG and LGCI paths don't render relationship lists. A
  follow-up could add purpose to the `egeria_types` collection's indexed text so
  "what kind of relationship is X" questions can be answered.

---

## 4. Phased plan

| Phase | Items | Size | Exit criteria |
|-------|-------|------|---------------|
| **0 — Verify wire format** ✅ 2026-11-03 | Call `/open-metadata-types/relationship-defs` (raw JSON) against a server built from current `main`; record the exact `relationshipPurpose` shape and a few sample values; confirm inherited values are filled in for subtypes (e.g. a `LineageRelationship` subtype → `DESIGN_LINEAGE`). Also try an older server to confirm the field is absent/null. | S | Shape recorded in this doc (§1.2.3 updated). |
| **1 — Backend + shared module** ✅ 2026-11-03 | B1, B2, §3.2 shared constants/hook/badge/grouping helper. Unit tests for `_norm_purpose` (constant, display name, dict, null, garbage) and for the B2 endpoint (cache hit, `serverReportsPurpose` false). | S–M | `/api/types` and `/api/types/relationship-purposes` return purposes; tests pass. |
| **2 — Type Explorer** ✅ 2026-11-04 (T4 deferred) | T1, T2, T3 (T4 optional). | M | Relationship types are browsable by purpose in the sidebar and entity Relationships tab; `RelDetail` shows purpose. |
| **3 — Detail pages** ✅ 2026-11-04 | D1, D2 in `type-explorer.html`. | M | All `GenericRelationshipsSection` panels group by family; graceful fallback on old servers. |
| **4 — Other apps** ✅ 2026-11-04 | D3 (`data-mesh.html` de-dup + grouping), D4 (`tech-catalog.html`). | M | Same grouping and badges across the three apps. |
| **5 — Docs & release** | `portal-docs/tools/egeria-explorer.md` (new "Relationship purposes" section with the family table), `Extending the TypeExplorer.md` (how to use the shared helpers), CHANGELOG / RELEASE_NOTES. | S | Docs merged. |

### Testing

- **Backend:** pytest for `_norm_purpose` and the B2 endpoint (mock
  `ValidMetadataManager`).
- **Browser:** extend `tests/browser/` (Playwright) with (1 and the
  `serverReportsPurpose: false` case for the Type Explorer are in
  `test_relationship_purpose_type_explorer.py`, Phase 2; 2 and the detail-page
  `serverReportsPurpose: false` case are in `test_relationship_purpose_detail.py`,
  Phase 3):
  1. Type Explorer → pick an entity with many relationships (e.g. `Asset`) →
     Relationships tab shows family groups; purpose filter narrows them.
  2. A detail panel with Composition + Governance content → all families
     start folded; opening one survives a reload.
  3. Purpose endpoint stubbed to `serverReportsPurpose: false` → flat layout plus
     the hint, no empty family headers.
- **Manual:** check light and dark themes for badge and family-header contrast.

---

## 5. Open questions

1. **Fold defaults.** ~~Composition + Governance open, the rest folded.~~
   **Decided 2026-11-04: every family is folded by default** on detail pages;
   the user's per-family choice is remembered in `localStorage`.
2. **Family names.** **Decided 2026-11-04:** keep "Governance & Description";
   rename "Related Elements" → **"Associations"** (Association + Peer). Labels
   live in one place (`REL_PURPOSE_FAMILIES`), so revisiting is cheap.
3. **Per-row badges.** **Decided 2026-11-04:** show a row's `PurposeBadge` only
   where it adds information: when the row's family holds more than one
   purpose (Composition, Associations, Design & Deployment, Operations), or
   when the row's own family differs from the family its key group was
   placed under (minority rows from the majority rule in D1).
4. **"Property detail pages".** **Decided 2026-11-04:** means the element
   detail panels (`GenericRelationshipsSection` users, data-mesh, tech-catalog),
   as this doc assumes.
5. **B3 (server-side stamping).** **Decided 2026-11-04:** client-only for now;
   add B3 when a non-browser consumer (notebooks, MCP, advisor) needs purpose.

Further decisions (2026-11-04):
- **Type Explorer stays open.** The all-folded default is for element detail
  pages. The `TypeDetail` Relationships tab opens every family (reference
  view); the sidebar RELATIONSHIPS section stays folded except during a search.
- **Older-server hint wording:** "This Egeria server doesn't report
  relationship purposes, so relationships aren't grouped." Shown only when
  `serverReportsPurpose === false`. A failed lookup shows no hint, just the
  flat layout, because failure says nothing about the server.
- **PR scope:** one PR covering Phases 0–2.
