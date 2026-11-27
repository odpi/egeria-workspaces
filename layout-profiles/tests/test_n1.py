"""N1 (Phase 1c): composing profiles. `code-repo-conventions,docs-site` applies the docs-site rules inside a code repository: sites, sections, the fallback and the
D1 identity. The first-listed profile wins a conflict, a directory is claimed once, hidden subtrees still win. Synthetic only."""
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from recognizer import manifests as mf
from recognizer.layout_profile import ProfileError, compose_profiles, load_profile
from recognizer.recognize import Recognizer

PROFILES = Path(__file__).resolve().parent.parent / "profiles"
HERE = Path(__file__).resolve().parent.parent


def survey(tmp_path, files, spec, out="out", name="tree", source=True):
    root = tmp_path / name
    for rel, content in files.items():
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content)
    lst = tmp_path / f"{name}.tsv"
    lst.write_text("".join(f"{p}\t{len(files[p].encode())}\n" for p in sorted(files)))
    rec = Recognizer(compose_profiles(spec, PROFILES), blob_source=mf.FileSource(str(root)) if source else None)
    c = rec.run(lst, tmp_path / out)
    f = [json.loads(x) for x in (tmp_path / out / "findings.jsonl").read_text().splitlines()]
    by = {x["path"]: x for x in f if not x["rule_id"].startswith("F-")}
    return SimpleNamespace(c=c, by=by, f=f, rec=rec, out=tmp_path / out, allc=(tmp_path / out / "components-all.txt").read_text().split(),
                           comps=(tmp_path / out / "components.txt").read_text().split())


CODE_DOCS = "code-repo-conventions,docs-site"
MK = "site_name: x\nnav:\n  - Home: index.md\n  - Guide: [guide/a.md, guide/b.md]\n  - Ref: ref.md\n"
REPO = {"pyproject.toml": "[project]\nname='app'\n", "mkdocs.yml": MK, "docs/index.md": "x", "docs/guide/a.md": "x", "docs/guide/b.md": "x", "docs/ref.md": "x", "app/__init__.py": "x"}


def test_a_comma_list_composes_the_profiles_in_order_and_names_the_composite():
    p = compose_profiles(CODE_DOCS, PROFILES)
    assert p.profile_id == "code-repo-conventions+docs-site"
    assert [pid for pid, _ in p.composed_of] == ["code-repo-conventions+docs-site", "code-repo-conventions", "code-repo", "generic-relevance", "docs-site"]
    assert [r.id for r in p.rules].index("R-conv-docs") < [r.id for r in p.rules].index("R-docs-site-mkdocs")                  # the first-listed profile's rules come first
    ids = [r.id for r in p.rules]
    assert len(ids) == len(set(ids)) and ids.count("R-vcs-git") == 1                                                          # generic-relevance is loaded once (a diamond)
    assert compose_profiles("docs-site", PROFILES).profile_id == "docs-site"
    r = compose_profiles("docs-site, code-repo-conventions", PROFILES)
    assert [x.id for x in r.rules][0] == "R-docs-site-mkdocs"                                                                 # listed first: checked first


@pytest.mark.parametrize("spec,msg", [("", "no profile"), (",", "no profile"), ("docs-site,docs-site", "twice"), ("docs-site,nope", "not found")])
def test_bad_compositions_are_errors(spec, msg):
    with pytest.raises(ProfileError, match=msg):
        compose_profiles(spec, PROFILES)


def test_the_manifest_reading_of_both_profiles_is_available_in_the_composition():
    m = compose_profiles(CODE_DOCS, PROFILES).manifest_reading
    assert {"package-json", "cargo", "mkdocs", "gitmodules"} <= set(m.readers)
    assert m.member_rule is not None and m.section_rule is not None and m.fallback_site_rule == "R-docs-site-docusaurus"


def test_docs_sections_are_found_inside_a_code_repository(tmp_path):
    r = survey(tmp_path, REPO, CODE_DOCS)
    assert r.by["."]["root"] is True and r.by["."]["manifest_kind"] == "python-package"                                     # the root stays the code repository's root-project
    secs = sorted(p for p, x in r.by.items() if x.get("kind") == "doc-section")
    assert secs == ["docs/guide", "docs/ref.md"] and all(r.by[s]["part_of"] == "." for s in secs)
    assert r.by["."]["landing_page"] == "docs/index.md"
    assert "docs/guide" in r.allc and "docs/guide" not in r.comps


