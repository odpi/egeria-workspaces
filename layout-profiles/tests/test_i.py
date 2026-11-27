"""Phase 1i. I1: a private npm package (package.json "private": true, read) that is not the repository root is role test-support, kind private-package, not a
component, unless a segment of its path is apps, app, applications, services, sites, website or web. I1-G: an internal Gradle test project (a test word in its
name, no src/main, something besides its build files) is role fixture, kind test-project, and so is every Gradle project below it. Synthetic trees only."""
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from recognizer import manifests as mf
from recognizer.layout_profile import ProfileError, compose_profiles, load_profile
from recognizer.recognize import Recognizer

PROFILES = Path(__file__).resolve().parent.parent / "profiles"


def survey(tmp_path, files, out="out", name="tree", profile="code-repo-conventions", blobs=True):
    root = tmp_path / name
    for rel, content in files.items():
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content)
    lst = tmp_path / f"{name}.tsv"
    lst.write_text("".join(f"{p}\t{len(files[p].encode())}\n" for p in sorted(files)))
    prof = compose_profiles(profile, PROFILES) if "," in profile else load_profile(profile, PROFILES)
    rec = Recognizer(prof, blob_source=mf.FileSource(str(root)) if blobs else None)
    c = rec.run(lst, tmp_path / out)
    findings = [json.loads(x) for x in (tmp_path / out / "findings.jsonl").read_text().splitlines()]
    f = {x["path"]: x for x in findings if not x["rule_id"].startswith("F-")}
    rule = {p: (rec.classify(p)[0].id if rec.classify(p)[0] else None) for p in files}
    reads = (tmp_path / out / "manifest-reads.txt").read_text().split() if (tmp_path / out / "manifest-reads.txt").exists() else None
    return SimpleNamespace(c=c, f=f, rec=rec, rule=rule, reads=reads, findings=findings,
                           allc=(tmp_path / out / "components-all.txt").read_text().split(), top=(tmp_path / out / "components.txt").read_text().split())


PRIV = json.dumps({"name": "p", "private": True})
PUB = json.dumps({"name": "q"})
WS_ROOT = json.dumps({"name": "root", "private": True, "workspaces": ["packages/*", "private/*"]})


def not_component(r, d, rule_id, role):
    return d not in r.allc and d not in r.top and r.f[d]["rule_id"] == rule_id and r.f[d]["role"] == role


# ======================================================================== I1 ========================================================================================
# ---- (1) root workspaces [packages/*, private/*]; private/a private true: not a component, test-support
def test_a_private_workspace_package_is_test_support(tmp_path):
    r = survey(tmp_path, {"package.json": WS_ROOT, "private/a/package.json": PRIV, "private/a/src/x.ts": "x", "packages/b/package.json": PUB})
    assert not_component(r, "private/a", "R-ts-private-package", "test-support") and r.f["private/a"]["kind"] == "private-package"
    assert r.rule["private/a/src/x.ts"] == "F-source-folder" or r.rule["private/a/src/x.ts"] == "F-source-ext"


# ---- (2) packages/b without a private field: still a component
def test_a_workspace_package_without_private_is_still_a_component(tmp_path):
    r = survey(tmp_path, {"package.json": WS_ROOT, "private/a/package.json": PRIV, "packages/b/package.json": PUB})
    assert "packages/b" in r.top and r.f["packages/b"]["role"] == "component"


# ---- (3) the exempt folder names: a private application in a monorepo stays a component
@pytest.mark.parametrize("d", ["apps/web", "services/api", "app/x", "applications/x", "sites/x", "website", "web", "pkgs/web/ui", "Apps/x", "SERVICES/y"])
def test_a_private_package_under_an_exempt_folder_name_stays_a_component(tmp_path, d):
    r = survey(tmp_path, {"package.json": PUB, f"{d}/package.json": PRIV})
    assert d in r.allc and r.f[d]["role"] == "component"


