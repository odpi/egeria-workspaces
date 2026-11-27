"""Phase 2 notebook 04a, A1: the fea-sweep profile 0.1.0 on generated sweeps (samples/fea_sweep_gen.py): collapse (UC1), hiding (UC13), the
parameter tokens on the part findings (F1) and the closed sets of the study, cases/ and each case. Synthetic files only; names and sizes only."""
import json
import sys
from pathlib import Path

import pytest

from recognizer.layout_profile import load_profile, parse_profile
from recognizer.recognize import Recognizer

ROOT = Path(__file__).resolve().parent.parent
PROFILES = ROOT / "profiles"
sys.path.insert(0, str(ROOT / "samples"))
import fea_sweep_gen as g  # noqa: E402

PROF = load_profile("fea-sweep", PROFILES)
GENERIC = load_profile("generic-relevance", PROFILES)


def survey(tmp_path, files, name="o", prof=None):
    lst = tmp_path / f"{name}.tsv"
    lst.write_text("".join(f"{p}\t{len(files[p])}\n" for p in sorted(files)))
    c = Recognizer(prof or PROF).run(lst, tmp_path / name)
    fs = [json.loads(x) for x in (tmp_path / name / "findings.jsonl").read_text().splitlines()]
    return c, fs


def conf(fs):
    return [f for f in fs if f.get("grain") == "conformance"]


def parts(fs):
    return [f for f in fs if f.get("grain") == "component" and f.get("part_of")]


# ---- the profile --------------------------------------------------------------------------------------------------------------------------------
def test_the_profile_is_tuned_on_generated_sweeps_only():
    assert PROF.version == "0.1.0" and PROF.status == "proposed" and PROF.extends == ("generic-relevance",)
    own = [r for r in PROF.rules if r.origin == "fea-sweep"] + [x for x in PROF.path_grammar if x.origin == "fea-sweep"]
    assert own and all(x.tuned_on in ((), ("generated (fea_sweep_gen seeds 1-3)",)) for x in own)
    assert any(x.tuned_on for x in own)


# ---- collapse (UC1) -----------------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("seed", [1, 2, 3])
def test_clean_sweep_is_one_component_with_60_parts_and_fully_conformant(tmp_path, seed):
    files, _ = g.generate(seed)
    lay = g.layout(seed)
    c, fs = survey(tmp_path, files)
    assert c["components"] == {"top_level": 1, "parts": 60}
    assert (tmp_path / "o" / "components.txt").read_text() == lay["study"] + "\n"
    top = [f for f in fs if f.get("grain") == "component" and not f.get("part_of")]
    assert [(f["path"], f["kind"]) for f in top] == [(lay["study"], "simulation-sweep")]
    ps = parts(fs)
    assert sorted(f["path"].rsplit("/", 1)[1] for f in ps) == sorted(lay["cases"])
    assert all(f["part_of"] == lay["study"] and f["kind"] == "simulation-case" for f in ps)
    assert conf(fs) == [] and c["conformance"]["score"] == 1.0 and c["conformance"]["findings_total"] == 0
    assert c["shares"]["unclassified_files"] == 0.0


def test_large_sweep_is_one_component_with_600_parts(tmp_path):
    files, _ = g.generate(1, g.LARGE_GRID)
    c, fs = survey(tmp_path, files)
    assert c["components"] == {"top_level": 1, "parts": 600} and conf(fs) == []


def test_generic_relevance_alone_names_no_component(tmp_path):
    files, _ = g.generate(1)
    c, _ = survey(tmp_path, files, prof=GENERIC)
    assert c["components"] == {"top_level": 0, "parts": 0}
    assert c["shares"]["unclassified_files"] > 0.5                  # it hides the .log and .bak files only


