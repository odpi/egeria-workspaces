"""Phase 1j J0: named lists (`lists:`), referred to as `$name` (a whole value or a list element) or `{$name}` inside a regex; inherited through `extends`.
A refactor: the shipped profiles' behaviour does not change. Synthetic profiles only."""
import re
from pathlib import Path

import pytest
import yaml

from recognizer.layout_profile import ProfileError, compose_profiles, load_profile

PROFILES = Path(__file__).resolve().parent.parent / "profiles"
BASE = {"profile_id": "b", "version": "0.1.0", "status": "proposed", "applies_to": "any", "roles": ["component", "tooling"],
        "relevance": {"primary": ["component"], "supporting": ["tooling"], "hidden": []}}


def rule(match, rid="R", role="component", grain="component"):
    return {"id": rid, "match": match, "assign": {"role": role}, "grain": grain, "basis": "convention", "confidence": "low", "evidence": "x"}


def write(tmp_path, name, doc=None, text=None):
    (tmp_path / f"{name}.yaml").write_text(text if text is not None else yaml.safe_dump(doc, sort_keys=False))


def prof(tmp_path, name="b", **doc):
    write(tmp_path, name, {**BASE, "profile_id": name, **doc})
    return load_profile(name, tmp_path)


# ---- references
def test_a_whole_value_reference_becomes_the_list(tmp_path):
    p = prof(tmp_path, lists={"mf": ["a.toml", "b.json"]}, rules=[rule({"has_file": "$mf"})])
    assert p.rules[0].has_files == frozenset({"a.toml", "b.json"}) and p.rules[0].match["has_file"] == ["a.toml", "b.json"]


def test_a_reference_as_a_list_element_is_spliced_in_place(tmp_path):
    p = prof(tmp_path, lists={"mf": ["a.toml", "b.json"]}, rules=[rule({"has_file": ["x.cfg", "$mf", "y.ini"]})])
    assert p.rules[0].match["has_file"] == ["x.cfg", "a.toml", "b.json", "y.ini"]


def test_a_reference_inside_a_regex_becomes_an_escaped_alternation(tmp_path):
    p = prof(tmp_path, lists={"names": ["test", "end-to-end", "a.b"]}, rules=[rule({"name_regex": ["(?i)^(?:{$names})$"]})])
    (rx,) = p.rules[0].name_res
    assert rx.pattern == "(?i)^(?:test|end\\-to\\-end|a\\.b)$"
    assert rx.search("END-TO-END") and rx.search("a.b") and not rx.search("aXb") and not rx.search("end")


def test_a_nested_mapping_value_can_refer_to_a_list(tmp_path):
    p = prof(tmp_path, lists={"f": ["mkdocs.yml"], "e": [".md", ".rst"]},
             rules=[rule({"path_glob": "docs", "min_content": {"files": "$f", "min_files": 2, "extensions": "$e"}})])
    assert p.rules[0].content_files == frozenset({"mkdocs.yml"}) and p.rules[0].content_exts == (".md", ".rst")


def test_a_file_role_rule_can_refer_to_a_list(tmp_path):
    p = prof(tmp_path, lists={"ex": [".py", ".sh"]}, rules=[], file_roles=[rule({"extension": "$ex"}, rid="F", grain="dir")])
    assert p.file_roles[0].extensions == (".py", ".sh")


def test_lists_are_inherited_through_extends(tmp_path):
    write(tmp_path, "base", {**BASE, "profile_id": "base", "lists": {"mf": ["a.toml"]}, "rules": [rule({"has_file": "$mf"}, rid="RB")]})
    p = prof(tmp_path, name="child", extends=["base"], rules=[rule({"has_file": "$mf"}, rid="RC")])
    assert p.lists == {"mf": ("a.toml",)} and {r.id: r.has_files for r in p.rules} == {"RC": frozenset({"a.toml"}), "RB": frozenset({"a.toml"})}


