# layout-profiles: layout profile model v0 and the repo recognizer (Phase 1, milestone M0)

Today the Resource Explorer treats every folder as an asset (2.6 million "assets" in egeria-v6). This folder holds, standalone and with no
RE, no Egeria and no platform involved:

1. a small versioned **profile document** (YAML, not an Egeria type) that says which paths are components, source, tests, docs, config, and
   which are generated, vendored, runtime output, copies, backups or VCS internals; every rule carries its basis, confidence and evidence;
2. a **recognizer** that applies a profile to a list of repo-relative paths (names and sizes only, never contents) and writes components,
   findings with stable ids, class counts with hidden-but-counted figures, and a short report.

Status: M0 (schema, loader, `generic-relevance`, the recognizer, synthetic tests, the egeria-v6 numbers check) plus M1 (findings per
(rule, directory), `components-all.txt`, the `worktree-copies`, `egeria-workspace` and `code-repo` profiles, the manifest-probe regression).
Everything here is `proposed`: only a person confirms a profile.

## Use

```
cd layout-profiles                     # PyYAML and the standard library only
python -m recognizer.recognize PATHLIST --out OUTDIR [--profile generic-relevance] [--profiles-dir profiles]
python recognizer/gitlist.py REPO COMMIT OUT.tsv      # the files of ONE commit (git ls-tree -r -l: names and sizes, no contents)
python recognizer/listpaths.py ROOT OUT.tsv           # a walk that does not follow symlinks (for a tree that is not git)
python -m pytest tests                                 # set LAYOUT_EGERIA_V6_PATHS=<egeria-v6 path list> and LAYOUT_TUNE_PATHS_DIR=<dir with
                                                       # trellis/datahub/superset .paths.tsv> to run the data-dependent tests (else they skip)
```
PATHLIST is one path per line, optionally `path<TAB>size`. It must be sorted to be streamed (otherwise it is sorted in memory); a duplicate,
absolute or `..` path is an error. `components.txt` is one directory per line, the input format of the Phase 0 scorer (kept outside this repository); answer keys are never copied or edited.

Outputs in OUTDIR, byte-identical for the same input and profile (checked on the 2.6M-path list too): `components.txt` (top-level components),
`components-all.txt` (top-level plus the parts of components), `findings.jsonl`, `classes.json`, `report.md`; with `--per-file` also
`findings-files.jsonl` (one finding per file, large, for debugging).

## The profile document