# ---- hiding (UC13) ------------------------------------------------------------------------------------------------------------------------------
def test_results_status_restart_logs_scratch_and_backups_are_hidden_the_rest_is_shown(tmp_path):
    files, _ = g.generate(1)
    c, fs = survey(tmp_path, files)
    rel = {}
    for f in (f for f in fs if f.get("grain") in ("dir", "subtree")):
        rel[f["rule_id"]] = f["relevance"]
    hidden = {"R-fea-results", "R-fea-restart", "R-fea-status", "R-fea-run-log", "R-fea-scratch", "R-fea-backup"}
    shown = {"R-fea-deck", "R-fea-templates", "R-fea-mesh", "R-fea-post", "R-fea-validation", "R-fea-study-files"}
    assert {k for k, v in rel.items() if v == "hidden"} == hidden and {k for k, v in rel.items() if v != "hidden"} == shown
    by_rule = c["by_rule"]
    n = lambda ext: sum(1 for p in files if p.endswith(ext) and "/cases/" in p)
    assert by_rule["R-fea-results"]["files"] == n(".frd") + n(".dat") + n(".12d")
    assert by_rule["R-fea-status"]["files"] == n(".sta") + n(".cvg") + n(".msg")
    assert by_rule["R-fea-run-log"]["files"] == 60 and by_rule["R-fea-deck"]["files"] == 60
    hid = sum(v["files"] for k, v in by_rule.items() if k in hidden)
    assert c["by_relevance"]["hidden"]["files"] == hid
    assert 0 < c["shares"]["hidden_files"] < 1 and 0 < c["shares"]["hidden_bytes"] < 1


# ---- tokens on the part findings (F1) -----------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("seed", [1, 2, 3])
def test_every_clean_case_carries_its_parameter_tokens(tmp_path, seed):
    files, _ = g.generate(seed)
    lay = g.layout(seed)
    _, fs = survey(tmp_path, files)
    ps = parts(fs)
    assert len(ps) == 60
    for f in ps:
        k = g.parse_case(f["path"].rsplit("/", 1)[1])
        assert f["yields"] == "case" and f["tokens"] == {"E": k["E"], "mesh": k["mesh"], "study": lay["study"][len("study-"):], "t": k["t"]}
    assert sorted((int(f["tokens"]["E"]), f["tokens"]["t"], f["tokens"]["mesh"]) for f in ps) == \
        sorted((e, g.fmt_t(t), m) for e in lay["E"] for t in lay["t"] for m in lay["mesh"])
    study = next(f for f in fs if f.get("kind") == "simulation-sweep")
    assert "tokens" not in study                                        # PG-study has no `yields`


def test_tokens_are_the_raw_name_strings(tmp_path):
    clean, _ = g.generate(1)
    files, _ = g.generate(1, spec=g.parse_spec({"mutations": [{"class": "duplicate-combination", "variant": "t"}]}))
    _, fs = survey(tmp_path, files)
    new = [f for f in parts(fs) if f["path"] + "/job.inp" not in clean]
    assert len(new) == 1 and len(new[0]["tokens"]["t"].split("p")[1]) == 2      # t2p00 stays "2p00" (no normalisation in F1)


def test_a_misnamed_case_is_a_part_without_tokens(tmp_path):
    files, truth = g.generate(1, spec=g.parse_spec({"mutations": [{"class": "off-grammar-case-name", "variant": "wrong-case"}]}))
    c, fs = survey(tmp_path, files)
    assert c["components"]["parts"] == 60
    bad = next(f for f in parts(fs) if f["path"] == truth[0]["path"])
    assert "tokens" not in bad and "yields" not in bad


def test_tokens_are_off_for_bids_whose_yields_patterns_type_no_component(tmp_path):
    sys.path.insert(0, str(ROOT / "samples"))
    import bids_gen
    files, _ = bids_gen.generate(1, 6, 2, bids_gen.load_spec(ROOT / "samples" / "specs" / "drift-a.yaml"))
    prof = load_profile("bids-dataset", PROFILES)
    assert any(p.yields for p in prof.path_grammar)                    # PG-subject yields subject, but no subject folder is a component
    _, fs = survey(tmp_path, files, prof=prof)
    assert len(fs) == 11 and not any("tokens" in f or "yields" in f for f in fs)    # the 13 of drift-a less its 2 content findings (no blob source)


