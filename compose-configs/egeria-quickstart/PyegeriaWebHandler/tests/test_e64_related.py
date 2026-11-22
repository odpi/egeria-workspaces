"""The Egeria 6.4 rows on any element's existing card (e64_handler: /api/e64/elements/{guid}/related).

No live server: ClassificationExplorer is replaced by a fake (tests/e64_fixtures.py). The read is limited to
the 6.4 relationship types, so the absence rule's "asked for" is exactly the lists those types fill.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pytest  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import e64_handler as h  # noqa: E402
import egeria_6_4_support as e64  # noqa: E402
from e64_fixtures import ABOUT_6_3, ABOUT_6_4, FakeExplorer, assessment, client_error, positioned, rel  # noqa: E402


@pytest.fixture
def client(monkeypatch):
    app = FastAPI()
    app.include_router(h.router)
    e64.clear_cache()

    def setup(fake):
        async def factory(url=None, server=None):
            return fake
        monkeypatch.setattr(h, "_explorer_async", factory)
        return TestClient(app)
    yield setup
    e64.clear_cache()


class Recorder(FakeExplorer):
    async def _async_get_element_by_guid(self, guid, element_type_name=None, graph_query_depth=3, **kw):
        self.kw = kw
        return await super()._async_get_element_by_guid(guid, element_type_name, graph_query_depth, **kw)


def element(guid="t-1", type_name="GlossaryTerm", supers=("Referenceable",), header=None, **lists):
    return {"elementHeader": {"guid": guid, "type": {"typeName": type_name, "superTypeNames": list(supers)}, **(header or {})},
            "properties": {"displayName": "Lineage"}, **lists}


def _lists(body):
    return {l["key"]: l for s in body["sections"] for l in s["lists"]}


def test_before_6_4_one_needs_6_4_answer_and_nothing_sent(client):
    fake = FakeExplorer(about=ABOUT_6_3, elements={"t-1": element()})
    r = client(fake).get("/api/e64/elements/t-1/related")
    assert r.status_code == 200 and r.json()["needs64"] is True and "needs Egeria 6.4" in r.json()["words"]
    assert fake.calls == []


def test_unknown_version_and_bare_404_is_needs_6_4(client):
    r = client(FakeExplorer(about=RuntimeError("x"), fail=client_error(404))).get("/api/e64/elements/t-1/related")
    assert r.json()["needs64"] is True


def test_the_read_is_limited_to_the_6_4_relationship_types(client):
    fake = Recorder(about=ABOUT_6_4, elements={"t-1": element()})
    client(fake).get("/api/e64/elements/t-1/related")
    assert sorted(fake.kw["include_only_relationships"]) == sorted(
        {"Outcome", "Assessment", "ProjectTarget", "ProcessingVariable", "SupportedVariableType", "DataValueSource"})
    assert fake.calls[-1][3] == 1


def test_any_element_gets_decisions_projects_and_variables_but_not_type_specific_lists(client):
    body = client(FakeExplorer(about=ABOUT_6_4, elements={"t-1": element()})).get("/api/e64/elements/t-1/related").json()
    assert set(_lists(body)) == {"associatedDecisions", "assessmentDecisions", "workedOnByProjects",
                                 "processingVariables", "processVariableTypes"}
    assert all(l["st"] == {"state": "none"} for l in _lists(body).values())
    assert body["branch"] is None and body["carries"] is True


def test_type_specific_lists_on_project_asset_and_schema_type(client):
    els = {"p": element("p", "Project"), "a": element("a", "CSVFile", ("DataFile", "Asset", "Referenceable")),
           "s": element("s", "PrimitiveSchemaType", ("SchemaType", "Referenceable"))}
    c = client(FakeExplorer(about=ABOUT_6_4, elements=els))
    assert "projectTargets" in _lists(c.get("/api/e64/elements/p/related").json())
    assert "providesDataValues" in _lists(c.get("/api/e64/elements/a/related").json())
    assert "processVariableTypeUses" in _lists(c.get("/api/e64/elements/s/related").json())


def test_rows_with_properties_two_assessments_and_positions(client):
    el = element(
        associatedDecisions=[rel("Outcome", "o-1", "dec-1", el_type="Decision", el_props={"displayName": "Adopt"},
                                 rel_props={"label": "Rollout", "importance": "High", "disposition": "Started"})],
        assessmentDecisions=[assessment("a-1", "dec-1", "Adopt", "First", "2026-02-01T00:00:00Z"),
                             assessment("a-2", "dec-1", "Adopt", "Again", "2026-05-01T00:00:00Z")],
        processingVariables=[positioned("ProcessingVariable", "pv-0", "dv-0", "Unset", 0),
                             positioned("ProcessingVariable", "pv-1", "dv-1", "First", 1)],
        processVariableTypes=[positioned("SupportedVariableType", "sv-1", "st-1", "Int", 1, el_type="PrimitiveSchemaType",
                                         minCardinality=1, maxCardinality=3)],
        workedOnByProjects=[rel("ProjectTarget", "pt-1", "proj-1", el_type="Project", el_props={"displayName": "Rollout"})],
    )
    lists = _lists(client(FakeExplorer(about=ABOUT_6_4, elements={"t-1": el})).get("/api/e64/elements/t-1/related").json())
    assert lists["associatedDecisions"]["rows"][0]["disposition"] == "Started"
    assert [r["relationshipGuid"] for r in lists["assessmentDecisions"]["rows"]] == ["a-1", "a-2"]
    assert [(r["relationshipGuid"], r["position"]) for r in lists["processingVariables"]["rows"]] == [("pv-1", 1), ("pv-0", None)]
    sv = lists["processVariableTypes"]["rows"][0]
    assert (sv["position"], sv["minCardinality"], sv["maxCardinality"]) == (1, 1, 3)
    assert lists["workedOnByProjects"]["st"] == {"state": "read"}


def test_branch_badge_data_and_unknown_version_lists_are_not_known(client):
    branch = {"otherClassifications": [{"classificationName": "Branch", "classificationProperties": {
        "class": "BranchProperties", "displayName": "main", "purpose": "default branch", "url": "https://x/main"}}]}
    el = element(header=branch)
    body = client(FakeExplorer(about=RuntimeError("x"), elements={"t-1": el})).get("/api/e64/elements/t-1/related").json()
    assert body["branch"]["displayName"] == "main" and body["carries"] is None
    assert all(l["st"] == {"state": "not-known"} for l in _lists(body).values())


def test_requested_for_maps_relationship_types_to_lists():
    req = h._requested_for(["Outcome"])
    assert {"associatedDecisions", "decisionOutcomes"} <= req and "inputsToDecision" not in req


def test_generic_relationships_leave_the_6_4_lists_to_the_panel():
    # read-back S2: a card that renders E64RelatedPanel (here the Statement of Applicability card) does not
    # list the 14 Egeria 6.4 keys again in its generic Relationships block; other keys are untouched.
    import soa_handler
    from common_serialize import _generic_relationships
    soa = element("soa-1", "StatementOfApplicability", ("AuthoredReferenceable", "Referenceable"),
                  associatedDecisions=[rel("Outcome", "o-1", "dec-1", el_type="Decision", el_props={"displayName": "Adopt"})],
                  workedOnByProjects=[rel("ProjectTarget", "pt-1", "proj-1", el_type="Project")],
                  knownLocations=[rel("KnownLocation", "kl-1", "loc-1", el_type="Location")])
    rels = soa_handler._serialize_detail(soa)["relationships"]
    assert "knownLocations" in rels
    assert not set(rels) & set(e64.E64_LISTS)
    assert not set(_generic_relationships(soa)) & set(e64.E64_LISTS)


def test_a_404_on_a_6_4_platform_is_an_error_not_needs_6_4(client):
    r = client(FakeExplorer(about=ABOUT_6_4, fail=client_error(404))).get("/api/e64/elements/t-1/related")
    assert r.status_code >= 400 and "needs64" not in r.text
