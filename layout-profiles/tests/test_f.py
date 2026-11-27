"""Phase 1f (F1): a camelCase TEST SOURCE SET directly under `src` (src/intTest, src/functionalTest, src/jvmTest, src/testKit, ...) is a test segment, so a manifest
project at or below it is a fixture (R-fx-test-project), not a component. Synthetic only: the source-set names here are synthetic test paths; no rule names them.
Known limits (stated in the README): Maven's src/it is not matched; a source set without a test word is not matched; Kotlin Multiplatform test source sets are fixtures."""
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


# ---- (1) mod/src/intTest/projects/a/pom.xml and mod/src/intTest/projects/b/build.gradle: both dirs are fixtures
def test_src_intTest_projects_a_pom_xml_and_mod_src_intTest_projects_b_build_gradle_are_fixtures(tmp_path):
    files = {
        **ROOT,
        "core/package.json": PKG,
        "mod/src/intTest/projects/a/pom.xml": "<project/>",
        "mod/src/intTest/projects/b/build.gradle": "",
    }
    r = survey(tmp_path, files)
    # Both a and b should be fixtures with rule_id R-fx-test-project
    assert r.f["mod/src/intTest/projects/a"]["role"] == "fixture"
    assert r.f["mod/src/intTest/projects/a"]["rule_id"] == "R-fx-test-project"
    assert r.f["mod/src/intTest/projects/b"]["role"] == "fixture"
    assert r.f["mod/src/intTest/projects/b"]["rule_id"] == "R-fx-test-project"
    # Neither should be in allc
    assert "mod/src/intTest/projects/a" not in r.allc
    assert "mod/src/intTest/projects/b" not in r.allc
    # core should be in allc
    assert "core" in r.allc


# ---- (2) mod/src/functionalTest/resources/x/settings.gradle.kts plus .../x/build.gradle.kts: x is a fixture
def test_src_functionalTest_resources_x_is_a_fixture(tmp_path):
    files = {
        **ROOT,
        "core/package.json": PKG,
        "mod/src/functionalTest/resources/x/settings.gradle.kts": "",
        "mod/src/functionalTest/resources/x/build.gradle.kts": "",
    }
    r = survey(tmp_path, files)
    assert r.f["mod/src/functionalTest/resources/x"]["role"] == "fixture"
    assert r.f["mod/src/functionalTest/resources/x"]["rule_id"] == "R-fx-test-project"
    assert "mod/src/functionalTest/resources/x" not in r.allc
    assert "core" in r.allc


# ---- (3) mod/src/testKit/p/package.json: fixture
def test_src_testKit_p_package_json_is_a_fixture(tmp_path):
    files = {
        **ROOT,
        "core/package.json": PKG,
        "mod/src/testKit/p/package.json": PKG,
    }
    r = survey(tmp_path, files)
    assert r.f["mod/src/testKit/p"]["role"] == "fixture"
    assert r.f["mod/src/testKit/p"]["rule_id"] == "R-fx-test-project"
    assert "mod/src/testKit/p" not in r.allc
    assert "core" in r.allc


# ---- (4) mod/src/jvmTest/k/build.gradle.kts: fixture
def test_src_jvmTest_k_build_gradle_kts_is_a_fixture(tmp_path):
    files = {
        **ROOT,
        "core/package.json": PKG,
        "mod/src/jvmTest/k/build.gradle.kts": "",
    }
    r = survey(tmp_path, files)
    assert r.f["mod/src/jvmTest/k"]["role"] == "fixture"
    assert r.f["mod/src/jvmTest/k"]["rule_id"] == "R-fx-test-project"
    assert "mod/src/jvmTest/k" not in r.allc
    assert "core" in r.allc


# ---- (5) NEGATIVE cases: paths whose directory must stay a component
@pytest.mark.parametrize("path", [
    "mod/intTest/a/pom.xml",
    "mod/src/main/a/pom.xml",
    "mod/src/latest/a/pom.xml",
    "mod/src/contest/a/pom.xml",
    "mod/src/attest/a/pom.xml",
    "mod/src/IntTest/a/pom.xml",
    "mod/src/protest/a/pom.xml",
    "mod/src/inttest/a/pom.xml",
])
def test_negative_cases_stay_as_components(tmp_path, path):
    files = {
        **ROOT,
        "core/package.json": PKG,
        path: "<project/>",
    }
    r = survey(tmp_path, files)
    # The directory containing pom.xml should be a component
    dir_path = "/".join(path.split("/")[:-1])  # e.g., "mod/intTest/a"
    assert dir_path in r.allc
    assert r.f[dir_path]["role"] == "component"
    assert r.f[dir_path]["rule_id"] == "R-comp-pom"


