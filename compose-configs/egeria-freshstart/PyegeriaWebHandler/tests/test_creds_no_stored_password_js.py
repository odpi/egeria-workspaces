# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""The Egeria password is never kept in browser storage.

The Explorer (type-explorer.html) stores only { url, server, userId } in localStorage 'egeria-creds' and keeps
the password in memory for the page's life. A password an older page stored is removed, both by the Explorer
when it reads its settings and by static/egeria-shared-ui.js on every page that loads it. After a reload:
  - demo and persona pages re-run select-persona, which supplies the password again (in memory);
  - freshstart uses the Portal session (no stored identity is needed);
  - a local user who typed credentials sees Connection Settings with the user ID and an empty password.
The 401 refresh paths are unchanged (test_po41_refresher_js.py runs refreshPersonaToken).

Runs the storage helpers under node with a fake localStorage; skipped without node. Identical in both trees.
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

_DIR = Path(__file__).resolve().parent.parent
_EXPLORER = (_DIR / "type-explorer.html").read_text()
_SHARED = (_DIR / "static" / "egeria-shared-ui.js").read_text()

needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")

_PRELUDE = r"""
var store = {};
var localStorage = {
  getItem: function(k) { return k in store ? store[k] : null; },
  setItem: function(k, v) { store[k] = String(v); },
  removeItem: function(k) { delete store[k]; }
};
"""


def _fn(src: str, name: str) -> str:
    start = src.index(f"function {name}(")
    return src[start:src.index("\n}\n", start) + 3]


def _scrub_iife() -> str:
    start = _SHARED.index("(function removeStoredEgeriaPassword()")
    return _SHARED[start:_SHARED.index("})();", start) + 5]


def _run(js: str) -> dict:
    out = subprocess.run(["node", "-e", _PRELUDE + js], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout.strip().splitlines()[-1])


OLD = json.dumps({"url": "https://h:9443", "server": "qs-view-server", "userId": "garygeeke", "password": "pw"})


@needs_node
def test_write_never_stores_a_password():
    d = _run(_fn(_EXPLORER, "writeStoredCreds") + r"""
writeStoredCreds({ url: 'u', server: 's', userId: 'erinoverview', password: 'pw', token: 'tok' });
console.log(store['egeria-creds']);""")
    assert d == {"url": "u", "server": "s", "userId": "erinoverview"}


@needs_node
def test_read_removes_an_old_stored_password_and_keeps_the_rest():
    d = _run(_fn(_EXPLORER, "readStoredCreds") + f"""
store['egeria-creds'] = {json.dumps(OLD)};
var got = readStoredCreds();
console.log(JSON.stringify({{ got: got, stored: JSON.parse(store['egeria-creds']) }}));""")
    assert d["got"] == {"url": "https://h:9443", "server": "qs-view-server", "userId": "garygeeke"}
    assert d["stored"] == d["got"]


@needs_node
def test_read_with_nothing_or_bad_data_is_empty():
    d = _run(_fn(_EXPLORER, "readStoredCreds") + r"""
var a = readStoredCreds();
store['egeria-creds'] = 'not json';
var b = readStoredCreds();
console.log(JSON.stringify({ a: a, b: b }));""")
    assert d["a"] == d["b"] == {"url": "", "server": "", "userId": ""}


@needs_node
def test_shared_ui_removes_an_old_stored_password_on_load():
    d = _run(f"store['egeria-creds'] = {json.dumps(OLD)};\n" + _scrub_iife() + r"""
console.log(store['egeria-creds']);""")
    assert d == {"url": "https://h:9443", "server": "qs-view-server", "userId": "garygeeke"}


@needs_node
def test_shared_ui_leaves_settings_without_a_password_alone():
    keep = json.dumps({"url": "u", "server": "s", "userId": "x", "extra": 1})
    d = _run(f"store['egeria-creds'] = {json.dumps(keep)};\n" + _scrub_iife() + r"""
console.log(store['egeria-creds']);""")
    assert d == json.loads(keep)


def _save_creds_body() -> str:
    start = _EXPLORER.index("const saveCreds = useCallback(function(c) {")
    return _EXPLORER[start:_EXPLORER.index("}, [acquireToken]);", start)]


def test_save_creds_persists_through_write_stored_creds_only():
    body = _save_creds_body()
    assert "writeStoredCreds(withTok)" in body
    assert "localStorage.setItem" not in body and "password" not in body.replace("never the password", "")


def test_initial_state_never_reads_a_stored_password():
    start = _EXPLORER.index("const [creds, setCreds] = useState(function() {")
    init = _EXPLORER[start:_EXPLORER.index("});", start)]
    assert "readStoredCreds()" in init
    assert "userId: ''" in init and "password: ''" in init        # no identity until the password is given again
    assert "base.password" not in _EXPLORER


def test_persona_paths_still_carry_the_password_in_memory():
    # demo and non-demo persona restore re-run select-persona and hand its password to saveCreds
    assert len(re.findall(r"saveCreds\(\{ url: '', server: 'qs-view-server', userId: sel\.egeria_user, "
                          r"password: sel\.egeria_password \}\)", _EXPLORER)) == 2
    # the 401 refresher still mints from the in-memory credentials
    assert "return acquireToken(oldCreds, true)" in _EXPLORER or "return acquireToken(oldCreds" in _EXPLORER


def test_connection_form_asks_for_the_password_again():
    start = _EXPLORER.index("function ConnectionForm(")
    form = _EXPLORER[start:_EXPLORER.index("\n}\n", start)]
    assert "userId:   creds.userId || stored.userId" in form
    assert "password: creds.password," in form
    assert "the password is not saved in the browser" in form
