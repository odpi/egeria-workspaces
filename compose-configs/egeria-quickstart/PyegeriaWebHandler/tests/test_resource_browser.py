# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""The Resource Locator's pure helpers: flavour, lineage direction, survey statistics,
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
import re
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
           "_text_reason", "_merge", "_flavour_index", "_recent_rows",
           # phase 3
           "_is_repo", "_list_slug", "_list_origin", "_list_record", "_list_members", "_membership_body",
           "_is_group", "_shared_with", "_groups_of",
           # structure
           "_related_recs", "_is_schema_attribute", "_is_schema_element", "_container_of", "_part_record",
           "_group_label", "_attribute_noun", "_merge_reads", "_is_term", "_meanings_of"}
_CONSTS = {"_SKIP_CLASSIFICATIONS", "_LINEAGE_RELATIONSHIPS", "_TABLE_STATS_QN", "_COLUMN_STATS_QN",
           "_RESOURCE_TYPES", "_NOT_RESOURCES", "_KINDS", "_BADGES",
           "_REPO_QN_PREFIX", "_RE_LIST_PREFIX", "_PORTAL_LIST_PREFIX", "_COPY_KEYS", "_GROUP_TYPES",
           "_CONTAINS_KEYS", "_PART_OF_KEYS", "_PART_LABELS", "_COUNTED_TYPES"}


def _load(path: Path):
    if not path.exists():
        pytest.skip(f"{path} not present in this checkout")
    tree = ast.parse(path.read_text(encoding="utf-8"))
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in _NEEDED]
    assert {n.name for n in funcs} == _NEEDED
    consts = [n for n in tree.body if isinstance(n, ast.Assign)
              and isinstance(n.targets[0], ast.Name) and n.targets[0].id in _CONSTS]
    ns = {"Optional": Optional, "re": re}
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


def test_jdbc_column_is_not_a_table(rb):
    ap = {"jdbc.catalog": "coco", "jdbc.schema": "sales", "jdbc.table": "orders", "jdbc.column": "id"}
    assert rb["_jdbc_table_name"]({"additionalProperties": ap}) is None


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


# ── Phase 3: work lists ──────────────────────────────────────────────────────

def test_repo_is_a_plain_asset_named_by_its_url(rb):
    r = rb["_row"](_el("Asset", ["Referenceable"], qn="GitHubRepository::https://github.com/odpi/egeria"))
    assert r and r["kind"] == "repo"
    assert rb["_row"](_el("Asset", ["Referenceable"], qn="Something::else")) is None
    assert rb["_row"](_el("Asset", ["Referenceable"], qn="Something::else"), any_type=True)["kind"] == "other"


def test_list_origin_is_by_prefix_and_owner(rb):
    o = rb["_list_origin"]
    assert o("WorkingSet::portal::erin::sales-ab12", "erin") == "mine"
    assert o("WorkingSet::portal::peter::sales-ab12", "erin") == "portal"
    assert o("WorkingSet::portal::erin::sales-ab12", None) == "portal"
    assert o("WorkingSet::resource-explorer::wl-1", "erin") == "resource-explorer"
    assert o("WorkingSet::Investigation::x::keep", "erin") == "other"
    assert rb["_list_slug"]("Sales tables, Q3!", "ab12cd") == "sales-tables-q3-ab12cd"
    assert rb["_list_slug"]("???", "ab12cd") == "list-ab12cd"


def _ws(qn, members=(), ap=None):
    return {"elementHeader": {"guid": "L", "type": {"typeName": "WorkingSet"}, "versions": {"updatedBy": "erin"}},
            "properties": {"qualifiedName": qn, "displayName": "My list", "additionalProperties": ap or {}},
            "collectionMembers": list(members)}


