"""Phase 2 notebook 05, B1: path_grammar, name_grammar, required and allowed_only are evaluated (recognizer/grammar.py). Synthetic only.
A small test profile, written here, NOT the bids-dataset profile (that is B2). Each feature is tested both ways."""
import copy
import hashlib
import json
from pathlib import Path

import pytest
import yaml

from recognizer.layout_profile import ProfileError, load_profile, parse_profile
from recognizer.recognize import Recognizer

PROFILES = Path(__file__).resolve().parent.parent / "profiles"
README = Path(__file__).resolve().parent.parent / "README.md"

C = {"basis": "convention", "confidence": "high"}
DOC = {
    "profile_id": "gtest", "version": "1.2.0", "status": "proposed", "applies_to": "any", "roles": ["component"],
    "relevance": {"primary": ["component"]}, "rules": [],
    "path_grammar": [
        {"id": "PG-sub", "pattern": "sub-{sub}", "tokens": {"sub": {"regex": "[a-zA-Z0-9]+"}}, "yields": "subject", **C, "evidence": "subjects"},
        {"id": "PG-ses", "pattern": "sub-{sub}/ses-{ses}", "tokens": {"sub": {"regex": "[a-zA-Z0-9]+"}, "ses": {"regex": "[a-zA-Z0-9]+"}}, **C, "evidence": "sessions"},
        {"id": "PG-dt", "pattern": "sub-{sub}/{datatype}", "tokens": {"sub": {"regex": "[a-zA-Z0-9]+"}, "datatype": {"values": ["anat", "func"]}}, **C,
         "evidence": "datatype folders"},
        {"id": "PG-dt-ses", "pattern": "sub-{sub}/ses-{ses}/{datatype}",
         "tokens": {"sub": {"regex": "[a-zA-Z0-9]+"}, "ses": {"regex": "[a-zA-Z0-9]+"}, "datatype": {"values": ["anat", "func"]}}, **C, "evidence": "datatype folders"},
    ],
    "name_grammar": [{
        "id": "NG-f", **C, "evidence": "entity file names",
        "entities": [{"key": "sub", "token": "sub"}, {"key": "ses", "token": "ses"}, {"key": "task", "required_for": ["bold"]}, {"key": "run", "label": "[0-9]+"}],
        "label": "[a-zA-Z0-9]+",
        "suffixes": {"by_token": "datatype", "values": {"anat": ["T1w"], "func": ["bold", "events"]}},
        "extensions": {"default": [".nii.gz", ".json"], "by_suffix": {"events": [".tsv"]}},
    }],
    "required": [
        {"id": "RQ-desc", "path": "description.json", **C, "evidence": "the dataset description"},
        {"id": "RQ-ses", "of": "PG-ses", "for_each": ["sub"], **C, "evidence": "every subject has every session"},
        {"id": "RQ-dt-ses", "of": "PG-dt-ses", "for_each": ["sub"], **C, "evidence": "every subject has every datatype folder"},
    ],
    "allowed_only": [
        {"id": "AO-root", "under": ".", "dirs": ["PG-sub"], "files": ["description.json", "README"], "not_checked": ["derivatives", "*.md"], **C,
         "evidence": "closed top level"},
        {"id": "AO-sub", "under": "PG-sub", "dirs": ["PG-ses", "PG-dt"], **C, "evidence": "closed subject folder"},
        {"id": "AO-ses", "under": "PG-ses", "dirs": ["PG-dt-ses"], **C, "evidence": "closed session folder"},
        {"id": "AO-dt", "under": ["PG-dt", "PG-dt-ses"], "name_grammar": ["NG-f"], "not_checked": ["*_scans.tsv"], **C, "evidence": "closed datatype folder"},
    ],
}

CLEAN = ["README", "description.json"] + [f"sub-{s}/ses-{e}/{f}" for s in ("01", "02") for e in ("a", "b") for f in (
    f"anat/sub-{s}_ses-{e}_T1w.nii.gz", f"anat/sub-{s}_ses-{e}_T1w.json", f"func/sub-{s}_ses-{e}_task-x_bold.nii.gz",
    f"func/sub-{s}_ses-{e}_task-x_events.tsv")]


def profile(**changes):
    d = copy.deepcopy(DOC)
    d.update(changes)
    return parse_profile(d)


