"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Type Explorer "area" (Egeria's documentation grouping 0–7): _derive_area,
_area_from_wiki, AREA_ANCHORS and AREA_NAMES in type_system_handler.

Dan reported Report showing as Area 6. The old anchor map invented "Area 6 —
Data Stores" and anchored DataStore/DataSet/DataFile there, so Report
(Report → DataSet) came out 6. In Egeria, Report is model 0239 (Area 2) and
Area 6 is Discovery Surveys and Analysis (SurveyReport 0603, Annotation 0610).

fixtures/entity_types_egeria_8de9572c4d.json holds every Egeria entity type's
name, superType and descriptionWiki, built from the egeria source (see its
_source note), so the expected area of each type is Egeria's own model number.
"""

import json
import re
from pathlib import Path

import pytest

import type_system_handler as h

_FIXTURE = json.loads(
    (Path(__file__).resolve().parent / "fixtures" / "entity_types_egeria_8de9572c4d.json").read_text()
)
TYPES = _FIXTURE["entityTypes"]
SUP = {t["name"]: t["superType"] for t in TYPES}
WIKI = {t["name"]: t["descriptionWiki"] for t in TYPES}


def _egeria_area(name: str) -> int:
    """The area Egeria itself gives the type: the types/<area>/ directory of its
    wiki page, which matches the model number's second digit (0239 → 2)."""
    m = re.search(r"/types/(\d)/(?:0(\d)\d\d-)?", WIKI[name])
    if m.group(2) is not None:
        assert m.group(2) == m.group(1), f"{name}: wiki directory and model disagree"
    return int(m.group(1))


def _with_wiki(name: str) -> int:
    return h._derive_area(name, SUP, {}, WIKI)


def _anchors_only(name: str) -> int:
    """The fallback path: no descriptionWiki anywhere, anchors + supertypes only."""
    return h._derive_area(name, SUP, {})


# ── The reported bug ──────────────────────────────────────────────────────────

@pytest.mark.parametrize("derive", [_with_wiki, _anchors_only], ids=["wiki", "anchors"])
def test_report_is_area_2(derive):
    assert WIKI["Report"].endswith("/types/2/0239-Reports/")
    assert derive("Report") == 2


@pytest.mark.parametrize("derive", [_with_wiki, _anchors_only], ids=["wiki", "anchors"])
@pytest.mark.parametrize("name", ["DataStore", "DataSet", "DataFile", "DataFeed", "CSVFile"])
def test_data_stores_and_sets_are_area_2(derive, name):
    assert derive(name) == 2


@pytest.mark.parametrize("derive", [_with_wiki, _anchors_only], ids=["wiki", "anchors"])
@pytest.mark.parametrize("name", ["SurveyReport", "Annotation", "AnnotationReview",
                                  "ResourceProfileAnnotation", "SchemaAnalysisAnnotation"])
def test_discovery_types_are_area_6(derive, name):
    assert derive(name) == 6


def test_area_6_is_discovery_not_data_stores():
    assert h.AREA_NAMES[6] == "Discovery Surveys and Analysis"
    assert "Data Stores" not in h.AREA_NAMES.values()


# ── A sample from every area ──────────────────────────────────────────────────

SAMPLES = {
    0: ["Referenceable", "Asset", "Process", "Endpoint", "SoftwareCapability", "Collection"],
    1: ["Person", "Team", "UserIdentity", "Comment", "Project", "ToDo"],
    2: ["Report", "Connection", "Database", "Port", "DeployedConnector", "DataFolder"],
    3: ["Glossary", "GlossaryTerm"],
    4: ["GovernancePolicy", "IncidentReport", "EngineAction", "GovernanceRole",
        "IntegrationConnector", "ConnectorActivityReport", "SubjectArea"],
    5: ["SchemaElement", "SchemaAttribute", "DataField", "ValidValueDefinition", "DesignModel"],
    6: ["SurveyReport", "Annotation"],
    7: ["InformationSupplyChain", "SolutionComponent", "SolutionBlueprint",
        "DigitalProduct", "Agreement", "SavedQuery"],
}


@pytest.mark.parametrize("derive", [_with_wiki, _anchors_only], ids=["wiki", "anchors"])
@pytest.mark.parametrize("area,name", [(a, n) for a, ns in SAMPLES.items() for n in ns])
def test_sample_from_every_area(derive, area, name):
    assert _egeria_area(name) == area, "sample table disagrees with Egeria's model number"
    assert derive(name) == area


def test_samples_cover_every_area():
    assert set(SAMPLES) == set(range(8)) == set(h.AREA_NAMES)


# ── The whole Egeria type system ──────────────────────────────────────────────

def test_wiki_path_matches_egeria_for_every_entity_type():
    cache: dict = {}
    wrong = {n: h._derive_area(n, SUP, cache, WIKI) for n in SUP}
    wrong = {n: a for n, a in wrong.items() if a != _egeria_area(n)}
    assert wrong == {}


def test_anchor_fallback_matches_egeria_for_every_entity_type():
    """Without descriptionWiki the supertype walk alone still lands every one of
    Egeria's entity types in its documented area."""
    cache: dict = {}
    wrong = {n: h._derive_area(n, SUP, cache) for n in SUP}
    wrong = {n: (a, _egeria_area(n)) for n, a in wrong.items() if a != _egeria_area(n)}
    assert wrong == {}


def test_every_anchor_is_an_egeria_entity_type_in_its_own_area():
    """No invented anchors: each is a real entity type, at Egeria's area for it."""
    not_types = sorted(set(h.AREA_ANCHORS) - set(SUP))
    assert not_types == []
    wrong = {n: (a, _egeria_area(n)) for n, a in h.AREA_ANCHORS.items() if a != _egeria_area(n)}
    assert wrong == {}


# ── Wiki parsing and fallbacks ────────────────────────────────────────────────

@pytest.mark.parametrize("wiki,expected", [
    ("https://egeria-project.org/types/2/0239-Reports/", 2),
    ("https://egeria-project.org/types/6/0603-Survey-Reports/", 6),
    ("https://egeria-project.org/types/0/0010-Base-Model/", 0),
    ("https://egeria-project.org/types/1/", 1),        # TeamLeader, TeamMember
    ("", None),
    (None, None),
    ("https://egeria-project.org/concepts/asset/", None),
])
def test_area_from_wiki(wiki, expected):
    assert h._area_from_wiki(wiki) == expected


def test_extension_type_without_wiki_inherits_parents_wiki_area():
    """A custom subtype with no wiki of its own takes its parent's documented area."""
    sup = {"MyCustomReport": "Report", "Report": "DataSet"}
    wiki = {"Report": WIKI["Report"]}
    assert h._derive_area("MyCustomReport", sup, {}, wiki) == 2


def test_unknown_root_without_wiki_or_anchor_is_area_0():
    assert h._derive_area("Orphan", {"Orphan": None}, {}) == 0
