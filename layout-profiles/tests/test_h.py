"""Phase 1h. H1: a top-level scripts/ (or script/, scripts-*, scripts_*, script-*, script_*) folder is role tooling, kind maintenance-scripts, not a component, and
R-tool-package's segment list gains the same forms. The folder stays a file-role scope (rule option file_scope), so its files keep their roles. Synthetic trees only."""
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from recognizer import manifests as mf
from recognizer.layout_profile import ProfileError, compose_profiles, load_profile
from recognizer.recognize import Recognizer

PROFILES = Path(__file__).resolve().parent.parent / "profiles"


def survey(tmp_path, files, out="out", name="tree", profile="code-repo-conventions"):
    root = tmp_path / name
    for rel, content in files.items():
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content)
    lst = tmp_path / f"{name}.tsv"
    lst.write_text("".join(f"{p}\t{len(files[p].encode())}\n" for p in sorted(files)))
    prof = compose_profiles(profile, PROFILES) if "," in profile else load_profile(profile, PROFILES)
    rec = Recognizer(prof, blob_source=mf.FileSource(str(root)))
    c = rec.run(lst, tmp_path / out)
    findings = [json.loads(x) for x in (tmp_path / out / "findings.jsonl").read_text().splitlines()]
    f = {x["path"]: x for x in findings if not x["rule_id"].startswith("F-")}
    rule = {p: (rec.classify(p)[0].id if rec.classify(p)[0] else None) for p in files}
    role = {p: (rec.classify(p)[0].role if rec.classify(p)[0] else None) for p in files}
    return SimpleNamespace(c=c, f=f, rec=rec, rule=rule, role=role,
                           allc=(tmp_path / out / "components-all.txt").read_text().split(), top=(tmp_path / out / "components.txt").read_text().split())


PY_ROOT = {"pyproject.toml": "[project]\nname='r'\n", "core/pyproject.toml": "[project]\nname='c'\n"}


def is_tooling(r, d):
    return d not in r.allc and d not in r.top and r.f.get(d, {}).get("role") == "tooling"


# ======================================================================== H1 ========================================================================================
# ---- (1) scripts/a.py + scripts/b.sh: not a component, role tooling; the files keep their roles (with and without a root component)
@pytest.mark.parametrize("root", [PY_ROOT, {"core/pyproject.toml": "[project]\nname='c'\n"}])
def test_scripts_folder_is_tooling_and_its_files_keep_their_roles(tmp_path, root):
    r = survey(tmp_path, {**root, "scripts/a.py": "x", "scripts/b.sh": "x"})
    assert is_tooling(r, "scripts") and r.f["scripts"]["rule_id"] == "R-conv-scripts" and r.f["scripts"]["kind"] == "maintenance-scripts"
    assert r.rule["scripts/a.py"] == "F-source-ext" and r.rule["scripts/b.sh"] == "F-source-ext"      # file_scope: classified as before H1 (a component's files)


# ---- (2) scripts/build.gradle.kts included in the build: tooling, not a component
def test_a_gradle_project_in_scripts_included_in_the_build_is_tooling(tmp_path):
    r = survey(tmp_path, {"build.gradle": "", "settings.gradle": "include 'core', 'scripts'\n", "core/build.gradle": "", "scripts/build.gradle.kts": ""})
    assert is_tooling(r, "scripts") and "core" in r.allc


# ---- (3) scripts-ts/package.json + src/x.ts: tooling; its src is not a component either (Architect ruling (B): R-conv-node-src skips a src whose parent is tooling)
def test_a_scripts_dash_package_and_its_src_are_not_components(tmp_path):
    r = survey(tmp_path, {**PY_ROOT, "scripts-ts/package.json": '{"name": "x"}', "scripts-ts/src/x.ts": "x"})
    assert is_tooling(r, "scripts-ts") and "scripts-ts/src" not in r.allc and "scripts-ts/src" not in r.f


def test_a_tools_package_and_its_src_are_not_components(tmp_path):
    r = survey(tmp_path, {**PY_ROOT, "tools/package.json": '{"name": "x"}', "tools/src/a.ts": "x"})
    assert is_tooling(r, "tools") and r.f["tools"]["rule_id"] == "R-tool-package" and "tools/src" not in r.allc and "tools/src" not in r.f


