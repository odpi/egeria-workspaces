"""M5: the FILE-ROLE layer of code-repo-conventions 0.2.0 and the four hidden rules of generic-relevance 0.3.0. Synthetic path lists only."""
import json
from pathlib import Path

import pytest
import yaml

from recognizer.layout_profile import ProfileError, load_profile, parse_profile
from recognizer.recognize import Recognizer

PROFILES = Path(__file__).resolve().parent.parent / "profiles"


def run(tmp_path, rows, profile="code-repo-conventions", out="out", prof=None):
    p = tmp_path / f"{out}.tsv"
    p.write_text("".join(f"{r}\n" for r in sorted(set(rows))))
    c = Recognizer(prof or load_profile(profile, PROFILES)).run(p, tmp_path / out, per_file=True)
    per_file = {}
    for line in (tmp_path / out / "findings-files.jsonl").read_text().splitlines():
        f = json.loads(line)
        per_file[f["path"]] = f
    return c, per_file


def roles(tmp_path, rows, **kw):
    c, pf = run(tmp_path, rows, **kw)
    return {p: (f["role"], f["rule_id"]) for p, f in pf.items()}


# ---- the file-role layer ---------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("path,role", [
    (".github/workflows/ci.yml", "ci"), (".circleci/config.yml", "ci"), (".gitlab-ci.yml", "ci"), ("Jenkinsfile", "ci"),
    ("tests/a.py", "test"), ("pkg/test/a.java", "test"), ("web/__tests__/a.js", "test"), ("pkg/src/test/java/A.java", "test"),
    ("src/test/java/A.java", "test"), ("pkg/test_a.py", "test"), ("pkg/a_test.py", "test"), ("pkg/a_test.go", "test"),
    ("web/a.test.ts", "test"), ("web/a.spec.tsx", "test"),
    ("docs/a.png", "docs"), ("doc/x.txt", "docs"), ("README.md", "docs"), ("LICENSE", "docs"), ("LICENSE-APACHE", "docs"), ("pkg/NOTES.rst", "docs"),
    ("a/b/c.yaml", "config"), ("a.yml", "config"), ("x/y.toml", "config"), ("tox.ini", "config"), (".editorconfig", "config"),
    ("package.json", "build"), ("pkg/pyproject.toml", "build"), ("x/Cargo.toml", "build"), ("chart/Chart.yaml", "build"), ("setup.cfg", "build"), ("pom.xml", "build"), ("Makefile", "build"), ("Dockerfile", "build"), ("Dockerfile.base", "build"),
    ("app/build.gradle", "build"), ("app/build.gradle.kts", "build"), ("gradlew", "build"),
    ("src/a.txt", "source"), ("lib/b.dat", "source"), ("pkg/a.py", "source"), ("pkg/a.ts", "source"), ("pkg/A.java", "source"),
])
def test_each_path_pattern_gives_its_role(tmp_path, path, role):
    rows = [path, "pkg/pyproject.toml", "app/build.gradle"]         # a component exists, so a source extension under it is source
    got = roles(tmp_path, rows)
    assert got[path][0] == role, got[path]


def test_first_match_order_is_ci_test_docs_build_config_source_other(tmp_path):
    got = roles(tmp_path, [".github/tests/a.py", "tests/README.md", "docs/a.py", "docs/x.yaml", "pkg/pyproject.toml", "pkg/a.py", "z/odd.xyz"])
    assert got[".github/tests/a.py"][0] == "ci"                   # ci before test
    assert got["tests/README.md"][0] == "test"                    # test before docs
    assert got["docs/a.py"][0] == "docs"                          # docs before source
    assert got["docs/x.yaml"][0] == "docs"                        # docs before config
    assert got["pkg/pyproject.toml"][0] == "build"                # 0.3.0: exact manifest names are build BEFORE the config extensions
    assert got["pkg/a.py"][0] == "source"
    assert got["z/odd.xyz"] == ("other", "F-other")
    assert roles(tmp_path, ["a/x.yaml", "a/Chart.yaml"], out="b")["a/x.yaml"][0] == "config"      # a plain .yaml is still config


def test_a_source_extension_needs_a_component_a_dotfile_needs_a_component_root(tmp_path):
    got = roles(tmp_path, ["loose/a.py", "pkg/pyproject.toml", "pkg/b.py", "pkg/.gitignore", "pkg/sub/.gitignore", "other/.hidden"])
    assert got["loose/a.py"][0] == "other"                         # under no component
    assert got["pkg/b.py"][0] == "source"
    assert got["pkg/.gitignore"][0] == "config"                    # directly in a component's directory
    assert got["pkg/sub/.gitignore"][0] == "other"                 # inside a component but not at its root
    assert got["other/.hidden"][0] == "other"