# ---- (6) mod/src/testing/a/pom.xml: a fixture with rule_id R-fx-test-project
def test_src_testing_a_pom_xml_is_a_fixture(tmp_path):
    files = {
        **ROOT,
        "core/package.json": PKG,
        "mod/src/testing/a/pom.xml": "<project/>",
    }
    r = survey(tmp_path, files)
    assert r.f["mod/src/testing/a"]["role"] == "fixture"
    assert r.f["mod/src/testing/a"]["rule_id"] == "R-fx-test-project"
    assert "mod/src/testing/a" not in r.allc
    assert "core" in r.allc


# ---- (7) A project whose OWN directory is the source set: mod/src/intTest/pom.xml
def test_project_whose_own_directory_is_the_source_set(tmp_path):
    """A project directly under src/intTest (the source set directory itself has the manifest)."""
    files = {
        **ROOT,
        "core/package.json": PKG,
        "mod/src/intTest/pom.xml": "<project/>",
    }
    r = survey(tmp_path, files)
    # mod/src/intTest should be a fixture
    assert r.f["mod/src/intTest"]["role"] == "fixture"
    assert r.f["mod/src/intTest"]["rule_id"] == "R-fx-test-project"
    assert "mod/src/intTest" not in r.allc
    assert "core" in r.allc


# ---- (7b) a declared Gradle member with no manifest of its own below a source set is excluded too (the N3 member exclusion sees the same segment test)
def test_a_declared_member_without_a_manifest_below_a_source_set_is_a_fixture(tmp_path):
    files = {**ROOT, "core/package.json": PKG, "settings.gradle": "include 'core', 'mod:src:funcTest:p'\n", "mod/src/funcTest/p/src/T.java": "x"}
    r = survey(tmp_path, files)
    assert "mod/src/funcTest/p" not in r.allc and r.f["mod/src/funcTest/p"]["rule_id"] == "R-fx-test-project" and r.f["mod/src/funcTest/p"]["role"] == "fixture"
    assert "core" in r.allc


# ---- the forms the regex accepts, and testFixtures unchanged -------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("seg", ["intTest", "intTests", "dockerTest", "e2eTest", "integrationTest", "commonTest", "jvmTest", "testKit", "testFixtures", "testsSupport", "aTest"])
def test_accepted_source_set_names_make_a_fixture(tmp_path, seg):
    r = survey(tmp_path, {**ROOT, "core/package.json": PKG, f"mod/src/{seg}/p/pom.xml": "<project/>"})
    assert f"mod/src/{seg}/p" not in r.allc and r.f[f"mod/src/{seg}/p"]["rule_id"] == "R-fx-test-project"


@pytest.mark.parametrize("path", ["mod/testKit/p/pom.xml", "mod/source/intTest/p/pom.xml", "mod/Src/intTest/p/pom.xml", "mod/src/intTestx/p/pom.xml", "mod/src/int-Test/p/pom.xml",
                                  "mod/src/testkit/p/pom.xml", "mod/src/myTester/p/pom.xml", "mod/src/intTEST/p/pom.xml"])
def test_rejected_forms_stay_components(tmp_path, path):
    d = path.rsplit("/", 1)[0]
    r = survey(tmp_path, {**ROOT, "core/package.json": PKG, path: "<project/>"})
    assert d in r.allc and r.f[d]["role"] == "component"


def test_a_source_set_folder_without_a_manifest_is_not_a_finding(tmp_path):
    r = survey(tmp_path, {**ROOT, "core/package.json": PKG, "mod/src/intTest/projects/a/pom.xml": "<project/>", "mod/src/intTest/java/T.java": "x"})
    assert "mod/src/intTest" not in r.f and "mod/src/intTest" not in r.allc


