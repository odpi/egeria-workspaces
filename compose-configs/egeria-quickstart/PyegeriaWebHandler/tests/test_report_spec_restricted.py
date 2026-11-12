"""Portal-3: zone-restricted report specs, per signed-in user (BRIEF-LD-REMAINING-PHASES §2, D5).

- Listed with pyegeria's list_visible_restricted_specs AS THE USER's token; cached per credential identity
  (the token's hash), never by bare user id, never in the shared cache or registry; dropped after a sync.
- Described and run fetched from Egeria as the user (refresh_spec / fetch_spec_for_call), never a shared
  copy, never cached; the public execute route refuses the internal name of a spec fetched this way.
- Each answer is said: not signed in, unsupported, read failed, partial, none visible, ok.
Every Egeria-facing seam is faked; nothing talks to Egeria.
"""
import base64
import json
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import report_spec_restricted as rsr  # noqa: E402


def _jwt(sub="peterprofile", exp_in=3600, nonce="a"):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    return f"{enc({'alg': 'none'})}.{enc({'sub': sub, 'exp': time.time() + exp_in, 'n': nonce})}.sig"


TOKEN = _jwt()
SPEC = {"label": "Finance Secrets", "qualified_name": "ReportSpec::Finance Secrets", "guid": "g-fin",
        "version": 3, "zones": ["finance"], "folders": ["ReportSpecFolder::Consumer::Portal::Finance"]}
INDEX = {"status": "read", "consumers": [{"name": "Portal", "qualifiedName": "ReportSpecFolder::Consumer::Portal"}],
         "index": {}}


class World:
    def __init__(self):
        self.answer = {"status": "read", "specs": [SPEC], "folders": ["ReportSpecFolder::Consumer::Portal"]}
        self.reads = []
        self.raise_read = None


@pytest.fixture
def world(monkeypatch):
    import report_spec_consumers
    w = World()

    class Client:
        def __init__(self, token):
            self.token = token

    def reader(client, folders=None):
        w.reads.append((client.token, folders))
        if w.raise_read:
            raise w.raise_read
        return json.loads(json.dumps(w.answer))
    monkeypatch.setattr(rsr, "_reader", lambda: reader)
    monkeypatch.setattr(rsr, "_user_client", lambda token: Client(token))
    monkeypatch.setattr(rsr, "_platform", lambda token: ("https://localhost:9443", "qs-view-server"))
    monkeypatch.setattr(rsr, "_folders", lambda: ["ReportSpecFolder::Consumer::Portal"])
    monkeypatch.setattr(report_spec_consumers, "index", lambda: INDEX)
    rsr._reset_for_tests()
    yield w
    rsr._reset_for_tests()


# ── listing ───────────────────────────────────────────────────────────────────

def test_no_token_is_sign_in_not_an_empty_list(world):
    got = rsr.restricted_specs(None)
    assert got["state"] == "not_signed_in" and got["message"] == rsr.SIGN_IN and world.reads == []


def test_an_old_pyegeria_says_so(world, monkeypatch):
    monkeypatch.setattr(rsr, "_reader", lambda: None)
    got = rsr.restricted_specs(TOKEN)
    assert got["state"] == "unsupported" and "6.2.35" in got["message"]


def test_listed_as_the_user_with_the_badge_and_used_by(world):
    got = rsr.restricted_specs(TOKEN)
    assert got["state"] == "ok" and got["viewer"] == "peterprofile" and got["badge"] == "restricted (visible to you)"
    assert world.reads == [(TOKEN, ["ReportSpecFolder::Consumer::Portal"])]          # the user's own token
    assert got["specs"][0]["label"] == "Finance Secrets" and got["specs"][0]["zones"] == ["finance"]
    assert got["specs"][0]["usedBy"] == ["Portal"]                                    # a sub-folder of Portal


@pytest.mark.parametrize("answer,state,words", [
    ({"status": "read", "specs": [], "reason": "the folders hold no restricted spec this user may see"},
     "none_visible", "the folders hold no restricted spec this user may see"),
    ({"status": "read", "specs": []}, "none_visible", "No restricted report specs are visible to peterprofile."),
    ({"status": "partial", "specs": [SPEC], "reason": "one folder not read"}, "partial",
     "Restricted report specs were partly read: one folder not read"),
    ({"status": "not read", "specs": [], "reason": "root not found"}, "read_failed",
     "Restricted report specs were not read: root not found"),
])
def test_each_answer_is_said(world, answer, state, words):
    world.answer = answer
    got = rsr.restricted_specs(TOKEN)
    assert got["state"] == state and got["message"] == words


def test_cached_per_credential_never_by_user_id(world):
    assert rsr.restricted_specs(TOKEN)["cached"] is False
    assert rsr.restricted_specs(TOKEN)["cached"] is True and len(world.reads) == 1
    other = _jwt(nonce="b")                              # the same user, another sign-in
    assert rsr.restricted_specs(other)["cached"] is False and len(world.reads) == 2
    assert rsr.credential_key(TOKEN) != rsr.credential_key(other)