def run(tmp_path, paths, prof=None, name="o"):
    lst = tmp_path / f"{name}.tsv"
    lst.write_text("".join(f"{p}\t0\n" for p in sorted(paths)))
    c = Recognizer(prof or profile()).run(lst, tmp_path / name)
    fs = [json.loads(x) for x in (tmp_path / name / "findings.jsonl").read_text().splitlines()]
    conf = [f for f in fs if f.get("grain") == "conformance"]
    return c, {(f["path"], f["status"]): f for f in conf}


def swap(paths, old, new):
    return [new if p == old else p for p in paths]


# ---- a clean tree ---------------------------------------------------------------------------------------------------------------------------------
def test_a_clean_tree_has_no_finding_and_scores_one(tmp_path):
    c, f = run(tmp_path, CLEAN)
    assert f == {}
    k = c["conformance"]
    assert k["score"] == 1.0 and k["findings_total"] == 0 and k["checked"]["total"] == k["conformant"] > 0
    assert k["checked"]["required"] == 1 + 2 * 2 + 2 * 2 * 2           # the description, 2 subjects x 2 sessions, x 2 datatypes
    assert k["not_checked"] == {"files": 0, "roots": []}


def test_phase1_profiles_have_no_conformance_block(tmp_path):
    lst = tmp_path / "l.tsv"
    lst.write_text("".join(f"{p}\t0\n" for p in sorted(CLEAN)))
    for pid in ("generic-relevance", "code-repo-conventions", "docs-site", "workspace-repo", "egeria-workspace"):
        prof = load_profile(pid, PROFILES)
        assert not (prof.path_grammar or prof.name_grammar or prof.required or prof.allowed_only)
        c = Recognizer(prof).run(lst, tmp_path / pid)
        assert "conformance" not in c
        assert not any("status" in json.loads(x) for x in (tmp_path / pid / "findings.jsonl").read_text().splitlines())


# ---- path_grammar ---------------------------------------------------------------------------------------------------------------------------------
def test_path_pattern_matches_exactly_and_yields_tokens():
    pg = {p.id: p for p in profile().path_grammar}
    assert pg["PG-dt-ses"].match("sub-01/ses-a/anat") == {"sub": "01", "ses": "a", "datatype": "anat"}
    assert pg["PG-dt-ses"].match("sub-01/ses-a/Anat") is None and pg["PG-dt-ses"].match("sub-01/ses-a") is None
    assert pg["PG-sub"].match("sub-0_1") is None and pg["PG-sub"].match("Sub-01") is None and pg["PG-sub"].match("sub-") is None
    assert pg["PG-dt-ses"].render({"sub": "02", "ses": "b", "datatype": "func"}) == "sub-02/ses-b/func"


@pytest.mark.parametrize("bad", ["Sub-01", "sub-0_1", "sub-01!", "SUB-x"])
def test_a_directory_shaped_like_a_pattern_is_misnamed_and_nothing_below_it_is_judged(tmp_path, bad):
    paths = [p.replace("sub-01/", bad + "/") for p in CLEAN]
    c, f = run(tmp_path, paths)
    assert set(f) == {(bad, "misnamed")}
    assert f[(bad, "misnamed")]["kind"] == "naming" and f[(bad, "misnamed")]["rule_id"] == "PG-sub"
    assert {"path": bad, "reason": "below-finding", "files": 8} in c["conformance"]["not_checked"]["roots"]


def test_a_value_token_in_the_wrong_case_is_misnamed_and_not_also_missing(tmp_path):
    paths = [p.replace("sub-02/ses-a/anat/", "sub-02/ses-a/ANAT/") for p in CLEAN]
    _, f = run(tmp_path, paths)
    assert set(f) == {("sub-02/ses-a/ANAT", "misnamed")} and f[("sub-02/ses-a/ANAT", "misnamed")]["rule_id"] == "PG-dt-ses"


def test_a_directory_with_no_allowed_shape_is_unexpected(tmp_path):
    _, f = run(tmp_path, CLEAN + ["extra/x.txt", "sub-01/ses-a/notes/n.txt"])
    assert set(f) == {("extra", "unexpected"), ("sub-01/ses-a/notes", "unexpected")}
    assert f[("extra", "unexpected")]["rule_id"] == "AO-root" and f[("sub-01/ses-a/notes", "unexpected")]["rule_id"] == "AO-ses"
    assert f[("extra", "unexpected")]["kind"] == "structure"


