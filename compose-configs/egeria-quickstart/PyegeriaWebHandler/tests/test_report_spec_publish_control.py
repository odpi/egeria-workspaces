"""Stage 2: the Report Specs "Publish to / Withdraw from" control (BRIEF-SPEC-PUBLISH-STAGED-2026-11-12).

POST /api/report-specs/publish runs pyegeria's own report_spec_publish (6.2.40) as the signed-in user:
preview -> validate -> confirm -> process, the digest refusal, cache drop + sync after a process, and
refusals in words (no sign-in, built-in, restricted, folders not read, unknown folder, not held, a newer
copy in Egeria). Every Egeria-facing seam is a fake; the documents and checks are pyegeria's real ones.
Skipped without pyegeria >= 6.2.40.
"""
import base64
import json
import sys
import time
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

rsp = pytest.importorskip("pyegeria.view.report_spec_publish")

from pyegeria.view._output_format_models import FormatSet  # noqa: E402

PORTAL_QN = "ReportSpecFolder::Consumer::Portal"
ADVISOR_QN = "ReportSpecFolder::Consumer::EgeriaAdvisor"
CONSUMERS = {"status": "read", "reason": None,
             "consumers": [{"name": "Portal", "qualifiedName": PORTAL_QN, "status": "read"},
                           {"name": "EgeriaAdvisor", "qualifiedName": ADVISOR_QN, "status": "read"}]}


def _jwt(sub="peterprofile", exp_in=3600):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    return f"{enc({'alg': 'none'})}.{enc({'sub': sub, 'exp': time.time() + exp_in})}.sig"


TOKEN = _jwt()


def _fs(description="Projects of a team."):
    return FormatSet.model_validate({
        "target_type": "Project", "heading": "Team projects", "description": description,
        "formats": [{"types": ["TABLE"], "attributes": [{"name": "Display Name", "key": "display_name"}]}],
        "action": {"function": "ProjectManager.find_projects", "required_params": ["search_string"]}})


class World:
    def __init__(self):
        self.consumers = json.loads(json.dumps(CONSUMERS))
        self.source = {"source": "local", "label": "Team Projects"}
        self.registry = {"Team Projects": _fs()}
        self.tier = None                 # egeria_tier_info answer (held, public)
        self.restricted = {"status": "read", "specs": []}
        self.live = None
        self.runs = []
        self.run_answer = {"success": True, "commands_total": 2, "commands_succeeded": 2,
                           "validation_errors": [], "execution_errors": []}
        self.syncs = []


@pytest.fixture
def client(monkeypatch):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    import egeria_auth
    import report_spec_publish_handler as h
    w = World()
    monkeypatch.setattr(h, "_consumers", lambda: w.consumers)
    monkeypatch.setattr(h, "_registry", lambda: w.registry)
    monkeypatch.setattr(h, "_source", lambda name: w.source)
    monkeypatch.setattr(h, "_tier_info", lambda label: w.tier)
    monkeypatch.setattr(h, "_restricted_reader", lambda token: (lambda: w.restricted))
    monkeypatch.setattr(h, "_live_version", lambda token, guid: w.live)

    def run_as(token):
        def run(markdown, directive):
            w.runs.append((token, directive, markdown))
            return w.run_answer
        return run
    monkeypatch.setattr(h, "_run_as_user", run_as)
    import report_spec_sync
    monkeypatch.setattr(report_spec_sync, "start", lambda trigger="admin": w.syncs.append(trigger) or True)
    app = FastAPI()
    app.add_middleware(egeria_auth.EgeriaTokenMiddleware)
    app.include_router(h.router)
    return TestClient(app), w


def post(c, token=TOKEN, **body):
    body = {"spec_name": "Team Projects", "folder": "Portal", **body}
    headers = {"X-Egeria-Token": token} if token else {}
    return c.post("/api/report-specs/publish", json=body, headers=headers)


# ── refusals, in words ────────────────────────────────────────────────────────

