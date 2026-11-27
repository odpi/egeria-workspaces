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
- M1: the three tune-set answer keys (trellis, datahub, superset; draft labels, unreviewed) were used only through the Phase 0 scorer, for the manifest-probe
  regression; none was copied or edited, and the scores are provisional until the keys are reviewed.
- M5 (Phase 1b): no new answer key was used beyond the three tune-set keys (through the scorer, to confirm the component scores did not move). The egeria-v6 stratified sample (a 89-directory sheet) motivated the four hidden rules; it is spent. The held-out repositories of Phase 1b were not listed, opened or run.
- M6 (Phase 1b): the recognizer read manifests of the three tune-set repositories at the same commits as the path lists (package.json, lerna.json and the like; at most 37 per repository, at most 56 KB); tests use synthetic manifests only. No manifest was copied into the repository.
- M7 (Phase 1b): the five `mkdocs.yml` files of the mkdocs tutorial sample (a public tutorial tree used for tuning, 914 bytes in all) were read for their nav; tests use synthetic nav files only.
- M7 follow-up: the Docusaurus rule uses the config file NAME only, from the manifest-reading scope note; no Docusaurus repository was looked at and no config was read.
- M5b (Phase 1b): the egeria-v6 list is used by names and sizes only, as before; `.gitmodules` is read only by the recognizer in tests (synthetic files) and where a blob source is given; the three new rules come from the egeria-v6 re-check sample, which is now spent.
- M5c (Phase 1b): the egeria-v6 list by names and sizes only; the layout lists and the runtime-volumes rule are the owner's rulings after the third draw, which is now spent.
- N6 (Phase 1c): the workspaces repository at commit 6b040618 and egeria-python at 98837e05 (the dogfood trees; not held out, and known to the builder) were listed by names and sizes and their compose YAML read from the git object database; their answer keys were used only through the scorer, as a fit.
- Phase 1d (D5): the kafka repository at commit c4cddf09 (a spent held-out repository) was listed by names and sizes and its Gradle settings read through the git object database, only to re-score the rules as a fit against its key (b1bdaf54).
- Phase 1e (E2): the spring-boot repository at commit f580d002 (spent after D6; its path list and key a1aaf8a9 were used to re-score the E1 rule as a fit), kafka (c4cddf09, spent, key b1bdaf54), and the tune set and dogfood trees as before, by names and sizes with manifests read from the git object database; no held-out tree or key was opened.
- Phase 2 notebook 05 (B0): `samples/bids_gen.py` writes synthetic BIDS-shaped trees (empty data files, `{}` sidecars, a three-field `dataset_description.json` it writes itself, License CC0); nothing is copied from a dataset.
- Phase 2 notebook 05 (B2), the specification: `profiles/bids-dataset.yaml` 0.1.0 (0.1.1 since B6) restates facts (entity names and order, datatype folders, suffixes, the
  dataset_description.json fields) from the Brain Imaging Data Structure (BIDS) specification v1.11.2, https://bids-specification.readthedocs.io/en/v1.11.2/,
  by the BIDS contributors, licensed CC-BY-4.0 (https://creativecommons.org/licenses/by/4.0/). No text of the specification is copied; the version, URL and
  licence were verified by the Architect on 2026-11-27 (URL live; repository licence CC-BY-4.0; release v1.11.2 published 2026-09-29).
- Phase 2 notebook 05 (B2), the dataset: ds000117 ("Multisubject, multimodal face processing", Wakeman, DG and Henson, RN, as listed in its
  dataset_description.json) from bids-standard/bids-examples @ 5e00d47b6f1db106dda1b776d5243eb41b4cb95b. Licence CC0, as stated in its
  dataset_description.json (the repository has no repo-level licence). Copied: the file list (names and sizes of the 2,448 blobs under `ds000117/`, from
  the git tree API, as `samples/ds000117/paths.tsv`) and `dataset_description.json` verbatim (blob 40598363). Nothing else: no sidecar, table, text,
  derivative or data file. Fetched once at build time; nothing is fetched at run time.
- The BIDS validator (bids-validator, MIT) is a reference only: it is not installed, run or copied here (the Architect runs it once, offline, after B4).
- Phase 2 notebook 04a (A0): `samples/fea_sweep_gen.py` writes synthetic CalculiX-shaped sweep trees. It models file-NAME conventions only, which
  are facts: the CalculiX extensions `.inp`, `.frd`, `.dat`, `.sta`, `.cvg`, `.msg`, `.12d`, `.rout`/`.rin` (CalculiX, http://www.calculix.de/, by
  Guido Dhondt; GNU GPL version 2 "or (at your option) any later version", GPL-2.0-or-later (checked 2026-11-27)) and the Gmsh mesh extension
  `.msh` (Gmsh, https://gmsh.info/, by Christophe Geuzaine and Jean-Francois Remacle; GNU GPL "Version 2 or later, with the following exception",
  GPL-2.0-or-later with a linking exception, https://gmsh.info/LICENSE.txt (checked 2026-11-27)). The licences are recorded for provenance only:
  only file-name conventions are modelled. Abaqus (proprietary) is named only as the origin of the `.inp` keyword style; nothing of it is
  modelled beyond the shared extension. Every generated file is a one-line placeholder: no solver code, input deck, mesh, result, example,
  tutorial tree or documentation text is copied, and no tool is shipped, installed or run.
