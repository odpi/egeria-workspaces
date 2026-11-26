"""The numbers check: the recognizer's class counts on the egeria-v6 tree must equal the Phase 0 census EXACTLY.

Needs a path list of an egeria-v6 working tree (names and sizes only, made by recognizer/listpaths.py); it is not in the repository.
Set LAYOUT_EGERIA_V6_PATHS to its location; the test skips if the variable is unset or the file is missing."""
import json
import os
from pathlib import Path

import pytest

from recognizer.layout_profile import load_profile
from recognizer.recognize import Recognizer

HERE = Path(__file__).resolve().parent
LIST = Path(os.environ["LAYOUT_EGERIA_V6_PATHS"]).expanduser() if os.environ.get("LAYOUT_EGERIA_V6_PATHS") else None
CENSUS = json.loads((HERE / "census_egeria_v6.json").read_text())


@pytest.mark.skipif(LIST is None or not LIST.is_file(), reason="LAYOUT_EGERIA_V6_PATHS is unset or not a file (make a list with recognizer/listpaths.py)")
def test_class_counts_equal_the_phase0_census(tmp_path):
    c = Recognizer(load_profile("egeria-workspace", HERE.parent / "profiles")).run(LIST, tmp_path)
    n = lambda *rules: sum(c["by_rule"].get(r, {}).get("files", 0) for r in rules)
    got = {
        "total_files": c["total_files"],
        "vendored_or_build": n("R-vend-installed", "R-gen-build-output", "R-gen-tool-cache"),
        "runtime_events": n("R-run-openlineage-event"),
        "logs": n("R-run-log"),
        "vcs_internal": n("R-vcs-git"),
        "backups": n("R-backup-dir", "R-backup-file"),
        "heap_dumps": n("R-run-heap-dump"),
        "worktree_copy_residual": n("R-copy-worktree-name"),
        "residual": c["by_role"]["unclassified"]["files"],
    }
    want = {k: v for k, v in CENSUS.items() if k != "source"}
    assert got == want
    assert sum(v for k, v in got.items() if k != "total_files") == got["total_files"]      # every file is in exactly one class