def test_no_sign_in_is_refused_never_the_service_account(client):
    c, w = client
    r = post(c, token=None)
    assert r.status_code == 401 and r.json()["message"].startswith("Sign in to publish or withdraw a report spec")
    r = post(c, token=_jwt(exp_in=-10))
    assert r.status_code == 401 and w.runs == []


def test_a_built_in_spec_is_refused(client):
    c, w = client
    w.source = {"source": "builtin", "label": "Collections"}
    r = post(c, spec_name="Collections")
    assert r.status_code == 400
    assert r.json()["message"] == ("'Collections' is a pyegeria built-in spec: built-ins are published later, after "
                                   "consumer-folders phase 3 (a built-in is referenced, not copied, into Egeria).")


def test_a_restricted_spec_is_refused_never_declassified(client):
    c, w = client
    w.restricted = {"status": "read", "specs": [{"label": "Team Projects", "zones": ["finance"]}]}
    r = post(c)
    assert r.status_code == 400 and "restricted publish comes later, after the zone proof" in r.json()["message"]
    assert "finance" in r.json()["message"] and w.runs == []


def test_folders_not_read_is_refused(client):
    c, w = client
    w.consumers = {"status": "not read", "reason": "no sync yet", "consumers": []}
    r = post(c)
    assert r.status_code == 409 and r.json()["message"].startswith("The consumer folders were not read (no sync yet)")


def test_an_unknown_folder_is_refused(client):
    c, _ = client
    r = post(c, folder="Elsewhere")
    assert r.status_code == 400 and "not one of the consumer folders the last sync found (EgeriaAdvisor, Portal)" in r.json()["message"]


def test_an_unknown_spec_is_404(client):
    c, w = client
    w.registry = {}
    assert post(c).status_code == 404


def test_withdraw_needs_a_spec_held_in_egeria(client):
    c, _ = client
    r = post(c, action="withdraw")
    assert r.status_code == 400 and r.json()["message"].startswith("'Team Projects' is not held in Egeria")


def test_without_pyegeria_6_2_40_it_says_so(client, monkeypatch):
    import report_spec_publish_handler as h
    c, _ = client
    def missing():
        raise h.Refused("Publishing needs pyegeria 6.2.40 or later (pyegeria.view.report_spec_publish): x", 501)
    monkeypatch.setattr(h, "_publish_module", missing)
    assert post(c).status_code == 501


# ── preview -> validate -> confirm -> process ─────────────────────────────────

def test_preview_shows_the_exact_document_and_sends_nothing(client):
    c, w = client
    r = post(c, step="preview")
    d = r.json()
    assert r.status_code == 200 and d["step"] == "preview" and d["verb"] == "Create" and w.runs == []
    md = d["markdown"]
    assert "## Create Report Spec" in md and f"### Collection Id\n{PORTAL_QN}" in md and "Parent ID" not in md
    assert d["folders"] == [PORTAL_QN] and d["digest"] == rsp.document_digest(md)
    assert d["steps"][-1] == f"add it to {PORTAL_QN}"
    assert "held" not in d


def test_validate_runs_as_the_user(client):
    c, w = client
    d = post(c, step="validate").json()
    assert d["step"] == "validate" and w.runs[0][:2] == (TOKEN, "validate") and "after" not in d


def test_process_needs_a_confirm(client):
    c, w = client
    digest = post(c, step="preview").json()["digest"]
    r = post(c, step="process", digest=digest, confirmed=False)
    assert r.status_code == 400 and r.json()["message"] == "Confirm first: the document runs as you, and writes to Egeria."
    assert w.runs == []


