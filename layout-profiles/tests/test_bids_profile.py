"""Phase 2 notebook 05, B2: the bids-dataset profile 0.1.0 on generated trees (samples/bids_gen.py), the dataset_description.json content checks
(NOTE-PHASE2 §2 row and §10), and the real ds000117 file list (names only; reported, not scored). Synthetic files only, except the ds000117
names and its dataset_description.json, which are copied as SOURCES.md records."""
import copy
import hashlib
import json
import sys
from pathlib import Path

import pytest
import yaml

from recognizer import manifests as mf
from recognizer.layout_profile import ProfileError, compose_profiles, load_profile, parse_profile
from recognizer.recognize import Recognizer

ROOT = Path(__file__).resolve().parent.parent
PROFILES = ROOT / "profiles"
SAMPLES = ROOT / "samples"
sys.path.insert(0, str(SAMPLES))
import bids_gen as g  # noqa: E402

PROF = load_profile("bids-dataset", PROFILES)


def survey(tmp_path, files, name="o", source=True, prof=None):
    root = tmp_path / f"{name}-tree"
    for rel, data in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    lst = tmp_path / f"{name}.tsv"
    lst.write_text("".join(f"{p}\t{len(files[p])}\n" for p in sorted(files)))
    c = Recognizer(prof or PROF, blob_source=mf.FileSource(str(root)) if source else None).run(lst, tmp_path / name)
    fs = [json.loads(x) for x in (tmp_path / name / "findings.jsonl").read_text().splitlines()]
    return c, [f for f in fs if f.get("grain") == "conformance"]


def key(f):
    return (f["path"], f["kind"], f["status"], f["rule_id"])


def truth_key(t):
    return (t["path"], t["kind"], t["status"], t["rule"])


# ---- the profile --------------------------------------------------------------------------------------------------------------------------------
def test_the_profile_names_its_spec_version_and_tuning():
    text = (PROFILES / "bids-dataset.yaml").read_text()
    assert "v1.11.2" in text and PROF.version == "0.1.0" and PROF.status == "proposed"
    for item in (*PROF.path_grammar, *PROF.name_grammar):
        assert item.tuned_on[0] == "generated (bids_gen seeds 1-3)"
        assert set(item.tuned_on[1:]) <= {"BIDS spec; noticed on ds000117 (reported-only sample)"}      # read-back FIX-A/B: spec facts, noticed there
    rules = "\n".join(l for l in text.splitlines() if "tuned_on" not in l)
    for word in ("ds000117", "openneuro", "wakeman", "henson", "facerecognition"):   # no rule names a real dataset
        assert word not in rules.lower()


def test_the_entities_are_the_subset_in_spec_order():
    assert [e[0] for e in PROF.name_grammar[0].entities] == ["sub", "ses", "task", "acq", "dir", "run", "echo"]
    assert set(PROF.name_grammar[0].suffixes) == {"anat", "func", "dwi", "fmap"}


@pytest.mark.parametrize("kind", ["structure", "naming", "content-type"])
def test_a_component_or_role_kind_may_not_be_a_conformance_kind(kind):
    base = {"profile_id": "k", "version": "0.1.0", "status": "proposed", "applies_to": "any", "roles": ["component", "vendored"],
            "relevance": {"primary": ["component"], "hidden": ["vendored"]}}
    rule = {"id": "R-x", "match": {"has_file": "x.toml"}, "assign": {"role": "component", "kind": kind}, "grain": "component", "basis": "manifest",
            "confidence": "high", "evidence": "x"}
    with pytest.raises(ProfileError):
        parse_profile({**base, "rules": [rule]})
    role_rule = {**rule, "match": {"path_segment": "vendor"}, "assign": {"role": "vendored", "kind": kind}, "grain": "subtree", "basis": "convention"}
    with pytest.raises(ProfileError):
        parse_profile({**base, "rules": [role_rule]})
    with pytest.raises(ProfileError):
        parse_profile({**base, "rules": [], "structural_rules": [{"id": "S-x", "op": "notebook-folder", "min": 1, "kind": kind, "basis": "judgement",
                                                                  "confidence": "low", "evidence": "x"}]})
    ok = {**rule, "assign": {"role": "component", "kind": "library"}}
    assert parse_profile({**base, "rules": [ok]}).rules[0].kind == "library"


