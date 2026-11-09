"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Shared SemanticAssignment lookup.

Used to badge both physical schema elements (tech_catalog_handler.py's
SchemaPane) and logical Data Design elements (data_design_handler.py's
DataField/DataStructure detail, where it's already surfaced generically under
the raw "assignedMeanings" key -- see _extract_all_rels) with their assigned
glossary term(s), and to answer the reverse question from a GlossaryTerm's
side ("which physical and logical elements point to me?") in glossary_handler.py.

Per https://egeria-project.org/types/3/0370-Semantic-Assignment/, end1 is the
assigned element ("elements", many), end2 is the GlossaryTerm ("meanings",
many). insights_handler.py's module docstring documents a confirmed-live
finding (2026-08-06) that SemanticAssignment's REAL participant *types* are
broader/different than its declared ends -- that finding is about which
entity types populate each end, not which end is which, so the
end1=element/end2=term convention below still holds. As a defensive backstop
we trust each end's own `type.typeName` over position when it's present and
disagrees with the positional default.

One bounded paged read per call (at most _REL_PAGES pages of _REL_PAGE), not one call per element --
the same "commonly interesting, not exhaustive" tradeoff
insights_handler.py's _relationship_type_stats already makes for this app,
reused here rather than reimplemented.
"""
import threading
import time
from typing import Optional

from loguru import logger

# Egeria refuses pageSize > 1000 (OMAG-COMMON-400-010). The old single read of
# 2000 was refused on every call, and the failure was swallowed into [] -- so the
# term's "Where is this used?" panel and the schema tree's term badges said
# "nothing assigned" against a store holding hundreds of assignments. Read pages
# of 1000; only an EMPTY page ends the read (a short page is not the last one,
# per Egeria's paging contract). Still bounded: this feeds interactive
# badges/lookups, not a governance-audit total.
_REL_PAGE = 1000
_REL_PAGES = 5
READ_LIMIT = _REL_PAGE * _REL_PAGES     # shown to people when a read stops here ("the read stopped at 5,000")

# The paged read is the slow part (measured live 2026-11-09, 747 assignments: the term panel ~9 s, an asset's
# schema tree with term badges ~16 s). Both use the same read, so it is cached briefly and shared between them.
# Key: the caller's hashed credential (result_cache.request_identity -- never a bare user id or a token's
# sub; zone security can hide assignments from some viewers), the platform/server read, the As-of time and the
# forLineage toggle. A caller with no identity (an expired token) passes None: no cache. Only a successful
# read is cached; a short TTL keeps new assignments visible within two minutes.
_ASSIGN_TTL = 120
_ASSIGN_CACHE: dict = {}      # key -> (stored_at, links, capped)
_ASSIGN_LOCK = threading.Lock()


def _assign_cache_key(ce, identity: Optional[str], as_of_time: Optional[str]) -> Optional[str]:
    if not identity:
        return None
    from egeria_auth import lineage_key
    return (f"{getattr(ce, 'platform_url', '')}|{getattr(ce, 'view_server', '')}|{identity}"
            f"|{as_of_time or ''}{lineage_key()}")


def _flat_props(props_dict: dict) -> dict:
    """Flatten a properties dict that may use propertyValueMap encoding.
    Duplicated from tech_catalog_handler.py's helper of the same name — kept
    local so this module has no import-order dependency on any one app's
    handler (data_design_handler.py and glossary_handler.py both use it too)."""
    if not isinstance(props_dict, dict):
        return {}
    flat = {}
    prop_map = props_dict.get("propertyValueMap") or {}
    if prop_map:
        for k, v in prop_map.items():
            pv = v.get("primitiveValue", "") if isinstance(v, dict) else v
            flat[k] = str(pv) if not isinstance(pv, (dict, list)) else ", ".join(str(i) for i in pv) if isinstance(pv, list) else ""
    else:
        for k, v in props_dict.items():
            if k not in ("class", "propertyValueMap", "propertiesAsStrings"):
                flat[k] = str(v) if not isinstance(v, (dict, list)) else ""
    return {k: v for k, v in flat.items() if v}


def _end_guid(end: dict) -> str:
    return (end or {}).get("guid") or ""


def _end_is_term(end: dict) -> Optional[bool]:
    """True/False if the end's own type info says GlossaryTerm/not; None if absent."""
    type_name = ((end or {}).get("type") or {}).get("typeName")
    if not type_name:
        return None
    return type_name == "GlossaryTerm"


