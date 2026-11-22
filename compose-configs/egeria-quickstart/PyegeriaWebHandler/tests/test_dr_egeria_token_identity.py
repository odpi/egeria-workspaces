"""Dr.Egeria execute takes its identity from the sign-in token (PO-20), and /dr-egeria/process keeps the
request's context in its worker thread (PO-21). Architect brief BRIEF-PO-DRE-EXECUTE-TOKEN-IDENTITY-2026-11-15.

Before: /api/dr-egeria/execute and execute-document ran as the request BODY's user_id with the configured
(demo) password and ignored X-Egeria-Token, so on a multi-user Portal any caller could run Dr.Egeria writes as
any persona. These tests go through the real routes and EgeriaTokenMiddleware with a JWT-shaped Egeria token;
only pyegeria's EgeriaTech and Dr.Egeria's dispatcher are replaced, by fakes that record who the run's client
is and whether it signed in with a password."""
import asyncio
import base64
import json
import sys
import time
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import egeria_auth  # noqa: E402
import dr_egeria_md  # noqa: E402
import dr_egeria_commands_handler as dch  # noqa: E402


def _jwt(sub, exp_in=3600):
    def part(d):
        return base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    return f"{part({'alg': 'none'})}.{part({'sub': sub, 'exp': int(time.time()) + exp_in})}.sig"


PETER = _jwt("peterprofile")
EXPIRED = _jwt("peterprofile", exp_in=-60)


@pytest.fixture
def world(monkeypatch, tmp_path):
    """Fakes for the client and the dispatcher; records every client built and every sign-in."""
    w = {"clients": [], "signins": [], "dispatched": 0}

    class FakeTech:
        def __init__(self, server, url, user_id=None, user_pwd=None):
            self.server, self.platform_url, self.user_id = server, url, user_id
            self.built_with_pwd = user_pwd
            self.user_pwd = None if user_pwd is None or not user_pwd else user_pwd
            self.token = None
            w["clients"].append(self)

        def set_bearer_token(self, token):
            self.token = token

        def create_egeria_bearer_token(self, user_id=None, user_pwd=None):
            w["signins"].append((user_id, user_pwd))

    class FakeDispatcher:
        async def dispatch_batch(self, commands, context=None):
            w["dispatched"] += 1
            return [{"is_command": True, "status": "success", "message": "ok", "verb": "View",
                     "object_type": "Thing"}]

    monkeypatch.setattr(dr_egeria_md, "EgeriaTech", FakeTech)
    monkeypatch.setattr(dr_egeria_md, "setup_dispatcher", lambda client: FakeDispatcher())
    monkeypatch.setattr(dr_egeria_md, "UniversalExtractor",
                        lambda content: type("X", (), {"extract_commands": lambda self: ["cmd"]})())
    monkeypatch.setattr(egeria_auth, "resolve_platform", lambda url, **k: url or "https://egeria.test:9443")
    monkeypatch.setattr(dch, "EGERIA_ROOT_PATH", str(tmp_path))
    monkeypatch.setenv("EGERIA_ROOT_PATH", str(tmp_path))
    import demo_feedback_handler as dfh
    monkeypatch.setattr(dfh, "DEMO_MODE", False)
    monkeypatch.setattr(dfh, "SERVER_MANAGED_AUTH", False)
    w["dfh"] = dfh
    app = FastAPI()
    app.add_middleware(egeria_auth.EgeriaTokenMiddleware)
    app.include_router(dch.router)
    w["client"] = TestClient(app)
    return w


def _execute(w, token=None, **body):
    headers = {"X-Egeria-Token": token} if token else {}
    return w["client"].post("/api/dr-egeria/execute", headers=headers,
                            json={"title": "View Glossary", "params": {}, "directive": "display", **body})


def _document(w, token=None, **body):
    headers = {"X-Egeria-Token": token} if token else {}
    return w["client"].post("/api/dr-egeria/execute-document", headers=headers,
                            json={"content": "## View Glossary\n", "directive": "display", **body})


@pytest.mark.parametrize("call", [_execute, _document], ids=["execute", "execute-document"])
def test_token_peter_with_body_erin_runs_as_peter_with_no_password(world, call):
    r = call(world, PETER, user_id="erinoverview", user_pwd="secret")
    assert r.status_code == 200, r.text
    [c] = world["clients"]
    assert c.user_id == "peterprofile" and c.token == PETER
    assert c.user_pwd is None
    assert c.built_with_pwd is not None and not c.built_with_pwd   # NO_PASSWORD (falsy), never a password
    assert repr(c.built_with_pwd) == "NO_PASSWORD"
    assert world["signins"] == []                                   # no password sign-in at all
    assert world["dispatched"] == 1


@pytest.mark.parametrize("call", [_execute, _document], ids=["execute", "execute-document"])
def test_an_expired_token_is_401_and_nothing_runs(world, call):
    r = call(world, EXPIRED, user_id="erinoverview", user_pwd="secret")
    assert r.status_code == 401 and "sign in again" in r.json()["detail"]
    assert world["clients"] == [] and world["dispatched"] == 0