# ---- name_grammar ---------------------------------------------------------------------------------------------------------------------------------
NG_CASES = [
    ("sub-01_ses-a_T1w.nii.gz", "anat", ""),
    ("sub-01_ses-a_T1w.nii", "anat", "extension"),
    ("sub-01_ses-a_T1w.tsv", "anat", "extension"),
    ("sub-01_ses-a_task-x_events.json", "func", "extension"),
    ("sub-01_ses-a_task-x_events.tsv", "func", ""),
    ("sub-01_ses-a_foo-x_T1w.nii.gz", "anat", "unknown-entity"),
    ("task-x_sub-01_ses-a_bold.nii.gz", "func", "entity-order"),
    ("sub-01_ses-a_run-x_T1w.nii.gz", "anat", "label"),
    ("sub-01_ses-a_task-x!_bold.nii.gz", "func", "label"),
    ("sub-01_ses-a_T1W.nii.gz", "anat", "case"),
    ("sub-01_ses-a_Task-x_bold.nii.gz", "func", "case"),
    ("sub-01_ses-a_bold.nii.gz", "anat", "suffix"),
    ("sub-01_ses-a_bold.nii.gz", "func", "missing-entity"),
    ("sub-02_ses-a_T1w.nii.gz", "anat", "entity-differs-from-folder"),
    ("sub-01_T1w.nii.gz", "anat", "missing-entity"),
    ("sub-01_ses-a_ses-a_T1w.nii.gz", "anat", "duplicate-entity"),
    ("sub-01_ses-a_T1w_final_v2.nii.gz", "anat", "not-an-entity"),
    ("T1w.nii.gz", "anat", "no-entity"),
]


@pytest.mark.parametrize("name,dt,reason", NG_CASES)
def test_name_grammar_check(name, dt, reason):
    ng = profile().name_grammar[0]
    assert ng.check(name, {"sub": "01", "ses": "a", "datatype": dt}) == reason


def test_an_entity_without_its_folder_token_is_misnamed():
    ng = profile().name_grammar[0]
    assert ng.check("sub-01_ses-a_T1w.nii.gz", {"sub": "01", "datatype": "anat"}) == "entity-without-folder"
    assert ng.check("sub-01_T1w.nii.gz", {"sub": "01", "datatype": "anat"}) == ""


@pytest.mark.parametrize("name,shaped", [("sub-01_T1W.nii.gz", True), ("task-x_sub-01_bold.nii.gz", True), ("x_bold.nii.gz", True),
                                         ("notes.txt", False), ("info.csv", False), ("Thumbs.db", False), ("protocol_v2.pdf", False)])
def test_name_shape(name, shaped):
    assert profile().name_grammar[0].shaped(name) is shaped


def test_misnamed_and_unexpected_files_in_a_datatype_folder(tmp_path):
    old = "sub-01/ses-a/func/sub-01_ses-a_task-x_bold.nii.gz"
    paths = swap(CLEAN, old, "sub-01/ses-a/func/task-x_sub-01_ses-a_bold.nii.gz") + ["sub-02/ses-b/anat/notes.txt"]
    _, f = run(tmp_path, paths)
    assert set(f) == {("sub-01/ses-a/func/task-x_sub-01_ses-a_bold.nii.gz", "misnamed"), ("sub-02/ses-b/anat/notes.txt", "unexpected")}
    m = f[("sub-01/ses-a/func/task-x_sub-01_ses-a_bold.nii.gz", "misnamed")]
    assert m["rule_id"] == "NG-f" and m["reason"] == "entity-order" and m["kind"] == "naming"
    assert f[("sub-02/ses-b/anat/notes.txt", "unexpected")]["rule_id"] == "AO-dt"


def test_an_allowed_literal_name_in_the_wrong_case_is_misnamed_and_not_also_missing(tmp_path):
    _, f = run(tmp_path, swap(CLEAN, "description.json", "Description.json"))
    assert set(f) == {("Description.json", "misnamed")} and f[("Description.json", "misnamed")]["rule_id"] == "AO-root"


# ---- required -------------------------------------------------------------------------------------------------------------------------------------
def test_a_missing_literal_path_is_reported_at_the_expected_path(tmp_path):
    _, f = run(tmp_path, [p for p in CLEAN if p != "description.json"])
    assert set(f) == {("description.json", "missing")}
    assert f[("description.json", "missing")]["kind"] == "structure" and f[("description.json", "missing")]["rule_id"] == "RQ-desc"


def test_a_folder_missing_in_one_subject_is_reported_at_the_expected_path(tmp_path):
    _, f = run(tmp_path, [p for p in CLEAN if not p.startswith("sub-02/ses-b/func/")])
    assert set(f) == {("sub-02/ses-b/func", "missing")} and f[("sub-02/ses-b/func", "missing")]["rule_id"] == "RQ-dt-ses"