def test_no_shipped_profile_uses_a_conformance_kind():
    for p in sorted(PROFILES.glob("*.yaml")):
        load_profile(p.stem, PROFILES)                                         # the loader refuses one that does


def test_only_bids_dataset_may_read_dataset_description():
    doc = yaml.safe_load((PROFILES / "bids-dataset.yaml").read_text())
    doc["profile_id"] = "other"
    with pytest.raises(ProfileError):
        parse_profile(doc, profiles_dir=PROFILES)
    doc = yaml.safe_load((PROFILES / "bids-dataset.yaml").read_text())
    doc["content_checks"][0]["file"] = "participants.tsv"
    with pytest.raises(ProfileError):
        parse_profile(doc, profiles_dir=PROFILES)
    doc = yaml.safe_load((PROFILES / "bids-dataset.yaml").read_text())
    doc["content_checks"][0]["field"] = "Authors"
    with pytest.raises(ProfileError):
        parse_profile(doc, profiles_dir=PROFILES)
    doc = yaml.safe_load((PROFILES / "bids-dataset.yaml").read_text())
    doc["content_checks"] = doc["content_checks"][:3]                          # no unreadable item
    with pytest.raises(ProfileError):
        parse_profile(doc, profiles_dir=PROFILES)


# ---- clean trees: 0 findings, 100% conformant ---------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("seed", [1, 2, 3])
@pytest.mark.parametrize("subjects,sessions", [(3, 2), (2, 0), (4, 3), (1, 1)])
def test_a_clean_tree_is_fully_conformant(tmp_path, seed, subjects, sessions):
    files, truth = g.generate(seed, subjects, sessions)
    c, f = survey(tmp_path, files)
    assert truth == [] and f == []
    k = c["conformance"]
    assert k["score"] == 1.0 and k["checked"]["fields"] == 3 and k["not_checked"]["files"] == 0 and k["content_reading"]["files_read"] == ["dataset_description.json"]


# ---- every class, alone, is found with the right kind, status and rule --------------------------------------------------------------------------
CASES = [(c, None) for c in g.CLASSES if c not in g.VARIANTS] + [(c, v) for c in g.VARIANTS for v in g.VARIANTS[c]]


@pytest.mark.parametrize("seed", [1, 2, 3, 11])
@pytest.mark.parametrize("cls,variant", CASES)
def test_each_class_alone_is_detected_exactly(tmp_path, cls, variant, seed):
    sessions = 2 if cls == "session-inconsistency" else (seed % 3)
    spec = g.parse_spec({"mutations": [{"class": cls, **({"variant": variant} if variant else {})}]})
    files, truth = g.generate(seed, 3, sessions, spec)
    _, f = survey(tmp_path, files)
    assert sorted(map(key, f)) == sorted(map(truth_key, truth))


@pytest.mark.parametrize("f", sorted(g.TOP_FILES))
def test_each_missing_top_level_file_is_detected(tmp_path, f):
    files, truth = g.generate(2, 3, 2, g.parse_spec({"mutations": [{"class": "missing-top-level-file", "file": f}]}))
    _, found = survey(tmp_path, files)
    assert sorted(map(key, found)) == sorted(map(truth_key, truth))


ALL = {"mutations": [{"class": c} for c in g.CLASSES if c not in ("malformed-json", "license-empty", "bidsversion-invalid", "missing-top-level-file")]
       + [{"class": "missing-top-level-file", "file": "CHANGES"}, {"class": "unexpected-file-in-modality-folder", "count": 2}, {"class": "stray-name", "count": 2}]}


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_many_classes_together_are_detected_exactly_and_nothing_else(tmp_path, seed):
    files, truth = g.generate(seed, 8, 2, g.parse_spec(ALL))
    c, f = survey(tmp_path, files)
    assert sorted(map(key, f)) == sorted(map(truth_key, truth))
    assert c["conformance"]["findings_total"] == len(truth) and c["conformance"]["score"] < 1.0


