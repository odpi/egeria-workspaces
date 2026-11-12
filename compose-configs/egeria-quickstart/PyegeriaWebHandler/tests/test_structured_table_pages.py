"""P1b: Local Dashboards and Report Specs ask for pyegeria's structured TABLE (BRIEF-P1-PORTAL-STRUCTURED-TABLE).

- /api/report-specs/execute passes `table_shape` to exec_report_spec ONLY for output_format TABLE; any
  other value than "rows"/"structured" is a 400 with a sentence; the default is unchanged; the result
  cache keeps the two shapes apart.
- local-dashboards.html: a TABLE placement requests table_shape "structured" and renders kind "table"
  through static/egeria-table.js (notes in the table's footer, not twice; element links to The
  Catalog's ?guid= resolver). type-explorer.html's Report Specs Run does the same.
- governance-metrics.html requests DICT only, so it is unchanged.

The table result is real: tests/fixtures/structured_table_laz_2026_11_12.json (pyegeria 6.2.39,
read-only on laz). exec_report_spec is a fake. The page parts run under node (skipped without it).
"""
import copy
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

LAZ = json.loads((HERE / "fixtures" / "structured_table_laz_2026_11_12.json").read_text())
RISK = LAZ["Risk-DrE-Basic"]
DP = LAZ["Digital-Products"]


# ── The handler ───────────────────────────────────────────────────────────────

@pytest.fixture
def client(monkeypatch):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    import egeria_auth
    import report_specs_handler as rh
    import pyegeria.view.format_set_executor as fse
    from result_cache import ResultCache
    state = {"calls": []}

    def fake_exec(name, **kwargs):
        state["calls"].append(kwargs)
        if kwargs.get("table_shape") == "structured":
            return copy.deepcopy(RISK)
        return {"kind": "json", "data": [{"Display Name": "x"}]}

    monkeypatch.setattr(fse, "exec_report_spec", fake_exec)
    monkeypatch.setattr(rh, "_RESULT_CACHE", ResultCache(ttl=300, max_stale=3600, max_entries=10, refresh_backoff=30))
    app = FastAPI()
    app.add_middleware(egeria_auth.EgeriaTokenMiddleware)
    app.include_router(rh.router)
    return TestClient(app), state


def _post(c, fmt, shape=..., cache=False):
    body = {"spec_name": "Risk-DrE-Basic", "output_format": fmt, "params": {"search_string": "*"}, "cache": cache}
    if shape is not ...:
        body["table_shape"] = shape
    return c.post("/api/report-specs/execute", json=body)


def test_structured_table_passes_through_for_table(client):
    c, state = client
    r = _post(c, "TABLE", "structured")
    assert r.status_code == 200
    body = r.json()
    assert body["kind"] == "table" and body["columns"] == RISK["columns"] and "specSource" in body
    assert state["calls"][-1]["table_shape"] == "structured" and state["calls"][-1]["output_format"] == "TABLE"


@pytest.mark.parametrize("fmt", ["DICT", "REPORT", "LIST", "JSON", "MD"])
def test_other_formats_never_send_table_shape(client, fmt):
    c, state = client
    assert _post(c, fmt, "structured").status_code == 200
    assert "table_shape" not in state["calls"][-1]


def test_lower_case_table_counts_as_table(client):
    c, state = client
    _post(c, "table", "structured")
    assert state["calls"][-1]["table_shape"] == "structured"


def test_default_is_unchanged(client):
    c, state = client
    body = _post(c, "TABLE").json()
    assert body["kind"] == "json" and "table_shape" not in state["calls"][-1]


def test_rows_is_passed_as_asked(client):
    c, state = client
    _post(c, "TABLE", "rows")
    assert state["calls"][-1]["table_shape"] == "rows"


@pytest.mark.parametrize("fmt", ["TABLE", "DICT"])
@pytest.mark.parametrize("bad", ["nested", "STRUCTURED", ""])
def test_other_values_are_refused_with_a_sentence(client, fmt, bad):
    c, state = client
    r = _post(c, fmt, bad)
    assert r.status_code == 400
    assert r.json()["detail"] == f'table_shape must be "rows" or "structured", not {bad!r}.'
    assert state["calls"] == []                                         # refused before Egeria


def test_bad_value_is_refused_before_the_cache(client):
    c, state = client
    r = _post(c, "TABLE", "nested", cache=True)
    assert r.status_code == 400 and state["calls"] == []


def test_cache_keeps_the_two_shapes_apart(client):
    c, state = client
    a = _post(c, "TABLE", "structured", cache=True)
    b = _post(c, "TABLE", cache=True)
    a2 = _post(c, "TABLE", "structured", cache=True)
    assert a.json()["kind"] == "table" and b.json()["kind"] == "json" and a2.json()["kind"] == "table"
    assert len(state["calls"]) == 2 and a2.headers["X-Cache"] == "hit"


def test_cache_shares_an_entry_when_the_shape_is_ignored(client):
    c, state = client
    _post(c, "DICT", "structured", cache=True)
    assert _post(c, "DICT", cache=True).headers["X-Cache"] == "hit"     # DICT ignores the flag
    assert len(state["calls"]) == 1