def test_a_missing_session_is_reported_once_not_with_its_folders(tmp_path):
    _, f = run(tmp_path, [p for p in CLEAN if not p.startswith("sub-01/ses-b/")])
    assert set(f) == {("sub-01/ses-b", "missing")} and f[("sub-01/ses-b", "missing")]["rule_id"] == "RQ-ses"


def test_a_shape_seen_in_no_subject_is_not_required(tmp_path):
    c, f = run(tmp_path, [p for p in CLEAN if "/func/" not in p])
    assert f == {} and c["conformance"]["checked"]["required"] == 1 + 4 + 4


def test_a_misnamed_subject_is_not_counted_as_a_subject_that_lacks_folders(tmp_path):
    _, f = run(tmp_path, [p.replace("sub-01/", "Sub-01/") for p in CLEAN])
    assert set(f) == {("Sub-01", "misnamed")}


def test_a_missing_finding_keeps_its_id_across_surveys(tmp_path):
    a = run(tmp_path, [p for p in CLEAN if p != "description.json"], name="a")[1]
    b = run(tmp_path, [p for p in CLEAN if p != "description.json"] + ["sub-01/ses-a/anat/notes.txt"], name="b")[1]
    fid = a[("description.json", "missing")]["finding_id"]
    assert b[("description.json", "missing")]["finding_id"] == fid
    assert fid == hashlib.sha256(b"gtest@1|RQ-desc|description.json").hexdigest()[:16]
    assert profile(version="1.9.3") and run(tmp_path, [p for p in CLEAN if p != "description.json"], profile(version="1.9.3"), "c")[1][
        ("description.json", "missing")]["finding_id"] == fid                                   # a minor bump keeps the id
    assert run(tmp_path, [p for p in CLEAN if p != "description.json"], profile(version="2.0.0"), "d")[1][
        ("description.json", "missing")]["finding_id"] != fid                                   # a major bump changes it


# ---- allowed_only ---------------------------------------------------------------------------------------------------------------------------------
def test_not_checked_names_are_counted_and_never_judged(tmp_path):
    c, f = run(tmp_path, CLEAN + ["derivatives/a/b.txt", "derivatives/c.txt", "NOTES.md", "sub-01/ses-a/anat/sub-01_ses-a_scans.tsv"])
    assert f == {}
    nc = c["conformance"]["not_checked"]
    assert nc["files"] == 4
    assert {r["path"]: (r["reason"], r["rule_id"], r["files"]) for r in nc["roots"]} == {
        "derivatives": ("not-checked", "AO-root", 2), "NOTES.md": ("not-checked", "AO-root", 1), "sub-01/ses-a/anat/sub-01_ses-a_scans.tsv": ("not-checked", "AO-dt", 1)}


def test_a_folder_no_closed_set_covers_is_not_checked(tmp_path):
    prof = profile(allowed_only=[a for a in DOC["allowed_only"] if a["id"] != "AO-dt"])
    c, f = run(tmp_path, CLEAN + ["sub-01/ses-a/anat/anything.txt"], prof)
    assert f == {}
    roots = {r["path"]: r["reason"] for r in c["conformance"]["not_checked"]["roots"]}
    assert roots["sub-01/ses-a/anat"] == "no-closed-set-files" and c["conformance"]["not_checked"]["files"] == 17


def test_hidden_files_are_not_judged(tmp_path):
    d = copy.deepcopy(DOC)
    d["roles"] = ["component", "vcs-internal"]
    d["relevance"] = {"primary": ["component"], "hidden": ["vcs-internal"]}
    d["rules"] = [{"id": "R-git", "match": {"path_segment": ".git"}, "assign": {"role": "vcs-internal"}, "grain": "subtree", **C, "evidence": "git"}]
    _, f = run(tmp_path, CLEAN + [".git/HEAD"], parse_profile(d))
    assert f == {}


def test_score_counts_checked_items(tmp_path):
    c, f = run(tmp_path, [p for p in CLEAN if p != "README"] + ["extra/x"])
    k = c["conformance"]
    assert k["findings_total"] == 1 and k["conformant"] == k["checked"]["total"] - 1
    assert k["score"] == round((k["checked"]["total"] - 1) / k["checked"]["total"], 6)
    assert k["findings"] == {"structure": {"unexpected": 1}}


def test_two_runs_are_byte_identical(tmp_path):
    paths = [p.replace("sub-01/", "Sub-01/") for p in CLEAN if p != "description.json"] + ["extra/x", "derivatives/y"]
    run(tmp_path, paths, name="a")
    run(tmp_path, paths, name="b")
    for f in ("findings.jsonl", "classes.json", "report.md", "components.txt"):
        assert (tmp_path / "a" / f).read_bytes() == (tmp_path / "b" / f).read_bytes()


