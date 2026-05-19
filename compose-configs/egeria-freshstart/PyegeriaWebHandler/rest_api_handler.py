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

import json
import os
import re
import time
from pathlib import Path
from typing import Optional

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

def _fetch_openapi(platform_url: str) -> dict:
    """Fetch the OpenAPI spec from a live Egeria platform (with caching)."""
    cached = _openapi_cache.get(platform_url)
    if cached and (time.time() - cached[0]) < _OPENAPI_TTL:
        logger.debug(f"OpenAPI cache hit for {platform_url}")
        return cached[1]

    for path in ("/v3/api-docs", "/v2/api-docs", "/api-docs"):
        url = platform_url.rstrip("/") + path
        try:
            resp = requests.get(url, verify=False, timeout=30)
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
        # Strip trailing plural 's' to get type name
        if raw.endswith("s") and len(raw) > 4:
            raw = raw[:-1]
        return raw

    return ""


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
        "url":     os.environ.get("EGERIA_PLATFORM_URL", "https://egeria-main:9443"),
        "server":  os.environ.get("EGERIA_VIEW_SERVER",  "qs-view-server"),
        "user_id": os.environ.get("EGERIA_USER",         "erinoverview"),
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
    http_dir = Path(raw_path)
    if not http_dir.is_dir():
        raise HTTPException(
            status_code=422,
            detail=f"Directory not found: {http_dir}",
        )
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
    url:     Optional[str] = Query(None, description="Egeria platform URL"),
    server:  Optional[str] = Query(None, description="Egeria view server name"),
):
    """
    Fetch the Egeria OpenAPI spec and return a structured endpoint catalog,
    augmented with Layer 1 body type information from the local catalog.

    Results are cached in process for one hour; call POST /api/rest-apis/refresh
    to force an immediate re-fetch.
    """
    d = _env_defaults()
    platform_url = url or d["url"]

    try:
        spec    = _fetch_openapi(platform_url)
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
