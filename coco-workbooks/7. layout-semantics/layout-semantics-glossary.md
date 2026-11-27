# Layout Semantics Glossary

> **Author:** Dan Wolfson  
> **Version:** 1.0  
> **Status:** DRAFT  
> **Date:** 2026-11-27  
> **Description:** The vocabulary of the Layout Semantics project — the layout profile model and its recognizer, conformance and drift, the method used to test the rules honestly, the terms of the three scenarios (code repositories, BIDS neuroimaging datasets and simulation sweeps), and what those scenarios have discovered so far.

---

## Overview

Many valuable file systems and repositories are laid out to match a process: build, test, tune, validate, run, simulate,
share, release.  If the layout can be recognized, from a manifest or by convention, then a catalog no longer has to treat
every folder as an asset, and the parts that matter can be tied to their meaning, their owner and their place in a
process.  That is the idea behind **Layout Semantics**.

The project works in small, checked steps.  A **layout profile** is a short, versioned document that says which folders
are components, what role each file plays and what should be hidden.  A **recognizer** applies profiles to a list of
paths — names and sizes, almost never file contents — and writes findings that keep the same identity from one survey to
the next.  The same model then checks **conformance**: whether a tree follows a declared layout, and how it has
**drifted** since the last survey.  So far it has been tried on three kinds of tree:

* **Code repositories** — which folders are real components, and which are tests, fixtures, tooling, generated output
  or copies.
* **BIDS neuroimaging datasets** (notebook 05, `conformance-and-drift`) — structure and naming against a declared subset
  of the BIDS specification.
* **Simulation sweeps** (notebook 04a, `simulation-case-layout`) — a generated, CalculiX-shaped finite-element
  parameter sweep, recognized as one sweep with one part per case.

The same words came back with different meanings as the work went on.  *Run* meant a case to one reader and an
execution to another; *spent*, *held out* and *fit* were used as if everyone knew the method behind them; *not checked*
was easy to confuse with *unexpected*.  This glossary fixes the meaning that the briefs, design notes and the
`layout-profiles` README use.  The simulation terms follow the Architect's glossary of simulation studies, and where that
glossary maps a term to an Egeria type the mapping is given in the term's description.  No new Egeria type is proposed
here.

The last folder, **What the Scenarios Discovered**, records lessons in plain words.  Each says what was learned, which
rule or decision followed, and the limit that is still known.  Repositories used as held-out tests are not named in this
glossary; where a lesson came from one, it says so generically.

Everything here is new and has not been reviewed, so the glossary, its folders, its terms and its relationships are all
DRAFT.

**Prerequisites:** none.  This file creates every element it refers to: the glossary, its folders, its terms and the
relationships between them.  It does not link to any element defined elsewhere.

---

## Part 1: The Glossary

___

## Create Glossary

### Display Name
Layout Semantics Glossary

### Qualified Name
Glossary::LayoutSemanticsGlossary

### Description
The vocabulary of the Layout Semantics project: the layout profile model and its recognizer, conformance and drift, the method used to evaluate the rules, the terms of the code-repository, BIDS and simulation-sweep scenarios, and the lessons those scenarios have produced.

### Language
English

### Usage
Reference this glossary when reading or writing a layout profile, a recognizer report, a conformance or drift result, a test plan for the rules, or one of the Layout Semantics notebooks, so that each term carries the same meaning everywhere.

### Purpose
To give the people building, reviewing and using layout profiles one agreed reading of the project's words, and to record what the scenarios have taught so far together with their known limits.

### Search Keywords
- Layout Semantics
- Layout Profile
- Conformance
- Drift
- BIDS
- Simulation Sweep
- Resource Explorer

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

## Part 2: Organizing the Glossary

The folders follow the shape of the work: the model first, then conformance and drift, then the evaluation method, then
one folder per scenario, and finally the lessons the scenarios produced.

___

## Create Collection Folder

### Display Name
The Layout Profile Model

### Qualified Name
CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Description
The parts of the layout profile model and the recognizer: profiles, rules, evidence, findings, components and parts, file roles, relevance classes, and what the recognizer may read.

### Purpose
Groups the terms that describe how a tree is recognized, so that every later term can be stated in them.

### Parent ID
Glossary::LayoutSemanticsGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Dan Wolfson

### Content Status
DRAFT

___

---

___

## Create Collection Folder

### Display Name
Conformance and Drift

### Qualified Name
CollectionFolder::LayoutSemanticsGlossary::ConformanceAndDrift

### Description
The terms for checking a tree against a declared layout: path and name grammars, required items, closed sets, conformance findings and their score, and drift between two surveys.

### Purpose
Groups the terms used when a profile judges a tree rather than only describing it.

### Parent ID
Glossary::LayoutSemanticsGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Dan Wolfson

### Content Status
DRAFT

___

---

___

## Create Collection Folder

### Display Name
Evaluation Method

### Qualified Name
CollectionFolder::LayoutSemanticsGlossary::EvaluationMethod

### Description
How the project tests its rules honestly: answer keys, tune sets, held-out repositories, pre-registration, read-back, fits and confirming runs, the scores, and generated trees with injected deviations.

### Purpose
Groups the terms that say how much a reported number can be trusted.

### Parent ID
Glossary::LayoutSemanticsGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Dan Wolfson

### Content Status
DRAFT

___

---

___

## Create Collection Folder

### Display Name
Scenario: Code Repositories

### Qualified Name
CollectionFolder::LayoutSemanticsGlossary::CodeRepositories

### Description
Terms from recognizing components in source-code repositories: test source sets, CI-configuration folders, documentation folders, aggregators, included builds and benchmark harnesses.

### Purpose
Groups the code-repository terms that the profile rules depend on.

### Parent ID
Glossary::LayoutSemanticsGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Dan Wolfson

### Content Status
DRAFT

___

---

___

## Create Collection Folder

### Display Name
Scenario: BIDS Neuroimaging Datasets

### Qualified Name
CollectionFolder::LayoutSemanticsGlossary::BIDSDatasets

### Description
Terms from checking a BIDS-shaped neuroimaging dataset (notebook 05): the standard itself, its folders, file-name parts, metadata files and the top-level files.

### Purpose
Groups the BIDS terms that the bids-dataset profile restates from the specification.

### Parent ID
Glossary::LayoutSemanticsGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Dan Wolfson

### Content Status
DRAFT

___

---

___

## Create Collection Folder

### Display Name
Scenario: Simulation Sweeps

### Qualified Name
CollectionFolder::LayoutSemanticsGlossary::SimulationSweeps

### Description
Terms for a parametric simulation study (notebook 04a, a CalculiX-shaped finite-element sweep): study, sweep, case, run attempt and its outcomes, result set, sealing, and the solver's file kinds. They follow the Architect's glossary of simulation studies, with its mapping to Egeria types.

### Purpose
Groups the simulation terms so that a case is never confused with a sweep, nor a run with a case.

### Parent ID
Glossary::LayoutSemanticsGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Dan Wolfson

### Content Status
DRAFT

___

---

___

## Create Collection Folder

### Display Name
What the Scenarios Discovered

### Qualified Name
CollectionFolder::LayoutSemanticsGlossary::Discoveries

### Description
Short findings, in plain words, that the scenarios produced: each says what was learned, which rule or decision followed, and the limit that is still known.

### Purpose
Groups the lessons so that they can be cited, reviewed and linked to the terms they change.

### Parent ID
Glossary::LayoutSemanticsGlossary

### Parent Relationship Type Name
CollectionMembership

### Authors
- Dan Wolfson

### Content Status
DRAFT

___

---

## Part 3: The Layout Profile Model

These are the terms every other folder is written in: what a profile is, how its rules claim paths, and what the recognizer writes.

___

## Create Glossary Term

### Display Name
Layout Profile

### Summary
A versioned document that says how a kind of tree is laid out: which folders are components, what role each file plays, what is hidden, and, optionally, which names and structure are expected.

### Description
A layout profile is a small YAML document with a stable profile id, a semantic version, a status, the roles it knows, the relevance of each role, an ordered list of rules and, optionally, conformance items (path grammar, name grammar, required items and closed sets). Any rule change bumps the version. The loader rejects an unknown key, an unknown role or relevance, a duplicate rule id and a rule without evidence. The profiles of this project live in `layout-profiles/profiles/`, for example `generic-relevance`, `code-repo-conventions`, `docs-site`, `workspace-repo`, `bids-dataset` and `fea-sweep`. A layout profile is not an Egeria type. In Egeria its naming rules could be held as NamingStandardRule elements (`namePatterns`) grouped in a NamingStandardRuleSet; its path and structure rules have no Egeria element today, which the Architect's Egeria-fit review lists as a candidate feature to raise, not a decided one.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::LayoutProfile

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Quote the profile id and version beside any result, because the same tree gives different findings under a different profile or version.

### Example
`fea-sweep` 0.1.0 recognizes a CalculiX-shaped parametric sweep as one component with one part per case, and hides the solver output.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Profile Rule

### Summary
One ordered rule of a layout profile: what it matches, what it assigns, how far the assignment reaches, and why.

### Description
A rule has an id, a match (directory segment, file name, extension, glob, or a file the directory holds), an assignment (role, kind and relevance), a grain (subtree, the directory only, or component), a basis, a confidence and an evidence string. Rules are tried in order and the FIRST match wins, so the most specific rules come first. A rule may also carry `tuned_on`, which names the trees that motivated it.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::ProfileRule

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Every rule must carry `tuned_on` so a reviewer can remove it and see what changes. A rule motivated by one repository only is marked suspect.

### Example
`R-vend-node-modules` matches the segment `node_modules`, assigns role vendored with relevance hidden, applies to the whole subtree, and rests on convention with high confidence.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Rule Basis

### Summary
The kind of evidence a rule or finding rests on: manifest, convention, judgement, or manifest content.

### Description
`manifest` means a file declares it (a `pyproject.toml` declares a package). `convention` means a widely used name or layout says it (`node_modules` is an install directory). `judgement` means the profile author's call, usually with low confidence. `manifest-content` means a value read from an allowed field of an allowed manifest file, under the manifest reading rules.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::RuleBasis

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Prefer a declared basis to an inferred one: the design's rule is that declared beats inferred.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Confidence

### Summary
How sure a rule is of its claim: high, medium or low.

### Description
Confidence is set on the rule and copied to every finding the rule makes. The recognizer never invents or raises it. A name-only guess is low: build output that has no corroborating evidence is low confidence and is shown rather than hidden, and the worktree-copy name rule is judgement with low confidence.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Confidence

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Use confidence to decide what a person should review first. It is not a probability.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Evidence