# ---- the loader -----------------------------------------------------------------------------------------------------------------------------------
def _bad(path, value):
    d = copy.deepcopy(DOC)
    node = d
    for k in path[:-1]:
        node = node[k]
    if value is KeyError:
        del node[path[-1]]
    else:
        node[path[-1]] = value
    return d


@pytest.mark.parametrize("path,value", [
    (("path_grammar", 0, "extra"), 1),
    (("path_grammar", 0, "tokens", "sub", "extra"), 1),
    (("path_grammar", 0, "tokens"), {}),                                    # a token in the pattern is not defined
    (("path_grammar", 0, "tokens", "zzz"), {"regex": "x"}),                 # a defined token the pattern does not use
    (("path_grammar", 0, "pattern"), "/sub-{sub}"),
    (("path_grammar", 0, "pattern"), "sub-{sub}/../x"),
    (("path_grammar", 0, "tokens", "sub"), {"regex": "("}),
    (("path_grammar", 0, "evidence"), ""),
    (("path_grammar", 0, "basis"), "hunch"),
    (("name_grammar", 0, "entities", 0, "colour"), "red"),
    (("name_grammar", 0, "entities", 1, "key"), "sub"),                     # a key twice
    (("name_grammar", 0, "suffixes", "extra"), 1),
    (("name_grammar", 0, "extensions", "by_suffix", "nope"), [".x"]),        # not one of the suffixes
    (("name_grammar", 0, "extensions", "default"), ["nii"]),               # no leading dot
    (("name_grammar", 0, "label"), KeyError),
    (("required", 0, "for_each"), ["sub"]),                                 # for_each belongs to of
    (("required", 1, "of"), "PG-nope"),
    (("required", 1, "for_each"), ["nope"]),
    (("required", 1, "for_each"), KeyError),
    (("required", 0, "extra"), 1),
    (("allowed_only", 0, "under"), "PG-nope"),
    (("allowed_only", 0, "dirs"), ["PG-nope"]),
    (("allowed_only", 3, "name_grammar"), ["NG-nope"]),
    (("allowed_only", 0, "files"), ["a/b"]),
    (("allowed_only", 0, "extra"), 1),
    (("allowed_only", 1, "id"), "PG-sub"),                                  # an id used twice
])
def test_the_loader_rejects(path, value):
    with pytest.raises(ProfileError):
        parse_profile(_bad(path, value))


def test_a_grammar_id_may_not_reuse_a_rule_id():
    d = copy.deepcopy(DOC)
    d["roles"] = ["component", "vcs-internal"]
    d["relevance"] = {"primary": ["component"], "hidden": ["vcs-internal"]}
    d["rules"] = [{"id": "AO-root", "match": {"path_segment": ".git"}, "assign": {"role": "vcs-internal"}, "grain": "subtree", **C, "evidence": "git"}]
    with pytest.raises(ProfileError):
        parse_profile(d)


def test_grammar_lists_compose_through_extends(tmp_path):
    (tmp_path / "gtest.yaml").write_text(yaml.safe_dump(DOC))
    child = {"profile_id": "child", "version": "0.1.0", "status": "proposed", "applies_to": "any", "roles": ["component"],
             "relevance": {"primary": ["component"]}, "rules": [], "extends": ["gtest"],
             "allowed_only": [{"id": "AO-extra", "under": ".", "files": ["CHANGES"], **C, "evidence": "child allows CHANGES"}]}
    (tmp_path / "child.yaml").write_text(yaml.safe_dump(child))
    p = load_profile("child", tmp_path)
    assert [a.id for a in p.allowed_only][:2] == ["AO-extra", "AO-root"] and len(p.path_grammar) == 4
    lst = tmp_path / "l.tsv"
    lst.write_text("".join(f"{x}\t0\n" for x in sorted(CLEAN + ["CHANGES"])))
    Recognizer(p).run(lst, tmp_path / "o")
    assert not any(json.loads(x).get("status") for x in (tmp_path / "o" / "findings.jsonl").read_text().splitlines())


def test_the_new_keys_are_documented_in_the_readme():
    text = README.read_text()
    for word in ("path_grammar", "name_grammar", "required", "allowed_only", "not_checked", "for_each", "by_token", "by_suffix", "required_for",
                 "misnamed", "unexpected", "missing", "content-type"):
        assert f"`{word}`" in text, word
