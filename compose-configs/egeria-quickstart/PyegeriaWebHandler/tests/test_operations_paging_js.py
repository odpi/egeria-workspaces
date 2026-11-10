"""egeria-operations.html: the engine-action count words and the catalog-target heading, run under node
(skips when node is not installed; the container has none). Wiring checks run everywhere."""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

HTML = (Path(__file__).resolve().parent.parent / "egeria-operations.html").read_text()


def _call(fn, *args):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    m = re.search(r"function " + fn + r"\(.*?\n\}\n", HTML, re.S)
    assert m, f"{fn} not found"
    js = m.group(0) + f"console.log(JSON.stringify({fn}(...{json.dumps(list(args))})));"
    out = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_a_page_is_never_called_the_total():
    assert _call("opsActionsCountLabel", 200, {"more": True}) == "newest 200, more available"
    assert _call("opsActionsCountLabel", 200, {"more": True, "repositoryCount": 21908}) == "newest 200 of 21,908 in the repository"
    assert _call("opsActionsCountLabel", 200, {"more": None}) == "newest 200 (could not check for more)"


def test_an_exact_total_is_said_as_such():
    assert _call("opsActionsCountLabel", 50, {"more": False, "total": 50}) == "all 50"
    assert _call("opsActionsCountLabel", 200, {"more": True, "total": 450}) == "newest 200 of 450"


def test_catalog_target_heading_unknown_partial_exact():
    assert _call("opsTargetsHeading", {"catalogTargets": [], "catalogTargetsError": "could not be read: timed out after 20 s"}) \
        == "Catalog Targets (could not be read)"
    assert _call("opsTargetsHeading", {"catalogTargets": [1] * 3, "catalogTargetsLowerBound": 1000}) == "Catalog Targets (1000+)"
    assert _call("opsTargetsHeading", {"catalogTargets": [], "catalogTargetCount": 0}) == "Catalog Targets (0)"
    assert _call("opsTargetsHeading", {"catalogTargets": [1, 2]}) == "Catalog Targets (2)"


def test_wiring():
    assert "opsActionsCountLabel(rows.length, pageInfo)" in HTML
    assert "'/api/operations/engine-actions?start=0&page_size=' + EA_PAGE" in HTML
    assert "'/api/operations/engine-actions?start=' + pageInfo.nextStart" in HTML
    assert "'Load more'" in HTML
    assert "sectionHdr(opsTargetsHeading(sel))" in HTML
    assert "el(CatalogTargetsSection, { row: sel })" in HTML
    assert 'This is not "none": they are unknown.' in HTML
