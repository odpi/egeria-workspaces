"""M7: documentation sections from the nav of mkdocs.yml (docs-site 0.2.0). Synthetic sites only; nothing copied from a real documentation tree."""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from recognizer import manifests as mf
from recognizer.layout_profile import ProfileError, load_profile, parse_profile
from recognizer.recognize import Recognizer

PROFILES = Path(__file__).resolve().parent.parent / "profiles"


def survey(tmp_path, files: dict, mkdocs: str | None = None, site="s", out="out", source=True, profile="docs-site", name="tree"):
    files = dict(files)
    if mkdocs is not None:
        files[(site + "/" if site else "") + "mkdocs.yml"] = mkdocs
    root = tmp_path / name
    for rel, content in files.items():
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content)
    lst = tmp_path / f"{name}.tsv"
    lst.write_text("".join(f"{p}\t{len(files[p].encode())}\n" for p in sorted(files)))
    rec = Recognizer(load_profile(profile, PROFILES), blob_source=mf.FileSource(str(root)) if source else None)
    c = rec.run(lst, tmp_path / out)
    f = {x["path"]: x for x in map(json.loads, (tmp_path / out / "findings.jsonl").read_text().splitlines())}
    return SimpleNamespace(c=c, f=f, comps=(tmp_path / out / "components.txt").read_text().split(), allc=(tmp_path / out / "components-all.txt").read_text().split(),
                           rec=rec, out=tmp_path / out)


def sections(r):
    return sorted(p for p, x in r.f.items() if x.get("kind") == "doc-section")


PAGES = {f"s/docs/{p}": "# x" for p in ("index.md", "a.md", "b.md", "guide/one.md", "guide/two.md", "guide/deep/three.md", "ref/api.md", "ref/cli.md", "misc.md")}


# ---- section identity (D1) ---------------------------------------------------------------------------------------------------------------
def test_pages_sharing_one_top_level_folder_make_that_folder_the_section(tmp_path):
    r = survey(tmp_path, PAGES, "site_name: x\nnav:\n  - Home: index.md\n  - Guide:\n      - one.md: guide/one.md\n      - Deeper: guide/deep/three.md\n      - guide/two.md\n")
    assert sections(r) == ["s/docs/guide"]                                         # at any depth below the folder; Home is the landing page
    g = r.f["s/docs/guide"]
    assert g["rule_id"] == "M-docs-section" and g["identity"] == "folder" and g["pages_kept"] == 3 and g["part_of"] == "s" and g["nav_title"] == "Guide"
    assert g["evidence_file"] == "s/mkdocs.yml" and g["evidence_field"] == "nav" and g["evidence_blob"]
    assert r.f["s"]["landing_page"] == "s/docs/index.md" and r.comps == ["s"] and "s/docs/guide" in r.allc


def test_pages_in_different_folders_or_in_docs_dir_itself_use_the_first_page_file(tmp_path):
    r = survey(tmp_path, PAGES, "nav:\n  - Mixed:\n      - guide/one.md\n      - ref/api.md\n  - Flat: a.md\n  - Both:\n      - b.md\n      - ref/cli.md\n  - Ref:\n      - ref/cli.md\n")
    assert sections(r) == ["s/docs/a.md", "s/docs/b.md", "s/docs/guide/one.md", "s/docs/ref"]       # the last entry's one page sits in ONE folder: the folder
    assert r.f["s/docs/guide/one.md"]["identity"] == "first-page" and r.f["s/docs/guide/one.md"]["pages_kept"] == 2
    assert r.f["s/docs/ref"]["identity"] == "folder" and r.f["s/docs/ref"]["part_of"] == "s" and r.f["s/docs/b.md"]["part_of"] == "s"
    assert sorted(r.allc) == sorted(["s", *sections(r)]) and r.comps == ["s"]      # sections are parts of their site, never top-level


def test_a_single_page_section_is_that_page(tmp_path):
    r = survey(tmp_path, PAGES, "nav:\n  - Home: index.md\n  - A: a.md\n")
    assert sections(r) == ["s/docs/a.md"] and r.f["s/docs/a.md"]["pages_kept"] == 1


def test_urls_anchors_and_outside_entries_are_skipped_and_a_section_with_no_kept_page_is_not_a_component(tmp_path):
    nav = ("nav:\n  - Ext: https://example.org/x\n  - Ext2: [http://a/b, 'mailto:x@y']\n  - Anchor: '#top'\n  - Up: ../outside.md\n  - Abs: /etc/passwd\n"
           "  - Missing: nowhere.md\n  - Mixed:\n      - https://example.org\n      - '#frag'\n      - a.md#section\n      - ../x.md\n  - Ok: b.md\n")
    r = survey(tmp_path, PAGES, nav)
    assert sections(r) == ["s/docs/a.md", "s/docs/b.md"]                              # `a.md#section` names a.md (the fragment is dropped)
    assert r.f["s"]["unresolved_nav"] == ["Ext", "Ext2", "Anchor", "Up", "Abs", "Missing"]
    assert r.f["s/docs/a.md"]["pages_kept"] == 1


