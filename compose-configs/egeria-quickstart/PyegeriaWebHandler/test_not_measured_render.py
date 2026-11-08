# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Offline tests: report-spec results that say "not measured" never render as an answer.

pyegeria's exec_report_spec (behind POST /api/report-specs/execute) returns
`kind:"absent"` for a value that is not established (ISSUE-171, already in 6.2.26),
and since odpi/egeria-python #555 also for a scalar or chart whose count was not
measured; and it adds `unmeasured: [{count, reason, at_least}]` to table/json
results whose unmeasured cells are null. These tests run the REAL page code —
static/egeria-not-measured.js, local-dashboards.html's renderExecResult and
governance-metrics.html's renderRunOutput, pulled out of the HTML by name — in
node, against recorded output shapes from both pyegeria 6.2.26 and #555, and
assert on the HTML a reader would see. The 6.2.26 shapes are also compared with
the same functions as they are on the base commit, so "renders exactly as now"
is checked, not assumed.

Needs only node (no pyegeria, no fastapi, no Egeria):

    python -m pytest test_not_measured_render.py -q
"""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="node is not installed")

# ── recorded output shapes ────────────────────────────────────────────────────

# pyegeria 6.2.26 (deployed): no `unmeasured` key anywhere.
OLD_SCALAR = {"kind": "json", "data": 500}
OLD_ZERO = {"kind": "json", "data": 0}
OLD_TABLE = {"kind": "json", "data": [{"type": "Asset", "count": 12, "latest": None},
                                      {"type": "Process", "count": 3, "latest": "2026-11-01"}]}
OLD_EMPTY = {"kind": "empty"}
OLD_CHART = {"kind": "json", "data": {"$schema": "https://vega.github.io/schema/vega-lite/v5.json",
                                      "mark": "bar", "data": {"values": []}}}
# ISSUE-171 kind:"absent", which 6.2.26 already emits (no unmeasured notes).
OLD_ABSENT = {
    "kind": "absent", "content": "Not measured: the survey has not run yet.",
    "absence": {"state": "not_measured", "sentence": "Not measured: the survey has not run yet.",
                "reason": "the survey has not run yet", "declared": False},
    "envelope": {"state": "not_established", "reason": "the survey has not run yet",
                 "subtitle": "not established · the survey has not run yet"},
}
OLD_NOT_APPLICABLE = {
    "kind": "absent", "content": "Does not apply: no zones are defined.",
    "absence": {"state": "not_applicable", "sentence": "Does not apply: no zones are defined.",
                "reason": "no zones are defined", "declared": False},
}

# odpi/egeria-python #555 (5ac4bb54): `_absent_output` with notes, and json/empty with notes.
_NOTE = {"count": "Asset (viewer scope)",
         "reason": "the native count timed out; the find fallback stopped at its page cap of 500",
         "at_least": 500}
NEW_ABSENT_SCALAR = {
    "kind": "absent",
    "content": ("Not measured: Asset (viewer scope): the native count timed out; the find fallback "
                "stopped at its page cap of 500. Not measured: Asset (viewer scope): the native count "
                "timed out; the find fallback stopped at its page cap of 500."),
    "absence": {"state": "not_measured", "sentence": "Not measured: Asset (viewer scope): ...",
                "reason": "Asset (viewer scope): ...", "declared": False},
    "unmeasured": [_NOTE],
    "envelope": {"state": "not_established", "reason": "Asset (viewer scope): ...",
                 "subtitle": "not established · Asset (viewer scope): ..."},
}
NEW_ABSENT_CHART = {
    "kind": "absent", "content": "Not measured. Not measured: Process: the count failed: 504.",
    "absence": {"state": "not_measured", "sentence": "Not measured.", "reason": "", "declared": True},
    "detail": [{"type": "Asset", "count": 41}, {"type": "Process", "count": None}],
    "unmeasured": [{"count": "Process", "reason": "the count failed: 504", "at_least": None}],
}
NEW_TABLE = {
    "kind": "json",
    "data": [{"type": "Asset", "count": None, "byZone": {"public": None, "private": 4}},
             {"type": "Glossary", "count": 7, "byZone": {"public": 7}}],
    "unmeasured": [_NOTE],
}
NEW_EMPTY = {"kind": "empty", "unmeasured": [{"count": "Process", "reason": "timed out", "at_least": None}]}

# Recorded verbatim from pyegeria at odpi/egeria-python 5ac4bb54 (#555): format_set_executor's
# _absent_output / json-with-notes, driven by overview_metrics counts over a find fallback that
# stopped at its 500 cap (no Egeria; see the PR body for the script).
REAL_555_SCALAR = {"kind": "absent", "content": "The elements were not counted: the count query failed or timed out, or the server could not answer it in the population asked for. A fallback that stopped at its page cap is a lower bound, never a total. Not measured: Asset: no native count is available, and the find fallback stopped at its 500-element page cap, so there are at least 500.", "absence": {"state": "not_measured", "sentence": "The elements were not counted: the count query failed or timed out, or the server could not answer it in the population asked for. A fallback that stopped at its page cap is a lower bound, never a total.", "reason": "Asset: no native count is available, and the find fallback stopped at its 500-element page cap, so there are at least 500", "declared": True}, "unmeasured": [{"count": "Asset", "reason": "no native count is available, and the find fallback stopped at its 500-element page cap, so there are at least 500", "at_least": 500}], "envelope": {"state": "not_established", "reason": "Asset: no native count is available, and the find fallback stopped at its 500-element page cap, so there are at least 500", "subtitle": "not established · Asset: no native count is available, and the find fallback stopped at its 500-element page cap, so there are at least 500"}}
REAL_555_TABLE = {"kind": "json", "data": {"total": None, "byType": [{"label": "Assets", "type": "Asset", "count": None}, {"label": "Terms", "type": "GlossaryTerm", "count": 12}]}, "unmeasured": [{"count": "Asset", "reason": "no native count is available, and the find fallback stopped at its 500-element page cap, so there are at least 500", "at_least": 500}]}

# ── harness ───────────────────────────────────────────────────────────────────


def _function_source(text: str, name: str) -> str:
    """The source of `function name(...) {...}` in a page's inline script, by brace
    matching that skips string literals and // comments."""
    start = text.index(f"function {name}(")
    line = text[start:text.index("\n", start)].rstrip()
    if line.endswith("}"):  # a one-line function (its regex literal may hold quotes)
        return line
    i, parens = text.index("(", start), 0
    while True:  # past the parameter list, which may destructure ({ a, b })
        parens += {"(": 1, ")": -1}.get(text[i], 0)
        i += 1
        if parens == 0:
            break
    i = text.index("{", i)
    depth, quote = 0, None
    while i < len(text):
        c = text[i]
        if quote:
            if c == "\\":
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in "'\"`":
            quote = c
        elif c == "/" and text[i + 1] == "/":
            i = text.index("\n", i)
            continue
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
        i += 1
    raise AssertionError(f"unbalanced function {name}")


