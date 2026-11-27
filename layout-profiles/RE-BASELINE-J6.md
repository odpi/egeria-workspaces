# Re-baseline after Phase 1j J6: finding ids are made from the defining profile

**What changed.** Before J6, `finding_id = sha256(<run profile id>@<run profile major> | rule | path)`: the id of a finding depended on which profile (or
composition, such as `code-repo-conventions+docs-site`) ran the survey. From J6 (Dan's decision D-J3), `finding_id = sha256(<defining profile id>@<its major>
| rule | path)`, where the defining profile is the one whose file defines the rule (an in-place replacement in an overlay defines it anew; a structural rule
is defined by the profile that declares it). Composed profile ids no longer enter the hash.

**Which ids change.** Every finding whose rule is defined by a profile other than the one that ran the survey: in a run of `code-repo-conventions`, the
findings of the rules of `code-repo` and `generic-relevance` (and their file-role rules); in a run of a composition, every finding (the composite id was in
every hash before). Findings of rules defined by the run's own profile keep their ids. Nothing else in any output changes: the same findings, paths, rules,
roles, counts and configuration record; only the `finding_id` field moves.

**Why.** A rule keeps its id whichever profile or composition runs it, so a user overlay that changes nothing, or a composition, keeps every id, and an overlay
that replaces one rule changes only that rule's ids.

**Consequences for Phase 2 drift baselines (NB05, 04a).** Drift compares surveys BY finding id, so drift across the J6 boundary is not meaningful: a survey
made before J6 and one made after it differ in ids that did not change in substance. **Every Phase 2 drift baseline (NB05 and 04a) needs a new survey after
J6**, and drift is compared only between surveys made on the same side of J6. The NB05 and 04a outputs are otherwise identical across J6 except the
`finding_id` fields. (A configuration change is reported separately by `recognizer.config_drift`; the J6 boundary is not a configuration change, so it must be
handled by re-surveying, as above.)

The per-repository counts, the old -> new id maps and the new hash lists of the regression repositories and NB05 are kept with the Phase 1j J6 read-back.
