"""egeriaFetch (static/egeria-shared-ui.js) sends ?user_id= only when it has no token (PO-4).

With an X-Egeria-Token every handler takes the identity from the token (egeria_auth.apply_token sets
client.user_id from the token's sub; result_cache.request_identity keys on the token), so ?user_id= was
dead and only misled whoever read the access log: /api/types?user_id=erinoverview for a request that ran
as someone else. Without a token many handlers still read ?user_id=, so it stays in that case.

The behaviour tests run egeriaFetch itself under node (skipped when node is not installed: the Portal
container has none); the source pin runs everywhere."""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SHARED = (ROOT / "static" / "egeria-shared-ui.js").read_text()

HARNESS = r"""
var calls = [];
function egeriaForLineageOn() { return false; }
var responses = [];
function fetch(url, opts) {
  calls.push({ url: url, token: (opts.headers || {})['X-Egeria-Token'] || null });
  var status = responses.length ? responses.shift() : 200;
  return Promise.resolve({ status: status });
}
var _tokenRefresher = { refresh: null };
eval(SRC);
_tokenRefresher = { refresh: function(c) { return Promise.resolve(Object.assign({}, c, { token: 'fresh' })); } };
async function main() {
  var out = {};
  calls = [];
  await egeriaFetch('/api/types', { url: 'https://p:9443', server: 'qs', userId: 'erinoverview', token: 't1' });
  out.withToken = calls[0];
  calls = [];
  await egeriaFetch('/api/types?area=1', { url: 'https://p:9443', server: 'qs', userId: 'peterprofile' });
  out.noToken = calls[0];
  calls = []; responses = [401, 200];
  var r = await egeriaFetch('/api/types', { userId: 'erinoverview', token: 'old' });
  out.retry = { status: r.status, calls: calls };
  console.log(JSON.stringify(out));
}
main().catch(function(e) { console.log(JSON.stringify({ error: String(e) })); });
"""


def _egeria_fetch_src():
    m = re.search(r"var _tokenRefresher = \{ refresh: null \};\n\nfunction egeriaFetch\(.*?\n\}\n", SHARED, re.S)
    assert m, "egeriaFetch not found in static/egeria-shared-ui.js"
    return m.group(0)


def _run():
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    js = "var SRC = " + json.dumps(_egeria_fetch_src()) + ";\n" + HARNESS
    out = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    res = json.loads(out.stdout.strip().splitlines()[-1])
    assert "error" not in res, res
    return res


def test_with_a_token_the_url_names_no_user():
    call = _run()["withToken"]
    assert call["token"] == "t1"
    assert "user_id" not in call["url"], call["url"]
    assert call["url"] == "/api/types?url=https%3A%2F%2Fp%3A9443&server=qs"


def test_without_a_token_user_id_stays():
    call = _run()["noToken"]
    assert call["token"] is None
    assert call["url"] == "/api/types?area=1&url=https%3A%2F%2Fp%3A9443&server=qs&user_id=peterprofile"


def test_a_401_still_refreshes_and_the_retry_names_no_user():
    res = _run()["retry"]
    assert res["status"] == 200
    assert [c["token"] for c in res["calls"]] == ["old", "fresh"]
    assert all("user_id" not in c["url"] for c in res["calls"]), res["calls"]


def test_source_pin():
    src = _egeria_fetch_src()
    assert "if (creds.userId && !creds.token) p.set('user_id', creds.userId);" in src
    assert src.count("p.set('user_id'") == 1