### Summary
The stated reason, carried on every rule and finding, that a reviewer can check.

### Description
Every rule has an evidence string, and every finding carries it. A claim made from manifest content also carries the file, the field and the blob id it came from. Only the extracted values (names, member globs, nav titles and paths, module names) are stored; no other file text is copied. "Evidence and confidence on every claim" is a requirement of the plan.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Evidence

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
When a finding is disputed, start from its evidence and rule id, not from the role it assigned.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Profile Composition

### Summary
Building one profile from others with `extends`, or applying several profiles at once.

### Description
A profile may declare `extends: [a, b]`: its own rules are checked first, then those of a, then those of b. The recognizer also accepts a list on the command line (`--profile a,b`). The first-listed profile wins a conflict, a directory is claimed once, and a hidden subtree still wins over any component claim. A cycle of `extends` is a load error.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::ProfileComposition

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Compose instead of copying rules, so that a fix to a shared profile reaches every profile that extends it.

### Example
`workspace-repo` extends `code-repo-conventions` and then `docs-site`, so the code rules win a conflict and documentation sites inside a repository are still recognized.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Proposed Status

### Summary
The status of a profile that no person has confirmed yet; the other statuses are confirmed and retired.

### Description
Every profile has a status of proposed, confirmed or retired. Only a person confirms a profile, and everything in this project so far is proposed. In the design, only confirmed profiles would drive governance; proposed ones are visible but advisory.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::ProposedStatus

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Treat findings from a proposed profile as suggestions to review, not as decisions.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Recognizer

### Summary
The program that applies one or more layout profiles to a path list and writes components, findings and class counts.

### Description
The recognizer reads a path list (names and sizes) and writes, into one output folder: `components.txt` (top-level components), `components-all.txt` (with their parts), `findings.jsonl`, `classes.json` (counts and bytes per role and relevance, with the shares classified and hidden) and `report.md`. It is deterministic: the same input and profile give byte-identical output. It uses only the Python standard library and PyYAML, makes no network call, and never opens a file except under the manifest reading rules or a profile instance. Unclassified is a first-class result, never silently dropped.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Recognizer

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Run it standalone; it does not need the Resource Explorer, Egeria or a platform. Integration with the Resource Explorer survey is a later step.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Path List

### Summary
The recognizer's input: one repository-relative path per line, optionally with its size.

### Description
A path list comes from `git ls-tree` of ONE commit (`recognizer/gitlist.py`), so a dirty working tree cannot leak in, or from a walk that does not follow symbolic links (`recognizer/listpaths.py`) for a tree that is not in git. Names and sizes only: no file content. A duplicate, absolute or `..` path is an error. Without sizes, bytes are reported as 0.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::PathList

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Record the commit or listing that produced a path list beside any result, so the survey can be repeated.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Survey Snapshot

### Summary
One recognizer pass over one tree at one time: its findings, classes and conformance, written once and never edited.

### Description
A survey snapshot is the output folder of one run. It is never edited; a new survey is a new folder. Drift compares two snapshots. In Egeria this maps to a SurveyReport, linked to its annotations by ReportedAnnotation, with the survey settings (such as the commit and the names-only promise) in `analysisParameters`; each snapshot is a new report and none is edited. The mapping is for Phase 3 and is not built.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::SurveySnapshot

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Keep each snapshot: the history of a tree is reconstructed from the snapshots, not from edits to one of them.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Finding

### Summary
A record the recognizer writes for one thing a rule claimed, with the rule, role, relevance, basis, confidence and evidence behind it.

### Description
One finding is written per (rule, directory) that a rule claimed: the subtree root for a subtree rule, the directory holding the file for a file-name rule, or the directory itself for a component. Its fields include the finding id, path, role, kind, relevance, rule id, basis, confidence, evidence, grain, profile id and version, the files and bytes claimed, and `part_of` for a part. A profile that judges conformance also writes conformance findings. In Egeria a finding maps to an Annotation, with the rule id, basis, kind, status and finding id in `additionalProperties` under fixed keys: the modelling-standard item C1, still to be written.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Finding

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Cite a finding by its finding id, not by its line in a file.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Finding Id

### Summary
The stable identity of a finding across surveys, made from the profile id and major version, the rule id and the path.

### Description
`finding_id = sha256(profile_id@major | rule_id | path)`, cut to 16 characters. It holds no time, run id, tree id or content, so the same node keeps its id from one survey to the next, and a minor or patch version change of the profile keeps every id. A missing item keeps its id because its path is the expected path. The id is path-based, so a rename shows as one resolved and one new finding. An Egeria element's own guid would differ; the mapping is a Resource Explorer concern.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::FindingId

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Compare surveys by finding id. Do not compare ids across a major version change of the profile: they are not comparable, and drift refuses.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Component

### Summary
A directory that a profile says is a real, distinct thing worth cataloguing: a package, module, documentation set, deployment, notebook set or simulation sweep.

### Description
Components come from directory rules only: a manifest (a `pyproject.toml` or `pom.xml` in the folder), a convention (a top-level `docs` folder with real content) or a structural rule (a folder of notebooks, a compose deployment). A directory inside a hidden subtree can never be a component. The point is collapse: the design's first use case is turning tens of thousands of folders into a few hundred components that people can work with. In Egeria a code component maps to a SoftwareComponent or SoftwareModule, and a released one to a RunnableSoftwareComponent.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Component

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Say "component" only for what the profile lists in `components.txt` or `components-all.txt`; everything else is a file role or a relevance class.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Part

### Summary
A component nested inside another component, recorded with `part_of` the outer one.

### Description
A nested component is a part of the component around it, and only top-level components appear in `components.txt`; `components-all.txt` adds the parts. Only a component that a manifest declares can have parts: a convention folder such as `docker/` groups its images, so they stay top-level. In the simulation scenario, each case folder is a part of the sweep.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Part

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Count parts separately from components when quoting a collapse figure, for example "1 sweep and 60 cases".

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Candidate

### Summary
A directory the recognizer proposes as a component, before it is compared with an answer key or confirmed by a person.

### Description
When scored against an answer key, each candidate is a true positive (the key lists it), a labelled false positive (the key explicitly excludes it) or unlabelled (the key says nothing about it). Candidates exclude the scanned root.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Candidate

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
A candidate is a proposal, never a decision: nothing is linked or catalogued without a person's confirmation.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
File Role

### Summary
The one role each file gets from the file-role layer when no other rule has claimed it: ci, test, docs, config, build, source or other.

### Description
The file-role layer is path rules only, tried in a fixed order: `ci`, `test`, `docs`, `config`, `build`, `source`, then the catch-all `other`. It is consulted last, so it can never change a component or un-hide a file. Inside a documentation site the docs-site profile adds `static-assets`, `theme` and `include-fragments`. `other` counts as classified but is reported on its own, and a share of `other` above 20% is flagged, so a catch-all cannot hide the target of at most 5% unclassified files. In Egeria the file types BuildInstructionFile, SourceCodeFile, ScriptFile, YAMLFile and PropertiesFile cover some roles; test, CI and docs roles would be classifications or an annotation type.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::FileRole

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Use file roles to answer "what kind of file is this?", and components to answer "what thing does it belong to?".

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Relevance Class

### Summary
Whether a role is shown by default: primary (shown), supporting (shown on drill-down) or hidden (counted but not shown).

### Description
Every role in a profile maps to one relevance class. Components are primary; source, test, docs, config, CI, tooling and examples are supporting; generated, vendored, scratch, archive, audit, runtime output, version-control internals, worktree copies, backups and secrets are hidden. Hidden is never silent: hidden files are counted, by count and by bytes, so a view can say how many it is not showing and why. The design also names finer classes for later (intermediate, derived, archive or backup, audit or write-once, unknown) with a default visibility per perspective.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::RelevanceClass

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Report hidden counts beside every shown count, for example "312 assets (3,911 intermediate and 18,402 cache files hidden)".

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Fixture

### Summary
The role of a manifest project that exists only to test something; it is not a component.

### Description
A manifest project whose path holds a test segment is role `fixture`, kind sample-project. The test segments are `test`, `tests`, `testing`, `__tests__`, `testFixtures`, `fixture`, `fixtures`, `testdata`, `test-data`, a segment ending in the plural `-tests` or `_tests`, a segment starting with `test-`, `test_`, `tests-` or `tests_`, a test word with a version or number tail, a singular `-test` or `_test` folder that is not itself a project and holds two or more projects, and a camelCase test source set under `src`. A top-level test folder is the exception: it is itself a test-suite component, and only the projects inside it are excluded. Sample, example, template and demo projects are excluded the same way, as role `example`.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Fixture

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Do not count fixtures as components when quoting an inventory. Known limit: a published test library named like a fixture (for example a `test-utils` artifact) is excluded too.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Tooling Package

### Summary
A manifest project that builds, checks or runs the repository rather than being part of what it delivers; it is not a component.

### Description
A manifest project under a tooling segment is role `tooling`, kind tooling-package. The segments are `tools`, `tooling`, `devtools`, `dev-tools`, `build-tools`, `buildSrc`, `_ext` and `scripts`, plus the closed list of CI-configuration folders. A Gradle included build is tooling too. Under the owner's ruling for Phase 1h, a top-level `scripts` folder, and a configuration folder that holds only lint settings, are tooling too, not components.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::ToolingPackage

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Known limit, kept on purpose: `tools` is always treated as internal tooling, so a shipped module named `tools` is missed.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Generated Content

### Summary
Files a tool produced from other files, which can be produced again: build output, a built documentation site, caches, notebook checkpoints and solver results.

### Description
Generated content has role `generated` and is hidden. Build output folders (`build`, `target`, `dist`, `.next`) are hidden only with corroboration, never by name alone: a build manifest beside them, no source-like files in them, a build tool's own child folders in them, or a parent holding nothing else. Without corroboration such a folder is low confidence and is shown. `.ipynb_checkpoints` and `.cache` are generated. In Egeria generated output maps to the GeneratedTarget classification.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::GeneratedContent

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Generated and vendored content are separate roles even though both are hidden: generated content can be rebuilt from the tree, vendored content came from somewhere else.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Vendored and Copied Content

### Summary
Code or trees that came from somewhere else: installed packages, a nested repository, or a worktree copy. Hidden.