def _fetch_semantic_assignments(ce, as_of_time: Optional[str] = None, identity: Optional[str] = None) -> tuple:
    """One bounded paged read of every SemanticAssignment relationship, normalized to
    ([{"elementGuid": ..., "termGuid": ...}, ...], capped). Direction resolved per module docstring.

    capped=True means every one of the _REL_PAGES pages came back full, so more assignments may exist than
    were read: the callers must show their answer as a lower bound ("at least N"), never as complete."""
    # Errors propagate: a failed read is not "nothing is assigned". The callers decide -- the
    # assigned-elements route answers 500 (the panel says the lookup failed); the schema tree drops its badges.
    key = _assign_cache_key(ce, identity, as_of_time)
    if key:
        with _ASSIGN_LOCK:
            hit = _ASSIGN_CACHE.get(key)
        if hit and time.time() - hit[0] < _ASSIGN_TTL:
            return list(hit[1]), hit[2]
    raw = []
    capped = True
    for page in range(_REL_PAGES):
        body = {"class": "ResultsRequestBody", "startFrom": page * _REL_PAGE, "pageSize": _REL_PAGE}
        if as_of_time:
            body["asOfTime"] = as_of_time   # point-in-time (the view's As-of slider)
        batch = ce.get_relationships(
            relationship_type="SemanticAssignment", start_from=page * _REL_PAGE,
            page_size=_REL_PAGE, output_format="JSON", body=body,
        )
        if not isinstance(batch, list) or not batch:     # empty page (or pyegeria's "none found" string): done
            capped = False
            break
        raw.extend(batch)
    if capped:
        logger.info(f"semantic_links: SemanticAssignment read stopped at {READ_LIMIT} (cap); answers are lower bounds")
    out = []
    for r in raw:
        if not isinstance(r, dict):
            continue
        end1, end2 = r.get("end1") or {}, r.get("end2") or {}
        g1, g2 = _end_guid(end1), _end_guid(end2)
        if not g1 or not g2:
            continue
        is1_term, is2_term = _end_is_term(end1), _end_is_term(end2)
        if is1_term is True or is2_term is False:
            element_guid, term_guid = g2, g1
        else:
            # Default per the type model: end1 = element, end2 = term.
            element_guid, term_guid = g1, g2
        out.append({"elementGuid": element_guid, "termGuid": term_guid})
    if key:
        with _ASSIGN_LOCK:
            _ASSIGN_CACHE[key] = (time.time(), out, capped)
            for k in [k for k, v in _ASSIGN_CACHE.items() if time.time() - v[0] >= _ASSIGN_TTL]:
                _ASSIGN_CACHE.pop(k, None)        # drop expired entries so old times/tokens do not pile up
    return list(out), capped


def _resolve_display(ce, guid: str, as_of_time: Optional[str] = None) -> dict:
    """{guid, displayName, qualifiedName, typeName} for one guid — cheap, depth 0."""
    try:
        body = {"class": "GetRequestBody", "graphQueryDepth": 0}
        if as_of_time:
            body["asOfTime"] = as_of_time
        raw = ce.get_element_by_guid(guid=guid, output_format="JSON", body=body)
        el = raw[0] if isinstance(raw, list) and raw else (raw if isinstance(raw, dict) else None)
        if not isinstance(el, dict):
            return {"guid": guid, "displayName": guid, "qualifiedName": "", "typeName": ""}
        hdr = el.get("elementHeader") or {}
        props = _flat_props(el.get("properties") or {})
        return {
            "guid": guid,
            "displayName": props.get("displayName") or props.get("name") or props.get("qualifiedName") or guid,
            "qualifiedName": props.get("qualifiedName") or "",
            "typeName": (hdr.get("type") or {}).get("typeName") or "",
        }
    except Exception:
        logger.debug("semantic_links: could not resolve %s", guid)
        return {"guid": guid, "displayName": guid, "qualifiedName": "", "typeName": ""}


def terms_for_element_guids(ce, element_guids, as_of_time: Optional[str] = None,
                            identity: Optional[str] = None) -> tuple:
    """(element_guid -> [{guid, displayName, qualifiedName, typeName}, ...] of assigned glossary terms, capped).
    One bounded relationship read plus one _resolve_display call per *distinct* term actually found (not per
    element). capped: see _fetch_semantic_assignments -- some terms may be missing from the map."""
    wanted = {g for g in (element_guids or []) if g}
    if not wanted:
        return {}, False
    all_links, capped = _fetch_semantic_assignments(ce, as_of_time, identity)
    links = [l for l in all_links if l["elementGuid"] in wanted]
    if not links:
        return {}, capped
    term_guids = sorted({l["termGuid"] for l in links})
    terms = {g: _resolve_display(ce, g, as_of_time) for g in term_guids}
    result: dict = {}
    for l in links:
        result.setdefault(l["elementGuid"], []).append(terms[l["termGuid"]])
    return result, capped


def elements_for_term_guid(ce, term_guid: str, as_of_time: Optional[str] = None,
                           identity: Optional[str] = None) -> tuple:
    """(Elements (physical or logical, whatever's assigned) for one glossary term, resolved to display info,
    capped) — the reverse direction of terms_for_element_guids. capped: the list may be incomplete."""
    if not term_guid:
        return [], False
    all_links, capped = _fetch_semantic_assignments(ce, as_of_time, identity)
    links = [l for l in all_links if l["termGuid"] == term_guid]
    seen = set()
    out = []
    for l in links:
        if l["elementGuid"] in seen:
            continue
        seen.add(l["elementGuid"])
        out.append(_resolve_display(ce, l["elementGuid"], as_of_time))
    return out, capped
