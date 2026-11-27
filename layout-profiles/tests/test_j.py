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
    assert load_profile("code-repo-conventions", PROFILES).version == "0.11.0" and load_profile("code-repo", PROFILES).version == "0.5.0"
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
    # an overlay beside no copies: it extends the SHIPPED profiles in place (J3b)
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


# ======================================================================== J2 ========================================================================================
def lbase(tmp_path):
    write(tmp_path, "base", {**BASE, "profile_id": "base", "lists": {"mf": ["a.toml", "b.json"], "other": ["x.cfg"]},
                             "rules": [rule({"has_file": "$mf"}, rid="A"), rule({"name_regex": ["^(?:{$mf})$"]}, rid="B"), rule({"has_file": "$other"}, rid="C")]})
    return load_profile("base", tmp_path)


@pytest.mark.parametrize("op,vals,want", [("replace", ["c.yml"], ("c.yml",)), ("add", ["c.yml"], ("a.toml", "b.json", "c.yml")),
                                          ("remove", ["a.toml"], ("b.json",))])
def test_each_override_changes_the_list_and_the_inherited_rules_that_use_it(tmp_path, op, vals, want):
    b = lbase(tmp_path)
    p = prof(tmp_path, name="child", extends=["base"], lists={"mf": {op: vals}}, rules=[rule({"has_file": "$mf"}, rid="OWN")])
    by = {r.id: r for r in p.rules}
    assert p.lists["mf"] == want and p.lists["other"] == ("x.cfg",) and p.overridden == ("mf",)
    assert by["A"].has_files == frozenset(want) and by["OWN"].has_files == frozenset(want)
    assert all(by["B"].name_res[0].search(x) for x in want) and not any(by["B"].name_res[0].search(x) for x in {"a.toml", "b.json"} - set(want))
    assert by["A"].origin == "base"                                            # recompiled, still defined by the base
    assert by["C"] is {r.id: r for r in b.rules}["C"] or by["C"] == {r.id: r for r in b.rules}["C"]    # a rule that does not use the list is untouched


def test_an_override_carries_through_a_further_extends(tmp_path):
    lbase(tmp_path)
    write(tmp_path, "mid", {**BASE, "profile_id": "mid", "extends": ["base"], "lists": {"mf": {"add": ["c.yml"]}}, "rules": []})
    p = prof(tmp_path, name="top", extends=["mid"], lists={"mf": {"remove": ["a.toml"]}}, rules=[])
    assert p.lists["mf"] == ("b.json", "c.yml") and p.overridden == ("mf",) and {r.id: r for r in p.rules}["A"].has_files == frozenset({"b.json", "c.yml"})


@pytest.mark.parametrize("lists,msg", [
    ({"nope": {"add": ["x"]}}, "unknown list"),
    ({"mf": {"add": ["a.toml"]}}, "already in the list"),
    ({"mf": {"remove": ["zz"]}}, "not in the list"),
    ({"mf": {"remove": ["a.toml", "b.json"]}}, "would be empty"),
    ({"mf": {"replace": []}}, "non-empty"),
    ({"mf": {"replace": ["a/b"]}}, "'/'"),
    ({"mf": {"add": ["x", "x"]}}, "twice"),
    ({"mf": {"add": [3]}}, "non-empty"),
    ({"mf": {"add": ["x"], "remove": ["a.toml"]}}, "exactly one"),
    ({"mf": {"append": ["x"]}}, "exactly one"),
    ({"mf": ["c.yml"]}, "already defined by an extended profile"),
])
def test_a_bad_override_is_rejected(tmp_path, lists, msg):
    lbase(tmp_path)
    with pytest.raises(ProfileError, match=msg):
        prof(tmp_path, name="child", extends=["base"], lists=lists, rules=[])


def test_a_profile_cannot_override_its_own_list(tmp_path):
    with pytest.raises(ProfileError, match="unknown list"):
        prof(tmp_path, lists={"mf": {"add": ["x"]}}, rules=[rule({"has_file": "a"})])


def test_a_new_list_and_an_override_in_one_profile(tmp_path):
    lbase(tmp_path)
    p = prof(tmp_path, name="child", extends=["base"], lists={"mine": ["q.txt"], "other": {"replace": ["y.cfg"]}}, rules=[rule({"has_file": "$mine"}, rid="M")])
    assert p.lists["mine"] == ("q.txt",) and {r.id: r for r in p.rules}["C"].has_files == frozenset({"y.cfg"}) and p.overridden == ("other",)


