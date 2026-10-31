"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

re_analytics.curation_coverage_tile: the Portal's thin HTTP client for
Resource Explorer's curation-coverage tile. RE and Egeria are faked; what is
tested is the Portal's side of the contract: who it signs in as, what it
caches, and that every failure is a not_established tile with its reason,
never counts.
"""

import httpx
import pytest

import re_analytics
import report_viewer

_PERSONA = {"password": "secret", "display_name": "Erin Overview"}
_TILE = {"state": "measured", "state_reason": "", "subtitle": "measured", "Published": 3, "kpis": []}


class _Resp:
    def __init__(self, status, payload=None, text=""):
        self.status_code, self._payload, self.text = status, payload, text

    def json(self):
        if self._payload is None:
            raise ValueError("no json")
        return self._payload


@pytest.fixture(autouse=True)
def _clean(monkeypatch):
    re_analytics._sessions.clear()
    monkeypatch.setattr("demo_config.EGERIA_ADVISOR_SSO_SECRET", "test-secret", raising=False)
    yield
    re_analytics._sessions.clear()


@pytest.fixture
def viewer():
    tok = report_viewer.set_viewer({"persona_id": "erinoverview", "persona": _PERSONA, "user": None, "reason": ""})
    yield
    report_viewer.reset_viewer(tok)


@pytest.fixture
def fake_http(monkeypatch):
    calls = {"token": 0, "exchange": 0, "tile": [], "tile_status": [200], "exchange_status": 200}

    def post(url, json=None, **kw):
        if url.endswith("/api/token"):
            calls["token"] += 1
            return _Resp(200, text="egeria-bearer")
        if url.endswith("/api/auth/portal"):
            calls["exchange"] += 1
            assert "portal_token" in json
            n = calls["exchange"]
            return _Resp(calls["exchange_status"], {"access_token": f"re-session-{n}", "token_type": "bearer"})
        raise AssertionError(url)

    def get(url, headers=None, **kw):
        calls["tile"].append(headers["Authorization"])
        status = calls["tile_status"].pop(0) if len(calls["tile_status"]) > 1 else calls["tile_status"][0]
        return _Resp(status, _TILE if status == 200 else {"detail": "x"})

    monkeypatch.setattr(re_analytics.httpx, "post", post)
    monkeypatch.setattr(re_analytics.httpx, "get", get)
    return calls


def test_no_viewer_is_not_established_not_a_default_user(fake_http):
    tok = report_viewer.set_viewer(report_viewer.resolve_viewer(None, None))
    try:
        tile = re_analytics.curation_coverage_tile("coco_pharma")
    finally:
        report_viewer.reset_viewer(tok)
    assert tile["state"] == "not_established"
    assert "choose a persona" in tile["state_reason"]
    assert fake_http["exchange"] == 0 and not fake_http["tile"]
    assert "Published" not in tile


def test_unsupported_type_is_not_applicable(viewer, fake_http):
    tile = re_analytics.curation_coverage_tile("x", resource_type="topic")
    assert tile["state"] == "not_applicable"
    assert not fake_http["tile"]


def test_tile_passes_through_and_session_is_cached(viewer, fake_http):
    assert re_analytics.curation_coverage_tile("coco_pharma") == _TILE
    assert re_analytics.curation_coverage_tile("coco_pharma") == _TILE
    assert fake_http["exchange"] == 1
    assert fake_http["tile"] == ["Bearer re-session-1", "Bearer re-session-1"]


def test_401_re_exchanges_once(viewer, fake_http):
    fake_http["tile_status"] = [401, 200]
    assert re_analytics.curation_coverage_tile("coco_pharma") == _TILE
    assert fake_http["exchange"] == 2
    assert fake_http["tile"] == ["Bearer re-session-1", "Bearer re-session-2"]


@pytest.mark.parametrize("status,words", [(403, "daemon account"), (503, "not configured on Resource Explorer"),
                                          (401, "refused the Portal sign-in")])
def test_exchange_refusal_is_not_established_with_reason(viewer, fake_http, status, words):
    fake_http["exchange_status"] = status
    tile = re_analytics.curation_coverage_tile("coco_pharma")
    assert tile["state"] == "not_established" and words in tile["state_reason"]
    assert not fake_http["tile"]


def test_non_200_tile_is_not_established(viewer, fake_http):
    fake_http["tile_status"] = [500]
    tile = re_analytics.curation_coverage_tile("coco_pharma")
    assert tile["state"] == "not_established" and "HTTP 500" in tile["state_reason"]
    assert "Published" not in tile


def test_unreachable_re_is_not_established(viewer, monkeypatch):
    def boom(*a, **k):
        raise httpx.ConnectError("refused")
    monkeypatch.setattr(re_analytics.httpx, "post", boom)
    tile = re_analytics.curation_coverage_tile("coco_pharma")
    assert tile["state"] == "not_established"
    assert "could not be reached" in tile["state_reason"] or "not reachable" in tile["state_reason"]


def test_report_spec_loads_under_its_label():
    specs = re_analytics.report_specs()
    assert re_analytics.TILE_LABEL in specs
    fs = specs[re_analytics.TILE_LABEL]
    assert fs.action.analytic_function == re_analytics.TILE_FUNCTION


def test_report_spec_function_resolves_by_registered_name():
    # pyegeria refuses an unregistered dotted path outside its allowed packages, so the
    # spec must name a registered function that resolves to this module's tile.
    from pyegeria.view.format_set_executor import _resolve_analytic_function
    fs = re_analytics.report_specs()[re_analytics.TILE_LABEL]
    assert "." not in fs.action.analytic_function
    assert _resolve_analytic_function(fs.action.analytic_function) is re_analytics.curation_coverage_tile
    re_analytics.register_tile_function()  # a second load does not collide
