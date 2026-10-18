<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Automatically Loading Dr.Egeria Files in the Egeria Portal

User guide · updated 2026-10-08

The Egeria Portal's **Data Initialization** feature now loads Dr.Egeria files from subfolders, runs them in an order you control, and loads each file as the Egeria user who owns it. Existing folders keep working without changes. This guide covers what changed and how to use it.

## What's new

| Change | Before | Now |
| --- | --- | --- |
| Subfolders | Ignored unless given their own symlink in `dr-egeria-inbox` | Run inline, at their place in the parent folder's order |
| Order within a folder | `_batch.json` could list files only | `_batch.json` can list files, subfolders (`"sub/"`) and files inside subfolders (`"sub/x.md"`) |
| Leaving files out | Every `.md` file ran, including READMEs | `README.md` and output folders such as `dr-egeria-outbox` are skipped; a new `exclude` field skips others |
| Who a file runs as | Every file ran as Dr.Egeria's default user | A new `userid` field sets the Egeria user per folder or per file |
| Running a file twice | Possible when two batches reached the same file | Each file runs at most once per run; a folder with its own batch is skipped by its parent |
| Checking your setup | No feedback | The admin panel lists ordering and validation notes for each batch |
| Run history | Only in the activity log | Each file shows whether the Portal has run it, and whether it has changed since |

