"""
REST API Explorer — FastAPI router.

Provides four endpoints:

  GET  /api/request-bodies           → Layer 1 request body catalog (static JSON, no Egeria needed)
  POST /api/request-bodies/rebuild   → regenerate catalog from http-client-collections
  GET  /api/rest-apis                → OpenAPI-based endpoint catalog (requires live Egeria)
  POST /api/rest-apis/refresh        → clear the in-process OpenAPI cache

To regenerate the catalog after an Egeria upgrade:
  python3 build_request_body_catalog.py [/path/to/http-client-collections]
  or POST /api/request-bodies/rebuild with {"http_collections_path": "..."}
"""

import asyncio
import ipaddress
import json
import os
import re
import socket
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import requests
import urllib3
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

router = APIRouter(tags=["rest-api-explorer"])

_HERE = Path(__file__).resolve().parent
_CATALOG_PATH = _HERE / "egeria_request_body_catalog.json"

# ── In-process caches ──────────────────────────────────────────────────────────

_catalog_cache: dict | None = None
_openapi_cache: dict[str, tuple[float, dict]] = {}  # url -> (fetched_at, spec)
_OPENAPI_TTL = 3600.0  # seconds; refresh forces immediate re-fetch


# ── Catalog helpers ────────────────────────────────────────────────────────────

def _load_catalog() -> dict:
    global _catalog_cache
    if _catalog_cache is None:
        if not _CATALOG_PATH.exists():
            raise HTTPException(
                status_code=503,
                detail=f"Catalog file not found at {_CATALOG_PATH}. "
                       "Run build_request_body_catalog.py to generate it.",
            )
        _catalog_cache = json.loads(_CATALOG_PATH.read_text())
        logger.info(f"Loaded request body catalog: {len(_catalog_cache.get('bodies', {}))} types")
    return _catalog_cache


def _rebuild_catalog(http_dir: Path) -> dict:
    """Re-run the extraction and overwrite the catalog JSON on disk."""
    from build_request_body_catalog import build_catalog  # local sibling module
    catalog = build_catalog(http_dir)
    _CATALOG_PATH.write_text(json.dumps(catalog, indent=2))
    global _catalog_cache
    _catalog_cache = catalog
    logger.info(f"Rebuilt catalog: {catalog['_meta']['bodyCount']} body types")
    return catalog


# ── OpenAPI helpers ────────────────────────────────────────────────────────────

def _bearer_token_for_spec_fetch(user_id: str, user_pwd: str, url: str, server: str) -> Optional[str]:
    """Best-effort bearer token for the plain `requests` call below -- prefers
    the per-request X-Egeria-Token (egeria_auth's contextvar) so this reuses
    whatever session the caller already has, falling back to minting a fresh
    one from env-var credentials. Never raises -- a failure here just means
    _fetch_openapi tries unauthenticated (which used to be enough; no longer
    is, see below), not that the whole request 500s."""
    from egeria_auth import get_request_token
    tok = get_request_token()
    if tok:
        return tok
    try:
        from pyegeria import ValidMetadataManager
        vmm = ValidMetadataManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
        token = vmm.create_egeria_bearer_token()
        vmm.close_session()
        return token
    except Exception as exc:
        logger.warning(f"Could not obtain bearer token for OpenAPI spec fetch: {exc}")
        return None


async def _async_bearer_token_for_spec_fetch(user_id: str, user_pwd: str, url: str, server: str) -> Optional[str]:
    """Async counterpart of _bearer_token_for_spec_fetch -- for the startup
    warm-up task below, which runs from an async context (the lifespan
    coroutine), not a request. CLAUDE.md's async-invariants note applies:
    the sync create_egeria_bearer_token() must never be called from async
    code (it calls asyncio.get_event_loop().run_until_complete() internally
    and raises on an already-running loop) -- use the _async_* method instead."""
    from egeria_auth import get_request_token
    tok = get_request_token()
    if tok:
        return tok
    try:
        from pyegeria import ValidMetadataManager
        vmm = ValidMetadataManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
        token = await vmm._async_create_egeria_bearer_token()
        vmm.close_session()
        return token
    except Exception as exc:
        logger.warning(f"Could not obtain bearer token for OpenAPI warm-up fetch: {exc}")
        return None


