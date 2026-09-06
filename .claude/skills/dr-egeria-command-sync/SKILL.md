---
name: dr-egeria-command-sync
description: >
  Use this skill any time the user wants to add, change, or remove a Dr.Egeria
  command or attribute, regenerate Dr.Egeria templates/help/report specs, run
  refresh_specs, validate_compact_specs, gen_md_cmd_templates, gen_dr_help, or
  gen_report_specs, or sync Dr.Egeria templates and help content across the
  egeria-python, egeria-workspaces, and egeria-advisor repos. Covers the full
  lifecycle: compact-spec edits made directly through the Dr.Egeria Spec
  Editor's local REST API (the sole edit path as of 2026-08-05 - Tinderbox is
  retired, this repo's compact JSON is the system of record, no mirroring/
  re-export step) -> compact command JSON in egeria-python -> refresh_specs
  regeneration -> updating the dr-egeria Glossary -> propagating templates/
  help files to egeria-workspaces (Egeria Portal) and egeria-advisor. Trigger
  this even when the user only describes a desired command change in plain
  language ("I want a new attribute on Create Term", "the Data Designer
  family needs a new command") without naming any of these tools directly.
---

# Dr.Egeria command lifecycle sync

Dr.Egeria commands are not edited directly in the processor code — the spec
that drives templates/help/report-specs lives in compact command JSON. Make
compact-spec edits (attributes/bundles/commands) yourself through the
Dr.Egeria Spec Editor's local REST API — a FastAPI app at
`commands/tech/spec_editor.py`, launched via `dr_egeria_spec_editor`
(`http://localhost:8420` by default; `uv sync --extra spec-editor` one-time).
**Tinderbox is retired** (confirmed by the user 2026-08-05: they will not
maintain the Tinderbox file going forward) — this repo's compact JSON is the
sole system of record. There is no mirroring or re-export step; once the API
edit + regeneration + processor wiring are done and verified, the change is
complete. Several generated artifacts (templates, help glossary, report
specs) get rebuilt from the compact JSON and pushed out to two downstream
repos; this skill walks that whole chain so nothing gets missed or left
stale.

## Mental model

```
Dr.Egeria Spec Editor REST API (localhost:8420)  <- Claude edits here directly;
        |                                            sole system of record,
        |  refresh_specs                             no mirroring step
        v
egeria-python/md_processing/data/compact_commands/*.json   <- never hand-edit
        |                                                      the JSON text
        v                                                      directly - go
  +-----------------+-----------------+---------------------------+  through
  |                 |                 |                           |  the API
templates       help glossary     report specs (FormatSets)        above
(sample-data/    doc (dr-egeria-   (pyegeria/view/
templates/)      help-*.md)         base_report_formats.py)
        |             |
        | mirror-copy | dr_egeria --process
        v             v  (creates/updates "dr-egeria" Glossary)
  egeria-workspaces   Egeria server
  egeria-advisor
```

Things that make this lifecycle easy to get wrong, learned from the current
state of the repos (see `references/repo_paths.md` for full history/detail):

1. **Compact command JSON files are edited through the Spec Editor API,
   never hand-edited, and Tinderbox is not part of the loop at all.** If the
   user wants a new/changed command or attribute: make the edit yourself via
   the Spec Editor's REST API (see Step 1) — don't hand-edit the JSON text
   directly (the API does structural validation — bundle-chain resolution,
   unknown-attribute checks, duplicate-name checks — that raw editing
   skips). Once the API edit lands and the downstream steps below are done,
   the change is complete — there is nothing to hand off to the user for
   Tinderbox, and nothing pending on their side.

   Before proposing what a new/changed command should look like, ground it in
   what's actually real rather than guessing — check, in roughly this order:
   - `egeria-python/pyegeria/omvs/` — what the relevant OMVS client can
     actually call; a command is only useful if there's a real method behind
     it.
   - `egeria-python/pyegeria/http clients/Egeria-api-*.http` — worked example
     REST calls (URL + body shape) for that OMVS, useful for confirming exact
     attribute names/types.
   - `/Users/dwolfson/localGit/egeria-v6/egeria/open-metadata-implementation`
     — the local odpi/egeria core repo; the type-system source of truth for
     valid attributes, relationships, and classifications.
   - `/Users/dwolfson/localGit/egeria-v6/egeria-advisor/data/repos/egeria-docs/site/docs/reference`
     — a local copy of the Egeria docs reference section, better for
     structural/conceptual questions (what a type means) than for exact API
     shapes.
   - For live interrogation of what's actually deployed on a running Egeria
     server, see `type_system_handler.py` in
     `egeria-workspaces-fs/compose-configs/egeria-quickstart/PyegeriaWebHandler/`
     for how to query the type system directly.

2. **Template propagation must be a mirror, not an additive copy.** The old
   `egeria-workspaces` checkout's copy went stale for ~6 months because
   commands were added/renamed upstream and nobody removed the old family
   folders downstream. Always sync with delete-of-stale-files semantics (the
   bundled script does this with `rsync --delete`), never just copy new files
   on top of old ones.

3. **Two local checkouts of egeria-workspaces exist — use the `-fs` one.**
   `/Users/dwolfson/localGit/egeria-v6/egeria-workspaces-fs` is the active
   working copy (same GitHub repo, different clone) and is what the Portal
   app's `PyegeriaWebHandler` actually reads templates from at runtime. The
   plain `egeria-workspaces` checkout is stale — don't sync into it.

4. **Tinderbox is retired — don't tell the user to mirror anything there.**
   `DrEgeria-Specs-<Month>.tbx` was the long-term source of truth for full
   re-exports before 2026-08-05; the user has since confirmed they will not
   maintain it going forward. `references/tinderbox_export.md` is kept only
   as historical background (useful for understanding *why* the compact
   JSON is shaped the way it is, and for the rare case where the Spec
   Editor's scope genuinely can't express a change — e.g. creating brand-new
   cross-family structure — where its manual-export mechanics might still
   inform how to hand-craft something), not as an active step in this
   skill's lifecycle.

## Step 1 — Make the compact-spec edit through the Spec Editor API

Confirm the Spec Editor is running (`GET http://localhost:8420/api/families`
— if that fails to connect, start it: `dr_egeria_spec_editor`, from the
`egeria-python` repo root, backgrounded or in its own terminal).

Ground the proposed change in what's actually real (see the checklist above
this step — OMVS client methods, `.http` worked examples, the local Egeria
type-system checkout, live type queries) before making any edit.