@pytest.mark.parametrize("d", ["webapp/x", "my-apps/x", "frontend", "service/x", "site/x", "tools-web/x"])
def test_names_outside_the_exempt_list_are_not_exempt(tmp_path, d):
    r = survey(tmp_path, {"package.json": PUB, f"{d}/package.json": PRIV})
    assert not_component(r, d, "R-ts-private-package", "test-support")


# ---- (4) a ROOT package.json with private true changes nothing
def test_a_private_root_changes_nothing(tmp_path):
    files = {"src/a.ts": "x", "lib/package.json": PUB}
    r1 = survey(tmp_path, {**files, "package.json": json.dumps({"name": "r", "private": True})}, out="o1", name="t1")
    r2 = survey(tmp_path, {**files, "package.json": json.dumps({"name": "r"})}, out="o2", name="t2")
    assert r1.allc == r2.allc and "." in r1.allc and r1.f["."]["rule_id"] == r2.f["."]["rule_id"] == "R-comp-package-json"
    assert [{k: v for k, v in f.items() if k != "bytes"} for f in r1.findings] == [{k: v for k, v in f.items() if k != "bytes"} for f in r2.findings]   # the root file is 13 bytes longer


# ---- (5) only the boolean true counts
@pytest.mark.parametrize("value", ['"true"', "false", "1", "null", '"yes"', "[true]", '{"private": true}'])
def test_a_private_field_that_is_not_the_boolean_true_changes_nothing(tmp_path, value):
    r = survey(tmp_path, {"package.json": PUB, "x/package.json": '{"name": "x", "private": %s}' % value})
    assert "x" in r.allc and r.f["x"]["rule_id"] == "R-comp-package-json"


def test_a_nested_private_key_is_not_the_top_level_field(tmp_path):
    r = survey(tmp_path, {"package.json": PUB, "x/package.json": json.dumps({"name": "x", "publishConfig": {"private": True}})})
    assert "x" in r.allc


# ---- (6) a private package that is not a workspace member (no root workspaces): also not a component
def test_a_private_package_outside_any_workspace_is_test_support(tmp_path):
    r = survey(tmp_path, {"harness/package.json": PRIV, "harness/run.js": "x", "core/pyproject.toml": "[project]\nname='c'\n"})
    assert not_component(r, "harness", "R-ts-private-package", "test-support") and "core" in r.allc


def test_a_private_package_without_a_name_is_still_read(tmp_path):
    r = survey(tmp_path, {"package.json": PUB, "x/package.json": '{"private": true}'})
    assert not_component(r, "x", "R-ts-private-package", "test-support")


# ---- (iii) its files keep their file roles (a file-role scope), also without a root component
def test_the_files_of_a_private_package_keep_their_roles(tmp_path):
    files = {"core/pyproject.toml": "[project]\nname='c'\n", "harness/run.js": "x", "harness/.eslintrc": "{}"}
    r1 = survey(tmp_path, {**files, "harness/package.json": PUB}, out="o1", name="t1")
    r2 = survey(tmp_path, {**files, "harness/package.json": PRIV}, out="o2", name="t2")
    assert "harness" in r1.allc and "harness" not in r2.allc
    assert r1.rule == r2.rule and r2.rule["harness/run.js"] == "F-source-ext" and r2.rule["harness/.eslintrc"] == "F-config-component-dotfile"


# ---- a private workspace ROOT below the repository root (it declares workspaces) stays an aggregator: it was not a component already
def test_a_private_aggregator_stays_an_aggregator(tmp_path):
    r = survey(tmp_path, {"mono/package.json": json.dumps({"name": "m", "private": True, "workspaces": ["packages/*"]}), "mono/packages/a/package.json": PUB})
    assert r.f["mono"]["rule_id"] == "M-aggregator" and "mono/packages/a" in r.top


# ---- without manifest reading (names and sizes only) the rule never applies
def test_without_manifest_reading_nothing_changes(tmp_path):
    r = survey(tmp_path, {"package.json": PUB, "x/package.json": PRIV}, blobs=False)
    assert "x" in r.allc and r.f["x"]["rule_id"] == "R-comp-package-json"


