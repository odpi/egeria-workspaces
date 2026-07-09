"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Note Log Explorer — FastAPI router.

A NoteLog is an ordered list of related notes attached to a subject element
(a Person, Community, Asset, etc.). Each note (a NoteEntry / ActivityEntry /
Notification) carries a title, body text, and authorship/timestamps.

Endpoints:
  GET /api/notelogs          → list all note logs (summary)
  GET /api/notelogs/{guid}   → full detail for one note log (subjects + entries)

Performance notes (qs-view-server, pyegeria 6.0.14.6):
  - `find_note_logs('*')` at the default graph depth still expands every log's
    notes inline (~30s here, because two system logs hold ~1000 / ~500 notes),
    and `graph_query_depth` is not bounded by `page_size`. So the LIST uses
    graph_query_depth=0 (≈0.3s) — names only, no entries.
  - `get_notes_for_note_log(guid)` was fixed in 6.0.14.6: with default kwargs it
    now returns the *notes* (not the log) and honours `page_size`, so DETAIL
    fetches entries directly and cheaply even for the giant logs
    (page_size=100 ≈ 7s on the worst log; small logs are sub-second). Do NOT
    pass `metadata_element_type_name="NoteLog"` — that now returns zero notes.
  - The subject the log is *about* is not present at depth 0 in `noteLogSubjects`,
    but every log carries an `Anchors` classification in its elementHeader
    (anchorGUID + anchorTypeName) — a cheap, reliable cross-link target. DETAIL
    additionally makes a best-effort depth-1 narrowed find (short timeout) to
    enrich the subject with its display name; on timeout (the giant logs) it
    falls back to the anchor.
