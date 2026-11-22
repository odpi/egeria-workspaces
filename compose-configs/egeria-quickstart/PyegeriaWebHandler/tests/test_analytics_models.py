"""Models and Runs (analytics_models_handler: /api/analytics-models[/{guid}], /api/analytics-model-runs[/{guid}]).

No live server, and laz holds no model data: ClassificationExplorer is replaced by tests/e64_fixtures.FakeExplorer.
Shapes follow Egeria 90232870b2: RunMetrics is a header classification (ElementHeader.runMetrics, RunMetricsProperties);
Experiment is a Project classification with `hypothesis`; each relationship list is RelatedMetadataElementSummary.
"""
import inspect
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pytest  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import analytics_models_handler as h  # noqa: E402
import egeria_6_4_support as e64  # noqa: E402
from e64_fixtures import ABOUT_6_3, ABOUT_6_4, FakeExplorer, client_error, rel  # noqa: E402

ABOUT_6_1 = {"version": "6.1", "time": "2026-06-01T12:00:00Z"}

METRICS = {"class": "RunMetricsProperties", "runCount": 12, "failedRunCount": 0, "lastRunStatus": "COMPLETE",
           "lastRunDuration": 61000, "lastRunStartTime": "2026-11-20T10:00:00.000+00:00"}


def _hdr(guid, type_name, supers, run_metrics=None, other=None):
    h_ = {"guid": guid, "status": "ACTIVE", "type": {"typeName": type_name, "superTypeNames": supers}}
    if run_metrics is not None:
        h_["runMetrics"] = {"class": "ElementClassification", "classificationName": "RunMetrics",
                            "classificationProperties": run_metrics}
    if other:
        h_["otherClassifications"] = other
    return h_


MODEL_SUPERS = ["DeployedSoftwareComponent", "Process", "Asset", "Referenceable", "OpenMetadataRoot"]
RUN_SUPERS = ["TransientEmbeddedProcess", "EmbeddedProcess", "Process", "Asset", "Referenceable", "OpenMetadataRoot"]


def run_rel(rel_guid, run_guid, name, start="", status="", metrics=None, rel_type="ProcessHierarchy"):
    r = rel(rel_type, rel_guid, run_guid, el_type="AnalyticsModelRun", super_types=RUN_SUPERS,
            el_props={"displayName": name, **({"startTime": start} if start else {}),
                      **({"activityStatus": status} if status else {})})
    if metrics is not None:
        r["relatedElement"]["elementHeader"]["runMetrics"] = {"classificationName": "RunMetrics",
                                                              "classificationProperties": metrics}
    return r


def project_rel(rel_guid, guid, name, hypothesis=None, rel_type="ProjectTarget"):
    r = rel(rel_type, rel_guid, guid, el_type="Project", el_props={"displayName": name})
    if hypothesis is not None:
        r["relatedElement"]["elementHeader"]["projectClassification"] = [
            {"classificationName": "Experiment", "classificationProperties": {"hypothesis": hypothesis}}]
    return r


def model(guid="m-1", runs=None, metrics=None, extra=None, props=None):
    el = {"class": "OpenMetadataRootElement", "elementHeader": _hdr(guid, "DeployedAnalyticsModel", MODEL_SUPERS, metrics),
          "properties": {"class": "DeployedAnalyticsModelProperties", "qualifiedName": f"Model::{guid}",
                         "displayName": "Churn predictor", "implementationLanguage": "Python",
                         "versionIdentifier": "3", **(props or {})}}
    if runs is not None:
        el["childProcesses"] = runs
    el.update(extra or {})
    return el


def run(guid="r-1", models=None, metrics=None, props=None, extra=None):
    el = {"class": "OpenMetadataRootElement", "elementHeader": _hdr(guid, "AnalyticsModelRun", RUN_SUPERS, metrics),
          "properties": {"class": "AnalyticsModelRunProperties", "qualifiedName": f"Run::{guid}",
                         "displayName": "Churn run 7", **(props or {})}}
    if models is not None:
        el["parentProcesses"] = models
    el.update(extra or {})
    return el


@pytest.fixture
def client(monkeypatch):
    app = FastAPI()
    app.include_router(h.router)
    e64.clear_cache()

    def setup(fake):
        async def factory(url=None, server=None):
            return fake
        monkeypatch.setattr(h, "_explorer_async", factory)
        return TestClient(app)
    yield setup
    e64.clear_cache()


