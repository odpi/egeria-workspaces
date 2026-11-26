"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

The Solution Boundary views in type-explorer.html (the pure block between solution-boundary-pure:begin and :end), run under node with test_e64_cards_js's stub React.
Standalone (no app imports); skipped when node is not installed (the Portal container has none). The detail rows are the REAL output of
solution_architect_handler._serialize_boundary_detail on the REAL shape copied from egeria-python v6.3.4 (solution_boundary_retrieve_real_shape_..._5a8d6a12.json);
the cases that need a deeper, cyclic, empty or larger answer are SYNTHETIC and say so. READ-ONLY: no write control exists in the view.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_e64_cards_js import _PRELUDE  # noqa: E402

import solution_architect_handler as sah  # noqa: E402

_HERE = Path(__file__).resolve().parent
_HTML = (_HERE.parent / "type-explorer.html").read_text()
_FX = _HERE / "fixtures"
REAL = json.loads((_FX / "solution_boundary_retrieve_real_shape_2026_11_25_5a8d6a12.json").read_text())
DETAIL = sah._serialize_boundary_detail(REAL)             # what GET /api/solution/boundaries/{guid} returns for the real file
OUTER = REAL["elementHeader"]["guid"]
INNER = REAL["collectionMembers"][0]["relatedElement"]["elementHeader"]["guid"]
ROLE = REAL["collectionMembers"][0]["nestedElements"][0]["relatedElement"]["elementHeader"]["guid"]
BLUEPRINT = REAL["memberOfCollections"][0]["relatedElement"]["elementHeader"]["guid"]


def _block():
    m = re.search(r"/\* solution-boundary-pure:begin \*/(.*?)/\* solution-boundary-pure:end \*/", _HTML, re.S)
    assert m, "the solution-boundary-pure block is missing from type-explorer.html"
    return m.group(1)


def _run(body):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    r = subprocess.run([node, "-e", _PRELUDE + _block() + "\n" + body], capture_output=True, text=True, timeout=20)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


HANDLERS = ("var calls = [];"
            "var H = { onNavigateToBoundary: function(g) { calls.push(['boundary', g]); }, onNavigateToBlueprint: function(g) { calls.push(['blueprint', g]); },"
            " onNavigateToComponent: function(g) { calls.push(['component', g]); }, onNavigateToRole: function(g) { calls.push(['role', g]); },"
            " onNavigateToElement: function(i) { calls.push(['element', i.guid]); } };")


def _card(boundary, handlers=True):
    props = "Object.assign({ boundary: %s }, %s)" % (json.dumps(boundary), "H" if handlers else "{}")
    return _run(HANDLERS + "var t = render(React.createElement(SolutionBoundaryCard, " + props + "));"
                "var nodes = all(t, 'details').concat(all(t, 'div')).filter(function(n) { return n.p && n.p['data-test'] === 'member-node'; });"
                "out({ text: text(t), "
                "fields: all(t, 'div').filter(function(n) { return n.p && n.p['data-field']; }).map(function(n) { return n.p['data-field']; }), "
                "tests: all(t, 'div').concat(all(t, 'details')).filter(function(n) { return n.p && n.p['data-test']; }).map(function(n) { return n.p['data-test']; }), "
                "nodes: nodes.map(function(n) { return { tag: n.t, guid: n.p['data-guid'], depth: n.p['data-depth'], open: n.p.open }; }), "
                "buttons: all(t, 'button').map(text), tags: ['input','textarea','select','form','a'].filter(function(x) { return all(t, x).length; }), "
                "badges: all(t, 'span').filter(function(n) { return n.p && n.p.className === 'badge'; }).map(text) });")


# ── the real boundary ────────────────────────────────────────────────────────────────────────────────────────────

def test_the_header_fields_and_description_of_the_real_boundary():
    r = _card(DETAIL)
    assert "probe-boundary-1-renamed" in r["text"] and "SolutionBoundary" in r["badges"] and OUTER in r["text"]
    assert {"qualified-name", "status"} <= set(r["fields"]) and "probe::boundary::1" in r["text"]
    assert "boundary-description" in r["tests"] and "window P probe element, renamed" in r["text"]
    assert "version" not in r["fields"] and "lifecycle-status" not in r["fields"]               # a field the type does not return is not shown


