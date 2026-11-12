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
- lazily (`retry_if_index_not_read`), at most every LAZY_RETRY_S (2 minutes), on a Report Specs listing
  or a publish request while the consumer index is "not read". A sync can succeed while Egeria is still
  starting and leave the index "not read" (2026-11-12: the startup sync at 17:02:58Z, during an
  egeria-main restart at 16:59:47Z, counted as done); and nothing else re-syncs when egeria-main
  restarts after the Portal. A sync whose index comes back "not read" has outcome "index_not_read",
  which the startup run retries like a failure.

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
#: The least time between two lazy syncs while the consumer index stays "not read".
LAZY_RETRY_S = float(os.environ.get("PORTAL_REPORT_SPEC_INDEX_RETRY", "120"))
#: Outcomes the startup run tries again: a failed sync, and a sync whose consumer index was not read.
RETRY_OUTCOMES = ("failed", "index_not_read")
#: "enabled" is False only in the test suite (tests/conftest.py), so a listing in one test never starts a
#: real background sync that races another test's sync state.
#: The longest wait between two syncs for the same "not read" reason (lazy and startup retries back off,
#: doubling, up to this): a permanent cause (the consumer root missing) must not mean a full sync every
#: two minutes for ever.
BACKOFF_CAP_S = float(os.environ.get("PORTAL_REPORT_SPEC_INDEX_RETRY_CAP", "1800"))
_LAZY = {"last": None, "enabled": True, "reason": None, "fires": 0}


def backoff(base: float, repeats: int) -> float:
    """The wait before the next try after `repeats` tries for the same reason: base, 2x, 4x ... capped."""
    return min(BACKOFF_CAP_S, base * (2 ** max(0, repeats - 1)))

_LOCK = threading.Lock()
_STATE: Dict[str, Any] = {
    "running": False,     # a sync thread is working now
    "trigger": None,      # "startup" | "admin" for the current or last run
    "started_at": None,
    "finished_at": None,
    # None (never ran) | "synced" | "folders_missing" (every configured folder was not found) |
    # "not_configured" | "already_running" (another process held the cache lock) | "failed" |
    # "index_not_read" (the specs synced, but the consumer index came back "not read": retried"
    "outcome": None,
    "report": None,       # SyncReport.to_dict() of the last completed sync
    "error": None,        # the words of the last failure
    "missing_folders": [],  # configured folders the last sync did not find in Egeria
    "phase": None,        # while running: "waiting" (startup delay) | "syncing" | "retry_wait"
    "attempt": 0,         # attempt number of the current or last run
    "attempts": 0,        # attempts this run may make (startup retries; 1 for the admin button)
}

_NOT_FOUND = "folder not found"


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
    """A copy of the sync state plus the configured folders. Holds error text and skip reasons:
    give it only to callers allowed the detail (see public_status)."""
    with _LOCK:
        out = dict(_STATE)
    out["folders"] = configured_folders()
    return out


def public_status() -> Dict[str, Any]:
    """The sync state without error text, skip reasons or the sync identity, for callers not
    allowed the detail. The outcome word and counts stay, so it is still honest."""
    full = status()
    rep = full.get("report") or {}
    out = {k: full.get(k) for k in ("running", "trigger", "started_at", "finished_at", "outcome", "phase",
                                     "attempt", "attempts", "folders", "missing_folders")}
    out["report"] = ({k: list(rep.get(k) or []) for k in ("added", "updated", "unchanged", "pruned")}
                     | {"skipped": [[who, "(detail withheld)"] for who, _why in (rep.get("skipped") or [])]}
                     | ({"consumers": {k: rep["consumers"].get(k) for k in ("status", "consumers", "labels")}}
                        if isinstance(rep.get("consumers"), dict) else {})
                     if rep else None)
    out["error"] = "(detail withheld: sign in as an administrator to see it)" if full.get("error") else None
    out["detail"] = False
    return out


