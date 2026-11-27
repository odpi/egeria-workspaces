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
`relevance` (role -> primary | supporting | hidden), ordered `rules`, and the conformance lists `path_grammar`, `name_grammar`, `required` and
`allowed_only` (schema-only until Phase 2; see B1 below).

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

## N6 (Phase 1c): the workspace-repo profile (`workspace-repo` 0.1.0; structural rules)

For repositories whose parts are deployments, notebooks, templates and documents rather than packages. `workspace-repo` extends `code-repo-conventions` then `docs-site` (the code profile wins a conflict) and adds four STRUCTURAL rules
(`structural_rules`, new ops), by file kinds and names, never by a repository's folder names (a test asserts none is named in them). They run after every other claim, so a manifest or convention claim always wins, and none
claims a directory that is hidden, inside a claimed component (the repository root does not count) or, for (a) and (b), a fixture, sample or tooling path. A deployment found this way also has parts: the images and projects built inside it.

- **(a) `S-compose-deployment`** (kind `deployment`): a directory holding a compose file by name (`compose.y?ml`, `docker-compose*.y?ml`, `*-compose.y?ml`) or a YAML file whose top-level `services` key is a mapping (new reader `compose-services`, the same
  caps and safe loader as every manifest, shallowest first, after the manifests; Helm `templates/` folders and hidden subtrees are never opened; a file that does not parse is skipped quietly). The unit is the child of the nearest GROUPING folder (a non-root
  folder with two or more children that hold deployments), otherwise the outermost compose directory on the way.
- **(b) `S-notebooks`** (kind `notebooks`): the shallowest directory with three or more `.ipynb` files below it (hidden checkpoints do not count), or holding an Obsidian vault (`.obsidian/`).
- **(c) `S-mostly-docs`** (kind `documentation`): a top-level directory of at least 3 files, at least 80% of them `.md` by count. **(d) `S-mostly-data`** (kind `sample-data`): the same with at least 80% `.csv`, `.json`, `.jsonl`, `.parquet` or `.yaml` and no code.
  The minimum of three files is mine (a one-file folder would trivially qualify). New structural-rule keys: `kind`, `share`, `extensions`, `no_code`, `name_regex`, `yaml_key`.

**Scored on the dogfood key of the workspaces repository itself (b0da1ad8; commit 6b040618, names and the compose YAML read from the git object database). These rules were tuned on it and the builder knows the repository: the score is a FIT, not a result.**

| key | list | before (`code-repo-conventions,docs-site`) | `workspace-repo` |
|---|---|---|---|
| egeria-workspaces (24) | all components | 17/11/6/0, recall 0.46, precision 0.65 | 27/19/8/0, recall 0.79, precision 0.70 |
| egeria-workspaces | top level | 17/11/6/0 | 23/19/4/0, precision 0.83 |
| egeria-python (9), a regression check | all and top | 8/8/0/0, recall 0.89 | 9/9/0/0, recall 1.00 |