See `profiles/generic-relevance.yaml` and `recognizer/layout_profile.py`. In short: `profile_id`, `version` (semver; a rule change bumps it),
`status` (proposed | confirmed | retired), `applies_to`, optional `extends: [a, b]` (the child's rules first, then a's, then b's), `roles`,
`relevance` (role -> primary | supporting | hidden), ordered `rules`, and schema-only `path_grammar` / `name_grammar`.

A rule: `id`, `match`, `assign {role, kind?, relevance?}`, `grain`, `basis`, `confidence`, `evidence`. The loader rejects: an unknown key at any
level, an unknown role or relevance, a role with no relevance, a duplicate rule id, a rule without evidence, a subtree rule that cannot say
where the subtree starts, a bad regex, and an `extends` cycle.

**Matching.** Rules are tried in order and the FIRST match wins. `path_segment` matches a *directory* segment anywhere in the path (never the
file name). `name`, `extension` (a suffix, so `.sql.gz` works) and `name_regex` (a search) test the file name. `path_glob` tests the whole path
(`*` within a segment, `**` across segments). `has_file` / `parent_has_file` test a directory (does it, or its parent, hold a file of that
name); they cannot be combined with `extension` or `path_glob` in v0. Several keys in one rule must all match.

**Grain.** `subtree`: everything below the matched directory gets the role, and ONE finding is written for the subtree root (the shallowest
matching directory). `dir`: only the matched node, a file for a file-name rule and a directory for a directory rule. `component`: the directory
is a component (it must come from `has_file` / `parent_has_file`); the files inside are not re-labelled, they go on through the other rules.
A component nested inside another component is a **part** of it: its finding carries `part_of`, and only top-level components are listed in
`components.txt`. A more specific earlier rule can say otherwise (see `test_a_more_specific_rule_can_make_a_nested_manifest_an_example`).

**Findings.** One finding per (rule, directory) that a rule claimed: the subtree root for a subtree rule, the directory holding the file for a
file-name rule, the directory itself for a component. `finding_id = sha256(profile_id + "@" + version-major + "|" + rule_id + "|" + path)[:16]`
where path is that directory: no time, run id, tree sha or count, so the same node keeps its id across surveys, and a minor or patch bump of
the profile keeps ids (a major bump changes them). Fields: finding_id, path, role, kind, relevance, rule_id, basis, confidence, evidence,
grain, profile_id, profile_version, files and bytes (what the rule claimed there; absent on a pure component claim) and `part_of` for a part.
Sorted by path then rule id.

**Hidden subtrees win.** A directory inside a subtree that a hidden-relevance path rule claims (node_modules, build, a worktree copy, ...)
can never be a component: a `pyproject.toml` inside `node_modules` is vendored, not a component.

## The numbers check (egeria-v6, listing only)

`recognizer/listpaths.py` walked an egeria-v6 working tree without following symlinks, reading names and sizes only (75 s), and the
recognizer classified that list in about 10 s with the `egeria-workspace` profile (generic-relevance, then worktree-copies last). Against the Phase 0 census of the same tree (kept outside this repository), counts are EXACTLY equal:

| class | rules | recognizer | census |
|---|---|---:|---:|
| all files | | 2,612,019 | 2,612,019 |
| vendored / build output | R-vend-installed + R-gen-build-output + R-gen-tool-cache | 1,113,920 | 1,113,920 |
| runtime events (.openlineageevent) | R-run-openlineage-event | 634,944 | 634,944 |
| logs | R-run-log | 623,778 | 623,778 |
| .git internals | R-vcs-git | 37,636 | 37,636 |
| backups | R-backup-dir + R-backup-file | 16 | 16 |
| heap dumps (.hprof) | R-run-heap-dump | 3 | 3 |
| worktree copies of residual files | R-copy-worktree-name (profile `egeria-workspace`) | 52,946 | 52,946 |
| residual (unclassified) | | 148,776 | 148,776 |

`tests/test_numbers_egeria_v6.py` asserts this (expected values in `tests/census_egeria_v6.json`) and that every file is in exactly one class.
Three things to know: (a) the census splits "vendored or build" as one class; here it is three rules and two roles (`vendored`: installed
packages; `generated`: build output and tool caches), so the test sums them. (b) The census decides `.git` versus a vendored directory by
position (the first segment wins), this profile by rule order; no path in egeria-v6 has both, so the counts cannot differ here, but they
could on another tree. (c) Since M1 the worktree-copy name rule lives in `worktree-copies` and is composed last by `egeria-workspace`;
`generic-relevance` 0.2.0 no longer has it, so on a plain code repository it does not apply.

## Tune-set class shares (committed trees, `generic-relevance` only)

File lists are `git ls-tree -r -l` of the keyed commit (never a working tree); symlinks and submodules skipped. superset's 5,511 equals the
Phase 0 `git archive d2cce51dd` count.

| repo @ commit | files | bytes | primary | supporting | hidden | unclassified |
|---|---:|---:|---:|---:|---:|---:|
| trellis @ 142bd786 | 4,470 | 105,293,226 | 0 | 0 | 0 | 4,470 (100%) |
| datahub @ bc0c3ef7ef2 | 7,273 | 84,342,076 | 0 | 0 | 0 | 7,273 (100%) |
| superset @ d2cce51dd | 5,511 | 230,285,594 | 0 | 0 | 0 | 5,511 (100%) |

That is the expected reading, not a failure: a committed tree holds no installed packages, build output, logs or VCS internals, so the
generic profile has nothing to hide, and it names no component (that is `code-repo`, M1). Its value shows on trees that were built and run
(egeria-v6: 94.3% hidden).

## M1: the code-repo profile and the manifest-probe regression

`profiles/code-repo.yaml` (extends `generic-relevance`): one component rule per manifest, first match per directory in this order:
pyproject.toml, setup.py, package.json, pom.xml, build.gradle, Cargo.toml, go.mod, Chart.yaml, Dockerfile, then metadata.yaml last (weaker:
a directory that carries only metadata.yaml). All are `basis: manifest`; every claim carries its evidence. A manifest nested inside a component
is a **part** of it (`part_of`), listed in `components-all.txt` only; the repository root is not a parent (see below).

Regression against the Phase 0 manifest probe: apply `code-repo`, take `components-all.txt`, drop the repository root and the directories
claimed only by metadata.yaml (the probe did not count that file), and score with the Phase 0 scorer (tune-set keys, provisional):

| repo @ commit | candidates | TP | Phase 0 baseline | note |
|---|---:|---:|---|---|
| trellis @ 142bd786 | 25 | 14 | 25 / 14 | reproduced |
| datahub @ bc0c3ef7ef2 | 82 | 65 | 82 / 65 | reproduced |
| superset @ d2cce51dd (5,511 files) | 37 | 30 | 37 / 30 (corrected; the earlier 33 / 27 was the pre-fix probe) | see below |

The superset figure of the first re-measure (34 manifest dirs, 33 candidates, TP 27) is what the Phase 0 probe produced BEFORE its own documented
bug fix (a manifest one directory down was collapsed to the root). Reproducing that bug on the same list gives exactly 34 dirs / 33 / 27
(and datahub 63 dirs, as the correction note says); the corrected probe, and this recognizer, give 38 dirs / 37 / 30, the corrected superset
figure of Phase 0. The in-repo test pins the candidate counts (25, 82, 37) when `LAYOUT_TUNE_PATHS_DIR` is set; scoring needs the keys, which are
not in this repository. No improvement is claimed: M1 reproduces the probe, M2 is where it has to be beaten.

**Root manifest.** A manifest at the repository root makes the root a component flagged `root: true` with `kind: root-project` (the manifest's
own kind is kept as `manifest_kind`); it does NOT make the other manifest directories its parts. Nested manifest directories are top-level
components, and a **part** exists only below a non-root component (for example an `examples/` manifest inside a package). So `components.txt`
(top-level components, including `.` for the root) stands on its own, and `components-all.txt` keeps every manifest directory. The Phase 0
scorer ignores `.`, so scoring is unaffected. Gate 1 reports both lists.

## M2: components by convention (`profiles/code-repo-conventions.yaml`, extends `code-repo`)

A manifest cannot find the documentation, configuration, scripts, deployment files, tests or requirements of a repository, nor a Python backend or
a frontend `src` that has no manifest of its own. M2 adds, each with its own evidence string, basis and confidence: top-level `docs`/`doc`/
`documentation`, `config`/`configs`/`conf`, `scripts`, `docker`/`deploy`/`deployment`/`k8s`, `tests`/`test`, `requirements` (kind documentation,
configuration, scripts, deployment, test-suite, dependency-pins); a top-level directory with an `__init__.py` (an importable Python package where
the manifest sits at the root); the `src` directly under a top-level folder that holds a `package.json` (judgement, low); and manifests under
`examples/` become role `example` (kind sample-project) and are not candidates. The rules come first, so a conventional name wins over a manifest
in the same directory. To express them the engine now lets a component rule test the directory itself with `path_glob`, `path_segment`, `name`
or `name_regex` (no file needed). Parts: only a component that a *manifest* declares can have parts; a convention folder such as `docker/` groups
its images, so they stay top-level components.

Scores against the DRAFT keys (provisional until the key review; tune set only). "All" = components-all.txt, "top" = components.txt; candidates
exclude the root and metadata.yaml-only directories; recall = TP / key size; precision is true precision TP / candidates (labelled false
positives are those the key excludes explicitly):

| repo | list | candidates | TP | labelled FP | unlabelled | recall | true precision | M1 manifest probe (recall / true precision) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| trellis | all | 19 | 18 | 1 | 0 | 1.00 | 0.95 | 0.78 / 0.56 |
| trellis | top | 18 | 18 | 0 | 0 | 1.00 | 1.00 | |
| superset | all | 46 | 36 | 6 | 4 | 1.00 | 0.78 | 0.83 / 0.81 |
| superset | top | 39 | 35 | 2 | 2 | 0.97 | 0.90 | |
| datahub | all | 84 | 66 | 11 | 7 | 1.00 | 0.79 | 0.98 / 0.79 |
| datahub | top | 75 | 63 | 9 | 3 | 0.95 | 0.84 | |

(M1 probe figures are from the regression above; trellis' ten example manifests are the main precision gain: 25 candidates to 19.)

**Held out on keys and on tuning, not blind on facts.** The held-out repositories (airbyte, egeria-docs) were not tuned on and their answer keys were not opened, but the brief and the Phase 0 notes carry facts about them (egeria-docs' site and docs layout; airbyte's connectors that carry a `metadata.yaml`), and some rules exist because of such facts: the `metadata.yaml` rule in `code-repo` is there because the brief's manifest list named it for airbyte. Results on those repositories are therefore *key-blind, not fact-blind*: that weakens the claim and does not invalidate the test. Every held-out result must say so.

**Recall 1.00 on the tune set is a fit, not a result.** The rules were written while looking at these three trees and scored against labels
made for them, so the numbers above say the rules can describe these repositories, not that they will on another. The only real test is the
held-out repositories at M4, run once by the reviewer; they were not touched. Precision on superset (0.78) is slightly BELOW the manifest probe's
(0.81): four unlabelled `src` directories of manifest components.

**Structural rule (not a name list).** `structural_rules: S-workspace-siblings` (judgement, low; evidence "workspace-style layout: many sibling
manifests under one parent"): five or more nested manifest directories of the SAME kind that are direct siblings under one parent directory,
inside a manifest component, are top-level components instead of parts (an npm or cargo workspace, a multi-module build: the parent only
aggregates them). Four siblings stay parts; kinds are counted separately; siblings under different parents are not pooled; no folder name is
involved. Such a finding carries `structure_rule_id`, `structure_basis`, `structure_confidence` and `structure_evidence`. On superset it lifts
the top-level list from recall 0.25 to 0.97 (the `superset-frontend` plugins and packages); it changes nothing on trellis or datahub.

**Overfit controls.** Every M2 rule has a `tuned_on` note naming the tune-set repositories that motivated it, so a reviewer can ablate it; a
rule motivated by one repository is suspect: R-conv-config (trellis), R-conv-tests, R-conv-requirements, R-conv-root-import-package,
R-conv-node-src and S-workspace-siblings (superset). Two or more: R-ex-example-manifest and R-conv-docs (trellis, datahub), R-conv-scripts
and R-conv-deployment (trellis, superset). No rule was added for the 11 labelled false positives of datahub (examples, fixtures and docker
sub-images): the same pattern did not appear in two of the three repositories. **M2 is frozen at `code-repo-conventions` 0.1.0**; the figures
above are its final provisional scores.

## M3: documentation sites (`profiles/docs-site.yaml`, names only)

`docs-site` 0.1.0 (extends `generic-relevance`): a directory holding `mkdocs.yml` or `mkdocs.yaml` is a docs-site component (manifest, high);
beside it the default content folder `docs` (role docs, subtree) and the default build output `site` (generated, hidden, counted) are claimed.
A top-level docs folder with **no** `mkdocs.yml` is the repository's documentation (kind `documentation`), never a site; a `docs/archive`
folder under it is archive (hidden; the only name, because it is the only one that occurs in a tuning tree). The mkdocs rule comes first, so a directory is claimed once; composed with
`code-repo-conventions` in either order, the first-listed profile wins (tested both ways) and the loader now accepts a shared base reached twice
(a diamond) while a real id clash between two profiles is still an error. No rule finds *sections*: in the tuning sample they are files
(`tutorials.md` ...), and the key says a section is not a component. The navigation, a non-default `docs_dir` or `site_dir`: not recognized,
because that needs the contents of `mkdocs.yml`, which is not read.

**Candidate copies (a report, not a rule).** `--copies-of KIND` writes `candidate-copies.json`: components of that kind whose sorted sets of
relative file names are identical (the files compared are those the profile does not hide, so a built `site/` or a `venv` does not make two copies
differ). Nothing is hidden or merged because of it; it is evidence for a later duplicate-tree test.

Scores against the two tuning keys (provisional; a names-only fit on two tiny trees, not a result; the keys were written before this profile):

| tree | candidates | TP | labelled FP | unlabelled | recall | precision | hidden and counted |
|---|---:|---:|---:|---:|---:|---:|---|
| mkdocs tutorial sample (17,522 files) | 5 | 5 | 0 | 0 | 1.00 | 1.00 | `site/` 2 x 45 files, `venv` 17,345 files |
| trellis docs folder (scored on the whole trellis list) | 1 | 1 | 0 | 0 | 1.00 | 1.00 | `docs/archive` 2 files |

On the sample the copies report finds one group: `source_code_step_4`, `source_code_step_5` and `source_code_step_6` have identical sets of 9 file
names; `source_code_final` and `src` differ. `tuned_on` is `mkdocs-sample` for the three mkdocs rules and `trellis` for the archive and the
plain-docs-folder rules (one-tree rules: suspect).

## M5: a file-role layer, and four more hidden rules (Phase 1b)

**The file-role layer** (`code-repo-conventions` 0.2.0, top-level key `file_roles`). Path rules, no file content. A file that no rule above claimed
(nothing hidden, no component) gets exactly one role, FIRST match wins, in the brief's order: `ci`, `test`, `docs`, `config`, `build`, `source`,
then the catch-all `other`. It cannot change a component (components come from directory rules only; `components.txt` and `components-all.txt`
are byte-identical to M2 on all three tune repositories) and it cannot un-hide a file (it is consulted last). `other` is a classified result,
reported beside the unclassified target (`shares.other_files`); the target is "unclassified at most 5%", and `other` above 20% is flagged.
New schema pieces: the `file_roles` list (same keys as a rule; grain `dir`; file tests only), the match key `component_scope` (`within` = under
some component, `root` = directly in a component's directory), and the roles `build`, `data-fixture`, `other`.

Order, as in the brief: a manifest such as `pyproject.toml` or `Chart.yaml` is `config` (it matches `*.toml` / `*.yaml` first); `build` keeps the manifests
no config pattern claims, `Makefile`, `Dockerfile*`, `*.gradle*`. `data-fixture`, `example` and `generated`/`vendored` have no pattern in this layer.

| repository (committed tree) | files | unclassified | other | docs | source | test | config | build | ci |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| trellis | 4,470 | 0.0% | 5.2% | 35.3% | 28.5% | 27.2% | 3.5% | 0.1% | 0.1% |
| datahub | 7,273 | 0.0% | 16.2% | 4.9% | 48.8% | 25.3% | 2.9% | 1.5% | 0.4% |
| superset | 5,511 | 0.0% | 15.8% | 6.4% | 54.1% | 19.3% | 2.6% | 0.9% | 0.9% |

`other` is under 20% everywhere. `tuned_on` is honest: the patterns that come straight from the brief say so and are not fitted to a repository.
Only `F-docs-markup-anywhere` (a `.md`, `.mdx` or `.rst` file anywhere, the generalisation of the brief's top-level `*.md`) was added after a look at
the tune set: trellis `other` was 39.6% before it, almost all nested Markdown files; its `tuned_on` is trellis, datahub and superset (the three have
Markdown outside the top level). The component scores are unchanged (trellis 19/18, superset 46/36, datahub 84/66; recall 1.00 on each list).

**Four hidden rules** (`generic-relevance` 0.3.0), added AFTER every older rule and ordered specific-first among themselves, so no older rule's
count moves. Each carries `tuned_on: ["egeria-v6 stratified sample (6994dff1)"]`. They are written from that sample, which is now spent.

| rule | what | files on the egeria-v6 list |
|---|---|---:|
| `R-wt-claude-worktree` | a folder under `.claude/worktrees/` is a working copy, whatever it is named (worktree-copy, hidden) | 57,668 |
| `R-tool-idea` | `.idea` is IDE tooling (hidden) | 1,612 |
| `R-run-volume-logs` | a `logs` folder under `runtime-volumes` is runtime output, with or without a `.log` suffix | 1,725 |
| `R-vend-nested-repo` | a repository inside another repository is vendored (hidden) | 60,798 |

Globs match whole path segments. Unanchored (`**/`) forms are needed because both `.claude/worktrees` and `runtime-volumes` sit one level down in
the workspace (`<repo>/.claude/worktrees/*`, `<repo>/runtime-volumes/...`).

**The nested-repository reading** (settled in review). A directory is hidden when it holds a `.git` (a folder or a worktree file) AND some ancestor
directory, the scanned root included, also holds a `.git`. For a lone repository scanned from its root this is "any `.git` below the root". For a workspace of
repositories the repositories directly under the workspace root are not nested: read literally ("any directory below the root that holds a `.git`"), the
rule would hide the 27 real repositories of the workspace, 148,753 of the 148,776 previously unclassified files. A nested repository wins over a manifest
inside it ("vendored wins"), also for the manifest of the repository itself. Overlap: all 57,668 worktree-rule files also match the nested rule; the
specific rule is ordered first, so the nested rule keeps the other 60,798.

Totals on the M0 egeria-v6 list (`egeria-workspace` 0.2.0): 2,612,019 files, unchanged; hidden 2,463,243 -> 2,585,046 (+121,803, exactly the four
rules' files); unclassified 148,776 -> 26,973; files the old rules hid that are now not hidden: 0. The old rules' counts match the Phase 0 census as before.

## M6: manifest reading (`recognizer/manifests.py`; `code-repo` 0.2.0, `code-repo-conventions` 0.3.0)

Until M5 the recognizer read names and sizes only. M6 lets it read a SHORT, CLOSED list of manifests, when it is given a blob source
(`--blobs-git REPO REV` reads the blobs of one commit from the git object database; `--blobs-dir DIR` reads a non-git tree without following symlinks).
Without a source the run is exactly the names-and-sizes run of M5 (`classes.json` says `manifest_reading.enabled: false`).

**What may be read, and what is extracted** (nothing else is copied into a finding): `package.json` (`name`, `workspaces`), `pnpm-workspace.yaml` (`packages`),
`lerna.json` (`packages`), `Cargo.toml` (`[package].name`, `[workspace].members/exclude`), `pyproject.toml` (`[project].name`, `[tool.poetry].name`,
`[tool.uv.workspace].members/exclude`), `go.work` (`use`), `pom.xml` (`artifactId`, `packaging`, `modules`), `settings.gradle(.kts)` (the string literals of `include`
calls, by regex, never evaluated). **Never opened:** lock files, `.env` files, data files, notebooks, `setup.py`, `build.gradle`, `Dockerfile`, `metadata.yaml`,
CODEOWNERS, and anything inside a hidden subtree (hidden wins before any read; the paths actually opened are written to `manifest-reads.txt`).
`go.mod`, `Chart.yaml`, `catalog-info.yaml` and `mkdocs.yml` are also on the Phase 2 list; M6 does not need them and does not read them (mkdocs is M7).

**Caps** (a profile may tighten, never raise): 256 KiB per file, 5,000 manifests and 64 MiB per survey, shallowest manifests first. A manifest over the file cap
or past a survey cap is not read: its finding stays presence-only and carries `skipped: size` or `skipped: cap`; a cap reached is named in `report.md` and in
`classes.json`. **Safe parsing:** `json.loads` (depth <= 50), `tomllib`, a YAML SafeLoader subclass that turns every unknown tag (`!ENV`, `!!python/name:`) into
null and refuses aliases, XML refused when it has a DOCTYPE or ENTITY, 1 s per file. A parse error never aborts a survey: the finding keeps its presence-only claim,
with `parse_error` and one step lower confidence. Member paths are resolved against the path list only: absolute, `..` or no match = `unresolved` (listed on the
declaring directory's finding, never created or fetched).

**What it changes.** A directory a manifest declares as a workspace or module member is a component of its own (top-level, not a part of the aggregator), claimed by
the member rule `M-workspace-member` (basis `manifest-content`) where no manifest rule claimed it, and carrying `member_of`, `evidence_file`, `evidence_field`
and `evidence_blob`. A non-root directory that only AGGREGATES (a `package.json` / `pnpm-workspace.yaml` / `lerna.json` with workspaces, a pom with `pom` packaging,
a virtual Cargo or uv workspace) is no longer a component: it gets `M-aggregator` (role `other`) and keeps `manifest_kind`. The repository root stays a component
(`root-project`). The `S-workspace-siblings` name-and-shape rule stays as the fallback where nothing declares the members.

**Fix from the M5 review.** In the file-role layer the exact manifest names (`pyproject.toml`, `Cargo.toml`, `Chart.yaml`, `setup.cfg`, `package.json`, ...) now come
BEFORE the config extensions, so a manifest is `build`, not `config`. Tune-set shares after the fix: trellis config 3.0% / build 0.7%, datahub 2.8% / 1.6%, superset
2.5% / 1.0%; `other` unchanged (5.2%, 16.2%, 15.9%).

**Regression (provisional against the draft keys; ALL = components-all.txt, TOP = components.txt; candidates / TP / labelled-FP / unlabelled):**

| repo | list | before (names only) | with manifest reading | change |
|---|---|---|---|---|
| trellis | ALL | 19 / 18 / 1 / 0, recall 1.00, precision 0.95 | same | none (26 manifests read, 24 members, no aggregator) |
| trellis | TOP | 18 / 18 / 0 / 0, 1.00, 1.00 | same | none |
| superset | ALL | 46 / 36 / 6 / 4, 1.00, 0.86 | 45 / 36 / 6 / 3, 1.00, 0.86 | the aggregator `superset-frontend` (a lerna workspace of 56 packages) is no longer a candidate; it was an unlabelled one |
| superset | TOP | 39 / 35 / 2 / 2, 0.97, 0.95 | 42 / 36 / 5 / 1, 1.00, 0.88 | `superset-frontend/src` is found (was the one miss); three workspace members become top-level: `superset-frontend/cypress-base` and the two `tools/eslint-plugin-*` packages, which the draft key labels non-components (`cypress-base` is a labelled test fixture), so labelled precision falls |
| datahub | ALL | 84 / 66 / 11 / 7, 1.00, 0.86 | same | none |
| datahub | TOP | 75 / 63 / 9 / 3, 0.95, 0.88 | 80 / 66 / 11 / 3, 1.00, 0.86 | the three misses (`metadata-io/metadata-io-api`, `openapi-entity-servlet/generators`, `openapi-servlet/models`) are found, because Gradle members are no longer parts of their parent; two more members are labelled test fixtures in the draft key (`entity-registry/custom-test-model`, `metadata-service/plugin/src/test/sample-test-plugins`), so labelled precision falls |

So recall never drops and on the TOP lists it rises to 1.00; labelled precision on the superset and datahub TOP lists falls by the declared members the draft key
calls test fixtures. That is the rule doing what it says (a declared member is a component), against a key that applies a further judgement (a test fixture is
not one); it is reported, not tuned away, and the key labels are for review. The M1 manifest-probe baselines reproduce unchanged (trellis 25/14, superset 37/30,
datahub 82/65, names only). Two runs of each repository are byte-identical.

## M7: documentation sections from the nav (`docs-site` 0.2.0; the `mkdocs` reader)

Given a blob source, `docs-site` reads `mkdocs.yml` / `mkdocs.yaml` (fields: `nav` titles and paths, `docs_dir`, `site_dir`; nothing else) and turns each
TOP-LEVEL nav entry into a `doc-section` component (`M-docs-section`, basis `manifest-content`), a PART of its site (it is in `components-all.txt`, not in
`components.txt`). The site itself stays a `docs-site` component.

**Section identity.** Collect the entry's page paths in nav order, recursing into sub-groups. Skip URLs and anchors (an entry that starts with `#`; a
`page.md#frag` names `page.md`) and entries outside `docs_dir` (absolute or with `..`); keep only paths that resolve to a FILE of the path list. If every kept page
sits under ONE top-level folder of `docs_dir` (at any depth below it; a page directly in `docs_dir` does not) the identity is that folder; otherwise it is the first
kept page's file path (so a section can be a FILE path). A single-page section in a folder is that folder; one directly in `docs_dir` is that page. No kept page:
not a component, listed as `unresolved_nav` on the site. Two entries with the same identity make one component. The bare `index.md` entry is the site's landing page
(`landing_page` on the site), not a section.

**docs_dir and site_dir.** Where `mkdocs.yml` names another `docs_dir` the folder is claimed as the default `docs` is; another `site_dir` is hidden (generated) as the default
`site` is. An absolute or `..` docs_dir gives no sections (`unresolved_docs_dir`).

**No nav.** A site whose `mkdocs.yml` has no nav gets, as a fallback, one `doc-section` of LOW confidence (`M-docs-section-folder`, basis `convention`) per top-level folder of
`docs_dir` that holds Markdown or reStructuredText pages, except `assets`, `js`, `css`, `img`, `images`, `overrides`, `snippets`, `includes` and names starting with `.` or `_`.
A site built by another generator is recognized by its config FILE NAME only: a directory that holds `docusaurus.config.{js,ts,mjs,cjs}` (never read; the sidebars are JavaScript
and are not read either) is a `docs-site` component (`R-docs-site-docusaurus`, `basis: convention`), its content folder is the generator default `docs/` beside the config, and
the same low-confidence fallback applies there (it needs no blob source). A plain documentation folder with NO site generator (no `mkdocs.yml`, no generator config) is NOT a
site and gets no sections: it stays one `documentation` component (version 0.2.1 of the profile adds the Docusaurus rule). A malformed, oversize or past-cap `mkdocs.yml` leaves the presence-only site (`parse_error` or `skipped`, lower confidence).
Translations (language folders beside the main site) are not recognized in this milestone.

**Scores against the tuning keys** (provisional; the mkdocs sample is a tutorial tree, not a held-out one):

| key | list | candidates / TP / labelled-FP / unlabelled | recall | precision |
|---|---|---|---|---|
| mkdocs sample v1 (21 components: 5 sites + 16 sections) | components-all.txt | 21 / 21 / 0 / 0 | 1.00 | 1.00 |
| mkdocs sample v1 | components.txt (top level only) | 5 / 5 / 0 / 0 | 0.24 | 1.00 |
| trellis docs | components-all.txt, names only or with reading | 1 / 1 / 0 / 0 | 1.00 | 1.00 |

The top-level list scores 0.24 BY DESIGN: sections are parts of their sites, and the 16 sections are in the all-components list. In the sample the four sites with a
nav each yield four one-page sections (the page file is the identity), the four landing pages are not sections, and `source_code_final`'s nav names `platform.md`, which
is not in its docs folder: unresolved, so no section. `trellis-docs` is unchanged: no `mkdocs.yml`, so no reading and no sections. The code-repo outputs of M6 are
byte-identical. The `.idea`, `venv` and `site` folders stay hidden and counted. The recall of 1.00 on the sample is a fit, not a result: the key was written from the same
nav the rule reads.

## M5b: tighter hiding, four more rules (`generic-relevance` 0.4.0, `worktree-copies` 0.2.0)

Dan's review rulings of 2026-11-26 (`tuned_on: "Dan's review 2026-11-26"`) and three rules from the egeria-v6 re-check sample (`tuned_on: "egeria-v6 re-check sample (be675143)"`).
M5's "nothing hidden becomes unhidden" check does NOT apply here: this milestone un-hides on purpose, and reports what it un-hides.

**Tightened**
1. `R-run-log`, `R-backup-file`: hide only the matching FILES; a folder is never hidden because of one stray `.log` or `.bak`. The rules were file-level already, so no count moves. Where a
   majority of a folder's files match, the other files are already hidden by other rules (checked on the M0 list: 0 further files), so no folder-promotion rule was added.
2. `R-gen-build-output` (`build`, `target`, `dist`, `.next`): hidden only with corroboration, as three directory rules in order: a build manifest beside the folder (`R-gen-build-output`);
   else no source-like file anywhere below it (`R-gen-build-output-no-source`); else the folder is SHOWN as `generated`, low confidence (`R-gen-build-output-unconfirmed`, relevance supporting).
   A manifest corroborates whatever is inside; "source-like" is the file-role layer's list of programming-language extensions. New directory tests: `no_source_files`.
3. `R-copy-worktree-name` (worktree-copies): a worktree name AND a `.git` FILE (the link of a `git worktree`; a clone has a `.git` folder) hides the folder. The name alone is
   `R-copy-worktree-name-only`: shown, low confidence.
4. `R-vend-nested-repo`: a directory that the outer repository's `.gitmodules` declares as a submodule is part of the outer repository, so it is not claimed. Only the `path` entries of the
   `[submodule "..."]` sections are extracted (never the url); the file is read through the same capped, safe reader (reader `gitmodules`, only where a blob source is given, never inside a
   hidden subtree, at most once per directory). Without a blob source every nested repository is vendored, as in M5.

**Added**, ahead of the M5 rules, in this order: `R-gen-ipynb-checkpoints` (`.ipynb_checkpoints`, any depth, generated, hidden), `R-gen-distribution-hub` (`exchange-*/distribution-hub/**`, hidden;
written with the unanchored `**/` form too, because in the workspace the folder sits one level down: `<repo>/exchange-quickstart/distribution-hub`), `R-secret-private-in-cert-dir` (a folder named
`private` whose PARENT's name has the whole word `cert`, `certificate`, `ca` or `pki`, any case: role `secret`, hidden, by name only; the words are split at punctuation and at case changes, so
`EgeriaRootCA` is egeria, root, ca; `certs` and `capital` are not matches). Archive stays hidden in the default view (the role map; no rule change).

**Per-rule files on the M0 egeria-v6 list** (2,612,019 files; names and sizes only; `egeria-workspace` 0.3.0). M5 -> M5b:

| rule | M5 | M5b |
|---|---:|---:|
| R-gen-build-output (hidden: manifest beside) | 27,267 | 24,871 |
| R-gen-build-output-no-source (hidden) | - | 0 |
| R-gen-build-output-unconfirmed (SHOWN, low) | - | 2,323 |
| R-copy-worktree-name (hidden: name + `.git` file) | 52,946 | 52,928 |
| R-copy-worktree-name-only (SHOWN, low) | - | 0 |
| R-gen-ipynb-checkpoints | - | 65 |
| R-gen-distribution-hub | - | 1,692 |
| R-secret-private-in-cert-dir | - | 2 |
| R-vend-nested-repo | 60,798 | 60,861 |
| R-wt-claude-worktree | 57,668 | 57,654 |
| R-run-log / R-backup-file / R-vend-installed / R-vcs-git / events / dumps / caches | unchanged | unchanged |
| unclassified | 26,973 | 25,256 |

Un-hidden: 2,323 files, in 34 `build` folders (all under one repository of the workspace) that have no manifest beside them and source-like files inside; 0 files from the
other tightened rules (all worktree-named folders of the list hold a `.git` file; the list has no `.gitmodules`, so rule 4 un-hides nothing here; the file was not read). Newly hidden: 1,717
files (1,658 distribution-hub, 57 checkpoints, 2 private). 115 hidden files only change rule (73 build -> nested repository, 34 worktree or nested-repository -> distribution-hub, 8 nested repository -> checkpoints). The total is unchanged.
Hidden 2,585,046 -> 2,584,440. Tune set (trellis, datahub, superset, with manifest reading) and the mkdocs sample and trellis docs: components, file roles and scores are byte-identical to M7.

## M5c: build-layout corroboration, orphaned output and runtime-volumes data (`generic-relevance` 0.5.0, `workspace-runtime-data` 0.1.0, `egeria-workspace` 0.4.0)

From the third egeria-v6 draw (`tuned_on: "egeria-v6 third draw (c67c74a8)"`, a sample that is now spent): all 30 build folders that M5b un-hid were orphaned Gradle output.

1. `build`, `target`, `dist` and `.next` are ALSO hidden when either holds, alongside the M5b corroborations (a manifest beside the folder; no source-like file below it):
   (a) **build-tool layout**: the folder directly contains a child folder from a fixed list. Gradle `build/`: `classes`, `libs`, `tmp`, `reports`, `generated`, `docs/javadoc` (`R-gen-build-output-gradle-layout`);
   Maven `target/`: `classes`, `test-classes`, `maven-status` (`R-gen-build-output-maven-layout`). The lists are Dan's, exactly; a name is added only with his word (`dist` has no list).
   (b) **orphaned**: the folder's parent holds nothing but that folder, no files and no other folders (`R-gen-build-output-orphaned`; the root of the scanned tree counts as a parent).
   With none of the four the folder stays `R-gen-build-output-unconfirmed`: shown, low confidence. New directory tests: `has_child_dir` (relative folder paths, two levels allowed) and `orphaned`.
2. **egeria-workspace only:** everything under a `runtime-volumes` folder (any depth) is hidden runtime data (`R-run-volume-data`, role `runtime-output`), in a small profile (`workspace-runtime-data`) composed
   LAST, so every earlier rule keeps its files and only files nobody claimed move. It is not in generic-relevance, which keeps the narrower `R-run-volume-logs` for other profiles.
3. **No name-only `logs` rule:** a folder called `logs` elsewhere stays shown.

**Against M5b, on the M0 egeria-v6 list** (2,612,019 files, unchanged; names and sizes only):

| rule | M5b | M5c |
|---|---:|---:|
| R-gen-build-output-gradle-layout (hidden) | - | 2,322 |
| R-gen-build-output-maven-layout (hidden) | - | 0 |
| R-gen-build-output-orphaned (hidden) | - | 0 (the 33 orphans are claimed by the layout rule first) |
| R-gen-build-output-unconfirmed (shown, low) | 2,323 | 1 |
| R-run-volume-data (hidden) | - | 865 |
| unclassified | 25,256 | 24,391 |
| hidden | 2,584,440 | 2,587,627 |

Un-hidden: 0 files. Newly hidden: 3,187 files (2,322 build-output files in 33 Gradle module folders, previously shown; 865 runtime-volumes files, previously unclassified). No file changes rule. The one build-like folder still shown
is a one-file `dist` folder with a sibling folder and no layout child. All 33 hidden folders satisfy both (a) and (b). The tune set (trellis, datahub, superset), the mkdocs sample and the trellis docs are byte-identical (findings differ only in the profile version).

## N1 (Phase 1c): composing profiles (`--profile a,b`)

`--profile code-repo-conventions,docs-site` composes profiles at run time (`compose_profiles`; a profile may also `extends` several). The FIRST-listed profile's rules are checked first, so it wins a
conflict; a directory is claimed once; a profile that two of them extend (generic-relevance) is loaded once; hidden subtrees still win (nothing inside node_modules, a build folder or a nested repository is
read or claimed). The composite is named `a+b` and its parts and versions are in `classes.json` (`composed_of`). The manifest-reading blocks of the parts combine (readers unioned, caps the tighter).

What it enables: the docs-site rules inside a code repository: `mkdocs.yml` sites with their nav sections (the D1 identity), the no-nav fallback, and Docusaurus sites. A site's sections are parts of the
site's directory even when a code manifest claimed it (the repository root stays the `root-project`). A Docusaurus site is recognized by its config file NAME wherever it is, also when a convention
(`docs`) claimed the directory first.

**Tune set with docs-site added** (provisional, vs the draft keys; before = `code-repo-conventions` alone): trellis and datahub: components and scores identical (trellis: the 2 files of `docs/archive` become hidden archive).
superset: recall unchanged (1.00); six new `doc-section` parts appear, from the Docusaurus site in `docs/` (`docs/docs/contributing`, `creating-charts-dashboards`, `databases`, `installation`, `miscellaneous`,
`security`; low-confidence fallback), which the draft key does not label: ALL 45/36/6/3 -> 51/36/6/9 (candidates / TP / labelled-FP / unlabelled), labelled precision 0.86 unchanged, precision against all candidates 0.80 -> 0.71.
The key predates the docs-section principle; whether these are labelled is the key audit's question.

## N2 (Phase 1c): Gradle `projectDir` mappings and aggregators (`code-repo` 0.3.0)

`settings.gradle(.kts)`: besides `include`, the recognizer reads `project(':x').projectDir = file('dir')` and the `new File('dir')` / `new File(settingsDir, 'dir')` / `File(rootDir, "dir")` forms (also
`findProject(...)`), as string literals by regex; nothing is evaluated (a variable, a computed path or a `rootProject.children.each` loop is not read). Each included project's directory is the mapped one
where there is a mapping, otherwise its path (`:a:b` is `a/b`); a mapping for a project that is not included is ignored. An include with no directory in the path list (a BOM, a mapped folder that does not
exist, a path with `..` or an absolute one) is not a component and is listed in `unresolved_members`. An included project whose only children are other included projects (no file of its own, every sub-folder an
included project) is not a component: it gets `M-aggregator` and is listed in `gradle_aggregators`; its children are the components. `tuned_on` for the member and aggregator rules now also names "iceberg (M8, spent)".

Tune set (trellis, datahub, superset, with manifest reading): components and scores identical to before N2 (none of the three uses `projectDir`; the aggregator test removes nothing there).

## N3 (Phase 1c): fixtures, samples, templates and tooling are not components (`code-repo-conventions` 0.4.0)

Dan's key principle, as GENERAL rules with general segment lists (whole segments, case-insensitive; no name from a held-out or spent repository in them, which a test asserts):

- **(a) A manifest project whose path has a test, sample, template or demo segment is not a component.** Test-like segments (`R-fx-test-project`, role `fixture`, kind `sample-project`): `test`, `tests`, `testing`, `__tests__`,
  `testFixtures`, `fixture`, `fixtures`, `testdata`, `test-data`, and any segment ending in the PLURAL `_tests` or `-tests`. Sample-like segments (`R-fx-sample-project`, role `example`, kind `sample-project`): `sample`, `samples`,
  `example`, `examples`, `template`, `templates`, `demo`, `demos`. The project's own directory name counts. A directory with no manifest is not a project and is untouched.
  **Exception:** a TOP-LEVEL test folder (`tests`, `test`, `testing`, `__tests__`, `integration_tests`, `smoke-tests`, ...) keeps or gets its convention component, kind `test-suite` (`R-conv-tests`, checked first); only the manifest projects INSIDE it are excluded.
  A top-level `examples/` or `templates/` stays role `example` and is not a component.
- **(b) A package under a tooling segment is tooling and not a component** (`R-tool-package`, role `tooling`): `tools`, `tooling`, `devtools`, `dev-tools`, `build-tools`, `buildSrc`, `_ext`, `ci`, `.ci`, `.github`, `.buildkite`, `.circleci`, `scripts`.
  The top-level `scripts` folder keeps its convention component (`R-conv-scripts` comes first).
- A manifest-declared member (a Gradle include, a workspace member) with no manifest of its own is excluded by the same segments (it is claimed by the exclusion rule, not the member rule).
- New directory test `segment_regex` (a whole path segment matches); new role `fixture`. `R-ex-example-manifest` (examples/example only, M2) is replaced by `R-fx-sample-project`.

**Plural suffixes only.** The singular `-test` and `_test` suffixes were dropped after the first tune-set run: superset's `legacy-plugin-chart-paired-t-test` is a real component (it is named for a statistical test), and `smoke-test`-style names are not reliably fixtures. Only `_tests` and `-tests` count.

**Tune set against the draft keys, row by row** (candidates / TP / labelled-FP / unlabelled; N2 baseline -> N3; superset against the key that now labels its Docusaurus sections, so its rows use the composition `code-repo-conventions,docs-site`):

| repo | list | before | after | what changed |
|---|---|---|---|---|
| trellis | ALL, TOP | 19/18/1/0, 18/18/0/0 | same | nothing |
| superset (composite, 42 truth) | ALL | 51/42/6/3 | 49/42/4/3 | removed: the two `tools/eslint-plugin-*` packages (tooling; labelled non-components); recall 1.00 |
| superset (composite) | TOP | 48/42/5/1 | 46/42/3/1 | the same two |
| datahub | ALL | 84/66/11/7 | 81/66/9/6 | removed: `buildSrc` (tooling), `metadata-service/plugin/src/test/sample-test-plugins` and `smoke-test/tests/cypress` (labelled test fixtures); recall 1.00 |
| datahub | TOP | 80/66/11/3 | 78/66/9/3 | `buildSrc` is not in the list; the two labelled fixtures removed |

Net: labelled false positives fall (superset 6 -> 4, datahub 11 -> 9) and no true package is lost.

## N4 (Phase 1c): a docs-site file-role layer (`docs-site` 0.3.0)

The docs counterpart of M5: a `file_roles` layer, consulted last (it cannot change a component or un-hide a file) and only for files INSIDE a component (a site or a documentation folder). First match wins:
`F-docs-fragments` (`snippets`, `includes` folders -> role `include-fragments`), `F-docs-theme` (`overrides`, `theme` -> `theme`), `F-docs-static` (`assets`, `img`, `images`, `css`, `js`, `static` -> `static-assets`),
`F-docs-page` (`.md`, `.mdx`, `.rst`, `.ipynb` -> `docs`), `F-docs-config` (`.yml`, `.yaml`, `.toml`, `.ini`, `.cfg` -> `config`), `F-docs-other` (everything else -> `other`, classified and reported). All are supporting; the built
`site/` stays generated and hidden (`R-docs-site-output`). New roles `static-assets`, `theme`, `include-fragments`. The patterns come from the plan's role list, not from a repository (`tuned_on` says so).
One structural change: the content-folder rule `R-docs-site-content` still CLAIMS the folder (it is a component for the layer's scope and for `docs_dir`) but no longer classifies every file below it as `docs`; its files are classified one by one, so an
image under `docs/` is a static asset, not a page. In a composition (`code-repo-conventions,docs-site`) the code roles come first.

| tree | files | unclassified | other | notes |
|---|---:|---:|---:|---|
| mkdocs tutorial sample | 17,522 | 0.0% | 37 (0.21%; 57% of the 65 files that are not hidden: the sample's Python code and requirements, outside any docs folder) | 99.6% hidden (venv, build output); docs 22, config 6 |
| trellis docs folder (34 files of the trellis tree) | 34 | 0 | 2 (`docs/experiments/*.json`) | docs 30, archive 2 (hidden) |

Components and scores are identical to M7 (mkdocs sample 21/21, trellis docs 1/1; superset's composite unchanged).

## N5 (Phase 1c): INHERIT translations (`docs-site` 0.4.0)

`INHERIT` joins the mkdocs fields that are read (path string only; manifest note d2bf881b). A directory whose `mkdocs.yml` has `INHERIT: <path>` that resolves to ANOTHER site's `mkdocs.yml` (or `.yaml`) is a `doc-translation`
component (`M-docs-translation`), a PART of that site (`part_of`, `translation_of`), NOT a `docs-site`; its nav entries are not sections, and it is in `components-all.txt`, not `components.txt`. The path is resolved against the path
list only: relative to the config's directory, never above the repository root, never absolute; the inherited file is never read through it (it is read only if it is itself a site, as always). Where the target is missing, is not a
`mkdocs.yml`, is outside the repository or is the same directory, the directory stays a site and the finding carries `inherit_warning` (counted in `classes.json`). An INHERIT cycle makes no translation (both stay sites, with a warning);
a chain resolves one step at a time (`c` -> `b` -> `a`: `c` is a translation of `b`, `b` of `a`). A non-string or empty `INHERIT` is ignored. Without a blob source nothing is known and every config stays a site.
`tuned_on` is "fastapi (M8, spent)". Tune set and the mkdocs sample: unchanged (none of them has an INHERIT).

## Decisions made so far (for review)

1. `vendored` (installed packages) and `generated` (build output, tool caches) are separate roles; both are hidden. `.cache` is `generated`.
2. The worktree-copy name rule is `basis: judgement`, `confidence: low`, in its own profile, composed last. `*-vocab[0-9]*` is the glob form of
   the census regex `.*-vocab\d+$` (it also matches `x-vocab1a`; no such folder exists in egeria-v6). A duplicate-tree test is backlog.
3. Findings are per (rule, directory) with files and bytes; `--per-file` restores the per-file view. For egeria-v6 that is 619,607 findings
   (331 MB) instead of 1,259,309 per-file ones: only about half, because egeria-v6 holds roughly one event or log file per directory, so a
   (rule, directory) finding is not much smaller than a per-file one there. Subtree rules (node_modules, .git) are already one finding each.
4. `components.txt` lists the top-level components (the root as `.`, nested manifest directories); `components-all.txt` adds the parts.
5. Sizes are optional in the list; without them bytes are 0.
6. One `unclassified` class (148,776 files in egeria-v6); a residual-primary class only if a rule says so.
7. Parts belong to manifest components only (M2).

## Open points

1. Findings volume on a runtime-output-heavy tree (decision 3): accepted as is; counts per rule, role and relevance are in `classes.json`.
2. The duplicate-tree test for worktree copies (backlog, M2+).

No Egeria type or API is used or invented; no key was opened for M0, and in M1 only the three tune-set keys were used (via the scorer);
the two held-out keys and repositories were not touched.

M5 (Phase 1b): no held-out key or repository was opened or run (the tune set is trellis, datahub, superset, the mkdocs sample and the egeria-v6 list); the tune-set answer keys were used only through the scorer, to check that the component scores did not move.

M6: manifests were read only from the three tune-set repositories (by commit, through the git object database) and from synthetic files in tests; no held-out repository, tree or key was listed, opened or run.

M7: `mkdocs.yml` was read only in the mkdocs tutorial sample and in synthetic tests; the trellis docs run read nothing. No held-out repository, tree or key was listed, opened or run.

M5b: no repository was read; the egeria-v6 list is names and sizes only (its `.gitmodules` question is therefore a names check); nothing under the held-out trees or keys was listed, opened or run.

M5c: names and sizes only; nothing under the held-out trees or keys was listed, opened or run.

N1: composition tested on the three tune-set repositories and synthetic trees only; no held-out tree or key was listed, opened or run.

N2: synthetic settings files and the three tune-set repositories only; no held-out tree or key was opened.

N3: the tune-set repositories and synthetic trees only; no held-out tree or key was listed, opened or run.

N4: the mkdocs tutorial sample and the trellis tree only; no held-out tree or key was opened.

N5: synthetic trees and the mkdocs tutorial sample; no held-out tree or key was opened.
