"""Phase 1j J4 (D-J2): the effective key of a run, from one key with per-setting `when:` deltas. Synthetic keys only (no real key is opened)."""
import json
from pathlib import Path

import pytest

from recognizer.layout_profile import load_profile
from scoring.effective_key import KeyFormatError, effective_key, governed_rules, read_findings, shipped_defaults

PROFILES = Path(__file__).resolve().parent.parent / "profiles"
PROF = load_profile("code-repo-conventions", PROFILES)
DEF = shipped_defaults(PROF)
GOV = governed_rules(PROF)

KEY = {"repo": "synthetic", "components": ["core", {"path": "scripts", "class": "x"}, "docs"], "excluded": [{"path": "tools", "class": "tooling"}],
       "when": [{"when": {"scripts-are-tooling": False}, "components_add": ["scripts-ts"], "excluded_remove": ["tools"]},
                {"when": {"docs-min-files": 1}, "components_add": ["notes"]}]}
FINDINGS = [{"path": "scripts", "rule_id": "R-conv-scripts"}, {"path": "scripts-ts", "rule_id": "R-conv-scripts"}, {"path": "config", "rule_id": "R-conv-config-lint"},
            {"path": "core", "rule_id": "R-comp-pyproject"}, {"path": "x-test", "rule_id": "R-ts-private-package"}, {"path": "docs", "rule_id": "R-conv-docs"}]


def test_the_governed_rules_come_from_the_profile():
    assert GOV["scripts-are-tooling"] == {"R-conv-scripts", "R-tool-package"}
    assert GOV["lint-config-is-tooling"] == {"R-conv-config-lint"} and GOV["docs-min-files"] == {"R-conv-docs", "R-conv-src-docs"}
    assert GOV["private-test-packages-internal"] == {"R-ts-private-package"} and GOV["gradle-test-projects-internal"] == {"R-fx-gradle-test-project"}
    assert GOV["src-docs-is-documentation"] == {"R-conv-src-docs"} and set(GOV) == set(DEF)


# ---- default settings: the key is unchanged
@pytest.mark.parametrize("run", [{}, dict(DEF)])
def test_default_settings_leave_the_key_unchanged(run):
    e = effective_key(KEY, run, defaults=DEF, governed=GOV, findings=FINDINGS)
    assert e.key == {k: v for k, v in KEY.items() if k != "when"} and e.applied == [] and e.differing == [] and e.unscoreable == {} and e.scoreable


def test_a_key_without_when_blocks_at_default_settings_is_unchanged():
    k = {"components": ["a"], "excluded": ["b"], "assumes": {"scripts-are-tooling": True}}
    assert effective_key(k, {}, defaults=DEF).key == {"components": ["a"], "excluded": ["b"]}


# ---- a covered delta is applied
def test_a_covered_delta_is_applied():
    e = effective_key(KEY, {"scripts-are-tooling": False}, defaults=DEF, governed=GOV, findings=FINDINGS)
    assert e.applied == [0] and e.differing == ["scripts-are-tooling"] and e.scoreable
    assert e.key["components"] == ["core", {"path": "scripts", "class": "x"}, "docs", "scripts-ts"] and e.key["excluded"] == []
    assert KEY["excluded"] == [{"path": "tools", "class": "tooling"}]                 # the input key is not modified


def test_two_covered_deltas_apply_in_key_order():
    e = effective_key(KEY, {"scripts-are-tooling": False, "docs-min-files": 1}, defaults=DEF, governed=GOV, findings=FINDINGS)
    assert e.applied == [0, 1] and e.key["components"][-2:] == ["scripts-ts", "notes"] and e.scoreable


def test_a_block_needs_all_its_settings():
    k = {"components": ["a"], "when": [{"when": {"scripts-are-tooling": False, "docs-min-files": 1}, "components_add": ["b"]}]}
    e = effective_key(k, {"scripts-are-tooling": False}, defaults=DEF, governed=GOV, findings=FINDINGS)
    assert e.applied == [] and e.key["components"] == ["a"] and set(e.unscoreable) == {"scripts-are-tooling"}


