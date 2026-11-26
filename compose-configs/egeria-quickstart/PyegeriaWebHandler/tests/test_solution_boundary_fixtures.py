"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Provenance of the Solution Boundary fixtures (Portal boundary view, Part C, amendment 1).

REAL SHAPE: the two P1a files are copied byte-identical from egeria-python tag v6.3.4 (commit 97dbd1692ca36be0787fbf6b9ae78772a3eb759d); their SHA-256 is pinned here.
SYNTHETIC: the boundary find list and the DesignModelBoundary mixed-type find are built ONLY from elements of those files; a test proves each element is a copy and
that the one changed element differs from its source in the typeName alone. Nothing real was captured for a find: the live quickstart platform has no SolutionBoundary.
"""
import hashlib
import json
from pathlib import Path

_FX = Path(__file__).resolve().parent / "fixtures"
SUFFIX = "5a8d6a12"
BLUEPRINT_FILE = f"solution_blueprint_nested_boundaries_real_shape_2026_11_25_{SUFFIX}.json"
BOUNDARY_FILE = f"solution_boundary_retrieve_real_shape_2026_11_25_{SUFFIX}.json"
FIND_FILE = f"solution_boundary_find_SYNTHETIC_from_{SUFFIX}_elements.json"
DMB_FILE = f"design_model_boundary_find_mixed_SYNTHETIC_from_{SUFFIX}_elements.json"
PINNED = {
    BLUEPRINT_FILE: "bd46f6ecfbee0e1a6cb3e964aa0497b08c79bfb22b95ff302c074fae1056c0d8",
    BOUNDARY_FILE: "6b6d73e61f5fe2618d7444d861fbd36d412246ba832c579a35419830ecad0dd8",
}


def load(name):
    return json.loads((_FX / name).read_text())


def test_the_real_shape_files_are_the_upstream_bytes():
    for name, digest in PINNED.items():
        assert hashlib.sha256((_FX / name).read_bytes()).hexdigest() == digest, name
    assert "97dbd1692ca36be0787fbf6b9ae78772a3eb759d" in (_FX / f"solution_boundary_real_shape_2026_11_25_{SUFFIX}.SOURCE.md").read_text()


def test_the_real_shape_files_carry_the_nesting_the_view_needs():
    outer = load(BOUNDARY_FILE)
    assert outer["elementHeader"]["type"]["typeName"] == "SolutionBoundary"
    inner = outer["collectionMembers"][0]
    assert inner["relatedElement"]["elementHeader"]["type"]["typeName"] == "SolutionBoundary" and inner["nestedElements"][0]["relatedElement"]["elementHeader"]["type"]["typeName"] == "SolutionActorRole"
    assert outer["memberOfCollections"][0]["relatedElement"]["elementHeader"]["type"]["typeName"] == "SolutionBlueprint"
    bp = load(BLUEPRINT_FILE)
    assert bp["elementHeader"]["type"]["typeName"] == "SolutionBlueprint" and bp["collectionMembers"] and bp["mermaidGraph"]


def test_the_synthetic_find_is_two_unmodified_elements_of_the_real_file():
    real = load(BOUNDARY_FILE)
    f = load(FIND_FILE)
    assert "SYNTHETIC" in f["_note"] and FIND_FILE.count("SYNTHETIC") == 1
    assert f["list"] == [real, real["collectionMembers"][0]["relatedElement"]]


def test_the_synthetic_dmb_find_changes_one_element_by_its_type_name_only():
    real = load(BOUNDARY_FILE)
    d = load(DMB_FILE)
    assert "SYNTHETIC" in d["_note"] and "typeName" in d["_note"] and "SYNTHETIC" in DMB_FILE
    sb, dm = d["list"]
    assert sb == real
    src = real["collectionMembers"][0]["relatedElement"]
    assert dm["elementHeader"]["type"]["typeName"] == "DesignModelBoundary" and dm["properties"]["typeName"] == "DesignModelBoundary"
    back = json.loads(json.dumps(dm))
    back["elementHeader"]["type"]["typeName"] = back["properties"]["typeName"] = "SolutionBoundary"
    assert back == src
    assert dm["elementHeader"]["guid"] != sb["elementHeader"]["guid"]


def test_no_fixture_carries_a_token_password_or_header():
    import re
    for name in (BLUEPRINT_FILE, BOUNDARY_FILE, FIND_FILE, DMB_FILE):
        text = (_FX / name).read_text()
        assert not re.search(r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}", text) and not re.search(r'"[^"]*(?:token|passw|secret|authoriz|cookie|bearer)[^"]*"\s*:', text, re.I), name


def test_the_empty_state_fixture_is_an_empty_list_labelled_synthetic():
    # live has no SolutionBoundary today: the routes and the view must handle this answer
    e = load("solution_boundary_find_SYNTHETIC_empty.json")
    assert e["list"] == [] and "SYNTHETIC" in e["_note"] and "SYNTHETIC" in "solution_boundary_find_SYNTHETIC_empty.json"