def test_control_an_app_src_is_still_a_component(tmp_path):
    r = survey(tmp_path, {**PY_ROOT, "app/package.json": '{"name": "x"}', "app/src/a.ts": "x"})
    assert "app/src" in r.allc and r.f["app/src"]["rule_id"] == "R-conv-node-src" and "app" in r.allc


# ---- (4) script/run.sh: tooling
def test_a_script_folder_is_tooling(tmp_path):
    r = survey(tmp_path, {**PY_ROOT, "script/run.sh": "x"})
    assert is_tooling(r, "script") and r.rule["script/run.sh"] == "F-source-ext"


@pytest.mark.parametrize("name", ["scripts", "script", "Scripts", "SCRIPT", "scripts-ts", "scripts_dev", "script-utils", "script_x"])
def test_every_top_level_form_is_tooling(tmp_path, name):
    r = survey(tmp_path, {**PY_ROOT, f"{name}/run.sh": "x"})
    assert is_tooling(r, name)


@pytest.mark.parametrize("name", ["scripts-ts", "scripts_dev", "script-utils", "script"])
def test_a_manifest_project_under_a_new_form_is_tooling_at_any_depth(tmp_path, name):
    r = survey(tmp_path, {**PY_ROOT, f"pkg/{name}/p/package.json": '{"name": "x"}'})
    assert f"pkg/{name}/p" not in r.allc and r.f[f"pkg/{name}/p"]["rule_id"] == "R-tool-package"


# ---- (5) NOT matched: myscripts/, src/scripts/ (not top level: existing behaviour stands), postscript/, scriptsfoo/
@pytest.mark.parametrize("path", ["myscripts/run.sh", "postscript/run.sh", "scriptsfoo/run.sh", "scripting/run.sh", "descripts/run.sh"])
def test_other_names_are_not_matched(tmp_path, path):
    d = path.split("/")[0]
    r = survey(tmp_path, {**PY_ROOT, path: "x"})
    assert r.f.get(d, {}).get("rule_id") != "R-conv-scripts"


def test_a_nested_scripts_folder_keeps_the_existing_behaviour(tmp_path):
    r = survey(tmp_path, {**PY_ROOT, "src/scripts/run.sh": "x", "src/scripts/p/package.json": '{"name": "x"}', "pkg/myscripts/q/package.json": '{"name": "y"}'})
    assert "src/scripts" not in r.f                                                   # no rule claims the folder itself, as before
    assert r.f["src/scripts/p"]["rule_id"] == "R-tool-package"                        # a package under any scripts segment was tooling before H1 too
    assert "pkg/myscripts/q" in r.allc                                                # myscripts is not a scripts segment


@pytest.mark.parametrize("name", ["myscripts", "postscript", "scriptsfoo"])
def test_other_names_with_a_manifest_stay_components(tmp_path, name):
    r = survey(tmp_path, {**PY_ROOT, f"{name}/package.json": '{"name": "x"}'})
    assert name in r.allc and r.f[name]["role"] == "component"


# ---- (6) the finding id of an unaffected component does not change
def test_h1_leaves_finding_ids_of_unaffected_components_unchanged(tmp_path):
    files1 = {**PY_ROOT, "lib/pom.xml": "<project/>"}
    r1 = survey(tmp_path, files1, out="r1", name="tree1")
    r2 = survey(tmp_path, {**files1, "scripts/run.sh": "x", "scripts-ts/package.json": '{"name": "x"}'}, out="r2", name="tree2")
    assert load_profile("code-repo-conventions", PROFILES).major == "0"
    for d in ("core", "lib"):
        rid = r1.f[d]["rule_id"]
        assert r1.f[d]["finding_id"] == r2.f[d]["finding_id"] == hashlib.sha256(f"code-repo-conventions@0|{rid}|{d}".encode()).hexdigest()[:16]


