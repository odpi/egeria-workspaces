"""M3: the docs-site profile (names only), its composition with the M2 conventions in both orders, diamond composition, and the
candidate-copies report. Synthetic path lists; the tune-tree pins skip when the lists are not given."""
import json
import os
import shutil
from pathlib import Path

import pytest
import yaml

from recognizer.layout_profile import ProfileError, load_profile, parse_profile
from recognizer.recognize import Recognizer

PROFILES = Path(__file__).resolve().parent.parent / "profiles"


def run(tmp_path, rows, profile="docs-site", out="out", profiles_dir=PROFILES, copies=()):
    p = tmp_path / f"{out}.tsv"
    p.write_text("".join(f"{r}\n" for r in rows))
    c = Recognizer(load_profile(profile, profiles_dir)).run(p, tmp_path / out, copies_of=tuple(copies))
    f = [x for x in (json.loads(y) for y in (tmp_path / out / "findings.jsonl").read_text().splitlines()) if not x["rule_id"].startswith("F-")]   # the file-role layer (M5) is tested in test_m5
    return c, f, {(x["path"], x["rule_id"]): x for x in f}


def lines(tmp_path, name, out="out"):
    return (tmp_path / out / name).read_text().splitlines()


SITE = ["mkdocs.yml", "docs/index.md", "docs/guide/a.md", "site/index.html", "site/404.html"]


def test_profile_loads_with_evidence_and_tuned_on():
    p = load_profile("docs-site", PROFILES)
    own = [r for r in p.rules if r.origin == "docs-site"]
    assert [r.id for r in own][0] == "R-docs-site-mkdocs"                       # the mkdocs.yml rule is first
    assert all(r.evidence and r.tuned_on and set(r.tuned_on) <= {"mkdocs-sample", "trellis", "note 568fc678 (no repository looked at)"} for r in own)
    assert [pid for pid, _ in p.composed_of] == ["docs-site", "generic-relevance"]


def test_a_directory_with_mkdocs_yml_is_a_docs_site_with_its_default_children(tmp_path):
    rows = ["web/" + r for r in SITE] + ["web/overrides/main.html"]
    c, f, by = run(tmp_path, rows)
    assert by[("web", "R-docs-site-mkdocs")]["kind"] == "docs-site" and by[("web", "R-docs-site-mkdocs")]["basis"] == "manifest"
    assert by[("web/docs", "R-docs-site-content")]["role"] == "docs" and by[("web/docs", "R-docs-site-content")]["files"] == 2
    out = by[("web/site", "R-docs-site-output")]
    assert out["role"] == "generated" and out["relevance"] == "hidden" and out["files"] == 2          # hidden AND counted
    assert lines(tmp_path, "components-all.txt") == ["web"]


def test_mkdocs_yaml_spelling_also_counts(tmp_path):
    c, f, by = run(tmp_path, ["a/mkdocs.yaml", "a/docs/x.md"])
    assert ("a", "R-docs-site-mkdocs") in by and ("a/docs", "R-docs-site-content") in by


def test_docs_and_site_only_count_beside_a_mkdocs_file(tmp_path):
    c, f, by = run(tmp_path, ["pkg/docs/a.md", "pkg/site/index.html", "pkg/README.md"])
    assert not [k for k in by if k[1] in ("R-docs-site-content", "R-docs-site-output")]


def test_a_docs_folder_with_no_mkdocs_yml_is_documentation_not_a_site(tmp_path):
    c, f, by = run(tmp_path, ["docs/a.md", "docs/b.md", "docs/archive/old.md", "docs/experiments/e.md", "src/x.py"])
    x = by[("docs", "R-docs-folder-top-level")]
    assert x["kind"] == "documentation" and x["role"] == "component"
    assert not [k for k in by if k[1] == "R-docs-site-mkdocs"]
    arc = by[("docs/archive", "R-docs-archive-folder")]
    assert arc["role"] == "archive" and arc["relevance"] == "hidden" and arc["files"] == 1
    assert ("docs/experiments", "R-docs-archive-folder") not in by                       # no rule from one repository's working area
    assert lines(tmp_path, "components-all.txt") == ["docs"]


@pytest.mark.parametrize("name", ["old", "legacy", "saved", "experiments", "attic"])
def test_only_a_folder_named_archive_is_archived(tmp_path, name):
    c, f, by = run(tmp_path, [f"docs/{name}/a.md", "docs/live.md"])
    assert not [k for k in by if k[1] == "R-docs-archive-folder"]                         # no name that neither tuning tree contains


