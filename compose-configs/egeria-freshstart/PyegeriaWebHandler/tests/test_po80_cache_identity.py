"""PO-80: freshstart's per-process caches of user-visible Egeria data are keyed on the credential PRESENTED
(a hash of the X-Egeria-Token, result_cache.request_identity), never on the bare ?user_id= (None for every
token-authenticated user once the browser stops sending it, so all of them would share one entry) or on a
token's unverified `sub`. Quickstart got this in 40c4e91c; freshstart never did.

One check per cache family: two tokens never share an entry, the same token hits the cache, an expired
token neither reads nor fills it. Plus: background builds run as the caller (copy_context), and the
async client factories act only as the token's user (no 401 re-login as the service user)."""
import base64
import json
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402
from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import egeria_auth  # noqa: E402

PLATFORM = "https://127.0.0.1:9"     # nothing listens here


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    monkeypatch.setenv("EGERIA_PLATFORM_URL", PLATFORM)
    monkeypatch.setenv("EGERIA_USER", "svcuser")
    monkeypatch.setenv("EGERIA_USER_PASSWORD", "svc-test-password")


def _jwt(sub, exp_in=3600, salt=""):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b"=").decode()
    return f"{enc({'alg': 'none'})}.{enc({'sub': sub, 'exp': int(time.time()) + exp_in, 'n': salt})}.sig"


PETER, ERIN = _jwt("peter"), _jwt("erin")
FORGED_PETER = _jwt("peter", salt="forged")      # same `sub`, different (unsigned) token
EXPIRED = _jwt("peter", exp_in=-60)


def _as(token):
    """Run the body with `token` as the current request's X-Egeria-Token."""
    class _Ctx:
        def __enter__(self):
            self.reset = egeria_auth._egeria_token.set(token)

        def __exit__(self, *exc):
            egeria_auth._egeria_token.reset(self.reset)
    return _Ctx()


class _Counting:
    """A pyegeria stand-in: every method call is counted and returns an empty result."""
    def __init__(self, result=None):
        self.calls = 0
        self.result = [] if result is None else result

    def __getattr__(self, name):
        def call(*a, **k):
            self.calls += 1
            return self.result
        return call


def _app(module):
    app = FastAPI()
    app.add_middleware(egeria_auth.EgeriaTokenMiddleware)
    app.include_router(module.router)
    return TestClient(app)


# ── cache families served through a route: (setup, path, cache) ───────────────

def _collections(monkeypatch, mgr):
    import collections_handler as m
    m._TREE_CACHE.clear()
    monkeypatch.setattr(m, "_get_manager", lambda *a, **k: mgr)
    return m, m._TREE_CACHE


def _sa_folios(monkeypatch, mgr):
    import solution_architect_handler as m
    m._BP_FOLIO_CACHE.clear()
    monkeypatch.setattr(m, "_get_manager", lambda *a, **k: mgr)
    return m, m._BP_FOLIO_CACHE


def _sa_tree(monkeypatch, mgr):
    import solution_architect_handler as m
    m._COMP_TREE_CACHE.clear()
    monkeypatch.setattr(m, "_get_manager", lambda *a, **k: mgr)
    monkeypatch.setattr(m, "_get_classification_explorer", lambda *a, **k: mgr)
    return m, m._COMP_TREE_CACHE


OLDEST = [{"elementHeader": {"versions": {"createTime": "2020-01-01T00:00:00.000+00:00"}}}]


def _oldest(monkeypatch, mgr):
    import catalog_search_handler as m
    m._oldest_cache.clear()
    mgr.result = OLDEST
    monkeypatch.setattr(m, "_classification_explorer", lambda *a, **k: mgr)
    return m, m._oldest_cache


ROUTES = [
    (_collections, "/api/collections/root-1/tree"),
    (_collections, "/api/collections/node-1/children"),
    (_sa_folios, "/api/solution/blueprints/folios"),
    (_sa_tree, "/api/solution/components/tree"),
    (_oldest, "/api/catalog/oldest-create-time"),
]


@pytest.mark.parametrize("setup,path", ROUTES)
def test_two_tokens_never_share_an_entry(monkeypatch, setup, path):
    mgr = _Counting()
    module, _ = setup(monkeypatch, mgr)
    c = _app(module)
    assert c.get(path, headers={"X-Egeria-Token": PETER}).status_code == 200
    first = mgr.calls
    assert first > 0
    assert c.get(path, headers={"X-Egeria-Token": ERIN}).status_code == 200
    assert mgr.calls > first, "erin was served peter's cached entry"
    second = mgr.calls
    assert c.get(path, headers={"X-Egeria-Token": FORGED_PETER}).status_code == 200
    assert mgr.calls > second, "a token forging peter's `sub` was served peter's cached entry"


