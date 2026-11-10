"""Refreshing a seeded SavedQuery (insights_handler.refresh_saved_query).

A SavedQuery made by Dr.Egeria has no resultsSetGuid and no formula; the refresh
finds its Results Set through SmartQuery and its search in
additionalProperties.searchSpec. Overrides may never carry connection keys, and
a parameters declaration limits what may be overridden. No Egeria: the pyegeria
clients and the in-process search are fakes.
"""
import json

import pytest
from fastapi import HTTPException
from fastapi.responses import JSONResponse

import insights_handler as ih

SQ = "sq-guid"
RS = "rs-guid"


def _related(*guids):
    return {"elementList": [
        {"relationshipGUID": f"rel-{g}", "elementAtEnd1": True,
         "element": {"elementGUID": g, "type": {"typeName": "ResultsSet",
                                                  "superTypeNames": ["Collection", "Referenceable"]}}}
        for g in guids]}


class Fake:
    def __init__(self, additional, formula=None, related=None, members=()):
        self.el = {"elementHeader": {"guid": SQ}, "properties": {
            "qualifiedName": "SavedQuery::seed", "displayName": "Seed", "formula": formula,
            "additionalProperties": additional}}
        self.related = related if related is not None else _related(RS)
        self.members = [{"elementHeader": {"guid": g}} for g in members]
        self.added, self.removed, self.updates, self.related_calls = [], [], [], 0
        self.searched = []

    # AssetMaker
    def get_asset_by_guid(self, guid, output_format="JSON"):
        return self.el

    def update_asset(self, guid, body):
        self.updates.append(body)

    # CollectionManager
    def get_collection_members(self, collection_guid, output_format="JSON", page_size=500):
        assert collection_guid == RS
        return self.members

    def add_to_collection(self, rs, g, body=None):
        self.added.append(g)

    def remove_from_collection(self, rs, g):
        self.removed.append(g)

    # MetadataExpert
    def get_related_metadata_elements(self, guid, rel_type, body, starting_at_end=0):
        assert (guid, rel_type) == (SQ, "SmartQuery")
        self.related_calls += 1
        return self.related


@pytest.fixture
def run(monkeypatch):
    def _run(fake, overrides=None, hits=("a", "b")):
        for name in ("_am", "_cm", "_expert"):
            monkeypatch.setattr(ih, name, lambda *a, **k: fake)

        def search(body):
            fake.searched.append(body)
            return JSONResponse({"results": [{"guid": g} for g in hits]})

        monkeypatch.setattr(ih, "search_elements", search)
        resp = ih.refresh_saved_query(SQ, ih.RefreshQueryBody(overrides=overrides))
        return json.loads(resp.body)
    return _run


SEED = {"pyegeriaInsightsQuery": "True", "searchSpec": json.dumps({"type_name": "Asset"})}


def _stamped(fake):
    return fake.updates[-1]["properties"]["additionalProperties"]


# ── the Results Set, by relationship ─────────────────────────────────────────

def test_seeded_query_refreshes_through_the_smartquery_link(run):
    fake = Fake(dict(SEED), members=("b", "c"))
    out = run(fake)
    assert out["resultsSetGuid"] == RS and out["specSource"] == "searchSpec"
    assert sorted(fake.added) == ["a"] and fake.removed == ["c"]
    assert fake.searched[0].type_name == "Asset"
    stamped = _stamped(fake)
    assert stamped["resultsSetGuid"] == RS and stamped["smartQueryRelGuid"] == f"rel-{RS}"
    assert stamped["resultCount"] == "2"


def test_pinned_results_set_skips_the_lookup(run):
    fake = Fake({**SEED, "resultsSetGuid": RS})
    run(fake)
    assert fake.related_calls == 0


@pytest.mark.parametrize("related, says", [
    (_related(), "no linked ResultsSet"),
    (_related(RS, "rs-2"), "2 ResultsSets are linked"),
])
def test_zero_or_two_links_are_refused_with_a_sentence(run, related, says):
    fake = Fake(dict(SEED), related=related)
    with pytest.raises(HTTPException) as e:
        run(fake)
    assert e.value.status_code == 409 and says in e.value.detail
    assert not fake.updates and not fake.added


