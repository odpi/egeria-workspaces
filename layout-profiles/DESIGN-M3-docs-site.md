# M3 design note: a `docs-site` profile (names and sizes only)

Update after building it (README, section "M3"): the profile is built as described below, with two corrections from the reviewed tuning keys:
sections in the tutorial sample are FILES, not sub-folders with a landing page, so no rule finds sections; and step copies are reported by a
names-only `--copies-of` report, not hidden. The rest of this note is the design as first written.

Status: a design note, no code. M3 is "a docs-site profile from the section layout (and, later, mkdocs.yml's nav)", tuned on a documentation tree
that is NOT the egeria-docs corpus. This note says what such a profile can recognize from names alone with the engine as it stands after M2,
what it cannot, and what to decide before building it. Nothing here was run on the held-out repositories, and no file content was read.

## What was looked at (names and sizes only)

1. **The trellis `docs/` folder** at the keyed commit (the path list only): 34 files, no `mkdocs.yml`, no images; one flat folder of about 30
   design, plan and audit documents (`*.md`) with a `README.md`, and two sub-folders, `experiments/` (4 files) and `archive/` (2 files). It is a
   *documentation folder*, not a site: nothing declares navigation.
2. **The mkdocs tutorial sample** (a public tutorial repository with one finished project and numbered step copies): several complete project
   copies side by side (`source_code_step_N/`, `source_code_final/`), most with a `mkdocs.yml` and a `docs/` beside it holding `index.md`,
   `tutorials.md`, `how-to-guides.md`, `reference.md`, `explanation.md` (the four-part documentation layout), one with a built `site/` folder
   (`404.html`, `index.html`, `sitemap.xml`), a `venv/`, and a source package next to the docs. It is a *site that is repeated*: the same docs tree
   appears in a copy per step.

Two shapes, therefore: a docs folder with no site machinery (trellis), and a site with machinery plus build output plus copies (the sample).

## What names alone can say

| signal (names only) | claim | role and kind | note |
|---|---|---|---|
| a directory holding `mkdocs.yml` or `mkdocs.yaml` | this directory is a docs site | component, kind `docs-site` (manifest, high) | a manifest rule, the same shape as the code-repo ones |
| `docs/` directly beside that file (`parent_has_file: mkdocs.yml`, `name: docs`) | the site's content root (mkdocs' default `docs_dir`) | docs, supporting | the real `docs_dir` is a setting inside the file: not readable here, so this is the default only, with confidence medium |
| `site/` directly beside it | the default build output | generated, hidden subtree | a dir rule with `grain: subtree` already exists in the engine; the name is mkdocs' default `site_dir` |
| `overrides/` beside it, `snippets/` or `includes/` under the docs root | theme overrides and include fragments | supporting / hidden-from-nav candidates | fragments are pulled in by pages, they are not pages: a docs site with thousands of them would otherwise look like thousands of documents |
| a sub-folder of the docs root that holds an `index.md` (or `README.md`) | a *section* of the site (its landing page names it) | docs, kind `docs-section` | the section list is the top-level layout; nesting is kept by `part_of` |
| `archive/` under the docs root | not part of the live documentation | archive, hidden | trellis `docs/archive/` is the instance and the only name that occurs in a tuning tree; as with every convention it carries `tuned_on` |
| `experiments/` under docs | a working area, not a section | scratch or supporting (undecided) | only trellis has it: do NOT make a rule from one repository |
| images and diagrams (`png`, `svg`, `drawio`) under the docs root | assets of pages | docs assets, counted but not shown | a file-name rule, like the logs rule |

Everything above uses keys the engine already has (`has_file`, `parent_has_file`, `name`, `path_glob`, `path_segment`, `extension`, directory
rules, subtree grain). No new schema key is needed for a names-only M3.

## What names alone cannot say (and the options)

1. **The navigation.** The nav tree lives in `mkdocs.yml`; sections by folder are a proxy that fails when the nav reorders, renames or omits
   pages. Reading the file is reading a manifest's *contents*, which Phase 1 does not do (the decision is the owner's). Recommendation: M3 ships the names-only profile and reports
   the nav comparison as a later step that needs that decision, for manifests only.
2. **`docs_dir` and `site_dir`** when they are not the defaults (same reason).
3. **A site that is repeated.** The sample shows the same docs tree in six copies. Names cannot tell the live one from a step copy, nor can a
   name pattern; the duplicate-tree test already on the backlog (same file names and sizes under two roots) would, and it is the same test that
   would replace the worktree-name rule. Until then every copy is a `docs-site` component with a `part_of`/sibling relation we cannot state.
4. **Content-derived structure** (the four-part layout is recognizable from names here, but only because this author used the conventional file
   names).

## Proposed shape of the profile (for review, not built)

`docs-site` 0.1.0, `applies_to: docs-site`, `extends: [generic-relevance]` (so `venv`, `node_modules`, build output are already hidden):
(1) manifest rule for `mkdocs.yml`/`mkdocs.yaml` (component, docs-site); (2) `docs` beside it (docs, medium); (3) `site` beside it
(generated subtree); (4) sections by an `index.md`/`README.md` in a sub-folder of the docs root (component kind docs-section, judgement, low,
parts of the site); (5) an `archive` folder under the docs root (archive, hidden, `tuned_on: [trellis]` and therefore flagged as a
one-repository rule); (6) image files as counted assets. Order: site root first, its default children next, sections last. No rule for
`experiments/`.

## Acceptance for M3, and a gap in the corpus

The brief asks for a docs profile tuned on a tree that is not egeria-docs. There is **no answer key** for the trellis docs folder or the
tutorial sample, so there is nothing to score against yet. Needed from the reviewer: either (a) a small draft key for the tutorial sample (which
folder is the site, which are sections, which are copies) and for the trellis `docs/` folder (one documentation component, two or zero sections),
or (b) agreement that M3's acceptance is a names-only regression on these two trees (the profile finds one `docs-site` per `mkdocs.yml`, the
`site/` output is hidden and counted, the four sections of the sample are found, the trellis folder is one documentation component with
`archive/` hidden). I recommend (b) now and (a) before M4, because a key written after seeing the held-out result would be worthless.

## Questions to settle before building

1. Is a docs folder with no `mkdocs.yml` (trellis) a component at all, or only the generic `docs` convention that M2 already claims? (M2's
   `R-conv-docs` claims a top-level `docs` directory; a `docs-site` profile composed with it should not double-claim: the more specific
   `mkdocs.yml` rule must come first.)
2. Do step or version copies of a site (the sample) count as separate sites? (blocked on the duplicate-tree test.)
3. May the nav be read from `mkdocs.yml` (owner's decision), and if yes, only for `mkdocs.yml`?
4. Who writes the draft keys for the two tuning trees, and before or after the profile?
