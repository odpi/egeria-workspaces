"""A deterministic, seeded generator of CalculiX-SHAPED parametric-sweep trees for notebook 04a (Phase 2). Synthetic only: file NAMES follow the
CalculiX (.inp, .frd, .dat, .sta, .cvg, .msg, .12d, .rout) and Gmsh (.msh) conventions; every file is a one-line placeholder. No solver input,
mesh, result or example is copied, and no tool is run.

    python samples/fea_sweep_gen.py --seed 1 --out OUT [--grid 4x5x3 | --large] [--ran-fraction 0.8] [--mutations SPEC.yaml]

Writes, below OUT (which must be empty or absent):
  OUT/study-<name>/...        the tree (below). The scanned root is OUT, the PARENT of the study folder: the recognizer makes parts only below a
                              component that is not the scanned root, and the study is that component
  OUT/paths.tsv               `path<TAB>size` of every file below OUT/study-<name>, sorted (the recognizer's input; paths start with study-<name>/;
                              paths.tsv and truth.jsonl themselves are not listed)
  OUT/truth.jsonl             one line per INJECTED deviation: path, kind, status, the mutation class, the variant injected (a class with
                              variants) and the expected rule (off-grammar-case-name). Empty for a clean tree.

The tree:
  study-<name>/README.md, sweep.yaml           sweep.yaml is a placeholder: presence only, never read
  templates/base.inp, materials/<material>.inp, mesh/<part>_<level>.msh
  cases/case_E<E>_t<t>_mesh-<level>/           one per grid point: job.inp and run.log; a case that RAN also has job.frd, job.dat, job.sta,
                                               job.cvg and job.msg, and some have job.12d and job.rout
  post/<case-id>/plot-*.png, summary.csv       for every case that ran; post/sweep-summary.csv
  validation/rig-<id>/reference.csv            names only: a test-rig reference folder
  scratch/..., *.bak, *~                       junk a profile should hide

Grid: --grid ExTxM (moduli x thicknesses x mesh levels; default 4x5x3 = 60 cases; --large is 10x20x3 = 600). E is an integer (GPa), t a
thickness with `p` for the decimal point (2p0 = 2.0 mm), the mesh level one of coarse, medium, fine (the first M of them). The seed picks the
grid values, the study name, parts and materials, which cases ran (--ran-fraction of them, rounded), the junk files and the mutation targets.
The same seed, grid, fraction and spec give a byte-identical tree and truth.

SPEC.yaml:
  mutations:
    - class: off-grammar-case-name   # one of CLASSES below
      variant: no-decimal            # only where the class has variants (VARIANTS); default: seeded
      count: 2                       # optional, default 1

The kind and status of each class are fixed (CLASSES). An off-grammar-case-name line also carries `rule`: PG-case when the new name has the case
SHAPE (expected_case_rule), else PG-case-any. A bad mesh level is injected in a case name only (mesh/ file names are not judged in 0.1.0). off-grid
and duplicate findings need the declared grid (the profile instance); a duplicate's path is the SECOND folder of the pair in sorted path order. A `missing` deviation's path is the EXPECTED
path. A mutation that renames or removes a case removes that case's post/ folder too, except orphan-post, which keeps it on purpose.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

MESH_LEVELS = ("coarse", "medium", "fine")
E_POOL = tuple(range(40, 240, 10))                        # 20 moduli, GPa
T_POOL = tuple(x / 2 for x in range(1, 21))                # 20 thicknesses, 0.5 .. 10.0 mm
DEFAULT_GRID = (4, 5, 3)
LARGE_GRID = (10, 20, 3)
STUDY_WORDS = ("bracket", "beam", "flange", "hinge", "plate", "rib")
MATERIALS = ("aluminium", "copper", "steel", "titanium")
PLOTS = ("plot-displacement.png", "plot-stress.png")
RAN_FILES = ("job.frd", "job.dat", "job.sta", "job.cvg", "job.msg")
UNEXPECTED_DIRS = ("archive_old", "misc", "notes", "old_runs", "results_v1")    # no name a hide rule claims (scratch, build, .git ...)
STRAY_DECKS = ("job_old.inp", "job_backup.inp", "old_job.inp")
BAD_MESH = ("ultra", "veryfine", "xfine")
STRAY_TAGS = ("final_v2", "copy", "old")

# class -> (kind, status), or variant -> (kind, status) where the variant decides
CLASSES = {
    "missing-input-deck": ("structure", "missing"),
    "off-grammar-case-name": ("naming", "misnamed"),       # every folder directly under cases/ that fails the case grammar is a misnamed case
    "off-grid-value": ("naming", "off-grid"),
    "duplicate-combination": ("structure", "duplicate"),
    "results-without-deck": ("structure", "missing"),
    "stray-deck": ("structure", "unexpected"),
    "bad-mesh-level": ("naming", "off-grid"),             # in a CASE name only: mesh is a grid axis (mesh/ file names are not judged in 0.1.0)
    "unexpected-top-level-folder": ("structure", "unexpected"),
    "orphan-post": ("structure", "unexpected"),
}
VARIANTS = {"off-grammar-case-name": ("no-decimal", "wrong-case", "stray-suffix"), "off-grid-value": ("E", "t"), "duplicate-combination": ("E", "t")}
ORDER = tuple(CLASSES)                                     # mutations are applied in this order, whatever the spec order
SPEC_KEYS = ("class", "variant", "count")


class SpecError(ValueError):
    """The grid or the mutation spec cannot be used (an unknown class, key or variant, or no case left to mutate)."""


# ---- names -----------------------------------------------------------------------------------------------------------------------------------------
def fmt_t(t: float) -> str:
    """2.0 -> '2p0', 0.5 -> '0p5' (one decimal, `p` for the point)."""
    return f"{t:.1f}".replace(".", "p")


def case_id(e: int, t: float, level: str) -> str:
    return f"case_E{e}_t{fmt_t(t)}_mesh-{level}"


CASE_RE = re.compile(r"^case_E(?P<E>[0-9]+)_t(?P<t>[0-9]+p[0-9]+)_mesh-(?P<mesh>[a-z]+)$")


def parse_case(name: str) -> dict | None:
    """{'E': '210', 't': '2p0', 'mesh': 'fine'} for a clean case folder name, else None (used by tests and the notebook to check tokens)."""
    m = CASE_RE.match(name)
    return m.groupdict() if m else None


# The SHAPE of the case pattern study-{study}/cases/case_E{E}_t{t}_mesh-{mesh} in its last segment, as recognizer/grammar.py relaxes it: literals
# compared ignoring case, any text (one character or more) for each regex token. A misnamed folder under cases/ with this shape is reported under
# PG-case; any other folder name under cases/ under the catch-all PG-case-any.
CASE_SHAPE = re.compile(r"case_E.+_t.+_mesh-.+", re.IGNORECASE)


def expected_case_rule(name: str) -> str:
    """The rule a misnamed folder directly under cases/ is reported under: PG-case when it has the case shape, else PG-case-any."""
    return "PG-case" if CASE_SHAPE.fullmatch(name) else "PG-case-any"


def parse_grid(text: str) -> tuple:
    m = re.fullmatch(r"([0-9]+)x([0-9]+)x([0-9]+)", str(text))
    if not m:
        raise SpecError(f"--grid is ExTxM, like 4x5x3, not {text!r}")
    ne, nt, nm = (int(x) for x in m.groups())
    if not (1 <= ne <= len(E_POOL) and 1 <= nt <= len(T_POOL) and 1 <= nm <= len(MESH_LEVELS)):
        raise SpecError(f"--grid: E from 1 to {len(E_POOL)}, t from 1 to {len(T_POOL)}, mesh levels from 1 to {len(MESH_LEVELS)}")
    return ne, nt, nm


def placeholder(what: str) -> bytes:
    return f"fea_sweep_gen placeholder: {what}; not a real file of any tool\n".encode("utf-8")


# ---- the clean tree --------------------------------------------------------------------------------------------------------------------------------
def clean_tree(seed: int, grid: tuple = DEFAULT_GRID, ran_fraction: float = 0.8) -> tuple[dict, dict]:
    """(files: path -> bytes, layout facts). Paths are relative to the scanned root and start with study-<name>/."""
    if not 0.0 <= ran_fraction <= 1.0:
        raise SpecError("--ran-fraction is from 0 to 1")
    ne, nt, nm = grid
    rng = random.Random(f"fea_sweep_gen:{seed}:tree")
    study = f"study-{rng.choice(STUDY_WORDS)}"
    parts = sorted(rng.sample(STUDY_WORDS, rng.randint(1, 2)))
    materials = sorted(rng.sample(MATERIALS, rng.randint(1, 3)))
    es = sorted(rng.sample(E_POOL, ne))
    ts = sorted(rng.sample(T_POOL, nt))
    levels = list(MESH_LEVELS[:nm])
    cases = [case_id(e, t, lv) for e in es for t in ts for lv in levels]
    ran = set(rng.sample(cases, round(ran_fraction * len(cases))))
    s = study + "/"
    files = {
        s + "README.md": placeholder("study README"),
        s + "sweep.yaml": b"# fea_sweep_gen placeholder: the sweep definition; presence only, never read\n",
        s + "templates/base.inp": placeholder("input deck template"),
        s + "post/sweep-summary.csv": placeholder("sweep summary table"),
    }
    for m in materials:
        files[f"{s}materials/{m}.inp"] = placeholder(f"material {m}")
    for p in parts:
        for lv in levels:
            files[f"{s}mesh/{p}_{lv}.msh"] = placeholder(f"mesh {p} {lv}")
    for c in cases:
        d = f"{s}cases/{c}/"
        files[d + "job.inp"] = placeholder("input deck")
        files[d + "run.log"] = placeholder("run log")
        if c in ran:
            for f in RAN_FILES:
                files[d + f] = placeholder(f"solver output {f}")
            if rng.random() < 0.5:
                files[d + "job.12d"] = placeholder("eigen data")
            if rng.random() < 0.3:
                files[d + "job.rout"] = placeholder("restart data")
            for f in PLOTS:
                files[f"{s}post/{c}/{f}"] = placeholder(f"plot {f}")
            files[f"{s}post/{c}/summary.csv"] = placeholder("case summary")
    for n in range(1, rng.randint(1, 2) + 1):
        files[f"{s}validation/rig-{n:02d}/reference.csv"] = placeholder("test-rig reference")
    # junk the profile should hide: a scratch folder, backup copies and editor leftovers
    files[s + "scratch/try1.inp"] = placeholder("scratch deck")
    files[s + "scratch/notes.txt"] = placeholder("scratch notes")
    files[s + "README.md~"] = placeholder("editor backup")
    files[s + "templates/base.inp~"] = placeholder("editor backup")
    for c in sorted(rng.sample(cases, min(2, len(cases)))):
        files[f"{s}cases/{c}/job.inp.bak"] = placeholder("backup deck")
    lay = {"study": study, "E": es, "t": ts, "mesh": levels, "cases": cases, "ran": sorted(ran), "parts": parts, "materials": materials}
    return files, lay


# ---- mutations -------------------------------------------------------------------------------------------------------------------------------------
def load_spec(path: Path | None) -> list:
    if path is None:
        return []
    import yaml
    doc = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return parse_spec(doc)


def parse_spec(doc) -> list:
    """A list of (class, variant | None), one entry per mutation (count expanded), in the order they are applied."""
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
        count = m.get("count", 1)
        if not isinstance(count, int) or isinstance(count, bool) or count < 1:
            raise SpecError(f"mutations[{n}]: count must be a positive integer")
        out += [(cls, variant)] * count
    return sorted(out, key=lambda x: ORDER.index(x[0]))


def kind_status(cls: str, variant: str | None) -> tuple:
    ks = CLASSES[cls]
    return ks[variant] if isinstance(ks, dict) else ks


def mutate(files: dict, lay: dict, seed: int, spec: list) -> list:
    """Apply the spec to `files` IN PLACE and return the truth lines. Each mutation uses its own case(s): no case is mutated twice."""
    rng = random.Random(f"fea_sweep_gen:{seed}:mutations")
    spec = [(c, v or (rng.choice(VARIANTS[c]) if c in VARIANTS else None)) for c, v in spec]      # seeded variants first, so the rest is fixed
    s = lay["study"] + "/"
    free = list(lay["cases"])                              # cases no mutation has used
    ran = set(lay["ran"])
    truth: list = []

    def add(path, cls, variant=None, rule=None):
        kind, status = kind_status(cls, variant)
        t = {"path": path, "kind": kind, "status": status, "class": cls}
        if variant is not None:
            t["variant"] = variant                         # which form was injected
        if rule is not None:
            t["rule"] = rule                               # off-grammar-case-name: PG-case or PG-case-any, by the stated shape criterion
        truth.append(t)

    def take(cls, pred=lambda c: True):
        cands = [c for c in free if pred(c)]
        if not cands:
            raise SpecError(f"{cls}: no case left to use")
        c = rng.choice(cands)
        free.remove(c)
        return c

    def case_files(c):
        return sorted(p for p in files if p.startswith(f"{s}cases/{c}/"))

    def drop_post(c):
        for p in [p for p in files if p.startswith(f"{s}post/{c}/")]:
            del files[p]

    def rename_case(old, new):
        if any(p.startswith(f"{s}cases/{new}/") for p in files):
            raise SpecError(f"cases/{new} exists already")
        for p in case_files(old):
            files[f"{s}cases/{new}/" + p.rsplit("/", 1)[1]] = files.pop(p)
        drop_post(old)

    def toks(c):
        return parse_case(c)

    for cls, variant in spec:
        if cls == "missing-input-deck":                    # a case that did not run loses its deck (run.log keeps the folder)
            c = take(cls, lambda c: c not in ran)
            del files[f"{s}cases/{c}/job.inp"]
            add(f"{s}cases/{c}/job.inp", cls)
        elif cls == "results-without-deck":                # a case that ran (results are there) loses its deck
            c = take(cls, lambda c: c in ran)
            del files[f"{s}cases/{c}/job.inp"]
            add(f"{s}cases/{c}/job.inp", cls)
        elif cls == "off-grammar-case-name":
            c = take(cls)
            k = toks(c)
            if variant == "no-decimal":                    # case_E210_t2_mesh-fine: the thickness without its decimal part
                new = f"case_E{k['E']}_t{k['t'].split('p')[0]}_mesh-{k['mesh']}"
            elif variant == "wrong-case":                  # Case_E210_t2p0_mesh-fine
                new = "C" + c[1:]
            else:                                          # case_E210_t2p0_final_v2: a hand-renamed copy, the mesh level lost
                new = f"case_E{k['E']}_t{k['t']}_{rng.choice(STRAY_TAGS)}"
            rename_case(c, new)
            add(f"{s}cases/{new}", cls, variant, rule=expected_case_rule(new))
        elif cls == "off-grid-value":                      # a value the declared grid does not have (t9p9, E999)
            c = take(cls)
            k = toks(c)
            new = f"case_E999_t{k['t']}_mesh-{k['mesh']}" if variant == "E" else f"case_E{k['E']}_t9p9_mesh-{k['mesh']}"
            rename_case(c, new)
            add(f"{s}cases/{new}", cls, variant)
        elif cls == "duplicate-combination":               # a second folder with the same values, spelt differently (E0210, t2p00)
            c = take(cls)
            k = toks(c)
            new = f"case_E0{k['E']}_t{k['t']}_mesh-{k['mesh']}" if variant == "E" else f"case_E{k['E']}_t{k['t']}0_mesh-{k['mesh']}"
            if any(p.startswith(f"{s}cases/{new}/") for p in files):
                raise SpecError(f"{cls}: cases/{new} exists already")
            for p in case_files(c):
                files[f"{s}cases/{new}/" + p.rsplit("/", 1)[1]] = files[p]
            add(f"{s}cases/{max(c, new)}", cls, variant)   # the second folder in sorted path order is the duplicate (the first is the one it repeats)
        elif cls == "stray-deck":                          # a deck loose in cases/, at the level of the case folders
            names = [n for n in STRAY_DECKS if f"{s}cases/{n}" not in files]
            if not names:
                raise SpecError(f"{cls}: no stray deck name left")
            n = rng.choice(names)
            files[f"{s}cases/{n}"] = placeholder("stray input deck")
            add(f"{s}cases/{n}", cls)
        elif cls == "bad-mesh-level":                      # case_E210_t2p0_mesh-ultra: a level outside the declared grid (case names only)
            c = take(cls)
            k = toks(c)
            new = f"case_E{k['E']}_t{k['t']}_mesh-{rng.choice(BAD_MESH)}"
            rename_case(c, new)
            add(f"{s}cases/{new}", cls)
        elif cls == "unexpected-top-level-folder":
            names = [n for n in UNEXPECTED_DIRS if not any(p.startswith(f"{s}{n}/") for p in files)]
            if not names:
                raise SpecError(f"{cls}: no unexpected folder name left")
            n = rng.choice(names)
            files[f"{s}{n}/notes.txt"] = placeholder("unexpected folder")
            add(f"{s}{n}", cls)
        elif cls == "orphan-post":                         # the case is gone, its post/ folder stays
            c = take(cls, lambda c: c in ran)
            for p in case_files(c):
                del files[p]
            add(f"{s}post/{c}", cls)
    truth.sort(key=lambda t: (t["path"], t["class"]))
    return truth


def generate(seed: int, grid: tuple = DEFAULT_GRID, ran_fraction: float = 0.8, spec: list | None = None) -> tuple[dict, list]:
    """(files: path -> bytes, truth lines) for one seed, grid, ran fraction and parsed spec."""
    files, lay = clean_tree(seed, grid, ran_fraction)
    truth = mutate(files, lay, seed, spec or [])
    return dict(sorted(files.items())), truth


def layout(seed: int, grid: tuple = DEFAULT_GRID, ran_fraction: float = 0.8) -> dict:
    """The clean tree's facts (study, grid values, cases, which ran): what a test or the notebook checks the recognizer against."""
    return clean_tree(seed, grid, ran_fraction)[1]


