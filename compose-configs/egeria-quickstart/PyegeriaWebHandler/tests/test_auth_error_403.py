"""ERR-403 (PO-9): an Egeria auth refusal is told apart by exception class and HTTP code, never by text.

A 401 means the sign-in was refused (a bad or expired token): the answer is 401 and "sign in again".
A 403 means the user is signed in and Egeria refused this request for them (a zone they cannot see):
the answer is 403 "Not permitted", because a new token changes nothing. Before this, operations,
audit, glossary and The Catalog's handlers answered every auth error with 401 "session expired" (and
the Explorer's 401 refresher then minted a token that could not help), and matched on message text, so
"HTTP CODE: 403" or "401 " anywhere in a message read as a sign-in problem.

The exceptions here are pyegeria's own (6.2.34+ raises Egeria's 403 as PyegeriaUnauthorizedException with
related_http_code 403, AUTHORIZATION_ERROR_403), built from the response shapes pyegeria builds them from.
Each route-level case asserts what the browser receives: the status and the detail."""
import shutil
import subprocess
import sys
from pathlib import Path

import httpx
import pytest
from fastapi import HTTPException

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

pytest.importorskip("pyegeria.core._exceptions")
from pyegeria.core._exceptions import (  # noqa: E402
    PyegeriaAPIException, PyegeriaClientException, PyegeriaUnauthorizedException,
)

import egeria_error_mapping as em  # noqa: E402

REQ = httpx.Request("POST", "https://egeria.test:9443/servers/v/api/open-metadata/x")


def _forbidden():
    """Egeria's own 403: UserNotAuthorizedException, an element in a zone the user cannot see."""
    body = {"relatedHTTPCode": 403, "exceptionClassName": "org.odpi.openmetadata.UserNotAuthorizedException",
            "exceptionErrorMessageId": "OPEN-METADATA-SECURITY-403-020",
            "exceptionErrorMessage": "OPEN-METADATA-SECURITY-403-020 the element is not visible to peterprofile"}
    return PyegeriaUnauthorizedException(httpx.Response(200, request=REQ, json=body), {},
                                         additional_info={**body, "userid": "peterprofile"})


def _expired():
    """A transport 401: the bearer token was refused."""
    return PyegeriaUnauthorizedException(httpx.Response(401, request=REQ, text="token expired"), {},
                                         additional_info={"userid": "peterprofile"})


def _has_dependents():
    """relatedHTTPCode 403 that is NOT an auth failure (an InvalidParameterException, ISSUE-142)."""
    body = {"relatedHTTPCode": 403, "exceptionClassName": "org.odpi.openmetadata.InvalidParameterException",
            "exceptionErrorMessageId": "OMAG-GENERIC-HANDLERS-403-005",
            "exceptionErrorMessage": "OMAG-GENERIC-HANDLERS-403-005 the element still has dependents"}
    return PyegeriaAPIException(httpx.Response(200, request=REQ, json=body), {}, additional_info=body)


def _wire(code):
    return PyegeriaClientException(httpx.Response(code, request=REQ, text="refused"), {}, {"userid": "p"})


# ── the classifier ───────────────────────────────────────────────────────────

def test_egerias_403_is_403():
    assert em.auth_error_status(_forbidden()) == 403


def test_a_refused_token_is_401():
    assert em.auth_error_status(_expired()) == 401


def test_a_wire_status_is_read_by_code():
    assert em.auth_error_status(_wire(403)) == 403
    assert em.auth_error_status(_wire(401)) == 401
    assert em.auth_error_status(_wire(500)) is None


def test_a_403_that_is_not_authorization_is_not_an_auth_error():
    assert em.auth_error_status(_has_dependents()) is None


def test_text_alone_is_never_an_auth_error():
    for words in ("HTTP CODE: 403 AUTHORIZATION_ERROR_403", "USER_NOT_AUTHORIZED", "got 401 from the proxy",
                  "Client error '401 Unauthorized'"):
        assert em.auth_error_status(RuntimeError(words)) is None, words


def test_the_cause_chain_is_followed():
    try:
        try:
            raise _forbidden()
        except Exception as inner:
            raise RuntimeError("wrapped") from inner
    except RuntimeError as outer:
        assert em.auth_error_status(outer) == 403


def test_the_portals_own_http_exceptions_keep_their_status():
    assert em.auth_error_status(HTTPException(status_code=401, detail="x")) == 401
    assert em.auth_error_status(HTTPException(status_code=403, detail="x")) == 403
    assert em.auth_error_status(HTTPException(status_code=500, detail="x")) is None


def test_auth_http_exception_words():
    assert (em.auth_http_exception(_forbidden()).status_code, em.auth_http_exception(_forbidden()).detail) == \
        (403, em.AUTH_403_DETAIL)
    assert em.AUTH_403_DETAIL.startswith("Not permitted")
    assert (em.auth_http_exception(_expired(), "custom").status_code,
            em.auth_http_exception(_expired(), "custom").detail) == (401, "custom")