### Description
`node_modules` and other install folders are role `vendored`. A directory below the scanned root that holds its own `.git` is a vendored or copied repository and is hidden as a whole, unless the outer repository declares it as a submodule in `.gitmodules`, in which case it is part of the outer repository. A worktree copy needs a `.git` FILE as well as a matching name; a name alone is low confidence and is shown.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::VendoredContent

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Hide copies so that one thing is not counted many times; the design's copies-and-versions use case starts from this.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Runtime Output

### Summary
Files written by running software rather than by people or builds: event output, logs, heap dumps, solver status files and runtime data volumes.

### Description
Runtime output has role `runtime-output` and is hidden. Log and backup rules hide the matching FILES; a folder is hidden as a whole only when most of its files match, so one stray `.log` never hides its folder. A folder named `logs` is not hidden by its name alone.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::RuntimeOutput

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Runtime output is counted, so a steward can still see how much of a tree it is.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Manifest Reading

### Summary
The one exception to names-only: reading a closed list of small manifest files, for named fields only, under size caps and with safe parsers.

### Description
The recognizer may read only the files on a closed list (such as `package.json` workspaces, `pom.xml` modules, Gradle `include` calls, `Cargo.toml` members, `mkdocs.yml` nav, `.gitmodules` paths and, under `bids-dataset` only, three fields of `dataset_description.json`), and only the fields named for each. Files are read from the git object database at the surveyed commit, never from a working tree. Caps: 256 KiB per file; 5,000 files and 64 MiB per survey; 1 second and a nesting depth of 50 per parse. Parsers: JSON and TOML from the standard library, YAML with a safe loader that turns unknown tags into null and refuses aliases, XML that refuses a DOCTYPE, Gradle by regular expression over string literals, never evaluated. Never read: lock files, `.env` files, data files, notebooks, or anything inside a hidden subtree. CODEOWNERS is out of scope because it carries people's handles. A parse error never stops a survey; the finding falls back to presence-only with lower confidence.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::ManifestReading

### Folders
- CollectionFolder::LayoutSemanticsGlossary::LayoutModel

### Usage
Adding a file or field to the list is a profile change and needs a stated reason. Every file opened is listed in `content-reads.txt`.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

## Part 4: Conformance and Drift

These terms are used when a profile judges a tree against a declared layout and compares one survey with the next.

___

## Create Glossary Term

### Display Name
Layout Standard

### Summary
A published or declared layout that a tree is expected to follow, such as BIDS, an eCTD submission structure, a trial master file or a project template.

### Description
A layout standard is the thing a tree conforms to. A profile encodes a DECLARED SUBSET of it, names the version it encodes, and records the standard's licence and source. Anything the standard allows but the subset leaves out is not checked, rather than reported as unexpected. Where a profile is stricter than the standard on purpose, it says so per rule and scores those checks as study consistency.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::LayoutStandard

### Folders
- CollectionFolder::LayoutSemanticsGlossary::ConformanceAndDrift

### Usage
Always say which version and which subset of a standard a conformance score refers to.

### Is Abstract Concept
True

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Path Grammar

### Summary
Directory patterns with named tokens that say where folders of a given kind sit, such as `sub-{sub}/ses-{ses}/{datatype}`.

### Description
A path grammar item has an id, a relative directory pattern, and a definition of each token as a regular expression or a list of allowed values. Its optional `yields` names what a matching folder is (a subject, a session, a case). A folder that has the SHAPE of a pattern but breaks it (wrong case, a bad label) is reported as misnamed against that pattern.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::PathGrammar

### Folders
- CollectionFolder::LayoutSemanticsGlossary::ConformanceAndDrift

### Usage
Write a token's values in the profile only when they are fixed by the standard; values that vary per tree belong in a profile instance.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Name Grammar

### Summary
The grammar of file names: ordered entities (key-label pairs), a label pattern, the allowed suffixes and the allowed extensions.

### Description
A name grammar describes names of the form `<key>-<label>[_<key>-<label>...]_<suffix><extension>`. The entities are listed in their required order; an entity may be tied to a folder token (the `sub-01_` in a file name must equal its `sub-01/` folder) or be required for certain suffixes. Suffixes may depend on the folder (one list per datatype) and extensions on the suffix. The longest listed extension is taken, so `.nii.gz` is matched before `.gz`. A misnamed file carries a short reason: entity-order, unknown-entity, label, case, suffix, extension or missing-entity. In Egeria a NamingStandardRule's `namePatterns` can hold the grammar as text; the check itself stays in the Resource Explorer.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::NameGrammar

### Folders
- CollectionFolder::LayoutSemanticsGlossary::ConformanceAndDrift

### Usage
Naming is part of conformance, not an extra: drift can be in names alone.

### Example
`sub-01_ses-1_task-rest_run-1_bold.nii.gz` has the entities sub, ses, task and run in order, the suffix `bold` and the extension `.nii.gz`.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Token

### Summary
A named, variable part of a path pattern whose value is taken from the folder name, and what the pattern says the folder is.

### Description
Each token of a path grammar is defined by a regular expression or a list of values. When a pattern with `yields` types a component folder, the component's finding carries `yields` (the word, such as `case`) and `tokens` (the raw strings taken from the name). Token values are compared normalised for grid checks: digits with `p` as the decimal point are numbers, so `t2p00` equals `t2p0`.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Token

### Folders
- CollectionFolder::LayoutSemanticsGlossary::ConformanceAndDrift

### Usage
Use tokens to build tables from names alone, without opening any file.

### Example
`case_E210_t2p0_mesh-fine` yields a case with tokens E = 210, t = 2p0 (2.0) and mesh = fine.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Required Item

### Summary
A path that must exist: a literal path, or a file or folder required for every folder of a given pattern.

### Description
A required item is a literal path, or is stated per pattern: for each value of some tokens, every combination of the others seen in the tree must exist, or every folder typed by a pattern must hold a given file. An absent required item is a structure finding with status missing, and its path is the EXPECTED path. Only the shallowest absence is reported.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::RequiredItem

### Folders
- CollectionFolder::LayoutSemanticsGlossary::ConformanceAndDrift

### Usage
Mark a required item that the standard does not itself require as study consistency, so it is scored apart.

### Example
In `fea-sweep`, every case folder must hold `job.inp`, and a case that holds `job.frd` must also hold `job.sta`.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Closed Set

### Summary
A rule (the profile key `allowed_only`) that below a given folder only the listed folders and files are allowed.

### Description
A closed set lists the sub-folders (by path grammar), the files (by exact name or name grammar) and the `not_checked` patterns allowed below a folder. Each entry is judged in order: an exact match conforms; a not-checked match is counted but not judged; something with the SHAPE of an allowed item is misnamed; anything else is unexpected. Nothing below a misnamed or unexpected folder is judged. A folder that no closed set covers is not checked at all.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::ClosedSet

### Folders
- CollectionFolder::LayoutSemanticsGlossary::ConformanceAndDrift

### Usage
Use a closed set only where the standard really is closed; elsewhere use not-checked, so that legitimate extras are not reported.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Catch-All Pattern

### Summary
A pattern that no folder can satisfy, used so that every wrongly named folder in a place that holds only one kind of thing is reported as misnamed rather than unexpected.

### Description
In `fea-sweep`, `cases/` holds only case folders. The catch-all `PG-case-any` has a token whose expression never matches, so no folder conforms to it; but because the engine reports any folder with the shape of an allowed pattern as misnamed, every folder under `cases/` that fails the real case grammar becomes a misnamed case. A name that has the case shape is reported against `PG-case`, any other name against `PG-case-any`. It is a declared rule of that profile only.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::CatchAllPattern

### Folders
- CollectionFolder::LayoutSemanticsGlossary::ConformanceAndDrift

### Usage
Use a catch-all only where the closed set holds one kind of thing, and state the criterion that picks between the real pattern and the catch-all.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Conformance Finding

### Summary
A finding about a deviation from a declared layout, with a kind (structure, naming or content-type) and a status.

### Description
A conformance finding has grain `conformance`, a `kind` and a `status`. Kind `structure`: status missing, unexpected or duplicate. Kind `naming`: status misnamed or off-grid. Kind `content-type`: status missing-field, invalid-value or unreadable, about an extracted field of an allowed manifest file. A misnamed finding also carries a `reason`. These kinds are kept apart from the kind of a component finding, and the loader refuses a rule that mixes them. The design also names an `immutability` kind for changes to sealed sets; it is not built. In Egeria a conformance finding that needs follow-up maps to a RequestForAction, linked by RequestForActionTarget to the element that needs work (modelling-standard item C6).

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::ConformanceFinding

### Folders
- CollectionFolder::LayoutSemanticsGlossary::ConformanceAndDrift

### Usage
Read the kind first: a structure finding asks for a file to be added or removed, a naming finding for a rename, and a content-type finding for a field to be fixed.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Conformance Category

### Summary
Whether a conformance check comes from the standard itself or from the study's own consistency rules, so the two can be scored apart.

### Description
A required item may carry `category: study-consistency`; the default is `standard`. Study-consistency checks are a regular study's protocol (every subject has every session) or files the profile requires that the standard only recommends. When a profile has such items, the score is also given per category, so a report can say "BIDS 69%, study consistency 94%". In Egeria the two categories become two QualityAnnotations with different `qualityDimension` values.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::ConformanceCategory

### Folders
- CollectionFolder::LayoutSemanticsGlossary::ConformanceAndDrift

### Usage
Never mix the two in one headline: a dataset can follow the standard fully and still be irregular as a study.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Conformance Score

### Summary
Conformant checked items divided by checked items, with the findings counted by kind and status.

### Description
Checked items are the entries judged, the required paths expected and the content fields read. Not-checked files and counted states are left out. The headline percentage is rounded down, so a tree with any finding never shows 100%: for example "97% conformant; 12 findings". Where categories exist the score is given per category as well. In Egeria a conformance score maps to a QualityAnnotation (`qualityDimension` "layout conformance", `qualityScore`, `qualityDescription`).

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::ConformanceScore

### Folders
- CollectionFolder::LayoutSemanticsGlossary::ConformanceAndDrift

### Usage
Quote the score with the finding count and the profile version; a score alone hides what was not checked.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Not Checked

### Summary
The treatment of parts of a tree that the profile's declared subset leaves out: shown and counted, never judged, and outside the score.

### Description
Not-checked is not the same as unexpected. In `bids-dataset`, `derivatives/`, `sourcedata/`, `code/`, `stimuli/`, `phenotype/`, datatypes other than anat, func, dwi and fmap, and inherited metadata files at the top, subject and session level are not checked. The list uses the standard's own names, not names taken from any one dataset.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::NotChecked

