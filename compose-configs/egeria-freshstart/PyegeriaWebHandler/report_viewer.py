"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Who is viewing a report spec execution.

pyegeria's exec_report_spec hands an analytic function only the spec's JSON
parameters, never the caller. A routine that has to act as the viewer
somewhere else (re_analytics.py calls Resource Explorer as them) reads the
viewer from this contextvar instead. report_specs_handler.execute_spec sets
it around the call; it is per request, so concurrent requests never see each
other's viewer.

The viewer is the persona the browser picked (localStorage['egeria-persona'])
and sent with the execute request, checked the same way the Portal's
Resource Explorer handoff checks it: in demo mode the Portal account must be
signed in and verified, and the persona must exist in personas.json. When any
of that fails, the viewer is still recorded, with `reason` saying why and no
persona, so a routine can say "not established" rather than fall back to a
default user.
"""

from contextvars import ContextVar
from typing import Optional

from fastapi import HTTPException, Request

_viewer: ContextVar[Optional[dict]] = ContextVar("report_viewer", default=None)


def current_viewer() -> Optional[dict]:
    """{"persona_id", "persona", "user", "reason"} for this request, or None when none was resolved."""
    return _viewer.get()


def resolve_viewer(request: Request, persona_id: Optional[str]) -> dict:
    if not persona_id:
        return {"persona_id": None, "persona": None, "user": None,
                "reason": "no persona was chosen in this browser"}
    try:
        from resource_explorer_handler import _load_personas, _require_verified_or_local
    except ImportError:
        return {"persona_id": None, "persona": None, "user": None,
                "reason": "this environment has no Resource Explorer handoff"}
    try:
        user = _require_verified_or_local(request)
    except HTTPException as exc:
        return {"persona_id": None, "persona": None, "user": None,
                "reason": f"the Portal account is not signed in ({exc.detail})"}
    persona = _load_personas().get(persona_id)
    if not persona:
        return {"persona_id": None, "persona": None, "user": user,
                "reason": f"persona {persona_id!r} is not known to this Portal"}
    return {"persona_id": persona_id, "persona": persona, "user": user, "reason": ""}


def set_viewer(viewer: Optional[dict]):
    return _viewer.set(viewer)


def reset_viewer(token) -> None:
    _viewer.reset(token)
