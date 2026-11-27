"""Phase 2 notebook 04a, A3: coco-workbooks/7. layout-semantics/04a simulation-case-layout.ipynb runs top to bottom from a checkout, with the
network blocked, in well under 2 minutes; its outputs are cleared; it holds no absolute or local path; it imports only the standard library,
PyYAML and this folder's code; the Phase 3/4 cells are marked and do nothing."""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

NB = Path(__file__).resolve().parents[2] / "coco-workbooks" / "7. layout-semantics" / "04a simulation-case-layout.ipynb"
RUNNER = r'''
import json, os, socket, sys
nb = sys.argv[1]
os.chdir(os.path.dirname(nb))
def no_net(*a, **k):
    raise OSError("network blocked")
socket.socket = no_net
socket.create_connection = no_net
g = {"__name__": "__main__"}
for c in json.load(open(nb, encoding="utf-8"))["cells"]:
    if c["cell_type"] == "code":
        exec(compile("".join(c["source"]), "<cell>", "exec"), g)
'''


def cells():
    return json.loads(NB.read_text(encoding="utf-8"))["cells"]


def test_outputs_are_cleared():
    for c in cells():
        if c["cell_type"] == "code":
            assert c["outputs"] == [] and c["execution_count"] is None


def test_no_absolute_or_local_path():
    text = NB.read_text(encoding="utf-8")
    for pat in (r"/Users/", r"/home/", r"/private/", r"/tmp/", r"[A-Za-z]:\\\\", r"~/", r"\.re-gate", r"localGit"):
        assert not re.search(pat, text), pat


def test_imports_only_the_standard_library_pyyaml_and_this_code():
    src = "\n".join("".join(c["source"]) for c in cells() if c["cell_type"] == "code")
    mods = set(re.findall(r"^\s*(?:from|import)\s+([A-Za-z_][\w]*)", src, re.M))
    assert mods <= {"json", "sys", "tempfile", "pathlib", "collections", "shutil", "fea_sweep_gen", "recognizer"}, mods


def test_phase34_cells_are_marked_and_do_nothing():
    code = ["".join(c["source"]) for c in cells() if c["cell_type"] == "code"]
    p34 = [c for c in code if c.startswith("# Phase 3/4 — not run")]
    assert len(p34) == 4
    for c in p34:
        assert "PHASE34" in c and "requests" not in c and "pyegeria" not in c
    assert any("lineage" in c for c in p34)
    assert any("## Phase 3/4 — not run" in "".join(c["source"]) for c in cells() if c["cell_type"] == "markdown")


def test_it_runs_top_to_bottom_without_network_in_under_two_minutes():
    t = time.time()
    r = subprocess.run([sys.executable, "-I", "-c", RUNNER, str(NB)], capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr[-2000:]
    assert time.time() - t < 120
    out = r.stdout
    assert "generic-relevance: 497 assets shown in 116 folders; 0 components" in out
    assert "1 sweep, 60 cases, 61% hidden output" in out and "60 of 60 cases have parameter tokens" in out
    assert "100% conformant; 0 findings" in out and "not-run: 12 of 60 cases" in out
    assert "10 injected, 10 new findings, equal: True" in out
    assert "parts: 7 new, 3 resolved, 57 unchanged" in out and "work folder removed" in out
