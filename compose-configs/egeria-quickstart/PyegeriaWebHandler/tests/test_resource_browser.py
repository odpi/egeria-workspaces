# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""The Resource Browser's pure helpers: flavour, lineage direction, survey statistics,
and (phase 2) result rows, resource kinds, search relevance and the flavour index.

Spec §3 asks for one flavour function with one test per flavour and one for the
precedence (hub > product > known). The other tests pin the honesty rules the page
depends on: lineage direction comes from which end the related element sits at, the
newest survey wins per subject, and a table only gets statistics when its catalog,
schema and table names are all known.

The functions are extracted from each handler file (quickstart and freshstart carry
identical copies) and run without importing pyegeria or FastAPI.
"""
import ast
from pathlib import Path
from typing import Optional

import pytest

_HERE = Path(__file__).resolve().parent
# Inside the container /app/tests has no freshstart sibling; that copy is then skipped.
_COMPOSE = _HERE.parents[2] if len(_HERE.parents) > 2 else _HERE
_HANDLERS = {
    "quickstart": _HERE.parent / "resource_browser_handler.py",
    "freshstart": _COMPOSE / "egeria-freshstart" / "PyegeriaWebHandler" / "resource_browser_handler.py",
}
_NEEDED = {"_type_names", "_display_name", "_related", "_classifications", "_data_scope", "_flavour",
           "_lineage", "_stats_name_of", "_latest_by_subject", "_jdbc_table_name",
           # phase 2
           "_owner", "_kind_of", "_is_resource", "_looks_automated", "_row", "_rows", "_relevance",
           "_text_reason", "_merge", "_flavour_index", "_recent_rows"}
_CONSTS = {"_SKIP_CLASSIFICATIONS", "_LINEAGE_RELATIONSHIPS", "_TABLE_STATS_QN", "_COLUMN_STATS_QN",
           "_RESOURCE_TYPES", "_NOT_RESOURCES", "_KINDS", "_BADGES"}


def _load(path: Path):
    if not path.exists():
        pytest.skip(f"{path} not present in this checkout")
    tree = ast.parse(path.read_text(encoding="utf-8"))
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in _NEEDED]
    assert {n.name for n in funcs} == _NEEDED
    consts = [n for n in tree.body if isinstance(n, ast.Assign)
              and isinstance(n.targets[0], ast.Name) and n.targets[0].id in _CONSTS]
    ns = {"Optional": Optional}
    exec(compile(ast.Module(body=consts + funcs, type_ignores=[]), str(path), "exec"), ns)
    return ns


@pytest.fixture(params=sorted(_HANDLERS), ids=sorted(_HANDLERS))
def rb(request):
    return _load(_HANDLERS[request.param])


def _coll(type_name, name="c", supers=None):
    return {"guid": name + "-guid", "displayName": name, "typeName": type_name, "superTypeNames": supers or ["Collection"]}


# ── Flavour (spec §3) ─────────────────────────────────────────────────────────

def test_flavour_known_when_nothing_else_applies(rb):
    f = rb["_flavour"]("RelationalTable", ["SchemaAttribute"], [_coll("Folder")])
    assert f["flavour"] == "known" and f["all"] == ["known"]


def test_flavour_product_by_membership(rb):
    f = rb["_flavour"]("ReferenceCodeTable", ["Asset"], [_coll("DigitalProduct", "p")])
    assert f["flavour"] == "product"
    assert f["via"]["product"] == [{"guid": "p-guid", "displayName": "p"}]


def test_flavour_product_by_being_one(rb):
    assert rb["_flavour"]("DigitalProduct", ["Collection"], [])["flavour"] == "product"


def test_flavour_product_by_subtype(rb):
    sub = _coll("SpecialProduct", "s", supers=["DigitalProduct", "Collection"])
    assert rb["_flavour"]("DataFile", ["Asset"], [sub])["flavour"] == "product"


def test_flavour_hub_by_membership(rb):
    f = rb["_flavour"]("DataFile", ["Asset"], [_coll("DataSharingHub", "h")])
    assert f["flavour"] == "hub"
    assert f["via"]["hub"] == [{"guid": "h-guid", "displayName": "h"}]


def test_flavour_precedence_hub_over_product_over_known(rb):
    f = rb["_flavour"]("DataFile", ["Asset"], [_coll("DigitalProduct", "p"), _coll("DataSharingHub", "h")])
    assert f["flavour"] == "hub"
    assert f["all"] == ["hub", "product", "known"]


# ── Classifications and data scope ───────────────────────────────────────────

def _cls(name, props=None):
    return {"class": "ElementClassification", "classificationName": name,
            "classificationProperties": dict({"class": name + "Properties"}, **(props or {}))}


def test_classifications_skip_infrastructure_and_read_lists(rb):
    hdr = {"anchor": _cls("Anchors", {"anchorGUID": "x"}),
           "dataScope": _cls("DataScope", {"minLatitude": 0, "dataCollectionStartTime": "2021-01-01"}),
           "otherClassifications": [_cls("Ownership", {"owner": "Jules"})],
           "guid": "g"}
    names = [c["name"] for c in rb["_classifications"](hdr)]
    assert names == ["DataScope", "Ownership"]


def test_data_scope_absent_is_none_not_empty(rb):
    assert rb["_data_scope"]([]) is None
    scope = rb["_data_scope"]([{"name": "DataScope", "properties": {"minLatitude": 0}}])
    assert scope == {"minLatitude": 0}


# ── Lineage direction ────────────────────────────────────────────────────────

def _rel(rel_type, at_end1, guid):
    return {"guid": guid, "typeName": "Process", "displayName": guid, "relationshipType": rel_type, "atEnd1": at_end1}


def test_lineage_end1_is_upstream_end2_downstream(rb):
    lin = rb["_lineage"]([_rel("DataFlow", True, "src"), _rel("DataFlow", False, "dst"),
                          _rel("DataSetContent", True, "schema")])
    assert [r["guid"] for r in lin["upstream"]] == ["src"]
    assert [r["guid"] for r in lin["downstream"]] == ["dst"]


def test_lineage_none_recorded_is_two_empty_lists(rb):
    assert rb["_lineage"]([]) == {"upstream": [], "downstream": []}


def test_related_reads_edge_type_and_end(rb):
    item = {"relationshipHeader": {"type": {"typeName": "DataFlow"}}, "relatedElementAtEnd1": True,
            "relationshipProperties": {"class": "x", "label": "feeds"},
            "relatedElement": {"elementHeader": {"guid": "g", "type": {"typeName": "Process"}},
                               "properties": {"displayName": "P"}}}
    r = rb["_related"](item)
    assert (r["relationshipType"], r["atEnd1"], r["displayName"]) == ("DataFlow", True, "P")
    assert r["relationshipProperties"] == {"label": "feeds"}
    assert rb["_related"]({"relatedElement": {"elementHeader": {}}}) is None


# ── Survey statistics ────────────────────────────────────────────────────────

def _ann(qn, when, values=None):
    return {"elementHeader": {"guid": qn[-4:], "versions": {"createTime": when}},
            "properties": {"qualifiedName": qn, "annotationType": "t", "resourceProperties": values or {}}}


def test_latest_survey_wins_per_subject(rb):
    p = rb["_COLUMN_STATS_QN"]
    anns = [_ann(p + "db.s.t.a::1111", "2026-10-01T00:00:00", {"v": "old"}),
            _ann(p + "db.s.t.a::2222", "2026-10-12T00:00:00", {"v": "new"}),
            _ann(p + "db.s.t.b::3333", "2026-10-05T00:00:00", {"v": "b"})]
    latest = rb["_latest_by_subject"](anns, p)
    assert latest["db.s.t.a"]["values"] == {"v": "new"}
    assert latest["db.s.t.a"]["measuredAt"] == "2026-10-12T00:00:00"
    assert set(latest) == {"db.s.t.a", "db.s.t.b"}


def test_stats_name_strips_prefix_and_uuid(rb):
    p = rb["_TABLE_STATS_QN"]
    assert rb["_stats_name_of"](p + "coco.sales.orders::abc-123", p) == "coco.sales.orders"


def test_jdbc_table_name_needs_all_three_parts(rb):
    ap = {"jdbc.catalog": "coco", "jdbc.schema": "sales", "jdbc.table": "orders"}
    assert rb["_jdbc_table_name"]({"additionalProperties": ap}) == "coco.sales.orders"
    assert rb["_jdbc_table_name"]({"additionalProperties": {"jdbc.catalog": "coco", "jdbc.table": "orders"}}) is None
    assert rb["_jdbc_table_name"]({}) is None


# ── Phase 2: rows, kinds, relevance, flavour index ───────────────────────────

def _el(type_name, supers, name="x", guid="g1", desc="", qn="", cls=None, updated_by="erinoverview", when="2026-10-01"):
    hdr = {"guid": guid, "type": {"typeName": type_name, "superTypeNames": supers},
           "versions": {"updatedBy": updated_by, "updateTime": when}}
    hdr.update(cls or {})
    return {"elementHeader": hdr, "properties": {"displayName": name, "description": desc, "qualifiedName": qn}}


_TABLE = ["SchemaAttribute", "SchemaElement", "Referenceable"]
_SURVEY = ["Report", "DataSet", "DataAsset", "Asset", "Referenceable"]


def test_kind_follows_type_and_supertypes(rb):
    assert rb["_kind_of"]("RelationalTable", _TABLE) == "table"
    assert rb["_kind_of"]("ReferenceCodeTable", ["TabularDataSet", "DataSet", "DataAsset"]) == "dataset"
    assert rb["_kind_of"]("RelationalDatabase", ["Database", "DataStore", "DataAsset"]) == "database"
    assert rb["_kind_of"]("Report", _SURVEY) == "report"
    assert rb["_kind_of"]("Something", ["DataAsset"]) == "other"


def test_operational_records_and_templates_are_not_rows(rb):
    assert rb["_is_resource"]("RelationalTable", _TABLE)
    assert not rb["_is_resource"]("SurveyReport", _SURVEY)
    assert not rb["_is_resource"]("Notification", ["Action", "Asset"])
    assert rb["_row"](_el("SurveyReport", _SURVEY)) is None
    tmpl = {"template": {"class": "ElementClassification", "classificationName": "Template", "classificationProperties": {}}}
    assert rb["_row"](_el("RelationalTable", _TABLE, cls=tmpl)) is None
    rows, skipped = rb["_rows"]([_el("RelationalTable", _TABLE), _el("Notification", ["Asset"], guid="n")])
    assert len(rows) == 1 and skipped == 1


def test_row_reads_owner_badges_scope_and_automation(rb):
    cls = {"ownership": _cls("Ownership", {"owner": "Jules"}),
           "otherClassifications": [_cls("Confidentiality", {"levelIdentifier": 2}), _cls("Anchors")],
           "dataScope": _cls("DataScope", {"scopeStartTime": "2020"})}
    r = rb["_row"](_el("RelationalTable", _TABLE, cls=cls, updated_by="dbcatnpa"))
    assert (r["owner"], r["badges"], r["automated"], r["kind"]) == ("Jules", ["Confidentiality"], True, "table")
    assert r["dataScope"] == {"scopeStartTime": "2020"}
    plain = rb["_row"](_el("RelationalTable", _TABLE))
    assert plain["owner"] is None and plain["dataScope"] is None and plain["automated"] is False


def test_relevance_puts_name_matches_first(rb):
    rows = [rb["_row"](_el("RelationalTable", _TABLE, name=n, guid=n, desc=d, qn=q))
            for n, d, q in [("currency", "", "db.sales.currency"), ("salesperson", "", ""), ("sales", "", ""),
                            ("orders", "sales orders", ""), ("vsales", "", "")]]
    order = [r["displayName"] for r in sorted(rows, key=lambda r: rb["_relevance"](r, "Sales"))]
    assert order == ["sales", "salesperson", "vsales", "currency", "orders"]
    assert rb["_text_reason"](rows[0], "sales") == "qualified name"
    assert rb["_text_reason"](rows[3], "sales") == "description"


def test_merge_keeps_one_row_and_every_reason(rb):
    found = {}
    r = rb["_row"](_el("RelationalTable", _TABLE))
    rb["_merge"](found, [r], "name")
    rb["_merge"](found, [r], "column: a, b")
    rb["_merge"](found, [r], "name")
    assert list(found) == ["g1"] and found["g1"]["matched"] == ["name", "column: a, b"]
    assert r["matched"] == []  # the input row is not mutated


def _member(guid):
    return {"relatedElement": {"elementHeader": {"guid": guid, "type": {"typeName": "TabularDataSet"}},
                               "properties": {"displayName": guid}},
            "relationshipHeader": {"type": {"typeName": "CollectionMembership"}}}


def test_flavour_index_maps_members_and_knows_when_hubs_are_unknown(rb):
    prod = {"elementHeader": {"guid": "p"}, "properties": {"displayName": "P"}, "collectionMembers": [_member("m1")]}
    idx = rb["_flavour_index"]([prod], None)
    assert idx["product"] == {"m1": [{"guid": "p", "displayName": "P"}]}
    assert idx["productGuids"] == ["p"] and idx["hub"] == {} and idx["hubTypeKnown"] is False
    idx = rb["_flavour_index"]([], [])
    assert idx["hubTypeKnown"] is True and idx["hubCount"] == 0


def test_recent_rows_merge_newest_first_without_noise(rb):
    a = [_el("RelationalTable", _TABLE, guid="t1", when="2026-10-02"), _el("SurveyReport", _SURVEY, guid="s", when="2026-10-09")]
    b = [_el("RelationalDatabase", ["Database", "DataAsset"], guid="d", when="2026-10-05"),
         _el("RelationalTable", _TABLE, guid="t1", when="2026-10-02")]
    assert [r["guid"] for r in rb["_recent_rows"]([a, b])] == ["d", "t1"]
