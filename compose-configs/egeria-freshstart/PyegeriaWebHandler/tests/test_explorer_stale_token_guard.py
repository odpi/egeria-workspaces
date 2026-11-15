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
    js.write_text(_js_function(_page(), "credsIfStillCurrent") + "\n" + body, encoding="utf-8")
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
