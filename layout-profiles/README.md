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

## Open points

1. Findings volume on a runtime-output-heavy tree (decision 3): accepted as is; counts per rule, role and relevance are in `classes.json`.
2. The duplicate-tree test for worktree copies (backlog, M2+).

No Egeria type or API is used or invented; no key was opened for M0, and in M1 only the three tune-set keys were used (via the scorer);
the two held-out keys and repositories were not touched.