### Folders
- CollectionFolder::LayoutSemanticsGlossary::ConformanceAndDrift

### Usage
When a profile covers only part of a standard, mark the rest not-checked rather than leaving it to be reported as unexpected.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Inheritance Principle

### Summary
The BIDS rule that a metadata file placed higher in the tree applies to the matching data files below it.

### Description
Under the inheritance principle, sidecars and tables at the top level, subject level or session level hold metadata for the data files beneath them. `bids-dataset` does not model inheritance: such `*.json` and `*.tsv` files at the top, subject and session level are not checked. A dataset without sessions keeps its inherited files in the subject folder, so the rule applies at subject level as well as session level.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::InheritancePrinciple

### Folders
- CollectionFolder::LayoutSemanticsGlossary::ConformanceAndDrift

### Usage
Known limit: because inheritance is not modelled, these files are not judged at all, neither as right nor as wrong.

### Is Abstract Concept
True

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Drift

### Summary
The difference between two surveys of the same tree, by finding id: new, resolved and unchanged findings.

### Description
Drift compares the conformance findings of two survey snapshots by finding id. New findings are in the newer survey only, resolved ones in the older only, and unchanged ones in both; an unchanged id whose status or reason changed is marked changed. When either survey has part findings, drift also compares parts. Both surveys must use the same profile id and major version. A missing file keeps its id, so it stays unchanged until it is put back. Drift is not an Egeria type: in Egeria it is found by comparing the annotations of two SurveyReports by finding id (modelling-standard item C6), and each survey is kept, so the history can be rebuilt. A change to a sealed set is an immutability violation, not drift.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Drift

### Folders
- CollectionFolder::LayoutSemanticsGlossary::ConformanceAndDrift

### Usage
Report drift as a headline, for example "3 new since last survey; 0 resolved", and keep both snapshots.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Profile Instance

### Summary
A small YAML file beside a profile that states the values for one particular tree, such as one sweep's declared grid.

### Description
A profile instance has the keys `instance_of` (the profile id), `id`, `grid` and an optional `evidence`. It is passed with `--instance`, read whole (at most 64 KiB) with a safe loader, and listed in `content-reads.txt` and `classes.json` with its sha256. For `fea-sweep` it is the only content read. It is not an Egeria element; it is an input to the Resource Explorer. In Egeria a closed list of values could be held as ValidValue sets, one per parameter; ranges and the numeric normalisation of tokens cannot be expressed there and stay in the Resource Explorer.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::ProfileInstance

### Folders
- CollectionFolder::LayoutSemanticsGlossary::ConformanceAndDrift

### Usage
Put the facts that vary per tree in the instance, not in the profile, and never take them from a file inside the surveyed tree.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Declared Grid

### Summary
The allowed values of each parameter of a sweep, as declared in the profile instance.

### Description
The declared grid comes from the profile instance, never from the sweep's own `sweep.yaml`, which is never opened. Against it, each case folder gets two checks: off-grid (a token value outside the grid) and duplicate (a later folder whose parameters equal an earlier one's). With no instance there is no grid check at all. In Egeria, ValidValue sets (one per parameter) could hold the allowed values; this is a modelling convention, and the Architect's glossary rates it a partial fit.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::DeclaredGrid

### Folders
- CollectionFolder::LayoutSemanticsGlossary::ConformanceAndDrift

### Usage
Known limit: the grid is checked per token, so a grid that is not a full product cannot be declared, and a grid point with no case is not reported.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
State

### Summary
A counted condition of a folder that is not a defect, such as not-run for a case with no results.

### Description
A profile may declare states that are counted per typed folder, with their paths, in `classes.json`. They are not findings and are not in the score. In `fea-sweep`, a case without `job.frd` is `not-run`. In Egeria a not-run case has no run-attempt Process, or a planned attempt with an activity status of REQUESTED.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::State

### Folders
- CollectionFolder::LayoutSemanticsGlossary::ConformanceAndDrift

### Usage
Report states beside the score, for example "100% conformant; 0 findings; 12 not-run".

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

## Part 5: Evaluation Method

These terms say how a reported number was obtained, and so how far it can be trusted.

___

## Create Glossary Term

### Display Name
Answer Key

### Summary
A hand-written list of the expected components of one repository at one commit, and of what is explicitly not a component.

### Description
An answer key is a short YAML file of expected components (path and kind) and excluded classes (generated, vendored, fixture, tooling and so on), labelled from names, manifests and READMEs. It is kept outside the repository being measured and frozen by its hash. Builders never edit a key: a disagreement is written up, and the Architect makes a logged change. Keys follow the owner's key principle that fixtures, samples, templates and tooling are not components. Draft keys give provisional scores until they are reviewed.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::AnswerKey

### Folders
- CollectionFolder::LayoutSemanticsGlossary::EvaluationMethod

### Usage
Write a held-out key before any recognizer output exists for that repository.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Tune Set

### Summary
The repositories whose facts and keys the rules may be written and adjusted against.

### Description
The tune set for code repositories is three code repositories; for documentation sites it is a public tutorial sample and one documentation folder. Rules name the tune-set repositories that motivated them in `tuned_on`. Scores on the tune set are fits.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::TuneSet

### Folders
- CollectionFolder::LayoutSemanticsGlossary::EvaluationMethod

### Usage
A tune-set change that is not explained by the rule being added is a defect. Tune-set recall must not drop when a rule is added.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Dogfood

### Summary
A repository the team itself works in and knows well, used as an extra check of the rules.

### Description
Dogfood repositories have their own keys, but the builders know them and some rules were tuned on them, so their scores are reported as fits, not results.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Dogfood

### Folders
- CollectionFolder::LayoutSemanticsGlossary::EvaluationMethod

### Usage
Use the dogfood to see whether a rule makes sense on familiar ground, never as evidence that it generalizes.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Held-Out Repository

### Summary
A repository kept apart from all tuning, whose key is written first and which is scored once.

### Description
A held-out repository is picked by the owner and named in a pre-registration. Its key is written from names and READMEs before any recognizer output exists for it. Builders never list, open or run anything on it, and it is never named in a builder brief. The Architect runs the score once. Results are "key-blind, not fact-blind" when a brief or note carries facts about the repository, which weakens the claim without voiding it. A second run after any tuning is a new test that needs new repositories.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::HeldOutRepository

### Folders
- CollectionFolder::LayoutSemanticsGlossary::EvaluationMethod

### Usage
Never name a held-out repository in a rule, a brief, a test or this glossary.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Spent Repository

### Summary
A held-out repository that has been scored and whose misses are known, so it can never be a held-out test again.

### Description
Once a held-out repository is scored and its misses reported, it is spent. Its facts may then inform rules, and every such rule says so in `tuned_on`. Later scores on it are fits. Samples drawn for label checks become spent in the same way once rules are written from them.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::SpentRepository

### Folders
- CollectionFolder::LayoutSemanticsGlossary::EvaluationMethod

### Usage
Do not quote a re-score on a spent repository as evidence that a rule works elsewhere.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Reserve Repository

### Summary
A repository set aside for a future held-out test, recorded only in the Architect's own notes.

### Description
A reserve is never named in a builder brief; a reserve name that appeared in one brief was removed by amendment. Keeping reserves unnamed keeps them usable as clean held-out tests.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::ReserveRepository

### Folders
- CollectionFolder::LayoutSemanticsGlossary::EvaluationMethod

### Usage
Never name a reserve outside the Architect's own notes.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Pre-Registration

### Summary
A written record, made before any output exists, of exactly what a test will run and what it must meet.

### Description
A pre-registration names the repository, commit and path (or, for a generated tree, the seed and grid), the profile and version, the key's hash once written, any sampling seed and strata, and the target figures. It is logged before the run. A deviation from it is logged too, with the owner's agreement.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::PreRegistration

### Folders
- CollectionFolder::LayoutSemanticsGlossary::EvaluationMethod

### Usage
Write the pre-registration first; a target chosen after seeing the output is not a test.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Read-Back

### Summary
The Architect's check of each milestone before it counts: signature, trailers, files touched and every acceptance row.

### Description
At read-back the Architect checks the patch or commit against the brief: a valid signature, the required sign-off and no forbidden trailers, only the allowed files changed, each acceptance row met, and no held-out name in the rules (against a list the builder is not given). When work is saved as a patch first, the later signed commit's tree must equal the tree that was read.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::ReadBack

### Folders
- CollectionFolder::LayoutSemanticsGlossary::EvaluationMethod

### Usage
A milestone is not done until its read-back passes.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Fit

### Summary
A score on trees the rules were written against; it shows the rules can describe those trees, not that they will work on others.

### Description
Every score on the tune set, the dogfood or a spent repository is a fit. "Recall 1.00 on the tune set is a fit, not a result." Fits are still reported, row by row, so that a regression is seen.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Fit

### Folders
- CollectionFolder::LayoutSemanticsGlossary::EvaluationMethod

### Usage
Label every fit as a fit in a report.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Confirming Run

### Summary
The single, pre-registered run on fresh held-out repositories that decides whether a phase's rules count as confirmed.

### Description
A confirming run is done by the Architect, once, on the signed head of the phase, against keys written and frozen beforehand. A phase counts as confirmed only if the run meets the targets. A rule written after seeing a run's failures is not confirmed by that run; it needs another confirming run on new repositories.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::ConfirmingRun

### Folders
- CollectionFolder::LayoutSemanticsGlossary::EvaluationMethod

### Usage
Say "confirmed" only after a confirming run; until then, say "fits the tune set".

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Recall

### Summary
The share of the key's components that the recognizer found: true positives divided by the number of components in the key.

### Description
Recall is reported for the full list (components and parts) and for the top-level list. A first goal in the plan was to find 90% of labelled components.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Recall

### Folders
- CollectionFolder::LayoutSemanticsGlossary::EvaluationMethod

### Usage
Read recall with precision: listing every folder gives perfect recall and is useless.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Precision

### Summary
The share of the labelled candidates that are real components: true positives divided by true positives plus labelled false positives.

### Description
This project measures precision against the LABELLED candidates: TP / (TP + labelled false positives). An unlabelled candidate, one the answer key says nothing about, is reviewed by hand rather than counted as wrong, because it may point to a gap in the key rather than in the rules. The strict figure, true positives divided by all candidates, may be quoted as a secondary number, and the unlabelled count is always reported beside it. Today's behaviour, every folder as an asset, gave very low precision on the keyed repositories, which is the problem this project addresses.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Precision

### Folders
- CollectionFolder::LayoutSemanticsGlossary::EvaluationMethod