def test_two_surveys_are_byte_identical(tmp_path):
    files, _ = g.generate(3, 5, 2, g.parse_spec(ALL))
    survey(tmp_path, files, "a")
    survey(tmp_path, files, "b")
    for name in ("findings.jsonl", "classes.json", "report.md", "content-reads.txt", "components.txt"):
        assert (tmp_path / "a" / name).read_bytes() == (tmp_path / "b" / name).read_bytes()


# ---- content checks (NOTE-PHASE2 §10) ------------------------------------------------------------------------------------------------------------
def desc(**fields):
    doc = {"BIDSVersion": "1.11.2", "Name": "x", "License": "CC0"}
    for k, v in fields.items():
        if v is KeyError:
            doc.pop(k)
        else:
            doc[k] = v
    return (json.dumps(doc) + "\n").encode()


def content(tmp_path, data, name="o", **kw):
    files, _ = g.generate(1, 2, 0)
    files["dataset_description.json"] = data
    c, f = survey(tmp_path, files, name, **kw)
    return c, {(x["rule_id"], x["status"]): x for x in f}


def test_a_valid_description_has_no_content_finding(tmp_path):
    c, f = content(tmp_path, desc())
    assert f == {} and c["conformance"]["checked"]["fields"] == 3


@pytest.mark.parametrize("field,rule", [("BIDSVersion", "CT-bidsversion"), ("Name", "CT-name"), ("License", "CT-license")])
def test_each_field_missing(tmp_path, field, rule):
    _, f = content(tmp_path, desc(**{field: KeyError}))
    assert set(f) == {(rule, "missing-field")}
    x = f[(rule, "missing-field")]
    assert x["kind"] == "content-type" and x["path"] == "dataset_description.json" and x["evidence_field"] == field and "value" not in x
    assert x["basis"] == "manifest-content" and x["evidence_file"] == "dataset_description.json" and len(x["evidence_blob"]) == 64


def test_a_field_that_is_a_number_is_missing(tmp_path):
    _, f = content(tmp_path, desc(BIDSVersion=1.8))
    assert set(f) == {("CT-bidsversion", "missing-field")}


@pytest.mark.parametrize("value", ["1.8", "v1.11.2", "1.11.2-dev", ""])
def test_an_invalid_bidsversion(tmp_path, value):
    _, f = content(tmp_path, desc(BIDSVersion=value))
    assert set(f) == {("CT-bidsversion", "invalid-value")} and f[("CT-bidsversion", "invalid-value")]["value"] == value


@pytest.mark.parametrize("field,rule", [("Name", "CT-name"), ("License", "CT-license")])
def test_an_empty_name_or_license(tmp_path, field, rule):
    _, f = content(tmp_path, desc(**{field: "  "}))
    assert set(f) == {(rule, "invalid-value")}


def test_a_value_over_256_characters_is_invalid_and_not_stored(tmp_path):
    _, f = content(tmp_path, desc(Name="n" * 257))
    assert set(f) == {("CT-name", "invalid-value")} and "value" not in f[("CT-name", "invalid-value")]
    _, f = content(tmp_path, desc(Name="n" * 256), name="p")
    assert f == {}


def test_malformed_json_is_unreadable_and_no_field_is_checked(tmp_path):
    c, f = content(tmp_path, desc()[:-3])
    assert set(f) == {("CT-unreadable", "unreadable")} and f[("CT-unreadable", "unreadable")]["note"].startswith("parse_error")
    assert c["conformance"]["checked"]["fields"] == 1


def test_a_json_list_is_unreadable(tmp_path):
    _, f = content(tmp_path, b"[1, 2]\n")
    assert set(f) == {("CT-unreadable", "unreadable")}


def test_an_over_cap_description_is_unreadable_and_not_read(tmp_path):
    big = desc(Extra="x" * (mf.DEFAULT_MAX_FILE_BYTES + 10))
    _, f = content(tmp_path, big)
    assert set(f) == {("CT-unreadable", "unreadable")} and f[("CT-unreadable", "unreadable")]["note"] == "skipped: size"


