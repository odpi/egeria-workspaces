"""Phase 1e (E1): a SINGULAR -test or _test folder that groups projects (it is not itself a project and has more than one project below it) is a test segment.
Synthetic only. Known limit (stated in the README): a real product folder that groups two or more published test libraries would be excluded."""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from recognizer import manifests as mf
from recognizer.layout_profile import ProfileError, load_profile
from recognizer.recognize import Recognizer

PROFILES = Path(__file__).resolve().parent.parent / "profiles"
RECOGNIZER = Path(__file__).resolve().parent.parent / "recognizer"


def survey(tmp_path, files, out="out", name="tree", source=True, profile="code-repo-conventions"):
    root = tmp_path / name
    for rel, content in files.items():
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content)
    lst = tmp_path / f"{name}.tsv"
    lst.write_text("".join(f"{p}\t{len(files[p].encode())}\n" for p in sorted(files)))
    rec = Recognizer(load_profile(profile, PROFILES), blob_source=mf.FileSource(str(root)) if source else None)
    c = rec.run(lst, tmp_path / out)
    f = {x["path"]: x for x in map(json.loads, (tmp_path / out / "findings.jsonl").read_text().splitlines()) if not x["rule_id"].startswith("F-")}
    return SimpleNamespace(c=c, f=f, rec=rec, allc=(tmp_path / out / "components-all.txt").read_text().split(), top=(tmp_path / out / "components.txt").read_text().split())


PKG = '{"name": "x"}'
ROOT = {"pyproject.toml": "[project]\nname='r'\n"}


# ---- (1) a top-level <word>-test/ with 3 Gradle includes and no manifest of its own ------------------------------------------------------------------------------
@pytest.mark.parametrize("with_build_files", [True, False])
def test_a_top_level_singular_test_folder_with_three_gradle_includes_is_a_test_suite_and_its_members_are_excluded(tmp_path, with_build_files):
    files = {**ROOT, "settings.gradle": "include 'wb-test:a', 'wb-test:b', 'wb-test:c'\ninclude 'core'\n", "core/build.gradle": "", "core/src/Main.java": "x"}
    for m in "abc":
        files[f"wb-test/{m}/src/T.java"] = "x"
        if with_build_files:
            files[f"wb-test/{m}/build.gradle"] = ""
    r = survey(tmp_path, files)
    assert r.f["wb-test"]["role"] == "component" and r.f["wb-test"]["kind"] == "test-suite" and r.f["wb-test"]["rule_id"] == "R-conv-test-group"
    assert "wb-test" in r.top and "core" in r.allc
    for m in "abc":
        p = f"wb-test/{m}"
        assert p not in r.allc and r.f[p]["role"] == "fixture"
    assert r.f["core"]["role"] == "component"


# ---- (2) a nested pkg/<word>_test/ with 2 npm packages -----------------------------------------------------------------------------------------------------------
def test_a_nested_singular_test_folder_with_two_npm_packages_excludes_them_and_is_not_a_component(tmp_path):
    files = {**ROOT, "pkg/real/package.json": PKG, "pkg/e2e_test/a/package.json": PKG, "pkg/e2e_test/b/package.json": PKG}
    r = survey(tmp_path, files)
    assert "pkg/e2e_test/a" not in r.allc and "pkg/e2e_test/b" not in r.allc and "pkg/e2e_test" not in r.allc
    assert r.f["pkg/e2e_test/a"]["rule_id"] == "R-fx-test-group-project" and r.f["pkg/e2e_test/a"]["role"] == "fixture"
    assert "pkg/real" in r.allc


# ---- (3) a leaf project named ...-test --------------------------------------------------------------------------------------------------------------------------
def test_a_leaf_project_named_test_stays_a_component(tmp_path):
    r = survey(tmp_path, {**ROOT, "plugins/chart-paired-t-test/package.json": PKG, "plugins/other/package.json": PKG})
    assert "plugins/chart-paired-t-test" in r.allc and r.f["plugins/chart-paired-t-test"]["rule_id"] == "R-comp-package-json"


def test_a_top_level_leaf_project_named_test_stays_a_component(tmp_path):
    r = survey(tmp_path, {**ROOT, "paired-t-test/package.json": PKG, "other/package.json": PKG})
    assert "paired-t-test" in r.allc and r.f["paired-t-test"]["role"] == "component" and r.f["paired-t-test"]["rule_id"] == "R-comp-package-json"


