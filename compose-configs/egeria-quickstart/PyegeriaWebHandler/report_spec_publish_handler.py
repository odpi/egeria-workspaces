"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Publish a report spec to a tool's consumer folder, or withdraw it (BRIEF-SPEC-PUBLISH-STAGED-2026-11-12,
stage 2: the Portal's minimal control, PUBLIC specs only).

    POST /api/report-specs/publish
      {spec_name, action: "publish" | "withdraw", folder: <consumer name, e.g. "Portal">,
       step: "preview" | "validate" | "process", confirmed: bool, digest: str | null}

The documents, their checks and the digest refusal are pyegeria's own (`pyegeria.view.report_spec_publish`,
pyegeria >= 6.2.40, shared with Egeria Advisor): `Create`/`Update Report Spec` then `Add Member to
Collection` (never a Parent ID), or `Remove Member from Collection`. This handler supplies what is the
Portal's:

- **who**: the signed-in user's own token (X-Egeria-Token), never the Portal's service account; no
  token -> 401 in words. The document runs through Dr.Egeria in this process as that user (a client that
  holds the token and no password, egeria_auth.use_token), so Egeria records the real person and Egeria
  decides whether they may write the folder: its refusal is shown in its own words;
- **which folders**: the consumer folders the last sync found (report_spec_consumers.index()); if that
  index was not read, the control is refused, in words, rather than guessed;
- **which specs**: public only. Refused in words: a built-in spec ("built-ins come later, after
  consumer-folders phase 3"), and any spec this user can see held with zones ("restricted publish comes
  later, after the zone proof"). Withdraw needs a spec held in Egeria;
- **no stale overwrite**: an Update rebuilds the spec from the Portal's synced copy, so the live element
  is read first (as the user) and a newer version in Egeria refuses ("sync first");
- **afterwards**: a successful process drops this label's cached results and starts the existing
  report-spec sync (report_spec_sync.start), so "Used by" shows the change once it finishes.

Steps are pyegeria's: preview (the document, nothing sent), validate (Dr.Egeria's validate run), then
process, which needs `confirmed` and the previewed `digest`; the plan is rebuilt from the current state
and a different document is refused (the spec, or what Egeria holds, changed since the preview).
"""
from __future__ import annotations

import asyncio
import os
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel

router = APIRouter(tags=["report-spec-publish"])

ACTIONS = ("publish", "withdraw")
BUILTIN_LATER = ("'{label}' is a pyegeria built-in spec: built-ins are published later, after consumer-folders "
                 "phase 3 (a built-in is referenced, not copied, into Egeria).")
RESTRICTED_LATER = ("'{label}' is held in Egeria with zones ({zones}): restricted publish comes later, after the "
                    "zone proof. Nothing is changed.")
NOT_HELD = "'{label}' is not held in Egeria, so there is nothing to withdraw."
SIGN_IN = "Sign in to publish or withdraw a report spec: it runs as you, never as the Portal's service account."
NO_FOLDERS = ("The consumer folders were not read ({reason}), so there is nowhere to publish to yet. "
              "Run the report-spec sync, or wait: the Portal tries again every 2 minutes.")
PUBLISH_REFUSED_FALLBACK = "pyegeria refused the request (no reason was given)."
STALE = ("'{label}' changed in Egeria since the Portal's last sync (Egeria has version {live}, the Portal's copy "
         "is version {cached}). Publishing would write the older copy back: sync first, then publish.")


class PublishRequest(BaseModel):
    spec_name: str
    action: str = "publish"
    folder: str
    step: str = "preview"
    confirmed: bool = False
    digest: Optional[str] = None


class Refused(Exception):
    """A request the control will not run, with the words (and the HTTP status) to show. `message` is
    the only text a caller sees: written for users, never an exception's own text."""

    def __init__(self, words: str, status: int = 400):
        super().__init__(words)
        self.message = words
        self.status = status


def _reference() -> str:
    """A short id that ties a fixed message the user sees to the server log line with the details."""
    import secrets
    return secrets.token_hex(4)


# ── seams (replaced in tests) ─────────────────────────────────────────────────

def _publish_module():
    try:
        from pyegeria.view import report_spec_publish as rsp
    except ImportError:
        logger.exception("report spec publish: pyegeria.view.report_spec_publish could not be imported")
        raise Refused("Publishing needs pyegeria 6.2.40 or later (pyegeria.view.report_spec_publish).", 501)
    return rsp


def _consumers() -> Dict[str, Any]:
    import report_spec_consumers
    return report_spec_consumers.index()


