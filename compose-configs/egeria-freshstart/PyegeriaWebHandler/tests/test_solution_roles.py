"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

SolutionActorRole on the Solution Architect page: /api/solution/roles (list, get by guid), the type-nav-map entry and the
in-app dispatcher. A SolutionActorRole is the DESIGN-time role of a solution; it is an ActorRole by supertype, and it must
never land on the Actors card.

The Egeria side is a recorded REAL shape (tests/fixtures/solution_actor_role_real_shape_2026_11_25_*.json and
solution_role_find_mixed_types_real_shape_2026_11_25_*.json, read-only captures of find_solution_roles and
get_solution_role_by_guid on the quickstart platform, with the image digest in the name). Nothing here is SYNTHETIC
except the two small empty-result bodies named as such.
"""
import glob
import json
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

import solution_architect_handler as sah

_DIR = Path(__file__).resolve().parent
_FX = _DIR / "fixtures"


def _fixture(pattern):
    paths = glob.glob(str(_FX / pattern))
    assert len(paths) == 1, f"expected one fixture for {pattern}, found {paths}"
    return json.loads(Path(paths[0]).read_text())


REAL = _fixture("solution_actor_role_real_shape_2026_11_25_*.json")
MIXED = _fixture("solution_role_find_mixed_types_real_shape_2026_11_25_*.json")


class FakeManager:
    """Stands in for pyegeria SolutionArchitect; records the kwargs of each call."""

    def __init__(self, listing=None, by_guid=None, boom=None):
        self.listing, self.by_guid, self.boom = listing, by_guid, boom
        self.find_calls, self.get_calls = [], []

    def find_solution_roles(self, **kw):
        self.find_calls.append(kw)
        if self.boom:
            raise self.boom
        return self.listing

    def get_solution_role_by_guid(self, guid, **kw):
        self.get_calls.append((guid, kw))
        return self.by_guid


@pytest.fixture
def app_client(monkeypatch):
    app = FastAPI()
    app.include_router(sah.router)

    def install(mgr):
        monkeypatch.setattr(sah, "_get_manager", lambda *a, **k: mgr)
        return TestClient(app)
    return install


def _by_name(items, name):
    return next(i for i in items if i["properties"]["displayName"] == name)


# ── list ──────────────────────────────────────────────────────────────────────────────────────────

def test_list_asks_for_the_solution_role_type_and_returns_only_it(app_client):
    # find_solution_roles with no type filter returns every ActorRole subtype (371 on the quickstart platform; a 200-row
    # page held 15 of the 23 solution roles), so the call carries the type AND the result is checked again.
    mgr = FakeManager(listing=MIXED["list"])
    r = app_client(mgr).get("/api/solution/roles")
    assert r.status_code == 200
    assert mgr.find_calls[0]["metadata_element_type"] == "SolutionActorRole"
    body = r.json()
    assert [x["typeName"] for x in body["roles"]] == ["SolutionActorRole"]   # PersonRole and GovernanceRole dropped
    assert body["total"] == 1


def test_list_rows_carry_only_what_the_type_returns(app_client):
    mgr = FakeManager(listing=REAL["list"])
    roles = app_client(mgr).get("/api/solution/roles").json()["roles"]
    assert [x["displayName"] for x in roles] == sorted([x["displayName"] for x in roles], key=str.lower)
    researcher = next(x for x in roles if x["displayName"] == "New Treatment Researcher")
    assert researcher["scope"] == "Within Solution" and researcher["identifier"] == "NewTreatmentResearcher"
    assert researcher["status"] == "ACTIVE" and researcher["actorRoleGroups"] == []
    assert all(x["title"] == "" for x in roles)            # the live type returns no title: empty, not invented
    member = next(x for x in roles if x["displayName"].endswith("Community Member"))
    assert member["actorRoleGroups"] == ["community-member"]


def test_list_with_no_roles_is_an_empty_list_not_an_error(app_client):
    # SYNTHETIC: an empty find result
    r = app_client(FakeManager(listing=[])).get("/api/solution/roles")
    assert r.status_code == 200 and r.json() == {"roles": [], "total": 0}


def test_list_on_a_non_list_answer_is_empty(app_client):
    # SYNTHETIC: pyegeria returns a string when nothing matches in some versions
    r = app_client(FakeManager(listing="No elements found")).get("/api/solution/roles")
    assert r.status_code == 200 and r.json()["roles"] == []


def test_list_failure_is_an_http_error(app_client):
    r = app_client(FakeManager(boom=RuntimeError("platform down"))).get("/api/solution/roles")
    assert r.status_code >= 400


# ── detail ────────────────────────────────────────────────────────────────────────────────────────

def test_detail_links_blueprints_and_components_and_marks_holders(app_client):
    mgr = FakeManager(by_guid=REAL["by_guid"])
    guid = REAL["by_guid"]["elementHeader"]["guid"]
    d = app_client(mgr).get(f"/api/solution/roles/{guid}").json()
    assert mgr.get_calls[0][0] == guid
    assert d["displayName"] == "Open Metadata Product Subscriber"
    assert len(d["blueprints"]) == 5 and all(b["typeName"] == "SolutionBlueprint" for b in d["blueprints"])
    assert len(d["components"]) == 3
    assert d["memberOf"] == []                      # nothing but blueprints on this role
    assert d["holders"] == []                       # a design role has no live holder by default
    assert all(b["guid"] for b in d["blueprints"] + d["components"])


def test_detail_of_a_role_with_no_links_is_all_empty_lists(app_client):
    runtime = _by_name(REAL["list"], "Runtime Manager")
    d = app_client(FakeManager(by_guid=runtime)).get("/api/solution/roles/x").json()
    assert d["blueprints"] == d["components"] == d["memberOf"] == d["holders"] == []
    assert d["identifier"] == "RUNTIME-MANAGER" and d["scope"] == ""


def test_detail_splits_member_of_by_type_and_dedupes_holders(app_client):
    # SYNTHETIC: a real element with one extra collection (a Folio) and the same holder on both holder keys
    el = json.loads(json.dumps(_by_name(REAL["list"], "Open Metadata Product Subscriber")))
    rel = json.loads(json.dumps(el["memberOfCollections"][0]))
    rel["relatedElement"]["elementHeader"]["type"]["typeName"] = "Folio"
    rel["relatedElement"]["elementHeader"]["guid"] = "folio-1"
    el["memberOfCollections"].append(rel)
    holder = {"relatedElement": {"elementHeader": {"guid": "h-1", "type": {"typeName": "Person"}},
                                 "properties": {"displayName": "Erin"}}, "relationshipHeader": {"type": {"typeName": "AssignmentScope"}}}
    el["rolePerformers"], el["assignedActors"] = [holder], [holder]
    d = app_client(FakeManager(by_guid=el)).get("/api/solution/roles/x").json()
    assert [m["guid"] for m in d["memberOf"]] == ["folio-1"]
    assert len(d["blueprints"]) == 5
    assert [h["displayName"] for h in d["holders"]] == ["Erin"]


@pytest.mark.parametrize("answer", [None, "", "not found"])
def test_detail_not_found_is_404(app_client, answer):
    r = app_client(FakeManager(by_guid=answer)).get("/api/solution/roles/nope")
    assert r.status_code == 404