# ---- no new file is opened: the package.json files were read before I1 too
def test_the_read_log_is_unchanged(tmp_path):
    files = {"package.json": WS_ROOT, "private/a/package.json": PRIV, "packages/b/package.json": PUB, "x/Cargo.toml": "[package]\nname='x'\n"}
    r = survey(tmp_path, files)
    assert r.reads == ["package.json", "x/Cargo.toml", "packages/b/package.json", "private/a/package.json"]


@pytest.mark.parametrize("text,want", [('{"private": true}', True), ('{"name": "a", "private": true}', True), ('{"name": "a", "private": "true"}', False),
                                       ('{"name": "a", "private": false}', False), ('{"name": "a", "private": 1}', False), ('{"name": "a"}', False)])
def test_the_reader_records_private_as_a_boolean_only(text, want):
    d = mf.extract("package-json", "x/package.json", text.encode())
    assert d is not None and d.private is want


def test_the_reader_still_returns_nothing_for_a_package_json_that_says_nothing():
    assert mf.extract("package-json", "x/package.json", b'{"version": "1", "private": false}') is None


# ---- (7) unaffected finding ids do not change
def test_i1_leaves_finding_ids_of_unaffected_components_unchanged(tmp_path):
    files1 = {"package.json": PUB, "lib/pom.xml": "<project/>", "core/pyproject.toml": "[project]\nname='c'\n"}
    r1 = survey(tmp_path, files1, out="r1", name="tree1")
    r2 = survey(tmp_path, {**files1, "harness/package.json": PRIV, "gen-test/build.gradle": "", "gen-test/model/a.smithy": "x"}, out="r2", name="tree2")
    assert load_profile("code-repo-conventions", PROFILES).major == "0"
    for d in ("core", "lib"):
        rid = r1.f[d]["rule_id"]
        assert r1.f[d]["finding_id"] == r2.f[d]["finding_id"] == hashlib.sha256(f"code-repo-conventions@0|{rid}|{d}".encode()).hexdigest()[:16]


def test_i1_in_the_composite_profile(tmp_path):
    r = survey(tmp_path, {"package.json": PUB, "harness/package.json": PRIV, "apps/web/package.json": PRIV}, profile="code-repo-conventions,docs-site")
    assert not_component(r, "harness", "R-ts-private-package", "test-support") and "apps/web" in r.allc


# ======================================================================== I1-G ======================================================================================
ROOT_G = {"build.gradle": "", "settings.gradle": "rootProject.name = 'r'\n"}


# ---- (1) x-codegen-test/build.gradle.kts + model/a.smithy: fixture, not a component
def test_a_codegen_test_project_is_a_fixture(tmp_path):
    r = survey(tmp_path, {**ROOT_G, "x-codegen-test/build.gradle.kts": "", "x-codegen-test/model/a.smithy": "x"})
    assert not_component(r, "x-codegen-test", "R-fx-gradle-test-project", "fixture") and r.f["x-codegen-test"]["kind"] == "test-project"


# ---- (2) x-protocol-test-codegen/build.gradle.kts + smithy-build.json: fixture
def test_a_test_word_in_the_middle_of_the_name_counts(tmp_path):
    r = survey(tmp_path, {**ROOT_G, "x-protocol-test-codegen/build.gradle.kts": "", "x-protocol-test-codegen/smithy-build.json": "{}"})
    assert not_component(r, "x-protocol-test-codegen", "R-fx-gradle-test-project", "fixture")


# ---- (3) a project nested in (1), with its own src/main: fixture
def test_a_gradle_project_nested_below_a_test_project_is_a_fixture(tmp_path):
    r = survey(tmp_path, {**ROOT_G, "x-codegen-test/build.gradle.kts": "", "x-codegen-test/model/a.smithy": "x",
                          "x-codegen-test/inner/build.gradle.kts": "", "x-codegen-test/inner/src/main/java/A.java": "x",
                          "x-codegen-test/a/b/core/build.gradle": "", "x-codegen-test/a/b/core/src/main/java/B.java": "x"})
    for d in ("x-codegen-test/inner", "x-codegen-test/a/b/core"):
        assert not_component(r, d, "R-fx-gradle-test-project", "fixture")


