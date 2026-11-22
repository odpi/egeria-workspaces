"""Configuration Values (was Data Values) and Models and Runs moved from Egeria Explorer to The Catalog (2026-11-22).

Three things, in the style of the W1 tests (test_analytics_models.py):
  * the cards appear once, in The Catalog only (Explorer keeps no second copy; the list + detail frame they share
    with the Explorer's Decisions is in static/egeria-shared-ui.js, once);
  * an old Explorer link to either section (#data-values, ?section=..., ?guid=X&kind=runs#analytics-models,
    a favourite, a link from another app) is sent to The Catalog's section with its guid and kind;
  * the new name is used everywhere a person sees it.
The redirect and The Catalog's first-tab helpers run under node; skipped when node is not installed.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_e64_cards_js import CATALOG, HTML, SHARED, _DIR, _run  # noqa: E402

FRESH = _DIR.parent.parent / "egeria-freshstart" / "PyegeriaWebHandler"

MOVED = ["DataValueDetail", "DataValueValuePanel", "DATA_VALUES_VIEW_CFG", "ModelCardFrame", "AnalyticsModelDetail",
         "AnalyticsModelRunDetail", "ANALYTICS_MODELS_VIEW_CFG", "ANALYTICS_MODEL_RUNS_VIEW_CFG", "RunMetricsPanel",
         "ModelRunDatesPanel", "ModelRunsTable", "RunModelsTable", "ModelProjectsTable", "ModelSourcesTable",
         "ModelVariablesTable", "ModelSignatureTable", "ModelLineageTable", "MODEL_VARIABLES_NOTE", "modelListSubtitle",
         "modelRunListSubtitle"]


def _defs(src, name):
    return len(re.findall(r"^(?:function|var|const|let) " + re.escape(name) + r"\b", src, re.M))


# ── the cards appear once, in The Catalog only ──────────────────────────────────────────────────────────

@pytest.mark.parametrize("name", MOVED)
def test_each_moved_card_and_helper_is_defined_once_in_the_catalog_only(name):
    assert _defs(CATALOG, name) == 1, name
    assert _defs(HTML, name) == 0, name + " is still defined in type-explorer.html"
    assert _defs(SHARED, name) == 0, name
    for page in ("type-explorer.html", "tech-catalog.html"):
        p = FRESH / page
        if p.exists():
            assert _defs(p.read_text(), name) == 0, f"freshstart {page}: {name}"


def test_the_explorer_has_no_section_view_or_card_left_for_either():
    for gone in ("function DataValuesView", "function AnalyticsModelsView", "React.createElement(DataValueDetail",
                 "React.createElement(AnalyticsModelDetail", "onNavigateToDataValue", "onNavigateToAnalyticsModel",
                 "section === 'data-values'", "section === 'analytics-models'", "section: 'data-values',",
                 "section: 'analytics-models',", "{ id: 'data-values',", "{ id: 'analytics-models',",
                 "'data-values': 'Data Values'", "'analytics-models': 'Models and Runs'"):
        assert gone not in HTML, gone
    # neither is a section the Explorer opens any more: only the redirect table names them
    assert "'decisions','data-values'" not in HTML and "'decisions','analytics-models'" not in HTML
    block = _js_block(HTML, "moved-sections")
    for sid in ("'data-values'", "'analytics-models'"):
        assert HTML.count(sid) == block.count(sid) > 0, sid                    # only inside the redirect block


def test_the_list_and_detail_frame_is_shared_once():
    assert _defs(SHARED, "E64ElementsView") == 1 and _defs(SHARED, "_e64FetchJson") == 1
    assert _defs(HTML, "E64ElementsView") == 0 and _defs(CATALOG, "E64ElementsView") == 0
    assert _defs(HTML, "_e64FetchJson") == 0 and _defs(CATALOG, "_e64FetchJson") == 0
    assert "React.createElement(E64ElementsView, { cfg: DECISIONS_VIEW_CFG" in HTML      # Decisions stays in the Explorer
    assert "React.createElement(E64ElementsView, { key: currentTab.id, cfg: CATALOG_E64_TAB_CFG[currentTab.id]," in CATALOG
    frame = SHARED[SHARED.index("function E64ElementsView("):]
    assert "useResizable(" in frame and "ResizeDivider" in frame                         # the list pane stays resizable
    fresh = FRESH / "static" / "egeria-shared-ui.js"
    assert _defs(fresh.read_text(), "E64ElementsView") == 1                              # SHARE-3: both mirrors


def test_the_catalog_opens_each_section_on_its_tab():
    assert "'namespaces','data-values','analytics-models']);" in CATALOG                 # #hash cold load
    assert "'config-values': DATA_VALUES_VIEW_CFG," in CATALOG
    assert "'models': ANALYTICS_MODELS_VIEW_CFG," in CATALOG and "'runs': ANALYTICS_MODEL_RUNS_VIEW_CFG," in CATALOG
    assert "onNavigateToElement: navigateToElementFromCard" in CATALOG


# ── old Explorer links land on The Catalog ──────────────────────────────────────────────────────────────

def _js_block(src, tag):
    m = re.search(r"/\* " + tag + r":begin \*/(.*?)/\* " + tag + r":end \*/", src, re.S)
    assert m, tag
    return m.group(1)


def _node(js):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    r = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


@pytest.mark.parametrize("search,hash_,expect", [
    ("", "#data-values", "/tech-catalog#data-values"),
    ("?guid=dv-1", "#data-values", "/tech-catalog?guid=dv-1#data-values"),
    ("?section=data-values", "", "/tech-catalog#data-values"),
    ("?guid=dv-1", "#data-values?x=1", "/tech-catalog?guid=dv-1#data-values"),        # legacy #section?query
    ("", "#analytics-models", "/tech-catalog#analytics-models"),
    ("?guid=r-1&kind=runs", "#analytics-models", "/tech-catalog?guid=r-1&kind=runs#analytics-models"),   # a run favourite
    ("?guid=m-1&kind=models", "#analytics-models", "/tech-catalog?guid=m-1&kind=models#analytics-models"),
    ("?kind=runs", "#analytics-models", "/tech-catalog?kind=runs#analytics-models"),
    ("?section=analytics-models&kind=runs", "", "/tech-catalog?kind=runs#analytics-models"),
    ("?kind=<script>", "#analytics-models", "/tech-catalog#analytics-models"),          # only models/runs pass
    ("?guid=a%20b", "#data-values", "/tech-catalog?guid=a+b#data-values"),
    ("?guid=d-1", "#decisions", None),                                                  # Decisions stays
    ("", "", None),
    ("?section=glossary", "#glossary", None),
])
def test_an_old_explorer_link_is_sent_to_the_catalog(search, hash_, expect):
    got = _node(_js_block(HTML, "moved-sections") + f"console.log(JSON.stringify(explorerMovedSectionUrl({json.dumps(search)}, {json.dumps(hash_)})));")
    assert got == expect


def test_the_redirect_runs_before_the_explorer_renders_and_on_a_hash_change():
    i = HTML.index("/* moved-sections:end */")
    tail = HTML[i:i + 400]
    assert "window.location.replace(u)" in tail and "addEventListener('hashchange', go)" in tail
    assert i < HTML.index("\nfunction App(") < HTML.index("ReactDOM.createRoot")


@pytest.mark.parametrize("type_name,supers,expect", [
    ("DataValue", [], "/tech-catalog?guid=g-1#data-values"),
    ("LiteralDataValue", ["DataValue"], "/tech-catalog?guid=g-1#data-values"),
    ("DeployedAnalyticsModel", ["Asset"], "/tech-catalog?guid=g-1#analytics-models"),
    ("AnalyticsModelRun", ["Process", "Asset"], "/tech-catalog?guid=g-1&kind=runs#analytics-models"),
])
def test_explorer_cross_links_to_a_moved_type_open_the_catalog(type_name, supers, expect):
    got = _node(_js_block(HTML, "moved-sections")
                + f"console.log(JSON.stringify(catalogUrlForElement('g-1', {json.dumps(type_name)}, {json.dumps(supers)})));")
    assert got == expect
    # the Explorer's dispatcher still treats these types as linkable and opens them there
    assert "window.open(catalogUrlForElement(guid, typeName, superTypes), '_blank'); return;" in HTML


def test_the_catalog_opens_a_kind_runs_link_on_the_model_runs_tab():
    fn = CATALOG[CATALOG.index("function catalogInitialNavTarget("):CATALOG.index("\nfunction App(")]
    js = fn + ("console.log(JSON.stringify([catalogInitialNavTarget('?kind=runs', '#analytics-models'),"
               " catalogInitialNavTarget('?guid=r-1&kind=runs', '#analytics-models'),"
               " catalogInitialNavTarget('', '#analytics-models'), catalogInitialNavTarget('?kind=runs', '#data-values')]));")
    assert _node(js) == [{"section": "analytics-models", "tab": "runs"}, None, None, None]
    # a ?guid= is resolved through element-nav and the type-nav map, which also picks the tab
    m = json.loads((_DIR / "static" / "type-nav-map.json").read_text())
    for t, sec, tab in (("DataValue", "data-values", "config-values"), ("LiteralDataValue", "data-values", "config-values"),
                        ("DeployedAnalyticsModel", "analytics-models", "models"), ("AnalyticsModelRun", "analytics-models", "runs")):
        assert m[t] == {"catalogSection": sec, "catalogTab": tab}, t
        assert "explorerHash" not in m[t]             # so every other app's resolver sends these to The Catalog
    assert "if (entry.catalogSection) return { section: entry.catalogSection, tab: entry.catalogTab };" in CATALOG


def test_favourites_from_the_moved_cards_point_at_the_catalog():
    assert "app: 'tech-catalog', section: 'data-values'" in CATALOG
    assert "url: '/tech-catalog?guid=' + encodeURIComponent(detail.guid) + '#data-values'" in CATALOG
    assert "app: 'tech-catalog', section: 'analytics-models'" in CATALOG
    assert "'/tech-catalog?guid=' + encodeURIComponent(detail.guid) + '&kind=' + tab + '#analytics-models'" in CATALOG
    assert "/egeria-explorer?guid=' + encodeURIComponent(detail.guid) + '#data-values'" not in CATALOG + HTML


# ── the new name everywhere ─────────────────────────────────────────────────────────────────────────────

def test_configuration_values_is_the_name_a_person_sees():
    assert "{ id: 'data-values', icon: '◇', label: 'Configuration Values'," in CATALOG       # tile + nav button
    assert "{ id: 'config-values', label: 'Configuration Values', custom: true }" in CATALOG # tab / heading
    assert "noun: 'Configuration value', nounPlural: 'Configuration values', empty: 'No configuration values exist yet.'" in CATALOG
    assert "'Configures (processing variables)'" in CATALOG
    assert CATALOG.count("'Configuration values (processing variables)' + _modelCount(detail.variables, lists.variables)") == 2
    assert "emptyText: 'No configuration values are linked to this model.'" in CATALOG
    desc = re.search(r"\{ id: 'data-values', icon: '◇', label: 'Configuration Values', desc: '([^']*)' \}", CATALOG).group(1)
    for words in ("configure a process, model or run", "DataValue and LiteralDataValue", "ProcessingVariable",
                  "not the data in assets, Valid Metadata Values or Reference Data"):
        assert words in desc, words


@pytest.mark.parametrize("path", ["type-explorer.html", "tech-catalog.html", "e64_handler.py", "analytics_models_handler.py",
                                  "static/egeria-shared-ui.js"])
def test_the_old_name_is_not_shown_anywhere(path):
    src = (_DIR / path).read_text()
    shown = [m.group(0) for m in re.finditer(r"(['\"])[^'\"\n]*\bData [Vv]alues?\b[^'\"\n]*\1", src)
             if not src[src.rfind("\n", 0, m.start()) + 1:m.start()].lstrip().startswith(("//", "#", "*"))]
    assert shown == [], shown


def test_the_backend_version_words_use_the_new_name():
    src = (_DIR / "e64_handler.py").read_text()
    assert '"The Configuration Values list"' in src and '"The Configuration Value card"' in src


# ── PO-76: a ProcessingVariable link has one name, "Configuration values" ───────────────────────────────
# Every string a person can see says "configuration values"; "processing variables" appears only as the
# bracketed Egeria name after it, and "process variables" not at all.

_PV_FILES = ["type-explorer.html", "tech-catalog.html", "e64_handler.py", "analytics_models_handler.py",
             "egeria_6_4_support.py", "static/egeria-shared-ui.js"]


def _shown_strings(src):
    for m in re.finditer(r"(['\"])[^'\"\n]*\1", src):
        line = src[src.rfind("\n", 0, m.start()) + 1:m.start()].lstrip()
        if not line.startswith(("//", "#", "*")):
            yield m.group(0)


@pytest.mark.parametrize("path", [*_PV_FILES, "fresh:static/egeria-shared-ui.js"])
def test_po_76_no_process_variables_wording_on_screen(path):
    src = ((FRESH / path[6:]) if path.startswith("fresh:") else (_DIR / path)).read_text()
    bad = [s for s in _shown_strings(src)
           if re.search(r"\bprocess variables?\b", s, re.I)
           or re.search(r"(?<!\()\bprocessing variables?\b", s, re.I)]
    assert bad == [], bad


def test_po_76_the_6_4_panel_has_one_configuration_values_section():
    src = (_DIR / "e64_handler.py").read_text()
    block = src[src.index("_REVERSE_SECTIONS = ("):src.index("_REVERSE_REL_TYPES")]
    titles = re.findall(r'^    \("(\w+)", "([^"]+)", \($', block, re.M)
    assert titles == [("decisions", "Decisions"), ("projects", "Projects"), ("variables", "Configuration values")]
    assert '("processingVariables", "Configuration values (processing variables)"' in block
    assert '("providesDataValues", "Provides configuration values"' in block
    for root in (_DIR, FRESH):
        ui = (root / "static/egeria-shared-ui.js").read_text()
        assert "'Decisions, projects and configuration values'" in ui


def test_po_76_the_needs_6_4_words_name_configuration_values():
    sup = (_DIR / "egeria_6_4_support.py").read_text()
    assert "needs Egeria 6.4 (odpi/egeria#9463, configuration values and decisions)" in sup
    src = (_DIR / "e64_handler.py").read_text()
    assert src.count('"Decisions, project targets, configuration values and Branch"') == 2
    am = (_DIR / "analytics_models_handler.py").read_text()
    assert "\"The run's configuration values (processing variables)\"" in am


# ── PO-73: the 6.4 panel's "none of these" line joins with "or" ─────────────────────────────────────────

@pytest.mark.parametrize("titles,expect", [
    (["Decisions"], "None recorded: no decisions are linked to this element."),
    (["Decisions", "Projects"], "None recorded: no decisions or projects are linked to this element."),
    (["Decisions", "Projects", "Configuration values"],
     "None recorded: no decisions, projects or configuration values are linked to this element."),
])
def test_po_73_the_all_none_line_says_or(titles, expect):
    secs = [{"key": "k%d" % i, "title": t, "lists": [{"key": "l%d" % i, "label": t, "rows": [], "st": {"state": "none"}}]}
            for i, t in enumerate(titles)]
    data = {"guid": "g", "typeName": "GlossaryTerm", "carries": True, "branch": None, "sections": secs}
    got = _run(f"out(text(render(React.createElement(E64RelatedRows, {{ data: {json.dumps(data)} }}))));")
    assert got.strip() == expect