# ---- (8) the finding id of an unaffected component does not change (the profile's major version is unchanged, and the id is profile@major|rule|path)
def test_finding_ids_of_unaffected_components_do_not_change(tmp_path):
    import hashlib
    files1 = {**ROOT, "core/package.json": PKG, "lib/pom.xml": "<project/>"}
    r1 = survey(tmp_path, files1, out="r1", name="tree1")
    r2 = survey(tmp_path, {**files1, "mod/src/intTest/projects/a/pom.xml": "<project/>"}, out="r2", name="tree2")
    assert load_profile("code-repo-conventions", PROFILES).major == "0"
    for d in ("core", "lib"):
        rid = r1.f[d]["rule_id"]
        assert r1.f[d]["finding_id"] == r2.f[d]["finding_id"] == hashlib.sha256(f"code-repo-conventions@0|{rid}|{d}".encode()).hexdigest()[:16]


# ---- (9) the composite profile with docs-site behaves the same
def test_the_composite_profile_with_docs_site_behaves_the_same(tmp_path):
    from recognizer.layout_profile import compose_profiles
    p = compose_profiles("code-repo-conventions,docs-site", PROFILES)
    files = {**ROOT, "core/package.json": PKG, "mod/src/dockerTest/projects/a/pom.xml": "<project/>"}
    root = tmp_path / "t"
    for rel, content in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(content)
    lst = tmp_path / "t.tsv"
    lst.write_text("".join(f"{x}\t{len(files[x].encode())}\n" for x in sorted(files)))
    Recognizer(p, blob_source=mf.FileSource(str(root))).run(lst, tmp_path / "o")
    allc = (tmp_path / "o" / "components-all.txt").read_text().split()
    assert "mod/src/dockerTest/projects/a" not in allc and "core" in allc


# ---- the loader and provenance -------------------------------------------------------------------------------------------------------------------------------------
BASE = {"profile_id": "t", "version": "0.1.0", "status": "proposed", "applies_to": "any", "roles": ["component", "fixture"],
        "relevance": {"primary": ["component"], "supporting": ["fixture"], "hidden": []}}


def prof(tmp_path, match):
    import yaml
    d = {**BASE, "rules": [{"id": "R", "match": match, "assign": {"role": "fixture"}, "grain": "dir", "basis": "convention", "confidence": "low", "evidence": "x"}]}
    (tmp_path / "t.yaml").write_text(yaml.safe_dump(d))
    return load_profile("t", tmp_path)


@pytest.mark.parametrize("bad", [{"regex": ["x"]}, {"parent": ["src"]}, {"parent": [], "regex": ["x"]}, {"parent": ["src"], "regex": []}, {"parent": ["a/b"], "regex": ["x"]},
                                 {"parent": ["src"], "regex": ["("]}, {"parent": ["src"], "regex": ["x"], "extra": 1}, "src", {"parent": [""], "regex": ["x"]}])
def test_child_segment_regex_is_validated(tmp_path, bad):
    with pytest.raises(ProfileError):
        prof(tmp_path, {"child_segment_regex": bad})


def test_child_segment_regex_alone_is_a_directory_rule_and_matches_only_under_its_parent(tmp_path):
    r = prof(tmp_path, {"child_segment_regex": {"parent": "src", "regex": "^xY$"}}).rules[0]
    assert r.is_dir_rule and r.has_segment_test
    assert r.segment_matches(["a", "src", "xY", "b"]) and r.segment_matches(["src", "xY"])
    assert not r.segment_matches(["xY", "src"]) and not r.segment_matches(["a", "xY"]) and not r.segment_matches(["a", "src", "xy"])


def test_the_f1_rule_keeps_its_id_and_carries_provenance_and_the_known_limits():
    p = load_profile("code-repo-conventions", PROFILES)
    r = {x.id: x for x in p.rules}["R-fx-test-project"]
    assert p.version == "0.8.0" and r.child_seg_parents == frozenset({"src"}) and len(r.child_seg_res) == 2 and r.role == "fixture"
    assert "spring-boot (D6, spent)" in r.tuned_on and "src/it" in r.evidence and "Multiplatform" in r.evidence
    assert all("(?i)" not in rx.pattern for rx in r.child_seg_res)   # case-sensitive