# ---- (4) a starter that is ONLY its build file(s): still a component
@pytest.mark.parametrize("extra", [{}, {"starter/x-starter-test/gradle.properties": "", "starter/x-starter-test/settings.gradle.kts": ""}])
def test_a_build_file_only_test_project_stays_a_component(tmp_path, extra):
    r = survey(tmp_path, {**ROOT_G, "starter/x-starter-test/build.gradle": "", **extra})
    assert "starter/x-starter-test" in r.allc and r.f["starter/x-starter-test"]["role"] == "component"


# ---- (5) x-test/build.gradle + src/main/java/A.java: still a component (a published test library)
def test_a_test_library_with_src_main_stays_a_component(tmp_path):
    r = survey(tmp_path, {**ROOT_G, "x-test/build.gradle": "", "x-test/src/main/java/A.java": "x", "x-test/src/test/java/T.java": "x"})
    assert "x-test" in r.allc and r.f["x-test"]["role"] == "component"


def test_a_test_project_with_only_src_test_is_a_fixture(tmp_path):
    r = survey(tmp_path, {**ROOT_G, "x-test/build.gradle": "", "x-test/src/test/java/T.java": "x"})
    assert not_component(r, "x-test", "R-fx-gradle-test-project", "fixture")


# ---- (6) x-test-utils with src/main: still a component (known limit)
def test_a_test_utils_library_with_src_main_stays_a_component(tmp_path):
    r = survey(tmp_path, {**ROOT_G, "x-test-utils/build.gradle": "", "x-test-utils/src/main/kotlin/U.kt": "x"})
    assert "x-test-utils" in r.allc and r.f["x-test-utils"]["role"] == "component"


# ---- (7) test inside a word: unchanged
@pytest.mark.parametrize("d", ["contest", "attestation", "latest-x", "x-testkit", "x-tested", "testx", "x.test"])
def test_test_inside_a_word_is_not_matched(tmp_path, d):
    r = survey(tmp_path, {**ROOT_G, f"{d}/build.gradle": "", f"{d}/model/a.smithy": "x"})
    assert d in r.allc and r.f[d]["role"] == "component"


@pytest.mark.parametrize("d", ["x_test", "X-Codegen-TEST", "x-tests-codegen", "x-testing", "a_b-test-c"])
def test_every_separator_and_case_counts(tmp_path, d):
    r = survey(tmp_path, {**ROOT_G, f"pkg/{d}/build.gradle": "", f"pkg/{d}/model/a.smithy": "x"})
    assert not_component(r, f"pkg/{d}", "R-fx-gradle-test-project", "fixture")


# ---- (8) the existing test-folder rules keep precedence; a folder that is not itself a Gradle project is untouched
def test_a_top_level_grouping_test_folder_without_its_own_build_file_is_unchanged(tmp_path):
    r = survey(tmp_path, {**ROOT_G, "foo-test/a/build.gradle": "", "foo-test/a/x.txt": "x", "foo-test/b/build.gradle": "", "foo-test/b/y.txt": "x"})
    assert r.f["foo-test"]["rule_id"] == "R-conv-test-group" and "foo-test" in r.top
    assert r.f["foo-test/a"]["rule_id"] == "R-fx-test-group-project" and r.f["foo-test/b"]["rule_id"] == "R-fx-test-group-project"


@pytest.mark.parametrize("d,rid", [("tests/x", "R-fx-test-project"), ("test-x", "R-fx-test-project"), ("x-tests", "R-conv-tests"),
                                   ("samples/x-test", "R-fx-sample-project"), ("x-test-bench", "R-fx-benchmark-project")])
def test_the_earlier_rules_keep_precedence(tmp_path, d, rid):
    r = survey(tmp_path, {**ROOT_G, f"{d}/build.gradle": "", f"{d}/model/a.smithy": "x"})
    assert r.f[d]["rule_id"] == rid


