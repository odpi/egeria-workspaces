"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Schema-driven fuzzing (Schemathesis) against the FastAPI app's own
auto-generated OpenAPI spec — no hand-written test cases, no mocked backend.
Generates valid/boundary/invalid parameter combinations per endpoint and
checks for unhandled 5xxs.

Scope, deliberately narrow for this first slice: only the "collections" and
"projects" tags (GET endpoints only) — the two routers touched by the
2026-07-31 Collections-vs-Digital-Products routing fix. Widen `.include(...)`
below tag by tag as each new area gets its own error-mapping pass (see
egeria_error_mapping.py).

Assertion scope, deliberately narrow too: this only checks for unhandled 5xxs
(the actual bug class found and fixed here — every one of these 8 endpoints'
blanket `except Exception: raise HTTPException(500, ...)` was turning
legitimate upstream 401s/404s into opaque 500s; see egeria_error_mapping.py's
module docstring for the full story). Full `case.validate_response()` schema
conformance is NOT run here on purpose — first pass surfaced two more classes
of finding that are real but belong to a separate project, not this one:

  1. Undocumented status codes — the route decorators didn't declare 401/
     400/404/502/504 as possible responses (fixed here via
     `responses=EGERIA_ERROR_RESPONSES`, but the other ~196 endpoints in this
     app likely have the same gap).
  2. `RejectedPositiveData` — e.g. `url=null` (the literal string) is
     schema-compliant (an unconstrained string) but gets rejected with 400,
     because the `url`/`server`/etc. query params across these handlers are
     typed as plain `Optional[str]` with no `format`/`pattern` constraining
     them to look like an actual URL — so Schemathesis (rightly, given the
     schema as declared) expects it to be accepted.

Both are legitimate, but tightening every query-param schema across the API
is a distinct, larger project from "stop leaking 500s." Re-enable full
`case.validate_response()` once that pass happens.

Run (inside the quickstart-pyegeria-web container, where EGERIA_PLATFORM_URL
resolves): `pytest tests/test_schema_fuzz.py -v`
"""

import sys
from pathlib import Path

import schemathesis

_THIS_DIR = Path(__file__).resolve().parent
_MODULE_DIR = _THIS_DIR.parent
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import pyegeria_handler as handler  # type: ignore  # noqa: E402

schema = schemathesis.openapi.from_asgi("/openapi.json", handler.app).include(
    tag=["collections", "projects"], method="GET"
)


@schema.parametrize()
def test_no_unhandled_server_errors(case):
    response = case.call()
    # 500 specifically = raise_egeria_http_error's final, unmapped fallback —
    # a genuinely unhandled exception type. 502/503/504 are deliberate
    # gateway-style mappings raise_egeria_http_error uses for "the Egeria
    # round-trip itself failed" (timeout, unreachable, unmapped pyegeria
    # exception) and are not bugs in this app's own code.
    assert response.status_code != 500, (
        f"{case.operation.method.upper()} {case.operation.path} -> "
        f"{response.status_code}: {response.text[:500]}"
    )
