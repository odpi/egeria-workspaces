# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""PO-41: an expired token on a persona page renews as that persona, never by user_id alone.

Runs egeriaFetch + refreshPersonaToken from static/egeria-shared-ui.js under node with a fake fetch:
  - a 401 redoes select-persona and posts {user_id, password, renew} to /api/egeria-token, then retries
    the request with the new token, once;
  - no persona login for the page's user, or a persona changed in another tab: the refresh rejects and
    the original 401 comes back (no request runs as anyone else);
  - every page's refresher goes through refreshPersonaToken (the pages using acquireToken send their
    own password).
Skipped without node."""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

_DIR = Path(__file__).resolve().parent.parent
_JS = (_DIR / "static" / "egeria-shared-ui.js").read_text()


def _fn(name: str) -> str:
    start = _JS.index(f"function {name}(")
    return _JS[start:_JS.index("\n}\n", start) + 3]


_PRELUDE = r"""
var _tokenRefresher = { refresh: null };
function egeriaForLineageOn() { return false; }
var store = {}; var localStorage = { getItem: function(k) { return k in store ? store[k] : null; } };
var calls = [];
function resp(status, body) { return Promise.resolve({ status: status, ok: status < 400, json: function() { return Promise.resolve(body); } }); }
var routes = {};
function fetch(url, opts) {
  var body = opts && opts.body ? JSON.parse(opts.body) : null;
  calls.push({ url: url.split('?')[0], token: opts && opts.headers && opts.headers['X-Egeria-Token'], body: body });
  return routes[url.split('?')[0]](body, opts);
}
"""


def _run(body: str) -> dict:
    js = _PRELUDE + _fn("egeriaFetch") + _fn("refreshPersonaToken") + body
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout.strip().splitlines()[-1])


needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")

_SETUP = r"""
store['egeria-persona'] = JSON.stringify({ id: 'peter' });
routes['/api/demo/select-persona'] = function() { return resp(200, { egeria_user: SEL_USER, egeria_password: 'pw' }); };
routes['/api/egeria-token'] = function(b) { return resp(200, { token: 'new-tok', user_id: b.user_id }); };
routes['/api/thing'] = function(b, opts) { return resp(opts.headers['X-Egeria-Token'] === 'new-tok' ? 200 : 401, {}); };
var creds = { server: 's', userId: 'peterprofile', token: 'old-tok' };
var latest = null;
_tokenRefresher.refresh = function(old) { return refreshPersonaToken(old).then(function(n) { latest = n; return n; }); };
egeriaFetch('/api/thing', creds).then(function(r) {
  console.log(JSON.stringify({ status: r.status, latest: latest, calls: calls }));
});
"""


@needs_node
def test_expired_token_renews_as_the_persona_with_its_password():
    d = _run("var SEL_USER = 'peterprofile';" + _SETUP)
    assert d["status"] == 200
    urls = [c["url"] for c in d["calls"]]
    assert urls == ["/api/thing", "/api/demo/select-persona", "/api/egeria-token", "/api/thing"]
    tok = d["calls"][2]["body"]
    assert tok["user_id"] == "peterprofile" and tok["password"] == "pw" and tok["renew"] is True
    assert d["calls"][3]["token"] == "new-tok"
    assert d["latest"]["userId"] == "peterprofile"


@needs_node
def test_a_persona_changed_in_another_tab_keeps_the_401():
    d = _run("var SEL_USER = 'someoneelse';" + _SETUP)
    assert d["status"] == 401
    assert [c["url"] for c in d["calls"]] == ["/api/thing", "/api/demo/select-persona"]   # no token minted
    assert d["latest"] is None


@needs_node
def test_no_persona_login_keeps_the_401_and_never_posts_user_id_alone():
    d = _run("var SEL_USER = 'peterprofile';" + _SETUP.replace(
        "store['egeria-persona'] = JSON.stringify({ id: 'peter' });", ""))
    assert d["status"] == 401
    assert all(c["url"] != "/api/egeria-token" for c in d["calls"])


def test_every_page_refresher_uses_it():
    pages = [p for p in sorted(_DIR.glob("*.html")) if "_tokenRefresher.refresh = " in p.read_text()]
    assert pages
    for p in pages:
        s = p.read_text()
        for m in re.finditer(r"_tokenRefresher\.refresh = function\((\w+)\) ?\{", s):
            body = s[m.end():m.end() + 300]
            assert "refreshPersonaToken(" in body or "acquireToken(" in body, p.name