def test_without_docs_site_the_same_repository_has_no_sections(tmp_path):
    r = survey(tmp_path, REPO, "code-repo-conventions")
    assert not [p for p, x in r.by.items() if x.get("kind") == "doc-section"]


def test_the_first_listed_profile_wins_a_conflict_and_a_directory_is_claimed_once(tmp_path):
    files = {"site/pyproject.toml": "[project]\nname='s'\n", "site/mkdocs.yml": "nav: [a.md]\n", "site/docs/a.md": "x"}
    a = survey(tmp_path, files, "code-repo-conventions,docs-site", out="a", name="ta")
    b = survey(tmp_path, files, "docs-site,code-repo-conventions", out="b", name="tb")
    assert a.by["site"]["rule_id"] == "R-comp-pyproject" and b.by["site"]["rule_id"] == "R-docs-site-mkdocs"
    for r in (a, b):
        assert [x["rule_id"] for x in r.f if x["path"] == "site" and x["role"] == "component"].__len__() == 1               # claimed once
        assert r.by["site/docs/a.md"]["kind"] == "doc-section" and r.by["site/docs/a.md"]["part_of"] == "site"             # the section is found either way


def test_hidden_subtrees_still_win_inside_a_composition(tmp_path):
    files = dict(REPO)
    files.update({"node_modules/pkg/mkdocs.yml": "nav: [a.md]\n", "node_modules/pkg/docs/a.md": "x", "build/mkdocs.yml": "nav: [x.md]\n", "build/docs/x.md": "x", "other.txt": "x"})
    r = survey(tmp_path, files, CODE_DOCS)
    assert all(not p.startswith(("node_modules", "build")) for p in r.by if r.by[p].get("kind") in ("doc-section", "docs-site", "python-package"))
    assert "node_modules/pkg/mkdocs.yml" not in r.rec.reading.log and "build/mkdocs.yml" not in r.rec.reading.log


def test_a_docusaurus_site_inside_a_code_repository_gets_its_fallback_sections_even_when_a_convention_claims_docs(tmp_path):
    files = {"pyproject.toml": "[project]\nname='p'\n", "docs/docusaurus.config.js": "module.exports={}", "docs/docs/intro/a.md": "x", "docs/docs/guides/b.md": "x", "docs/docs/index.md": "x",
             "docs/docs/assets/c.md": "x"}
    r = survey(tmp_path, files, CODE_DOCS, source=False)
    assert r.by["docs"]["rule_id"] == "R-conv-docs"                                                                       # the first-listed profile claimed the directory
    secs = sorted(p for p, x in r.by.items() if x.get("kind") == "doc-section")
    assert secs == ["docs/docs/guides", "docs/docs/intro"]                                                                # the content folder is docs/ BESIDE the config; assets is not a section
    assert all(r.by[p]["confidence"] == "low" and r.by[p]["part_of"] == "docs" for p in secs)


def test_two_runs_and_the_command_line_comma_form_agree(tmp_path):
    root = tmp_path / "t"
    for rel, content in REPO.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(content)
    lst = tmp_path / "t.tsv"
    lst.write_text("".join(f"{p}\t{len((root / p).read_bytes())}\n" for p in sorted(REPO)))
    outs = []
    for n in ("o1", "o2"):
        subprocess.run([sys.executable, "-m", "recognizer.recognize", str(lst), "--out", str(tmp_path / n), "--profile", CODE_DOCS, "--blobs-dir", str(root)],
                       cwd=HERE, check=True, capture_output=True)
        outs.append(tmp_path / n)
    for n in ("components.txt", "components-all.txt", "findings.jsonl", "classes.json", "manifest-reads.txt"):
        assert (outs[0] / n).read_bytes() == (outs[1] / n).read_bytes(), n
    classes = json.loads((outs[0] / "classes.json").read_text())
    assert classes["profile"]["profile_id"] == "code-repo-conventions+docs-site" and classes["manifest_reading"]["docs_sections"]["sections"] == 2
