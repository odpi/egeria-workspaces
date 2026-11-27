"""Phase 1j J5: the configuration a survey ran with is recorded (classes.json and report.md), the sample user overlay, and a drift comparison that reports a
CONFIGURATION CHANGE instead of finding drift. Synthetic trees only."""
import copy
import json
from pathlib import Path

import pytest
import yaml

from recognizer import config_drift as cd
from recognizer import configuration as cfg
from recognizer.layout_profile import compose_profiles, load_profile, parse_profile
from recognizer.recognize import Recognizer, main

PROFILES = Path(__file__).resolve().parent.parent / "profiles"
SAMPLE = PROFILES / "samples" / "user-preferences-example.yaml"
TREE = {"pyproject.toml": "[project]\nname='r'\n", "scripts/package.json": '{"name": "s"}', "scripts/run.sh": "x", "config/checkstyle.xml": "x",
        "docs/a.md": "x", "core/pyproject.toml": "[project]\nname='c'\n"}


def tree(tmp_path, files=TREE):
    lst = tmp_path / "tree.tsv"
    lst.write_text("".join(f"{k}\t{len(v)}\n" for k, v in sorted(files.items())))
    return lst


def survey(tmp_path, out, profile="code-repo-conventions"):
    lst = tree(tmp_path)
    assert main([str(lst), "--out", str(tmp_path / out), "--profile", str(profile)]) == 0
    c = json.loads((tmp_path / out / "classes.json").read_text())
    return c, (tmp_path / out / "report.md").read_text(), (tmp_path / out / "components-all.txt").read_text().split()


# ---- the record at the defaults
def test_a_default_run_records_its_configuration(tmp_path):
    c, rep, comps = survey(tmp_path, "o")
    conf = c["configuration"]
    assert [(x["profile_id"], x["shipped"]) for x in conf["chain"]] == [("code-repo-conventions", True), ("code-repo", True), ("generic-relevance", True)]
    assert conf["chain"][0]["version"] == "0.11.0" and conf["default_configuration"] is True and conf["overlays"] == []
    assert all(s["is_default"] for s in conf["settings"].values()) and len(conf["settings"]) == 6 and conf["non_default_settings"] == [] and conf["settings_set"] == []
    assert conf["disabled_rules"] == conf["replaced_rules"] == conf["overridden_lists"] == []
    assert conf["config_sha256"] == cfg.config_sha256(load_profile("code-repo-conventions", PROFILES))
    assert "## Configuration" in rep and "Default configuration (Dan's rulings)" in rep and "NON-DEFAULT" not in rep and conf["config_sha256"] in rep
    assert "Disabled rules: none." in rep and "Replaced rules: none." in rep and "Overridden lists: none." in rep


def test_the_record_is_the_same_in_two_runs(tmp_path):
    a, ra, _ = survey(tmp_path, "a")
    b, rb, _ = survey(tmp_path, "b")
    assert a == b and ra == rb


def test_a_profile_without_settings_records_its_chain(tmp_path):
    c, rep, _ = survey(tmp_path, "o", "docs-site")
    assert c["configuration"]["settings"] == {} and c["configuration"]["default_configuration"] is True and "| setting |" not in rep


def test_a_composition_records_every_part(tmp_path):
    c, _, _ = survey(tmp_path, "o", "code-repo-conventions,docs-site")
    ch = [(x["profile_id"], x["shipped"]) for x in c["configuration"]["chain"]]
    assert ch[0] == ("code-repo-conventions+docs-site", None) and ("docs-site", True) in ch and ("generic-relevance", True) in ch


# ---- the sample overlay
def test_the_sample_is_an_overlay_with_three_non_default_settings():
    p = load_profile(str(SAMPLE))
    assert p.shipped is False and p.has_overlay is True and p.settings_set == ("scripts-are-tooling", "lint-config-is-tooling", "docs-min-files")
    assert {k: p.settings[k] for k in p.settings_set} == {"scripts-are-tooling": False, "lint-config-is-tooling": False, "docs-min-files": 1}
    assert p.manifest_reading.readers == load_profile("code-repo-conventions", PROFILES).manifest_reading.readers


def test_the_sample_runs_and_its_report_shows_the_non_default_settings(tmp_path):
    c, rep, comps = survey(tmp_path, "o", SAMPLE)
    conf = c["configuration"]
    assert conf["default_configuration"] is False and conf["overlays"] == ["user-preferences-example"]
    assert conf["non_default_settings"] == ["docs-min-files", "lint-config-is-tooling", "scripts-are-tooling"]
    assert "**NON-DEFAULT CONFIGURATION.** Only the default configuration is held-out-confirmed" in rep and "(OVERLAY)" in rep
    assert "| scripts-are-tooling | false **(set)** | true |" in rep and "| docs-min-files | 1 **(set)** | 2 |" in rep
    assert {"scripts", "config", "docs", "core"} <= set(comps)                       # scripts and config are components; one docs file makes docs one
    _, _, dcomps = survey(tmp_path, "d")
    assert not {"scripts", "config", "docs"} & set(dcomps)


