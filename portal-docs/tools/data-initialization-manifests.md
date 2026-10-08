# Data Initialization — manifest and ordering file specs

Reference for the two optional JSON files that control how [Data Initialization](data-initialization.md) discovers, orders, and describes batches. Neither file is required — every folder under `dr-egeria-inbox` works with no manifest at all, alphabetical order, auto-heal off. These exist for when the defaults aren't enough.

---

## `_batch.json` — per-folder manifest

Lives at the root of a batch folder (a sibling of that folder's `.md` files), e.g. `dr-egeria-inbox/Local Dashboards/_batch.json`. Customizes one folder's display name, description, auto-heal canary, default enabled state, re-run safety, file execution order, and the Egeria user each file is loaded as.

### Fields

| Field | Default | Meaning |
|---|---|---|
| `displayName` | the folder name | Label shown in the batch list. |
| `description` | *(empty)* | Shown under the display name in the panel. |
| `canary` | *(none)* | `{"type": <Egeria metadata element type name>, "name": <exact displayName>}`. If present, the Portal periodically searches for an `ACTIVE` element of that type whose `displayName` exactly matches `name` (a cheap bounded, page-size-1 lookup); if nothing matches, it silently re-runs the batch's files in the background. Omit `canary` entirely for a manual-only batch — nothing runs on its own, an admin has to opt in from the panel. |
| `defaultEnabled` | `false` | Whether a freshly-discovered batch (no saved admin selection yet) starts checked. Core-portal batches that must survive a reset with zero admin action set this `true`; anything admin-droppable defaults to `false` so nothing runs until someone opts in. |
| `idempotent` | `true` | Set `false` only if one of the folder's commands creates a relationship/record with no pre-existence check, so re-running against already-seeded data would duplicate it. This gates the admin panel's manual Run Now/Run All Enabled with a confirmation prompt; auto-heal is unaffected (it only ever runs when the canary is confirmed missing, so there's never an already-seeded target to duplicate against). Leave the default alone unless you've confirmed a specific command actually lacks that check. |
| `files` | *(none — alphabetical)* | Explicit execution order, in the order listed. An entry can be a file (`"glossary.md"`), a file in a subfolder (`"mapping-the-systems/egeria-implementation.md"`), or a whole subfolder (`"strategic-digital-products/"`), which runs in place, in its own order (its own `_batch.json`, recursively). Anything **not** listed is appended afterward: `.md` files alphabetically, then subfolders alphabetically. Each appended item is flagged in the panel, because its position was defaulted rather than chosen. A stale entry (no longer present) is skipped and flagged. |
| `userid` | *(none — dr_egeria's default user)* | The Egeria user this folder's files are loaded as, and the default for its subfolders. A single entry in `files` can override it with the object form `{"file": "risk-register.md", "userid": "juleskeeper"}`. That form also works for a subfolder entry (`{"file": "mapping-the-systems/", "userid": "peterprofile"}`), where it sets the default for that subfolder. See [Run-as identity](#run-as-identity). |
| `exclude` | *(none)* | Files or subfolders in this folder that should never run, e.g. prose documents that sit next to the command files. `README.md` and the plumbing/output folders `dr-egeria-outbox`, `egeria-outbox`, `logs`, `data`, `templates`, `__pycache__` and `.ipynb_checkpoints` are always skipped, unless named explicitly in `files`. |

### Example — `Local Dashboards/_batch.json` (real, shipped)

```json
{
  "displayName": "Local Dashboards",
  "description": "Seeds the Local Dashboards feature's WorkItemList roadmap, work items, and demo report/analytics dashboard sheets, then the digital products demo and the worked examples from the two tutorials.",
  "canary": {"type": "WorkItemList", "name": "Local Dashboards - Next Steps"},
  "defaultEnabled": true,
  "files": [
    "LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md",
    "LOCAL_DASHBOARDS_WORK_ITEMS.dr-egeria.md",
    "LOCAL_DASHBOARDS_NEXT_STEPS_REPORTS.dr-egeria.md",
    "LOCAL_DASHBOARDS_ANALYTICS_DEMO.dr-egeria.md",
    "LOCAL_DASHBOARDS_ASSETS_BY_TYPE_LOCATION_DEMO.dr-egeria.md",
    "DIGITAL_PRODUCTS_DEMO.dr-egeria.md",
    "LOCAL_DASHBOARDS_TUTORIAL.md",
    "DIGITAL_PRODUCT_SUBSCRIPTION_TUTORIAL.md"
  ]
}
```

No `userid`, so every file runs as dr_egeria's default user.

### Example — `coco-workbooks/0. data-governance-program/_batch.json` (real, shipped, abridged)

`Coco - 0. Data Governance Program` is a `coco-workbooks` folder symlinked into `dr-egeria-inbox` (see [Ordering across the coco-workbooks symlinks](#ordering-across-the-coco-workbooks-symlinks) below), not an admin-droppable folder someone built from scratch. Its manifest ships as part of the `coco-workbooks` content itself:

```json
{
  "displayName": "Coco - 0. Data Governance Program",
  "description": "Coco Pharmaceuticals' governance program: ... Files run in the order the story happens — see the README.",
  "canary": {"type": "Glossary", "name": "Employee Glossary"},
  "defaultEnabled": false,
  "files": [
    {"file": "jules-90-day-plan.md", "userid": "juleskeeper"},
    {"file": "data-strategy-framework.md", "userid": "juleskeeper"},
    {"file": "joint-governance-officer-definitions.md", "userid": "juleskeeper"},
    {"file": "risk-register.md", "userid": "juleskeeper"},
    {"file": "privacy-governance-program.md", "userid": "faithbroker"},
    {"file": "data-security-strategy.md", "userid": "ivorpadlock"},
    {"file": "drug-development-governance.md", "userid": "tessatube"},
    "...",
    {"file": "employee-glossary.md", "userid": "erinoverview"},
    {"file": "strategic-information-supply-chains.md", "userid": "juleskeeper"}
  ]
}
```

The 19 files run in this explicit order, which is the order the story in Jules Keeper's plan happens, not alphabetical. The `README.md` is skipped. Each file is loaded as the governance leader the README names as its owner, so the definitions are attributed to that person rather than to whoever ran the load. `canary` checks for the `Employee Glossary` Glossary that `employee-glossary.md` creates. It needs to show that the batch's main content loaded, so it points at one of the last steps. `defaultEnabled` stays `false`: this is Coco Pharmaceuticals scenario content, not a core-portal feature that has to survive a reset unattended.

### Example — `coco-workbooks/1. coco-data-hub/_batch.json` (real, shipped, abridged)

The Data Hub README orders files and subfolders together, so its manifest does too:

```json
{
  "displayName": "Coco - 1. Data Hub",
  "files": [
    {"file": "strategic-supply-chain-analysis.md", "userid": "erinoverview"},
    "extending-the-systems-inventory/",
    {"file": "mapping-the-systems/", "userid": "peterprofile"},
    "data-field-naming/",
    "strategic-digital-products/",
    {"file": "solution-design.md", "userid": "erinoverview"},
    {"file": "software-development-governance-program.md", "userid": "pollytasker"}
  ],
  "exclude": ["founders-briefing-script.md", "reporting-subscription-gaps.md", "strategic-supply-chain-system-matches.md"]
}
```

`extending-the-systems-inventory/` and `strategic-digital-products/` have their own `_batch.json`, which sets their file order and their `userid` (`garygeeke` and `erinoverview`). `data-field-naming/` is listed to record its place in the story, but it is also its own batch through an inbox symlink, so it runs there instead (see below). The three excluded files are narrative documents with no commands.

### Run-as identity

Each file is run as `dr_egeria --process <file> --userid <userid> --user_pass <password>` when a `userid` applies to it, and without `--userid` otherwise. With no `--userid`, dr_egeria uses `EGERIA_USER`, or its built-in default `erinoverview`.

The nearest declaration wins:

1. the file's own `files` entry in its folder's `_batch.json`
2. the `userid` of the `_batch.json` in the file's folder
3. whatever the parent folders pass down: the parent's entry for this subfolder, else the parent's own `userid`, and so on up

Manifests never contain passwords. The password for a user comes from the environment variable `EGERIA_BOOTSTRAP_PASSWORD_<USERID>` (the userid in upper case, e.g. `EGERIA_BOOTSTRAP_PASSWORD_JULESKEEPER`), then `EGERIA_USER_PASSWORD`, then `secret`, which is the demo personas' password and the same fallback the Portal's other handlers use.

The admin panel shows each file's run-as user ("as juleskeeper", or "default user").

### Subfolders, and running each file once

Subfolders of a batch run inline, at their place in the parent's order (see `files` above). A nested folder therefore doesn't need its own symlink into `dr-egeria-inbox` to be loaded: `1. coco-data-hub/strategic-digital-products` runs as part of `Coco - 1. Data Hub`.

A nested folder **can** still be given its own symlink, which makes it a separate batch with its own canary, enable checkbox and place in `_folder_order.json`. Its parent then skips that subfolder and notes this in the panel, so the folder runs once, in its own batch. `Coco - 1. Data Field Naming` (`1. coco-data-hub/data-field-naming`) and `Coco - 4. Martyns Law` (`4. keeping-safe/martyns-law`) work this way. Removing such a symlink folds the folder back into its parent, at the position the parent's `files` list gives it.

Within one Run All or auto-heal pass, each file runs at most once, even if two batches reach it (for example, two symlinks to the same folder). The second occurrence is reported as `duplicate`, not as a failure, and the panel flags the overlap.

### Run ledger

Each file the Portal runs successfully is recorded in `~/.pyegeria/bootstrap_ledger.json` with a hash of its content. The panel marks a file **changed since last run** when its content has changed since, and ✓ when it hasn't. `·` means the Portal has no record of running it, which is not the same as "never loaded": a file loaded from a notebook, from Obsidian, from the CLI, or before the ledger existed shows `·` too. The ledger is advisory only and never causes a file to be skipped. Adding a file to a batch that's already loaded still does not trigger auto-heal, whose only signal is the canary. Use Run Now to load it.

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

The `Coco - *` batches carry number prefixes, but the dependency order in the coco-workbooks READMEs isn't numeric. The data processing purposes in `6. data-privacy` come straight after the data governance program. The data field naming standard has to load before the strategic digital products in the Data Hub. Keeping Safe needs the Data Hub's systems inventory. Martyn's Law comes after Sustainability. The shipped `_folder_order.json` encodes that order:

```json
["Coco - 0. Data Governance Program", "Coco - 6. Data Privacy", "Coco - 1. Data Field Naming",
 "Coco - 1. Data Hub", "Coco - 4. Keeping Safe", "Coco - 3. Sustainability",
 "Coco - 4. Martyns Law", "Coco - 5. Sales Forecast Consolidation"]
```

This file is deployment-specific (it lives under `dr-egeria-inbox`, which is environment data, not Portal code) — quickstart and freshstart each have their own `dr-egeria-inbox` and so their own independent `_folder_order.json`, even though the coco-workbooks batches themselves are the same symlinked content in both.

---

## Further resources

- [Data Initialization](data-initialization.md) — the admin panel these files configure
