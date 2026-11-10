"""Per-process caches of user-visible Egeria data are keyed on the credential PRESENTED (a hash of the
X-Egeria-Token, see result_cache.request_identity), never on a bare user_id (None for every
token-authenticated user, so all of them shared one entry) or a token's unverified `sub`.

Checked per route: two different tokens never share an entry, the same token on a repeat call is a
cache hit (no second Egeria call), and an expired token bypasses the cache entirely."""
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
import result_cache  # noqa: E402


def _jwt(sub, exp_in=3600, salt=""):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b"=").decode()
    return f"{enc({'alg': 'none'})}.{enc({'sub': sub, 'exp': int(time.time()) + exp_in, 'n': salt})}.sig"


PETER, ERIN = _jwt("peter"), _jwt("erin")
FORGED_PETER = _jwt("peter", salt="forged")      # same `sub`, different (unsigned) token
EXPIRED = _jwt("peter", exp_in=-60)


# ── request_identity itself ──────────────────────────────────────────────────

def _identity_for(token, user_id=None, user_pwd=None):
    reset = egeria_auth._egeria_token.set(token)
    try:
        return result_cache.request_identity(user_id, user_pwd)
    finally:
        egeria_auth._egeria_token.reset(reset)


def test_identity_hashes_the_whole_token_not_its_sub():
    a, b = _identity_for(PETER), _identity_for(FORGED_PETER)
    assert a.startswith("t:") and b.startswith("t:") and a != b
    assert "peter" not in a                                   # the secret / claim is never in the key
    assert _identity_for(PETER) == a                          # stable for the same token


def test_identity_is_none_for_an_expired_token():
    assert _identity_for(EXPIRED) is None


def test_identity_without_a_token_uses_the_password_too():
    assert _identity_for(None, "peter", "right") != _identity_for(None, "peter", "wrong")
    assert _identity_for(None).startswith("svc:")


# ── routes ───────────────────────────────────────────────────────────────────

class _Counting:
    """A pyegeria stand-in: every method call is counted and returns an empty result."""
    def __init__(self):
        self.calls = 0

    def __getattr__(self, name):
        def call(*a, **k):
            self.calls += 1
            return []
        return call


def _app(module):
    app = FastAPI()
    app.add_middleware(egeria_auth.EgeriaTokenMiddleware)
    app.include_router(module.router)
    return TestClient(app)


def _collections(monkeypatch, mgr):
    import collections_handler as m
    m._TREE_CACHE.clear()
    monkeypatch.setattr(m, "_get_manager", lambda *a, **k: mgr)
    return m


def _digital_products(monkeypatch, mgr):
    import digital_products_handler as m
    m._TREE_CACHE.clear()
    monkeypatch.setattr(m, "_get_manager", lambda *a, **k: mgr)
    return m


def _projects(monkeypatch, mgr):
    import project_handler as m
    m._PROJ_TREE_CACHE.clear()
    monkeypatch.setattr(m, "_get_manager", lambda *a, **k: mgr)
    return m


ROUTES = [
    (_collections, "/api/collections/root-1/tree"),
    (_collections, "/api/collections/node-1/children"),
    (_digital_products, "/api/digital-products/catalogs/cat-1/tree"),
    (_digital_products, "/api/digital-products/node-1/children"),
    (_projects, "/api/projects/tree"),
    (_projects, "/api/projects/dependencies"),
]


@pytest.mark.parametrize("setup,path", ROUTES)
def test_two_tokens_never_share_an_entry(monkeypatch, setup, path):
    mgr = _Counting()
    c = _app(setup(monkeypatch, mgr))
    assert c.get(path, headers={"X-Egeria-Token": PETER}).status_code == 200
    first = mgr.calls
    assert c.get(path, headers={"X-Egeria-Token": ERIN}).status_code == 200
    assert mgr.calls > first, "erin was served peter's cached entry"
    second = mgr.calls
    assert c.get(path, headers={"X-Egeria-Token": FORGED_PETER}).status_code == 200
    assert mgr.calls > second, "a token forging peter's `sub` was served peter's cached entry"


@pytest.mark.parametrize("setup,path", ROUTES)
def test_same_token_on_a_repeat_call_hits_the_cache(monkeypatch, setup, path):
    mgr = _Counting()
    c = _app(setup(monkeypatch, mgr))
    c.get(path, headers={"X-Egeria-Token": PETER})
    first = mgr.calls
    assert first > 0
    assert c.get(path, headers={"X-Egeria-Token": PETER}).status_code == 200
    assert mgr.calls == first, "repeat call with the same token went back to Egeria"


