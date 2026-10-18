# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""_schema_coverage() must read every page of SchemaType elements.

A catalog with more than one page of schema types used to report "assets with schema" as unmeasured
because a single full page was treated as capped. It now reads pages until an empty one (Egeria's paging
contract) and only reports a lower bound -- withholding the figure -- after _REL_MAX_PAGES full pages
without reaching the end, or when any page fails.

The function is extracted from each handler file (quickstart and freshstart carry identical copies) and
run against a fake manager, without importing pyegeria or FastAPI.
"""
import ast
from pathlib import Path
from typing import Optional

import pytest

_HERE = Path(__file__).resolve().parent
_HANDLERS = {
    "quickstart": _HERE.parent / "overview_handler.py",
    "freshstart": _HERE.parents[2] / "egeria-freshstart" / "PyegeriaWebHandler" / "overview_handler.py",
}
_PAGE = 1000


def _load(path: Path):
    if not path.exists():
        pytest.skip(f"{path} not present in this checkout")
    tree = ast.parse(path.read_text(encoding="utf-8"))
    wanted = {"_classification_props", "_schema_coverage"}
    body = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in wanted]
    assert {n.name for n in body} == wanted
    ns = {"Optional": Optional, "_SURVEY_LINK_CAP": _PAGE, "_REL_MAX_PAGES": 10,
          "logger": type("L", (), {"debug": staticmethod(lambda *a, **k: None)})()}
    exec(compile(ast.Module(body=body, type_ignores=[]), str(path), "exec"), ns)
    return ns["_schema_coverage"]


def _schema(i, anchor):
    return {"elementHeader": {"guid": f"s{i}"}, "classifications": [
        {"classificationName": "Anchors", "classificationProperties": {"anchorGUID": anchor}}]}


class _Mgr:
    def __init__(self, total, anchor_of=lambda i: f"a{i}", fail_at=None):
        self.total, self.anchor_of, self.fail_at, self.starts = total, anchor_of, fail_at, []

    def find_metadata_elements(self, body):
        self.starts.append(body["startFrom"])
        if self.fail_at is not None and body["startFrom"] >= self.fail_at:
            raise RuntimeError("boom")
        lo = body["startFrom"]
        return [_schema(i, self.anchor_of(i)) for i in range(lo, min(lo + body["pageSize"], self.total))]


@pytest.fixture(params=sorted(_HANDLERS))
def cover(request):
    return _load(_HANDLERS[request.param])


def test_reads_past_the_first_full_page(cover):
    m = _Mgr(2500)
    out = cover(m)
    assert out["schemaTypes"] == 2500 and out["schemaCapped"] is False
    assert out["assetsWithSchema"] == 2500          # one anchor per schema type
    assert m.starts == [0, 1000, 2000, 3000]        # ends on the empty page, not a short one


def test_exactly_one_full_page_is_not_assumed_to_be_the_end(cover):
    m = _Mgr(1000)
    out = cover(m)
    assert out["schemaCapped"] is False and out["assetsWithSchema"] == 1000 and m.starts == [0, 1000]


def test_anchors_are_distinct_and_survey_analysed_assets_are_unioned(cover):
    out = cover(_Mgr(1500, anchor_of=lambda i: f"a{i % 10}"), analysed=["a1", "x1", "x2"])
    assert out["assetsWithSchema"] == 12            # 10 anchors + 2 survey-only assets
    assert out["schemaAnalysedAssets"] == 2


def test_no_schema_types_is_a_real_zero(cover):
    out = cover(_Mgr(0))
    assert out["assetsWithSchema"] == 0 and out["schemaTypes"] == 0 and out["schemaCapped"] is False


def test_hitting_the_page_limit_withholds_the_figure(cover):
    out = cover(_Mgr(10 * _PAGE + 5))
    assert out["schemaCapped"] is True and out["assetsWithSchema"] is None and out["schemaTypes"] == 10 * _PAGE


def test_a_failed_page_discards_everything(cover):
    out = cover(_Mgr(5000, fail_at=2000))
    assert out == {"assetsWithSchema": None, "schemaTypes": None, "schemaCapped": None, "schemaAnalysedAssets": None}
