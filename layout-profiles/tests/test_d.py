"""Phase 1d (D1 to D4): a test word with a version or number tail, test-/tests- prefixes, includeBuild as internal tooling, and benchmark harnesses as test support. Synthetic only.
Known limits (kept by Dan, stated in the README): a PUBLISHED test library named test-* is excluded; a composite build that includes a real product build is mis-classed;
`tools` stays an internal-tooling segment."""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from recognizer import manifests as mf
from recognizer.layout_profile import load_profile
from recognizer.recognize import Recognizer

PROFILES = Path(__file__).resolve().parent.parent / "profiles"


def survey(tmp_path, files, out="out", name="tree", source=True):
    root = tmp_path / name
    for rel, content in files.items():
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content)
    lst = tmp_path / f"{name}.tsv"
    lst.write_text("".join(f"{p}\t{len(files[p].encode())}\n" for p in sorted(files)))

    class Rec:
        def __init__(self):
            self.inner, self.asked = mf.FileSource(str(root)), []

        def read(self, path, mx):
            self.asked.append(path)
            return self.inner.read(path, mx)

        def close(self):
            pass
    src = Rec() if source else None
    rec = Recognizer(load_profile("code-repo-conventions", PROFILES), blob_source=src)
    c = rec.run(lst, tmp_path / out)
    f = {x["path"]: x for x in map(json.loads, (tmp_path / out / "findings.jsonl").read_text().splitlines()) if not x["rule_id"].startswith("F-")}
    return SimpleNamespace(c=c, f=f, rec=rec, src=src, allc=(tmp_path / out / "components-all.txt").read_text().split())


def one(tmp_path, seg, out="o"):
    p = f"real/{seg}/proj"
    r = survey(tmp_path, {"real/pyproject.toml": "[project]\nname='r'\n", f"{p}/package.json": "{}"}, out=out, name="t" + out)
    return r.f[p], p in r.allc


# ---- D1: a test word with a version or number tail --------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("seg", ["foo-tests-44", "tests_2", "integration-tests-3.7", "test-3", "foo_test_12", "Testing-2", "unit.tests.1", "foo-tests-44-rc1", "tests-2a", "integration-tests-3.7_b2"])
def test_a_test_word_with_a_version_or_number_tail_is_a_fixture(tmp_path, seg):
    f, is_comp = one(tmp_path, seg, out="a" + str(abs(hash(seg)) % 10**6))
    assert f["role"] == "fixture" and f["rule_id"] == "R-fx-test-project" and not is_comp


@pytest.mark.parametrize("seg", ["latest-3", "contest-2", "attest_1", "paired-t-test", "protest-4", "greatest_2", "tester-2", "testbed-3", "tested-1", "retest-5", "my-testing", "foo-testing-tools"])
def test_the_embedded_or_tailless_cases_are_not_matched(tmp_path, seg):
    f, is_comp = one(tmp_path, seg, out="n" + str(abs(hash(seg)) % 10**6))
    assert f["rule_id"] == "R-comp-package-json" and is_comp


def test_no_word_is_added_beyond_the_n3_list():
    p = load_profile("code-repo-conventions", PROFILES)
    r = [x for x in p.rules if x.id == "R-fx-test-project"][0]
    words = set()
    for rx in r.segment_res:
        words |= {w for w in ("spec", "check", "verify", "qa", "e2e", "integration", "unit", "smoke", "mock", "stub") if w in rx.pattern.lower()}
    assert words == set()                                                                    # only test, tests, testing (and the N3 names) appear in the patterns


# ---- D2: test- and tests- prefixes ----------------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("seg", ["test-utils", "test_common", "tests-and-more", "tests_helpers", "Test-Utils", "TESTS_X"])
def test_a_segment_that_starts_with_a_test_prefix_is_a_fixture(tmp_path, seg):
    f, is_comp = one(tmp_path, seg, out="p" + str(abs(hash(seg)) % 10**6))
    assert f["role"] == "fixture" and not is_comp


@pytest.mark.parametrize("seg", ["testing-tools-x", "tester", "testbed", "testify", "testsuite", "tests"[:0] + "attestation", "contest-lib"])
def test_other_prefixes_are_not_matched(tmp_path, seg):
    f, is_comp = one(tmp_path, seg, out="q" + str(abs(hash(seg)) % 10**6))
    assert f["rule_id"] == "R-comp-package-json" and is_comp