Then make the edit directly via the REST API:
- `GET /api/families/{family}` — fetch the current family JSON (also
  returns `attribute_sharing`, showing which other families already define
  a given attribute name — check this before adding a duplicate).
- `POST /api/families/{family}/attributes` `{"name": ..., "definition":
  {...}}` — add a new attribute; `PUT .../attributes/{name}` to change one;
  `DELETE .../attributes/{name}` to remove one (fails with 409 if still
  referenced by a bundle/command — the response names the referencer).
- Same `POST`/`PUT`/`DELETE` shape for `.../bundles/{name}` and
  `.../commands/{name}`. Bundle/command edits are validated server-side
  (unknown attribute names, unresolvable `"inherits"` chains) — a 400
  response means fix the definition, not that something is broken.
- `POST /api/families` `{"family": "New Family Name"}` — scaffold a brand
  new family file (rare; most changes target an existing family).
- `POST /api/validate/{family}` — runs the same `validate_compact_json`/
  `validate_compact_specs` checks the CLI does; call this after any edit
  and fix anything it flags before moving on.

If the requested change is bigger than the API's scope (e.g. brand-new
cross-family structure, not just attributes/bundles/commands within an
existing family), discuss the design with the user directly and, if useful,
consult `references/tinderbox_export.md`'s document-structure notes for
background on how families were previously organized — not to hand the
change off to Tinderbox, just as a source of structural conventions.

Once the edit is confirmed valid, also run the CLI validator for a second
confirmation and to match the rest of this skill's existing habits:

```bash
cd /Users/dwolfson/localGit/egeria-python
source .venv/bin/activate   # or prefix subsequent commands with `uv run`
validate_compact_specs
```

## Step 2 — Regenerate templates, help doc, and report specs

```bash
refresh_specs --merge-reports
```

This runs, in order: `generate_md_cmd_templates` (Basic + Advanced) ->
`generate_dr_help` (Basic + Advanced) -> `gen_report_specs --merge`. The
`--merge-reports` flag is what actually persists the new report specs into
`pyegeria/view/base_report_formats.py` — without it the specs are generated
but not written back into the module that `EgeriaTech` consumers rely on.

Outputs to note:
- Templates: `sample-data/templates/{basic,advanced}/<Family>/*.md`
- Help doc: a **new timestamped file**,
  `sample-data/egeria-inbox/dr-egeria-inbox/dr-egeria-help-<ISO8601>.md`
  (find it with `ls -t sample-data/egeria-inbox/dr-egeria-inbox/dr-egeria-help-*.md | head -1`)
