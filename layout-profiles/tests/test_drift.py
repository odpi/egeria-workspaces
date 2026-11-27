"""Phase 2 notebook 05, B3: the conformance report (recognizer.conformance) and drift by finding id (recognizer.drift), on generated trees.
Specs are builder-written (samples/specs/); the held-out drift spec is the Architect's (B5) and is not here."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

from recognizer import conformance as cf
from recognizer import drift as dr
from recognizer import manifests as mf
from recognizer.layout_profile import load_profile
from recognizer.recognize import Recognizer

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "samples"
sys.path.insert(0, str(SAMPLES))
import bids_gen as g  # noqa: E402

PROF = load_profile("bids-dataset", ROOT / "profiles")
SPECS = {"a": (SAMPLES / "specs" / "drift-a.yaml", 6, 2), "b": (SAMPLES / "specs" / "drift-b.yaml", 3, 2)}
OUTPUTS = ("findings.jsonl", "classes.json", "report.md", "components.txt", "components-all.txt", "content-reads.txt", "conformance.json")


def survey(tmp_path, files, name):
    root = tmp_path / f"{name}-tree"
    for rel, data in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_bytes(data)
    lst = tmp_path / f"{name}.tsv"
    lst.write_text("".join(f"{p}\t{len(files[p])}\n" for p in sorted(files)))
    Recognizer(PROF, blob_source=mf.FileSource(str(root))).run(lst, tmp_path / name)
    cf.write(tmp_path / name)
    return tmp_path / name


def tkey(t):
    return (t["path"], t["kind"], t["status"], t["rule"])


def fkey(f):
    return (f["path"], f["kind"], f["status"], f["rule_id"])


def test_the_conformance_report(tmp_path):
    spec, n, s = SPECS["a"]
    files, truth = g.generate(1, n, s, g.load_spec(spec))
    out = survey(tmp_path, files, "m")
    c = json.loads((out / "conformance.json").read_text())
    assert c["findings_total"] == len(truth) == 13 and sorted(map(fkey, c["findings"])) == sorted(map(tkey, truth))
    assert c["conformant"] == c["checked"]["total"] - 13 and c["score"] == round(c["conformant"] / c["checked"]["total"], 6)
    assert c["findings_by_kind"] == {"content-type": 2, "naming": 6, "structure": 5}
    report = (out / "report.md").read_text()
    assert f"**{cf.headline(c)}**" in report and cf.headline(c).endswith("conformant; 13 findings")
    assert report.count(cf.BEGIN) == 1


def test_the_headline():
    assert cf.headline({"score": 0.971, "findings_total": 12}) == "97% conformant; 12 findings"
    assert cf.headline({"score": 0.9999, "findings_total": 1}) == "99% conformant; 1 finding"
    assert cf.headline({"score": 1.0, "findings_total": 0}) == "100% conformant; 0 findings"


def test_a_clean_tree_reports_100_percent(tmp_path):
    out = survey(tmp_path, g.generate(2, 3, 2)[0], "c")
    assert cf.headline(json.loads((out / "conformance.json").read_text())) == "100% conformant; 0 findings"


def test_a_profile_without_conformance_is_refused(tmp_path):
    lst = tmp_path / "l.tsv"
    lst.write_text("a.py\t1\n")
    Recognizer(load_profile("generic-relevance", ROOT / "profiles")).run(lst, tmp_path / "o")
    with pytest.raises(cf.ConformanceError):
        cf.write(tmp_path / "o")


@pytest.mark.parametrize("which", ["a", "b"])
def test_two_surveys_of_the_same_tree_have_no_drift_and_identical_outputs(tmp_path, which):
    spec, n, s = SPECS[which]
    files, _ = g.generate(2, n, s, g.load_spec(spec))
    a, b = survey(tmp_path, files, "a"), survey(tmp_path, files, "b")
    d = dr.write(a, b)
    assert d["counts"]["new"] == 0 and d["counts"]["resolved"] == 0 and d["counts"]["unchanged"] > 0
    dr.write(a, a, tmp_path / "self.json")
    for name in OUTPUTS:
        if name != "report.md":
            assert (a / name).read_bytes() == (b / name).read_bytes(), name


@pytest.mark.parametrize("seed", [1, 2, 3])
@pytest.mark.parametrize("which", ["a", "b"])
def test_clean_to_mutated_is_exactly_the_truth_and_back_resolves_it(tmp_path, seed, which):
    spec, n, s = SPECS[which]
    clean, _ = g.generate(seed, n, s)
    mutated, truth = g.generate(seed, n, s, g.load_spec(spec))
    c0, m, c1 = survey(tmp_path, clean, "c0"), survey(tmp_path, mutated, "m"), survey(tmp_path, clean, "c1")
    d = dr.write(c0, m)
    assert sorted(map(fkey, d["new"])) == sorted(map(tkey, truth)) and d["counts"]["resolved"] == 0 and d["counts"]["unchanged"] == 0
    back = dr.write(m, c1)
    assert sorted(map(fkey, back["resolved"])) == sorted(map(tkey, truth)) and back["counts"]["new"] == 0
    assert {f["finding_id"] for f in back["resolved"]} == {f["finding_id"] for f in d["new"]}


def test_a_missing_file_keeps_its_id_and_a_changed_status_is_marked(tmp_path):
    base, _ = g.generate(1, 3, 0)
    one = dict(base)
    del one["CHANGES"]
    one["dataset_description.json"] = g.description(1, set_={"BIDSVersion": "1.8"})
    two = dict(one)
    two["dataset_description.json"] = g.description(1, drop=("BIDSVersion",))
    two["sub-01/anat/notes.txt"] = b""
    d = dr.write(survey(tmp_path, one, "one"), survey(tmp_path, two, "two"))
    assert [f["path"] for f in d["new"]] == ["sub-01/anat/notes.txt"] and d["resolved"] == []
    un = {f["rule_id"]: f for f in d["unchanged"]}
    assert set(un) == {"RQ-changes", "CT-bidsversion"} and "changed" not in un["RQ-changes"]
    assert un["CT-bidsversion"]["changed"] is True and un["CT-bidsversion"]["old_status"] == "invalid-value" and un["CT-bidsversion"]["status"] == "missing-field"
    assert d["counts"] == {"new": 1, "resolved": 0, "unchanged": 2, "changed": 1}
    assert "1 new since last survey" in (tmp_path / "two" / "report.md").read_text()


def test_different_profile_majors_are_refused(tmp_path):
    out = survey(tmp_path, g.generate(1, 2, 0)[0], "x")
    other = tmp_path / "y"
    other.mkdir()
    for name in ("findings.jsonl", "classes.json"):
        (other / name).write_text((out / name).read_text())
    cl = json.loads((other / "classes.json").read_text())
    cl["profile"]["version"] = "1.0.0"
    (other / "classes.json").write_text(json.dumps(cl))
    with pytest.raises(dr.DriftError):
        dr.diff(out, other)


def test_the_command_lines(tmp_path):
    spec, n, s = SPECS["b"]
    py = sys.executable
    for name, extra in (("c", []), ("m", ["--mutations", str(spec)])):
        subprocess.run([py, str(SAMPLES / "bids_gen.py"), "--seed", "1", "--subjects", str(n), "--sessions", str(s), "--out", str(tmp_path / name)] + extra,
                       check=True, capture_output=True)
        subprocess.run([py, "-m", "recognizer.recognize", str(tmp_path / name / "paths.tsv"), "--out", str(tmp_path / f"{name}-out"), "--profile",
                        "bids-dataset", "--blobs-dir", str(tmp_path / name / "dataset")], check=True, capture_output=True, cwd=ROOT)
        r = subprocess.run([py, "-m", "recognizer.conformance", str(tmp_path / f"{name}-out")], check=True, capture_output=True, text=True, cwd=ROOT)
    assert r.stdout.strip().endswith("conformant; 3 findings")
    r = subprocess.run([py, "-m", "recognizer.drift", str(tmp_path / "c-out"), str(tmp_path / "m-out")], check=True, capture_output=True, text=True, cwd=ROOT)
    assert r.stdout.strip() == "3 new since last survey; 0 resolved; 0 unchanged"
    truth = [json.loads(x) for x in (tmp_path / "m" / "truth.jsonl").read_text().splitlines()]
    d = json.loads((tmp_path / "m-out" / "drift.json").read_text())
    assert sorted(map(fkey, d["new"])) == sorted(map(tkey, truth))


def test_running_the_reports_again_changes_nothing(tmp_path):
    spec, n, s = SPECS["b"]
    files, _ = g.generate(3, n, s, g.load_spec(spec))
    a, b = survey(tmp_path, g.generate(3, n, s)[0], "a"), survey(tmp_path, files, "b")
    dr.write(a, b)
    before = {p.name: p.read_bytes() for p in b.iterdir()}
    cf.write(b)
    dr.write(a, b)
    assert {p.name: p.read_bytes() for p in b.iterdir()} == before
    assert (b / "report.md").read_text().count(dr.BEGIN) == 1


def test_a_configuration_change_is_reported_not_compared(tmp_path):
    """Merge note (1j read-back): drift runs config_change() first (J5); surveys with different configurations are not compared by finding id."""
    out = survey(tmp_path, g.generate(1, 2, 0)[0], "x")
    other = tmp_path / "y"
    other.mkdir()
    for name in ("findings.jsonl", "classes.json", "report.md"):
        (other / name).write_text((out / name).read_text())
    cl = json.loads((other / "classes.json").read_text())
    cl["configuration"]["config_sha256"] = "0" * 64
    (other / "classes.json").write_text(json.dumps(cl))
    d = dr.write(out, other)
    assert d["configuration_change"]["status"] == "CONFIGURATION CHANGED" and "counts" not in d
    assert dr.headline(d).startswith("CONFIGURATION CHANGED (not finding drift)")
    assert "findings are not compared" in (other / "report.md").read_text()
    assert dr.diff(out, out)["counts"]["new"] == 0                  # the same configuration: compared by finding id, as before