def test_a_failed_read_is_said_and_never_cached(world):
    world.raise_read = ConnectionError("platform down /internal")
    got = rsr.restricted_specs(TOKEN)
    assert got["state"] == "read_failed" and "internal" not in got["message"]
    world.raise_read = None
    assert rsr.restricted_specs(TOKEN)["state"] == "ok"


def test_a_refused_token_raises(world):
    class Refused(Exception):
        http_error_code = 401
    world.raise_read = Refused("HTTP Code: 401")
    with pytest.raises(rsr.TokenRefused):
        rsr.restricted_specs(TOKEN)


def test_nothing_reaches_the_shared_registry(world):
    from pyegeria.view.base_report_formats import get_report_registry
    rsr.restricted_specs(TOKEN)
    assert "Finance Secrets" not in get_report_registry()


def test_a_sync_drops_the_listings(world, monkeypatch):
    import report_spec_sync as rss
    import pyegeria.view.egeria_spec_cache as esc

    class Rep:
        def to_dict(self):
            return {"folders": [], "added": [], "updated": [], "unchanged": [], "pruned": [], "skipped": []}
    monkeypatch.setattr(esc, "sync_report_specs", lambda client, shared=True: Rep())
    monkeypatch.setattr(rss, "_service_client", lambda: None)
    monkeypatch.setattr(rss, "_reconcile_fallbacks", lambda: None)
    monkeypatch.setattr(rss, "configured_folders", lambda: ["F"])
    rsr.restricted_specs(TOKEN)
    assert rss._sync_once() == "synced"
    assert rsr.restricted_specs(TOKEN)["cached"] is False


# ── describe and run: fetched as the user ─────────────────────────────────────

def _fs():
    from pyegeria.view._output_format_models import FormatSet
    return FormatSet.model_validate({
        "target_type": "Asset", "heading": "Finance", "description": "Secret finance assets.",
        "formats": [{"types": ["TABLE", "DICT"], "attributes": [{"name": "Name", "key": "display_name"}]}],
        "action": {"function": "AssetMaker.find_assets", "required_params": ["search_string"]}})


def test_describe_fetches_as_the_user(world, monkeypatch):
    import pyegeria.view.egeria_spec_cache as esc
    calls = []
    monkeypatch.setattr(esc, "fetch_spec_for_call", lambda client, label: calls.append((client.token, label))
                        or f"egeria:{label}@v3")
    monkeypatch.setattr(esc, "_FETCHED", {("Finance Secrets", 3): (_fs(), {})})
    monkeypatch.setattr(esc, "fetched_spec", lambda name: _fs())
    row = rsr.describe(TOKEN, "Finance Secrets")
    assert calls == [(TOKEN, "Finance Secrets")]
    assert row["restricted"] is True and row["source"] == "restricted" and row["sourceLabel"] == rsr.BADGE
    assert row["zones"] == ["finance"] and row["output_types"] == ["DICT", "TABLE"]
    assert rsr.is_restricted_fetch("egeria:Finance Secrets@v3") and rsr.is_restricted_fetch("Finance Secrets@v3")


def test_describe_and_run_refuse_a_spec_not_visible(world):
    with pytest.raises(LookupError):
        rsr.describe(TOKEN, "Someone Elses")
    with pytest.raises(LookupError):
        rsr.run(TOKEN, "Someone Elses", output_format="TABLE")


# ── routes ────────────────────────────────────────────────────────────────────

@pytest.fixture
def app(world, monkeypatch):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    import egeria_auth
    import report_specs_handler as rh
    import pyegeria.view.format_set_executor as fse
    runs = []

    def fake_exec(name, **kw):
        runs.append((name, kw))
        return {"kind": "json", "data": [{"Name": "secret asset"}]}
    monkeypatch.setattr(fse, "exec_report_spec", fake_exec)
    a = FastAPI()
    a.add_middleware(egeria_auth.EgeriaTokenMiddleware)
    a.include_router(rh.router)
    return TestClient(a), runs


def test_route_lists_as_the_signed_in_user(app):
    c, _ = app
    assert c.get("/api/report-specs/restricted").json()["state"] == "not_signed_in"
    got = c.get("/api/report-specs/restricted", headers={"X-Egeria-Token": TOKEN}).json()
    assert got["state"] == "ok" and got["specs"][0]["label"] == "Finance Secrets"


def test_restricted_run_needs_a_token(app):
    c, runs = app
    r = c.post("/api/report-specs/execute", json={"spec_name": "Finance Secrets", "output_format": "TABLE",
                                                  "restricted": True})
    assert r.status_code == 401 and r.json()["detail"] == rsr.SIGN_IN and runs == []


def test_restricted_run_is_fetched_as_the_user_and_never_cached(app):
    c, runs = app
    body = {"spec_name": "Finance Secrets", "output_format": "TABLE", "restricted": True, "cache": True,
            "user_id": "erinoverview", "user_pwd": "secret"}
    for _ in range(2):
        r = c.post("/api/report-specs/execute", json=body, headers={"X-Egeria-Token": TOKEN})
        assert r.status_code == 200 and r.json()["specSource"]["source"] == "restricted"
    assert len(runs) == 2                                                   # never served from a cache
    name, kw = runs[0]
    assert name == "Finance Secrets" and kw["refresh_spec"] is True and kw["token"] == TOKEN
    assert kw["user"] == "peterprofile" and kw["user_pass"] == ""          # never the service password