def _registry() -> Dict[str, Any]:
    from pyegeria.view.base_report_formats import get_report_registry
    return get_report_registry()


def _source(name: str) -> Optional[Dict[str, Any]]:
    from report_specs_handler import spec_source_for
    return spec_source_for(name)


def _tier_info(label: str) -> Optional[Dict[str, Any]]:
    from pyegeria.view.egeria_spec_cache import egeria_tier_info
    return egeria_tier_info(label)


def _platform(token: str) -> str:
    """The platform this token may be used on (egeria_auth's one gate); raises PlatformRefused (401/400)."""
    from egeria_auth import default_platform_url, resolve_platform, token_platform
    return resolve_platform(token_platform(token) or default_platform_url(), token=token)


def _user_client(token: str):
    """A pyegeria client that acts only as the token's user: no password, so no silent re-login."""
    from pyegeria import EgeriaTech
    from egeria_auth import use_token
    url = _platform(token)
    server = os.environ.get("EGERIA_VIEW_SERVER", "qs-view-server")
    client = EgeriaTech(server, url, user_id=os.environ.get("EGERIA_USER", "erinoverview"))
    use_token(client, token)
    return client


def _restricted_reader(token: str):
    def read():
        from pyegeria.view.egeria_spec_cache import list_visible_restricted_specs
        return list_visible_restricted_specs(_user_client(token))
    return read


def _live_version(token: str, guid: str) -> Optional[int]:
    """The element's version in Egeria now, read as the user; None when it cannot be read."""
    found = _user_client(token).get_collection_by_guid(guid, output_format="JSON")
    el = found[0] if isinstance(found, list) and found else (found if isinstance(found, dict) else None)
    v = ((el or {}).get("elementHeader") or {}).get("versions", {}).get("version") if el else None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _run_as_user(token: str):
    """The runner pyegeria's run_document calls: run(markdown, directive) -> Dr.Egeria's result, as the
    signed-in user, in this process (the Portal's own Dr.Egeria API, without a temp file or a password)."""
    def run(markdown: str, directive: str) -> Dict[str, Any]:
        from md_processing.dr_egeria import setup_dispatcher
        from md_processing.v2 import UniversalExtractor
        from dr_egeria_commands_handler import _build_execute_response
        client = _user_client(token)
        commands = UniversalExtractor(markdown).extract_commands()
        if not commands:
            return {"success": False, "output": "No Dr.Egeria commands were found in the document.",
                    "execution_errors": [{"message": "no commands"}]}

        async def go():
            return await setup_dispatcher(client).dispatch_batch(commands, context={"directive": directive})

        results = asyncio.run(go())
        output = "\n\n".join(r["output"] for r in results if r.get("output"))
        return _build_execute_response({"output": output, "results": results}, directive)
    return run


def _after_success(label: str) -> Dict[str, Any]:
    """Drop this label's cached results and start the report-spec sync, so "Used by" catches up."""
    import report_spec_sync
    import report_specs_handler as rsh
    # the execute cache's keys start with the spec name, maybe tier-prefixed ("egeria:<label>@vN")
    dropped = rsh._RESULT_CACHE.drop(
        lambda key: isinstance(key, tuple) and bool(key) and str(key[0]).split(":", 1)[-1].split("@")[0] == label)
    started = report_spec_sync.start("publish")
    return {"resultsDropped": dropped, "syncStarted": started,
            "message": ("The report-spec sync has started; Used by shows the change when it finishes."
                        if started else "A report-spec sync is already running; Used by shows the change after "
                                        "it (or the next one) finishes.")}


# ── the plan ──────────────────────────────────────────────────────────────────

def _folder_qn(folder: str) -> tuple[str, List[str]]:
    idx = _consumers()
    if (idx.get("status") or "not read") == "not read":
        try:                                   # heal it for the next try (at most every 2 minutes)
            import report_spec_sync
            report_spec_sync.retry_if_index_not_read("not read")
        except Exception:  # noqa: BLE001
            pass
        raise Refused(NO_FOLDERS.format(reason=idx.get("reason") or "no reason given"), 409)
    names = {c.get("name"): c.get("qualifiedName") for c in idx.get("consumers") or [] if c.get("qualifiedName")}
    if folder not in names:
        raise Refused(f"'{folder}' is not one of the consumer folders the last sync found "
                      f"({', '.join(sorted(n for n in names if n)) or 'none'}).")
    return names[folder], [q for q in names.values() if q]