def test_a_non_results_set_neighbour_does_not_count(run):
    related = _related(RS)
    related["elementList"].append({"relationshipGUID": "x", "element": {
        "elementGUID": "other", "type": {"typeName": "Asset", "superTypeNames": ["Referenceable"]}}})
    fake = Fake(dict(SEED), related=related)
    assert run(fake)["resultsSetGuid"] == RS


# ── where the search comes from ──────────────────────────────────────────────

def test_formula_wins_over_search_spec(run):
    fake = Fake(dict(SEED), formula=json.dumps({"type_name": "DataSet"}))
    out = run(fake)
    assert out["specSource"] == "formula" and fake.searched[0].type_name == "DataSet"


def test_with_neither_the_refusal_says_what_is_missing(run):
    fake = Fake({"pyegeriaInsightsQuery": "true"}, formula="")
    with pytest.raises(HTTPException) as e:
        run(fake)
    assert e.value.status_code == 400
    assert "formula is empty" in e.value.detail and "searchSpec" in e.value.detail


def test_a_search_spec_that_is_not_json_is_refused(run):
    fake = Fake({"pyegeriaInsightsQuery": "true", "searchSpec": "{type_name: Asset"})
    with pytest.raises(HTTPException) as e:
        run(fake)
    assert "searchSpec is not valid JSON" in e.value.detail


def test_without_the_marker_it_is_not_a_saved_query(run):
    fake = Fake({"searchSpec": json.dumps({"type_name": "Asset"})})
    with pytest.raises(HTTPException) as e:
        run(fake)
    assert e.value.status_code == 404


# ── connection keys never come from the spec or the overrides ────────────────

@pytest.mark.parametrize("key, value", [
    ("url", "https://attacker.example:9443"), ("server", "other-view-server"),
    ("user_id", "garygeeke"), ("user_pwd", "stolen"),
])
def test_connection_keys_in_overrides_are_dropped(run, key, value):
    fake = Fake(dict(SEED))
    out = run(fake, overrides={key: value, "type_name": "DataSet"})
    body = fake.searched[0]
    assert getattr(body, key) != value
    assert body.type_name == "DataSet"
    assert key not in out["lastRefreshParams"]


def test_connection_keys_in_a_stored_spec_are_dropped(run):
    spec = {"type_name": "Asset", "url": "https://attacker.example:9443", "user_id": "garygeeke",
            "server": "other-view-server", "user_pwd": "stolen"}
    fake = Fake({"pyegeriaInsightsQuery": "true", "searchSpec": json.dumps(spec)})
    run(fake)
    body = fake.searched[0]
    assert body.url != spec["url"] and body.user_id != "garygeeke"
    assert body.server != "other-view-server" and body.user_pwd != "stolen"


def test_an_override_that_is_not_a_search_field_is_refused(run):
    fake = Fake(dict(SEED))
    with pytest.raises(HTTPException) as e:
        run(fake, overrides={"platform": "x"})
    assert e.value.status_code == 400 and "platform" in e.value.detail


# ── declared parameters ─────────────────────────────────────────────────────

PARAMS = [{"name": "type_name", "type": "string", "default": "Asset"},
          {"name": "relationship_conditions.0.relationship_type", "type": "string"},
          {"name": "page_size", "type": "integer", "default": 50}]
PSPEC = {"type_name": "Asset",
         "relationship_conditions": [{"relationship_type": "DataContentForDataSet", "presence": "has"}]}


def _declared():
    return Fake({"pyegeriaInsightsQuery": "true", "searchSpec": json.dumps(PSPEC),
                 "parameters": json.dumps(PARAMS)})