# ── lists: 0, 1, many; before 5.2 ────────────────────────────────────────────────────────────────────────

def test_empty_model_list_is_an_empty_read_not_an_error(client):
    r = client(FakeExplorer(about=ABOUT_6_4)).get("/api/analytics-models")
    assert r.status_code == 200 and r.json() == {"items": [], "total": 0, "capped": False}


def test_one_and_many_models_sorted_by_name(client):
    a = model("m-a", props={"displayName": "Zeta"})
    b = model("m-b", props={"displayName": "alpha"}, metrics=METRICS)
    r = client(FakeExplorer(about=ABOUT_6_4, pages=[[a]])).get("/api/analytics-models").json()
    assert [i["guid"] for i in r["items"]] == ["m-a"] and r["items"][0]["implementationLanguage"] == "Python"
    r = client(FakeExplorer(about=ABOUT_6_4, pages=[[a, b]])).get("/api/analytics-models").json()
    assert [i["guid"] for i in r["items"]] == ["m-b", "m-a"]
    assert r["items"][0]["hasRunMetrics"] is True and r["items"][1]["hasRunMetrics"] is False


def test_list_reads_by_type_and_never_gates(client):
    fake = FakeExplorer(about=ABOUT_6_3, pages=[[run("r-1", props={"startTime": "2026-11-01T00:00:00Z"})]])
    body = client(fake).get("/api/analytics-model-runs").json()
    assert body["total"] == 1 and body["items"][0]["startTime"] == "2026-11-01T00:00:00Z"
    assert fake.calls[0] == ("by-type", "AnalyticsModelRun", 0)      # a 6.3 platform is still read


def test_templates_left_out_unless_asked(client):
    t = model("m-t", extra={})
    t["elementHeader"]["template"] = {"classificationName": "Template"}
    fake = FakeExplorer(about=ABOUT_6_4, pages=[[t, model("m-1")]])
    assert [i["guid"] for i in client(fake).get("/api/analytics-models").json()["items"]] == ["m-1"]
    fake = FakeExplorer(about=ABOUT_6_4, pages=[[t, model("m-1")]])
    assert client(fake).get("/api/analytics-models?include_templates=true").json()["total"] == 2


def test_a_bare_404_with_the_version_unreadable_says_the_platform_lacks_the_type(client):
    fake = FakeExplorer(about=RuntimeError("unreadable"), fail=client_error(404))
    body = client(fake).get("/api/analytics-models").json()
    assert body["needsVersion"] is True and body["items"] == []
    assert "need Egeria 5.2 or later" in body["words"] and "version could not be read" in body["words"]


@pytest.mark.parametrize("about", [ABOUT_6_4, ABOUT_6_3])
def test_a_bare_404_on_a_known_platform_is_an_error_with_no_version_words(client, about):
    r = client(FakeExplorer(about=about, fail=client_error(404))).get("/api/analytics-models")
    assert r.status_code == 404
    assert "needsVersion" not in r.text and "need Egeria" not in r.text


def test_a_platform_known_to_predate_5_2_sends_nothing(client):
    fake = FakeExplorer(about={"version": "5.1", "time": "2025-01-01T00:00:00Z"})
    body = client(fake).get("/api/analytics-model-runs").json()
    assert body["needsVersion"] is True and "runs Egeria 5.1" in body["words"]
    assert fake.calls == []


def test_other_errors_stay_errors(client):
    r = client(FakeExplorer(about=ABOUT_6_4, fail=client_error(500))).get("/api/analytics-model-runs")
    assert r.status_code >= 500


# ── the model card ───────────────────────────────────────────────────────────────────────────────────────

def test_model_with_no_runs_says_none_and_no_metrics_says_none(client):
    body = client(FakeExplorer(about=ABOUT_6_4, elements={"m-1": model()})).get("/api/analytics-models/m-1").json()
    assert body["runs"] == [] and body["lists"]["runs"] == {"state": "none"}
    assert body["runMetrics"] == {"state": "none"}                    # never zeros
    assert body["lists"]["projects"] == {"state": "none"}             # 6.4 platform, read, none