def test_the_landing_page_is_not_a_section_only_when_the_entry_is_exactly_index_md(tmp_path):
    r = survey(tmp_path, PAGES, "nav:\n  - index.md\n  - Start:\n      - index.md\n      - a.md\n")
    assert r.f["s"]["landing_page"] == "s/docs/index.md"                                 # the bare `index.md` entry is the landing page
    assert sections(r) == ["s/docs/index.md"]                                            # the second entry holds index.md AND a.md: a section, identified by its first page
    assert r.f["s/docs/index.md"]["identity"] == "first-page" and r.f["s/docs/index.md"]["pages_kept"] == 2


def test_two_entries_with_the_same_identity_make_one_component(tmp_path):
    r = survey(tmp_path, PAGES, "nav:\n  - A: guide/one.md\n  - B: guide/two.md\n  - C: [guide/deep/three.md]\n")
    assert sections(r) == ["s/docs/guide"] and "s/docs/guide/one.md" not in r.f          # three single-page entries in one folder: one identity, so one component
    assert r.rec.docs_stats["merged"] == 2


# ---- docs_dir, site_dir, the nav shapes --------------------------------------------------------------------------------------------------
def test_a_custom_docs_dir_is_the_content_folder_and_a_custom_site_dir_is_hidden(tmp_path):
    files = {"s/documentation/index.md": "x", "s/documentation/api/a.md": "x", "s/documentation/api/b.md": "x", "s/public/index.html": "<html>", "s/public/deep/x.html": "x",
             "s/docs/old.md": "x"}
    r = survey(tmp_path, files, "docs_dir: documentation\nsite_dir: public\nnav:\n  - Home: index.md\n  - API: [api/a.md, api/b.md]\n")
    assert sections(r) == ["s/documentation/api"] and r.f["s"]["docs_dir"] == "documentation" and r.f["s"]["site_dir"] == "public"
    assert r.c["by_relevance"]["hidden"]["files"] == 2 and r.f["s/public"]["role"] == "generated"                  # the custom build output is hidden and counted
    assert r.f["s/documentation"]["role"] == "docs"                                                                    # and the custom content folder is claimed as docs


def test_a_docs_dir_that_is_absolute_or_leaves_the_site_gives_no_sections(tmp_path):
    for n, bad in enumerate(("../elsewhere", "/abs/docs")):
        r = survey(tmp_path, PAGES, f"docs_dir: {bad}\nnav:\n  - A: a.md\n", out=f"o{n}", name=f"t{n}")
        assert sections(r) == [] and r.f["s"]["unresolved_docs_dir"] == bad


def test_nested_nav_groups_are_walked_in_order_and_non_strings_are_ignored(tmp_path):
    r = survey(tmp_path, PAGES, "nav:\n  - Guide:\n      - Intro: guide/one.md\n      - More:\n          - guide/two.md\n          - 7\n          - null\n      - guide/deep/three.md\n  - 3\n")
    assert sections(r) == ["s/docs/guide"] and r.f["s/docs/guide"]["pages_kept"] == 3


def test_mkdocs_yml_with_env_and_python_tags_is_read_without_constructing_anything(tmp_path):
    r = survey(tmp_path, PAGES, "site_name: !ENV [SITE, x]\nhooks: !!python/name:os.system\nnav:\n  - A: a.md\n")
    assert sections(r) == ["s/docs/a.md"] and r.c["manifest_reading"]["parse_errors"] == 0


def test_without_a_nav_each_top_level_folder_with_pages_is_a_low_confidence_section(tmp_path):
    files = {"s/docs/index.md": "x", "s/docs/guide/a.md": "x", "s/docs/guide/sub/b.md": "x", "s/docs/ref/c.rst": "x", "s/docs/assets/logo.md": "x", "s/docs/img/p.png": "x",
             "s/docs/overrides/main.md": "x", "s/docs/empty/readme.txt": "x", "s/docs/_private/p.md": "x", "s/docs/top.md": "x"}
    r = survey(tmp_path, files, "site_name: no nav\n")
    assert sections(r) == ["s/docs/guide", "s/docs/ref"]
    g = r.f["s/docs/guide"]
    assert g["rule_id"] == "M-docs-section-folder" and g["confidence"] == "low" and g["basis"] == "convention" and g["identity"] == "folder-fallback" and g["part_of"] == "s"
    assert r.rec.docs_stats["fallback_sections"] == 2


