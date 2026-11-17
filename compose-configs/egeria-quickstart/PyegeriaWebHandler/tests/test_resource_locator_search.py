# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Resource Locator search: several kinds at once, and the parts of resources: columns and other schema
attributes, and data fields. Each part is a row of its own that says what holds it,
and still rolls up to the resource that holds it.

Quickstart only: the freshstart copy is stale (BACKLOG "Mirror egeria-freshstart"),
so these helpers are pinned on the quickstart handler. Functions are extracted from the
handler with ast and run without pyegeria or FastAPI, as in test_resource_browser.py.
"""
import ast
import asyncio
import re
from pathlib import Path
from typing import Optional

import pytest

_HANDLER = Path(__file__).resolve().parent.parent / "resource_browser_handler.py"
_FUNCS = {"_type_names", "_display_name", "_related", "_related_recs", "_classifications", "_data_scope",
          "_owner", "_has_scope", "_kind_of", "_is_resource", "_looks_automated", "_is_repo", "_row", "_elements",
          "_is_schema_attribute", "_is_schema_element", "_container_of",
          "_part_kind", "_part_row", "_part_types", "_kind_types", "_parse_kinds", "_may_have_more", "_search_parts", "_get_depth1"}
_CONSTS = {"_SKIP_CLASSIFICATIONS", "_RESOURCE_TYPES", "_NOT_RESOURCES", "_KINDS", "_PART_KINDS", "_BADGES",
           "_REPO_QN_PREFIX", "_PART_OF_KEYS", "_COUNTED_TYPES", "_PART_LOOKUP_CAP", "_SEARCH_PAGE",
           "_LOOKUP_CONCURRENCY", "_KIND_IDS", "_STRUCTURE_INCLUDE"}


@pytest.fixture(scope="module")
def rb():
    tree = ast.parse(_HANDLER.read_text(encoding="utf-8"))
    nodes = [n for n in tree.body if (isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name in _FUNCS)
             or (isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in _CONSTS)]
    assert {n.name for n in nodes if not isinstance(n, ast.Assign)} == _FUNCS
    ns = {"Optional": Optional, "re": re, "asyncio": asyncio}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(_HANDLER), "exec"), ns)
    return ns


_ATTR = ["SchemaAttribute", "SchemaElement", "Referenceable"]


def _el(guid, type_name, supers, name, anchor=None, **rels):
    hdr = {"guid": guid, "type": {"typeName": type_name, "superTypeNames": supers}}
    if anchor:
        hdr["anchor"] = {"class": "ElementClassification", "classificationName": "Anchors",
                         "classificationProperties": {"anchorGUID": anchor[0], "anchorTypeName": anchor[1]}}
    return {"elementHeader": hdr, "properties": {"displayName": name, "qualifiedName": f"qn::{name}"}, **rels}


def _item(el, rel):
    return {"relatedElement": el, "relationshipHeader": {"type": {"typeName": rel}}, "relatedElementAtEnd1": True}


def test_part_kinds_are_columns_attributes_and_fields_not_tables(rb):
    assert rb["_part_kind"]("RelationalColumn", _ATTR) == "attribute"
    assert rb["_part_kind"]("EventSchemaAttribute", _ATTR) == "attribute"
    assert rb["_part_kind"]("APIParameter", _ATTR) == "attribute"
    assert rb["_part_kind"]("DataField", ["Referenceable"]) == "field"
    # A table is a schema attribute in Egeria, but it is a resource with a kind of its own.
    assert rb["_part_kind"]("RelationalTable", _ATTR) is None
    assert rb["_part_kind"]("DeployedDatabaseSchema", ["DataSet"]) is None
    # _kind_of never returns a part kind, so Browse, Home and the structure card are unchanged.
    assert rb["_kind_of"]("RelationalColumn", _ATTR) == "other"
    assert {"attribute", "field"} <= set(rb["_KIND_IDS"])


def test_part_types_per_kind(rb):
    assert rb["_part_types"](None) == ["SchemaAttribute", "DataField"]
    assert rb["_part_types"](["table"]) == ["SchemaAttribute"]   # columns roll up to their table
    assert rb["_part_types"](["attribute"]) == ["SchemaAttribute"]
    assert rb["_part_types"](["field"]) == ["DataField"]
    assert rb["_part_types"](["report"]) == []
    assert rb["_part_types"](["table", "attribute", "field"]) == ["SchemaAttribute", "DataField"]


def test_several_kinds_parse_in_order_without_repeats(rb):
    assert rb["_parse_kinds"](None) is None and rb["_parse_kinds"]("") is None and rb["_parse_kinds"](" , ") is None
    assert rb["_parse_kinds"]("schema,table, schema") == ["schema", "table"]
    with pytest.raises(ValueError, match="nonsense"):
        rb["_parse_kinds"]("table,nonsense")


def test_text_search_asks_for_the_union_of_the_kinds_types(rb):
    assert rb["_kind_types"](None) == rb["_RESOURCE_TYPES"]
    assert rb["_kind_types"](["schema", "table"]) == ["RelationalTable", "VirtualRelationalTable", "DeployedDatabaseSchema"]
    # "other" is whatever is left over, so it needs every resource type, then the kind filter.
    assert rb["_kind_types"](["table", "other"]) == rb["_RESOURCE_TYPES"]
    # Code repositories are read from their own cache and parts from the parts search: no text search.
    assert rb["_kind_types"](["repo"]) == [] and rb["_kind_types"](["attribute", "field"]) == []


def test_part_row_says_what_holds_it_or_that_nothing_does(rb):
    col = _el("c1", "RelationalColumn", _ATTR, "customer_id")
    row = rb["_part_row"](col, {"guid": "t1", "displayName": "customers", "typeName": "RelationalTable"})
    assert (row["kind"], row["displayName"], row["partOf"]) == (
        "attribute", "customer_id", {"guid": "t1", "displayName": "customers", "typeName": "RelationalTable"})
    assert rb["_part_row"](col, None)["partOf"] is None
    assert rb["_part_row"](_el("t1", "RelationalTable", _ATTR, "customers"), None) is None


def test_data_field_sits_in_its_data_structure(rb):
    field = _el("f1", "DataField", ["Referenceable"], "customer_identifier", anchor=("hub", "DataSharingHub"),
                partOfDataStructures=[_item(_el("ds", "DataStructure", ["Referenceable"], "invoice"), "MemberDataField")])
    up = rb["_container_of"](field)
    assert (up["guid"], up["displayName"]) == ("ds", "invoice")


def test_empty_page_ends_paging_but_a_short_page_does_not(rb):
    # Egeria's paging contract: a short page is not the last page; only null means no more.
    assert rb["_may_have_more"]([{"elementHeader": {"guid": "x"}}]) is True
    assert rb["_may_have_more"]([]) is False


class _FakeClient:
    """find returns the page; get_element_by_guid returns depth-1 or depth-0 reads by guid."""
    def __init__(self, page, depth1, depth0):
        self.page, self.depth1, self.depth0, self.reads = page, depth1, depth0, []

    async def _async_find_elements_by_property_value(self, **kw):
        self.find_kwargs = kw
        return self.page

    async def _async_get_element_by_guid(self, guid, graph_query_depth=0, **kw):
        self.reads.append((guid, graph_query_depth))
        return (self.depth1 if graph_query_depth else self.depth0).get(guid)


def test_search_parts_lists_parts_and_rolls_up_to_resources(rb):
    table = _el("t1", "RelationalTable", _ATTR, "customers")
    topic = _el("tp", "Topic", ["DataFeed", "DataAsset", "Asset"], "CustomerChangeTopic")
    col = _el("c1", "RelationalColumn", _ATTR, "customer_id")
    api_param = _el("p1", "APIParameter", _ATTR, "customerNo", anchor=("api", "DeployedAPI"))
    field = _el("f1", "DataField", ["Referenceable"], "customer_identifier")
    page = [col, api_param, field, table]   # the SchemaAttribute find returns tables too
    depth1 = {
        "c1": dict(col, parentSchemaElements=[_item(table, "NestedSchemaAttribute")]),
        "p1": dict(api_param, parentSchemaElements=[_item(_el("pl", "APIParameterList", ["SchemaType", "SchemaElement"],
                                                              "Request"), "AttributeForSchema")]),
        "f1": field,
    }
    depth0 = {"t1": table, "api": _el("api", "DeployedAPI", ["Asset"], "Customer API"), "tp": topic}
    client = _FakeClient(page, depth1, depth0)
    out = asyncio.run(rb["_search_parts"](client, "customer", 0, ["SchemaAttribute", "DataField"]))

    assert client.find_kwargs["metadata_element_subtypes"] == ["SchemaAttribute", "DataField"]
    by = {r["guid"]: r for r in out["rows"]}
    assert set(by) == {"c1", "p1", "f1"}                    # the table is not a part row
    assert by["c1"]["partOf"]["displayName"] == "customers"
    # An API parameter sits in a parameter list, which is no container: it belongs to its anchor,
    # whose name is read so the row can say it.
    assert (by["p1"]["partOf"]["guid"], by["p1"]["partOf"]["displayName"]) == ("api", "Customer API")
    assert by["f1"]["partOf"] is None and by["f1"]["partOfKnown"] is True
    rolled = {row["guid"]: names for row, names in out["rollups"]}
    assert rolled == {"t1": ["customer_id"], "api": ["customerNo"]}
    assert (out["found"], out["lookedUp"]) == (4, 3)


def test_search_parts_beyond_the_lookup_cap_say_so(rb):
    cols = [_el(f"c{i}", "RelationalColumn", _ATTR, f"col{i}") for i in range(rb["_PART_LOOKUP_CAP"] + 2)]
    client = _FakeClient(cols, {}, {})
    out = asyncio.run(rb["_search_parts"](client, "col", 0, ["SchemaAttribute"]))
    assert len(out["rows"]) == len(cols) and out["lookedUp"] == rb["_PART_LOOKUP_CAP"]
    assert [r["partOfKnown"] for r in out["rows"][-2:]] == [False, False]
    assert len([g for g, d in client.reads if d]) == rb["_PART_LOOKUP_CAP"]