@pytest.mark.parametrize("setup,path", ROUTES)
def test_same_token_on_a_repeat_call_hits_the_cache(monkeypatch, setup, path):
    mgr = _Counting()
    module, _ = setup(monkeypatch, mgr)
    c = _app(module)
    c.get(path, headers={"X-Egeria-Token": PETER})
    first = mgr.calls
    assert first > 0
    assert c.get(path, headers={"X-Egeria-Token": PETER}).status_code == 200
    assert mgr.calls == first, "repeat call with the same token went back to Egeria"


@pytest.mark.parametrize("setup,path", ROUTES)
def test_an_expired_token_neither_reads_nor_fills_the_cache(monkeypatch, setup, path):
    mgr = _Counting()
    module, cache = setup(monkeypatch, mgr)
    c = _app(module)
    c.get(path, headers={"X-Egeria-Token": EXPIRED})
    c.get(path, headers={"X-Egeria-Token": EXPIRED})
    assert cache == {}, "an expired token's answer was cached"


def test_collections_as_of_time_and_lineage_stay_in_the_key(monkeypatch):
    m, cache = _collections(monkeypatch, _Counting())
    c = _app(m)
    c.get("/api/collections/root-1/tree", headers={"X-Egeria-Token": PETER})
    c.get("/api/collections/root-1/tree", headers={"X-Egeria-Token": PETER},
          params={"as_of_time": "2026-11-06T00:00:00.000Z"})
    c.get("/api/collections/root-1/tree", headers={"X-Egeria-Token": PETER, "X-Egeria-For-Lineage": "true"})
    assert len(cache) == 3
    assert any(k.endswith("|fl") for k in cache)
    assert any("|2026-11-06T00:00:00.000Z" in k for k in cache)


def test_oldest_create_time_reads_with_the_callers_token(monkeypatch):
    import catalog_search_handler as m
    m._oldest_cache.clear()
    seen = []

    def explorer(url, server, user_id, user_pwd, token=None):
        seen.append(token)
        return _Counting(OLDEST)

    monkeypatch.setattr(m, "_classification_explorer", explorer)
    r = _app(m).get("/api/catalog/oldest-create-time", headers={"X-Egeria-Token": PETER})
    assert r.json() == {"createTime": OLDEST[0]["elementHeader"]["versions"]["createTime"]}
    assert seen == [PETER], "the lookup did not carry the caller's token"


# ── operations: integration-connectors report cache ───────────────────────────

def _operations(monkeypatch):
    import operations_handler as m
    keys = []

    async def client(*a, **k):
        return object()

    def report(rm, server_guid, key):
        keys.append(key)
        return None, False, True      # "loading": the route answers at once

    monkeypatch.setattr(m, "_runtime_manager_async", client)
    monkeypatch.setattr(m, "_automated_curation_async", client)
    monkeypatch.setattr(m, "_get_server_report_cached", report)
    return m, keys


def test_integration_connector_reports_are_keyed_per_token(monkeypatch):
    m, keys = _operations(monkeypatch)
    c = _app(m)
    for tok in (PETER, ERIN, FORGED_PETER, PETER):
        r = c.get("/api/operations/integration-connectors", params={"server_guid": "srv-1"},
                  headers={"X-Egeria-Token": tok})
        assert r.status_code == 200, r.text
    assert len(set(keys[:3])) == 3, "two tokens shared one report cache entry"
    assert keys[3] == keys[0], "the same token got a different key"
    assert all(k.startswith("srv-1|") for k in keys), "server_guid must stay first (_invalidate_server_cache)"


def test_an_expired_token_gets_401_and_no_report(monkeypatch):
    m, keys = _operations(monkeypatch)
    r = _app(m).get("/api/operations/integration-connectors", params={"server_guid": "srv-1"},
                    headers={"X-Egeria-Token": EXPIRED})
    assert r.status_code == 401
    assert keys == []


# ── tech catalog: list caches and survey types ────────────────────────────────

def _list_key(token):
    import tech_catalog_handler as tc
    with _as(token):
        return tc._list_key("assets", None, None, None, None, False, None)


