"""The recognizer on SYNTHETIC path lists (hand-written, no repository content): first match, grain, determinism, stable ids."""
import json
import random
from pathlib import Path

import pytest
import yaml

from recognizer.layout_profile import parse_profile
from recognizer.recognize import Recognizer, finding_id, read_rows

PROFILES = Path(__file__).resolve().parent.parent / "profiles"


def rule(rid, match, role, grain="dir", conf="high", kind=None, **assign):
    return {"id": rid, "match": match, "assign": {"role": role, "kind": kind, **assign} if kind else {"role": role, **assign},
            "grain": grain, "basis": "convention", "confidence": conf, "evidence": f"evidence for {rid}"}


def make_profile(rules, version="0.1.0", pid="synthetic"):
    return parse_profile({
        "profile_id": pid, "version": version, "status": "proposed", "applies_to": "any",
        "roles": ["component", "vendored", "generated", "runtime-output", "example", "worktree-copy", "vcs-internal", "source"],
        "relevance": {"primary": ["component"], "supporting": ["example", "source"],
                      "hidden": ["vendored", "generated", "runtime-output", "worktree-copy", "vcs-internal"]},
        "rules": rules})


def write_list(tmp_path, rows, name="paths.tsv"):
    p = tmp_path / name
    p.write_text("".join(f"{r}\n" if isinstance(r, str) else f"{r[0]}\t{r[1]}\n" for r in rows))
    return p


def run(profile, tmp_path, rows, out="out"):
    c = Recognizer(profile).run(write_list(tmp_path, rows), tmp_path / out)
    findings = [json.loads(line) for line in (tmp_path / out / "findings.jsonl").read_text().splitlines()]
    return c, findings


NM = rule("R-nm", {"path_segment": "node_modules"}, "vendored", "subtree")
LOG = rule("R-log", {"extension": ".log"}, "runtime-output", "dir")


def test_first_match_wins_and_order_matters(tmp_path):
    rows = ["app/node_modules/pkg/run.log", "app/run.log", "app/src/main.py"]
    c, f = run(make_profile([NM, LOG]), tmp_path, rows, "ab")
    assert c["by_rule"]["R-nm"]["files"] == 1 and c["by_rule"]["R-log"]["files"] == 1
    c, f = run(make_profile([LOG, NM]), tmp_path, rows, "ba")                 # the same rules, swapped
    assert c["by_rule"]["R-log"]["files"] == 2 and "R-nm" not in c["by_rule"]


def test_subtree_grain_one_finding_per_root_and_every_file_counted(tmp_path):
    rows = [("a/node_modules/x/1.js", 10), ("a/node_modules/x/2.js", 20), ("a/node_modules/y/3.js", 30), ("b/keep.txt", 5)]
    c, f = run(make_profile([NM]), tmp_path, rows)
    assert [(x["path"], x["rule_id"], x["grain"]) for x in f] == [("a/node_modules", "R-nm", "subtree")]
    assert c["by_role"]["vendored"] == {"files": 3, "bytes": 60}
    assert c["by_role"]["unclassified"] == {"files": 1, "bytes": 5}


def test_the_shallowest_subtree_root_is_the_node(tmp_path):
    c, f = run(make_profile([NM]), tmp_path, ["a/node_modules/b/node_modules/x.js", "a/node_modules/y.js"])
    assert [x["path"] for x in f] == ["a/node_modules"]


def test_file_rules_give_one_finding_per_file(tmp_path):
    c, f = run(make_profile([LOG]), tmp_path, [("a.log", 3), ("d/b.log", 4), ("d/e.log", 5), ("d/c.txt", 9)])
    assert [(x["path"], x["files"], x["bytes"]) for x in f] == [(".", 1, 3), ("d", 2, 9)]       # one finding per (rule, directory), with counts
    assert all(x["grain"] == "dir" and x["role"] == "runtime-output" for x in f)


def test_a_path_segment_is_a_directory_never_the_file_name(tmp_path):
    c, f = run(make_profile([NM]), tmp_path, ["src/node_modules"])             # a FILE called node_modules
    assert not f and c["by_role"]["unclassified"]["files"] == 1