def test_the_shipped_profiles_override_nothing():
    for pid in ("code-repo-conventions", "code-repo", "docs-site", "generic-relevance", "workspace-repo"):
        assert load_profile(pid, PROFILES).overridden == ()


# ---- on a tree: the shared test-folder list, overridden once, changes BOTH rules that use it
def test_adding_a_test_folder_name_changes_both_test_folder_rules(tmp_path):
    p = overlay(tmp_path, "mine", extends=["code-repo-conventions"], lists={"test-folder-names": {"add": ["qa"]}})
    r = run(tmp_path, p, {"pyproject.toml": "[project]\nname='r'\n", "qa/x/package.json": '{"name": "x"}', "qa/y/package.json": '{"name": "y"}'})
    assert r.f["qa"]["rule_id"] == "R-conv-tests" and r.f["qa/x"]["rule_id"] == "R-fx-test-project" and "qa/x" not in r.allc


def test_removing_a_test_folder_name_changes_both_test_folder_rules(tmp_path):
    p = overlay(tmp_path, "mine", extends=["code-repo-conventions"], lists={"test-folder-names": {"remove": ["e2e"]}})
    r = run(tmp_path, p, {"pyproject.toml": "[project]\nname='r'\n", "e2e/a.ts": "x", "pkg/e2e/p/package.json": '{"name": "p"}'})
    assert "e2e" not in r.f and "pkg/e2e/p" in r.allc and r.f["pkg/e2e/p"]["rule_id"] == "R-comp-package-json"


def test_the_default_profile_keeps_qa_and_e2e_as_before(tmp_path):
    r = run(tmp_path, load_profile("code-repo-conventions", PROFILES), {"pyproject.toml": "[project]\nname='r'\n", "qa/x/package.json": '{"name": "x"}', "e2e/a.ts": "x"})
    assert "qa/x" in r.allc and r.f["e2e"]["rule_id"] == "R-conv-tests"


# ======================================================================== J3 ========================================================================================
DEFAULTS = {"scripts-are-tooling": True, "lint-config-is-tooling": True, "docs-min-files": 2, "private-test-packages-internal": True,
            "gradle-test-projects-internal": True, "src-docs-is-documentation": True}
PYR = {"pyproject.toml": "[project]\nname='r'\n"}


def mine(tmp_path, **settings):
    return overlay(tmp_path, "mine", extends=["code-repo-conventions"], settings=settings)


def test_the_shipped_settings_and_their_defaults():
    p = load_profile("code-repo-conventions", PROFILES)
    assert p.settings == DEFAULTS and set(p.settings_decl) == set(DEFAULTS) and p.settings_set == () and p.version == "0.11.0"
    assert all(d["doc"] for d in p.settings_decl.values()) and p.settings_decl["private-test-packages-internal"]["reads"] == ("package-json.private",)
    assert p.manifest_reading.skip_fields == frozenset()
    assert [r.id for r in p.rules] == [r.id for r in p.all_rules]                # every rule is active at the defaults
    c = compose_profiles("code-repo-conventions,docs-site", PROFILES)
    assert c.settings == DEFAULTS


def test_setting_every_default_explicitly_changes_nothing(tmp_path):
    p = mine(tmp_path, **DEFAULTS)
    d = load_profile("code-repo-conventions", PROFILES)
    assert [r.id for r in p.rules] == [r.id for r in d.rules] and p.settings == DEFAULTS and p.settings_set == tuple(DEFAULTS)
    assert [(r.id, r.match) for r in p.rules] == [(r.id, r.match) for r in d.rules]