# ---- (4) a <word>-test/ holding ONE project ----------------------------------------------------------------------------------------------------------------------
def test_a_singular_test_folder_with_one_project_is_unchanged(tmp_path):
    r = survey(tmp_path, {**ROOT, "smoke-test/inner/package.json": PKG, "other/package.json": PKG})
    assert "smoke-test/inner" in r.allc and r.f["smoke-test/inner"]["rule_id"] == "R-comp-package-json"
    assert "smoke-test" not in r.top


def test_a_singular_test_folder_with_one_gradle_include_is_unchanged(tmp_path):
    r = survey(tmp_path, {**ROOT, "settings.gradle": "include 'wb-test:a'\n", "wb-test/a/build.gradle": "", "wb-test/a/src/T.java": "x"})
    assert "wb-test/a" in r.allc and "wb-test" not in r.top


# ---- (5) a <word>-test/ that has its own manifest and 2 sub-projects ---------------------------------------------------------------------------------------------
def test_a_singular_test_folder_that_is_itself_a_project_is_unchanged(tmp_path):
    r = survey(tmp_path, {**ROOT, "x-test/package.json": PKG, "x-test/a/package.json": PKG, "x-test/b/package.json": PKG})
    assert "x-test" in r.allc and r.f["x-test"]["rule_id"] == "R-comp-package-json"
    assert "x-test/a" in r.allc and "x-test/b" in r.allc


def test_a_singular_test_folder_that_is_a_declared_gradle_project_is_unchanged(tmp_path):
    files = {**ROOT, "settings.gradle": "include 'x-test', 'x-test:a', 'x-test:b'\n", "x-test/build.gradle": "", "x-test/a/build.gradle": "", "x-test/b/build.gradle": ""}
    r = survey(tmp_path, files)
    assert "x-test" in r.allc and "x-test/a" in r.allc and "x-test/b" in r.allc


# ---- (6) words that end in "test" without the separator ----------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("word", ["latest", "contest", "attest", "protest", "greatest"])
def test_words_ending_in_test_without_a_separator_are_unchanged(tmp_path, word):
    r = survey(tmp_path, {**ROOT, f"{word}/a/package.json": PKG, f"{word}/b/package.json": PKG, f"pkg/{word}/c/package.json": PKG, f"pkg/{word}/d/package.json": PKG})
    for p in (f"{word}/a", f"{word}/b", f"pkg/{word}/c", f"pkg/{word}/d"):
        assert p in r.allc and r.f[p]["rule_id"] == "R-comp-package-json"
    assert word not in r.top


@pytest.mark.parametrize("seg", ["wb-test", "WB_TEST", "Wb-Test"])
def test_the_suffix_is_case_insensitive_and_either_separator(tmp_path, seg):
    r = survey(tmp_path, {**ROOT, f"{seg}/a/package.json": PKG, f"{seg}/b/package.json": PKG})
    assert seg in r.top and f"{seg}/a" not in r.allc


# ---- the count is "more than one project", and the plural-only ruling for leaf projects stays ---------------------------------------------------------------------
def test_a_nested_group_with_exactly_two_projects_excludes_both_and_one_fewer_does_not(tmp_path):
    two = survey(tmp_path, {**ROOT, "pkg/it_test/a/package.json": PKG, "pkg/it_test/b/package.json": PKG}, out="two", name="two")
    one = survey(tmp_path, {**ROOT, "pkg/it_test/a/package.json": PKG}, out="one", name="one")
    assert "pkg/it_test/a" not in two.allc and "pkg/it_test/a" in one.allc


def test_a_deeper_project_below_a_group_is_excluded_too(tmp_path):
    r = survey(tmp_path, {**ROOT, "app-test/suites/s1/package.json": PKG, "app-test/suites/s2/package.json": PKG, "app-test/suites/s2/deep/package.json": PKG})
    assert not [p for p in r.allc if p.startswith("app-test/")] and "app-test" in r.top


def test_a_leaf_singular_project_inside_a_plain_folder_with_other_projects_stays(tmp_path):
    r = survey(tmp_path, {**ROOT, "libs/a/package.json": PKG, "libs/b/package.json": PKG, "libs/unit-test/package.json": PKG})
    assert "libs/unit-test" in r.allc and "libs/a" in r.allc


def test_names_only_runs_count_manifest_files(tmp_path):
    r = survey(tmp_path, {**ROOT, "wb-test/a/package.json": PKG, "wb-test/b/package.json": PKG}, source=False)
    assert "wb-test" in r.top and "wb-test/a" not in r.allc


def test_a_vendored_project_does_not_count_towards_the_group(tmp_path):
    files = {**ROOT, "wb-test/a/package.json": PKG, "wb-test/node_modules/x/package.json": PKG}
    r = survey(tmp_path, files)
    assert "wb-test/a" in r.allc and "wb-test" not in r.top


