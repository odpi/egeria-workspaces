<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Mapping TestGen results into Egeria (design only)

**Status:** mapping only. Nothing in this directory writes to Egeria. Publishing is Resource
Explorer's job, through its quality slice 1 publisher (not yet built). A write to the dev
Egeria is a shared write that needs a peer round and Dan's word.

**Baseline:** Resource Explorer's
`packages/resource-explorer/docs/design-notes/DESIGN-VALUE-PROFILE-AND-QUALITY-CHECKS.md`
(trellis), §7 for `DataQualityRule`s and §8 for `QualityAnnotation`s. That mapping is decided,
and **this note does not restate or change it.** It only says what differs when the check was
run by TestGen rather than by RE, using the fields that `scripts/export_testgen.py` exports.

## One rule, two engines

A TestGen test and an RE check for the same column and test type have the same `check_key`,
`schema.table[.column]::Test_Type`. So they evaluate **the same `DataQualityRule`**, whose
qualified name §7 roots at the database Asset:
`<databaseAssetQN>::Quality::<check_key>`. A TestGen result never creates a second rule. It is
a second set of evidence against the rule a person accepted in RE.

TestGen generates many test types that RE has no rule for yet (slice 1 has seven). A TestGen
result whose `check_key` has no accepted rule maps to **no** annotation. It is "not governed",
and it is reported by `compare/` as `testgen_only`, never published as a free-standing finding.

## Results: TestGen fields → §8's `QualityAnnotation`

| §8 field | From the TestGen export |
|---|---|
| `qualifiedName` | §8's scheme, with TestGen's run time: `Annotation::PostgreSQL::<re_slug>::<tested_at>::Quality::<check_key>` |
| run time (report, `qualifiedName`) | `tested_at`, the TestGen test run's `test_starttime`. **Never the export, import or publish time** (owner, with Mandy, 2026-10-20: "the time that TestGen ran the analysis not when we imported from Testgen"). |
| status (`qualityDescription`, `jsonProperties.status`) | `result.result_status`: `Passed` → `pass`, `Warning` → `warning`, `Failed` → `fail`, `Log` → `logged`. `Error` → **no annotation** (§8: a check that reached no conclusion gets none). |
| `jsonProperties.measure` | `result.result_measure`, as a number |
| `jsonProperties.thresholdValues` | `result.threshold_value`, stringified as Bitol does |
| `jsonProperties.comparisonOperator` | from the test type's `test_operator`, inverted to ODCS *must-be* exactly as §7 does |
| `jsonProperties.recordCt` | the profile's `record_ct` for that table, from the same export |
| `qualityScore` | §8's 0-100 conformance from `measure` and `recordCt`, with the same row-count and statistic split |
| `jsonProperties.ruleSource` | `testgen`, so a reader can tell the two engines' evidence apart |
| `jsonProperties.engineRunId` | the TestGen `test_run_id` |
| `analysisStep` | `testgen_test_run` (RE's own is `run_quality_checks`) |
| `GovernedBy` to the rule, `AssociatedAnnotation` to the column | exactly as §8 |

A test with `result: null` (it was not in the latest complete run) maps to no annotation. A
table group whose `tests_state` is `never_run` contributes nothing. Neither is ever "passed".

## Profiles: TestGen fields → RE's value profile

TestGen's `profile_results` columns are the names RE's `database_value_profiles` uses, so a
TestGen profile row could be published by the same code as RE's profile annotations (`#750`).
The run time is the export's `profiled_at`, the TestGen profiling run's start. Sampling
differs: RE slice 1 profiles whole tables (`sample_ratio` NULL). A TestGen table group with
sampling on reports `sample_ratio`, which must carry through to the annotation's sampling
fields and must not be presented as a whole-table count.

## Open questions for the owner

1. **Should TestGen results be published at all, or only compared?** The examples here only
   compare. Publishing them means two engines' evidence on one rule.
2. **`qualityEngine` on the rule.** §7 sets `resource-explorer`. If TestGen evidence is
   published against the same rule, does the rule stay `resource-explorer`, with the engine per
   annotation in `ruleSource`? The Apache-2.0 licence grants no trademark, so naming TestGen in
   published metadata as a factual "which engine ran this" should be confirmed.
3. **A rule TestGen re-baselines.** TestGen's generation refreshes baselines unless
   `lock_refresh` is set; RE's accepted parameters win (§7). When TestGen's threshold differs
   from the rule's `thresholdValues`, should the TestGen result be published, or reported as
   "evaluated against a different threshold"? `compare/results.csv` shows both thresholds.