def test_list_record_editable_only_for_the_creator_and_keeps_provenance(rb):
    ap = {"copiedFromGUID": "S", "copiedFromName": "Scouting", "copiedAt": "2026-10-13", "other": "x"}
    mine = rb["_list_record"](_ws("WorkingSet::portal::erin::a-1", ap=ap), "erin")
    assert mine["editable"] and mine["creator"] == "erin"
    assert mine["copiedFrom"] == {"copiedFromGUID": "S", "copiedFromName": "Scouting", "copiedAt": "2026-10-13"}
    re_list = rb["_list_record"](_ws("WorkingSet::resource-explorer::wl-1"), "erin")
    assert not re_list["editable"] and re_list["creator"] is None and re_list["copiedFrom"] is None


def test_list_members_keep_reason_confidence_and_non_resources(rb):
    # confidence 0 is Egeria's default for "never set", so it reads as None
    def m(guid, type_name, supers, qn="", rel=None):
        return {"relatedElement": {"elementHeader": {"guid": guid, "type": {"typeName": type_name, "superTypeNames": supers}},
                                   "properties": {"displayName": guid, "qualifiedName": qn}},
                "relationshipProperties": dict({"class": "CollectionMembershipProperties"}, **(rel or {}))}
    members = rb["_list_members"](_ws("q", [
        m("t", "RelationalTable", _TABLE, rel={"membershipRationale": "has the sales figures", "confidence": 80}),
        m("p", "Person", ["ActorProfile"], rel={"confidence": 0}),
        m("r", "Asset", ["Referenceable"], qn="GitHubRepository::https://github.com/odpi/egeria.git"),
    ]))
    t, p, r = members
    assert (r["kind"], r["isResource"]) == ("repo", True)
    assert (t["rationale"], t["confidence"], t["isResource"]) == ("has the sales figures", 80, True)
    assert (p["rationale"], p["confidence"], p["isResource"], p["kind"]) == ("", None, False, "other")


def test_membership_body_only_when_there_is_something_to_say(rb):
    assert rb["_membership_body"](None) is None
    body = rb["_membership_body"]("why", 70)
    assert body["properties"] == {"membershipRationale": "why", "confidence": 70,
                                  "class": "CollectionMembershipProperties"}
    assert rb["_membership_body"]("why", 0)["properties"] == {"membershipRationale": "why",
                                                              "class": "CollectionMembershipProperties"}


# ── Phase 3: team sharing ────────────────────────────────────────────────────

def _rel_item(rel_type, guid, type_name, supers=(), name=None, at_end1=True):
    return {"relationshipHeader": {"type": {"typeName": rel_type}}, "relatedElementAtEnd1": at_end1,
            "relatedElement": {"elementHeader": {"guid": guid, "type": {"typeName": type_name, "superTypeNames": list(supers)}},
                               "properties": {"displayName": name or guid}}}


def test_groups_are_teams_communities_and_their_subtypes(rb):
    assert rb["_is_group"]("Team", []) and rb["_is_group"]("Community", [])
    assert rb["_is_group"]("Organization", ["Team", "ActorProfile"])
    assert not rb["_is_group"]("Person", ["ActorProfile"]) and not rb["_is_group"]("Project", [])


def test_shared_with_reads_resource_list_from_groups_only(rb):
    ws = _ws("WorkingSet::portal::erin::x-1")
    ws["resourceListUsers"] = [_rel_item("ResourceList", "t1", "Team", name="Chief Data Office"),
                               _rel_item("ResourceList", "p1", "Project", name="Some project")]
    ws["collectionMembers"] = [_rel_item("CollectionMembership", "c1", "Community", name="Not a share")]
    assert rb["_shared_with"](ws) == [{"guid": "t1", "displayName": "Chief Data Office", "typeName": "Team"}]
    assert rb["_list_record"](ws, "erin")["sharedWith"][0]["guid"] == "t1"


