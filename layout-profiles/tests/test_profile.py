"""Profile model v0: what the loader accepts and what it must reject. Synthetic documents only."""
import copy
from pathlib import Path

import pytest
import yaml

from recognizer.layout_profile import ProfileError, load_profile, parse_profile

PROFILES = Path(__file__).resolve().parent.parent / "profiles"

BASE = yaml.safe_load("""
profile_id: t
version: 0.1.0
status: proposed
applies_to: any
roles: [component, vendored, example]
relevance: {primary: [component], supporting: [example], hidden: [vendored]}
rules:
  - id: R-a
    match: {path_segment: node_modules}
    assign: {role: vendored}
    grain: subtree
    basis: convention
    confidence: high
    evidence: "installed packages"
""")


def doc(**changes):
    d = copy.deepcopy(BASE)
    for k, v in changes.items():
        d[k] = v
    return d


def rule(**changes):
    r = copy.deepcopy(BASE["rules"][0])
    r.update(changes)
    return r


def test_the_shipped_generic_profile_loads_and_is_ordered():
    p = load_profile("generic-relevance", PROFILES)
    ids = [r.id for r in p.rules]
    assert ids[0] == "R-vcs-git" and "R-copy-worktree-name" not in ids      # .git first; the worktree name pattern moved out in 0.2.0
    assert len(set(ids)) == len(ids)
    assert p.status == "proposed" and p.version == "0.5.0"
    assert all(r.evidence and r.basis and r.confidence for r in p.rules)


def test_the_workspace_profile_composes_generic_first_and_the_worktree_name_rule_last():
    p = load_profile("egeria-workspace", PROFILES)
    ids = [r.id for r in p.rules]
    assert ids[0] == "R-vcs-git" and ids[-1] == "R-run-volume-data" and len(ids) == 24
    assert [pid for pid, _ in p.composed_of] == ["egeria-workspace", "generic-relevance", "worktree-copies", "workspace-runtime-data"]
    assert p.applies_to == "workspace-of-repos"


def test_every_shipped_profile_loads():
    for name in ("generic-relevance", "worktree-copies", "egeria-workspace", "code-repo"):
        assert load_profile(name, PROFILES).rules is not None


def test_a_valid_minimal_profile_loads():
    assert parse_profile(BASE).rules[0].relevance == "hidden"               # relevance comes from the role map


@pytest.mark.parametrize("bad", [
    doc(surprise=1),                                                         # unknown top-level key
    doc(version="1.0"), doc(version=1.0), doc(status="draft"), doc(applies_to="everything"),
    doc(roles=["component", "wizard"]),                                      # unknown role
    doc(relevance={"primary": ["component"], "loud": ["example"], "hidden": []}),   # unknown relevance level
    doc(relevance={"primary": ["component"], "hidden": ["vendored", "component"]}),  # a role under two levels
    doc(relevance={"primary": ["component"], "hidden": ["ghost"]}),         # a role the profile does not declare
    doc(profile_id="Not A Slug"),
])
def test_document_level_errors(bad):
    with pytest.raises(ProfileError):
        parse_profile(bad)


@pytest.mark.parametrize("changes", [
    {"surprise": 1},                                                         # unknown rule key
    {"match": {"path_segment": "x", "colour": "red"}},                       # unknown match key
    {"match": {}},                                                           # a rule that matches nothing
    {"assign": {"role": "vendored", "mood": "x"}},                           # unknown assign key
    {"assign": {"role": "wizard"}},                                          # unknown role
    {"assign": {"role": "vendored", "relevance": "loud"}},                   # unknown relevance
    {"assign": {"role": "example", "relevance": "loud"}},
    {"grain": "forest"}, {"basis": "vibes"}, {"confidence": "certain"},
    {"evidence": ""}, {"evidence": "   "},                                   # a claim without evidence
    {"id": "has space"},
    {"match": {"extension": ".log"}, "grain": "subtree"},                    # a subtree needs somewhere to start
    {"match": {"extension": ".log"}, "grain": "component"},                  # a component is a directory claim
    {"match": {"has_file": "x"}, "assign": {"role": "vendored"}, "grain": "component"},   # a component must assign role component
    {"match": {"has_file": "x", "extension": ".log"}, "grain": "dir"},       # a directory test plus a file-name test
    {"match": {"name_regex": "("}, "grain": "dir"},                          # a regex that does not compile
])
def test_rule_level_errors(changes):
    d = doc(rules=[rule(**changes)])
    with pytest.raises(ProfileError):
        parse_profile(d)


