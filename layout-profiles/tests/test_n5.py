"""N5 (Phase 1c): INHERIT translations. A directory whose mkdocs.yml has `INHERIT: <path to another site's mkdocs.yml>` is a `doc-translation` component, a part of that site, NOT a docs-site,
and its nav entries are not sections. The INHERIT path is resolved against the path list only (relative, never above the repository root) and the inherited file is never read through it.
A missing target leaves a site, with a warning. Synthetic only."""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from recognizer import manifests as mf
from recognizer.layout_profile import load_profile
from recognizer.recognize import Recognizer

PROFILES = Path(__file__).resolve().parent.parent / "profiles"


def survey(tmp_path, files, out="out", name="tree", source=True):
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
    src = Rec() if source else None
    rec = Recognizer(load_profile("docs-site", PROFILES), blob_source=src)
    c = rec.run(lst, tmp_path / out)
    f = {x["path"]: x for x in map(json.loads, (tmp_path / out / "findings.jsonl").read_text().splitlines())}
    return SimpleNamespace(c=c, f=f, rec=rec, src=src, out=tmp_path / out, allc=(tmp_path / out / "components-all.txt").read_text().split(),
                           comps=(tmp_path / out / "components.txt").read_text().split())


NAV = "nav:\n  - Home: index.md\n  - Guide: guide.md\n"
EN = {"en/mkdocs.yml": NAV, "en/docs/index.md": "x", "en/docs/guide.md": "x"}


def secs(r):
    return sorted(p for p, x in r.f.items() if x.get("kind") == "doc-section")


def test_a_config_that_inherits_another_sites_config_is_a_translation_of_that_site(tmp_path):
    r = survey(tmp_path, {**EN, "es/mkdocs.yml": "INHERIT: ../en/mkdocs.yml\nsite_name: es\nnav:\n  - Inicio: index.md\n  - Guia: guia.md\n", "es/docs/index.md": "x", "es/docs/guia.md": "x"})
    t = r.f["es"]
    assert t["kind"] == "doc-translation" and t["rule_id"] == "M-docs-translation" and t["role"] == "component" and t["part_of"] == "en" and t["translation_of"] == "en"
    assert t["evidence_file"] == "es/mkdocs.yml" and t["evidence_field"] == "INHERIT" and t["evidence_blob"] and t["inherit"] == "../en/mkdocs.yml"
    assert r.f["en"]["kind"] == "docs-site" and r.comps == ["en"] and "es" in r.allc and "es" not in r.comps          # a part of the site, not a site and not top-level
    assert secs(r) == ["en/docs/guide.md"]                                                                              # the translation's nav entries are NOT sections
    assert r.rec.docs_stats["translations"] == 1 and not [p for p in r.f if p.startswith("es/docs/g")]


def test_the_path_forms_that_resolve(tmp_path):
    files = {"mkdocs.yml": NAV, "docs/index.md": "x", "docs/guide.md": "x", "docs/es/mkdocs.yaml": "INHERIT: ../../mkdocs.yml\n", "docs/fr/mkdocs.yml": "INHERIT: ./../../mkdocs.yml\n",
             "x/de/mkdocs.yml": "INHERIT: ..//..//mkdocs.yml\n"}
    r = survey(tmp_path, files)
    assert {p: r.f[p]["kind"] for p in ("docs/es", "docs/fr", "x/de")} == {p: "doc-translation" for p in ("docs/es", "docs/fr", "x/de")}
    assert all(r.f[p]["part_of"] == "." for p in ("docs/es", "docs/fr", "x/de")) and r.f["."]["rule_id"] == "R-docs-site-mkdocs"


def test_a_missing_target_leaves_a_site_with_a_warning(tmp_path):
    r = survey(tmp_path, {**EN, "es/mkdocs.yml": "INHERIT: ../nowhere/mkdocs.yml\nnav:\n  - Guia: guia.md\n", "es/docs/guia.md": "x"})
    assert r.f["es"]["kind"] == "docs-site" and r.f["es"]["inherit_warning"] == "INHERIT target not found: nowhere/mkdocs.yml"
    assert secs(r) == ["en/docs/guide.md", "es/docs/guia.md"] and r.rec.docs_stats["inherit_warnings"] == 1 and r.rec.docs_stats["translations"] == 0
    assert sorted(r.comps) == ["en", "es"]


@pytest.mark.parametrize("inherit,msg", [("../../outside/mkdocs.yml", "not a path inside the repository"), ("/abs/mkdocs.yml", "not a path inside the repository"),
                                         ("C:/x/mkdocs.yml", "not a path inside the repository"), ("../en/base.yml", "not a mkdocs.yml"), ("mkdocs.yml", "not another site")])
