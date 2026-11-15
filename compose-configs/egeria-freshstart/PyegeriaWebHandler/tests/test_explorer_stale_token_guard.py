"""A token minted for one identity never lands on another in the Explorer (type-explorer.html, A2).

On load the Explorer mints a token for the creds it read from localStorage. If the user picks a
different persona (saveCreds) before that mint resolves, the late result used to be set as-is and
put the stale identity back, so later calls ran as the persona the user had switched away from.
The load effect and the 401 refresher now set creds functionally, through credsIfStillCurrent.
The race runs under node (skipped without it; the Portal container has none).
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _page():
    return (ROOT / "type-explorer.html").read_text(encoding="utf-8")


def _js_function(source, name):
    m = re.search(r"\nfunction " + name + r"\(.*?\n\}\n", source, re.S)
    assert m, f"{name} not found"
    return m.group(0)


def _node(tmp_path, body):
    node = shutil.which("node")
    if not node:
        pytest.skip("node is not installed (the Portal container has none)")
    js = tmp_path / "stale_token.js"
    page = _page()
    shared = (ROOT / "static" / "egeria-shared-ui.js").read_text(encoding="utf-8")
    parts = [_js_function(page, n) for n in ("credsIfStillCurrent", "takeSaveTicket", "refreshedOrRefused")]
    parts += ["function egeriaForLineageOn() { return false; }", "var _tokenRefresher = {};",
              _js_function(shared, "egeriaFetch")]
    js.write_text("\n".join(parts) + "\n" + body, encoding="utf-8")
    out = subprocess.run([node, str(js)], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_a_late_mint_for_the_old_persona_does_not_overwrite_the_new_one(tmp_path):
    got = _node(tmp_path, """
// A React-like state cell: setCreds takes a value or a function of the current value.
var creds = { url: '', server: '', userId: 'erinoverview', password: 'pw-e' };      // from localStorage
function setCreds(v) { creds = typeof v === 'function' ? v(creds) : v; }
var loadMint = Object.assign({}, creds, { token: 'ERIN-TOKEN' });                    // started on load
// The user picks peter; saveCreds' own mint settles first.
setCreds({ url: '', server: '', userId: 'peterprofile', password: 'pw-p', token: 'PETER-TOKEN' });
// Now the load effect's mint resolves, late.
setCreds(function(cur) { return credsIfStillCurrent(cur, loadMint); });
var afterLate = creds;
// The same identity's own mint still lands.
setCreds({ url: '', server: '', userId: 'calliequartile', password: 'pw-c' });
setCreds(function(cur) { return credsIfStillCurrent(cur, Object.assign({}, cur, { token: 'CALLIE-TOKEN' })); });
console.log(JSON.stringify({ afterLate: afterLate, own: creds }));
""")
    assert got["afterLate"]["userId"] == "peterprofile" and got["afterLate"]["token"] == "PETER-TOKEN"
    assert got["own"]["userId"] == "calliequartile" and got["own"]["token"] == "CALLIE-TOKEN"


def test_any_identity_field_change_drops_the_result(tmp_path):
    got = _node(tmp_path, """
var base = { url: 'https://a:9443', server: 'qs-view-server', userId: 'u', password: 'p' };
var result = Object.assign({}, base, { token: 'T' });
var out = {};
['url', 'server', 'userId', 'password'].forEach(function(k) {
  var cur = Object.assign({}, base); cur[k] = cur[k] + 'x';
  out[k] = credsIfStillCurrent(cur, result) === cur;
});
out.same = credsIfStillCurrent(Object.assign({}, base), result) === result;
out.blankEqualsMissing = credsIfStillCurrent({ userId: 'u', password: 'p' },
                                            { url: '', server: '', userId: 'u', password: 'p', token: 'T' }).token === 'T';
out.nullCur = credsIfStillCurrent(null, result) === null;
console.log(JSON.stringify(out));
""")
    assert got == {"url": True, "server": True, "userId": True, "password": True, "same": True,
                   "blankEqualsMissing": True, "nullCur": True}


def test_the_load_effect_and_the_refresher_set_creds_through_the_guard():
    html = _page()
    # Quickstart also keeps a failed mint (tokenTried, F1b R2); freshstart sets a token only.
    assert re.search(r"if \(withTok\.token( \|\| withTok\.tokenTried)?\) setCreds\(function\(cur\) "
                     r"\{ return credsIfStillCurrent\(cur, withTok\); \}\);", html)
    assert "setCreds(function(cur) { return credsIfStillCurrent(cur, withTok); });   // never a switched-away identity" in html
    # No bare setCreds(withTok) is left outside saveCreds (the user's own, latest choice).
    bare = [m.start() for m in re.finditer(r"setCreds\(withTok\)", html)]
    save = html.index("const saveCreds = useCallback(")
    assert len(bare) == 1 and save < bare[0] < html.index("}, [acquireToken]);", save)


# ── A2 R1: saveCreds as well; and a stale 401 refresh is refused ────────────────────────────────

def test_quick_switches_whose_mints_resolve_out_of_order_end_with_the_last_save(tmp_path):
    """The page's saveCreds shape, with mints resolved by hand: the first save's mint lands last."""
    got = _node(tmp_path, """