def test_a_test_named_folder_without_a_build_file_is_untouched(tmp_path):
    r = survey(tmp_path, {**ROOT_G, "x-codegen-test/model/a.smithy": "x", "x-codegen-test/pom.xml": "<project/>"})
    assert r.f["x-codegen-test"]["rule_id"] == "R-comp-pom"


def test_the_repository_root_is_never_a_test_project(tmp_path):
    r = survey(tmp_path, {"build.gradle": "", "model/a.smithy": "x"}, name="x-codegen-test")
    assert "." in r.allc


def test_its_files_keep_their_roles(tmp_path):
    files = {"core/pyproject.toml": "[project]\nname='c'\n", "x-codegen-test/build.gradle.kts": "", "x-codegen-test/gen.kt": "x", "x-codegen-test/.gitignore": "x"}
    r = survey(tmp_path, files)
    assert "x-codegen-test" not in r.allc and r.rule["x-codegen-test/gen.kt"] == "F-source-ext" and r.rule["x-codegen-test/.gitignore"] == "F-config-component-dotfile"


def test_a_declared_gradle_member_is_claimed_by_the_rule_not_the_member_rule(tmp_path):
    r = survey(tmp_path, {**ROOT_G, "settings.gradle": "include 'x-codegen-test'\n", "x-codegen-test/build.gradle.kts": "", "x-codegen-test/model/a.smithy": "x"})
    assert not_component(r, "x-codegen-test", "R-fx-gradle-test-project", "fixture")


def test_names_only_runs_apply_i1g_too(tmp_path):
    r = survey(tmp_path, {**ROOT_G, "x-codegen-test/build.gradle.kts": "", "x-codegen-test/model/a.smithy": "x"}, blobs=False)
    assert not_component(r, "x-codegen-test", "R-fx-gradle-test-project", "fixture")


# ---- (9) unaffected finding ids do not change: see test_i1_leaves_finding_ids_of_unaffected_components_unchanged (gen-test there)
def test_the_i1_rules_carry_provenance_and_the_known_limits():
    p = load_profile("code-repo-conventions", PROFILES)
    by = {x.id: x for x in p.rules}
    ids = [x.id for x in p.rules]
    g, t = by["R-fx-gradle-test-project"], by["R-ts-private-package"]
    assert p.version == "0.10.0" and load_profile("code-repo", PROFILES).version == "0.5.0"
    assert g.role == "fixture" and g.kind == "test-project" and g.grain == "dir" and g.file_scope and "Known limits" in g.evidence
    assert t.role == "test-support" and t.kind == "private-package" and t.grain == "dir" and t.file_scope and "Known limits" in t.evidence
    assert any(x.startswith("Phase 1i I1-G") for x in g.tuned_on) and any(x.startswith("Phase 1i I1 ") for x in t.tuned_on)
    assert ids.index("R-fx-benchmark-project") < ids.index("R-fx-gradle-test-project") < ids.index("R-conv-docs")
    assert ids.index("R-ts-private-package") < ids.index("R-comp-package-json") and ids.index("R-fx-gradle-test-project") < ids.index("R-comp-gradle")
    assert t.not_segments == frozenset({"apps", "app", "applications", "services", "sites", "website", "web"})
    assert g.tp_words == frozenset({"test", "tests", "testing"}) and g.tp_not_child == "src/main"
    assert g.tp_other_than == frozenset({"build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts", "gradle.properties"})


# ---- loader validation
def _prof(tmp_path, rule):
    import yaml
    base = {"profile_id": "t", "version": "0.1.0", "status": "proposed", "applies_to": "any", "roles": ["component", "fixture", "test-support"],
            "relevance": {"primary": ["component"], "supporting": ["fixture", "test-support"], "hidden": []}}
    (tmp_path / "t.yaml").write_text(yaml.safe_dump({**base, "rules": [{"id": "R", "basis": "convention", "confidence": "low", "evidence": "x", **rule}]}))
    return load_profile("t", tmp_path)


TP = {"name_words": ["test"], "not_child_dir": "src/main", "other_than": ["build.gradle"]}