(candidates / TP / labelled-FP / unlabelled.) Found by the new rules: the three compose-configs deployments (two directly, `optional-associated-runtimes` as the unit of its 13 deployments), `coco-workbooks` (an Obsidian vault), `workbooks` (notebooks),
`exchange-quickstart` (3 notebooks; the key calls it an exchange area), `templates` and `design-docs` (mostly Markdown); in egeria-python `sample-data` (mostly Markdown, kind documentation where the key says sample data; the path matches). Still missed:
`charts/tests` (a judgement test-suite), `coco-data` (it holds code, so it is not data), `design-patterns` (55% Markdown), `portal-docs` (70%), `exchange-freshstart` (two notebooks). The eight false positives: four Dockerfile images inside deployments (parts in the
top-level list), three under `runtime-volumes` (hidden by the egeria-workspace profile's data rule, which this profile does not include: composed with it the all-components list is 24/19/5 and the top-level list 20/19/1) and `work`, three notebooks in a folder the key calls scratch.

## Phase 1d (D1 to D4): the four general gaps behind kafka's recorded exception (`code-repo-conventions` 0.5.0, `code-repo` 0.4.0)

- **D1: a test word with a version or number tail.** The test segments (`test`, `tests`, `testing`; no new words) also match when one is followed by `[-_.]` and a number, optionally a short tag: `foo-tests-44`, `tests_2`, `integration-tests-3.7`, `test-3-rc1`. The word must start the segment or follow `-`, `_` or `.`.
  Not matched: `latest-3`, `contest-2`, `attest_1`, `paired-t-test`, `my-testing` (no number).
- **D2: `test-`, `test_`, `tests-` and `tests_` prefixes** count as test segments (for a manifest project and for a declared member). **Known limit (kept by Dan):** a PUBLISHED test library named this way (a `test-utils` artifact) is excluded; it is the same kind of limit as `tools`, which stays an internal-tooling segment, so a shipped module named `tools` is missed. A top-level test folder
  (`tests`, `integration_tests`, ...) still keeps its convention component.
- **D3: `includeBuild('<dir>')`** (and `includeBuild '<dir>'`, the Kotlin form) in `settings.gradle(.kts)`, a string literal read by regex and never evaluated, marks `<dir>` and every manifest project below it as role `tooling` (`M-included-build`), not components. A path that leaves the repository, is
  absolute, is not a directory of the list or is not a literal is ignored. `buildSrc` stays tooling as before. **Known limit:** a composite build that includes a real product build is mis-classed.
- **D4: benchmark harnesses are test support.** A manifest project with a `benchmark`, `benchmarks`, `bench` or `jmh` segment, or one starting or ending with them joined by `-` or `_`, is role `test-support` (new), kind `benchmark-project`, and not a component. `workbench` and `benchmarker` are not matched.

No name from a held-out or spent repository is in any rule (a test checks the earlier list and `upgrade-system`, `api-checker`, `generator`, `test-common`, `kafka`, `streams`, `connect`, `tools-api`). `tuned_on` for D3 and D4 names "kafka (N7, spent)".

**D5, re-score (a FIT for kafka, which is spent; candidates / TP / labelled-FP / unlabelled; before = the Phase 1c code at 283fb3f0):**

| repo (key) | list | before | after | changed candidates |
|---|---|---|---|---|
| kafka (b1bdaf54), spent | all | 73/31/37/5, recall 0.91, precision 0.46 | 36/30/1/5, recall 0.88, precision 0.97 | 37 removed (below) |
| kafka | top | 72/31/37/4 | 35/30/1/4, precision 0.97 | the same |
| trellis | all, top | 19/18/1/0, 18/18/0/0 | same | none |
| superset (42, composite) | all, top | 49/42/4/3, 46/42/3/1 | same | none |
| datahub | all | 81/66/9/6 | 79/66/8/5, precision 0.89 | `test-models` (a labelled false positive), `metadata-integration/java/spark-lineage/spark-smoke-test/test-spark-lineage` |
| datahub | top | 78/66/9/3 | 77/66/8/3 | `test-models` |
| egeria-workspaces dogfood | all, top | 27/19/8/0, 23/19/4/0 | same | none |
| egeria-python dogfood | all, top | 9/9/0/0 | same | none |

Tune-set recall does not drop (1.00 on trellis, superset and datahub). The kafka figures reproduce the recorded exception before the change (73 candidates, precision 0.46). The 37 removed kafka candidates: the 34 `streams/upgrade-system-tests-*` projects (D1), the three `test-common/*` projects and `connect/test-plugins` (D2), `api-checker` and its
three sub-projects (D3), `jmh-benchmarks` (D4) and `streams/test-utils`. That last one is the key's published test library: the known limit of D2 costs one true component (recall 0.91 -> 0.88), and leaves one labelled false positive.

## Phase 1e (E1, E2): a singular test-grouping folder (`code-repo-conventions` 0.6.0)

Cause (the D6 gate-1 recorded exception, spring-boot, now spent): 109 of 114 labelled false positives sat below ONE top-level test folder with a SINGULAR name (`<word>-test`) whose many projects do not end in `-tests`; the same folders were the 3 recall misses (the top-level test-suite components).

- **E1, one structural rule.** A directory whose own name ends, case-insensitively, in `-test` or `_test` is a test segment when BOTH: (i) it is not itself a project (no manifest file of its own, not a declared Gradle/npm/Cargo/... member that is more than an aggregator), and (ii) MORE THAN ONE project (at least 2) lies below it. Two new match keys: `groups_projects: {min, files}` (the directory itself) and `group_segment_regex: {min, files, regex}` (some proper ancestor with a matching name groups projects). Two rules use them: `R-conv-test-group` (a TOP-LEVEL such folder keeps or gets its convention component, kind test-suite, like the plural `-tests` folder) and `R-fx-test-group-project` (a manifest project below such a folder, or a declared member with no manifest, is a fixture, not a component). A project is a directory holding one of the manifest names, or a member that a manifest read declares; hidden (vendored) directories do not count; a names-only run counts manifest files.
- **Unchanged:** a leaf project named `...-test` (it is itself the project, so condition (i) fails: a statistical-test package stays a component); a `-test` folder with one project; a `-test` folder that has its own manifest and sub-projects; words ending in `test` without the separator (`latest`, `contest`, `attest`). The plural-only ruling stays for leaf projects. N1 to N6 and D1 to D4 are untouched.
- **Known limit (stated, as for D2):** a real product folder named `<word>-test` that groups two or more published modules (for example several published test libraries under one folder) is excluded. Test source-set folders with camelCase names (`intTest`, `dockerTest`) are still not test segments; that is a separate rule and Dan's call, not in this phase.
- No name from a held-out or spent repository and no word list is in any rule: a test asserts that the rules' match values and the recognizer sources contain none of `smoke`, `spring`, `integration-test`, `system-test`. `tuned_on` names `spring-boot (D6, spent)` on the two new rules.

**E2, re-score (a FIT, not a result; candidates / TP / labelled-FP / unlabelled; before = 196ca988):**

| repo (key) | list | before | after | changed candidates |
|---|---|---|---|---|
| spring-boot (a1aaf8a9), spent | all | 587/326/114/147, recall 0.99, precision 0.74 | 481/329/5/147, recall 1.00, precision 0.99 | 109 removed (all `smoke-test/spring-boot-smoke-test-*`), 3 added: `integration-test`, `smoke-test`, `system-test` (test-suite, R-conv-test-group) |
| spring-boot | top | 586/326/114/146 | 480/329/5/146 | the same 109 removed, the same 3 added |
| kafka (b1bdaf54), spent | all, top | 36/30/1/5, 35/30/1/4 | same | none |
| trellis | all, top | 19/18/1/0, 18/18/0/0 | same | none |
| superset (42, composite) | all, top | 49/42/4/3, 46/42/3/1 | same (the paired-t-test package stays a component) | none |
| datahub | all, top | 79/66/8/5, 77/66/8/3 | same | none |
| egeria-workspaces dogfood | all, top | 27/19/8/0, 23/19/4/0 | same | none |
| egeria-python dogfood | all, top | 9/9/0/0 | same | none |

Tune-set recall does not drop (1.00 on trellis, superset and datahub). The 146 unlabelled Maven fixtures under `src/intTest` and `src/dockerTest` are unchanged (out of scope), and so is the unlabelled count (147). The 5 labelled false positives left on spring-boot are not caused by this rule. The after figures are a fit: E1 was tuned after seeing D6, so it counts as fixed only after E3 (a fresh held-out code repository, Architect only).

## Phase 2, notebook 05, B0: a seeded BIDS-shaped generator (`samples/bids_gen.py`)

Command: `python samples/bids_gen.py --seed 1 --subjects 3 --sessions 2 --out OUT [--mutations SPEC.yaml]`. `OUT` must be absent or empty.

It writes `OUT/dataset/` (the tree), `OUT/paths.tsv` (`path<TAB>size`, sorted, the same as `recognizer/listpaths.py` gives) and `OUT/truth.jsonl`
(one line per injected deviation: path, kind, status, rule, class; empty for a clean tree).

The tree holds, per subject (and per session when `--sessions` > 0), the modality folders `anat`, `func`, `dwi` and `fmap`, and the top-level files
`dataset_description.json`, `README`, `participants.tsv` and `CHANGES`. Data files are empty and sidecars are `{}`. `dataset_description.json` has exactly
three fields: `BIDSVersion` (1.11.2), `Name` and `License` (`CC0`). Labels are synthetic (`sub-01`, `sub-02`, ...). No real data.

The seed picks the tasks, runs, echoes, an acquisition label, the field-map layout, the session labels and the mutation targets. The same seed, counts
and spec give a byte-identical tree and truth (tested).

A spec is `mutations:`, a list of `{class, variant?, count?, file?}`. Mutations are applied in a fixed class order, whatever the spec order. The
closed list of 17 classes:

| class | kind/status | expected rule |
|---|---|---|
| missing-top-level-file | structure/missing | RQ-dataset-description, RQ-readme, RQ-participants or RQ-changes |
| missing-modality-folder | structure/missing | RQ-datatype-ses (RQ-datatype without sessions) |
| unexpected-top-level-folder | structure/unexpected | AO-root |
| unexpected-file-in-modality-folder | structure/unexpected | AO-datatype |
| entity-order (`task-x_sub-01_...`) | naming/misnamed | NG-bids |
| unknown-entity-key | naming/misnamed | NG-bids |
| illegal-label-character (`sub-0_1`, `sub-01!`) | naming/misnamed | PG-subject |
| wrong-case, variant dir (`Sub-01`) or file (`T1W`) | naming/misnamed | PG-subject or NG-bids |
| wrong-extension (`.nii.zip` for `.nii.gz`; BIDS allows `.nii.gz` and `.nii`) | naming/misnamed | NG-bids |
| session-inconsistency | structure/missing | RQ-session |
| stray-name (a `final_v2`-style copy) | naming/misnamed | NG-bids |
| bidsversion-missing, license-missing | content-type/missing-field | CT-bidsversion, CT-license |
| bidsversion-invalid, license-empty, name-empty | content-type/invalid-value | CT-bidsversion, CT-license, CT-name |
| malformed-json | content-type/unreadable | CT-unreadable |

A `missing` deviation's path is the EXPECTED path. A subject-level mutation (illegal-label-character, wrong-case dir, session-inconsistency,
missing-modality-folder) uses a whole subject, and one subject always stays untouched as a witness, so every folder required per subject is still seen
somewhere. Conflicts (two content mutations of one field, malformed-json with another content mutation, too few subjects or sessions) are refused.
Rule ids are those of `profiles/bids-dataset.yaml` (B2).

