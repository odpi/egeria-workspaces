"""The absence rule for the 14 Egeria 6.4 relationship lists, via RELATIONSHIP_FIELDS.

Egeria leaves an empty relationship list out of its answer, so an absent list can mean "none" only when it
was asked for. One that wasn't asked for is "not read", on a platform without 6.4 it is "needs Egeria 6.4",
and when the platform's version is not known it is "not known". It is never "none" in those cases.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402

import egeria_6_4_support as e64  # noqa: E402

FIXTURE = json.loads((Path(__file__).resolve().parent / "fixtures" / "egeria_6_4_relationship_fields.json").read_text())
ROWS = FIXTURE["egeria_6_4_rows"]


def test_the_14_lists_match_pyegerias_generated_table():
    assert len(ROWS) == 14
    assert {k: (v,) for k, v in e64.E64_LISTS.items()} == {k: tuple(v) for k, v in ROWS.items()}


def test_installed_relationship_fields_agree_once_they_carry_the_lists():
    from pyegeria.view.egeria_relationship_fields import RELATIONSHIP_FIELDS
    for key, rel_types in ROWS.items():
        if key in RELATIONSHIP_FIELDS:            # a pyegeria generated from 6.4
            assert tuple(RELATIONSHIP_FIELDS[key]) == tuple(rel_types)
    fields = e64.relationship_fields()
    assert set(ROWS) <= set(fields)
    assert set(RELATIONSHIP_FIELDS) <= set(fields)     # nothing of the installed table is lost


REQUESTED = e64.relationship_fields()      # a graph read asks for every list
INPUT = {"relationshipHeader": {"guid": "as-1"}, "relatedElement": {"elementHeader": {"guid": "t-1"}}}


@pytest.mark.parametrize("key", sorted(ROWS))
def test_requested_and_empty_is_none(key):
    assert e64.list_state({}, key, REQUESTED, True) == {"state": e64.NONE}
    assert e64.list_state({key: []}, key, REQUESTED, True) == {"state": e64.NONE}


@pytest.mark.parametrize("key", sorted(ROWS))
def test_not_requested_is_not_read_even_when_present(key):
    assert e64.list_state({}, key, set(), True) == {"state": e64.NOT_READ}
    assert e64.list_state({key: [INPUT]}, key, set(), True) == {"state": e64.NOT_READ}


@pytest.mark.parametrize("key", sorted(ROWS))
def test_requested_with_entries_is_read(key):
    assert e64.list_state({key: [INPUT]}, key, REQUESTED, True) == {"state": e64.READ}


@pytest.mark.parametrize("key", sorted(ROWS))
def test_before_6_4_an_absent_list_needs_6_4_never_none(key):
    st = e64.list_state({}, key, REQUESTED, False, "X needs Egeria 6.4 ...")
    assert st == {"state": e64.NEEDS_6_4, "words": "X needs Egeria 6.4 ..."}


@pytest.mark.parametrize("key", sorted(ROWS))
def test_unknown_version_and_absent_is_not_known_never_none(key):
    assert e64.list_state({}, key, REQUESTED, None) == {"state": e64.NOT_KNOWN}


def test_a_pre_6_4_list_absent_is_plain_none_whatever_the_gate_says():
    # knownLocations is not a 6.4 list: its absence on a read element is "none" on any platform
    assert e64.list_state({}, "knownLocations", REQUESTED, False) == {"state": e64.NONE}


def test_a_key_that_is_not_a_relationship_list_is_not_read():
    assert e64.list_state({"bogus": [INPUT]}, "bogus", set(REQUESTED) | {"bogus"}, True) == {"state": e64.NOT_READ}


def test_related_rows_keep_two_relationships_to_one_element_and_drop_a_repeat():
    entry = lambda rg, when: {"relationshipHeader": {"guid": rg, "type": {"typeName": "Assessment"}},
                              "relationshipProperties": {"class": "AssessmentProperties", "label": "L",
                                                         "assessmentTime": when},
                              "relatedElement": {"elementHeader": {"guid": "t-1", "type": {"typeName": "GlossaryTerm"}},
                                                 "properties": {"displayName": "Lineage"}}}
    el = {"inputsToDecision": [entry("as-1", "2026-01-01"), entry("as-2", "2026-02-01"), entry("as-1", "2026-01-01")]}
    rows = e64.related_rows(el, "inputsToDecision", ("label", "assessmentTime"))
    assert [r["relationshipGuid"] for r in rows] == ["as-1", "as-2"]
    assert {r["guid"] for r in rows} == {"t-1"}
    assert rows[1]["assessmentTime"] == "2026-02-01"


def test_branch_is_read_from_other_classifications():
    el = {"elementHeader": {"otherClassifications": [
        {"class": "ElementClassification", "classificationName": "Branch",
         "classificationProperties": {"class": "BranchProperties", "displayName": "main", "purpose": "default branch",
                                      "url": "https://github.com/odpi/egeria/tree/main"}}]}}
    assert e64.branch_of(el) == {"displayName": "main", "scope": "", "purpose": "default branch",
                                 "url": "https://github.com/odpi/egeria/tree/main"}
    assert e64.branch_of({"elementHeader": {}}) is None