_DASHBOARD_FUNCS = ["esc", "renderExecResult", "_renderExecResultBody", "renderJsonTableHtml",
                    "_seriesValues", "_sparkPts", "_capContent"]


def _harness(page_text: str, funcs, with_module: bool) -> str:
    parts = ["var window = globalThis;", "var _MAX_RENDER_CHARS = 20000; var _vegaSeq = 0;",
             "function renderMdWithMermaid(t){ return {html: '<md>' + t + '</md>', mermaidBlocks: []}; }"]
    if with_module:
        parts.append((HERE / "static" / "egeria-not-measured.js").read_text())
    for f in funcs:
        if f"function {f}(" in page_text:
            parts.append(_function_source(page_text, f))
    return "\n".join(parts)


def _run(js: str, call: str, payloads):
    """Run `call` (a JS expression over `r`) for each payload; return the results."""
    script = js + "\nvar out = JSON.parse(process.argv[1]).map(function(r){ return " + call + "; });" \
                  "\nprocess.stdout.write(JSON.stringify(out));"
    proc = subprocess.run([NODE, "-e", script, json.dumps(payloads)], capture_output=True, text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def _git_show(path: str, rev: str = "3156a8d2") -> str:
    rel = (HERE / path).relative_to(_repo_root())
    proc = subprocess.run(["git", "show", f"{rev}:{rel.as_posix()}"], cwd=_repo_root(),
                          capture_output=True, text=True)
    if proc.returncode != 0:
        pytest.skip(f"base commit {rev} not available: {proc.stderr.strip()}")
    return proc.stdout


def _repo_root() -> Path:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True, text=True)
    if out.returncode != 0:
        pytest.skip("not in a git checkout")
    return Path(out.stdout.strip())