def test_process_runs_the_previewed_document_then_drops_and_syncs(client, monkeypatch):
    import report_specs_handler as rsh
    from result_cache import ResultCache
    cache = ResultCache(ttl=300)
    cache.put(("Team Projects", "TABLE", "{}"), b"x")
    cache.put(("egeria:Team Projects@v3", "TABLE", "{}"), b"y")
    cache.put(("Other", "TABLE", "{}"), b"z")
    monkeypatch.setattr(rsh, "_RESULT_CACHE", cache)
    c, w = client
    prev = post(c, step="preview").json()
    d = post(c, step="process", digest=prev["digest"], confirmed=True).json()
    assert w.runs == [(TOKEN, "process", prev["markdown"])]
    assert d["result"]["success"] is True
    assert d["after"]["invalidate"] == ["Team Projects"] and d["after"]["syncStarted"] is True
    assert d["after"]["resultsDropped"] == 2 and w.syncs == ["publish"]
    assert cache.lookup(("Other", "TABLE", "{}"))[0] != "miss"


def test_a_document_that_changed_since_the_preview_is_refused(client):
    c, w = client
    digest = post(c, step="preview").json()["digest"]
    w.registry = {"Team Projects": _fs("Someone changed the spec meanwhile.")}
    r = post(c, step="process", digest=digest, confirmed=True)
    assert r.status_code == 400 and r.json()["message"].startswith("The document changed since you previewed it")
    assert w.runs == []


def test_egeria_refusing_the_write_is_shown_in_its_words(client):
    c, w = client
    w.run_answer = {"success": False, "commands_total": 2, "commands_succeeded": 0, "validation_errors": [],
                    "execution_errors": [{"command": "Add Member to Collection",
                                          "message": "OMAG-SECURITY-403-001 peterprofile is not authorized"}]}
    digest = post(c, step="preview").json()["digest"]
    d = post(c, step="process", digest=digest, confirmed=True).json()
    assert d["result"]["success"] is False and "is not authorized" in d["result"]["execution_errors"][0]["message"]
    assert "after" not in d and w.syncs == []


# ── a spec already held in Egeria (public) ────────────────────────────────────

def test_held_public_spec_updates_when_the_portals_copy_is_current(client):
    c, w = client
    w.source = {"source": "egeria", "label": "Team Projects"}
    w.tier = {"guid": "g-1", "header_version": 4}
    w.live = 4
    d = post(c, step="preview").json()
    assert d["verb"] == "Update" and "## Update Report Spec" in d["markdown"]


def test_held_public_spec_newer_in_egeria_is_refused(client):
    c, w = client
    w.tier, w.live = {"guid": "g-1", "header_version": 4}, 5
    r = post(c, step="preview")
    assert r.status_code == 409 and "Egeria has version 5, the Portal's copy is version 4" in r.json()["message"]
    assert "sync first" in r.json()["message"]


def test_held_public_spec_version_unreadable_is_refused(client):
    c, w = client
    w.tier, w.live = {"guid": "g-1", "header_version": 4}, None
    r = post(c, step="preview")
    assert r.status_code == 409 and "Could not tell whether" in r.json()["message"]


def test_withdraw_a_held_spec(client):
    c, w = client
    w.tier = {"guid": "g-1", "header_version": 4}
    d = post(c, action="withdraw", folder="EgeriaAdvisor", step="preview").json()
    assert "## Remove Member from Collection" in d["markdown"] and ADVISOR_QN in d["markdown"]
    assert "Create Report Spec" not in d["markdown"] and "Update Report Spec" not in d["markdown"]


def test_a_bad_action_is_refused(client):
    c, _ = client
    r = post(c, action="delete")
    assert r.status_code == 400 and r.json()["message"] == "The action must be publish or withdraw, not 'delete'."


# ── wiring ────────────────────────────────────────────────────────────────────

def test_result_cache_drop():
    from result_cache import ResultCache
    cache = ResultCache(ttl=300)
    cache.put(("a",), 1)
    cache.put(("b",), 2)
    assert cache.drop(lambda k: k[0] == "a") == 1 and cache.lookup(("a",))[0] == "miss"


