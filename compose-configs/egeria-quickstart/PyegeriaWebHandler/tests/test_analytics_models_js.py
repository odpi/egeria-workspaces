"""Models and Runs in type-explorer.html: the pure helpers and hook-free tables (inside e64-pure), run under node
with test_e64_cards_js's stub React. Rows are shaped like analytics_models_handler.py's (tests/test_analytics_models.py
pins those against the handler). Skipped when node is not installed.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_e64_cards_js import HTML, _DIR, _run  # noqa: E402


def _render(component, props):
    return _run(f"var t = render(React.createElement({component}, {json.dumps(props)}));"
                "out({ text: text(t), keys: rows(t).map(function(r) { return r.p['data-row-key']; }), "
                "      cells: rows(t).map(function(r) { return all(r, 'td').map(text); }) });")


def _run_row(rel, guid, name, start="", status="", last="", has=False, end=""):
    return {"relationshipGuid": rel, "relationshipType": "ProcessHierarchy", "guid": guid, "typeName": "AnalyticsModelRun",
            "displayName": name, "qualifiedName": "", "activityStatus": status, "startTime": start, "completionTime": end,
            "lastRunStatus": last, "hasRunMetrics": has}


# ── runs of a model: 0, 1, many ──────────────────────────────────────────────────────────────────────────

def test_zero_runs_read_say_none_in_words():
    r = _render("ModelRunsTable", {"rows": [], "st": {"state": "none"}})
    assert r["keys"] == [] and r["text"] == "No runs are linked to this model."


def test_zero_runs_not_read_say_not_read():
    r = _render("ModelRunsTable", {"rows": [], "st": {"state": "not-read"}})
    assert "Not read" in r["text"] and "No runs" not in r["text"]


def test_one_run():
    r = _render("ModelRunsTable", {"rows": [_run_row("ph-1", "r-1", "Run 1", start="2026-11-20T10:00:00Z", status="COMPLETED",
                                                     last="COMPLETE", has=True)], "st": {"state": "read"}})
    assert r["keys"] == ["ph-1"]
    assert r["cells"][0][0].startswith("Run 1") and r["cells"][0][1] == "COMPLETED"
    assert r["cells"][0][2] == "20 Nov 2026 10:00 UTC" and r["cells"][0][4] == "COMPLETE"


def test_many_runs_with_missing_dates_and_no_metrics_said_in_words():
    rows = [_run_row("ph-2", "r-2", "new", start="2026-11-20T10:00:00Z", end="2026-11-20T10:05:00Z"),
            _run_row("ph-1", "r-1", "unstarted"),
            _run_row("ph-3", "r-3", "odd", start="last tuesday", has=True)]
    r = _render("ModelRunsTable", {"rows": rows, "st": {"state": "read"}})
    assert r["keys"] == ["ph-2", "ph-1", "ph-3"]                      # the backend's order is kept
    assert r["cells"][1][2] == "start not recorded" and r["cells"][1][1] == "not recorded"
    assert r["cells"][1][4] == "no run metrics"                       # a run with no RunMetrics says so
    assert r["cells"][2][2] == "not readable: last tuesday"
    assert r["cells"][2][4] == "not recorded"                         # has RunMetrics, no lastRunStatus in it


# ── run metrics ──────────────────────────────────────────────────────────────────────────────────────────

def test_a_run_with_no_metrics_says_so_never_zero():
    r = _render("RunMetricsPanel", {"metrics": {"state": "none"}, "noun": "run"})
    assert r["text"] == "No run metrics are recorded for this run." and "0" not in r["text"]


def test_metrics_before_6_2_and_unknown_version_words():
    words = "Run metrics need Egeria 6.2 (the RunMetrics classification): the platform at x runs Egeria 6.1."
    assert _render("RunMetricsPanel", {"metrics": {"state": "needs-6.2", "words": words}, "noun": "run"})["text"] == words
    t = _render("RunMetricsPanel", {"metrics": {"state": "not-known"}, "noun": "model"})["text"]
    assert t.startswith("No run metrics are recorded for this model.") and "could not be read" in t


def test_metrics_table_unrecorded_values_say_not_recorded_and_zero_stays_zero():
    m = {"state": "read", "values": {"runCount": 1200, "failedRunCount": 0, "lastRunDuration": 61000,
                                     "totalBytesRead": 2048, "lastRunStartTime": "2026-11-20T10:00:00Z"},
         "additionalProperties": {"engine": "spark"}}
    r = _render("RunMetricsPanel", {"metrics": m, "noun": "model"})
    cells = {c[0]: c[1] for c in r["cells"]}
    assert cells["Runs recorded"] == "1,200" and cells["Failed runs"] == "0"
    assert cells["Last run duration"] == "1 min 1 s" and cells["Total bytes read"] == "2.0 KB"
    assert cells["Total rows read"] == "not recorded" and cells["Last run status"] == "not recorded"
    assert cells["engine"] == "spark"


# ── a run's own dates ────────────────────────────────────────────────────────────────────────────────────

def test_run_dates_missing_and_duration():
    r = _render("ModelRunDatesPanel", {"detail": {"startTime": "2026-11-20T10:00:00Z", "completionTime": "2026-11-20T11:30:00Z"}})
    cells = {c[0]: c[1] for c in r["cells"]}
    assert cells["Requested"] == "not recorded" and cells["Duration"] == "1 h 30 min"
    r = _render("ModelRunDatesPanel", {"detail": {"startTime": "2026-11-20T10:00:00Z", "completionTime": ""}})
    cells = {c[0]: c[1] for c in r["cells"]}
    assert cells["Completed"] == "not recorded" and cells["Duration"] == "not known: no readable completion time"
    cells = {c[0]: c[1] for c in _render("ModelRunDatesPanel", {"detail": {}})["cells"]}
    assert cells["Started"] == "not recorded" and cells["Duration"] == "not known: no readable start time"


# ── model of a run, projects, sources, list subtitles ────────────────────────────────────────────────────

def test_run_with_no_model_says_so():
    assert _render("RunModelsTable", {"rows": [], "st": {"state": "none"}})["text"] == "No model is linked to this run."


def test_projects_experiment_and_needs_6_4():
    rows = [{"relationshipGuid": "pt-2", "guid": "p-2", "typeName": "Project", "displayName": "Churn experiment",
             "isExperiment": True, "hypothesis": "Tenure predicts churn", "relationshipType": "ProjectTarget"},
            {"relationshipGuid": "pt-3", "guid": "p-3", "typeName": "Project", "displayName": "Bare experiment",
             "isExperiment": True, "hypothesis": "", "relationshipType": "ProjectTarget"},
            {"relationshipGuid": "pt-1", "guid": "p-1", "typeName": "Project", "displayName": "Plain",
             "isExperiment": False, "hypothesis": "", "relationshipType": "ResourceList"}]
    r = _render("ModelProjectsTable", {"rows": rows, "st": {"state": "read"}})
    assert r["keys"] == ["pt-2", "pt-3", "pt-1"]
    assert r["cells"][0][1] == "Experiment" and r["cells"][0][2] == "Tenure predicts churn"
    assert r["cells"][1][2] == "no hypothesis recorded" and r["cells"][2][1] == "Project"
    w = "The project list needs Egeria 6.4 (odpi/egeria#9463 ...): the platform at x runs Egeria 6.3."
    assert "needs Egeria 6.4" in _render("ModelProjectsTable", {"rows": [], "st": {"state": "needs-6.4", "words": w}})["text"]
    assert _render("ModelProjectsTable", {"rows": [], "st": {"state": "none"}})["text"] == "No projects or experiments are linked."


def test_sources_url_or_words():
    rows = [{"relationshipGuid": "e-1", "guid": "s-1", "typeName": "ExternalModelSource", "displayName": "Card", "url": "", "organization": ""}]
    r = _render("ModelSourcesTable", {"rows": rows, "st": {"state": "read"}})
    assert r["cells"][0][1] == "no URL recorded"


def test_list_subtitles():
    out = _run("out([modelListSubtitle({ implementationLanguage: 'Python', versionIdentifier: '3' }), modelListSubtitle({}),"
               " modelRunListSubtitle({ activityStatus: 'COMPLETED', startTime: '2026-11-20T10:00:00Z' }),"
               " modelRunListSubtitle({}), modelRunListSubtitle({ startTime: 'garbage' })]);")
    assert out == ["Python · version 3", "", "COMPLETED · started 20 Nov 2026", "start not recorded", "start not readable"]


# ── wiring (the pyegeria-spa-add-tab checks) ─────────────────────────────────────────────────────────────

def test_models_section_is_wired():
    assert "'analytics-models': 'Models and Runs'," in HTML                         # SECTION_LABELS
    assert "section: 'analytics-models'," in HTML                                   # home-page card
    assert "{ id: 'analytics-models'," in HTML                                      # nav menu
    assert "section === 'analytics-models'\n      ? React.createElement(AnalyticsModelsView" in HTML   # render switch
    assert HTML.count("'data-values','analytics-models'") == 2                      # valid hashes + isActive
    assert "onNavigateToAnalyticsModel(guid, 'models'); return; }" in HTML           # dispatcher
    assert "onNavigateToAnalyticsModel(guid, 'runs'); return; }" in HTML
    assert "onNavigateToDataValue, onNavigateToAnalyticsModel]);" in HTML           # dispatcher deps
    assert "if (item.typeName === 'DeployedAnalyticsModel' || superTypes.indexOf('DeployedAnalyticsModel') !== -1) return true;" in HTML
    assert "if (item.typeName === 'AnalyticsModelRun' || superTypes.indexOf('AnalyticsModelRun') !== -1) return true;" in HTML
    assert "'DeployedAnalyticsModel': { color:" in HTML and "'AnalyticsModelRun': { color:" in HTML   # DD_TYPE_NAV
    assert "d.needs64 || d.needsVersion" in HTML                                    # before-5.2 words, not an empty list


def test_type_nav_map_routes_models_and_runs():
    m = json.loads((_DIR / "static" / "type-nav-map.json").read_text())
    assert m["DeployedAnalyticsModel"]["explorerHash"] == "analytics-models" and m["DeployedAnalyticsModel"]["kind"] == "models"
    assert m["DeployedAnalyticsModel"]["catalogSection"] == "processes"             # The Catalog keeps its own card
    assert m["AnalyticsModelRun"] == {"explorerHash": "analytics-models", "kind": "runs"}


def test_lists_and_panes_are_resizable():
    # the list pane is E64ElementsView (useResizable + ResizeDivider); every table is E64Table (a plain <table>
    # that egeria-resize.js makes column-resizable)
    assert "sideKey: 'AnalyticsModelsView.sideW'" in HTML and "sideKey: 'AnalyticsModelRunsView.sideW'" in HTML
    block = HTML[HTML.index("// ── Models and Runs: DeployedAnalyticsModel"):HTML.index("/* e64-pure:end */")]
    assert block.count("React.createElement(E64Table") == 6   # metrics, dates, runs, model, projects, sources and "'table'" not in block
