"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

The boundary fixture capture script (P1): its member walk and its stop rules, on SYNTHETIC answers only (no platform, no network).
"""
import argparse
import asyncio
import json

import pytest

import capture_boundary_fixtures as cap


def el(guid, tname, name=""):
    return {"elementHeader": {"guid": guid, "type": {"typeName": tname}}, "properties": {"displayName": name or guid}}


def member(related, nested=None, side=None):
    return {"relatedElement": related, **({"nestedElements": nested} if nested else {}), **({"sideLinks": side} if side else {})}


def boundary(guid, members=None, member_of=None):
    d = el(guid, "SolutionBoundary")
    if members:
        d["collectionMembers"] = members
    if member_of:
        d["memberOfCollections"] = [{"relatedElement": m} for m in member_of]
    return d


OUTER, INNER, LEAF = "outer", "inner", "leaf"


def test_real_nesting_is_found_with_its_depth():
    d = boundary(OUTER, [member(el("c1", "SolutionComponent")), member(el(INNER, "SolutionBoundary"), nested=[member(el("r1", "SolutionActorRole"), side=[member(el(INNER, "SolutionBoundary"))]),
                                                                                                         member(el("deep", "SolutionBoundary"), nested=[member(el("c2", "SolutionComponent"))])])])
    assert cap.nested_boundaries(d) == {INNER: 1, "deep": 2}
    assert cap.other_elements(d) == {"c1", INNER, "r1", "deep", "c2"}


def test_an_inner_boundary_with_only_a_parent_is_not_nested():
    # the inner boundary is seen from below: its parent is in sideLinks and in memberOfCollections, never in collectionMembers
    d = boundary(INNER, [member(el("c1", "SolutionComponent"), side=[member(el(OUTER, "SolutionBoundary"))])], member_of=[el(OUTER, "SolutionBoundary")])
    d["sideLinks"] = [member(el(OUTER, "SolutionBoundary"))]
    assert cap.nested_boundaries(d) == {} and cap.other_elements(d) == {"c1"}


def test_a_boundary_that_contains_itself_is_not_followed_again():
    d = boundary(OUTER, [member(el(INNER, "SolutionBoundary"), nested=[member(el(OUTER, "SolutionBoundary"), nested=[member(el(INNER, "SolutionBoundary"))])])])
    assert cap.nested_boundaries(d) == {INNER: 1}


def test_malformed_members_are_skipped():
    d = boundary(OUTER)
    d["collectionMembers"] = [None, {"relatedElement": None}, {"nothing": 1}, member(el("c1", "SolutionComponent"), nested="oops")]
    assert cap.other_elements(d) == {"c1"} and cap.nested_boundaries(d) == {}


class FakeSA:
    def __init__(self, details, blueprints=()):
        self.details, self.blueprints = details, list(blueprints)

    async def _async_find_solution_boundaries(self, *a, **k):
        return [self.details[g] for g in self.details]

    async def _async_get_solution_boundary_by_guid(self, guid, **k):
        return self.details[guid]

    async def _async_find_solution_blueprints(self, *a, **k):
        return self.blueprints

    async def _async_get_solution_blueprint_by_guid(self, guid, **k):
        return next(b for b in self.blueprints if cap.guid_of(b) == guid)


class FakeCM:
    async def _async_find_collections(self, *a, **k):
        return [el("x", "DesignModelBoundary"), el(INNER, "SolutionBoundary")]


ARGS = argparse.Namespace(depth=8)


def run(sa):
    log: list = []
    return asyncio.run(cap.capture(ARGS, sa, FakeCM(), log)), log


def test_an_inner_boundary_with_only_a_parent_stops_with_exit_3():
    inner = boundary(INNER, [member(el("c1", "SolutionComponent"), side=[member(el(OUTER, "SolutionBoundary"))])], member_of=[el(OUTER, "SolutionBoundary")])
    report, log = run(FakeSA({INNER: inner}))
    assert report["stop"] == cap.EXIT_NO_NESTING and "fixtures" not in report
    assert all("_async_find_" in c or "_async_get_" in c for c in log)


def test_real_nesting_passes_the_exit_3_check_and_the_note_names_the_nested_guids_and_depths():
    outer = boundary(OUTER, [member(el(INNER, "SolutionBoundary"), nested=[member(el("c1", "SolutionComponent"))])])
    bp = el("bp1", "SolutionBlueprint")
    bp["memberOfCollections"] = [{"relatedElement": el(OUTER, "SolutionBoundary")}]
    report, _ = run(FakeSA({OUTER: outer}, [bp]))
    assert "stop" not in report and report["best"]["guid"] == OUTER
    assert f"{{'{INNER}': 1}}" in report["fixtures"]["solution_boundary_by_guid_nested"]["calls"]


def test_no_blueprint_in_a_boundary_stops_with_exit_4():
    outer = boundary(OUTER, [member(el(INNER, "SolutionBoundary"), nested=[member(el("c1", "SolutionComponent"))])])
    report, _ = run(FakeSA({OUTER: outer}, [el("bp1", "SolutionBlueprint")]))
    assert report["stop"] == cap.EXIT_NO_BLUEPRINT


def test_only_find_and_get_calls_are_allowed_and_secrets_are_scrubbed():
    assert all(n.startswith(("_async_find_", "_async_get_")) for n in cap.ALLOWED_CALLS)
    with pytest.raises(SystemExit):
        asyncio.run(cap.ReadOnlyCalls(FakeSA({}), []).call("_async_anything_else"))
    n: dict = {}
    s = cap.scrub({"a": {"accessToken": "x", "k": "eyJabcdefgh.abcdefgh12.sig"}}, n)
    assert s == {"a": {"k": "<scrubbed>"}} and n == {"keys": 1, "strings": 1}
    with pytest.raises(SystemExit):
        cap.assert_clean(json.dumps({"bearerToken": "x"}), "t")