def test_a_diamond_sees_one_list(tmp_path):
    write(tmp_path, "root", {**BASE, "profile_id": "root", "lists": {"mf": ["a.toml"]}, "rules": [rule({"has_file": "$mf"}, rid="R0")]})
    write(tmp_path, "l", {**BASE, "profile_id": "l", "extends": ["root"], "rules": [rule({"has_file": "$mf"}, rid="RL")]})
    write(tmp_path, "r", {**BASE, "profile_id": "r", "extends": ["root"], "rules": [rule({"has_file": "$mf"}, rid="RR")]})
    p = prof(tmp_path, name="top", extends=["l", "r"], rules=[rule({"has_file": "$mf"}, rid="RT")])
    assert p.lists == {"mf": ("a.toml",)}


# ---- rejections
def test_an_unknown_reference_is_rejected(tmp_path):
    with pytest.raises(ProfileError, match=r"unknown list \$nope"):
        prof(tmp_path, lists={"mf": ["a.toml"]}, rules=[rule({"has_file": "$nope"})])
    with pytest.raises(ProfileError, match=r"unknown list \$nope"):
        prof(tmp_path, lists={"mf": ["a.toml"]}, rules=[rule({"name_regex": "^(?:{$nope})$"})])
    with pytest.raises(ProfileError, match=r"unknown list \$nope"):
        prof(tmp_path, rules=[rule({"has_file": ["x", "$nope"]})])


@pytest.mark.parametrize("lists", [{"mf": []}, {"mf": "a.toml"}, {"mf": [""]}, {"mf": [1]}, {"mf": ["a", "a"]}, {"Bad_Name": ["a"]}, {}, ["a"]])
def test_a_bad_list_is_rejected(tmp_path, lists):
    with pytest.raises(ProfileError):
        prof(tmp_path, lists=lists, rules=[rule({"has_file": "x"})])


def test_a_list_name_defined_twice_in_one_profile_is_rejected(tmp_path):
    text = yaml.safe_dump({**BASE, "rules": [rule({"has_file": "$mf"})]}, sort_keys=False) + "lists:\n  mf: [a.toml]\n  mf: [b.json]\n"
    write(tmp_path, "b", text=text)
    with pytest.raises(ProfileError, match="defined twice"):
        load_profile("b", tmp_path)


def test_a_child_may_not_redefine_an_inherited_list(tmp_path):
    write(tmp_path, "base", {**BASE, "profile_id": "base", "lists": {"mf": ["a.toml"]}, "rules": [rule({"has_file": "$mf"}, rid="RB")]})
    with pytest.raises(ProfileError, match="already defined by an extended profile"):
        prof(tmp_path, name="child", extends=["base"], lists={"mf": ["b.json"]}, rules=[])


def test_two_extended_profiles_with_different_items_under_one_name_are_rejected(tmp_path):
    write(tmp_path, "x1", {**BASE, "profile_id": "x1", "lists": {"mf": ["a.toml"]}, "rules": [rule({"has_file": "$mf"}, rid="R1")]})
    write(tmp_path, "x2", {**BASE, "profile_id": "x2", "lists": {"mf": ["b.json"]}, "rules": [rule({"has_file": "$mf"}, rid="R2")]})
    with pytest.raises(ProfileError, match="two extended profiles"):
        prof(tmp_path, name="top", extends=["x1", "x2"], rules=[])


def test_a_dollar_inside_an_ordinary_regex_is_not_a_reference(tmp_path):
    p = prof(tmp_path, rules=[rule({"name_regex": ["^main$", "Main$", "x{1,2}$"]})])
    assert [r.pattern for r in p.rules[0].name_res] == ["^main$", "Main$", "x{1,2}$"]