## Phase 2, notebook 05, B1: grammars, required paths and closed sets are evaluated (`recognizer/grammar.py`)

`path_grammar` and `name_grammar` are no longer schema-only, and two new top-level keys join them: `required` and `allowed_only`. Every
Phase 1 profile has none of them, so its outputs are byte-identical to ef5e2b14 (checked on the tune set and the dogfood trees, every profile,
with and without manifest reading). A profile that declares `allowed_only` or `required` makes the recognizer judge the tree (every file the
profile does not hide) and add CONFORMANCE findings to `findings.jsonl` and a `conformance` block to `classes.json`. Names only: no file is opened.

Every item carries `id`, `basis`, `confidence` and `evidence` (and may carry `tuned_on`); the loader rejects an unknown key at any level, a reference
to an id that does not exist, and an id used twice or equal to a rule id (the id goes into the finding id). Items compose through `extends` as rules do.

- **`path_grammar`**: `{id, pattern, tokens, yields?}`. `pattern` is a relative directory path with named tokens, `sub-{sub}/ses-{ses}/{datatype}`;
  `tokens` maps each token to `{regex: R}` (a full match) or `{values: [..]}` (one of them, exactly). Every token is defined and used once.
- **`name_grammar`**: `{id, entities, label, suffixes, extensions}` for FILE names `<key>-<label>[_<key>-<label>...]_<suffix><extension>`.
  `entities` is the ORDERED list of keys, each `{key, label?, token?, required_for?}`: `label` overrides the grammar's `label` regex; `token` ties the
  entity to a token of the folder's pattern (present, and equal, exactly when the folder has that token: `sub-01_...` inside `sub-01/`); `required_for`
  lists the suffixes that need the entity. `suffixes` is a list, or `{by_token: datatype, values: {anat: [T1w], ...}}` (`by_token` names the folder token the list depends on).
  `extensions` is a list, or `{default: [...], by_suffix: {events: [.tsv]}}` (`by_suffix` overrides the default for a suffix); the longest listed extension is taken (`.nii.gz` before `.gz`).
- **`required`**: a literal `{path}` that must exist, or `{of: <path_grammar id>, for_each: [tokens]}`: for each value of the `for_each` tokens seen in
  the tree, every combination of the pattern's other tokens seen in it must exist (every subject has every session, and every datatype folder of it).
- **`allowed_only`**: `{under, dirs?, files?, name_grammar?, not_checked?}`: a CLOSED set below the directories `under` names (`.` for the root, or
  path_grammar ids): the sub-directories it allows (path_grammar ids), the files (exact names, and name_grammar ids), and `not_checked` globs of names
  that are counted but never judged (with everything below them).

