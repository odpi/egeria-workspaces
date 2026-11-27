"""M5c (Dan, 2026-11-26, after the third draw): build output is also hidden when a build-tool layout folder is inside it or when it is orphaned; everything under
runtime-volumes is hidden runtime data in the egeria-workspace profile only; there is no name-only `logs` rule. Synthetic only."""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from recognizer.layout_profile import ProfileError, load_profile, parse_profile
from recognizer.recognize import Recognizer

PROFILES = Path(__file__).resolve().parent.parent / "profiles"


def run(tmp_path, rows, profile="egeria-workspace", out="out"):
    lst = tmp_path / f"{out}.tsv"
    lst.write_text("".join(f"{r}\n" for r in sorted(set(rows))))
    c = Recognizer(load_profile(profile, PROFILES)).run(lst, tmp_path / out, per_file=True)
    pf = {x["path"]: x for x in map(json.loads, (tmp_path / out / "findings-files.jsonl").read_text().splitlines())}
    return SimpleNamespace(c=c, pf=pf)


def rid(r, path):
    return (r.pf[path]["rule_id"], r.pf[path]["relevance"]) if path in r.pf else None


# ---- (a) a build-tool layout folder inside ------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("child", ["classes", "libs", "tmp", "reports", "generated", "docs/javadoc"])
def test_a_gradle_build_folder_with_a_listed_layout_child_is_hidden(tmp_path, child):
    r = run(tmp_path, [f"mod/build/{child}/x.dat", "mod/build/other.py", "mod/README.txt", "mod2/readme.txt"])         # source-like file inside, no manifest, a sibling: only the layout corroborates
    assert rid(r, "mod/build/other.py") == ("R-gen-build-output-gradle-layout", "hidden") and rid(r, f"mod/build/{child}/x.dat")[1] == "hidden"


@pytest.mark.parametrize("child", ["classes", "test-classes", "maven-status"])
def test_a_maven_target_folder_with_a_listed_layout_child_is_hidden(tmp_path, child):
    r = run(tmp_path, [f"mod/target/{child}/x.dat", "mod/target/other.py", "mod/README.txt", "mod2/readme.txt"])
    assert rid(r, "mod/target/other.py") == ("R-gen-build-output-maven-layout", "hidden")


@pytest.mark.parametrize("path", ["mod/build/test-classes/x.py", "mod/build/maven-status/x.py", "mod/target/libs/x.py", "mod/target/tmp/x.py", "mod/target/docs/javadoc/x.py",
                                  "mod/build/docs/other/x.py", "mod/build/docs/x.py", "mod/build/classes.py", "mod/build/my-classes/x.py"])
def test_a_name_that_is_not_in_the_list_for_that_tool_does_not_corroborate(tmp_path, path):
    r = run(tmp_path, [path, "mod/README.txt", "mod2/readme.txt"])
    assert rid(r, path) == ("R-gen-build-output-unconfirmed", "supporting")                                         # Dan's list, exactly: maven names do not corroborate build/, and the reverse


def test_a_layout_child_must_be_a_folder_directly_inside_not_deeper_and_dist_has_no_layout_list(tmp_path):
    r = run(tmp_path, ["a/build/sub/classes/x.py", "a/keep.txt", "b/dist/classes/y.py", "b/keep.txt"])
    assert rid(r, "a/build/sub/classes/x.py")[0] == "R-gen-build-output-unconfirmed"                                # classes is two levels down
    assert rid(r, "b/dist/classes/y.py")[0] == "R-gen-build-output-unconfirmed"                                     # dist has no layout list; Dan's word is needed for one


# ---- (b) orphaned output --------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("name", ["build", "target", "dist", ".next"])
def test_a_build_folder_that_is_the_only_thing_in_its_parent_is_hidden(tmp_path, name):
    r = run(tmp_path, [f"gone-module/{name}/tool.py", "other/README.txt"])
    assert rid(r, f"gone-module/{name}/tool.py") == ("R-gen-build-output-orphaned", "hidden")


def test_a_parent_that_holds_another_file_or_folder_is_not_an_orphan(tmp_path):
    r = run(tmp_path, ["f/build/a.py", "f/notes.txt", "d/build/a.py", "d/src/b.txt", "ok/build/a.py", "ok/build2/x"])
    for p in ("f/build/a.py", "d/build/a.py", "ok/build/a.py"):
        assert rid(r, p) == ("R-gen-build-output-unconfirmed", "supporting"), p


def test_the_layout_rule_is_checked_before_the_orphan_rule_and_the_older_corroborations_first(tmp_path):
    r = run(tmp_path, ["m/build/classes/x.class", "m2/package.json", "m2/build/y.py", "m3/target/a.class", "m3/target/b.class", "z/readme.txt"])
    assert rid(r, "m/build/classes/x.class")[0] == "R-gen-build-output-no-source"                                    # no source-like file: the earlier rule claims it
    assert rid(r, "m2/build/y.py")[0] == "R-gen-build-output"                                                       # a manifest beside it
    assert rid(r, "m3/target/a.class")[0] == "R-gen-build-output-no-source"


def test_the_root_of_the_scanned_tree_counts_as_a_parent(tmp_path):
    assert rid(run(tmp_path, ["build/a.py"]), "build/a.py")[0] == "R-gen-build-output-orphaned"
    assert rid(run(tmp_path, ["build/a.py", "README.md"], out="o2"), "build/a.py")[0] == "R-gen-build-output-unconfirmed"


