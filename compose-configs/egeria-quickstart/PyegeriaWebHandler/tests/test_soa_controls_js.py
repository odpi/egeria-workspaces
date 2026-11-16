"""Statements of Applicability: the controls table's pure sort/filter helpers (type-explorer.html), run under
node with egeria-shared-ui.js's listMatches. Standalone: needs no app imports. Skipped when node is not
installed (the container has none). Rows are shaped like soa_handler.py's control rows, with the
Coco workbook's values (coco-workbooks/4. keeping-safe/statement-of-applicability.md)."""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

_DIR = Path(__file__).resolve().parent.parent
HTML = (_DIR / "type-explorer.html").read_text()
SHARED = (_DIR / "static" / "egeria-shared-ui.js").read_text()


def _src():
    start = HTML.index("var SOA_STATUS_ORDER = ")
    end = HTML.index("function soaFiltersActive(f) {")
    end = HTML.index("\n}\n", end) + 3
    m = re.search(r"function listMatches\(query, parts\) \{.*?\n\}\n", SHARED, re.S)
    assert m, "listMatches not found in egeria-shared-ui.js"
    return m.group(0) + HTML[start:end]


def _run(expr):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    out = subprocess.run([node, "-e", _src() + f"\nconsole.log(JSON.stringify({expr}));"],
                         capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def _row(label, applicable=True, status="", **kw):
    return {"label": label, "displayName": kw.pop("name", "Control " + label), "isApplicable": applicable,
            "implementationStatus": status, "reviewDate": kw.pop("reviewDate", ""), **kw}


ROWS = [
    _row("A.8.30", False, justification="We do not outsource development."),
    _row("A.5.12", True, "PARTIALLY_IMPLEMENTED", inclusionReasons=["Risk Treatment"]),
    _row("A.5.9", True, "PARTIALLY_IMPLEMENTED", reviewDate="2026-12-01T00:00:00.000+00:00"),
    _row("A.8.8", True, "PLANNED", implementationDescription="Patch window planned"),
    _row("A.5.1", True, "IMPLEMENTED", inclusionReasons=["Best Practice", "Business Requirement"],
         reviewDate="2026-11-16T00:00:00.000+00:00"),
    _row("A.6.3", None, ""),                       # isApplicable unset, no status
]
R = json.dumps(ROWS)


def _labels(expr):
    return [r["label"] for r in _run(expr)]


def test_control_numbers_sort_numerically_both_ways():
    asc = ["A.5.1", "A.5.9", "A.5.12", "A.6.3", "A.8.8", "A.8.30"]
    assert _labels(f"soaSortRows({R}, 'label', 'asc')") == asc
    assert _labels(f"soaSortRows({R}, 'label', 'desc')") == asc[::-1]


def test_compare_labels_handles_plain_and_mixed_numbers():
    assert _run("['5.12','5.9','10.1','8.30','5.1'].sort(soaCompareLabels)") == ["5.1", "5.9", "5.12", "8.30", "10.1"]


def test_status_sorts_in_implementation_order_not_alphabetically():
    assert _labels(f"soaSortRows({R}, 'status', 'asc')") == ["A.8.8", "A.5.12", "A.5.9", "A.5.1", "A.6.3", "A.8.30"]


def test_status_buckets_keep_not_recorded_and_not_applicable_apart():
    assert _run(f"{R}.map(soaStatusBucket)") == [
        "NOT_APPLICABLE", "PARTIALLY_IMPLEMENTED", "PARTIALLY_IMPLEMENTED", "PLANNED", "IMPLEMENTED", "NOT_RECORDED"]


def test_review_date_sorts_as_a_date_and_missing_dates_stay_last():
    assert _labels(f"soaSortRows({R}, 'reviewDate', 'asc')")[:2] == ["A.5.1", "A.5.9"]
    assert _labels(f"soaSortRows({R}, 'reviewDate', 'desc')")[:2] == ["A.5.9", "A.5.1"]


def test_filter_by_status_applicable_reason_and_text():
    assert _labels(f"soaFilterRows({R}, {{statuses: ['PARTIALLY_IMPLEMENTED']}})") == ["A.5.12", "A.5.9"]
    assert _labels(f"soaFilterRows({R}, {{applicable: ['no']}})") == ["A.8.30"]
    assert len(_run(f"soaFilterRows({R}, {{applicable: ['yes']}})")) == 5      # unset counts as applicable
    assert _labels(f"soaFilterRows({R}, {{reasons: ['Best Practice', 'Risk Treatment']}})") == ["A.5.12", "A.5.1"]
    assert _labels(f"soaFilterRows({R}, {{text: 'outsource'}})") == ["A.8.30"]          # justification
    assert _labels(f"soaFilterRows({R}, {{text: 'patch planned'}})") == ["A.8.8"]       # implementation, all words
    assert _labels(f"soaFilterRows({R}, {{text: 'A.5.1'}})") == ["A.5.12", "A.5.1"]     # control number
    assert _labels(f"soaFilterRows({R}, {{statuses: ['NOT_RECORDED']}})") == ["A.6.3"]


def test_filters_combine_and_empty_filters_keep_everything():
    assert _labels(f"soaFilterRows({R}, {{statuses: ['PARTIALLY_IMPLEMENTED'], text: '5.9'}})") == ["A.5.9"]
    assert len(_run(f"soaFilterRows({R}, {{statuses: [], applicable: [], reasons: [], text: ''}})")) == len(ROWS)
    assert _run("[soaFiltersActive({statuses: [], applicable: [], reasons: [], text: '  '}), "
                "soaFiltersActive({statuses: ['PLANNED'], applicable: [], reasons: [], text: ''})]") == [False, True]


def test_view_wiring():
    # header label is a sort button inside a plain <th> so egeria-resize.js keeps the edge drag
    assert "'aria-sort': aria" in HTML
    assert "React.createElement(SoaSummary, { summary: detail.summary, filters: filters, onPick: setFilters })" in HTML
    assert "'No controls match these filters ('" in HTML
    assert "'No controls are linked to this statement of applicability yet.'" in HTML
    assert "'Showing ' + shown.length + ' of ' + controls.length" in HTML