def test_model_runs_newest_first_and_unstarted_last(client):
    runs = [run_rel("ph-1", "r-1", "old", start="2026-01-01T00:00:00Z"),
            run_rel("ph-2", "r-2", "new", start="2026-11-01T00:00:00Z", metrics={"lastRunStatus": "FAILED"}),
            run_rel("ph-3", "r-3", "b-unstarted"), run_rel("ph-4", "r-4", "a-unstarted")]
    body = client(FakeExplorer(about=ABOUT_6_4, elements={"m-1": model(runs=runs)})).get("/api/analytics-models/m-1").json()
    assert [r["guid"] for r in body["runs"]] == ["r-2", "r-1", "r-4", "r-3"]
    assert body["runs"][0]["lastRunStatus"] == "FAILED" and body["runs"][0]["relationshipType"] == "ProcessHierarchy"
    assert body["lists"]["runs"] == {"state": "read"}
    assert "childProcesses" not in body["relationships"]              # shown once, in Runs


def test_runs_found_through_any_relationship_and_a_repeated_relationship_dropped(client):
    other = run_rel("df-1", "r-9", "lineage run", rel_type="DataFlow")
    el = model(runs=[run_rel("ph-1", "r-1", "one"), run_rel("ph-1", "r-1", "one")], extra={"dataFlowTargets": [other]})
    body = client(FakeExplorer(about=ABOUT_6_4, elements={"m-1": el})).get("/api/analytics-models/m-1").json()
    assert sorted(r["relationshipGuid"] for r in body["runs"]) == ["df-1", "ph-1"]


def test_non_run_children_stay_in_relationships(client):
    child = rel("ProcessHierarchy", "ph-x", "p-x", el_type="Process", super_types=["Asset", "Referenceable"])
    body = client(FakeExplorer(about=ABOUT_6_4, elements={"m-1": model(runs=[child])})).get("/api/analytics-models/m-1").json()
    assert body["runs"] == [] and "childProcesses" in body["relationships"]


def test_model_metrics_read_keep_only_recorded_values(client):
    body = client(FakeExplorer(about=ABOUT_6_4, elements={"m-1": model(metrics=METRICS)})).get("/api/analytics-models/m-1").json()
    m = body["runMetrics"]
    assert m["state"] == "read" and m["values"]["runCount"] == 12 and m["values"]["failedRunCount"] == 0
    assert "totalRowsRead" not in m["values"]                         # not recorded -> absent, not 0


@pytest.mark.parametrize("about,state,words", [
    (ABOUT_6_1, "needs-6.2", "need Egeria 6.2"),
    (RuntimeError("unreadable"), "not-known", None),
    (ABOUT_6_3, "none", None),
])
def test_absent_metrics_words_depend_on_the_platform(client, about, state, words):
    body = client(FakeExplorer(about=about, elements={"r-1": run()})).get("/api/analytics-model-runs/r-1").json()
    assert body["runMetrics"]["state"] == state
    if words:
        assert words in body["runMetrics"]["words"] and "runs Egeria 6.1" in body["runMetrics"]["words"]


def test_projects_and_experiments(client):
    el = model(extra={"workedOnByProjects": [project_rel("pt-1", "p-1", "Plain project"),
                                              project_rel("pt-2", "p-2", "Churn experiment", hypothesis="Tenure predicts churn")]})
    body = client(FakeExplorer(about=ABOUT_6_4, elements={"m-1": el})).get("/api/analytics-models/m-1").json()
    assert [p["guid"] for p in body["projects"]] == ["p-2", "p-1"]    # experiments first
    assert body["projects"][0]["isExperiment"] and body["projects"][0]["hypothesis"] == "Tenure predicts churn"
    assert body["projects"][1]["isExperiment"] is False
    assert body["lists"]["projects"] == {"state": "read"}


def test_projects_before_6_4_say_needs_6_4_not_none(client):
    body = client(FakeExplorer(about=ABOUT_6_3, elements={"m-1": model()})).get("/api/analytics-models/m-1").json()
    assert body["lists"]["projects"]["state"] == "needs-6.4"
    assert "needs Egeria 6.4" in body["lists"]["projects"]["words"]


def test_projects_linked_another_way_are_shown_on_any_platform(client):
    el = model(extra={"resourceListUsers": [project_rel("rl-1", "p-1", "Old project", rel_type="ResourceList")]})
    body = client(FakeExplorer(about=ABOUT_6_3, elements={"m-1": el})).get("/api/analytics-models/m-1").json()
    assert body["lists"]["projects"] == {"state": "read"} and body["projects"][0]["relationshipType"] == "ResourceList"


