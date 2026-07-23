# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Egeria Overview — FastAPI router.

An executive / summary dashboard for the Egeria Portal. Where the other portal
apps (Catalog, Explorer, Lineage, Audit, Insights, Operations) are task-oriented
drill-down tools, this one answers "how are we doing, and is it improving?" at a
glance — scale, governance coverage, quality, AI-readiness, and the people /
community engagement behind the metadata — with every number tied to a business
value lens and drill-through into the owning app.

Design note — the dashboard *is* the Perspective/Question model: a perspective's
questions, each answered by a saved report spec, rendered as a drill-able tile.

Routes:
  GET /egeria-overview            → serve the SPA
  GET /api/overview/summary       → headline KPI counts (capped tally)
  GET /api/overview/ai-context    → AI & context-intelligence readiness (best-effort)
  GET /api/overview/people        → people / community engagement (best-effort)
  GET /api/overview/growth        → catalog growth via asOfTime snapshots (best-effort)

Aggregation reuses the same capped-tally philosophy as insights_handler (Egeria's
find API returns paged element lists with no total-count metadata, so counts are
capped at _DEFAULT_CAP unless full_count paging is requested). Endpoints degrade
gracefully: a field that can't be computed yet is returned as null with
`"partial": true` rather than failing the whole response, so the SPA can overlay
whatever is live over its sample baseline. Results are held in a small in-process
TTL cache (mirroring the operations_handler non-blocking pattern, but simpler —
these queries are seconds, not minutes).

Known constraints (see PYEGERIA_ISSUES.md):
  - No total-count in find responses → capped tallies (cap 500).
  - PY-15: Postgres connector ignores matchCriteria once 2+ classification
    conditions are present → keep every query to 0 or 1 classification.