# ---- each setting, both states, on a synthetic tree
def test_scripts_are_tooling_on_and_off(tmp_path):
    files = {**PYR, "scripts/a.sh": "x", "scripts-ts/package.json": '{"name": "x"}', "scripts-ts/src/x.ts": "x"}
    on = run(tmp_path / "on", load_profile("code-repo-conventions", PROFILES), files)
    assert on.f["scripts"]["rule_id"] == on.f["scripts-ts"]["rule_id"] == "R-conv-scripts" and "scripts-ts/src" not in on.allc
    off = run(tmp_path / "off", mine(tmp_path, **{"scripts-are-tooling": False}), files)
    assert "scripts" not in off.f and off.f["scripts-ts"]["rule_id"] == "R-comp-package-json" and off.f["scripts-ts/src"]["rule_id"] == "R-conv-node-src"
    tools = run(tmp_path / "tools", mine(tmp_path, **{"scripts-are-tooling": False}), {**PYR, "tools/package.json": '{"name": "t"}'})
    assert tools.f["tools"]["rule_id"] == "R-tool-package"                       # the tooling principle itself is fixed


def test_lint_config_is_tooling_on_and_off(tmp_path):
    files = {**PYR, "config/checkstyle.xml": "x", "config/suppressions.xml": "x"}
    assert run(tmp_path / "on", load_profile("code-repo-conventions", PROFILES), files).f["config"]["rule_id"] == "R-conv-config-lint"
    off = run(tmp_path / "off", mine(tmp_path, **{"lint-config-is-tooling": False}), files)
    assert off.f["config"]["rule_id"] == "R-conv-config" and "config" in off.allc


@pytest.mark.parametrize("n,docs_one,docs_two", [(2, False, True), (1, True, True), (3, False, False)])
def test_docs_min_files(tmp_path, n, docs_one, docs_two):
    p = load_profile("code-repo-conventions", PROFILES) if n == 2 else mine(tmp_path, **{"docs-min-files": n})
    r1 = run(tmp_path / "one", p, {**PYR, "docs/a.md": "x", "src/main/docs/a.adoc": "x"})
    r2 = run(tmp_path / "two", p, {**PYR, "docs/a.md": "x", "docs/b.md": "x", "src/main/docs/a.adoc": "x", "src/main/docs/b.adoc": "x"})
    assert ("docs" in r1.allc) is docs_one and ("src/main/docs" in r1.allc) is docs_one
    assert ("docs" in r2.allc) is docs_two and ("src/main/docs" in r2.allc) is docs_two
    by = {r.id: r for r in p.rules}
    assert by["R-conv-docs"].content_min == by["R-conv-src-docs"].content_min == n


def reads_of(tmp_path, p, files):
    root = tmp_path / "t"
    for rel, content in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(content)
    lst = tmp_path / "t.tsv"
    lst.write_text("".join(f"{k}\t{len(v)}\n" for k, v in sorted(files.items())))
    rec = Recognizer(p, blob_source=mf.FileSource(str(root)))
    rec.run(lst, tmp_path / "o")
    return rec


def test_private_test_packages_on_and_off_and_off_does_not_read_the_field(tmp_path):
    files = {"package.json": '{"name": "r"}', "x-test/package.json": '{"name": "x", "private": true}', "n-test/package.json": '{"private": true}'}
    on = run(tmp_path / "on", load_profile("code-repo-conventions", PROFILES), files)
    assert on.f["x-test"]["rule_id"] == "R-ts-private-package" and "x-test" not in on.allc
    p = mine(tmp_path, **{"private-test-packages-internal": False})
    assert p.manifest_reading.skip_fields == frozenset({"package-json.private"}) and "R-ts-private-package" not in [r.id for r in p.rules]
    off = run(tmp_path / "off", p, files)
    assert "x-test" in off.allc and off.f["x-test"]["rule_id"] == "R-comp-package-json"
    rec = reads_of(tmp_path, p, files)
    assert all(d.private is False for ds in rec.reading.decls.values() for d in ds)          # D-J4: the field is not extracted at all
    assert "n-test/package.json" not in rec.reading.decls                                    # a package.json that says only private declares nothing now
    rec_on = reads_of(tmp_path / "on2", load_profile("code-repo-conventions", PROFILES), files)
    assert rec_on.reading.log == rec.reading.log                                             # the same files are opened either way


def test_gradle_test_projects_on_and_off(tmp_path):
    files = {"build.gradle": "", "settings.gradle": "rootProject.name = 'r'\n", "x-codegen-test/build.gradle": "", "x-codegen-test/model/a.smithy": "x"}
    assert run(tmp_path / "on", load_profile("code-repo-conventions", PROFILES), files).f["x-codegen-test"]["rule_id"] == "R-fx-gradle-test-project"
    off = run(tmp_path / "off", mine(tmp_path, **{"gradle-test-projects-internal": False}), files)
    assert "x-codegen-test" in off.allc and off.f["x-codegen-test"]["rule_id"] == "R-comp-gradle"