@pytest.mark.parametrize("match", [
    {"has_file": "package.json", "manifest_private": False},
    {"has_file": "package.json", "manifest_private": "yes"},
    {"has_file": "package.json", "not_path_segment": []},
    {"has_file": "package.json", "not_path_segment": ["a/b"]},
    {"has_file": "build.gradle", "test_project": {**TP, "extra": 1}},
    {"has_file": "build.gradle", "test_project": {"name_words": ["test"], "not_child_dir": "src/main"}},
    {"has_file": "build.gradle", "test_project": {**TP, "name_words": []}},
    {"has_file": "build.gradle", "test_project": {**TP, "name_words": ["a-b"]}},
    {"has_file": "build.gradle", "test_project": {**TP, "not_child_dir": "/src"}},
    {"has_file": "build.gradle", "test_project": {**TP, "not_child_dir": "../x"}},
    {"has_file": "build.gradle", "test_project": {**TP, "other_than": []}},
    {"has_file": "build.gradle", "test_project": "yes"},
])
def test_the_new_keys_are_validated(tmp_path, match):
    with pytest.raises(ProfileError):
        _prof(tmp_path, {"match": match, "assign": {"role": "fixture"}, "grain": "dir"})


def test_the_new_keys_load(tmp_path):
    r = _prof(tmp_path, {"match": {"has_file": "build.gradle", "test_project": TP}, "assign": {"role": "fixture"}, "grain": "dir"}).rules[0]
    assert r.test_project and r.is_dir_rule and r.tp_words == frozenset({"test"})
    r = _prof(tmp_path, {"match": {"has_file": "package.json", "manifest_private": True, "not_path_segment": ["Apps"]}, "assign": {"role": "test-support"},
                         "grain": "dir"}).rules[0]
    assert r.manifest_private and r.not_segments == frozenset({"apps"}) and r.is_dir_rule


# ======================================================================== I2 ========================================================================================
I2_NAMES = ["testbed", "testbeds", "test-bed", "test_bed", "e2e", "end-to-end", "end2end", "itest", "itests"]
PY_ROOT = {"pyproject.toml": "[project]\nname='r'\n"}


# ---- (1) testbed/x + testbed/y: testbed is one test-suite component; x and y are fixtures
def test_a_testbed_folder_is_one_test_suite_and_its_projects_are_fixtures(tmp_path):
    r = survey(tmp_path, {**PY_ROOT, "testbed/x/package.json": PUB, "testbed/y/package.json": PUB})
    assert r.f["testbed"]["rule_id"] == "R-conv-tests" and r.f["testbed"]["kind"] == "test-suite" and "testbed" in r.top
    for d in ("testbed/x", "testbed/y"):
        assert not_component(r, d, "R-fx-test-project", "fixture")


# ---- (2) e2e/ with test files and no manifest: a test-suite component
def test_an_e2e_folder_without_a_manifest_is_a_test_suite(tmp_path):
    r = survey(tmp_path, {**PY_ROOT, "e2e/login.spec.ts": "x", "e2e/cart.spec.ts": "x"})
    assert "e2e" in r.top and r.f["e2e"]["rule_id"] == "R-conv-tests"


@pytest.mark.parametrize("name", I2_NAMES + ["TestBed", "E2E", "End-To-End", "ITests"])
def test_every_new_name_is_a_top_level_test_suite(tmp_path, name):
    r = survey(tmp_path, {**PY_ROOT, f"{name}/a.py": "x"})
    assert name in r.top and r.f[name]["rule_id"] == "R-conv-tests"


@pytest.mark.parametrize("name", I2_NAMES + ["TestBed", "E2E"])
def test_every_new_name_makes_a_manifest_project_below_it_a_fixture_at_any_depth(tmp_path, name):
    r = survey(tmp_path, {**PY_ROOT, f"pkg/{name}/p/package.json": PUB})
    assert not_component(r, f"pkg/{name}/p", "R-fx-test-project", "fixture")


