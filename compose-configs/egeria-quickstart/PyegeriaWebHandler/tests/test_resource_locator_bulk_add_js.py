# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Bulk add from Search and Browse to a working set (Dan, 2026-11-17, PO-37; design note
DESIGN-RL-BULK-ADD-AND-BREADCRUMBS, Architect read-back R1, R4).

Pinned here:
  - Select all takes the rows shown (loaded and passing the filters), keeps an earlier selection,
    and the summary counts selected rows the filters now hide;
  - 230 rows go as 100/100/30, one request at a time: a chunk is done only when its response
    arrives (never two in flight), and progress names the rows in flight (R4);
  - a row already in a fully read list is not sent; for a list read at its limit everything is
    sent and a success says "added or already in it" (R1);
  - a 207's failed map fails those rows only; a request that fails as a whole fails every row it
    carried, never counted as added.
Runs the helpers from resource-browser.html under node; skipped without node."""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

_PAGE = (Path(__file__).resolve().parent.parent / "resource-browser.html").read_text()
_NAMES = ("selectAllShown", "selectionSummary", "chunk", "planBulkAdd", "chunkOutcomes", "bulkSummary", "bulkAdd")


def _fn(name: str) -> str:
    start = _PAGE.index(f"function {name}(")
    return _PAGE[start:_PAGE.index("\n}\n", start) + 3]


def _run(body: str) -> dict:
    js = "var BULK_CHUNK = 100;\n" + "\n".join(_fn(n) for n in _NAMES) + "\n" + body
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout.strip().splitlines()[-1])


needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")


@needs_node
def test_select_all_takes_the_shown_rows_and_counts_hidden_ones():
    d = _run(r"""
var shown = [{ guid: 'a' }, { guid: 'b' }];
var sel = selectAllShown(shown, { z: true });
console.log(JSON.stringify({ sel: Object.keys(sel).sort(), sum: selectionSummary(sel, shown),
  afterFilter: selectionSummary(sel, [{ guid: 'a' }]), chunks: chunk(new Array(230).fill(0), 100).map(function(c) { return c.length; }) }));""")
    assert d["sel"] == ["a", "b", "z"]
    assert d["sum"] == {"count": 3, "hidden": 1} and d["afterFilter"] == {"count": 3, "hidden": 2}
    assert d["chunks"] == [100, 100, 30]


@needs_node
def test_chunks_go_one_at_a_time_and_failures_are_per_row():
    d = _run(r"""
var guids = []; for (var i = 0; i < 230; i++) guids.push('g' + i);
var inFlight = 0, peak = 0, calls = [], progress = [];
function post(part) {
  inFlight++; peak = Math.max(peak, inFlight); calls.push(part.length);
  var n = calls.length;
  return new Promise(function(res, rej) { setTimeout(function() {
    inFlight--;
    if (n === 2) res({ failed: { g150: 'not visible' } });            // a 207 with one failed row
    else if (n === 3) rej(new Error('HTTP 504'));                      // the whole request failed
    else res({ guid: 'L' });
  }, 5); });
}
var memberOf = { g5: ['L'] };                                          // already in the (fully read) list
bulkAdd({ guid: 'L', displayName: 'Q3', membersCapped: false }, guids, memberOf, post, function(t) { progress.push(t); })
  .then(function(o) {
    var states = {}; Object.keys(o).forEach(function(g) { states[o[g].state] = (states[o[g].state] || 0) + 1; });
    console.log(JSON.stringify({ peak: peak, calls: calls, progress: progress, states: states,
      g5: o.g5, g150: o.g150, g229: o.g229, summary: bulkSummary(o, 'Q3') }));
  });""")
    assert d["peak"] == 1, "never two chunks in flight"
    assert d["calls"] == [100, 100, 29]                 # g5 was not sent
    assert d["progress"] == ["Adding 1–100 of 229…", "Adding 101–200 of 229…", "Adding 201–229 of 229…"]
    assert d["g5"] == {"state": "already"}
    assert d["g150"] == {"state": "failed", "message": "not visible"}
    assert d["g229"] == {"state": "failed", "message": "HTTP 504"}
    assert d["states"] == {"already": 1, "added": 199, "failed": 30}
    assert "added 199" in d["summary"] and "1 already in it" in d["summary"] and "30 failed" in d["summary"]


@needs_node
def test_a_list_read_at_its_limit_sends_everything_and_says_added_or_already():
    d = _run(r"""
var sent = [];
bulkAdd({ guid: 'L', displayName: 'Big', membersCapped: true }, ['a', 'b'], { a: ['L'] },
        function(part) { sent = part; return Promise.resolve({}); }, function() {})
  .then(function(o) { console.log(JSON.stringify({ sent: sent, a: o.a.state, b: o.b.state, summary: bulkSummary(o, 'Big') })); });""")
    assert d["sent"] == ["a", "b"]
    assert d["a"] == d["b"] == "addedOrAlready"
    assert "2 added or already in it" in d["summary"]


def test_the_bar_is_on_search_and_browse_and_the_list_flag_is_served():
    assert _PAGE.count("el(BulkBar, {") == 2
    assert _PAGE.count("sel: sel") >= 4
    handler = (Path(__file__).resolve().parent.parent / "resource_browser_handler.py").read_text()
    assert 'rec["membersCapped"] = rec["memberCount"] >= _LIST_CAP' in handler


# ── The server side the bar relies on: one request, per-row failures as 207 ─────

import resource_browser_handler as rb   # noqa: E402  (kept apart from the node tests above)


class _Collections:
    def __init__(self):
        self.added = []

    async def _async_add_to_collection(self, list_guid, guid, body=None):
        if guid == "bad":
            raise RuntimeError("not visible to the caller")
        self.added.append(guid)


@pytest.fixture
def fake_lists(monkeypatch):
    cm = _Collections()

    async def explorer():
        return object()

    async def my_list(_client, guid):
        return {"guid": guid}

    async def collections():
        return cm

    async def get_list(guid):
        return rb.JSONResponse({"guid": guid, "members": [{"guid": g} for g in cm.added]})
    monkeypatch.setattr(rb, "_explorer_async", explorer)
    monkeypatch.setattr(rb, "_my_list", my_list)
    monkeypatch.setattr(rb, "_collections_async", collections)
    monkeypatch.setattr(rb, "get_list", get_list)
    return cm


def test_add_members_reports_only_the_failed_row_as_207(client, fake_lists):
    r = client.post("/api/resource-browser/lists/L/members", json={"guids": ["a", "bad", "b", "a"], "rationale": "q3"})
    assert r.status_code == 207
    assert list(r.json()["failed"]) == ["bad"] and fake_lists.added == ["a", "b"]


def test_add_members_caps_one_request_at_100(client, fake_lists):
    r = client.post("/api/resource-browser/lists/L/members", json={"guids": [f"g{i}" for i in range(101)]})
    assert r.status_code == 400 and fake_lists.added == []