def test_groups_of_follow_roles_and_direct_scope(rb):
    person = {"assignmentScope": [_rel_item("AssignmentScope", "proj", "Project"),
                                  _rel_item("AssignmentScope", "c9", "Community", name="Direct SIG")]}
    role_a = {"properties": {"displayName": "TeamMembers::Department::7432"},
              "assignmentScope": [_rel_item("AssignmentScope", "t1", "Team", name="Chief Data Office")]}
    role_b = {"properties": {"displayName": "Member: SIG"},
              "assignmentScope": [_rel_item("AssignmentScope", "t1", "Team", name="Chief Data Office"),
                                  _rel_item("AssignmentScope", "c1", "Community", name="Data Science SIG")]}
    groups = rb["_groups_of"](person, [role_a, role_b])
    assert [(g["typeName"], g["displayName"], g["via"]) for g in groups] == [
        ("Community", "Data Science SIG", "Member: SIG"),
        ("Community", "Direct SIG", "you directly"),
        ("Team", "Chief Data Office", "TeamMembers::Department::7432"),
    ]


# ── Structure: part of / contains ────────────────────────────────────────────

def _part_item(guid, type_name, supers=(), name="n", rel="R", at_end1=False):
    return {"relatedElement": {"elementHeader": {"guid": guid, "type": {"typeName": type_name,
                                                                        "superTypeNames": list(supers)}},
                               "properties": {"displayName": name}},
            "relationshipHeader": {"type": {"typeName": rel}}, "relatedElementAtEnd1": at_end1}


_TABLE_SUPERS = ["SchemaAttribute", "SchemaElement", "Referenceable"]


def test_related_recs_takes_a_list_or_one_element(rb):
    one = _part_item("s1", "RelationalDBSchemaType")
    assert [r["guid"] for r in rb["_related_recs"](one)] == ["s1"]
    assert [r["guid"] for r in rb["_related_recs"]([one, _part_item("s2", "X")])] == ["s1", "s2"]
    assert rb["_related_recs"](None) == []


def test_schema_sits_in_its_database(rb):
    el = {"elementHeader": {"guid": "sch", "type": {"typeName": "DeployedDatabaseSchema"}},
          "dataSetContent": [_part_item("db", "RelationalDatabase", ["Database"], "coco", "DataSetContent")]}
    assert rb["_container_of"](el)["guid"] == "db"


def test_column_sits_in_its_table_and_table_in_its_anchor(rb):
    column = {"elementHeader": {"guid": "col", "type": {"typeName": "RelationalColumn", "superTypeNames": _TABLE_SUPERS},
                                "anchor": {"classificationProperties": {"anchorGUID": "sch"}}},
              "parentSchemaElements": [_part_item("tab", "RelationalTable", _TABLE_SUPERS, rel="NestedSchemaAttribute")]}
    assert rb["_container_of"](column)["guid"] == "tab"
    # A top-level table hangs off a schema type, which is not a container people browse:
    # its container is the asset it is anchored to.
    table = {"elementHeader": {"guid": "tab", "type": {"typeName": "RelationalTable", "superTypeNames": _TABLE_SUPERS},
                               "anchor": {"classificationProperties": {"anchorGUID": "sch",
                                                                       "anchorTypeName": "DeployedDatabaseSchema"}}},
             "parentSchemaElements": [_part_item("st", "RelationalDBSchemaType", ["ComplexSchemaType"], rel="AttributeForSchema")]}
    up = rb["_container_of"](table)
    assert (up["guid"], up["typeName"]) == ("sch", "DeployedDatabaseSchema")


def test_top_of_the_path_has_no_container(rb):
    db = {"elementHeader": {"guid": "db", "type": {"typeName": "RelationalDatabase", "superTypeNames": ["Database", "Asset"]},
                            "anchor": {"classificationProperties": {"anchorGUID": "db"}}},
          "supportedDataSets": [_part_item("sch", "DeployedDatabaseSchema")]}
    assert rb["_container_of"](db) is None