### Usage
Report the candidate, true-positive, labelled-false-positive and unlabelled counts with every precision figure.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Labelled False Positive

### Summary
A candidate that the answer key explicitly says is not a component.

### Description
A labelled false positive is a candidate the key excludes on purpose, for example as a fixture, example, tooling package or generated folder. A candidate the key says nothing about is unlabelled instead, and is reported separately because it may point to a gap in the key rather than in the rules.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::LabelledFalsePositive

### Folders
- CollectionFolder::LayoutSemanticsGlossary::EvaluationMethod

### Usage
Review labelled false positives by cause: the code-repository discoveries in this glossary started as groups of false components.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Byte-Identical Regression

### Summary
The check that a change leaves every output it should not affect exactly the same, byte for byte.

### Description
Every change shows hash lists of all outputs before and after, on the tune set, the dogfood and the generated samples, and two runs of the new code must also be byte-identical. A new engine feature must be inert for a profile that does not use it.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::ByteIdenticalRegression

### Folders
- CollectionFolder::LayoutSemanticsGlossary::EvaluationMethod

### Usage
Any difference that the change does not explain is a defect, however small.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Mutation Spec

### Summary
A YAML list of deviations to inject into a generated tree, with a truth file that records exactly what was injected.

### Description
A mutation spec lists mutation classes from a closed list, with variants and counts. The generator applies them in a fixed order and writes `truth.jsonl`, one line per injected deviation with its path, kind, status and expected rule. The survey never sees the truth file. For a held-out test the Architect writes the spec and seed, freezes them read-only before any output exists, and never shows them to the builder. The targets were mutation recall and finding precision of at least 0.95, with a clean tree giving no findings.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::MutationSpec

### Folders
- CollectionFolder::LayoutSemanticsGlossary::EvaluationMethod

### Usage
Compare the survey's conformance findings with the truth file by path, kind, status and rule; they should be equal, with nothing extra.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Generated Tree

### Summary
A synthetic tree written by a seeded generator, with empty or one-line files, so that the right answer is known exactly.

### Description
The generators (`samples/bids_gen.py`, `samples/fea_sweep_gen.py`) write a tree, its path list and a truth file. The same seed, sizes and spec give a byte-identical tree and truth. A tree with no mutations must score 100% conformant with no findings. Generated trees keep the key exact and keep third-party data out of the repository.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::GeneratedTree

### Folders
- CollectionFolder::LayoutSemanticsGlossary::EvaluationMethod

### Usage
Prefer a generated tree to copied data; use a real public dataset only as a reported sample, not a scored one.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

## Part 6: Scenario — Code Repositories

These terms come from recognizing components in source-code repositories.

___

## Create Glossary Term

### Display Name
Test Source Set

### Summary
A folder under `src` that holds one set of test sources, such as `src/test` or, in camelCase, `src/intTest` or `src/functionalTest`.

### Description
Build tools such as Gradle keep each set of sources in its own folder under `src`. A camelCase test source set is a test segment when BOTH its parent segment is exactly `src` AND its name is camelCase ending in `Test` or `Tests` after a lower-case start, or starts with a lower-case `test` or `tests` followed by capitalized words (case-sensitive: `^[a-z][a-z0-9]*(?:[A-Z][a-z0-9]*)*Tests?$` or `^tests?(?:[A-Z][a-z0-9]*)+$`). There is no list of prefix words. Manifest projects below such a folder are fixtures.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::TestSourceSet

### Folders
- CollectionFolder::LayoutSemanticsGlossary::CodeRepositories

### Usage
Known limits: Maven's `src/it` is not matched; a source set named without a test word (`src/e2e`, `src/benchmarks`) is not matched; a project under a Kotlin Multiplatform test source set (`commonTest`, `jvmTest`) is treated as a fixture, which is intended.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
CI-Configuration Folder

### Summary
A folder that holds a continuous-integration system's configuration, such as `.github` or `.teamcity`.

### Description
One closed list of CI-configuration folder names is used in two places: a manifest project below one of them is a tooling package, never a component, and every file below one of them gets file role `ci`. The list is `.github`, `.circleci`, `.buildkite`, `ci`, `.ci`, `.teamcity`, `.gitlab`, `.azure-pipelines`, `.azuredevops`, `.woodpecker`, `.tekton`, `.semaphore` and `.jenkins`, each matched as a whole path segment. For file roles a bare `ci` (no dot) counts only at the top level, because a deeper `ci` is often a source package.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::CIConfigurationFolder

### Folders
- CollectionFolder::LayoutSemanticsGlossary::CodeRepositories

### Usage
Known limit: a CI folder outside the closed list is not recognized; `teamcity/` without the dot is not on the list.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Documentation Folder

### Summary
A top-level `docs`, `doc` or `documentation` folder; it is a component only when it has a site or build configuration or real content.

### Description
A top-level documentation folder is a component only when either (i) it holds a site or build configuration file directly or in a direct child folder (`mkdocs.yml`, `mkdocs.yaml`, `docusaurus.config.*`, `conf.py`, `antora.yml`, `book.toml`, `_config.yml`, `package.json`, `pom.xml`, `build.gradle`, `build.gradle.kts`, `Makefile`), or (ii) at least 2 documentation files lie anywhere below it (`.md`, `.mdx`, `.rst`, `.adoc`, `.asciidoc`, `.txt`, `.ipynb`; images do not count). Names only; no file is opened. A folder with a site generator's configuration is a documentation site instead, whose navigation sections are components that are parts of the site.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::DocumentationFolder

### Folders
- CollectionFolder::LayoutSemanticsGlossary::CodeRepositories

### Usage
A folder that fails the test is not a component, but it is not hidden either: its files keep their roles and are counted.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Aggregator

### Summary
A manifest project that only groups other projects, such as a Maven parent with `pom` packaging; it is not a component, its members are.

### Description
Manifest reading makes workspace and module members components and makes their grouping parent an aggregator: a `pom.xml` with `pom` packaging and modules, a `package.json` that only declares workspaces, or a Gradle included project whose only children are other included projects. An included Gradle project with no directory of its own (such as a bill of materials) is not a component either. Without manifest content, a fallback treats five or more sibling manifests of the same kind under one parent as a workspace.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Aggregator

### Folders
- CollectionFolder::LayoutSemanticsGlossary::CodeRepositories

### Usage
Count the members, not the aggregator, when building an inventory.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Included Build

### Summary
A separate Gradle build that the main build pulls in with `includeBuild`; it is treated as internal tooling.

### Description
In `settings.gradle` or `settings.gradle.kts`, `includeBuild('<dir>')` marks `<dir>` as role tooling, read as a string literal by regular expression and never evaluated. Manifest projects inside it are not components. `buildSrc` is tooling in the same way.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::IncludedBuild

### Folders
- CollectionFolder::LayoutSemanticsGlossary::CodeRepositories

### Usage
Known limit: a composite build that includes a real product build is classed wrongly.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Benchmark Harness

### Summary
A project that exists to measure performance, such as a JMH benchmark module; it is test support, not a component.

### Description
A manifest project with a segment `benchmark`, `benchmarks`, `bench` or `jmh`, or one that starts or ends with one of them joined by `-` or `_`, is role `test-support` and is not a component.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::BenchmarkHarness

### Folders
- CollectionFolder::LayoutSemanticsGlossary::CodeRepositories

### Usage
Treat benchmark harnesses like fixtures when counting what a repository delivers.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

## Part 7: Scenario — BIDS Neuroimaging Datasets

These terms are restated from the BIDS specification, as the bids-dataset profile encodes them.

___

## Create Glossary Term

### Display Name
BIDS

### Summary
The Brain Imaging Data Structure: a community standard for organizing and naming neuroimaging data files.

### Description
BIDS fixes the folders, file names and metadata files of a neuroimaging dataset. The `bids-dataset` profile 0.1.1 encodes a declared subset of BIDS specification v1.11.2 (by the BIDS contributors, licensed CC-BY-4.0): the datatypes anat, func, dwi and fmap, the entities sub, ses, task, acq, dir, run and echo in the specification's order, the suffixes per datatype, and the top-level files. The public dataset ds000117 from bids-examples (CC0) is used as names and sizes only, as a reported sample, not a scored one. The bids-validator (MIT) is a reference only and is not part of the repository. In Egeria the dataset's standard version and licence would go in the DataSet's `additionalProperties` (modelling-standard item C7).

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::BIDS

### Folders
- CollectionFolder::LayoutSemanticsGlossary::BIDSDatasets

### Usage
Say "conforms to the bids-dataset subset of BIDS 1.11.2", never just "is valid BIDS": the subset does not check everything the validator checks.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Dataset Description File

### Summary
`dataset_description.json`, the required file at a BIDS dataset's root; three of its fields are the only content the BIDS profile reads.

### Description
Under `bids-dataset` only, and only at the recognized dataset root, the recognizer reads `BIDSVersion` (must look like `1.2.3`), `Name` (must not be empty) and `License` (must not be empty), each at most 256 characters, under the manifest reading caps. Problems are content-type findings: missing-field, invalid-value or unreadable. A missing file is a structure finding instead. No other field is copied anywhere.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::DatasetDescriptionFile

### Folders
- CollectionFolder::LayoutSemanticsGlossary::BIDSDatasets

### Usage
The License value is not checked against a list in version 0.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Subject and Session

### Summary
The two upper levels of a BIDS dataset: a folder `sub-<label>` per subject and, optionally, `ses-<label>` folders inside it.

### Description
A label is alphanumeric. `sub-emptyroom`, the specification's subject for MEG empty-room recordings, is outside the profile's subset and is not checked. Checks that every subject has every session seen in the dataset are study-consistency checks, because BIDS itself does not require a regular study. In Egeria subject and session folders map to DataFolder assets; the subject as a person is never catalogued.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::SubjectAndSession

### Folders
- CollectionFolder::LayoutSemanticsGlossary::BIDSDatasets

### Usage
A study whose subjects legitimately differ will have study-consistency findings; read them as a description of the study, not as errors.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Datatype Folder

### Summary
The folder inside a subject or session that groups data files of one kind, such as `anat`, `func`, `dwi` or `fmap`.

### Description
The profile checks the datatype folders anat, func, dwi and fmap. Other datatypes (meg, eeg, ieeg, beh, pet and others) are not checked: they are counted but not judged.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::DatatypeFolder

### Folders
- CollectionFolder::LayoutSemanticsGlossary::BIDSDatasets