def test_a_declared_member_with_such_a_segment_is_excluded_too(tmp_path):
    files = {"settings.gradle": "include 'app', 'app:test-utils', 'app:foo-tests-44', 'app:lib'\n", "build.gradle": "x", "app/build.gradle": "x", "app/lib/L.java": "x", "app/test-utils/T.java": "x",
             "app/foo-tests-44/F.java": "x"}
    r = survey(tmp_path, files)
    assert {"app", "app/lib"} <= set(r.allc) and "app/test-utils" not in r.allc and "app/foo-tests-44" not in r.allc
    assert r.f["app/test-utils"]["role"] == "fixture" and r.f["app/foo-tests-44"]["role"] == "fixture"


def test_a_top_level_test_folder_keeps_its_component_but_a_top_level_test_prefixed_project_does_not(tmp_path):
    r = survey(tmp_path, {"pyproject.toml": "[project]\nname='p'\n", "tests/helper.py": "x", "tests/pyproject.toml": "[project]\nname='t'\n", "test-utils/package.json": "{}", "lib/package.json": "{}"}, out="top", name="top")
    assert r.f["tests"]["rule_id"] == "R-conv-tests" and "tests" in r.allc and "test-utils" not in r.allc and "lib" in r.allc


# ---- D3: includeBuild is internal tooling ------------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("line", ["includeBuild('build-logic')", 'includeBuild("build-logic")', "includeBuild 'build-logic'", 'includeBuild "build-logic"', "includeBuild('build-logic') { dependencySubstitution {} }"])
def test_an_included_build_and_the_projects_below_it_are_tooling_not_components(tmp_path, line):
    files = {"settings.gradle": f"include 'app'\n{line}\n", "build.gradle": "x", "app/build.gradle": "x", "build-logic/settings.gradle": "include 'conventions'\n",
             "build-logic/build.gradle": "x", "build-logic/conventions/build.gradle": "x", "build-logic/plugins/deep/build.gradle": "x"}
    r = survey(tmp_path, files, out="o" + str(abs(hash(line)) % 10**6), name="t" + str(abs(hash(line)) % 10**6))
    assert "app" in r.allc and not [p for p in r.allc if p.startswith("build-logic")]
    assert r.f["build-logic"]["rule_id"] == "M-included-build" and r.f["build-logic"]["role"] == "tooling" and r.f["build-logic"]["tooling_of"] == "."
    assert r.f["build-logic/conventions"]["role"] == "tooling" and r.f["build-logic/plugins/deep"]["role"] == "tooling" and r.f["build-logic"]["evidence_field"] == "includeBuild"


def test_the_kotlin_form_a_nested_settings_file_and_a_parent_path_resolve(tmp_path):
    files = {"sub/settings.gradle.kts": 'includeBuild("../shared-logic")\ninclude(":mod")\n', "sub/build.gradle": "x", "sub/mod/build.gradle.kts": "x", "shared-logic/build.gradle": "x", "shared-logic/p/build.gradle": "x"}
    r = survey(tmp_path, files)
    assert "sub" in r.allc and "sub/mod" in r.allc and not [p for p in r.allc if p.startswith("shared-logic")] and r.f["shared-logic"]["tooling_of"] == "sub"


@pytest.mark.parametrize("line", ["includeBuild('../../outside')", "includeBuild('/abs/x')", "includeBuild('missing')", "includeBuild(someVariable)", "// includeBuild('real')", "includeBuild('')"])
def test_unsafe_missing_or_non_literal_included_builds_are_ignored(tmp_path, line):
    files = {"settings.gradle": f"include 'real'\n{line}\n", "build.gradle": "x", "real/build.gradle": "x"}
    r = survey(tmp_path, files, out="u" + str(abs(hash(line)) % 10**6), name="u" + str(abs(hash(line)) % 10**6))
    assert "real" in r.allc and not r.rec.tooling_roots