def test_model_sources(client):
    src = rel("ExternalReferenceLink", "erl-1", "s-1", el_type="ExternalModelSource",
              super_types=["ExternalReference", "Referenceable"],
              el_props={"displayName": "Hugging Face card", "url": "https://hf.example/churn"})
    body = client(FakeExplorer(about=ABOUT_6_4, elements={"m-1": model(extra={"externalReferences": [src]})})).get(
        "/api/analytics-models/m-1").json()
    assert body["sources"][0]["url"] == "https://hf.example/churn" and body["lists"]["sources"] == {"state": "read"}
    assert "externalReferences" not in body["relationships"]


# ── the run card ─────────────────────────────────────────────────────────────────────────────────────────

def test_run_card_dates_model_and_metrics(client):
    mrel = rel("ProcessHierarchy", "ph-1", "m-1", el_type="DeployedAnalyticsModel", super_types=MODEL_SUPERS,
               el_props={"displayName": "Churn predictor", "implementationLanguage": "Python"})
    el = run(models=[mrel], metrics=METRICS, props={"startTime": "2026-11-20T10:00:00Z", "activityStatus": "COMPLETED"})
    body = client(FakeExplorer(about=ABOUT_6_4, elements={"r-1": el})).get("/api/analytics-model-runs/r-1").json()
    assert body["models"][0]["guid"] == "m-1" and body["lists"]["models"] == {"state": "read"}
    assert body["startTime"] == "2026-11-20T10:00:00Z" and body["completionTime"] == ""   # missing date: empty, said in words by the UI
    assert body["activityStatus"] == "COMPLETED" and body["runMetrics"]["state"] == "read"


# ── parameters and results (ProcessingVariable), the signature (SupportedVariableType): Egeria 6.4 ─────────

def pv(rel_guid, dv_guid, name, position=None, label="", literal=None, el_type="LiteralDataValue", **dv):
    rp = {"label": label}
    if position is not None:
        rp["position"] = position
    props = {"displayName": name, **dv, **({"dataValue": literal} if literal is not None else {})}
    return rel("ProcessingVariable", rel_guid, dv_guid, el_type=el_type, el_props=props, rel_props=rp,
               super_types=(["DataValue", "Referenceable"] if el_type == "LiteralDataValue" else ["Referenceable"]))


def svt(rel_guid, st_guid, name, position=None, mn=None, mx=None):
    rp = {"label": name}
    for k, v in (("position", position), ("minCardinality", mn), ("maxCardinality", mx)):
        if v is not None:
            rp[k] = v
    return rel("SupportedVariableType", rel_guid, st_guid, el_type="PrimitiveSchemaType", el_props={"displayName": name, "dataType": "float"},
               rel_props=rp, super_types=["SchemaType", "Referenceable"])


def test_run_parameters_and_results_in_position_order_with_values(client):
    el = run(extra={"processingVariables": [
        pv("pv-3", "dv-3", "score", position=0, label="result", literal="0.82", dataType="float"),
        pv("pv-2", "dv-2", "threshold", position=2, label="parameter", literal="0.5"),
        pv("pv-1", "dv-1", "training set", position=1, label="input", el_type="DataValue", dataFormat="parquet"),
        pv("pv-1", "dv-1", "training set", position=1, label="input", el_type="DataValue")]})   # same relationship twice
    body = client(FakeExplorer(about=ABOUT_6_4, elements={"r-1": el})).get("/api/analytics-model-runs/r-1").json()
    assert [v["relationshipGuid"] for v in body["variables"]] == ["pv-1", "pv-2", "pv-3"]   # 1, 2, then unset
    assert body["variables"][2]["position"] is None and body["variables"][2]["positionSet"] is False
    assert body["variables"][1]["value"] == {"kind": "literal", "dataValue": "0.5", "dataValueList": None, "dataValueMap": None}
    assert body["variables"][0]["value"] == {"kind": "not-literal"} and body["variables"][0]["dataFormat"] == "parquet"
    assert [v["label"] for v in body["variables"]] == ["input", "parameter", "result"]
    assert body["lists"]["variables"] == {"state": "read"}
    assert "processingVariables" not in body["relationships"]
    assert all(l["key"] != "processingVariables" for s_ in body["related"]["sections"] for l in s_["lists"])


