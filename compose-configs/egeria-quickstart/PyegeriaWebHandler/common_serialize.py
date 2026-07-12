"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Shared serialization helpers for element headers.

Every Egeria metadata element has an `elementHeader` with the same shape
regardless of type (guid, type, status, versions). `AuthoredReferenceable`
(and its many subtypes — GlossaryTerm, Project, GovernanceDefinition, etc.)
also contributes three properties: authors, contentStatus,
userDefinedContentStatus. Handler-specific serializers previously hand-picked
which fields to expose, so these were silently dropped everywhere. This
module centralizes that extraction so every serializer can add it with one
line: `out.update(_authored_fields(el))`.
"""

from typing import Optional


def _authored_fields(el: dict) -> dict:
    """Header/version + AuthoredReferenceable metadata, present on virtually
    every element. Safe to call on any element — fields are simply absent
    (empty string/list) when the underlying type doesn't define them or the
    value was never set."""
    hdr = (el.get("elementHeader") or {}) if isinstance(el, dict) else {}
    props = (el.get("properties") or {}) if isinstance(el, dict) else {}
    versions = hdr.get("versions") or {}
    return {
        "authors":                   props.get("authors") or [],
        "contentStatus":             props.get("contentStatus") or "",
        "userDefinedContentStatus":  props.get("userDefinedContentStatus") or "",
        "createTime":                versions.get("createTime") or "",
        "updateTime":                versions.get("updateTime") or "",
        "createdBy":                 versions.get("createdBy") or "",
        "updatedBy":                 versions.get("updatedBy") or "",
        "maintainedBy":              versions.get("maintainedBy") or [],
    }


def _header_summary(el: dict) -> Optional[dict]:
    """Normalized header subset for the frontend's "Header" info popover —
    guid/type/status/version plus the same authorship/versions fields.
    Returns None for non-dict input so callers can drop it with `or None`."""
    if not isinstance(el, dict):
        return None
    hdr = el.get("elementHeader") or {}
    type_info = hdr.get("type") or {}
    versions = hdr.get("versions") or {}
    return {
        "guid":        hdr.get("guid", ""),
        "typeName":    type_info.get("typeName", ""),
        "status":      hdr.get("status", ""),
        "version":     versions.get("version"),
        "createdBy":   versions.get("createdBy") or "",
        "createTime":  versions.get("createTime") or "",
        "updatedBy":   versions.get("updatedBy") or "",
        "updateTime":  versions.get("updateTime") or "",
        "maintainedBy": versions.get("maintainedBy") or [],
    }


_RELATIONSHIP_SKIP_KEYS = {"elementHeader", "properties", "classifications", "class"}
_REL_ITEM_META_KEYS = {"relationshipHeader", "relationshipProperties", "relatedElement",
                        "relatedElementAtEnd1", "class"}


def _unwrap_relationship_item(item: dict) -> Optional[dict]:
    """Normalise one RelatedMetadataElementSummary-shaped dict (however it's
    nested — under `relatedElement`, or the element fields directly at the
    top level of `item`) into {guid, typeName, superTypeNames, displayName,
    qualifiedName, description, properties}. Returns None if it doesn't look
    like a related-element entry (no guid found)."""
    if not isinstance(item, dict):
        return None
    nested = item.get("relatedElement")
    if isinstance(nested, dict) and "elementHeader" in nested:
        elem = nested
    elif "elementHeader" in item:
        elem = {k: v for k, v in item.items() if k not in _REL_ITEM_META_KEYS}
    else:
        return None
    elem_hdr = elem.get("elementHeader") or {}
    elem_props = elem.get("properties") or {}
    guid = elem_hdr.get("guid") or ""
    if not guid:
        return None
    type_info = elem_hdr.get("type") or {}
    # Some related types (e.g. Annotation) have no displayName/name of their
    # own — fall back through summary/qualifiedName before the guid, so cards
    # don't just show a raw GUID (see 2026-07-08 fix in tech_catalog_handler).
    display_name = (
        elem_props.get("displayName") or elem_props.get("name") or
        elem_props.get("summary") or elem_props.get("qualifiedName") or guid
    )
    skip_extra = {"class", "displayName", "name", "description", "qualifiedName"}
    extra_props = {}
    for k, v in elem_props.items():
        if k in skip_extra:
            continue
        if isinstance(v, bool) or isinstance(v, (int, float)):
            extra_props[k] = v
        elif isinstance(v, str) and v.strip():
            extra_props[k] = v
    return {
        "guid":           guid,
        "typeName":       type_info.get("typeName", ""),
        "superTypeNames": type_info.get("superTypeNames") or [],
        "displayName":    display_name,
        "qualifiedName":  elem_props.get("qualifiedName") or "",
        "description":    elem_props.get("description") or "",
        "properties":     extra_props,
    }


def _generic_relationships(element: dict, skip: tuple = ()) -> dict:
    """Group every top-level relationship-shaped key on a graph-queried
    element into {keyName: [relatedElement, ...]}. A key qualifies if its
    value is a list of dicts (or a single dict) that look like
    RelatedMetadataElementSummary entries. Keys with no valid entries are
    omitted, so `bool(result)` tells you whether there's anything to show.

    This replaces handler-specific curated relationship-key lists (which
    silently drop any relationship Egeria returns under a key nobody
    hand-picked) with the same fully-generic extraction tech_catalog_handler
    already used for The Catalog's Asset relationships.

    `skip`: extra key names to omit — pass the keys a caller already surfaces
    via its own curated/derived logic, so this only fills in what's missing
    rather than duplicating what's already shown."""
    if not isinstance(element, dict):
        return {}
    skip_set = _RELATIONSHIP_SKIP_KEYS | set(skip)
    result = {}
    for key, val in element.items():
        if key in skip_set:
            continue
        if isinstance(val, list):
            candidates = val
        elif isinstance(val, dict):
            candidates = [val]
        else:
            continue
        items = []
        for entry in candidates:
            r = _unwrap_relationship_item(entry)
            if r:
                items.append(r)
        if items:
            result[key] = items
    return result
