#!/usr/bin/env python3
"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

P1 of the Portal boundary view: capture REAL-SHAPE fixtures for Solution Boundaries, READ-ONLY, from the live quickstart platform.

MEMBERS are read from collectionMembers[].relatedElement and, below it, nestedElements ONLY (never sideLinks or memberOfCollections, which lead UP
to a parent), so an inner boundary that merely has a parent is not counted as nested.

WHAT IT CALLS (find and get requests only; the five names in ALLOWED_CALLS are the whole list, and a call to any other name stops the script):
  SolutionArchitect._async_find_solution_boundaries          (a) a boundary find
  SolutionArchitect._async_get_solution_boundary_by_guid     (b) a boundary by GUID that has members, including a NESTED boundary
  CollectionManager._async_find_collections                  (c) metadata_element_type='DesignModelBoundary'; it also returns Solution Boundaries
  SolutionArchitect._async_find_solution_blueprints          (d) the blueprints to look through,
  SolutionArchitect._async_get_solution_blueprint_by_guid        and one blueprint whose memberOfCollections names a boundary

It never changes anything on the platform. It makes no other request, shells out to nothing, and reads no file except this one's neighbours.

WHAT IT WRITES: four JSON files under tests/fixtures/, named like the existing captures:
  <what>_real_shape_<YYYY_MM_DD>_<platform container>-<id>.json
Each has a `_note` that says where it came from, then the raw elements UNMODIFIED, except that any token, password, secret, cookie or authorization
key, and any JWT-looking string, is dropped (counted in the note). GUIDs and names stay. Nothing is written unless ALL four are found; the files are
opened for exclusive creation, so an existing fixture is never replaced.

STOPS (writes nothing, prints what it saw, exit code 3 or 4):
  3  no boundary on the platform has a nested boundary among its members. Do not make one: the Coordinator arranges data separately.
  4  no blueprint has a boundary in memberOfCollections.

NOT RUN YET: the Architect reads this first, and the run needs Dan's word. Run it inside the portal's PyegeriaWebHandler environment, the one that has
pyegeria and egeria_auth and the EGERIA_PLATFORM_URL, EGERIA_VIEW_SERVER and EGERIA_USER settings (the password comes from egeria_auth.service_password()
and is never printed), for example:
  python tests/capture_boundary_fixtures.py --dry-run
  python tests/capture_boundary_fixtures.py --container egeria-quickstart-platform --container-id c461d5bfce7f
