"""Bug B5 (Egeria 8840035f, 2026-11-12): a find with pageSize 1 answers "No elements found" even when a
match exists; pageSize 10, 25 or none returns it. The Portal's canary lookups asked for 1, so the
OpenLineage Events canary read as missing and the monitor re-healed it every pass.

The fakes here behave like 8840035f: "No elements found" for pageSize 1, the element(s) otherwise.
- The canary and the manual-step lookup ask for _CANARY_PAGE_SIZE (25) and read a present element as
  present; a truly absent one still reads missing / not found.
- The oldest-createTime lookup asks for a page of 25 sorted oldest first and takes raw[0].
Offline: nothing talks to Egeria.
"""
import asyncio
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import bootstrap_monitor_handler as bm  # noqa: E402

NO = "No elements found"


def _b5(found):
    """A find that behaves like Egeria 8840035f: pageSize 1 -> "No elements found"."""
    calls = []

    async def find(body):
        calls.append(body)
        if body.get("pageSize") == 1:
            return NO
        return list(found) if found else NO
    return find, calls


@pytest.fixture
def expert(monkeypatch):
    """pyegeria.MetadataExpert replaced by a fake whose find is `state["find"]`; no token, no network."""
    import pyegeria
    import egeria_auth
    state = {}

    class FakeExpert:
        def __init__(self, *a, **k):
            pass

        async def _async_find_metadata_elements(self, body):
            return await state["find"](body)

        async def _async_close_session(self):
            pass

    async def no_token(mgr):
        return None

    monkeypatch.setattr(pyegeria, "MetadataExpert", FakeExpert)
    monkeypatch.setattr(egeria_auth, "async_apply_token", no_token)
    return state


FAMILY = {"name": "batch:OpenLineage Events", "canary_type": "Topic", "canary_name": "openlineage.events"}
TOPIC = {"elementGUID": "00daa9fb-11b7-409d-9ee2-1602ea0aff42"}


def test_the_page_size_is_not_one():
    assert bm._CANARY_PAGE_SIZE >= 2
    src = (Path(bm.__file__)).read_text()
    assert '"pageSize": 1' not in src and "pageSize=1." not in src


def test_a_present_canary_reads_present_under_b5(expert):
    expert["find"], calls = _b5([TOPIC])
    assert asyncio.run(bm._canary_present(FAMILY)) == (True, True)
    assert [c["pageSize"] for c in calls] == [bm._CANARY_PAGE_SIZE]


def test_an_absent_canary_still_reads_missing(expert):
    expert["find"], calls = _b5([])
    assert asyncio.run(bm._canary_present(FAMILY)) == (False, True)
    assert calls[0]["searchProperties"]["conditions"][0]["value"]["primitiveValue"] == "openlineage.events"


def test_what_pagesize_1_would_have_said(expert):
    """The bug itself, for the record: the same fake at pageSize 1 says nothing is there."""
    find, _ = _b5([TOPIC])
    assert asyncio.run(find({"pageSize": 1})) == NO and asyncio.run(find({"pageSize": 25})) == [TOPIC]


STEP = {"id": "saved-query-first-refresh", "type": "SavedQuery", "qualifiedName": "SavedQuery::X",
        "doneProperty": "lastRefreshedTime", "description": "d", "how": "h"}


def test_the_manual_step_lookup_reads_the_element_under_b5(expert):
    el = {"properties": {"qualifiedName": "SavedQuery::X", "additionalProperties": {"lastRefreshedTime": "t"}}}
    expert["find"], calls = _b5([el])
    st = asyncio.run(bm._manual_step_state(STEP))
    assert st["state"] == "done" and [c["pageSize"] for c in calls] == [bm._CANARY_PAGE_SIZE]


def test_an_absent_manual_step_element_is_still_not_found(expert):
    expert["find"], _ = _b5([])
    st = asyncio.run(bm._manual_step_state(STEP))
    assert st["state"] == "not checked" and "was not found" in st["detail"]


# ── catalog_search: the oldest createTime ─────────────────────────────────────

def test_oldest_create_time_under_b5(monkeypatch):
    import catalog_search_handler as cs
    bodies = []
    oldest = {"elementHeader": {"versions": {"createTime": "2021-12-20T07:20:40.038+00:00"}}}
    newer = {"elementHeader": {"versions": {"createTime": "2026-11-12T10:00:00+00:00"}}}

    class FakeCE:
        def find_root_elements(self, body=None, output_format=None):
            bodies.append(body)
            return NO if body.get("pageSize") == 1 else [oldest, newer]   # sorted oldest first

    monkeypatch.setattr(cs, "_classification_explorer", lambda *a: FakeCE())
    monkeypatch.setattr(cs, "request_identity", lambda u, p: None)       # no cache in play
    r = cs.oldest_create_time(url=None, server=None, user_id=None)
    import json
    assert json.loads(r.body) == {"createTime": "2021-12-20T07:20:40.038+00:00"}
    assert bodies[0]["pageSize"] == cs._OLDEST_PAGE_SIZE == 25
    assert bodies[0]["sequencingOrder"] == "CREATION_DATE_OLDEST"


def test_oldest_create_time_with_nothing_is_still_could_not_tell(monkeypatch):
    import catalog_search_handler as cs

    class FakeCE:
        def find_root_elements(self, body=None, output_format=None):
            return NO

    monkeypatch.setattr(cs, "_classification_explorer", lambda *a: FakeCE())
    monkeypatch.setattr(cs, "request_identity", lambda u, p: None)
    import json
    assert json.loads(cs.oldest_create_time(url=None, server=None, user_id=None).body) == {"createTime": None}
