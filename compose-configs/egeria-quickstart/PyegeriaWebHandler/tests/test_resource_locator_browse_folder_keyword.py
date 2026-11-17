# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Resource Locator Browse by Folder and by Search keyword (Dan, 2026-11-17; design note
DESIGN-RL-BROWSE-CLASSIFICATION-TERM-CATEGORY-FOLDER-KEYWORD, Architect read-back R3, R5).

Pinned here:
  - folder values: every visible CollectionFolder except templates, with where it is anchored
    and NO count (a count would take one read per folder; absent is never 0);
  - a folder list: resources, glossary terms and parts as rows, sub-folders apart, what holds the
    folder, and everything else counted by type; a folder at the depth-1 limit says "at least" (R5),
    and so does a collection (same helper);
  - keyword values group by text ignoring case and count attachments; the list reads exactly those
    keyword elements, so rows + hidden + unread + not shown always equals the count (R3);
  - an empty folder says it holds nothing you can see; a keyword not visible is 404.
Endpoints run through the real app with fake Egeria clients; nothing is written."""
import pytest

import resource_browser_handler as rb


def _el(guid, type_name, supers, name, **hdr_extra):
    hdr = {"guid": guid, "type": {"typeName": type_name, "superTypeNames": supers}, "versions": {}, **hdr_extra}
    return {"elementHeader": hdr, "properties": {"displayName": name, "qualifiedName": f"qn::{name}"}}


def _anchor(type_name):
    return {"anchor": {"class": "ElementClassification", "classificationName": "Anchors",
                       "classificationProperties": {"anchorTypeName": type_name}}}


def _tmpl():
    return {"template": {"class": "ElementClassification", "classificationName": "Template"}}


_FOLDER_T = ["Collection", "AuthoredReferenceable", "Referenceable"]
_TABLE = _el("r1", "RelationalTable", ["SchemaAttribute", "DataAsset"], "orders")
_TERM = _el("t1", "GlossaryTerm", ["AuthoredReferenceable", "Referenceable"], "Order")
_FIELD = _el("f1", "DataField", ["Referenceable"], "order_id")
_GAT = _el("g1", "GovernanceActionType", ["Referenceable"], "survey")
_SUB = _el("sub", "CollectionFolder", _FOLDER_T, "Sub folder")


def _item(el, end1=False):
    return {"relatedElement": el, "relationshipHeader": {"type": {"typeName": "CollectionMembership"}}, "relatedElementAtEnd1": end1}


class _Explorer:
    def __init__(self, state):
        self.state = state

    async def _async_get_element_by_guid(self, guid, **kw):
        if guid in self.state.get("fail", ()):
            raise RuntimeError("read failed")
        return self.state["elements"][guid]

    async def _async_find_search_keywords(self, search_string="*", start_from=0, **kw):
        assert search_string == "*" and kw.get("graph_query_depth") == 0
        return [] if start_from else self.state["keywords"]


@pytest.fixture
def fake(monkeypatch):
    state = {"elements": {}, "keywords": [], "folders": [], "folders_capped": False}

    async def explorer():
        return _Explorer(state)

    async def all_elements(_client, type_name, *a, **kw):
        assert type_name == "CollectionFolder"
        return state["folders"], state["folders_capped"]

    async def cached(name, producer, ttl=600):
        return await producer(), rb.datetime.now(rb.timezone.utc)
    monkeypatch.setattr(rb, "_explorer_async", explorer)
    monkeypatch.setattr(rb, "_all_elements", all_elements)
    monkeypatch.setattr(rb, "_cached", cached)
    return state


def _folder(guid, members, parents=()):
    el = _el(guid, "CollectionFolder", _FOLDER_T, "Orders folder")
    el["collectionMembers"] = [_item(m) for m in members]
    el["memberOfCollections"] = [_item(p, end1=True) for p in parents]
    return el


# ── Folder ──────────────────────────────────────────────────────────────────

def test_folder_values_skip_templates_say_where_and_carry_no_count(client, fake):
    fake["folders"] = [_el("a", "CollectionFolder", _FOLDER_T, "Beta", **_anchor("Glossary")),
                       _el("b", "CollectionFolder", _FOLDER_T, "alpha", **_anchor("CollectionFolder")),
                       _el("c", "CollectionFolder", _FOLDER_T, "Gamma"),
                       _el("d", "CollectionFolder", _FOLDER_T, "Template folder", **_tmpl())]
    d = client.get("/api/resource-browser/browse/folder").json()
    assert [(v["label"], v["description"]) for v in d["values"]] == [
        ("alpha", "inside another folder"), ("Beta", "anchored to a Glossary"), ("Gamma", "no anchor recorded")]
    assert all("count" not in v for v in d["values"])
    assert "one read per folder" in d["note"] and d["countsAre"] is None


def test_folder_values_capped_say_at_least(client, fake):
    fake["folders"], fake["folders_capped"] = [_el("a", "CollectionFolder", _FOLDER_T, "A")], True
    assert "at least" in client.get("/api/resource-browser/browse/folder").json()["countsAre"]


def test_folder_list_shows_rows_subfolders_holder_and_names_the_rest(client, fake):
    glossary = _el("gl", "Glossary", _FOLDER_T, "Sales glossary")
    fake["elements"]["F"] = _folder("F", [_TABLE, _TERM, _FIELD, _GAT, _GAT, _SUB], parents=[glossary])
    d = client.get("/api/resource-browser/browse/folder/F").json()
    assert sorted((r["guid"], r["kind"]) for r in d["items"]) == [("f1", "field"), ("r1", "table"), ("t1", "term")]
    assert d["subfolders"] == [{"guid": "sub", "displayName": "Sub folder"}]
    assert d["heldBy"] == [{"guid": "gl", "displayName": "Sales glossary", "typeName": "Glossary"}]
    assert d["notShownTypes"] == {"GovernanceActionType": 2} and d["notShown"] == 2
    assert d["membersRead"] == 6 and d["capped"] is False


def test_empty_folder_says_it_holds_nothing_you_can_see(client, fake):
    fake["elements"]["E"] = _folder("E", [])
    d = client.get("/api/resource-browser/browse/folder/E").json()
    assert d["items"] == [] and "holds nothing you can see" in d["note"]


def test_folder_and_collection_at_the_depth1_limit_are_capped(client, fake, monkeypatch):
    monkeypatch.setattr(rb, "_RELATED_LIMIT", 3)
    fake["elements"]["F"] = _folder("F", [_TABLE, _TERM, _FIELD])
    assert client.get("/api/resource-browser/browse/folder/F").json()["capped"] is True
    coll = _folder("C", [_TABLE, _TERM, _FIELD])
    coll["elementHeader"]["type"]["typeName"] = "DigitalProductFamily"
    fake["elements"]["C"] = coll
    assert client.get("/api/resource-browser/browse/collection/C").json()["capped"] is True


def test_folder_list_takes_a_lens(client, fake, monkeypatch):
    fake["elements"]["F"] = _folder("F", [_TABLE])

    async def apply(lens, rows, capped):
        return {"lens": {"guid": lens}, "lensCounts": {"inside": 0, "outside": 0, "notComparable": len(rows), "notRead": 0, "partial": capped}}
    monkeypatch.setattr(rb, "_apply_lens", apply)
    d = client.get("/api/resource-browser/browse/folder/F?lens=L1").json()
    assert d["lens"] == {"guid": "L1"} and d["lensCounts"]["notComparable"] == 1


# ── Search keyword ──────────────────────────────────────────────────────────

def _kw(guid, text):
    return {"elementHeader": {"guid": guid, "type": {"typeName": "SearchKeyword", "superTypeNames": ["OpenMetadataRoot"]}},
            "properties": {"displayName": text}}


def _kw_read(guid, linked):
    el = _kw(guid, "x")
    el["keywordElements"] = [{"relatedElement": e} for e in linked]
    return el


def _keyword_state(fake):
    fake["keywords"] = [_kw("k1", "Reference Data"), _kw("k2", "reference data"), _kw("k3", "Reference data"),
                        _kw("k4", "Reference Data"), _kw("k5", "Reference Data"), _kw("k6", "productized")]
    fake["elements"].update(k1=_kw_read("k1", [_TABLE]), k2=_kw_read("k2", [_TERM]), k3=_kw_read("k3", []),
                            k4=_kw_read("k4", [_GAT]), k6=_kw_read("k6", [_TABLE]))
    fake["fail"] = {"k5"}


def test_keyword_values_group_ignoring_case_and_count_attachments(client, fake):
    _keyword_state(fake)
    d = client.get("/api/resource-browser/browse/keyword").json()
    assert [(v["label"], v["count"]) for v in d["values"]] == [("productized", 1), ("Reference Data", 5)]
    assert "attachments" in d["countsAre"]


def test_keyword_list_accounts_for_its_count(client, fake):
    _keyword_state(fake)
    d = client.get("/api/resource-browser/browse/keyword/REFERENCE%20DATA").json()
    assert d["title"] == "Keyword: Reference Data"
    assert sorted(r["guid"] for r in d["items"]) == ["r1", "t1"]
    assert d["hiddenAttachments"] == 1 and d["unreadAttachments"] == 1 and d["notShownTypes"] == {"GovernanceActionType": 1}
    assert len(d["items"]) + d["hiddenAttachments"] + d["unreadAttachments"] + d["notShown"] == d["attachments"] == 5
    assert "cannot see" in d["note"] and "could not be read" in d["note"]


def test_a_keyword_you_cannot_see_is_404(client, fake):
    _keyword_state(fake)
    r = client.get("/api/resource-browser/browse/keyword/nope")
    assert r.status_code == 404 and "visible to you" in r.json()["detail"]