def _validate_platform_url(platform_url: str) -> None:
    """Reject SSRF-risky targets before we ever issue an outbound request.

    `platform_url` reaches here from the unauthenticated `url` query param on
    `GET /api/rest-apis` (see `get_rest_apis`), so it must be treated as
    attacker-controlled. The frontend never actually sends a custom `url`
    override for this endpoint (confirmed via grep on type-explorer.html --
    the param exists only for consistency with the app's broader url/server/
    user_id/user_pwd convention), so the only address that legitimately needs
    to work here is the deployment's own configured default.

    We resolve the hostname and reject it if it lands on a private/loopback/
    link-local/reserved/multicast address -- UNLESS the hostname matches the
    deployment's own default platform host, since that intentionally resolves
    to a Docker-internal address (compose service name / host.docker.internal)
    and is the one legitimate target.
    """
    default_host = urlparse(_env_defaults()["url"]).hostname
    parsed = urlparse(platform_url if "://" in platform_url else f"//{platform_url}")
    host = parsed.hostname
    if not host:
        raise HTTPException(status_code=400, detail="Invalid platform URL.")

    if default_host and host.lower() == default_host.lower():
        return  # the deployment's own platform -- intentionally internal

    try:
        addrinfo = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise HTTPException(status_code=400, detail=f"Could not resolve host: {host}") from exc

    for family, _, _, _, sockaddr in addrinfo:
        ip = ipaddress.ip_address(sockaddr[0])
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
            or ip.is_unspecified
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Refusing to fetch from a private/internal address: {host}",
            )


def _fetch_openapi(platform_url: str, server: str, user_id: str, user_pwd: str) -> dict:
    """Fetch the OpenAPI spec from a live Egeria platform (with caching).

    Auth added 2026-08-18 (Dan's report -- REST APIs view was a blank screen):
    these endpoints used to be reachable unauthenticated but now 401 without a
    bearer token (confirmed live: /v2/api-docs and /api-docs 401 anonymous,
    404 -- i.e. genuinely not found, past the auth check -- with a valid
    token; /v3/api-docs times out anonymous but returns 200 in ~21s with a
    token). Timeout bumped 30s -> 60s to give that ~21s real fetch headroom
    under load -- it was already close to the old timeout even when auth
    wasn't the blocker.

    SSRF guard added 2026-09-03 (CodeQL Critical alert): `platform_url` can
    be attacker-controlled via the unauthenticated `url` query param on the
    calling endpoint, so we validate it before issuing any outbound request.
    """
    _validate_platform_url(platform_url)

    cached = _openapi_cache.get(platform_url)
    if cached and (time.time() - cached[0]) < _OPENAPI_TTL:
        logger.debug(f"OpenAPI cache hit for {platform_url}")
        return cached[1]

    token = _bearer_token_for_spec_fetch(user_id, user_pwd, platform_url, server)
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    for path in ("/v3/api-docs", "/v2/api-docs", "/api-docs"):
        url = platform_url.rstrip("/") + path
        try:
            resp = requests.get(url, verify=False, timeout=60, headers=headers)
            if resp.status_code == 200:
                spec = resp.json()
                _openapi_cache[platform_url] = (time.time(), spec)
                logger.info(f"Fetched OpenAPI spec from {url}: "
                            f"{len(spec.get('paths', {}))} paths")
                return spec
        except Exception as exc:
            logger.debug(f"Failed to fetch {url}: {exc}")

    raise HTTPException(
        status_code=502,
        detail=f"Could not fetch OpenAPI spec from {platform_url}. "
               "Tried /v3/api-docs, /v2/api-docs, /api-docs.",
    )


def _resolve_ref(spec: dict, ref: str) -> dict:
    """Resolve a JSON $ref pointer within the OpenAPI spec."""
    if not ref.startswith("#/"):
        return {}
    parts = ref.lstrip("#/").split("/")
    node = spec
    for part in parts:
        if not isinstance(node, dict):
            return {}
        node = node.get(part, {})
    return node if isinstance(node, dict) else {}


def _schema_name_from_ref(ref: str) -> str:
    """Extract the bare schema name from a $ref string."""
    return ref.split("/")[-1] if ref else ""


