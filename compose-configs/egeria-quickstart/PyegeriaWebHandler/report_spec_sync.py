"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Report specs held in Egeria, synced into the Portal (RS-EGERIA-TIER, Portal adoption).

pyegeria's registry has an EGERIA tier that it reads from a local cache. Only
`sync_report_specs` fills that cache, from the CollectionFolders named in
`PYEGERIA_REPORT_SPEC_FOLDERS` (or config.json's "Pyegeria Report Spec Folders"). This module
runs that sync for the Portal:

- at startup, in a daemon thread, after a short delay. The Egeria platform starts after the
  Portal, so a failed attempt (Egeria not up yet) is retried a few times. Startup never waits
  for it. Set PORTAL_REPORT_SPEC_SYNC_AT_STARTUP=0 to turn this off.
- on demand, from the admin "Sync from Egeria" button in Egeria Explorer's Report Specs view
  (POST /api/report-specs/sync).

The sync runs as the Portal's service identity (EGERIA_USER), not as the signed-in viewer,
because the cache is shared by everyone who uses this Portal. It marks the cache `shared`, so
a fetch-on-call (`refresh_spec=True`) never writes into it.

Reads Egeria only. It never writes to Egeria.

The sync is sync pyegeria (it calls run_until_complete internally), so it runs only in its own
thread with its own client, never on the event loop (same rule as
collections_handler.warm_roots_cache).
"""

from __future__ import annotations

import os
import threading
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from loguru import logger

_STARTUP_DELAY_S = float(os.environ.get("PORTAL_REPORT_SPEC_SYNC_DELAY", "30"))
_RETRY_INTERVAL_S = float(os.environ.get("PORTAL_REPORT_SPEC_SYNC_RETRY", "120"))
_STARTUP_ATTEMPTS = int(os.environ.get("PORTAL_REPORT_SPEC_SYNC_ATTEMPTS", "10"))

_LOCK = threading.Lock()
_STATE: Dict[str, Any] = {
    "running": False,     # a sync thread is working now
    "trigger": None,      # "startup" | "admin" for the current or last run
    "started_at": None,
    "finished_at": None,
    "outcome": None,      # None (never ran) | "synced" | "not_configured" | "already_running" | "failed"
    "report": None,       # SyncReport.to_dict() of the last completed sync
    "error": None,        # the words of the last failure
    "attempt": 0,         # startup attempt number, for the status line
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def configured_folders() -> List[str]:
    """The folders a plain sync takes, as pyegeria reads them; [] if pyegeria cannot say."""
    try:
        from pyegeria.view.egeria_spec_cache import configured_folders as _cf
        return list(_cf())
    except Exception as exc:  # noqa: BLE001 -- older pyegeria, or settings that do not load
        logger.debug(f"report-spec sync: configured folders unavailable: {exc}")
        return []


def status() -> Dict[str, Any]:
    """A copy of the sync state plus the configured folders."""
    with _LOCK:
        out = dict(_STATE)
    out["folders"] = configured_folders()
    return out


def _service_client():
    from pyegeria.omvs.collection_manager import CollectionManager
    server = os.environ.get("EGERIA_VIEW_SERVER", "qs-view-server")
    url = os.environ.get("EGERIA_VIEW_SERVER_URL") or os.environ.get("EGERIA_PLATFORM_URL", "https://localhost:9443")
    user_id = os.environ.get("EGERIA_USER", "erinoverview")
    user_pwd = os.environ.get("EGERIA_USER_PASSWORD", "secret")
    client = CollectionManager(server, url, user_id=user_id, user_pwd=user_pwd)
    client.create_egeria_bearer_token()   # sync: fine here, this runs in its own thread
    return client


def _sync_once() -> str:
    """Run one sync. Returns the outcome word; never raises (a failure is recorded and returned
    as "failed")."""
    folders = configured_folders()
    if not folders:
        with _LOCK:
            _STATE.update(outcome="not_configured", report=None, error=None, finished_at=_now())
        logger.info("report-spec sync: no report spec folders configured (PYEGERIA_REPORT_SPEC_FOLDERS); "
                    "nothing synced, so no report specs are held in Egeria for this Portal")
        return "not_configured"
    client = None
    try:
        from pyegeria.view.egeria_spec_cache import SyncAlreadyRunning, sync_report_specs
        client = _service_client()
        try:
            report = sync_report_specs(client, shared=True)
        except SyncAlreadyRunning as exc:
            with _LOCK:
                _STATE.update(outcome="already_running", error=str(exc), finished_at=_now())
            logger.info(f"report-spec sync: another process is syncing this cache: {exc}")
            return "already_running"
        rep = report.to_dict()
        with _LOCK:
            _STATE.update(outcome="synced", report=rep, error=None, finished_at=_now())
        logger.info(f"report-spec sync: folders {rep.get('folders')}: {len(rep.get('added', []))} added, "
                    f"{len(rep.get('updated', []))} updated, {len(rep.get('unchanged', []))} unchanged, "
                    f"{len(rep.get('pruned', []))} pruned, {len(rep.get('skipped', []))} skipped")
        return "synced"
    except Exception as exc:  # noqa: BLE001 -- Egeria down, bad credentials, ...: record and carry on
        with _LOCK:
            _STATE.update(outcome="failed", error=f"{type(exc).__name__}: {exc}"[:600], finished_at=_now())
        logger.warning(f"report-spec sync failed: {type(exc).__name__}: {str(exc)[:300]}")
        return "failed"
    finally:
        if client is not None:
            try:
                client.close_session()
            except Exception:  # noqa: BLE001
                pass


def _run(trigger: str, attempts: int, delay: float) -> None:
    try:
        if delay:
            time.sleep(delay)
        for attempt in range(1, attempts + 1):
            with _LOCK:
                _STATE.update(attempt=attempt, started_at=_now())
            outcome = _sync_once()
            if outcome != "failed" or attempt == attempts:
                return
            time.sleep(_RETRY_INTERVAL_S)   # Egeria may still be starting; try again later
    finally:
        with _LOCK:
            _STATE["running"] = False


def start(trigger: str = "admin") -> bool:
    """Start a sync in a daemon thread. False if one is already running (nothing new started).
    The startup trigger waits a little first and retries on failure; the admin trigger runs once,
    now."""
    with _LOCK:
        if _STATE["running"]:
            return False
        _STATE.update(running=True, trigger=trigger, attempt=0)
    if trigger == "startup":
        args = (trigger, max(1, _STARTUP_ATTEMPTS), _STARTUP_DELAY_S)
    else:
        args = (trigger, 1, 0.0)
    threading.Thread(target=_run, args=args, daemon=True, name=f"report-spec-sync-{trigger}").start()
    return True


def start_at_startup() -> None:
    """Called from the app lifespan. Never blocks; does nothing when turned off."""
    if os.environ.get("PORTAL_REPORT_SPEC_SYNC_AT_STARTUP", "1") == "0":
        logger.info("report-spec sync at startup is off (PORTAL_REPORT_SPEC_SYNC_AT_STARTUP=0)")
        return
    start("startup")