"""

import os
from egeria_auth import apply_token
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

from common_serialize import _authored_fields, _header_summary

router = APIRouter(tags=["notelogs"])

MAX_ENTRIES = 100      # most recent notes returned per log (bounds giant-log latency)
SUBJECT_TIMEOUT = 5    # seconds for best-effort subject-name enrichment (anchor is the fallback)
_EXECUTOR = ThreadPoolExecutor(max_workers=4)


def _get_manager(url=None, server=None, user_id=None, user_pwd=None):
    from pyegeria import CollectionManager
    import pyegeria
    pyegeria.enable_ssl_check = False
    pyegeria.disable_ssl_warnings = True
    url      = url      or os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = server   or os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = user_id  or os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = user_pwd or os.environ.get("EGERIA_USER_PASSWORD", "secret")
    mgr = CollectionManager(view_server=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    apply_token(mgr)
    return mgr


def _is_template(element: dict) -> bool:
    for val in (element.get("elementHeader") or {}).values():
        if isinstance(val, dict) and val.get("class") == "ElementClassification":
            name = val.get("classificationName") or (val.get("type") or {}).get("typeName") or ""
            if name == "Template":
                return True
    return False


def _props(element: dict) -> dict:
    return element.get("properties") or {}


def _header(element: dict) -> dict:
    return element.get("elementHeader") or {}


def _type_name(element: dict) -> str:
    return (_header(element).get("type") or {}).get("typeName", "") or ""


def _super_type_names(element: dict) -> list:
    return (_header(element).get("type") or {}).get("superTypeNames") or []


def _display_name(props: dict, guid: str = "") -> str:
    name = props.get("displayName") or props.get("name") or props.get("title")
    if name:
        return name
    # Note logs are often unnamed; derive a friendly label from the last
    # "::" segment of the qualifiedName (e.g. "Community::Jacquard::GovernanceSIG_noteLog").
    qn = props.get("qualifiedName") or ""
    if qn:
        tail = qn.split("::")[-1].strip()
        if tail and tail != qn:
            return tail
        return qn
    return guid or ""


def _subject_label_from_log(props: dict) -> str:
    """Best-effort label for an anchor subject derived from the note log's own
    qualifiedName tail, e.g. "Community::Jacquard::GovernanceSIG_noteLog" →
    "GovernanceSIG". Only meaningful when the tail names the subject (the common
    case for the giant community logs we can't enrich at depth 1)."""
    qn = props.get("qualifiedName") or ""
    if not qn:
        return ""
    tail = qn.split("::")[-1].strip()
    for suffix in ("_noteLog", "_notelog", "noteLog", "NoteLog"):
        if tail.endswith(suffix) and len(tail) > len(suffix):
            return tail[: -len(suffix)].rstrip("_")
    return ""


def _anchor_subject(notelog_element: dict) -> Optional[dict]:
    """The element a note log is *about*, read cheaply from its Anchors
    classification (present at depth 0). Cross-linkable by guid + typeName."""
    anchor = _header(notelog_element).get("anchor") or {}
    cp = anchor.get("classificationProperties") or {}
    g = cp.get("anchorGUID") or ""
    if not g:
        return None
    return {
        "guid":           g,
        "displayName":    _subject_label_from_log(_props(notelog_element)),
        "qualifiedName":  "",
        "description":    "",
        "typeName":       cp.get("anchorTypeName") or "",
        "superTypeNames": [],
    }


def _serialize_subject(rel: dict) -> Optional[dict]:
    """One depth-1 noteLogSubjects entry → the element the log is *about*."""
    re = rel.get("relatedElement") or {}
    rh = re.get("elementHeader") or {}
    rp = re.get("properties") or {}
    rtype = rh.get("type") or {}
    g = rh.get("guid", "")
    if not g:
        return None
    return {
        "guid":           g,
        "displayName":    rp.get("displayName") or rp.get("fullName") or rp.get("name") or rp.get("qualifiedName") or "",
        "qualifiedName":  rp.get("qualifiedName") or "",
        "description":    rp.get("description") or "",
        "typeName":       rtype.get("typeName") or "",
        "superTypeNames": rtype.get("superTypeNames") or [],
    }


def _serialize_note(element: dict) -> Optional[dict]:
    """One note element from get_notes_for_note_log → a single note. Unlike the
    depth-1 noteLogEntries shape, the note element is top-level (its
    elementHeader/properties are not wrapped in a relatedElement)."""
    rh = element.get("elementHeader") or {}
    rp = element.get("properties") or {}
    rtype = rh.get("type") or {}
    versions = rh.get("versions") or {}
    g = rh.get("guid", "")
    if not g:
        return None
    return {
        "guid":       g,
        "title":      rp.get("title") or rp.get("displayName") or rp.get("name") or "",
        "text":       rp.get("text") or rp.get("description") or "",
        "situation":  rp.get("situation") or "",
        "typeName":   rtype.get("typeName") or "",
        "createdBy":  versions.get("createdBy") or "",
        "updatedBy":  versions.get("updatedBy") or "",
        "createTime": versions.get("createTime") or "",
        "updateTime": versions.get("updateTime") or "",
        **_authored_fields(element),
    }


def _serialize_notelog_summary(element: dict) -> dict:
    props  = _props(element)
    header = _header(element)
    guid   = header.get("guid", "")
    return {
        "guid":           guid,
        "displayName":    _display_name(props, guid),
        "qualifiedName":  props.get("qualifiedName") or "",
        "description":    props.get("description") or "",
        "status":         header.get("status") or "",
        "typeName":       _type_name(element) or "NoteLog",
        "superTypeNames": _super_type_names(element),
        "_header":        _header_summary(element),
        **_authored_fields(element),
    }


def _find_note_logs(mgr, search_string: str, start_from: int, page_size: int, depth: int) -> list:
    raw = mgr.find_note_logs(
        search_string=search_string,
        starts_with=False,
        output_format="JSON",
        start_from=start_from,
        page_size=page_size,
        graph_query_depth=depth,
    )
    return raw if isinstance(raw, list) else []


def _enrich_subjects_in_thread(creds: dict, search_string: str, guid: str) -> Optional[list]:
    """Best-effort: a narrowed depth-1 find to read the log's noteLogSubjects
    with display names. pyegeria drives asyncio via the calling thread's event
    loop, so give this worker its own loop and a freshly-built manager."""
    import asyncio
    asyncio.set_event_loop(asyncio.new_event_loop())
    mgr = _get_manager(**creds)
    matches = _find_note_logs(mgr, search_string, 0, 25, 1)
    rich = next((e for e in matches if isinstance(e, dict) and _header(e).get("guid") == guid), None)
    if rich is None:
        return None
    subjects = [s for s in (_serialize_subject(r) for r in (rich.get("noteLogSubjects") or [])) if s]
    mermaid = rich.get("mermaidGraph") or ""
    return [subjects, mermaid]


@router.get("/api/notelogs", summary="List all note logs")
def list_notelogs(
    start_from: int = Query(0,   ge=0),
    page_size:  int = Query(200, ge=1, le=1000),
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
    include_templates: bool = Query(False, description="When False, elements with the Template classification are excluded"),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create manager for note log list")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    try:
        # depth=0: names only — fast even when logs hold thousands of notes.
        raw = _find_note_logs(mgr, "*", start_from, page_size, depth=0)
    except Exception as exc:
        logger.exception("find_note_logs failed")
        raise HTTPException(status_code=500, detail=f"Note log retrieval failed: {exc}")

    if not include_templates:
        raw = [e for e in raw if isinstance(e, dict) and not _is_template(e)]

    notelogs = [_serialize_notelog_summary(e) for e in raw if isinstance(e, dict)]
    notelogs.sort(key=lambda x: (x.get("displayName") or x.get("qualifiedName") or "").lower())
    return JSONResponse({"notelogs": notelogs, "total": len(notelogs)})


@router.get("/api/notelogs/{guid}", summary="Get full detail for a note log")
def get_notelog(
    guid: str,
    url:      Optional[str] = Query(None),
    server:   Optional[str] = Query(None),
    user_id:  Optional[str] = Query(None),
    user_pwd: Optional[str] = Query(None),
):
    try:
        mgr = _get_manager(url, server, user_id, user_pwd)
    except Exception as exc:
        logger.exception("Failed to create manager for note log detail")
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}")

    # Step 1: locate the log cheaply (depth 0) for its header + qualifiedName +
    # Anchors classification (which names the subject the log is about).
    try:
        index = _find_note_logs(mgr, "*", 0, 1000, depth=0)
    except Exception as exc:
        logger.exception(f"note log index lookup failed for {guid}")
        raise HTTPException(status_code=500, detail=f"Note log lookup failed: {exc}")

    header_el = next((e for e in index if isinstance(e, dict) and _header(e).get("guid") == guid), None)
    if not header_el:
        raise HTTPException(status_code=404, detail=f"Note log {guid!r} not found")

    out = _serialize_notelog_summary(header_el)
    qn = _props(header_el).get("qualifiedName") or ""

    # Step 2: subjects. Best-effort depth-1 enrichment for display names; fall
    # back to the cheap Anchors classification (always available) on timeout.
    subjects = None
    mermaid = ""
    if qn:
        creds = {"url": url, "server": server, "user_id": user_id, "user_pwd": user_pwd}
        future = _EXECUTOR.submit(_enrich_subjects_in_thread, creds, qn, guid)
        try:
            result = future.result(timeout=SUBJECT_TIMEOUT)
            if result:
                subjects, mermaid = result[0], result[1]
        except FutureTimeout:
            logger.info(f"note log {guid} ({qn}) subject enrichment timed out; using anchor")
        except Exception:
            logger.exception(f"note log subject enrichment failed for {guid} ({qn})")
    if not subjects:
        anchor = _anchor_subject(header_el)
        subjects = [anchor] if anchor else []
    out["subjects"] = subjects

    # Step 3: entries — get_notes_for_note_log returns the notes directly and
    # honours page_size (fixed in 6.0.14.6), so this is reliable for all logs.
    entries = []
    try:
        raw_notes = mgr.get_notes_for_note_log(guid, output_format="JSON", page_size=MAX_ENTRIES)
        notes = raw_notes if isinstance(raw_notes, list) else []
        entries = [e for e in (_serialize_note(n) for n in notes if isinstance(n, dict)) if e]
        entries.sort(key=lambda e: e.get("createTime") or "", reverse=True)
    except Exception:
        logger.exception(f"get_notes_for_note_log failed for {guid}")

    out["entries"] = entries
    out["entryCount"] = len(entries)
    out["entriesTruncated"] = len(entries) >= MAX_ENTRIES
    if mermaid and isinstance(mermaid, str) and not mermaid.lower().startswith("no "):
        out["mermaidGraph"] = mermaid
    return JSONResponse(out)