def test_tech_catalog_list_key_is_the_presented_credential():
    peter, erin, forged = _list_key(PETER), _list_key(ERIN), _list_key(FORGED_PETER)
    assert len({peter, erin, forged}) == 3, "two tokens (or a forged sub) shared a list cache key"
    assert _list_key(PETER) == peter
    assert "peter" not in peter                       # neither the claim nor the token is in the key


def test_tech_catalog_list_key_refuses_an_expired_token():
    with pytest.raises(HTTPException) as exc:
        _list_key(EXPIRED)
    assert exc.value.status_code == 401


def test_survey_types_are_built_once_as_the_service_user_for_everyone(monkeypatch):
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
                  params={"user_id": "x"})
    assert first.json().get("loading") is True
    # built with no caller credentials and no caller URL: the env service user on the env platform
    assert clients == [(None, None, None, None, None)]
    for _ in range(50):                                   # let the background Task finish
        if tc._SURVEY_TYPES_CACHE:
            break
        time.sleep(0.02)
    assert list(tc._SURVEY_TYPES_CACHE) and all(k.startswith("svc:") for k in tc._SURVEY_TYPES_CACHE)
    for tok in (ERIN, EXPIRED):                           # one shared entry, no second build
        assert c.get("/api/tech-catalog/survey-types", headers={"X-Egeria-Token": tok}).json() == \
            {"items": [{"guid": "s1", "displayName": "Survey"}]}
    assert len(clients) == 1


# ── async client factories act only as the token's user ───────────────────────

class _Client:
    """A pyegeria client stand-in: the real constructors call the platform (/api/about)."""
    def __init__(self, *a, view_server=None, server_name=None, platform_url=None, user_id=None,
                 user_pwd=None, token=None, **k):
        self.view_server = view_server or server_name
        self.server_name = self.view_server
        self.platform_url, self.user_id, self.user_pwd = platform_url, user_id, user_pwd
        self.token = token

    def set_bearer_token(self, token):
        self.token = token

    async def _async_create_egeria_bearer_token(self):
        raise AssertionError("signed in with the client's own (service) credentials")


@pytest.fixture
def _fake_clients(monkeypatch):
    import pyegeria
    import catalog_search_handler as cs
    for name in ("AutomatedCuration", "AssetMaker", "GovernanceOfficer"):
        monkeypatch.setattr(pyegeria, name, _Client)
    monkeypatch.setattr(cs, "ClassificationExplorer", _Client)


@pytest.mark.parametrize("factory", ["_automated_curation_async", "_async_asset_maker", "_governance_officer_async"])
def test_async_factories_take_the_tokens_user_and_drop_the_service_password(_fake_clients, factory):
    import asyncio
    import tech_catalog_handler as tc
    client = asyncio.run(getattr(tc, factory)(None, None, None, None, token=PETER))
    assert client.user_id == "peter", "a 401 retry would sign in as the service user"
    assert not client.user_pwd, "the service password stayed on a token user's client"


def test_classification_explorer_takes_the_tokens_user(_fake_clients):
    import catalog_search_handler as cs
    ce = cs._classification_explorer(None, None, None, None, token=PETER)
    assert ce.user_id == "peter"
    assert not ce.user_pwd


# ── background work runs as the caller ────────────────────────────────────────

def test_component_groups_build_runs_with_the_callers_token(monkeypatch):
    """The background build started in an empty context, so it ran as the service user."""
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
    keys = list(sa._COMP_GROUPS_CACHE)
    done.clear()
    c.get("/api/solution/components/groups", headers={"X-Egeria-Token": ERIN})
    assert done.wait(5)
    assert len(set(sa._COMP_GROUPS_CACHE) - set(keys)) == 1, "erin's groups were not a separate entry"


def test_notelog_subject_enrichment_runs_with_the_callers_token(monkeypatch):
    import notelog_handler as nl
    seen = []
    log = {"elementHeader": {"guid": "log-1"}, "properties": {"qualifiedName": "NoteLog::x"}}

    def enrich(creds, qn, guid):
        seen.append(egeria_auth.get_request_token())
        return None

    monkeypatch.setattr(nl, "_get_manager", lambda *a, **k: _Counting())
    monkeypatch.setattr(nl, "_find_note_logs", lambda *a, **k: [log])
    monkeypatch.setattr(nl, "_enrich_subjects_in_thread", enrich)
    r = _app(nl).get("/api/notelogs/log-1", headers={"X-Egeria-Token": PETER})
    assert r.status_code == 200, r.text
    assert seen == [PETER], "the enrichment thread ran without the caller's token (as the service user)"