def missing_folders(report: Dict[str, Any], folders: List[str]) -> List[str]:
    """Configured folders the sync reported as not found (not unreadable: those keep their specs)."""
    return [who for who, why in (report.get("skipped") or [])
            if who in folders and str(why).startswith(_NOT_FOUND)]


def _service_client():
    from pyegeria.omvs.collection_manager import CollectionManager
    server = os.environ.get("EGERIA_VIEW_SERVER", "qs-view-server")
    url = os.environ.get("EGERIA_VIEW_SERVER_URL") or os.environ.get("EGERIA_PLATFORM_URL", "https://localhost:9443")
    user_id = os.environ.get("EGERIA_USER", "erinoverview")
    user_pwd = os.environ.get("EGERIA_USER_PASSWORD", "secret")
    client = CollectionManager(server, url, user_id=user_id, user_pwd=user_pwd)
    from egeria_auth import check_client_platform
    check_client_platform(client)         # env-configured platform: always allow-listed
    client.create_egeria_bearer_token()   # sync: fine here, this runs in its own thread
    return client


def _reconcile_fallbacks() -> None:
    """After a sync: withdraw the Portal's local copy of a spec Egeria now holds, or restore it
    for one Egeria no longer holds (local_spec_fallback.py). Never raises."""
    try:
        import local_spec_fallback
        local_spec_fallback.reconcile()
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"report-spec sync: could not reconcile the local fallback specs: {exc}")


def _sync_once() -> str:
    """Run one sync. Returns the outcome word; never raises (a failure is recorded and returned
    as "failed")."""
    folders = configured_folders()
    if not folders:
        with _LOCK:
            _STATE.update(outcome="not_configured", report=None, error=None, missing_folders=[], finished_at=_now())
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
        missing = missing_folders(rep, folders)
        outcome = "folders_missing" if missing and len(missing) == len(folders) else "synced"
        index = rep.get("consumers") if isinstance(rep.get("consumers"), dict) else {}
        error = None
        if outcome == "synced" and index.get("status") == "not read":
            # The specs synced, but "Used by" and publishing need the consumer index: try again.
            outcome = "index_not_read"
            error = f"the consumer index was not read: {index.get('reason') or 'no reason given'}"[:600]
            logger.warning(f"report-spec sync: {error}; it will be tried again")
        with _LOCK:
            _STATE.update(outcome=outcome, report=rep, error=error, missing_folders=missing, finished_at=_now())
        logger.info(f"report-spec sync: folders {rep.get('folders')}: {len(rep.get('added', []))} added, "
                    f"{len(rep.get('updated', []))} updated, {len(rep.get('unchanged', []))} unchanged, "
                    f"{len(rep.get('pruned', []))} pruned, {len(rep.get('skipped', []))} skipped")
        _reconcile_fallbacks()
        return outcome
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
            with _LOCK:
                _STATE.update(phase="waiting")
            time.sleep(delay)
        same, last_error = 0, None
        for attempt in range(1, attempts + 1):
            with _LOCK:
                _STATE.update(attempt=attempt, phase="syncing", started_at=_now())
            outcome = _sync_once()
            if outcome not in RETRY_OUTCOMES or attempt == attempts:
                return
            with _LOCK:
                _STATE.update(phase="retry_wait")
                error = _STATE.get("error")
            # Egeria may still be starting: try again later. A "not read" index for the same reason again
            # backs off (doubling, capped); a failed sync (Egeria down) keeps the plain interval.
            same = same + 1 if outcome == "index_not_read" and error == last_error else (1 if outcome == "index_not_read" else 0)
            last_error = error if outcome == "index_not_read" else None
            time.sleep(backoff(_RETRY_INTERVAL_S, same) if same else _RETRY_INTERVAL_S)
    finally:
        with _LOCK:
            _STATE.update(running=False, phase=None)


