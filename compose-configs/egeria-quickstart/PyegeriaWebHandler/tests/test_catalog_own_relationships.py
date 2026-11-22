"""The Catalog's asset detail lists only the asset's OWN relationships.

get_asset_graph_by_guid (depth 5) returns the whole reachable subgraph in one flat `relationships`
list; each entry's startingElementGUID says which element it was recorded from. Customer API on laz
(fixture fetched read-only as erinoverview, 2026-11-13) showed SemanticAssignment ->
UniqueCustomerIdentifier twice: the term is assigned to the request and the response customerNo
APIParameters, not to the API. Fourteen such nested-element relationships were shown as the API's own.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import tech_catalog_handler as t  # noqa: E402

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "customer_api_asset_graph_laz_2026_11_13.json"
API_GUID = "5d6ec7aa-9b13-4286-ad00-af82709a259b"
REQUEST_CUSTOMER_NO = "1ca8155c-fc49-4d43-b54a-7ffc945ed796"
RESPONSE_CUSTOMER_NO = "a7b6360d-3c76-4ffc-8fbb-4d57b7ddbb8f"


def _graph():
    return json.loads(FIXTURE.read_text())


def _shown(el):
    return [(r["relationshipType"], r["relatedElement"].get("displayName")) for r in t._extract_relationships(el)]


def test_the_fixture_is_the_real_shape():
    el = _graph()
    assert el["elementHeader"]["guid"] == API_GUID
    flat = el["relationships"]
    sem = [r for r in flat if r["relationshipHeader"]["type"]["typeName"] == "SemanticAssignment"]
    assert len(sem) == 2 and len({r["relationshipHeader"]["guid"] for r in sem}) == 2
    assert {r["startingElementGUID"] for r in sem} == {REQUEST_CUSTOMER_NO, RESPONSE_CUSTOMER_NO}
    assert sum(1 for r in flat if r.get("startingElementGUID") not in (None, API_GUID)) == 14


def test_only_the_apis_own_relationships_are_shown():
    assert sorted(_shown(_graph())) == [("DataFlow", "RETAILSCHEMA"), ("Schema", "Customer API API Schema Type")]


def test_the_glossary_term_is_not_shown_as_the_apis_meaning():
    assert not any(rt == "SemanticAssignment" for rt, _ in _shown(_graph()))


def test_a_relationship_recorded_from_the_asset_itself_is_kept():
    el = _graph()
    sem = next(r for r in el["relationships"] if r["relationshipHeader"]["type"]["typeName"] == "SemanticAssignment")
    el["relationships"].append({**sem, "startingElementGUID": API_GUID,
                                "relationshipHeader": {**sem["relationshipHeader"], "guid": "own-semantic-assignment"}})
    assert _shown(el).count(("SemanticAssignment", "UniqueCustomerIdentifier")) == 1


def test_an_entry_without_a_starting_element_is_kept():
    """Other fetch paths (endpoints, capabilities, fallbacks) return flat lists without the field."""
    el = _graph()
    for r in el["relationships"]:
        r.pop("startingElementGUID", None)
    assert ("SemanticAssignment", "UniqueCustomerIdentifier") in _shown(el)


def test_the_flat_list_is_left_whole_for_the_schema_tree():
    """_serialize_schema reads the nested entries straight from el["relationships"]: the detail
    filter must not remove them from the element."""
    el = _graph()
    before = json.dumps(el["relationships"], sort_keys=True)
    t._serialize(el, include_relationships=True)
    assert json.dumps(el["relationships"], sort_keys=True) == before and len(el["relationships"]) == 15


def test_the_detail_payload_uses_the_filtered_list():
    out = t._serialize(_graph(), include_relationships=True)
    assert sorted(r["relationshipType"] for r in out["relationships"]) == ["DataFlow", "Schema"]
