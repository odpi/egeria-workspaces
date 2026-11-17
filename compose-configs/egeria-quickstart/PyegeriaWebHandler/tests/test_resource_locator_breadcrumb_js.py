# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Breadcrumb back to the list a resource was opened from (Dan, 2026-11-17, PO-38; design note
DESIGN-RL-BULK-ADD-AND-BREADCRUMBS, Architect read-back R2, R3).

Pinned here:
  - the crumb names where the resource came from (Search "q" (kinds), Browse › facet › value,
    a work list, a lens, Resource Locator Home);
  - only a search string of this page is accepted as where to go back to; a full URL, "//x",
    a stale state for another resource, or none falls back to Resource Locator Home (R2);
  - view state round-trips through sessionStorage with a 30-minute expiry, and holds only what
    it is given (no rows, no token);
  - restoring reads at most 10 pages one at a time; a failed page stops it and says the list is
    not the full one, never showing a partial list as the rows you had (R3).
Runs the helpers from resource-browser.html under node; skipped without node."""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

_PAGE = (Path(__file__).resolve().parent.parent / "resource-browser.html").read_text()
_NAMES = ("routeLabel", "safeFrom", "viewKey", "loadView", "saveView", "mergeResults", "restorePages")


def _fn(name: str) -> str:
    start = _PAGE.index(f"function {name}(")
    return _PAGE[start:_PAGE.index("\n}\n", start) + 3]


def _run(body: str) -> dict:
    js = ("var HOME_LABEL = 'Resource Locator Home'; var VIEW_TTL_MS = 30 * 60 * 1000; var RESTORE_MAX_PAGES = 10;\n"
          "var FACETS = [{ id: 'keyword', label: 'Search keyword' }, { id: 'tag', label: 'Tag' }];\n"
          + "\n".join(_fn(n) for n in _NAMES) + "\n" + body)
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout.strip().splitlines()[-1])


needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")


@needs_node
def test_labels_name_where_the_resource_came_from():
    d = _run(r"""console.log(JSON.stringify([
  routeLabel({ page: 'search', q: 'customer' }, 'Tables, Schemas'), routeLabel({ page: 'search', q: 'x' }, ''),
  routeLabel({ page: 'browse', facet: 'keyword', value: 'App/AI Builder' }, ''), routeLabel({ page: 'browse', facet: 'tag', value: 'g1' }, 'pii'),
  routeLabel({ page: 'list' }, 'Q3 sources'), routeLabel({ page: 'lens' }, 'UK'), routeLabel({ page: 'home' }, '')]));""")
    assert d == ["Search “customer” (Tables, Schemas)", "Search “x”",
                 "Browse › Search keyword › App/AI Builder", "Browse › Tag › pii",
                 "Work list ‘Q3 sources’", "Data lens ‘UK’", "Resource Locator Home"]


@needs_node
def test_only_a_search_string_of_this_page_is_accepted():
    d = _run(r"""
function f(from, guid) { return safeFrom({ guid: 'g1', from: from, fromLabel: 'Search' }, guid || 'g1'); }
console.log(JSON.stringify({ ok: f('?q=customer&kind=table'), home: f(''), evil: f('https://evil/x'), slashes: f('//x'),
  path: f('/other?q=1'), hash: f('?q=1#x'), js: f('javascript:alert(1)'), stale: f('?q=1', 'other'), none: safeFrom(null, 'g1'),
  notString: safeFrom({ guid: 'g1', from: 5 }, 'g1'), noLabel: safeFrom({ guid: 'g1', from: '?q=1' }, 'g1') }));""")
    assert d["ok"] == {"from": "?q=customer&kind=table", "label": "Search"}
    assert d["home"] == {"from": "", "label": "Search"}
    for k in ("evil", "slashes", "path", "hash", "js", "stale", "none", "notString"):
        assert d[k] is None, k
    assert d["noLabel"]["label"] == "the list you came from"


@needs_node
def test_view_state_round_trips_and_expires():
    d = _run(r"""
