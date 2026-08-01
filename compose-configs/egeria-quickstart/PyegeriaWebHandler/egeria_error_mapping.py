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