def test_run_with_no_variables_on_6_4_says_none_and_before_6_4_needs_6_4(client):
    body = client(FakeExplorer(about=ABOUT_6_4, elements={"r-1": run()})).get("/api/analytics-model-runs/r-1").json()
    assert body["variables"] == [] and body["lists"]["variables"] == {"state": "none"}
    # the gate caches per platform URL: each platform here gets its own
    body = client(FakeExplorer(about=ABOUT_6_3, elements={"r-1": run()}, url="https://e63.test:9443")).get("/api/analytics-model-runs/r-1").json()
    st = body["lists"]["variables"]
    assert st["state"] == "needs-6.4" and "parameters and results" in st["words"] and "runs Egeria 6.3" in st["words"]
    body = client(FakeExplorer(about=RuntimeError("x"), elements={"r-1": run()}, url="https://unknown.test:9443")).get("/api/analytics-model-runs/r-1").json()
    assert body["lists"]["variables"] == {"state": "not-known"}


def test_model_signature_in_position_order(client):
    el = model(extra={"processVariableTypes": [svt("s-2", "st-2", "threshold", position=2, mn=1, mx=1),
                                                svt("s-0", "st-0", "extras", position=0),
                                                svt("s-1", "st-1", "features", position=1, mn=1)]})
    body = client(FakeExplorer(about=ABOUT_6_4, elements={"m-1": el})).get("/api/analytics-models/m-1").json()
    assert [t["relationshipGuid"] for t in body["variableTypes"]] == ["s-1", "s-2", "s-0"]
    assert body["variableTypes"][0]["minCardinality"] == 1 and body["variableTypes"][0]["maxCardinality"] is None
    assert body["variableTypes"][0]["dataType"] == "float" and body["lists"]["variableTypes"] == {"state": "read"}
    assert "processVariableTypes" not in body["relationships"]


def test_model_signature_before_6_4_says_needs_6_4(client):
    body = client(FakeExplorer(about=ABOUT_6_3, elements={"m-1": model()})).get("/api/analytics-models/m-1").json()
    assert body["lists"]["variableTypes"]["state"] == "needs-6.4" and "signature" in body["lists"]["variableTypes"]["words"]


def test_other_6_4_lists_go_to_related_rows_and_never_to_relationships(client):
    dec = rel("Outcome", "o-1", "dec-1", el_type="Decision", el_props={"displayName": "Use the churn model"})
    el = model(extra={"associatedDecisions": [dec]})
    body = client(FakeExplorer(about=ABOUT_6_4, elements={"m-1": el})).get("/api/analytics-models/m-1").json()
    assert "associatedDecisions" not in body["relationships"]
    keys = [l["key"] for s_ in body["related"]["sections"] for l in s_["lists"]]
    assert "associatedDecisions" in keys
    assert not set(keys) & {"processingVariables", "processVariableTypes", "workedOnByProjects", "projectTargets"}
    out = [l for s_ in body["related"]["sections"] for l in s_["lists"] if l["key"] == "associatedDecisions"][0]
    assert out["rows"][0]["guid"] == "dec-1" and out["st"] == {"state": "read"}


def test_run_with_no_model_says_none(client):
    body = client(FakeExplorer(about=ABOUT_6_4, elements={"r-1": run()})).get("/api/analytics-model-runs/r-1").json()
    assert body["models"] == [] and body["lists"]["models"] == {"state": "none"}


def test_wrong_type_and_missing_are_404(client):
    fake = FakeExplorer(about=ABOUT_6_4, elements={"m-1": model()})
    assert client(fake).get("/api/analytics-model-runs/m-1").status_code == 404
    assert client(FakeExplorer(about=ABOUT_6_4)).get("/api/analytics-models/nope").status_code == 404


def test_card_reads_a_graph(client):
    fake = FakeExplorer(about=ABOUT_6_4, elements={"m-1": model()})
    client(fake).get("/api/analytics-models/m-1")
    assert fake.calls == [("by-guid", "m-1", "DeployedAnalyticsModel", 1)]


# ── helpers and invariants ───────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("v,ok", [("6.2", True), ("6.1", False), ("6.4-SNAPSHOT", True), ("6.2.1 built x", True),
                                  ("5.9", False), ("", None), ("unknown", None)])
def test_egeria_at_least(v, ok):
    assert h.egeria_at_least(v, (6, 2)) is ok


def test_every_route_is_async_and_token_only():
    for r in h.router.routes:
        assert inspect.iscoroutinefunction(r.endpoint), r.path
        params = set(inspect.signature(r.endpoint).parameters)
        assert not params & {"user_id", "user_pwd"}, r.path


def test_registered_in_the_app():
    src = (Path(__file__).resolve().parent.parent / "pyegeria_handler.py").read_text()
    assert "from analytics_models_handler import router" in src and "app.include_router(analytics_models_router)" in src