**Judging an entry** of a directory an `allowed_only` item covers, in this order: it matches an allowed pattern or name exactly (conformant; a
directory takes the pattern's tokens and is looked into); it matches a `not_checked` glob (not checked); it has the SHAPE of an allowed item (a
pattern with its literals compared ignoring case and any text for a regex token, a value token ignoring case; for a file, a key of the grammar
followed by `-`, or one of its suffixes ignoring case, among its `_` parts; an allowed exact name ignoring case): `naming`/`misnamed`, rule = that
item, with a short `reason` (`entity-order`, `unknown-entity`, `label`, `case`, `suffix`, `extension`, `missing-entity` ...); otherwise
`structure`/`unexpected`, rule = the first `allowed_only` item that covers the directory. Nothing below a misnamed or unexpected directory is judged.
A `required` path that is absent is `structure`/`missing`, and the finding's path is the EXPECTED path. It is not reported when its parent folder is
absent too (only the shallowest absence is reported), nor when a sibling that differs from it only in case was reported misnamed (one deviation).
A folder that no `allowed_only` item covers is not checked.

**Findings.** A conformance finding has `kind` (`structure`, `naming` or `content-type`) and `status` (`missing` or `unexpected`; `misnamed`;
`missing-field`, `invalid-value` or `unreadable`), `grain: conformance`, the item's id as `rule_id`, its basis, confidence and evidence, and
`reason` for a misnamed one. It has no role or relevance (the `kind` of a component finding is unchanged). `finding_id` keeps its formula,
`sha256(profile_id@major | rule_id | path)[:16]`, so a missing file keeps its id across surveys. `content-type` (B2) is in the enum from the start.
**`classes.json` `conformance`**: checked items (entries judged plus required paths expected), conformant items, findings by kind and status, the
score (conformant / checked) and the not-checked files with their roots and reasons (`not-checked`, `below-finding`, `no-closed-set`).

## Phase 2, notebook 05, B2 and B6: the `bids-dataset` profile 0.1.1 and the `dataset_description.json` content checks

`profiles/bids-dataset.yaml` (extends `generic-relevance`, so `.git` and the like stay hidden and are not judged) declares a SUBSET of BIDS v1.11.2
(SOURCES.md): the datatypes `anat`, `func`, `dwi` and `fmap`; the entities `sub`, `ses`, `task`, `acq`, `dir`, `run` and `echo` in the specification's
order; the suffixes per datatype in the profile; NIfTI data as `.nii.gz` or `.nii`; the top-level files; and three content checks. `sub-emptyroom`, the
specification's subject for MEG empty-room recordings, is outside the subset and not checked. Its rule ids are the ones `samples/bids_gen.py` puts
in `truth.jsonl`: `PG-subject`, `PG-session`, `PG-datatype(-ses)`, `NG-bids`, `RQ-*`, `AO-root`, `AO-subject`, `AO-session`, `AO-datatype` and `CT-*`.
`tuned_on: "generated (bids_gen seeds 1-3)"`; no rule names a real dataset. Two facts were corrected after the Architect's read-back, from the
specification's own text (`.nii` is BIDS; `sub-emptyroom` is MEG's), and carry `tuned_on: "BIDS spec; noticed on ds000117 (reported-only sample)"`.
The scanned root is the dataset root.

**Study consistency apart from the standard.** A `required` item may carry `category: study-consistency` (default `standard`). `RQ-session`,
`RQ-datatype` and `RQ-datatype-ses` (every subject has every session, and every datatype folder, seen in the dataset) are study-consistency
checks: a regular study's protocol, which BIDS itself does not require. So are (0.1.1) `RQ-readme`, `RQ-participants` and `RQ-changes`, files this
profile requires that BIDS only recommends or allows. When a profile has such items, the `conformance` block of `classes.json`
has `by_category` (checked items, findings and score per category; entries and content fields count as `standard`) and each conformance finding
carries its `category`, so a report can say "BIDS 69%, study consistency 94%".

**`kind` takes its vocabulary from the grain.** For grain `conformance` it is one of `structure`, `naming` or `content-type` (with a `status`). For
component and role findings it stays the component or role kind, as before. The loader refuses a rule, manifest rule or structural rule whose
kind is `structure`, `naming` or `content-type`, so the two vocabularies cannot be confused.

