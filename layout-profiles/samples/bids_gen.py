"""A deterministic, seeded generator of BIDS-SHAPED sample trees for the conformance notebook (Phase 2, notebook 05). Synthetic only: no real data.

    python samples/bids_gen.py --seed 1 --subjects 3 --sessions 2 --out OUT [--mutations SPEC.yaml]

Writes, below OUT (which must be empty or absent):
  OUT/dataset/...      the tree: modality folders anat, func, dwi and fmap per subject (and session), the top-level files dataset_description.json,
                       README, participants.tsv and CHANGES. Data files are EMPTY, sidecars are `{}`, and dataset_description.json carries exactly
                       the three fields BIDSVersion, Name and License (synthetic, CC0).
  OUT/paths.tsv        `path<TAB>size` of every file of OUT/dataset, sorted (the recognizer's input; the same as recognizer/listpaths.py gives)
  OUT/truth.jsonl      one line per INJECTED deviation: path, kind, status, the rule expected to report it, and the mutation class. Empty for a clean tree.

The same seed, subject and session counts and spec give a byte-identical tree and truth. The seed picks the tasks, runs, echoes, acquisition labels,
field-map layout and session labels of the clean tree, and the targets of the mutations; a spec entry may name its target where the class allows it.

SPEC.yaml:
  mutations:
    - class: wrong-case          # one of CLASSES below
      variant: file              # only where the class has variants (see VARIANTS)
      count: 2                   # optional, default 1
      file: CHANGES              # missing-top-level-file only: which file (default: seeded)

A finding's kind and status, and the rule expected to report it, are fixed per class (CLASSES). Rule ids are those of profiles/bids-dataset.yaml.
A `missing` deviation's path is the EXPECTED path (the file or folder that is not there).
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

BIDS_VERSION = "1.11.2"                         # the spec version the generated tree claims (bids-dataset 0.1.0 encodes a subset of it)
TOP_FILES = {"dataset_description.json": "RQ-dataset-description", "README": "RQ-readme", "participants.tsv": "RQ-participants", "CHANGES": "RQ-changes"}
DATATYPES = ("anat", "func", "dwi", "fmap")
TASK_WORDS = ("faces", "motor", "nback", "rest", "stroop")
SESSION_STYLES = (("01", "02", "03", "04"), ("pre", "post", "followup"))
UNEXPECTED_DIRS = ("analysis_old", "extra", "misc", "notes", "results")      # no name a hidden-subtree rule claims (build, tmp, .git ...), none shaped like sub-
UNEXPECTED_FILES = ("info.csv", "notes.txt", "protocol.pdf", "Thumbs.db")    # no entity, no BIDS suffix, no hidden extension (.log, .bak ...)
UNKNOWN_KEYS = ("batch", "foo", "scanner", "site")
STRAY_TAGS = ("FINAL", "copy2", "final_v2", "old")
BAD_VERSIONS = ("1.8", "latest", "v1.11.2")

# class -> (kind, status). The expected rule depends on the target and is set where the mutation is made.
CLASSES = {
    "missing-top-level-file": ("structure", "missing"),
    "missing-modality-folder": ("structure", "missing"),
    "unexpected-top-level-folder": ("structure", "unexpected"),
    "unexpected-file-in-modality-folder": ("structure", "unexpected"),
    "entity-order": ("naming", "misnamed"),
    "unknown-entity-key": ("naming", "misnamed"),
    "illegal-label-character": ("naming", "misnamed"),
    "wrong-case": ("naming", "misnamed"),
    "wrong-extension": ("naming", "misnamed"),
    "session-inconsistency": ("structure", "missing"),
    "stray-name": ("naming", "misnamed"),
    "bidsversion-missing": ("content-type", "missing-field"),
    "bidsversion-invalid": ("content-type", "invalid-value"),
    "license-missing": ("content-type", "missing-field"),
    "license-empty": ("content-type", "invalid-value"),
    "name-empty": ("content-type", "invalid-value"),
    "malformed-json": ("content-type", "unreadable"),
}
VARIANTS = {"wrong-case": ("dir", "file"), "illegal-label-character": ("underscore", "bang")}
SUBJECT_CLASSES = ("illegal-label-character", "session-inconsistency", "missing-modality-folder")   # each (and wrong-case dir) uses up one whole subject
CONTENT_CLASSES = tuple(c for c in CLASSES if CLASSES[c][0] == "content-type")
ORDER = ("illegal-label-character", "wrong-case", "session-inconsistency", "missing-modality-folder", "entity-order", "unknown-entity-key", "wrong-extension",
         "stray-name", "unexpected-file-in-modality-folder", "unexpected-top-level-folder", "missing-top-level-file") + CONTENT_CLASSES
SPEC_KEYS = ("class", "variant", "count", "file")


class SpecError(ValueError):
    """The mutation spec cannot be applied to this tree (an unknown class or key, a conflict, or too few subjects or sessions)."""


# ---- the clean tree --------------------------------------------------------------------------------------------------------------------------------
def _name(entities: list, suffix: str, ext: str) -> str:
    return "_".join(f"{k}-{v}" for k, v in entities) + f"_{suffix}{ext}"


def _layout(rng: random.Random, sessions: int) -> dict:
    """The seeded choices that every subject shares (a regular dataset: the same scans for every subject and session)."""
    style = rng.choice([s for s in SESSION_STYLES if len(s) >= sessions]) if sessions else ()
    return {
        "sessions": list(style[:sessions]),
        "tasks": sorted(rng.sample(TASK_WORDS, rng.randint(1, 2))),
        "runs": rng.randint(1, 2),
        "echoes": 2 if rng.random() < 0.25 else 1,
        "t2w": rng.random() < 0.5,
        "anat_acq": "mprage" if rng.random() < 0.3 else None,
        "dwi_dir": rng.choice([None, "AP"]),
        "fmap": rng.choice(["phasediff", "epi"]),
    }


def _scans(sub: str, ses: str | None, lay: dict) -> list:
    """(datatype, file name) of one subject and session, in BIDS entity order: sub, ses, task, acq, dir, run, echo."""
    base = [("sub", sub)] + ([("ses", ses)] if ses else [])
    out = []
    acq = [("acq", lay["anat_acq"])] if lay["anat_acq"] else []
    for suffix in ["T1w"] + (["T2w"] if lay["t2w"] else []):
        out += [("anat", _name(base + acq, suffix, ".nii.gz")), ("anat", _name(base + acq, suffix, ".json"))]
    for task in lay["tasks"]:
        for run in range(1, lay["runs"] + 1):
            ent = base + [("task", task)] + ([("run", str(run))] if lay["runs"] > 1 else [])
            for echo in range(1, lay["echoes"] + 1):
                e = ent + ([("echo", str(echo))] if lay["echoes"] > 1 else [])
                out += [("func", _name(e, "bold", ".nii.gz")), ("func", _name(e, "bold", ".json"))]
            out.append(("func", _name(ent, "events", ".tsv")))
    d = [("dir", lay["dwi_dir"])] if lay["dwi_dir"] else []
    out += [("dwi", _name(base + d, "dwi", x)) for x in (".nii.gz", ".json", ".bval", ".bvec")]
    if lay["fmap"] == "phasediff":
        for suffix in ("magnitude1", "magnitude2", "phasediff"):
            out += [("fmap", _name(base, suffix, ".nii.gz")), ("fmap", _name(base, suffix, ".json"))]
    else:
        for pe in ("AP", "PA"):
            out += [("fmap", _name(base + [("dir", pe)], "epi", ".nii.gz")), ("fmap", _name(base + [("dir", pe)], "epi", ".json"))]
    return out


def description(seed: int, drop: tuple = (), set_: dict | None = None, malformed: bool = False) -> bytes:
    doc = {"BIDSVersion": BIDS_VERSION, "Name": f"Synthetic BIDS-shaped dataset (bids_gen seed {seed})", "License": "CC0"}
    for k in drop:
        doc.pop(k, None)
    doc.update(set_ or {})
    text = json.dumps(doc, indent=2) + "\n"
    if malformed:
        text = text.rstrip().rstrip("}") + "\n"                       # the closing brace is gone: not JSON any more
    return text.encode("utf-8")


def clean_tree(seed: int, subjects: int, sessions: int) -> tuple[dict, dict]:
    """(files: path -> bytes, layout facts) of the clean tree. Labels are synthetic: sub-01, sub-02 ..."""
    if subjects < 1 or sessions < 0:
        raise SpecError("--subjects must be 1 or more and --sessions 0 or more")
    if sessions > max(len(s) for s in SESSION_STYLES):
        raise SpecError(f"--sessions is at most {max(len(s) for s in SESSION_STYLES)}")
    rng = random.Random(f"bids_gen:{seed}:tree")
    lay = _layout(rng, sessions)
    subs = [f"{i:02d}" for i in range(1, subjects + 1)]
    files = {
        "dataset_description.json": description(seed),
        "README": f"Synthetic BIDS-shaped dataset written by layout-profiles/samples/bids_gen.py (seed {seed}). Every data file is empty.\n".encode(),
        "CHANGES": b"1.0.0 2026-11-27\n  - Generated by bids_gen.py.\n",
        "participants.tsv": ("participant_id\n" + "".join(f"sub-{s}\n" for s in subs)).encode(),
    }
    for s in subs:
        for ses in (lay["sessions"] or [None]):
            prefix = f"sub-{s}/" + (f"ses-{ses}/" if ses else "")
            for dt, name in _scans(s, ses, lay):
                files[prefix + dt + "/" + name] = b"{}" if name.endswith(".json") else b""
    lay["subjects"] = subs
    return files, lay


# ---- mutations -------------------------------------------------------------------------------------------------------------------------------------
def load_spec(path: Path | None) -> list:
    if path is None:
        return []
    import yaml
    doc = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return parse_spec(doc)


def parse_spec(doc) -> list:
    """A list of (class, variant | None, file | None), one entry per mutation (count expanded), in the order they are applied."""
    if not isinstance(doc, dict) or set(doc) - {"mutations"}:
        raise SpecError("a spec is a mapping with the one key 'mutations'")
    items = doc.get("mutations") or []
    if not isinstance(items, list):
        raise SpecError("mutations must be a list")
    out = []
    for n, m in enumerate(items):
        if not isinstance(m, dict) or set(m) - set(SPEC_KEYS) or "class" not in m:
            raise SpecError(f"mutations[{n}]: a mapping with 'class' and optionally {list(SPEC_KEYS[1:])}")
        cls = m["class"]
        if cls not in CLASSES:
            raise SpecError(f"mutations[{n}]: unknown class {cls!r}; known {sorted(CLASSES)}")
        variant = m.get("variant")
        if variant is not None and variant not in VARIANTS.get(cls, ()):
            raise SpecError(f"mutations[{n}]: class {cls!r} has variants {list(VARIANTS.get(cls, ()))}, not {variant!r}")
        f = m.get("file")
        if f is not None and (cls != "missing-top-level-file" or f not in TOP_FILES):
            raise SpecError(f"mutations[{n}]: 'file' is for missing-top-level-file only, one of {sorted(TOP_FILES)}")
        count = m.get("count", 1)
        if not isinstance(count, int) or isinstance(count, bool) or count < 1:
            raise SpecError(f"mutations[{n}]: count must be a positive integer")
        out += [(cls, variant, f)] * count
    return sorted(out, key=lambda x: ORDER.index(x[0]))                # a fixed order of application, whatever the spec order


def _expected_rule_datatype(lay: dict) -> str:
    return "RQ-datatype-ses" if lay["sessions"] else "RQ-datatype"


def mutate(files: dict, lay: dict, seed: int, spec: list) -> list:
    """Apply the spec to `files` IN PLACE and return the truth lines. A whole subject is kept untouched as a witness, so every folder that the profile
    requires per subject is still seen in some conforming subject (otherwise a deleted folder could not be expected)."""
    rng = random.Random(f"bids_gen:{seed}:mutations")
    spec = [(c, v or (rng.choice(VARIANTS[c]) if c in VARIANTS else None), f) for c, v, f in spec]      # seeded variants first, so the rest is fixed
    truth: list = []
    subs = list(lay["subjects"])
    free = list(subs)                                                 # subjects no subject-level mutation has used
    needs_witness = any(c in SUBJECT_CLASSES or (c, v) == ("wrong-case", "dir") for c, v, _ in spec)
    if needs_witness:
        if len(subs) < 2:
            raise SpecError("a subject-level mutation needs at least 2 subjects (one stays untouched)")
        free.remove(rng.choice(subs))
    renamed: dict = {}                                                # old subject folder -> new name (its files are then not checked)
    gone: set = set()                                                 # path prefixes that were deleted
    touched_files: set = set()
    content: dict = {"drop": [], "set": {}, "malformed": False, "fields": set()}

    def add(path, cls, rule):
        kind, status = CLASSES[cls]
        truth.append({"path": path, "kind": kind, "status": status, "rule": rule, "class": cls})

    def take_subject(cls):
        if not free:
            raise SpecError(f"{cls}: no subject left to use (each subject-level mutation needs its own subject, and one stays untouched)")
        s = rng.choice(free)
        free.remove(s)
        return s

    def data_files(pred):
        """Clean files still in place: not deleted, not in a renamed subject, not already mutated; sorted, so the seeded choice is stable."""
        return sorted(p for p in files if "/" in p and p not in touched_files and not any(p.startswith(g + "/") for g in gone)
                      and p.split("/", 1)[0] not in renamed and pred(p))

    def rename_file(old, new, cls):
        files[new] = files.pop(old)
        touched_files.add(new)
        add(new, cls, "NG-bids")

    for cls, variant, which in spec:
        if cls == "illegal-label-character" or (cls, variant) == ("wrong-case", "dir"):
            s = take_subject(cls)
            old = f"sub-{s}"
            if cls == "wrong-case":
                new = f"Sub-{s}"
            else:
                new = f"sub-{s[0]}_{s[1:]}" if variant == "underscore" else f"sub-{s}!"
            for p in sorted(p for p in files if p.startswith(old + "/")):
                files[new + p[len(old):]] = files.pop(p)
            renamed[new] = old
            add(new, cls, "PG-subject")
        elif cls == "wrong-case":                                     # the file variant: a suffix in the wrong case (T1W, BOLD)
            cands = data_files(lambda p: p.endswith(".nii.gz"))
            if not cands:
                raise SpecError(f"{cls}: no data file left")
            old = rng.choice(cands)
            d, _, name = old.rpartition("/")
            stem = name[:-len(".nii.gz")]
            head, _, suffix = stem.rpartition("_")
            bad = suffix.upper() if suffix.upper() != suffix else suffix.lower()
            rename_file(old, f"{d}/{head}_{bad}.nii.gz", cls)
        elif cls == "session-inconsistency":
            if len(lay["sessions"]) < 2:
                raise SpecError(f"{cls}: needs at least 2 sessions")
            s = take_subject(cls)
            ses = rng.choice(lay["sessions"])
            prefix = f"sub-{s}/ses-{ses}"
            for p in [p for p in files if p.startswith(prefix + "/")]:
                del files[p]
            gone.add(prefix)
            add(prefix, cls, "RQ-session")
        elif cls == "missing-modality-folder":
            s = take_subject(cls)
            ses = rng.choice(lay["sessions"]) if lay["sessions"] else None
            dt = rng.choice(DATATYPES)
            prefix = f"sub-{s}/" + (f"ses-{ses}/" if ses else "") + dt
            for p in [p for p in files if p.startswith(prefix + "/")]:
                del files[p]
            gone.add(prefix)
            add(prefix, cls, _expected_rule_datatype(lay))
        elif cls == "entity-order":                                   # the task entity moved in front of sub
            cands = data_files(lambda p: "_task-" in p.rpartition("/")[2] and p.endswith(".nii.gz"))
            if not cands:
                raise SpecError(f"{cls}: no functional file left")
            old = rng.choice(cands)
            d, _, name = old.rpartition("/")
            parts = name.split("_")
            task = next(x for x in parts if x.startswith("task-"))
            parts.remove(task)
            rename_file(old, f"{d}/{'_'.join([task] + parts)}", cls)
        elif cls == "unknown-entity-key":
            cands = data_files(lambda p: p.endswith(".nii.gz"))
            if not cands:
                raise SpecError(f"{cls}: no data file left")
            old = rng.choice(cands)
            d, _, name = old.rpartition("/")
            parts = name.split("_")
            at = 2 if len(parts) > 2 and parts[1].startswith("ses-") else 1
            parts.insert(at, f"{rng.choice(UNKNOWN_KEYS)}-a")
            rename_file(old, f"{d}/{'_'.join(parts)}", cls)
        elif cls == "wrong-extension":
            cands = data_files(lambda p: p.endswith(".nii.gz"))
            if not cands:
                raise SpecError(f"{cls}: no data file left")
            old = rng.choice(cands)
            rename_file(old, old[:-len(".nii.gz")] + ".nii.zip", cls)               # BIDS allows .nii.gz and .nii, not .nii.zip
        elif cls == "stray-name":                                     # a stray copy beside the original: sub-01_T1w_final_v2.nii.gz
            cands = data_files(lambda p: p.endswith(".nii.gz"))
            if not cands:
                raise SpecError(f"{cls}: no data file left")
            src = rng.choice(cands)
            new = src[:-len(".nii.gz")] + f"_{rng.choice(STRAY_TAGS)}.nii.gz"
            if new in files:
                raise SpecError(f"{cls}: {new} exists already")
            files[new] = b""
            touched_files.update({src, new})
            add(new, cls, "NG-bids")
        elif cls == "unexpected-file-in-modality-folder":
            dirs = sorted({p.rpartition("/")[0] for p in data_files(lambda p: p.rpartition("/")[0].rpartition("/")[2] in DATATYPES)})
            if not dirs:
                raise SpecError(f"{cls}: no modality folder left")
            d = rng.choice(dirs)
            names = [n for n in UNEXPECTED_FILES if f"{d}/{n}" not in files]
            new = f"{d}/{rng.choice(names)}"
            files[new] = b""
            touched_files.add(new)
            add(new, cls, "AO-datatype")
        elif cls == "unexpected-top-level-folder":
            names = [n for n in UNEXPECTED_DIRS if not any(p.startswith(n + "/") for p in files)]
            if not names:
                raise SpecError(f"{cls}: no unexpected folder name left")
            n = rng.choice(names)
            files[f"{n}/{rng.choice(UNEXPECTED_FILES)}"] = b""
            add(n, cls, "AO-root")
        elif cls == "missing-top-level-file":
            left = sorted(f for f in TOP_FILES if f in files and not (f == "dataset_description.json" and any(c in CONTENT_CLASSES for c, _, _ in spec)))
            f = which or (rng.choice(left) if left else None)
            if f is None or f not in files:
                raise SpecError(f"{cls}: {f or 'no top-level file'} is not there to remove")
            if f == "dataset_description.json" and content["fields"]:
                raise SpecError(f"{cls}: dataset_description.json is changed by a content-type mutation; it cannot also be missing")
            del files[f]
            add(f, cls, TOP_FILES[f])
        else:                                                         # content-type: dataset_description.json fields
            if "dataset_description.json" not in files:
                raise SpecError(f"{cls}: dataset_description.json is missing")
            field = {"bidsversion": "BIDSVersion", "license": "License", "name": "Name", "malformed": "*"}[cls.split("-")[0]]
            if field in content["fields"] or content["malformed"] or (field == "*" and content["fields"]):
                raise SpecError(f"{cls}: a second content-type mutation of the same field (or with malformed-json)")
            content["fields"].add(field)
            if cls == "malformed-json":
                content["malformed"] = True
                rule = "CT-unreadable"
            elif cls.endswith("-missing"):
                content["drop"].append(field)
                rule = f"CT-{field.lower()}"
            else:
                content["set"][field] = rng.choice(BAD_VERSIONS) if cls == "bidsversion-invalid" else ""
                rule = f"CT-{field.lower()}"
            files["dataset_description.json"] = description(seed, tuple(content["drop"]), content["set"], content["malformed"])
            add("dataset_description.json", cls, rule)
    truth.sort(key=lambda t: (t["path"], t["rule"], t["class"]))
    return truth


def generate(seed: int, subjects: int = 3, sessions: int = 2, spec: list | None = None) -> tuple[dict, list]:
    """(files: path -> bytes, truth lines) for one seed, subject count, session count and parsed spec."""
    files, lay = clean_tree(seed, subjects, sessions)
    truth = mutate(files, lay, seed, spec or [])
    return dict(sorted(files.items())), truth


# ---- writing ---------------------------------------------------------------------------------------------------------------------------------------
def write_outputs(files: dict, truth: list, out: Path) -> None:
    """Write OUT/dataset/<path> for every file, OUT/paths.tsv and OUT/truth.jsonl. OUT must be absent or an empty directory."""
    out = Path(out)
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise SpecError(f"{out} exists and is not an empty directory")
    root = out / "dataset"
    root.mkdir(parents=True)
    for rel in sorted(files):
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(files[rel])
    (out / "paths.tsv").write_bytes("".join(f"{rel}\t{len(files[rel])}\n" for rel in sorted(files)).encode("utf-8"))
    (out / "truth.jsonl").write_bytes("".join(json.dumps(t, sort_keys=True, separators=(",", ":")) + "\n" for t in truth).encode("utf-8"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--subjects", type=int, default=3)
    ap.add_argument("--sessions", type=int, default=2)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--mutations", type=Path, metavar="SPEC.yaml")
    a = ap.parse_args(argv)
    try:
        files, truth = generate(a.seed, a.subjects, a.sessions, load_spec(a.mutations))
        write_outputs(files, truth, a.out)
    except SpecError as exc:
        print(f"bids_gen: {exc}", file=sys.stderr)
        return 2
    print(f"bids_gen seed {a.seed}: {len(files)} files, {len(truth)} injected deviation(s) -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