# ---- the shipped profile: the named lists and who uses them
def test_the_shipped_lists_are_the_closed_lists_of_the_rules():
    p = load_profile("code-repo-conventions", PROFILES)
    by = {r.id: r for r in p.rules}
    L = p.lists
    assert set(L) >= {"test-folder-names", "manifest-files", "lint-config-dirs", "lint-config-names", "app-folders", "test-words", "gradle-build-files",
                      "docs-site-files", "docs-extensions"}
    tests_rx, fx_rx = by["R-conv-tests"].name_res[0], by["R-fx-test-project"].segment_res[0]
    for n in L["test-folder-names"]:                     # one list, two rules: they cannot drift
        assert tests_rx.search(n) and fx_rx.search(n)
    for n in L["fixture-folder-names"]:
        assert fx_rx.search(n) and not tests_rx.search(n)
    for rid in ("R-fx-test-project", "R-fx-sample-project", "R-fx-benchmark-project", "R-tool-package", "R-fx-test-group-project"):
        assert by[rid].has_files == frozenset(L["manifest-files"])
    assert by["R-conv-test-group"].group_files == by["R-fx-test-group-project"].group_files == frozenset(L["manifest-files"])
    assert by["R-conv-config-lint"].only_dirs == frozenset(L["lint-config-dirs"]) and len(by["R-conv-config-lint"].only_res) == len(L["lint-config-names"])
    assert by["R-ts-private-package"].not_segments == frozenset(L["app-folders"])
    assert by["R-ts-private-package"].name_words == by["R-fx-gradle-test-project"].tp_words == frozenset(L["test-words"])
    assert by["R-fx-gradle-test-project"].tp_other_than == frozenset(L["gradle-build-files"])
    for rid in ("R-conv-docs", "R-conv-src-docs"):
        assert by[rid].content_files == frozenset(L["docs-site-files"]) and by[rid].content_exts == L["docs-extensions"]


def test_the_composite_profile_sees_the_lists():
    p = compose_profiles("code-repo-conventions,docs-site", PROFILES)
    assert "test-folder-names" in p.lists


def test_the_profile_versions_are_unchanged_by_j0():
    assert load_profile("code-repo-conventions", PROFILES).version == "0.10.0" and load_profile("code-repo", PROFILES).version == "0.5.0"
    assert load_profile("docs-site", PROFILES).version == "0.5.0"


def test_no_inline_copy_of_a_named_list_is_left_in_the_rules():
    doc = yaml.safe_load((PROFILES / "code-repo-conventions.yaml").read_text())
    lists = [tuple(v) for v in doc["lists"].values()]

    def walk(v):
        if isinstance(v, dict):
            for x in v.values():
                yield from walk(x)
        elif isinstance(v, list):
            yield v
            for x in v:
                yield from walk(x)
    for r in doc["rules"]:
        for seq in walk(r["match"]):
            assert tuple(seq) not in lists, (r["id"], seq)                 # a closed list that has a name is referred to by $name
    text = yaml.safe_dump([r["match"] for r in doc["rules"]])
    assert "testbed|testbeds" not in text and "testfixtures|fixture" not in text


# ======================================================================== J1 ========================================================================================
import json                                                                       # noqa: E402
from types import SimpleNamespace                                                 # noqa: E402

from recognizer import manifests as mf                                            # noqa: E402
from recognizer.recognize import Recognizer                                       # noqa: E402


def three(tmp_path):
    write(tmp_path, "base", {**BASE, "profile_id": "base", "rules": [rule({"has_file": "a"}, rid="A"), rule({"has_file": "b"}, rid="B"),
                                                                     rule({"has_file": "c"}, rid="C")],
                             "file_roles": [rule({"extension": ".x"}, rid="FX", grain="dir"), rule({"extension": ".y"}, rid="FY", grain="dir")]})


# ---- disable
def test_disable_removes_an_inherited_rule_and_a_file_role_rule(tmp_path):
    three(tmp_path)
    p = prof(tmp_path, name="child", extends=["base"], disable=["B", "FY"], rules=[])
    assert [r.id for r in p.rules] == ["A", "C"] and [r.id for r in p.file_roles] == ["FX"]
    assert p.disabled == ("B", "FY") and p.replaced == () and p.effective_order == ("A", "C", "FX")


@pytest.mark.parametrize("disable", [["Z"], ["B", "Z"], [], "B", ["B", "B"], [""]])
def test_a_bad_or_unknown_disable_is_rejected(tmp_path, disable):
    three(tmp_path)
    with pytest.raises(ProfileError):
        prof(tmp_path, name="child", extends=["base"], disable=disable, rules=[])


