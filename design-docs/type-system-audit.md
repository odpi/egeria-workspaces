# Type System Data Audit

Tracks which parts of the codebase use hardcoded Egeria type data versus pulling it
dynamically from the live type system. Review this whenever new types are added to
Egeria or a new feature area is built.

**Principle:** Structural hierarchies (supertype chains) should be derived from the
live type system via `ValidMetadataManager.get_all_entity_defs()` and cached with a
TTL. Hardcoded type lists are acceptable only for UI routing/classification decisions
that represent product choices, not type-system facts.

---

## Dynamic — pulled from Egeria at runtime

| Location | API / method | Notes |
|---|---|---|
| `type_system_handler.py` `/api/types` | `ValidMetadataManager.get_all_entity_defs()` | Full entity, classification, and relationship type catalogue for Egeria Explorer. Cached process-wide. |
| `governance_definitions_handler.py` `/api/governance/tree` | `ValidMetadataManager.get_all_entity_defs()` | Full `GovernanceDefinition` subtype tree, built by inverting the supertype map. 300 s TTL, falls back to `GOV_TYPE_TREE`. |
| `tech_catalog_handler.py` `/api/tech-catalog/tech-types/hierarchy` | `AutomatedCuration.get_tech_type_hierarchy()` | Technology type hierarchy (deployed implementation types). Fully live, no cache. |
| `tech_catalog_handler.py` `/api/tech-catalog/tech-types` | `AutomatedCuration.find_technology_types()` | Technology type list; deduplicates by qualifiedName at call time. |

---

## Hardcoded — intentional product/UI decisions

These are not derivable from the type system alone; they encode application-level
choices about how types map to UI sections or behaviours.