# ---- (3) NOT matched: testbedding/, e2etools/; src/e2e is not a top-level test suite
@pytest.mark.parametrize("name", ["testbedding", "e2etools", "my-e2e", "e2e-utils", "itesting", "end2ending", "pre-testbed"])
def test_other_names_are_not_test_folders(tmp_path, name):
    r = survey(tmp_path, {**PY_ROOT, f"{name}/a.py": "x", f"{name}/p/package.json": PUB})
    assert r.f.get(name, {}).get("rule_id") != "R-conv-tests" and f"{name}/p" in r.allc


def test_src_e2e_is_not_a_test_suite_but_a_manifest_project_in_it_is_a_fixture(tmp_path):
    # R-conv-tests is top level only: src/e2e itself is no test-suite component. The R-fx-test-project segment rule applies below it, and to src/e2e
    # itself, only where there is a manifest project.
    r1 = survey(tmp_path, {**PY_ROOT, "src/e2e/a.spec.ts": "x"}, out="o1", name="t1")
    assert "src/e2e" not in r1.f and "src/e2e" not in r1.allc
    r2 = survey(tmp_path, {**PY_ROOT, "src/e2e/x/package.json": PUB, "src/e2e/package.json": PUB}, out="o2", name="t2")
    assert not_component(r2, "src/e2e/x", "R-fx-test-project", "fixture") and not_component(r2, "src/e2e", "R-fx-test-project", "fixture")


def test_an_e2e_folder_with_its_own_manifest_is_a_test_suite_not_a_package(tmp_path):
    r = survey(tmp_path, {**PY_ROOT, "e2e/package.json": PUB, "e2e/a.spec.ts": "x"})
    assert r.f["e2e"]["rule_id"] == "R-conv-tests" and "e2e" in r.top


# ---- (4) unaffected finding ids do not change
def test_i2_leaves_finding_ids_of_unaffected_components_unchanged(tmp_path):
    files1 = {**PY_ROOT, "lib/pom.xml": "<project/>", "core/pyproject.toml": "[project]\nname='c'\n", "tests/a.py": "x"}
    r1 = survey(tmp_path, files1, out="r1", name="tree1")
    r2 = survey(tmp_path, {**files1, "testbed/x/package.json": PUB, "e2e/a.ts": "x"}, out="r2", name="tree2")
    for d in ("core", "lib", "tests"):
        rid = r1.f[d]["rule_id"]
        assert r1.f[d]["finding_id"] == r2.f[d]["finding_id"] == hashlib.sha256(f"code-repo-conventions@0|{rid}|{d}".encode()).hexdigest()[:16]


def test_the_two_rules_carry_the_same_closed_list():
    p = load_profile("code-repo-conventions", PROFILES)
    by = {x.id: x for x in p.rules}
    (tests_rx,) = by["R-conv-tests"].name_res
    fx_rx = by["R-fx-test-project"].segment_res[0]
    for n in I2_NAMES:
        assert tests_rx.search(n) and fx_rx.search(n)
    assert any(t.startswith("Phase 1i I2") for t in by["R-conv-tests"].tuned_on) and any(t.startswith("Phase 1i I2") for t in by["R-fx-test-project"].tuned_on)


# ======================================================================== I3 ========================================================================================
GRADLE_ROOT = {"build.gradle": "", "settings.gradle": "rootProject.name = 'r'\n", "src/main/java/A.java": "x"}


def is_doc_component(r, d):
    return d in r.top and r.f[d]["rule_id"] == "R-conv-src-docs" and r.f[d]["role"] == "component" and r.f[d]["kind"] == "documentation"


# ---- (1) src/main/docs/guide/a.adoc + b.adoc + toc.yml: src/main/docs is a documentation component (not guide/)
def test_a_guide_under_src_main_docs_is_a_documentation_component(tmp_path):
    r = survey(tmp_path, {**GRADLE_ROOT, "src/main/docs/guide/a.adoc": "x", "src/main/docs/guide/b.adoc": "x", "src/main/docs/guide/toc.yml": "x"})
    assert is_doc_component(r, "src/main/docs") and "src/main/docs/guide" not in r.allc and "src/main/docs/guide" not in r.f