- Report specs: diff in `pyegeria/view/base_report_formats.py`

Run the unit tests before going further — no live server needed:

```bash
pytest -m unit
pytest tests/micro-tests/test_gen_report_specs.py
```

## Step 3 — Verify processing code actually handles the change

**Mandatory, not optional — do this even if the change "looks like" pure
data.** A new/changed `custom_attributes` entry landing in the compact JSON
and flowing through to a regenerated template proves the *spec* changed; it
proves nothing about whether the *processor* that executes the command was
ever taught to read that attribute. These are two independent systems that
only happen to be edited in the same session — regenerating one does not
regenerate the other.

**Learned the hard way (2026-07-06):** a `Sub-Projects` attribute was added
to `Create Project` in Tinderbox, exported, and propagated through templates/
help/Glossary — a full skill run, reported as done — before anyone checked
whether `ProjectProcessor.apply_changes()` in `md_processing/v2/project.py`
actually read it. It didn't. The field validated fine, rendered fine in the
template, and silently dropped every value a user typed into it at execution
time. This was only caught because the user asked directly afterward.

For every command whose `custom_attributes` list changed in this session's
diff (added, removed, or renamed — check `git diff` on the compact JSON
files, not just the template diff, since template diffs can be dominated by
unrelated shared-attribute-pool noise):

1. **Find the processor.** Check the dispatcher registration in
   `md_processing/dr_egeria.py` (`setup_dispatcher()`) or the family-specific
   module under `md_processing/v2/` (e.g. `project.py`, `glossary.py`,
   `solution_architect.py`, `governance.py`) for which `AsyncBaseCommandProcessor`
   subclass handles this command.
2. **Grep `apply_changes()`** (and any helper methods it calls, e.g. a
   `_sync_*` method) for the attribute's display name or `variable_name`
   (e.g. `attributes.get('Sub-Projects', ...)`). If it's a
   `Reference Name`/`Reference Name List` style attribute meant to establish
   a relationship, look for the existing sibling pattern first —
   `BlueprintProcessor._sync_components()` in `solution_architect.py` and
   `ProjectProcessor._sync_sub_projects()` in `project.py` are the reference
   shape (fetch as-is via the element GET endpoint's nested relationship
   field, diff against the to-be guid list, issue add/remove calls through
   `self.sync_members()` in `processors.py`) — don't invent a new shape.
3. **If the attribute isn't read anywhere:** this is a real gap, not a style
   nit. Report it explicitly and either implement the missing handling now
   (mirroring the sibling pattern) or get an explicit decision from the user
   to defer it — never silently proceed to Steps 4-8 leaving it unhandled.
4. **If you do implement it:** verify against a live server before calling it
   done, not just a `--validate` pass — validation only proves the attribute
   parses and resolves to a guid_list, not that the write call fires
   correctly. Use throwaway test elements, confirm the actual relationship
   via a direct element fetch (don't trust an intermediate "any relationship"
   listing endpoint without cross-checking — `_async_get_linked_projects`
   returned "No elements found" for a relationship that demonstrably existed
   in `_async_get_project_by_guid()`'s own `managedProjects` field), then
   delete the throwaway elements afterward.

Data-driven families and anything covered by `COLLECTION_SUBTYPES`/
`PROJECT_SUBTYPES` auto-routing may genuinely need no processor change for
some kinds of edits (e.g. a new scalar property that flows through the
generic `set_element_prop_body()` path) — but a new relationship-establishing
attribute (`Reference Name`/`Reference Name List` style) almost always needs
explicit wiring, since those aren't generic. Don't assume "no code change
needed" — check.

## Step 3b — (Optional) Regression test markdown + runner

Once Step 3 confirms the processing code is correct (whether it needed a
change or not), offer to write regression coverage for the new/changed commands as
Dr.Egeria markdown documents, plus a runner script, both living together in
`egeria-python/tests/dr-egeria-command-tests/` — this is optional, so raise
it with the user rather than generating it unprompted; realistic sample
values for a new command are often easier for them to supply than to guess.

`egeria-python/tests/dr-egeria-command-tests/` already exists (migrated
2026-07-02 from the older split of `tests/scenario-tests/run_dr_tests.py` +
`dr_test_*.md` fixtures scattered under
`sample-data/egeria-inbox/dr-egeria-inbox/`, which mixed test fixtures into
a scratch working folder). It holds 12 existing `dr_test_*.md` files and
`run_dr_tests.py`, which resolves them by **absolute path** so the folder is
self-contained. To add coverage for a new change:

1. Add one markdown file per family or per change,
   `dr_test_<family_or_topic>.md`, with Dr.Egeria command blocks exercising
   the new/changed commands (Create/Update/View/Link as relevant). Look at
   the existing files in this folder for the shape/style to match.
2. Add the new filename to `run_dr_tests.py`'s `TEST_FILES` list. (If this
   folder or script is ever missing — e.g. a fresh clone predating the
   migration — recreate the script from
   `~/.claude/skills/dr-egeria-command-sync/scripts/run_dr_tests_template.py`.)
