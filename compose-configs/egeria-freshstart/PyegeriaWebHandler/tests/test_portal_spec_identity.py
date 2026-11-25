"""Report-spec reads run as the signed-in user, never as the Portal's service user (portal_spec_identity).

pyegeria keys fetched specs and the EGERIA tier by credential identity. A request's identity-less read would
otherwise run as the service user (EGERIA_USER, Erin). Here a private spec is a spec fetched by one user,
held in pyegeria's real store in the shape _finish_fetch writes. Through EgeriaTokenMiddleware: the user who
fetched it sees it, another user doesn't, and an anonymous caller sees public specs only.
"""
import base64
import json
import os
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import portal_spec_identity as psi  # noqa: E402

LABEL = "Finance Secrets"
FETCHED = f"egeria:{LABEL}@v3"


def _jwt(sub, nonce="a"):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    return f"{enc({'alg': 'none'})}.{enc({'sub': sub, 'exp': time.time() + 3600, 'n': nonce})}.sig"


PETER, CALLIE = _jwt("peterprofile"), _jwt("calliequartile", "b")


def _esc():
    import pyegeria.view.egeria_spec_cache as esc
    if not hasattr(esc, "client_credential_identity"):
        pytest.skip("pyegeria without the spec-cache identity change (credential identities)")
    return esc


def _fs():
    from pyegeria.view._output_format_models import FormatSet
    return FormatSet.model_validate({
        "target_type": "Asset", "heading": "Finance", "description": "Secret finance assets.",
        "formats": [{"types": ["TABLE", "DICT"], "attributes": [{"name": "Name", "key": "display_name"}]}],
        "action": {"function": "AssetMaker.find_assets", "required_params": ["search_string"]}})


@pytest.fixture
def probe(monkeypatch):
    esc = _esc()
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from egeria_auth import EgeriaTokenMiddleware
    from pyegeria.view.base_report_formats import report_spec_source

    monkeypatch.delenv("PORTAL_ALLOWED_PLATFORM_URLS", raising=False)
    monkeypatch.setattr(esc, "_FETCHED", {})
    identity = psi.token_spec_identity(PETER)
    assert identity and identity.startswith("peterprofile@")
    esc._FETCHED[(identity, LABEL, 3)] = (_fs(), {
        "tier": "egeria", "label": LABEL, "guid": "g-fin", "version": "1.0", "header_version": 3,
        "fetched_at": "2026-11-14T00:00:00Z", "fetched": True, "shared": True,
        "qualified_name": f"ReportSpec::{LABEL}", "visibility": "zoned"})

    app = FastAPI()

    @app.get("/probe")
    def _probe(name: str):
        bare = name.split("egeria:", 1)[-1]
        return {"tierInfo": esc.egeria_tier_info(bare), "source": report_spec_source(name)}
    app.add_middleware(EgeriaTokenMiddleware)
    client = TestClient(app)

    def get(name, token=None):
        r = client.get("/probe", params={"name": name}, headers={"X-Egeria-Token": token} if token else {})
        assert r.status_code == 200, r.text
        return r.json()
    return get


def _public_label():
    from pyegeria.view.base_report_formats import get_report_registry, report_spec_source
    for label in get_report_registry().keys():
        if (report_spec_source(label) or {}).get("tier") == "builtin":
            return label
    pytest.skip("no built-in report spec in this pyegeria")


def test_the_user_who_fetched_a_private_spec_sees_it(probe):
    got = probe(FETCHED, PETER)
    assert got["tierInfo"]["label"] == LABEL and got["tierInfo"]["fetched"] is True
    assert got["source"]["tier"] == "egeria" and got["source"]["guid"] == "g-fin"


def test_another_user_does_not_see_it(probe):
    assert probe(FETCHED, CALLIE) == {"tierInfo": None, "source": None}


def test_anonymous_sees_public_specs_only(probe):
    assert probe(FETCHED) == {"tierInfo": None, "source": None}
    public = _public_label()
    for token in (None, PETER, CALLIE):
        assert probe(public, token)["source"]["tier"] == "builtin"


def test_a_signed_in_run_is_made_as_the_token_user(monkeypatch):
    """pyegeria reads the EGERIA tier for credential_identity(user, ...): a token's run must not pass Erin."""
    import egeria_auth
    import report_specs_handler as rsh
    import report_viewer
    import pyegeria.view.format_set_executor as fse
    users = []
    monkeypatch.setattr(fse, "exec_report_spec", lambda *a, **k: users.append(k["user"]) or {"kind": "empty"})
    monkeypatch.setattr(report_viewer, "resolve_viewer", lambda request, persona: None)
    monkeypatch.setattr(report_viewer, "set_viewer", lambda viewer: None)
    monkeypatch.setattr(report_viewer, "reset_viewer", lambda token: None)
    monkeypatch.setenv("EGERIA_USER", "erinoverview")
    req = SimpleNamespace(spec_name="Anything", output_format="DICT", params={}, url=None, server=None,
                          user_id=None, user_pwd=None, persona=None)
    for token in (PETER, None):
        reset = egeria_auth._egeria_token.set(token)
        try:
            rsh.execute_spec(req, None)
        finally:
            egeria_auth._egeria_token.reset(reset)
    assert users == ["peterprofile", "erinoverview"]


def test_declare_multi_user(monkeypatch):
    import pyegeria.view.egeria_spec_cache as esc
    import pyegeria
    monkeypatch.setenv(psi.MULTI_USER_ENV, "")          # recorded, so the flag is restored afterwards
    monkeypatch.delattr(esc, "declare_multi_user", raising=False)
    monkeypatch.delattr(pyegeria, "declare_multi_user", raising=False)
    assert psi.declare_multi_user() == "flag only" and os.environ[psi.MULTI_USER_ENV] == "1"
    calls = []
    monkeypatch.setattr(esc, "declare_multi_user", lambda: calls.append(1), raising=False)
    assert psi.declare_multi_user() == "declared" and calls == [1]
    monkeypatch.setenv(psi.MULTI_USER_ENV, "0")
    assert psi.declare_multi_user() == "off" and calls == [1]
