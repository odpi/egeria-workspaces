"""The browser's side of the same rule (static/egeria-shared-ui.js), run under node. Standalone; skipped when
node is not installed (the Portal container has none)."""
import json, re, shutil, subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
UI = (ROOT / "static" / "egeria-shared-ui.js").read_text()
TE = (ROOT / "type-explorer.html").read_text()


def _node(expr, keys):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    grab = lambda pat: re.search(pat, UI, re.S).group(0)
    js = "\n".join([
        grab(r"var _MERMAID_FIELD_LABELS = \{.*?\n\};"),
        grab(r"function _isMermaidKey\(k\) \{.*?\n\}"),
        grab(r"var _GRAPH_PREFERRED_ORDER = [^\n]*;"),
        grab(r"function _graphKeysOrdered\(keys\) \{.*?\n\}"),
        grab(r"function _mermaidLabel\(k\) \{.*?\n\}"),
        f"console.log(JSON.stringify({expr}));",
    ]).replace("KEYS", json.dumps(keys))
    out = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_is_mermaid_key_covers_the_four_families():
    keys = ["mermaidGraph", "activityMermaidGraph", "collectionMermaidMindMap", "zoneProfileMermaidPieChart",
            "localLineageGraph", "fieldLevelLineageGraph", "someFutureMermaidGraph", "displayName", "description"]
    assert _node("KEYS.map(_isMermaidKey)", keys) == [True] * 7 + [False, False]


def test_order_is_context_then_action_then_activity_then_the_rest():
    keys = ["zoneProfileMermaidPieChart", "activityMermaidGraph", "edgeMermaidGraph", "mermaidGraph", "actionMermaidGraph"]
    assert _node("_graphKeysOrdered(KEYS)", keys) == ["mermaidGraph", "actionMermaidGraph", "activityMermaidGraph",
                                                       "edgeMermaidGraph", "zoneProfileMermaidPieChart"]


def test_activity_graph_has_a_label():
    assert _node("_mermaidLabel('activityMermaidGraph')", []) == "Activity Graph"
    assert _node("_mermaidLabel('someFutureMermaidMindMap')", []) == "Some Future Mind Map"


def test_diagrams_are_one_chip_bar_not_a_stack_of_buttons():
    assert "function GraphTabs({ graphs, extra, initial })" in UI
    assert "React.createElement(GraphTabs, { graphs: graphs })" in UI               # AvailableMermaidDiagrams
    assert "role: 'tablist'" in UI and "'aria-selected'" in UI
    assert "useState(initial || null)" in UI                                        # nothing renders until a chip is chosen


def test_the_context_section_fetches_all_graphs_once_and_does_not_double_list():
    assert "/api/mermaid/' + encodeURIComponent(guid), creds" in UI
    assert "data && typeof data[k] === 'string' && data[k].trim()" in UI             # not listed twice beside the pane's own


def test_views_that_showed_only_mermaidGraph_now_offer_the_other_diagrams():
    assert TE.count("AvailableMermaidDiagrams, { data: src, skip: new Set(['mermaidGraph']) }") == 4
    assert "_ALL_JS_MERMAID_FIELDS" not in TE and "_ALL_MERMAID_FIELDS" not in (ROOT / "tech-catalog.html").read_text()
