"""Egeria 6.4 cards in type-explorer.html: the pure helpers and hook-free tables between e64-pure:begin and
e64-pure:end, run under node with a stub React that renders to a plain tree. Standalone (needs no app
imports); skipped when node is not installed (the Portal container has none).

Rows are shaped like e64_handler.py's (tests/test_e64_decisions.py pins those against the handler).
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

_DIR = Path(__file__).resolve().parent.parent
HTML = (_DIR / "type-explorer.html").read_text()
SHARED = (_DIR / "static" / "egeria-shared-ui.js").read_text()

# A stub React: createElement builds {t, p, c}; components are plain functions of props (no hooks here).
_PRELUDE = r"""
var React = { createElement: function(t, p) { return { t: t, p: p || {}, c: Array.prototype.slice.call(arguments, 2) }; },
              Fragment: 'frag' };
var _elementIsLinkable = function(r) { return r.typeName !== 'Unlinkable'; };
function render(n) {
  if (n === null || n === undefined || n === false || n === true) return null;
  if (Array.isArray(n)) return n.map(render).filter(function(x) { return x !== null; });
  if (typeof n !== 'object') return n;
  if (typeof n.t === 'function') return render(n.t(Object.assign({}, n.p, n.c.length ? { children: n.c } : {})));
  return { t: n.t, p: n.p, c: render(n.c) };
}
function text(n) {
  if (n === null || n === undefined) return '';
  if (Array.isArray(n)) return n.map(text).join(' ');
  if (typeof n !== 'object') return String(n);
  return text(n.c);
}
function all(n, tag, out) {
  out = out || [];
  if (Array.isArray(n)) { n.forEach(function(x) { all(x, tag, out); }); return out; }
  if (n && typeof n === 'object') { if (n.t === tag) out.push(n); all(n.c, tag, out); }
  return out;
}
function rows(tree) { return all(tree, 'tbody').length ? all(all(tree, 'tbody')[0], 'tr') : []; }
function out(x) { console.log(JSON.stringify(x)); }
"""


def _block():
    sh = re.search(r"/\* e64-shared:begin \*/(.*?)/\* e64-shared:end \*/", SHARED, re.S)
    assert sh, "the e64-shared block is missing from static/egeria-shared-ui.js"
    m = re.search(r"/\* e64-pure:begin \*/(.*?)/\* e64-pure:end \*/", HTML, re.S)
    assert m, "the e64-pure block is missing from type-explorer.html"
    return sh.group(1) + "\nE64UI.isLinkable = _elementIsLinkable;\n" + m.group(1)


def _run(body):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    js = _PRELUDE + _block() + "\n" + body
    r = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def _arow(rel, el, name, label, when, **kw):
    return {"relationshipGuid": rel, "guid": el, "typeName": "GlossaryTerm", "displayName": name, "label": label,
            "assessmentTime": when, "assessor": kw.get("assessor", ""), "assessorTypeName": kw.get("assessorTypeName", ""),
            "assessorPropertyName": "", "expiryTime": "", "notes": kw.get("notes", ""), "description": ""}


ONE = [_arow("as-1", "term-1", "Lineage", "Initial review", "2026-02-01T10:00:00.000+00:00", assessor="Erin")]
TWO_OF_ONE = [
    _arow("as-2", "term-1", "Lineage", "Re-review", "2026-05-01T10:00:00.000+00:00"),
    _arow("as-1", "term-1", "Lineage", "Initial review", "2026-02-01T10:00:00.000+00:00"),
]
MANY = TWO_OF_ONE + [_arow("as-3", "term-2", "Pipelines", "Initial review", "2026-02-02T10:00:00.000+00:00"),
                     _arow("as-4", "term-3", "Access", "Initial review", "")]


def _table(rows, st):
    return _run(f"var t = render(React.createElement(DecisionAssessmentsTable, {{ rows: {json.dumps(rows)}, st: {json.dumps(st)}, onNavigateToElement: function(){{}} }}));"
                "out({ text: text(t), keys: rows(t).map(function(r) { return r.p['data-row-key']; }), "
                "      cells: rows(t).map(function(r) { return all(r, 'td').map(text); }) });")


# ── 0, 1 and many rows ───────────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("st,words", [
    ({"state": "none"}, "None recorded."),
    ({"state": "not-read"}, "Not read: this list was not asked for."),
    ({"state": "not-known"}, "Not known:"),
    ({"state": "needs-6.4", "words": "The Decision card needs Egeria 6.4 (odpi/egeria#9463 ...)"}, "needs Egeria 6.4"),
])
def test_zero_rows_say_why_in_words(st, words):
    r = _table([], st)
    assert r["keys"] == [] and words in r["text"]


def test_none_and_not_read_are_different_words():
    assert _table([], {"state": "none"})["text"] != _table([], {"state": "not-read"})["text"]


def test_one_row():
    r = _table(ONE, {"state": "read"})
    assert r["keys"] == ["as-1"]
    assert r["cells"][0][0].startswith("Lineage") and "Initial review" in r["cells"][0][1]
    assert "of this element" not in r["text"]           # a single assessment is not numbered


def test_many_rows_grouped_by_element_with_a_missing_time_said_in_words():
    r = _table(MANY, {"state": "read"})
    assert r["keys"] == ["as-4", "as-1", "as-2", "as-3"]       # Access, Lineage x2 (oldest first), Pipelines
    assert r["cells"][0][2] == "not recorded"


def test_two_assessments_of_one_element_are_two_rows_numbered_oldest_first():
    r = _table(TWO_OF_ONE, {"state": "read"})
    assert r["keys"] == ["as-1", "as-2"]
    assert "assessment 1 of 2 of this element" in r["cells"][0][1]
    assert "assessment 2 of 2 of this element" in r["cells"][1][1]


def test_rows_without_a_relationship_guid_still_get_distinct_keys():
    rows = [dict(ONE[0], relationshipGuid=""), dict(ONE[0], relationshipGuid="", label="Again")]
    assert len(set(_table(rows, {"state": "read"})["keys"])) == 2


def test_outcomes_table_zero_one_and_needs_6_4():
    o = [{"relationshipGuid": "out-1", "guid": "p-1", "typeName": "Project", "displayName": "Rollout",
          "label": "Rollout", "importance": "High", "disposition": "Started", "description": ""}]
    r = _run(f"var a = render(React.createElement(DecisionOutcomesTable, {{ rows: {json.dumps(o)}, st: {{state:'read'}} }}));"
             "var b = render(React.createElement(DecisionOutcomesTable, { rows: [], st: {state:'none'} }));"
             "var c = render(React.createElement(DecisionOutcomesTable, { rows: [], st: {state:'needs-6.4', words:'needs Egeria 6.4 here'} }));"
             "out([rows(a).length, text(a), text(b), text(c)]);")
    assert r[0] == 1 and "Started" in r[1]
    assert r[2] == "None recorded." and r[3] == "needs Egeria 6.4 here"


# ── dates against now ────────────────────────────────────────────────────────────────────────────────────

NOW = "Date.parse('2026-11-21T12:00:00Z')"


def _flags(d):
    return _run(f"out(decisionDateFlags({json.dumps(d)}, {NOW}));")


def test_overdue_review_and_expired():
    f = _flags({"nextReviewTime": "2026-09-01T00:00:00.000+00:00", "expiryTime": "2026-10-01T00:00:00.000+00:00"})
    assert f["review"]["state"] == "overdue" and f["review"]["text"].startswith("Review overdue (was due 1 Sep")
    assert f["expiry"]["state"] == "expired" and f["expiry"]["text"].startswith("Expired on 1 Oct")


def test_future_review_is_scheduled_and_future_expiry_active():
    f = _flags({"nextReviewTime": "2027-03-01T00:00:00Z", "expiryTime": "2027-06-01T00:00:00Z"})
    assert (f["review"]["state"], f["expiry"]["state"]) == ("scheduled", "active")
    assert f["review"]["text"].startswith("Next review 1 Mar 2027")


def test_missing_dates_are_words_never_on_time():
    f = _flags({})
    assert f["review"] == {"state": "none", "text": "No review date", "tone": "warn"}
    assert f["expiry"]["state"] == "none" and f["expiry"]["text"] == "No expiry date"
    assert f["review"]["tone"] != "ok"


def test_an_unreadable_date_is_said_not_guessed():
    f = _flags({"nextReviewTime": "next spring"})
    assert f["review"]["state"] == "unreadable" and "not readable: next spring" in f["review"]["text"]


def test_dates_panel_renders_the_flags_and_not_recorded():
    r = _run(f"var t = render(React.createElement(DecisionDatesPanel, {{ detail: {{ startTime: '2026-01-01T00:00:00Z' }}, nowMs: {NOW} }}));"
             "out(text(t));")
    assert "No review date" in r and "No expiry date" in r and "not recorded" in r and "1 Jan 2026" in r


# ── header and body ──────────────────────────────────────────────────────────────────────────────────────

def test_header_badges_say_not_recorded_for_missing_values():
    r = _run("out(text(render(React.createElement(DecisionHeaderBadges, { detail: { disposition: 'Approved' } }))));")
    assert "Disposition: Approved" in r and "Importance: not recorded" in r and "Status: not recorded" in r


def test_body_lists_implications_and_says_when_empty():
    r = _run("out([text(render(React.createElement(DecisionBody, { detail: { summary: 'S', implications: ['a', 'b'], notes: 'N' } }))),"
             "     text(render(React.createElement(DecisionBody, { detail: {} })))]);")
    assert "Summary S" in r[0] and "Implications a b" in r[0] and "Notes N" in r[0]
    assert r[1].startswith("No summary, scope, usage, implications or notes")


# ── wiring (the pyegeria-spa-add-tab checks) ─────────────────────────────────────────────────────────────

def test_decisions_section_is_wired():
    assert "'decisions': 'Decisions'," in HTML                                    # SECTION_LABELS
    assert "section: 'decisions'," in HTML                                        # home-page card
    assert "{ id: 'decisions'," in HTML                                           # nav menu
    assert "section === 'decisions'\n      ? React.createElement(DecisionsView" in HTML   # render switch
    assert HTML.count("'statements-of-applicability','decisions'") == 2           # valid hashes + isActive
    assert "if (typeName === 'Decision' || superTypes.indexOf('Decision') !== -1) { onNavigateToDecision(guid); return; }" in HTML
    assert "if (item.typeName === 'Decision' || superTypes.indexOf('Decision') !== -1) return true;" in HTML
    assert "'Decision':        { color:" in HTML                                  # DD_TYPE_NAV


def test_the_page_parses():
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    scripts = re.findall(r"<script(?:(?!src)[^>])*>(.*?)</script>", HTML, re.S)
    r = subprocess.run([node, "--check", "-"], input="\n".join(scripts), capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr[:2000]


# ── C2: DataValue / LiteralDataValue ─────────────────────────────────────────────────────────────────────

def _prow(rel, el, name, position, set_=None):
    return {"relationshipGuid": rel, "guid": el, "typeName": "DataValue", "displayName": name, "label": "",
            "description": "", "position": position, "positionSet": (position is not None) if set_ is None else set_}


EMB = [_prow("e-3", "d3", "Third", 3), _prow("e-0", "d0", "Unset (0)", None), _prow("e-1", "d1", "First", 1),
       _prow("e-n", "dn", "Another unset", None)]


def _ptable(rows, st, extra=""):
    return _run(f"var t = render(React.createElement(E64PositionedTable, {{ rows: {json.dumps(rows)}, st: {json.dumps(st)}{extra} }}));"
                "out({ text: text(t), keys: rows(t).map(function(r) { return r.p['data-row-key']; }), "
                "      cells: rows(t).map(function(r) { return all(r, 'td').map(text); }) });")


def test_embedded_values_ordered_by_position_and_unset_said_in_words():
    r = _ptable(EMB, {"state": "read"})
    assert r["keys"] == ["e-1", "e-3", "e-n", "e-0"]
    assert [c[1] for c in r["cells"]] == ["position 1", "position 3", "position unset", "position unset"]


def test_positioned_table_zero_one_many():
    assert _ptable([], {"state": "none"})["text"] == "None recorded."
    assert "Needs" in _ptable([], {"state": "needs-6.4"})["text"]
    assert _ptable(EMB[:1], {"state": "read"})["keys"] == ["e-3"]
    assert len(_ptable(EMB, {"state": "read"})["keys"]) == 4


def test_stored_in_has_no_position_column():
    r = _ptable([_prow("s-1", "f1", "limits.csv", None)], {"state": "read"}, ", withPosition: false")
    assert len(r["cells"][0]) == 3 and "position" not in r["text"]


@pytest.mark.parametrize("value,expect", [
    ({"kind": "literal", "dataValue": "3"}, ["Literal value 3"]),
    ({"kind": "list", "dataValueList": ["a", "b"]}, ["Value list (2)", "1 a", "2 b"]),
    ({"kind": "map", "dataValueMap": {"retries": "3", "backoff": "2s"}}, ["Value map (2)", "backoff 2s", "retries 3"]),
    ({"kind": "empty"}, ["No value is recorded"]),
    ({"kind": "not-literal"}, ["holds no value of its own"]),
])
def test_value_panel_literal_list_map_and_words(value, expect):
    t = _run(f"out(text(render(React.createElement(DataValueValuePanel, {{ value: {json.dumps(value)} }}))));")
    for e in expect:
        assert e in t, (e, t)


def test_data_values_section_is_wired():
    assert "'data-values': 'Data Values'," in HTML
    assert "section: 'data-values'," in HTML and "{ id: 'data-values'," in HTML
    assert "section === 'data-values'\n      ? React.createElement(DataValuesView" in HTML
    assert HTML.count("'decisions','data-values'") == 2
    assert "{ onNavigateToDataValue(guid); return; }" in HTML
    assert "item.typeName === 'LiteralDataValue' || superTypes.indexOf('DataValue') !== -1) return true;" in HTML
    assert "'DataValue':       { color:" in HTML and "'LiteralDataValue': { color:" in HTML


# ── C3: the 6.4 rows on an existing card (E64RelatedRows in egeria-shared-ui.js) ──────────────────────────

def _list(key, label, rows, state="read"):
    return {"key": key, "label": label, "rows": rows, "st": {"state": state}}


def _related(sections, carries=True, branch=None, **kw):
    return {"guid": "g", "typeName": "GlossaryTerm", "carries": carries, "branch": branch, "sections": sections, **kw}


def _render_related(data):
    return _run(f"var t = render(React.createElement(E64RelatedRows, {{ data: {json.dumps(data)}, onNavigateToElement: function(){{}} }}));"
                "out({ text: text(t), lists: all(t, 'div').filter(function(d) { return d.p['data-list']; }).map(function(d) {"
                "  return [d.p['data-list'], rows(d).map(function(r) { return r.p['data-row-key']; }), text(d)]; }) });")


DEC = lambda rel, name, label, when: {"relationshipGuid": rel, "guid": "dec-" + name, "typeName": "Decision",
                                      "displayName": name, "label": label, "assessmentTime": when, "assessor": "Erin"}


def test_related_needs_6_4_is_one_line_of_words():
    r = _render_related({"needs64": True, "words": "Decisions, project targets ... needs Egeria 6.4 (x): runs Egeria 6.3."})
    assert r["text"] == "Decisions, project targets ... needs Egeria 6.4 (x): runs Egeria 6.3." and r["lists"] == []


def test_related_all_none_is_one_line_and_not_known_is_not_none():
    secs = [{"key": "decisions", "title": "Decisions", "lists": [_list("associatedDecisions", "Outcome of", [], "none")]},
            {"key": "projects", "title": "Projects", "lists": [_list("workedOnByProjects", "Worked on by projects", [], "none")]}]
    r = _render_related(_related(secs))
    assert r["text"] == "None recorded: no decisions, projects are linked to this element."
    secs[0]["lists"][0]["st"] = {"state": "not-known"}
    r = _render_related(_related(secs, carries=None))
    assert "None recorded: no" not in r["text"] and "Not known:" in r["text"] and "Branch: not known" in r["text"]


def test_related_zero_one_many_and_two_assessments_for_one_decision():
    secs = [{"key": "decisions", "title": "Decisions", "lists": [
        _list("associatedDecisions", "Outcome of", [dict(DEC("o-1", "Adopt", "Rollout", ""), importance="High")]),
        _list("assessmentDecisions", "Assessed for", [DEC("a-2", "Adopt", "Re-review", "2026-05-01T00:00:00Z"),
                                                      DEC("a-1", "Adopt", "First", "2026-02-01T00:00:00Z"),
                                                      DEC("a-3", "Retire", "Only", "")]),
    ]}, {"key": "projects", "title": "Projects", "lists": [_list("workedOnByProjects", "Worked on by projects", [], "none")]}]
    lists = {k: (keys, t) for k, keys, t in _render_related(_related(secs))["lists"]}
    assert lists["associatedDecisions"][0] == ["o-1"] and "High" in lists["associatedDecisions"][1]
    assert lists["assessmentDecisions"][0] == ["a-1", "a-2", "a-3"]
    assert "assessment 1 of 2 for this decision" in lists["assessmentDecisions"][1]
    assert "not recorded" in lists["assessmentDecisions"][1]
    assert lists["workedOnByProjects"][0] == [] and "None recorded." in lists["workedOnByProjects"][1]


def test_related_positions_and_cardinality_in_words():
    rows = [{"relationshipGuid": "v-0", "guid": "st-0", "typeName": "PrimitiveSchemaType", "displayName": "Z",
             "position": None, "positionSet": False, "minCardinality": None, "maxCardinality": 3},
            {"relationshipGuid": "v-2", "guid": "st-2", "typeName": "PrimitiveSchemaType", "displayName": "A",
             "position": 2, "positionSet": True, "minCardinality": 1, "maxCardinality": None}]
    secs = [{"key": "variables", "title": "Process variables", "lists": [_list("processVariableTypes", "Variable types", rows)]}]
    (k, keys, t), = _render_related(_related(secs))["lists"]
    assert keys == ["v-2", "v-0"]
    assert "position 2" in t and "position unset" in t
    assert "min 1, max not set" in t and "min not set, max 3" in t


def test_branch_badge():
    r = _render_related(_related([], branch={"displayName": "main", "purpose": "default branch", "scope": "",
                                             "url": "https://github.com/odpi/egeria/tree/main"}))
    assert "Branch: main" in r["text"] and "default branch" in r["text"]
    assert "Branch" not in _render_related(_related([], branch=None))["text"]      # known: no Branch, no badge


def test_the_related_panel_is_on_every_explorer_card_and_the_catalogs():
    comments = HTML.count("React.createElement(EgeriaCommentsSection, { guid: ")
    panels = HTML.count("React.createElement(E64RelatedPanel, { guid: ")
    assert comments == panels == 24       # 23 + the Models and Runs card frame (both its cards)
    tc = (_DIR / "tech-catalog.html").read_text()
    assert tc.count("React.createElement(E64RelatedPanel, { guid: item.guid })") == 3
    assert "E64UI.isLinkable = _elementIsLinkable;" in HTML
    for page in ("type-explorer.html", "tech-catalog.html"):
        assert "egeria-shared-ui.js?v=2026-11-22-e64" in (_DIR / page).read_text()


def test_type_nav_map_routes_the_6_4_types_to_their_explorer_sections():
    m = json.loads((_DIR / "static" / "type-nav-map.json").read_text())
    assert m["Decision"] == {"explorerHash": "decisions"}
    assert m["DataValue"] == m["LiteralDataValue"] == {"explorerHash": "data-values"}
