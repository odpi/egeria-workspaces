"""
workbench_watchdog.py — evict a demo workbench session stuck at its CPU cap.

Demo mode only (WORKBENCH_GATE). The demo caps JupyterLab and Obsidian at
WORKBENCH_CPU_CAP cores each (egeria-quickstart-demo.yaml); the caps stop a
runaway notebook or a miner from starving Egeria, but nobody notices a
container pinned at its cap. Every minute this samples each workbench's CPU
through docker-proxy. After WORKBENCH_WATCHDOG_MINUTES consecutive samples at
or above WORKBENCH_WATCHDOG_THRESHOLD of the cap it:

  - releases the Portal lock if someone holds it (which also closes the gate
    and cuts their connection -- workbench_access.revoke), and
  - restarts the container, which ends whatever was burning the CPU, kernel
    or not (a process left running from a terminal survives kernel shutdown),

then emails ALERT_EMAIL_TO through Resend. A hot workbench with nobody holding
the lock is treated the same way, and is the more suspicious case: that is
what the 2026-10-17 Obsidian miner looked like.
"""
from __future__ import annotations

import asyncio
import os
from datetime import datetime
from typing import Optional

import httpx
from loguru import logger

import workbench_access as wb

_CPU_CAP    = float(os.environ.get("WORKBENCH_CPU_CAP", "2"))
_THRESHOLD  = float(os.environ.get("WORKBENCH_WATCHDOG_THRESHOLD", "0.9"))
_MINUTES    = int(os.environ.get("WORKBENCH_WATCHDOG_MINUTES", "10"))
_INTERVAL   = 60   # seconds between samples
_ALERT_TO   = os.environ.get("ALERT_EMAIL_TO", "")
_DOCKER     = os.environ.get("DOCKER_HOST", "tcp://docker-proxy:2375").replace("tcp://", "http://")

CONTAINERS = {
    "jupyter":  os.environ.get("WORKBENCH_JUPYTER_CONTAINER", "quickstart-jupyter-work-full"),
    "obsidian": os.environ.get("WORKBENCH_OBSIDIAN_CONTAINER", "obsidian-quickstart"),
}

_hot: dict[str, int] = {app: 0 for app in CONTAINERS}
_task: Optional[asyncio.Task] = None


async def _sample(c: httpx.AsyncClient, container: str) -> tuple[float, int]:
    """Cores in use (averaged over Docker's ~1 s sample) and memory in bytes."""
    r = await c.get(f"/containers/{container}/stats", params={"stream": "false"})
    r.raise_for_status()
    s = r.json()
    cpu, pre = s["cpu_stats"], s["precpu_stats"]
    cpu_delta = cpu["cpu_usage"]["total_usage"] - pre.get("cpu_usage", {}).get("total_usage", 0)
    sys_delta = cpu.get("system_cpu_usage", 0) - pre.get("system_cpu_usage", 0)
    online = cpu.get("online_cpus") or len(cpu["cpu_usage"].get("percpu_usage") or [1])
    cores = (cpu_delta / sys_delta) * online if sys_delta > 0 and cpu_delta > 0 else 0.0
    return cores, s.get("memory_stats", {}).get("usage", 0)


async def _restart(c: httpx.AsyncClient, container: str) -> bool:
    try:
        r = await c.post(f"/containers/{container}/restart", params={"t": 10})
        r.raise_for_status()
        return True
    except Exception as exc:
        logger.error(f"workbench watchdog: could not restart {container}: {exc}")
        return False


async def _release(app: str) -> Optional[str]:
    if app == "jupyter":
        from jupyter_lock_handler import watchdog_release
    else:
        from obsidian_lock_handler import watchdog_release
    return await watchdog_release("watchdog_cpu")


def _alert(app: str, container: str, holder: Optional[str], cores: float, mem: int, restarted: bool) -> None:
    from demo_auth_handler import _send_email
    who = f"Session holder <b>{holder}</b> was evicted." if holder else \
          "<b>Nobody held the Portal lock</b> -- check for a runaway or unwanted process."
    subject = f"[demo] {app} pinned at its CPU cap for {_MINUTES} min -- " + \
              ("session evicted" if holder else "no session held")
    html = (
        f"<p>{container} ran at {cores:.2f} of {_CPU_CAP:g} cores (threshold "
        f"{_THRESHOLD:.0%}) for {_MINUTES} consecutive minutes, ending "
        f"{datetime.utcnow():%Y-%m-%d %H:%M} UTC. Memory: {mem / 2**30:.2f} GiB.</p>"
        f"<p>{who}</p>"
        f"<p>Container {'restarted' if restarted else '<b>restart FAILED</b>'}.</p>"
    )
    if not _ALERT_TO:
        logger.warning(f"ALERT_EMAIL_TO not set -- skipped alert: {subject}")
        return
    _send_email(_ALERT_TO, subject, html)


async def _check(c: httpx.AsyncClient, app: str, container: str) -> None:
    try:
        cores, mem = await _sample(c, container)
    except Exception as exc:
        # Restarting, or not running: no evidence either way.
        logger.debug(f"workbench watchdog: no stats for {container}: {exc}")
        _hot[app] = 0
        return
    if cores < _THRESHOLD * _CPU_CAP:
        _hot[app] = 0
        return
    _hot[app] += 1
    logger.info(f"workbench watchdog: {container} at {cores:.2f} cores ({_hot[app]}/{_MINUTES})")
    if _hot[app] < _MINUTES:
        return
    _hot[app] = 0
    holder = await _release(app)
    restarted = await _restart(c, container)
    logger.warning(f"workbench watchdog: {container} pinned for {_MINUTES} min -- "
                   f"holder={holder!r}, restarted={restarted}")
    await asyncio.to_thread(_alert, app, container, holder, cores, mem, restarted)


async def _loop() -> None:
    async with httpx.AsyncClient(base_url=_DOCKER, timeout=30) as c:
        while True:
            await asyncio.sleep(_INTERVAL)
            for app, container in CONTAINERS.items():
                try:
                    await _check(c, app, container)
                except Exception as exc:
                    logger.error(f"workbench watchdog: {app} check failed: {exc}")


async def start() -> None:
    global _task
    if not wb.GATE_ENABLED:
        return
    _task = asyncio.create_task(_loop())
    logger.info(f"workbench watchdog started (cap {_CPU_CAP:g} cores, "
                f"{_THRESHOLD:.0%} for {_MINUTES} min)")


async def stop() -> None:
    global _task
    if _task and not _task.done():
        _task.cancel()
        try:
            await _task
        except asyncio.CancelledError:
            pass
    _task = None
