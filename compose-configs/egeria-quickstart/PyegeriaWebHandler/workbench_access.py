"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Workbench gate — ties Apache access to /jupyter/ and /obsidian/ to the
Portal's session locks (jupyter_lock_handler.py, obsidian_lock_handler.py).

Both workbenches give whoever reaches them code execution in a container, so
in demo mode they are reachable ONLY through Apache on 443, and only by the
current lock holder:

  * On acquire, the lock handler mints a random access key, sets it as an
    HttpOnly cookie scoped to the app's path, and records it here.
  * This module writes the current keys to a RewriteMap file
    (``<app> <key>`` per line; ``-`` when free) shared with apache-web.
    workbench-locations.conf compares the cookie with the map on every
    request, WebSocket upgrades included; mod_rewrite re-reads the file
    whenever its mtime changes.
  * On release/expiry/eviction the key is revoked, and live connections are
    cut: Jupyter's kernels and terminals are shut down via its REST API;
    the Obsidian container is restarted through docker-proxy (its Selkies
    stream is a single long-lived WebSocket that a map change can't end).

The upstream credentials (Jupyter token, Obsidian basic-auth password) are
WORKBENCH_SECRET, which Apache injects and browsers never see. It also stops
one workbench being used to reach the other directly over egeria_network.

Disabled (every function a no-op) unless WORKBENCH_GATE is true, which only
egeria-quickstart-demo.yaml sets; local/developer mode keeps the direct ports.
"""

import asyncio
import os
import secrets
from pathlib import Path
from typing import Optional

import httpx
from fastapi import Response
from loguru import logger

GATE_ENABLED = os.environ.get("WORKBENCH_GATE", "false").lower() in ("true", "1", "yes")

_MAP_FILE = Path(os.environ.get("WORKBENCH_ACCESS_MAP", "/app/workbench-access/access.map"))
_SECRET = os.environ.get("WORKBENCH_SECRET", "")
_JUPYTER_INTERNAL = os.environ.get(
    "WORKBENCH_JUPYTER_INTERNAL_URL", "http://quickstart-jupyter-work-full:7888/jupyter"
)
_OBSIDIAN_CONTAINER = os.environ.get("WORKBENCH_OBSIDIAN_CONTAINER", "obsidian-quickstart")
_DOCKER_HOST = os.environ.get("DOCKER_HOST", "tcp://docker-proxy:2375").replace("tcp://", "http://")

# Public paths, as routed by workbench-locations.conf. The cookie path must
# match the Location prefix, or the browser won't send it.
APP_PATHS = {"jupyter": "/jupyter/", "obsidian": "/obsidian/"}
APP_URLS = {"jupyter": "/jupyter/lab", "obsidian": "/obsidian/"}

_keys: dict[str, Optional[str]] = {"jupyter": None, "obsidian": None}


def cookie_name(app: str) -> str:
    return f"wb_{app}"


def public_url(app: str) -> Optional[str]:
    """URL the Portal tile should open, or None when the gate is off."""
    return APP_URLS[app] if GATE_ENABLED else None


def _write_map() -> None:
    # Write-then-rename so Apache never reads a half-written file. The
    # directory (not the file) is bind-mounted, so the rename is visible.
    try:
        _MAP_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = _MAP_FILE.with_suffix(".tmp")
        tmp.write_text("".join(f"{app} {key or '-'}\n" for app, key in _keys.items()))
        tmp.chmod(0o644)
        os.replace(tmp, _MAP_FILE)
    except Exception as exc:
        logger.error(f"workbench gate: could not write {_MAP_FILE}: {exc}")


def restore(app: str, key: Optional[str]) -> None:
    """Re-publish a key restored from the lock's saved state (startup)."""
    if not GATE_ENABLED:
        return
    _keys[app] = key
    _write_map()


def grant(app: str, response: Response) -> Optional[str]:
    """Mint a key for the new lock holder, publish it, and set the cookie.

    Returns the key so the caller can persist it with the lock state."""
    if not GATE_ENABLED:
        return None
    key = secrets.token_hex(32)
    _keys[app] = key
    _write_map()
    response.set_cookie(
        cookie_name(app), key,
        path=APP_PATHS[app], secure=True, httponly=True, samesite="lax",
    )
    logger.info(f"workbench gate: {app} access granted")
    return key


def revoke(app: str) -> None:
    """Withdraw access and cut live connections (fire-and-forget)."""
    if not GATE_ENABLED:
        return
    had_key = _keys.get(app) is not None
    _keys[app] = None
    _write_map()
    if not had_key:
        return
    logger.info(f"workbench gate: {app} access revoked")
    disconnect = _disconnect_jupyter if app == "jupyter" else _disconnect_obsidian
    try:
        asyncio.get_running_loop().create_task(disconnect())
    except RuntimeError:
        pass  # no loop (e.g. called at import time) -- nothing live to cut


async def _disconnect_jupyter() -> None:
    headers = {"Authorization": f"token {_SECRET}"}
    try:
        async with httpx.AsyncClient(base_url=_JUPYTER_INTERNAL, headers=headers, timeout=15) as c:
            for k in (await c.get("/api/kernels")).json():
                await c.delete(f"/api/kernels/{k['id']}")
            for t in (await c.get("/api/terminals")).json():
                await c.delete(f"/api/terminals/{t['name']}")
        logger.info("workbench gate: jupyter kernels and terminals shut down")
    except Exception as exc:
        logger.warning(f"workbench gate: could not shut down jupyter sessions: {exc}")


async def _disconnect_obsidian() -> None:
    try:
        async with httpx.AsyncClient(base_url=_DOCKER_HOST, timeout=60) as c:
            r = await c.post(f"/containers/{_OBSIDIAN_CONTAINER}/restart", params={"t": 10})
            r.raise_for_status()
        logger.info("workbench gate: obsidian container restarted")
    except Exception as exc:
        logger.warning(f"workbench gate: could not restart obsidian: {exc}")