def test_part_record_kind_group_and_catalog_anchor(rb):
    rec = rb["_related"](_part_item("tab", "RelationalTable", _TABLE_SUPERS, "orders"))
    rec["elementHeader"]["anchor"] = {"classificationProperties": {"anchorGUID": "sch"}}
    part = rb["_part_record"](rec)
    assert (part["kind"], part["anchorGUID"], rb["_group_label"](part)) == ("table", "sch", "Tables")
    field = rb["_part_record"](rb["_related"](_part_item("f", "TabularColumn", ["SchemaAttribute"])))
    assert rb["_group_label"](field) == "Fields"
    # A data set subtype groups under its kind; a type with no kind keeps its own name.
    secrets = rb["_part_record"](rb["_related"](_part_item("o", "SecretsCollection", ["DataSet"])))
    assert rb["_group_label"](secrets) == "Data sets"
    other = rb["_part_record"](rb["_related"](_part_item("v", "VirtualConnection", ["Connection"])))
    assert rb["_group_label"](other) == "Virtual Connection"
    op = rb["_part_record"](rb["_related"](_part_item("op", "APIOperation", ["SchemaType", "SchemaElement"])))
    assert rb["_group_label"](op) == "Operations"


def test_api_operation_and_event_type_belong_to_their_anchor(rb):
    op = {"elementHeader": {"guid": "op", "type": {"typeName": "APIOperation", "superTypeNames": ["SchemaType", "SchemaElement"]},
                            "anchor": {"classificationProperties": {"anchorGUID": "api", "anchorTypeName": "DeployedAPI"}}},
          "parentSchemaElements": [_part_item("st", "APISchemaType", ["SchemaType", "SchemaElement"], rel="APIOperations")]}
    assert rb["_container_of"](op)["guid"] == "api"
    # A field of an event type sits in the event type, which is browsable.
    field = {"elementHeader": {"guid": "f", "type": {"typeName": "EventSchemaAttribute", "superTypeNames": _TABLE_SUPERS},
                               "anchor": {"classificationProperties": {"anchorGUID": "topic"}}},
             "parentSchemaElements": [_part_item("et", "EventType", ["SchemaType", "SchemaElement"], rel="AttributeForSchema")]}
    assert rb["_container_of"](field)["guid"] == "et"


def test_attribute_noun(rb):
    recs = lambda t, s: [rb["_related"](_part_item("g", t, s))]
    assert rb["_attribute_noun"](recs("RelationalTable", _TABLE_SUPERS)) == "tables"
    assert rb["_attribute_noun"](recs("RelationalColumn", _TABLE_SUPERS)) == "columns"
    assert rb["_attribute_noun"](recs("EventSchemaAttribute", _TABLE_SUPERS)) == "fields"


def test_merge_reads_keeps_each_relationship_once(rb):
    def item(rel_guid, guid):
        it = _part_item(guid, "X")
        it["relationshipHeader"]["guid"] = rel_guid
        return it
    a = {"elementHeader": {"guid": "e"}, "properties": {"n": 1}, "class": "C",
         "lineageLinkage": [item("r1", "a"), item("r2", "b")], "schemaType": item("r9", "st")}
    b = {"elementHeader": {"guid": "e"}, "properties": {"n": 1}, "lineageLinkage": [item("r2", "b"), item("r3", "c")]}
    m = rb["_merge_reads"]([a, b])
    assert [i["relatedElement"]["elementHeader"]["guid"] for i in m["lineageLinkage"]] == ["a", "b", "c"]
    assert m["schemaType"]["relatedElement"]["elementHeader"]["guid"] == "st" and m["class"] == "C"


def test_meanings_are_terms_by_semantic_assignment(rb):
    t = _part_item("t1", "GlossaryTerm", ["Referenceable"], "Customer", rel="SemanticAssignment")
    t["relationshipProperties"] = {"termAssignmentStatus": "PROPOSED", "class": "SemanticAssignmentProperties"}
    t["relationshipHeader"]["versions"] = {"createdBy": "erinoverview", "createTime": "2026-10-13"}
    not_term = _part_item("x", "Comment", rel="SemanticAssignment")
    other_rel = _part_item("t2", "GlossaryTerm", rel="RelatedTerm")
    out = rb["_meanings_of"]({"elementHeader": {}, "meanings": [t, not_term], "relatedTerms": [other_rel]})
    assert [(m["guid"], m["status"], m["assignedBy"]) for m in out] == [("t1", "PROPOSED", "erinoverview")]
