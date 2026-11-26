"""M1: findings per (rule, directory) with counts, components and parts, vendored wins, the code-repo profile. Synthetic path lists only."""
import json
import os
from pathlib import Path

import pytest

from recognizer.layout_profile import load_profile
from recognizer.recognize import Recognizer

PROFILES = Path(__file__).resolve().parent.parent / "profiles"


def run(profile_name, tmp_path, rows, out="out", per_file=False):
    p = tmp_path / f"{out}.tsv"
    p.write_text("".join(f"{r}\n" if isinstance(r, str) else f"{r[0]}\t{r[1]}\n" for r in rows))
    c = Recognizer(load_profile(profile_name, PROFILES)).run(p, tmp_path / out, per_file=per_file)
    findings = [json.loads(x) for x in (tmp_path / out / "findings.jsonl").read_text().splitlines()]
    return c, findings


def lines(tmp_path, out, name):
    return (tmp_path / out / name).read_text().splitlines()


def test_findings_are_per_rule_and_directory_with_counts_and_ids_do_not_depend_on_the_counts(tmp_path):
    rows1 = [("svc/node_modules/a/1.js", 10), ("svc/node_modules/b/2.js", 20), ("svc/logs/x.log", 5), ("svc/logs/y.log", 6), ("svc/main.py", 1)]
    rows2 = [("svc/node_modules/a/1.js", 99), ("svc/logs/x.log", 5), ("svc/main.py", 1), ("svc/logs/z.log", 1), ("svc/logs/w.log", 1)]
    c1, f1 = run("generic-relevance", tmp_path, rows1, "r1")
    c2, f2 = run("generic-relevance", tmp_path, rows2, "r2")
    k = lambda f: {(x["rule_id"], x["path"]): x for x in f}
    assert set(k(f1)) == {("R-vend-installed", "svc/node_modules"), ("R-run-log", "svc/logs")}
    assert (k(f1)[("R-vend-installed", "svc/node_modules")]["files"], k(f1)[("R-vend-installed", "svc/node_modules")]["bytes"]) == (2, 30)
    assert k(f2)[("R-run-log", "svc/logs")]["files"] == 3 and k(f1)[("R-run-log", "svc/logs")]["files"] == 2
    for key in k(f1):                                                       # the id comes from rule and directory, never from the counts
        assert k(f1)[key]["finding_id"] == k(f2)[key]["finding_id"]
    assert sum(x["files"] for x in f1) == c1["total_files"] - c1["by_role"]["unclassified"]["files"]


def test_per_file_option_adds_a_debug_file_and_leaves_the_counts_alone(tmp_path):
    rows = [("a/x.log", 1), ("a/y.log", 2), ("b/z.js", 3)]
    c1, f1 = run("generic-relevance", tmp_path, rows, "plain")
    c2, f2 = run("generic-relevance", tmp_path, rows, "debug", per_file=True)
    assert c1 == c2 and f1 == f2                                            # classes.json and findings.jsonl identical
    assert not (tmp_path / "plain" / "findings-files.jsonl").exists()
    per_file = [json.loads(x) for x in lines(tmp_path, "debug", "findings-files.jsonl")]
    assert [x["path"] for x in per_file] == ["a/x.log", "a/y.log"] and all(x["files"] == 1 for x in per_file)


def test_components_txt_is_top_level_and_components_all_adds_the_parts(tmp_path):
    rows = ["packages/a/pyproject.toml", "packages/a/sub/pyproject.toml", "packages/b/package.json", "docs/readme.md"]
    c, f = run("code-repo", tmp_path, rows)
    assert lines(tmp_path, "out", "components.txt") == ["packages/a", "packages/b"]
    assert lines(tmp_path, "out", "components-all.txt") == ["packages/a", "packages/a/sub", "packages/b"]
    assert c["components"] == {"top_level": 2, "parts": 1}
    parts = {x["path"]: x.get("part_of") for x in f if x["role"] == "component"}
    assert parts == {"packages/a": None, "packages/a/sub": "packages/a", "packages/b": None}


def test_a_root_manifest_is_a_root_project_and_does_not_swallow_nested_components(tmp_path):
    rows = ["pyproject.toml", "pkg/package.json", "svc/pom.xml", "svc/sub/package.json", "README.md"]
    c, f = run("code-repo", tmp_path, rows)
    assert lines(tmp_path, "out", "components.txt") == [".", "pkg", "svc"]              # the nested manifest dirs are top-level components
    assert lines(tmp_path, "out", "components-all.txt") == [".", "pkg", "svc", "svc/sub"]  # every manifest directory
    by = {x["path"]: x for x in f}
    assert by["."]["root"] is True and by["."]["kind"] == "root-project" and by["."]["manifest_kind"] == "python-package"
    assert "part_of" not in by["pkg"] and "part_of" not in by["svc"] and "root" not in by["pkg"]
    assert by["svc/sub"]["part_of"] == "svc"                                              # parts only below a NON-root component
    assert c["components"] == {"top_level": 3, "parts": 1}


