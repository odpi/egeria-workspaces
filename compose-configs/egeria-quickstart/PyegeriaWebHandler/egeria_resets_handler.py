"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

The "last Egeria reset" panel's data: GET /api/admin/egeria-resets (admin only, read only).

Rows are written by the HOST-only CLI compose-configs/egeria-quickstart/bin/egeria-upgrade-reset
into Postgres coco_pharma.demo.egeria_resets (the schema demo.feedback uses; created by
docker-entrypoint-initdb.d/init_egeria.sql and again by the CLI). The Portal never writes it and
has no action that resets anything.

Absence is an answer, never an empty list:
- `state: "none"`      no row, or no table yet (the CLI creates it when it records): "No reset recorded
                        by egeria-upgrade-reset.";
- `state: "not read"`  the table could not be read (Postgres down, no permission), with the reason;
- `state: "read"`      the rows, newest first.
"""
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(tags=["egeria-resets"])

_COLUMNS = ("id", "started_at", "finished_at", "outcome", "operator", "host", "database", "old_digest",
            "new_digest", "old_image_id", "new_image_id", "backup_path", "backup_bytes", "backup_sha256",
            "heal", "verify", "steps", "state_dir")


def _admin(request: Request) -> None:
    from report_specs_handler import _is_admin_closed
    if not _is_admin_closed(request):
        raise HTTPException(status_code=403, detail="The reset history is for administrators.")


def _read(limit: int) -> list[dict]:
    """Rows newest first. Raises on any failure; the route turns that into `not read`."""
    from sqlalchemy import create_engine, text
    from demo_config import DEMO_DB_URL
    engine = create_engine(DEMO_DB_URL, pool_pre_ping=True)
    try:
        with engine.connect() as conn:
            rows = conn.execute(text(f"SELECT {', '.join(_COLUMNS)} FROM demo.egeria_resets "
                                     "ORDER BY started_at DESC, id DESC LIMIT :n"), {"n": limit}).mappings().all()
    finally:
        engine.dispose()
    out = []
    for r in rows:
        d = dict(r)
        for k in ("started_at", "finished_at"):
            d[k] = d[k].isoformat() if d.get(k) is not None else None
        out.append(d)
    return out


def resets_payload(limit: int = 20, reader=None) -> dict:
    try:
        rows = (reader or _read)(limit)
    except Exception as exc:  # noqa: BLE001
        reason = str(exc).splitlines()[0][:200] if str(exc) else type(exc).__name__
        if "egeria_resets" in str(exc) and "does not exist" in str(exc):
            # The CLI creates the table when it records a reset, so no table means none recorded.
            return {"state": "none", "rows": [],
                    "message": "No reset recorded by egeria-upgrade-reset (the table demo.egeria_resets does not exist yet)."}
        logger.info(f"egeria resets: not read: {reason}")
        return {"state": "not read", "reason": reason, "rows": None}
    if not rows:
        return {"state": "none", "message": "No reset recorded by egeria-upgrade-reset.", "rows": []}
    return {"state": "read", "latest": rows[0], "rows": rows}


@router.get("/api/admin/egeria-resets", summary="Egeria resets recorded by egeria-upgrade-reset (admin, read only)")
def egeria_resets(request: Request, limit: int = Query(20, ge=1, le=200)):
    _admin(request)
    return JSONResponse(resets_payload(limit))