def test_src_docs_is_documentation_on_and_off(tmp_path):
    files = {**PYR, "src/main/docs/a.adoc": "x", "src/main/docs/b.adoc": "x"}
    assert "src/main/docs" in run(tmp_path / "on", load_profile("code-repo-conventions", PROFILES), files).allc
    off = run(tmp_path / "off", mine(tmp_path, **{"src-docs-is-documentation": False}), files)
    assert "src/main/docs" not in off.allc and "src/main/docs" not in off.f


def test_test_folder_names_is_a_list_not_a_switch():
    p = load_profile("code-repo-conventions", PROFILES)
    assert "test-folder-names" in p.lists and "test-folder-names" not in p.settings


# ---- `when:` and settings across extends
def test_an_inactive_rule_comes_back_when_a_further_profile_turns_the_setting_on(tmp_path):
    overlay(tmp_path, "off", extends=["code-repo-conventions"], settings={"scripts-are-tooling": False})
    write(tmp_path, "on", {"profile_id": "on", "version": "0.1.0", "status": "proposed", "applies_to": "code-repo", "roles": ["component"],
                           "relevance": {"primary": ["component"], "supporting": [], "hidden": []}, "rules": [], "extends": ["off"],
                           "settings": {"scripts-are-tooling": True}})
    p = load_profile("on", tmp_path)
    off = load_profile("off", tmp_path)
    assert "R-conv-scripts" not in [r.id for r in off.rules] and "R-conv-scripts" in [r.id for r in off.all_rules]
    assert [r.id for r in p.rules] == [r.id for r in load_profile("code-repo-conventions", PROFILES).rules]
    assert len({r.id: r for r in p.rules}["R-tool-package"].segment_res) == 2 and len({r.id: r for r in off.rules}["R-tool-package"].segment_res) == 1
    assert p.settings_set == ("scripts-are-tooling",)


def sprof(tmp_path, name="s", **doc):
    return prof(tmp_path, name=name, **doc)


DECL = {"flag": {"type": "bool", "default": True, "doc": "d"}, "n": {"type": "int", "default": 2, "doc": "d"}, "names": {"type": "list", "default": ["a"], "doc": "d"}}


def test_when_and_setting_references_in_a_synthetic_profile(tmp_path):
    p = sprof(tmp_path, settings=DECL, rules=[rule({"has_file": "a"}, rid="ON"), {**rule({"has_file": "b"}, rid="OFF"), "when": {"flag": False}},
                                             rule({"path_glob": "docs", "min_content": {"files": ["x"], "min_files": "$n", "extensions": [".md"]}}, rid="D"),
                                             rule({"has_file": ["z", {"when": {"flag": True}, "item": "w"}, {"when": {"flag": False}, "item": "v"}]}, rid="C"),
                                             rule({"has_file": "$names"}, rid="L")])
    by = {r.id: r for r in p.rules}
    assert set(by) == {"ON", "D", "C", "L"} and by["D"].content_min == 2 and by["C"].has_files == frozenset({"z", "w"}) and by["L"].has_files == frozenset({"a"})
    write(tmp_path, "c", {**BASE, "profile_id": "c", "extends": ["s"], "settings": {"flag": False, "n": 5, "names": ["q", "r"]}, "rules": []})
    c = load_profile("c", tmp_path)
    cb = {r.id: r for r in c.rules}
    assert set(cb) == {"ON", "OFF", "D", "C", "L"} and cb["D"].content_min == 5 and cb["C"].has_files == frozenset({"z", "v"}) and cb["L"].has_files == frozenset({"q", "r"})
    assert c.settings == {"flag": False, "n": 5, "names": ["q", "r"]} and c.settings_set == ("flag", "n", "names")