def _plan(req: PublishRequest, token: str) -> Dict[str, Any]:
    rsp = _publish_module()
    if req.action not in ACTIONS:
        raise Refused(f"The action must be publish or withdraw, not {req.action!r}.")
    name = (req.spec_name or "").strip()
    src = _source(name) or {}
    label = src.get("label") or name
    if src.get("source") == "builtin":
        raise Refused(BUILTIN_LATER.format(label=label))
    folder_qn, allowed = _folder_qn(req.folder)
    held = rsp.held_in_egeria(label, shared_tier=_tier_info, restricted_reader=_restricted_reader(token),
                              app="the Portal")
    if held.get("zones"):
        raise Refused(RESTRICTED_LATER.format(label=label, zones=", ".join(held["zones"])))
    if req.action == "withdraw":
        if not held.get("held"):
            raise Refused(NOT_HELD.format(label=label) + f" ({held.get('how')})")
        plan = rsp.build_withdraw_document(label, [folder_qn], allowed=allowed,
                                           allowed_words="the consumer folders the last sync found")
    else:
        fs = _registry().get(name) or _registry().get(label)
        if fs is None:
            raise Refused(f"No report spec named '{name}' is registered in the Portal.", 404)
        if held.get("held"):
            info = _tier_info(label) or {}
            if info.get("guid"):
                try:
                    live = _live_version(token, info["guid"])
                except HTTPException as exc:          # PlatformRefused: its own status and words
                    raise Refused(str(exc.detail), exc.status_code)
                except Exception:  # noqa: BLE001
                    ref = _reference()
                    logger.exception(f"report spec publish [{ref}]: the live version of {label!r} could not be read")
                    raise Refused(f"Could not read '{label}' in Egeria to check it is not newer than the "
                                  f"Portal's copy; nothing is changed (reference {ref}).", 502)
                cached = info.get("header_version")
                # pyegeria's cache records version 0 when it could not read one: that is unknown, not "0"
                if not isinstance(live, int) or live <= 0 or not isinstance(cached, int) or cached <= 0:
                    raise Refused(f"Could not tell whether '{label}' in Egeria is newer than the Portal's copy "
                                  f"(Egeria version {live}, the Portal's {cached}); nothing is changed.", 409)
                if live > cached:
                    raise Refused(STALE.format(label=label, live=live, cached=cached), 409)
        plan = rsp.build_publish_document(label, fs, folders=[folder_qn], visibility="public", held=held)
    return {**plan, "action": req.action, "folder": req.folder, "how": held.get("how")}


# ── the route ─────────────────────────────────────────────────────────────────

@router.post("/api/report-specs/publish",
             summary="Publish a report spec to a consumer folder, or withdraw it (as the signed-in user)")
def publish_spec(req: PublishRequest, request: Request):
    from egeria_auth import _token_expired, get_request_token
    token = get_request_token()
    try:
        if not token or _token_expired(token):
            raise Refused(SIGN_IN, 401)
        try:
            _platform(token)          # a token for another platform, or a refused URL: its own 401/400 and words
        except HTTPException as exc:
            raise Refused(str(exc.detail), exc.status_code)
        rsp = _publish_module()
        plan = _plan(req, token)
        out = rsp.run_document(plan, step=req.step, run=_run_as_user(token),
                               confirmed=req.confirmed, digest=req.digest)
    except Refused as exc:
        return JSONResponse({"refused": True, "message": exc.message}, status_code=exc.status)
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001 -- pyegeria's PublishRefused, or a run that failed
        if type(exc).__name__ == "PublishRefused":
            # pyegeria's refusal words are written for users (the shared helper's checks); nothing else is sent
            words = exc.args[0] if exc.args and isinstance(exc.args[0], str) else PUBLISH_REFUSED_FALLBACK
            return JSONResponse({"refused": True, "message": words}, status_code=400)
        ref = _reference()
        logger.exception(f"report spec publish [{ref}] failed")
        return JSONResponse({"refused": True, "reference": ref,
                             "message": f"Publishing failed in the Portal; the server log has the details "
                                        f"(reference {ref})."}, status_code=500)
    if out.get("after"):
        try:
            out["after"] = {**out["after"], **_after_success(out["label"])}
        except Exception:  # noqa: BLE001 -- the write happened; say the follow-up did not
            ref = _reference()
            logger.exception(f"report spec publish [{ref}]: the sync after {out.get('label')!r} could not start")
            out["after"] = {**out["after"], "syncStarted": False, "reference": ref,
                            "message": f"Done in Egeria, but the Portal could not start its sync (reference {ref})."}
    out.pop("held", None)
    return JSONResponse(out)
