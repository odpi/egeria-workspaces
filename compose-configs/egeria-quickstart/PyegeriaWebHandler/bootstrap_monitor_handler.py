"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Bootstrap monitor — detects when the Egeria repository has been reset
(a redeploy, a manual DB drop, DEMO_MODE's own scheduled reset) and
automatically re-runs the Dr.Egeria documents that seed each portal
feature's reference data, since the Egeria repository itself has no
"was this reset" signal of its own.

Detection: `homeMetadataCollectionId` does NOT change across a reset
(confirmed live 2026-08-18 against a real reset) — the only reliable
signal is a "canary" element per bootstrap family going missing. Every
Dr.Egeria doc this module re-runs is upsert-safe, so healing is always
correct, never a duplication risk.

States
------
  reinitializing   True while a heal pass is actively re-running docs for
                   at least one family — the frontend banner shows during
                   this window.
  families         Per-family last-known presence + heal outcome, for the
                   status endpoint / a future admin view.

Mirrors advisor_lock_handler.py / demo_reset_handler.py's own
start_scheduler()/stop_scheduler() background-task shape (same asyncio.Lock
+ module-level state pattern) so this fits the existing lifespan wiring in
pyegeria_handler.py without introducing a new convention.
"""

import asyncio
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from loguru import logger

router = APIRouter(prefix="/api/bootstrap", tags=["bootstrap-monitor"])

# ── Bootstrap family registry ────────────────────────────────────────────────
# Empty now -- the two families this used to hardcode (local-dashboards,
# overview-governance-metrics) were migrated to _batch.json manifests
# (see bootstrap_batches.py's _EXTRA_BATCH_ROOTS for the latter, which lives
# alongside the handler code rather than under dr-egeria-inbox) with
# "defaultEnabled": true, so they keep auto-healing out of the box via
# _dynamic_families() below with no seed file needed, while also being
# visible/toggleable in the admin panel's Data Initialization tab.
#
# The dr-egeria help Glossary is deliberately NOT a family here yet -- its
# generated help doc is a NEW timestamped file every `refresh_specs` run
# (see the dr-egeria-command-sync skill), so there's no single canonical
# checked-in file to re-run automatically today. Revisit once one exists.
BOOTSTRAP_FAMILIES = []

_CHECK_INTERVAL = int(os.environ.get("BOOTSTRAP_CHECK_INTERVAL_SECONDS", "600"))  # 10 min
# 900s (15 min), was 300s -- the Design Patterns batch's poim-pattern-links.md
# (~1,058 relationship-link commands per the design-patterns/README) reliably
# exceeded the old 300s cap (confirmed live, 2026-08-28), and every timeout
# used to leave the dr_egeria subprocess orphaned and running (see the
# _active_procs comment on _heal_family) -- that half of the bug is fixed
# now regardless of this value, but a heal that can never actually finish in
# time would still never successfully clear this family's canary and would
# just retry-and-give-up every _CHECK_INTERVAL forever. Generous headroom is
# safe here: every doc this module re-runs is upsert-safe, so a longer wait
# never risks anything, it only avoids giving up on genuinely slow (not
# stuck) large batches.
_DR_EGERIA_TIMEOUT = int(os.environ.get("BOOTSTRAP_HEAL_TIMEOUT_SECONDS", "900"))
# Per-family canary-presence check timeout (2026-09-03 incident fix -- see
# _canary_present's docstring). Deliberately much shorter than
# _DR_EGERIA_TIMEOUT: this guards a "cheap point lookup", not actual healing
# work, and start_scheduler() awaits check_and_heal_all() (which calls this
# once per family, serially) directly from the app's lifespan -- an
# unbounded or over-generous value here blocks the whole app's startup for
# as long as Egeria stays slow, times number of families.
_CANARY_CHECK_TIMEOUT = int(os.environ.get("BOOTSTRAP_CANARY_TIMEOUT_SECONDS", "15"))
# Startup fast-retry window -- see start_scheduler()'s docstring comment.
_STARTUP_RETRY_INTERVAL = int(os.environ.get("BOOTSTRAP_STARTUP_RETRY_SECONDS", "20"))
_STARTUP_RETRY_WINDOW = int(os.environ.get("BOOTSTRAP_STARTUP_RETRY_WINDOW_SECONDS", "300"))  # 5 min

_mu = asyncio.Lock()
_state: dict = {
    "reinitializing": False,
    "lastCheckAt": None,
    "message": None,
    "families": {f["name"]: {"present": None, "lastHealedAt": None, "lastHealResult": None} for f in BOOTSTRAP_FAMILIES},
}
_scheduler_task: Optional[asyncio.Task] = None


def _now_iso() -> str:
    return datetime.utcnow().isoformat()


async def _canary_present(family: dict) -> tuple[bool, bool]:
    """Cheap bounded point lookup -- one Egeria find, pageSize=1. Returns
    (present, reachable). `present` fails open to True on any error
    (connection failure isn't evidence of a reset -- don't trigger a heal
    pass just because Egeria was briefly unreachable); `reachable` tells
    the caller whether that True actually means "confirmed present" or
    "couldn't check" -- see start_scheduler()'s fast-retry-on-startup use
    of this distinction.

    Timeout added 2026-09-03 (incident: a degraded Egeria -- repeated 401s
    from the metadata-expert search endpoint -- left this call relying on
    pyegeria/httpx's own default timeouts, which were generous enough that
    check_and_heal_all()'s serial per-family loop took several minutes end
    to end. Since start_scheduler() awaits that loop directly from
    pyegeria_handler.py's lifespan, the whole app's ASGI startup was blocked
    for those several minutes -- not infinite, but indistinguishable from a
    hang from the outside, and it got worse every time a redeploy restarted
    the in-progress attempt from scratch. Bounding each individual family's
    check keeps the worst case at _CANARY_CHECK_TIMEOUT seconds no matter
    how degraded Egeria is or how many families exist, and does NOT touch
    _heal_family's own separate, deliberately generous _DR_EGERIA_TIMEOUT --
    that one guards actual healing work, which is allowed to take longer.
    """
    try:
        from pyegeria import MetadataExpert
        import pyegeria
        from egeria_auth import async_apply_token
        pyegeria.enable_ssl_check = False
        pyegeria.disable_ssl_warnings = True
        url    = os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
        server = os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
        user   = os.environ.get("EGERIA_USER",          "erinoverview")
        pwd    = os.environ.get("EGERIA_USER_PASSWORD", "secret")
        mgr = MetadataExpert(view_server=server, platform_url=url, user_id=user, user_pwd=pwd)

        async def _do_check():
            await async_apply_token(mgr)
            body = {
                "class": "FindRequestBody", "metadataElementTypeName": family["canary_type"],
                "searchProperties": {
                    "class": "SearchProperties", "matchCriteria": "ALL",
                    "conditions": [{"property": "displayName", "operator": "EQ",
                                     "value": {"class": "PrimitiveTypePropertyValue", "typeName": "string",
                                               "primitiveValue": family["canary_name"]}}],
                },
                "limitResultsByStatus": ["ACTIVE"], "graphQueryDepth": 0, "startFrom": 0, "pageSize": 1,
            }
            els = await mgr._async_find_metadata_elements(body)
            await mgr._async_close_session()
            return els

        els = await asyncio.wait_for(_do_check(), timeout=_CANARY_CHECK_TIMEOUT)
        return isinstance(els, list) and len(els) > 0, True
    except asyncio.TimeoutError:
        logger.warning(
            f"bootstrap monitor: canary check for {family['name']} timed out "
            f"after {_CANARY_CHECK_TIMEOUT}s -- Egeria is likely slow/degraded"
        )
        return True, False
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"bootstrap monitor: canary check failed for {family['name']}: {exc}")
        return True, False


# Subprocesses currently in flight, so stop_scheduler() (app shutdown/reload)
# and the timeout/cancellation paths below can actually terminate them.
#
# BUG (found 2026-08-28, Design Patterns batch): a heal's `dr_egeria
# --process <file>` subprocess was never killed on either a timeout or a
# cancelled heal task -- asyncio.wait_for()'s TimeoutError just abandons the
# await, and cancelling _scheduler_task (stop_scheduler(), called on every
# app reload/restart) only unwinds the Python coroutine, neither of which
# sends any signal to the actual OS child process. The orphaned `dr_egeria`
# process keeps running to completion on its own, invisible to this module's
# state. Confirmed live: `poim-pattern-links.md` (22k lines) reliably
# exceeds the 300s default _DR_EGERIA_TIMEOUT, so every heal attempt against
# it timed out and orphaned a process; a `docker cp` reload during that
# window (this session ran several while investigating something unrelated)
# then restarted the scheduler, found the canary still missing (the orphan
# hadn't finished), and started a SECOND heal -- two concurrent
# `dr_egeria --process poim-pattern-links.md` runs against the same file,
# each creating its own duplicate DesignPattern elements instead of one run
# upserting cleanly. See cleanup notes in PYEGERIA... (this repo's) git log
# for the one-off dedup this caused.
_active_procs: set = set()


async def _kill_proc(proc) -> None:
    try:
        proc.kill()
        await proc.wait()
    except ProcessLookupError:
        pass  # already exited
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"bootstrap monitor: error killing orphaned dr_egeria process: {exc}")


async def _heal_family(family: dict) -> str:
    """Re-run every doc in this family's list, in order, via `dr_egeria
    --process`. Stops at the first failing doc (later docs in the same
    family typically depend on earlier ones' output). Every doc is
    upsert-safe, so re-running is always the correct fix."""
    for doc in family["docs"]:
        if not Path(doc).exists():
            logger.warning(f"bootstrap monitor: {family['name']} doc missing, skipping: {doc}")
            continue
        proc = None
        try:
            proc = await asyncio.create_subprocess_exec(
                "dr_egeria", "--process", doc,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
            )
            _active_procs.add(proc)
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=_DR_EGERIA_TIMEOUT)
            if proc.returncode != 0:
                tail = stdout.decode(errors="replace")[-800:] if stdout else ""
                logger.error(f"bootstrap monitor: heal failed for {family['name']} on {doc}: {tail}")
                return f"failed on {Path(doc).name}"
            logger.info(f"bootstrap monitor: healed {family['name']} via {Path(doc).name}")
        except asyncio.TimeoutError:
            logger.error(f"bootstrap monitor: heal timed out for {family['name']} on {doc} -- killing it "
                         f"(was previously left running orphaned; see _active_procs comment above)")
            if proc is not None:
                await _kill_proc(proc)
            return f"timed out on {Path(doc).name}"
        except asyncio.CancelledError:
            # App shutdown/reload mid-heal (stop_scheduler()) -- kill the
            # child before letting the cancellation propagate, same reason
            # as the timeout branch above.
            if proc is not None:
                await _kill_proc(proc)
            raise
        except Exception as exc:  # noqa: BLE001
            logger.error(f"bootstrap monitor: heal error for {family['name']} on {doc}: {exc}")
            return f"error on {Path(doc).name}: {exc}"
        finally:
            if proc is not None:
                _active_procs.discard(proc)
    return "ok"


def _dynamic_families() -> list[dict]:
    """Admin-selected bootstrap batches (see bootstrap_batches.py / the
    admin panel's Data Initialization tab) that also declare a `canary` in
    their folder's _batch.json manifest -- those get the same auto-heal
    treatment as the hardcoded BOOTSTRAP_FAMILIES above, just discovered at
    runtime instead of hand-registered. A batch with no canary is
    manual/run-on-demand only (see bootstrap_admin_handler.py) -- it's
    never auto-healed, since there's no signal to detect it went missing."""
    try:
        import bootstrap_batches as bb
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"bootstrap monitor: bootstrap_batches unavailable: {exc}")
        return []
    families = []
    for batch in bb.enabled_batches():
        canary = batch.get("canary")
        if not canary or not canary.get("type") or not canary.get("name"):
            continue
        families.append({
            "name":        f"batch:{batch['id']}",
            "canary_type": canary["type"],
            "canary_name": canary["name"],
            "docs":        [str(Path(batch["path"]) / f) for f in batch["files"]],
        })
    return families


async def check_and_heal_all() -> bool:
    """Check every family's canary; heal (re-run its docs) any that's
    missing. Safe to call repeatedly -- a present canary is a fast no-op.
    Returns True if ANY canary check couldn't actually reach Egeria this
    pass (as opposed to reaching it and confirming presence) -- used by
    start_scheduler()'s startup fast-retry window."""
    all_families = BOOTSTRAP_FAMILIES + _dynamic_families()

    async with _mu:
        for family in all_families:
            _state["families"].setdefault(
                family["name"], {"present": None, "lastHealedAt": None, "lastHealResult": None}
            )

    # Concurrent, not serial (2026-09-03 incident fix) -- each check is
    # already individually bounded by _CANARY_CHECK_TIMEOUT, but a serial
    # loop's *total* worst case still scales with family count (13 families
    # * 15s = ~3 min even bounded). start_scheduler() awaits this whole
    # function directly from the app's lifespan, so this phase's wall-clock
    # is what actually gates app startup -- running the checks concurrently
    # caps the whole phase at ~_CANARY_CHECK_TIMEOUT regardless of how many
    # families exist. Safe to parallelize: each check is read-only against
    # Egeria (a single bounded find), independent per family, and its own
    # state write below is serialized through _mu like everywhere else.
    results = await asyncio.gather(*(_canary_present(family) for family in all_families))

    any_unreachable = False
    to_heal = []
    for family, (present, reachable) in zip(all_families, results):
        if not reachable:
            any_unreachable = True
        async with _mu:
            _state["families"][family["name"]]["present"] = present
        if not present:
            to_heal.append(family)

    async with _mu:
        _state["lastCheckAt"] = _now_iso()

    if not to_heal:
        return any_unreachable

    async with _mu:
        _state["reinitializing"] = True
        _state["message"] = "Reinitializing Portal — re-seeding " + ", ".join(f["name"] for f in to_heal)
    logger.info(f"bootstrap monitor: healing {[f['name'] for f in to_heal]} (canary missing)")

    for family in to_heal:
        result = await _heal_family(family)
        async with _mu:
            _state["families"][family["name"]]["lastHealedAt"] = _now_iso()
            _state["families"][family["name"]]["lastHealResult"] = result

    async with _mu:
        _state["reinitializing"] = False
        _state["message"] = None

    return any_unreachable


_startup_deadline: Optional[float] = None  # time.monotonic() cutoff; None once settled


async def start_scheduler() -> None:
    global _scheduler_task, _startup_deadline
    # Run one check immediately at startup (covers the redeploy case, where
    # the process restarts right alongside the reset) rather than waiting
    # a full interval before the first check.
    #
    # egeria-quickstart.yaml's pyegeria-web `depends_on: egeria-main` has no
    # `condition:` (defaults to service_started, not service_healthy), so on
    # a full stack cold-start this container routinely starts running before
    # Egeria is actually reachable -- this first check fails open (see
    # _canary_present) and effectively no-ops. Rather than then waiting the
    # full _CHECK_INTERVAL (10 min default) for the next real attempt, open
    # a short fast-retry window: if this first check couldn't reach Egeria
    # at all, _monitor_loop below retries every BOOTSTRAP_STARTUP_RETRY_SECONDS
    # until either it succeeds or BOOTSTRAP_STARTUP_RETRY_WINDOW_SECONDS
    # elapses, then settles into the normal cadence for good -- a LATER,
    # separate outage does not reopen this window and gets the same gentle
    # periodic cadence as any other transient unreachability. Fast-retrying
    # forever on a genuine extended outage would just hammer Egeria for no
    # benefit.
    _startup_deadline = time.monotonic() + _STARTUP_RETRY_WINDOW
    try:
        unreachable = await check_and_heal_all()
    except Exception as exc:  # noqa: BLE001
        logger.error(f"bootstrap monitor: startup check failed: {exc}")
        unreachable = True
    if not unreachable:
        _startup_deadline = None  # already reachable on the very first try -- no fast-retry needed
    _scheduler_task = asyncio.create_task(_monitor_loop())
    logger.info(
        f"bootstrap monitor scheduler started (interval={_CHECK_INTERVAL}s"
        + (f", fast-retrying every {_STARTUP_RETRY_INTERVAL}s for up to {_STARTUP_RETRY_WINDOW}s "
           "while Egeria isn't reachable yet" if _startup_deadline else "") + ")"
    )


async def stop_scheduler() -> None:
    global _scheduler_task
    if _scheduler_task and not _scheduler_task.done():
        _scheduler_task.cancel()
        try:
            await _scheduler_task
        except asyncio.CancelledError:
            pass
    _scheduler_task = None
    # Belt-and-braces: _heal_family's own CancelledError handler should have
    # already killed whatever it was awaiting, but if the task's cancellation
    # landed somewhere else in the coroutine (e.g. between subprocess creation
    # and the try block, or a future code path that adds another await point),
    # don't leave anything in _active_procs still running across this restart.
    for proc in list(_active_procs):
        await _kill_proc(proc)
    _active_procs.clear()


async def _monitor_loop() -> None:
    # Covers a reset that happens without the web app process restarting
    # (e.g. only the Egeria database container is reset) -- the startup
    # check alone would miss that case.
    global _startup_deadline
    while True:
        fast_phase = _startup_deadline is not None and time.monotonic() < _startup_deadline
        await asyncio.sleep(_STARTUP_RETRY_INTERVAL if fast_phase else _CHECK_INTERVAL)
        try:
            unreachable = await check_and_heal_all()
        except Exception as exc:  # noqa: BLE001
            logger.error(f"bootstrap monitor: periodic check failed: {exc}")
            unreachable = True
        if _startup_deadline is not None and (not unreachable or time.monotonic() >= _startup_deadline):
            _startup_deadline = None  # reachable now, or waited long enough -- stop fast-retrying for good


@router.get("/status")
async def bootstrap_status():
    """Public — current reinitializing state, for the frontend banner."""
    async with _mu:
        return JSONResponse(dict(_state))