@pytest.mark.parametrize("settings", [
    {"x": {"type": "float", "default": 1, "doc": "d"}},
    {"x": {"type": "bool", "default": 1, "doc": "d"}},
    {"x": {"type": "int", "default": True, "doc": "d"}},
    {"x": {"type": "list", "default": [], "doc": "d"}},
    {"x": {"type": "bool", "default": True, "doc": ""}},
    {"x": {"type": "bool", "default": True}},
    {"x": {"type": "bool", "default": True, "doc": "d", "extra": 1}},
    {"Bad": {"type": "bool", "default": True, "doc": "d"}},
    {},
])
def test_a_bad_setting_declaration_is_rejected(tmp_path, settings):
    with pytest.raises(ProfileError):
        sprof(tmp_path, settings=settings, rules=[rule({"has_file": "a"})])


def test_setting_values_are_validated(tmp_path):
    sprof(tmp_path, settings=DECL, rules=[rule({"has_file": "a"})])
    for vals, msg in (({"nope": True}, "not a setting declared"), ({"flag": "yes"}, "not a bool"), ({"n": 2.5}, "not a int"), ({"names": "a"}, "not a list")):
        write(tmp_path, "c", {**BASE, "profile_id": "c", "extends": ["s"], "settings": vals, "rules": []})
        with pytest.raises(ProfileError, match=msg):
            load_profile("c", tmp_path)
    write(tmp_path, "c", {**BASE, "profile_id": "c", "extends": ["s"], "settings": {"flag": {"type": "bool", "default": False, "doc": "d"}}, "rules": []})
    with pytest.raises(ProfileError, match="already declared"):
        load_profile("c", tmp_path)


@pytest.mark.parametrize("r,msg", [
    ({**rule({"has_file": "a"}), "when": {"nope": True}}, "not a declared setting"),
    ({**rule({"has_file": "a"}), "when": {"flag": 1}}, "type"),
    ({**rule({"has_file": "a"}), "when": {}}, "when needs"),
    (rule({"has_file": "$flag"}), "bool setting"),
    (rule({"has_file": ["a", {"when": {"nope": True}, "item": "b"}]}), "not a declared setting"),
])
def test_bad_when_and_references_are_rejected(tmp_path, r, msg):
    with pytest.raises(ProfileError, match=msg):
        sprof(tmp_path, settings=DECL, rules=[r])


def test_a_setting_and_a_list_may_not_share_a_name(tmp_path):
    with pytest.raises(ProfileError, match="share"):
        sprof(tmp_path, lists={"flag": ["a"]}, settings=DECL, rules=[rule({"has_file": "a"})])


# ---- D-J4: narrow only. No setting, list or override can add a reader, a manifest field or a content read.
READING = {"readers": ["package-json"], "member_rule": {"id": "M", "role": "component", "kind": "k", "basis": "manifest-content", "confidence": "high", "evidence": "e"},
           "aggregator_rule": {"id": "AG", "role": "tooling", "kind": "k", "basis": "manifest-content", "confidence": "high", "evidence": "e"}}


@pytest.mark.parametrize("reading", [
    {**READING, "readers": "$my-readers"},
    {**READING, "readers": ["package-json", "$more"]},
    {**READING, "readers": ["{$more}"]},
    {**READING, "max_file_bytes": "$n"},
])
def test_manifest_reading_may_not_name_a_list_or_a_setting(tmp_path, reading):
    with pytest.raises(ProfileError, match="D-J4"):
        sprof(tmp_path, lists={"my-readers": ["mkdocs"], "more": ["mkdocs"]}, settings=DECL, manifest_reading=reading, rules=[rule({"has_file": "a"})])


def test_an_overlay_cannot_reach_the_readers_through_a_list_override(tmp_path):
    # the readers are never resolved from a list, so overriding a list changes no reader: shown on the shipped profile
    p = overlay(tmp_path, "mine", extends=["code-repo-conventions"], lists={"manifest-files": {"add": ["mkdocs.yml"]}})
    d = load_profile("code-repo-conventions", PROFILES)
    assert p.manifest_reading.readers == d.manifest_reading.readers and p.manifest_reading.skip_fields == d.manifest_reading.skip_fields
    with pytest.raises(ProfileError, match="D-J4"):
        overlay(tmp_path, "mine2", extends=["code-repo-conventions"], manifest_reading={**READING, "readers": "$manifest-files"})


