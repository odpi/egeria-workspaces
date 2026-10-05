# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""_survey_reports() must read both annotation payload shapes.

A platform that reuses survey annotations returns the list `fromSurveyReports`; a platform that
does not returns the single `fromSurveyReport`. The Tech Catalog's report column, report filter and
"go to report" button depend on this helper, so a handler that read only one shape would silently
lose every report link on the other kind of platform.

The helper is a pure function, so it is extracted from each handler file (quickstart and freshstart
carry identical copies) and exercised without importing pyegeria or FastAPI.
"""
import ast
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
_HANDLERS = {
    "quickstart": _HERE.parent / "tech_catalog_handler.py",
    "freshstart": _HERE.parents[2] / "egeria-freshstart" / "PyegeriaWebHandler" / "tech_catalog_handler.py",
}


def _load_survey_reports(path: Path):
    if not path.exists():
        pytest.skip(f"{path} not present in this checkout")
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    func = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_survey_reports")
    namespace: dict = {}
    exec(compile(ast.Module(body=[func], type_ignores=[]), str(path), "exec"), namespace)  # noqa: S102
    return namespace["_survey_reports"]


@pytest.fixture(params=sorted(_HANDLERS))
def survey_reports(request):
    return _load_survey_reports(_HANDLERS[request.param])


def _rel(guid, name="", created=""):
    """One fromSurveyReport(s) entry: a RelatedMetadataElementSummary."""
    header = {"guid": guid}
    if created:
        header["versions"] = {"createTime": created}
    props = {"displayName": name} if name else {}
    return {"class": "RelatedMetadataElementSummary", "relatedElement": {"elementHeader": header, "properties": props}}


def test_list_payload_is_read_newest_first(survey_reports):
    ann = {"fromSurveyReports": [_rel("old", "Survey: a", "2026-10-01T10:00:00"),
                                 _rel("new", "Survey: a (repeat)", "2026-10-04T10:00:00"),
                                 _rel("mid", "Survey: a (again)", "2026-10-02T10:00:00")]}
    assert [r["guid"] for r in survey_reports(ann)] == ["new", "mid", "old"]
    assert survey_reports(ann)[0] == {"guid": "new", "displayName": "Survey: a (repeat)",
                                      "createTime": "2026-10-04T10:00:00"}


def test_single_payload_is_read_as_a_one_item_list(survey_reports):
    ann = {"fromSurveyReport": _rel("only", "Survey: b", "2026-10-03T09:00:00")}
    assert survey_reports(ann) == [{"guid": "only", "displayName": "Survey: b", "createTime": "2026-10-03T09:00:00"}]


def test_list_wins_when_both_are_present_and_nothing_is_duplicated(survey_reports):
    ann = {"fromSurveyReports": [_rel("r1", "x", "2026-10-02"), _rel("r2", "y", "2026-10-03")],
           "fromSurveyReport": _rel("r1", "x", "2026-10-02")}
    assert [r["guid"] for r in survey_reports(ann)] == ["r2", "r1"]


def test_empty_list_falls_back_to_the_single_form(survey_reports):
    ann = {"fromSurveyReports": [], "fromSurveyReport": _rel("legacy", "z")}
    assert [r["guid"] for r in survey_reports(ann)] == ["legacy"]


@pytest.mark.parametrize("ann", [{}, {"fromSurveyReports": None, "fromSurveyReport": None},
                                 {"fromSurveyReports": []}, {"fromSurveyReport": {}}])
def test_no_report_link_gives_an_empty_list(survey_reports, ann):
    assert survey_reports(ann) == []


def test_malformed_entries_are_skipped_not_fatal(survey_reports):
    ann = {"fromSurveyReports": ["not a dict", None, {"relatedElement": {}},
                                 {"relatedElement": {"elementHeader": {}}}, _rel("good", "ok", "2026-10-04")]}
    assert [r["guid"] for r in survey_reports(ann)] == ["good"]


@pytest.mark.parametrize("bad", ["a string", 7, True])
def test_a_wrongly_typed_list_field_is_ignored(survey_reports, bad):
    assert survey_reports({"fromSurveyReports": bad}) == []


def test_a_single_dict_in_the_list_field_is_tolerated(survey_reports):
    assert [r["guid"] for r in survey_reports({"fromSurveyReports": _rel("solo", "s")})] == ["solo"]


def test_a_report_without_a_create_time_sorts_last_and_keeps_empty_strings(survey_reports):
    ann = {"fromSurveyReports": [_rel("undated", "u"), _rel("dated", "d", "2026-10-04")]}
    got = survey_reports(ann)
    assert [r["guid"] for r in got] == ["dated", "undated"]
    assert got[1]["createTime"] == "" and got[1]["displayName"] == "u"