@pytest.mark.parametrize("setup,path", ROUTES)
def test_an_expired_token_neither_reads_nor_fills_the_cache(monkeypatch, setup, path):
    mgr = _Counting()
    module = setup(monkeypatch, mgr)
    c = _app(module)
    c.get(path, headers={"X-Egeria-Token": EXPIRED})
    c.get(path, headers={"X-Egeria-Token": EXPIRED})
    cache = module._TREE_CACHE if hasattr(module, "_TREE_CACHE") else module._PROJ_TREE_CACHE
    assert cache == {}, "an expired token's answer was cached"


def test_as_of_time_and_lineage_stay_in_the_key(monkeypatch):
    mgr = _Counting()
    m = _collections(monkeypatch, mgr)
    c = _app(m)
    c.get("/api/collections/root-1/tree", headers={"X-Egeria-Token": PETER})
    c.get("/api/collections/root-1/tree", headers={"X-Egeria-Token": PETER},
          params={"as_of_time": "2026-11-06T00:00:00.000Z"})
    c.get("/api/collections/root-1/tree", headers={"X-Egeria-Token": PETER, "X-Egeria-For-Lineage": "true"})
    assert len(m._TREE_CACHE) == 3
    assert any(k.endswith("|fl") for k in m._TREE_CACHE)
    assert any("|2026-11-06T00:00:00.000Z" in k for k in m._TREE_CACHE)


def test_component_groups_build_runs_with_the_callers_token(monkeypatch):
    """The background build used to start in an empty context, so it ran as the service user."""
    import threading
    import solution_architect_handler as sa
    sa._COMP_GROUPS_CACHE.clear()
    seen, done = [], threading.Event()

    def build(*a):
        seen.append(egeria_auth.get_request_token()); done.set()
        return {"blueprints": {}, "supplyChains": {}, "members": {}, "builtAt": time.time()}

    monkeypatch.setattr(sa, "_build_component_groups", build)
    c = _app(sa)
    assert c.get("/api/solution/components/groups", headers={"X-Egeria-Token": PETER}).json() == {"loading": True}
    assert done.wait(5)
    assert seen == [PETER]


# ── follow-up: auth failures surface; survey types are the service user's ────

class _Refusing:
    """get_collection_members raises what pyegeria raises for a refused/expired token."""
    def __init__(self, status):
        self.status = status

    def get_collection_members(self, **k):
        raise RuntimeError(f"Client error '{self.status} ' -- HTTP code: {self.status}")


@pytest.mark.parametrize("setup,path", ROUTES[:4])
@pytest.mark.parametrize("status", [401, 403])
def test_a_refused_token_is_a_401_or_403_not_an_empty_tree(monkeypatch, setup, path, status):
    module = setup(monkeypatch, _Refusing(status))
    r = _app(module).get(path, headers={"X-Egeria-Token": PETER})
    assert r.status_code == status, r.text
    assert module._TREE_CACHE == {}, "a refusal was cached"


def test_other_member_read_failures_still_degrade_to_an_empty_tree(monkeypatch):
    class _Broken:
        def get_collection_members(self, **k):
            raise RuntimeError("connection reset")
    m = _collections(monkeypatch, _Broken())
    r = _app(m).get("/api/collections/node-1/children", headers={"X-Egeria-Token": PETER})
    assert r.status_code == 200 and r.json() == {"children": []}


def test_survey_types_are_built_once_as_the_service_user_for_everyone(monkeypatch):
    import asyncio
    import tech_catalog_handler as tc
    tc._SURVEY_TYPES_CACHE.clear(); tc._SURVEY_TYPES_TASKS.clear()
    clients = []

    async def fake_client(url, server, user_id, user_pwd, token=None):
        clients.append((url, server, user_id, user_pwd, token))
        return object()

    async def fake_build(ac):
        return [{"guid": "s1", "displayName": "Survey"}]

    monkeypatch.setattr(tc, "_automated_curation_async", fake_client)
    monkeypatch.setattr(tc, "_build_survey_types", fake_build)
    c = _app(tc)
    first = c.get("/api/tech-catalog/survey-types", headers={"X-Egeria-Token": PETER},
                  params={"url": "https://elsewhere.example", "user_id": "x", "user_pwd": "y"})
    assert first.json().get("loading") is True
    # the build ran with no caller credentials and no caller URL: the env service user on the env platform
    assert clients == [(None, None, None, None, None)]
    for _ in range(50):                                   # let the background Task finish
        if tc._SURVEY_TYPES_CACHE:
            break
        time.sleep(0.02)
    assert list(tc._SURVEY_TYPES_CACHE) and all(k.startswith("svc:") for k in tc._SURVEY_TYPES_CACHE)
    # a different user (and an expired token) reads the same shared entry, no second build
    for tok in (ERIN, EXPIRED):
        assert c.get("/api/tech-catalog/survey-types", headers={"X-Egeria-Token": tok}).json() == \
            {"items": [{"guid": "s1", "displayName": "Survey"}]}
    assert len(clients) == 1