def test_the_archive_rule_is_exactly_the_archive_folder_and_one_tuning_tree_motivates_it():
    r = {x.id: x for x in load_profile("docs-site", PROFILES).rules}["R-docs-archive-folder"]
    assert sorted(r.match["path_glob"]) == ["doc/archive/**", "docs/archive/**"] and r.tuned_on == ("trellis",)
    assert "old" not in r.evidence.split() and "legacy" not in r.evidence and "saved" not in r.evidence


def test_in_the_docs_site_profile_mkdocs_yml_wins_over_the_docs_folder_rule(tmp_path):
    c, f, by = run(tmp_path, ["docs/mkdocs.yml", "docs/docs/a.md"])
    assert [k for k in by if k[0] == "docs" and k[1].startswith(("R-docs-site-mkdocs", "R-docs-folder"))] == [("docs", "R-docs-site-mkdocs")]


def compose(tmp_path, name, order):
    for n in ("generic-relevance", "docs-site", "code-repo", "code-repo-conventions"):
        shutil.copy(PROFILES / f"{n}.yaml", tmp_path / f"{n}.yaml")
    (tmp_path / f"{name}.yaml").write_text(
        f"profile_id: {name}\nversion: 0.1.0\nstatus: proposed\napplies_to: any\nextends: {order}\nroles: [component]\n"
        "relevance: {primary: [component], supporting: [], hidden: []}\nrules: []\n")


@pytest.mark.parametrize("order,winner", [(["docs-site", "code-repo-conventions"], "R-docs-site-mkdocs"),
                                          (["code-repo-conventions", "docs-site"], "R-conv-docs")])
def test_a_directory_is_claimed_once_in_either_composition_order(tmp_path, order, winner):
    compose(tmp_path, "both", order)
    c, f, by = run(tmp_path, ["docs/mkdocs.yml", "docs/a.md"], profile="both", profiles_dir=tmp_path)
    claims = [k for k in by if k[0] == "docs"]
    assert len(claims) == 1 and claims[0][1] == winner                    # first listed wins; never both


@pytest.mark.parametrize("order", [["docs-site", "code-repo-conventions"], ["code-repo-conventions", "docs-site"]])
def test_a_plain_docs_folder_is_claimed_once_in_either_order(tmp_path, order):
    compose(tmp_path, "both", order)
    c, f, by = run(tmp_path, ["docs/a.md", "tests/t.py"], profile="both", profiles_dir=tmp_path)
    assert len([k for k in by if k[0] == "docs"]) == 1


def test_a_shared_base_is_loaded_once_and_a_real_clash_is_still_an_error(tmp_path):
    compose(tmp_path, "both", ["docs-site", "code-repo-conventions"])           # both extend generic-relevance: a diamond
    p = load_profile("both", tmp_path)
    ids = [r.id for r in p.rules]
    assert len(ids) == len(set(ids)) and ids.count("R-vcs-git") == 1
    assert [pid for pid, _ in p.composed_of].count("generic-relevance") == 1
    base = yaml.safe_load((PROFILES / "worktree-copies.yaml").read_text())
    clash = {**base, "profile_id": "clash"}
    (tmp_path / "clash.yaml").write_text(yaml.safe_dump(clash))
    (tmp_path / "other.yaml").write_text(yaml.safe_dump({**base, "profile_id": "other", "extends": ["clash"]}))      # same rule id, two profiles
    with pytest.raises(ProfileError):
        load_profile("other", tmp_path)


def test_sections_are_not_components_here(tmp_path):
    c, f, by = run(tmp_path, ["mkdocs.yml", "docs/index.md", "docs/tutorials.md", "docs/guides/index.md", "docs/guides/a.md"])
    assert lines(tmp_path, "components-all.txt") == ["."]                  # no rule finds sections (the key says a section is not a component)


# ---- the candidate-copies report: names only, not a rule -----------------------------------------------------------------------------

def copies(tmp_path, rows, **kw):
    run(tmp_path, rows, copies=("docs-site",), **kw)
    return json.loads((tmp_path / "out" / "candidate-copies.json").read_text())


def site_files(prefix, extra=()):
    return [f"{prefix}/{n}" for n in ("mkdocs.yml", "docs/index.md", "docs/tutorials.md", "app/__init__.py", *extra)]


def test_sites_with_identical_file_name_sets_are_grouped_as_candidate_copies(tmp_path):
    rows = site_files("step_4") + site_files("step_5") + site_files("final", ("extra.md",)) + site_files("step_6")
    rep = copies(tmp_path, rows)
    assert rep["kinds"] == ["docs-site"]
    assert rep["groups"] == [{"files": 4, "members": ["step_4", "step_5", "step_6"], "names_sha256": rep["groups"][0]["names_sha256"]}]
    assert len(rep["groups"][0]["names_sha256"]) == 64


