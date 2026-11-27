"""N2 (Phase 1c): Gradle `projectDir` mappings in settings.gradle(.kts), read as string literals by regex and never evaluated. An include with no directory is not a
component; an included project whose only children are other included projects is not a component either. Synthetic only."""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from recognizer import manifests as mf
from recognizer.layout_profile import load_profile
from recognizer.recognize import Recognizer

PROFILES = Path(__file__).resolve().parent.parent / "profiles"


def survey(tmp_path, files, out="out", name="tree"):
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
    src = Rec()
    rec = Recognizer(load_profile("code-repo-conventions", PROFILES), blob_source=src)
    c = rec.run(lst, tmp_path / out)
    f = [json.loads(x) for x in (tmp_path / out / "findings.jsonl").read_text().splitlines()]
    by = {x["path"]: x for x in f}
    return SimpleNamespace(c=c, by=by, rec=rec, src=src, allc=(tmp_path / out / "components-all.txt").read_text().split(),
                           comps=(tmp_path / out / "components.txt").read_text().split())


def g(**mods):
    return mods


def extract(text):
    return mf.extract("gradle", "settings.gradle", text.encode())


# ---- the regex reader -------------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("line,expect", [
    ("project(':a').projectDir = file('modules/a')", {"a": "modules/a"}),
    ('project(":a").projectDir = file("modules/a")', {"a": "modules/a"}),
    ("project(':a').projectDir = new File('modules/a')", {"a": "modules/a"}),
    ("project(':a').projectDir = new File(settingsDir, 'modules/a')", {"a": "modules/a"}),
    ('project(":a").projectDir = File(rootDir, "modules/a")', {"a": "modules/a"}),
    ('project(":a").projectDir = new File(rootProject.projectDir, "modules/a")', {"a": "modules/a"}),
    ("project(':a:b').projectDir = file('x/b')", {"a/b": "x/b"}),
    ("findProject(':a')?.projectDir = file('m/a')", {"a": "m/a"}),
    ("project( ':a' ) . projectDir =   file( 'm/a' )", {"a": "m/a"}),
    ("project(':a').projectDir = file(someVariable)", {}),                       # not a literal: never evaluated
    ("project(':a').projectDir = file(\"$rootDir/a\")", {"a": "$rootDir/a"}),     # a literal string, taken as written (it will not resolve to a directory)
    ("// project(':a').projectDir = file('m/a')", {}), ("/* project(':a').projectDir = file('m/a') */", {}),
    ("project(':a').name = 'other'", {}),
])
def test_projectdir_forms(line, expect):
    d = extract(f"include ':a', ':a:b'\n{line}\n")
    assert d.project_dirs == expect


def test_each_included_project_maps_to_its_directory_and_the_default_is_its_path():
    d = extract("include 'a', 'a:b', 'plain', ':k:l'\nproject(':a').projectDir = file('modules/a')\nproject(':a:b').projectDir = new File(settingsDir, 'x/b')\n")
    assert d.members == ["modules/a", "x/b", "plain", "k/l"]
    d2 = extract("include 'a'\nproject(':notincluded').projectDir = file('zzz')\nproject(':a').projectDir = file('m/a')\n")
    assert d2.members == ["m/a"] and d2.project_dirs == {"a": "m/a"}                # a mapping for a project that is not included is ignored
    assert extract("include 'a', 'b'\nproject(':a').projectDir = file('same')\nproject(':b').projectDir = file('same')\n").members == ["same"]


# ---- components -----------------------------------------------------------------------------------------------------------------------------------
def test_included_projects_are_components_at_their_mapped_directories(tmp_path):
    files = {"settings.gradle": "include 'core', 'api', 'data'\nproject(':core').projectDir = file('modules/core')\nproject(':api').projectDir = new File(settingsDir, 'services/api')\n",
             "build.gradle": "x", "modules/core/build.gradle": "x", "modules/core/src/A.java": "x", "services/api/build.gradle": "x", "data/build.gradle": "x",
             "core/build.gradle": "x"}                                                   # a directory called core exists too, but the project `core` lives in modules/core
    r = survey(tmp_path, files)
    for m in ("modules/core", "services/api", "data"):
        assert r.by[m]["member_of"] == "." and r.by[m]["evidence_field"] == "include" and m in r.comps, m
    assert r.by["core"].get("member_of") is None                                          # present as a manifest directory, but not the declared project `core`
    assert r.by["."]["members_declared"] == 3 and "unresolved_members" not in r.by["."]


