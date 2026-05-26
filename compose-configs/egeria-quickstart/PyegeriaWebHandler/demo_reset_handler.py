"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Demo reset — stops the Egeria platform container, drops the metadata store
schema from PostgreSQL, and restarts the container so Egeria re-seeds all
Coco Pharmaceuticals data from scratch.  End-user accounts are untouched.

Two modes:
  - Scheduled: a background asyncio task checks every 5 min whether the
    configured interval has elapsed and triggers a reset automatically.
  - Manual: POST /api/demo/reset (admin only) triggers an immediate reset.

Docker socket must be mounted into the container:
  /var/run/docker.sock:/var/run/docker.sock
"""

import asyncio
from datetime import datetime
from typing import Optional

import psycopg2
from fastapi import APIRouter, Depends, HTTPException, Request
from loguru import logger
from sqlalchemy.orm import Session

from demo_config import (
    DEMO_DB_HOST, DEMO_DB_PORT,
    EGERIA_CONTAINER_NAME,
    EGERIA_META_DB_NAME, EGERIA_META_DB_USER, EGERIA_META_DB_PASSWORD,
)
from demo_db import get_db, get_config, set_config
from demo_auth_handler import require_admin

router = APIRouter(tags=["demo-reset"])

_reset_lock = asyncio.Lock()
_scheduler_task: Optional[asyncio.Task] = None
_SCHEMA_TO_DROP = "repository_qs_metadata_store"
_SCHEDULER_INTERVAL_SEC = 300  # check every 5 minutes


# ── Lifecycle ──────────────────────────────────────────────────────────────────

async def start_scheduler() -> None:
    global _scheduler_task
    _scheduler_task = asyncio.create_task(_scheduler_loop())
    logger.info("Demo reset scheduler started")


async def stop_scheduler() -> None:
    global _scheduler_task
    if _scheduler_task and not _scheduler_task.done():
        _scheduler_task.cancel()
        try:
            await _scheduler_task
        except asyncio.CancelledError:
            pass
    _scheduler_task = None


# ── Scheduler ──────────────────────────────────────────────────────────────────

async def _scheduler_loop() -> None:
    while True:
        await asyncio.sleep(_SCHEDULER_INTERVAL_SEC)
        try:
            await _maybe_scheduled_reset()
        except Exception as exc:
            logger.error(f"Reset scheduler error: {exc}")


async def _maybe_scheduled_reset() -> None:
    try:
        interval_hours = float(get_config("reset_interval_hours", "0") or "0")
    except ValueError:
        return
    if interval_hours <= 0:
        return
    if get_config("reset_state", "ready") == "resetting":
        return
    last_str = get_config("last_reset_at", "")
    if last_str:
        try:
            last = datetime.fromisoformat(last_str)
            elapsed_h = (datetime.utcnow() - last).total_seconds() / 3600
            if elapsed_h < interval_hours:
                return
        except ValueError:
            pass
    logger.info(f"Scheduled reset triggered (interval={interval_hours}h)")
    asyncio.create_task(_run_reset())


# ── Reset execution ────────────────────────────────────────────────────────────

async def _run_reset() -> None:
    if _reset_lock.locked():
        logger.warning("Reset already in progress — skipping duplicate trigger")
        return
    async with _reset_lock:
        logger.info("Demo environment reset starting")
        set_config("reset_state", "resetting")
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, _do_reset_blocking)
            set_config("last_reset_at", datetime.utcnow().isoformat())
            logger.info("Demo environment reset complete — Egeria will finish initializing in ~5 min")
        except Exception as exc:
            logger.error(f"Demo reset failed: {exc}")
            raise
        finally:
            set_config("reset_state", "ready")


def _do_reset_blocking() -> None:
    """Blocking reset: stop container → drop schema → start container."""
    import docker  # imported here so the module loads even without docker SDK at startup
    client = docker.from_env()

    logger.info(f"Stopping container: {EGERIA_CONTAINER_NAME}")
    try:
        container = client.containers.get(EGERIA_CONTAINER_NAME)
    except docker.errors.NotFound:
        raise RuntimeError(f"Container '{EGERIA_CONTAINER_NAME}' not found — check EGERIA_CONTAINER_NAME env var")
    container.stop(timeout=60)
    logger.info("Container stopped")

    logger.info(f"Dropping schema {_SCHEMA_TO_DROP} from {EGERIA_META_DB_NAME}")
    conn = psycopg2.connect(
        host=DEMO_DB_HOST,
        port=DEMO_DB_PORT,
        dbname=EGERIA_META_DB_NAME,
        user=EGERIA_META_DB_USER,
        password=EGERIA_META_DB_PASSWORD,
    )
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute(f"DROP SCHEMA IF EXISTS {_SCHEMA_TO_DROP} CASCADE")
        logger.info("Schema dropped")
    finally:
        conn.close()

    logger.info(f"Starting container: {EGERIA_CONTAINER_NAME}")
    container.start()
    logger.info("Container started")


# ── API routes ─────────────────────────────────────────────────────────────────

@router.get("/api/demo/reset/status")
async def reset_status(
    request: Request,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    return {
        "state":                 get_config("reset_state",         "ready"),
        "last_reset_at":         get_config("last_reset_at",        ""),
        "reset_interval_hours":  get_config("reset_interval_hours", "0"),
    }


@router.post("/api/demo/reset")
async def trigger_reset(
    request: Request,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    if get_config("reset_state", "ready") == "resetting":
        raise HTTPException(status_code=409, detail="Reset already in progress")
    asyncio.create_task(_run_reset())
    return {"status": "reset_started"}