def test_a_profile_cannot_disable_its_own_rule(tmp_path):
    with pytest.raises(ProfileError, match="not a rule of an extended profile"):
        prof(tmp_path, disable=["R"], rules=[rule({"has_file": "a"})])


def test_disable_and_replace_of_one_id_is_rejected(tmp_path):
    three(tmp_path)
    with pytest.raises(ProfileError, match="both disabled and redefined"):
        prof(tmp_path, name="child", extends=["base"], disable=["B"], rules=[rule({"has_file": "b2"}, rid="B")])


# ---- replace in place
def test_a_child_rule_with_an_inherited_id_replaces_it_at_the_inherited_position(tmp_path):
    three(tmp_path)
    p = prof(tmp_path, name="child", extends=["base"], rules=[rule({"has_file": "n"}, rid="N"), rule({"has_file": "b2"}, rid="B")])
    assert [r.id for r in p.rules] == ["N", "A", "B", "C"]                      # the child's new rule first; B where B was
    b = {r.id: r for r in p.rules}["B"]
    assert b.origin == "child" and b.has_files == frozenset({"b2"}) and p.replaced == ("B",)
    assert p.effective_order == ("N", "A", "B", "C", "FX", "FY")


def test_a_file_role_rule_is_replaced_in_place_too(tmp_path):
    three(tmp_path)
    p = prof(tmp_path, name="child", extends=["base"], rules=[], file_roles=[rule({"extension": ".x2"}, rid="FX", grain="dir")])
    assert [r.id for r in p.file_roles] == ["FX", "FY"] and p.file_roles[0].extensions == (".x2",) and p.replaced == ("FX",)


@pytest.mark.parametrize("doc", [{"rules": [rule({"has_file": "z"}, rid="FX")]}, {"rules": [], "file_roles": [rule({"extension": ".z"}, rid="A", grain="dir")]}])
def test_a_replacement_in_the_other_layer_is_rejected(tmp_path, doc):
    three(tmp_path)
    with pytest.raises(ProfileError, match="same layer"):
        prof(tmp_path, name="child", extends=["base"], **doc)


def test_the_same_id_from_two_different_extended_profiles_is_still_an_error(tmp_path):
    three(tmp_path)
    write(tmp_path, "base2", {**BASE, "profile_id": "base2", "rules": [rule({"has_file": "a2"}, rid="A")]})
    with pytest.raises(ProfileError, match="used twice"):
        prof(tmp_path, name="child", extends=["base", "base2"], rules=[])


def test_disabled_and_replaced_ids_carry_through_a_further_extends(tmp_path):
    three(tmp_path)
    write(tmp_path, "mid", {**BASE, "profile_id": "mid", "extends": ["base"], "disable": ["A"], "rules": [rule({"has_file": "c2"}, rid="C")]})
    p = prof(tmp_path, name="top", extends=["mid"], rules=[rule({"has_file": "b3"}, rid="B")])
    assert [r.id for r in p.rules] == ["B", "C"] and p.disabled == ("A",) and set(p.replaced) == {"B", "C"}
    assert {r.id: r.origin for r in p.rules} == {"B": "top", "C": "mid"}


def test_the_shipped_profiles_disable_and_replace_nothing():
    for pid in ("code-repo-conventions", "code-repo", "docs-site", "generic-relevance", "workspace-repo"):
        p = load_profile(pid, PROFILES)
        assert p.disabled == () and p.replaced == () and p.effective_order == tuple(r.id for r in p.rules) + tuple(r.id for r in p.file_roles)
    c = compose_profiles("code-repo-conventions,docs-site", PROFILES)
    assert c.disabled == () and c.replaced == ()