# ---- (2) src/docs/asciidoc/index.adoc + one more .adoc: src/docs is a component
def test_src_docs_is_a_documentation_component(tmp_path):
    r = survey(tmp_path, {**GRADLE_ROOT, "src/docs/asciidoc/index.adoc": "x", "src/docs/asciidoc/usage.adoc": "x"})
    assert is_doc_component(r, "src/docs") and "src/docs/asciidoc" not in r.allc


def test_a_site_config_in_a_direct_child_folder_is_enough(tmp_path):
    r = survey(tmp_path, {**GRADLE_ROOT, "src/docs/site/antora.yml": "x", "src/docs/site/x.png": "x"})
    assert is_doc_component(r, "src/docs")


# ---- (3) src/main/docs/one.adoc alone: not a component (min_content)
@pytest.mark.parametrize("files", [{"src/main/docs/one.adoc": "x"}, {"src/docs/a.png": "x", "src/docs/b.css": "x"}])
def test_too_little_content_is_not_a_component(tmp_path, files):
    r = survey(tmp_path, {**GRADLE_ROOT, **files})
    d = "/".join(next(iter(files)).split("/")[:-1])
    assert d not in r.allc and d not in r.f


# ---- (4) inside a sub-project: unchanged
@pytest.mark.parametrize("d", ["module/src/main/docs", "module/src/docs", "src/main/other/docs", "docs/src/docs", "src/test/docs"])
def test_a_docs_folder_elsewhere_is_unchanged(tmp_path, d):
    r = survey(tmp_path, {**GRADLE_ROOT, "module/build.gradle": "", f"{d}/a.adoc": "x", f"{d}/b.adoc": "x"})
    assert r.f.get(d, {}).get("rule_id") != "R-conv-src-docs" and d not in r.allc


def test_the_files_keep_their_roles(tmp_path):
    files = {**GRADLE_ROOT, "src/main/docs/guide/a.adoc": "x", "src/main/docs/guide/b.md": "x"}
    r = survey(tmp_path, files)
    assert r.rule["src/main/docs/guide/a.adoc"] == "F-source-folder" and r.rule["src/main/docs/guide/b.md"] == "F-docs-markup-anywhere"


# ---- (5) unaffected finding ids do not change
def test_i3_leaves_finding_ids_of_unaffected_components_unchanged(tmp_path):
    files1 = {**GRADLE_ROOT, "lib/pom.xml": "<project/>", "core/pyproject.toml": "[project]\nname='c'\n", "docs/a.md": "x", "docs/b.md": "x"}
    r1 = survey(tmp_path, files1, out="r1", name="tree1")
    r2 = survey(tmp_path, {**files1, "src/main/docs/a.adoc": "x", "src/main/docs/b.adoc": "x"}, out="r2", name="tree2")
    assert is_doc_component(r2, "src/main/docs")
    for d in ("core", "lib", "docs"):
        rid = r1.f[d]["rule_id"]
        assert r1.f[d]["finding_id"] == r2.f[d]["finding_id"] == hashlib.sha256(f"code-repo-conventions@0|{rid}|{d}".encode()).hexdigest()[:16]


def test_i3_in_the_composite_profile(tmp_path):
    r = survey(tmp_path, {**GRADLE_ROOT, "src/main/docs/a.adoc": "x", "src/main/docs/b.adoc": "x"}, profile="code-repo-conventions,docs-site")
    assert is_doc_component(r, "src/main/docs")


def test_the_i3_rule_uses_the_same_minimum_content_as_r_conv_docs():
    p = load_profile("code-repo-conventions", PROFILES)
    by = {x.id: x for x in p.rules}
    a, b = by["R-conv-docs"], by["R-conv-src-docs"]
    assert (a.content_files, a.content_min, a.content_exts) == (b.content_files, b.content_min, b.content_exts)
    assert [g.pattern for g in b.globs] == ["^src/docs$", "^src/main/docs$"] and b.grain == "component" and b.basis == "convention"
    assert any(t.startswith("Phase 1i I3") for t in b.tuned_on) and "Known limit" in b.evidence