def test_an_unrelated_extra_field_changes_no_finding_id(tmp_path):
    _, a = content(tmp_path, desc(BIDSVersion="1.8"), "a")
    _, b = content(tmp_path, desc(BIDSVersion="1.8", Authors=["x"], Funding="y"), "b")
    assert a[("CT-bidsversion", "invalid-value")]["finding_id"] == b[("CT-bidsversion", "invalid-value")]["finding_id"]
    _, c = content(tmp_path, desc(BIDSVersion="latest"), "c")                  # the id is stable when the value changes
    assert c[("CT-bidsversion", "invalid-value")]["finding_id"] == a[("CT-bidsversion", "invalid-value")]["finding_id"]
    assert a[("CT-bidsversion", "invalid-value")]["finding_id"] == hashlib.sha256(b"bids-dataset@0|CT-bidsversion|dataset_description.json").hexdigest()[:16]


def test_no_other_field_is_copied(tmp_path):
    files, _ = g.generate(1, 2, 0)
    files["dataset_description.json"] = desc(BIDSVersion="1.8", Authors=["SECRET-AUTHOR"], Acknowledgements="SECRET-ACK")
    survey(tmp_path, files)
    for p in (tmp_path / "o").iterdir():
        assert "SECRET" not in p.read_text(), p.name


def test_a_description_below_the_root_is_never_opened(tmp_path):
    files, _ = g.generate(1, 2, 0)
    files["derivatives/pipeline/dataset_description.json"] = b"not json"
    files["sub-01/anat/dataset_description.json"] = b"not json"
    c, f = survey(tmp_path, files)
    assert (tmp_path / "o" / "content-reads.txt").read_text() == "dataset_description.json\n"
    assert not any(x["kind"] == "content-type" for x in f)


def test_without_a_blob_source_no_content_is_read(tmp_path):
    files, _ = g.generate(1, 2, 0)
    files["dataset_description.json"] = b"not json"
    c, f = survey(tmp_path, files, source=False)
    assert f == [] and c["conformance"]["content_reading"] == {"enabled": False, "files_read": []} and c["conformance"]["checked"]["fields"] == 0
    assert (tmp_path / "o" / "content-reads.txt").read_text() == ""


def test_a_missing_description_is_a_structure_finding_only(tmp_path):
    files, _ = g.generate(1, 2, 0)
    del files["dataset_description.json"]
    c, f = survey(tmp_path, files)
    assert [key(x) for x in f] == [("dataset_description.json", "structure", "missing", "RQ-dataset-description")]
    assert c["conformance"]["content_reading"]["files_read"] == []


def test_a_git_blob_source_gives_the_blob_sha(tmp_path):
    import subprocess
    files, _ = g.generate(1, 2, 0)
    files["dataset_description.json"] = desc(License="")
    repo = tmp_path / "repo"
    for rel, data in files.items():
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_bytes(data)
    env = {"GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null", "PATH": "/usr/bin:/bin:/opt/homebrew/bin", "HOME": str(tmp_path)}
    for cmd in (["init", "-q"], ["add", "-A"], ["-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", "commit", "-qm", "t"]):
        subprocess.run(["git", "-C", str(repo)] + cmd, check=True, env=env)
    lst = tmp_path / "l.tsv"
    lst.write_text("".join(f"{p}\t{len(files[p])}\n" for p in sorted(files)))
    src = mf.GitBlobSource(str(repo), "HEAD")
    try:
        Recognizer(PROF, blob_source=src).run(lst, tmp_path / "o")
    finally:
        src.close()
    x = [json.loads(l) for l in (tmp_path / "o" / "findings.jsonl").read_text().splitlines() if '"content-type"' in l]
    blob = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD:dataset_description.json"], capture_output=True, text=True, env=env).stdout.strip()
    assert [(y["rule_id"], y["status"], y["evidence_blob"]) for y in x] == [("CT-license", "invalid-value", blob)]


# ---- the real dataset: ds000117, names only (reported, not scored) ------------------------------------------------------------------------------
DS = SAMPLES / "ds000117"