def test_the_nested_boundary_is_a_collapsible_node_with_its_role_below_it():
    r = _card(DETAIL)
    by = {n["guid"]: n for n in r["nodes"]}
    assert by[INNER]["tag"] == "details" and by[INNER]["depth"] == 0 and by[INNER]["open"] is True        # a boundary with members collapses
    assert by[ROLE]["tag"] == "div" and by[ROLE]["depth"] == 1                                            # a leaf does not; it sits one level below
    assert "Members (2)" in r["text"] and "probe-boundary-2" in r["text"] and "probe-role-1" in r["text"]
    assert "SolutionActorRole" in r["badges"]


def test_view_buttons_open_each_member_in_its_own_view():
    r = _run(HANDLERS + "var t = render(React.createElement(SolutionBoundaryCard, Object.assign({ boundary: %s }, H)));"
             "all(t, 'button').forEach(function(b) { b.p.onClick(); });"
             "out({ calls: calls, labels: all(t, 'button').map(text) });" % json.dumps(DETAIL))
    assert ["boundary", INNER] in r["calls"] and ["role", ROLE] in r["calls"] and ["blueprint", BLUEPRINT] in r["calls"]
    assert all(lab.strip().startswith("View") for lab in r["labels"])


def test_the_blueprint_this_boundary_is_in_is_listed_as_a_member_of():
    r = _card(DETAIL)
    assert "member-of-boundary" in r["tests"] and "probe-blueprint-1" in r["text"]


def test_an_element_type_this_page_has_no_view_for_goes_to_the_generic_handler():
    node = {"guid": "x1", "typeName": "DesignModelBoundary", "displayName": "dmb"}
    r = _run(HANDLERS + "var h = boundaryOpenHandler(%s, H); h(); var none = boundaryOpenHandler(%s, {});" "out({ calls: calls, none: none === null });" % (json.dumps(node), json.dumps(node)))
    assert r["calls"] == [["element", "x1"]] and r["none"] is True


def test_help_text_carries_the_403_and_the_613_notes():
    r = _card(DETAIL)
    for needle in ("403 OMAG-GENERIC-HANDLERS-403-005", "Members must be removed first", "#613", "GUID or Version Identifier", "Display Name"):
        assert needle in r["text"], needle
    assert "boundary-help" in r["tests"]


# ── SYNTHETIC answers ─────────────────────────────────────────────────────────────────────────────────────────────

def _h(**kw):
    base = {"members": [], "nodeCount": 0, "maxDepth": 8, "maxNodes": 500, "complete": True, "notes": []}
    base.update(kw)
    return base


def _node(guid, typ="SolutionBoundary", children=None, **kw):
    return {"guid": guid, "typeName": typ, "displayName": guid, "qualifiedName": "q::" + guid, "relationshipType": "CollectionMembership", "isBoundary": typ == "SolutionBoundary",
            "cycle": False, "alsoLinkedTo": [], "children": children or [], "deeperNotShown": False, **kw}


def test_an_empty_boundary_says_it_has_no_members():
    # SYNTHETIC: a boundary with no members
    r = _card({"guid": "b", "displayName": "empty", "typeName": "SolutionBoundary", "memberHierarchy": _h(), "memberOf": []})
    assert "no-members" in r["tests"] and "This boundary has no members" in r["text"] and "Members (0)" in r["text"] and r["nodes"] == []
    assert "member-of-boundary" not in r["tests"] and "hierarchy-notes" not in r["tests"]