def test_glob_subtree_root_and_the_name_pattern_claims_only_what_is_left(tmp_path):
    wt = rule("R-wt", {"path_glob": ["wt-*/**", "*-vocab[0-9]*/**"]}, "worktree-copy", "subtree")
    rows = ["wt-one/src/a.py", "wt-one/run.log", "x/wt-notatop/a.py", "q-vocab12/z.txt", "q-vocab/z.txt", "top.py"]
    c, f = run(make_profile([LOG, wt]), tmp_path, rows)
    assert c["by_rule"]["R-log"]["files"] == 1                                 # the log inside a worktree stays a log
    assert c["by_rule"]["R-wt"]["files"] == 2                                  # wt-one/src/a.py and q-vocab12/z.txt
    wt_roots = sorted(x["path"] for x in f if x["rule_id"] == "R-wt")
    assert wt_roots == ["q-vocab12", "wt-one"]
    assert c["by_role"]["unclassified"]["files"] == 3                          # x/wt-notatop/a.py, q-vocab/z.txt, top.py


def test_unclassified_is_a_first_class_result(tmp_path):
    c, f = run(make_profile([NM]), tmp_path, [("a.py", 7), ("b/c.py", 3)])
    assert c["by_role"] == {"unclassified": {"files": 2, "bytes": 10}}
    assert c["shares"]["unclassified_files"] == 1.0 and c["shares"]["classified_files"] == 0.0 and not f


def test_shares_and_totals(tmp_path):
    c, _ = run(make_profile([NM]), tmp_path, [("a/node_modules/x", 100), ("b.py", 300)])
    assert c["total_files"] == 2 and c["total_bytes"] == 400
    assert c["shares"]["hidden_files"] == 0.5 and c["shares"]["hidden_bytes"] == 0.25 and c["shares"]["classified_files"] == 0.5
    assert c["by_relevance"]["hidden"] == {"files": 1, "bytes": 100}


def test_output_is_byte_identical_across_runs_and_input_order(tmp_path):
    prof = make_profile([NM, LOG])
    rows = [(f"d{i % 7}/node_modules/p{i}/f{i}.js" if i % 3 else f"d{i % 5}/run{i}.log", i) for i in range(200)] + [("z/keep.py", 1)]
    names = ("components.txt", "findings.jsonl", "classes.json", "report.md")
    run(prof, tmp_path, sorted(rows), "one")
    run(prof, tmp_path, sorted(rows), "two")
    shuffled = rows[:]
    random.Random(7).shuffle(shuffled)
    run(prof, tmp_path, shuffled, "three")                                    # an unsorted list is sorted in memory first
    for n in names:
        a, b, c3 = ((tmp_path / d / n).read_bytes() for d in ("one", "two", "three"))
        assert a == b == c3, n


def test_unsorted_and_tab_free_input_and_crlf(tmp_path):
    p = tmp_path / "p.txt"
    p.write_bytes(b"b/x.log\r\na/x.log\r\n")
    c = Recognizer(make_profile([LOG])).run(p, tmp_path / "o")
    assert c["total_files"] == 2 and c["by_rule"]["R-log"]["bytes"] == 0       # no sizes given: bytes are 0, files are counted


def test_a_path_with_a_non_numeric_tail_after_a_tab_is_all_path(tmp_path):
    p = tmp_path / "p.txt"
    p.write_text("odd\tname.log\nplain.log\t12\n")
    rows = list(read_rows(p))
    assert rows == [("odd\tname.log", 0), ("plain.log", 12)] or sorted(rows) == sorted([("odd\tname.log", 0), ("plain.log", 12)])


@pytest.mark.parametrize("bad", ["/abs/path.py", "a//b.py", "a/../b.py", "a/./", ".."])
def test_bad_paths_are_rejected(tmp_path, bad):
    with pytest.raises(ValueError):
        list(read_rows(write_list(tmp_path, [bad, "ok.py"])))


def test_duplicate_paths_are_rejected(tmp_path):
    with pytest.raises(ValueError):
        list(read_rows(write_list(tmp_path, ["a.py", "a.py"])))
    with pytest.raises(ValueError):
        list(read_rows(write_list(tmp_path, ["b.py", "a.py", "b.py"])))


def test_the_recognizer_never_opens_the_listed_files(tmp_path):
    c, _ = run(make_profile([NM]), tmp_path, ["/no/such"[1:] + "/node_modules/x.js"])    # the path does not exist anywhere
    assert c["by_role"]["vendored"]["files"] == 1


# ---- finding identity ------------------------------------------------------------------------------------------------------