@pytest.mark.parametrize("hidden_dir", ["node_modules", ".venv", "build", "dist", "target", "__pycache__", ".git"])
def test_a_manifest_inside_a_hidden_subtree_is_never_a_component(tmp_path, hidden_dir):
    rows = [f"app/{hidden_dir}/pkg/pyproject.toml", f"app/{hidden_dir}/package.json", "app/package.json"]
    c, f = run("code-repo", tmp_path, rows)
    assert lines(tmp_path, "out", "components-all.txt") == ["app"]                                # only the real one
    assert c["by_relevance"]["hidden"]["files"] == 2                                              # the other two files are counted, hidden


def test_a_manifest_inside_a_worktree_copy_is_not_a_component_in_a_workspace(tmp_path):
    import shutil
    for n in ("generic-relevance", "worktree-copies", "code-repo"):
        shutil.copy(PROFILES / f"{n}.yaml", tmp_path / f"{n}.yaml")
    (tmp_path / "ws-code.yaml").write_text(
        "profile_id: ws-code\nversion: 0.1.0\nstatus: proposed\napplies_to: workspace-of-repos\nextends: [code-repo, worktree-copies]\n"
        "roles: [component]\nrelevance: {primary: [component], supporting: [], hidden: []}\nrules: []\n")
    p = tmp_path / "l.tsv"
    p.write_text("real/pyproject.toml\nwt-x/.git\nwt-x/pyproject.toml\nwt-x/src/a.py\n")        # wt-x holds a .git FILE: a worktree
    c = Recognizer(load_profile("ws-code", tmp_path)).run(p, tmp_path / "o")
    assert (tmp_path / "o" / "components-all.txt").read_text() == "real\n"          # the copy's manifest is hidden with the copy
    assert c["by_role"]["worktree-copy"]["files"] == 3


def test_first_manifest_rule_wins_per_directory_and_kinds(tmp_path):
    rows = ["a/pyproject.toml", "a/package.json", "b/package.json", "b/Dockerfile", "c/pom.xml", "d/build.gradle", "e/Cargo.toml", "f/go.mod",
            "g/Chart.yaml", "h/Dockerfile", "i/metadata.yaml", "j/setup.py"]
    _, f = run("code-repo", tmp_path, rows)
    kinds = {x["path"]: (x["kind"], x["rule_id"], x["basis"]) for x in f}
    assert kinds["a"][:2] == ("python-package", "R-comp-pyproject")                                # pyproject before package.json
    assert kinds["b"][:2] == ("node-package", "R-comp-package-json")                               # package.json before Dockerfile
    assert kinds["c"][0] == "maven-module" and kinds["d"][0] == "gradle-module" and kinds["e"][0] == "rust-crate"
    assert kinds["f"][0] == "go-module" and kinds["g"][0] == "helm-chart" and kinds["h"][0] == "docker-image"
    assert kinds["i"][:2] == ("connector-metadata", "R-comp-metadata-yaml") and kinds["j"][0] == "python-package"
    assert all(v[2] == "manifest" for v in kinds.values())


def test_the_code_repo_profile_extends_generic_relevance_and_carries_evidence(tmp_path):
    p = load_profile("code-repo", PROFILES)
    assert [pid for pid, _ in p.composed_of] == ["code-repo", "generic-relevance"]
    assert all(r.evidence and r.confidence and r.basis for r in p.rules)
    assert any(r.id == "R-vcs-git" for r in p.rules)                         # the generic rules come along (after the manifest rules)


def test_unmanifested_files_stay_unclassified_in_code_repo(tmp_path):
    c, _ = run("code-repo", tmp_path, ["docs/guide.md", "a/package.json"])
    assert c["by_role"]["unclassified"]["files"] == 2                      # a component dir's files are not re-labelled (M2 does that)


# ---- the manifest-probe regression, candidate counts only (needs the tune-set path lists; the keys are NOT in this repository) -------

TUNE = os.environ.get("LAYOUT_TUNE_PATHS_DIR")


@pytest.mark.skipif(not TUNE or not (Path(TUNE) / "trellis.paths.tsv").is_file(), reason="LAYOUT_TUNE_PATHS_DIR (trellis/datahub/superset lists) not set")
@pytest.mark.parametrize("repo,expected", [("trellis", 25), ("datahub", 82), ("superset", 37)])
def test_manifest_probe_candidate_counts(tmp_path, repo, expected):
    """candidates = components-all minus the repository root minus directories claimed only by metadata.yaml (the Phase 0 probe did not
    count metadata.yaml). trellis 25 and datahub 82 are the Phase 0 baselines exactly; superset is 37, the corrected probe figure (the
    33 in the first baseline came from a probe bug that collapsed one-level-deep manifests to the root)."""
    c = Recognizer(load_profile("code-repo", PROFILES)).run(Path(TUNE) / f"{repo}.paths.tsv", tmp_path)
    meta = {json.loads(x)["path"] for x in (tmp_path / "findings.jsonl").read_text().splitlines() if json.loads(x)["rule_id"] == "R-comp-metadata-yaml"}
    cand = [x for x in (tmp_path / "components-all.txt").read_text().splitlines() if x not in (".", "") and x not in meta]
    assert len(cand) == expected