def test_a_cap_cycle_and_depth_note_are_shown_and_a_cycle_has_no_view_button():
    # SYNTHETIC: what the route returns when it stopped
    deep = _node("deep", deeperNotShown=True)
    cyc = _node("cyc", cycle=True)
    h = _h(members=[_node("a", children=[deep, cyc])], nodeCount=3, complete=False,
           notes=["More members are not shown: the view stops at 500 members.", "Deeper members are not shown: the view stops at 8 levels.", "A member that is already above it in the hierarchy was not followed again."])
    r = _card({"guid": "b", "displayName": "big", "typeName": "SolutionBoundary", "memberHierarchy": h, "memberOf": []})
    assert "hierarchy-notes" in r["tests"] and "500 members" in r["text"] and "8 levels" in r["text"] and "already above it" in r["text"]
    assert "(deeper members not shown)" in r["text"] and "(already above: not followed again)" in r["text"]
    assert len(r["buttons"]) == 2                                      # a, deep: the cyclic node offers no View


def test_nodes_nest_to_the_depth_given_and_indent_by_level():
    # SYNTHETIC: a chain of six nested boundaries
    chain = None
    for i in range(6, 0, -1):
        chain = _node(f"n{i}", children=[chain] if chain else None)
    r = _card({"guid": "b", "displayName": "chain", "typeName": "SolutionBoundary", "memberHierarchy": _h(members=[chain], nodeCount=6), "memberOf": []})
    assert [n["depth"] for n in r["nodes"]] == [0, 1, 2, 3, 4, 5]
    assert [n["open"] for n in r["nodes"][:5]] == [True, True, False, False, False]                # the first two levels open, the rest collapsed
    assert r["nodes"][5]["tag"] == "div"


def test_a_side_link_to_something_other_than_the_parent_is_shown():
    # SYNTHETIC
    n = _node("a", alsoLinkedTo=[{"guid": "o", "typeName": "SolutionBlueprint", "displayName": "other blueprint"}])
    r = _card({"guid": "b", "displayName": "x", "typeName": "SolutionBoundary", "memberHierarchy": _h(members=[n], nodeCount=1), "memberOf": []})
    assert "also linked to: SolutionBlueprint: other blueprint" in r["text"]


# ── the lists and the Member of boundary links ───────────────────────────────────────────────────────────────────

def _list(items, flt="", selected=None):
    return _run("var picked = [];"
                "var t = render(React.createElement(SolutionBoundaryList, { items: %s, filter: %s, selected: %s, emptyText: 'No solution boundaries found', onSelect: function(b) { picked.push(b.guid); } }));"
                "var rows = all(t, 'div').filter(function(n) { return n.p && n.p['data-guid']; });"
                "rows.forEach(function(n) { n.p.onClick(); });"
                "out({ text: text(t), tests: all(t, 'div').map(function(n) { return n.p && n.p['data-test']; }).filter(Boolean), picked: picked, sel: rows.map(function(n) { return n.p.className; }) });"
                % (json.dumps(items), json.dumps(flt), json.dumps(selected)))


def test_the_boundary_list_shows_its_rows_and_selects_one():
    items = [{"guid": OUTER, "displayName": "probe-boundary-1-renamed", "typeName": "SolutionBoundary"}, {"guid": INNER, "displayName": "probe-boundary-2", "typeName": "SolutionBoundary"}]
    r = _list(items, selected=INNER)
    assert "probe-boundary-1-renamed" in r["text"] and r["picked"] == [OUTER, INNER] and r["sel"] == ["tree-item", "tree-item sel"]


def test_the_boundary_list_filters_and_says_when_nothing_matches():
    items = [{"guid": "1", "displayName": "alpha"}, {"guid": "2", "displayName": "beta"}]
    assert _list(items, "alp")["picked"] == ["1"]
    assert "boundary-list-nomatch" in _list(items, "zzz")["tests"]


def test_the_empty_boundary_list_says_so():
    # the empty-state fixture (live has no SolutionBoundary today): a list of nothing is a normal answer, not an error
    r = _list([])
    assert "boundary-list-empty" in r["tests"] and "No solution boundaries found" in r["text"]