# ---- writing ---------------------------------------------------------------------------------------------------------------------------------------
def write_outputs(files: dict, truth: list, out: Path) -> None:
    """Write OUT/<path> for every file (OUT/study-<name>/...), OUT/paths.tsv and OUT/truth.jsonl. OUT must be absent or an empty directory."""
    out = Path(out)
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise SpecError(f"{out} exists and is not an empty directory")
    root = out
    root.mkdir(parents=True, exist_ok=True)
    for rel in sorted(files):
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(files[rel])
    (out / "paths.tsv").write_bytes("".join(f"{rel}\t{len(files[rel])}\n" for rel in sorted(files)).encode("utf-8"))
    (out / "truth.jsonl").write_bytes("".join(json.dumps(t, sort_keys=True, separators=(",", ":")) + "\n" for t in truth).encode("utf-8"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--grid", help="ExTxM: moduli x thicknesses x mesh levels (default 4x5x3)")
    ap.add_argument("--large", action="store_true", help=f"the grid {'x'.join(map(str, LARGE_GRID))} (about 600 cases)")
    ap.add_argument("--ran-fraction", type=float, default=0.8)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--mutations", type=Path, metavar="SPEC.yaml")
    a = ap.parse_args(argv)
    try:
        if a.large and a.grid:
            raise SpecError("--grid and --large are exclusive")
        grid = LARGE_GRID if a.large else (parse_grid(a.grid) if a.grid else DEFAULT_GRID)
        files, truth = generate(a.seed, grid, a.ran_fraction, load_spec(a.mutations))
        write_outputs(files, truth, a.out)
    except SpecError as exc:
        print(f"fea_sweep_gen: {exc}", file=sys.stderr)
        return 2
    print(f"fea_sweep_gen seed {a.seed}: {len(files)} files, {len(truth)} injected deviation(s) -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