def test_raise_if_auth_error():
    with pytest.raises(HTTPException) as ei:
        em.raise_if_auth_error(_forbidden())
    assert ei.value.status_code == 403 and ei.value.detail == em.AUTH_403_DETAIL
    with pytest.raises(HTTPException) as ei:
        em.raise_if_auth_error(_expired())
    assert ei.value.status_code == 401
    assert em.raise_if_auth_error(_has_dependents()) is None
    assert em.raise_if_auth_error(RuntimeError("HTTP CODE: 403")) is None


# ── the handlers that answered every auth error with 401 ─────────────────────

@pytest.mark.parametrize("module", ["glossary_handler", "operations_handler"])
def test_raise_http_tells_403_from_401(module):
    mod = __import__(module)
    with pytest.raises(HTTPException) as ei:
        mod._raise_http(_forbidden())
    assert (ei.value.status_code, ei.value.detail) == (403, em.AUTH_403_DETAIL)
    with pytest.raises(HTTPException) as ei:
        mod._raise_http(_expired())
    assert ei.value.status_code == 401 and "reconnect" in ei.value.detail
    with pytest.raises(HTTPException) as ei:
        mod._raise_http(_has_dependents())
    assert ei.value.status_code == 500


def test_the_handlers_use_the_shared_classifier():
    import glossary_handler, operations_handler, tech_catalog_handler
    for mod in (glossary_handler, operations_handler, tech_catalog_handler):
        assert mod._is_auth_error is em._is_auth_error, mod.__name__


def test_tech_catalog_cached_list_error_keeps_its_kind():
    import tech_catalog_handler as tc
    for kind, status in (("Not permitted", 403), ("Unauthorized", 401), ("boom", 500)):
        tc._da_errors["k-po9"] = kind
        with pytest.raises(HTTPException) as ei:
            tc._cached_list_response("k-po9", "label", False, None, None)
        assert ei.value.status_code == status, kind
        if status == 403:
            assert ei.value.detail == em.AUTH_403_DETAIL


def test_tech_catalog_routes_answer_403_for_egerias_403():
    src = (ROOT / "tech_catalog_handler.py").read_text()
    assert "raise HTTPException(status_code=401, detail=str(exc))" not in src
    assert src.count("raise auth_http_exception(exc,") == 9


def test_audit_passes_auth_errors_through():
    src = (ROOT / "audit_handler.py").read_text()
    assert src.count("raise_if_auth_error(exc)") == 6
    assert '"AUTHORIZATION_ERROR" in s' not in src


# ── local dashboards: the refusal label ──────────────────────────────────────

def test_refusal_label_says_not_permitted_for_403():
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    import re
    html = (ROOT / "local-dashboards.html").read_text()
    fn = re.search(r"function refusalLabel\(status\) \{.*?\n\}\n", html, re.S).group(0)
    js = fn + "console.log(JSON.stringify([refusalLabel(403), refusalLabel(401)]));"
    out = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == '["Not permitted","Sign-in needed"]'


# ── the report-spec execute route, type system, lineage ──────────────────────

@pytest.mark.parametrize("exc,status", [(_forbidden, 403), (_expired, 401)])
def test_execute_route_tells_403_from_401(monkeypatch, exc, status):
    import types
    import pyegeria.view.format_set_executor as fse
    import report_specs_handler as rsh
    from egeria_auth import TOKEN_REFUSED_WORDS

    def boom(*a, **k):
        raise exc()
    monkeypatch.setattr(fse, "exec_report_spec", boom)
    req = types.SimpleNamespace(spec_name="Any Spec", output_format="REPORT", params={}, table_shape=None)
    with pytest.raises(HTTPException) as ei:
        rsh._run_spec(req, None, None, "https://egeria.test:9443", "qs-view-server", "u", None)
    assert ei.value.status_code == status
    assert ei.value.detail == (em.AUTH_403_DETAIL if status == 403 else TOKEN_REFUSED_WORDS)


def test_execute_route_text_alone_is_not_401(monkeypatch):
    import types
    import pyegeria.view.format_set_executor as fse
    import report_specs_handler as rsh

    def boom(*a, **k):
        raise RuntimeError("HTTP Code: 401 somewhere in the words")
    monkeypatch.setattr(fse, "exec_report_spec", boom)
    req = types.SimpleNamespace(spec_name="Any Spec", output_format="REPORT", params={}, table_shape=None)
    with pytest.raises(HTTPException) as ei:
        rsh._run_spec(req, None, None, "https://egeria.test:9443", "qs-view-server", "u", None)
    assert ei.value.status_code == 500


def test_no_text_matching_is_left():
    for name in ("report_specs_handler.py", "report_spec_restricted.py", "type_system_handler.py",
                 "lineage_handler.py", "local_dashboards_handler.py", "glossary_handler.py",
                 "operations_handler.py", "tech_catalog_handler.py", "audit_handler.py"):
        src = (ROOT / name).read_text()
        for needle in ('"HTTP Code: 401" in', '"AUTHORIZATION_ERROR" in', '"NOT_AUTHORIZED" in', '"401 " in',
                       'http_error_code", None) == 401'):
            assert needle not in src, (name, needle)
    assert (ROOT / "type_system_handler.py").read_text().count("raise auth_http_exception(exc,") == 3
    assert (ROOT / "lineage_handler.py").read_text().count("raise auth_http_exception(exc,") == 2
