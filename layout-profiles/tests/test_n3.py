"""N3 (Phase 1c): fixture, sample, template and tooling exclusion, by GENERAL segment lists (Dan's key principle). A manifest project whose path has a test, sample, template
or demo segment is a fixture or an example (kind sample-project) and not a component; a package under a tooling segment is tooling and not a component. A top-level test
folder keeps its convention component (kind test-suite); only the manifest projects inside it are excluded. Synthetic only."""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from recognizer import manifests as mf
from recognizer.layout_profile import ProfileError, load_profile, parse_profile
from recognizer.recognize import Recognizer

PROFILES = Path(__file__).resolve().parent.parent / "profiles"


def run(tmp_path, rows, out="out", extra=None):
    lst = tmp_path / f"{out}.tsv"
    lst.write_text("".join(f"{r}\n" for r in sorted(set(rows))))
    c = Recognizer(load_profile("code-repo-conventions", PROFILES)).run(lst, tmp_path / out)
    f = [json.loads(x) for x in (tmp_path / out / "findings.jsonl").read_text().splitlines()]
    by = {x["path"]: x for x in f if not x["rule_id"].startswith("F-")}
    return SimpleNamespace(c=c, by=by, allc=(tmp_path / out / "components-all.txt").read_text().split(), comps=(tmp_path / out / "components.txt").read_text().split())


def proj(*paths):
    return ["real/pyproject.toml"] + [p.rstrip("/") + "/package.json" for p in paths]


# ---- (a) fixtures, samples, templates, demos --------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("seg", ["test", "tests", "testing", "__tests__", "testFixtures", "fixture", "fixtures", "testdata", "test-data", "TESTS", "Fixtures"])
def test_a_manifest_project_under_a_test_or_fixture_segment_is_a_fixture(tmp_path, seg):
    p = f"real/{seg}/proj"
    r = run(tmp_path, proj(p))
    assert r.by[p]["role"] == "fixture" and r.by[p]["kind"] == "sample-project" and r.by[p]["rule_id"] == "R-fx-test-project"
    assert p not in r.allc and "real" in r.allc


@pytest.mark.parametrize("seg", ["sample", "samples", "example", "examples", "template", "templates", "demo", "demos", "Examples", "TEMPLATES"])
def test_a_manifest_project_under_a_sample_template_or_demo_segment_is_an_example(tmp_path, seg):
    p = f"real/{seg}/proj"
    r = run(tmp_path, proj(p))
    assert r.by[p]["role"] == "example" and r.by[p]["kind"] == "sample-project" and r.by[p]["rule_id"] == "R-fx-sample-project" and p not in r.allc


@pytest.mark.parametrize("seg", ["unit_tests", "e2e-tests", "Integration_Tests", "smoke-tests"])
def test_a_segment_ending_in_the_plural_tests_after_an_underscore_or_hyphen_counts(tmp_path, seg):
    p = f"real/{seg}/proj"
    assert run(tmp_path, proj(p)).by[p]["role"] == "fixture"


@pytest.mark.parametrize("seg", ["unit_test", "smoke-test", "legacy-plugin-chart-paired-t-test", "e2e_test", "latest", "contest", "attest", "testing-tools-x", "tester", "protests", "my-testbed", "tests-and-more", "sampler", "exampled", "demonstration"])
def test_whole_segments_only_and_the_singular_test_suffix_does_not_count(tmp_path, seg):
    p = f"real/{seg}/proj"
    r = run(tmp_path, proj(p))
    assert r.by[p]["rule_id"] == "R-comp-package-json" and p in r.allc


def test_the_projects_own_directory_name_counts_and_a_directory_without_a_manifest_is_untouched(tmp_path):
    r = run(tmp_path, ["real/pyproject.toml", "real/pkg-tests/package.json", "real/tests/helpers/util.py", "real/samples/readme.md"])
    assert r.by["real/pkg-tests"]["role"] == "fixture"
    assert "real/tests/helpers" not in r.by and "real/samples" not in r.by                 # no manifest: not a project, so nothing to exclude


# ---- the top-level test folder exception ------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("name", ["tests", "test", "testing", "__tests__", "integration_tests", "smoke-tests", "unit-tests"])
def test_a_top_level_test_folder_keeps_or_gets_its_convention_component(tmp_path, name):
    r = run(tmp_path, ["pyproject.toml", f"{name}/helper.py", f"{name}/pyproject.toml", f"{name}/inner/package.json"])
    assert r.by[name]["rule_id"] == "R-conv-tests" and r.by[name]["kind"] == "test-suite" and r.by[name]["role"] == "component" and name in r.allc
    assert r.by[f"{name}/inner"]["role"] == "fixture" and f"{name}/inner" not in r.allc            # only the manifest projects INSIDE it are excluded


def test_the_exception_is_for_top_level_test_folders_only(tmp_path):
    r = run(tmp_path, ["pyproject.toml", "pkg/tests/pyproject.toml", "pkg/pyproject.toml"])
    assert r.by["pkg/tests"]["role"] == "fixture" and "pkg/tests" not in r.allc