var creds = null, saveSeq = { current: 0 }, pending = {};
function setCreds(v) { creds = v; }
function acquireToken(c) { return new Promise(function(res) { pending[c.userId] = function() { res(Object.assign({}, c, { token: c.userId + '-T' })); }; }); }
function saveCreds(c) {                       // as in type-explorer.html
  var isLatest = takeSaveTicket(saveSeq);
  return acquireToken(c).then(function(withTok) { if (!isLatest()) return; setCreds(withTok); });
}
var out = {};
var a = saveCreds({ userId: 'peterprofile', password: 'p' });
var b = saveCreds({ userId: 'calliequartile', password: 'c' });
pending.calliequartile(); b.then(function() {
  out.afterSecond = creds.userId;
  pending.peterprofile(); return a;
}).then(function() {
  out.afterFirstLate = creds.userId;
  // three switches: erin -> peter -> rover, resolved rover, erin, peter
  var e = saveCreds({ userId: 'erinoverview', password: 'e' }), p = saveCreds({ userId: 'peterprofile', password: 'p' }),
      r = saveCreds({ userId: 'roverrevenue', password: 'r' });
  pending.roverrevenue();
  return r.then(function() { pending.erinoverview(); return e; }).then(function() { pending.peterprofile(); return p; });
}).then(function() { out.three = creds.userId; out.token = creds.token; console.log(JSON.stringify(out)); });
""")
    assert got == {"afterSecond": "calliequartile", "afterFirstLate": "calliequartile",
                   "three": "roverrevenue", "token": "roverrevenue-T"}


def test_a_stale_refresh_keeps_the_401_and_does_not_retry_as_the_old_identity(tmp_path):
    """Through the shared egeriaFetch: a 401, a refresh minted for erin while the view is now peter's."""
    got = _node(tmp_path, """
var sent = [];
function fetch(url, opts) {
  var tok = ((opts || {}).headers || {})['X-Egeria-Token'] || null;
  sent.push(tok);
  return Promise.resolve({ status: tok === 'OLD' ? 401 : 200 });
}
var current = null;
function installRefresher() {                // as in type-explorer.html
  _tokenRefresher.refresh = function(oldCreds) {
    return Promise.resolve(Object.assign({}, oldCreds, { token: 'NEW-' + oldCreds.userId })).then(function(withTok) {
      refreshedOrRefused(current, withTok);
      return withTok;
    });
  };
}
installRefresher();
var erin = { userId: 'erinoverview', password: 'e', token: 'OLD' };
var out = {};
current = { userId: 'peterprofile', password: 'p', token: 'PETER' };          // switched while erin's call ran
egeriaFetch('/api/x', erin).then(function(r) {
  out.staleStatus = r.status; out.staleSent = sent.slice();
  sent.length = 0; current = { userId: 'erinoverview', password: 'e', token: 'OLD' };   // still erin
  return egeriaFetch('/api/x', erin);
}).then(function(r) { out.liveStatus = r.status; out.liveSent = sent.slice(); console.log(JSON.stringify(out)); });
""")
    assert got["staleStatus"] == 401 and got["staleSent"] == ["OLD"]            # no retry as erin
    assert got["liveStatus"] == 200 and got["liveSent"] == ["OLD", "NEW-erinoverview"]


def test_save_creds_and_the_refresher_use_the_guards():
    html = _page()
    save = html.index("const saveCreds = useCallback(")
    body = html[save:html.index("}, [acquireToken]);", save)]
    assert "var isLatest = takeSaveTicket(saveSeq);" in body and "if (!isLatest()) return;" in body
    assert body.index("if (!isLatest()) return;") < body.index("setCreds(withTok);")
    assert "const saveSeq = React.useRef(0);" in html
    assert "credsNow.current = creds;" in html
    assert "refreshedOrRefused(credsNow.current, withTok);" in html