def _find_body_ref(spec: dict, request_body: dict) -> str:
    """
    Walk the requestBody to find the primary $ref schema name.
    Returns the schema name (e.g. 'NewElementRequestBody') or ''.
    """
    content = request_body.get("content", {})
    schema = (
        content.get("application/json", {}).get("schema")
        or content.get("*/*", {}).get("schema")
        or {}
    )
    if not schema:
        return ""

    # Direct $ref
    if "$ref" in schema:
        return _schema_name_from_ref(schema["$ref"])

    # Resolve inline schema
    resolved = _resolve_ref(spec, schema.get("$ref", "")) if "$ref" in schema else schema

    # oneOf / anyOf: take the first entry
    for key in ("oneOf", "anyOf", "allOf"):
        variants = resolved.get(key, [])
        if variants and "$ref" in variants[0]:
            return _schema_name_from_ref(variants[0]["$ref"])

    return ""


def _infer_properties_type(
    spec: dict,
    body_schema_name: str,
    summary: str,
    path: str,
) -> str:
    """
    Try to determine the Layer 2 properties type name.

    Strategy (in order):
    1. Look at the body schema's 'properties.properties.$ref' — if it resolves
       to something ending in 'Properties' (not a generic), use it.
    2. Parse the operation summary for "Create/Update/Get a <TypeName>" patterns.
    3. Derive from the URL path's last meaningful segment.
    Returns '' when nothing confident can be determined.
    """
    # 1. Schema inspection
    if body_schema_name:
        body_schema = _resolve_ref(spec, f"#/components/schemas/{body_schema_name}")
        props_field = body_schema.get("properties", {}).get("properties", {})
        ref = props_field.get("$ref", "")
        if ref:
            name = _schema_name_from_ref(ref)
            if name.endswith("Properties") and name not in {
                "ElementProperties", "ReferenceableProperties",
                "OpenMetadataRootProperties",
            }:
                return name[: -len("Properties")]

    # 2. Summary heuristic
    if summary:
        m = re.search(
            r'\b(?:create|update|delete|get|find|retrieve)\s+(?:a\s+|an\s+|the\s+)?'
            r'([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)?)',
            summary,
            re.IGNORECASE,
        )
        if m:
            words = m.group(1).split()
            return "".join(w.capitalize() for w in words)

    # 3. URL segment heuristic — last non-placeholder segment before any verb suffixes
    segments = [
        s for s in path.split("/")
        if s and not s.startswith("{") and s not in {
            "api", "open-metadata", "servers", "create", "update", "delete",
            "get", "find", "by-name", "by-guid", "by-search-string",
        }
    ]
    if segments:
        raw = segments[-1].replace("-", " ").title().replace(" ", "")
        return _singularize(raw)

    return ""


def _singularize(word: str) -> str:
    """Best-effort English singular for a URL-derived type name, e.g.
    'Communities' → 'Community', 'UserIdentities' → 'UserIdentity',
    'Assets' → 'Asset'. Leaves short or non-plural words untouched."""
    if len(word) <= 4:
        return word
    if word.endswith("ies"):
        return word[:-3] + "y"
    if word.endswith(("ses", "xes", "zes", "ches", "shes")):
        return word[:-2]
    if word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def _extract_parameters(operation: dict) -> tuple[list, list]:
    """Return (path_params, query_params) as lists of dicts."""
    path_params, query_params = [], []
    for p in operation.get("parameters", []):
        entry = {
            "name":        p.get("name", ""),
            "required":    p.get("required", False),
            "description": p.get("description", ""),
            "schema":      p.get("schema", {}),
        }
        if p.get("in") == "path":
            path_params.append(entry)
        elif p.get("in") == "query":
            query_params.append(entry)
    return path_params, query_params


