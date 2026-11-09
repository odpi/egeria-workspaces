# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Which keys of an element are diagrams, found by shape, not by a fixed list.

Egeria keeps adding graph kinds (Egeria 6.3 split Action and Activity relationships out of `mermaidGraph`
into `actionMermaidGraph` and `activityMermaidGraph`), and a fixed allow-list in each handler silently
dropped every new one. A key is a diagram if it is a Mermaid or lineage graph of any kind:

    *MermaidGraph  *MermaidMindMap  *MermaidPieChart  *LineageGraph   (and the older *PieChart)

Matching is case-insensitive, so the 'iscimplementationMermaidGraph' spelling some Egeria calls return is
found too. The browser has the same rule (_isMermaidKey in static/egeria-shared-ui.js); keep them in step.
"""
from typing import Any, Dict, Iterable, List

# Shown first, in this order; everything else follows alphabetically.
PREFERRED_ORDER = ["mermaidGraph", "actionMermaidGraph", "activityMermaidGraph"]


def is_graph_key(key: str) -> bool:
    """True for a Mermaid / lineage diagram key: anything containing 'mermaid' (case-insensitive), or ending
    in graph, mindmap, piechart or chart. That covers *MermaidGraph, *MermaidMindMap, *MermaidPieChart and
    *LineageGraph (two lineage keys have no 'Mermaid' in them)."""
    if not isinstance(key, str):
        return False
    kl = key.lower()
    return "mermaid" in kl or kl.endswith(("graph", "mindmap", "piechart", "chart"))


def graph_value(value: Any) -> bool:
    """A usable diagram body: a non-empty string that is not Egeria's 'No ... found' placeholder."""
    return isinstance(value, str) and bool(value.strip()) and not value.lower().startswith("no ")


def order_graph_keys(keys: Iterable[str]) -> List[str]:
    ks = list(keys)
    rank = {k.lower(): i for i, k in enumerate(PREFERRED_ORDER)}
    return sorted(ks, key=lambda k: (rank.get(k.lower(), len(PREFERRED_ORDER)), k.lower()))


def extract_graph_fields(*sources: Dict[str, Any]) -> Dict[str, str]:
    """Every non-empty diagram field found at the top level of the given dicts (earlier sources win),
    in display order (context graph, action, activity, then the rest)."""
    found: Dict[str, str] = {}
    for src in sources:
        if not isinstance(src, dict):
            continue
        for k, v in src.items():
            if k not in found and is_graph_key(k) and graph_value(v):
                found[k] = v
    return {k: found[k] for k in order_graph_keys(found)}