def test_member_of_boundary_lists_the_boundaries_and_is_silent_when_there_are_none():
    items = [{"guid": INNER, "displayName": "probe-boundary-2", "typeName": "SolutionBoundary", "qualifiedName": "probe::boundary::2"}]
    r = _run("var opened = []; var t = render(React.createElement(SolutionBoundaryLinks, { items: %s, onOpen: function(g) { opened.push(g); } }));"
             "var none = render(React.createElement(SolutionBoundaryLinks, { items: [] })); var nul = render(React.createElement(SolutionBoundaryLinks, {}));"
             "all(t, 'button').forEach(function(b) { b.p.onClick(); });"
             "out({ text: text(t), opened: opened, none: none === null, nul: nul === null });" % json.dumps(items))
    assert "Member of boundary (1)" in r["text"] and "probe-boundary-2" in r["text"] and r["opened"] == [INNER] and r["none"] and r["nul"]


# ── read only, and wired in ───────────────────────────────────────────────────────────────────────────────────────

def test_there_is_no_write_control_in_the_boundary_view():
    r = _card(DETAIL)
    assert r["tags"] == []                                              # no input, textarea, select, form or link
    assert all(b.strip().startswith("View") for b in r["buttons"])
    src = _block()
    assert not re.search(r"\b(?:fetch|egeriaFetch|XMLHttpRequest)\b|method\s*:|\b(?:POST|PUT|DELETE|PATCH)\b", src)
    assert "onSubmit" not in src and "onChange" not in src


def _slice(start, end):
    a = _HTML.index(start)
    return _HTML[a:_HTML.index(end, a)]


def test_the_boundary_effects_only_read():
    for part in (_slice("// Load solution boundaries and design model boundaries when", "// Fetch blueprint detail when selection changes"),
                 _slice("// Fetch boundary detail when selection changes", "function onNavigateToBoundary(guid)")):
        assert "egeriaFetch(" in part and not re.search(r"method\s*:|\b(?:POST|PUT|DELETE|PATCH)\b", part)
    # both lists are asked for, GET only
    assert "/api/solution/boundaries'" in _HTML and "/api/solution/design-model-boundaries'" in _HTML


def test_blueprint_and_component_detail_show_the_member_of_boundary_links_and_the_app_routes_a_boundary_here():
    bp = _slice("function SolutionBlueprintDetail(", "function SolutionComponentDetail(")
    comp = _slice("function SolutionComponentDetail(", "/* solution-role-pure:begin */")
    assert "SolutionBoundaryLinks, { items: blueprint.boundaries, onOpen: onNavigateToBoundary }" in bp
    assert "SolutionBoundaryLinks, { items: component.boundaries, onOpen: onNavigateToBoundary }" in comp
    assert "if (typeName === 'SolutionBoundary') { onNavigateToSolutionBoundary(guid); return; }" in _HTML
    assert "setSolutionNav({ kind: 'boundaries', guid: guid })" in _HTML and "k === 'boundaries'" in _HTML


def test_the_page_says_so_when_there_are_no_boundaries():
    assert "There are no solution boundaries on this platform yet" in _HTML and "No design model boundaries found" in _HTML


def _boundary_load_effect():
    """The body of the effect that loads the boundary lists, wrapped as a function of the values it reads, so node can run it with stubs."""
    a = _HTML.index("  useEffect(function() {\n    if (subNav !== 'boundaries') return;")
    b = _HTML.index("  }, [subNav, boundaryAttempt, inclTempl]);", a)
    body = _HTML[a:b].split("useEffect(function() {", 1)[1]
    assert "[subNav, boundaryAttempt, inclTempl]" in _HTML[b:b + 80]
    return body