def ids(findings):
    return {(x["rule_id"], x["path"]): x["finding_id"] for x in findings}


def test_finding_ids_are_stable_across_runs_and_across_a_different_tree_sha(tmp_path):
    prof = make_profile([NM, LOG])
    tree1 = [("a/node_modules/x.js", 1), ("a/run.log", 10), ("a/src/main.py", 5)]
    tree2 = [("a/node_modules/x.js", 999), ("a/run.log", 11), ("a/src/main.py", 6), ("a/src/new.py", 2), ("b/other.log", 3)]   # "another sha"
    _, f1 = run(prof, tmp_path, tree1, "t1")
    _, f1b = run(prof, tmp_path, tree1, "t1b")
    _, f2 = run(prof, tmp_path, tree2, "t2")
    assert ids(f1) == ids(f1b)
    for key, fid in ids(f1).items():
        assert ids(f2)[key] == fid                                           # the same node keeps its id, whatever else changed
    assert all(len(v) == 16 and int(v, 16) >= 0 for v in ids(f1).values())
    # the finding body carries no time, run id or tree sha
    assert set(f1[0]) == {"finding_id", "path", "role", "kind", "relevance", "rule_id", "basis", "confidence", "evidence", "grain",
                          "profile_id", "profile_version", "files", "bytes"}


def test_finding_id_changes_with_rule_path_profile_and_major_version_only(tmp_path):
    base = make_profile([NM], "0.1.0")
    fid = finding_id(base, "R-nm", "a/node_modules")
    assert fid == finding_id(make_profile([NM], "0.9.4"), "R-nm", "a/node_modules")       # minor/patch bumps keep ids
    assert fid != finding_id(make_profile([NM], "1.0.0"), "R-nm", "a/node_modules")       # a major bump changes them
    assert fid != finding_id(base, "R-other", "a/node_modules")
    assert fid != finding_id(base, "R-nm", "b/node_modules")
    assert fid != finding_id(make_profile([NM], pid="other"), "R-nm", "a/node_modules")


def test_confidence_basis_and_evidence_are_copied_from_the_rule(tmp_path):
    r = rule("R-low", {"extension": ".tmp"}, "runtime-output", conf="low", kind="scratch-file")
    _, f = run(make_profile([r]), tmp_path, ["x.tmp"])
    assert (f[0]["confidence"], f[0]["basis"], f[0]["evidence"], f[0]["kind"]) == ("low", "convention", "evidence for R-low", "scratch-file")


# ---- directory rules: components and parts ---------------------------------------------------------------------------------

PYPROJ = {"id": "R-comp", "match": {"has_file": "pyproject.toml"}, "assign": {"role": "component", "kind": "python-package"},
          "grain": "component", "basis": "manifest", "confidence": "high", "evidence": "pyproject.toml declares a package"}


def test_components_come_from_manifest_files_and_nested_ones_are_parts(tmp_path):
    rows = ["pyproject.toml", "packages/a/pyproject.toml", "packages/a/src/x.py", "packages/a/examples/e1/pyproject.toml",
            "packages/b/pyproject.toml", "docs/index.md"]
    c, f = run(make_profile([PYPROJ]), tmp_path, rows)
    assert (tmp_path / "out" / "components.txt").read_text() == ".\npackages/a\npackages/b\n"    # the root is a component, not their parent
    parts = {x["path"]: x.get("part_of") for x in f if x["rule_id"] == "R-comp"}
    assert parts == {".": None, "packages/a": None, "packages/a/examples/e1": "packages/a", "packages/b": None}
    root = next(x for x in f if x["path"] == ".")
    assert root["root"] is True and root["kind"] == "root-project" and root["manifest_kind"] == "python-package"
    assert c["components"] == {"top_level": 3, "parts": 1}


def test_without_a_root_manifest_the_top_level_ones_are_components(tmp_path):
    rows = ["packages/a/pyproject.toml", "packages/a/sub/pyproject.toml", "packages/b/pyproject.toml"]
    c, f = run(make_profile([PYPROJ]), tmp_path, rows)
    assert (tmp_path / "out" / "components.txt").read_text() == "packages/a\npackages/b\n"
    assert {x["path"]: x.get("part_of") for x in f} == {"packages/a": None, "packages/a/sub": "packages/a", "packages/b": None}