def test_the_composite_profile_with_docs_site_behaves_the_same(tmp_path):
    from recognizer.layout_profile import compose_profiles
    p = compose_profiles("code-repo-conventions,docs-site", PROFILES)
    root = tmp_path / "t"
    for rel in ("pyproject.toml", "wb-test/a/package.json", "wb-test/b/package.json", "x/package.json"):
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text("{}")
    lst = tmp_path / "t.tsv"
    lst.write_text("".join(f"{x}\t2\n" for x in ("pyproject.toml", "wb-test/a/package.json", "wb-test/b/package.json", "x/package.json")))
    Recognizer(p, blob_source=mf.FileSource(str(root))).run(lst, tmp_path / "o")
    allc = (tmp_path / "o" / "components-all.txt").read_text().split()
    assert "wb-test" in allc and "wb-test/a" not in allc and "x" in allc


# ---- the loader --------------------------------------------------------------------------------------------------------------------------------------------------
BASE = {"profile_id": "t", "version": "0.1.0", "status": "proposed", "applies_to": "any", "roles": ["component", "fixture"],
        "relevance": {"primary": ["component"], "supporting": ["fixture"], "hidden": []}}


def prof(tmp_path, match, **extra):
    import yaml
    d = {**BASE, "rules": [{"id": "R", "match": match, "assign": {"role": "fixture"}, "grain": "dir", "basis": "convention", "confidence": "low", "evidence": "x"}], **extra}
    (tmp_path / "t.yaml").write_text(yaml.safe_dump(d))
    return load_profile("t", tmp_path)


@pytest.mark.parametrize("bad", [{"min": 1, "files": ["package.json"]}, {"min": "2", "files": ["package.json"]}, {"min": 2}, {"min": 2, "files": []}, "yes", {"min": 2, "files": ["a"], "extra": 1}, {"min": True, "files": ["a"]}])
def test_groups_projects_is_validated(tmp_path, bad):
    with pytest.raises(ProfileError):
        prof(tmp_path, {"name_regex": ["x$"], "groups_projects": bad})


def test_group_segment_regex_needs_a_regex_and_a_good_one(tmp_path):
    with pytest.raises(ProfileError):
        prof(tmp_path, {"group_segment_regex": {"min": 2, "files": ["package.json"]}})
    with pytest.raises(ProfileError):
        prof(tmp_path, {"group_segment_regex": {"min": 2, "files": ["package.json"], "regex": ["("]}})
    with pytest.raises(ProfileError):
        prof(tmp_path, {"name_regex": ["x$"], "groups_projects": {"min": 2, "files": ["package.json"], "regex": ["x"]}})
    ok = prof(tmp_path, {"group_segment_regex": {"min": 2, "files": ["package.json"], "regex": ["(?i)-test$"]}})
    assert ok.rules[0].is_dir_rule and ok.rules[0].group_min == 2


# ---- no held-out names, structural only ---------------------------------------------------------------------------------------------------------------------------
def test_no_rule_or_recognizer_source_carries_a_held_out_name_or_a_word_list():
    banned = ("smoke", "spring", "integration-test", "system-test")
    for pid in ("code-repo-conventions", "code-repo", "generic-relevance", "docs-site", "workspace-repo"):
        for r in load_profile(pid, PROFILES).rules:
            text = " ".join([*(rx.pattern for rx in r.segment_res + r.name_res + r.group_seg_res), *r.segments, *r.names, *[str(g.pattern) for g in r.globs], *r.group_files]).lower()
            for b in banned:
                assert b not in text, (pid, r.id, b)
    for src in RECOGNIZER.glob("*.py"):
        text = src.read_text().lower()
        for b in banned:
            assert b not in text, (src.name, b)


def test_the_e1_rules_are_structural_and_carry_provenance_and_the_known_limit():
    p = load_profile("code-repo-conventions", PROFILES)
    by = {r.id: r for r in p.rules}
    ids = [r.id for r in p.rules]
    assert p.version == "0.6.0" and ids.index("R-conv-tests") < ids.index("R-conv-test-group") < ids.index("R-fx-test-project") < ids.index("R-fx-test-group-project") < ids.index("R-fx-sample-project")
    for rid in ("R-conv-test-group", "R-fx-test-group-project"):
        assert by[rid].tuned_on == ("spring-boot (D6, spent)",) and "Known limit" in by[rid].evidence and by[rid].group_min == 2
    assert by["R-conv-test-group"].kind == "test-suite" and by["R-conv-test-group"].grain == "component" and by["R-fx-test-group-project"].role == "fixture"
