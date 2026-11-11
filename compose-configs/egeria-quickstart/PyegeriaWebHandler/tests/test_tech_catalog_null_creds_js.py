"""The Catalog (tech-catalog.html) views must render before any connection is
saved. Run under node; skipped when node is not installed (the Portal container
has none).

The App starts with creds = null and only sets it once a persona is chosen (or
server-managed auth answers). NamespacesView, SurveyTypesView and
GovernanceProcessesView read creds.url in their effect dependency lists, which
React evaluates during render: with no saved connection the TypeError blanked
the whole SPA (seen 2026-11-11 opening Namespaces from the Catalog home in a
fresh browser; the public demo's first visitors hit the same path).

Each view's function is pulled out of the page and called directly with stub
hooks (render-time code such as dependency lists runs for real; effects are
run too, against a fetch stub). Any other global the view touches resolves to
a harmless stub through a `with` scope, so the test exercises only the view's
own code."""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
TC = (ROOT / "tech-catalog.html").read_text()

VIEWS = ["NamespacesView", "SurveyTypesView", "GovernanceProcessesView"]

HARNESS = r"""
var deps = [], fetched = [];
function stub() { return stub; }
stub.then = undefined;   // never look like a promise
var React = {
  useState: function(init) { return [typeof init === 'function' ? init() : init, function() {}]; },
  useEffect: function(fn, d) { deps.push(d); try { fn(); } catch (e) { throw e; } },
  useRef: function(v) { return { current: v }; },
  useCallback: function(fn) { return fn; },
  useMemo: function(fn) { return fn(); },
  useContext: function() { return null; },
  createElement: function(type, props) { return { type: type, props: props || {} }; },
  Fragment: 'Fragment',
};
var fake = {
  React: React,
  useState: React.useState, useEffect: React.useEffect, useRef: React.useRef,
  useCallback: React.useCallback, useMemo: React.useMemo,
  fetchWithToken: function(url, creds) {
    fetched.push([url, creds]);
    return { then: function() { return this; }, catch: function() { return this; } };
  },
};
var scope = new Proxy(fake, {
  has: function(t, k) { return typeof k === 'string' && !(k in globalThis && k !== 'fetch'); },
  get: function(t, k) { return k in t ? t[k] : stub; },
});
var VIEW = (function() { with (scope) { return eval('(' + SRC + ')'); } })();
var out;
try {
  var el = VIEW({ creds: null, navTarget: null, onNavigate: function() {} });
  out = { ok: true, rendered: !!el, deps: deps.map(function(d) { return d && d.length; }), fetched: fetched.length };
} catch (e) {
  out = { ok: false, error: String(e) };
}
console.log(JSON.stringify(out));
"""


def _render(view):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    m = re.search(r"function " + view + r"\(\{[^)]*\}\) \{.*?\n\}\n", TC, re.S)
    assert m, f"{view} not found in tech-catalog.html"
    helper = re.search(r"function credsDep\(creds\) \{.*?\n\}\n", TC, re.S)
    assert helper, "credsDep not found in tech-catalog.html"
    # The real helper is a top-level global, so the `with` scope defers to it.
    js = helper.group(0) + "var SRC = " + json.dumps(m.group(0)) + ";\n" + HARNESS
    out = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout.strip().splitlines()[-1])


def test_creds_dep_is_null_safe_and_tracks_the_connection():
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    helper = re.search(r"function credsDep\(creds\) \{.*?\n\}\n", TC, re.S).group(0)
    js = helper + ("console.log(JSON.stringify([credsDep(null), credsDep({}), "
                   "credsDep({url: 'u', server: 's', userId: 'erin'}), credsDep({url: 'u', server: 's', userId: 'gary'})]));")
    out = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    none, empty, erin, gary = json.loads(out.stdout)
    assert none == empty                     # no connection yet == blank connection
    assert erin != gary                      # a persona switch still refetches


@pytest.mark.parametrize("view", VIEWS)
def test_view_renders_with_no_saved_connection(view):
    r = _render(view)
    assert r["ok"], r.get("error")
    assert r["rendered"]
    assert r["fetched"] >= 1          # it still loads, using the server's defaults


def test_no_unguarded_creds_field_reads_left():
    """creds is null until a connection exists, so every creds.<field> read in
    the page must be guarded (creds may be passed whole: egeriaFetch handles null)."""
    assert re.findall(r"[^\w.]creds\.[A-Za-z]", TC) == []