def test_unsafe_or_unsuitable_targets_stay_sites_with_a_warning(tmp_path, inherit, msg):
    r = survey(tmp_path, {**EN, "en/base.yml": "x", "es/mkdocs.yml": f"INHERIT: {inherit}\n"})
    assert r.f["es"]["kind"] == "docs-site" and msg in r.f["es"]["inherit_warning"]


def test_the_inherited_file_is_never_read_through_the_path(tmp_path):
    r = survey(tmp_path, {**EN, "en/base.yml": "SECRET: do-not-read\n", "es/mkdocs.yml": "INHERIT: ../en/base.yml\n", "fr/mkdocs.yml": "INHERIT: ../en/mkdocs.yml\n"})
    assert "en/base.yml" not in r.src.asked and "SECRET" not in json.dumps(r.f)
    assert r.src.asked.count("en/mkdocs.yml") == 1                                                                      # read once, as its own site, not once more through fr's INHERIT


def test_a_cycle_makes_no_translation_and_chains_resolve(tmp_path):
    r = survey(tmp_path, {"a/mkdocs.yml": "INHERIT: ../b/mkdocs.yml\n", "b/mkdocs.yml": "INHERIT: ../a/mkdocs.yml\n"})
    assert r.f["a"]["kind"] == "docs-site" and r.f["b"]["kind"] == "docs-site" and "cycle" in r.f["a"]["inherit_warning"] and "cycle" in r.f["b"]["inherit_warning"]
    r2 = survey(tmp_path, {"a/mkdocs.yml": NAV, "b/mkdocs.yml": "INHERIT: ../a/mkdocs.yml\n", "c/mkdocs.yml": "INHERIT: ../b/mkdocs.yml\n"}, out="o2", name="t2")
    assert r2.f["b"]["translation_of"] == "a" and r2.f["c"]["translation_of"] == "b" and r2.f["a"]["kind"] == "docs-site"


def test_an_inherit_that_is_not_a_string_or_is_empty_is_ignored(tmp_path):
    r = survey(tmp_path, {**EN, "es/mkdocs.yml": "INHERIT: [a, b]\n", "fr/mkdocs.yml": "INHERIT: ''\n", "de/mkdocs.yml": "nav: [x.md]\n"})
    assert all(r.f[p]["kind"] == "docs-site" and "inherit_warning" not in r.f[p] for p in ("es", "fr", "de"))


def test_without_a_blob_source_nothing_is_known_and_every_config_is_a_site(tmp_path):
    r = survey(tmp_path, {**EN, "es/mkdocs.yml": "INHERIT: ../en/mkdocs.yml\n"}, source=False)
    assert r.f["es"]["kind"] == "docs-site"


def test_a_translation_inside_a_hidden_subtree_is_not_read_or_claimed(tmp_path):
    r = survey(tmp_path, {**EN, "node_modules/p/mkdocs.yml": "INHERIT: ../../en/mkdocs.yml\n"})
    assert "node_modules/p" not in r.f and "node_modules/p/mkdocs.yml" not in r.src.asked


def test_the_translations_content_folder_is_still_claimed_and_runs_are_identical(tmp_path):
    files = {**EN, "es/mkdocs.yml": "INHERIT: ../en/mkdocs.yml\ndocs_dir: contenido\n", "es/contenido/index.md": "x"}
    a = survey(tmp_path, files, out="a", name="ta")
    b = survey(tmp_path, files, out="b", name="tb")
    assert a.f["es/contenido"]["role"] == "docs" and a.f["es"]["kind"] == "doc-translation"
    for n in ("components.txt", "components-all.txt", "findings.jsonl", "classes.json"):
        assert (a.out / n).read_bytes() == (b.out / n).read_bytes(), n


def test_the_profile_has_a_translation_rule_with_provenance_and_the_reader_extracts_the_path_only():
    m = load_profile("docs-site", PROFILES).manifest_reading
    assert m.translation_rule.id == "M-docs-translation" and m.translation_rule.kind == "doc-translation" and m.translation_rule.tuned_on == ("fastapi (M8, spent)",)
    d = mf.extract("mkdocs", "es/mkdocs.yml", b"INHERIT: ../en/mkdocs.yml\nplugins: [search]\nsecret_token: abc\n")
    assert d.inherit == "../en/mkdocs.yml" and "abc" not in json.dumps(d, default=lambda o: o.__dict__)
