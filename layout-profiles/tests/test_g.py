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
    assert p.version == "0.11.0"
    rx, scripts_rx = tool.segment_res                    # Phase 1j J3: the scripts segments are their own regex, present while scripts-are-tooling is on
    alts = re.findall(r"\^\(\?:([^)]*)\)\$", rx.pattern)
    assert len(alts) == 2
    tooling_words = alts[0].split("|")
    ci_words = [w.replace("\\.", ".") for w in alts[1].split("|")]
    assert tuple(ci_words) == CI_FOLDERS
    assert tooling_words == ["tools", "tooling", "devtools", "dev-tools", "build-tools", "buildsrc", "_ext"]
    assert scripts_rx.pattern == "(?i)^(?:scripts|script)$|^scripts?[-_]"        # Phase 1h H1 (script and the scripts?[-_] prefix form)
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


# ======================================================================== G2 ========================================================================================
DOCS_PROFILES = ["code-repo-conventions", "docs-site", "code-repo-conventions,docs-site"]
DOCS_RULE = {"code-repo-conventions": "R-conv-docs", "docs-site": "R-docs-folder-top-level", "code-repo-conventions,docs-site": "R-conv-docs"}
PY_ROOT = {"pyproject.toml": "[project]\nname='r'\n", "core/pyproject.toml": "[project]\nname='c'\n"}


def is_docs_component(r, d):
    return d in r.allc and r.f.get(d, {}).get("role") == "component"


# ---- (1) one notes file, (2) images only: not a component; the files are still classified and counted
@pytest.mark.parametrize("profile", DOCS_PROFILES)
@pytest.mark.parametrize("files", [{"docs/agents/notes.md": "x"}, {"docs/images/a.png": "x", "docs/images/b.png": "x", "docs/images/c.svg": "x"},
                                   {"docs/a.md": "x", "docs/logo.png": "x"}])
def test_a_docs_folder_without_enough_content_is_not_a_component(tmp_path, profile, files):
    r = survey(tmp_path, {**PY_ROOT, **files}, profile=profile)
    assert not is_docs_component(r, "docs") and "docs" not in r.top and "docs" not in r.f
    for p in files:
        assert r.role[p] in ("docs", "other", "static-assets"), (p, r.role[p])          # still classified


def test_the_files_of_a_failed_docs_folder_keep_the_docs_role_in_the_code_profile(tmp_path):
    r = survey(tmp_path, {**PY_ROOT, "docs/agents/notes.md": "x"})
    assert r.role["docs/agents/notes.md"] == "docs" and r.rule["docs/agents/notes.md"] == "F-docs-folder"


# ---- (3) two doc files make a component
@pytest.mark.parametrize("profile", DOCS_PROFILES)
def test_two_doc_files_make_a_docs_component(tmp_path, profile):
    r = survey(tmp_path, {**PY_ROOT, "docs/a.md": "x", "docs/b.md": "x"}, profile=profile)
    assert is_docs_component(r, "docs") and r.f["docs"]["rule_id"] == DOCS_RULE[profile] and r.f["docs"]["kind"] == "documentation"


@pytest.mark.parametrize("ext", [".md", ".mdx", ".rst", ".adoc", ".asciidoc", ".txt", ".ipynb"])
def test_every_listed_extension_counts_anywhere_below(tmp_path, ext):
    r = survey(tmp_path, {**PY_ROOT, f"docs/x/a{ext}": "x", f"docs/y/z/b{ext}": "x"})
    assert is_docs_component(r, "docs")


@pytest.mark.parametrize("other", ["docs/b.png", "docs/b.html", "docs/b.MD", "docs/b.yml"])
def test_other_files_do_not_count_as_doc_files(tmp_path, other):
    r = survey(tmp_path, {**PY_ROOT, "docs/a.md": "x", other: "x"})
    assert not is_docs_component(r, "docs")


