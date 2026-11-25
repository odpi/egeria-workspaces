"""Report-spec reads run as the signed-in user, never as the Portal's service user (portal_spec_identity).

pyegeria keys fetched specs and the EGERIA tier by credential identity. A request's identity-less read would
otherwise run as the service user (EGERIA_USER, Erin). Here a private spec is a spec fetched by one user,
held in pyegeria's real store in the shape _finish_fetch writes. Through EgeriaTokenMiddleware and the
Portal's own read helpers: the user who fetched it sees it, another user doesn't, and an anonymous caller
sees public specs only.
"""
import base64
import json
import sys
import time
from pathlib import Path

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
def store(monkeypatch):
    """Peter has fetched the zoned spec (kept in-process, keyed by his identity, as _finish_fetch does)."""
    esc = _esc()
    monkeypatch.delenv("PORTAL_ALLOWED_PLATFORM_URLS", raising=False)
    monkeypatch.setattr(esc, "_FETCHED", {})
    identity = psi.token_spec_identity(PETER)
    assert identity and identity.startswith("peterprofile@")
    esc._FETCHED[(identity, LABEL, 3)] = (_fs(), {
        "tier": "egeria", "label": LABEL, "guid": "g-fin", "version": "1.0", "header_version": 3,
        "fetched_at": "2026-11-14T00:00:00Z", "fetched": True, "shared": True,
        "qualified_name": f"ReportSpec::{LABEL}", "visibility": "zoned"})
    return esc


@pytest.fixture
def probe(store):
    """A route behind the Portal's real token middleware that reads the way the Portal's handlers do."""
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from egeria_auth import EgeriaTokenMiddleware
    import report_spec_publish_handler as rsp
    import report_specs_handler as rsh

    app = FastAPI()

    @app.get("/probe")
    def _probe(name: str):                       # a sync route: runs in the threadpool, as the real ones do
        bare = name.split("egeria:", 1)[-1]     # tier info takes "<label>@v<N>" (report_spec_source strips it)
        return {"tierInfo": store.egeria_tier_info(bare), "publishTierInfo": rsp._tier_info(bare),
                "specSource": rsh.spec_source_for(name)}
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
    assert got["publishTierInfo"]["guid"] == "g-fin"
    assert got["specSource"]["source"] == "egeria" and got["specSource"]["label"] == LABEL


def test_another_user_does_not_see_it(probe):
    got = probe(FETCHED, CALLIE)
    assert got == {"tierInfo": None, "publishTierInfo": None, "specSource": None}


def test_anonymous_sees_public_specs_only(probe):
    assert probe(FETCHED) == {"tierInfo": None, "publishTierInfo": None, "specSource": None}
    public = _public_label()
    for token in (None, PETER, CALLIE):
        assert probe(public, token)["specSource"]["source"] == "builtin"


def test_request_identity_is_the_identity_the_restricted_path_fetches_with(store):
    import report_spec_restricted as rsr
    assert psi.token_spec_identity(PETER) == store.client_credential_identity(rsr._user_client(PETER))


def test_no_token_or_no_user_means_no_identity(store):
    assert psi.token_spec_identity(None) is None
    assert psi.token_spec_identity("not-a-jwt") is None
    with psi.request_spec_identity(None) as identity:
        assert identity is None and store._SPEC_IDENTITY.get() is None


def test_shared_decisions_are_made_as_no_one(store, monkeypatch):
    """The public route's shared-tier check and fallback registration never use the requester's identity."""
    import local_spec_fallback as lsf
    import report_spec_restricted as rsr
    seen = []
    monkeypatch.setattr(store, "egeria_tier_info", lambda label: seen.append(store._SPEC_IDENTITY.get()) or None)
    monkeypatch.setattr(store, "egeria_tier", lambda force=False: seen.append(store._SPEC_IDENTITY.get()) or {})
    with psi.request_spec_identity(PETER) as identity:
        assert identity and store._SPEC_IDENTITY.get() == identity
        rsr._shared_tier_version(LABEL)
        lsf._egeria_labels()
        assert store._SPEC_IDENTITY.get() == identity            # restored after each
    assert seen == [None, None]


def test_a_signed_in_run_is_made_as_the_token_user():
    import report_specs_handler as rsh
    assert rsh._run_user(PETER, "erinoverview") == "peterprofile"
    assert rsh._run_user(None, "erinoverview") == "erinoverview"
    assert rsh._run_user("not-a-jwt", "erinoverview") == "erinoverview"


# ── the startup declaration ───────────────────────────────────────────────────

def test_declare_multi_user_sets_the_flag_on_a_pyegeria_without_the_function(monkeypatch):
    import pyegeria.view.egeria_spec_cache as esc
    import pyegeria
    monkeypatch.setenv(psi.MULTI_USER_ENV, "")        # recorded, so the flag is restored afterwards
    monkeypatch.delattr(esc, "declare_multi_user", raising=False)
    monkeypatch.delattr(pyegeria, "declare_multi_user", raising=False)
    assert psi.declare_multi_user() == "flag only"
    import os
    assert os.environ[psi.MULTI_USER_ENV] == "1"


def test_declare_multi_user_calls_pyegerias_function(monkeypatch):
    import pyegeria.view.egeria_spec_cache as esc
    calls = []
    monkeypatch.setenv(psi.MULTI_USER_ENV, "")        # recorded, so the flag is restored afterwards
    monkeypatch.setattr(esc, "declare_multi_user", lambda: calls.append(1), raising=False)
    assert psi.declare_multi_user() == "declared" and calls == [1]


def test_an_explicit_off_is_respected(monkeypatch):
    import pyegeria.view.egeria_spec_cache as esc
    calls = []
    monkeypatch.setenv(psi.MULTI_USER_ENV, "0")
    monkeypatch.setattr(esc, "declare_multi_user", lambda: calls.append(1), raising=False)
    assert psi.declare_multi_user() == "off" and calls == []
