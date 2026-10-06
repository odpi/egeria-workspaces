# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""_assets_by_technology() groups assets by deployedImplementationType into exclusive buckets.

Most catalogued assets record no technology, so the result must add up to the asset total (each technology
+ assets that record none + template placeholders) and must never present a partial read as a total: it
reads pages until an empty one and returns None everywhere if a page failed or the page limit was hit.

The function is extracted from each handler file (quickstart and freshstart carry identical copies) and run
against a fake manager, without importing pyegeria or FastAPI.
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
_NONE = {"technologies": None, "unrecorded": None, "placeholders": None, "total": None}


def _load(path: Path):
    if not path.exists():
        pytest.skip(f"{path} not present in this checkout")
    tree = ast.parse(path.read_text(encoding="utf-8"))
    body = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_assets_by_technology"]
    assert len(body) == 1
    ns = {"Optional": Optional, "_SURVEY_LINK_CAP": _PAGE, "_REL_MAX_PAGES": 10,
          "logger": type("L", (), {"debug": staticmethod(lambda *a, **k: None)})()}
    exec(compile(ast.Module(body=body, type_ignores=[]), str(path), "exec"), ns)
    return ns["_assets_by_technology"]


def _asset(tech=None):
    props = {} if tech is None else {"deployedImplementationType": tech}
    return {"elementGUID": "g", "elementProperties": {"propertiesAsStrings": props}}


class _Mgr:
    def __init__(self, assets, fail_at=None):
        self.assets, self.fail_at, self.bodies = assets, fail_at, []

    def find_metadata_elements(self, body):
        self.bodies.append(body)
        if self.fail_at is not None and body["startFrom"] >= self.fail_at:
            raise RuntimeError("boom")
        lo = body["startFrom"]
        return self.assets[lo:lo + body["pageSize"]]


@pytest.fixture(params=sorted(_HANDLERS))
def by_tech(request):
    return _load(_HANDLERS[request.param])


def test_buckets_are_exclusive_and_add_up_to_the_total(by_tech):
    assets = [_asset("CSV Data File")] * 3 + [_asset("Integration Connector")] + [_asset()] * 5 \
        + [_asset("~{deployedImplementationType}~")] * 2 + [_asset("   ")]
    out = by_tech(_Mgr(assets))
    assert out["technologies"] == {"CSV Data File": 3, "Integration Connector": 1}
    assert out["unrecorded"] == 6 and out["placeholders"] == 2 and out["total"] == 12
    assert sum(out["technologies"].values()) + out["unrecorded"] + out["placeholders"] == out["total"]


def test_reads_every_page_and_ends_on_an_empty_one(by_tech):
    m = _Mgr([_asset("A")] * 2500)
    out = by_tech(m)
    assert out["technologies"] == {"A": 2500} and out["total"] == 2500
    assert [b["startFrom"] for b in m.bodies] == [0, 1000, 2000, 3000]


def test_as_of_time_is_sent_and_only_active_assets_are_read(by_tech):
    m = _Mgr([_asset("A")])
    by_tech(m, "2026-10-01T00:00:00")
    assert m.bodies[0]["asOfTime"] == "2026-10-01T00:00:00"
    assert m.bodies[0]["limitResultsByStatus"] == ["ACTIVE"] and m.bodies[0]["metadataElementTypeName"] == "Asset"


def test_no_assets_is_a_real_zero(by_tech):
    assert by_tech(_Mgr([])) == {"technologies": {}, "unrecorded": 0, "placeholders": 0, "total": 0}


def test_hitting_the_page_limit_withholds_everything(by_tech):
    assert by_tech(_Mgr([_asset("A")] * (10 * _PAGE + 1))) == _NONE


def test_a_failed_page_discards_everything(by_tech):
    assert by_tech(_Mgr([_asset("A")] * 5000, fail_at=2000)) == _NONE
