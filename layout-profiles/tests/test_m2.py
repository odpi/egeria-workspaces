"""M2: components by convention (docs, config, scripts, deployment, tests, requirements, a root import package, a node package's src) and
manifests under examples/ as samples. Synthetic path lists only."""
import json
import shutil
from pathlib import Path

import pytest
import yaml

from recognizer.layout_profile import ProfileError, load_profile, parse_profile
from recognizer.recognize import Recognizer

PROFILES = Path(__file__).resolve().parent.parent / "profiles"


def run(tmp_path, rows, profile="code-repo-conventions", out="out"):
    p = tmp_path / f"{out}.tsv"
    p.write_text("".join(f"{r}\n" for r in rows))
    c = Recognizer(load_profile(profile, PROFILES)).run(p, tmp_path / out)
    f = [json.loads(x) for x in (tmp_path / out / "findings.jsonl").read_text().splitlines()]
    return c, f, {x["path"]: x for x in f}


def lines(tmp_path, name, out="out"):
    return (tmp_path / out / name).read_text().splitlines()


def test_the_profile_loads_with_evidence_on_every_rule():
    p = load_profile("code-repo-conventions", PROFILES)
    assert [pid for pid, _ in p.composed_of] == ["code-repo-conventions", "code-repo", "generic-relevance"]
    assert all(r.evidence.strip() and r.basis in ("convention", "judgement") for r in p.rules[:9])      # M2's own rules come first
    assert len({r.id for r in p.rules}) == len(p.rules)


@pytest.mark.parametrize("path,rule,kind", [
    ("docs/index.md", "R-conv-docs", "documentation"), ("doc/a.md", "R-conv-docs", "documentation"),
    ("config/app.yaml", "R-conv-config", "configuration"), ("conf/x.ini", "R-conv-config", "configuration"),
    ("scripts/run.sh", "R-conv-scripts", "scripts"), ("docker/Dockerfile.base", "R-conv-deployment", "deployment"),
    ("deploy/k.yaml", "R-conv-deployment", "deployment"), ("tests/test_a.py", "R-conv-tests", "test-suite"),
    ("requirements/base.txt", "R-conv-requirements", "dependency-pins"),
])
def test_top_level_convention_directories_are_components(tmp_path, path, rule, kind):
    c, f, by = run(tmp_path, [path])
    top = path.split("/")[0]
    assert by[top]["rule_id"] == rule and by[top]["kind"] == kind and by[top]["role"] == "component"
    assert by[top]["basis"] in ("convention", "judgement") and by[top]["evidence"]


def test_convention_names_apply_at_the_top_level_only(tmp_path):
    c, f, by = run(tmp_path, ["pkg/docs/index.md", "pkg/scripts/run.sh", "pkg/tests/t.py", "src/config/a.yaml"])
    assert not f                                                         # a nested docs/ or tests/ is part of its package, not a component


def test_a_conventional_name_wins_over_a_manifest_in_the_same_directory(tmp_path):
    c, f, by = run(tmp_path, ["docs/package.json", "docs/index.md"])
    assert by["docs"]["rule_id"] == "R-conv-docs" and by["docs"]["kind"] == "documentation"


def test_manifests_under_examples_are_samples_not_components(tmp_path):
    rows = ["packages/a/pyproject.toml", "packages/a/examples/s1/pyproject.toml", "packages/a/examples/s2/package.json", "examples/e/pom.xml"]
    c, f, by = run(tmp_path, rows)
    assert by["packages/a"]["role"] == "component"
    for sample in ("packages/a/examples/s1", "packages/a/examples/s2", "examples/e"):
        assert by[sample]["role"] == "example" and by[sample]["kind"] == "sample-project" and by[sample]["rule_id"] == "R-ex-example-manifest"
    assert lines(tmp_path, "components-all.txt") == ["packages/a"]       # samples are not candidates


def test_a_root_import_package_by_its_init_file(tmp_path):
    c, f, by = run(tmp_path, ["pyproject.toml", "mypkg/__init__.py", "mypkg/core/__init__.py", "other/data.csv"])
    assert by["mypkg"]["rule_id"] == "R-conv-root-import-package" and by["mypkg"]["kind"] == "python-package"
    assert "mypkg/core" not in by and "other" not in by                  # only a TOP-LEVEL directory with an __init__.py


def test_a_top_level_apps_src_is_its_source_root_but_a_nested_packages_src_is_not(tmp_path):
    rows = ["web/package.json", "web/src/app.ts", "web/plugins/p1/package.json", "web/plugins/p1/src/i.ts", "lib/src/x.py"]
    c, f, by = run(tmp_path, rows)
    assert by["web/src"]["rule_id"] == "R-conv-node-src" and by["web/src"]["kind"] == "source-root"
    assert "web/plugins/p1/src" not in by and "lib/src" not in by        # no package.json beside it / too deep


