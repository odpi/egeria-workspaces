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

Docker access goes through the docker-proxy sidecar (DOCKER_HOST=tcp://docker-proxy:2375,
see egeria-quickstart-demo.yaml), which only allows inspect/stop/start of the Egeria
container. The raw socket is deliberately not mounted into this internet-facing app.
"""

import asyncio
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
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

# Indexes the demo adds to Egeria's metadata store. Egeria's JDBC repository
# only indexes entity on (instance_guid, version) and type_name, and finds an
# element's current version with "instance_guid = ? and version_end_time is
# null". The watchdog's award-karma-points requests write a new version of a
# ContributionRecord on every change -- one record reached ~200k versions in a
# day -- so for those guids the planner falls back to a parallel seq scan of
# the whole table (~100 ms each), and Postgres CPU climbs all day until the
# nightly reset. A partial index on the current versions makes that lookup
# ~0.2 ms. DROP SCHEMA in the reset removes it, and Egeria only recreates the
# tables after it restarts, so _ensure_store_indexes() re-adds it from the
# scheduler loop once the table is back (this also covers redeploys and fresh
# stores). Remove when Egeria indexes this itself.
_STORE_INDEXES = {
    "entity_current_guid_idx":
        "ON {schema}.entity (instance_guid) WHERE version_end_time IS NULL",
}

# Every reset lifecycle line below is logged at INFO, but pyegeria's
# config_logging() runs at import time, removes loguru's default sink and
# leaves the console sink at ERROR -- so those lines land only in
# /app/logs/pyegeria.log.  A nightly reset that stops the Egeria container and
# drops the metadata store schema therefore left no trace in
# `docker logs quickstart-pyegeria-web`, which is exactly where someone looks
# when the platform appears to have died.  Attach a small stderr sink scoped to
# this module so the reset narrates itself there too, without raising the
# console level for every other handler.
_console_sink_id: Optional[int] = None


def _ensure_console_sink() -> None:
    """Idempotently attach an INFO stderr sink for this module's records only.

    Called from start_scheduler() and _run_reset() rather than at import time:
    both run after pyegeria's config_logging(), whose logger.remove() would
    otherwise drop a sink added here on import.
    """
    global _console_sink_id
    if _console_sink_id is not None:
        return
    _console_sink_id = logger.add(
        sys.stderr,
        level="INFO",
        filter=lambda record: record["name"] == __name__,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <7} | demo-reset | {message}",
    )


# Marker the container watchdog (watchdog/watch-egeria.sh) reads to tell this
# reset's deliberate SIGTERM apart from a real crash.  Without it every nightly
# reset emails an "Egeria down: exited (code 143)" alert, which just trains the
# reader to ignore the one that eventually matters.  Epoch seconds rather than
# ISO-8601 so the watchdog's busybox `sh` can compare it with plain integer
# arithmetic.  Written immediately before the container stop and deliberately
# never deleted: the watchdog honours it only within its own grace window, so a
# stale marker ages out by itself instead of masking a later real crash.
_RESET_MARKER = Path(os.environ.get("DEMO_RESET_MARKER", "/app/demo-data/reset-marker"))


def _write_reset_marker() -> None:
    try:
        _RESET_MARKER.parent.mkdir(parents=True, exist_ok=True)
        _RESET_MARKER.write_text(f"{int(time.time())}\n")
    except OSError as exc:
        # Never let a marker failure block the reset itself -- the only
        # consequence is one spurious watchdog alert.
        logger.warning(f"Could not write reset marker {_RESET_MARKER}: {exc}")


# ── Lifecycle ──────────────────────────────────────────────────────────────────

async def start_scheduler() -> None:
    global _scheduler_task
    _ensure_console_sink()
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
        if not _reset_lock.locked():
            try:
                await asyncio.get_event_loop().run_in_executor(None, _ensure_store_indexes)
            except Exception as exc:
                logger.error(f"Store index check failed: {exc}")


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
    anchor = None
    if last_str:
        try:
            last = datetime.fromisoformat(last_str)
            due = last + timedelta(hours=interval_hours)
            now = datetime.utcnow()
            if now < due:
                return
            # Record the slot that was due, not when the reset finished, so the
            # schedule keeps its time of day instead of creeping later by the
            # reset's duration every cycle. A slot missed by more than a whole
            # interval (platform down for days) re-anchors on now.
            if now - due < timedelta(hours=interval_hours):
                anchor = due
        except ValueError:
            pass
    logger.info(f"Scheduled reset triggered (interval={interval_hours}h)")
    asyncio.create_task(_run_reset(anchor))


# ── Reset execution ────────────────────────────────────────────────────────────

async def _run_reset(anchor: datetime | None = None) -> None:
    _ensure_console_sink()
    if _reset_lock.locked():
        logger.warning("Reset already in progress — skipping duplicate trigger")
        return
    async with _reset_lock:
        logger.info("Demo environment reset starting")
        set_config("reset_state", "resetting")
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, _do_reset_blocking)
            set_config("last_reset_at", (anchor or datetime.utcnow()).isoformat())
            logger.info("Demo environment reset complete — Egeria will finish initializing in ~5 min")
        except Exception as exc:
            logger.error(f"Demo reset failed: {exc}")
            raise
        finally:
            set_config("reset_state", "ready")


_DOCKER_SOCKET = os.environ.get("DOCKER_HOST", "unix:///var/run/docker.sock")


def _do_reset_blocking() -> None:
    """Blocking reset: stop container → drop schema → start container."""
    import docker  # imported here so the module loads even without docker SDK at startup
    try:
        client = docker.DockerClient(base_url=_DOCKER_SOCKET)
        client.ping()  # verify connectivity before proceeding
    except Exception as exc:
        raise RuntimeError(
            f"Cannot reach Docker daemon at {_DOCKER_SOCKET!r}: {exc}. "
            "Ensure the docker-proxy service is running (egeria-quickstart-demo.yaml)."
        ) from exc

    # Address the container by NAME via the low-level API (not the high-level
    # Container object, which switches to the container ID): the docker-proxy
    # sidecar allow-lists these calls by container name only.
    logger.info(f"Stopping container: {EGERIA_CONTAINER_NAME}")
    try:
        client.api.inspect_container(EGERIA_CONTAINER_NAME)
    except docker.errors.NotFound:
        raise RuntimeError(f"Container '{EGERIA_CONTAINER_NAME}' not found — check EGERIA_CONTAINER_NAME env var")
    _write_reset_marker()
    client.api.stop(EGERIA_CONTAINER_NAME, timeout=60)
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
    client.api.start(EGERIA_CONTAINER_NAME)
    logger.info("Container started")


def _ensure_store_indexes() -> None:
    """Create any missing _STORE_INDEXES once Egeria has created its tables.

    Blocking; run in an executor. A no-op while the schema is absent (mid-reset,
    Egeria still starting) or the indexes already exist. CONCURRENTLY so Egeria
    keeps writing during the build; a build that fails that way leaves an
    INVALID index which IF NOT EXISTS would then skip forever, so drop it and
    let the next pass retry.
    """
    conn = psycopg2.connect(
        host=DEMO_DB_HOST,
        port=DEMO_DB_PORT,
        dbname=EGERIA_META_DB_NAME,
        user=EGERIA_META_DB_USER,
        password=EGERIA_META_DB_PASSWORD,
    )
    conn.autocommit = True  # CREATE INDEX CONCURRENTLY can't run in a transaction
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT to_regclass(%s)", (f"{_SCHEMA_TO_DROP}.entity",))
            if cur.fetchone()[0] is None:
                return
            for name, definition in _STORE_INDEXES.items():
                cur.execute(
                    "SELECT i.indisvalid FROM pg_index i"
                    " JOIN pg_class c ON c.oid = i.indexrelid"
                    " JOIN pg_namespace n ON n.oid = c.relnamespace"
                    " WHERE n.nspname = %s AND c.relname = %s",
                    (_SCHEMA_TO_DROP, name),
                )
                row = cur.fetchone()
                if row and row[0]:
                    continue
                if row:
                    logger.warning(f"Dropping invalid store index {name} to rebuild it")
                    cur.execute(f"DROP INDEX CONCURRENTLY IF EXISTS {_SCHEMA_TO_DROP}.{name}")
                started = time.monotonic()
                cur.execute(
                    f"CREATE INDEX CONCURRENTLY IF NOT EXISTS {name} "
                    + definition.format(schema=_SCHEMA_TO_DROP)
                )
                cur.execute(f"ANALYZE {_SCHEMA_TO_DROP}.entity")
                logger.info(f"Created store index {name} in {time.monotonic() - started:.1f}s")
    finally:
        conn.close()


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
