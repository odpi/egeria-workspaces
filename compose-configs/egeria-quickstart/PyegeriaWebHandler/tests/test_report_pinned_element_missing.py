"""W1: a dashboard tile whose Report pins a collection that no longer exists says so, not a raw 400.

The "Tasks" tile on local-dashboards-next-steps pinned collection_guid 0affb580-...; after the platform was
re-seeded Egeria answered CLIENT_ERROR_400 and the tile showed "Execution failed: ...". The execute endpoint
now answers 404 "The collection this report names no longer exists (<guid or name>)." for that case, and
for pyegeria's not-found on a pinned qualifiedName; any other failure keeps its own words.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import egeria_auth  # noqa: E402
import report_specs_handler  # noqa: E402
from report_specs_handler import missing_pinned_element  # noqa: E402

GUID = "0affb580-fa81-4d00-9438-b26faf11845d"
QN = "Coco Pharmaceuticals::WorkItemList::Local-Dashboards---Next-Steps::1.0"


class _EgeriaError(Exception):
    """Shaped like pyegeria's exceptions: the HTTP code Egeria reported, and its words in str()."""
    def __init__(self, text, related_http_code=None, response_code=200):
        super().__init__(text)
        self.related_http_code = related_http_code
        self.response_code = response_code


STALE_GUID_400 = _EgeriaError(
    f"CLIENT_ERROR_400 ... OMAG-REPOSITORY-HANDLER-400-020 The unique identifier {GUID} passed on the "
    f"collectionGUID parameter is not recognized", related_http_code=400)


def test_a_stale_guid_400_is_the_sentence():
    assert missing_pinned_element(STALE_GUID_400, {"collection_guid": GUID}) == (
        f"The collection this report names no longer exists ({GUID}).")


def test_a_not_found_qualified_name_is_the_sentence():
    exc = _EgeriaError(f"The collection {QN!r} was not found.", related_http_code=404)
    assert missing_pinned_element(exc, {"collection_qname": QN}) == (
        f"The collection this report names no longer exists ({QN}).")


def test_the_code_can_come_from_the_text_alone():
    exc = Exception(f"PyegeriaClientException CLIENT_ERROR_400 for /collections/{GUID}/members")
    assert missing_pinned_element(exc, {"collection_guid": GUID})


@pytest.mark.parametrize("exc, params", [
    (STALE_GUID_400, {}),                                                     # nothing pinned
    (STALE_GUID_400, {"collection_guid": "some-other-guid"}),                 # a 400 about something else
    (_EgeriaError("CLIENT_ERROR_400 bad sequencing property", 400), {"collection_guid": GUID}),
    (_EgeriaError("SERVER_ERROR_500", 500), {"collection_guid": GUID}),
    (_EgeriaError("timed out", None, 504), {"collection_guid": GUID}),
    (STALE_GUID_400, {"type_name": GUID}),                                    # not an element pin
])
def test_other_failures_keep_their_own_words(exc, params):
    assert missing_pinned_element(exc, params) is None


def _client(monkeypatch, exc):
    import pyegeria.view.format_set_executor as fse

    def boom(*a, **k):
        raise exc
    monkeypatch.setattr(fse, "exec_report_spec", boom)
    app = FastAPI()
    app.add_middleware(egeria_auth.EgeriaTokenMiddleware)
    app.include_router(report_specs_handler.router)
    return TestClient(app)


def test_the_execute_endpoint_answers_404_with_the_sentence(monkeypatch):
    r = _client(monkeypatch, STALE_GUID_400).post("/api/report-specs/execute", json={
        "spec_name": "Collection Members", "output_format": "MERMAID", "params": {"collection_guid": GUID},
        "cache": True})
    assert r.status_code == 404, r.text
    assert r.json()["detail"] == f"The collection this report names no longer exists ({GUID})."


def test_an_unrelated_failure_is_still_a_500(monkeypatch):
    r = _client(monkeypatch, _EgeriaError("SERVER_ERROR_500 boom", 500)).post("/api/report-specs/execute", json={
        "spec_name": "Collection Members", "output_format": "MERMAID", "params": {"collection_guid": GUID}})
    assert r.status_code == 500
    assert r.json()["detail"].startswith("Execution failed")


def test_the_tile_labels_a_404_not_found():
    html = (Path(__file__).resolve().parent.parent / "local-dashboards.html").read_text()
    assert "status === 404 ? 'Not found'" in html