### Usage
Known limit: files of a datatype outside the subset at session level, other than sidecars and tables, are still reported as unexpected.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Entity

### Summary
A key-label pair in a BIDS file name, such as `sub-01` or `task-rest`, which must appear in the specification's order.

### Description
An entity is written `<key>-<label>` and entities are joined by `_`. The profile knows sub, ses, task, acq, dir, run and echo; `run` and `echo` take numbers; `task` is required for the bold, sbref and events suffixes. An entity out of order or with an unknown key makes the file misnamed, with reason entity-order or unknown-entity.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Entity

### Folders
- CollectionFolder::LayoutSemanticsGlossary::BIDSDatasets

### Usage
Known limit: any other BIDS entity (ce, rec, mod, part and so on) is reported as unknown-entity in version 0.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Suffix

### Summary
The last part of a BIDS file name before the extension, saying what the file holds, such as `T1w`, `bold` or `phasediff`.

### Description
Each datatype has its own list of allowed suffixes: for example anat allows T1w, T2w, FLAIR, PDw and FLASH, and func allows bold, sbref and events. A suffix not on the list makes the file misnamed with reason suffix.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Suffix

### Folders
- CollectionFolder::LayoutSemanticsGlossary::BIDSDatasets

### Usage
Known limit: only the listed suffixes are accepted; others that BIDS allows, such as T2starw, are reported.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Sidecar

### Summary
A metadata file, usually JSON, that sits beside a data file and describes it.

### Description
Sidecars share the data file's name with a different extension. Their content is never read: generated trees write `{}` as their content. Sidecars and tables at the top, subject and session level hold inherited metadata and are not checked.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Sidecar

### Folders
- CollectionFolder::LayoutSemanticsGlossary::BIDSDatasets

### Usage
Known limit: sidecar content is not checked at all; the validator checks it and this profile does not.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
BIDS Top-Level Files

### Summary
`README`, `participants.tsv` and `CHANGES` at the dataset root: required by the profile, but scored as study consistency.

### Description
The profile requires all three. BIDS 1.11.2 recommends README and participants.tsv and makes CHANGES optional, so the profile scores all three as study consistency rather than as the standard. README.md, README.rst and README.txt are allowed but do not satisfy the README requirement. The content of participants.tsv is never read.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::BIDSTopLevelFiles

### Folders
- CollectionFolder::LayoutSemanticsGlossary::BIDSDatasets

### Usage
A dataset without these files can still conform fully to the standard; the study-consistency score shows the gap.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

## Part 8: Scenario — Simulation Sweeps

These terms follow the Architect's glossary of simulation studies, including its mapping to Egeria types.

___

## Create Glossary Term

### Display Name
Study

### Summary
The investigation as a piece of work: its goal, owner, method and decisions.

### Description
A study is not visible from file names; its README and `sweep.yaml` are present but never read. In Egeria a study maps to a Project with the StudyProject classification (a focused analysis), or to an Experiment, which tests a hypothesis; related studies can be grouped by a Campaign project.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Study

### Folders
- CollectionFolder::LayoutSemanticsGlossary::SimulationSweeps

### Usage
Keep the study (the work) apart from the sweep (its data).

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Sweep

### Summary
The set of cases generated from one template over one declared parameter grid: the data side of a study.

### Description
In layout terms a sweep is ONE component, kind simulation-sweep: the folder `study-<name>/` that holds `sweep.yaml`. Its templates, materials and meshes are supporting inputs; its cases are parts. In Egeria a sweep maps to a Collection (or a DataSet) that holds the cases and is linked to the study's Project; this is the modelling-standard item C2 (gap G1 in the simulation glossary), a convention and not an Egeria change.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Sweep

### Folders
- CollectionFolder::LayoutSemanticsGlossary::SimulationSweeps

### Usage
A sweep is never a case, and a case is never the sweep.

### Example
"1 sweep, 60 cases": the default generated grid of 4 moduli by 5 thicknesses by 3 mesh levels.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Case

### Summary
One point of a sweep's grid: one combination of parameter values, with its own folder and input deck.

### Description
A case folder is `cases/case_E<E>_t<t>_mesh-<level>/`, where `p` is the decimal point (`t2p0` is 2.0). It is a part of the sweep, and its finding carries the parameter tokens. It requires `job.inp`. Its identity is stable over time. In Egeria a case maps to a DataFolder or FileFolder asset (or a DataSet), a member of the sweep's Collection (modelling-standard item C3). Egeria has no first-class element for a case's parameter values: that is candidate gap G2, not a decided feature, and `additionalProperties` is the interim option.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Case

### Folders
- CollectionFolder::LayoutSemanticsGlossary::SimulationSweeps

### Usage
Use "case" for the grid point and "run attempt" for an execution of it.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Run Attempt

### Summary
One execution of a case: its start, end, status and the outputs it wrote. A case has zero, one or many attempts.

### Description
A run attempt is the unit that should be immutable once finished. fea-sweep 0.1.0 does not model attempts: one folder per case holds one set of outputs. A proposed layout, `cases/<case>/attempts/<NNN>/`, numbers attempts and never reuses a number; it is not built and waits for the owner's decision. In Egeria a run attempt maps to a Process for one execution, such as a TransientEmbeddedProcess with `deployedImplementationType` set to the solver, using its `activityStatus`, `startTime` and `completionTime`, with DataFlow lineage for its inputs and outputs (modelling-standard item C4); a named subtype is optional (gap G3).

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::RunAttempt

### Folders
- CollectionFolder::LayoutSemanticsGlossary::SimulationSweeps

### Usage
In this project "run" means a run attempt, never a case.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Run Status

### Summary
The outcome of a run attempt: completed, failed, cancelled, abandoned and so on.

### Description
From names alone, "ran" means the case holds `job.frd`, and a failure cannot be told from a success without reading a status file. In Egeria run status maps to `activityStatus` (ActivityStatus: REQUESTED through IN_PROGRESS, COMPLETED, FAILED, CANCELLED, ABANDONED, IGNORED and OTHER).

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::RunStatus

### Folders
- CollectionFolder::LayoutSemanticsGlossary::SimulationSweeps

### Usage
Report "ran (outcome unknown)" rather than "succeeded" while only names are read.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Re-Run

### Summary
A new attempt of the same case with unchanged parameters.

### Description
A re-run is invisible today, because the solver writes its files in place. A copied attempt folder (`case_..._v2`, `_old`) is reported as a misnamed case, or as a duplicate when its parameters match. In Egeria a re-run maps to a second attempt Process under the same case; the IGNORED activity status ("another activity has superseded it") can mark the superseded attempt.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::ReRun

### Folders
- CollectionFolder::LayoutSemanticsGlossary::SimulationSweeps

### Usage
Do not copy case folders to keep an old attempt; that breaks the case grammar. Wait for the attempt layout.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Restart

### Summary
An attempt that continues from another attempt's restart file, rather than starting from the beginning.

### Description
A CalculiX restart writes a `.rout` file and reads a `.rin` file. Both are hidden as generated restart data (kind solver-restart). In Egeria the chain maps to lineage: a DataFlow from the earlier attempt's restart file to the new attempt.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Restart

### Folders
- CollectionFolder::LayoutSemanticsGlossary::SimulationSweeps

### Usage
Keep restart files with the attempt that wrote them; they are the link between attempts.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Result Set

### Summary
The outputs of one run attempt, together with their post-processing.

### Description
A result set is the solver results of an attempt (`.frd`, `.dat`, `.12d`), which are generated and hidden but counted, and its post-processing folder `post/<case-id>/`, which is derived and supporting. A post folder with no matching case is structure/unexpected. In Egeria result sets map to DataFile or DataFileCollection assets with a DataFlow from the attempt; approval goes in `contentStatus` (modelling-standard item C5). An archived attempt, whose files are gone but whose record stays for lineage, maps to the Memento classification.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::ResultSet

### Folders
- CollectionFolder::LayoutSemanticsGlossary::SimulationSweeps

### Usage
Cite the result set of the current attempt in a review, never "the latest files".

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Current Attempt

### Summary
The attempt whose results count for review, chosen explicitly and never inferred from "the latest".

### Description
The proposal is to declare the current attempt in the profile instance or in a marker file in the case folder (which, being content, would need a ruling). It is not built. Egeria has no dedicated relationship for it; the options are a membership status on the case's Collection, or ContentStatus APPROVED on that attempt's result set (gap G4).

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::CurrentAttempt

### Folders
- CollectionFolder::LayoutSemanticsGlossary::SimulationSweeps

### Usage
Until it is declared, no attempt is current; do not guess.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Seal

### Summary
Freezing a finished attempt or result set: a checksum list recorded once and checked again at every survey.

### Description
After sealing, any change to the set is an `immutability` finding, which is a violation, not ordinary drift. Sealing is not built (use case UC14). In Egeria the Retention classification covers how long data is kept; no element was found for the seal itself (checksum list, sealed-at, verified-at). That is candidate gap G6, to be raised after a platform check; it is not an existing or decided Egeria feature.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::Seal

### Folders
- CollectionFolder::LayoutSemanticsGlossary::SimulationSweeps

### Usage
Who may seal is open; the design's position is that the Resource Explorer records seal evidence and a person or system seals.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Input Deck

### Summary
The solver input file of a case: for CalculiX, `job.inp`.

### Description
Every case folder must hold `job.inp`; a missing deck is structure/missing at `<case>/job.inp`. The base deck that every case is derived from is `templates/base.inp`, and shared inputs are materials and Gmsh meshes (`mesh/<part>_<level>.msh`). Deck content is never read. In Egeria an input deck maps to a DataFile asset with a DataFlow from the template deck; it must not be confused with Egeria's Template classification, which is for metadata templates.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::InputDeck

### Folders
- CollectionFolder::LayoutSemanticsGlossary::SimulationSweeps

### Usage
A case with results but no deck is still a missing-deck finding: the results cannot be traced to an input.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Solver Results

### Summary
The results files a CalculiX run writes: `.frd` results, `.dat` printed output and `.12d` eigen data.

### Description
Solver results are role generated, kind solver-results: hidden by default and counted. The presence of `.frd` is what "ran" means in fea-sweep 0.1.0.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::SolverResults

### Folders
- CollectionFolder::LayoutSemanticsGlossary::SimulationSweeps

### Usage
Use the hidden count to see how much of a sweep is output; use the result set to say which outputs belong to which attempt.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Solver Status and Log Files

### Summary
The files a CalculiX run writes about itself: `.sta` step status, `.cvg` convergence, `.msg` messages, and the case's `run.log`.

