"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Solution Boundaries on the Solution Architect page (Portal boundary view, Part C): GET /api/solution/boundaries, /boundaries/{guid} and
/design-model-boundaries. READ-ONLY. The Egeria side is the REAL shape copied from egeria-python v6.3.4 (solution_boundary_retrieve_real_shape_..._5a8d6a12.json,
solution_blueprint_nested_boundaries_real_shape_..._5a8d6a12.json). The boundary FIND list, the DesignModelBoundary mixed-type find and the empty answer are
SYNTHETIC, built from those elements (the live quickstart platform has no SolutionBoundary). Every test that rests on a synthetic fixture says so.
Fixtures are never joined across files by GUID: the synthetic DMB element reuses the inner boundary's GUID on purpose.
"""
import copy
import inspect
import json
import re
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

import solution_architect_handler as sah

_FX = Path(__file__).resolve().parent / "fixtures"


def fx(name):
    return json.loads((_FX / name).read_text())


BOUNDARY = fx("solution_boundary_retrieve_real_shape_2026_11_25_5a8d6a12.json")                      # REAL: the outer boundary by GUID
BLUEPRINT = fx("solution_blueprint_nested_boundaries_real_shape_2026_11_25_5a8d6a12.json")           # REAL: blueprint > boundary > boundary > role
FIND = fx("solution_boundary_find_SYNTHETIC_from_5a8d6a12_elements.json")                           # SYNTHETIC
DMB = fx("design_model_boundary_find_mixed_SYNTHETIC_from_5a8d6a12_elements.json")                  # SYNTHETIC
EMPTY = fx("solution_boundary_find_SYNTHETIC_empty.json")                                           # SYNTHETIC
OUTER = BOUNDARY["elementHeader"]["guid"]
INNER = BOUNDARY["collectionMembers"][0]["relatedElement"]["elementHeader"]["guid"]
ROLE = BOUNDARY["collectionMembers"][0]["nestedElements"][0]["relatedElement"]["elementHeader"]["guid"]


class FakeSA:
    """Stands in for pyegeria SolutionArchitect: the async find and get only, recording their arguments."""

    def __init__(self, listing=None, by_guid=None, boom=None):
        self.listing, self.by_guid, self.boom = listing, by_guid, boom
        self.find_calls, self.get_calls = [], []

    async def _async_find_solution_boundaries(self, **kw):
        self.find_calls.append(kw)
        if self.boom:
            raise self.boom
        return self.listing

    async def _async_get_solution_boundary_by_guid(self, guid, **kw):
        self.get_calls.append((guid, kw))
        if self.boom:
            raise self.boom
        return self.by_guid


class FakeCM:
    def __init__(self, listing=None, boom=None):
        self.listing, self.boom, self.find_calls = listing, boom, []

    async def _async_find_collections(self, **kw):
        self.find_calls.append(kw)
        if self.boom:
            raise self.boom
        return self.listing


@pytest.fixture
def app_client(monkeypatch):
    app = FastAPI()
    app.include_router(sah.router)

    def install(sa=None, cm=None):
        async def get_sa(*a, **k):
            return sa

        async def get_cm(*a, **k):
            return cm
        monkeypatch.setattr(sah, "_get_manager_async", get_sa)
        monkeypatch.setattr(sah, "_get_collection_manager_async", get_cm)
        return TestClient(app)
    return install


# ── list ────────────────────────────────────────────────────────────────────────────────────────────────────────

def test_list_serializes_the_boundaries_sorted_by_name_and_asks_for_depth_zero(app_client):
    # rests on the SYNTHETIC find list (the outer and inner boundary of the real file)
    sa = FakeSA(listing=FIND["list"])
    r = app_client(sa).get("/api/solution/boundaries")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 2 and [b["displayName"] for b in body["boundaries"]] == ["probe-boundary-1-renamed", "probe-boundary-2"]
    outer = body["boundaries"][0]
    assert outer["guid"] == OUTER and outer["typeName"] == "SolutionBoundary" and outer["qualifiedName"] == "probe::boundary::1" and outer["status"] == "ACTIVE"
    assert outer["memberCount"] == 1 and body["boundaries"][1]["memberCount"] is None      # a find at depth 0 carries no members: null, not 0
    assert sa.find_calls[0]["graph_query_depth"] == 0 and sa.find_calls[0]["search_string"] == "*"


def test_list_empty_is_an_empty_list_not_an_error(app_client):
    # rests on the SYNTHETIC empty fixture: live has no SolutionBoundary today
    r = app_client(FakeSA(listing=EMPTY["list"])).get("/api/solution/boundaries")
    assert r.status_code == 200 and r.json() == {"boundaries": [], "total": 0}


@pytest.mark.parametrize("answer", ["No elements found", None, {}])
def test_list_on_a_non_list_answer_is_empty(app_client, answer):
    r = app_client(FakeSA(listing=answer)).get("/api/solution/boundaries")
    assert r.status_code == 200 and r.json()["boundaries"] == []


def test_list_failure_is_an_http_error(app_client):
    assert app_client(FakeSA(boom=RuntimeError("platform down"))).get("/api/solution/boundaries").status_code >= 400


def test_list_hides_templates_unless_asked(app_client):
    tpl = copy.deepcopy(FIND["list"][1])
    tpl["elementHeader"]["Template"] = {"class": "ElementClassification", "classificationName": "Template"}
    sa = FakeSA(listing=[FIND["list"][0], tpl])
    c = app_client(sa)
    assert c.get("/api/solution/boundaries").json()["total"] == 1
    assert c.get("/api/solution/boundaries", params={"include_templates": "true"}).json()["total"] == 2


# ── detail ──────────────────────────────────────────────────────────────────────────────────────────────────────

def test_detail_is_the_boundary_with_its_member_hierarchy_nested_to_depth(app_client):
    sa = FakeSA(by_guid=BOUNDARY)
    d = app_client(sa).get(f"/api/solution/boundaries/{OUTER}").json()
    assert sa.get_calls[0][0] == OUTER and sa.get_calls[0][1]["body"]["graphQueryDepth"] == 10
    assert d["guid"] == OUTER and d["displayName"] == "probe-boundary-1-renamed" and d["typeName"] == "SolutionBoundary"
    h = d["memberHierarchy"]
    assert h["complete"] is True and h["notes"] == [] and h["nodeCount"] == 2
    inner = h["members"][0]
    assert inner["guid"] == INNER and inner["isBoundary"] is True and inner["typeName"] == "SolutionBoundary" and inner["relationshipType"] == "CollectionMembership"
    role = inner["children"][0]
    assert role["guid"] == ROLE and role["typeName"] == "SolutionActorRole" and role["isBoundary"] is False and role["children"] == []


def test_detail_never_counts_a_parent_as_a_member(app_client):
    # in the real file the inner boundary's sideLinks lead UP to the outer boundary, and the outer boundary's memberOfCollections to a blueprint
    d = app_client(FakeSA(by_guid=BOUNDARY)).get(f"/api/solution/boundaries/{OUTER}").json()
    inner = d["memberHierarchy"]["members"][0]
    assert inner["alsoLinkedTo"] == [] and inner["children"][0]["alsoLinkedTo"] == []        # a side link back to the parent is not shown
    assert [m["typeName"] for m in d["memberOf"]] == ["SolutionBlueprint"]
    seen = {n["guid"] for n in _walk(d["memberHierarchy"]["members"])}
    assert OUTER not in seen and "SolutionBlueprint" not in {n["typeName"] for n in _walk(d["memberHierarchy"]["members"])}


def _walk(nodes):
    for n in nodes:
        yield n
        yield from _walk(n["children"])


def test_detail_shows_a_side_link_that_names_something_other_than_the_parent():
    el = copy.deepcopy(BOUNDARY)
    other = {"relationshipHeader": {"type": {"typeName": "CollectionMembership"}}, "relatedElement": {"elementHeader": {"guid": "other-1", "type": {"typeName": "SolutionBlueprint"}}, "properties": {"displayName": "other"}}}
    el["collectionMembers"][0]["sideLinks"].append(other)                                      # SYNTHETIC edit of a real element
    inner = sah._serialize_boundary_detail(el)["memberHierarchy"]["members"][0]
    assert [x["guid"] for x in inner["alsoLinkedTo"]] == ["other-1"]


def test_detail_carries_the_mermaid_graph_and_the_blueprint_it_is_in(app_client):
    d = app_client(FakeSA(by_guid=BOUNDARY)).get(f"/api/solution/boundaries/{OUTER}").json()
    assert d["mermaidGraph"].startswith("---") and "collectionMermaidMindMap" in d
    assert d["memberOf"][0]["typeName"] == "SolutionBlueprint" and d["memberOf"][0]["displayName"] == "probe-blueprint-1"


@pytest.mark.parametrize("answer", [None, "", "no such element", {}])
def test_detail_for_an_unknown_guid_is_a_404(app_client, answer):
    r = app_client(FakeSA(by_guid=answer)).get("/api/solution/boundaries/nope")
    assert r.status_code == 404 and "nope" in r.json()["detail"]


def test_detail_failure_is_an_http_error(app_client):
    assert app_client(FakeSA(boom=RuntimeError("platform down"))).get(f"/api/solution/boundaries/{OUTER}").status_code >= 400


# ── the cap and cycle guard (SYNTHETIC chains and loops, built in the test) ─────────────────────────────────────────

def member(guid, typ="SolutionBoundary", nested=None, side=None):
    m = {"relationshipHeader": {"type": {"typeName": "CollectionMembership"}}, "relatedElement": {"elementHeader": {"guid": guid, "type": {"typeName": typ}}, "properties": {"displayName": guid}}}
    if nested:
        m["nestedElements"] = nested
    if side:
        m["sideLinks"] = side
    return m


def top(guid, members):
    return {"elementHeader": {"guid": guid, "type": {"typeName": "SolutionBoundary"}}, "properties": {"displayName": guid}, "collectionMembers": members}


def chain(n):
    node = None
    for i in range(n, 0, -1):
        node = member(f"b{i}", nested=[node] if node else None)
    return [node]


def test_the_hierarchy_stops_at_eight_levels_and_says_so():
    h = sah._boundary_member_hierarchy(top("root", chain(12)))
    depth = len(list(_walk(h["members"])))
    assert depth == 8 and h["complete"] is False and any("8 levels" in n for n in h["notes"])
    last = list(_walk(h["members"]))[-1]
    assert last["deeperNotShown"] is True and last["children"] == []


def test_a_chain_of_exactly_eight_levels_is_complete():
    h = sah._boundary_member_hierarchy(top("root", chain(8)))
    assert len(list(_walk(h["members"]))) == 8 and h["complete"] is True


def test_the_hierarchy_stops_at_the_member_cap_and_says_so():
    h = sah._boundary_member_hierarchy(top("root", [member(f"c{i}", "SolutionComponent") for i in range(7)]), max_nodes=5)
    assert h["nodeCount"] == 5 and len(h["members"]) == 5 and any("5 members" in n for n in h["notes"]) and h["complete"] is False
    full = sah._boundary_member_hierarchy(top("root", [member(f"c{i}", "SolutionComponent") for i in range(500)]))
    assert full["nodeCount"] == 500 and full["complete"] is True


def test_a_boundary_that_contains_itself_through_nesting_stops_and_says_so():
    # root > a > b > a (a is already above it) and root > root (the boundary lists itself)
    h = sah._boundary_member_hierarchy(top("root", [member("a", nested=[member("b", nested=[member("a")])]), member("root")]))
    nodes = list(_walk(h["members"]))
    cycles = [n for n in nodes if n["cycle"]]
    assert sorted(n["guid"] for n in cycles) == ["a", "root"] and all(n["children"] == [] for n in cycles)
    assert h["complete"] is False and any("already above" in n for n in h["notes"])


def test_a_member_shared_by_two_branches_is_not_a_cycle():
    h = sah._boundary_member_hierarchy(top("root", [member("a", nested=[member("s")]), member("b", nested=[member("s")])]))
    assert h["complete"] is True and [n["guid"] for n in _walk(h["members"])].count("s") == 2


def test_malformed_members_are_skipped():
    el = top("root", [None, {"relatedElement": None}, {"nothing": 1}, member("ok")])
    el["collectionMembers"][3]["nestedElements"] = "oops"
    h = sah._boundary_member_hierarchy(el)
    assert [n["guid"] for n in h["members"]] == ["ok"]


def test_a_boundary_with_no_members_has_an_empty_complete_hierarchy():
    h = sah._boundary_member_hierarchy(top("root", None))
    assert h == {"members": [], "nodeCount": 0, "maxDepth": 8, "maxNodes": 500, "complete": True, "notes": []}


# ── design model boundaries ────────────────────────────────────────────────────────────────────────────────────

def test_the_dmb_list_excludes_solution_boundaries_by_type_name_synthetic(app_client):
    # rests on the SYNTHETIC mixed-type find: one real SolutionBoundary and one element whose only change is its typeName
    cm = FakeCM(listing=DMB["list"])
    body = app_client(cm=cm).get("/api/solution/design-model-boundaries").json()
    assert body["total"] == 1 and [b["typeName"] for b in body["boundaries"]] == ["DesignModelBoundary"]
    assert body["boundaries"][0]["displayName"] == "probe-boundary-2"
    assert cm.find_calls[0]["metadata_element_type"] == "DesignModelBoundary" and cm.find_calls[0]["search_string"] == "*"


def test_the_dmb_list_keeps_a_design_model_boundary_even_if_its_name_looks_like_a_solution_boundary(app_client):
    el = copy.deepcopy(DMB["list"][1])
    el["properties"]["displayName"] = "Solution Boundary (not really)"                       # SYNTHETIC: the exclusion is by type name, never by display name
    sb = copy.deepcopy(DMB["list"][0])
    sb["properties"]["displayName"] = "plain name"
    body = app_client(cm=FakeCM(listing=[sb, el])).get("/api/solution/design-model-boundaries").json()
    assert [b["displayName"] for b in body["boundaries"]] == ["Solution Boundary (not really)"]


def test_the_dmb_list_empty_and_failure(app_client):
    assert app_client(cm=FakeCM(listing=EMPTY["list"])).get("/api/solution/design-model-boundaries").json() == {"boundaries": [], "total": 0}      # SYNTHETIC empty
    assert app_client(cm=FakeCM(listing="nothing")).get("/api/solution/design-model-boundaries").json()["boundaries"] == []
    assert app_client(cm=FakeCM(boom=RuntimeError("down"))).get("/api/solution/design-model-boundaries").status_code >= 400


# ── blueprint and component detail name their boundaries ─────────────────────────────────────────────────────────

def test_a_blueprint_that_is_not_in_a_boundary_has_an_empty_boundaries_list():
    # REAL blueprint: it CONTAINS the boundary (collectionMembers) and is a member of nothing
    d = sah._serialize_blueprint_detail(BLUEPRINT)
    assert d["boundaries"] == []


def test_blueprint_and_component_detail_list_the_boundaries_they_are_members_of():
    # SYNTHETIC memberOfCollections: the real membership relationship pointing at the real inner boundary element
    rel = copy.deepcopy(BOUNDARY["memberOfCollections"][0])
    rel["relatedElement"] = copy.deepcopy(BOUNDARY["collectionMembers"][0]["relatedElement"])
    other = copy.deepcopy(BOUNDARY["memberOfCollections"][0])                                  # a blueprint membership: not a boundary
    for el, ser in ((copy.deepcopy(BLUEPRINT), sah._serialize_blueprint_detail), ({"elementHeader": {"guid": "c1", "type": {"typeName": "SolutionComponent"}}, "properties": {"displayName": "c"}}, sah._serialize_component_detail)):
        el["memberOfCollections"] = [rel, other]
        d = ser(el)
        assert [(b["guid"], b["typeName"], b["displayName"]) for b in d["boundaries"]] == [(INNER, "SolutionBoundary", "probe-boundary-2")]


# ── read-only and async invariants ──────────────────────────────────────────────────────────────────────────────

def test_the_module_never_references_a_create_update_delete_add_member_or_remove_member_method():
    src = Path(sah.__file__).read_text()
    assert not re.search(r"\.\s*_?(?:async_)?(?:create|update|delete|add|remove|link|unlink|set|publish|merge|attach|detach|move|clear|archive|restore)_\w*\(", src)
    assert not re.search(r"(?:add|remove|delete|update|create)_?(?:member|collection|boundary)", src, re.I)


def test_no_route_on_boundaries_takes_anything_but_get():
    for route in sah.router.routes:
        if "boundar" in route.path:
            assert route.methods == {"GET"}, route.path


def test_the_boundary_routes_are_async_and_never_use_a_sync_pyegeria_call():
    for fn in (sah.list_boundaries, sah.get_boundary, sah.list_design_model_boundaries):
        assert inspect.iscoroutinefunction(fn), fn.__name__
        src = inspect.getsource(fn)
        assert "run_until_complete" not in src and "apply_token(" not in src.replace("async_apply_token(", "") and "_get_manager(" not in src
        assert all(m.startswith("_async_") for m in re.findall(r"\b(?:mgr|cm)\.(\w+)\(", src)), fn.__name__
    for fn in (sah._get_manager_async, sah._get_collection_manager_async):
        assert inspect.iscoroutinefunction(fn) and "await async_apply_token(" in inspect.getsource(fn)
