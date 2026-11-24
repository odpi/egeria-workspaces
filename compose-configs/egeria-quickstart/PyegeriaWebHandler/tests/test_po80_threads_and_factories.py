"""PO-80 (quickstart half): the note-log subject enrichment runs on a pool thread in a COPY of the request
context (it ran with an empty one, so as the Portal's service user), and the tech catalog's async client
factories act only as the token's user (set_bearer_token alone left the service user and password on the
client, so pyegeria's 401 retry signed in as the service user)."""
import asyncio
import base64
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import egeria_auth  # noqa: E402


def _jwt(sub, exp_in=3600):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b"=").decode()
    return f"{enc({'alg': 'none'})}.{enc({'sub': sub, 'exp': int(time.time()) + exp_in})}.sig"


PETER = _jwt("peter")


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    monkeypatch.setenv("EGERIA_PLATFORM_URL", "https://127.0.0.1:9")
    monkeypatch.setenv("EGERIA_USER", "svcuser")
    monkeypatch.setenv("EGERIA_USER_PASSWORD", "svc-test-password")


class _Empty:
    def __getattr__(self, name):
        return lambda *a, **k: []


def test_notelog_subject_enrichment_runs_with_the_callers_token(monkeypatch):
    import notelog_handler as nl
    seen = []
    log = {"elementHeader": {"guid": "log-1"}, "properties": {"qualifiedName": "NoteLog::x"}}

    def enrich(creds, qn, guid):
        seen.append(egeria_auth.get_request_token())
        return None

    monkeypatch.setattr(nl, "_get_manager", lambda *a, **k: _Empty())
    monkeypatch.setattr(nl, "_find_note_logs", lambda *a, **k: [log])
    monkeypatch.setattr(nl, "_enrich_subjects_in_thread", enrich)
    app = FastAPI()
    app.add_middleware(egeria_auth.EgeriaTokenMiddleware)
    app.include_router(nl.router)
    r = TestClient(app).get("/api/notelogs/log-1", headers={"X-Egeria-Token": PETER})
    assert r.status_code == 200, r.text
    assert seen == [PETER], "the enrichment thread ran without the caller's token (as the service user)"


class _Client:
    """A pyegeria client stand-in: the real constructors call the platform (/api/about)."""
    def __init__(self, *a, view_server=None, server_name=None, platform_url=None, user_id=None,
                 user_pwd=None, **k):
        self.view_server = self.server_name = view_server or server_name
        self.platform_url, self.user_id, self.user_pwd = platform_url, user_id, user_pwd

    def set_bearer_token(self, token):
        self.token = token

    async def _async_create_egeria_bearer_token(self):
        raise AssertionError("signed in with the client's own (service) credentials")


@pytest.mark.parametrize("factory", ["_automated_curation_async", "_async_asset_maker", "_governance_officer_async"])
def test_async_factories_take_the_tokens_user_and_drop_the_service_password(monkeypatch, factory):
    import pyegeria
    import tech_catalog_handler as tc
    for name in ("AutomatedCuration", "AssetMaker", "GovernanceOfficer"):
        monkeypatch.setattr(pyegeria, name, _Client)
    client = asyncio.run(getattr(tc, factory)(None, None, None, None, token=PETER))
    assert client.user_id == "peter", "a 401 retry would sign in as the service user"
    assert not client.user_pwd, "the service password stayed on a token user's client"
