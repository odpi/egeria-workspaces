# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
PO-86: the People section's karma leaderboard has three states, and the page must tell them apart.

    null / missing   the leaderboard could not be read (no pyegeria routine, no connection, the find raised, or
                     pyegeria 6.3.3 returned None because it could not read every record): the payload says why
                     in notMeasured["leaderboard"], and the page shows "Not measured: ... could not be read"
    []               a real answer: no contributors ("No karma records found.")
    [rows]           the leaderboard

The page used to render only when `Array.isArray(d.leaderboard)`, so a null left the "Loading…" placeholder on
screen for good. Never "Loading…" once the response has arrived, never "no contributors" for a null.

No Egeria needed: every Egeria call is stubbed. The page half is a source scan of egeria-overview.html (the same
kind of check test_overview_specs.py makes). Run where pyegeria and fastapi are importable:

    EGERIA_USER_PASSWORD=x python -m pytest test_overview_leaderboard_null.py -q
"""
import re
from pathlib import Path

import pytest

import overview_handler as oh

_HTML = Path(__file__).parent / "egeria-overview.html"


class _Expert:
    """Every find answers pyegeria's null for a find."""
    def find_metadata_elements(self, body):
        return "No elements found"


class _CE:
    def get_relationships(self, *a, **k):
        return None


@pytest.fixture
def people(monkeypatch):
    from pyegeria.view import overview_metrics as om
    monkeypatch.setattr(om, "_native_count_method", lambda *a, **k: None)
    monkeypatch.setattr(oh, "_expert", lambda *a, **k: _Expert())
    monkeypatch.setattr(oh, "_make", lambda *a, **k: _CE())
    monkeypatch.setattr(oh, "_count_scope", lambda *fns: oh.VIEWER)
    monkeypatch.setattr(oh, "people_counts", lambda mgr, as_of, strict=False, scope=None: {
        "persons": 4, "teams": 1, "organizations": 1, "itProfiles": 0, "communities": 2})

    def compute():
        return oh._compute_people(None, None, None, None, None)
    return compute


# ── server side ──────────────────────────────────────────────────────────────

def test_a_leaderboard_that_returns_none_is_null_and_says_why(people, monkeypatch):
    monkeypatch.setattr(oh, "karma_leaderboard", lambda expert, as_of: None)
    p = people()
    assert p["leaderboard"] is None
    assert p["notMeasured"].get("leaderboard")


def test_a_leaderboard_that_raises_is_null_and_says_why(people, monkeypatch):
    def boom(expert, as_of):
        raise RuntimeError("find failed")
    monkeypatch.setattr(oh, "karma_leaderboard", boom)
    p = people()
    assert p["leaderboard"] is None
    assert "RuntimeError" in p["notMeasured"]["leaderboard"]


def test_a_missing_leaderboard_routine_is_null_and_says_why(people, monkeypatch):
    monkeypatch.setattr(oh, "karma_leaderboard", None)
    p = people()
    assert p["leaderboard"] is None
    assert p["notMeasured"].get("leaderboard")


def test_an_empty_leaderboard_stays_an_empty_list_with_no_reason(people, monkeypatch):
    monkeypatch.setattr(oh, "karma_leaderboard", lambda expert, as_of: [])
    p = people()
    assert p["leaderboard"] == []
    assert "leaderboard" not in p["notMeasured"]


def test_a_leaderboard_with_rows_is_unchanged(people, monkeypatch):
    rows = [{"name": "A", "karmaPoints": 5, "anchorGuid": "g", "anchorType": "Person"}]
    monkeypatch.setattr(oh, "karma_leaderboard", lambda expert, as_of: rows)
    p = people()
    assert p["leaderboard"] == rows and "leaderboard" not in p["notMeasured"]


# ── page side (source scan) ──────────────────────────────────────────────────

def _leaderboard_block() -> str:
    html = _HTML.read_text()
    start = html.index("var leadEl = document.getElementById('leaderboard');")
    end = html.index("// Engagement over time", start)
    return html[start:end]