def test_ds000117_copy_is_names_and_the_description_only():
    assert sorted(p.name for p in DS.iterdir()) == ["dataset_description.json", "paths.tsv"]
    rows = DS.joinpath("paths.tsv").read_text().splitlines()
    assert len(rows) == 2448 and rows == sorted(rows)
    assert hashlib.sha1(b"blob %d\0" % DS.joinpath("dataset_description.json").stat().st_size + DS.joinpath("dataset_description.json").read_bytes()).hexdigest() \
        == "405983638d3b21510bdca7d99d7337c824a4adb3"                      # the blob at bids-examples 5e00d47b, copied verbatim
    assert json.loads(DS.joinpath("dataset_description.json").read_text())["License"] == "CC0"


def test_ds000117_survey_reads_only_its_description_and_leaves_the_outside_of_the_subset_unchecked(tmp_path):
    src = mf.FileSource(str(DS))
    c = Recognizer(PROF, blob_source=src).run(DS / "paths.tsv", tmp_path / "o")
    k = c["conformance"]
    assert (tmp_path / "o" / "content-reads.txt").read_text() == "dataset_description.json\n"
    found = [json.loads(x) for x in (tmp_path / "o" / "findings.jsonl").read_text().splitlines() if '"grain":"conformance"' in x]
    assert not any(f["kind"] == "content-type" for f in found)                 # BIDSVersion 1.8.0, a Name, License CC0
    roots = {r["path"]: r["reason"] for r in k["not_checked"]["roots"]}
    assert roots.get("derivatives") == "not-checked" and roots.get("stimuli") == "not-checked" and roots.get("sub-emptyroom") == "not-checked"
    assert not any(f["rule_id"] == "RQ-session" or f.get("reason") == "extension" for f in found)        # read-back FIX-B and FIX-A
    assert any(p.endswith("/meg") and r == "not-checked" for p, r in roots.items())
    assert 0 < k["score"] <= 1 and k["checked"]["fields"] == 3


# ---- read-back fixes (Architect, B2): .nii is BIDS, sub-emptyroom is MEG's, study consistency is apart -------------------------------------------
def test_nii_and_nii_gz_are_both_allowed_and_nii_zip_is_not():
    ng = PROF.name_grammar[0]
    caps = {"sub": "01", "datatype": "fmap"}
    assert ng.check("sub-01_phasediff.nii", caps) == "" and ng.check("sub-01_phasediff.nii.gz", caps) == ""
    assert ng.check("sub-01_phasediff.nii.zip", caps) == "extension" and ng.check("sub-01_phasediff.img", caps) == "extension"
    assert ng.check("sub-01_dwi.nii", {"sub": "01", "datatype": "dwi"}) == ""


def test_sub_emptyroom_is_not_checked_and_asks_nothing_of_the_others(tmp_path):
    files, _ = g.generate(1, 3, 2)
    for d in ("20090409", "20090506"):
        files[f"sub-emptyroom/ses-{d}/meg/sub-emptyroom_ses-{d}_task-noise_meg.fif"] = b""
        files[f"sub-emptyroom/ses-{d}/sub-emptyroom_ses-{d}_scans.tsv"] = b""
    c, f = survey(tmp_path, files)
    assert f == []
    roots = {r["path"]: (r["reason"], r.get("rule_id"), r["files"]) for r in c["conformance"]["not_checked"]["roots"]}
    assert roots == {"sub-emptyroom": ("not-checked", "AO-root", 4)}


def test_study_consistency_is_scored_apart_from_the_standard(tmp_path):
    spec = g.parse_spec({"mutations": [{"class": "session-inconsistency"}, {"class": "unexpected-file-in-modality-folder"}]})
    files, truth = g.generate(2, 4, 2, spec)
    c, f = survey(tmp_path, files)
    cats = c["conformance"]["by_category"]
    assert set(cats) == {"standard", "study-consistency"}
    assert cats["standard"]["findings"] == 1 and cats["study-consistency"]["findings"] == 1
    assert cats["standard"]["checked"] + cats["study-consistency"]["checked"] == c["conformance"]["checked"]["total"]
    assert {x["rule_id"]: x["category"] for x in f} == {"RQ-session": "study-consistency", "AO-datatype": "standard"}
    assert {r.id for r in PROF.required if r.category == "study-consistency"} == {"RQ-session", "RQ-datatype", "RQ-datatype-ses"}
