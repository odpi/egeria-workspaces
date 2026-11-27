"""Phase 1g. G1: ONE closed list of CI-configuration folder names, used by R-tool-package (a manifest project under one is `tooling`, never a component) and by the
F-ci file-role globs (a file below one has role `ci`); each name is a path SEGMENT at any depth. G2 (below): a top-level docs, doc or documentation folder is a component
only with a site or build configuration file (in it or in a direct child folder) or at least 2 documentation files below it; names only. Synthetic trees only."""
import hashlib
import json
import re
from pathlib import Path
from types import SimpleNamespace

import pytest

from recognizer import manifests as mf
from recognizer.layout_profile import compose_profiles, load_profile
from recognizer.recognize import Recognizer

PROFILES = Path(__file__).resolve().parent.parent / "profiles"
RECOGNIZER = Path(__file__).resolve().parent.parent / "recognizer"

CI_FOLDERS = (".github", ".circleci", ".buildkite", "ci", ".ci", ".teamcity", ".gitlab", ".azure-pipelines", ".azuredevops", ".woodpecker", ".tekton", ".semaphore", ".jenkins")


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
    role = {p: (rec.classify(p)[0].role if rec.classify(p)[0] else None) for p in files}
    rule = {p: (rec.classify(p)[0].id if rec.classify(p)[0] else None) for p in files}
    return SimpleNamespace(c=c, f=f, rec=rec, role=role, rule=rule, findings=findings,
                           allc=(tmp_path / out / "components-all.txt").read_text().split(), top=(tmp_path / out / "components.txt").read_text().split())


GRADLE_ROOT = {"build.gradle": "", "settings.gradle": "rootProject.name = 'r'\n", "core/build.gradle": "", "core/src/main/java/A.java": "x"}


# ======================================================================== G1 ========================================================================================
# ---- (1) .teamcity/pom.xml beside a root Gradle build: not a component, the pom is tooling-package, the files are role ci
def test_teamcity_pom_is_tooling_and_its_files_are_ci(tmp_path):
    files = {**GRADLE_ROOT, ".teamcity/pom.xml": "<project/>", ".teamcity/settings.kts": "x", ".teamcity/patches/a.kts": "x"}
    r = survey(tmp_path, files)
    assert ".teamcity" not in r.allc and ".teamcity" not in r.top
    assert r.f[".teamcity"]["role"] == "tooling" and r.f[".teamcity"]["kind"] == "tooling-package" and r.f[".teamcity"]["rule_id"] == "R-tool-package"
    for p in (".teamcity/pom.xml", ".teamcity/settings.kts", ".teamcity/patches/a.kts"):
        assert r.role[p] == "ci" and r.rule[p] == "F-ci", p
    assert "core" in r.allc


# ---- (2) the same for .gitlab/x/package.json and .azure-pipelines/build.gradle.kts
@pytest.mark.parametrize("path", [".gitlab/x/package.json", ".azure-pipelines/build.gradle.kts"])
def test_gitlab_and_azure_pipelines_projects_are_tooling_and_ci(tmp_path, path):
    d = path.rsplit("/", 1)[0]
    r = survey(tmp_path, {**GRADLE_ROOT, path: '{"name": "x"}', f"{d}/notes.txt": "x"})
    assert d not in r.allc and r.f[d]["role"] == "tooling" and r.f[d]["kind"] == "tooling-package"
    assert r.role[path] == "ci" and r.role[f"{d}/notes.txt"] == "ci"


# ---- every listed folder, at the top and nested, as a segment
@pytest.mark.parametrize("folder", CI_FOLDERS)
@pytest.mark.parametrize("prefix", ["", "sub/"])
def test_every_listed_ci_folder_is_tooling_and_ci_at_any_depth(tmp_path, folder, prefix):
    d = f"{prefix}{folder}/p"
    r = survey(tmp_path, {**GRADLE_ROOT, f"{d}/pom.xml": "<project/>", f"{prefix}{folder}/run.sh": "x"})
    assert d not in r.allc and r.f[d]["role"] == "tooling"                    # R-tool-package: any depth, the bare ci included (as before G1)
    file_ci = not (folder == "ci" and prefix)                                # F-ci: the bare ci is top level only
    assert (r.role[f"{d}/pom.xml"] == "ci") is file_ci and (r.role[f"{prefix}{folder}/run.sh"] == "ci") is file_ci


# ---- the bare ci is a CI folder only at the top level: deeper down it is often a source package
def test_a_bare_ci_folder_is_ci_at_the_top_and_not_as_a_source_package(tmp_path):
    r = survey(tmp_path, {**GRADLE_ROOT, "ci/run.sh": "x", "src/main/java/org/x/ci/Foo.java": "x", "core/src/main/java/org/x/ci/Bar.java": "x"})
    assert r.role["ci/run.sh"] == "ci" and r.rule["ci/run.sh"] == "F-ci"
    assert r.role["src/main/java/org/x/ci/Foo.java"] != "ci" and r.role["core/src/main/java/org/x/ci/Bar.java"] == "source"


