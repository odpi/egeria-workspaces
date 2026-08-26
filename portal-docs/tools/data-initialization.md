# Data Initialization

Several Portal features — the Overview dashboard's Governance Metrics, Local Dashboards' roadmap and work items, and whatever else your deployment adds — depend on specific elements existing in Egeria, seeded by Dr.Egeria markdown documents. When Egeria's metadata store gets wiped (a redeploy, a manual DB drop, a Reset tab action), those documents need to run again, or the feature just renders empty with no explanation.

Data Initialization is the admin panel for that: it discovers the folders of seed documents, watches for the reset, and re-runs them automatically where it can — and gives you a manual override for everything else.

Access it from the **Data Initialization** tab/section on the Admin page (`/admin`), in all three environments (quickstart demo, quickstart local, freshstart).

---

## Batches

Every folder under `dr-egeria-inbox` is a **batch**, discovered automatically — no code change or redeploy needed to add one. Drop a new folder of Dr.Egeria `.md` files in, and it appears in the list on next page load.

Each batch shows:
- A checkbox to **enable** it — only enabled batches ever run, whether automatically or via Run All Enabled.
- Its files, each individually checkable — you can enable a folder but leave specific files out.
- An **auto-heal** badge if the batch has a way to detect its data went missing, or **manual only** if not (see below).
- A **⚠ not safe to re-run** badge if the batch contains a command known to duplicate data when re-run against an already-seeded target — see [Confirmation on risky re-runs](#confirmation-on-risky-re-runs).

Selections save automatically as you check/uncheck — there's no separate Save button.

---

## The `_batch.json` manifest

A folder needs no manifest at all — drop in `.md` files and it becomes a batch, files run alphabetically, auto-heal is off, and the folder name is the display name. An optional `_batch.json` in the folder's root customizes its display name, description, auto-heal canary, default enabled state, re-run safety, and file execution order.

Full field reference, the shipped `Local Dashboards` example, and a worked coco-workbooks example: **[Manifest and ordering file specs](data-initialization-manifests.md)**.

---

## Auto-heal vs. manual-only

A batch that declares a **canary** — one specific element the Portal can check for — gets auto-healed: the Portal periodically searches for an `ACTIVE` element of type `canary.type` whose `displayName` exactly matches `canary.name` (a cheap bounded, page-size-1 lookup). If nothing matches, it silently re-runs the batch's files in the background. You'll see a banner across the top of most pages while this is happening. A connection failure during the check is treated as "can't tell," not "missing" — it never triggers a heal pass on its own.

A batch with no canary is **manual only** — it never runs on its own. This is the safe default for a folder someone just dropped in: nothing runs until an admin explicitly opts in, either by giving it a canary (if you maintain the folder yourself — ask whoever built the feature that owns it) or by running it manually from this panel.

---

## Running manually

- **Run Now** on a single batch runs its enabled files, in the order described in [The `_batch.json` manifest](#the-_batchjson-manifest), and reports per-file results inline — including files that failed, with a short excerpt of the error.
- **Run All Enabled (in order)** runs every enabled batch across the whole tree, in the order described in [Cross-folder ordering](#cross-folder-ordering-_folder_orderjson) below, and shows a per-batch pass/fail summary.

Every document here is meant to be safe to re-run — creating the same element twice should just update it, not duplicate it. That's true for the overwhelming majority of what ships here, but not universally guaranteed for every possible command a folder's documents might use.

### Confirmation on risky re-runs

If a batch is flagged **⚠ not safe to re-run**, clicking Run Now (or Run All Enabled, if that batch is among the enabled ones) prompts for confirmation with a specific explanation before it actually runs — it won't proceed silently. Auto-heal is never affected by this: it only re-runs a batch when its canary is confirmed missing in the first place, so there's no already-seeded target to duplicate against.

If you see this warning and aren't sure whether the batch's data already exists, check first — e.g. search for the relevant elements in [Egeria Explorer](egeria-explorer.md) — rather than confirming without knowing.

---

## Cross-folder ordering (`_folder_order.json`)

By default, batches run in alphabetical order by folder name. To change that — e.g. so a batch that other batches' elements depend on runs first — drop a `_folder_order.json` in `dr-egeria-inbox` itself (a sibling of the batch folders, not inside any of them): a flat array of batch ids, explicit order first, then everything else alphabetically.

Full spec and a worked coco-workbooks example: **[Manifest and ordering file specs](data-initialization-manifests.md)**.

---

## Further resources

- [Manifest and ordering file specs](data-initialization-manifests.md) — full `_batch.json`/`_folder_order.json` reference, with examples
- [Admin Guide](../quickstart/demo/admin-guide.md) — where this panel sits alongside the rest of each environment's admin tools
- [Egeria Overview](egeria-overview.md) — the dashboard whose Governance Metrics are seeded by one of the batches this panel manages
- [Local Dashboards](local-dashboards.md) — another feature whose reference data is seeded this way