def _process_openapi(spec: dict, catalog: dict) -> dict:
    """
    Translate the raw OpenAPI spec into a structured endpoint catalog.

    Returns:
        {
          "services": [
            { "tag": str, "endpointCount": int, "endpoints": [...] }
          ]
        }
    """
    known_bodies: set[str] = set(catalog.get("bodies", {}).keys())

    # Collect all operations, grouped by primary tag
    tag_map: dict[str, list] = {}

    for path, path_item in spec.get("paths", {}).items():
        for method, operation in path_item.items():
            if method not in {"get", "post", "put", "patch", "delete"}:
                continue
            if not isinstance(operation, dict):
                continue

            tags = operation.get("tags", ["Other"])
            primary_tag = tags[0] if tags else "Other"

            summary = operation.get("summary", "")
            request_body = operation.get("requestBody", {})
            body_schema_name = _find_body_ref(spec, request_body) if request_body else ""

            # Validate — only record body types we know about
            outer_body = body_schema_name if body_schema_name in known_bodies else ""
            properties_type = _infer_properties_type(
                spec, body_schema_name, summary, path
            ) if body_schema_name else ""

            path_params, query_params = _extract_parameters(operation)

            endpoint = {
                "method":          method.upper(),
                "path":            path,
                "operationId":     operation.get("operationId", ""),
                "summary":         summary,
                "description":     operation.get("description", ""),
                "outerBodyType":   outer_body,
                "rawBodySchema":   body_schema_name,  # even if not in catalog
                "propertiesType":  properties_type,
                "pathParams":      path_params,
                "queryParams":     query_params,
            }

            tag_map.setdefault(primary_tag, []).append(endpoint)

    services = [
        {
            "tag":           tag,
            "endpointCount": len(eps),
            "endpoints":     sorted(eps, key=lambda e: (e["path"], e["method"])),
        }
        for tag, eps in sorted(tag_map.items())
    ]

    return {"services": services}


# ── Default connection ─────────────────────────────────────────────────────────

def _env_defaults() -> dict:
    return {
        "url":      os.environ.get("EGERIA_PLATFORM_URL",  "https://egeria-main:9443"),
        "server":   os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server"),
        "user_id":  os.environ.get("EGERIA_USER",          "erinoverview"),
        "user_pwd": os.environ.get("EGERIA_USER_PASSWORD", "secret"),
    }


# ── Routes ─────────────────────────────────────────────────────────────────────

@router.get(
    "/api/request-bodies",
    summary="Get the Layer 1 request body catalog",
)
def get_request_bodies():
    """
    Return the complete Egeria outer request body catalog.

    This is a static JSON document derived from the Egeria http-client-collections.
    It requires no live Egeria connection and loads from disk on first call.
    Regenerate it after an Egeria upgrade by running build_request_body_catalog.py.
    """
    return JSONResponse(_load_catalog())


class RebuildRequest(BaseModel):
    http_collections_path: str | None = None


def _validate_http_collections_dir(raw_path: str) -> Path:
    """Reject path-traversal-risky targets before reading files from disk.

    `raw_path` can reach here from the unauthenticated `http_collections_path`
    field on `POST /api/request-bodies/rebuild` (CodeQL High: py/path-injection),
    so it must be treated as attacker-controlled -- an unrestricted value would
    let a caller point this at any readable directory in the container and have
    its *.http files parsed and echoed back via the public `GET
    /api/request-bodies` endpoint.

    Restrict to an explicit allowlist of roots: the HTTP_COLLECTIONS_ALLOWED_ROOTS
    env var (colon-separated absolute paths) if set, otherwise just the directory
    named by HTTP_COLLECTIONS_PATH itself -- i.e. by default, the request body's
    override is only honored when it resolves to the same, admin-configured
    directory an unauthenticated caller couldn't otherwise redirect. A deployment
    that genuinely wants the flexible "point anywhere" workflow can opt back in
    by setting HTTP_COLLECTIONS_ALLOWED_ROOTS explicitly.
    """
    http_dir = Path(raw_path).resolve()
    if not http_dir.is_dir():
        raise HTTPException(status_code=422, detail=f"Directory not found: {http_dir}")

    env_roots = os.environ.get("HTTP_COLLECTIONS_ALLOWED_ROOTS")
    if env_roots:
        allowed_roots = [Path(p).resolve() for p in env_roots.split(":") if p]
    else:
        env_default = os.environ.get("HTTP_COLLECTIONS_PATH")
        allowed_roots = [Path(env_default).resolve()] if env_default else []

    if not allowed_roots:
        raise HTTPException(
            status_code=400,
            detail=(
                "Refusing to read an arbitrary directory: neither HTTP_COLLECTIONS_PATH "
                "nor HTTP_COLLECTIONS_ALLOWED_ROOTS is configured on this deployment. "
                "Set one of these environment variables to the http-client-collections "
                "location before calling this endpoint."
            ),
        )
    if not any(http_dir == root or http_dir.is_relative_to(root) for root in allowed_roots):
        raise HTTPException(
            status_code=400,
            detail=f"Directory not permitted: {http_dir}. Set HTTP_COLLECTIONS_ALLOWED_ROOTS "
                   "to allow additional locations.",
        )
    return http_dir