3. Run it in validate mode first (the default — no live writes):
   ```bash
   python tests/dr-egeria-command-tests/run_dr_tests.py
   ```
   Only pass `--process` once the user confirms they want to write these
   test elements to a live Egeria server, and confirm which server first —
   same caution as step 4 below.

## Step 4 — Update the dr-egeria Glossary (help content)

The generated help file is itself a Dr.Egeria document: its first command
creates the `dr-egeria` Glossary if it doesn't already exist, then it emits a
`Create Term` per command family and per command. This is what backs the
`dr_egeria_help` search tool — the help content only takes effect once this
file is processed against a running Egeria server, it isn't just a static
doc.

This writes metadata to a live server, so confirm the target rather than
silently assuming — the usual default is a local instance at
`https://localhost:9443` (view server `qs-view-server` — note
`egeria-python/config/config.json` incorrectly says `qs-view-server2`;
confirmed by the user 2026-07-08 that the real server name has no "2"), but
confirm it's actually up and that's still the intended target before
proceeding. Then:

```bash
dr_egeria <path-to-dr-egeria-help-*.md> --process
```

Prefer `--validate` first if there's any doubt about the diff size — this
file can be large (100+ commands) and a validate pass shows exactly what will
change without committing it.

## Step 5 — Propagate templates to downstream repos

Run the bundled sync script, which mirrors (not merges) the generated
`basic`/`advanced` template trees into both downstream repos:

```bash
bash ~/.claude/skills/dr-egeria-command-sync/scripts/sync_templates.sh
```

It prints an `rsync` summary of what was added/changed/removed in each
destination. Review that output — a large number of deletions is expected the
first time this runs after a long gap (see the mental-model note above), but
a large number of deletions on a routine run is worth double-checking with
the user before treating as normal. It also removes an accidental nested
`templates/templates/` duplicate directory in `egeria-workspaces-fs` if still
present (leftover from a past mistaken copy, unrelated to this pipeline).

Destinations (see `references/repo_paths.md` if these ever need to change):
- `egeria-workspaces-fs/templates/{basic,advanced}/<Family>/` — this is what
  the Portal app's `PyegeriaWebHandler` reads from at runtime
- `trellis/config/dr-egeria-templates/{basic,advanced}/` (moved 2026-09-06 from
  `trellis/packages/egeria-advisor/examples/templates/` — repo-level, not package-level)

## Step 6 — Update documentation

`refresh_specs` and the template sync only touch generated artifacts — every
hand-written doc that mentions families or commands by name has to be
checked and updated as part of this same pass, not left for later. Work
through `references/documentation_surfaces.md`, which lists every known doc
across all three repos plus the in-Tinderbox README notes, with what in each
one tracks the command surface.

For each entry: compare it against the family/command diff from this run. If
it mentions something added, removed, or renamed, edit it now — these are
plain text edits, safe to make directly (the user reviews via `git diff`
same as the template sync). If a doc genuinely isn't affected by this
specific change, say so explicitly in the final report rather than silently
skipping it, so the user knows it was checked, not missed.

Keep `references/documentation_surfaces.md` itself current — if you find a
doc that references the command surface and isn't on that list, add it so
future runs don't miss it.

## Step 7 — Report and hand off for review/commit

Do **not** commit or push in `egeria-workspaces-fs` or `egeria-advisor` as
part of this skill — those are separate repos with their own review process.
Instead, summarize for the user:
- Which families/commands were added, changed, or removed (from the compact
  JSON diff and the `rsync` output)
- Whether Step 3's processing-code check found a gap, and what was done about it
- Whether regression tests were added in step 3b, and their validate-mode
  results
- The path to the new help markdown file and whether step 4 was run
- Which docs were edited in step 6, and which were checked but found
  unaffected
- `git status` in all three repos so the user can review and commit each one
  themselves