# ---- (4) a site config alone: a component (in docs-site the mkdocs rule claims it as a site, as today)
@pytest.mark.parametrize("profile", DOCS_PROFILES)
def test_mkdocs_yml_alone_makes_a_component(tmp_path, profile):
    r = survey(tmp_path, {**PY_ROOT, "docs/mkdocs.yml": "site_name: x\n"}, profile=profile)
    assert is_docs_component(r, "docs")
    assert r.f["docs"]["rule_id"] == ("R-docs-site-mkdocs" if profile == "docs-site" else DOCS_RULE[profile])


@pytest.mark.parametrize("cfg", ["mkdocs.yml", "mkdocs.yaml", "docusaurus.config.js", "docusaurus.config.ts", "docusaurus.config.mjs", "docusaurus.config.cjs", "conf.py", "antora.yml",
                                 "book.toml", "_config.yml", "package.json", "pom.xml", "build.gradle", "build.gradle.kts", "Makefile"])
@pytest.mark.parametrize("where", ["docs/", "docs/source/"])
def test_every_listed_config_in_the_folder_or_a_direct_child_makes_a_component(tmp_path, cfg, where):
    r = survey(tmp_path, {**PY_ROOT, f"{where}{cfg}": "{}" if cfg.endswith("json") else "x"}, profile="code-repo-conventions,docs-site")
    assert is_docs_component(r, "docs")


# ---- (5) docs/source/conf.py and one .rst: a component
@pytest.mark.parametrize("profile", DOCS_PROFILES)
def test_sphinx_source_conf_and_one_rst_make_a_component(tmp_path, profile):
    r = survey(tmp_path, {**PY_ROOT, "docs/source/conf.py": "x", "docs/source/index.rst": "x"}, profile=profile)
    assert is_docs_component(r, "docs") and r.f["docs"]["rule_id"] == DOCS_RULE[profile]


def test_a_config_two_levels_down_is_not_seen_known_limit(tmp_path):
    r = survey(tmp_path, {**PY_ROOT, "docs/a/b/conf.py": "x", "docs/a/b/index.rst": "x"})
    assert not is_docs_component(r, "docs")


def test_a_config_name_elsewhere_does_not_help(tmp_path):
    r = survey(tmp_path, {**PY_ROOT, "docs/a.md": "x", "other/conf.py": "x", "docs-extra/Makefile": "x"})
    assert not is_docs_component(r, "docs")


# ---- (6) doc/ and documentation/ behave like docs/
@pytest.mark.parametrize("top", ["doc", "documentation"])
@pytest.mark.parametrize("profile", DOCS_PROFILES)
def test_doc_and_documentation_behave_like_docs(tmp_path, top, profile):
    r1 = survey(tmp_path, {**PY_ROOT, f"{top}/notes.md": "x"}, profile=profile, out="o1", name="t1")
    r2 = survey(tmp_path, {**PY_ROOT, f"{top}/a.md": "x", f"{top}/b.rst": "x"}, profile=profile, out="o2", name="t2")
    r3 = survey(tmp_path, {**PY_ROOT, f"{top}/source/conf.py": "x"}, profile=profile, out="o3", name="t3")
    assert not is_docs_component(r1, top) and is_docs_component(r2, top) and is_docs_component(r3, top)


# ---- (7) a nested x/docs is unaffected: the rule is top-level only, as before
def test_a_nested_docs_folder_is_unaffected(tmp_path):
    files = {**PY_ROOT, "x/docs/a.md": "x", "x/docs/b.md": "x", "y/docs/mkdocs-notes.md": "x"}
    r = survey(tmp_path, files)
    assert "x/docs" not in r.f and "y/docs" not in r.f and "x/docs" not in r.allc


# ---- (8) the finding id of an unaffected component does not change
def test_g2_leaves_finding_ids_of_unaffected_components_unchanged(tmp_path):
    files1 = {**PY_ROOT, "lib/pom.xml": "<project/>", "docs/a.md": "x", "docs/b.md": "x"}
    r1 = survey(tmp_path, files1, out="r1", name="tree1")
    r2 = survey(tmp_path, {**files1, "doc/only.md": "x"}, out="r2", name="tree2")
    assert "doc" not in r2.f
    for d in ("core", "lib", "docs"):
        rid = r1.f[d]["rule_id"]
        assert r1.f[d]["finding_id"] == r2.f[d]["finding_id"] == hashlib.sha256(f"code-repo-conventions@0|{rid}|{d}".encode()).hexdigest()[:16]