@router.post(
    "/api/request-bodies/rebuild",
    summary="Regenerate the request body catalog",
)
def rebuild_request_bodies(body: RebuildRequest = RebuildRequest()):
    """
    Re-extract all outer body types from the http-client-collections directory
    and overwrite egeria_request_body_catalog.json.

    Supply http_collections_path in the request body, or set the
    HTTP_COLLECTIONS_PATH environment variable before starting the server.
    """
    raw_path = (
        body.http_collections_path
        or os.environ.get("HTTP_COLLECTIONS_PATH")
    )
    if not raw_path:
        raise HTTPException(
            status_code=422,
            detail=(
                "Provide http_collections_path in the request body "
                "or set the HTTP_COLLECTIONS_PATH environment variable."
            ),
        )
    http_dir = _validate_http_collections_dir(raw_path)
    try:
        catalog = _rebuild_catalog(http_dir)
        return {
            "status":    "success",
            "bodyCount": catalog["_meta"]["bodyCount"],
            "source":    str(http_dir),
        }
    except Exception as exc:
        logger.exception(f"Catalog rebuild failed: {exc}")
        raise HTTPException(status_code=500, detail=f"Rebuild failed: {exc}")


@router.get(
    "/api/rest-apis",
    summary="Get the OpenAPI endpoint catalog",
)
def get_rest_apis(
    url:      Optional[str] = Query(None, description="Egeria platform URL"),
    server:   Optional[str] = Query(None, description="Egeria view server name"),
    user_id:  Optional[str] = Query(None, description="Egeria user id (overrides env)"),
    user_pwd: Optional[str] = Query(None, description="Egeria user password (overrides env)"),
):
    """
    Fetch the Egeria OpenAPI spec and return a structured endpoint catalog,
    augmented with Layer 1 body type information from the local catalog.

    Results are cached in process for one hour; call POST /api/rest-apis/refresh
    to force an immediate re-fetch.
    """
    d = _env_defaults()
    platform_url = url      or d["url"]
    server       = server   or d["server"]
    user_id      = user_id  or d["user_id"]
    user_pwd     = user_pwd or d["user_pwd"]

    try:
        spec    = _fetch_openapi(platform_url, server, user_id, user_pwd)
        catalog = _load_catalog()
        result  = _process_openapi(spec, catalog)
        return JSONResponse(result)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception(f"REST API catalog failed: {exc}")
        raise HTTPException(status_code=500, detail=f"Failed: {exc}")


@router.post(
    "/api/rest-apis/refresh",
    summary="Clear the OpenAPI spec cache",
)
def refresh_rest_apis(
    url: Optional[str] = Query(None, description="Egeria platform URL to clear (clears all if omitted)"),
):
    """Force the next GET /api/rest-apis call to re-fetch the OpenAPI spec."""
    if url:
        _openapi_cache.pop(url, None)
        return {"status": "cleared", "url": url}
    _openapi_cache.clear()
    return {"status": "cleared", "entries": "all"}


# ── Startup warm-up (background, non-blocking) ─────────────────────────────────

# Overall cap on the warm-up task's own runtime -- belt-and-braces on top of
# it already being fire-and-forget (asyncio.create_task, never awaited by
# the lifespan). Incident 2026-09-03: a *different*, pre-existing bug
# (bootstrap_monitor_handler.py's unbounded, AWAITED canary-check loop) once
# blocked the whole app's startup for several minutes; this warm-up task was
# never actually the cause, but the postmortem's lesson stands regardless --
# nothing that talks to a possibly-degraded Egeria should run unbounded, even
# when it's structurally non-blocking today. See bootstrap_monitor_handler.py
# _CANARY_CHECK_TIMEOUT for the sibling fix on the call that WAS the cause.
_WARMUP_TIMEOUT = int(os.environ.get("REST_APIS_WARMUP_TIMEOUT_SECONDS", "60"))