**Content checks** (top-level key `content_checks`; NOTE-PHASE2 §2 row and §10). Only `dataset_description.json`, only its fields `BIDSVersion`,
`Name` and `License`, only at the scanned root, only under `bids-dataset` (the loader refuses any other file, field or profile), and only when a
blob source is given (`--blobs-dir DIR` or `--blobs-git REPO REV`); without one, `classes.json` says `content_reading.enabled: false`. One item per
field (`{id, file, field, check: {regex: R} | {non_empty: true}}`) and one `unreadable: true` item. The file is read under the 256 KiB cap by the
safe JSON parser (time limit, depth limit). Statuses: `missing-field` (absent or not a string), `invalid-value` (fails the check, or is longer than
256 characters; the value is stored only up to 256 characters), `unreadable` (parse error, not a JSON object, over the cap; no field is checked
then). The checks: `BIDSVersion` matches `\d+\.\d+\.\d+`, `Name` and `License` are not empty. Findings carry `basis: manifest-content`,
`evidence_file`, `evidence_field` and `evidence_blob` (the git blob sha, or the file's sha256 for a non-git tree). No other field is copied
anywhere (tested). A missing `dataset_description.json` is a `structure`/`missing` finding only. Each checked field counts as one checked item;
an unreadable file counts as one. `content-reads.txt` lists the files opened.

Results: clean trees (seeds 1-3 and more, with and without sessions) have 0 findings and score 1.0. Each of the 17 classes injected alone, and
all of them together, is found exactly: the conformance findings equal `truth.jsonl` by path, kind, status and rule, with nothing else.

**ds000117** (bids-examples @ 5e00d47b, names and sizes only plus its `dataset_description.json`; reported, NOT scored). On `samples/ds000117/paths.tsv`
with `--blobs-dir samples/ds000117`, under 0.1.1: 2,448 files; 1,792 not checked (derivatives, stimuli, sub-emptyroom, meg, beh, top-level,
subject-level and session-level sidecars and tables, scans files); 866 checked items, 5 findings, score 0.994 (standard 1.0 on 767 items, 0 findings;
study consistency 0.949 on 99, 5 findings). The content checks pass (BIDSVersion 1.8.0, License CC0). The 5 `missing` are `dwi` folders absent for
some subjects: honest study-consistency findings. **B6 (0.1.1)** closed three gaps the Architect found on 0.1.0, which had 882 checked items, 245
findings, score 0.722 (standard 0.695 on 786 items, 240 findings; study consistency 0.948 on 96, 5 findings): `RQ-participants` and `RQ-changes`
(BIDS RECOMMENDS participants.tsv and makes CHANGES OPTIONAL) are now `study-consistency`; `FLASH` (deprecated in BIDS 1.11.2 but still valid) is an
`anat` suffix (was 224 `suffix` findings); and `*.tsv` is not checked at subject and session level, as `*.json` was (inheritance; was 16 `unexpected` MEG
`channels.tsv` files at session level). B6.1 made `RQ-readme` study consistency too (BIDS RECOMMENDS README), which moves one checked
item from standard to study consistency and changes no finding. Before the read-back fixes the figures were 423 findings, score 0.589 (47 `.nii` field
maps, and 130 + 1 + its file from `sub-emptyroom`). The Architect's offline bids-validator run compares them after B4.

**Known limits** (what the subset leaves out or judges more strictly than BIDS):
- `derivatives/`, `sourcedata/`, `code/`, `stimuli/` and `phenotype/` are not checked (only counted).
- Inheritance is not modelled: top-level, subject-level and session-level sidecars and tables (`*.json`, `*.tsv`) are not checked. Inheritance applies at subject level too (a dataset without sessions keeps its inherited sidecars and tables in the subject folder), so AO-subject leaves `*.tsv` not checked as AO-session does.
- Sidecar content, `participants.tsv` and every data file are never read; only `BIDSVersion`, `Name` and `License` of the root `dataset_description.json` are read.
- Other datatypes (meg, eeg, ieeg, beh, pet, perf, micr, motion, mrs, nirs) are not checked; physio and stim recordings are not checked.
- Only the entities sub, ses, task, acq, dir, run and echo; any other BIDS entity (ce, rec, mod, part, ...) is reported as `unknown-entity`.
- Only the suffixes listed per datatype; others, such as T2starw, are reported as `suffix`.
- Any listed entity may appear with any suffix; per-suffix entity rules beyond `task` for bold, sbref and events are not checked.
- README, participants.tsv and CHANGES are required here; BIDS 1.11.2 recommends the first two and makes CHANGES optional. All three are scored as study consistency (0.1.1). README.md, README.rst and README.txt are allowed but do not satisfy the README requirement.
- RQ-session, RQ-datatype and RQ-datatype-ses expect a regular study (every subject has every session and datatype folder seen); they are study-consistency checks, scored apart, and a study whose subjects legitimately differ will have findings there.
- Session-level files of datatypes outside the subset other than sidecars and tables (`*.json`, `*.tsv`), such as `*_physio.tsv.gz`, are reported `unexpected`.
- The License value is not checked against a list in v0.
- `.bidsignore` is not read.

## Phase 2, notebook 05, B3: the conformance report and drift (`recognizer/conformance.py`, `recognizer/drift.py`)

```
python -m recognizer.conformance OUTDIR              # writes OUTDIR/conformance.json and a "Conformance" section of OUTDIR/report.md
python -m recognizer.drift OLD_OUTDIR NEW_OUTDIR     # writes NEW_OUTDIR/drift.json (or --out) and a "Drift" section of NEW_OUTDIR/report.md
```
Both read only the outputs of a survey (`findings.jsonl`, `classes.json`), never the tree. Each replaces its own marked section of `report.md`, so
running them again changes no byte.

**`conformance.json`**: the profile, the score (conformant checked items / checked items), the checked items (entries, required paths, content
fields), the findings by kind and by kind and status, the not-checked files and roots, what content was read, and the conformance findings
(id, path, kind, status, rule, reason). The headline is `97% conformant; 12 findings` (the percentage is floored, so a tree with a finding never
shows 100%). It refuses a survey whose profile declares no conformance.

**`drift.json`**: the CONFORMANCE findings of the two surveys compared by `finding_id`: `new` (in NEW only), `resolved` (in OLD only) and `unchanged`
(in both; an unchanged id whose status or reason changed, such as a field that went from `invalid-value` to `missing-field`, is marked `changed` with
the old status), with counts. A missing file keeps its id, so it stays `unchanged` until it is put back. The two surveys must use the same profile id
and major version (otherwise the ids are not comparable and drift refuses). Headline: `3 new since last survey; 0 resolved; 0 unchanged`.

Results (tests, seeds 1-3, the builder-written specs `samples/specs/drift-a.yaml` (13 deviations) and `drift-b.yaml` (3)): two surveys of the same
tree have 0 new and 0 resolved and byte-identical outputs; clean to mutated gives `new` = exactly the truth set; mutated to fixed back gives
`resolved` = the same set, with the same ids. Where the survey has `by_category`, `conformance.json` carries it and the report section gives the
score per category.

## Phase 2, notebook 05, B4: the notebook (`coco-workbooks/7. layout-semantics/05 conformance-and-drift.ipynb`)

The Coco pattern, local only (decision 4(a)): generate a clean tree (seed 1, 6 subjects, 2 sessions), survey it (100% conformant; 0 findings),
inject `samples/specs/drift-a.yaml`, survey again (95% conformant; 13 findings; BIDS and study consistency scored apart), report drift (13 new since
last survey), answer the UC6 questions from the stored `conformance.json` and `drift.json`, check the answer against `truth.jsonl` (equal), fix the tree
back (13 resolved, same ids), and survey the ds000117 file list (reported, not scored). The Resource Explorer, Portal and Egeria cells are marked
"Phase 3 — not run" and do nothing. "Over the allowed count" is answered "not checked in v0": the profile has no count rules.

`tests/test_notebook05.py` runs the notebook's code cells top to bottom in a fresh interpreter with the network blocked (well under 2 minutes), and
checks that the outputs are cleared, that no absolute or local path is in it, that it imports only the standard library, PyYAML and this folder's
code, and that the Phase 3 cells are marked. It works from the notebook's own folder in a checkout; the work folder is a temporary folder, removed
at the end.

## Phase 2, notebook 04a, A0: a seeded CalculiX-shaped parametric-sweep generator (`samples/fea_sweep_gen.py`)

Command: `python samples/fea_sweep_gen.py --seed 1 --out OUT [--grid 4x5x3 | --large] [--ran-fraction 0.8] [--mutations SPEC.yaml]`. `OUT` must be
absent or empty.

It writes `OUT/study-<name>/` (the tree), `OUT/paths.tsv` (`path<TAB>size` of the study's files, sorted, paths starting with `study-<name>/`) and
`OUT/truth.jsonl` (one line per injected deviation: path, kind, status, class, the variant for a class that has variants, and the expected rule for
off-grammar-case-name; empty for a clean tree).
**The scanned root is `OUT`, the parent of the study folder**: the recognizer makes parts only below a component that is not the scanned root, and the
study is that component (approved by the Architect, 2026-11-27).

The tree models file NAME conventions only: CalculiX (`.inp` input deck, `.frd` results, `.dat` printed output, `.sta` step status, `.cvg`
convergence, `.msg` messages, `.12d` eigen data, `.rout` restart) and Gmsh (`.msh` meshes). Every file is a one-line placeholder; no deck, mesh,
result or example is copied and no tool is run (SOURCES.md). Per study: `README.md`, `sweep.yaml` (presence only, never read), `templates/base.inp`,
`materials/<material>.inp`, `mesh/<part>_<level>.msh`, one folder `cases/case_E<E>_t<t>_mesh-<level>/` per grid point (`job.inp` and `run.log`;
a case that ran also has `job.frd`, `job.dat`, `job.sta`, `job.cvg`, `job.msg`, and some `job.12d` and `job.rout`), `post/<case-id>/` for each case
that ran and `post/sweep-summary.csv`, `validation/rig-<id>/`, and junk to hide (`scratch/`, `job.inp.bak`, `README.md~`, `templates/base.inp~`).

The grid is `--grid ExTxM`: E moduli (integers, GPa), t thicknesses (`p` is the decimal point: `t2p0` = 2.0) and M mesh levels (the first M of
coarse, medium, fine). The default is 4x5x3 = 60 cases; `--large` is 10x20x3 = 600. `--ran-fraction` (default 0.8, rounded) of the cases ran. The
seed picks the grid values, the study name, parts and materials, which cases ran, and the mutation targets. The same seed, grid, fraction and spec
give a byte-identical tree and truth (tested).

A spec is `mutations:`, a list of `{class, variant?, count?}`, applied in a fixed class order. The closed list of 9 classes (kind/status as ruled
by the Architect, 2026-11-27):

| class | example | kind/status |
|---|---|---|
| missing-input-deck | a case that did not run has no `job.inp` | structure/missing (path `<case>/job.inp`) |
| results-without-deck | a case that ran has no `job.inp` | structure/missing (path `<case>/job.inp`; never the same case as the class above) |
| off-grammar-case-name, variants no-decimal, wrong-case, stray-suffix | `case_E210_t2_mesh-fine`, `Case_E210_t2p0_mesh-fine`, `case_E210_t2p0_final_v2` | naming/misnamed (a folder under `cases/` is a case); rule PG-case or PG-case-any, below |
| off-grid-value, variants E, t | `case_E999_...`, `case_E210_t9p9_...` | naming/off-grid |
| duplicate-combination, variants E, t | `case_E0210_...` beside `case_E210_...`, `t2p00` beside `t2p0` | structure/duplicate (path: the SECOND folder in sorted path order) |
| stray-deck | `cases/job_old.inp` at the level of the case folders | structure/unexpected |
| bad-mesh-level | `case_E210_t2p0_mesh-ultra`, in case names only (mesh is a grid axis) | naming/off-grid |
| unexpected-top-level-folder | `study-<name>/misc/` | structure/unexpected |
| orphan-post | `post/<case-id>/` whose case is gone | structure/unexpected ("no matching case") |

A mutation that renames or removes a case removes that case's `post/` folder too (except orphan-post), so each mutation is one deviation. Each
mutation uses its own case. off-grid and duplicate are found only against a declared grid (the profile instance, A2). A bad mesh level is never
injected into `mesh/` file names: those are not judged against the levels in 0.1.0.

**The expected rule of a misnamed case folder** is decided by one stated criterion, the same in the generator (`expected_case_rule`) and the engine:
the name has the case SHAPE (the last segment of the PG-case pattern with its literals compared ignoring case and each regex token relaxed to
one character or more: `case_E.+_t.+_mesh-.+`, any case) gives PG-case; any other folder name directly under `cases/` gives the catch-all
PG-case-any. So `case_E210_t2_mesh-fine` and `Case_E210_...` are PG-case, `case_E210_t2p0_final_v2` and `case_E210_t2p0_mesh-` are PG-case-any.

## Phase 2, notebook 04a, A1: the `fea-sweep` profile 0.1.0 and the parameter tokens on part findings (F1)

`profiles/fea-sweep.yaml` (extends `generic-relevance`) recognizes a CalculiX-shaped parametric sweep by file NAMES only (`sweep.yaml`, decks
and logs are never opened). The scanned root is the PARENT of `study-<name>/`. `tuned_on: "generated (fea_sweep_gen seeds 1-3)"`; no rule
names a real study.

- **One component, N parts.** The folder that holds `sweep.yaml` is ONE component, kind `simulation-sweep` (basis manifest: the file's presence,
  as for `pyproject.toml`). Every folder directly under its `cases/` is a part (`part_of` the sweep), kind `simulation-case`.
- **Supporting:** `templates/` and `materials/` (role source, kind `input`), `mesh/` (source, `mesh`), each case's `job.inp` (source,
  `input-deck`), `post/` (role generated with relevance supporting, kind `derived`), `validation/` (test, `validation-reference`), and the
  study's `README.md` and `sweep.yaml`.
- **Hidden (counted per rule in `classes.json`, not shown):** `.frd`, `.dat` and `.12d` in a case (generated, `solver-results`); `.rout` and
  `.rin` (generated, `solver-restart`); `.sta`, `.cvg` and `.msg` (runtime-output, `solver-status`); a case's `run.log` (runtime-output,
  `run-log`); `scratch/` (scratch); and `*.bak` and `*~` below the study (backup, files only).
