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

One bounded fetch per call (capped at _REL_CAP), not one call per element --
the same "commonly interesting, not exhaustive" tradeoff
insights_handler.py's _relationship_type_stats already makes for this app,
reused here rather than reimplemented.
"""
from typing import Optional

from loguru import logger

# Generous cap for a single relationship-type fetch. Not exhaustive on very
# large repositories, same tradeoff insights_handler.py's _DEFAULT_CAP makes
# — this feeds interactive badges/lookups, not a governance-audit total.
_REL_CAP = 2000


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


def _fetch_semantic_assignments(ce) -> list:
    """One bounded fetch of every SemanticAssignment relationship, normalized to
    [{"elementGuid": ..., "termGuid": ...}, ...]. Direction resolved per module
    docstring."""
    try:
        raw = ce.get_relationships(
            relationship_type="SemanticAssignment", start_from=0,
            page_size=_REL_CAP, output_format="JSON", body=None,
        )
    except Exception:
        logger.debug("semantic_links: SemanticAssignment fetch failed")
        return []
    out = []
    for r in (raw if isinstance(raw, list) else []):
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
    return out


def _resolve_display(ce, guid: str) -> dict:
    """{guid, displayName, qualifiedName, typeName} for one guid — cheap, depth 0."""
    try:
        body = {"class": "GetRequestBody", "graphQueryDepth": 0}
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


def terms_for_element_guids(ce, element_guids) -> dict:
    """element_guid -> [{guid, displayName, qualifiedName, typeName}, ...] of
    assigned glossary terms. One bounded relationship fetch plus one
    _resolve_display call per *distinct* term actually found (not per element)."""
    wanted = {g for g in (element_guids or []) if g}
    if not wanted:
        return {}
    links = [l for l in _fetch_semantic_assignments(ce) if l["elementGuid"] in wanted]
    if not links:
        return {}
    term_guids = sorted({l["termGuid"] for l in links})
    terms = {g: _resolve_display(ce, g) for g in term_guids}
    result: dict = {}
    for l in links:
        result.setdefault(l["elementGuid"], []).append(terms[l["termGuid"]])
    return result


def elements_for_term_guid(ce, term_guid: str) -> list:
    """Elements (physical or logical, whatever's assigned) for one glossary term,
    resolved to display info — the reverse direction of terms_for_element_guids."""
    if not term_guid:
        return []
    links = [l for l in _fetch_semantic_assignments(ce) if l["termGuid"] == term_guid]
    seen = set()
    out = []
    for l in links:
        if l["elementGuid"] in seen:
            continue
        seen.add(l["elementGuid"])
        out.append(_resolve_display(ce, l["elementGuid"]))
    return out