def _dashboard(payloads, page_text=None, with_module=True):
    text = page_text if page_text is not None else (HERE / "local-dashboards.html").read_text()
    return _run(_harness(text, _DASHBOARD_FUNCS, with_module), "renderExecResult(r)", payloads)


# ── the shared module ─────────────────────────────────────────────────────────

def _module(call, payloads):
    return _run("var window = globalThis;\n" + (HERE / "static" / "egeria-not-measured.js").read_text(),
                call, payloads)


def test_module_says_nothing_about_old_shapes():
    olds = [OLD_SCALAR, OLD_ZERO, OLD_TABLE, OLD_EMPTY, OLD_CHART]
    assert _module("EgeriaNotMeasured.hasUnmeasured(r)", olds) == [False] * len(olds)
    assert _module("EgeriaNotMeasured.footnoteHtml(r)", olds) == [""] * len(olds)
    assert _module("EgeriaNotMeasured.isAbsent(r)", olds) == [False] * len(olds)


def test_module_headlines_by_state():
    got = _module("EgeriaNotMeasured.headline(r)", [OLD_ABSENT, OLD_NOT_APPLICABLE, NEW_ABSENT_SCALAR])
    assert got == ["Not measured", "Does not apply", "Not measured"]


def test_module_at_least_and_cell_text():
    assert _module("EgeriaNotMeasured.atLeastText(r)", [NEW_ABSENT_SCALAR, NEW_ABSENT_CHART, OLD_ABSENT]) \
        == ["at least 500", "", ""]
    assert _module("[EgeriaNotMeasured.cellText(r, true), EgeriaNotMeasured.cellText(r, false)]",
                   [None, 0, {"a": None}]) \
        == [["not measured", ""], ["0", "0"], ['{"a":"not measured"}', '{"a":null}']]


# ── local-dashboards.html ─────────────────────────────────────────────────────

def test_dashboard_absent_scalar_is_not_a_number():
    out, = _dashboard([NEW_ABSENT_SCALAR])
    html = out["html"]
    assert 'class="nm-headline">Not measured<' in html
    assert "page cap of 500" in html                       # pyegeria's sentence
    assert 'class="nm-atleast">at least 500<' in html      # the lower bound, secondary
    assert "p-kpi-number" not in html                       # never big-number style
    assert ">500<" not in html                              # never the cap as the answer
    assert out["vegaBlocks"] == []


def test_dashboard_absent_chart_withheld_detail_collapsed():
    out, = _dashboard([NEW_ABSENT_CHART])
    html = out["html"]
    assert out["vegaBlocks"] == [] and "vega-block" not in html
    assert "<details" in html and "Partial result" in html
    assert "not measured" in html.split("<details", 1)[1]   # the null in the partial result
    assert "nm-atleast" not in html                          # at_least is null: no bound shown


def test_dashboard_old_absent_no_longer_raw_json():
    """6.2.26 already emits kind:"absent"; it used to fall through to a <pre> JSON dump."""
    before, = _dashboard([OLD_ABSENT], page_text=_git_show("local-dashboards.html"), with_module=False)
    assert before["html"].startswith("<pre")
    after = _dashboard([OLD_ABSENT, OLD_NOT_APPLICABLE])
    assert "<pre" not in after[0]["html"] and "Not measured" in after[0]["html"]
    assert "Does not apply" in after[1]["html"]


