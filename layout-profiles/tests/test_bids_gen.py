"""Phase 2 notebook 05, B0: the seeded BIDS-shaped generator (samples/bids_gen.py). Synthetic only.
Determinism, the clean tree, and one test per mutation class that injects ONLY that class. (Detection by the bids-dataset profile is B2.)"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

SAMPLES = Path(__file__).resolve().parent.parent / "samples"
sys.path.insert(0, str(SAMPLES))
import bids_gen as g  # noqa: E402


def tree_digest(out: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(x for x in out.rglob("*") if x.is_file()):
        h.update(str(p.relative_to(out)).encode() + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()


def one(cls, subjects=3, sessions=2, seed=1, **kw):
    spec = g.parse_spec({"mutations": [{"class": cls, **kw}]})
    clean, _ = g.generate(seed, subjects, sessions)
    files, truth = g.generate(seed, subjects, sessions, spec)
    assert len(truth) == 1, truth
    t = truth[0]
    assert t["class"] == cls and (t["kind"], t["status"]) == g.CLASSES[cls]
    assert set(t) == {"path", "kind", "status", "rule", "class"}
    return clean, files, t


# ---- determinism ---------------------------------------------------------------------------------------------------------------------------------
ALL_SPEC = {"mutations": [{"class": c} for c in g.CLASSES if c not in ("malformed-json", "license-empty", "bidsversion-invalid")]}


@pytest.mark.parametrize("spec", [None, ALL_SPEC])
def test_same_seed_and_spec_give_a_byte_identical_tree_and_truth(tmp_path, spec):
    sp = None
    if spec is not None:
        sp = tmp_path / "spec.yaml"
        import yaml
        sp.write_text(yaml.safe_dump(spec))
    digests = []
    for n in (1, 2):
        out = tmp_path / f"run{n}"
        args = [sys.executable, str(SAMPLES / "bids_gen.py"), "--seed", "7", "--subjects", "6", "--sessions", "2", "--out", str(out)]
        subprocess.run(args + (["--mutations", str(sp)] if sp else []), check=True, capture_output=True)
        digests.append(tree_digest(out))
    assert digests[0] == digests[1]
    truth = (tmp_path / "run1" / "truth.jsonl").read_text()
    assert (truth == "") == (spec is None)


def test_different_seeds_give_different_trees():
    assert g.generate(1)[0] != g.generate(2)[0]


def test_paths_tsv_lists_every_file_with_its_size_sorted(tmp_path):
    files, truth = g.generate(3, 2, 0)
    g.write_outputs(files, truth, tmp_path / "o")
    rows = (tmp_path / "o" / "paths.tsv").read_text().splitlines()
    assert rows == sorted(rows) and len(rows) == len(files)
    for row in rows:
        p, size = row.split("\t")
        assert (tmp_path / "o" / "dataset" / p).stat().st_size == int(size)


def test_paths_tsv_is_what_listpaths_gives(tmp_path):
    files, truth = g.generate(2, 2, 2)
    g.write_outputs(files, truth, tmp_path / "o")
    lp = Path(__file__).resolve().parent.parent / "recognizer" / "listpaths.py"
    subprocess.run([sys.executable, str(lp), str(tmp_path / "o" / "dataset"), str(tmp_path / "lp.tsv")], check=True, capture_output=True)
    assert (tmp_path / "lp.tsv").read_text() == (tmp_path / "o" / "paths.tsv").read_text()


def test_the_output_folder_must_be_empty(tmp_path):
    (tmp_path / "o").mkdir()
    (tmp_path / "o" / "x").write_text("x")
    with pytest.raises(g.SpecError):
        g.write_outputs(*g.generate(1), tmp_path / "o")


# ---- the clean tree ------------------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("seed", [1, 2, 3])
@pytest.mark.parametrize("sessions", [0, 2])
def test_the_clean_tree_has_the_top_files_and_four_modalities_per_subject_and_session(seed, sessions):
    files, truth = g.generate(seed, 3, sessions)
    assert truth == []
    for f in g.TOP_FILES:
        assert f in files
    subs = sorted({p.split("/")[0] for p in files if "/" in p})
    assert subs == ["sub-01", "sub-02", "sub-03"]
    dirs = {p.rpartition("/")[0] for p in files if "/" in p}
    for s in subs:
        if sessions:
            seslabels = sorted({p.split("/")[1] for p in files if p.startswith(s + "/")})
            assert len(seslabels) == 2 and all(x.startswith("ses-") for x in seslabels)
            for ses in seslabels:
                assert {f"{s}/{ses}/{dt}" for dt in g.DATATYPES} <= dirs
        else:
            assert {f"{s}/{dt}" for dt in g.DATATYPES} == dirs & {f"{s}/{dt}" for dt in g.DATATYPES}
            assert not any(p.split("/")[1].startswith("ses-") for p in files if p.startswith(s + "/"))
    for p, data in files.items():
        if "/" in p:
            assert data == (b"{}" if p.endswith(".json") else b""), p
            name = p.rpartition("/")[2]
            assert name.startswith(p.split("/")[0] + "_")


def test_dataset_description_has_exactly_three_synthetic_fields():
    files, _ = g.generate(1)
    doc = json.loads(files["dataset_description.json"])
    assert set(doc) == {"BIDSVersion", "Name", "License"}
    assert doc["License"] == "CC0" and doc["BIDSVersion"] == g.BIDS_VERSION and "seed 1" in doc["Name"]


def test_entities_are_in_bids_order():
    order = ["sub", "ses", "task", "acq", "dir", "run", "echo"]
    for seed in range(1, 12):
        files, _ = g.generate(seed, 2, 2)
        for p in files:
            if "/" not in p:
                continue
            keys = [x.split("-", 1)[0] for x in p.rpartition("/")[2].split(".")[0].split("_")[:-1]]
            assert keys == sorted(keys, key=order.index), p


# ---- one test per class, injecting ONLY that class -----------------------------------------------------------------------------------------------
@pytest.mark.parametrize("f", sorted(g.TOP_FILES))
def test_missing_top_level_file(f):
    clean, files, t = one("missing-top-level-file", file=f)
    assert t["path"] == f and f in clean and f not in files and t["rule"] == g.TOP_FILES[f]
    assert set(clean) - set(files) == {f} and set(files) <= set(clean)


@pytest.mark.parametrize("sessions", [0, 2])
def test_missing_modality_folder(sessions):
    clean, files, t = one("missing-modality-folder", sessions=sessions)
    p = t["path"]
    assert p.rpartition("/")[2] in g.DATATYPES and p.count("/") == (2 if sessions else 1)
    assert any(x.startswith(p + "/") for x in clean) and not any(x.startswith(p + "/") for x in files)
    assert t["rule"] == ("RQ-datatype-ses" if sessions else "RQ-datatype")
    assert set(files) == {x for x in clean if not x.startswith(p + "/")}


def test_unexpected_top_level_folder():
    clean, files, t = one("unexpected-top-level-folder")
    assert t["path"] in g.UNEXPECTED_DIRS and t["rule"] == "AO-root"
    added = set(files) - set(clean)
    assert len(added) == 1 and next(iter(added)).startswith(t["path"] + "/") and set(clean) <= set(files)


def test_unexpected_file_in_modality_folder():
    clean, files, t = one("unexpected-file-in-modality-folder")
    assert set(files) - set(clean) == {t["path"]} and t["rule"] == "AO-datatype"
    d, _, name = t["path"].rpartition("/")
    assert d.rpartition("/")[2] in g.DATATYPES and name in g.UNEXPECTED_FILES


def _renamed(clean, files, t):
    added, removed = set(files) - set(clean), set(clean) - set(files)
    assert added == {t["path"]} and len(removed) == 1
    return next(iter(removed)), t["path"]


def test_entity_order():
    clean, files, t = one("entity-order")
    old, new = _renamed(clean, files, t)
    assert new.rpartition("/")[2].startswith("task-") and sorted(old.split("/")[-1].split("_")) == sorted(new.split("/")[-1].split("_"))
    assert t["rule"] == "NG-bids"


def test_unknown_entity_key():
    clean, files, t = one("unknown-entity-key")
    old, new = _renamed(clean, files, t)
    extra = set(new.rpartition("/")[2].split("_")) - set(old.rpartition("/")[2].split("_"))
    assert len(extra) == 1 and next(iter(extra)).split("-")[0] in g.UNKNOWN_KEYS and t["rule"] == "NG-bids"


@pytest.mark.parametrize("variant", ["underscore", "bang"])
def test_illegal_label_character(variant):
    clean, files, t = one("illegal-label-character", variant=variant)
    assert t["rule"] == "PG-subject" and "/" not in t["path"]
    assert ("_" in t["path"][4:]) if variant == "underscore" else t["path"].endswith("!")
    moved = [x for x in files if x.startswith(t["path"] + "/")]
    assert moved and len(files) == len(clean)


def test_wrong_case_dir():
    clean, files, t = one("wrong-case", variant="dir")
    assert t["path"].startswith("Sub-") and t["rule"] == "PG-subject" and len(files) == len(clean)


def test_wrong_case_file():
    clean, files, t = one("wrong-case", variant="file")
    old, new = _renamed(clean, files, t)
    assert old.lower() == new.lower() and old != new and t["rule"] == "NG-bids"


def test_wrong_extension():
    clean, files, t = one("wrong-extension")
    old, new = _renamed(clean, files, t)
    assert old[:-len(".nii.gz")] == new[:-len(".nii.zip")] and new.endswith(".nii.zip") and t["rule"] == "NG-bids"


def test_session_inconsistency():
    clean, files, t = one("session-inconsistency")
    p = t["path"]
    assert p.count("/") == 1 and p.split("/")[1].startswith("ses-") and t["rule"] == "RQ-session"
    assert set(files) == {x for x in clean if not x.startswith(p + "/")}


def test_session_inconsistency_needs_two_sessions():
    with pytest.raises(g.SpecError):
        g.generate(1, 3, 1, g.parse_spec({"mutations": [{"class": "session-inconsistency"}]}))


def test_stray_name():
    clean, files, t = one("stray-name")
    assert set(files) - set(clean) == {t["path"]} and set(clean) <= set(files) and t["rule"] == "NG-bids"
    assert any(t["path"].endswith(f"_{x}.nii.gz") for x in g.STRAY_TAGS)


@pytest.mark.parametrize("cls,field,rule", [("bidsversion-missing", "BIDSVersion", "CT-bidsversion"), ("license-missing", "License", "CT-license")])
def test_content_field_missing(cls, field, rule):
    clean, files, t = one(cls)
    doc = json.loads(files["dataset_description.json"])
    assert field not in doc and len(doc) == 2 and t["path"] == "dataset_description.json" and t["rule"] == rule
    assert {k for k in files if files[k] != clean.get(k)} == {"dataset_description.json"}


@pytest.mark.parametrize("cls,field,rule", [("bidsversion-invalid", "BIDSVersion", "CT-bidsversion"), ("license-empty", "License", "CT-license"),
                                            ("name-empty", "Name", "CT-name")])
def test_content_field_invalid(cls, field, rule):
    _, files, t = one(cls)
    doc = json.loads(files["dataset_description.json"])
    assert set(doc) == {"BIDSVersion", "Name", "License"} and t["rule"] == rule
    assert doc[field] in (("",) if field != "BIDSVersion" else g.BAD_VERSIONS)


def test_malformed_json():
    _, files, t = one("malformed-json")
    with pytest.raises(ValueError):
        json.loads(files["dataset_description.json"])
    assert t["rule"] == "CT-unreadable"


def test_every_class_has_a_test_here():
    src = Path(__file__).read_text()
    for cls in g.CLASSES:
        assert f'"{cls}"' in src, cls


# ---- the spec ------------------------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("bad", [{"mutations": [{"class": "nope"}]}, {"mutations": [{"class": "wrong-case", "variant": "x"}]},
                                 {"mutations": [{"class": "entity-order", "file": "README"}]}, {"mutations": [{"class": "stray-name", "count": 0}]},
                                 {"mutations": [{"class": "stray-name", "extra": 1}]}, {"other": []}])
def test_a_bad_spec_is_refused(bad):
    with pytest.raises(g.SpecError):
        g.parse_spec(bad)


def test_conflicting_content_mutations_are_refused():
    for pair in (["license-missing", "license-empty"], ["malformed-json", "name-empty"]):
        with pytest.raises(g.SpecError):
            g.generate(1, spec=g.parse_spec({"mutations": [{"class": c} for c in pair]}))
    with pytest.raises(g.SpecError):
        g.generate(1, spec=g.parse_spec({"mutations": [{"class": "name-empty"}, {"class": "missing-top-level-file", "file": "dataset_description.json"}]}))


def test_subject_level_mutations_leave_one_subject_untouched():
    spec = g.parse_spec({"mutations": [{"class": "missing-modality-folder", "count": 2}, {"class": "wrong-case", "variant": "dir"}]})
    clean, _ = g.generate(5, 4, 2)
    files, truth = g.generate(5, 4, 2, spec)
    touched = {t["path"].split("/")[0].lower() for t in truth}
    untouched = [s for s in ("sub-01", "sub-02", "sub-03", "sub-04") if s not in touched]
    assert len(untouched) == 1
    s = untouched[0]
    assert sorted(p for p in files if p.startswith(s + "/")) == sorted(p for p in clean if p.startswith(s + "/"))
    with pytest.raises(g.SpecError):
        g.generate(5, 3, 2, g.parse_spec({"mutations": [{"class": "missing-modality-folder", "count": 3}]}))


def test_many_classes_together_give_one_truth_line_each_and_distinct_paths():
    spec = g.parse_spec(ALL_SPEC)
    files, truth = g.generate(9, 8, 2, spec)
    assert len(truth) == len(spec)
    paths = [t["path"] for t in truth if t["kind"] != "content-type"]
    assert len(paths) == len(set(paths))
    for t in truth:
        present = t["path"] in files or any(p.startswith(t["path"] + "/") for p in files)
        assert present == (t["status"] != "missing" or t["kind"] == "content-type"), t