def test_toggling_include_templates_after_the_first_load_reloads_the_boundary_lists():
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    js = ("var ref = { current: null }; var fetched = []; var states = []; var cleanups = [];"
          "function egeriaFetch(u) { fetched.push(u); return new Promise(function() {}); }"
          "function run(subNav, boundaryState, inclTempl) {"
          "  var setBoundaryState = function(s) { states.push(s); }, setBoundaryError = function() {}, setBoundaries = function() {}, setDmBoundaries = function() {}, creds = {}, boundaryLoadedTempl = ref;"
          "  var cleanup = (function() {" + _boundary_load_effect() + "})(); if (cleanup) cleanups.push(cleanup); return fetched.length; }"
          "var out1 = run('boundaries', 'idle', false);"       # first open: loads both lists, no query
          "var out2 = run('boundaries', 'ready', false);"      # same setting, already loaded: nothing
          "var out3 = run('boundaries', 'ready', true);"       # templates switched on after the load: reloads both, with the flag
          "var out4 = run('boundaries', 'ready', true);"       # nothing new
          "var out5 = run('boundaries', 'ready', false);"      # and off again: reloads without it
          "var out6 = run('roles', 'idle', true);"             # another tab: never loads
          "console.log(JSON.stringify({ counts: [out1, out2, out3, out4, out5, out6], fetched: fetched, states: states, cleanups: cleanups.length }));")
    r = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["counts"] == [2, 2, 4, 4, 6, 6]
    assert d["fetched"] == ["/api/solution/boundaries", "/api/solution/design-model-boundaries",
                            "/api/solution/boundaries?include_templates=true", "/api/solution/design-model-boundaries?include_templates=true",
                            "/api/solution/boundaries", "/api/solution/design-model-boundaries"]
    assert d["states"] == ["loading", "loading", "loading"] and d["cleanups"] == 3                  # each load returns a cleanup that drops its stale answer


def test_the_boundary_load_effect_drops_an_answer_for_an_older_setting():
    body = _boundary_load_effect()
    assert "boundaryLoadedTempl.current === inclTempl" in body and "if (!cancelled)" in body
    assert "return function() { cancelled = true; if (!done) boundaryLoadedTempl.current = null; }" in body and body.count("done = true") == 2


def test_leaving_mid_load_and_coming_back_loads_again_and_the_stale_answer_is_dropped():
    # SYNTHETIC timing: the answers are promises the test settles by hand
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    js = ("var ref = { current: null }; var calls = []; var pending = []; var states = []; var shown = [];"
          "function egeriaFetch(u) { return new Promise(function(resolve) { pending.push({ url: u, resolve: resolve }); calls.push(u); }); }"
          "function run(subNav, boundaryState, inclTempl, tag) {"
          "  var setBoundaryState = function(s) { states.push(tag + ':' + s); }, setBoundaryError = function() {}, creds = {}, boundaryLoadedTempl = ref;"
          "  var setBoundaries = function(b) { shown.push(tag + ':' + b.length); }, setDmBoundaries = function() {};"
          "  return (function() {" + _boundary_load_effect() + "})(); }"
          "function answer(n) { var a = pending.splice(0, n); a.forEach(function(p) { p.resolve({ ok: true, json: function() { return Promise.resolve({ boundaries: [{ guid: 'g' }] }); } }); }); return a.length; }"
          "async function main() {"
          "  var c1 = run('boundaries', 'idle', false, 'first');"        # open Boundaries: two requests, state loading
          "  c1();"                                                      # switch sub-tab before the answer arrives: the cleanup runs
          "  var c2 = run('boundaries', 'loading', false, 'second');"    # come back: the state is still 'loading', but the load must start again
          "  var afterReturn = calls.length;"
          "  answer(4); await new Promise(function(r) { setTimeout(r, 20); });"   # both loads' answers arrive; the first load's are stale
          "  c2();"                                                      # leave again, after the load completed
          "  var c3 = run('boundaries', 'ready', false, 'third');"       # come back: a completed load is not fetched again
          "  console.log(JSON.stringify({ afterReturn: afterReturn, total: calls.length, shown: shown, states: states, third: c3 === undefined }));"
          "} main();")
    r = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["afterReturn"] == 4 and d["total"] == 4 and d["third"] is True      # leaving mid-load reloads on return; a completed load does not refetch
    assert d["shown"] == ["second:1"]                                           # the stale answer of the first load is dropped
    assert d["states"] == ["first:loading", "second:loading", "second:ready"]
