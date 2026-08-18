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
_DR_EGERIA_TIMEOUT = int(os.environ.get("BOOTSTRAP_HEAL_TIMEOUT_SECONDS", "300"))

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


async def _canary_present(family: dict) -> bool:
    """Cheap bounded point lookup -- one Egeria find, pageSize=1."""
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
        return isinstance(els, list) and len(els) > 0
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"bootstrap monitor: canary check failed for {family['name']}: {exc}")
        # Connection failure isn't evidence of a reset -- don't trigger a
        # heal pass just because Egeria was briefly unreachable.
        return True


async def _heal_family(family: dict) -> str:
    """Re-run every doc in this family's list, in order, via `dr_egeria
    --process`. Stops at the first failing doc (later docs in the same
    family typically depend on earlier ones' output). Every doc is
    upsert-safe, so re-running is always the correct fix."""
    for doc in family["docs"]:
        if not Path(doc).exists():
            logger.warning(f"bootstrap monitor: {family['name']} doc missing, skipping: {doc}")
            continue
        try:
            proc = await asyncio.create_subprocess_exec(
                "dr_egeria", "--process", doc,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
            )
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=_DR_EGERIA_TIMEOUT)
            if proc.returncode != 0:
                tail = stdout.decode(errors="replace")[-800:] if stdout else ""
                logger.error(f"bootstrap monitor: heal failed for {family['name']} on {doc}: {tail}")
                return f"failed on {Path(doc).name}"
            logger.info(f"bootstrap monitor: healed {family['name']} via {Path(doc).name}")
        except asyncio.TimeoutError:
            logger.error(f"bootstrap monitor: heal timed out for {family['name']} on {doc}")
            return f"timed out on {Path(doc).name}"
        except Exception as exc:  # noqa: BLE001
            logger.error(f"bootstrap monitor: heal error for {family['name']} on {doc}: {exc}")
            return f"error on {Path(doc).name}: {exc}"
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


async def check_and_heal_all() -> None:
    """Check every family's canary; heal (re-run its docs) any that's
    missing. Safe to call repeatedly -- a present canary is a fast no-op."""
    all_families = BOOTSTRAP_FAMILIES + _dynamic_families()

    to_heal = []
    for family in all_families:
        async with _mu:
            _state["families"].setdefault(family["name"], {"present": None, "lastHealedAt": None, "lastHealResult": None})
        present = await _canary_present(family)
        async with _mu:
            _state["families"][family["name"]]["present"] = present
        if not present:
            to_heal.append(family)

    async with _mu:
        _state["lastCheckAt"] = _now_iso()

    if not to_heal:
        return

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


async def start_scheduler() -> None:
    global _scheduler_task
    # Run one check immediately at startup (covers the redeploy case, where
    # the process restarts right alongside the reset) rather than waiting
    # a full interval before the first check.
    try:
        await check_and_heal_all()
    except Exception as exc:  # noqa: BLE001
        logger.error(f"bootstrap monitor: startup check failed: {exc}")
    _scheduler_task = asyncio.create_task(_monitor_loop())
    logger.info(f"bootstrap monitor scheduler started (interval={_CHECK_INTERVAL}s)")


async def stop_scheduler() -> None:
    global _scheduler_task
    if _scheduler_task and not _scheduler_task.done():
        _scheduler_task.cancel()
        try:
            await _scheduler_task
        except asyncio.CancelledError:
            pass
    _scheduler_task = None


async def _monitor_loop() -> None:
    # Covers a reset that happens without the web app process restarting
    # (e.g. only the Egeria database container is reset) -- the startup
    # check alone would miss that case.
    while True:
        await asyncio.sleep(_CHECK_INTERVAL)
        try:
            await check_and_heal_all()
        except Exception as exc:  # noqa: BLE001
            logger.error(f"bootstrap monitor: periodic check failed: {exc}")


@router.get("/status")
async def bootstrap_status():
    """Public — current reinitializing state, for the frontend banner."""
    async with _mu:
        return JSONResponse(dict(_state))
