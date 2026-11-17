"""Overview honest-data P3s (egeria-overview.html), the pure tile-text helpers run under node.
Standalone: needs no app imports. The node tests skip when node is not installed (the container has
none); the wiring checks run everywhere."""
import json, re, shutil, subprocess
from pathlib import Path

import pytest

HTML = (Path(__file__).resolve().parent.parent / "egeria-overview.html").read_text()


def _call(fn, *args):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    m = re.search(r"function " + fn + r"\(.*?\n\}\n", HTML, re.S)
    assert m, f"{fn} not found in egeria-overview.html"
    js = m.group(0) + f"console.log(JSON.stringify({fn}(...{json.dumps(list(args))})));"
    out = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_governed_small_share_shows_its_real_value_not_lt1():
    assert _call("overviewGovernedPct", 3, 1000, False) == "0.3%"
    assert _call("overviewGovernedPct", 2, 10000, False) == "0.02%"
    assert _call("overviewGovernedPct", 0, 1000, False) == "0%"          # zero is zero, not "<1%"
    assert _call("overviewGovernedPct", 420, 1000, False) == "42%"
    assert _call("overviewGovernedPct", 420, 1000, True) == "≥42%"
    assert _call("overviewGovernedPct", None, 1000, False) is None       # not measured is never 0
    assert _call("overviewGovernedPct", 5, 0, False) is None
    assert _call("overviewGovernedPct", 1001, 1000, False) is None       # disagreeing reads: no share


def test_pipeline_capped_zero_is_not_measured_not_zero():
    assert _call("overviewPipelineCount", {"failed": 0, "total": 500, "capped": True}) == "—"
    assert _call("overviewPipelineCount", {"failed": 7, "total": 500, "capped": True}) == "≥7"
    assert _call("overviewPipelineCount", {"failed": 0, "total": 12, "capped": False}) == "0"
    assert _call("overviewPipelineCount", None) == "—"


def test_tiles_use_the_helpers_and_say_why():
    assert "pcnt.textContent = overviewPipelineCount(ph);" in HTML
    assert "store.governedPct = overviewGovernedPct(d.governedCount, d.assetTotal, d.governedCapped);" in HTML
    assert "'<1'" not in HTML
    assert "else if (ph.capped && !ph.failed) pdesc.textContent = 'Not measured:" in HTML
    # a stale "—" carries the reason (backend staleAssetNote, else the generic not-measured words)
    assert "if (d.staleAssetCount == null) {" in HTML and "d.staleAssetNote ||" in HTML