def test_other_is_classified_reported_separately_and_unclassified_is_zero(tmp_path):
    c, pf = run(tmp_path, ["z/a.xyz", "z/b.xyz", "pkg/pyproject.toml", "pkg/a.py"])
    assert c["by_role"]["other"]["files"] == 2 and "unclassified" not in c["by_role"]
    assert c["shares"]["unclassified_files"] == 0.0 and c["shares"]["other_files"] == 0.5
    assert c["shares"]["classified_files"] == 1.0
    assert "other 50.0%" in (tmp_path / "out" / "report.md").read_text()


def test_the_shares_have_no_other_key_for_a_profile_without_file_roles(tmp_path):
    c, pf = run(tmp_path, ["a/b.py"], profile="generic-relevance")
    assert "other_files" not in c["shares"] and c["shares"]["unclassified_files"] == 1.0


def test_file_roles_never_change_the_components(tmp_path):
    rows = ["pyproject.toml", "pkg/pyproject.toml", "pkg/a.py", "docs/index.md", "tests/t.py", "docker/Dockerfile", "ui/package.json", "ui/src/a.ts",
            "x/examples/e/pyproject.toml", "node_modules/m/package.json"]
    c1, _ = run(tmp_path, rows, out="with")
    doc = yaml.safe_load((PROFILES / "code-repo-conventions.yaml").read_text())
    doc.pop("file_roles")
    c2, _ = run(tmp_path, rows, out="without", prof=parse_profile(doc, "no-file-roles", PROFILES))
    for n in ("components.txt", "components-all.txt"):
        assert (tmp_path / "with" / n).read_bytes() == (tmp_path / "without" / n).read_bytes()
    assert c2["by_role"].get("unclassified", {}).get("files", 0) > 0        # the same list had unclassified files before the layer


def test_file_roles_never_unhide_a_hidden_file(tmp_path):
    rows = ["node_modules/p/tests/a.py", "build/out/docs/x.md", "pkg/pyproject.toml", "pkg/.pytest_cache/v/x.json", "pkg/a.py"]
    got = roles(tmp_path, rows)
    assert got["node_modules/p/tests/a.py"] == ("vendored", "R-vend-installed")
    assert got["build/out/docs/x.md"][1] == "R-gen-build-output-no-source"     # no manifest beside it, but no source below it either
    assert got["pkg/.pytest_cache/v/x.json"][1] == "R-gen-tool-cache"
    assert got["pkg/a.py"][0] == "source"


def test_every_file_role_rule_carries_evidence_basis_confidence_and_tuned_on():
    p = load_profile("code-repo-conventions", PROFILES)
    assert p.version == "0.3.0" and len(p.file_roles) >= 12
    for r in p.file_roles:
        assert r.id.startswith("F-") and r.evidence.strip() and r.basis and r.confidence and r.tuned_on, r.id
        assert r.grain == "dir" and not r.is_dir_rule


def test_the_file_role_findings_are_stable_and_deterministic(tmp_path):
    rows = ["pkg/pyproject.toml", "pkg/a.py", "tests/t.py", "x/y.bin"]
    c1, f1 = run(tmp_path, rows, out="a")
    c2, f2 = run(tmp_path, rows, out="b")
    assert c1 == c2 and f1 == f2
    assert (tmp_path / "a" / "findings.jsonl").read_bytes() == (tmp_path / "b" / "findings.jsonl").read_bytes()


# ---- the loader -----------------------------------------------------------------------------------------------------------------
def _doc(**extra):
    d = {"profile_id": "t", "version": "0.1.0", "status": "proposed", "applies_to": "code-repo", "roles": ["source", "other"],
         "relevance": {"primary": [], "supporting": ["source", "other"], "hidden": []}, "rules": [], "file_roles": []}
    d.update(extra)
    return d


def _fr(**over):
    r = {"id": "F-a", "match": {"extension": ".py"}, "assign": {"role": "source"}, "grain": "dir", "basis": "convention",
         "confidence": "high", "evidence": "py is source"}
    r.update(over)
    return r


def test_a_file_role_rule_is_loaded_and_ids_are_unique_across_both_lists():
    p = parse_profile(_doc(file_roles=[_fr()]), "t")
    assert [r.id for r in p.file_roles] == ["F-a"]
    with pytest.raises(ProfileError, match="used twice"):
        parse_profile(_doc(file_roles=[_fr(), _fr()]), "t")
    with pytest.raises(ProfileError, match="used twice"):
        parse_profile(_doc(rules=[_fr(id="F-a")], file_roles=[_fr()]), "t")