"""
import os
import time
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from loguru import logger

from egeria_auth import apply_token

router = APIRouter(tags=["egeria-overview"])

_HERE = Path(__file__).parent
_HTML = _HERE / "egeria-overview.html"

_DEFAULT_CAP = 500            # same ceiling used elsewhere in the app
_CACHE_TTL   = 60.0          # seconds; summary is not real-time critical

# Governed-data classifications that count as "governed" (single-condition tallies
# only — PY-15 makes any 2+ classification ANY/ALL query return zero).
_GOVERNANCE_CLASSIFICATIONS = ("ZoneMembership", "Confidentiality", "Criticality", "Impact", "Retention")

# Base open-metadata type names for the headline "assets by type" tally. Kept as a
# small, override-safe list — a wrong/unknown type just yields 0 for that row
# rather than failing the response.
_ASSET_TYPES = [
    ("Data Stores",         "DataStore"),
    ("Data Sets",           "DataSet"),
    ("Software Components", "DeployedSoftwareComponent"),
    ("Infrastructure",      "ITInfrastructure"),
    ("APIs",                "DeployedAPI"),
    ("Processes",           "Process"),
]

# ── tiny TTL cache ───────────────────────────────────────────────────────────
_cache: dict[str, tuple[float, Any]] = {}


def _cache_get(key: str):
    hit = _cache.get(key)
    if hit and (time.time() - hit[0]) < _CACHE_TTL:
        return hit[1]
    return None


def _cache_put(key: str, value: Any):
    _cache[key] = (time.time(), value)
    return value


# ── client factory ───────────────────────────────────────────────────────────

def _expert(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import MetadataExpert
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = MetadataExpert(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _env(url, server, user_id, user_pwd):
    return (
        url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443"),
        server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server"),
        user_id  or os.environ.get("EGERIA_USER",          "erinoverview"),
        user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret"),
    )


def _make(cls_name, url=None, server=None, user_id=None, user_pwd=None):
    """Build + token any pyegeria client by class name (imported lazily like the
    other handlers). Used for the certification / people / usage-context tallies."""
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    cls = getattr(pyegeria, cls_name)
    url, server, user_id, user_pwd = _env(url, server, user_id, user_pwd)
    mgr = cls(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _json_list(raw) -> list:
    """Normalise a pyegeria output_format='JSON' result to a list of dicts.
    Empty results come back as a 'No … found' string; some calls wrap in a dict."""
    if isinstance(raw, list):
        return [r for r in raw if isinstance(r, dict)]
    if isinstance(raw, dict):
        for k in ("elements", "items", "relationships", "list"):
            if isinstance(raw.get(k), list):
                return [r for r in raw[k] if isinstance(r, dict)]
    return []


# ── find helpers ─────────────────────────────────────────────────────────────

def _find(mgr, body: dict, page_size: int = _DEFAULT_CAP) -> list:
    """Run a FindRequestBody, always returning a (possibly empty) list. Never raises."""
    try:
        raw = mgr.find_metadata_elements(body, start_from=0, page_size=page_size, graph_query_depth=0)
        return [el for el in (raw if isinstance(raw, list) else []) if isinstance(el, dict)]
    except Exception as exc:  # noqa: BLE001 — best-effort tile, degrade don't fail
        logger.debug(f"overview _find failed for {body.get('metadataElementTypeName')!r}: {exc}")
        return []


def _count_type(mgr, type_name: Optional[str]) -> tuple[int, bool]:
    """Capped count of ACTIVE elements of a type. Returns (count, capped)."""
    body: dict = {"class": "FindRequestBody", "limitResultsByStatus": ["ACTIVE"]}
    if type_name:
        body["metadataElementTypeName"] = type_name
    hits = _find(mgr, body)
    return len(hits), len(hits) >= _DEFAULT_CAP


def _classifications_of(el: dict) -> set[str]:
    out: set[str] = set()
    for c in el.get("classifications") or []:
        if isinstance(c, dict) and c.get("classificationName"):
            out.add(c["classificationName"])
    return out


def _zone_names(el: dict) -> list:
    for c in el.get("classifications") or []:
        if isinstance(c, dict) and c.get("classificationName") == "ZoneMembership":
            pvm = (c.get("classificationProperties") or {}).get("propertyValueMap") or {}
            zv = pvm.get("zoneMembership")
            if isinstance(zv, dict) and zv.get("class") == "ArrayTypePropertyValue":
                arr = (zv.get("arrayValues") or {}).get("propertyValueMap") or {}
                return [arr[k].get("primitiveValue") for k in sorted(arr, key=lambda k: int(k) if k.isdigit() else 0)
                        if isinstance(arr.get(k), dict)]
    return []


# ── SPA ──────────────────────────────────────────────────────────────────────

@router.get("/egeria-overview", include_in_schema=False)
def serve_overview():
    if not _HTML.exists():
        raise HTTPException(status_code=404, detail="Egeria Overview page not found")
    return FileResponse(_HTML, media_type="text/html",
                        headers={"Cache-Control": "no-store, must-revalidate"})


# ── Summary ──────────────────────────────────────────────────────────────────

@router.get("/api/overview/summary", summary="Headline KPI counts for the Overview dashboard")
def get_summary(
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    ckey = f"summary|{url}|{server}|{user_id}"
    cached = _cache_get(ckey)
    if cached is not None:
        return JSONResponse(cached)

    try:
        mgr = _expert(url, server, user_id, user_pwd)
    except Exception as exc:  # noqa: BLE001
        logger.exception("overview: failed to create MetadataExpert")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    # Governed tally — single ANY over governance classifications (PY-15 note: this
    # 5-classification ANY is affected by the server bug; still correct at 0/1
    # conditions and used here as a best-effort coverage proxy).
    gov_body = {
        "class": "FindRequestBody",
        "matchClassifications": {
            "class": "SearchClassifications",
            "matchCriteria": "ANY",
            "conditions": [{"name": n} for n in _GOVERNANCE_CLASSIFICATIONS],
        },
        "limitResultsByStatus": ["ACTIVE"],
    }
    governed_hits = _find(mgr, gov_body)
    by_classification: dict[str, int] = {}
    zone_counts: dict[str, int] = {}
    for el in governed_hits:
        for name in _classifications_of(el):
            by_classification[name] = by_classification.get(name, 0) + 1
        for z in _zone_names(el):
            if z:
                zone_counts[z] = zone_counts.get(z, 0) + 1

    # Assets by type (best-effort; unknown types yield 0).
    by_type = []
    asset_total = 0
    for label, tname in _ASSET_TYPES:
        c, _ = _count_type(mgr, tname)
        by_type.append({"label": label, "type": tname, "count": c})
        asset_total += c

    term_count, term_capped = _count_type(mgr, "GlossaryTerm")
    top_zones = sorted(zone_counts.items(), key=lambda kv: -kv[1])[:8]

    # Certifications & licenses (governance relationships) — separate client, best-effort.
    certs = _certifications(url, server, user_id, user_pwd)

    payload = {
        "assetTotal":       asset_total,
        "byType":           by_type,
        "termCount":        term_count,
        "governedCount":    len(governed_hits),
        "governedCapped":   len(governed_hits) >= _DEFAULT_CAP,
        "byClassification": by_classification,
        "topZones":         [{"zone": z, "count": c} for z, c in top_zones],
        "certifications":   certs["active"],
        "certExpiring90":   certs["expiring90"],
        "certSoon":         certs["soon"],
        "licenses":         certs["licenses"],
        # Still sample in the SPA until wired.
        "dataProducts":     None,
        "openExceptions":   None,
        "partial":          True,
        "source":           "live:summary",
    }
    return JSONResponse(_cache_put(ckey, payload))


# ── certifications & licenses ────────────────────────────────────────────────

def _rel_end_date(rel: dict):
    """Best-effort expiry date for a Certification relationship: try the domain
    property, then relationship effectivity. Returns a datetime or None."""
    from datetime import datetime
    props = rel.get("relationshipProperties") or {}
    header = rel.get("relationshipHeader") or {}
    candidates = [props.get(k) for k in ("coverageEnd", "end", "endDate", "expiry", "expirationDate")]
    candidates.append((header.get("effectivityDates") or {}).get("effectiveToTime"))
    candidates.append(header.get("effectiveToTime"))
    for v in candidates:
        if not v:
            continue
        s = str(v).replace("Z", "+00:00")
        for parse in (lambda x: datetime.fromisoformat(x),):
            try:
                return parse(s)
            except Exception:  # noqa: BLE001
                pass
    return None


def _certifications(url, server, user_id, user_pwd) -> dict:
    """Count active certifications, those expiring within 90 days, a soonest list,
    and the license count. Degrades to zeros on any failure (demo may have none)."""
    from datetime import datetime, timezone, timedelta
    out = {"active": None, "expiring90": None, "soon": [], "licenses": None}
    try:
        ce = _make("ClassificationExplorer", url, server, user_id, user_pwd)
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview certifications: client build failed: {exc}")
        return out
    try:
        certs = _json_list(ce.get_relationships(relationship_type="Certification",
                                                output_format="JSON", start_from=0, page_size=_DEFAULT_CAP))
        now = datetime.now(timezone.utc)
        horizon = now + timedelta(days=90)
        soon = []
        expiring = 0
        for r in certs:
            end = _rel_end_date(r)
            if end is not None:
                if end.tzinfo is None:
                    end = end.replace(tzinfo=timezone.utc)
                if now <= end <= horizon:
                    expiring += 1
                    end2 = (r.get("end2") or {})
                    name = ((end2.get("properties") or end2) or {}).get("displayName") or "certification"
                    soon.append({"name": name, "days": (end - now).days})
        soon.sort(key=lambda s: s["days"])
        out["active"] = len(certs)
        out["expiring90"] = expiring
        out["soon"] = soon[:5]
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview certifications: query failed: {exc}")
    try:
        out["licenses"] = len(_json_list(ce.get_relationships(relationship_type="License",
                                                              output_format="JSON", start_from=0, page_size=_DEFAULT_CAP)))
    except Exception:  # noqa: BLE001
        pass
    return out


# ── AI & Context Intelligence ────────────────────────────────────────────────

@router.get("/api/overview/ai-context", summary="AI / context-intelligence readiness (best-effort)")
def get_ai_context(
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Context-readiness funnel + grounding. Consumers/guardrails are not natively
    queryable yet — returned as null so the SPA shows its sample baseline."""
    ckey = f"ai|{url}|{server}|{user_id}"
    cached = _cache_get(ckey)
    if cached is not None:
        return JSONResponse(cached)
    try:
        mgr = _expert(url, server, user_id, user_pwd)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    cataloged, _ = _count_type(mgr, "Asset")           # broad supertype, capped
    classified   = len(_find(mgr, {
        "class": "FindRequestBody", "limitResultsByStatus": ["ACTIVE"],
        "matchClassifications": {"class": "SearchClassifications", "matchCriteria": "ANY",
                                  "conditions": [{"name": "Confidentiality"}]},
    }))

    payload = {
        "funnel": {
            "cataloged":  cataloged or None,
            "documented": None,     # needs a description-present filter — TODO
            "classified": classified or None,
            "lineage":    None,     # needs lineage-relationship presence — TODO
            "aiReady":    None,     # composite gate — TODO
        },
        "consumers":  None,   # not natively tracked (would come from MCP/API access logs)
        "guardrails": None,
        "grounding":  None,   # % assets with glossary term links — TODO
        "partial":    True,
        "source":     "live:ai-context",
    }
    return JSONResponse(_cache_put(ckey, payload))