def test_buildsrc_stays_tooling_and_an_included_build_is_not_a_member_and_runs_are_identical(tmp_path):
    files = {"settings.gradle": "include 'a'\nincludeBuild('conv')\n", "build.gradle": "x", "a/build.gradle": "x", "buildSrc/build.gradle": "x", "conv/build.gradle": "x"}
    a = survey(tmp_path, files, out="a", name="ta")
    b = survey(tmp_path, files, out="b", name="tb")
    assert a.f["buildSrc"]["role"] == "tooling" and a.f["buildSrc"]["rule_id"] == "R-tool-package" and a.f["conv"]["rule_id"] == "M-included-build"
    for n in ("components.txt", "components-all.txt", "findings.jsonl", "classes.json"):
        assert (tmp_path / "a" / n).read_bytes() == (tmp_path / "b" / n).read_bytes(), n


def test_a_declared_workspace_member_inside_an_included_build_is_tooling_too(tmp_path):
    files = {"settings.gradle": "includeBuild('logic')\n", "build.gradle": "x", "logic/settings.gradle": "include 'x'\n", "logic/build.gradle": "x", "logic/x/build.gradle": "x"}
    r = survey(tmp_path, files)
    assert not [p for p in r.allc if p.startswith("logic")]


# ---- D4: benchmark harnesses are test support -----------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("seg", ["benchmark", "benchmarks", "bench", "jmh", "jmh-benchmarks", "kafka-bench", "bench_utils", "my-benchmark", "Benchmarks", "JMH_x"])
def test_a_benchmark_project_is_test_support_not_a_component(tmp_path, seg):
    f, is_comp = one(tmp_path, seg, out="b" + str(abs(hash(seg)) % 10**6))
    assert f["role"] == "test-support" and f["kind"] == "benchmark-project" and f["rule_id"] == "R-fx-benchmark-project" and not is_comp


@pytest.mark.parametrize("seg", ["workbench", "benchmarker", "benches", "jmhx", "xbench", "benchmarking", "bench2"])
def test_other_names_are_not_benchmarks(tmp_path, seg):
    f, is_comp = one(tmp_path, seg, out="c" + str(abs(hash(seg)) % 10**6))
    assert f["rule_id"] == "R-comp-package-json" and is_comp


def test_a_declared_member_that_is_a_benchmark_is_excluded_too(tmp_path):
    r = survey(tmp_path, {"settings.gradle": "include 'core', 'jmh-benchmarks'\n", "build.gradle": "x", "core/build.gradle": "x", "jmh-benchmarks/J.java": "x"})
    assert "core" in r.allc and "jmh-benchmarks" not in r.allc and r.f["jmh-benchmarks"]["role"] == "test-support"


# ---- the profile and the held-out names ------------------------------------------------------------------------------------------------------------------------------
def test_no_rule_contains_a_name_from_a_held_out_or_spent_repository():
    banned = ("automation", "kitchen-sink", "sample-repos", "cypress", "eslint-plugin", "upgrade-system", "api-checker", "generator", "test-common", "kafka", "streams", "connect", "tools-api")
    for pid in ("code-repo-conventions", "code-repo", "generic-relevance", "docs-site", "workspace-repo"):
        p = load_profile(pid, PROFILES)
        for r in p.rules:
            text = " ".join([*(rx.pattern for rx in r.segment_res + r.name_res), *r.segments, *r.names, *[str(g.pattern) for g in r.globs]]).lower()
            for b in banned:
                assert b not in text, (pid, r.id, b)


def test_the_new_rules_carry_provenance_and_the_known_limits_are_stated():
    p = load_profile("code-repo-conventions", PROFILES)
    by = {r.id: r for r in p.rules}
    assert p.version == "0.6.0" and "Known limit" in by["R-fx-test-project"].evidence and by["R-fx-benchmark-project"].role == "test-support"
    assert by["R-fx-benchmark-project"].tuned_on == ("kafka (N7, spent)",) and ids_in_order(p, "R-fx-sample-project", "R-fx-benchmark-project", "R-conv-docs")
    m = load_profile("code-repo", PROFILES).manifest_reading.included_build_rule
    assert m.id == "M-included-build" and m.role == "tooling" and "Known limit" in m.evidence and m.tuned_on == ("kafka (N7, spent)",)


def ids_in_order(p, *ids):
    order = [r.id for r in p.rules]
    return [order.index(i) for i in ids] == sorted(order.index(i) for i in ids)