def test_a_docs_folder_with_no_mkdocs_yml_gets_no_sections_whatever_it_holds(tmp_path):
    files = {"docs/guide/a.md": "x", "docs/ref/b.md": "x", "docs/archive/old.md": "x", "docs/index.md": "x"}
    r = survey(tmp_path, files, None, site="")
    assert sections(r) == [] and r.comps == ["docs"] and r.f["docs"]["kind"] == "documentation"                        # the trellis shape: unchanged


def test_a_site_at_the_repository_root_still_has_its_sections_as_parts(tmp_path):
    r = survey(tmp_path, {"docs/index.md": "x", "docs/g/a.md": "x", "docs/g/b.md": "x"}, "nav:\n  - Home: index.md\n  - G: [g/a.md, g/b.md]\n", site="")
    assert sections(r) == ["docs/g"] and r.f["docs/g"]["part_of"] == "." and r.comps == ["."]


def test_a_site_inside_a_hidden_subtree_is_never_read(tmp_path):
    files = {"node_modules/pkg/mkdocs.yml": "nav: [a.md]", "node_modules/pkg/docs/a.md": "x", "real/mkdocs.yml": "nav:\n  - A: a.md\n", "real/docs/a.md": "x"}
    r = survey(tmp_path, files, None, site="")
    assert r.rec.reading.log == ["real/mkdocs.yml"] and sections(r) == ["real/docs/a.md"]


# ---- failure, stability, determinism ---------------------------------------------------------------------------------------------------
def test_a_malformed_or_oversize_mkdocs_yml_keeps_the_presence_only_site(tmp_path):
    r = survey(tmp_path, PAGES, "nav: [a.md\n")
    assert sections(r) == [] and r.f["s"]["rule_id"] == "R-docs-site-mkdocs" and r.f["s"]["parse_error"].startswith("yaml") and r.f["s"]["confidence"] == "medium"
    bomb = "a: &a [x, x]\nnav: *a\n"
    r2 = survey(tmp_path, PAGES, bomb, out="o2", name="t2")
    assert sections(r2) == [] and "alias" in r2.f["s"]["parse_error"]
    r3 = survey(tmp_path, PAGES, "nav:\n  - A: a.md\n# " + "x" * (mf.DEFAULT_MAX_FILE_BYTES + 5), out="o3", name="t3")
    assert sections(r3) == [] and r3.f["s"]["skipped"] == "size"


def test_a_section_id_does_not_change_when_unrelated_manifest_text_changes(tmp_path):
    a = survey(tmp_path, PAGES, "site_name: one\nnav:\n  - A: a.md\n  - G: [guide/one.md]\n", out="a", name="ta")
    b = survey(tmp_path, PAGES, "site_name: two\ntheme: material\nnav:\n  - A: a.md\n  - G: [guide/one.md]\n", out="b", name="tb")
    assert {k: v["finding_id"] for k, v in a.f.items()} == {k: v["finding_id"] for k, v in b.f.items()}
    assert a.f["s/docs/a.md"]["evidence_blob"] != b.f["s/docs/a.md"]["evidence_blob"]


def test_without_a_blob_source_there_are_no_sections_and_the_run_is_the_m3_run(tmp_path):
    r = survey(tmp_path, PAGES, "nav:\n  - A: a.md\n", source=False)
    assert sections(r) == [] and r.allc == ["s"] and r.c["manifest_reading"]["enabled"] is False


def test_two_runs_are_byte_identical(tmp_path):
    nav = "nav:\n  - Home: index.md\n  - A: a.md\n  - G: [guide/one.md, guide/two.md]\n  - R: [ref/api.md, ref/cli.md]\n  - X: https://e.org\n"
    r1 = survey(tmp_path, PAGES, nav, out="o1", name="t1")
    r2 = survey(tmp_path, PAGES, nav, out="o2", name="t2")
    for n in ("components.txt", "components-all.txt", "findings.jsonl", "classes.json", "manifest-reads.txt"):
        assert (r1.out / n).read_bytes() == (r2.out / n).read_bytes(), n