@pytest.mark.parametrize("name", ["examples", "templates", "samples", "demo", "fixtures", "testdata"])
def test_top_level_examples_templates_and_data_folders_are_not_components(tmp_path, name):
    r = run(tmp_path, ["pyproject.toml", f"{name}/pyproject.toml", f"{name}/p/package.json", f"{name}/readme.md"])
    assert name not in r.allc and f"{name}/p" not in r.allc
    assert r.by[name]["role"] in ("example", "fixture") and r.by[name]["kind"] == "sample-project"


# ---- (b) tooling -----------------------------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("seg", ["tools", "tooling", "devtools", "dev-tools", "build-tools", "buildSrc", "_ext", "ci", ".ci", ".github", ".buildkite", ".circleci", "scripts", "TOOLS", "BuildSrc"])
def test_a_package_under_a_tooling_segment_is_tooling_and_not_a_component(tmp_path, seg):
    p = f"real/{seg}/pkg"
    r = run(tmp_path, proj(p))
    assert r.by[p]["role"] == "tooling" and r.by[p]["kind"] == "tooling-package" and r.by[p]["rule_id"] == "R-tool-package" and p not in r.allc


def test_the_top_level_scripts_folder_keeps_its_convention_component_but_a_package_inside_it_is_tooling(tmp_path):
    r = run(tmp_path, ["pyproject.toml", "scripts/run.sh", "scripts/pyproject.toml", "scripts/helper/package.json"])
    assert r.by["scripts"]["rule_id"] == "R-conv-scripts" and "scripts" in r.allc and r.by["scripts/helper"]["role"] == "tooling"


@pytest.mark.parametrize("seg", ["toolbox", "tools-x", "scriptsx", "cisco", "ci-cd", "githubs", "automation", "kitchen-sink"])
def test_other_names_are_not_tooling_segments(tmp_path, seg):
    p = f"real/{seg}/pkg"
    assert run(tmp_path, proj(p)).by[p]["rule_id"] == "R-comp-package-json"


# ---- members declared by a manifest follow the same principle -------------------------------------------------------------------------------------------
def test_a_declared_member_under_such_a_segment_is_excluded_too(tmp_path):
    root = tmp_path / "t"
    files = {"settings.gradle": "include 'app', 'app:tests:it', 'app:tools:gen'\n", "build.gradle": "x", "app/build.gradle": "x", "app/tests/it/A.java": "x", "app/tools/gen/B.java": "x"}
    for rel, c in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(c)
    lst = tmp_path / "t.tsv"
    lst.write_text("".join(f"{p}\t{len(files[p])}\n" for p in sorted(files)))
    Recognizer(load_profile("code-repo-conventions", PROFILES), blob_source=mf.FileSource(str(root))).run(lst, tmp_path / "o")
    by = {x["path"]: x for x in map(json.loads, (tmp_path / "o" / "findings.jsonl").read_text().splitlines())}
    allc = (tmp_path / "o" / "components-all.txt").read_text().split()
    assert "app" in allc and "app/tests/it" not in allc and "app/tools/gen" not in allc
    assert by["app/tests/it"]["role"] == "fixture" and by["app/tools/gen"]["role"] == "tooling"


# ---- the lists themselves ----------------------------------------------------------------------------------------------------------------------------------
def test_no_segment_list_contains_a_name_from_a_held_out_or_spent_repository():
    p = load_profile("code-repo-conventions", PROFILES)
    text = " ".join(rx.pattern.lower() for r in p.rules for rx in r.segment_res + r.name_res) + " " + " ".join(s.lower() for r in p.rules for s in r.segments)
    for banned in ("automation", "kitchen-sink", "kitchen", "sample-repos", "cypress", "eslint-plugin", "eslint"):
        assert banned not in text, banned


def test_the_new_rules_carry_their_provenance_and_the_test_folder_rule_comes_first():
    p = load_profile("code-repo-conventions", PROFILES)
    ids = [r.id for r in p.rules]
    assert p.version == "0.4.0" and ids.index("R-conv-tests") < ids.index("R-fx-test-project") < ids.index("R-fx-sample-project") < ids.index("R-conv-docs")
    assert ids.index("R-conv-scripts") < ids.index("R-tool-package")                                                   # the top-level scripts folder keeps its component
    by = {r.id: r for r in p.rules}
    for rid in ("R-fx-test-project", "R-fx-sample-project", "R-tool-package"):
        assert by[rid].evidence and by[rid].tuned_on and by[rid].relevance == "supporting" and by[rid].grain == "dir"
    assert "iceberg (M8, spent)" in by["R-fx-test-project"].tuned_on and "dagster (M8, spent)" in by["R-fx-sample-project"].tuned_on


def test_segment_regex_is_validated_and_fixture_is_a_known_role():
    base = {"profile_id": "t", "version": "0.1.0", "status": "proposed", "applies_to": "any", "roles": ["fixture"], "relevance": {"primary": [], "supporting": ["fixture"], "hidden": []},
            "rules": [{"id": "R-x", "match": {"segment_regex": ["(?i)^tests?$"], "has_file": "package.json"}, "assign": {"role": "fixture"}, "grain": "dir", "basis": "convention",
                       "confidence": "low", "evidence": "e"}]}
    assert parse_profile(base).rules[0].segment_res[0].search("Tests")
    for bad in (["("], [""], [3]):
        d = json.loads(json.dumps(base))
        d["rules"][0]["match"]["segment_regex"] = bad
        with pytest.raises(ProfileError):
            parse_profile(d)