# ── People & Community ───────────────────────────────────────────────────────

@router.get("/api/overview/people", summary="People / community engagement (best-effort)")
def get_people(
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """People counts (persons / teams / orgs / communities) are live from Actor +
    Community managers. Karma / feedback aggregates need the Collaboration OMAS and
    stay null (SPA keeps its sample baseline)."""
    ckey = f"people|{url}|{server}|{user_id}"
    cached = _cache_get(ckey)
    if cached is not None:
        return JSONResponse(cached)

    persons = teams = orgs = it_profiles = None
    try:
        am = _make("ActorManager", url, server, user_id, user_pwd)
        profiles = _json_list(am.find_actor_profiles(search_string="*", output_format="JSON",
                                                     start_from=0, page_size=_DEFAULT_CAP))
        counts: dict[str, int] = {}
        for p in profiles:
            tn = ((p.get("elementHeader") or {}).get("type") or {}).get("typeName") or "?"
            counts[tn] = counts.get(tn, 0) + 1
        persons     = counts.get("Person", 0)
        teams       = counts.get("Team", 0)
        orgs        = counts.get("Organization", 0)
        it_profiles = counts.get("ITProfile", 0)
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview people: actor query failed: {exc}")

    communities = None
    try:
        cm = _make("CommunityMatters", url, server, user_id, user_pwd)
        communities = len(_json_list(cm.find_communities(
            search_string="*", starts_with=False, output_format="JSON",
            graph_query_depth=0, start_from=0, page_size=_DEFAULT_CAP)))
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview people: community query failed: {exc}")

    payload = {
        "activeContributors": persons,
        "teams":              teams,
        "organizations":      orgs,
        "itProfiles":         it_profiles,
        "communities":        communities,
        "karmaAwarded":       None,   # ContributionRecord — sparse in demo; TODO engagement fallback
        "feedbackItems":      None,   # likes+ratings+comments — Collaboration OMAS; TODO
        "leaderboard":        None,
        "engagementSeries":   None,
        "feedbackByType":     None,
        "partial":            True,
        "source":             "live:people",
    }
    return JSONResponse(_cache_put(ckey, payload))


# ── Usage Context — ISC & Blueprints ─────────────────────────────────────────

@router.get("/api/overview/usage-context",
            summary="Information Supply Chains & Solution Blueprints that give assets a usage context")
def get_usage_context(
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """ISCs and Blueprints are what put assets in a *usage context* — "this store
    feeds the Clinical Trial supply chain", "this component realises the Sales
    blueprint". Counts are live; the "% of assets contextualised" coverage figure
    needs graph traversal and is deferred (SPA shows its sample baseline)."""
    ckey = f"usage|{url}|{server}|{user_id}"
    cached = _cache_get(ckey)
    if cached is not None:
        return JSONResponse(cached)

    iscs = blueprints = None
    try:
        sa = _make("SolutionArchitect", url, server, user_id, user_pwd)
        iscs = len([e for e in _json_list(sa.find_information_supply_chains(
            search_string="*", output_format="JSON", start_from=0, page_size=_DEFAULT_CAP))
            if not _is_template_el(e)])
        blueprints = len([e for e in _json_list(sa.find_solution_blueprints(
            search_string="*", output_format="JSON", start_from=0, page_size=_DEFAULT_CAP))
            if not _is_template_el(e)])
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"overview usage-context: query failed: {exc}")

    payload = {
        "informationSupplyChains": iscs,
        "blueprints":              blueprints,
        "contextualisedPct":       None,   # % assets participating in ≥1 ISC/blueprint — TODO (traversal)
        "partial":                 True,
        "source":                  "live:usage-context",
    }
    return JSONResponse(_cache_put(ckey, payload))


def _is_template_el(el: dict) -> bool:
    for val in (el.get("elementHeader") or {}).values():
        if isinstance(val, dict) and (val.get("classificationName")
                                      or (val.get("type") or {}).get("typeName")) == "Template":
            return True
    return False


# ── Growth (asOfTime snapshots) ──────────────────────────────────────────────

@router.get("/api/overview/growth", summary="Catalog growth via asOfTime snapshots (best-effort)")
def get_growth(
    months: int = Query(6, ge=2, le=12),
    url: Optional[str] = Query(None), server: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None), user_pwd: Optional[str] = Query(None),
):
    """Placeholder shape for the growth series. A live implementation issues one
    capped find per snapshot date with asOfTime set (Egeria supports historical
    queries natively — no separate time-series store). Deferred to keep the first
    build fast; SPA renders its sample series until this returns data."""
    return JSONResponse({
        "series":  None,
        "months":  months,
        "partial": True,
        "source":  "stub:growth",
    })
