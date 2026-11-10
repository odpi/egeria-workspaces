"""Report-spec consumer folders, phase 2, the Portal side: "Used by" in the Report Specs view.

report_spec_consumers.py turns pyegeria's cached consumer index into per-spec fields, and
/api/report-specs carries them. Absence is never "none": an index that was not read (or a pyegeria
without one, 6.2.32 and earlier) is "not read" with the reason; built-in and local specs are "not
tracked"; only a spec held in Egeria that no consumer folder holds is "none". The chip row itself
(RsUsedBy, in both environments' type-explorer.html) runs under node when node is installed.
No Egeria call is made by any test here.
"""
import json
import re
import shutil
import subprocess
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import report_spec_consumers as rsc  # noqa: E402
import report_specs_handler  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
FRESH = HERE.parent.parent / "egeria-freshstart" / "PyegeriaWebHandler"

READ = {"format": "pyegeria-report-spec-consumers/1", "status": "read", "reason": None,
        "root": "RootCollection::ReportSpecs", "read_at": "2026-11-10T20:00:00Z", "read_as": "portal",
        "consumers": [{"name": "Egeria Advisor", "status": "read", "reason": None, "specs": 1},
                      {"name": "Jupyter", "status": "read", "reason": None, "specs": 0},
                      {"name": "Portal", "status": "read", "reason": None, "specs": 2}],
        "index": {"Analytic - Generic Metric Trend": ["Egeria Advisor", "Portal"],
                  "Resource Explorer - Curation Coverage": ["Portal"]}}


def _with_reader(monkeypatch, fn):
    from pyegeria.view import egeria_spec_cache as esc
    monkeypatch.setattr(esc, "read_consumer_index", fn, raising=False)


# ── report_spec_consumers ──

def test_index_on_a_pyegeria_without_one_is_not_read(monkeypatch):
    from pyegeria.view import egeria_spec_cache as esc
    monkeypatch.delattr(esc, "read_consumer_index", raising=False)
    idx = rsc.index()
    assert idx["status"] == "not read" and idx["supported"] is False
    assert "has no consumer index" in idx["reason"] and idx["index"] == {}


def test_index_passes_the_cached_index_through(monkeypatch):
    _with_reader(monkeypatch, lambda **_: READ)
    idx = rsc.index()
    assert idx["status"] == "read" and idx["supported"] is True
    assert [c["name"] for c in idx["consumers"]] == ["Egeria Advisor", "Jupyter", "Portal"]
    assert idx["index"]["Resource Explorer - Curation Coverage"] == ["Portal"]
    assert "index" not in rsc.summary(idx)


def test_a_reader_error_is_not_read_with_the_reason(monkeypatch):
    def boom(**_):
        raise OSError("permission denied")
    _with_reader(monkeypatch, boom)
    idx = rsc.index()
    assert idx["status"] == "not read" and "permission denied" in idx["reason"]


def test_a_not_read_index_never_lends_its_labels(monkeypatch):
    _with_reader(monkeypatch, lambda **_: dict(READ, status="not read", reason="root not visible"))
    assert rsc.index()["index"] == {}


def test_used_by_states():
    read = dict(READ, supported=True)
    # A label the index holds: its consumers, whatever the row's source.
    assert rsc.used_by("Analytic - Generic Metric Trend", "egeria", {"guid": "g"}, read) == {
        "usedBy": ["Egeria Advisor", "Portal"], "usedByState": "read", "usedByReason": None}
    assert rsc.used_by("egeria:Resource Explorer - Curation Coverage", None, None, read)["usedBy"] == ["Portal"]
    # Held in Egeria, in no consumer folder: none.
    assert rsc.used_by("Some-Held-Spec", "egeria", None, read) == {
        "usedBy": [], "usedByState": "read", "usedByReason": None}
    # Built-in or local: not tracked (phase 3), never "none".
    nt = rsc.used_by("Collections", "builtin", None, read)
    assert nt["usedBy"] is None and nt["usedByState"] == "not tracked"
    # Not read: every row says so, with the reason.
    nr = rsc.used_by("Some-Held-Spec", "egeria", None, {"status": "not read", "reason": "no sync yet"})
    assert nr == {"usedBy": None, "usedByState": "not read", "usedByReason": "no sync yet"}
    # Partial: what was read, and the reason.
    part = rsc.used_by("Some-Held-Spec", "egeria", None, dict(read, status="partial", reason="not fully read: Jupyter"))
    assert part == {"usedBy": [], "usedByState": "partial", "usedByReason": "not fully read: Jupyter"}


# ── /api/report-specs ──

@pytest.fixture
def api():
    app = FastAPI()
    app.include_router(report_specs_handler.router)
    return TestClient(app)


