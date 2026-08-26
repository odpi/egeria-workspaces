# Data Initialization — manifest and ordering file specs

Reference for the two optional JSON files that control how [Data Initialization](data-initialization.md) discovers, orders, and describes batches. Neither file is required — every folder under `dr-egeria-inbox` works with no manifest at all, alphabetical order, auto-heal off. These exist for when the defaults aren't enough.

---

## `_batch.json` — per-folder manifest

Lives at the root of a batch folder (a sibling of that folder's `.md` files), e.g. `dr-egeria-inbox/Local Dashboards/_batch.json`. Customizes one folder's display name, description, auto-heal canary, default enabled state, re-run safety, and file execution order.

### Fields

| Field | Default | Meaning |
|---|---|---|
| `displayName` | the folder name | Label shown in the batch list. |
| `description` | *(empty)* | Shown under the display name in the panel. |
| `canary` | *(none)* | `{"type": <Egeria metadata element type name>, "name": <exact displayName>}`. If present, the Portal periodically searches for an `ACTIVE` element of that type whose `displayName` exactly matches `name` (a cheap bounded, page-size-1 lookup); if nothing matches, it silently re-runs the batch's files in the background. Omit `canary` entirely for a manual-only batch — nothing runs on its own, an admin has to opt in from the panel. |
| `defaultEnabled` | `false` | Whether a freshly-discovered batch (no saved admin selection yet) starts checked. Core-portal batches that must survive a reset with zero admin action set this `true`; anything admin-droppable defaults to `false` so nothing runs until someone opts in. |
| `idempotent` | `true` | Set `false` only if one of the folder's commands creates a relationship/record with no pre-existence check, so re-running against already-seeded data would duplicate it. This gates the admin panel's manual Run Now/Run All Enabled with a confirmation prompt; auto-heal is unaffected (it only ever runs when the canary is confirmed missing, so there's never an already-seeded target to duplicate against). Leave the default alone unless you've confirmed a specific command actually lacks that check. |
| `files` | *(none — pure alphabetical)* | Explicit execution order for the files named here, in the order listed. Any `.md` file in the folder **not** listed is appended afterward, alphabetically. A stale filename (no longer present in the folder) is silently skipped, not an error. |

### Example — `Local Dashboards/_batch.json` (real, shipped)

```json
{
  "displayName": "Local Dashboards",
  "description": "Seeds the Local Dashboards feature's WorkItemList roadmap, work items, and demo report/analytics dashboard sheets.",
  "canary": {"type": "WorkItemList", "name": "Local Dashboards - Next Steps"},
  "defaultEnabled": true,
  "idempotent": true,
  "files": [
    "LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md",
    "LOCAL_DASHBOARDS_WORK_ITEMS.dr-egeria.md",
    "LOCAL_DASHBOARDS_NEXT_STEPS_REPORTS.dr-egeria.md"
  ]
}
```

### Example — a coco-workbooks folder (illustrative, not shipped)

`Coco - Data Governance Program` (the batch created by symlinking `coco-workbooks/0. data-governance-program` into `dr-egeria-inbox`, see [Ordering across the coco-workbooks symlinks](#ordering-across-the-coco-workbooks-symlinks) below) currently has **no** `_batch.json` — it runs as 18 files in plain alphabetical order, manual-only, no canary. That's a reasonable default, but the folder isn't actually order-independent: `data-strategy-framework.md` creates the `Data Strategy Framework` Solution Blueprint that later docs' Solution Components attach to, and `employee-glossary.md` and `joint-governance-officer-definitions.md` define terms/roles other docs in the folder reference by name. If this folder were promoted to auto-heal with an explicit order, its manifest might look like:

```json
{
  "displayName": "Coco - Data Governance Program",
  "description": "Coco Pharmaceuticals' data strategy framework, governance program definitions, and supporting glossaries — see coco-workbooks/0. data-governance-program.",
  "canary": {"type": "SolutionBlueprint", "name": "Data Strategy Framework"},
  "defaultEnabled": false,
  "files": [
    "employee-glossary.md",
    "joint-governance-officer-definitions.md",
    "data-strategy-framework.md",
    "data-governance-program.md"
  ]
}
```

`employee-glossary.md`, `joint-governance-officer-definitions.md`, `data-strategy-framework.md`, and `data-governance-program.md` run first, in that order; the remaining 14 files (`README.md`, `biological-agents-and-gmo.md`, `corporate-governance-program.md`, …) run afterward, alphabetically — the explicit-list-then-alphabetical-remainder rule from the Fields table above. `canary` points at the `Data Strategy Framework` Solution Blueprint that `data-strategy-framework.md` creates — a real, specific element the Portal can check for, per the `canary` row above. `defaultEnabled` is left `false` since this is admin-droppable content, not a core-portal feature that must survive a reset unattended.

This manifest doesn't exist in the repo — it's illustrative. Adding it for real is a legitimate follow-up if you want this folder to auto-heal with this ordering; ask if you'd like that done.

### The core-portal exception

A manifest is optional for every folder under `dr-egeria-inbox` — but it's the *only* way to register one of the handful of core-portal seed batches that ship as `.md` files alongside the Portal's own code rather than under `dr-egeria-inbox` (e.g. the Governance Metrics seed doc next to `gen_governance_metrics.py`). For those, a manifest is **required** — no manifest means that batch simply doesn't appear — and their `files` list is used exactly as given, with **no** alphabetical-remainder auto-append (that folder also holds unrelated `.py`/`.html` source, so "every other file in the folder" isn't a safe rule there).

---

## `_folder_order.json` — cross-folder ordering

Lives directly under `dr-egeria-inbox` itself (a sibling of the batch folders, not inside any of them). By default, batches run in alphabetical order by folder name; this file overrides that — e.g. so a batch other batches' elements depend on runs first.

### Shape

A flat JSON array of batch ids. A batch's id is its folder name, or a core-portal batch's fixed id (e.g. `overview-governance-metrics`).

```json
["Local Dashboards", "Sustainability Commands", "ML-OPS"]
```

Listed batches run first, in that order; every other batch runs afterward, alphabetically by id — same explicit-list-then-alphabetical-remainder rule `files` uses within a folder. There's no requirement to list every batch — an empty or missing `_folder_order.json` is just alphabetical-everywhere.

### Ordering across the coco-workbooks symlinks

The six `Coco - *` batches (symlinks into `coco-workbooks`, see [Data Initialization](data-initialization.md)) sort alphabetically by default: `Coco - Data Governance Program`, `Coco - Data Hub`, `Coco - Data Privacy`, `Coco - Keeping Safe`, `Coco - Sales Forecast Consolidation`, `Coco - Sustainability`. If the Coco Pharmaceuticals scenario has a real dependency order — e.g. the data governance program's glossary and roles should exist before the other five folders' docs reference them — a `_folder_order.json` naming just that one batch first would suffice, since everything not listed keeps running alphabetically afterward:

```json
["Coco - Data Governance Program"]
```

This file is deployment-specific (it lives under `dr-egeria-inbox`, which is environment data, not Portal code) — quickstart and freshstart each have their own `dr-egeria-inbox` and so their own independent `_folder_order.json`, even though the coco-workbooks batches themselves are the same symlinked content in both.

---

## Further resources

- [Data Initialization](data-initialization.md) — the admin panel these files configure
