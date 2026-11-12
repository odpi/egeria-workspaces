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

GET /api/admin/infra-health (admin only, read only) is the "Shared infrastructure" line beside it: the
latest row of demo.infra_checks, written on the HOST by `egeria-upgrade-reset infra-check --record`
(the Portal has no Docker socket and must not get one). A row older than 30 minutes is `stale` and
the page greys it ("last checked <time>: not current"), never green. With no row: `state: "none"`.
Separately, and labelled as a different fact, the Portal's own TCP reachability of the shared ports
now (it says nothing about restart policies).
"""
import datetime as _dt
import json
import socket
from typing import Optional

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


# ── Shared infrastructure ─────────────────────────────────────────────────────

INFRA_STALE_S = 30 * 60     # = egeria_upgrade_reset.INFRA_STALE_S
NEVER_CHECKED = "not checked yet (run `egeria-upgrade-reset infra-check --record` on the host)"
# The shared ports as the Portal's own container reaches them on egeria_network (shared-infra.yaml).
PORTAL_PORTS = (("postgres", "egeria-shared-postgres", 5442), ("kafka", "egeria-shared-kafka", 9192),
                ("openlineage proxy", "egeria-shared-openlineage-proxy-backend", 6000),
                ("kroki", "egeria-shared-kroki", 8000))


def _read_infra() -> Optional[dict]:
    """The newest demo.infra_checks row, or None. Raises on any failure (-> `not read`)."""
    from sqlalchemy import create_engine, text
    from demo_config import DEMO_DB_URL
    engine = create_engine(DEMO_DB_URL, pool_pre_ping=True)
    try:
        with engine.connect() as conn:
            row = conn.execute(text("SELECT checked_at, host, compose_files, result FROM demo.infra_checks "
                                    "ORDER BY checked_at DESC, id DESC LIMIT 1")).mappings().first()
    finally:
        engine.dispose()
    return dict(row) if row else None


def _probe(host: str, port: int, timeout: float = 1.0) -> Optional[str]:
    """None when a TCP connection opens, else why not."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return None
    except OSError as exc:
        return f"{type(exc).__name__}: {exc}"[:160]


def portal_reachability(probe=None, now=None) -> dict:
    probe = probe or _probe
    at = (now or _dt.datetime.now(_dt.timezone.utc)).isoformat()
    ports = []
    for name, host, port in PORTAL_PORTS:
        err = probe(host, port)
        ports.append({"name": name, "host": host, "port": port, "reachable": err is None, "error": err})
    return {"label": "reachable from the Portal now", "checkedAt": at, "ports": ports}


def _as_dt(v) -> Optional[_dt.datetime]:
    if v is None:
        return None
    if isinstance(v, _dt.datetime):
        return v if v.tzinfo else v.replace(tzinfo=_dt.timezone.utc)
    try:
        d = _dt.datetime.fromisoformat(str(v).replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=_dt.timezone.utc)
    except ValueError:
        return None


def infra_payload(reader=None, now=None, probe=None) -> dict:
    now = now or _dt.datetime.now(_dt.timezone.utc)
    out = {"staleAfterSeconds": INFRA_STALE_S, "reachability": portal_reachability(probe, now)}
    try:
        row = (reader or _read_infra)()
    except Exception as exc:  # noqa: BLE001
        reason = str(exc).splitlines()[0][:200] if str(exc) else type(exc).__name__
        if "infra_checks" in str(exc) and "does not exist" in str(exc):
            return {**out, "state": "none", "message": NEVER_CHECKED}
        logger.info(f"infra health: not read: {reason}")
        return {**out, "state": "not read", "reason": reason}
    if not row:
        return {**out, "state": "none", "message": NEVER_CHECKED}
    result = row.get("result")
    if isinstance(result, str):
        try:
            result = json.loads(result)
        except ValueError:
            result = None
    checked = _as_dt(row.get("checked_at"))
    age = (now - checked).total_seconds() if checked else None
    stale = age is None or age > INFRA_STALE_S
    return {**out, "state": "read", "checkedAt": checked.isoformat() if checked else None,
            "ageSeconds": None if age is None else round(age), "stale": stale, "host": row.get("host"),
            "result": result}


@router.get("/api/admin/infra-health", summary="Shared-infrastructure health recorded on the host (admin, read only)")
def infra_health(request: Request):
    _admin(request)
    return JSONResponse(infra_payload())
