"""pyegeria's result notes are shown under every rendered result (node).

pyegeria 6.2.37+ returns words beside a result in `notes`, for example F8's "Showing the first 100: the
query stopped at its page size of 100; more may exist." The Portal used to drop them, so a capped DICT
tile or Run Report result read as the whole answer. static/egeria-not-measured.js now renders them
(EgeriaNotMeasured.resultNotesHtml): escaped, one per line, muted. Local Dashboards shows them under
every tile and in the drill-down drawer; the Explorer's Run Report panel under every result kind.

Uses the real results in fixtures/result_notes_pyegeria_replay_2026_11_11.json. Skipped when node is
not installed (the Portal container has none).
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MODULE = ROOT / "static" / "egeria-not-measured.js"
LD = (ROOT / "local-dashboards.html").read_text()
TE = (ROOT / "type-explorer.html").read_text()
FX = json.loads((HERE / "fixtures" / "result_notes_pyegeria_replay_2026_11_11.json").read_text())
F8 = "Showing the first 100: the query stopped at its page size of 100; more may exist."


def _node(js):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    out = subprocess.run([node, "-"], input=js, capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def _helper(expr, **data):
    return _node("var NM = require(" + json.dumps(str(MODULE)) + ");\n"
                 + "".join(f"var {k} = {json.dumps(v)};\n" for k, v in data.items())
                 + f"console.log(JSON.stringify({expr}));")


def _notes_divs(html):
    return re.findall(r'<div class="nm-result-note">(.*?)</div>', html)


def test_capped_result_renders_its_note():
    html = _helper("NM.resultNotesHtml(R)", R=FX["digital_products_dict"])
    assert html.startswith('<div class="nm-result-notes" data-nm="result-notes">')
    assert _notes_divs(html) == [F8]


def test_result_without_notes_renders_nothing():
    assert _helper("NM.resultNotesHtml(R)", R=FX["risk_register_dict"]) == ""
    assert _helper("[NM.resultNotesHtml(null), NM.resultNotesHtml({kind: 'json', notes: []}), "
                   "NM.resultNotesHtml({kind: 'json', notes: 'not a list'}), NM.resultNotesHtml({notes: [null, '  ']})]") == ["", "", "", ""]


def test_notes_are_escaped_one_per_line():
    r = {"kind": "json", "data": [], "notes": ["<script>alert(1)</script>", "a & b", "<img src=x onerror=alert(1)>"]}
    html = _helper("NM.resultNotesHtml(R)", R=r)
    assert "<script" not in html and "<img" not in html
    assert _notes_divs(html) == ["&lt;script&gt;alert(1)&lt;/script&gt;", "a &amp; b",
                                 "&lt;img src=x onerror=alert(1)&gt;"]


def test_text_result_does_not_repeat_its_own_line():
    r = {"kind": "text", "content": "| A |\n|---|\n| 1 |\n\n" + F8, "notes": [F8, "another note"]}
    assert _helper("NM.resultNotes(R)", R=r) == ["another note"]


# ── Local Dashboards: tiles and the drill-down drawer share renderExecResult ──

def _ld_render(result):
    grab = lambda pat: re.search(pat, LD, re.S).group(0)
    js = "\n".join([
        "var window = globalThis;",
        "window.EgeriaNotMeasured = require(" + json.dumps(str(MODULE)) + ");",
        "var EgeriaNotMeasured = window.EgeriaNotMeasured;",
        grab(r"function esc\(s\) \{.*?\n\}"),
        grab(r"var TABLE_WIDE_COLS = [^\n]*;"),
        grab(r"function tableWrapOpen\(nCols\) \{.*?\n\}"),
        grab(r"var TABLE_WRAP_CLOSE = [^\n]*;"),
        grab(r"var JSON_TABLE_MAX_ROWS = [^\n]*;"),
        grab(r"function hiddenColumnsNote\(hidden\) \{.*?\n\}"),
        grab(r"function renderJsonTableHtml\(data, unmeasured\) \{.*?\n\}\n"),
        "var _vegaSeq = 0;",
        "function _seriesValues() { return null; }",
        grab(r"function renderExecResult\(result, params\) \{.*?\n\}\n"),
        grab(r"function _renderExecResultBody\(result, params\) \{.*?\n\}\n"),
        f"console.log(JSON.stringify(renderExecResult({json.dumps(result)}, {{}}).html));",
    ])
    return _node(js)


def test_local_dashboards_tile_shows_the_note_under_the_table():
    html = _ld_render(FX["digital_products_dict"])
    assert html.count("<tr>") == 101                      # the 100 rows still render
    assert html.index("</table></div>") < html.index('class="nm-result-notes"')
    assert _notes_divs(html) == [F8]


def test_local_dashboards_tile_without_notes_is_unchanged():
    html = _ld_render(FX["risk_register_dict"])
    assert "nm-result-notes" not in html and html.count("<tr>") == 13


def test_every_local_dashboards_path_goes_through_render_exec_result():
    # report tiles, analytic tiles and the drill-down drawer
    assert len(re.findall(r"var out = renderExecResult\(result, (?:effParams|analyticParams|params)\)", LD)) == 3
    assert "EgeriaNotMeasured.resultNotesHtml(result)" in LD


# ── Egeria Explorer: Run Report panel ────────────────────────────────────────

def test_run_report_panel_wraps_every_result_kind_with_notes():
    body = TE[TE.index("var notesHtml = (NM && NM.resultNotesHtml)"):]
    body = body[:body.index("\n  return React.createElement('div', { className: 'detail'")]
    returns = re.findall(r"^\s*(?:if \([^)]*\) )?return (.*)$", body, re.M)
    real = [r for r in returns if not r.startswith("notesHtml ?")]   # skip withNotes' own body
    assert real and all(r.startswith("withNotes(") for r in real), real


def test_pages_load_the_new_module_version():
    for page in ("local-dashboards.html", "type-explorer.html", "governance-metrics.html"):
        assert "egeria-not-measured.js?v=2026-11-11a" in (ROOT / page).read_text(), page