# ---- names only: the same answer with no blob source (nothing can be opened)
def test_g2_reads_names_only(tmp_path):
    files = {"docs/source/conf.py": "x", "doc/a.md": "x", "documentation/one.md": "x", "README.md": "x"}
    root = tmp_path / "t"
    for rel, c in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(c)
    lst = tmp_path / "t.tsv"
    lst.write_text("".join(f"{p}\t1\n" for p in sorted(files)))
    out = {}
    for tag, src in (("blobs", mf.FileSource(str(root))), ("names", None)):
        Recognizer(load_profile("code-repo-conventions", PROFILES), blob_source=src).run(lst, tmp_path / tag)
        out[tag] = (tmp_path / tag / "components-all.txt").read_text().split()
    assert out["blobs"] == out["names"] and "docs" in out["names"] and "doc" not in out["names"] and "documentation" not in out["names"]


# ---- the two rules use the same closed lists, carry the stated judgement, and the loader validates min_content
def test_both_docs_rules_share_the_lists_and_state_the_judgement():
    a = {r.id: r for r in load_profile("code-repo-conventions", PROFILES).rules}["R-conv-docs"]
    b = {r.id: r for r in load_profile("docs-site", PROFILES).rules}["R-docs-folder-top-level"]
    assert load_profile("docs-site", PROFILES).version == "0.5.0" and load_profile("code-repo-conventions", PROFILES).version == "0.11.0"
    for r in (a, b):
        assert r.content_min == 2 and r.content_exts == (".md", ".mdx", ".rst", ".adoc", ".asciidoc", ".txt", ".ipynb")
        assert r.content_files == frozenset({"mkdocs.yml", "mkdocs.yaml", "docusaurus.config.js", "docusaurus.config.ts", "docusaurus.config.mjs", "docusaurus.config.cjs", "conf.py",
                                             "antora.yml", "book.toml", "_config.yml", "package.json", "pom.xml", "build.gradle", "build.gradle.kts", "Makefile"})
        assert "a single notes file is not a documentation component" in r.evidence and any("Phase 1g G2" in t for t in r.tuned_on)
        assert [g.pattern for g in r.globs] == [g.pattern for g in a.globs]


GOOD_MC = {"files": ["conf.py"], "min_files": 2, "extensions": [".md"]}


@pytest.mark.parametrize("bad", [{"files": ["conf.py"], "min_files": 2}, {**GOOD_MC, "extra": 1}, {**GOOD_MC, "min_files": 0}, {**GOOD_MC, "min_files": True},
                                 {**GOOD_MC, "min_files": "2"}, {**GOOD_MC, "files": []}, {**GOOD_MC, "files": ["a/conf.py"]}, {**GOOD_MC, "files": [""]},
                                 {**GOOD_MC, "extensions": []}, {**GOOD_MC, "extensions": ["md"]}, {**GOOD_MC, "extensions": ["."]}, "conf.py"])
def test_min_content_is_validated(tmp_path, bad):
    import yaml
    from recognizer.layout_profile import ProfileError
    base = {"profile_id": "t", "version": "0.1.0", "status": "proposed", "applies_to": "any", "roles": ["component"],
            "relevance": {"primary": ["component"], "supporting": [], "hidden": []}}
    d = {**base, "rules": [{"id": "R", "match": {"path_glob": "docs", "min_content": bad}, "assign": {"role": "component"}, "grain": "component", "basis": "convention",
                            "confidence": "low", "evidence": "x"}]}
    (tmp_path / "t.yaml").write_text(yaml.safe_dump(d))
    with pytest.raises(ProfileError):
        load_profile("t", tmp_path)
    d["rules"][0]["match"]["min_content"] = GOOD_MC
    (tmp_path / "t.yaml").write_text(yaml.safe_dump(d))
    assert load_profile("t", tmp_path).rules[0].content_min == 2