def test_hidden_output_and_environments_do_not_make_copies_differ(tmp_path):
    rows = site_files("a") + site_files("b") + ["a/site/index.html", "a/site/x.html", "b/venv/bin/python", "b/__pycache__/m.pyc"]
    rep = copies(tmp_path, rows)
    assert [g["members"] for g in rep["groups"]] == [["a", "b"]]          # a/site (generated) and b/venv (vendored) are hidden, so not compared


def test_no_group_when_nothing_is_identical_and_nothing_is_hidden_or_merged_by_the_report(tmp_path):
    rows = site_files("a") + site_files("b", ("more.md",))
    rep = copies(tmp_path, rows)
    assert rep["groups"] == []
    c, f, by = run(tmp_path, rows, out="plain")
    assert lines(tmp_path, "components-all.txt", "plain") == ["a", "b"]    # both stay separate components whatever the report says


def test_the_report_is_only_written_when_asked_and_is_deterministic(tmp_path):
    rows = site_files("a") + site_files("b")
    run(tmp_path, rows, out="x")
    assert not (tmp_path / "x" / "candidate-copies.json").exists()
    run(tmp_path, rows, out="y", copies=("docs-site",))
    run(tmp_path, list(reversed(rows)), out="z", copies=("docs-site",))
    assert (tmp_path / "y" / "candidate-copies.json").read_bytes() == (tmp_path / "z" / "candidate-copies.json").read_bytes()


def test_only_the_named_kind_is_compared(tmp_path):
    rows = ["a/pyproject.toml", "a/x.py", "b/pyproject.toml", "b/x.py"] + site_files("s1") + site_files("s2")
    p = tmp_path / "m.tsv"
    p.write_text("".join(r + "\n" for r in rows))
    from recognizer.layout_profile import load_profile as lp
    shutil.copy(PROFILES / "code-repo.yaml", tmp_path / "code-repo.yaml")
    shutil.copy(PROFILES / "docs-site.yaml", tmp_path / "docs-site.yaml")
    shutil.copy(PROFILES / "generic-relevance.yaml", tmp_path / "generic-relevance.yaml")
    (tmp_path / "both.yaml").write_text("profile_id: both\nversion: 0.1.0\nstatus: proposed\napplies_to: any\nextends: [docs-site, code-repo]\nroles: [component]\n"
                                        "relevance: {primary: [component], supporting: [], hidden: []}\nrules: []\n")
    Recognizer(lp("both", tmp_path)).run(p, tmp_path / "o", copies_of=("docs-site",))
    rep = json.loads((tmp_path / "o" / "candidate-copies.json").read_text())
    assert [g["members"] for g in rep["groups"]] == [["s1", "s2"]]        # the two identical python packages are NOT reported


# ---- the two tuning trees (pins; the lists are not in the repository) -----------------------------------------------------------------------

TUNE = os.environ.get("LAYOUT_TUNE_PATHS_DIR")


@pytest.mark.skipif(not TUNE or not (Path(TUNE) / "mkdocs-sample.paths.tsv").is_file(), reason="LAYOUT_TUNE_PATHS_DIR has no mkdocs-sample list")
def test_mkdocs_sample_has_five_sites_and_one_group_of_three_copies(tmp_path):
    Recognizer(load_profile("docs-site", PROFILES)).run(Path(TUNE) / "mkdocs-sample.paths.tsv", tmp_path, copies_of=("docs-site",))
    assert (tmp_path / "components-all.txt").read_text().split() == ["source_code_final", "source_code_step_4", "source_code_step_5", "source_code_step_6", "src"]
    rep = json.loads((tmp_path / "candidate-copies.json").read_text())
    assert [g["members"] for g in rep["groups"]] == [["source_code_step_4", "source_code_step_5", "source_code_step_6"]]
    classes = json.loads((tmp_path / "classes.json").read_text())
    assert classes["by_rule"]["R-docs-site-output"]["files"] == 90 and classes["by_rule"]["R-vend-installed"]["files"] == 17345   # hidden and counted


@pytest.mark.skipif(not TUNE or not (Path(TUNE) / "trellis.paths.tsv").is_file(), reason="LAYOUT_TUNE_PATHS_DIR has no trellis list")
def test_trellis_docs_is_one_documentation_component_with_archive_hidden(tmp_path):
    Recognizer(load_profile("docs-site", PROFILES)).run(Path(TUNE) / "trellis.paths.tsv", tmp_path)
    assert (tmp_path / "components-all.txt").read_text().split() == ["docs"]
    classes = json.loads((tmp_path / "classes.json").read_text())
    assert classes["by_rule"]["R-docs-archive-folder"]["files"] == 2