def test_a_declared_override_runs_and_is_recorded(run):
    fake = _declared()
    out = run(fake, overrides={"type_name": "DataSet",
                               "relationship_conditions.0.relationship_type": "SemanticAssignment"})
    body = fake.searched[0]
    assert body.type_name == "DataSet"
    assert body.relationship_conditions[0].relationship_type == "SemanticAssignment"
    assert body.page_size == 50  # default fills a missing path
    want = {"type_name": "DataSet", "relationship_conditions.0.relationship_type": "SemanticAssignment",
            "page_size": 50}
    assert out["lastRefreshParams"] == want
    assert json.loads(_stamped(fake)["lastRefreshParams"]) == want
    assert "lastRefreshedTime" in _stamped(fake)


def test_without_overrides_the_stored_values_are_recorded(run):
    fake = _declared()
    out = run(fake)
    assert out["lastRefreshParams"] == {
        "type_name": "Asset", "relationship_conditions.0.relationship_type": "DataContentForDataSet",
        "page_size": 50}


def test_an_undeclared_override_is_refused_with_the_declared_list(run):
    fake = _declared()
    with pytest.raises(HTTPException) as e:
        run(fake, overrides={"sort_by": "displayName"})
    assert e.value.status_code == 400
    assert "sort_by" in e.value.detail and "type_name" in e.value.detail and "page_size" in e.value.detail
    assert not fake.searched


@pytest.mark.parametrize("name, value", [("type_name", 7), ("page_size", "50"), ("page_size", True)])
def test_a_wrong_type_is_refused(run, name, value):
    fake = _declared()
    with pytest.raises(HTTPException) as e:
        run(fake, overrides={name: value})
    assert e.value.status_code == 400 and name in e.value.detail
    assert not fake.searched


def test_connection_keys_are_dropped_even_when_declared_parameters_exist(run):
    fake = _declared()
    run(fake, overrides={"url": "https://attacker.example:9443"})
    assert fake.searched[0].url != "https://attacker.example:9443"


def test_a_declaration_cannot_name_a_connection_key(run):
    fake = Fake({"pyegeriaInsightsQuery": "true", "searchSpec": json.dumps(PSPEC),
                 "parameters": json.dumps([{"name": "url", "type": "string"}])})
    with pytest.raises(HTTPException) as e:
        run(fake, overrides={"url": "https://attacker.example:9443"})
    assert e.value.status_code == 400 and "not a search field" in e.value.detail


def test_a_parameter_path_into_nothing_is_refused(run):
    fake = Fake({"pyegeriaInsightsQuery": "true", "searchSpec": json.dumps({"type_name": "Asset"}),
                 "parameters": json.dumps([{"name": "relationship_conditions.3.relationship_type",
                                            "type": "string"}])})
    with pytest.raises(HTTPException) as e:
        run(fake, overrides={"relationship_conditions.3.relationship_type": "X"})
    assert "points at nothing" in e.value.detail


# ── the cached-results view finds a seeded query's Results Set too ───────────

def test_cached_results_resolve_through_the_link(monkeypatch):
    fake = Fake(dict(SEED), members=("m1",))
    for name in ("_am", "_cm", "_expert"):
        monkeypatch.setattr(ih, name, lambda *a, **k: fake)
    monkeypatch.setattr(ih, "_serialize_member", lambda m: {"guid": m["elementHeader"]["guid"]})
    out = json.loads(ih.get_saved_query_results(SQ, None, None, None).body)
    assert out == {"results": [{"guid": "m1"}], "total": 1}


def test_summary_shows_a_seeded_spec_and_its_parameters():
    fake = _declared()
    s = ih._saved_query_summary(fake.el)
    assert s["spec"]["type_name"] == "Asset" and s["specSource"] == "searchSpec"
    assert [p["name"] for p in s["parameters"]] == [p["name"] for p in PARAMS]


# ── a failed stamp is reported, not swallowed (SQ-1) ─────────────────────────

def test_a_successful_stamp_says_so(run):
    out = run(Fake(dict(SEED)))
    assert out["stamped"] is True and out["stampError"] is None


