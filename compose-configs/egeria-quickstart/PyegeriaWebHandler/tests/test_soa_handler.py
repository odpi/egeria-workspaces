"""Statements of Applicability (Explorer section): list paging, detail serialization, the controls
table and its summary, and that a failed read / a missing SoA / "no controls" are three different answers.

The element shape is the live getStatementOfApplicabilityByGUID response (Egeria 6.3) that pyegeria's
own micro-test pins (egeria-python tests/micro-tests/test_security_officer_soa.py, SOA_WITH_CONTROLS).
No live server: the SecurityOfficer client is replaced by a fake.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402
from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import soa_handler as sh  # noqa: E402

NO_ELEMENTS = "No elements found"

SOA_PROPS = {
    "class": "StatementOfApplicabilityProperties",
    "qualifiedName": "StatementOfApplicability::Coco Pharmaceuticals ISMS",
    "displayName": "Coco Pharmaceuticals ISMS",
    "versionIdentifier": "1.0",
    "scope": "Coco Pharmaceuticals ISMS",
    "reviewDate": "2026-10-26T00:00:00Z",
    "authors": ["Simon Burr"],
    "contentStatus": "DRAFT",
}


def _rel(rel_type, control_guid, control_props, rel_props):
    return {
        "class": "RelatedMetadataElementSummary",
        "relationshipHeader": {"guid": f"rel-{control_guid}", "type": {"typeName": rel_type}},
        "relationshipProperties": {"class": f"{rel_type}Properties", "typeName": rel_type, **rel_props},
        "relatedElement": {"elementHeader": {"guid": control_guid, "type": {"typeName": "GovernanceControl"}},
                           "properties": control_props},
    }


def _soa(guid="soa-guid", rels=None, name="Coco Pharmaceuticals ISMS"):
    return {
        "elementHeader": {"guid": guid, "type": {"typeName": "StatementOfApplicability",
                                                 "superTypeNames": ["AuthoredReferenceable", "Referenceable"]}},
        "properties": {**SOA_PROPS, "displayName": name},
        "otherRelatedElements": rels or [],
    }


SOA_WITH_CONTROLS = _soa(rels=[
    _rel("ControlApplicability", "c-825", {"displayName": "Secure development", "description": "Control text"},
         {"label": "8.25", "implementationStatus": "PLANNED"}),
    _rel("ControlApplicability", "c-820", {"displayName": "Network security"},
         {"label": "8.20", "description": "Plant network first", "isApplicable": True,
          "implementationStatus": "IMPLEMENTED"}),
    _rel("ControlApplicability", "c-501", {"displayName": "Policies"},
         {"label": "5.1", "isApplicable": False, "justification": "Covered by group policy"}),
    _rel("ControlApplicability", "c-600", {"displayName": "Screening"}, {"label": "6.1"}),
    _rel("SomethingElse", "x-1", {"displayName": "Not a control"}, {}),
])


class _SO:
    """Fake SecurityOfficer: `pages` served by start_from, `detail` returned (or raised) by get-by-guid."""

    def __init__(self, pages=None, detail=None, fail=None):
        self.pages, self.detail, self.fail, self.calls = pages or [], detail, fail, []

    async def _async_find_statements_of_applicability(self, **kw):
        self.calls.append(kw)
        if self.fail:
            raise self.fail
        i = kw["start_from"] // kw["page_size"]
        return self.pages[i] if i < len(self.pages) else NO_ELEMENTS

    async def _async_get_statement_of_applicability_by_guid(self, guid, **kw):
        self.calls.append({"guid": guid, **kw})
        if self.fail:
            raise self.fail
        return self.detail


@pytest.fixture
def client(monkeypatch):
    app = FastAPI()
    app.include_router(sh.router)

    def setup(fake):
        async def factory(url=None, server=None):
            if isinstance(fake, Exception):
                raise fake
            return fake
        monkeypatch.setattr(sh, "_security_officer_async", factory)
        return TestClient(app, raise_server_exceptions=False)
    return setup


# ── list ─────────────────────────────────────────────────────────────────────

def test_list_returns_sorted_flat_items(client):
    fake = _SO(pages=[[_soa("b", name="Zeta SoA"), _soa("a", name="alpha SoA")]])
    r = client(fake).get("/api/statements-of-applicability")
    assert r.status_code == 200
    d = r.json()
    assert [i["guid"] for i in d["items"]] == ["a", "b"]
    assert d["items"][0]["scope"] == "Coco Pharmaceuticals ISMS"
    assert d["items"][0]["contentStatus"] == "DRAFT"
    assert (d["total"], d["capped"]) == (2, False)
    assert fake.calls[0]["graph_query_depth"] == 0          # list reads flat properties only


def test_list_with_none_is_an_empty_200_not_an_error(client):
    r = client(_SO(pages=[])).get("/api/statements-of-applicability")
    assert r.status_code == 200
    assert r.json() == {"items": [], "total": 0, "capped": False}


def test_list_pages_until_an_empty_page_not_a_short_one(client):
    full = [_soa(f"g{i}", name=f"SoA {i:03d}") for i in range(sh._PAGE_SIZE)]
    short = [_soa("last", name="ZZZ last")]
    fake = _SO(pages=[full, short])
    d = client(fake).get("/api/statements-of-applicability").json()
    assert d["total"] == sh._PAGE_SIZE + 1
    # a short page is not proof of the end (Egeria paging contract): the third page is still asked for
    assert [c["start_from"] for c in fake.calls] == [0, sh._PAGE_SIZE, 2 * sh._PAGE_SIZE]


def test_list_says_capped_when_it_stops_at_the_page_limit(client, monkeypatch):
    monkeypatch.setattr(sh, "_MAX_PAGES", 2)
    page = [_soa("x")] * sh._PAGE_SIZE
    d = client(_SO(pages=[page, page, page])).get("/api/statements-of-applicability").json()
    assert d["capped"] is True


def test_list_hides_templates_unless_asked(client):
    tmpl = _soa("t", name="Template SoA")
    tmpl["elementHeader"]["template"] = {"class": "ElementClassification", "classificationName": "Template"}
    c = client(_SO(pages=[[_soa("a"), tmpl]]))
    assert [i["guid"] for i in c.get("/api/statements-of-applicability").json()["items"]] == ["a"]
    with_t = c.get("/api/statements-of-applicability", params={"include_templates": "true"}).json()
    assert {i["guid"] for i in with_t["items"]} == {"a", "t"}


def test_list_failure_is_an_http_error_not_an_empty_list(client):
    r = client(_SO(fail=RuntimeError("boom"))).get("/api/statements-of-applicability")
    assert r.status_code == 500


def test_platform_refusal_passes_through_with_its_status(client):
    r = client(HTTPException(status_code=401, detail="not for that platform")).get(
        "/api/statements-of-applicability")
    assert r.status_code == 401


def test_no_credential_query_params_are_declared():
    for route in sh.router.routes:
        names = {p.name for p in route.dependant.query_params}
        assert not names & {"user_id", "user_pwd"}, route.path


# ── detail ───────────────────────────────────────────────────────────────────

def test_detail_flattens_properties_for_generic_table(client):
    d = client(_SO(detail=SOA_WITH_CONTROLS)).get("/api/statements-of-applicability/soa-guid").json()
    assert d["guid"] == "soa-guid"
    assert d["typeName"] == "StatementOfApplicability"
    assert d["scope"] == "Coco Pharmaceuticals ISMS"
    assert d["reviewDate"] == "2026-10-26T00:00:00Z"
    assert d["versionIdentifier"] == "1.0"
    assert d["authors"] == ["Simon Burr"]
    assert "class" not in d


def test_detail_controls_one_row_per_control_in_label_order(client):
    d = client(_SO(detail=SOA_WITH_CONTROLS)).get("/api/statements-of-applicability/soa-guid").json()
    assert d["controlsRead"] is True
    rows = d["controls"]
    assert [r["label"] for r in rows] == ["5.1", "6.1", "8.20", "8.25"]
    by = {r["label"]: r for r in rows}
    # relationship description is the assessment's notes; the control's own description stays separate
    assert by["8.20"]["notes"] == "Plant network first"
    assert by["8.25"]["controlDescription"] == "Control text" and by["8.25"]["notes"] == ""
    # unset isApplicable stays unset (UI says "applicable (default)"), stored values are kept
    assert by["6.1"]["isApplicable"] is None
    assert by["5.1"]["isApplicable"] is False
    assert by["5.1"]["justification"] == "Covered by group policy"
    assert by["8.20"]["guid"] == "c-820"


def test_label_sort_is_numeric():
    assert sorted(["8.25", "10.1", "8.3", "", "5.1"], key=sh._label_sort_key) == ["5.1", "8.3", "8.25", "10.1", ""]


def test_detail_summary_counts_applicable_controls_and_keeps_unset_apart(client):
    s = client(_SO(detail=SOA_WITH_CONTROLS)).get("/api/statements-of-applicability/soa-guid").json()["summary"]
    assert (s["total"], s["applicable"], s["notApplicable"]) == (4, 3, 1)
    assert s["byStatus"]["PLANNED"] == 1 and s["byStatus"]["IMPLEMENTED"] == 1
    assert s["byStatus"]["NOT_STARTED"] == 0      # 6.1 has no status: counted as unset, not NOT_STARTED
    assert s["statusUnset"] == 1
    assert set(sh._implementation_statuses()) <= set(s["byStatus"])   # every status present, zeros real


def test_detail_relationship_cards_exclude_the_control_links(client):
    d = client(_SO(detail=SOA_WITH_CONTROLS)).get("/api/statements-of-applicability/soa-guid").json()
    rel_guids = [i["guid"] for items in d["relationships"].values() for i in items]
    assert rel_guids == ["x-1"]


def test_control_link_listed_under_two_keys_is_one_row(client):
    soa = _soa(rels=[_rel("ControlApplicability", "c-1", {"displayName": "A"}, {"label": "1"})])
    soa["relationships"] = list(soa["otherRelatedElements"])
    d = client(_SO(detail=soa)).get("/api/statements-of-applicability/soa-guid").json()
    assert len(d["controls"]) == 1


def test_detail_with_no_controls_is_an_empty_read_table(client):
    d = client(_SO(detail=_soa())).get("/api/statements-of-applicability/soa-guid").json()
    assert d["controls"] == [] and d["controlsRead"] is True
    assert d["summary"]["total"] == 0


def test_detail_not_found_is_404(client):
    r = client(_SO(detail=NO_ELEMENTS)).get("/api/statements-of-applicability/missing-guid")
    assert r.status_code == 404


def test_detail_failure_is_an_http_error(client):
    r = client(_SO(fail=RuntimeError("boom"))).get("/api/statements-of-applicability/soa-guid")
    assert r.status_code == 500


def test_detail_asks_for_full_mermaid(client):
    fake = _SO(detail=SOA_WITH_CONTROLS)
    client(fake).get("/api/statements-of-applicability/soa-guid")
    assert fake.calls[0]["max_mermaid_node_count"] == 250