def test_the_page_has_a_branch_for_a_leaderboard_that_could_not_be_read():
    block = _leaderboard_block()
    assert "Array.isArray(d.leaderboard)" in block
    # the unreadable branch is the one that is NOT the array branch, and it names the failure and the reason
    not_read = re.search(r"else if \(leadEl\)\s*\{(?P<body>.*)\}\s*$", block, re.S)
    assert not_read, "no `else if (leadEl)` branch for a null or missing leaderboard"
    body = not_read.group("body")
    assert "could not be read" in body and "nmReason('leaderboard'" in body
    assert "No karma records found." not in body       # never "no contributors" for a null


def test_the_empty_array_keeps_its_own_text_and_differs_from_the_unreadable_text():
    block = _leaderboard_block()
    assert block.count("No karma records found.") == 1
    assert "d.leaderboard.length === 0" in block
    assert block.index("No karma records found.") < block.index("could not be read")


def test_the_loading_placeholder_is_replaced_in_every_branch():
    block = _leaderboard_block()
    # the array branch and the unreadable branch each clear the placeholder before drawing
    assert block.count("leadEl.innerHTML = '';") == 2


# ── page side (the block itself, run under node against a minimal DOM) ──────

_HARNESS = r"""
function mk(tag){ return {tag:tag, children:[], style:{}, className:'', _t:'',
  set innerHTML(v){ this.children = []; }, get innerHTML(){ return ''; },
  set textContent(v){ this._t = v; }, get textContent(){ return this._t; },
  appendChild(c){ this.children.push(c); return c; } }; }
var lead = mk('div'); lead.children.push({_t:'Loading…', children:[]});
var document = { getElementById: function(id){ return id === 'leaderboard' ? lead : null; },
                 createElement: mk };
var store = {}; var notes = [];
function uncNote(id, m){ notes.push([id, m]); }
function uncMark(){ return null; }
function nmReason(key){ return NM; }
function fmt(n){ return String(n); }
function texts(e){ return [e._t].concat((e.children||[]).map(texts).flat()).filter(Boolean); }
var d = DATA;
%s
console.log(JSON.stringify({texts: lead.children.map(texts).flat(), n: lead.children.length}));
"""


def _run_block(data_js: str, reason_js: str = "null") -> dict:
    import json
    import shutil
    import subprocess
    if shutil.which("node") is None:
        pytest.skip("node is not installed")
    js = "var NM=%s;\n" % reason_js + _HARNESS.replace("DATA", data_js) % _leaderboard_block()
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout
    return json.loads(out.strip().splitlines()[-1])


@pytest.mark.parametrize("data", ["{leaderboard: null}", "{}", "{leaderboard: undefined}"])
def test_run_a_null_or_missing_leaderboard_shows_could_not_be_read(data):
    r = _run_block(data, '"the contribution record find failed (RuntimeError)"')
    assert r["n"] == 1
    assert r["texts"] == ["Not measured: the karma leaderboard could not be read "
                          "(the contribution record find failed (RuntimeError))"]


def test_run_a_null_leaderboard_without_a_reason_still_says_it_could_not_be_read():
    r = _run_block("{leaderboard: null}")
    assert r["texts"] == ["Not measured: the karma leaderboard could not be read"]


def test_run_an_empty_leaderboard_says_no_karma_records_not_could_not_be_read():
    r = _run_block("{leaderboard: []}")
    assert r["texts"] == ["No karma records found."]


def test_run_a_leaderboard_with_rows_draws_the_rows():
    r = _run_block("{leaderboard: [{name:'Ada', karmaPoints: 9}, {name:'Bo', karmaPoints: 4}]}")
    assert r["n"] == 2 and "Ada" in r["texts"] and "Bo" in r["texts"]
    assert not any("could not be read" in t or "Loading" in t for t in r["texts"])