def test_a_more_specific_rule_can_make_a_nested_manifest_an_example(tmp_path):
    ex = {"id": "R-ex", "match": {"has_file": "pyproject.toml", "path_segment": "examples"}, "assign": {"role": "example"},
          "grain": "dir", "basis": "convention", "confidence": "medium", "evidence": "a manifest under examples/ is a sample, not a package"}
    c, f = run(make_profile([ex, PYPROJ]), tmp_path, ["packages/a/pyproject.toml", "packages/a/examples/e1/pyproject.toml"])
    got = {x["path"]: x["role"] for x in f}
    assert got == {"packages/a": "component", "packages/a/examples/e1": "example"}
    assert (tmp_path / "out" / "components.txt").read_text() == "packages/a\n"


def test_parent_has_file(tmp_path):
    r = {"id": "R-pk", "match": {"parent_has_file": "workspace.yaml"}, "assign": {"role": "component"}, "grain": "component",
         "basis": "judgement", "confidence": "low", "evidence": "a direct child of a workspace root is a member"}
    c, f = run(make_profile([r]), tmp_path, ["ws/workspace.yaml", "ws/m1/x.py", "ws/m2/y.py", "ws/m1/deep/z.py"])
    assert [x["path"] for x in f] == ["ws/m1", "ws/m2"]


def test_a_directory_subtree_rule_claims_the_files_below(tmp_path):
    r = {"id": "R-cache", "match": {"has_file": "CACHEDIR.TAG"}, "assign": {"role": "generated"}, "grain": "subtree",
         "basis": "convention", "confidence": "high", "evidence": "a CACHEDIR.TAG marks a cache directory"}
    c, f = run(make_profile([r]), tmp_path, ["c/CACHEDIR.TAG", "c/sub/blob", "d/keep.py"])
    assert c["by_role"]["generated"]["files"] == 2 and c["by_role"]["unclassified"]["files"] == 1
    assert [x["path"] for x in f] == ["c"]


def test_findings_interleave_directory_and_file_findings_deterministically(tmp_path):
    rows = ["a/pyproject.toml", "a/run.log", "b/run.log", "c/pyproject.toml"]
    _, f = run(make_profile([PYPROJ, LOG]), tmp_path, rows, "x")
    _, g = run(make_profile([PYPROJ, LOG]), tmp_path, rows, "y")
    assert [x["finding_id"] for x in f] == [x["finding_id"] for x in g]
    assert [(x["path"], x["rule_id"]) for x in f] == [("a", "R-comp"), ("a", "R-log"), ("b", "R-log"), ("c", "R-comp")]


# ---- the shipped generic profile on a synthetic tree -------------------------------------------------------------------------

def test_generic_relevance_on_a_synthetic_tree(tmp_path):        # the worktree name rule is NOT in generic-relevance since 0.2.0
    from recognizer.layout_profile import load_profile
    prof = load_profile("generic-relevance", PROFILES)
    rows = ["svc/.git/HEAD", "svc/node_modules/x/index.js", "svc/build/out.class", "svc/__pycache__/m.pyc", "svc/src/main.py",
            "svc/logs/app.log", "logs/e1.openlineageevent", "svc/core.hprof", "db-backups/b1.sql", "svc/dump.sql.gz",
            "wt-feature/src/a.py", "wt-feature/node_modules/p.js", "wt-feature/run.log", "README.md"]
    c, f = run(prof, tmp_path, rows)
    got = {k: v["files"] for k, v in c["by_rule"].items()}
    assert got == {"R-vcs-git": 1, "R-vend-installed": 2, "R-gen-build-output-no-source": 1, "R-gen-tool-cache": 1, "R-run-log": 2,
                   "R-run-openlineage-event": 1, "R-run-heap-dump": 1, "R-backup-dir": 1, "R-backup-file": 1, "(none)": 3}
    assert c["by_role"]["unclassified"]["files"] == 3                          # svc/src/main.py, README.md, wt-feature/src/a.py
    c2, _ = run(load_profile("egeria-workspace", PROFILES), tmp_path, rows, "ws")      # with the workspace profile the copy is claimed
    assert c2["by_rule"]["R-copy-worktree-name-only"]["files"] == 1 and c2["by_role"]["unclassified"]["files"] == 2      # M5b: the name alone is shown
    assert c["components"] == {"top_level": 0, "parts": 0}
