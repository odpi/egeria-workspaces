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

### Example — `coco-workbooks/0. data-governance-program/_batch.json` (real, shipped)

`Coco - Data Governance Program` is a `coco-workbooks` folder symlinked into `dr-egeria-inbox` (see [Ordering across the coco-workbooks symlinks](#ordering-across-the-coco-workbooks-symlinks) below), not an admin-droppable folder someone built from scratch — its manifest ships as part of the `coco-workbooks` content itself:

```json
{
  "displayName": "Coco - Data Governance Program",
  "description": "Coco Pharmaceuticals' governance program: Jules Keeper's 90 day plan and data strategy, the governance officers' joint definitions and risk register, and the domain programs each officer's team produced. Files run in the order the story happens — see the README.",
  "canary": {"type": "Glossary", "name": "Employee Glossary"},
  "defaultEnabled": false,
  "files": [
    "jules-90-day-plan.md",
    "data-strategy-framework.md",
    "joint-governance-officer-definitions.md",
    "risk-register.md",
    "privacy-governance-program.md",
    "data-security-strategy.md",
    "drug-development-governance.md",
    "corporate-governance-program.md",
    "manufacturing-governance-program.md",
    "serialisation-governance-program.md",
    "human-resource-management.md",
    "health-and-safety.md",
    "biological-agents-and-gmo.md",
    "dangerous-goods-transport.md",
    "diversity-equity-inclusion.md",
    "data-governance-program.md",
    "employee-glossary.md"
  ]
}
```

17 files run in this explicit order — the story order Jules Keeper's plan actually happens in, not alphabetical — with `README.md` (the only `.md` in the folder not named here) appended last. `canary` checks for the `Employee Glossary` Glossary that `employee-glossary.md` creates — the last file in the list, which is deliberate: the canary only needs to confirm the *whole* batch completed, so it points at whatever the last step produces. `defaultEnabled` stays `false` — this is Coco Pharmaceuticals scenario content, not a core-portal feature that has to survive a reset unattended.

Three more `coco-workbooks` folders one level deeper than the six top-level ones also ship a manifest and need their own symlink into `dr-egeria-inbox` — `discover_batches()` only scans one level deep, so a nested folder is invisible unless it's symlinked in directly, same as any top-level one: `1. coco-data-hub/data-field-naming` ("Coco - Data Field Naming"), `4. keeping-safe/extending-the-systems-inventory` ("Coco - Systems Inventory"), and `4. keeping-safe/martyns-law` ("Coco - Martyn's Law").

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

The nine `Coco - *` batches (symlinks into `coco-workbooks`, see [Data Initialization](data-initialization.md)) sort alphabetically by default: `Coco - Data Field Naming`, `Coco - Data Governance Program`, `Coco - Data Hub`, `Coco - Data Privacy`, `Coco - Keeping Safe`, `Coco - Martyns Law`, `Coco - Sales Forecast Consolidation`, `Coco - Sustainability`, `Coco - Systems Inventory`. If the Coco Pharmaceuticals scenario has a real dependency order — e.g. the data governance program's glossary and roles should exist before the other folders' docs reference them — a `_folder_order.json` naming just that one batch first would suffice, since everything not listed keeps running alphabetically afterward:

```json
["Coco - Data Governance Program"]
```

This file is deployment-specific (it lives under `dr-egeria-inbox`, which is environment data, not Portal code) — quickstart and freshstart each have their own `dr-egeria-inbox` and so their own independent `_folder_order.json`, even though the coco-workbooks batches themselves are the same symlinked content in both.

---

## Further resources

- [Data Initialization](data-initialization.md) — the admin panel these files configure