# ── local-dashboards.html ─────────────────────────────────────────────────────

LD = (ROOT / "local-dashboards.html").read_text()


def _grab(src, pat):
    m = re.search(pat, src, re.S)
    assert m, pat
    return m.group(0)


def _node(js):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    out = subprocess.run([node, "-"], input=js, capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout.strip().splitlines()[-1])


def _ld_prelude():
    return "\n".join([
        "var window = globalThis;",
        "window.EgeriaTable = require(" + json.dumps(str(ROOT / "static" / "egeria-table.js")) + ");",
        "require(" + json.dumps(str(ROOT / "static" / "egeria-not-measured.js")) + ");",
        _grab(LD, r"function esc\(s\) \{.*?\n\}"),
        _grab(LD, r"var EXECUTE_CACHE_TTL_MS = [^\n]*;\nvar _executeCache = \{\};"),
        _grab(LD, r"var _execMeta = new WeakMap\(\);"),
        _grab(LD, r"function _fetchExecuteCached\(body, force\) \{.*?\n\}\n"),
        _grab(LD, r"// params: the placement's effective params.*?\nfunction renderExecResult\(result, params\) \{.*?\n\}\n"),
        _grab(LD, r"function tableLinkBuilder\(el\) \{.*?\n\}"),
        _grab(LD, r"function _renderExecResultBody\(result, params\) \{.*?\n\}\n"),
    ])


@pytest.mark.parametrize("fmt,expected", [("TABLE", "structured"), ("table", "structured"), ("DICT", None),
                                          ("REPORT", None), ("LIST", None)])
def test_a_table_placement_requests_the_structured_table(fmt, expected):
    js = _ld_prelude() + """
var sent = null;
window.fetch = function(url, opts) { sent = JSON.parse(opts.body);
  return Promise.resolve({ ok: true, headers: { get: function() { return null; } }, json: function() { return {kind: 'empty'}; } }); };
_fetchExecuteCached({ spec_name: 'Risk-DrE-Basic', output_format: %s, params: {} }, false).then(function() {
  console.log(JSON.stringify({ shape: sent.table_shape === undefined ? null : sent.table_shape, cache: sent.cache }));
});
""" % json.dumps(fmt)
    assert _node(js) == {"shape": expected, "cache": True}


def test_kind_table_renders_through_egeria_table_with_notes_once():
    js = _ld_prelude() + "console.log(JSON.stringify(renderExecResult(%s, {}).html));" % json.dumps(DP)
    html = _node(js)
    assert 'class="et" data-et-table' in html and "et-table et-wide" in html
    assert html.count("Uses Products: none on 55 rows") == 1                     # in the footer only
    assert "nm-result-notes" not in html
    assert "78 rows (one page; Egeria doesn&#39;t promise it is the last)." in html
    first = DP["rows"][0]["used_by_digital_products"][0]
    assert 'href="/tech-catalog?guid=' + first["guid"] + '"' in html
    assert "more column" not in html                                             # no 20-column cap


def test_kind_json_keeps_the_old_table_and_its_notes():
    # renderJsonTableHtml needs the page's other table helpers; check the branch order in the source.
    body = _grab(LD, r"function _renderExecResultBody\(result, params\) \{.*?\n\}\n")
    assert body.index("result.kind === 'table'") < body.index("result.kind === 'json'")
    assert "renderJsonTableHtml(result.data" in body
    notes = _grab(LD, r"function renderExecResult\(result, params\) \{.*?\n\}\n")
    assert "!(result && result.kind === 'table')" in notes and "resultNotesHtml(result)" in notes


def test_page_loads_the_renderer_and_attaches_once():
    assert '<script src="/static/egeria-table.js?v=' in LD
    assert LD.count("EgeriaTable.attach(document.body)") == 1
    assert "EgeriaTable.trim(target)" in _grab(LD, r"function afterPlacementResult\(p, i, result, target\) \{.*?\n\}")
    # the old TABLE-as-markdown branch stays, with a warning, until nothing hits it
    assert 'the old TABLE-as-markdown case' in LD


# ── type-explorer.html (Report Specs → Run) and governance-metrics.html ───────

TE = (ROOT / "type-explorer.html").read_text()


def test_report_specs_run_asks_for_and_renders_the_structured_table():
    assert '<script src="/static/egeria-table.js?v=' in TE
    run = _grab(TE, r"function runReport\(\) \{.*?\n  \}\n")
    assert "if (actualFmt === 'TABLE' && window.EgeriaTable) body.table_shape = 'structured';" in run
    res = _grab(TE, r"function renderExecResults\(\) \{.*?if \(execResult\.kind === 'json'\)")
    assert "execResult.kind === 'table' && window.EgeriaTable" in res
    assert "window.EgeriaTable.attach(el)" in res and "window.EgeriaTable.trim(el)" in res
    assert "'/tech-catalog?guid=' + encodeURIComponent(el.guid)" in res


def test_governance_metrics_requests_dict_only():
    gm = (ROOT / "governance-metrics.html").read_text()
    assert gm.count("/api/report-specs/execute") == 1
    assert "output_format: 'DICT'" in gm and "'TABLE'" not in gm