# ---- (3) .buildkite/pipeline.yml is role ci (F-ci lacked .buildkite before G1)
def test_buildkite_pipeline_is_ci(tmp_path):
    r = survey(tmp_path, {**GRADLE_ROOT, ".buildkite/pipeline.yml": "steps: []\n"})
    assert r.role[".buildkite/pipeline.yml"] == "ci" and r.rule[".buildkite/pipeline.yml"] == "F-ci"


# ---- (4) NOT matched: teamcity/ (no dot) with a pom stays a Maven module; a file NAMED like a CI folder is unchanged
def test_teamcity_without_a_dot_is_still_a_maven_module(tmp_path):
    r = survey(tmp_path, {**GRADLE_ROOT, "teamcity/pom.xml": "<project/>"})
    assert "teamcity" in r.allc and r.f["teamcity"]["role"] == "component" and r.f["teamcity"]["rule_id"] == "R-comp-pom"
    assert r.role["teamcity/pom.xml"] != "ci"


@pytest.mark.parametrize("path", ["src/main/resources/.teamcity-notes.txt", "core/src/main/resources/.teamcity-notes.txt", "x.teamcity/a.txt", "my-ci/a.txt", "civic/a.txt"])
def test_names_that_only_contain_a_ci_folder_name_are_not_ci(tmp_path, path):
    r = survey(tmp_path, {**GRADLE_ROOT, path: "x"})
    assert r.role[path] != "ci" and r.rule[path] != "F-ci"


def test_the_ci_file_role_stays_case_sensitive_as_before(tmp_path):
    r = survey(tmp_path, {**GRADLE_ROOT, ".TeamCity/a.kts": "x", ".GITHUB/w.yml": "x"})
    assert r.rule[".TeamCity/a.kts"] != "F-ci" and r.rule[".GITHUB/w.yml"] != "F-ci"


# ---- (5) the finding id of an unaffected component does not change (profile@major|rule|path; the major is unchanged)
def test_finding_ids_of_unaffected_components_do_not_change(tmp_path):
    files1 = {**GRADLE_ROOT, "lib/pom.xml": "<project/>"}
    r1 = survey(tmp_path, files1, out="r1", name="tree1")
    r2 = survey(tmp_path, {**files1, ".teamcity/pom.xml": "<project/>", ".buildkite/pipeline.yml": "x"}, out="r2", name="tree2")
    assert load_profile("code-repo-conventions", PROFILES).major == "0"
    for d in ("core", "lib"):
        rid = r1.f[d]["rule_id"]
        assert r1.f[d]["finding_id"] == r2.f[d]["finding_id"] == hashlib.sha256(f"code-repo-conventions@0|{rid}|{d}".encode()).hexdigest()[:16]


# ---- ONE closed list: R-tool-package's CI alternation and the F-ci folder globs name exactly the same folders
def test_the_ci_folder_list_is_one_closed_list_in_both_places():
    p = load_profile("code-repo-conventions", PROFILES)
    by = {r.id: r for r in (*p.rules, *p.file_roles)}
    tool, fci = by["R-tool-package"], by["F-ci"]
    assert p.version == "0.8.0"
    (rx,) = tool.segment_res
    alts = re.findall(r"\^\(\?:([^)]*)\)\$", rx.pattern)
    assert len(alts) == 2
    tooling_words = alts[0].split("|")
    ci_words = [w.replace("\\.", ".") for w in alts[1].split("|")]
    assert tuple(ci_words) == CI_FOLDERS
    assert tooling_words == ["tools", "tooling", "devtools", "dev-tools", "build-tools", "buildsrc", "_ext", "scripts"]
    globs = list(fci.match["path_glob"])
    assert globs == [g for x in CI_FOLDERS for g in ((f"{x}/**",) if x == "ci" else (f"{x}/**", f"**/{x}/**"))] + [".gitlab-ci.yml", "Jenkinsfile"]
    for x in CI_FOLDERS:
        assert rx.search(x) and rx.search(x.upper())          # R-tool-package stays case-insensitive
    assert p.file_roles[0].id == "F-ci"                        # still the first file role


def test_the_g1_rules_carry_provenance():
    p = load_profile("code-repo-conventions", PROFILES)
    by = {r.id: r for r in (*p.rules, *p.file_roles)}
    for rid in ("R-tool-package", "F-ci"):
        assert any("Phase 1g G1" in t for t in by[rid].tuned_on), rid
        assert ".teamcity" in by[rid].evidence and ".jenkins" in by[rid].evidence


# ---- the composite profile with docs-site behaves the same for G1
def test_g1_in_the_composite_profile(tmp_path):
    r = survey(tmp_path, {**GRADLE_ROOT, ".teamcity/pom.xml": "<project/>"}, profile="code-repo-conventions,docs-site")
    assert ".teamcity" not in r.allc and r.f[".teamcity"]["role"] == "tooling" and r.role[".teamcity/pom.xml"] == "ci"
