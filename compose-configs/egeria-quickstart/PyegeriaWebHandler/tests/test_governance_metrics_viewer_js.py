"""Egeria Audit's Governance Metrics tab reads as Audit's selected viewer (governance-metrics.html,
embed mode). The pure viewer-receiving helpers run under node; they skip when node is not
installed (the container has none). The wiring checks run everywhere."""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

DIR = Path(__file__).resolve().parent.parent
GM = (DIR / "governance-metrics.html").read_text()
AUDIT = (DIR / "egeria-audit.html").read_text()


def _fn(src, name):
    m = re.search(r"function " + name + r"\(.*?\n\}\n", src, re.S)
    assert m, f"{name} not found"
    return m.group(0)


def _run(body):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    js = _fn(GM, "gmReceiveViewer") + _fn(GM, "gmTimeout") + _fn(GM, "gmLoadTicket") + body
    out = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_viewer_before_the_timeout_starts_as_that_viewer():
    r = _run("""
var gm = {viewer:null, done:false, resolve:function(){ gm.started = (gm.started||0)+1; }}, reloads = 0;
var a = gmReceiveViewer(gm, {type:'egeria-viewer', token:'T1', userId:'peter', label:'peter'}, function(){ reloads++; });
var t = gmTimeout(gm);
console.log(JSON.stringify({a:a, t:t, started:gm.started, reloads:reloads, token:gm.viewer.token}));""")
    assert r == {"a": "first", "t": False, "started": 1, "reloads": 0, "token": "T1"}


def test_late_viewer_after_the_timeout_reloads_so_list_note_and_runs_agree():
    r = _run("""
var gm = {viewer:null, done:false, resolve:function(){ gm.started = (gm.started||0)+1; }}, reloads = 0;
var t = gmTimeout(gm);                      // 2 s passed: started as the service user
var a = gmReceiveViewer(gm, {type:'egeria-viewer', token:'T1', userId:'peter', label:'peter'}, function(){ reloads++; });
console.log(JSON.stringify({t:t, a:a, started:gm.started, reloads:reloads, token:gm.viewer.token}));""")
    # The late viewer is taken AND the list is fetched again as that viewer (not mixed identity).
    assert r == {"t": True, "a": "reload", "started": 1, "reloads": 1, "token": "T1"}


def test_same_viewer_again_does_not_reload_and_a_new_one_does():
    r = _run("""
var gm = {viewer:null, done:false, resolve:null}, reloads = 0, f = function(){ reloads++; };
gmReceiveViewer(gm, {type:'egeria-viewer', token:'T1', label:'peter'}, f);
var same = gmReceiveViewer(gm, {type:'egeria-viewer', token:'T1', label:'peter'}, f);
var other = gmReceiveViewer(gm, {type:'egeria-viewer', token:'T2', label:'gary'}, f);
var junk = gmReceiveViewer(gm, {type:'something-else'}, f);
console.log(JSON.stringify({same:same, other:other, junk:junk, reloads:reloads, label:gm.viewer.label}));""")
    assert r == {"same": "same", "other": "reload", "junk": "ignored", "reloads": 1, "label": "gary"}


def test_an_older_load_answering_last_is_dropped():
    # Service-user load (1) starts; the viewer arrives and its load (2) starts; (2) answers first,
    # then (1) answers last. Only (2) may change the page.
    r = _run("""
var gm = {}, state = {who: null}, applied = [];
function load(who) { var cur = gmLoadTicket(gm); return function answer() { if (!cur()) return; state.who = who; applied.push(who); }; }
var first = load('service-user');
var second = load('peter');
second(); first();
console.log(JSON.stringify({who: state.who, applied: applied, seq: gm.seq}));""")
    assert r == {"who": "peter", "applied": ["peter"], "seq": 2}


def test_a_single_load_is_current_and_a_newer_one_retires_it():
    r = _run("""
var gm = {};
var a = gmLoadTicket(gm), aBefore = a();
var b = gmLoadTicket(gm);
console.log(JSON.stringify({aBefore: aBefore, aAfter: a(), b: b()}));""")
    assert r == {"aBefore": True, "aAfter": False, "b": True}


def test_fetch_is_guarded_and_a_new_viewer_shows_loading_first():
    assert "var current = gmLoadTicket(GM);" in GM
    assert ".then(function(d){ if (!current()) return; STATE.metrics" in GM
    assert ".catch(function(e){ if (!current()) return; STATE.error" in GM
    assert "if (!STATE.loaded) { document.getElementById('app').innerHTML = '<div class=\"loading\">Loading…</div>'; return; }" in GM


def test_wiring_uses_the_helpers_and_checks_origin_and_source():
    assert ("gmReceiveViewer(GM, e.data, function(){ VIEWER = GM.viewer; STATE.loaded = false; route(); "
            "fetchMetrics().then(route); });") in GM
    assert "setTimeout(function(){ gmTimeout(GM); }, 2000);" in GM
    assert "if (e.origin !== location.origin || e.source !== window.parent) return;" in GM
    assert "_viewerReady.then(fetchMetrics).then(route);" in GM
    # Audit: same-origin only, frame source checked, token never in the key or a URL
    assert "f.contentWindow.postMessage(viewer, window.location.origin)" in AUDIT
    assert "e.source !== ref.current.contentWindow" in AUDIT
    assert "_tokenTag(creds && creds.token)" in AUDIT
    assert "token.slice(" not in AUDIT
    assert "embed=1&token" not in AUDIT and "token=" not in GM.split("<script>", 1)[0]