@pytest.mark.parametrize("decl,msg", [
    ({"type": "bool", "default": True, "doc": "d", "reads": ["package-json.version"]}, "narrow"),     # a field not read today
    ({"type": "bool", "default": True, "doc": "d", "reads": ["mkdocs.nav"]}, "narrow"),
    ({"type": "bool", "default": False, "doc": "d", "reads": ["package-json.private"]}, "default is true"),   # off by default = ON would add the read
    ({"type": "int", "default": 1, "doc": "d", "reads": ["package-json.private"]}, "bool"),
    ({"type": "bool", "default": True, "doc": "d", "reads": []}, "narrow"),
    ({"type": "bool", "default": True, "doc": "d", "readers": ["mkdocs"]}, "unknown key"),            # no way to name a reader
    ({"type": "bool", "default": True, "doc": "d", "fields": ["package-json.version"]}, "unknown key"),
])
def test_a_setting_cannot_widen_what_is_read(tmp_path, decl, msg):
    with pytest.raises(ProfileError, match=msg):
        sprof(tmp_path, settings={"s1": decl}, rules=[rule({"has_file": "a"})])


def test_turning_a_read_setting_on_again_reads_exactly_what_the_default_reads(tmp_path):
    overlay(tmp_path, "off", extends=["code-repo-conventions"], settings={"private-test-packages-internal": False})
    write(tmp_path, "on", {"profile_id": "on", "version": "0.1.0", "status": "proposed", "applies_to": "code-repo", "roles": ["component"],
                           "relevance": {"primary": ["component"], "supporting": [], "hidden": []}, "rules": [], "extends": ["off"],
                           "settings": {"private-test-packages-internal": True}})
    assert load_profile("on", tmp_path).manifest_reading.skip_fields == frozenset() == load_profile("code-repo-conventions", PROFILES).manifest_reading.skip_fields


# ======================================================================== J3b =======================================================================================
# D-J4 (the Architect's ruling): a profile loaded from the package's own profiles/ folder is SHIPPED; any other file is an OVERLAY. A chain with an overlay may
# read no more than the shipped profiles of the chain: the same or fewer readers, no field they skip, caps only tighter.
CODE_MR = {"member_rule": {"id": "M2", "role": "component", "kind": "k", "basis": "manifest-content", "confidence": "high", "evidence": "e"},
           "aggregator_rule": {"id": "AG2", "role": "other", "kind": "k", "basis": "manifest-content", "confidence": "high", "evidence": "e"}}


def test_shipped_and_overlay_are_recorded_for_every_profile_of_the_chain(tmp_path):
    d = load_profile("code-repo-conventions", PROFILES)
    assert d.shipped is True and d.has_overlay is False
    assert dict(d.chain_shipped) == {"code-repo-conventions": True, "code-repo": True, "generic-relevance": True}
    p = overlay(tmp_path, "mine", extends=["code-repo-conventions"], settings={"docs-min-files": 1})
    assert p.shipped is False and p.has_overlay is True and dict(p.chain_shipped)["mine"] is False and dict(p.chain_shipped)["code-repo"] is True
    c = compose_profiles("code-repo-conventions,docs-site", PROFILES)
    assert c.shipped is None and c.has_overlay is False


def test_an_overlay_adding_a_reader_is_rejected(tmp_path):
    with pytest.raises(ProfileError, match=r"D-J4.*\['compose-services'\]"):
        overlay(tmp_path, "mine", extends=["code-repo-conventions"], manifest_reading={"readers": ["compose-services"]})


def test_an_overlay_adding_a_reader_through_a_composition_with_its_own_reading_is_rejected(tmp_path):
    with pytest.raises(ProfileError, match="D-J4"):
        overlay(tmp_path, "mine", extends=["generic-relevance"], roles=["component", "other", "tooling"],
                relevance={"primary": ["component"], "supporting": ["other", "tooling"], "hidden": []},
                manifest_reading={"readers": ["package-json"], **CODE_MR})


def test_an_overlay_adding_a_field_is_rejected(tmp_path):
    # the only fields are those the readers extract; an overlay cannot name a field, and a field a shipped chain skips cannot be read again
    with pytest.raises(ProfileError):
        overlay(tmp_path, "mine", extends=["code-repo-conventions"], manifest_reading={"readers": ["package-json"], "fields": ["package-json.version"], **CODE_MR})
    with pytest.raises(ProfileError, match="narrow"):
        overlay(tmp_path, "mine2", extends=["code-repo-conventions"], settings={"read-more": {"type": "bool", "default": True, "doc": "d", "reads": ["package-json.version"]}})