def test_missing_rule_fields_are_errors():
    for missing in ("id", "match", "assign", "grain", "basis", "confidence", "evidence"):
        r = rule()
        del r[missing]
        with pytest.raises(ProfileError):
            parse_profile(doc(rules=[r]))


def test_a_role_without_a_relevance_is_an_error():
    d = doc(roles=["component", "vendored", "example", "docs"], rules=[rule(assign={"role": "docs"})])
    with pytest.raises(ProfileError):
        parse_profile(d)
    parse_profile(doc(roles=["component", "vendored", "example", "docs"], rules=[rule(assign={"role": "docs", "relevance": "supporting"})]))


def test_duplicate_rule_ids_are_an_error():
    with pytest.raises(ProfileError):
        parse_profile(doc(rules=[rule(), rule(match={"path_segment": "dist"})]))


def write(tmp_path, name, d):
    (tmp_path / f"{name}.yaml").write_text(yaml.safe_dump(d))


def test_extends_checks_the_child_first_then_the_listed_order(tmp_path):
    write(tmp_path, "base-a", doc(profile_id="base-a", rules=[rule(id="A-1")]))
    write(tmp_path, "base-b", doc(profile_id="base-b", rules=[rule(id="B-1", match={"path_segment": "dist"})]))
    write(tmp_path, "child", doc(profile_id="child", extends=["base-a", "base-b"], rules=[rule(id="C-1", match={"path_segment": "x"})]))
    p = load_profile("child", tmp_path)
    assert [r.id for r in p.rules] == ["C-1", "A-1", "B-1"]
    assert [pid for pid, _ in p.composed_of] == ["child", "base-a", "base-b"]


def test_extends_errors(tmp_path):
    write(tmp_path, "one", doc(profile_id="one", extends=["two"]))
    write(tmp_path, "two", doc(profile_id="two", extends=["one"]))
    with pytest.raises(ProfileError):
        load_profile("one", tmp_path)                                         # a cycle
    write(tmp_path, "lonely", doc(profile_id="lonely", extends=["nobody"]))
    with pytest.raises(ProfileError):
        load_profile("lonely", tmp_path)                                      # an unknown base
    write(tmp_path, "dup-a", doc(profile_id="dup-a"))
    write(tmp_path, "dup-b", doc(profile_id="dup-b", extends=["dup-a"]))      # both define R-a
    with pytest.raises(ProfileError):
        load_profile("dup-b", tmp_path)


def test_a_file_name_that_disagrees_with_the_profile_id_is_an_error(tmp_path):
    write(tmp_path, "other-name", doc(profile_id="real-name"))
    with pytest.raises(ProfileError):
        load_profile("other-name", tmp_path)


def test_invalid_yaml_is_a_profile_error(tmp_path):
    (tmp_path / "broken.yaml").write_text("a: [unclosed")
    with pytest.raises(ProfileError):
        load_profile("broken", tmp_path)


def test_grammar_blocks_are_schema_only_but_checked():
    ok = doc(path_grammar=[{"id": "PG-packages", "pattern": "packages/{name}", "yields": "component"}], name_grammar=[])
    assert parse_profile(ok).path_grammar[0]["id"] == "PG-packages"
    with pytest.raises(ProfileError):
        parse_profile(doc(path_grammar=[{"id": "PG-x", "pattern": "p", "yields": "component", "extra": 1}]))