If you maintain a folder of Dr.Egeria files, check its notes in the admin panel once (see [Reading the admin panel](#reading-the-admin-panel)). Items listed there as "isn't in `_batch.json`'s files list" run in alphabetical order, which may not be the order you intended.

## How the Portal finds files

Each folder directly under `dr-egeria-inbox` is a **batch**. A folder can also be a symlink to content kept elsewhere; the Coco Pharmaceuticals workbooks are linked in this way. A new folder appears in the admin panel the next time the page loads, with no code change or restart.

Inside a batch, the Portal collects:

1. every `.md` file in the folder
2. every subfolder, at any depth, collected the same way

These are always skipped, unless you name them explicitly in `_batch.json`:

- `README.md` files
- the folders `dr-egeria-outbox`, `egeria-outbox`, `logs`, `data`, `templates`, `__pycache__` and `.ipynb_checkpoints`, and any folder whose name starts with `.`

The outbox folders matter most. They hold Dr.Egeria's processed copies of earlier runs, which still contain live commands, so running them would replay old content.

Files in subfolders appear in the admin panel with their path, for example `strategic-digital-products/catalog.md`.

## Controlling the order

Two optional files set the order: `_batch.json` inside a folder, and `_folder_order.json` in `dr-egeria-inbox` itself. Without them, everything runs alphabetically.

### Within a folder: `_batch.json`

The `files` list gives the order. An entry can be:

| Entry | Example | What runs |
| --- | --- | --- |
| A file | `"glossary.md"` | That file |
| A file in a subfolder | `"mapping-the-systems/egeria-implementation.md"` | That file, at this position |
| A subfolder | `"strategic-digital-products/"` | The whole subfolder, at this position, in its own order |

A subfolder runs in the order set by its own `_batch.json`, or alphabetically if it has none.

Anything not in the list still runs, after the listed items: first the `.md` files alphabetically, then the subfolders alphabetically. The admin panel flags each of these, because its position was defaulted rather than chosen. An entry that no longer exists is skipped and flagged.

This example follows the step order in a README, which mixes files and subfolders:

```json
{
  "displayName": "Coco - 1. Data Hub",
  "files": [
    "strategic-supply-chain-analysis.md",
    "extending-the-systems-inventory/",
    "mapping-the-systems/",
    "strategic-digital-products/",
    "solution-design.md",
    "software-development-governance-program.md"
  ]
}
```

Tip: if a folder's README describes a load order, copy that order into `files`. The Portal reads `_batch.json`, not the README.

### Across folders: `_folder_order.json`

This file sits directly in `dr-egeria-inbox`. It is a list of batch names (folder names), and the batches it names run first, in that order. Other batches follow alphabetically.

```json
["Coco - 0. Data Governance Program", "Coco - 6. Data Privacy", "Coco - 1. Data Field Naming", "Coco - 1. Data Hub"]
```

Use it when one folder creates elements that another folder's files refer to. Number prefixes in folder names are not enough when the dependency order isn't numeric.

## Leaving files out

There are two ways to stop a file from running. Use `exclude` for content that should never run. Use the admin panel checkboxes for a choice that applies only to this Portal.

- **`exclude` in `_batch.json`.** List files or subfolders that should never run, such as narrative documents that sit next to the command files:

  ```json
  "exclude": ["founders-briefing-script.md", "walkthrough.md"]
  ```

  An excluded file doesn't appear in the admin panel.
- **Checkboxes in the admin panel.** Untick a file to leave it out of this Portal's runs. The choice is saved for this Portal only and doesn't change the folder.

The admin panel flags any file that contains no Dr.Egeria commands. Such a file is usually prose and a good candidate for `exclude`.

## Who each file runs as

A `userid` in `_batch.json` makes the Portal load files as that Egeria user, so the elements they create are attributed to the person who owns them. Without one, a file runs as Dr.Egeria's default user (`erinoverview` unless `EGERIA_USER` is set).

Set it for a whole folder, or per file with the object form of a `files` entry:

```json
{
  "userid": "erinoverview",
  "files": [
    {"file": "jules-90-day-plan.md", "userid": "juleskeeper"},
    {"file": "privacy-governance-program.md", "userid": "faithbroker"},
    "employee-glossary.md",
    {"file": "mapping-the-systems/", "userid": "peterprofile"}
  ]
}
```

Here `employee-glossary.md` runs as `erinoverview`, the folder's default. The `mapping-the-systems/` entry sets the default for everything in that subfolder.

When several settings apply, the most specific one wins:

1. the file's own entry in its folder's `_batch.json`
2. the `userid` of the `_batch.json` in the file's folder
3. the setting passed down from parent folders: the parent's entry for this subfolder, else the parent's `userid`, and so on up

**Passwords never go in `_batch.json`.** The Portal takes the password from the environment of the Portal container:

| Order | Source | Example |
| --- | --- | --- |
| 1 | `EGERIA_BOOTSTRAP_PASSWORD_<USERID>`, userid in upper case | `EGERIA_BOOTSTRAP_PASSWORD_JULESKEEPER` |
| 2 | `EGERIA_USER_PASSWORD` | |
| 3 | `secret`, the demo personas' password | |

Running a file as a different user changes who owns the elements it creates. That can change who can see them, because visibility follows governance zones. Check the result in Egeria Explorer after the first run with a new `userid`.

## When files run

Files run only for **enabled** batches, and only on one of three triggers. Adding or changing a file does not run it by itself.

| Trigger | What runs | When |
| --- | --- | --- |
| **Auto-heal** | Every enabled file in the batch, in order; stops at the first failure | The batch has a `canary` in `_batch.json`, and the Portal finds the canary element missing. It checks at startup and every 10 minutes. |
| **Run Now** on a batch | That batch's enabled files, in order; carries on after a failure | An admin clicks it |
| **Run All Enabled** | Every enabled batch in `_folder_order.json` order | An admin clicks it |

A **canary** is one element the batch creates, named in `_batch.json`:

```json
"canary": {"type": "InformationSupplyChain", "name": "Data Subject Rights Information Supply Chain"}
```

If that element is missing, the Portal assumes Egeria was reset and reloads the batch. Point it at something the last file creates, so that its presence means the whole batch loaded. A canary from an early file lets an interrupted reload look finished, and the batch is never retried. A batch without a canary never runs on its own.

**Each file runs at most once per run.** Two batches can reach the same file, for example through two symlinks to one folder. In that case the file runs in the first batch, and the second batch reports it as `duplicate`, which is not counted as a failure.

**Adding a file to a batch that's already loaded doesn't run it.** The canary is still present, so auto-heal has nothing to do. Use **Run Now** on that batch. Every Dr.Egeria command updates an element that already exists rather than creating a copy, so re-running the batch's other files is safe. The exception is a batch whose `_batch.json` sets `"idempotent": false`. The panel asks you to confirm before re-running one of those.

## Reading the admin panel

Open **Admin → Data Initialization**. Each batch lists its files in run order. Each file can carry these marks:

| Mark | Meaning |
| --- | --- |
| ✓ | The Portal last ran this file successfully, and it hasn't changed since. Hover for the time. |
| **changed since last run** | The Portal ran it, but the file has been edited since. Use **Run Now** to load the changes. |
| `·` | The Portal has no record of running it. It may still be loaded: files run from a notebook, Obsidian or the command line, or before this feature, show `·` too. |
| **no commands** | No Dr.Egeria commands found; probably prose. Consider `exclude`. |
| as *userid* | The Egeria user this file is loaded as |
| default user | No `userid` applies; it runs as Dr.Egeria's default user |

Under each batch, **ordering/validation notes** lists anything worth checking:

- a file or subfolder not in `_batch.json`'s `files` list, which runs alphabetically after the listed ones
- an entry in `files` that no longer exists
- a file with no Dr.Egeria commands
- a subfolder that runs as its own batch instead of inline (for information only)
- a file that another batch also reaches

A batch with no notes is running exactly the order its `_batch.json` sets.

## Recipes

### Add a new folder of Dr.Egeria files

1. Put the folder, or a symlink to it, in `dr-egeria-inbox`.
2. Add a `_batch.json` with `displayName`, the `files` order, any `exclude`, and a `userid` if the files have an owner.
3. To have it reloaded after a reset, add a `canary` naming an element one of the last files creates.
4. If it depends on another folder, add it to `_folder_order.json` after that folder.
5. In the admin panel, enable the batch, read its notes, and click **Run Now**.

### Add a file to an existing folder

1. Drop the file in.
2. Add it to `files` at the right position, with its `userid` if it differs from the folder's.
3. In the admin panel, check that the batch shows no new notes, then click **Run Now**. Auto-heal won't run the new file for you.

### Add a subfolder to an existing folder

1. Drop the subfolder in, with its own `_batch.json` if its files need an order or a `userid`.
2. Add `"subfolder-name/"` to the parent's `files` at the right position.
3. Click **Run Now** on the parent batch.

### Give a nested folder its own batch

Use this when a subfolder needs its own canary, its own checkbox, or its own place in `_folder_order.json`.

1. Create a symlink to the subfolder directly in `dr-egeria-inbox`.
2. Give the subfolder a `_batch.json` with its own `displayName` and `canary`.
3. Add the new batch to `_folder_order.json`.

The parent then skips that subfolder and shows a note saying it runs as its own batch. Remove the symlink to fold it back into the parent.

## Troubleshooting

| Symptom | Likely cause | What to do |
| --- | --- | --- |
| A new folder doesn't appear | It contains no `.md` files outside skipped folders, or its name starts with `.` | Check where the files are; name an otherwise-skipped folder in `files` if you really want it |
| A new file appears but its elements aren't in Egeria | Adding a file doesn't run it, and the canary is still present | Click **Run Now** on the batch |
| A batch is never reloaded after a reset | It's not enabled, or it has no `canary` | Enable it; add a `canary` |
| Files run in the wrong order | They're not in `files`, so they run alphabetically after the listed ones | Check the batch's notes; add them to `files` |
| A file fails with an authentication error | Its `userid` doesn't exist, or the password is wrong | Check the user in Egeria; set `EGERIA_BOOTSTRAP_PASSWORD_<USERID>` |
| Elements created are hidden from some users | They are now owned by the file's `userid`, and visibility follows governance zones | Check the zones of the elements and of the viewing user |
| A subfolder doesn't run with its parent | It's its own batch through a symlink in `dr-egeria-inbox` | Expected; the parent's notes say so. Remove the symlink to run it inline |

For details of a failure, open **Admin → Activity Log**. It shows one line per file run, plus Dr.Egeria's own errors and warnings.

The full reference for `_batch.json` and `_folder_order.json` is in [Data Initialization — manifest and ordering file specs](portal-docs/tools/data-initialization-manifests.md).