def test_tokens_are_off_without_a_yields_pattern(tmp_path):
    doc = {"profile_id": "t-noyields", "version": "0.1.0", "status": "proposed", "applies_to": "any", "roles": ["component"],
           "relevance": {"primary": ["component"], "supporting": [], "hidden": []},
           "rules": [{"id": "R-c", "match": {"path_glob": "s/*"}, "assign": {"role": "component", "kind": "k"}, "grain": "component", "basis": "convention",
                      "confidence": "high", "evidence": "e"},
                     {"id": "R-s", "match": {"has_file": "m.yaml"}, "assign": {"role": "component", "kind": "root"}, "grain": "component", "basis": "manifest",
                      "confidence": "high", "evidence": "e"}],
           "path_grammar": [{"id": "PG-s", "pattern": "s", "tokens": {}, "basis": "convention", "confidence": "high", "evidence": "e"},
                            {"id": "PG-c", "pattern": "s/{x}", "tokens": {"x": {"regex": "[a-z]+"}}, "basis": "convention", "confidence": "high", "evidence": "e"}],
           "allowed_only": [{"id": "AO-r", "under": ".", "dirs": ["PG-s"], "basis": "convention", "confidence": "high", "evidence": "e"},
                            {"id": "AO-s", "under": ["PG-s"], "dirs": ["PG-c"], "files": ["m.yaml"], "basis": "convention", "confidence": "high", "evidence": "e"}]}
    prof = parse_profile(doc)
    files = {"s/m.yaml": b"", "s/a/f": b"", "s/b/f": b""}
    c, fs = survey(tmp_path, files, prof=prof)
    assert c["components"]["parts"] == 2 and not any("tokens" in f or "yields" in f for f in fs)
    doc["path_grammar"][1]["yields"] = "thing"                          # the same profile WITH yields: tokens on
    c, fs = survey(tmp_path, files, name="y", prof=parse_profile(doc))
    assert sorted(f["tokens"]["x"] for f in parts(fs)) == ["a", "b"]


# ---- the closed sets (what A1 checks; the per-case required files and the grid are A2) ---------------------------------------------------------
@pytest.mark.parametrize("variant", ["no-decimal", "wrong-case", "stray-suffix"])
def test_misnamed_case_folders_are_reported_under_the_rule_the_generator_expects(tmp_path, variant):
    files, truth = g.generate(2, spec=g.parse_spec({"mutations": [{"class": "off-grammar-case-name", "variant": variant}]}))
    _, fs = survey(tmp_path, files)
    assert [(f["path"], f["kind"], f["status"], f["rule_id"]) for f in conf(fs)] == [(t["path"], t["kind"], t["status"], t["rule"]) for t in truth]


@pytest.mark.parametrize("name", ["case_E210_t2_mesh-fine", "CASE_e210_T2P0_MESH-FINE", "case_E210_t2p0_final_v2", "case_E210_t2p0_mesh-",
                                  "case_E_t2p0_mesh-fine", "case_Ex_ty_mesh-z", "case_Ex_t_mesh-y", "xcase_E210_t2p0_mesh-fine", "notes"])
def test_the_rule_split_matches_the_stated_shape_criterion_on_the_boundary(tmp_path, name):
    files, _ = g.generate(1)
    s = g.layout(1)["study"]
    files = dict(files, **{f"{s}/cases/{name}/job.inp": b"x\n"})
    _, fs = survey(tmp_path, files)
    assert [(f["path"], f["status"], f["rule_id"]) for f in conf(fs)] == [(f"{s}/cases/{name}", "misnamed", g.expected_case_rule(name))]


def test_stray_deck_and_unexpected_folder_are_unexpected(tmp_path):
    files, truth = g.generate(3, spec=g.parse_spec({"mutations": [{"class": "stray-deck"}, {"class": "unexpected-top-level-folder"}]}))
    _, fs = survey(tmp_path, files)
    got = sorted((f["path"], f["kind"], f["status"], f["rule_id"]) for f in conf(fs))
    assert [x[:3] for x in got] == sorted((t["path"], t["kind"], t["status"]) for t in truth)
    assert sorted(x[3] for x in got) == ["AO-cases", "AO-study"]


def test_two_surveys_are_byte_identical(tmp_path):
    files, _ = g.generate(2, spec=g.parse_spec({"mutations": [{"class": c} for c in g.CLASSES]}))
    survey(tmp_path, files, "a")
    survey(tmp_path, files, "b")
    for f in sorted((tmp_path / "a").iterdir()):
        assert f.read_bytes() == (tmp_path / "b" / f.name).read_bytes(), f.name