def test_a_mapping_works_for_kotlin_settings_too(tmp_path):
    files = {"settings.gradle.kts": 'include(":lib")\nproject(":lib").projectDir = file("libs/lib")\n', "libs/lib/build.gradle.kts": "x"}
    r = survey(tmp_path, files)
    assert r.by["libs/lib"]["member_of"] == "." and "libs/lib" in r.comps


def test_an_include_with_no_directory_is_not_a_component_and_is_listed_unresolved(tmp_path):
    files = {"settings.gradle": "include 'bom', 'real', 'mapped-away'\nproject(':mapped-away').projectDir = file('nowhere/at/all')\n", "real/build.gradle": "x", "build.gradle": "x"}
    r = survey(tmp_path, files)
    assert r.by["."]["unresolved_members"] == ["bom", "nowhere/at/all"]
    assert [p for p in r.comps if p in ("bom", "nowhere/at/all")] == [] and "real" in r.comps


def test_a_mapped_directory_outside_the_settings_directory_is_unresolved_and_nothing_is_read_there(tmp_path):
    files = {"sub/settings.gradle": "include 'out', 'abs'\nproject(':out').projectDir = file('../other')\nproject(':abs').projectDir = file('/etc')\n", "other/build.gradle": "x", "sub/build.gradle": "x"}
    r = survey(tmp_path, files)
    assert r.by["sub"]["unresolved_members"] == ["../other", "/etc"] and "other" not in {p for p, x in r.by.items() if x.get("member_of")}


# ---- aggregators --------------------------------------------------------------------------------------------------------------------------------
def test_an_included_project_whose_only_children_are_included_projects_is_not_a_component(tmp_path):
    files = {"settings.gradle": "include 'a', 'a:b', 'a:c', 'solo'\n", "a/b/build.gradle": "x", "a/c/build.gradle": "x", "solo/build.gradle": "x", "build.gradle": "x"}
    r = survey(tmp_path, files)
    assert "a" not in r.comps and "a" not in r.allc and r.by["a"]["rule_id"] == "M-aggregator" and r.by["a"]["role"] == "other"
    assert {"a/b", "a/c", "solo"} <= set(r.comps) and r.by["."]["gradle_aggregators"] == ["a"]


def test_a_parent_with_a_file_or_a_non_included_child_folder_is_a_project_not_an_aggregator(tmp_path):
    files = {"settings.gradle": "include 'f', 'f:x', 'd', 'd:y'\n", "f/build.gradle": "x", "f/x/build.gradle": "x", "d/y/build.gradle": "x", "d/extra/notes.txt": "x", "build.gradle": "x"}
    r = survey(tmp_path, files)
    assert "f" in r.comps and r.by["f"]["rule_id"] == "R-comp-gradle" and "d" in r.comps and r.by["d"]["rule_id"] == "M-workspace-member"
    assert r.by["."].get("gradle_aggregators") == []


def test_aggregation_follows_the_mapped_directories(tmp_path):
    files = {"settings.gradle": "include 'grp', 'grp:one', 'grp:two'\nproject(':grp').projectDir = file('g')\nproject(':grp:one').projectDir = file('g/one')\n"
                                "project(':grp:two').projectDir = file('g/two')\n", "g/one/build.gradle": "x", "g/two/build.gradle": "x", "build.gradle": "x"}
    r = survey(tmp_path, files)
    assert "g" not in r.comps and {"g/one", "g/two"} <= set(r.comps) and r.by["g"]["rule_id"] == "M-aggregator"


def test_only_the_settings_file_is_read_and_two_runs_are_identical(tmp_path):
    files = {"settings.gradle": "include 'a', 'a:b'\nproject(':a:b').projectDir = file('x')\n", "build.gradle": "tasks.register('boom') { 1/0 }", "a/b/build.gradle": "x", "x/build.gradle": "x"}
    r1 = survey(tmp_path, files, out="o1", name="t1")
    r2 = survey(tmp_path, files, out="o2", name="t2")
    assert r1.src.asked == ["settings.gradle"]                                              # build.gradle is code: never opened, never run
    for n in ("components.txt", "components-all.txt", "findings.jsonl", "classes.json"):
        assert (tmp_path / "o1" / n).read_bytes() == (tmp_path / "o2" / n).read_bytes(), n


def test_the_member_rule_carries_the_iceberg_provenance_in_the_profile():
    p = load_profile("code-repo", PROFILES)
    assert "iceberg (M8, spent)" in p.manifest_reading.member_rule.tuned_on and "iceberg (M8, spent)" in p.manifest_reading.aggregator_rule.tuned_on