# ---- disabling a rule another part depends on: it loads, and behaves as documented
def overlay(tmp_path, name, **doc):
    import shutil
    for f in PROFILES.glob("*.yaml"):
        shutil.copy(f, tmp_path / f.name)
    write(tmp_path, name, {"profile_id": name, "version": "0.1.0", "status": "proposed", "applies_to": "code-repo", "roles": ["component"],
                           "relevance": {"primary": ["component"], "supporting": [], "hidden": []}, "rules": [], **doc})
    return load_profile(name, tmp_path)


def run(tmp_path, p, files):
    root = tmp_path / "tree"
    for rel, content in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(content)
    lst = tmp_path / "tree.tsv"
    lst.write_text("".join(f"{k}\t{len(v)}\n" for k, v in sorted(files.items())))
    rec = Recognizer(p, blob_source=mf.FileSource(str(root)))
    rec.run(lst, tmp_path / "out")
    f = {x["path"]: x for x in map(json.loads, (tmp_path / "out" / "findings.jsonl").read_text().splitlines()) if not x["rule_id"].startswith("F-")}
    return SimpleNamespace(f=f, allc=(tmp_path / "out" / "components-all.txt").read_text().split())


SCRIPTS_TS = {"pyproject.toml": "[project]\nname='r'\n", "scripts-ts/package.json": '{"name": "x"}', "scripts-ts/src/x.ts": "x"}


def test_disabling_only_the_scripts_rule_keeps_a_scripts_package_tooling(tmp_path):
    # R-tool-package still claims scripts-ts (a manifest under a scripts- segment), so the parent_not_role of R-conv-node-src still holds
    p = overlay(tmp_path, "mine", extends=["code-repo-conventions"], disable=["R-conv-scripts"])
    r = run(tmp_path, p, SCRIPTS_TS)
    assert r.f["scripts-ts"]["rule_id"] == "R-tool-package" and "scripts-ts/src" not in r.allc


def test_disabling_both_tooling_rules_makes_the_package_and_its_src_components(tmp_path):
    # the parent_not_role target is a ROLE: with no tooling claim on scripts-ts, R-conv-node-src claims scripts-ts/src as documented
    p = overlay(tmp_path, "mine", extends=["code-repo-conventions"], disable=["R-conv-scripts", "R-tool-package"])
    r = run(tmp_path, p, SCRIPTS_TS)
    assert "scripts-ts" in r.allc and r.f["scripts-ts"]["rule_id"] == "R-comp-package-json"
    assert "scripts-ts/src" in r.allc and r.f["scripts-ts/src"]["rule_id"] == "R-conv-node-src"


def test_disabling_a_rule_that_manifest_reading_names_switches_that_feature_off(tmp_path):
    p = overlay(tmp_path, "mine", extends=["docs-site"], disable=["R-docs-site-docusaurus", "R-docs-site-output"])
    assert p.manifest_reading.fallback_site_rule is None and p.manifest_reading.site_output_rule is None
    assert p.manifest_reading.docs_content_rule == "R-docs-site-content"
    run(tmp_path, p, {"docusaurus.config.js": "x", "docs/guide/a.md": "x", "docs/guide/b.md": "x"})      # runs without the fallback sections


def test_a_replaced_rule_changes_only_its_own_claims(tmp_path):
    base = load_profile("code-repo-conventions", PROFILES)
    raw = yaml.safe_load((PROFILES / "code-repo-conventions.yaml").read_text())
    scripts = next(r for r in raw["rules"] if r["id"] == "R-conv-scripts")
    p = overlay(tmp_path, "mine", extends=["code-repo-conventions"], roles=["component", "tooling"],
                relevance={"primary": ["component"], "supporting": ["tooling"], "hidden": []},
                rules=[{**scripts, "match": {"path_glob": "*", "segment_regex": ["(?i)^scripts$"]}, "file_scope": True}])
    assert [r.id for r in p.rules] == [r.id for r in base.rules] and p.replaced == ("R-conv-scripts",)
    r = run(tmp_path, p, {"pyproject.toml": "[project]\nname='r'\n", "scripts/a.sh": "x", "script/b.sh": "x"})
    assert r.f["scripts"]["rule_id"] == "R-conv-scripts" and "script" not in r.f
