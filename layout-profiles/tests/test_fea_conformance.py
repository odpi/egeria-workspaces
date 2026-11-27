"""Phase 2 notebook 04a, A2: conformance and drift on generated sweeps (samples/fea_sweep_gen.py) with the fea-sweep profile 0.1.0 and its
instance (the declared grid). The engine features F2 (a required file per typed folder, with when_present, and the typing of folders that hold only
hidden files), F3 (states), F4 (--instance: off-grid and duplicate), F5 (match_of) and F6 (parts drift), each with a test that it is off when
absent. Synthetic files only; names only, except the instance file."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

from recognizer import drift
from recognizer import grammar as gm
from recognizer.layout_profile import ProfileError, load_profile, parse_profile
from recognizer.recognize import Recognizer, load_instance

ROOT = Path(__file__).resolve().parent.parent
PROFILES = ROOT / "profiles"
SPECS = ROOT / "samples" / "specs"
sys.path.insert(0, str(ROOT / "samples"))
import fea_sweep_gen as g  # noqa: E402

PROF = load_profile("fea-sweep", PROFILES)


def write_instance(tmp_path, lay, extra_e=(), name="instance.yaml"):
    p = tmp_path / name
    g.write_instance(g.instance(lay, extra_e), p)
    return p


def survey(tmp_path, files, name="o", inst=None, prof=None):
    lst = tmp_path / f"{name}.tsv"
    lst.write_text("".join(f"{p}\t{len(files[p])}\n" for p in sorted(files)))
    r = Recognizer(prof or PROF, instance=load_instance(inst, prof or PROF)[0] if inst else None)
    if inst:
        r.instance_file = load_instance(inst, prof or PROF)[1]
    c = r.run(lst, tmp_path / name)
    fs = [json.loads(x) for x in (tmp_path / name / "findings.jsonl").read_text().splitlines()]
    return c, [f for f in fs if f.get("grain") == "conformance"], fs


def key(f):
    return (f["path"], f["kind"], f["status"])


# ---- clean -> mutated: the new findings are exactly the truth set --------------------------------------------------------------------------------
@pytest.mark.parametrize("seed", [1, 2, 3])
@pytest.mark.parametrize("spec", ["fea-a.yaml", "fea-b.yaml"])
def test_clean_to_mutated_new_findings_are_exactly_the_truth(tmp_path, seed, spec):
    lay = g.layout(seed)
    inst = write_instance(tmp_path, lay)
    clean, _ = g.generate(seed)
    files, truth = g.generate(seed, spec=g.load_spec(SPECS / spec))
    c0, f0, _ = survey(tmp_path, clean, "clean", inst)
    c1, f1, _ = survey(tmp_path, files, "mut", inst)
    assert f0 == [] and c0["conformance"]["score"] == 1.0
    d = drift.write(tmp_path / "clean", tmp_path / "mut")
    assert d["counts"]["resolved"] == 0 and d["counts"]["unchanged"] == 0
    assert sorted(key(f) for f in d["new"]) == sorted(key(t) for t in truth)
    rules = {f["path"]: f["rule_id"] for f in d["new"]}
    for t in truth:
        if "rule" in t:
            assert rules[t["path"]] == t["rule"]


def test_the_rules_and_evidence_of_each_class(tmp_path):
    lay = g.layout(1)
    inst = write_instance(tmp_path, lay)
    files, truth = g.generate(1, spec=g.load_spec(SPECS / "fea-a.yaml"))
    _, fs, _ = survey(tmp_path, files, "m", inst)
    by = {t["class"]: next(f for f in fs if f["path"] == t["path"]) for t in truth if t["class"] != "off-grammar-case-name"}
    gid = g.instance(lay)["id"]
    assert by["missing-input-deck"]["rule_id"] == by["results-without-deck"]["rule_id"] == "RQ-case-deck"
    assert by["off-grid-value"]["rule_id"] == by["bad-mesh-level"]["rule_id"] == f"{gid}.off-grid"
    assert "token t = 9p9 is not in the declared grid t: [" in by["off-grid-value"]["evidence"]
    assert by["bad-mesh-level"]["evidence"].startswith("token mesh = ") and by["bad-mesh-level"]["reason"] == "mesh"
    dup = by["duplicate-combination"]
    assert dup["rule_id"] == f"{gid}.duplicate" and dup["evidence"].startswith("the same parameters as " + lay["study"] + "/cases/case_E0")
    assert (by["orphan-post"]["rule_id"], by["orphan-post"]["evidence"], by["orphan-post"]["reason"]) == ("PG-post-case", "no matching case", "no-match")
    assert by["stray-deck"]["rule_id"] == "AO-cases" and by["unexpected-top-level-folder"]["rule_id"] == "AO-study"


# ---- F2: a required file per case, and job.sta where job.frd is ---------------------------------------------------------------------------------
def test_a_case_that_ran_needs_its_status_file_and_one_that_did_not_does_not(tmp_path):
    files, _ = g.generate(2)
    lay = g.layout(2)
    s = lay["study"]
    ran, notrun = lay["ran"][0], next(c for c in lay["cases"] if c not in lay["ran"])
    del files[f"{s}/cases/{ran}/job.sta"]
    assert f"{s}/cases/{notrun}/job.sta" not in files
    _, fs, _ = survey(tmp_path, files)
    assert [(f["path"], f["kind"], f["status"], f["rule_id"]) for f in fs] == [(f"{s}/cases/{ran}/job.sta", "structure", "missing", "RQ-case-status")]


def test_a_case_with_only_hidden_files_is_typed_so_its_missing_deck_is_found(tmp_path):
    files, truth = g.generate(1, spec=g.parse_spec({"mutations": [{"class": "missing-input-deck"}]}))
    case = truth[0]["path"].rsplit("/", 1)[0]
    assert sorted(p for p in files if p.startswith(case + "/")) == [case + "/run.log"]           # run.log only, and run.log is hidden
    c, fs, all_ = survey(tmp_path, files)
    assert [key(f) for f in fs] == [key(truth[0])]
    assert any(f["path"] == case and f.get("part_of") for f in all_)                             # it is a part, as in A1 (parts come from all names)


def without(doc_key_filter):
    import yaml
    doc = yaml.safe_load((PROFILES / "fea-sweep.yaml").read_text())
    doc_key_filter(doc)
    return parse_profile(doc, "<test>", PROFILES)


def test_part_formation_and_hidden_shares_do_not_change_with_the_f2_typing(tmp_path):
    files, _ = g.generate(1, spec=g.parse_spec({"mutations": [{"class": "missing-input-deck", "count": 3}]}))
    no_f2 = without(lambda d: d.pop("required"))
    a, _, fa = survey(tmp_path, files, "with")
    b, fsb, fb = survey(tmp_path, files, "without", prof=no_f2)
    assert fsb == []                                                                             # without F2: the hidden-only cases are not typed
    for k in ("components", "shares", "by_relevance", "by_role", "by_rule"):
        assert a[k] == b[k]
    strip = lambda fs: [{k: v for k, v in f.items() if k not in ("tokens", "yields")} for f in fs if f["grain"] != "conformance"]
    assert strip(fa) == strip(fb)
    # the one difference: a case of hidden files only is typed with F2, so its part finding also carries its tokens (F1)
    assert sum(1 for f in fa if "tokens" in f) == sum(1 for f in fb if "tokens" in f) + 3


def test_hidden_subtrees_stay_out_of_the_typing(tmp_path):
    files, _ = g.generate(1)
    s = g.layout(1)["study"]
    files[f"{s}/scratch/case_E1_t1p0_mesh-fine/run.log"] = b"x\n"           # inside scratch/ (a hidden subtree): never typed or judged
    files[f"{s}/scratch/misc/run.log"] = b"x\n"
    _, fs, _ = survey(tmp_path, files)
    assert fs == []


def test_required_file_items_are_validated():
    base = {"id": "RQ-x", "basis": "convention", "confidence": "high", "evidence": "e"}
    for bad in ({"of": "PG-a", "path": "x", "for_each": ["t"]}, {"path": "x", "when_present": "y"}, {"of": "PG-a", "path": "/x"},
                {"of": "PG-a", "path": "x", "when_present": "../y"}):
        with pytest.raises(gm.GrammarError):
            gm.compile_required("t", {**base, **bad}, "o", ("convention",), ("high",), __import__("re").compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$"))


# ---- F3: the not-run state ----------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("seed,frac", [(1, 0.8), (2, 0.5), (3, 1.0)])
def test_not_run_is_a_count_not_a_finding(tmp_path, seed, frac):
    files, _ = g.generate(seed, ran_fraction=frac)
    lay = g.layout(seed, ran_fraction=frac)
    c, fs, _ = survey(tmp_path, files)
    st = c["conformance"]["states"]["not-run"]
    s = lay["study"]
    assert st["checked"] == 60 and st["count"] == 60 - len(lay["ran"]) and st["rule_id"] == "ST-not-run"
    assert st["paths"] == sorted(f"{s}/cases/{x}" for x in lay["cases"] if x not in lay["ran"])
    assert fs == [] and c["conformance"]["score"] == 1.0
    no_states = without(lambda d: d.pop("states"))
    c2, _, _ = survey(tmp_path, files, "ns", prof=no_states)
    assert "states" not in c2["conformance"] and c2["conformance"]["checked"] == c["conformance"]["checked"]


# ---- F4: the instance (declared grid) -----------------------------------------------------------------------------------------------------------
def test_without_an_instance_there_is_no_grid_check(tmp_path):
    files, truth = g.generate(1, spec=g.load_spec(SPECS / "fea-a.yaml"))
    c, fs, _ = survey(tmp_path, files)
    grid_classes = {"off-grid-value", "duplicate-combination", "bad-mesh-level"}
    assert sorted(key(f) for f in fs) == sorted(key(t) for t in truth if t["class"] not in grid_classes)
    assert "instance" not in c["conformance"] and "grid" not in c["conformance"]["checked"]
    assert not (tmp_path / "o" / "content-reads.txt").exists()


def test_the_instance_is_the_only_content_read_and_is_recorded(tmp_path):
    lay = g.layout(1)
    inst = write_instance(tmp_path, lay)
    files, _ = g.generate(1)
    c, fs, _ = survey(tmp_path, files, "o", inst)
    assert (tmp_path / "o" / "content-reads.txt").read_text() == "instance: instance.yaml\n"
    i = c["conformance"]["instance"]
    import hashlib
    assert i["file"] == "instance.yaml" and i["sha256"] == hashlib.sha256(inst.read_bytes()).hexdigest() and i["grid_checked"] == 120
    assert c["conformance"]["checked"]["grid"] == 120 and fs == []


def test_numbers_are_normalised_with_p_as_the_decimal_point():
    n = gm.norm_token
    assert n("2p00") == n("2p0") == n(2.0) == n("2") and n("E") == "E"
    assert n("0210") == n("210") == n(210) and n("fine") == "fine" and n("2p5") != n("2p0")


@pytest.mark.parametrize("variant", ["E", "t"])
def test_a_duplicate_is_the_second_folder_in_sorted_order(tmp_path, variant):
    lay = g.layout(3)
    files, truth = g.generate(3, spec=g.parse_spec({"mutations": [{"class": "duplicate-combination", "variant": variant}]}))
    _, fs, _ = survey(tmp_path, files, "o", write_instance(tmp_path, lay))
    assert [key(f) for f in fs] == [key(truth[0])]
    first = fs[0]["evidence"][len("the same parameters as "):]
    assert first < fs[0]["path"] and first + "/job.inp" in files and fs[0]["path"] + "/job.inp" in files


@pytest.mark.parametrize("doc,msg", [({"instance_of": "bids-dataset", "id": "x", "grid": {"PG-case": {"E": [1]}}}, "not the profile"),
                                     ({"instance_of": "fea-sweep", "id": "x", "grid": {"PG-nope": {"E": [1]}}}, "not a path_grammar"),
                                     ({"instance_of": "fea-sweep", "id": "x", "grid": {"PG-case": {"q": [1]}}}, "not a token"),
                                     ({"instance_of": "fea-sweep", "id": "x", "grid": {"PG-case": {"t": ["2p0", 2.0]}}}, "twice"),
                                     ({"instance_of": "fea-sweep", "id": "x", "grid": {"PG-case": {"E": []}}}, "non-empty"),
                                     ({"instance_of": "fea-sweep", "id": "x", "grid": {"PG-case": {"E": [1]}}, "extra": 1}, "unknown key"),
                                     ({"instance_of": "fea-sweep", "id": "x y", "grid": {"PG-case": {"E": [1]}}}, "identifier")])
def test_bad_instances_are_refused(tmp_path, doc, msg):
    import yaml
    p = tmp_path / "i.yaml"
    p.write_text(yaml.safe_dump(doc))
    with pytest.raises(ProfileError, match=msg):
        load_instance(p, PROF)


def test_the_instance_on_the_command_line(tmp_path):
    lay = g.layout(2)
    inst = write_instance(tmp_path, lay)
    files, truth = g.generate(2, spec=g.parse_spec({"mutations": [{"class": "off-grid-value"}]}))
    (tmp_path / "p.tsv").write_text("".join(f"{p}\t{len(files[p])}\n" for p in sorted(files)))
    r = subprocess.run([sys.executable, "-m", "recognizer.recognize", str(tmp_path / "p.tsv"), "--out", str(tmp_path / "o"), "--profile", "fea-sweep",
                        "--instance", str(inst)], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    fs = [json.loads(x) for x in (tmp_path / "o" / "findings.jsonl").read_text().splitlines() if '"conformance"' in x]
    assert [key(f) for f in fs] == [key(truth[0])]


# ---- F5: match_of --------------------------------------------------------------------------------------------------------------------------------
def test_a_post_folder_needs_a_case_of_the_same_normalised_tokens(tmp_path):
    files, _ = g.generate(1)
    lay = g.layout(1)
    s, c = lay["study"], lay["ran"][0]
    k = g.parse_case(c)
    spelt = f"case_E0{k['E']}_t{k['t']}0_mesh-{k['mesh']}"                 # the same parameters, spelt differently: it matches
    files[f"{s}/post/{spelt}/summary.csv"] = b"x\n"
    files[f"{s}/post/case_E999_t{k['t']}_mesh-{k['mesh']}/summary.csv"] = b"x\n"
    _, fs, _ = survey(tmp_path, files)
    assert [(f["path"], f["status"], f["evidence"]) for f in fs] == [(f"{s}/post/case_E999_t{k['t']}_mesh-{k['mesh']}", "unexpected", "no matching case")]


def test_match_of_is_off_when_absent_and_validated(tmp_path):
    files, truth = g.generate(1, spec=g.parse_spec({"mutations": [{"class": "orphan-post"}]}))
    no_match = without(lambda d: [p.pop("match_of", None) for p in d["path_grammar"]])
    _, fs, _ = survey(tmp_path, files, prof=no_match)
    assert fs == []
    for bad in ("PG-nope", "PG-post-case"):
        with pytest.raises(ProfileError):
            without(lambda d: next(p for p in d["path_grammar"] if p["id"] == "PG-post-case").update(match_of=bad))
    with pytest.raises(ProfileError, match="shares no token"):
        without(lambda d: next(p for p in d["path_grammar"] if p["id"] == "PG-post-case").update(match_of="PG-cases") or
                next(p for p in d["path_grammar"] if p["id"] == "PG-cases").update(pattern="cases", tokens={}))


# ---- F6 and the drift of a sweep ----------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("seed", [1, 2, 3])
def test_drift_after_adding_6_removing_2_and_renaming_1(tmp_path, seed):
    lay = g.layout(seed)
    files, _ = g.generate(seed)
    later, e_new, renames = g.evolve(files, lay, seed)
    inst = write_instance(tmp_path, lay, (e_new,))
    a, _, fa = survey(tmp_path, files, "a", inst)
    b, _, fb = survey(tmp_path, later, "b", inst)
    assert (a["components"], b["components"]) == ({"top_level": 1, "parts": 60}, {"top_level": 1, "parts": 64})
    d = drift.write(tmp_path / "a", tmp_path / "b")
    assert d["counts"] == {"new": 0, "resolved": 0, "unchanged": 0, "changed": 0}
    new = [f["path"].rsplit("/", 1)[1] for f in d["parts"]["new"]]
    res = [f["path"].rsplit("/", 1)[1] for f in d["parts"]["resolved"]]
    (old, moved), = renames
    assert len(new) == 7 and len(res) == 3 and d["parts"]["unchanged"] == 57
    assert moved in new and old in res                                       # the rename: one resolved and one new (ids are path-based)
    assert sum(1 for x in new if x.startswith(f"case_E{e_new}_") and x != moved) == 6
    assert "Parts: 7 new, 3 resolved, 57 unchanged" in (tmp_path / "b" / "report.md").read_text()


def test_drift_has_no_parts_key_without_part_findings(tmp_path):
    import bids_gen
    for name, spec in (("a", None), ("b", bids_gen.load_spec(SPECS / "drift-b.yaml"))):
        files, _ = bids_gen.generate(1, 6, 2, spec)
        survey(tmp_path, files, name, prof=load_profile("bids-dataset", PROFILES))
    d = drift.write(tmp_path / "a", tmp_path / "b")
    assert "parts" not in d and "Parts:" not in (tmp_path / "b" / "report.md").read_text()


def test_two_runs_are_byte_identical(tmp_path):
    lay = g.layout(2)
    inst = write_instance(tmp_path, lay)
    files, _ = g.generate(2, spec=g.load_spec(SPECS / "fea-a.yaml"))
    clean, _ = g.generate(2)
    for run in ("r1", "r2"):
        survey(tmp_path, clean, f"{run}-a", inst)
        survey(tmp_path, files, f"{run}-b", inst)
        drift.write(tmp_path / f"{run}-a", tmp_path / f"{run}-b")
    for side in ("a", "b"):
        names = sorted(p.name for p in (tmp_path / f"r1-{side}").iterdir())
        assert names == sorted(p.name for p in (tmp_path / f"r2-{side}").iterdir())
        for n in names:
            assert (tmp_path / f"r1-{side}" / n).read_bytes() == (tmp_path / f"r2-{side}" / n).read_bytes(), n


def test_states_are_validated():
    import re
    rid = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
    base = {"id": "ST-x", "of": "PG-a", "name": "n", "absent": "f", "basis": "convention", "confidence": "high", "evidence": "e"}
    assert gm.compile_state("t", base, "o", ("convention",), ("high",), rid).absent == "f"
    for bad in ({"absent": "../f"}, {"name": ""}, {"extra": 1}):
        with pytest.raises(gm.GrammarError):
            gm.compile_state("t", {**base, **bad}, "o", ("convention",), ("high",), rid)
    with pytest.raises(ProfileError, match="not a path_grammar id"):
        without(lambda d: d["states"][0].update(of="PG-nope"))
    with pytest.raises(ProfileError, match="used twice"):
        without(lambda d: d["states"].append({**d["states"][0], "id": "ST-other"}))