def test_restricted_run_of_a_spec_not_visible_is_404(app):
    c, runs = app
    r = c.post("/api/report-specs/execute", json={"spec_name": "Someone Elses", "output_format": "TABLE",
                                                  "restricted": True}, headers={"X-Egeria-Token": TOKEN})
    assert r.status_code == 404 and runs == []


def test_public_execute_refuses_a_restricted_fetched_name(app):
    c, runs = app
    rsr._RESTRICTED_FETCHED.add(("Finance Secrets", 3))
    r = c.post("/api/report-specs/execute", json={"spec_name": "egeria:Finance Secrets@v3", "output_format": "TABLE"})
    assert r.status_code == 403 and "fetched for one user's call" in r.json()["detail"] and runs == []


def test_public_execute_denies_fetched_names_by_default(app, monkeypatch):
    """Only a shared-tier (public) spec at exactly that version passes; any other fetched name is refused."""
    c, runs = app
    monkeypatch.setattr(rsr, "_shared_tier_version", lambda label: 2 if label == "Public Spec" else None)
    post = lambda n: c.post("/api/report-specs/execute", json={"spec_name": n, "output_format": "DICT"}).status_code
    assert post("egeria:Public Spec@v2") == 200 and post("Public Spec@v2") == 200
    assert post("egeria:Public Spec@v1") == 403                             # another version: not the tier's
    assert post("egeria:Unknown Spec@v4") == 403                            # not in the shared tier
    assert post("Public Spec") == 200                                       # not a fetched name: unchanged
    rsr._RESTRICTED_LABELS.add("Public Spec")                                # ... unless restricted-fetched
    assert post("egeria:Public Spec@v2") == 403


def test_a_concurrent_public_execute_during_a_restricted_run_is_refused(app, monkeypatch):
    """The window the read-back found: pyegeria holds "egeria:<label>@vN" while the restricted run is
    still going. The label is recorded before the fetch, so a public execute of that name is refused
    during the run, not only after it."""
    import pyegeria.view.format_set_executor as fse
    import report_specs_handler as rh
    from fastapi import HTTPException
    c, _ = app
    during = []

    def slow_restricted_exec(name, **kw):
        assert kw.get("refresh_spec") is True
        try:                                           # someone else, mid-run, asks for the fetched name
            rh._refuse_fetched_name(f"egeria:{name}@v3")
            during.append("ran")
        except HTTPException as exc:
            during.append(exc.status_code)
        return {"kind": "json", "data": []}
    monkeypatch.setattr(fse, "exec_report_spec", slow_restricted_exec)
    assert not rsr._RESTRICTED_LABELS and not rsr._RESTRICTED_FETCHED       # nothing recorded beforehand
    r = c.post("/api/report-specs/execute", json={"spec_name": "Finance Secrets", "output_format": "TABLE",
                                                  "restricted": True}, headers={"X-Egeria-Token": TOKEN})
    assert r.status_code == 200 and during == [403]


def test_describe_records_the_label_before_the_fetch(world, monkeypatch):
    import pyegeria.view.egeria_spec_cache as esc
    seen = []

    def fetch(client, label):
        seen.append(rsr.public_fetched_name_allowed(f"egeria:{label}@v3"))
        raise ConnectionError("platform went away")
    monkeypatch.setattr(esc, "fetch_spec_for_call", fetch)
    with pytest.raises(ConnectionError):
        rsr.describe(TOKEN, "Finance Secrets")
    assert seen == [False] and rsr.is_restricted_fetch("egeria:Finance Secrets@v9")


def test_describe_route_needs_a_token(app):
    c, _ = app
    assert c.get("/api/report-specs/restricted/Finance Secrets").status_code == 401


# ── the page ──────────────────────────────────────────────────────────────────

TE = (ROOT / "type-explorer.html").read_text()


def test_the_page_lists_restricted_specs_as_the_user_with_the_badge():
    assert "egeriaFetch('/api/report-specs/restricted', creds)" in TE
    assert "egeriaFetch('/api/report-specs/restricted/' + encodeURIComponent(row.label), creds)" in TE
    assert "restricted: { mark: 'R', color: '#f59e0b' }" in TE
    assert "'restricted (visible to you)'" in TE and "function RsRestrictedNote(" in TE


def test_the_page_runs_a_restricted_spec_with_the_token_only():
    run = TE[TE.index("function runReport()"):TE.index("function renderExecResults()")]
    assert "if (spec.restricted) body.restricted = true;" in run
    assert "if (creds.password && !spec.restricted) body.user_pwd = creds.password;" in run
    assert "egeriaFetch('/api/report-specs/execute', creds" in run


def test_the_publish_control_says_restricted_comes_later():
    assert "'Publish: restricted specs are published later, after the zone proof.'" in TE

