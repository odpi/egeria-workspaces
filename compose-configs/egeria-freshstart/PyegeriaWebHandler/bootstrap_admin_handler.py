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
  GET  /api/bootstrap/batches           → discovered batches + current selection
  POST /api/bootstrap/batches/selection → save selection (admin only)
  POST /api/bootstrap/batches/{id}/run  → run one batch now, its enabled files (admin only)
"""

from fastapi import APIRouter, HTTPException, Request
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


@router.post("/batches/{batch_id}/run", summary="Run one batch now (admin only)")
async def run_batch_now(batch_id: str, request: Request):
    _admin_gate(request)
    batches = {b["id"]: b for b in bb.batches_with_selection()}
    batch = batches.get(batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail=f"Batch {batch_id!r} not found")

    files = [f["name"] for f in batch["files"] if f["enabled"]]
    if not files:
        raise HTTPException(status_code=400, detail=f"Batch {batch_id!r} has no enabled files to run")

    logger.info(f"bootstrap batches: manually running {batch_id!r} ({len(files)} files)")
    results = await bb.run_batch({**batch, "files": files})
    ok = all(r["status"] == "ok" for r in results)
    return JSONResponse({"batch": batch_id, "success": ok, "results": results})