def test_a_token_with_no_user_is_401(world):
    r = _execute(world, "not.a.jwt")
    assert r.status_code == 401 and world["clients"] == []


@pytest.mark.parametrize("flag", ["DEMO_MODE", "SERVER_MANAGED_AUTH"])
@pytest.mark.parametrize("call", [_execute, _document], ids=["execute", "execute-document"])
def test_auth_on_without_a_token_is_401(world, monkeypatch, flag, call):
    monkeypatch.setattr(world["dfh"], flag, True)
    r = call(world, None, user_id="erinoverview", user_pwd="secret")
    assert r.status_code == 401
    assert world["clients"] == [] and world["dispatched"] == 0


def test_auth_off_without_a_token_is_todays_env_user(world, monkeypatch):
    monkeypatch.setenv("EGERIA_USER", "envuser")
    monkeypatch.setenv("EGERIA_USER_PASSWORD", "envpwd")
    r = _execute(world)
    assert r.status_code == 200, r.text
    [c] = world["clients"]
    assert c.user_id == "envuser" and c.token is None
    assert world["signins"] == [("envuser", "envpwd")]


def test_auth_off_without_a_token_keeps_the_body_user(world):
    # today's no-auth behaviour, unchanged (the brief allows it on a local Portal)
    r = _execute(world, user_id="peterprofile", user_pwd="pw")
    assert r.status_code == 200
    assert world["signins"] == [("peterprofile", "pw")]


def test_with_a_token_the_body_password_is_never_read():
    import inspect
    src = inspect.getsource(dch.dr_egeria_identity)
    token_branch = src[src.index("    if token:"):src.index("    if _auth_on():")]
    assert "user_pwd" not in token_branch.replace("user_pwd=None", "")
    for route in (dch.execute_command, dch.execute_document):
        body = inspect.getsource(route)
        assert "req.user_pwd" not in body and "dr_egeria_identity(req)" in body


# ── /dr-egeria/process: the worker thread sees the request's context (PO-21) ──

def test_process_executor_sees_the_token():
    import pyegeria_handler as ph
    seen = {}

    def probe(request):
        seen["token"] = egeria_auth.get_request_token()
        return ph.ProcessResponse(status="success", message="m", input_file="f", output_folder="",
                                  console_output="", environment_key="e", user_profile_key="u")

    req = ph.ProcessRequest(input_file="f.md", environment_key="e", user_profile_key="u",
                            user_id="peterprofile", user_pass="x")

    async def run():
        reset = egeria_auth._egeria_token.set(PETER)
        try:
            return await ph.process_markdown(req)
        finally:
            egeria_auth._egeria_token.reset(reset)

    orig = ph._invoke_processor
    ph._invoke_processor = probe
    try:
        asyncio.run(run())
    finally:
        ph._invoke_processor = orig
    assert seen["token"] == PETER


def test_process_uses_copy_context():
    src = (ROOT / "pyegeria_handler.py").read_text()
    assert "executor, contextvars.copy_context().run, _invoke_processor, request)" in src


# ── the front end sends the token, and only once it is minted ─────────────────

def _dre_ready_fn():
    import re
    html = (ROOT / "type-explorer.html").read_text()
    return re.search(r"function dreCredsReady\(creds\) \{.*?\n\}\n", html, re.S).group(0)


def test_dre_creds_ready_waits_for_the_token():
    import shutil
    import subprocess
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    js = _dre_ready_fn() + """console.log(JSON.stringify([
      dreCredsReady({userId: 'p', password: 'x'}),                     // minting: not ready
      dreCredsReady({userId: 'p', password: 'x', token: 't'}),         // minted
      dreCredsReady({userId: 'p', password: 'x', tokenTried: true}),   // mint tried and failed
      dreCredsReady({userId: 'p'}),                                    // no password: nothing to mint
      dreCredsReady(null)]));"""
    out = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    assert json.loads(out.stdout) == [False, True, True, True, True]


def test_explorer_sends_the_token_and_no_password_with_it():
    html = (ROOT / "type-explorer.html").read_text()
    start = html.index("function runExecute()")
    body = html[start:html.index("function renderExecutePanel(", start)]
    assert "egeriaFetch('/api/dr-egeria/execute', creds," in body
    assert "fetch('/api/dr-egeria/execute', {" not in body.replace("egeriaFetch('/api/dr-egeria/execute', creds, {", "")
    assert "if (!dreCredsReady(creds))" in body
    assert "if (!(creds && creds.token)) { execBody.user_id" in body   # user_id/user_pwd only without a token


def test_run_document_waits_for_the_viewer_token():
    html = (ROOT / "local-dashboards.html").read_text()
    start = html.index("function runDocument(directive)")
    body = html[start:html.index("function renderRunDocResult(", start)]
    assert body.index("viewerToken()") < body.index("fetch('/api/dr-egeria/execute-document'")
    assert "headers['X-Egeria-Token'] = token" in body
