# Sources

Nothing here is copied from a repository: profiles are written from conventions, tests use hand-written synthetic path lists.

- Build brief and Phase 0 corpus (answer keys, scorer, census notes): kept outside this repository.
- Rule set of `profiles/generic-relevance.yaml`, and the egeria-v6 expected counts (`tests/census_egeria_v6.json`): the Phase 0 census
  (a path-rule classification of a large unversioned egeria-v6 tree, 2026-11-26), kept outside this repository.
- Path lists (names and sizes only; not in the repository):
  - egeria-v6: a path list produced by `recognizer/listpaths.py` over an egeria-v6 working tree (not git), 2,612,019 files; no file was opened.
  - tune set, by `recognizer/gitlist.py` (`git ls-tree -r -l` of one commit): trellis `142bd786`, datahub `bc0c3ef7ef2`, superset `d2cce51dd`.
- Answer keys: not used in M0. Only the header lines (repo, commit, path) of the three tune-set keys were read to find the commits.
  The two held-out answer keys (airbyte, egeria-docs) were not opened, and those repositories were not run.