- **Closed sets (conformance, names only):** the scanned root holds the study folder (AO-root); the study holds `README.md`, `sweep.yaml`,
  `cases/` and the supporting folders (AO-study); `cases/` holds case folders only (AO-cases; a FILE there, such as `job_old.inp`, is
  `structure`/`unexpected`); a case folder holds `job.inp` (AO-case; its hidden files are not judged). `templates/`, `materials/`, `mesh/`,
  `post/` and `validation/` are not closed sets in 0.1.0.
- **The case grammar** PG-case is `study-{study}/cases/case_E{E}_t{t}_mesh-{mesh}`: E `[0-9]+`, t `[0-9]+p[0-9]+` (`p` is the decimal point),
  mesh `[a-z]+`. The values allowed are the grid's, declared in the profile instance (A2), not in the profile.
- **The catch-all PG-case-any** is `study-{study}/cases/{case}` with the token regex `(?!)`. That regex never matches, so no folder ever conforms
  to PG-case-any; but the engine reports a folder that has the SHAPE of an allowed pattern as misnamed, and a regex token's shape is any text, so
  every folder under `cases/` that fails PG-case is `naming`/`misnamed`: cases/ holds only cases, so such a folder is a misnamed case. The rule
  is PG-case when the name has PG-case's shape (`case_E.+_t.+_mesh-.+`, any case) and PG-case-any otherwise; the generator's
  `expected_case_rule` states the same criterion (tested on both sides and on the boundary). It is a declared rule of this profile only.