# ---- drift across a settings change: CONFIGURATION CHANGED, not finding drift
def test_drift_across_a_settings_change_reports_a_configuration_change(tmp_path):
    survey(tmp_path, "old")
    survey(tmp_path, "new", SAMPLE)
    d = cd.compare(tmp_path / "old", tmp_path / "new")
    assert d["status"] == "CONFIGURATION CHANGED" and "counts" not in d and "new" not in d
    assert d["settings"] == {"docs-min-files": {"old": 2, "new": 1}, "lint-config-is-tooling": {"old": True, "new": False},
                             "scripts-are-tooling": {"old": True, "new": False}}
    assert d["overlays"] == {"old": [], "new": ["user-preferences-example"]}
    assert cd.headline(d).startswith("CONFIGURATION CHANGED (not finding drift): docs-min-files 2 -> 1")


def test_drift_with_the_same_configuration_compares_findings(tmp_path):
    survey(tmp_path, "a")
    survey(tmp_path, "b")
    d = cd.compare(tmp_path / "a", tmp_path / "b")
    assert d["status"] == "SAME CONFIGURATION" and d["counts"]["new"] == d["counts"]["resolved"] == 0 and d["counts"]["unchanged"] > 0


def test_a_survey_without_a_configuration_record_is_unrecorded(tmp_path):
    survey(tmp_path, "a")
    survey(tmp_path, "b")
    c = json.loads((tmp_path / "a" / "classes.json").read_text())
    c.pop("configuration")
    (tmp_path / "a" / "classes.json").write_text(json.dumps(c))
    d = cd.compare(tmp_path / "a", tmp_path / "b")
    assert d["status"] == "CONFIGURATION UNRECORDED" and "UNRECORDED" in cd.headline(d)


def test_the_drift_cli(tmp_path, capsys):
    survey(tmp_path, "old")
    survey(tmp_path, "new", SAMPLE)
    capsys.readouterr()
    assert cd.main([str(tmp_path / "old"), str(tmp_path / "new")]) == 0
    assert capsys.readouterr().out.startswith("CONFIGURATION CHANGED")


# ---- every replaced, disabled and overridden id is listed (an accidental same-id rule is visible)
def test_disabled_replaced_and_overridden_are_listed(tmp_path):
    raw = yaml.safe_load((PROFILES / "code-repo-conventions.yaml").read_text())
    scripts = next(r for r in raw["rules"] if r["id"] == "R-conv-scripts")
    (tmp_path / "mine.yaml").write_text(yaml.safe_dump({
        "profile_id": "mine", "version": "0.1.0", "status": "proposed", "applies_to": "code-repo", "extends": ["code-repo-conventions"],
        "roles": ["component", "tooling"], "relevance": {"primary": ["component"], "supporting": ["tooling"], "hidden": []},
        "disable": ["R-conv-requirements"], "lists": {"test-folder-names": {"add": ["qa"]}}, "settings": {"gradle-test-projects-internal": False},
        "rules": [{**scripts, "match": {"path_glob": "*", "segment_regex": ["(?i)^scripts$"]}}]}))
    c, rep, _ = survey(tmp_path, "o", tmp_path / "mine.yaml")
    conf = c["configuration"]
    assert conf["disabled_rules"] == ["R-conv-requirements"] and conf["replaced_rules"] == ["R-conv-scripts"] and conf["overridden_lists"] == ["test-folder-names"]
    assert conf["settings_set"] == ["gradle-test-projects-internal"] and conf["default_configuration"] is False
    for line in ("Disabled rules: R-conv-requirements.", "Replaced rules: R-conv-scripts.", "Overridden lists: test-folder-names.",
                 "Settings set by a profile: gradle-test-projects-internal.", "Overlay profiles: mine."):
        assert line in rep


# ---- config_sha256
def test_config_sha256_moves_with_the_configuration_and_not_with_documentation():
    base = load_profile("code-repo-conventions", PROFILES)
    doc = yaml.safe_load((PROFILES / "code-repo-conventions.yaml").read_text())
    same = parse_profile(copy.deepcopy(doc), "x", PROFILES, _shipped=True)
    assert cfg.config_sha256(same) == cfg.config_sha256(base)
    d2 = copy.deepcopy(doc)
    d2["rules"][0]["evidence"] = "other words"
    d2["rules"][0]["tuned_on"] = ["elsewhere"]
    d2["settings"]["docs-min-files"]["doc"] = "other words"
    assert cfg.config_sha256(parse_profile(d2, "x", PROFILES, _shipped=True)) == cfg.config_sha256(base)       # documentation is not configuration
    d3 = copy.deepcopy(doc)
    d3["settings"]["docs-min-files"]["default"] = 3
    assert cfg.config_sha256(parse_profile(d3, "x", PROFILES, _shipped=True)) != cfg.config_sha256(base)
    assert cfg.config_sha256(load_profile(str(SAMPLE))) != cfg.config_sha256(base)
    assert cfg.config_sha256(compose_profiles("code-repo-conventions,docs-site", PROFILES)) != cfg.config_sha256(base)


def test_the_recognizer_writes_the_profile_it_was_given(tmp_path):
    p = load_profile(str(SAMPLE))
    lst = tree(tmp_path)
    c = Recognizer(p).run(lst, tmp_path / "o")
    assert c["configuration"]["config_sha256"] == cfg.config_sha256(p)