# ---- runtime-volumes: the workspace profile only; no name-only logs rule -----------------------------------------------------------------------------
@pytest.mark.parametrize("path", ["runtime-volumes/db/data.bin", "repo/runtime-volumes/cfg/app.yaml", "a/b/runtime-volumes/x", "repo/runtime-volumes/svc/state/x.json"])
def test_everything_under_runtime_volumes_is_hidden_runtime_data_in_the_workspace_profile(tmp_path, path):
    f = run(tmp_path, [path]).pf[path]
    assert f["rule_id"] == "R-run-volume-data" and f["role"] == "runtime-output" and f["relevance"] == "hidden"


@pytest.mark.parametrize("path", ["runtime-volumes-old/x", "repo/xruntime-volumes/y", "repo/runtime_volumes/z", "repo/volumes/runtime-volumes.txt"])
def test_whole_segments_only(tmp_path, path):
    assert path not in run(tmp_path, [path]).pf


def test_earlier_rules_keep_their_files_and_the_logs_rule_still_comes_first(tmp_path):
    r = run(tmp_path, ["repo/runtime-volumes/svc/logs/a", "repo/runtime-volumes/svc/x.log", "repo/runtime-volumes/svc/node_modules/p/i.js", "repo/runtime-volumes/svc/state/s"])
    assert rid(r, "repo/runtime-volumes/svc/logs/a")[0] == "R-run-volume-logs" and rid(r, "repo/runtime-volumes/svc/x.log")[0] == "R-run-log"
    assert rid(r, "repo/runtime-volumes/svc/node_modules/p/i.js")[0] == "R-vend-installed" and rid(r, "repo/runtime-volumes/svc/state/s")[0] == "R-run-volume-data"


def test_generic_relevance_does_not_hide_runtime_volumes_wholesale_and_has_no_name_only_logs_rule(tmp_path):
    g = load_profile("generic-relevance", PROFILES)
    assert "R-run-volume-data" not in {r.id for r in g.rules} and "R-run-volume-logs" in {r.id for r in g.rules}
    r = run(tmp_path, ["repo/runtime-volumes/svc/state/s", "repo/runtime-volumes/svc/logs/a", "repo/logs/a", "svc/logs/b.txt"], profile="generic-relevance")
    assert rid(r, "repo/runtime-volumes/svc/state/s") is None and rid(r, "repo/runtime-volumes/svc/logs/a")[0] == "R-run-volume-logs"
    ws = run(tmp_path, ["repo/logs/a", "svc/logs/b.txt", "repo/src/logs/c.py"], out="o2")
    assert all(p not in ws.pf for p in ("repo/logs/a", "svc/logs/b.txt", "repo/src/logs/c.py"))                    # a folder named logs elsewhere stays shown (Dan: no)
    assert not [x for x in load_profile("egeria-workspace", PROFILES).rules if x.match.get("name") == "logs" or x.match.get("path_segment") == "logs"]


def test_the_workspace_data_rule_is_composed_last_and_carries_provenance():
    p = load_profile("egeria-workspace", PROFILES)
    ids = [r.id for r in p.rules]
    assert p.version == "0.4.0" and ids[-1] == "R-run-volume-data" and ids.index("R-run-volume-logs") < ids.index("R-run-volume-data")
    rule = [r for r in p.rules if r.id == "R-run-volume-data"][0]
    assert rule.tuned_on == ("egeria-v6 third draw (c67c74a8)",) and rule.relevance == "hidden" and rule.origin == "workspace-runtime-data"
    g = load_profile("generic-relevance", PROFILES)
    by = {r.id: r for r in g.rules}
    for k in ("R-gen-build-output-gradle-layout", "R-gen-build-output-maven-layout", "R-gen-build-output-orphaned"):
        assert by[k].tuned_on == ("egeria-v6 third draw (c67c74a8)",) and by[k].relevance == "hidden" and by[k].grain == "subtree"
    assert by["R-gen-build-output-gradle-layout"].child_dirs == frozenset({"classes", "libs", "tmp", "reports", "generated", "docs/javadoc"})
    assert by["R-gen-build-output-maven-layout"].child_dirs == frozenset({"classes", "test-classes", "maven-status"})
    ids_g = [r.id for r in g.rules]
    assert ids_g.index("R-gen-build-output-no-source") < ids_g.index("R-gen-build-output-gradle-layout") < ids_g.index("R-gen-build-output-orphaned") < ids_g.index("R-gen-build-output-unconfirmed")


# ---- the new match keys ----------------------------------------------------------------------------------------------------------------------
def _doc(match):
    return {"profile_id": "t", "version": "0.1.0", "status": "proposed", "applies_to": "any", "roles": ["generated"], "relevance": {"primary": [], "supporting": [], "hidden": ["generated"]},
            "rules": [{"id": "R-x", "match": match, "assign": {"role": "generated"}, "grain": "subtree", "basis": "convention", "confidence": "low", "evidence": "e"}]}


def test_has_child_dir_and_orphaned_are_validated():
    assert parse_profile(_doc({"name": "build", "has_child_dir": ["a", "b/c"]})).rules[0].child_dirs == frozenset({"a", "b/c"})
    assert parse_profile(_doc({"name": "build", "orphaned": True})).rules[0].orphaned
    for bad in ({"name": "b", "orphaned": False}, {"name": "b", "has_child_dir": ["/abs"]}, {"name": "b", "has_child_dir": ["a/../b"]}, {"name": "b", "has_child_dir": ["a/"]},
                {"name": "b", "has_child_dir": [""]}, {"name": "b", "has_child_dir": [3]}):
        with pytest.raises(ProfileError):
            parse_profile(_doc(bad))
