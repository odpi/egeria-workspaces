# layout-profiles: layout profile model v0 and the repo recognizer (Phase 1, milestone M0)

Today the Resource Explorer treats every folder as an asset (2.6 million "assets" in egeria-v6). This folder holds, standalone and with no
RE, no Egeria and no platform involved:

1. a small versioned **profile document** (YAML, not an Egeria type) that says which paths are components, source, tests, docs, config, and
   which are generated, vendored, runtime output, copies, backups or VCS internals; every rule carries its basis, confidence and evidence;
2. a **recognizer** that applies a profile to a list of repo-relative paths (names and sizes only, never contents) and writes components,
   findings with stable ids, class counts with hidden-but-counted figures, and a short report.

Status: M0 (schema, loader, the `generic-relevance` profile, the recognizer, synthetic tests and the egeria-v6 numbers check).
Everything here is `proposed`: only a person confirms a profile.

## Use

```
cd layout-profiles                     # PyYAML and the standard library only
python -m recognizer.recognize PATHLIST --out OUTDIR [--profile generic-relevance] [--profiles-dir profiles]
python recognizer/gitlist.py REPO COMMIT OUT.tsv      # the files of ONE commit (git ls-tree -r -l: names and sizes, no contents)
python recognizer/listpaths.py ROOT OUT.tsv           # a walk that does not follow symlinks (for a tree that is not git)
python -m pytest tests                                 # 69 tests; set LAYOUT_EGERIA_V6_PATHS=<path list> to run the egeria-v6 numbers test (else it skips)
```
PATHLIST is one path per line, optionally `path<TAB>size`. It must be sorted to be streamed (otherwise it is sorted in memory); a duplicate,
absolute or `..` path is an error. `components.txt` is one directory per line, the input format of the Phase 0 scorer (kept outside this repository); answer keys are never copied or edited.

Outputs in OUTDIR, byte-identical for the same input and profile (checked on the 2.6M-path list too): `components.txt`, `findings.jsonl`,
`classes.json`, `report.md`.

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

**Findings.** `finding_id = sha256(profile_id + "@" + version-major + "|" + rule_id + "|" + path)[:16]`: no time, run id or tree sha, so the same
node keeps its id across surveys, and a minor or patch bump of the profile keeps ids (a major bump changes them). Fields: finding_id, path,
role, kind, relevance, rule_id, basis, confidence, evidence, grain, profile_id, profile_version (and `part_of` for a part).

## The numbers check (egeria-v6, listing only)

`recognizer/listpaths.py` walked an egeria-v6 working tree without following symlinks, reading names and sizes only (75 s), and the
recognizer classified that list in 12 s. Against the Phase 0 census of the same tree (kept outside this repository), counts are EXACTLY equal:

| class | rules | recognizer | census |
|---|---|---:|---:|
| all files | | 2,612,019 | 2,612,019 |
| vendored / build output | R-vend-installed + R-gen-build-output + R-gen-tool-cache | 1,113,920 | 1,113,920 |
| runtime events (.openlineageevent) | R-run-openlineage-event | 634,944 | 634,944 |
| logs | R-run-log | 623,778 | 623,778 |
| .git internals | R-vcs-git | 37,636 | 37,636 |
| backups | R-backup-dir + R-backup-file | 16 | 16 |
| heap dumps (.hprof) | R-run-heap-dump | 3 | 3 |
| worktree copies of residual files | R-copy-worktree-name | 52,946 | 52,946 |
| residual (unclassified) | | 148,776 | 148,776 |

`tests/test_numbers_egeria_v6.py` asserts this (expected values in `tests/census_egeria_v6.json`) and that every file is in exactly one class.
Two things to know: (a) the census splits "vendored or build" as one class; here it is three rules and two roles (`vendored`: installed
packages; `generated`: build output and tool caches), so the test sums them. (b) The census decides `.git` versus a vendored directory by
position (the first segment wins), this profile by rule order; no path in egeria-v6 has both, so the counts cannot differ here, but they
could on another tree.

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

## Decisions made in M0 (for review)

1. `vendored` (installed packages) and `generated` (build output, tool caches) are separate roles; both are hidden. `.cache` is `generated`.
2. Rule order is the census order, so `R-copy-worktree-name` is last and claims only files nothing else claims (this is how the census counted
   worktree copies); its finding is the copy's root folder, but only the files that rule claimed are counted against it.
3. `R-copy-worktree-name` is `basis: judgement`, `confidence: low`: a name pattern is a stand-in for a duplicate-tree test (open point 3).
   `*-vocab[0-9]*` is the glob form of the census regex `.*-vocab\d+$` (it also matches `x-vocab1a`; no such folder exists in egeria-v6).
4. A file-name rule writes one finding per file. For egeria-v6 that is 1,259,309 findings (728 MB, mostly the repeated evidence string); the
   file is evidence, kept out of the repository. A future option could write counts per (rule, folder) instead; not decided here.
5. `components.txt` lists top-level components only; parts are findings with `part_of`. If the root has a manifest, `.` is the only component.
6. Sizes come from the listing; a list without sizes works and reports bytes as 0.

## Open points raised, not decided (brief section 9, plus two)

1. Split "unclassified" into "unknown" and "residual primary"? Today it is one class (148,776 files in egeria-v6; all of the tune-set repos).
2. A manifest directory inside a vendored subtree: the profile as written makes vendored win, because the vendored rule matches first and a
   subtree is claimed at its shallowest root. Not exercised yet by a test of manifests (M1).
3. `worktree-copy` by a duplicate-tree test instead of a name pattern.
4. (new) Should `components.txt` list parts too (the manifest-probe baselines of M1 count every manifest directory)? It is one flag away.
5. (new) Findings volume: one line per hidden file is large for egeria-v6; per (rule, folder) would be 1000x smaller.

No Egeria type or API is used or invented; no key was opened for M0 (and the two held-out keys are untouched).
