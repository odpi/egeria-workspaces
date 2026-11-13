"""Report Specs -> Run offers TABLE for a spec whose format sets say ALL (BRIEF-CDO-SHEET-TABLE-2026-11-12).

pyegeria runs any format no set names through the ALL set, so Risk-DrE-Basic (sets "ALL" and "LIST") runs as
TABLE; the Run dropdown used to offer only ALL and LIST. rsRunFormats() in type-explorer.html adds the formats
ALL covers. The JS part runs under node (skipped without it).
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
TE = (ROOT / "type-explorer.html").read_text()


def _formats(types):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    src = re.search(r"var RS_ALL_COVERS = .*?\nfunction rsRunFormats\(spec\) \{.*?\n\}", TE, re.S).group(0)
    js = src + f"\nconsole.log(JSON.stringify(rsRunFormats({json.dumps({'output_types': types} if types is not None else None)})));"
    out = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_all_adds_table_and_the_formats_it_covers():
    assert _formats(["ALL", "LIST"]) == ["ALL", "LIST", "TABLE", "DICT", "REPORT", "MD", "FORM", "JSON"]


@pytest.mark.parametrize("types,expected", [
    (["DICT", "TABLE"], ["DICT", "TABLE"]),            # no ALL: only what the spec names
    (["BAR"], ["BAR"]),
    ([], ["DICT"]), (None, ["DICT"]),                   # unchanged fallback
])
def test_without_all_nothing_is_added(types, expected):
    assert _formats(types) == expected


def test_charts_and_document_are_never_added_by_all():
    assert not {"BAR", "PIE", "SERIES", "DOCUMENT", "MERMAID"} & set(_formats(["ALL"]))


def test_the_dropdown_uses_it():
    assert "}, rsRunFormats(spec).map(function(t) {" in TE
    assert "(spec.output_types && spec.output_types.length ? spec.output_types : ['DICT']).map" not in TE


@pytest.mark.parametrize("name", ["Risk-DrE-Basic", "Governance-Metric-DrE-Basic", "Project-DrE-Basic"])
def test_the_cdo_register_specs_have_all(name):
    """The three CDO registers (now TABLE tiles) name ALL, so the Run dropdown offers TABLE for them."""
    pytest.importorskip("pyegeria")
    import report_specs_handler as rsh
    fs = rsh._get_registry().get(name)
    assert fs is not None
    assert "ALL" in rsh._serialize(name, fs)["output_types"]