def test_a_failed_stamp_is_reported_and_the_results_still_return(run):
    fake = Fake(dict(SEED), members=("b", "c"))

    def boom(guid, body):
        fake.updates.append(body)
        raise RuntimeError("OMAG-REPOSITORY-HANDLER-500-001 update failed")

    fake.update_asset = boom
    out = run(fake)
    assert out["stamped"] is False
    assert "update failed" in out["stampError"] and "previous run" in out["stampError"]
    # The answer itself is fresh and fully reported.
    assert out["resultCount"] == 2 and out["added"] == 1 and out["removed"] == 1
    assert sorted(fake.added) == ["a"] and fake.removed == ["c"]
    assert out["resultsSetGuid"] == RS and "lastRefreshedTime" in out


def test_the_ui_shows_a_failed_stamp():
    import pathlib
    html = (pathlib.Path(ih.__file__).parent / "egeria-insights.html").read_text()
    assert "d.stamped === false" in html and "d.stampError" in html


# ── one parameter model with pyegeria (Architect P-2): searchPath + shared fixture ──

def test_search_path_applies_the_value_and_name_keys_the_record(run):
    params = [{"name": "kind", "type": "string", "default": "Asset", "searchPath": "type_name",
               "requestPath": "metadataElementTypeName"}]
    fake = Fake({"pyegeriaInsightsQuery": "true", "searchSpec": json.dumps({"type_name": "DataSet"}),
                 "parameters": json.dumps(params)})
    out = run(fake, overrides={"kind": "Process"})
    assert fake.searched[0].type_name == "Process"
    assert out["lastRefreshParams"] == {"kind": "Process"}


def test_overrides_go_by_name_not_by_search_path(run):
    params = [{"name": "kind", "type": "string", "searchPath": "type_name"}]
    fake = Fake({"pyegeriaInsightsQuery": "true", "searchSpec": json.dumps({"type_name": "DataSet"}),
                 "parameters": json.dumps(params)})
    with pytest.raises(HTTPException) as e:
        run(fake, overrides={"type_name": "Process"})
    assert "only accepts kind" in e.value.detail


def test_a_stored_value_wins_over_a_differing_default(run):
    params = [{"name": "kind", "type": "string", "default": "Asset", "searchPath": "type_name"}]
    fake = Fake({"pyegeriaInsightsQuery": "true", "searchSpec": json.dumps({"type_name": "DataSet"}),
                 "parameters": json.dumps(params)})
    assert run(fake)["lastRefreshParams"] == {"kind": "DataSet"}


def test_a_search_path_outside_the_search_is_refused(run):
    params = [{"name": "where", "type": "string", "searchPath": "url"}]
    fake = Fake({"pyegeriaInsightsQuery": "true", "searchSpec": json.dumps({"type_name": "Asset"}),
                 "parameters": json.dumps(params)})
    with pytest.raises(HTTPException) as e:
        run(fake)
    assert "searchPath 'url'" in e.value.detail and "not a search field" in e.value.detail


def test_a_duplicate_name_is_refused(run):
    params = [{"name": "kind", "type": "string", "searchPath": "type_name"},
              {"name": "kind", "type": "string", "searchPath": "sort_by"}]
    fake = Fake({"pyegeriaInsightsQuery": "true", "searchSpec": json.dumps({"type_name": "Asset"}),
                 "parameters": json.dumps(params)})
    with pytest.raises(HTTPException) as e:
        run(fake)
    assert "declared twice" in e.value.detail


FIXTURE = __import__("pathlib").Path(__file__).parent / "fixtures" / "saved_query_portal_shaped.json"


def _fixture():
    return json.loads(FIXTURE.read_text())


def test_shared_fixture_effective_values_match_this_rule():
    fx = _fixture()
    props = fx["savedQuery"]["properties"]
    spec, _ = ih._stored_search_spec(props)
    declared = ih._declared_parameters(props["additionalProperties"])
    for case in fx["cases"]:
        assert ih.effective_parameters(spec, case["request"], declared) == case["effective"], case["why"]