def test_only_manifest_components_have_parts(tmp_path):
    rows = ["docker/img/Dockerfile", "docker/img2/package.json", "pkg/pyproject.toml", "pkg/sub/pyproject.toml"]
    c, f, by = run(tmp_path, rows)
    assert "part_of" not in by["docker/img"] and "part_of" not in by["docker/img2"]     # docker/ is a grouping folder: its images are components
    assert by["pkg/sub"]["part_of"] == "pkg"                                            # a manifest component contains its nested manifests
    assert lines(tmp_path, "components.txt") == ["docker", "docker/img", "docker/img2", "pkg"]
    assert lines(tmp_path, "components-all.txt") == ["docker", "docker/img", "docker/img2", "pkg", "pkg/sub"]


def test_a_convention_directory_inside_a_hidden_subtree_is_not_a_component(tmp_path):
    c, f, by = run(tmp_path, ["node_modules/docs/a.md", "build/scripts/x.sh", "docs/a.md"])
    assert set(by) == {"build", "docs", "node_modules"}                   # the two hidden subtrees and the one real component
    assert by["docs"]["rule_id"] == "R-conv-docs"
    assert {k for k in by if by[k]["role"] == "component"} == {"docs"}


def test_a_directory_rule_may_not_test_a_file_name_and_needs_a_directory_test(tmp_path):
    def doc(**rule):
        base = yaml.safe_load((PROFILES / "worktree-copies.yaml").read_text())
        r = {"id": "R-x", "match": {"path_glob": "docs"}, "assign": {"role": "worktree-copy"}, "grain": "component", "basis": "convention",
             "confidence": "low", "evidence": "e"}
        r.update(rule)
        base["rules"] = [r]
        return base
    parse_profile({**doc(assign={"role": "worktree-copy"}, grain="dir")})                  # a plain file/dir glob rule is fine
    with pytest.raises(ProfileError):
        parse_profile(doc(assign={"role": "component"}, match={"extension": ".md"}))        # component + a file-name test
    with pytest.raises(ProfileError):
        parse_profile(doc(assign={"role": "worktree-copy"}))                                 # a component must assign role component
    with pytest.raises(ProfileError):
        parse_profile(doc(assign={"role": "component"}, match={"extension": ".md"}, grain="component"))


def test_output_is_deterministic_with_directory_conventions(tmp_path):
    rows = ["docs/a.md", "scripts/x.sh", "pkg/pyproject.toml", "pkg/examples/s/pyproject.toml", "tests/t.py", "web/package.json", "web/src/a.ts"]
    run(tmp_path, rows, out="a")
    run(tmp_path, list(reversed(rows)), out="b")
    for n in ("components.txt", "components-all.txt", "findings.jsonl", "classes.json", "report.md"):
        assert (tmp_path / "a" / n).read_bytes() == (tmp_path / "b" / n).read_bytes(), n


# ---- candidate counts on the tune-set lists (no key needed; scoring against the draft keys stays outside this repository) -------------

import os  # noqa: E402

TUNE = os.environ.get("LAYOUT_TUNE_PATHS_DIR")


@pytest.mark.skipif(not TUNE or not (Path(TUNE) / "trellis.paths.tsv").is_file(), reason="LAYOUT_TUNE_PATHS_DIR (trellis/datahub/superset lists) not set")
@pytest.mark.parametrize("repo,all_candidates,top_candidates", [("trellis", 19, 18), ("datahub", 84, 75), ("superset", 46, 39)])
def test_candidate_counts_with_conventions(tmp_path, repo, all_candidates, top_candidates):
    """Pinned so a rule change that moves the numbers is seen. candidates = the list minus the root and minus directories claimed only by
    metadata.yaml. Scored against the draft keys (provisional): trellis recall 1.00, superset 1.00, datahub 1.00 on components-all."""
    Recognizer(load_profile("code-repo-conventions", PROFILES)).run(Path(TUNE) / f"{repo}.paths.tsv", tmp_path)
    meta = {json.loads(x)["path"] for x in (tmp_path / "findings.jsonl").read_text().splitlines() if json.loads(x)["rule_id"] == "R-comp-metadata-yaml"}
    read = lambda n: [x for x in (tmp_path / n).read_text().splitlines() if x not in (".", "") and x not in meta]
    assert (len(read("components-all.txt")), len(read("components.txt"))) == (all_candidates, top_candidates)


# ---- the structural rule: many sibling manifests under one parent are top-level components, not parts ------------------------------