| Location | Constant | What it does | Why it's appropriate to keep hardcoded |
|---|---|---|---|
| `static/type-nav-map.json` + `static/type-nav-resolve.js` | `resolveTypeNav(typeName, superTypeNames)` (~95 entries) | Single source of truth for "which UI destination shows Egeria type X" — replaces three former hand-duplicated tables (see "Consolidation" below). Each entry carries `catalogSection`/`catalogTab` (Tech Catalog's own internal routing — only `tech-catalog.html` interprets these) and/or `explorerHash`(+`kind`) (the Egeria Explorer tab this type opens on when reached from outside Explorer). A handful of keys (`GlossaryTerm`/`Glossary`/`GlossaryCategory`, `GovernanceActionProcess`) carry both, since Tech Catalog owns an internal detail view for these but external callers need the Explorer route instead. Loaded via a bare `<script src="/static/type-nav-resolve.js">` tag — no React dependency, so the same file loads in React SPAs (`tech-catalog.html`, `type-explorer.html`, `egeria-operations/audit/insights/overview.html`, `lineage-explorer.html`) and the plain-vanilla `demo-portal.html` alike. | The mapping is a UI design decision. The type system says `RelationalDatabase` is a subtype of `DataStore`; it doesn't say which tab it belongs to. Review when new catalog tabs are added. |
| `static/egeria-shared-ui.js` | `resolveElementNav()` / `demo-portal.html`'s `portalResolveNav()` | Thin per-caller wrappers around `resolveTypeNav()` that add the one case the JSON can't express: `EngineAction` doesn't route to an Egeria Explorer hash at all — it opens the `egeria-operations` app directly (which has no per-guid deep link yet) — so it stays a small explicit code special-case in each wrapper, checked before the generic JSON lookup. `ToDo`/`Notification`/`Meeting`/`Review` (Action Center) and `ValidMetadataValue` used to be special-cased the same way; they are now plain `explorerHash` entries in the JSON. | `EngineAction`'s target app (not just target hash) genuinely differs per caller context, which the JSON schema doesn't model — a deliberate, narrow exception, not a sign the JSON approach failed. |
| `digital_products_handler.py` | `_CONTAINER_TYPES` (8 entries) | Identifies which collection subtypes are "containers" that can be recursed into when building the digital-products tree. | The set of container types is a feature decision; not every `Collection` subtype should be treated as a tree node. |
| `reference_data_handler.py` | `_SET_TYPES = {"ValidValueSet", "ReferenceDataSet"}` | Distinguishes reference-data sets from individual values. | Already partially resilient — also checks `superTypeNames` from the live element header. Small and stable; these two types are unlikely to be renamed. |
| `audit_handler.py` | `_AUDIT_REL_TYPES = {"Exception", "Certification", "License"}` | Allowlist of relationship types surfaced in the Audit detail panel. | Intentional filter — only a subset of relationship types are meaningful in the audit context. |
| `egeria_feedback_handler.py` | `_COMMENT_TYPES` (enum-like dict) | Maps comment-type labels to Egeria enum values for the feedback API. | These are Egeria API enum constants, not open metadata entity types. |

### Consolidation (2026-09-01)

Until 2026-09-01 the type→UI-destination mapping lived in **three**
physically-separate, hand-duplicated tables that had drifted out of sync with
each other and with the app's actual features: `TYPE_TO_NAV` in
`tech-catalog.html`, `EGERIA_EXPLORER_NAV` in `static/egeria-shared-ui.js`,
and `PORTAL_EXPLORER_NAV` in `demo-portal.html` (the last two hand-copied
because `demo-portal.html` can't load the React-dependent shared file).
Consolidating them into `static/type-nav-map.json` +
`static/type-nav-resolve.js` also fixed three concrete gaps found by
comparing the three tables against the live Egeria type catalogue and
against already-built display pages:
- `InformalTag` and `ContextEvent` had working display pages (Explorer's
  `InformalTagsView`/`ContextEventsView`, hashes `informal-tags`/
  `context-events`) but were missing from all three tables — added.
- `EngineAction`/`ToDo`/`Notification`/`Meeting`/`Review` worked in the
  Explorer/Portal tables via a code special-case but had no equivalent in
  `TYPE_TO_NAV` — a relationship row of one of these types in `AssetDetail`
  rendered with no "View →" button. `ToDo`/`Notification`/`Meeting`/`Review`
  are now plain `explorerHash: "action-center"` entries usable by all
  consumers; `EngineAction` remains a small code special-case (see table row
  above) but is now handled identically by all three former tables' call
  sites.

---

## Fallback / static trees kept as safety nets

| Location | Constant | Purpose |
|---|---|---|
| `governance_definitions_handler.py` | `GOV_TYPE_TREE` | Fallback returned by `_build_gov_tree()` when Egeria is unreachable at startup. Reflects the type system as of Egeria ~5.3. Update if the fallback diverges visibly from the live system. |

---

## How to audit

```bash
# Find any new hardcoded type-name lists in Python handlers
grep -rn "^\s*_.*TYPES\s*=\s*[{[]" compose-configs/egeria-quickstart/PyegeriaWebHandler/*.py

# Find hardcoded type strings that aren't in dynamic fetch paths
grep -rn "'[A-Z][a-zA-Z]\+'" compose-configs/egeria-quickstart/PyegeriaWebHandler/*.py \
  | grep -v "test\|#\|logger\|environ\|__pycache__"

# Check static/type-nav-map.json coverage against live type list
# Compare its keys against /api/types?area=2 (assets), area=3 (glossary), area=4 (governance)
python3 -m json.tool compose-configs/egeria-quickstart/PyegeriaWebHandler/static/type-nav-map.json
```

To verify the governance tree is complete, compare `/api/governance/tree` (dynamic)
against `/api/types?area=4` (all area-4 entities) and confirm every concrete subtype
of `GovernanceDefinition` appears in the tree.

---

## Review triggers

- Egeria version upgrade (new types added or renamed)
- New feature tab added to any portal app
- `GOV_TYPE_TREE` fallback diverges from live `/api/governance/tree` response
- `static/type-nav-map.json` is missing a type that users report as unroutable (single file now — no more cross-table sync to check)

*Last reviewed: 2026-09-01*