### Description
They are runtime output, hidden. A case that ran (it holds `job.frd`) must also hold `job.sta`. Their content is never read, which is why a failed run cannot be told from a good one.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::SolverStatusFiles

### Folders
- CollectionFolder::LayoutSemanticsGlossary::SimulationSweeps

### Usage
Reading one status file per attempt is an open decision (D2) for the owner.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

## Part 9: What the Scenarios Discovered

Each entry is a lesson: what was learned, which rule or decision followed, and the limit that is still known.

___

## Create Glossary Term

### Display Name
Test Source Sets Hold Fixtures, Not Components

### Summary
Manifest projects inside camelCase test source sets such as `src/intTest` are fixtures for tests, not components.

### Description
On a held-out code repository (now spent), the build's camelCase test source sets turned out to hold many small sample projects, each with its own manifest, which the recognizer listed as component candidates. Phase 1e had already recorded this as a known gap. The Phase 1f rule makes a camelCase test source set under `src` a test segment, using the shape of the name and no word list, so those projects become fixtures.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::TestSourceSetsHoldFixtures

### Folders
- CollectionFolder::LayoutSemanticsGlossary::Discoveries

### Usage
Learned: a manifest inside a test source set describes a test input, not a product. Known limit: `src/it`, `src/e2e` and `src/benchmarks` are not matched; Kotlin Multiplatform test source sets are treated as fixtures on purpose.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
CI Folders Are Tooling

### Summary
A build file inside a CI-configuration folder, such as the `pom.xml` that TeamCity's Kotlin DSL keeps in `.teamcity`, does not make that folder a component.

### Description
A confirming run found `.teamcity` reported as a Maven module, because the folder holds a `pom.xml` and was in neither the tooling list nor the CI file-role list. Phase 1g made one closed list of CI-configuration folders and used it in both places, so a manifest under one is tooling and its files are role ci.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::CIFoldersAreTooling

### Folders
- CollectionFolder::LayoutSemanticsGlossary::Discoveries

### Usage
Learned: CI configuration can carry build files of its own, and one list used in two places keeps the rules consistent. Known limit: a CI folder outside the closed list is still not recognized.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
A Docs Folder Needs Real Content

### Summary
A top-level `docs` folder is a component only when it has a site or build configuration or at least two documentation files.

### Description
A confirming run found a top-level `docs/` holding one notes file reported as a documentation component, because the rule took any top-level docs folder whatever it held. Phase 1g added a minimum-content test, by names only.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::DocsFolderNeedsContent

### Folders
- CollectionFolder::LayoutSemanticsGlossary::Discoveries

### Usage
Learned: a folder name alone does not make a documentation set. Known limit: the threshold of 2 is a judgement, open to review; a folder of two notes counts; a site configuration deeper than one level below the folder is not seen.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Deprecated BIDS Suffixes Are Still Valid

### Summary
A suffix that BIDS deprecates, such as FLASH, is still valid and must not be reported as misnamed.

### Description
On the public ds000117 sample, bids-dataset 0.1.0 reported 224 suffix findings for FLASH images, because the profile listed only current suffixes. BIDS 1.11.2 deprecates FLASH but still allows it, so 0.1.1 lists it. Two similar facts (`.nii` is valid BIDS beside `.nii.gz`; `sub-emptyroom` belongs to MEG) were also corrected from the specification's own text.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::DeprecatedSuffixesStillValid

### Folders
- CollectionFolder::LayoutSemanticsGlossary::Discoveries

### Usage
Learned: encode what the standard ALLOWS, not only what it recommends, and correct the profile from the specification's text, not from one dataset. Known limit: other valid suffixes outside the list are still reported.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Inherited Metadata Is Not Judged at Subject or Session Level

### Summary
Sidecars and tables at the top, subject and session level hold inherited metadata and are not checked.

### Description
On the public ds000117 sample, bids-dataset 0.1.0 reported 16 MEG `channels.tsv` files at session level as unexpected. Under BIDS inheritance such files legitimately sit above the data they describe, at session level and, in a dataset without sessions, at subject level. Version 0.1.1 leaves `*.json` and `*.tsv` not checked at both levels.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::InheritedMetadataNotJudged

### Folders
- CollectionFolder::LayoutSemanticsGlossary::Discoveries

### Usage
Learned: a closed set must make room for the standard's inheritance before it can call a file unexpected. Known limit: inheritance is not modelled, so these files are not judged at all, neither right nor wrong.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Names Alone Cannot Tell a Failed Run from a Good One

### Summary
From file names, a run that failed after writing partial results looks the same as one that succeeded.

### Description
fea-sweep 0.1.0 treats a case as ran when it holds `job.frd`. A failed attempt that wrote partial results is not told apart from a good one; that needs the content of the status file. Two options are open for the owner's decision D2: stay names-only and report "ran (outcome unknown)", or allow one narrow status-file read per attempt under an explicit exception like the one for `dataset_description.json`.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::NamesCannotTellFailedRun

### Folders
- CollectionFolder::LayoutSemanticsGlossary::Discoveries

### Usage
Learned: run outcome is content, not layout. Known limit: until D2 is decided, every "ran" figure means "wrote results", not "succeeded".

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Re-Runs Overwrite in Place and Are Invisible

### Summary
Because CalculiX writes `job.*` in place, a re-run replaces the previous attempt's files and leaves no trace in the layout.

### Description
fea-sweep 0.1.0 has one folder per case. A re-run overwrites the earlier attempt, so the layout shows only the last one. A copied attempt folder (`case_..._v2`, `_old`) is reported as a misnamed case, or as a duplicate when its parameters match. The proposed fix is an attempt layout, `cases/<case>/attempts/<NNN>/`, with sealing and a declared current attempt; none of it is built (decision D1).

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::ReRunsAreInvisible

### Folders
- CollectionFolder::LayoutSemanticsGlossary::Discoveries

### Usage
Learned: a layout cannot show history that the tool overwrites. Known limit: until attempts are modelled, nothing shows how many times a case was run, or which run the results came from.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
A Rename Shows as One Resolved and One New Finding

### Summary
Because finding ids are made from paths, drift reports a renamed folder as a resolved finding plus a new one, not as a move.

### Description
In the sweep drift test (6 cases added, 2 removed, 1 renamed), parts came out 7 new, 3 resolved and 57 unchanged: the rename is one of each. This is the price of ids that are stable without reading content.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::RenameIsResolvePlusNew

### Folders
- CollectionFolder::LayoutSemanticsGlossary::Discoveries

### Usage
Learned: path-based identity is stable and cheap but blind to moves. Known limit: move detection is backlog.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

___

## Create Glossary Term

### Display Name
Study Consistency Must Be Scored Apart from the Standard

### Summary
Checks a profile adds beyond the standard, such as every subject having every session, must be scored separately or they distort the standard's score.

### Description
On the public ds000117 sample, bids-dataset 0.1.0 scored 0.722 with 245 findings. After separating study-consistency checks from the standard, and fixing the FLASH suffix and the inheritance gap, 0.1.1 scored 0.994: the standard 1.0 with no findings, and study consistency 0.949 with 5 findings, all of them subjects that have no `dwi` folder. The sample is reported, not scored against a target.

### Glossary Name
Glossary::LayoutSemanticsGlossary

### Qualified Name
Glossary::LayoutSemanticsGlossary::StudyConsistencyApart

### Folders
- CollectionFolder::LayoutSemanticsGlossary::Discoveries

### Usage
Learned: a stricter-than-standard profile must label its additions, or a conforming dataset looks broken. Known limit: a study whose subjects legitimately differ still gets study-consistency findings.

### Authors
- Dan Wolfson

### Version Identifier
1.0

### Content Status
DRAFT

___

---

## Part 10: Term Relationships

The relationships tie each scenario term and each lesson back to the model terms it depends on. Most are `RelatedTerm` with an expression that reads from Term 1 to Term 2; `ISARelationship` says that Term 1 is a kind of Term 2, and the one `Antonym` records the difference between a fit and a confirming run.

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::ProfileRule

### Term 2
Glossary::LayoutSemanticsGlossary::LayoutProfile

### Expression
is one ordered entry of

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::RuleBasis

### Term 2
Glossary::LayoutSemanticsGlossary::ProfileRule

### Expression
is carried by every

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Confidence

### Term 2
Glossary::LayoutSemanticsGlossary::ProfileRule

### Expression
is set on each

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Evidence

### Term 2
Glossary::LayoutSemanticsGlossary::ProfileRule

### Expression
is required on each

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::ProfileComposition

### Term 2
Glossary::LayoutSemanticsGlossary::LayoutProfile

### Expression
builds one from several

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::ProposedStatus

### Term 2
Glossary::LayoutSemanticsGlossary::LayoutProfile

### Expression
is the status of every unconfirmed

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Recognizer

### Term 2
Glossary::LayoutSemanticsGlossary::LayoutProfile

### Expression
applies one or more

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Recognizer

### Term 2
Glossary::LayoutSemanticsGlossary::PathList

### Expression
reads

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Recognizer

### Term 2
Glossary::LayoutSemanticsGlossary::SurveySnapshot

### Expression
writes one

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Recognizer

### Term 2
Glossary::LayoutSemanticsGlossary::ManifestReading

### Expression
reads content only under

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::FindingId

### Term 2
Glossary::LayoutSemanticsGlossary::Finding

### Expression
identifies each

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::SurveySnapshot

### Term 2
Glossary::LayoutSemanticsGlossary::Finding

### Expression
holds the

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
ISARelationship

### Term 1
Glossary::LayoutSemanticsGlossary::Part

### Term 2
Glossary::LayoutSemanticsGlossary::Component

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Candidate

### Term 2
Glossary::LayoutSemanticsGlossary::Component

### Expression
is a proposed

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::FileRole

### Term 2
Glossary::LayoutSemanticsGlossary::RelevanceClass

### Expression
is shown or hidden by its

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::GeneratedContent

### Term 2
Glossary::LayoutSemanticsGlossary::RelevanceClass

### Expression
is hidden by its

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::VendoredContent

### Term 2
Glossary::LayoutSemanticsGlossary::RelevanceClass

### Expression
is hidden by its

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::RuntimeOutput

### Term 2
Glossary::LayoutSemanticsGlossary::RelevanceClass

### Expression
is hidden by its

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Fixture

### Term 2
Glossary::LayoutSemanticsGlossary::Component

### Expression
is never a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::ToolingPackage

### Term 2
Glossary::LayoutSemanticsGlossary::Component

### Expression
is never a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::LayoutProfile