async def warm_openapi_cache() -> None:
    """Populate the OpenAPI spec cache for the default platform at startup
    (fire-and-forget from pyegeria_handler.py's lifespan) so the REST APIs
    tab and portal search (see search_rest_apis below) both have data ready
    immediately, instead of every deployment's first visitor eating the
    ~20s cold fetch. New/changed REST endpoints only actually appear after
    an Egeria platform restart anyway (that's the whole reason the OpenAPI
    spec fetch is cached at all, see _OPENAPI_TTL) -- so warming it once at
    our own startup, refreshed hourly by the existing TTL, is exactly as
    fresh as this data can ever meaningfully be.

    Runs its own HTTP fetch via httpx.AsyncClient rather than calling
    _fetch_openapi() directly -- that function's requests.get() is a
    blocking sync call, which would stall the event loop for the ~20s
    cold-fetch duration if awaited directly here.

    Must be launched via asyncio.create_task(), never awaited directly from
    the lifespan -- see pyegeria_handler.py. The whole body is additionally
    wrapped in asyncio.wait_for(_WARMUP_TIMEOUT) so even a badly-behaved
    Egeria can't leave this task running indefinitely.

    Best-effort: any failure (platform not reachable yet at our own
    startup, credentials not ready, timeout, etc.) is logged and
    swallowed -- the first real GET /api/rest-apis call falls back to the
    normal on-demand fetch exactly as it did before this existed.
    """
    try:
        await asyncio.wait_for(_warm_openapi_cache_body(), timeout=_WARMUP_TIMEOUT)
    except asyncio.TimeoutError:
        logger.warning(f"OpenAPI cache warm-up timed out after {_WARMUP_TIMEOUT}s -- Egeria is likely slow/degraded")
    except Exception as exc:
        logger.warning(f"OpenAPI cache warm-up failed: {exc}")


async def _warm_openapi_cache_body() -> None:
    d = _env_defaults()
    platform_url, server, user_id, user_pwd = d["url"], d["server"], d["user_id"], d["user_pwd"]
    try:
        _validate_platform_url(platform_url)
    except HTTPException as exc:
        logger.warning(f"OpenAPI cache warm-up skipped -- platform URL rejected: {exc.detail}")
        return

    token = await _async_bearer_token_for_spec_fetch(user_id, user_pwd, platform_url, server)
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    import httpx
    async with httpx.AsyncClient(verify=False, timeout=30) as client:
        for path in ("/v3/api-docs", "/v2/api-docs", "/api-docs"):
            url = platform_url.rstrip("/") + path
            try:
                resp = await client.get(url, headers=headers)
                if resp.status_code == 200:
                    spec = resp.json()
                    _openapi_cache[platform_url] = (time.time(), spec)
                    logger.info(f"Warmed OpenAPI cache from {url}: {len(spec.get('paths', {}))} paths")
                    return
            except Exception as exc:
                logger.debug(f"OpenAPI warm-up: failed to fetch {url}: {exc}")


# ── Search (used by catalog_search_handler.py's portal-wide omni-search) ──────

def search_rest_apis(query: str, limit: int = 40) -> list[dict]:
    """Case-insensitive substring search over the REST API endpoint catalog
    (method, path, operationId, summary, description). Reads ONLY from
    whatever's already in _openapi_cache (populated by warm_openapi_cache()
    at startup, or by a prior GET /api/rest-apis call) -- deliberately does
    NOT trigger a fresh fetch itself, so a portal search never blocks on a
    live ~20s Egeria round-trip. Returns [] if nothing is cached yet for the
    default platform (e.g. it was unreachable at our own startup and no one
    has opened the REST APIs tab since).
    """
    q = query.lower().strip()
    if not q:
        return []
    platform_url = _env_defaults()["url"]
    cached = _openapi_cache.get(platform_url)
    if not cached:
        return []

    try:
        catalog = _load_catalog()
        processed = _process_openapi(cached[1], catalog)
    except Exception:
        logger.exception("search_rest_apis: failed to process cached OpenAPI spec")
        return []

    name_hits: list[dict] = []
    text_hits: list[dict] = []
    for svc in processed["services"]:
        for ep in svc["endpoints"]:
            name_hay = f"{ep['method']} {ep['path']} {ep.get('operationId', '')}".lower()
            text_hay = f"{ep.get('summary', '')} {ep.get('description', '')}".lower()
            bucket = name_hits if q in name_hay else (text_hits if q in text_hay else None)
            if bucket is not None:
                bucket.append({
                    "tag": svc["tag"], "method": ep["method"], "path": ep["path"],
                    "summary": ep.get("summary") or "",
                })

    return (name_hits + text_hits)[:limit]