# ---- the profile -------------------------------------------------------------------------------------------------------------------------
def test_the_docs_site_profile_is_0_3_0_with_a_section_rule_and_a_low_confidence_fallback():
    p = load_profile("docs-site", PROFILES)
    m = p.manifest_reading
    assert p.version == "0.3.0" and m.readers == ("mkdocs", "gitmodules") and m.member_rule is None and m.aggregator_rule is None
    assert (m.section_rule.confidence, m.fallback_section_rule.confidence) == ("high", "low")
    assert m.section_rule.kind == m.fallback_section_rule.kind == "doc-section" and m.docs_content_rule == "R-docs-site-content" and m.site_output_rule == "R-docs-site-output"
    assert all(r.evidence and r.tuned_on for r in (m.section_rule, m.fallback_section_rule))


def _doc(**change):
    d = yaml.safe_load((PROFILES / "docs-site.yaml").read_text())
    d["extends"] = []
    d["manifest_reading"].update(change)
    return d


@pytest.mark.parametrize("change,msg", [
    ({"section_rule": None}, "section_rule"), ({"readers": ["mkdocs", "cargo"]}, "member_rule"), ({"docs_content_rule": "R-nope"}, "not a rule of this profile"),
    ({"site_output_rule": 5}, "site_output_rule"), ({"fallback_site_rule": "R-nope"}, "not a rule of this profile"),
])
def test_a_bad_docs_manifest_reading_block_is_a_load_error(change, msg):
    d = _doc(**change)
    if change.get("section_rule", 1) is None:
        del d["manifest_reading"]["section_rule"]
    with pytest.raises(ProfileError, match=msg):
        parse_profile(d, "t", PROFILES)


# ---- a site recognized by a generator config FILE NAME (Docusaurus), never read ---------------------------------------------------------------------
DOCU = {"w/docusaurus.config.js": "module.exports = {secret: 'NEVER READ'};", "w/docs/index.md": "x", "w/docs/intro/a.md": "x", "w/docs/intro/b.md": "x", "w/docs/guides/g.mdx": "x",
        "w/docs/assets/logo.md": "x", "w/docs/img/p.png": "x", "w/docs/_partials/p.md": "x", "w/docs/top.md": "x", "w/sidebars.js": "module.exports = {}"}


@pytest.mark.parametrize("config", ["docusaurus.config.js", "docusaurus.config.ts", "docusaurus.config.mjs", "docusaurus.config.cjs"])
def test_a_docusaurus_config_file_name_makes_its_directory_a_docs_site_with_fallback_sections(tmp_path, config):
    files = {k.replace("docusaurus.config.js", config): v for k, v in DOCU.items()}
    r = survey(tmp_path, files, None, site="")
    assert r.comps == ["w"] and r.f["w"]["rule_id"] == "R-docs-site-docusaurus" and r.f["w"]["kind"] == "docs-site" and r.f["w"]["basis"] == "convention"
    assert sections(r) == ["w/docs/guides", "w/docs/intro"]
    g = r.f["w/docs/intro"]
    assert g["rule_id"] == "M-docs-section-folder" and g["confidence"] == "low" and g["part_of"] == "w" and g["identity"] == "folder-fallback"
    assert r.f["w"]["docs_dir"] == "docs" and r.f["w/docs"]["role"] == "docs"                                        # the generator default content folder is claimed


def test_the_generator_config_and_sidebars_are_never_opened(tmp_path):
    r = survey(tmp_path, DOCU, None, site="")
    assert r.rec.reading is None or r.rec.reading.log == []
    assert "NEVER READ" not in json.dumps(r.f) + (r.out / "report.md").read_text()
    assert not (r.out / "manifest-reads.txt").exists() or (r.out / "manifest-reads.txt").read_text() == ""


def test_the_docusaurus_fallback_does_not_need_a_blob_source_and_is_deterministic(tmp_path):
    a = survey(tmp_path, DOCU, None, site="", source=False, out="a", name="ta")
    b = survey(tmp_path, DOCU, None, site="", out="b", name="tb")
    assert sections(a) == sections(b) == ["w/docs/guides", "w/docs/intro"]
    assert (a.out / "components-all.txt").read_bytes() == (b.out / "components-all.txt").read_bytes()


def test_a_plain_docs_folder_with_no_generator_config_is_still_not_a_site(tmp_path):
    r = survey(tmp_path, {"docs/guide/a.md": "x", "docs/ref/b.md": "x", "sidebars.js": "x", "docusaurus.md": "x"}, None, site="")
    assert sections(r) == [] and r.comps == ["docs"] and r.f["docs"]["kind"] == "documentation"


def test_a_docusaurus_config_inside_a_hidden_subtree_makes_no_site(tmp_path):
    r = survey(tmp_path, {"node_modules/x/docusaurus.config.js": "x", "node_modules/x/docs/g/a.md": "x"}, None, site="")
    assert sections(r) == [] and r.comps == []