### Term 2
Glossary::LayoutSemanticsGlossary::LayoutStandard

### Expression
encodes a declared subset of a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::PathGrammar

### Term 2
Glossary::LayoutSemanticsGlossary::Token

### Expression
defines each

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::CatchAllPattern

### Term 2
Glossary::LayoutSemanticsGlossary::PathGrammar

### Expression
is a never-matching

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::CatchAllPattern

### Term 2
Glossary::LayoutSemanticsGlossary::ClosedSet

### Expression
makes every wrong name misnamed within a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::NotChecked

### Term 2
Glossary::LayoutSemanticsGlossary::ClosedSet

### Expression
is the escape from a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
ISARelationship

### Term 1
Glossary::LayoutSemanticsGlossary::ConformanceFinding

### Term 2
Glossary::LayoutSemanticsGlossary::Finding

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::RequiredItem

### Term 2
Glossary::LayoutSemanticsGlossary::ConformanceFinding

### Expression
gives a missing

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::ConformanceScore

### Term 2
Glossary::LayoutSemanticsGlossary::ConformanceFinding

### Expression
counts

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::ConformanceScore

### Term 2
Glossary::LayoutSemanticsGlossary::ConformanceCategory

### Expression
is given per

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::ConformanceScore

### Term 2
Glossary::LayoutSemanticsGlossary::NotChecked

### Expression
leaves out

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Drift

### Term 2
Glossary::LayoutSemanticsGlossary::SurveySnapshot

### Expression
compares two

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Drift

### Term 2
Glossary::LayoutSemanticsGlossary::FindingId

### Expression
is computed by

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::DeclaredGrid

### Term 2
Glossary::LayoutSemanticsGlossary::ProfileInstance

### Expression
is declared in the

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::State

### Term 2
Glossary::LayoutSemanticsGlossary::ConformanceScore

### Expression
is counted beside, not in, the

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::AnswerKey

### Term 2
Glossary::LayoutSemanticsGlossary::Candidate

### Expression
labels each

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Recall

### Term 2
Glossary::LayoutSemanticsGlossary::AnswerKey

### Expression
is measured against the

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Precision

### Term 2
Glossary::LayoutSemanticsGlossary::Candidate

### Expression
is the true share of

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::LabelledFalsePositive

### Term 2
Glossary::LayoutSemanticsGlossary::AnswerKey

### Expression
is excluded explicitly by the

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::TuneSet

### Term 2
Glossary::LayoutSemanticsGlossary::Fit

### Expression
gives only a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Dogfood

### Term 2
Glossary::LayoutSemanticsGlossary::Fit

### Expression
gives only a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::SpentRepository

### Term 2
Glossary::LayoutSemanticsGlossary::HeldOutRepository

### Expression
is a used-up

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::ReserveRepository

### Term 2
Glossary::LayoutSemanticsGlossary::HeldOutRepository

### Expression
is a future

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::PreRegistration

### Term 2
Glossary::LayoutSemanticsGlossary::ConfirmingRun

### Expression
is written before every

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::ConfirmingRun

### Term 2
Glossary::LayoutSemanticsGlossary::HeldOutRepository

### Expression
is run once on a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
Antonym

### Term 1
Glossary::LayoutSemanticsGlossary::Fit

### Term 2
Glossary::LayoutSemanticsGlossary::ConfirmingRun

### Expression
a fit shows the rules describe what they were written on; a confirming run tests them on what they were not

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::MutationSpec

### Term 2
Glossary::LayoutSemanticsGlossary::GeneratedTree

### Expression
is injected into a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::ReadBack

### Term 2
Glossary::LayoutSemanticsGlossary::ByteIdenticalRegression

### Expression
checks the

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::TestSourceSet

### Term 2
Glossary::LayoutSemanticsGlossary::Fixture

### Expression
holds projects that are each a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::CIConfigurationFolder

### Term 2
Glossary::LayoutSemanticsGlossary::ToolingPackage

### Expression
makes any manifest project below it a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::IncludedBuild

### Term 2
Glossary::LayoutSemanticsGlossary::ToolingPackage

### Expression
is treated as a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::BenchmarkHarness

### Term 2
Glossary::LayoutSemanticsGlossary::Fixture

### Expression
is excluded like a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Aggregator

### Term 2
Glossary::LayoutSemanticsGlossary::Component

### Expression
groups members that are each a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::DocumentationFolder

### Term 2
Glossary::LayoutSemanticsGlossary::Component

### Expression
is a component only with content, as a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
ISARelationship

### Term 1
Glossary::LayoutSemanticsGlossary::BIDS

### Term 2
Glossary::LayoutSemanticsGlossary::LayoutStandard

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::SubjectAndSession

### Term 2
Glossary::LayoutSemanticsGlossary::PathGrammar

### Expression
is described by a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::DatatypeFolder

### Term 2
Glossary::LayoutSemanticsGlossary::PathGrammar

### Expression
is described by a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Entity

### Term 2
Glossary::LayoutSemanticsGlossary::NameGrammar

### Expression
is ordered by the

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Suffix

### Term 2
Glossary::LayoutSemanticsGlossary::NameGrammar

### Expression
is listed per datatype in the

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::DatasetDescriptionFile

### Term 2
Glossary::LayoutSemanticsGlossary::ManifestReading

### Expression
is read for three fields under

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Sidecar

### Term 2
Glossary::LayoutSemanticsGlossary::InheritancePrinciple

### Expression
is placed higher in the tree under the

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::BIDSTopLevelFiles

### Term 2
Glossary::LayoutSemanticsGlossary::ConformanceCategory

### Expression
are scored as study consistency in the

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Sweep

### Term 2
Glossary::LayoutSemanticsGlossary::Study

### Expression
is the data side of a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Case

### Term 2
Glossary::LayoutSemanticsGlossary::Sweep

### Expression
is one grid point of a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Case

### Term 2
Glossary::LayoutSemanticsGlossary::Part

### Expression
is recognized as a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Sweep

### Term 2
Glossary::LayoutSemanticsGlossary::Component

### Expression
is recognized as one

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::DeclaredGrid

### Term 2
Glossary::LayoutSemanticsGlossary::Sweep

### Expression
states the allowed parameter values of a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::RunAttempt

### Term 2
Glossary::LayoutSemanticsGlossary::Case

### Expression
is one execution of a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::RunStatus

### Term 2
Glossary::LayoutSemanticsGlossary::RunAttempt

### Expression
is the outcome of a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
ISARelationship

### Term 1
Glossary::LayoutSemanticsGlossary::ReRun

### Term 2
Glossary::LayoutSemanticsGlossary::RunAttempt

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
ISARelationship

### Term 1
Glossary::LayoutSemanticsGlossary::Restart

### Term 2
Glossary::LayoutSemanticsGlossary::RunAttempt

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::ResultSet

### Term 2
Glossary::LayoutSemanticsGlossary::RunAttempt

### Expression
is written by one

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::CurrentAttempt

### Term 2
Glossary::LayoutSemanticsGlossary::RunAttempt

### Expression
is the declared, counting

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::Seal

### Term 2
Glossary::LayoutSemanticsGlossary::ResultSet

### Expression
freezes a finished

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::InputDeck

### Term 2
Glossary::LayoutSemanticsGlossary::Case

### Expression
is required in every

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::SolverResults

### Term 2
Glossary::LayoutSemanticsGlossary::ResultSet

### Expression
are the solver part of a

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::SolverResults

### Term 2
Glossary::LayoutSemanticsGlossary::GeneratedContent

### Expression
are hidden as

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::SolverStatusFiles

### Term 2
Glossary::LayoutSemanticsGlossary::RuntimeOutput

### Expression
are hidden as

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::SolverStatusFiles

### Term 2
Glossary::LayoutSemanticsGlossary::RunStatus

### Expression
hold, unread, the

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::State

### Term 2
Glossary::LayoutSemanticsGlossary::Case

### Expression
counts not-run for each

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::TestSourceSetsHoldFixtures

### Term 2
Glossary::LayoutSemanticsGlossary::TestSourceSet

### Expression
is the lesson behind the rule for

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::CIFoldersAreTooling

### Term 2
Glossary::LayoutSemanticsGlossary::CIConfigurationFolder

### Expression
is the lesson behind the list of

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::DocsFolderNeedsContent

### Term 2
Glossary::LayoutSemanticsGlossary::DocumentationFolder

### Expression
is the lesson behind the test for

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::DeprecatedSuffixesStillValid

### Term 2
Glossary::LayoutSemanticsGlossary::Suffix

### Expression
corrected the list of

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::InheritedMetadataNotJudged

### Term 2
Glossary::LayoutSemanticsGlossary::InheritancePrinciple

### Expression
applies the

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::NamesCannotTellFailedRun

### Term 2
Glossary::LayoutSemanticsGlossary::RunStatus

### Expression
is the known limit on

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::ReRunsAreInvisible

### Term 2
Glossary::LayoutSemanticsGlossary::ReRun

### Expression
is the known limit on

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::RenameIsResolvePlusNew

### Term 2
Glossary::LayoutSemanticsGlossary::FindingId

### Expression
is a consequence of the path-based

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

___

## Link Term-Term Relationship

### Relationship Type
RelatedTerm

### Term 1
Glossary::LayoutSemanticsGlossary::StudyConsistencyApart

### Term 2
Glossary::LayoutSemanticsGlossary::ConformanceCategory

### Expression
is the lesson behind the

### Steward
Dan Wolfson

### Term Relationship Status
DRAFT

___

---

## What the glossary is for

The point of fixing these words is that a layout result can then be read the same way by the person who built the rule,
the person who reviews it and the person who relies on it.  "1 sweep, 60 cases, 61% hidden output" means something
exact once **sweep**, **case**, **part** and **relevance class** are agreed; "97% conformant; 12 findings" means
something exact once **conformance score**, **not checked** and **conformance category** are.

The evaluation terms matter just as much.  A number from the tune set is a **fit**; a number from a **confirming run**
on a **held-out repository** is a result.  The code-repository lessons in the last folder began as false components on runs
that the rules had not seen, and the BIDS lessons as findings on a public sample that the specification's own text
showed to be wrong.  Each was turned into a general rule, by the shape of a name, a count or the standard's text rather
than by a list of repository names, and a rule tuned after seeing a run still needs a fresh run to be confirmed.

Two of the lessons are limits rather than fixes: names alone cannot say whether a run succeeded, and a solver that
overwrites its files leaves no history in the layout.  They are recorded so that nobody reads more into a layout result
than the layout can show.