def running_words(st: Dict[str, Any]) -> Optional[str]:
    """What a running sync is doing, in words; None when no sync is running."""
    if not st.get("running"):
        return None
    if st.get("trigger") == "lazy":
        return "a sync from Egeria is running (the consumer index was not read)"
    if st.get("trigger") != "startup":
        return "a sync from Egeria is running"
    n, of = st.get("attempt") or 0, st.get("attempts") or 0
    if st.get("phase") == "waiting" or n == 0:
        return "the startup sync from Egeria is starting"
    if n <= 1 and st.get("phase") == "syncing":
        return "the startup sync from Egeria is running"
    return f"the startup sync from Egeria is retrying (attempt {n} of {of}; Egeria may still be starting)"


def start(trigger: str = "admin") -> bool:
    """Start a sync in a daemon thread. False if one is already running (nothing new started).
    The startup trigger waits a little first and retries on failure; the admin trigger runs once,
    now."""
    with _LOCK:
        if _STATE["running"]:
            return False
        attempts = max(1, _STARTUP_ATTEMPTS) if trigger == "startup" else 1
        _STATE.update(running=True, trigger=trigger, attempt=0, attempts=attempts, phase="syncing")
    args = (trigger, attempts, _STARTUP_DELAY_S if trigger == "startup" else 0.0)
    threading.Thread(target=_run, args=args, daemon=True, name=f"report-spec-sync-{trigger}").start()
    return True


def retry_if_index_not_read(index_status: Optional[str] = None, now: Optional[float] = None, *,
                            supported: bool = True, reason: Optional[str] = None) -> bool:
    """Start a sync when the consumer index is "not read", a sync has finished before (the startup sync
    owns the first read), and the wait for this reason has passed. Called on a Report Specs listing or a
    publish request, so an egeria-main restart the Portal never saw heals itself. `index_status`,
    `supported` and `reason` are what the caller already read (report_spec_consumers.index()).

    - `supported` False (a pyegeria without the consumer index): never; a sync cannot change it.
    - The same reason again: the wait doubles from LAZY_RETRY_S (2 min) up to BACKOFF_CAP_S (30 min), so
      a permanent cause (the consumer root missing) is not a full sync every two minutes. A new reason
      starts again at 2 minutes; the index reading "read" resets it.
    Never blocks; True when a sync was started."""
    if index_status is None:
        try:
            import report_spec_consumers
            idx = report_spec_consumers.index()
            index_status, supported, reason = idx.get("status"), idx.get("supported", True), idx.get("reason")
        except Exception:  # noqa: BLE001
            return False
    if index_status != "not read":
        with _LOCK:
            _LAZY.update(reason=None, fires=0)          # read (or partly): the next "not read" starts afresh
        return False
    if not _LAZY.get("enabled", True) or supported is False or not configured_folders():
        return False
    now = time.monotonic() if now is None else now
    with _LOCK:
        # Only after a sync has finished at least once: before that, the startup sync owns the first
        # read (or it is turned off, and "no sync from Egeria has run" is the honest answer).
        if _STATE["running"] or _STATE["outcome"] is None:
            return False
        if reason != _LAZY["reason"]:
            _LAZY.update(reason=reason, fires=0)
        last, fires = _LAZY["last"], _LAZY["fires"]
        wait = backoff(LAZY_RETRY_S, fires) if fires else LAZY_RETRY_S
        if last is not None and now - last < wait:
            return False
        _LAZY.update(last=now, fires=fires + 1)
    started = start("lazy")
    if started:
        logger.info(f"report-spec sync: the consumer index is not read ({reason or 'no reason given'}); syncing "
                    f"again; the next try for the same reason waits {backoff(LAZY_RETRY_S, fires + 1):.0f}s")
    return started


def start_at_startup() -> None:
    """Called from the app lifespan. Never blocks; does nothing when turned off."""
    if os.environ.get("PORTAL_REPORT_SPEC_SYNC_AT_STARTUP", "1") == "0":
        logger.info("report-spec sync at startup is off (PORTAL_REPORT_SPEC_SYNC_AT_STARTUP=0)")
        return
    start("startup")