var mem = {}; var store = { getItem: function(k) { return mem[k] === undefined ? null : mem[k]; }, setItem: function(k, v) { mem[k] = v; } };
saveView(store, '?q=a', { filt: { owner: 'x' }, pages: 3 }, 1000);
saveView(store, '?q=a', { scrollY: 420 }, 2000);
var fresh = loadView(store, '?q=a', 2000 + 29 * 60 * 1000), old = loadView(store, '?q=a', 2000 + 31 * 60 * 1000);
mem['rb-view:?bad'] = '{not json';
console.log(JSON.stringify({ fresh: fresh, old: old, other: loadView(store, '?q=b', 2000), bad: loadView(store, '?bad', 0),
  keys: Object.keys(JSON.parse(mem['rb-view:?q=a'])).sort() }));""")
    assert d["fresh"] == {"filt": {"owner": "x"}, "pages": 3, "scrollY": 420, "at": 2000}
    assert d["old"] is None and d["other"] is None and d["bad"] is None
    assert d["keys"] == ["at", "filt", "pages", "scrollY"]


@needs_node
def test_restore_reads_at_most_ten_pages_and_stops_on_a_failure():
    d = _run(r"""
var calls = [], inFlight = 0, peak = 0;
function pages(failAt, last) {
  return function(page) {
    calls.push(page); inFlight++; peak = Math.max(peak, inFlight);
    return new Promise(function(res, rej) { setTimeout(function() {
      inFlight--;
      if (page === failAt) rej(new Error('HTTP 504'));
      else res({ items: [{ guid: 'p' + page, matched: [] }], mayHaveMore: page !== last });
    }, 2); });
  };
}
var progress = [];
restorePages(14, pages(-1, 99), function(t) { progress.push(t); }, function() {}).then(function(a) {
  var first = { n: calls.length, rows: a.rows.length, complete: a.complete, note: a.note, lastProgress: progress[progress.length - 1] };
  calls = [];
  return restorePages(5, pages(2, 99), function() {}, function() {}).then(function(b) {
    var second = { calls: calls.slice(), rows: b.rows.length, complete: b.complete, note: b.note };
    calls = [];
    return restorePages(6, pages(-1, 1), function() {}, function() {}).then(function(c) {
      console.log(JSON.stringify({ first: first, second: second, early: { calls: calls, rows: c.rows.length, complete: c.complete, note: c.note }, peak: peak }));
    });
  });
});""")
    assert d["first"]["n"] == 10 and d["first"]["rows"] == 10 and d["first"]["complete"] is True
    assert "first 10 of the 14 pages" in d["first"]["note"]
    assert d["first"]["lastProgress"] == "Restoring the results you had: page 10 of 10…"
    assert d["second"]["calls"] == [0, 1, 2] and d["second"]["rows"] == 2 and d["second"]["complete"] is False
    assert "Only 2 of the 5 pages" in d["second"]["note"] and "not the full list" in d["second"]["note"]
    assert d["early"]["calls"] == [0, 1] and d["early"]["complete"] is True and d["early"]["note"] == ""
    assert d["peak"] == 1


def test_the_resource_page_shows_the_crumb_and_pages_name_themselves():
    assert "el(BackCrumb, { guid: guid })," in _PAGE
    assert _PAGE.count("setPageLabel(") >= 6
    store = _PAGE[_PAGE.index("function openResource("):_PAGE.index("function goBackTo(")]
    assert "saveView(store, from, { scrollY:" in store and "token" not in store


@needs_node
def test_scroll_is_read_from_and_restored_to_the_content_pane():
    """PO-38 R4 (Coordinator's live check on laz, 2026-11-17): the list scrolls inside .rb-scroll
    (scrollTop 1000) while window.scrollY stays 0, so the old save stored 0. The pane is used when
    it scrolls, the window otherwise, and a restore retries until the rows are drawn."""
    js = "\n".join(_fn(n) for n in ("readScroll", "applyScroll", "restoreScroll")) + r"""
function pane(top, height, client) { return { scrollTop: top, scrollHeight: height, clientHeight: client }; }
function doc(p) { return { querySelector: function(sel) { return sel === '.rb-scroll' ? p : null; } }; }
var win = { scrollY: 0, scrollTo: function(x, y) { this.scrollY = y; } };
var paneDoc = doc(pane(1000, 5000, 800)), noPane = doc(null), flat = doc(pane(0, 800, 800));
var read = { pane: readScroll(paneDoc, { scrollY: 0 }), window: readScroll(noPane, { scrollY: 640 }), none: readScroll(flat, { scrollY: 0 }) };
var p2 = pane(0, 5000, 800); applyScroll(doc(p2), win, 1200);
var w2 = { scrollY: 0, scrollTo: function(x, y) { this.scrollY = y; } }; applyScroll(flat, w2, 300);
// restoreScroll: the pane grows as rows are drawn; it keeps trying until 1500 can be reached.
var growing = pane(0, 1000, 800);
var document = doc(growing), window = { scrollY: 0, scrollTo: function() {} };
growing.scrollHeight = 1000;
Object.defineProperty(growing, 'scrollTop', { get: function() { return this._t || 0; },
  set: function(v) { this._t = Math.min(v, this.scrollHeight - this.clientHeight); } });
restoreScroll(1500);
setTimeout(function() { growing.scrollHeight = 3000; }, 120);
setTimeout(function() {
  console.log(JSON.stringify({ read: read, paneSet: p2.scrollTop, windowSet: w2.scrollY, restored: growing.scrollTop }));
}, 600);"""
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    d = json.loads(out.stdout.strip().splitlines()[-1])
    assert d["read"] == {"pane": 1000, "window": 640, "none": 0}
    assert d["paneSet"] == 1200 and d["windowSet"] == 300
    assert d["restored"] == 1500


def test_open_resource_saves_the_pane_scroll():
    opener = _PAGE[_PAGE.index("function openResource("):_PAGE.index("function goBackTo(")]
    assert "scrollY: readScroll(document, window)" in opener
    assert "window.scrollTo(0, scrollY)" not in _PAGE and "window.scrollTo(0, v.scrollY)" not in _PAGE


@needs_node
def test_the_rows_shown_come_back_for_the_same_list_only():
    """Dan (2026-11-17): going back keeps the rows opened with "Show N more", so a deep scroll lands
    where it was. The count is kept per list (query, kind, filters); another list starts at 25."""
    js = "var ROWS_SHOWN = 25;\n" + _fn("initialShownCount") + r"""
console.log(JSON.stringify({
  same: initialShownCount({ shown: 75, shownKey: 'customer||{}' }, 'customer||{}'),
  other: initialShownCount({ shown: 75, shownKey: 'customer||{}' }, 'customer||{"owner":"x"}'),
  none: initialShownCount(null, 'k'), small: initialShownCount({ shown: 10, shownKey: 'k' }, 'k'),
  junk: initialShownCount({ shown: '99', shownKey: 'k' }, 'k') }));"""
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    assert json.loads(out.stdout.strip().splitlines()[-1]) == {"same": 75, "other": 25, "none": 25, "small": 25, "junk": 25}


def test_search_and_browse_lists_keep_their_shown_count():
    assert "if (store) saveView(store, viewSearch, { shown: n, shownKey: listKey }, Date.now());" in _PAGE
    assert "viewSearch: here, listKey: q + '|' + kind + '|' + JSON.stringify(filt)" in _PAGE
    assert "viewSearch: browseHere, listKey: (lens || '') + JSON.stringify(picked) + '|' + cat," in _PAGE
    # the list key and the ResultList key are the same expression, so a restored count matches its list
    assert _PAGE.count("key: q + '|' + kind + '|' + JSON.stringify(filt), rows: shown") == 1
