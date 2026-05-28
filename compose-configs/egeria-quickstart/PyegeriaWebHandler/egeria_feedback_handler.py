"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Egeria native feedback — proxies likes and ratings on any Egeria metadata element
using the configured demo user identity (EGERIA_USER env var).

GET    /api/egeria-feedback/{guid}          → summary (counts, user state)
POST   /api/egeria-feedback/{guid}/like     → toggle like
POST   /api/egeria-feedback/{guid}/rating   → set/update rating
DELETE /api/egeria-feedback/{guid}/rating   → remove rating
"""

import os
from typing import Optional

from fastapi import APIRouter, HTTPException
from loguru import logger
from pydantic import BaseModel

router = APIRouter(tags=["egeria-feedback"])

# Integer value for each StarRating enum name
_STAR_MAP: dict[str, int] = {
    "ONE_STAR": 1, "TWO_STARS": 2, "THREE_STARS": 3,
    "FOUR_STARS": 4, "FIVE_STARS": 5, "NO_RECOMMENDATION": 0,
}


# ── pyegeria client ────────────────────────────────────────────────────────────

def _get_client():
    from pyegeria import ServerClient
    url      = os.environ.get("EGERIA_PLATFORM_URL",  "https://localhost:9443")
    server   = os.environ.get("EGERIA_VIEW_SERVER",   "qs-view-server")
    user_id  = os.environ.get("EGERIA_USER",          "erinoverview")
    user_pwd = os.environ.get("EGERIA_USER_PASSWORD", "secret")
    client = ServerClient(server_name=server, platform_url=url, user_id=user_id, user_pwd=user_pwd)
    client.create_egeria_bearer_token()
    return client


# ── response parsing helpers ───────────────────────────────────────────────────

def _elements(result) -> list[dict]:
    """Normalise various Egeria response shapes into a list of element dicts."""
    if not result or isinstance(result, str):
        return []
    if isinstance(result, list):
        return result
    if isinstance(result, dict):
        if "elements" in result:
            elems = result["elements"]
            return elems if isinstance(elems, list) else []
        if result.get("elementHeader"):
            return [result]
    return []


def _created_by(element: dict) -> str:
    hdr = element.get("elementHeader") or {}
    versions = hdr.get("versions") or {}
    return versions.get("createdBy", "") or hdr.get("createdBy", "")


def _star_int(element: dict) -> Optional[int]:
    props = element.get("properties") or {}
    star = props.get("starRating")
    if star is None:
        return None
    if isinstance(star, int):
        return star
    if isinstance(star, str):
        return _STAR_MAP.get(star)
    return None


# ── aggregate helpers ──────────────────────────────────────────────────────────

def _likes_info(client, guid: str) -> tuple[int, bool]:
    try:
        result = client.get_attached_likes(guid)
        elems = _elements(result)
        my_like = any(_created_by(e) == client.user_id for e in elems)
        return len(elems), my_like
    except Exception as exc:
        logger.debug(f"get_attached_likes({guid}): {exc}")
        return 0, False


def _ratings_info(client, guid: str) -> tuple[Optional[float], int, Optional[int]]:
    """Returns (avg_rating, count, my_rating_int)."""
    try:
        result = client.get_attached_ratings(guid)
        elems = _elements(result)
        if not elems:
            return None, 0, None
        stars = [s for e in elems if (s := _star_int(e)) is not None and s > 0]
        my_rating = next(
            (_star_int(e) for e in elems if _created_by(e) == client.user_id),
            None,
        )
        avg = round(sum(stars) / len(stars), 1) if stars else None
        return avg, len(elems), my_rating
    except Exception as exc:
        logger.debug(f"get_attached_ratings({guid}): {exc}")
        return None, 0, None


# ── routes ─────────────────────────────────────────────────────────────────────

@router.get("/api/egeria-feedback/{guid}", summary="Get likes and ratings for an element")
def get_element_feedback(guid: str):
    client = _get_client()
    likes_count, my_like = _likes_info(client, guid)
    avg_rating, ratings_count, my_rating = _ratings_info(client, guid)
    return {
        "likes_count":   likes_count,
        "my_like":       my_like,
        "avg_rating":    avg_rating,
        "ratings_count": ratings_count,
        "my_rating":     my_rating,
    }


@router.post("/api/egeria-feedback/{guid}/like", summary="Toggle like on an element")
def toggle_like(guid: str):
    client = _get_client()
    _, my_like = _likes_info(client, guid)
    try:
        if my_like:
            client.remove_like_from_element(guid)
        else:
            client.add_like_to_element(guid)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    likes_count, my_like = _likes_info(client, guid)
    return {"likes_count": likes_count, "my_like": my_like}


class RatingRequest(BaseModel):
    star_rating: int
    review: Optional[str] = None


@router.post("/api/egeria-feedback/{guid}/rating", summary="Set or update a star rating")
def set_rating(guid: str, req: RatingRequest):
    if not 1 <= req.star_rating <= 5:
        raise HTTPException(status_code=400, detail="star_rating must be 1-5")
    client = _get_client()
    # Egeria: one rating per user — remove then add to update
    _, _, my_rating = _ratings_info(client, guid)
    if my_rating is not None:
        try:
            client.remove_rating_from_element(guid)
        except Exception:
            pass
    body = {
        "class": "NewAttachmentRequestBody",
        "properties": {"class": "RatingProperties", "starRating": req.star_rating},
    }
    if req.review:
        body["properties"]["review"] = req.review
    try:
        client.add_rating_to_element(guid, is_public=True, body=body)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    avg_rating, ratings_count, my_rating = _ratings_info(client, guid)
    return {"avg_rating": avg_rating, "ratings_count": ratings_count, "my_rating": my_rating}


@router.delete("/api/egeria-feedback/{guid}/rating", summary="Remove a star rating")
def remove_rating(guid: str):
    client = _get_client()
    try:
        client.remove_rating_from_element(guid)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    avg_rating, ratings_count, my_rating = _ratings_info(client, guid)
    return {"avg_rating": avg_rating, "ratings_count": ratings_count, "my_rating": my_rating}
