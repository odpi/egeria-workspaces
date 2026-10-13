# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""The Resource Browser's pure helpers: flavour, lineage direction, survey statistics.

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
           "_lineage", "_stats_name_of", "_latest_by_subject", "_jdbc_table_name"}
_CONSTS = {"_SKIP_CLASSIFICATIONS", "_LINEAGE_RELATIONSHIPS", "_TABLE_STATS_QN", "_COLUMN_STATS_QN"}


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