def test_the_list_carries_used_by_on_every_spec(api, monkeypatch):
    _with_reader(monkeypatch, lambda **_: READ)
    data = api.get("/api/report-specs").json()
    assert data["consumers"]["status"] == "read" and "index" not in data["consumers"]
    assert [c["name"] for c in data["consumers"]["consumers"]] == ["Egeria Advisor", "Jupyter", "Portal"]
    assert all(s["usedByState"] in ("read", "partial", "not tracked") for s in data["specs"])
    by_name = {s["name"]: s for s in data["specs"]}
    trend = by_name.get("Analytic - Generic Metric Trend")
    if trend:  # registered by the Portal at import (local) or synced (egeria)
        assert trend["usedBy"] == ["Egeria Advisor", "Portal"]
    assert by_name["Collections"]["usedByState"] == "not tracked"


def test_the_list_says_not_read_rather_than_none(api, monkeypatch):
    _with_reader(monkeypatch, lambda **_: {"format": "pyegeria-report-spec-consumers/1", "status": "not read",
                                           "reason": "the root RootCollection::ReportSpecs was not found",
                                           "consumers": [], "index": {}})
    data = api.get("/api/report-specs").json()
    assert data["consumers"]["status"] == "not read"
    assert all(s["usedByState"] == "not read" and s["usedBy"] is None for s in data["specs"])
    assert not any(s["usedBy"] == [] for s in data["specs"])


@pytest.mark.skipif(not FRESH.is_dir(), reason="the freshstart tree is not beside this checkout (a container's /app)")
def test_freshstart_ships_the_same_helper():
    assert (FRESH / "report_spec_consumers.py").read_text() == (HERE / "report_spec_consumers.py").read_text()
    handler = (FRESH / "report_specs_handler.py").read_text()
    assert "report_spec_consumers.used_by(" in handler and '"consumers":' in handler


# ── The chip row (RsUsedBy) ──

def _rs_used_by_source(page: Path) -> str:
    text = page.read_text()
    start = text.index("var _RS_CHIP = ")
    end = text.index("\nfunction RsSourceDetail(" if "function RsSourceDetail(" in text[start:] else "\nfunction ReportSpecDetail(", start)
    return text[start:end]


def _render(page: Path, spec: dict) -> str:
    """Render RsUsedBy(spec) to plain text with a stub React (node)."""
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    js = ("var React = {createElement: function(t, p) { var kids = [].slice.call(arguments, 2);"
          " var flat = [].concat.apply([], kids).filter(function(k){return k !== null && k !== undefined && k !== false;});"
          " return {t: t, p: p || {}, k: flat}; }};\n"
          "function txt(n) { if (n === null || n === undefined) return ''; if (typeof n !== 'object') return String(n);"
          " return n.k.map(txt).join(' '); }\n"
          + _rs_used_by_source(page) +
          f"\nconsole.log(JSON.stringify(txt(RsUsedBy({{spec: {json.dumps(spec)}}}))));")
    out = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    return re.sub(r"\s+", " ", json.loads(out.stdout)).strip()


@pytest.mark.parametrize("page", [HERE / "type-explorer.html", FRESH / "type-explorer.html"], ids=["quickstart", "freshstart"])
def test_chip_row_says_each_state(page):
    if not page.is_file():
        pytest.skip(f"{page} not in this checkout")
    assert _render(page, {"usedBy": ["Portal", "Egeria Advisor"], "usedByState": "read"}) == "Used by: Portal Egeria Advisor"
    assert _render(page, {"usedBy": [], "usedByState": "read"}) == "Used by: none"
    assert _render(page, {"usedBy": [], "usedByState": "partial", "usedByReason": "x"}) == "Used by: none found (partly read)"
    # The reason is said once in the sidebar; on each spec it is a tooltip.
    assert _render(page, {"usedBy": None, "usedByState": "not read", "usedByReason": "no sync yet"}) == "Used by: not read"
    assert "'Consumers not read' + (spec.usedByReason ? ': ' + spec.usedByReason : '')" in page.read_text()
    assert _render(page, {"usedBy": None, "usedByState": "not tracked"}) == "Used by: not tracked"
    assert _render(page, {"name": "older API"}) == ""


@pytest.mark.parametrize("page", [HERE / "type-explorer.html", FRESH / "type-explorer.html"], ids=["quickstart", "freshstart"])
def test_view_wires_the_chip_row_and_the_consumer_filter(page):
    if not page.is_file():
        pytest.skip(f"{page} not in this checkout")
    text = page.read_text()
    assert "React.createElement(RsUsedBy, { spec: spec })" in text
    assert "'aria-label': 'Filter by consumer'" in text
    assert "'Used by none (' + consumerCounts.__none__ + ')'" in text
    assert "'Consumers: not read'" in text  # the sidebar says not read instead of an empty filter
    assert "consumerFilter]);" in text       # the filter is a dependency of the filtered list