@pytest.mark.parametrize("bad,msg", [
    (_fr(match={"has_file": "x"}), "FILE"),                                   # a directory test is not a file role
    (_fr(grain="subtree", match={"path_segment": "x"}), "grain 'dir'"),
    (_fr(match={"extension": ".py", "component_scope": "nowhere"}), "component_scope"),
    (_fr(role_typo=1), "unknown key"),
])
def test_a_bad_file_role_rule_is_a_load_error(bad, msg):
    with pytest.raises(ProfileError, match=msg):
        parse_profile(_doc(file_roles=[bad]), "t")


def test_component_scope_on_a_directory_rule_is_rejected():
    rule = _fr(id="R-x", match={"has_file": "setup.py", "component_scope": "within"}, assign={"role": "other"})
    with pytest.raises(ProfileError, match="component_scope"):
        parse_profile(_doc(rules=[rule]), "t")


def test_file_roles_are_inherited_and_a_diamond_loads_them_once(tmp_path):
    for name, extends in (("base", []), ("left", ["base"]), ("right", ["base"]), ("top", ["left", "right"])):
        d = _doc(profile_id=name, extends=extends, file_roles=[_fr(id="F-" + name)])
        (tmp_path / f"{name}.yaml").write_text(yaml.safe_dump(d))
    p = load_profile("top", tmp_path)
    assert [r.id for r in p.file_roles] == ["F-top", "F-left", "F-base", "F-right"]


# ---- the four hidden rules of generic-relevance 0.3.0 ----------------------------------------------------------------------------
def ws(tmp_path, rows):
    return roles(tmp_path, rows, profile="egeria-workspace")


def test_a_nested_repository_is_hidden_but_a_repository_directly_under_a_workspace_root_is_not(tmp_path):
    rows = ["trellis/.git/HEAD", "trellis/a.py", "trellis/vendor/lib/.git", "trellis/vendor/lib/x.py", "trellis/data/clone/.git/HEAD",
            "trellis/data/clone/y.py", "other/.git/HEAD", "other/z.py"]
    got = ws(tmp_path, rows)
    assert "trellis/a.py" not in got                                           # no rule claims it: it stays unclassified
    assert "other/z.py" not in got                                             # a repository under a workspace that is not itself a repository
    assert got["trellis/vendor/lib/x.py"] == ("vendored", "R-vend-nested-repo")       # a .git FILE counts like a .git directory
    assert got["trellis/data/clone/y.py"] == ("vendored", "R-vend-nested-repo")
    assert got["trellis/.git/HEAD"] == ("vcs-internal", "R-vcs-git")           # the old rule keeps the .git internals


def test_the_scanned_roots_own_git_makes_every_repository_below_it_nested(tmp_path):
    got = ws(tmp_path, [".git/HEAD", "a.py", "sub/.git", "sub/b.py", "plain/c.py"])
    assert got[".git/HEAD"][1] == "R-vcs-git"
    assert got["sub/b.py"] == ("vendored", "R-vend-nested-repo")
    assert "a.py" not in got and "plain/c.py" not in got


def test_vendored_wins_over_a_manifest_inside_a_nested_repository(tmp_path):
    rows = ["outer/.git/HEAD", "outer/pyproject.toml", "outer/in/.git", "outer/in/pyproject.toml", "outer/in/a.py", "outer/in/pkg/pyproject.toml"]
    c, pf = run(tmp_path, rows, profile="code-repo-conventions")
    comps = (tmp_path / "out" / "components-all.txt").read_text().split()
    assert "outer" in comps and "outer/in" not in comps and "outer/in/pkg" not in comps
    assert pf["outer/in/a.py"]["rule_id"] == "R-vend-nested-repo" and pf["outer/in/a.py"]["relevance"] == "hidden"


def test_an_old_hiding_rule_keeps_its_file_when_a_new_rule_would_also_match(tmp_path):
    got = ws(tmp_path, ["r/.git/HEAD", "r/in/.git", "r/in/node_modules/m/a.js", "r/in/run.log", "r/in/b.py", "r/.claude/worktrees/w/.git/HEAD",
                        "r/.claude/worktrees/w/c.py"])
    assert got["r/in/node_modules/m/a.js"][1] == "R-vend-installed"
    assert got["r/in/run.log"][1] == "R-run-log"
    assert got["r/.claude/worktrees/w/.git/HEAD"][1] == "R-vcs-git"
    assert got["r/in/b.py"][1] == "R-vend-nested-repo"
    assert got["r/.claude/worktrees/w/c.py"] == ("worktree-copy", "R-wt-claude-worktree")      # specific-first: before the broad nested-repo rule