def test_shared_fixture_last_refresh_params_are_what_a_refresh_writes(run):
    fx = _fixture()
    el = json.loads(json.dumps(fx["savedQuery"]))
    add = el["properties"]["additionalProperties"]
    recorded = add.pop("lastRefreshParams")
    add["resultsSetGuid"] = RS  # the fake's Results Set
    fake = Fake({})
    fake.el = el
    out = run(fake, overrides=fx["lastRefresh"]["overrides"])
    assert out["lastRefreshParams"] == fx["lastRefresh"]["lastRefreshParams"]
    assert _stamped(fake)["lastRefreshParams"] == recorded  # byte-identical JSON string


def test_shared_fixture_request_paths_hold_the_same_values_the_portal_ran():
    """With no request, each requestPath in the stored queryRequestBody holds the
    value the Portal recorded, so pyegeria's comparison agrees with ours."""
    fx = _fixture()
    props = fx["savedQuery"]["properties"]
    body = json.loads(props["queryRequestBody"])
    no_request = next(c for c in fx["cases"] if c["request"] == {})["effective"]
    declared = ih._declared_parameters(props["additionalProperties"])
    with_request_path = [p for p in declared if p.get("requestPath")]
    assert with_request_path and any(not p.get("requestPath") for p in declared)
    for p in with_request_path:
        assert ih._get_path(body, p["requestPath"]) == no_request[p["name"]], p["name"]
    assert "{{" not in props["queryRequestBody"] and "{{" not in props["formula"]


# ── a registered Smart Collection runs only its stored values (Architect P-3) ──

def _registered(**extra):
    return Fake({"pyegeriaInsightsQuery": "true", "smartCollection": "true",
                 "searchSpec": json.dumps(PSPEC), "parameters": json.dumps(PARAMS), **extra})


def test_registered_query_refuses_a_changed_value(run):
    fake = _registered()
    with pytest.raises(HTTPException) as e:
        run(fake, overrides={"type_name": "DataSet"})
    assert e.value.status_code == 409
    assert "kept current by Egeria with its stored values; run other values live" in e.value.detail
    assert "type_name" in e.value.detail
    assert not fake.searched and not fake.added and not fake.updates


def test_registered_query_without_overrides_stamps_the_stored_effective_values(run):
    fake = _registered()
    out = run(fake)
    want = {"type_name": "Asset", "relationship_conditions.0.relationship_type": "DataContentForDataSet",
            "page_size": 50}
    assert out["lastRefreshParams"] == want
    assert json.loads(_stamped(fake)["lastRefreshParams"]) == want
    assert fake.searched[0].type_name == "Asset"


def test_registered_query_allows_an_override_equal_to_the_stored_value(run):
    fake = _registered()
    out = run(fake, overrides={"type_name": "Asset", "page_size": 50})  # stored value / default: changes nothing
    assert out["lastRefreshParams"]["type_name"] == "Asset"


def test_registered_query_without_a_declaration_refuses_a_changed_value(run):
    fake = Fake({"pyegeriaInsightsQuery": "true", "smartCollection": "true",
                 "searchSpec": json.dumps({"type_name": "Asset"})})
    with pytest.raises(HTTPException) as e:
        run(fake, overrides={"page_size": 10})
    assert e.value.status_code == 409 and "page_size" in e.value.detail


def test_registered_query_still_drops_connection_keys_rather_than_refusing(run):
    fake = _registered()
    run(fake, overrides={"url": "https://attacker.example:9443"})
    assert fake.searched[0].url != "https://attacker.example:9443"


def test_unregistered_query_still_takes_a_changed_value(run):
    fake = _declared()
    out = run(fake, overrides={"type_name": "DataSet"})
    assert out["lastRefreshParams"]["type_name"] == "DataSet"


def test_shared_fixture_is_registered_and_refuses_a_changed_value(run):
    fx = _fixture()
    fake = Fake({})
    fake.el = json.loads(json.dumps(fx["savedQuery"]))
    fake.el["properties"]["additionalProperties"]["resultsSetGuid"] = RS
    with pytest.raises(HTTPException) as e:
        run(fake, overrides={"min_level": 4})
    assert e.value.status_code == 409
