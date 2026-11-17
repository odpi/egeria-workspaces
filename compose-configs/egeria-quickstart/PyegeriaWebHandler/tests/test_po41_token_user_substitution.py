"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

PO-41 (security): POST /api/egeria-token must not sign in as a caller-named user with the Portal's own
password. With no password sent, only EGERIA_USER gets a token; a sent password (even one equal to the
service password, as every demo persona's is) may go with any user_id. And no page's 401 refresher asks
for a token by user_id alone.

No test reaches Egeria: the token-minting client is replaced.
"""
import re
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

_MODULE_DIR = Path(__file__).resolve().parent.parent
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import egeria_auth  # noqa: E402

HOME = "https://egeria.home.test:9443"
SERVICE_USER = "portal-service-user"
SERVICE_PWD = "service-secret"


class _Mint:
    calls = []

    def __init__(self, view_server=None, platform_url=None, user_id=None, user_pwd=None):
        self.user_id, self.user_pwd = user_id, user_pwd

    async def _async_create_egeria_bearer_token(self):
        _Mint.calls.append((self.user_id, self.user_pwd))
        return f"tok-{len(_Mint.calls)}"


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    for v in egeria_auth._PLATFORM_ENV_VARS + ("PORTAL_ALLOWED_PLATFORM_URLS", "PORTAL_ALLOW_CUSTOM_PLATFORMS",
                                               "DEMO_MODE"):
        monkeypatch.delenv(v, raising=False)
    monkeypatch.setenv("EGERIA_PLATFORM_URL", HOME)
    monkeypatch.setenv("EGERIA_USER", SERVICE_USER)
    monkeypatch.setenv("EGERIA_USER_PASSWORD", SERVICE_PWD)
    monkeypatch.setattr(egeria_auth, "_TOKEN_PLATFORMS", {})
    import pyegeria
    monkeypatch.setattr(pyegeria, "AssetMaker", _Mint)
    _Mint.calls = []


@pytest.fixture
def app_client():
    import pyegeria_handler as handler
    return TestClient(handler.app)


def _post(client, **body):
    return client.post("/api/egeria-token", json=body)


def test_user_id_with_no_password_is_refused_and_mints_nothing(app_client):
    r = _post(app_client, user_id="peterprofile")
    assert r.status_code == 400, r.text
    assert "own password" in r.json()["detail"] and r.json()["detail"] == egeria_auth.NAMED_USER_NEEDS_PASSWORD_WORDS
    assert _Mint.calls == []


@pytest.mark.parametrize("pwd", ["", None])
def test_an_empty_password_counts_as_none_sent(app_client, pwd):
    r = _post(app_client, user_id="peterprofile", password=pwd)
    assert r.status_code == 400 and _Mint.calls == []


def test_user_id_with_its_password_signs_in_as_that_user(app_client):
    r = _post(app_client, user_id="peterprofile", password="peters-own")
    assert r.status_code == 200, r.text
    assert r.json()["user_id"] == "peterprofile"
    assert _Mint.calls == [("peterprofile", "peters-own")]


def test_a_sent_password_equal_to_the_service_password_still_signs_in_as_that_user(app_client):
    """The demo personas' passwords all equal the service password: their sign-in must keep working."""
    r = _post(app_client, user_id="peterprofile", password=SERVICE_PWD)
    assert r.status_code == 200, r.text
    assert r.json()["user_id"] == "peterprofile"
    assert _Mint.calls == [("peterprofile", SERVICE_PWD)]


def test_no_user_id_and_no_password_is_the_service_user(app_client):
    r = _post(app_client)
    assert r.status_code == 200, r.text
    assert r.json()["user_id"] == SERVICE_USER
    assert _Mint.calls == [(SERVICE_USER, SERVICE_PWD)]


def test_the_service_user_named_with_no_password_still_works(app_client):
    r = _post(app_client, user_id=SERVICE_USER)
    assert r.status_code == 200, r.text
    assert _Mint.calls == [(SERVICE_USER, SERVICE_PWD)]


# ── no page asks for a token by user_id alone ────────────────────────────────────────────────────────

def _token_posts(src):
    """The JSON bodies sent to /api/egeria-token in a page's source (the text up to the body's end)."""
    for m in re.finditer(r"fetch\('/api/egeria-token'", src):
        yield src[m.end():m.end() + 500]


def test_every_refresher_renews_as_the_persona():
    pages = sorted(p for p in _MODULE_DIR.glob("*.html") if "_tokenRefresher.refresh = " in p.read_text())
    assert pages
    for p in pages:
        s = p.read_text()
        for m in re.finditer(r"_tokenRefresher\.refresh = function\((\w+)\) ?\{", s):
            body = s[m.end():m.end() + 400]
            assert ("refreshPersonaToken(" in body or "acquireToken(" in body), p.name


def test_no_page_posts_a_user_id_without_a_password():
    for p in sorted(_MODULE_DIR.glob("*.html")):
        for chunk in _token_posts(p.read_text()):
            stringify = re.search(r"JSON\.stringify\(\{(.*?)\}\)", chunk, re.S)
            if not stringify:
                continue
            fields = stringify.group(1)
            if re.search(r"\buser_id\s*:", fields):
                assert re.search(r"\bpassword\s*:", fields), f"{p.name}: user_id sent with no password"


def test_the_shared_refresher_never_sends_user_id_alone():
    js = (_MODULE_DIR / "static" / "egeria-shared-ui.js").read_text()
    start = js.index("function refreshPersonaToken(")
    fn = js[start:js.index("\n}\n", start)]
    assert "body.user_id = sel.egeria_user;" in fn and "body.password = sel.egeria_password;" in fn
    assert fn.index("body.user_id") > fn.index("sel.egeria_password)")      # only inside the password branch
    assert "throw new Error('No Egeria login to renew" in fn
