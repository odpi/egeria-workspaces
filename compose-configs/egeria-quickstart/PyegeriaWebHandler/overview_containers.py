"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Egeria Overview — Container model (NEXT-10, phase P2).

A **Container** is a named, ordered list of **placements** — each placement
references a tile in `overview_specs.SPECS` (a ReportSpec/FormatSet) or another
Container by name, plus presentation hints (`span`, `emphasis`). Containers can
nest. The "Overview" dashboard is one top-level Container.

Per the design doc's open-decision resolution (2026-07-26, OVERVIEW_REPORTING_MODEL.md
§10 #4): storage stays **pyegeria-local** (a Pydantic model + Python definitions,
mirroring how `overview_specs.py` defines FormatSets today) — this is deliberately
*not* a new Egeria element type. That step is P3 (backlogged). Likewise, Dr.Egeria
markdown commands to *author* containers (proposed in §4.3) are a further increment
on top of this model, not yet built — this module only ships the Container/placement
model + perspective-as-filter, the part needed to prove the layer and to let the
Overview dashboard be expressed as one.

Perspective as a lens (§6): a perspective is not a separate hardcoded selection
list — it's a **filtered, reordered view over a Container's placements**, computed
from each placed tile's own `question_spec.perspectives` (the same source
`overview_specs.perspectives_for()` already exposes). `view_for_perspective()` is
that computation; `overview_specs.PERSP_KPIS` remains as the frontend-facing
source of truth for *ordering* until the SPA renders directly from containers
(P1/P2 frontend work) — `test_overview_specs.py` guards the two stay in sync.
"""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field

import overview_specs as specs


Span = Literal["1", "2", "full"]
Emphasis = Literal["kpi", "panel"]


class Placement(BaseModel):
    """One entry in a Container's ordered layout.

    ``ref`` is a tile key (into `overview_specs.SPECS`) or another Container's
    ``name`` — which one it is is resolved by `resolve()` against a registry of
    known containers, not encoded on the placement itself (a Container doesn't
    need to know whether a name it references is a leaf tile or a sub-container).
    """
    ref: str
    span: Span = "1"
    emphasis: Emphasis = "kpi"


class Container(BaseModel):
    """A named, ordered, nestable placement list."""
    name: str
    heading: str
    description: str = ""
    placements: List[Placement] = Field(default_factory=list)


def _placement(ref: str, emphasis: Emphasis = "kpi") -> Placement:
    return Placement(ref=ref, emphasis=emphasis)


# ── The Overview dashboard, expressed as a Container ────────────────────────
# Placement order matches overview_specs.TILE_ORDER (the current dashboard's KPI
# band order) — test_overview_specs.py checks this doesn't silently drift.
OVERVIEW_CONTAINER = Container(
    name="overview-dashboard",
    heading="Egeria Overview",
    description="The system-default Overview dashboard — one Container of the "
                 "P0 KPI tiles, in their current display order.",
    placements=[_placement(key) for key in specs.TILE_ORDER],
)

# Registry of known top-level containers (by name). A Placement.ref that doesn't
# resolve against overview_specs.SPECS is looked up here — the mechanism nested/
# reused sub-containers (§4.3 "People panel", "Governance summary", ...) will use
# once those are authored; only the one dashboard container exists today.
CONTAINERS = {OVERVIEW_CONTAINER.name: OVERVIEW_CONTAINER}


class ResolvedPlacement(BaseModel):
    """A Placement joined with its target tile's display facts — what a renderer
    actually needs, without having to know FormatSet's internal shape."""
    ref: str
    span: Span
    emphasis: Emphasis
    kind: Literal["tile", "container"]
    heading: str
    icon: Optional[str] = None
    color: Optional[str] = None
    value_field: Optional[str] = None
    endpoint: Optional[str] = None
    detail_spec: Optional[str] = None
    series: Optional[str] = None
    unit: Optional[str] = None
    provenance: Optional[str] = None


def _resolve_placement(p: Placement) -> ResolvedPlacement:
    fs = specs.SPECS.get(p.ref)
    if fs is not None:
        ann = fs.annotations or {}
        attr = fs.formats[0].attributes[0] if fs.formats and fs.formats[0].attributes else None
        return ResolvedPlacement(
            ref=p.ref, span=p.span, emphasis=p.emphasis, kind="tile",
            heading=fs.heading,
            icon=(ann.get("icon") or [None])[0],
            color=(ann.get("color") or [None])[0],
            value_field=getattr(attr, "key", None),
            endpoint=(ann.get("endpoint") or [None])[0],
            detail_spec=getattr(attr, "detail_spec", None),
            series=(ann.get("series") or [None])[0],
            unit=(ann.get("unit") or [None])[0],
            provenance=(ann.get("provenance") or [None])[0],
        )
    sub = CONTAINERS.get(p.ref)
    if sub is not None:
        return ResolvedPlacement(ref=p.ref, span=p.span, emphasis=p.emphasis,
                                  kind="container", heading=sub.heading)
    raise KeyError(f"Placement ref {p.ref!r} matches neither a tile in "
                    f"overview_specs.SPECS nor a Container in CONTAINERS")


def resolve(container: Container) -> List[ResolvedPlacement]:
    """Every placement in ``container``, joined with its target's display facts,
    in declared order."""
    return [_resolve_placement(p) for p in container.placements]


def view_for_perspective(container: Container, perspective: str) -> List[ResolvedPlacement]:
    """Perspective as a filtered, reordered view over a Container (§6): keep only
    placements whose target tile lists ``perspective`` in its own
    `question_spec.perspectives`, ordered per `overview_specs.PERSP_KPIS[perspective]`
    where that ordering exists (frontend-compatible order), falling back to
    declaration order for anything PERSP_KPIS doesn't rank (e.g. sub-containers).
    """
    resolved = resolve(container)
    order = specs.PERSP_KPIS.get(perspective, [])
    rank = {ref: i for i, ref in enumerate(order)}

    def included(rp: ResolvedPlacement) -> bool:
        if rp.kind == "container":
            return True  # sub-containers aren't perspective-filtered themselves
        return perspective in specs.perspectives_for(rp.ref)

    kept = [rp for rp in resolved if included(rp)]
    kept.sort(key=lambda rp: rank.get(rp.ref, len(order) + resolved.index(rp)))
    return kept


def container_payload(container: Container, perspective: Optional[str] = None) -> dict:
    """JSON-ready payload for a container, optionally filtered to a perspective."""
    placements = (view_for_perspective(container, perspective) if perspective
                  else resolve(container))
    return {
        "name": container.name,
        "heading": container.heading,
        "description": container.description,
        "perspective": perspective,
        "placements": [p.dict() for p in placements],
    }
