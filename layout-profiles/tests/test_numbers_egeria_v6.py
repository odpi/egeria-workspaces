"""The numbers check: the recognizer's class counts on the egeria-v6 tree.

Needs a path list of an egeria-v6 working tree (names and sizes only, made by recognizer/listpaths.py); it is not in the repository.
Set LAYOUT_EGERIA_V6_PATHS to its location; the test skips if the variable is unset or the file is missing.

Two layers. (1) The rules that Phase 0 counted and that no later change touched (vendored installs, event files, logs, .git, dumps, heap dumps, tool caches,
backups) must still equal the Phase 0 census EXACTLY. (2) The per-rule table of the current profile (egeria-workspace 0.4.0, after the M5 hiding rules, the
M5b tightenings and the M5c build-layout and runtime-volumes rules) must match, and every file is in exactly one class."""
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
def test_class_counts_equal_the_phase0_census_and_the_current_rule_table(tmp_path):
    c = Recognizer(load_profile("egeria-workspace", HERE.parent / "profiles")).run(LIST, tmp_path)
    n = lambda *rules: sum(c["by_rule"].get(r, {}).get("files", 0) for r in rules)
    assert c["total_files"] == CENSUS["total_files"]
    untouched = {"vendored_installs": n("R-vend-installed"), "runtime_events": n("R-run-openlineage-event"), "logs": n("R-run-log"), "vcs_internal": n("R-vcs-git"),
                 "backups": n("R-backup-dir", "R-backup-file"), "heap_dumps": n("R-run-heap-dump")}
    assert untouched["runtime_events"] == CENSUS["runtime_events"] and untouched["logs"] == CENSUS["logs"] and untouched["vcs_internal"] == CENSUS["vcs_internal"]
    assert untouched["backups"] == CENSUS["backups"] and untouched["heap_dumps"] == CENSUS["heap_dumps"]
    assert untouched["vendored_installs"] + n("R-gen-tool-cache") == 1083855 + 2798          # the Phase 0 "vendored or build" figure also held the build folders (below)
    table = {k: v for k, v in CENSUS["m5c_rules_egeria_workspace_0_4_0"].items() if k != "note"}
    got = {k: v["files"] for k, v in c["by_rule"].items() if k != "(none)"}
    got["unclassified"] = c["by_role"]["unclassified"]["files"]
    assert got == table
    assert sum(v["files"] for v in c["by_rule"].values()) == c["total_files"]                  # every file is in exactly one class