def siblings(parent, n, manifest="package.json", start=0):
    return [f"{parent}/p{i}/{manifest}" for i in range(start, start + n)]


def test_five_sibling_manifests_of_one_kind_inside_a_component_are_top_level(tmp_path):
    rows = ["web/package.json"] + siblings("web/plugins", 5)
    c, f, by = run(tmp_path, rows)
    for i in range(5):
        x = by[f"web/plugins/p{i}"]
        assert "part_of" not in x and x["structure_rule_id"] == "S-workspace-siblings"
        assert x["structure_evidence"] == "workspace-style layout: many sibling manifests under one parent"
        assert (x["structure_basis"], x["structure_confidence"]) == ("judgement", "low")
    assert lines(tmp_path, "components.txt") == ["web"] + [f"web/plugins/p{i}" for i in range(5)]
    assert c["components"] == {"top_level": 6, "parts": 0}


def test_four_sibling_manifests_stay_parts(tmp_path):
    c, f, by = run(tmp_path, ["web/package.json"] + siblings("web/plugins", 4))
    assert all(by[f"web/plugins/p{i}"]["part_of"] == "web" for i in range(4))
    assert lines(tmp_path, "components.txt") == ["web"] and c["components"] == {"top_level": 1, "parts": 4}


def test_siblings_of_different_kinds_are_counted_per_kind(tmp_path):
    rows = ["app/package.json"] + siblings("app/mods", 3) + siblings("app/mods", 3, "pyproject.toml", 10)       # 3 + 3: neither reaches 5
    c, f, by = run(tmp_path, rows)
    assert all("part_of" in by[d] for d in by if d.startswith("app/mods/"))
    rows = ["app/package.json"] + siblings("app/mods", 5) + siblings("app/mods", 2, "pyproject.toml", 10)       # 5 node + 2 python
    c, f, by = run(tmp_path, rows, out="b")
    assert all("part_of" not in by[f"app/mods/p{i}"] for i in range(5))                                      # the five of one kind are promoted
    assert all(by[f"app/mods/p{i}"]["part_of"] == "app" for i in (10, 11))                                    # the other kind stays parts


def test_siblings_under_different_parents_are_not_pooled(tmp_path):
    rows = ["web/package.json"] + siblings("web/a", 3) + siblings("web/b", 3)
    c, f, by = run(tmp_path, rows)
    assert c["components"] == {"top_level": 1, "parts": 6}


def test_the_structural_rule_never_touches_a_part_only_by_its_names(tmp_path):
    # the same shape under any folder name is promoted; no name list is involved
    for parent in ("plugins", "packages", "anything-at-all"):
        c, f, by = run(tmp_path, ["root/package.json"] + siblings(f"root/{parent}", 5), out=parent)
        assert c["components"]["parts"] == 0


def test_structural_rule_schema_errors():
    base = yaml.safe_load((PROFILES / "worktree-copies.yaml").read_text())
    good = {"id": "S-x", "op": "sibling-manifests-top-level", "min": 5, "basis": "judgement", "confidence": "low", "evidence": "e"}
    parse_profile({**base, "structural_rules": [good]})
    for bad in ({**good, "op": "other"}, {**good, "min": 1}, {**good, "min": "5"}, {**good, "min": True}, {**good, "evidence": " "},
                {**good, "basis": "vibes"}, {**good, "extra": 1}, {k: v for k, v in good.items() if k != "evidence"},
                {**good, "id": "R-copy-worktree-name"}):
        with pytest.raises(ProfileError):
            parse_profile({**base, "structural_rules": [bad]})
    with pytest.raises(ProfileError):
        parse_profile({**base, "structural_rules": [good, good]})                                          # duplicate structural id


def test_every_m2_rule_names_the_repositories_that_motivated_it():
    p = load_profile("code-repo-conventions", PROFILES)
    own = [r for r in p.rules if r.origin == "code-repo-conventions"]
    assert len(own) == 9 and all(r.tuned_on and set(r.tuned_on) <= {"trellis", "datahub", "superset"} for r in own)
    assert [x["id"] for x in p.structural] == ["S-workspace-siblings"] and p.structural[0]["tuned_on"] == ["superset"]
    one_repo = sorted(r.id for r in own if len(r.tuned_on) == 1)
    assert "R-conv-node-src" in one_repo and "R-conv-docs" not in one_repo             # one-repository rules are visible, hence ablatable


def test_tuned_on_must_be_a_list_of_names():
    base = yaml.safe_load((PROFILES / "code-repo-conventions.yaml").read_text())
    base["extends"] = []
    base["structural_rules"] = []
    base["rules"][0]["tuned_on"] = "trellis"
    with pytest.raises(ProfileError):
        parse_profile(base)