@pytest.mark.parametrize("path", [".claude/worktrees/anything/a.py", "repo/.claude/worktrees/any-name/deep/a.py", "r/.claude/worktrees/wt-x/a/b/c.txt"])
def test_claude_worktrees_are_copies_whatever_they_are_named(tmp_path, path):
    assert ws(tmp_path, [path])[path] == ("worktree-copy", "R-wt-claude-worktree")


@pytest.mark.parametrize("path", ["repo/.claude/settings.json", "repo/.claude/worktrees-notes/a.md", "repo/not.claude/worktrees/x/a.py", "repo/.claude/worktrees/lonely.txt"])
def test_other_claude_paths_are_not_worktree_copies(tmp_path, path):
    assert path not in ws(tmp_path, [path])


@pytest.mark.parametrize("path", [".idea/workspace.xml", "repo/.idea/misc.xml", "repo/sub/.idea/deep/x"])
def test_idea_is_hidden_tooling(tmp_path, path):
    c, pf = run(tmp_path, [path], profile="egeria-workspace")
    assert pf[path]["rule_id"] == "R-tool-idea" and pf[path]["role"] == "tooling" and pf[path]["relevance"] == "hidden"


@pytest.mark.parametrize("path", ["runtime-volumes/logs/x", "runtime-volumes/svc/logs/Z.out", "repo/runtime-volumes/svc/a/logs/no-suffix",
                                  "repo/runtime-volumes/logs/dir/f"])
def test_logs_under_runtime_volumes_are_runtime_output_with_or_without_a_suffix(tmp_path, path):
    assert ws(tmp_path, [path])[path] == ("runtime-output", "R-run-volume-logs")


@pytest.mark.parametrize("path", ["runtime-volumes-old/logs/x", "repo/runtime-volumes/svc/mylogs/x", "repo/runtime-volumes/svc/logs-old/x", "repo/logs/x",
                                  "repo/runtime-volumes/data/x"])
def test_the_runtime_logs_rule_matches_whole_path_segments_under_runtime_volumes_only(tmp_path, path):
    assert path not in ws(tmp_path, [path])


def test_nothing_the_old_rules_hid_becomes_unhidden(tmp_path):
    rows = ["a/.git/HEAD", "a/node_modules/x/y.js", "a/build/o.class", "a/__pycache__/m.pyc", "a/e.openlineageevent", "a/h.hprof", "a/l.log", "a/db-backups/d",
            "a/x.bak", "wt-1/a.py", "a/.claude/worktrees/w/b.py", "a/.idea/x", "a/runtime-volumes/logs/z", "a/b/.git"]
    new = Recognizer(load_profile("egeria-workspace", PROFILES))
    p = tmp_path / "l.tsv"
    p.write_text("".join(f"{r}\n" for r in sorted(rows)))
    new.run(p, tmp_path / "o", per_file=True)
    got = {json.loads(l)["path"]: json.loads(l) for l in (tmp_path / "o" / "findings-files.jsonl").read_text().splitlines()}
    # (M5b un-hides on purpose: the name-only worktree copy `wt-1` is now SHOWN; see test_m5b. The rules that were not tightened still hide as before.)
    for path in ("a/.git/HEAD", "a/node_modules/x/y.js", "a/build/o.class", "a/__pycache__/m.pyc", "a/e.openlineageevent", "a/h.hprof", "a/l.log",
                 "a/db-backups/d", "a/x.bak"):
        assert got[path]["relevance"] == "hidden", path
    old_ids = {"R-vcs-git", "R-vend-installed", "R-gen-build-output-no-source", "R-gen-tool-cache", "R-run-openlineage-event", "R-run-heap-dump", "R-run-log",
               "R-backup-dir", "R-backup-file"}
    assert {got[p]["rule_id"] for p in ("a/.git/HEAD", "a/node_modules/x/y.js", "a/build/o.class")} <= old_ids


def test_the_new_rules_carry_evidence_and_the_sample_they_came_from():
    p = load_profile("generic-relevance", PROFILES)
    new = [r for r in p.rules if r.id in ("R-wt-claude-worktree", "R-tool-idea", "R-run-volume-logs", "R-vend-nested-repo")]
    assert len(new) == 4 and p.version == "0.4.0"
    assert all(r.relevance == "hidden" and r.grain == "subtree" and r.evidence and r.tuned_on == ("egeria-v6 stratified sample (6994dff1)",) for r in new)
    assert [r.id for r in p.rules][-4:] == ["R-wt-claude-worktree", "R-tool-idea", "R-run-volume-logs", "R-vend-nested-repo"]     # after every older rule
