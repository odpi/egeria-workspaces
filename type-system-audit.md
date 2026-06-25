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
| `tech-catalog.html` | `TYPE_TO_NAV` (~60 entries) | Maps open metadata type names to catalog sections and tabs (infrastructure / data-assets / APIs / processes / glossary / …). Also routes to external apps (Egeria Explorer, Governance Definitions, etc.). | The mapping is a UI design decision. The type system says `RelationalDatabase` is a subtype of `DataStore`; it doesn't say which tab it belongs to. Review when new catalog tabs are added. |
| `digital_products_handler.py` | `_CONTAINER_TYPES` (8 entries) | Identifies which collection subtypes are "containers" that can be recursed into when building the digital-products tree. | The set of container types is a feature decision; not every `Collection` subtype should be treated as a tree node. |
| `reference_data_handler.py` | `_SET_TYPES = {"ValidValueSet", "ReferenceDataSet"}` | Distinguishes reference-data sets from individual values. | Already partially resilient — also checks `superTypeNames` from the live element header. Small and stable; these two types are unlikely to be renamed. |
| `audit_handler.py` | `_AUDIT_REL_TYPES = {"Exception", "Certification", "License"}` | Allowlist of relationship types surfaced in the Audit detail panel. | Intentional filter — only a subset of relationship types are meaningful in the audit context. |
| `egeria_feedback_handler.py` | `_COMMENT_TYPES` (enum-like dict) | Maps comment-type labels to Egeria enum values for the feedback API. | These are Egeria API enum constants, not open metadata entity types. |

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

# Check TYPE_TO_NAV coverage against live type list
# Compare keys of TYPE_TO_NAV in tech-catalog.html against
# /api/types?area=2 (assets), area=3 (glossary), area=4 (governance)
```

To verify the governance tree is complete, compare `/api/governance/tree` (dynamic)
against `/api/types?area=4` (all area-4 entities) and confirm every concrete subtype
of `GovernanceDefinition` appears in the tree.

---

## Review triggers

- Egeria version upgrade (new types added or renamed)
- New feature tab added to any portal app
- `GOV_TYPE_TREE` fallback diverges from live `/api/governance/tree` response
- `TYPE_TO_NAV` in tech-catalog.html is missing a type that users report as unroutable

*Last reviewed: 2026-06-24*