**F1, tokens on part findings** (approved by the Architect, 2026-11-27). A COMPONENT finding whose folder a path_grammar pattern with `yields`
typed gets `yields` (the pattern's word, here `case`) and `tokens` (the raw name strings: `{"E": "210", "mesh": "fine", "study": "bracket",
"t": "2p0"}`; `t2p00` stays `2p00`). A folder that fails the grammar is still a part, without tokens. Nothing changes for a profile whose
`yields` patterns type no component folder (bids-dataset types subject folders, which are not components) or that has no `yields` (tested both
ways); the Phase 1 and NB05 outputs are byte-identical.

**Collapse (UC1), generic-relevance alone versus fea-sweep** (default grid 4x5x3; `--large` 10x20x3):

| tree | files | folders | generic-relevance: components, hidden files, unclassified | fea-sweep: components + parts, hidden files (bytes) |
|---|---:|---:|---|---|
| seed 1 | 559 | 116 | 0, 62 (11.1%), 88.9% | 1 + 60, 342 = 61.2% (61.4% of bytes) |
| seed 2 | 562 | 115 | 0, 62 (11.0%), 89.0% | 1 + 60, 348 = 61.9% (62.1%) |
| seed 3 | 560 | 115 | 0, 62 (11.1%), 88.9% | 1 + 60, 345 = 61.6% (61.8%) |
| seed 1 `--large` | 5,439 | 1,088 | 0, 602 (11.1%), 88.9% | 1 + 600, 3,386 = 62.3% (62.5%) |

generic-relevance hides only the `.log` and `.bak` files and names no component, so a reader sees 497 files in 116 folders; fea-sweep shows one
sweep of 60 cases and hides the solver output. Byte shares follow file shares because every generated file is a one-line placeholder. Token
extraction is 100% on clean names (every case of seeds 1-3 and the large grid; tested). Clean trees: 0 conformance findings, score 1.0.

**Known limits (0.1.0):**
- Mesh file names under `mesh/` are not checked against the declared levels (0.1.0); a bad mesh level is found in case names only.
- One solver's naming: other FEA tools (Code_Aster `.comm`/`.export`/`.med`, Abaqus `.odb`) need their own profile variants; they are not in 0.1.0.
- `templates/`, `materials/`, `mesh/`, `post/` and `validation/` are not closed sets; their file names are not judged.

## Phase 2, notebook 04a, A2: conformance and drift on the sweep (F2 to F6), and the profile instance

```
python -m recognizer.recognize OUT/paths.tsv --out SURVEY --profile fea-sweep --instance fea-sweep.instance.yaml
python -m recognizer.conformance SURVEY
python -m recognizer.drift OLD_SURVEY NEW_SURVEY
```

`fea-sweep` 0.1.0 adds, by names only:
- **RQ-case-deck**: every case folder holds `job.inp` (structure/missing at `<case>/job.inp`).
- **RQ-case-status**: a case that holds `job.frd` (it RAN) also holds `job.sta`.
- **ST-not-run**: a case without `job.frd` is counted as `not-run` in `classes.json` (`conformance.states`), with its path. It is a state, not a
  finding, and it is not in the score.
- **PG-post-case** with `match_of: PG-case`: a `post/<case-id>/` with no case of the same parameters is structure/unexpected, evidence "no matching
  case". `post/` holds the case folders and `sweep-summary.csv` (AO-post); a case's post folder holds `summary.csv` and `plot-*.png` (not checked).

**The profile instance** (`--instance FILE`): the grid comes from a small YAML that the notebook writes beside the profile, never from `sweep.yaml`
(never opened). Its keys are `instance_of` (the profile id), `id`, `grid` and an optional `evidence`; `grid` maps a path_grammar id to the values
each of its tokens may take, for example `{PG-case: {E: [70, 210], t: [2p0, 3p5], mesh: [coarse, medium, fine]}}`. It is read whole (at most
64 KiB) by PyYAML's safe loader, it is the ONLY content read, and it is listed in `content-reads.txt` (`instance: <file name>`) and in
`classes.json` (`conformance.instance`: id, file name, sha256, the grid). With no instance there is no grid check at all. Each typed folder of a
grid pattern is two checked items:
- **off-grid** (naming/off-grid, rule `<id>.off-grid`): a token value outside the declared grid. One finding per folder; its evidence names each
  such token and the grid, and `reason` lists the tokens. The mesh level is a grid axis like E and t.
- **duplicate** (structure/duplicate, rule `<id>.duplicate`): the second and later folders, in sorted path order, whose tokens equal an earlier
  folder's. Its evidence names the first folder.

Numbers are compared normalised: a value of digits with `p` as the decimal point, or a number in the instance, is a decimal, so `t2p00` == `t2p0`
== 2.0 and `E0210` == `E210`. Anything else is compared as a string.

**Engine features** (approved by the Architect, 2026-11-27; each is inert for a profile that does not use it, tested, and the Phase 1 and NB05
outputs are byte-identical):
- **F2**: a `required` item with `of` and `path` (and optionally `when_present`) asks that every folder typed by that pattern hold the file. Presence
  is tested on ALL listed names, hidden ones included (names only, nothing opened). When a profile declares such an item, folders that hold only
  hidden files (outside hidden subtrees such as `scratch/`) are typed too, so the missing deck of a case that holds only its (hidden) `run.log`
  is found. Hidden files are still never judged against a closed set, and part formation, relevance counts and shares do not change. A case
  folder whose files are all hidden is still a part; F2 types it, so its missing deck is reported (and its part finding carries its tokens).
- **F3**: `states: [{id, of, name, absent}]`, counted per typed folder.
- **F4**: `--instance` (above); the statuses `off-grid` (kind naming) and `duplicate` (kind structure) join the closed lists.
- **F5**: a path_grammar item may name `match_of: <path_grammar id>`; tokens the two patterns share are compared normalised.
- **F6**: when either survey has PART findings, `drift.json` has `parts: {new, resolved, unchanged}` by finding id, and the Drift section of
  `report.md` says so; otherwise the key is absent. Conformance drift is unchanged.

**Results** (tests; seeds 1-3; the builder-written specs `samples/specs/fea-a.yaml`, every class once, and `fea-b.yaml`, the other variants with
counts above one): clean trees have 0 conformance findings and score 1.0; clean to mutated gives `new` = exactly `truth.jsonl` by path, kind and
status (and rule for the misnamed cases), with nothing resolved. Drift (`samples/fea_sweep_gen.py`'s `evolve`: add 6 cases at a new modulus,
declared in the instance, remove 2, rename 1): 0 new and 0 resolved conformance findings; parts 7 new, 3 resolved, 57 unchanged. The rename is
one resolved and one new, because **finding ids are path-based** (`sha256(profile@major | rule | path)`): move detection is backlog. Two runs
give byte-identical outputs.

**Known limits (0.1.0):**
- Case state from names only: "ran" means `job.frd` exists. A run attempt that failed but wrote partial results is not told apart from a good
  one; that needs `.sta` content, a later decision (D2).
- A renamed case is one resolved part and one new part, not a move.
- The grid is checked per token; a grid that is not a full product (some combinations never planned) cannot be declared, and a grid point with no
  case is not reported.

## Phase 2, notebook 04a, A3: the notebook

`coco-workbooks/7. layout-semantics/04a simulation-case-layout.ipynb` generates a clean sweep (seed 1, 4x5x3), recognizes it with
`generic-relevance` alone (497 assets shown in 116 folders, no component) and with `fea-sweep` (1 sweep, 60 cases, 61% hidden output), prints a
parameter table from the case tokens, writes the profile instance in its work folder and checks conformance (100% conformant; 0 findings; 12
not-run), injects `samples/specs/fea-a.yaml` (10 new findings, equal to `truth.jsonl`), answers the E1 layout questions (which cases exist, which
ran, which are off-grid, where the results are) from the stored outputs, and reports drift after `evolve` (parts 7 new, 3 resolved). The Resource
Explorer, Portal, Egeria and lineage cells are marked "Phase 3/4 — not run". Outputs are cleared. `tests/test_notebook04a.py` runs the code cells
top to bottom with the network blocked and checks for cleared outputs, no absolute or local path, standard-library and PyYAML imports only, and
the marked Phase 3/4 cells.

**Terms** follow the Architect's glossary of simulation studies (2026-11-27): the **sweep** is the set of cases from one template over one declared
grid, ONE component (the folder `study-<name>/`); a **case** is ONE grid point, a part of the sweep and never the sweep; a **run** is one attempt
to execute a case; a **survey** is one snapshot, written once.

**Known limits of 0.1.0 (cases, run attempts and versions; brief Amendment 2):**
- One folder per case; "ran" means `job.frd` exists. A failed attempt is indistinguishable from a good one (names only).
- CalculiX writes `job.*` in place, so a re-run overwrites the previous attempt and is invisible. A copied attempt folder (`case_..._v2`,
  `_old`) is reported as a misnamed case, or as a duplicate when its parameters match.
- Survey outputs are immutable snapshots; drift compares two snapshots. Attempts are not sealed, and nothing checks that a finished result was
  left unchanged (UC14, not built).
- A renamed case is one resolved finding plus one new finding.
- Attempt folders, a current-attempt pointer, sealing and any read of `job.sta` are not built; they wait for Dan's decisions D1 and D2.

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

N6: the workspaces and egeria-python dogfood trees by git object database only (not held out); synthetic tests; no held-out tree or key was opened.

Phase 1d: the kafka tree (spent) was listed by names and read for settings.gradle through the git object database as a fit; no unspent held-out tree or key was opened.
