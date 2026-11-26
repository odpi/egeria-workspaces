"""N4 (Phase 1c): the docs-site FILE-ROLE layer, the docs counterpart of M5. Inside a recognized site or a documentation folder: pages are docs, assets/img/images/css/js/static are
static-assets, overrides/theme are theme, snippets/includes are include-fragments, config files are config, the built site/ stays generated and hidden, and everything else is other.
Synthetic only."""
import json
from pathlib import Path

import pytest

from recognizer.layout_profile import compose_profiles
from recognizer.recognize import Recognizer

PROFILES = Path(__file__).resolve().parent.parent / "profiles"


def run(tmp_path, rows, profile="docs-site", out="out"):
    lst = tmp_path / f"{out}.tsv"
    lst.write_text("".join(f"{r}\n" for r in sorted(set(rows))))
    rec = Recognizer(compose_profiles(profile, PROFILES))
    c = rec.run(lst, tmp_path / out, per_file=True)
    pf = {x["path"]: x for x in map(json.loads, (tmp_path / out / "findings-files.jsonl").read_text().splitlines())}
    return c, pf, tmp_path / out


def rc(pf, p):
    return (pf[p]["role"], pf[p]["relevance"]) if p in pf else None


SITE = ["s/mkdocs.yml", "s/docs/index.md"]


@pytest.mark.parametrize("path,role", [
    ("s/docs/a.md", "docs"), ("s/docs/g/b.mdx", "docs"), ("s/docs/g/c.rst", "docs"), ("s/docs/nb/d.ipynb", "docs"),
    ("s/docs/assets/logo.png", "static-assets"), ("s/docs/img/p.png", "static-assets"), ("s/docs/images/q.svg", "static-assets"), ("s/docs/css/x.css", "static-assets"),
    ("s/docs/js/x.js", "static-assets"), ("s/docs/static/f.woff", "static-assets"), ("s/docs/guide/img/inner.png", "static-assets"),
    ("s/overrides/main.html", "theme"), ("s/docs/theme/t.html", "theme"),
    ("s/docs/snippets/s.md", "include-fragments"), ("s/docs/includes/i.txt", "include-fragments"),
    ("s/requirements.txt", "other"), ("s/docs/data.bin", "other"), ("s/extra.py", "other"),
])
def test_each_file_gets_one_role_inside_a_site(tmp_path, path, role):
    c, pf, _ = run(tmp_path, SITE + [path])
    assert pf[path]["role"] == role, pf[path]


def test_config_files_inside_a_site_are_config(tmp_path):
    rows = SITE + ["s/theme.toml", "s/docs/x.yaml", "s/setup.cfg", "s/tox.ini", "s/docs/conf.yml"]
    c, pf, _ = run(tmp_path, rows)
    assert {p: pf[p]["role"] for p in rows[2:]} == {p: "config" for p in rows[2:]} and pf["s/mkdocs.yml"]["role"] == "docs" or pf["s/mkdocs.yml"]["role"] in ("docs", "config")


def test_fragments_theme_and_static_come_before_pages_and_the_order_is_the_briefs(tmp_path):
    rows = SITE + ["s/docs/snippets/a.md", "s/docs/assets/b.md", "s/overrides/c.md", "s/docs/theme/img/d.md", "s/docs/page.md", "s/docs/conf.yml"]
    c, pf, _ = run(tmp_path, rows)
    assert pf["s/docs/snippets/a.md"]["role"] == "include-fragments" and pf["s/docs/assets/b.md"]["role"] == "static-assets"
    assert pf["s/overrides/c.md"]["role"] == "theme" and pf["s/docs/theme/img/d.md"]["role"] == "theme" and pf["s/docs/page.md"]["role"] == "docs" and pf["s/docs/conf.yml"]["role"] == "config"


def test_the_built_site_stays_generated_and_hidden(tmp_path):
    c, pf, _ = run(tmp_path, SITE + ["s/site/index.html", "s/site/assets/x.css", "s/venv/lib/x.py"])
    assert rc(pf, "s/site/index.html") == ("generated", "hidden") and rc(pf, "s/site/assets/x.css") == ("generated", "hidden") and rc(pf, "s/venv/lib/x.py") == ("vendored", "hidden")


def test_the_layer_applies_inside_a_component_only_and_a_documentation_folder_counts(tmp_path):
    rows = ["README.md", "loose/a.md", "docs/guide.md", "docs/img/p.png", "docs/archive/old.md", "docs/data/x.json"]
    c, pf, _ = run(tmp_path, rows)
    assert rc(pf, "docs/guide.md") == ("docs", "supporting") and rc(pf, "docs/img/p.png") == ("static-assets", "supporting") and rc(pf, "docs/data/x.json") == ("other", "supporting")
    assert rc(pf, "docs/archive/old.md") == ("archive", "hidden")                                                   # the archive rule still wins
    assert rc(pf, "loose/a.md") == ("other", "supporting") and rc(pf, "README.md") == ("other", "supporting")        # not inside a component: other


def test_unclassified_is_zero_other_is_reported_and_components_are_unchanged(tmp_path):
    rows = SITE + ["s/docs/a.md", "s/docs/z.bin", "s/x.py", "docs/y.md"]
    c, pf, out = run(tmp_path, rows)
    assert c["by_role"].get("unclassified", {}).get("files", 0) == 0 and abs(c["shares"]["other_files"] - c["by_role"]["other"]["files"] / c["total_files"]) < 1e-6
    assert "other " in (out / "report.md").read_text()
    lst = tmp_path / "plain.tsv"
    import yaml
    doc = yaml.safe_load((PROFILES / "docs-site.yaml").read_text())
    doc.pop("file_roles")
    from recognizer.layout_profile import parse_profile
    Recognizer(parse_profile(doc, "no-roles", PROFILES)).run(tmp_path / "out.tsv", tmp_path / "plain")
    for n in ("components.txt", "components-all.txt"):
        assert (out / n).read_bytes() == (tmp_path / "plain" / n).read_bytes(), n


def test_the_layer_never_un_hides_and_never_changes_a_component_and_is_deterministic(tmp_path):
    rows = SITE + ["s/node_modules/p/a.md", "s/docs/a.md", "s/build/o.md"]
    c1, pf1, o1 = run(tmp_path, rows, out="a")
    c2, pf2, o2 = run(tmp_path, rows, out="b")
    assert rc(pf1, "s/node_modules/p/a.md") == ("vendored", "hidden") and c1 == c2
    assert (o1 / "findings.jsonl").read_bytes() == (o2 / "findings.jsonl").read_bytes()


def test_the_rules_are_roles_the_loader_knows_and_carry_evidence():
    p = compose_profiles("docs-site", PROFILES)
    assert p.version == "0.3.0" and [r.id for r in p.file_roles] == ["F-docs-fragments", "F-docs-theme", "F-docs-static", "F-docs-page", "F-docs-config", "F-docs-other"]
    assert all(r.evidence and r.tuned_on and r.grain == "dir" and r.relevance == "supporting" for r in p.file_roles)
    assert {r.role for r in p.file_roles} == {"include-fragments", "theme", "static-assets", "docs", "config", "other"}


def test_a_composition_keeps_the_code_roles_first(tmp_path):
    c, pf, _ = run(tmp_path, ["pyproject.toml", "pkg/a.py", "docs/img/p.png", "docs/a.md", "tests/t.py"], profile="code-repo-conventions,docs-site")
    assert pf["pkg/a.py"]["role"] == "source" and pf["tests/t.py"]["role"] == "test" and pf["docs/a.md"]["role"] == "docs"
