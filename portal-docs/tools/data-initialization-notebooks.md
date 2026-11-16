# Running notebooks during Data Initialization

[Data Initialization](data-initialization.md) can run Jupyter notebooks as well as Dr.Egeria documents. A notebook is listed in a folder's `_batch.json` manifest, beside the Dr.Egeria files and subfolders, and runs in the order the manifest gives. It runs when an admin clicks **Run Now** or **Run All Enabled**, or automatically when the batch's canary goes missing after Egeria is reset, exactly like a Dr.Egeria file.

There is no new screen or setting to switch on. Notebooks appear in the existing Data Initialization panel, with the same enable checkboxes.

This guide covers:

- [How it works](#how-it-works): which notebooks run, where, as whom, and what you get back
- [Writing a notebook that runs here](#writing-a-notebook-that-runs-here)
- [Techniques and best practices](#techniques-and-best-practices): searching efficiently, `check-only` cells, bounded waits, re-run safety
- [Adding a notebook to a batch](#adding-a-notebook-to-a-batch), with recipes
- [Walkthrough: try it end to end](#walkthrough-try-it-end-to-end)
- [Troubleshooting](#troubleshooting)

---

## How it works

### Which notebooks run

A notebook runs only if a `_batch.json` **lists it** in `files`. This differs from Dr.Egeria files, where every unlisted `.md` file in the folder runs anyway, after the listed ones. Workbook folders are mostly tutorials, which are not meant to run on their own, so notebooks are never picked up by default.

To run every notebook in a folder without listing each one, set `"notebooks": "all"` in that folder's `_batch.json`. Unlisted notebooks then run after the listed files, alphabetically, the same way unlisted `.md` files do.

### Where the Portal looks for manifests

There are two places:

1. **`dr-egeria-inbox`**, as before. Every folder there is a batch. The `Coco - …` batches are symlinks from the inbox into `coco-workbooks`.
2. **Scan roots.** The folders listed in the `EGERIA_BOOTSTRAP_SCAN_ROOTS` setting are searched recursively for `_batch.json` files. In quickstart this is `/coco-workbooks` (the repository's `coco-workbooks` folder). Freshstart has no scan roots by default.

In a scan root, each **topmost** folder that has a `_batch.json` becomes a batch, and everything below it runs inside that batch, in its manifest's order. A folder with no `_batch.json` is *not* a batch there, unlike in `dr-egeria-inbox`.

A folder that is already an inbox batch keeps its inbox name. For example, `coco-workbooks/1. coco-data-hub` is still `Coco - 1. Data Hub`, so the selections admins have saved for it carry over. A batch found only by scanning is named after its path, e.g. `coco-workbooks/egeria-api-samples/pyegeria`, unless its manifest gives a `displayName`.

### How a notebook runs

A notebook runs inside the Portal's own container (`quickstart-pyegeria-web`), not in the Jupyter container. Specifically:

- **In its own folder,** so relative paths such as `./data/sales.csv`, and `%run other-notebook.ipynb` for a notebook beside it, work as they do in Jupyter.
- **As the run-as user** from the manifest, using the same `userid` rules as Dr.Egeria files (see [Run-as identity](data-initialization-manifests.md#run-as-identity)). The notebook receives that user as the environment variables `EGERIA_USER` and `EGERIA_USER_PASSWORD`. With no `userid`, it gets the Portal's own `EGERIA_USER` (shown as **default user** in the panel).
- **With the Portal's Python environment:** its pyegeria release (6.2.x), `pandas`, `requests`, `sqlalchemy`, `psycopg2`, `rich` and `nest_asyncio`. `matplotlib` is not installed, and nor is anything that only the Jupyter image has, such as its `commands.*` modules.
- **Using the `python3` kernel,** whatever kernel the notebook names.
- **With no keyboard,** so a cell that calls `input()` fails at once rather than waiting.
- **Within time limits:** 10 minutes per cell (`BOOTSTRAP_NOTEBOOK_CELL_TIMEOUT_SECONDS`), 3 minutes for a cell tagged [`check-only`](#check-only-cells) (`BOOTSTRAP_NOTEBOOK_CHECK_CELL_TIMEOUT_SECONDS`), and 15 minutes for the whole notebook (`BOOTSTRAP_BATCH_TIMEOUT_SECONDS`).

The notebook file itself is never changed. The run works on a copy.

### What you get back

The result appears under the batch in the panel. Each failed file has its own line:

```
✗ 0/2 files ran clean
• initialize-pyegeria.ipynb: cell 1 of 15: ImportError: cannot import name 'render_markdown' from 'pyegeria' (…)
  Executed copy: /root/.pyegeria/notebook-runs/pyegeria-b7b8c666/initialize-pyegeria.ipynb
```

- A notebook **fails** as soon as one of its cells raises an error or times out. The rest of its cells don't run. The result names the cell, counting code cells only, and gives the error. The exception is a cell tagged [`check-only`](#check-only-cells): its failure is noted in the result and the notebook carries on.
- The **executed copy** is the notebook as it ran, with every cell's output, and the traceback if a cell failed. It is written on success and on failure, overwriting the previous run's copy. The path shown is inside the container. On the host it is:
  - quickstart: `runtime-volumes/quickstart-pyegeria-state/notebook-runs/…`
  - freshstart: `runtime-volumes/freshstart-pyegeria-state/notebook-runs/…`

  Open it in Jupyter or any notebook viewer.
- A failed file does **not** stop the batch. The next file in the order still runs, so a notebook that depends on an earlier one will fail too, with the same error.
- Every run is recorded in the run ledger like a Dr.Egeria file's. The panel shows ✓ after a clean run, **changed since last run** once the notebook is edited, or **failed** with the time and error after a failed run, whether Run Now or auto-heal ran it.

### Re-run safety

Notebooks often create elements without first checking whether they exist. So a batch that contains a notebook is treated as **not safe to re-run** by default (`idempotent: false`). The panel shows ⚠ for it, and Run Now asks for confirmation before running it. Auto-heal is not affected, because it only runs a batch when its canary is missing.

If your notebooks do check before creating, so that running them twice changes nothing, say so with `"idempotent": true` in the manifest.

---

## Writing a notebook that runs here

A notebook that runs top to bottom in Jupyter with **Restart & Run All** will usually run here. Check these points:

1. **Take the connection and identity from the environment,** with defaults for Jupyter:

   ```python
   import os
   view_server = os.environ.get("EGERIA_VIEW_SERVER", "qs-view-server")
   url = os.environ.get("EGERIA_VIEW_SERVER_URL", "https://host.docker.internal:9443")
   user_id = os.environ.get("EGERIA_USER", "peterprofile")
   user_pwd = os.environ.get("EGERIA_USER_PASSWORD", "secret")
   ```

   The Portal sets all four. Don't hard-code a user, or the manifest's `userid` has no effect.
2. **Import only what the Portal has.** Use pyegeria's public API for the current release, and avoid `commands.*`, `matplotlib`, and other packages from the Jupyter image. If a notebook needs an extra package, ask for it to be added to the Portal image rather than calling `pip install` in a cell.
3. **No interaction.** No `input()`, and no widgets that must be clicked before the next cell can run.
4. **Make it safe to re-run** if you can: look an element up before creating it (see [Make every create safe to run twice](#make-every-create-safe-to-run-twice)). Then set `"idempotent": true`.
5. **Mind what it writes to disk.** The notebook runs in its real folder in the repository, and `coco-workbooks` is mounted read-write, so files it saves land in your checkout. Write scratch output to a temporary directory instead.
6. **Create something recognisable last,** if the batch should heal itself after a reset. A canary is one element, found by type and exact display name (see [Choosing a canary](#choosing-a-canary)).

To check a notebook the way the Portal will run it, run it in the Portal's container from the notebook's folder, as the user the manifest names. The executed copy goes to `/tmp` in the container, not beside the notebook:

```bash
docker exec -w "/coco-workbooks/<folder>" \
  -e EGERIA_USER=peterprofile -e EGERIA_USER_PASSWORD=secret \
  quickstart-pyegeria-web \
  jupyter nbconvert --to notebook --execute --output /tmp/check.ipynb <notebook>.ipynb
```

This shows the same errors the Portal would. It doesn't apply the Portal's time limits or its handling of [`check-only` cells](#check-only-cells), though.

---

## Techniques and best practices

These come from getting the Coco workbooks to load reliably on a full quickstart, where a notebook that worked in Jupyter against a small repository timed out, blocked auto-heal, or failed on a second run.

### Search the repository once, not once per item

Each starts-with or contains search (`find_elements_by_property_value` with `starts_with=True`, or any `find_*` with a search string) is a regular-expression scan of the repository. One is cheap; one per row of a CSV is not. A cell that ran one starts-with search for each of 66 schemas took more than 10 minutes on a loaded quickstart. That was over the cell limit, so the batch stopped there.

List the elements **by type** instead, page through them, and do the matching in Python:

```python
PAGE_SIZE = 100    # the most a by-type listing returns per page

def list_by_type(type_name):
    """Every element of type_name, as returned by a by-type listing."""
    elements, start = [], 0
    while True:
        page = classification_explorer.find_elements_by_property_value(
            property_value="*", property_names=["qualifiedName"],
            metadata_element_type=type_name, graph_query_depth=0,
            start_from=start, page_size=PAGE_SIZE)
        if not isinstance(page, list) or not page:
            return elements
        elements += page
        if len(page) < PAGE_SIZE:
            return elements
        start += PAGE_SIZE

tables_by_schema = defaultdict(list)
for table in list_by_type("RelationalTable"):
    qualified_name = table["properties"]["qualifiedName"]
    if qualified_name.startswith(TABLE_PREFIX):
        schema, _, _ = qualified_name[len(TABLE_PREFIX):].partition("::")
        tables_by_schema[schema].append(qualified_name)
```

On the same repository this takes about 4 seconds for 555 tables. Narrowing it instead to one starts-with search on the common prefix still took about 150 seconds, because that is still a scan.

- With `property_value="*"` and a type, pyegeria lists elements by type, and caps each page at 100 (`STAR_PAGE_MAX`). Use a page size of 100, or the loop's "last page" test stops after the first page.
- Pass `metadata_element_type`. The older name `metadata_element_type_name` still works, but logs a deprecation warning in every executed copy.
- Pass `graph_query_depth=0` when only the element's own properties are needed.

### Check-only cells

Many workbooks end with cells that only report on what the earlier cells loaded: counts, coverage tables, a walk from one system to its tables. If one of those is slow or fails, it should not fail the notebook. A failed notebook stops auto-heal for the whole batch, so a canary created by a later file never appears, and the batch is retried, and fails again, on every check.

Add the tag `check-only` to such a cell (in Jupyter Lab: the property inspector's **Cell Tags**, or `"tags": ["check-only"]` in the cell's `metadata`). When the Portal runs the notebook, a `check-only` cell:

- gets its own, shorter limit: 3 minutes (`BOOTSTRAP_NOTEBOOK_CHECK_CELL_TIMEOUT_SECONDS`)
- is interrupted if it runs past it, and the error or timeout is noted in the result instead of failing the notebook: `ran 13 code cells; check-only cell 12 (CellTimeoutError: cell timed out) failed and was skipped`
- doesn't stop the cells after it from running

Tag only cells that change nothing in Egeria and that later cells don't depend on. A cell that waits for something the next cells need, such as the cataloguer finishing before a listener is connected, is not `check-only`. It needs [a bounded wait](#keep-waits-inside-the-cell-limit) instead.

The tag has no effect in Jupyter.

### Keep waits inside the cell limit

A cell that polls until Egeria has finished something must give up within the 10-minute cell limit, and leave room for its last check. Use a deadline below the limit, and make each check cheap (see [Search the repository once](#search-the-repository-once-not-once-per-item)):

```python
WAIT_MINUTES = 9          # the Portal allows 10 minutes per cell

deadline = time.time() + WAIT_MINUTES * 60
while True:
    missing = still_missing()          # one listing per check, not one search per item
    if not missing or time.time() > deadline:
        break
    time.sleep(30)
```

If the wait runs out, report what is still missing and skip the step that depended on it, rather than raising. The next run, manual or auto-heal, tries again.

The whole notebook also has to finish within 15 minutes (`BOOTSTRAP_BATCH_TIMEOUT_SECONDS`), so count every wait toward that too.

### Make every create safe to run twice

Auto-heal reruns a batch whenever its canary is missing, and Run Now reruns it on request. So each create should first check whether the element is there:

```python
def get_guid(qualified_name):
    guid = client.get_element_guid_by_unique_name(qualified_name)
    return None if guid in (None, NO_ELEMENTS_FOUND) else guid

if get_guid(qualified_name) is None:
    client.create_...(body)
```

A lookup can say "not found" for an element that exists, because the running user can't see it. `UserIdentity` elements, for example, are not returned to ordinary users' searches. The create then fails with `OMAG-COMMON-409-001` (the `qualifiedName` is already in use). That rejection means the element is there, so treat it as success:

```python
def create_unless_present(create, body):
    """Call create(body), treating Egeria's unique-name rejection as "already there"."""
    try:
        return create(body)
    except Exception as exc:
        if "OMAG-COMMON-409-001" in str(exc):
            return None
        raise
```

Only once every create in the notebook is guarded like this should the manifest say `"idempotent": true`.

### Find the slow cell from the result

The result line names the cell that failed or timed out, counting code cells only (`cell 12 of 13`). The executed copy has every cell's output up to that point. A cell that timed out has no traceback, because the Portal interrupted it. Its partial output, and any `DeprecationWarning` lines, usually show what it was doing.

---

## Adding a notebook to a batch

### Recipe: a notebook in an existing Coco batch

For example, to add `creating-system-data-layer.ipynb` to **Coco - 1. Data Hub**:

1. Open `coco-workbooks/1. coco-data-hub/_batch.json`.
2. Add the notebook to `files` at the point in the story where it belongs, with its path relative to the manifest, and the user it should run as:

   ```json
   "files": [
     {"file": "strategic-supply-chain-analysis.md", "userid": "erinoverview"},
     "extending-the-systems-inventory/",
     {"file": "mapping-the-systems/", "userid": "peterprofile"},
     {"file": "creating-system-data-layer/creating-system-data-layer.ipynb", "userid": "peterprofile"},
     "data-field-naming/",
     ...
   ]
   ```

   If the subfolder has several notebooks, give it its own `_batch.json` that lists them, and list `"creating-system-data-layer/"` in the parent instead.
3. Reload the admin page. The notebook appears in the batch's file list with its run-as user. The batch is now flagged ⚠ **not safe to re-run**, unless you add `"idempotent": true`.

A notebook added to a batch that already has a canary does not run until that canary goes missing, or until someone clicks Run Now.

### Recipe: a folder of notebooks as its own batch

Put a `_batch.json` in the folder, anywhere under `coco-workbooks` that is not already inside a Coco batch:

```json
{
  "displayName": "Sales forecast notebooks",
  "description": "Generates the sales data and onboards it. Creates elements without checking, so re-running duplicates them.",
  "defaultEnabled": false,
  "userid": "peterprofile",
  "files": [
    "1. generate-sales-data.ipynb",
    "2. onboarding-resource-explorer.ipynb"
  ]
}
```

It appears as its own batch on the next page load, switched off (`defaultEnabled: false`) and manual only, since it has no canary.

A folder that sits inside an existing Coco batch can't become a separate batch by scanning: the parent batch already owns it. To give such a folder its own batch, add a symlink to it in `dr-egeria-inbox`, as was done for `Coco - 1. Data Field Naming` (see [Give a nested folder its own batch](../../DR_EGERIA_AUTO_LOADING_GUIDE.md#give-a-nested-folder-its-own-batch)).

### Recipe: Dr.Egeria files and notebooks in one folder

List both, in the order they should run:

```json
"files": [
  "glossary.md",
  "load-reference-data.ipynb",
  "governance-definitions.md"
]
```

Unlisted `.md` files still run, after the listed files. Unlisted notebooks do not, unless `"notebooks": "all"` is set.

### Choosing a canary

The canary decides whether a batch heals itself. After a reset, the Portal looks for one `ACTIVE` element of the canary's `type` whose `displayName` is exactly `name`. If it isn't there, the batch runs. Choose an element that the **last** file in the batch creates, so a run that stopped partway is retried:

```json
"canary": {"type": "DataSet", "name": "Coco Sales Forecast 2026"}
```

Leave `canary` out for a batch that should only ever run when someone asks.

### Placing the batch among the others

Batches run in the order given by `dr-egeria-inbox/_folder_order.json`, then alphabetically. A scanned batch's id is its path, so list it under that id:

```json
["Coco - 0. Data Governance Program", "…", "coco-workbooks/5. sales-forecast-consolidation"]
```

---

## Walkthrough: try it end to end

This walkthrough uses a small notebook that changes nothing in Egeria, so it is safe on any quickstart.

**1. Make a test folder.** In `coco-workbooks`, create `zz-notebook-test/` containing a notebook `hello.ipynb` with two code cells:

```python
import os
print("folder:", os.getcwd())
print("user:", os.environ.get("EGERIA_USER"))
```

```python
from pyegeria import EgeriaTech
tech = EgeriaTech(os.environ["EGERIA_VIEW_SERVER"], os.environ["EGERIA_VIEW_SERVER_URL"],
                  os.environ["EGERIA_USER"], os.environ["EGERIA_USER_PASSWORD"])
tech.create_egeria_bearer_token()
print(tech.get_servers_by_name("qs-view-server"))
```

**2. Add a manifest.** `coco-workbooks/zz-notebook-test/_batch.json`:

```json
{
  "displayName": "Notebook test",
  "description": "Read-only check of notebook runs. Delete after testing.",
  "defaultEnabled": false,
  "idempotent": true,
  "userid": "peterprofile",
  "files": ["hello.ipynb"]
}
```

**3. Find it in the panel.** Open the Admin page's **Data Initialization** section and reload. **Notebook test** is listed, switched off, marked **manual only**, with `hello.ipynb` shown as **as peterprofile**.

**4. Run it.** Switch it on and click **Run Now**. It should report `✓ 1/1 files ran clean`.

**5. Check the executed copy.** Open `runtime-volumes/quickstart-pyegeria-state/notebook-runs/zz-notebook-test-<id>/hello.ipynb`. The first cell's output shows the folder as `/coco-workbooks/zz-notebook-test` and the user as `peterprofile`. The second shows the view server's details.

**6. See a failure.** Add a third cell `1/0`, then Run Now again. The result reads `cell 3 of 3: ZeroDivisionError: division by zero` with the executed-copy path, and the executed copy now holds the traceback.

**7. Try the ordering.** Add a Dr.Egeria file before the notebook in `files`, or a second notebook after it, and check that the panel lists them in that order and runs them in that order.

**8. Clean up.** Delete `zz-notebook-test/`. The batch disappears from the panel on the next reload.

To test a real notebook, add it to its batch as in the recipes, and check the executed copy after Run Now.

---

## Troubleshooting

**The notebook isn't in the batch's file list.**
It isn't listed in `files`, and the manifest doesn't say `"notebooks": "all"`. Also check the path: it is relative to the folder holding the `_batch.json`. A wrong path shows in the batch's ordering/validation notes as "lists '…', which isn't there -- skipped".

**The new folder doesn't appear as a batch.**
In a scan root, only a folder with a `_batch.json` is a batch, and only the topmost one: a manifest inside a folder that is already a batch makes it part of that batch, not a new one. Freshstart has no scan roots unless `EGERIA_BOOTSTRAP_SCAN_ROOTS` is set.

**`ImportError` or `ModuleNotFoundError`.**
The notebook uses something the Portal's Python doesn't have: a module from the Jupyter image, a package that isn't installed, or a pyegeria function that was renamed or removed in the current release. See [Writing a notebook that runs here](#writing-a-notebook-that-runs-here).

**`FileNotFoundError` on a data file.**
Relative paths are resolved from the notebook's own folder. A path written relative to the Jupyter home directory (`/home/jovyan/…`) does not exist in the Portal container.

**Authentication errors, or elements created as the wrong user.**
The notebook isn't reading `EGERIA_USER` and `EGERIA_USER_PASSWORD`, or the manifest gives no `userid`. The panel shows which user each file runs as. A user's password comes from `EGERIA_BOOTSTRAP_PASSWORD_<USERID>`, then `EGERIA_USER_PASSWORD`, then the demo password `secret`.

**"timed out", or `CellTimeoutError`.**
A cell took more than 10 minutes, or the notebook more than 15. First look for a search run once per item, or a wait with no deadline: see [Techniques and best practices](#techniques-and-best-practices). If the slow cell only reports, tag it [`check-only`](#check-only-cells). Otherwise increase `BOOTSTRAP_NOTEBOOK_CELL_TIMEOUT_SECONDS` or `BOOTSTRAP_BATCH_TIMEOUT_SECONDS` on the Portal container, or split the notebook.

**The same batch keeps re-running every few minutes.**
Auto-heal stops a batch at its first failing file, so its canary, created later, never appears, and every check retries the batch. The batch's status line shows **✗ failed**. Fix that file, or tag its report-only cells `check-only`.

**`OMAG-COMMON-409-001` on a second run.**
The notebook looked an element up, didn't see it, and tried to create it again. See [Make every create safe to run twice](#make-every-create-safe-to-run-twice).

**Run Now asks for confirmation.**
The batch contains a notebook and its manifest doesn't say `"idempotent": true`. Confirm only if the batch's data isn't loaded yet, or if running it again is harmless.

**Duplicate elements after a re-run.**
The notebook creates without checking first. Make it look up before creating, or leave `idempotent` unset so Run Now keeps asking.

---

## Further resources

- [Data Initialization](data-initialization.md): the admin panel
- [Manifest and ordering file specs](data-initialization-manifests.md): every `_batch.json` field
- [Automatically Loading Dr.Egeria Files — User Guide](../../DR_EGERIA_AUTO_LOADING_GUIDE.md): recipes for Dr.Egeria folders
- [Jupyter](jupyter.md): the Jupyter environment the Coco workbooks are written for
