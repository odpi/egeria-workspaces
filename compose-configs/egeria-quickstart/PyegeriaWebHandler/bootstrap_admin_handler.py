"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Bootstrap batches — admin API. Lets an admin see every folder of Dr.Egeria
documents discovered under dr-egeria-inbox, choose which folders/files
should run at (re)initialization, and manually run a batch on demand.

See bootstrap_batches.py for the discovery/selection/run mechanics and the
storage-choice rationale (a local ~/.pyegeria JSON file, not the demo_auth
Postgres table -- freshstart has no Postgres wired up at all).

Endpoints:
  GET  /api/bootstrap/batches               → discovered batches + current selection
  GET  /api/bootstrap/log                   → tail of bootstrap.log (recent batch/auto-heal activity)
  GET  /api/bootstrap/log/issues            → tail of pyegeria.log, ERROR/WARNING only (dr_egeria's own detail)
  POST /api/bootstrap/batches/selection     → save selection (admin only)
  POST /api/bootstrap/batches/{id}/run      → start running one batch in the background (admin only)
  GET  /api/bootstrap/batches/{id}/run-status → poll the run started above
  POST /api/bootstrap/batches/run-all       → start running every enabled batch in the background (admin only)
  GET  /api/bootstrap/batches/run-all/run-status → poll the run-all started above

The run endpoints return immediately ({"started": true, ...}) rather than
blocking on the run -- see bootstrap_batches.py's "Background run + poll"
section for why (a run routinely outlasts Apache's ProxyPass timeout).
Clients poll the matching run-status endpoint for the outcome.
"""

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from loguru import logger

import bootstrap_batches as bb

router = APIRouter(prefix="/api/bootstrap", tags=["bootstrap-admin"])


def _admin_gate(request: Request):
    """Same reused demo/freshstart gate as operations_handler.py's
    connector/server admin actions -- see that module for why this can't be
    a demo_auth-only check (freshstart has no Postgres/demo_auth at all)."""
    try:
        from demo_feedback_handler import _is_admin
    except Exception:
        _is_admin = None
    if _is_admin is not None and not _is_admin(request):
        raise HTTPException(status_code=403, detail="This operation requires an administrator.")


@router.get("/log", summary="Recent bootstrap/auto-heal activity (tail of bootstrap.log)")
def get_log(lines: int = Query(200, ge=1, le=2000)):
    return JSONResponse({"lines": bb.tail_log(lines)})


@router.get("/log/issues", summary="Recent dr_egeria ERROR/WARNING lines (tail of pyegeria.log)")
def get_log_issues(lines: int = Query(200, ge=1, le=2000)):
    return JSONResponse({"lines": bb.tail_dr_egeria_issues(lines)})


@router.get("/batches", summary="List discovered bootstrap batches and their selection state")
def list_batches():
    return JSONResponse({"batches": bb.batches_with_selection()})


class BatchFileSelection(BaseModel):
    enabled: bool = True


class BatchSelection(BaseModel):
    enabled: bool = False
    files: dict[str, bool] = {}


class SaveSelectionRequest(BaseModel):
    selection: dict[str, BatchSelection]


@router.post("/batches/selection", summary="Save which batches/files are marked for (re)initialization (admin only)")
def save_batch_selection(req: SaveSelectionRequest, request: Request):
    _admin_gate(request)
    payload = {
        batch_id: {"enabled": sel.enabled, "files": sel.files}
        for batch_id, sel in req.selection.items()
    }
    bb.save_selection(payload)
    logger.info(f"bootstrap batches: selection saved for {list(payload.keys())}")
    return JSONResponse({"saved": True, "selection": payload})


@router.post("/batches/{batch_id}/run", summary="Start running one batch now in the background (admin only)")
async def run_batch_now(batch_id: str, request: Request, confirm: bool = Query(False)):
    _admin_gate(request)
    batches = {b["id"]: b for b in bb.batches_with_selection()}
    batch = batches.get(batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail=f"Batch {batch_id!r} not found")

    files = [f["name"] for f in batch["files"] if f["enabled"]]
    if not files:
        raise HTTPException(status_code=400, detail=f"Batch {batch_id!r} has no enabled files to run")

    # See bootstrap_batches.py's discover_batches() docstring: some commands
    # (confirmed live -- Link Governance Results) create a relationship/record
    # with no pre-existence check, so re-running against an already-seeded
    # target duplicates it. Auto-heal never hits this (canary-gated, only
    # runs when missing) -- this manual path needs its own gate instead.
    if not batch["idempotent"] and not confirm:
        raise HTTPException(
            status_code=409,
            detail=f"Batch {batch_id!r} contains a command known to duplicate data if re-run "
                    "against an already-seeded target. Pass ?confirm=true to run it anyway.",
        )

    logger.info(f"bootstrap batches: manually running {batch_id!r} ({len(files)} files)")
    started = bb.start_background(batch_id, bb.run_batch({**batch, "files": files}))
    return JSONResponse({"started": True, "already_running": not started})


@router.get("/batches/{batch_id}/run-status", summary="Poll the outcome of a batch run started via POST .../run")
def batch_run_status(batch_id: str, request: Request):
    _admin_gate(request)
    return JSONResponse(bb.run_status(batch_id))


@router.post("/batches/run-all", summary="Start running every enabled batch, in folder order, in the background (admin only)")
async def run_all_batches_now(request: Request, confirm: bool = Query(False)):
    _admin_gate(request)
    enabled = bb.enabled_batches()
    if not enabled:
        raise HTTPException(status_code=400, detail="No batches are enabled")

    non_idempotent = [b["id"] for b in enabled if not b["idempotent"]]
    if non_idempotent and not confirm:
        raise HTTPException(
            status_code=409,
            detail=f"These enabled batches contain a command known to duplicate data if re-run "
                    f"against an already-seeded target: {', '.join(non_idempotent)}. "
                    "Pass ?confirm=true to run everything anyway.",
        )

    logger.info(f"bootstrap batches: manually running all enabled batches ({[b['id'] for b in enabled]})")
    started = bb.start_background(bb.RUN_ALL_KEY, bb.run_all_enabled())
    return JSONResponse({"started": True, "already_running": not started})


@router.get("/batches/run-all/run-status", summary="Poll the outcome of a run-all started via POST .../run-all")
def run_all_status(request: Request):
    _admin_gate(request)
    return JSONResponse(bb.run_status(bb.RUN_ALL_KEY))
