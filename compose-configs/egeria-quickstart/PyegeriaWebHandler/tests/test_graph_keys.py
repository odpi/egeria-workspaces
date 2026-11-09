"""Diagram keys are found by shape (graph_keys.py), so Egeria's new graph kinds -- activityMermaidGraph and
whatever comes next -- reach the browser without a handler edit. Plus a guard that no route was lost."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402

import graph_keys as gk  # noqa: E402

HERE = Path(__file__).resolve().parent.parent

# The owner's 25 Egeria graph keys, plus the two spellings pyegeria also returns.
EGERIA_KEYS = [
    "mermaidGraph", "actionMermaidGraph", "activityMermaidGraph", "anchorMermaidGraph", "edgeMermaidGraph",
    "specificationMermaidGraph", "solutionBlueprintMermaidGraph", "solutionSubcomponentMermaidGraph",
    "informationSupplyChainMermaidGraph", "iscImplementationMermaidGraph", "iscDataMeshMermaidGraph",
    "iscSystemFabricMermaidGraph", "iscDataFabricMermaidGraph", "iscDataMappingMermaidGraph",
    "governanceActionProcessMermaidGraph", "organizationTreeMermaidGraph", "collectionMermaidMindMap",
    "zoneProfileMermaidPieChart", "zoneProfileAnchoredMermaidPieChart", "zoneProfileAllMermaidPieChart",
    "userAccountTypeProfileMermaidPieChart", "userAccountStatusProfileMermaidPieChart",
    "fieldLevelLineageGraph", "localLineageGraph", "fullLineageMermaidGraph", "iscimplementationMermaidGraph",
    "zoneProfileAllPieChart",
]


@pytest.mark.parametrize("key", EGERIA_KEYS)
def test_every_known_graph_key_is_recognised(key):
    assert gk.is_graph_key(key)


@pytest.mark.parametrize("key", ["displayName", "qualifiedName", "description", "status", "guid", "typeName", "class"])
def test_ordinary_fields_are_not_graph_keys(key):
    assert not gk.is_graph_key(key)


def test_a_brand_new_graph_kind_needs_no_code_change():
    assert gk.is_graph_key("someFutureMermaidGraph") and gk.is_graph_key("someFutureMermaidMindMap")
    assert gk.is_graph_key("someFutureMermaidPieChart") and gk.is_graph_key("someFutureLineageGraph")


def test_extract_keeps_real_diagrams_drops_empty_and_placeholders_and_orders_them():
    el = {"displayName": "x", "zebraMermaidGraph": "graph TD;z", "activityMermaidGraph": "graph TD;act",
          "mermaidGraph": "graph TD;ctx", "actionMermaidGraph": "graph TD;act2", "edgeMermaidGraph": "",
          "anchorMermaidGraph": "No anchored elements found", "localLineageGraph": "graph LR;l"}
    got = gk.extract_graph_fields(el)
    assert list(got) == ["mermaidGraph", "actionMermaidGraph", "activityMermaidGraph", "localLineageGraph", "zebraMermaidGraph"]
    assert "edgeMermaidGraph" not in got and "anchorMermaidGraph" not in got


def test_every_handler_extractor_now_passes_activity_through():
    el = {"mermaidGraph": "graph TD;c", "actionMermaidGraph": "graph TD;a", "activityMermaidGraph": "graph TD;v"}
    import isc_handler, solution_architect_handler, data_design_handler, business_capability_handler, digital_products_handler
    for fn in (isc_handler._extract_mermaid, solution_architect_handler._extract_mermaid_fields,
               data_design_handler._extract_mermaid_fields, business_capability_handler._extract_mermaid_fields,
               digital_products_handler._extract_mermaid_fields):
        assert set(fn(el)) == {"mermaidGraph", "actionMermaidGraph", "activityMermaidGraph"}, fn.__module__


def test_the_mermaid_route_returns_every_graph_the_element_carries(monkeypatch):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    import mermaid_handler as mh
    class Fake:
        def get_element_by_guid(self, guid, **kw):
            return {"mermaidGraph": "graph TD;c", "actionMermaidGraph": "graph TD;a", "activityMermaidGraph": "graph TD;v",
                    "brandNewMermaidMindMap": "mindmap\n root", "displayName": "x"}
    monkeypatch.setattr(mh, "_get_classifier", lambda *a, **k: Fake())
    app = FastAPI(); app.include_router(mh.router)
    d = TestClient(app).get("/api/mermaid/g1").json()
    assert d["mermaidGraph"] == "graph TD;c"
    assert list(d["graphs"]) == ["mermaidGraph", "actionMermaidGraph", "activityMermaidGraph", "brandNewMermaidMindMap"]


def test_the_governance_definition_detail_carries_action_and_activity_graphs():
    import governance_definitions_handler as gd
    src = (HERE / "governance_definitions_handler.py").read_text()
    assert "extract_graph_fields(element).items() if k != \"mermaidGraph\"" in src


# A truncated edit once dropped seven routes and every test passed: pin the route count of every handler this
# change touched (counts taken before the change).
@pytest.mark.parametrize("module,routes", [
    ("isc_handler", 2), ("solution_architect_handler", 10), ("data_design_handler", 10),
    ("business_capability_handler", 2), ("mermaid_handler", 2), ("tech_catalog_handler", 28),
    ("digital_products_handler", 6), ("governance_definitions_handler", 4),
])
def test_no_route_was_lost(module, routes):
    import importlib
    m = importlib.import_module(module)
    assert len([r for r in m.router.routes if getattr(r, "path", "")]) == routes


def test_spelling_variants_are_one_diagram_under_the_canonical_name():
    el = {"iscimplementationMermaidGraph": "graph TD;typo", "iscImplementationMermaidGraph": "graph TD;canon",
          "ACTIONMERMAIDGRAPH": "graph TD;a"}
    got = gk.extract_graph_fields(el)
    assert list(got) == ["actionMermaidGraph", "iscImplementationMermaidGraph"]          # one each, canonical spelling
    assert got["iscImplementationMermaidGraph"] == "graph TD;canon"                      # the canonical key wins its variant
    only_typo = gk.extract_graph_fields({"iscimplementationMermaidGraph": "graph TD;typo"})
    assert only_typo == {"iscImplementationMermaidGraph": "graph TD;typo"}               # a lone variant is renamed


def test_unknown_keys_keep_egerias_spelling_and_earlier_source_wins():
    assert list(gk.extract_graph_fields({"someFutureMermaidGraph": "g"})) == ["someFutureMermaidGraph"]
    assert gk.extract_graph_fields({"mermaidGraph": "first"}, {"mermaidGraph": "second"}) == {"mermaidGraph": "first"}


def test_collections_handler_reuses_the_shared_canonicalisation():
    src = (HERE / "collections_handler.py").read_text()
    assert 'k.lower() == "iscimplementationmermaidgraph"' not in src                  # the copy is gone
    import collections_handler as ch
    assert "iscImplementationMermaidGraph" in ch._extract_mermaid_fields({"iscimplementationMermaidGraph": "graph TD;x"})