def test_router_is_registered_and_the_floor_is_6_2_40():
    assert "from report_spec_publish_handler import router as report_spec_publish_router" in (ROOT / "pyegeria_handler.py").read_text()
    assert (ROOT / "requirements.txt").read_text().splitlines()[6].startswith("pyegeria>=6.2.40")
    assert "ARG PYEGERIA_VERSION=pyegeria>=6.2.40" in (ROOT / "Dockerfile-fast-api").read_text()


def test_the_handler_never_falls_back_to_a_password():
    src = (ROOT / "report_spec_publish_handler.py").read_text()
    assert "use_token(client, token)" in src and "create_egeria_bearer_token" not in src
    assert "EGERIA_USER_PASSWORD" not in src


# ── the page ──────────────────────────────────────────────────────────────────

TE = (ROOT / "type-explorer.html").read_text()
CONTROL = TE[TE.index("function RsPublishControl("):TE.index("function ReportSpecDetail(")]


def test_the_control_sits_beside_used_by_and_gets_the_folders():
    assert "React.createElement(RsPublishControl, { spec: spec, consumers: consumers })" in TE
    assert "consumers: consumersInfo })" in TE


def test_preview_shows_the_document_and_confirm_gates_process():
    assert "egeriaFetch('/api/report-specs/publish', creds" in CONTROL
    assert "className: 'rs-publish-doc'" in CONTROL and "plan.markdown" in CONTROL
    assert "disabled: !!busy || !confirmed" in CONTROL                       # Publish/Withdraw needs the tick
    assert "confirmed: step === 'process' ? confirmed : false, digest: plan ? plan.digest : null" in CONTROL


def test_no_control_for_built_ins_folders_not_read_or_no_sign_in():
    assert "spec.source === 'builtin'" in CONTROL and "built-in specs are published later" in CONTROL
    assert "consumers.status === 'not read'" in CONTROL and "there is nowhere to publish to yet" in CONTROL
    assert "!creds || !creds.token" in CONTROL and "Sign in to publish or withdraw this spec" in CONTROL
    assert "setError(d.message || d.detail" in CONTROL                       # refusals in the server's words


def test_the_runner_dispatches_as_the_token_user_with_no_password(monkeypatch):
    """_run_as_user: a client that holds the caller's token and no password, Dr.Egeria's own dispatcher, and
    the Portal's usual response shape (dr_egeria_commands_handler._build_execute_response)."""
    import pyegeria
    import md_processing.dr_egeria as dre
    import report_spec_publish_handler as h
    made, seen = [], {}

    class FakeClient:
        def __init__(self, server, url, user_id=None):
            self.server, self.url, self.user_id, self.user_pwd = server, url, user_id, "service-secret"
            made.append(self)

        def set_bearer_token(self, token):
            self.token = token

    class FakeDispatcher:
        async def dispatch_batch(self, commands, context=None):
            seen["n"], seen["directive"] = len(commands), context["directive"]
            return [{"is_command": True, "status": "success", "verb": "Create", "object_type": "Report Spec",
                     "output": "created", "qualified_name": "ReportSpec::Team Projects"},
                    {"is_command": True, "status": "success", "verb": "Add Member", "object_type": "to Collection",
                     "output": "added"}]

    monkeypatch.setattr(pyegeria, "EgeriaTech", FakeClient)
    monkeypatch.setattr(dre, "setup_dispatcher", lambda client: FakeDispatcher())
    plan = rsp.build_publish_document("Team Projects", _fs(), folders=[PORTAL_QN])
    out = h._run_as_user(TOKEN)(plan["markdown"], "process")
    client = made[0]
    assert client.token == TOKEN and client.user_pwd is None and client.user_id == "peterprofile"
    from md_processing.v2 import UniversalExtractor
    assert seen == {"n": len(UniversalExtractor(plan["markdown"]).extract_commands()), "directive": "process"}
    assert out["success"] is True and out["commands_total"] == 2 and out["commands_succeeded"] == 2
    assert out["created_elements"][0]["qualified_name"] == "ReportSpec::Team Projects"