"""
import argparse
import asyncio
import datetime
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"

# The whole list of platform requests this script may make. Every name is a find or a get; anything else stops the script.
ALLOWED_CALLS = (
    "_async_find_solution_boundaries",
    "_async_get_solution_boundary_by_guid",
    "_async_find_collections",
    "_async_find_solution_blueprints",
    "_async_get_solution_blueprint_by_guid",
)
SECRET_KEY = re.compile(r"token|passw|secret|authoriz|cookie|bearer|credential|api[-_]?key", re.I)
JWT_LIKE = re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]*")
MAX_KEPT = 20            # elements kept in a find fixture (the first ones, unmodified), plus the first of every other type
MAX_DETAIL_CALLS = 60    # most boundaries (and, separately, blueprints) looked at one by one
EXIT_NO_NESTING, EXIT_NO_BLUEPRINT = 3, 4


class ReadOnlyCalls:
    """Wraps a pyegeria client so that only the names in ALLOWED_CALLS can be called, and keeps a log of the calls (name and arguments; no secrets)."""

    def __init__(self, client, log: list):
        self._client, self._log = client, log

    async def call(self, name: str, *args, **kwargs):
        if name not in ALLOWED_CALLS or not re.match(r"^_async_(find|get)_", name):
            raise SystemExit(f"refusing to call {name!r}: this script only makes the find and get requests in ALLOWED_CALLS")
        self._log.append(f"{type(self._client).__name__}.{name}({', '.join([repr(a) for a in args] + [f'{k}={v!r}' for k, v in kwargs.items()])})")
        return await getattr(self._client, name)(*args, **kwargs)


def walk(obj):
    """Every dict inside `obj`, itself included."""
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)


def header(d: dict) -> dict:
    h = d.get("elementHeader")
    return h if isinstance(h, dict) else {}


def type_name(d: dict) -> str:
    return (header(d).get("type") or {}).get("typeName", "") or ""


def guid_of(d: dict) -> str:
    return header(d).get("guid", "") or ""


def element_list(result) -> list:
    """A find answers a list of elements; accept a dict that wraps one, and answer [] for anything else (a text answer, None)."""
    if isinstance(result, list):
        return [x for x in result if isinstance(x, dict)]
    if isinstance(result, dict):
        for k in ("elements", "list", "searchResults"):
            if isinstance(result.get(k), list):
                return [x for x in result[k] if isinstance(x, dict)]
    return []


MAX_TREE_DEPTH = 50      # a safety stop for the member walk; the guids on the current path are never followed again


def members_below(detail: dict) -> list:
    """The members of a boundary as (guid, type name, depth, parent guid), depth 1 = a direct member. The walk follows ONLY
    `collectionMembers[].relatedElement` and, below it, `nestedElements` (the same shape, recursively), as pyegeria's
    solution_boundary_member_hierarchy does (RelatedMetadataHierarchySummary, odpi/egeria #9465). It never reads `sideLinks` or
    `memberOfCollections`: those lead UP to a parent, and counting a parent as a nested member would make an inner boundary look nested."""
    out: list = []
    root = guid_of(detail)

    def walk(items, depth, path, parent):
        for item in items if isinstance(items, list) else []:
            related = item.get("relatedElement") if isinstance(item, dict) else None
            if not isinstance(related, dict):
                continue
            guid = guid_of(related)
            if guid and guid in path:
                continue                                   # already above: a cycle, not followed again
            out.append((guid, type_name(related), depth, parent))
            if depth < MAX_TREE_DEPTH:
                walk(item.get("nestedElements"), depth + 1, path | {guid}, guid)

    walk(detail.get("collectionMembers"), 1, {root} if root else set(), root)
    return out


def nested_boundaries(detail: dict) -> dict:
    """GUID -> depth of every Solution Boundary that is a MEMBER (at any depth) of this boundary, from collectionMembers / nestedElements only."""
    found: dict = {}
    for guid, tname, depth, _ in members_below(detail):
        if tname == "SolutionBoundary" and guid and guid not in found:
            found[guid] = depth
    return found


def other_elements(detail: dict) -> set:
    """GUIDs of every member (any type, any depth) of this boundary, from collectionMembers / nestedElements only."""
    return {guid for guid, _, _, _ in members_below(detail) if guid}


def member_of_boundaries(detail: dict) -> list:
    """The (guid, name) of every element in `memberOfCollections[].relatedElement` that is a Solution Boundary."""
    out = []
    for d in walk(detail):
        for m in (d.get("memberOfCollections") or []) if isinstance(d.get("memberOfCollections"), list) else []:
            rel = (m or {}).get("relatedElement") if isinstance(m, dict) else None
            if isinstance(rel, dict) and type_name(rel) == "SolutionBoundary":
                out.append((guid_of(rel), (rel.get("properties") or {}).get("displayName", "")))
    return out


def has_member_of_collections(detail: dict) -> bool:
    return any(isinstance(d.get("memberOfCollections"), list) and d["memberOfCollections"] for d in walk(detail))


def scrub(obj, counter: dict):
    """A copy of `obj` without secret-looking keys or JWT-looking strings (counted in `counter`)."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if SECRET_KEY.search(str(k)):
                counter["keys"] = counter.get("keys", 0) + 1
                continue
            out[k] = scrub(v, counter)
        return out
    if isinstance(obj, list):
        return [scrub(v, counter) for v in obj]
    if isinstance(obj, str) and JWT_LIKE.search(obj):
        counter["strings"] = counter.get("strings", 0) + 1
        return JWT_LIKE.sub("<scrubbed>", obj)
    return obj


def assert_clean(text: str, what: str) -> None:
    if JWT_LIKE.search(text) or re.search(r'"[^"]*(?:token|passw|secret|authoriz|cookie|bearer)[^"]*"\s*:', text, re.I):
        raise SystemExit(f"{what}: a secret-looking key or string is still present after scrubbing; nothing was written")


def keep_first(elements: list, limit: int = MAX_KEPT) -> list:
    """The first `limit` elements, plus the first of every type not yet kept, all unmodified, in the order found."""
    kept, seen_types = elements[:limit], {type_name(e) for e in elements[:limit]}
    for e in elements[limit:]:
        if type_name(e) not in seen_types:
            kept.append(e)
            seen_types.add(type_name(e))
    return kept


def pyegeria_version() -> str:
    try:
        from importlib.metadata import version
        return version("pyegeria")
    except Exception:  # noqa: BLE001 -- a note only
        return "unknown"


async def make_clients():
    """The way the portal's handler builds a client (solution_architect_handler._get_manager), with the ASYNC token step that CLAUDE.md requires inside a running
    loop: the service user, `await async_apply_token`."""
    from egeria_auth import async_apply_token, service_password
    from pyegeria import CollectionManager, SolutionArchitect
    url = os.environ.get("EGERIA_PLATFORM_URL", "https://localhost:9443")
    server = os.environ.get("EGERIA_VIEW_SERVER", "qs-view-server")
    user = os.environ.get("EGERIA_USER", "erinoverview")
    pwd = service_password()
    clients = []
    for cls in (SolutionArchitect, CollectionManager):
        c = cls(view_server=server, platform_url=url, user_id=user, user_pwd=pwd)
        await async_apply_token(c)
        clients.append(c)
    return clients


async def capture(args, sa, cm, log: list) -> dict:
    sa, cm = ReadOnlyCalls(sa, log), ReadOnlyCalls(cm, log)
    report = {"seen": {}}

    # (a) the boundary find
    boundaries = element_list(await sa.call("_async_find_solution_boundaries", "*", page_size=500, graph_query_depth=1))
    report["seen"]["boundaries"] = len(boundaries)
    print(f"boundaries found: {len(boundaries)}")

    # (b) one by one: the boundary with the most members that has a nested boundary among them
    best = None
    for b in boundaries[:MAX_DETAIL_CALLS]:
        guid = guid_of(b)
        if not guid:
            continue
        detail = await sa.call("_async_get_solution_boundary_by_guid", guid, graph_query_depth=args.depth)
        if isinstance(detail, list) and detail:
            detail = detail[0]
        if not isinstance(detail, dict):
            continue
        nested, members = nested_boundaries(detail), other_elements(detail)
        name = (detail.get("properties") or {}).get("displayName", "")
        print(f"  boundary {guid} {name!r}: {len(members)} members, {len(nested)} nested boundaries {dict(sorted(nested.items()))}")
        if nested and (best is None or (len(nested), len(members)) > (len(best["nested"]), len(best["members"]))):
            best = {"guid": guid, "name": name, "detail": detail, "nested": nested, "members": members}
    report["seen"]["boundaries_looked_at"] = min(len(boundaries), MAX_DETAIL_CALLS)
    if best is None:
        report["stop"] = EXIT_NO_NESTING
        return report
    report["best"] = {k: best[k] for k in ("guid", "name")}

    # (c) the Design Model Boundary find (a solution boundary IS a design model boundary, so it returns both)
    dmb = element_list(await cm.call("_async_find_collections", "*", metadata_element_type="DesignModelBoundary", page_size=500, graph_query_depth=1))
    types = {}
    for e in dmb:
        types[type_name(e)] = types.get(type_name(e), 0) + 1
    report["seen"]["dmb_find_types"] = types
    print(f"design model boundary find: {len(dmb)} elements, types {types}")
    if not types.get("SolutionBoundary"):
        print("  WARNING: the find returned no SolutionBoundary; the fixture is saved, but it cannot show the exclusion by type name")

    # (d) a blueprint with memberOfCollections, preferably one in the boundary chosen for (b)
    blueprints = element_list(await sa.call("_async_find_solution_blueprints", "*", page_size=500, graph_query_depth=1))
    report["seen"]["blueprints"] = len(blueprints)
    chosen = None
    for bp in blueprints[:MAX_DETAIL_CALLS]:
        guid = guid_of(bp)
        if not guid:
            continue
        detail = await sa.call("_async_get_solution_blueprint_by_guid", guid, graph_query_depth=3)
        if isinstance(detail, list) and detail:
            detail = detail[0]
        if not isinstance(detail, dict) or not has_member_of_collections(detail):
            continue
        in_boundaries = member_of_boundaries(detail)
        score = (best["guid"] in [g for g, _ in in_boundaries], bool(in_boundaries))
        print(f"  blueprint {guid} {(detail.get('properties') or {}).get('displayName', '')!r}: memberOfCollections present, boundaries {[n for _, n in in_boundaries]}")
        if chosen is None or score > chosen["score"]:
            chosen = {"guid": guid, "detail": detail, "score": score, "boundaries": in_boundaries}
    report["seen"]["blueprints_looked_at"] = min(len(blueprints), MAX_DETAIL_CALLS)
    if chosen is None or not chosen["boundaries"]:
        report["stop"] = EXIT_NO_BLUEPRINT
        return report

    report["fixtures"] = {
        "solution_boundary_find": {"list": boundaries, "calls": "SolutionArchitect.find_solution_boundaries(search_string='*', page_size=500, graph_query_depth=1)"},
        "solution_boundary_by_guid_nested": {"by_guid": best["detail"], "calls": f"SolutionArchitect.get_solution_boundary_by_guid(guid={best['guid']!r}, graph_query_depth={args.depth}); "
                                             f"{len(best['nested'])} nested Solution Boundaries among its members (guid: depth, 1 = a direct member): {dict(sorted(best['nested'].items(), key=lambda kv: (kv[1], kv[0])))}"},
        "design_model_boundary_find_mixed_types": {"list": dmb, "calls": "CollectionManager.find_collections(search_string='*', metadata_element_type='DesignModelBoundary', page_size=500, "
                                                    f"graph_query_depth=1) returned types {types}"},
        "solution_blueprint_member_of_boundary": {"by_guid": chosen["detail"], "calls": f"SolutionArchitect.get_solution_blueprint_by_guid(guid={chosen['guid']!r}, graph_query_depth=3); "
                                                  f"memberOfCollections names the boundaries {[n for _, n in chosen['boundaries']]}"},
    }
    return report


def write_fixtures(args, fixtures: dict) -> list:
    stamp = args.date.replace("-", "_")
    written = []
    for what, spec in fixtures.items():
        counter: dict = {}
        body = {k: v for k, v in spec.items() if k != "calls"}
        total = len(body.get("list", [])) if "list" in body else 1
        if "list" in body:
            body["list"] = keep_first(body["list"])
        body = scrub(body, counter)
        kept = len(body["list"]) if "list" in body else 1
        note = (f"REAL SHAPE, read-only capture {args.date} from the live quickstart platform (container {args.container}-{args.container_id}, pyegeria {pyegeria_version()}), "
                f"{spec['calls']}. " + (f"{kept} of the {total} elements, unmodified. " if "list" in body else "The whole answer, unmodified. ")
                + f"Scrubbed of secrets: {counter.get('keys', 0)} keys and {counter.get('strings', 0)} strings dropped. Not SYNTHETIC.")
        text = json.dumps({"_note": note, **body}, indent=1, ensure_ascii=False) + "\n"
        assert_clean(text, what)
        written.append((FIXTURES / f"{what}_real_shape_{stamp}_{args.container}-{args.container_id}.json", text))
    for path, text in written:
        with open(path, "x", encoding="utf-8") as f:       # exclusive: an existing fixture is never replaced
            f.write(text)
        print(f"wrote {path.relative_to(HERE.parent)} ({len(text)} bytes)")
    return [p for p, _ in written]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Read-only capture of Solution Boundary fixtures from the live quickstart platform (find and get requests only).")
    ap.add_argument("--container", default="egeria-quickstart-platform", help="platform container name, used in the file names")
    ap.add_argument("--container-id", default=None, help="the platform image or container id suffix used in the file names, for example c461d5bfce7f (required unless --dry-run)")
    ap.add_argument("--date", default=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"), help="capture date, YYYY-MM-DD (default: today, UTC)")
    ap.add_argument("--depth", type=int, default=8, help="graph_query_depth for the boundary by GUID (the report spec's member hierarchy stops at 8 levels)")
    ap.add_argument("--dry-run", action="store_true", help="print the plan and the allowed calls; connect to nothing, write nothing")
    args = ap.parse_args(argv)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
        ap.error("--date must be YYYY-MM-DD")
    if args.dry_run:
        print("DRY RUN: connects to nothing, writes nothing.\nAllowed platform requests (find and get only):")
        for n in ALLOWED_CALLS:
            print(f"  {n}")
        print(f"Would write four files under {FIXTURES} named <what>_real_shape_{args.date.replace('-', '_')}_{args.container}-<id>.json:")
        for w in ("solution_boundary_find", "solution_boundary_by_guid_nested", "design_model_boundary_find_mixed_types", "solution_blueprint_member_of_boundary"):
            print(f"  {w}")
        return 0
    if not args.container_id or not re.fullmatch(r"[A-Za-z0-9._-]+", args.container_id) or not re.fullmatch(r"[A-Za-z0-9._-]+", args.container):
        ap.error("--container-id is required (letters, digits, . _ -), as is a plain --container")
    log: list = []

    async def run():
        sa, cm = await make_clients()
        return await capture(args, sa, cm, log)
    report = asyncio.run(run())
    print("requests made:")
    for line in log:
        print(f"  {line}")
    print(f"seen: {json.dumps(report['seen'])}")
    if report.get("stop") == EXIT_NO_NESTING:
        print("STOP: no boundary has a nested boundary among its members. Nothing was written. Report this; do not make one.")
        return EXIT_NO_NESTING
    if report.get("stop") == EXIT_NO_BLUEPRINT:
        print("STOP: no blueprint has a boundary in memberOfCollections. Nothing was written. Report this.")
        return EXIT_NO_BLUEPRINT
    write_fixtures(args, report["fixtures"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