def test_an_overlay_may_not_read_a_field_a_shipped_profile_skips(tmp_path):
    # model: a shipped chain whose package-json.private is skipped; an overlay of it that turns the setting back on would read the field again
    import recognizer.layout_profile as lpm
    shipped = load_profile("code-repo-conventions", PROFILES)
    from dataclasses import replace
    base = replace(shipped, shipped_skip=frozenset({"package-json.private"}))
    orig = lpm.load_profile
    try:
        lpm.load_profile = lambda pid, d=None, _stack=(): base if pid == "code-repo-conventions" else orig(pid, d, _stack)
        with pytest.raises(ProfileError, match="skip"):
            lpm.parse_profile({**BASE, "profile_id": "mine", "extends": ["code-repo-conventions"], "rules": []}, "mine", PROFILES)
    finally:
        lpm.load_profile = orig


def test_an_overlay_narrowing_is_accepted(tmp_path):
    p = overlay(tmp_path, "mine", extends=["code-repo-conventions"], settings={"private-test-packages-internal": False}, roles=["component", "other"],
                relevance={"primary": ["component"], "supporting": ["other"], "hidden": []}, manifest_reading={"readers": ["package-json"], "max_blobs": 100, **CODE_MR})
    d = load_profile("code-repo-conventions", PROFILES)
    assert set(p.manifest_reading.readers) == set(d.manifest_reading.readers) and p.manifest_reading.max_blobs == 100
    assert p.manifest_reading.skip_fields == frozenset({"package-json.private"})


def test_an_overlay_reading_nothing_new_is_accepted_and_reads_the_same(tmp_path):
    p = overlay(tmp_path, "mine", extends=["code-repo-conventions"], settings={"docs-min-files": 1})
    d = load_profile("code-repo-conventions", PROFILES)
    assert p.manifest_reading == d.manifest_reading


def test_a_shipped_profile_adding_a_reader_is_accepted_as_today():
    d = load_profile("docs-site", PROFILES)                        # docs-site adds mkdocs to generic-relevance's gitmodules: both shipped
    g = load_profile("generic-relevance", PROFILES)
    assert set(d.manifest_reading.readers) - set(g.manifest_reading.readers) == {"mkdocs"} and d.has_overlay is False
    w = load_profile("workspace-repo", PROFILES)
    assert "compose-services" in w.manifest_reading.readers and w.has_overlay is False


def test_a_copy_of_a_shipped_profile_in_another_folder_is_an_overlay(tmp_path):
    import shutil
    shutil.copy(PROFILES / "docs-site.yaml", tmp_path / "docs-site.yaml")      # a byte-identical copy, outside the package's profiles/ folder
    with pytest.raises(ProfileError, match=r"D-J4.*mkdocs"):
        load_profile("docs-site", tmp_path)                                    # its base generic-relevance is shipped (found in place); the copy adds mkdocs
    shutil.copy(PROFILES / "generic-relevance.yaml", tmp_path / "generic-relevance.yaml")
    with pytest.raises(ProfileError, match="D-J4"):
        load_profile("generic-relevance", tmp_path)                            # no shipped profile in the chain at all: it may read nothing


def test_a_copy_that_reads_nothing_is_an_overlay_that_loads(tmp_path):
    import shutil
    shutil.copy(PROFILES / "worktree-copies.yaml", tmp_path / "worktree-copies.yaml")
    p = load_profile("worktree-copies", tmp_path)
    assert p.shipped is False and p.has_overlay is True


def test_an_overlay_may_not_loosen_a_cap(tmp_path):
    with pytest.raises(ProfileError):
        overlay(tmp_path, "mine", extends=["code-repo-conventions"], roles=["component", "other"], relevance={"primary": ["component"], "supporting": ["other"], "hidden": []},
                manifest_reading={"readers": ["package-json"], "max_blobs": 6000, **CODE_MR})


def test_the_cli_default_folder_is_shipped():
    from recognizer.recognize import DEFAULT_PROFILES
    from recognizer.layout_profile import SHIPPED_DIR
    assert DEFAULT_PROFILES.resolve() == SHIPPED_DIR