def test_assumes_shifts_the_baseline():
    k = {"assumes": {"scripts-are-tooling": False}, "components": ["scripts"],
         "when": [{"when": {"scripts-are-tooling": True}, "components_remove": ["scripts"], "excluded_add": [{"path": "scripts", "class": "tooling"}]}]}
    assert effective_key(k, {"scripts-are-tooling": False}, defaults=DEF).key == {"components": ["scripts"]}
    e = effective_key(k, {}, defaults=DEF)                                             # the run uses the shipped default (true): the delta applies
    assert e.key == {"components": [], "excluded": [{"path": "scripts", "class": "tooling"}]} and e.differing == ["scripts-are-tooling"]


# ---- an uncovered setting: UNSCOREABLE, with the paths it touches in the run
def test_an_uncovered_setting_is_unscoreable_with_its_paths():
    e = effective_key(KEY, {"lint-config-is-tooling": False, "private-test-packages-internal": False}, defaults=DEF, governed=GOV, findings=FINDINGS)
    assert not e.scoreable and e.unscoreable == {"lint-config-is-tooling": ["config"], "private-test-packages-internal": ["x-test"]}
    assert e.key == {k: v for k, v in KEY.items() if k != "when"}                      # nothing applied


def test_covered_and_uncovered_together():
    e = effective_key(KEY, {"scripts-are-tooling": False, "docs-min-files": 3}, defaults=DEF, governed=GOV, findings=FINDINGS)
    assert e.applied == [0] and e.unscoreable == {"docs-min-files": ["docs"]}


def test_an_uncovered_setting_without_findings_has_no_paths_but_is_still_unscoreable():
    e = effective_key(KEY, {"src-docs-is-documentation": False}, defaults=DEF)
    assert e.unscoreable == {"src-docs-is-documentation": []} and not e.scoreable


def test_findings_can_be_read_from_a_run(tmp_path):
    (tmp_path / "findings.jsonl").write_text("".join(json.dumps(f) + "\n" for f in FINDINGS))
    e = effective_key(KEY, {"lint-config-is-tooling": False}, defaults=DEF, governed=GOV, findings=read_findings(tmp_path / "findings.jsonl"))
    assert e.unscoreable == {"lint-config-is-tooling": ["config"]}


# ---- key validation
@pytest.mark.parametrize("key", [
    {"assumes": {"nope": True}},
    {"assumes": {"docs-min-files": True}},
    {"assumes": ["scripts-are-tooling"]},
    {"when": {"when": {"scripts-are-tooling": False}}},
    {"when": [{"components_add": ["a"]}]},
    {"when": [{"when": {}, "components_add": ["a"]}]},
    {"when": [{"when": {"nope": False}, "components_add": ["a"]}]},
    {"when": [{"when": {"scripts-are-tooling": "no"}, "components_add": ["a"]}]},
    {"when": [{"when": {"scripts-are-tooling": True}, "components_add": ["a"]}]},          # the assumed value: it would change the default key
    {"when": [{"when": {"scripts-are-tooling": False}, "components_add": []}]},
    {"when": [{"when": {"scripts-are-tooling": False}, "labels_add": ["a"]}]},
    [],
])
def test_a_bad_key_is_rejected(key):
    with pytest.raises(KeyFormatError):
        effective_key(key, {"scripts-are-tooling": False}, defaults=DEF)


@pytest.mark.parametrize("block", [{"components_remove": ["zz"]}, {"components_add": ["core"]}, {"excluded_remove": ["zz"]}, {"components_add": [{"class": "x"}]}])
def test_a_delta_that_does_not_fit_the_key_is_rejected(block):
    with pytest.raises(KeyFormatError):
        effective_key({**KEY, "when": [{"when": {"scripts-are-tooling": False}, **block}]}, {"scripts-are-tooling": False}, defaults=DEF)


def test_an_unknown_run_setting_is_rejected():
    with pytest.raises(KeyFormatError):
        effective_key(KEY, {"nope": 1}, defaults=DEF)


def test_the_library_opens_no_key_file():
    src = (Path(__file__).resolve().parent.parent / "scoring" / "effective_key.py").read_text()
    assert "layout-corpus" not in src and "open(" in src and src.count("open(") == 1       # only read_findings opens a file: a run's findings
