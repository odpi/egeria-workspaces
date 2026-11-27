"""Phase 2 notebook 04a, A0: the seeded CalculiX-shaped sweep generator (samples/fea_sweep_gen.py). Synthetic only.
Determinism, the clean tree, and one test per mutation class that injects ONLY that class. (Detection by the fea-sweep profile is A1/A2.)"""
import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

SAMPLES = Path(__file__).resolve().parent.parent / "samples"
sys.path.insert(0, str(SAMPLES))
import fea_sweep_gen as g  # noqa: E402


def tree_digest(out: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(x for x in out.rglob("*") if x.is_file()):
        h.update(str(p.relative_to(out)).encode() + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()


def one(cls, seed=1, n=1, **kw):
    spec = g.parse_spec({"mutations": [{"class": cls, **kw}]})
    clean, _ = g.generate(seed)
    files, truth = g.generate(seed, spec=spec)
    assert len(truth) == n, truth
    for t in truth:
        assert t["class"] == cls and (t["kind"], t["status"]) == g.kind_status(cls, t.get("variant"))
        assert set(t) <= {"path", "kind", "status", "class", "variant", "rule"} and {"path", "kind", "status", "class"} <= set(t)
        assert ("variant" in t) == (cls in g.VARIANTS) and ("rule" in t) == (cls == "off-grammar-case-name")
    return clean, files, truth[0] if n == 1 else truth


def dirs_of(files):
    return {p.rsplit("/", 1)[0] for p in files}


def cases_of(files):
    return sorted({p.split("/")[2] for p in files if p.split("/")[1] == "cases" and p.count("/") >= 3})


# ---- determinism ---------------------------------------------------------------------------------------------------------------------------------
ALL_SPEC = {"mutations": [{"class": c} for c in g.CLASSES]}


@pytest.mark.parametrize("spec", [None, ALL_SPEC])
def test_same_seed_and_spec_give_a_byte_identical_tree_and_truth(tmp_path, spec):
    sp = None
    if spec is not None:
        import yaml
        sp = tmp_path / "spec.yaml"
        sp.write_text(yaml.safe_dump(spec))
    digests = []
    for n in (1, 2):
        out = tmp_path / f"run{n}"
        args = [sys.executable, str(SAMPLES / "fea_sweep_gen.py"), "--seed", "3", "--out", str(out)]
        subprocess.run(args + (["--mutations", str(sp)] if sp else []), check=True, capture_output=True)
        digests.append(tree_digest(out))
    assert digests[0] == digests[1]
    truth = (tmp_path / "run1" / "truth.jsonl").read_text()
    assert (truth == "") == (spec is None)


def test_different_seeds_give_different_trees():
    assert g.generate(1)[0] != g.generate(2)[0]


def test_spec_order_does_not_matter():
    a = g.parse_spec({"mutations": [{"class": "stray-deck"}, {"class": "missing-input-deck"}]})
    b = g.parse_spec({"mutations": [{"class": "missing-input-deck"}, {"class": "stray-deck"}]})
    assert g.generate(2, spec=a) == g.generate(2, spec=b)


# ---- the clean tree ------------------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("seed", [1, 2, 3])
def test_clean_tree_has_one_case_per_grid_point_and_the_layout(seed):
    files, truth = g.generate(seed)
    lay = g.layout(seed)
    assert truth == []
    s = lay["study"]
    assert all(p.startswith(s + "/") for p in files)
    assert len(lay["E"]) == 4 and len(lay["t"]) == 5 and lay["mesh"] == ["coarse", "medium", "fine"]
    assert cases_of(files) == sorted(lay["cases"]) and len(lay["cases"]) == 60
    assert len(lay["ran"]) == 48                                          # round(0.8 * 60)
    for f in ("README.md", "sweep.yaml", "templates/base.inp", "post/sweep-summary.csv", "scratch/try1.inp", "README.md~"):
        assert f"{s}/{f}" in files
    for c in lay["cases"]:
        d = f"{s}/cases/{c}/"
        assert d + "job.inp" in files and d + "run.log" in files
        ran = c in lay["ran"]
        assert all((d + f in files) == ran for f in g.RAN_FILES)
        assert (f"{s}/post/{c}/summary.csv" in files) == ran
        if not ran:
            assert not any(p.startswith(d) and p.rsplit("/", 1)[1] in ("job.12d", "job.rout") for p in files)
    assert any(p.endswith("/job.12d") for p in files) and any(p.endswith("/job.rout") for p in files)
    assert any(p.endswith("/job.inp.bak") for p in files)
    assert {p.split("/")[1] for p in files} == {"README.md", "README.md~", "sweep.yaml", "templates", "materials", "mesh", "cases", "post", "validation", "scratch"}
    for p in files:
        if p.startswith(f"{s}/mesh/"):
            part, _, level = p.rsplit("/", 1)[1][:-len(".msh")].rpartition("_")
            assert part in lay["parts"] and level in lay["mesh"]


def test_clean_case_names_follow_the_grammar_and_tokens_round_trip():
    lay = g.layout(1)
    for c in lay["cases"]:
        k = g.parse_case(c)
        assert k is not None and g.case_id(int(k["E"]), float(k["t"].replace("p", ".")), k["mesh"]) == c
    assert g.fmt_t(2.0) == "2p0" and g.fmt_t(0.5) == "0p5" and g.fmt_t(10.0) == "10p0"
    assert g.parse_case("case_E210_t2_mesh-fine") is None and g.parse_case("Case_E210_t2p0_mesh-fine") is None


def test_every_file_is_a_one_line_placeholder():
    files, _ = g.generate(1)
    for p, b in files.items():
        assert b.count(b"\n") == 1 and b.endswith(b"\n"), p
        assert b"placeholder" in b


def test_grid_and_large():
    assert g.parse_grid("4x5x3") == (4, 5, 3)
    files, _ = g.generate(1, grid=(2, 3, 1))
    assert len(cases_of(files)) == 6 and all(c.endswith("_mesh-coarse") for c in cases_of(files))
    lay = g.layout(1, g.LARGE_GRID)
    assert len(lay["cases"]) == 600
    for bad in ("4x5", "0x5x3", "4x5x4", "21x5x3", "axbxc"):
        with pytest.raises(g.SpecError):
            g.parse_grid(bad)


@pytest.mark.parametrize("frac,ran", [(0.0, 0), (1.0, 60), (0.5, 30)])
def test_ran_fraction(frac, ran):
    assert len(g.layout(2, ran_fraction=frac)["ran"]) == ran


# ---- one test per mutation class -----------------------------------------------------------------------------------------------------------------
def test_missing_input_deck():
    clean, files, t = one("missing-input-deck")
    case = t["path"].rsplit("/", 1)[0]
    assert t["path"].endswith("/job.inp") and t["path"] in clean and t["path"] not in files
    assert case + "/run.log" in files and case + "/job.frd" not in files            # a case that did not run; its folder stays
    assert set(clean) - set(files) == {t["path"]} and set(files) <= set(clean)


def test_results_without_deck():
    clean, files, t = one("results-without-deck")
    case = t["path"].rsplit("/", 1)[0]
    assert t["path"].endswith("/job.inp") and t["path"] not in files and case + "/job.frd" in files
    assert set(clean) - set(files) == {t["path"]}


def test_missing_deck_and_results_without_deck_never_share_a_case():
    for seed in range(1, 6):
        _, truth = g.generate(seed, spec=g.parse_spec({"mutations": [{"class": "missing-input-deck", "count": 3}, {"class": "results-without-deck", "count": 3}]}))
        assert len({t["path"] for t in truth}) == 6


@pytest.mark.parametrize("variant,expect,rule", [("no-decimal", r"case_E[0-9]+_t[0-9]+_mesh-[a-z]+", "PG-case"),
                                                 ("wrong-case", r"Case_E[0-9]+_t[0-9]+p[0-9]+_mesh-[a-z]+", "PG-case"),
                                                 ("stray-suffix", r"case_E[0-9]+_t[0-9]+p[0-9]+_(final_v2|copy|old)", "PG-case-any")])
def test_off_grammar_case_name(variant, expect, rule):
    import re
    clean, files, t = one("off-grammar-case-name", variant=variant)
    assert (t["kind"], t["status"], t["variant"], t["rule"]) == ("naming", "misnamed", variant, rule)
    name = t["path"].rsplit("/", 1)[1]
    assert t["path"].split("/")[1] == "cases" and re.fullmatch(expect, name) and g.parse_case(name) is None
    assert t["path"] + "/job.inp" in files
    assert len(cases_of(files)) == 60                                     # renamed, not added
    gone = set(cases_of(clean)) - set(cases_of(files))
    assert len(gone) == 1 and not any(p.split("/")[1:3] == ["post", next(iter(gone))] for p in files)   # its post/ folder went with it


@pytest.mark.parametrize("variant", ["E", "t"])
def test_off_grid_value(variant):
    clean, files, t = one("off-grid-value", variant=variant)
    k = g.parse_case(t["path"].rsplit("/", 1)[1])
    lay = g.layout(1)
    assert (t["kind"], t["status"]) == ("naming", "off-grid") and k is not None
    if variant == "E":
        assert k["E"] == "999" and 999 not in lay["E"]
    else:
        assert k["t"] == "9p9" and 9.9 not in lay["t"]
    assert len(cases_of(files)) == 60


@pytest.mark.parametrize("variant", ["E", "t"])
def test_duplicate_combination(variant):
    clean, files, t = one("duplicate-combination", variant=variant)
    assert (t["kind"], t["status"]) == ("structure", "duplicate")
    new = sorted(set(cases_of(files)) - set(cases_of(clean)))
    assert len(new) == 1 and len(cases_of(files)) == 61
    k = g.parse_case(new[0])
    orig = g.case_id(int(k["E"]), float(k["t"].replace("p", ".")), k["mesh"])
    assert orig in cases_of(files) and orig != new[0]
    assert t["path"].rsplit("/", 1)[1] == max(orig, new[0])               # the second of the pair in sorted path order
    s = g.layout(1)["study"]
    names = lambda c: sorted(p.rsplit("/", 1)[1] for p in files if p.startswith(f"{s}/cases/{c}/"))
    assert names(orig) == names(new[0])


def test_stray_deck():
    clean, files, t = one("stray-deck")
    assert (t["kind"], t["status"]) == ("structure", "unexpected")
    assert t["path"].split("/")[1:2] == ["cases"] and t["path"].count("/") == 2 and t["path"].endswith(".inp")
    assert set(files) - set(clean) == {t["path"]}


@pytest.mark.parametrize("name,rule", [("case_E210_t2_mesh-fine", "PG-case"), ("CASE_e210_T2P0_MESH-FINE", "PG-case"), ("case_E210_t2p0_final_v2", "PG-case-any"),
                                       ("case_E210_t2p0_mesh-", "PG-case-any"), ("case_E_t2p0_mesh-fine", "PG-case-any"), ("case_Ex_ty_mesh-z", "PG-case"), ("case_Ex_t_mesh-y", "PG-case-any"),
                                       ("xcase_E210_t2p0_mesh-fine", "PG-case-any")])
def test_expected_rule_follows_the_case_shape_including_the_boundary(name, rule):
    # the boundary: each relaxed token needs at least one character (case_E210_t2p0_mesh- and case_E_t2p0_... are not shaped, nor is case_Ex_t_mesh-y; case_Ex_ty_mesh-z is)
    assert g.expected_case_rule(name) == rule


def test_bad_mesh_level_in_a_case_name():
    clean, files, t = one("bad-mesh-level")
    k = g.parse_case(t["path"].rsplit("/", 1)[1])
    assert (t["kind"], t["status"]) == ("naming", "off-grid") and k["mesh"] in g.BAD_MESH
    assert len(cases_of(files)) == 60
    assert sorted(p for p in files if "/mesh/" in p) == sorted(p for p in clean if "/mesh/" in p)       # mesh/ file names are never mutated


def test_unexpected_top_level_folder():
    clean, files, t = one("unexpected-top-level-folder")
    assert (t["kind"], t["status"]) == ("structure", "unexpected")
    assert t["path"].count("/") == 1 and t["path"].split("/")[1] in g.UNEXPECTED_DIRS
    assert t["path"] in dirs_of(files) and t["path"] not in dirs_of(clean)


def test_orphan_post():
    clean, files, t = one("orphan-post")
    assert (t["kind"], t["status"]) == ("structure", "unexpected")
    s, post, case = t["path"].split("/")
    assert post == "post" and case not in cases_of(files) and case in cases_of(clean)
    assert any(p.startswith(t["path"] + "/") for p in files)
    assert set(files) <= set(clean)


def test_every_class_together_gives_one_truth_line_each_but_the_variants():
    files, truth = g.generate(1, spec=g.parse_spec(ALL_SPEC))
    assert sorted({t["class"] for t in truth}) == sorted(g.CLASSES)
    assert len(truth) == len(g.CLASSES) and len({t["path"] for t in truth}) == len(truth)


# ---- the spec ------------------------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("doc", [[], {"mutations": [{"class": "nope"}]}, {"mutations": [{"class": "stray-deck", "file": "x"}]},
                                 {"mutations": [{"class": "stray-deck", "variant": "x"}]}, {"mutations": [{"class": "stray-deck", "count": 0}]},
                                 {"other": 1}])
def test_bad_specs_are_refused(doc):
    with pytest.raises(g.SpecError):
        g.parse_spec(doc)


def test_too_many_mutations_for_the_cases_left_are_refused():
    with pytest.raises(g.SpecError):
        g.generate(1, grid=(1, 1, 1), spec=g.parse_spec({"mutations": [{"class": "orphan-post", "count": 2}]}))
    with pytest.raises(g.SpecError):
        g.generate(1, ran_fraction=1.0, spec=g.parse_spec({"mutations": [{"class": "missing-input-deck"}]}))     # no case that did not run