def test_h1_in_the_composite_profile(tmp_path):
    r = survey(tmp_path, {**PY_ROOT, "scripts/a.py": "x"}, profile="code-repo-conventions,docs-site")
    assert is_tooling(r, "scripts") and r.rule["scripts/a.py"] == "F-source-ext"


def test_the_h1_rule_carries_provenance_and_the_known_limit():
    p = load_profile("code-repo-conventions", PROFILES)
    r = {x.id: x for x in p.rules}["R-conv-scripts"]
    assert p.version == "0.9.0" and r.role == "tooling" and r.kind == "maintenance-scripts" and r.grain == "dir" and r.file_scope
    assert "Known limit" in r.evidence and any(t.startswith("Phase 1h H1") for t in r.tuned_on)


# ---- file_scope: validated by the loader
def _prof(tmp_path, rule):
    import yaml
    base = {"profile_id": "t", "version": "0.1.0", "status": "proposed", "applies_to": "any", "roles": ["component", "tooling"],
            "relevance": {"primary": ["component"], "supporting": ["tooling"], "hidden": []}}
    (tmp_path / "t.yaml").write_text(yaml.safe_dump({**base, "rules": [{"id": "R", "basis": "convention", "confidence": "low", "evidence": "x", **rule}]}))
    return load_profile("t", tmp_path)


@pytest.mark.parametrize("rule", [
    {"match": {"segment_regex": "x"}, "assign": {"role": "tooling"}, "grain": "dir", "file_scope": "yes"},
    {"match": {"segment_regex": "x"}, "assign": {"role": "component"}, "grain": "dir", "file_scope": True},      # role component
    {"match": {"segment_regex": "x"}, "assign": {"role": "tooling"}, "grain": "dir", "file_scope": 1},
    {"match": {"name": "x.py"}, "assign": {"role": "tooling"}, "grain": "dir", "file_scope": True},             # a file rule
    {"match": {"path_glob": "x"}, "assign": {"role": "component"}, "grain": "component", "file_scope": True},  # grain component
])
def test_file_scope_is_validated(tmp_path, rule):
    with pytest.raises(ProfileError):
        _prof(tmp_path, rule)


# ---- file_scope is off when absent: a tooling claim WITHOUT it (R-tool-package) is no file-role scope, as before H1
def test_file_scope_is_off_when_absent(tmp_path):
    r = survey(tmp_path, {"core/pyproject.toml": "[project]\nname='c'\n", "tools/package.json": '{"name": "x"}', "tools/a.py": "x", "scripts/b.py": "x"})
    assert is_tooling(r, "tools") and not {x.id: x for x in r.rec.p.rules}["R-tool-package"].file_scope
    assert r.rule["tools/a.py"] != "F-source-ext" and r.rule["scripts/b.py"] == "F-source-ext"


def test_parent_not_role_is_validated(tmp_path):
    with pytest.raises(ProfileError):
        _prof(tmp_path, {"match": {"path_glob": "*/src", "parent_not_role": ["nonsense"]}, "assign": {"role": "component"}, "grain": "component"})
    with pytest.raises(ProfileError):
        _prof(tmp_path, {"match": {"path_glob": "*/src", "parent_not_role": []}, "assign": {"role": "component"}, "grain": "component"})
    r = _prof(tmp_path, {"match": {"path_glob": "*/src", "parent_not_role": ["tooling"]}, "assign": {"role": "component"}, "grain": "component"}).rules[0]
    assert r.parent_not_roles == frozenset({"tooling"}) and r.is_dir_rule


def test_file_scope_true_on_a_grain_dir_directory_rule_loads(tmp_path):
    r = _prof(tmp_path, {"match": {"segment_regex": "x"}, "assign": {"role": "tooling"}, "grain": "dir", "file_scope": True}).rules[0]
    assert r.file_scope and r.is_dir_rule
    assert not _prof(tmp_path, {"match": {"segment_regex": "x"}, "assign": {"role": "tooling"}, "grain": "dir", "file_scope": False}).rules[0].file_scope
    assert not _prof(tmp_path, {"match": {"segment_regex": "x"}, "assign": {"role": "tooling"}, "grain": "dir"}).rules[0].file_scope
