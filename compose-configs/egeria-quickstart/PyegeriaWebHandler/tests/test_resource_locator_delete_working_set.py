# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""PO-43 (Dan, 2026-11-17): the owner deletes a working set, removing its links and then the set.

Design note DESIGN-RL-PO42-PO43-WORKING-SETS-RENAME-AND-DELETE-2026-11-17, Architect read-back R1-R4:
  - order: team shares, the owner's lenses, members one at a time, a re-read, then the delete;
  - R1: the delete sends no body, so cascadedDelete=false reaches Egeria (checked on the request);
  - members are never deleted; anything else linked or anchored blocks, named, with 0 writes;
  - R2: the plan endpoint writes nothing (every non-get/find call counts as a write);
  - R3: the per-set lock is dropped when its delete ends;
  - R4: a member added after the re-read (Egeria 403-005) is reported, nothing more removed;
  - a delete that stops part-way says what was removed and what is left (207).
No Egeria: the clients are fakes."""
import asyncio
import copy
import json

import pytest

import resource_browser_handler as rb

ME = "erin"
SET = "WS1"


def _item(rel_type, guid, type_name, at_end1, name=None, qn="", supers=(), anchor=None):
    hdr = {"guid": guid, "type": {"typeName": type_name, "superTypeNames": list(supers)}}
    if anchor:
        hdr["anchor"] = {"classificationProperties": {"anchorGUID": anchor}}
    return {"relationshipHeader": {"type": {"typeName": rel_type}}, "relatedElementAtEnd1": at_end1,
            "relatedElement": {"elementHeader": hdr, "properties": {"displayName": name or guid, "qualifiedName": qn}}}


def _set(members=("m1", "m2", "m3"), shares=("t1",), lenses=(("L1", "DataLens::portal::erin::uk"),), extra=None,
         qn="WorkingSet::portal::erin::q3-ab12"):
    el = {"elementHeader": {"guid": SET, "type": {"typeName": "WorkingSet"}, "versions": {}},
          "properties": {"qualifiedName": qn, "displayName": "Q3 sources"},
          "collectionMembers": [_item("CollectionMembership", g, "RelationalTable", False, name=g) for g in members],
          "resourceListUsers": [_item("ResourceList", g, "Team", True, name="Team " + g) for g in shares],
          "governedBy": [_item("GovernedBy", g, "DataLens", True, name="Lens " + g, qn=q) for g, q in lenses]}
    for k, v in (extra or {}).items():
        el[k] = v
    return el


class World:
    """The fake Egeria: one working set, the anchored-element index, and a log of every call."""

    def __init__(self, el, anchored=()):
        self.el = el
        self.anchored = list(anchored)
        self.calls = []
        self.fail = {}            # method name -> (guid or None, exception)
        self.on_call = {}         # method name -> callable(*args) run before answering

    def _maybe_fail(self, name, guid):
        f = self.fail.get(name)
        if f and (f[0] is None or f[0] == guid):
            raise f[1]

    def remove_rel(self, key, guid):
        self.el[key] = [i for i in self.el.get(key, []) if i["relatedElement"]["elementHeader"]["guid"] != guid]


class Recorder:
    """Every _async_* call is logged; anything not a get/find counts as a write (R2)."""

    def __init__(self, world, impl):
        self._w, self._impl = world, impl

    def __getattr__(self, name):
        if not name.startswith("_async_"):
            raise AttributeError(name)

        async def call(*args, **kwargs):
            self._w.calls.append((name, args, kwargs))
            if name in self._w.on_call:
                self._w.on_call[name](*args)
            fn = self._impl.get(name)
            if fn is None:
                raise AssertionError(f"unexpected call {name}")
            return fn(*args, **kwargs)
        return call


def _writes(world):
    return [c for c in world.calls if not c[0].startswith(("_async_get", "_async_find"))]


@pytest.fixture
def world(monkeypatch):
    w = World(_set())

    def get_el(guid, **k):
        return copy.deepcopy(w.el)

    def anchored(*a, **k):
        return list(w.anchored)

    def detach(group, guid, **k):
        w._maybe_fail("_async_detach_collection", group)
        w.remove_rel("resourceListUsers", group)

    def remove(guid, member, **k):
        w._maybe_fail("_async_remove_from_collection", member)
        w.remove_rel("collectionMembers", member)

    def delete(guid, **k):
        w._maybe_fail("_async_delete_collection", None)
        w.deleted = k

    def ungovern(guid, lens, **k):
        w._maybe_fail("_async_detach_governed_by_definition", lens)
        w.remove_rel("governedBy", lens)

    client = Recorder(w, {"_async_get_element_by_guid": get_el,
                          "_async_get_elements_by_classification_with_property_value": anchored})
    cm = Recorder(w, {"_async_detach_collection": detach, "_async_remove_from_collection": remove,
                      "_async_delete_collection": delete})
    officer = Recorder(w, {"_async_detach_governed_by_definition": ungovern})

    async def explorer():
        return client

    async def collections():
        return cm

    async def officer_async():
        return officer
    import resource_locator_lens_handler as lh
    monkeypatch.setattr(rb, "_explorer_async", explorer)
    monkeypatch.setattr(rb, "_collections_async", collections)
    monkeypatch.setattr(lh, "_officer_async", officer_async)
    monkeypatch.setattr(rb, "_token_user", lambda: ME)
    monkeypatch.setattr(rb, "_DELETE_LOCKS", {})
    w.deleted = None
    return w


def _names(world):
    return [c[0] for c in _writes(world)]


# ── the plan ─────────────────────────────────────────────────────────────────────────────────────────

def test_plan_names_what_goes_and_writes_nothing(client, world):
    r = client.get(f"/api/resource-browser/lists/{SET}/delete-plan")
    assert r.status_code == 200, r.text
    d = r.json()
    assert d["members"] == 3 and d["memberNames"] == ["m1", "m2", "m3"]
    assert [g["guid"] for g in d["shares"]] == ["t1"] and [l["guid"] for l in d["lenses"]] == ["L1"]
    assert d["blockers"] == [] and d["canDelete"] is True
    assert _writes(world) == []                                     # R2


@pytest.mark.parametrize("qn,words", [
    ("WorkingSet::portal::peter::q3-ab12", "Only the person who made a working set can delete it."),
    ("WorkingSet::resource-explorer::wl-1", "Resource Explorer working sets are managed in Resource Explorer"),
])
def test_only_the_owner_and_never_a_resource_explorer_set(client, world, qn, words):
    world.el = _set(qn=qn)
    for r in (client.get(f"/api/resource-browser/lists/{SET}/delete-plan"),
              client.delete(f"/api/resource-browser/lists/{SET}")):
        assert r.status_code == 403 and words in r.json()["detail"]
    assert _writes(world) == []


def test_blockers_are_named_and_nothing_is_written(client, world):
    world.el = _set(lenses=(("L1", "DataLens::portal::erin::uk"), ("L9", "DataLens::portal::peter::eu")),
                    extra={"attachedTags": [_item("AttachedTag", "tag1", "InformalTag", True, name="hot")],
                           "memberOfCollections": [_item("CollectionMembership", "P", "Collection", True, name="Parent")]})
    world.el["collectionMembers"].append(_item("CollectionMembership", "m9", "Comment", False, name="note", anchor=SET))
    world.anchored = [{"elementHeader": {"guid": "c7", "type": {"typeName": "Comment"}}, "properties": {"displayName": "why"}}]
    d = client.get(f"/api/resource-browser/lists/{SET}/delete-plan").json()
    texts = " | ".join(b["text"] for b in d["blockers"])
    assert d["canDelete"] is False
    assert "owned by peter" in texts and "AttachedTag link to ‘hot’" in texts
    assert "CollectionMembership link to ‘Parent’" in texts           # the set held by another collection
    assert "‘note’ (Comment) belongs to this working set" in texts      # an anchored member
    assert "‘why’ (Comment) belongs to this working set" in texts       # anchored, not linked
    r = client.delete(f"/api/resource-browser/lists/{SET}")
    assert r.status_code == 409 and r.json()["deleted"] is False and r.json()["detail"].startswith("Nothing was removed")
    assert _writes(world) == []


def test_a_capped_read_blocks(client, world):
    world.el = _set(members=[f"m{i}" for i in range(rb._RELATED_LIMIT)])
    d = client.get(f"/api/resource-browser/lists/{SET}/delete-plan").json()
    assert not d["canDelete"] and any(b["kind"] == "capped" for b in d["blockers"])


# ── the delete ───────────────────────────────────────────────────────────────────────────────────────

def test_delete_order_and_members_are_never_deleted(client, world):
    r = client.delete(f"/api/resource-browser/lists/{SET}")
    assert r.status_code == 200, r.text
    d = r.json()
    assert d["deleted"] is True and d["membersKept"] == 3
    assert _names(world) == ["_async_detach_collection", "_async_detach_governed_by_definition",
                             "_async_remove_from_collection", "_async_remove_from_collection",
                             "_async_remove_from_collection", "_async_delete_collection"]
    deletes = [c for c in _writes(world) if c[0] == "_async_delete_collection"]
    assert deletes == [("_async_delete_collection", (SET,), {"cascade": False})]   # R1: no body
    # the re-read happens between the last unlink and the delete
    names = [c[0] for c in world.calls]
    last_unlink = max(i for i, n in enumerate(names) if n == "_async_remove_from_collection")
    assert "_async_get_element_by_guid" in names[last_unlink:names.index("_async_delete_collection")]
    assert rb._DELETE_LOCKS == {}                                                # R3


def test_stops_at_the_first_failed_unlink_and_says_what_is_left(client, world):
    world.fail["_async_remove_from_collection"] = ("m2", RuntimeError("not authorised"))
    r = client.delete(f"/api/resource-browser/lists/{SET}")
    assert r.status_code == 207
    d = r.json()
    assert d["deleted"] is False and d["removed"]["members"] == 1
    assert d["left"] == {"shares": [], "lenses": [], "members": 2}
    assert d["failed"]["step"] == "unlink" and d["failed"]["guid"] == "m2"
    assert "_async_delete_collection" not in _names(world)
    # delete again carries on from what is left
    world.fail.clear()
    r = client.delete(f"/api/resource-browser/lists/{SET}")
    assert r.status_code == 200 and r.json()["deleted"] is True


def test_a_member_added_after_the_unlinks_stops_before_the_delete(client, world):
    """Someone adds a resource while the members are being unlinked: the re-read sees it, so the set is
    not deleted and nothing more is removed."""
    def add_once(*a):
        if not getattr(world, "_added", False):
            world._added = True
            world.el["collectionMembers"].append(_item("CollectionMembership", "late", "RelationalTable", False))
    world.on_call["_async_remove_from_collection"] = add_once
    r = client.delete(f"/api/resource-browser/lists/{SET}")
    assert r.status_code == 207
    d = r.json()
    assert d["deleted"] is False and d["failed"]["step"] == "re-read" and d["left"]["members"] == 1
    assert "nothing more was removed" in d["failed"]["message"]
    assert _names(world).count("_async_remove_from_collection") == 3      # only the planned three
    assert "_async_delete_collection" not in _names(world)


def test_r4_egeria_has_members_is_reported_and_nothing_more_removed(client, world):
    def late_add(*a):
        world.el["collectionMembers"].append(_item("CollectionMembership", "late", "RelationalTable", False))
    world.on_call["_async_delete_collection"] = late_add
    world.fail["_async_delete_collection"] = (None, RuntimeError("OMAG-GENERIC-HANDLERS-403-005 collection has members"))
    r = client.delete(f"/api/resource-browser/lists/{SET}")
    assert r.status_code == 207
    d = r.json()
    assert d["failed"]["step"] == "delete" and "A resource was added while deleting" in d["failed"]["message"]
    assert d["left"]["members"] == 1
    assert _names(world).count("_async_remove_from_collection") == 3      # no second round of unlinks


def test_a_refused_delete_after_every_unlink_says_the_set_is_empty(client, world):
    world.fail["_async_delete_collection"] = (None, RuntimeError("server busy"))
    d = client.delete(f"/api/resource-browser/lists/{SET}").json()
    assert d["deleted"] is False and d["left"] == {"shares": [], "lenses": [], "members": 0}
    assert "It is empty now" in d["failed"]["message"]


def test_a_second_delete_while_one_runs_is_409(world):
    lock = asyncio.Lock()

    async def go():
        await lock.acquire()
        rb._DELETE_LOCKS[SET] = lock
        try:
            await rb.delete_list(SET)
        except rb.HTTPException as exc:
            return exc.status_code, exc.detail
        finally:
            lock.release()
    status, detail = asyncio.run(go())
    assert status == 409 and "already running" in detail


# ── R1 on the request pyegeria builds ───────────────────────────────────────────────────────────────

def test_r1_the_delete_request_carries_cascaded_delete_false_and_no_purge():
    from pyegeria import CollectionManager
    sent = []
    cm = CollectionManager.__new__(CollectionManager)
    cm.collection_command_root = "https://egeria.test/servers/v/api/open-metadata/collection-manager/collections"

    async def make_request(method, url, body=None, *a, **k):
        sent.append((method, url, body))
    cm._async_make_request = make_request
    try:
        asyncio.run(cm._async_delete_collection(SET, cascade=False))
    except AttributeError as exc:                     # a pyegeria that needs more set-up than this fake
        pytest.skip(f"pyegeria CollectionManager needs more set-up: {exc}")
    (method, url, body), = sent
    assert method == "POST" and url.endswith(f"/{SET}/delete")
    body = json.loads(body) if isinstance(body, str) else (body or {})
    assert body.get("cascadedDelete") is False
    assert not any(k.lower().startswith("purge") or "purge" in k.lower() for k in body)
