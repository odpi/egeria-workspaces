"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Shared mapping from pyegeria exceptions to FastAPI HTTPException status codes.

Found via Schemathesis (2026-07-31, first run against the "collections" and
"projects" tags): every handler's blanket `except Exception: raise
HTTPException(500, ...)` was turning legitimate upstream 401s and 404s into
opaque 500s — e.g. an unknown/malformed guid produces a genuine "entity not
found" from Egeria (OMAG-REPOSITORY-HANDLER-404-007, relatedHTTPCode=404),
but the handler had no way to tell that apart from a real server bug.

This mirrors the pattern already established in operations_handler.py's
`_raise_http` (see that file's module docstring / CLAUDE.md), but is driven
by pyegeria's actual typed exception hierarchy
(pyegeria.core._exceptions) instead of string-matching, which is more
reliable — verified against pyegeria's source (_base_server_client.py):

  - PyegeriaTimeoutException            -> the request timed out
  - PyegeriaConnectionException         -> couldn't reach the Egeria platform
  - PyegeriaInvalidParameterException   -> client-supplied params were malformed
  - PyegeriaClientException            -> real HTTP error status from httpx
                                           (.response_code / .http_status_code
                                           carries the actual code, e.g. 401)
  - PyegeriaAPIException                -> Egeria wraps errors in HTTP 200
                                           responses; .related_http_code carries
                                           the semantic status (401/403/404/…)
  - ValueError (incl. pydantic's
    ValidationError, a ValueError
    subclass)                           -> caller-supplied param pyegeria/pydantic
                                           itself rejected while building the
                                           request (e.g. a malformed as_of_time
                                           string) -> 400, not our bug
  - httpx.InvalidURL                    -> caller-supplied param (e.g. a
                                           non-printable character in
                                           server/user_id) produced an
                                           unbuildable request URL -> 400
  - PyegeriaException (base class —
    catches PyegeriaUnknownException
    and any other subtype not
    explicitly enumerated above)        -> use .response_code/.http_status_code
                                           if usable, else 502 (something in the
                                           Egeria round-trip failed, but not one
                                           of the specific shapes above)
  - anything else                       -> genuinely unexpected -> 500
"""

from fastapi import HTTPException
from loguru import logger

# Shared `responses=` dict for routes using raise_egeria_http_error — pass to
# @router.get(..., responses=EGERIA_ERROR_RESPONSES) so the OpenAPI spec
# documents what this mapper can actually return (kept in sync with the
# status codes raised below).
EGERIA_ERROR_RESPONSES = {
    400: {"description": "Malformed request parameters (e.g. invalid platform URL)"},
    401: {"description": "Egeria rejected the supplied credentials"},
    404: {"description": "The requested element does not exist"},
    502: {"description": "Could not reach the Egeria platform, or Egeria returned an unmapped error"},
    504: {"description": "Egeria did not respond in time"},
}


def raise_egeria_http_error(exc: Exception, log_msg: str = "") -> None:
    """Re-raise a pyegeria exception as the correct FastAPI HTTPException.

    Always raises — never returns normally. Call from an `except Exception as
    exc:` block: `raise_egeria_http_error(exc, "some context")`.
    """
    if log_msg:
        logger.exception(log_msg)

    try:
        from pyegeria.core._exceptions import (
            PyegeriaAPIException,
            PyegeriaClientException,
            PyegeriaConnectionException,
            PyegeriaException,
            PyegeriaInvalidParameterException,
            PyegeriaTimeoutException,
        )
    except ImportError:
        # pyegeria's exception module moved/renamed — fall back to 500 rather
        # than crash the crash-handler.
        raise HTTPException(status_code=500, detail=str(exc))

    if isinstance(exc, PyegeriaTimeoutException):
        raise HTTPException(
            status_code=504,
            detail="Egeria did not respond in time — the server may be busy. Try again in a moment.",
        )

    if isinstance(exc, PyegeriaConnectionException):
        raise HTTPException(
            status_code=502,
            detail="Could not reach the Egeria platform — check the platform URL and that it is running.",
        )

    if isinstance(exc, PyegeriaInvalidParameterException):
        raise HTTPException(status_code=400, detail=str(getattr(exc, "message", exc)))

    if isinstance(exc, PyegeriaClientException):
        code = getattr(exc, "response_code", None) or getattr(exc, "http_status_code", None)
        code = code if isinstance(code, int) and 400 <= code < 600 else 502
        raise HTTPException(status_code=code, detail=str(getattr(exc, "message", exc)))

    if isinstance(exc, PyegeriaAPIException):
        code = getattr(exc, "related_http_code", None)
        code = code if isinstance(code, int) and 400 <= code < 600 else 502
        raise HTTPException(status_code=code, detail=str(getattr(exc, "message", exc)))

    if isinstance(exc, ValueError):
        # e.g. pydantic ValidationError building a request body from a
        # caller-supplied param (a malformed as_of_time string, etc.) —
        # the caller's fault, not ours.
        raise HTTPException(status_code=400, detail=str(exc))

    import httpx

    if isinstance(exc, httpx.InvalidURL):
        # e.g. a non-printable character in a caller-supplied server/user_id
        # param makes the resulting request URL unbuildable.
        raise HTTPException(status_code=400, detail=f"Invalid request parameters: {exc}")

    if isinstance(exc, PyegeriaException):
        # Catches PyegeriaUnknownException and anything else in the pyegeria
        # exception hierarchy not explicitly enumerated above — still an
        # Egeria round-trip failure, not one of our own bugs.
        code = getattr(exc, "response_code", None) or getattr(exc, "http_status_code", None)
        code = code if isinstance(code, int) and 400 <= code < 600 else 502
        raise HTTPException(status_code=code, detail=str(exc))

    raise HTTPException(status_code=500, detail=str(exc))


def _is_auth_error(exc: Exception) -> bool:
    """Return True if exc represents a 401/403 from Egeria (expired token /
    access denied). Shared copy of operations_handler.py's own helper of the
    same name — that one predates this module and is kept local there rather
    than retrofitted to import this, to avoid an unrelated diff; new callers
    should use this one."""
    seen = set()
    node = exc
    while node is not None and id(node) not in seen:
        seen.add(id(node))
        code = getattr(node, "response_code", None) or getattr(node, "http_status_code", None)
        if code in (401, 403):
            return True
        resp = getattr(node, "response", None)
        if resp is not None and getattr(resp, "status_code", None) in (401, 403):
            return True
        s = str(node).upper()
        if ("HTTP CODE: 401" in s or "HTTP CODE: 403" in s
                or "USER_NOT_AUTHORIZED" in s or "NOT_AUTHORIZED" in s
                or "AUTHORIZATION_ERROR" in s or "401 " in s
                or "CLIENT ERROR '401" in s or "CLIENT ERROR '403" in s):
            return True
        node = getattr(node, "__cause__", None) or getattr(node, "__context__", None)
    return False


def describe_bulk_item_error(exc: Exception) -> str:
    """Friendly one-line message for a single failed item in a partial-failure-
    tolerant bulk endpoint (collections/zones/classifications' `{added|removed,
    failed}` shape) -- NOT a raise_egeria_http_error() call, since one bad guid
    in a batch of N shouldn't abort the other N-1.

    Specifically distinguishes "you don't have permission" from other
    failures, so a permission-denied result reads as a clear, actionable
    message in the UI rather than a raw pyegeria exception dump. This is the
    intended way to handle authorization for bulk governance actions (zone
    membership, classification) -- let Egeria's own enforcement deny the real
    request and surface a clean message, rather than pre-testing whether a
    persona *would* be allowed to before offering the action. Pre-testing was
    tried once during design (governance_classifications_handler.py's
    authorization question, 2026-08-16) by actually setting/clearing a
    classification as several personas including non-privileged ones --
    caught after the fact: Egeria's classification versions carry `createdBy`/
    `updatedBy`, so those test calls are now permanently attributed to those
    personas in Egeria's own audit trail, which is exactly the kind of
    integrity problem this tool exists to help govern. Don't repeat that
    pattern -- this function is the fix.

    Categorical dispatch only (CodeQL Medium: py/stack-trace-exposure, added
    2026-09-03) -- every branch below returns a fixed string chosen by the
    exception's *type*, never by reading its message/args/str(exc). That's
    deliberate: this return value reaches the client directly (the bulk
    endpoint's `failed[].error` field), and a pyegeria/httpx exception's text
    can carry internal detail (qualified names, host info, raw HTTP bodies)
    that doesn't belong in a public response. The caller already logs the
    real exception via `logger.debug(...)` right before calling this, so
    nothing is lost -- just not echoed back over HTTP.
    """
    if _is_auth_error(exc):
        return "You don't have permission to do this."

    try:
        from pyegeria.core._exceptions import (
            PyegeriaAPIException,
            PyegeriaClientException,
            PyegeriaConnectionException,
            PyegeriaException,
            PyegeriaInvalidParameterException,
            PyegeriaTimeoutException,
        )
    except ImportError:
        return "Operation failed for this item -- see server logs for details."

    if isinstance(exc, PyegeriaTimeoutException):
        return "Egeria did not respond in time for this item."
    if isinstance(exc, PyegeriaConnectionException):
        return "Could not reach the Egeria platform."
    if isinstance(exc, (PyegeriaInvalidParameterException, ValueError)):
        return "Invalid parameters for this item."
    if isinstance(exc, (PyegeriaClientException, PyegeriaAPIException, PyegeriaException)):
        return "Egeria rejected this item -- see server logs for details."

    return "Operation failed for this item -- see server logs for details."