def test_dashboard_table_null_cell_and_footnote():
    out, = _dashboard([NEW_TABLE])
    html = out["html"]
    assert '<td class="nm-cell">not measured</td>' in html
    assert '"public":"not measured"' in html   # nested null too (this page\'s esc keeps quotes)
    assert "<td></td>" not in html
    assert 'data-nm="footnote"' in html
    assert "Asset (viewer scope): the native count timed out" in html


def test_dashboard_empty_with_notes_has_footnote():
    out, = _dashboard([NEW_EMPTY])
    assert "No results." in out["html"] and "Process: timed out" in out["html"]


def test_dashboard_6_2_26_shapes_render_exactly_as_before():
    olds = [OLD_SCALAR, OLD_ZERO, OLD_TABLE, OLD_EMPTY, OLD_CHART]
    before = _dashboard(olds, page_text=_git_show("local-dashboards.html"), with_module=False)
    after = _dashboard(olds)
    assert after == before
    assert "<td></td>" in after[2]["html"]          # an old null stays blank: no notes, no claim


def test_dashboard_without_module_still_renders_old_shapes():
    """If the new script fails to load, older shapes still render as before."""
    olds = [OLD_SCALAR, OLD_TABLE, OLD_EMPTY]
    assert _dashboard(olds, with_module=False) == _dashboard(olds)


# ── governance-metrics.html ───────────────────────────────────────────────────

def _gov(payloads, page_text=None, with_module=True):
    text = page_text if page_text is not None else (HERE / "governance-metrics.html").read_text()
    js = _harness(text, ["esc", "renderRunOutput"], with_module)
    call = ("(function(){ var o = {textContent: '', innerHTML: '', extra: '',"
            " insertAdjacentHTML: function(_, h){ this.extra += h; } };"
            " renderRunOutput(o, r); return o; })()")
    return _run(js, call, payloads)


def test_governance_metrics_absent_and_table():
    absent, table, empty = _gov([NEW_ABSENT_SCALAR, NEW_TABLE, NEW_EMPTY])
    assert "Not measured" in absent["innerHTML"] and "at least 500" in absent["innerHTML"]
    assert absent["textContent"] == ""
    assert '"count": "not measured"' in table["textContent"] and "null" not in table["textContent"]
    assert "Asset (viewer scope)" in table["extra"]
    assert empty["textContent"] == "No results." and "Process: timed out" in empty["extra"]


def test_governance_metrics_old_shapes_same_text():
    """The base page set out.textContent = JSON.stringify(d.data ?? d); the new one must too."""
    olds = [OLD_SCALAR, OLD_TABLE, OLD_EMPTY, OLD_CHART]
    got = _gov(olds)
    for o, r in zip(got, olds):
        assert o["textContent"] == json.dumps(r.get("data", r), indent=2, ensure_ascii=False)
        assert o["extra"] == "" and o["innerHTML"] == ""


# ── type-explorer.html (React; checked structurally, rendered in screenshots) ─

def test_type_explorer_wiring():
    text = (HERE / "type-explorer.html").read_text()
    assert '<script src="/static/egeria-not-measured.js' in text
    run = _function_source(text, "renderExecResults")
    assert run.index("NM.isAbsent(execResult)") < run.index("execResult.kind === 'empty'")
    dv = _function_source(text, "DictResultView")
    assert "unmeasured && val === null" in dv and "unmeasured: unmeasured" in dv


def test_every_execute_page_loads_the_module():
    for page in ("local-dashboards.html", "governance-metrics.html", "type-explorer.html"):
        text = (HERE / page).read_text()
        assert "/api/report-specs/execute" in text
        assert "/static/egeria-not-measured.js" in text, page


def test_recorded_555_outputs_render_honestly():
    scalar, table = _dashboard([REAL_555_SCALAR, REAL_555_TABLE])
    assert ">Not measured<" in scalar["html"] and "at least 500" in scalar["html"]
    assert "p-kpi-number" not in scalar["html"] and ">500<" not in scalar["html"]
    assert '<td class="nm-cell">not measured</td>' in table["html"]          # total: None
    assert '"count":"not measured"' in table["html"] and '"count":12' in table["html"]
    assert "Asset: no native count is available" in table["html"]           # the footnote
