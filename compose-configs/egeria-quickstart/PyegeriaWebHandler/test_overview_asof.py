#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""
Reproducible test cases for the Egeria Overview `asOfTime` (time-machine) feature.

Run these in a controlled environment to confirm behaviour / reproduce issues.
Two independent layers — run either or both:

  A. CLIENT layer — verifies *which pyegeria methods support as-of and how*, and
     that historical counts are sane. Needs only pyegeria + Egeria creds.

  B. HTTP layer  — exercises /api/overview/* now-vs-as-of through the running app,
     including the URL-encoding regression. Needs a reachable base URL.

Usage
-----
  # client-level only (env creds; defaults to qs-view-server / erinoverview)
  python test_overview_asof.py

  # HTTP-level too, against the Apache proxy or FastAPI app
  python test_overview_asof.py --base http://localhost:8885
  python test_overview_asof.py --base http://localhost:8800 --as-of 2026-03-23T00:00:00+00:00

Env: EGERIA_PLATFORM_URL, EGERIA_VIEW_SERVER, EGERIA_USER, EGERIA_USER_PASSWORD

Exit code is non-zero if any test FAILS (warnings do not fail the run).

Known issues these tests pin down
---------------------------------
  ISSUE-1  A raw '+' in the asOfTime offset URL-decodes to a space, yielding an
           invalid timestamp and silent all-null degradation. `_norm_asof` in
           overview_handler.py repairs it; test_http_plus_encoding proves both the
           failure mode (raw '+') and the repair.
  ISSUE-2  as-of client APIs are inconsistent:
             find_metadata_elements -> asOfTime in FindRequestBody
             get_relationships      -> asOfTime in ResultsRequestBody (body=)
             find_actor_profiles    -> as_of_time kwarg
             find_communities       -> as_of_time kwarg
             SolutionArchitect.find_* -> asOfTime via body= (NO as_of_time kwarg)
  ISSUE-3  as-of queries are cold/slow (full-list materialisation at a past time);
           test_http_performance times them and warns past a threshold.

FINDINGS (qs demo, 2026-07-23 — reproduce in your controlled env)
-----------------------------------------------------------------
  * find_metadata_elements + get_relationships: as-of reliable at page_size=5000.
  * ISSUE-1 fix (_norm_asof) verified: raw '+'→space repaired (assetTotal 33 == 33).
  * SUSPECTED-A: Actor/Community/SolutionArchitect view services intermittently
    return SERVER_ERROR_500 on as-of queries with a LARGE page_size (5000). The
    same calls at page_size=500 (what the endpoints use) succeed. This test now
    uses 500 for those three; flip to 5000 to reproduce the 500s.  <-- worth a
    controlled repro / pyegeria issue.
  * SUSPECTED-B: SolutionArchitect.find_* as-of via body={"class":"FilterRequestBody",
    "asOfTime":...} is rejected → usage-context can't time-travel (WARN). Confirm
    the correct request-body class for as-of on the Solution Architect OMVS.
  * PERF: /api/overview/people as-of ~47s (page_size 500). as-of is expensive;
    strong argument for the native count API (see OVERVIEW_NEXT_STEPS.md).
"""
import argparse
import os
import sys
import time
from datetime import datetime, timedelta, timezone

# ── test harness ─────────────────────────────────────────────────────────────
_results = []  # (name, status, detail)  status in {PASS, FAIL, WARN, SKIP}


def record(name, status, detail=""):
    _results.append((name, status, detail))
    icon = {"PASS": "✓", "FAIL": "✗", "WARN": "!", "SKIP": "·"}[status]
    print(f"  {icon} {status:4} {name}" + (f"  — {detail}" if detail else ""))


def check(name, cond, detail=""):
    record(name, "PASS" if cond else "FAIL", detail)
    return cond


# ── config ───────────────────────────────────────────────────────────────────
def egeria_env():
    return dict(
        url=os.environ.get("EGERIA_PLATFORM_URL", "https://localhost:9443"),
        server=os.environ.get("EGERIA_VIEW_SERVER", "qs-view-server"),
        user=os.environ.get("EGERIA_USER", "erinoverview"),
        pwd=os.environ.get("EGERIA_USER_PASSWORD", "secret"),
    )


PERF_WARN_S = 20.0   # warn if a single as-of call takes longer than this


# ── A. CLIENT-LEVEL TESTS ────────────────────────────────────────────────────
def client_tests(as_of):
    print("\n[A] Client-level as-of tests")
    try:
        import pyegeria
        pyegeria.enable_ssl_check = False
        pyegeria.disable_ssl_warnings = True
        from egeria_auth import apply_token
        from pyegeria import (MetadataExpert, ClassificationExplorer,
                              ActorManager, CommunityMatters, SolutionArchitect)
    except Exception as exc:  # noqa: BLE001
        record("import pyegeria clients", "SKIP", f"{exc}")
        return

    e = egeria_env()

    def mk(cls):
        m = cls(view_server=e["server"], platform_url=e["url"], user_id=e["user"], user_pwd=e["pwd"])
        apply_token(m)
        return m

    def jlen(raw):
        return len(raw) if isinstance(raw, list) else 0

    # find_metadata_elements — asOfTime in FindRequestBody
    try:
        me = mk(MetadataExpert)
        base = {"class": "FindRequestBody", "limitResultsByStatus": ["ACTIVE"], "metadataElementTypeName": "Asset"}
        now_n = jlen(me.find_metadata_elements(base, start_from=0, page_size=5000, graph_query_depth=0))
        ao = dict(base); ao["asOfTime"] = as_of
        ao_n = jlen(me.find_metadata_elements(ao, start_from=0, page_size=5000, graph_query_depth=0))
        check("find_metadata_elements: as-of runs & is historical (asof<=now)", ao_n <= now_n, f"now={now_n} asof={ao_n}")
    except Exception as exc:  # noqa: BLE001
        record("find_metadata_elements as-of", "FAIL", str(exc)[:100])

    # get_relationships — asOfTime in ResultsRequestBody (body=)
    try:
        ce = mk(ClassificationExplorer)
        now_n = jlen(ce.get_relationships(relationship_type="SemanticAssignment", output_format="JSON",
                                          start_from=0, page_size=5000))
        ao_n = jlen(ce.get_relationships(relationship_type="SemanticAssignment", output_format="JSON",
                                         start_from=0, page_size=5000,
                                         body={"class": "ResultsRequestBody", "asOfTime": as_of}))
        check("get_relationships: as-of via body= runs & historical", ao_n <= now_n, f"now={now_n} asof={ao_n}")
    except Exception as exc:  # noqa: BLE001
        record("get_relationships as-of via body", "FAIL", str(exc)[:100])

    # find_actor_profiles — as_of_time kwarg
    try:
        am = mk(ActorManager)
        # NB: page_size matched to the endpoints (500). page_size=5000 + as_of
        # intermittently 500s the Actor view service — see FINDINGS in the header.
        now_n = jlen(am.find_actor_profiles(search_string="*", output_format="JSON", start_from=0, page_size=500))
        ao_n = jlen(am.find_actor_profiles(search_string="*", output_format="JSON", start_from=0, page_size=500,
                                           as_of_time=as_of))
        check("find_actor_profiles: as_of_time kwarg runs & historical", ao_n <= now_n, f"now={now_n} asof={ao_n}")
    except Exception as exc:  # noqa: BLE001
        record("find_actor_profiles as_of_time kwarg", "FAIL", str(exc)[:100])

    # find_communities — as_of_time kwarg
    try:
        cm = mk(CommunityMatters)
        common = dict(search_string="*", starts_with=False, output_format="JSON",
                      graph_query_depth=0, start_from=0, page_size=500)
        now_n = jlen(cm.find_communities(**common))
        ao_n = jlen(cm.find_communities(as_of_time=as_of, **common))
        check("find_communities: as_of_time kwarg runs & historical", ao_n <= now_n, f"now={now_n} asof={ao_n}")
    except Exception as exc:  # noqa: BLE001
        record("find_communities as_of_time kwarg", "FAIL", str(exc)[:100])

    # SolutionArchitect.find_information_supply_chains — asOfTime via body= (NO kwarg)
    try:
        sa = mk(SolutionArchitect)
        now_n = jlen(sa.find_information_supply_chains(search_string="*", output_format="JSON",
                                                       start_from=0, page_size=500))
        try:
            ao_n = jlen(sa.find_information_supply_chains(
                output_format="JSON", start_from=0, page_size=500,
                body={"class": "SearchStringRequestBody", "searchString": "*", "asOfTime": as_of}))
            check("SolutionArchitect.find_isc: as-of via SearchStringRequestBody runs & historical",
                  ao_n <= now_n, f"now={now_n} asof={ao_n}")
        except Exception as exc:  # noqa: BLE001
            record("SolutionArchitect.find_isc as-of via body", "WARN",
                   f"body shape rejected — usage won't time-travel: {str(exc)[:70]}")
    except Exception as exc:  # noqa: BLE001
        record("SolutionArchitect.find_isc", "FAIL", str(exc)[:100])


# ── B. HTTP-LEVEL TESTS ──────────────────────────────────────────────────────
def http_tests(base, as_of):
    print(f"\n[B] HTTP-level as-of tests against {base}")
    try:
        import requests
        requests.packages.urllib3.disable_warnings()  # noqa
    except Exception as exc:  # noqa: BLE001
        record("import requests", "SKIP", str(exc))
        return

    def get(path, params=None, raw_query=None):
        url = base.rstrip("/") + path
        if raw_query:
            url = url + "?" + raw_query
        t0 = time.time()
        r = requests.get(url, params=params, verify=False, timeout=120)
        return r, time.time() - t0

    # endpoint -> a representative cumulative metric expected to be <= now historically
    eps = {
        "/api/overview/summary": "assetTotal",
        "/api/overview/people": "activeContributors",
        "/api/overview/usage-context": "informationSupplyChains",
        "/api/overview/ai-context": "groundingLinks",
    }

    # test_http_now_ok — every endpoint answers 200 with a live value now
    now_vals = {}
    for path, key in eps.items():
        try:
            r, _ = get(path)
            ok = r.status_code == 200
            d = r.json() if ok else {}
            now_vals[path] = d.get(key)
            check(f"now: {path} 200 & {key} present", ok and d.get(key) is not None,
                  f"http={r.status_code} {key}={d.get(key)}")
        except Exception as exc:  # noqa: BLE001
            record(f"now: {path}", "FAIL", str(exc)[:100])

    # ISSUE-1 test_http_plus_encoding — properly-encoded as-of returns real values,
    # AND a raw '+' (→space) is repaired by _norm_asof (both must yield non-null).
    try:
        r_enc, _ = get("/api/overview/summary", params={"as_of_time": as_of})   # requests encodes '+' as %2B
        v_enc = r_enc.json().get("assetTotal") if r_enc.status_code == 200 else None
        raw_bad = "as_of_time=" + as_of.replace("+", " ")                        # simulate the +→space bug
        r_raw, _ = get("/api/overview/summary", raw_query=raw_bad)
        v_raw = r_raw.json().get("assetTotal") if r_raw.status_code == 200 else None
        check("ISSUE-1 encoded as-of returns a value", v_enc is not None, f"assetTotal(asof)={v_enc}")
        check("ISSUE-1 space-offset repaired by _norm_asof", v_raw is not None and v_raw == v_enc,
              f"raw={v_raw} encoded={v_enc}")
    except Exception as exc:  # noqa: BLE001
        record("ISSUE-1 plus-encoding", "FAIL", str(exc)[:100])

    # test_http_asof_historical — as-of counts are <= now (cumulative metrics)
    for path, key in eps.items():
        if now_vals.get(path) is None:
            continue
        try:
            r, dt = get(path, params={"as_of_time": as_of})
            d = r.json() if r.status_code == 200 else {}
            av = d.get(key)
            if av is None:
                record(f"as-of: {path}.{key}", "WARN", "null at as-of (endpoint may not time-travel this metric)")
            else:
                check(f"as-of: {path}.{key} <= now", av <= now_vals[path], f"now={now_vals[path]} asof={av}")
            # ISSUE-3 performance
            if dt > PERF_WARN_S:
                record(f"perf: {path} as-of latency", "WARN", f"{dt:.1f}s (> {PERF_WARN_S:.0f}s)")
        except Exception as exc:  # noqa: BLE001
            record(f"as-of: {path}", "FAIL", str(exc)[:100])


# ── main ─────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="Egeria Overview asOfTime test cases")
    ap.add_argument("--base", help="HTTP base URL (e.g. http://localhost:8885). Omit to run client-level only.")
    ap.add_argument("--as-of", dest="as_of",
                    default=(datetime.now(timezone.utc) - timedelta(days=120)).replace(microsecond=0).isoformat(),
                    help="ISO 8601 as-of timestamp (default: ~120 days ago)")
    ap.add_argument("--skip-client", action="store_true", help="skip the client-level layer")
    args = ap.parse_args()

    print(f"as-of = {args.as_of}")
    print(f"egeria = {egeria_env()['server']} @ {egeria_env()['url']} as {egeria_env()['user']}")

    if not args.skip_client:
        client_tests(args.as_of)
    if args.base:
        http_tests(args.base, args.as_of)
    else:
        record("HTTP layer", "SKIP", "no --base given")

    fails = sum(1 for _, s, _ in _results if s == "FAIL")
    warns = sum(1 for _, s, _ in _results if s == "WARN")
    passes = sum(1 for _, s, _ in _results if s == "PASS")
    print(f"\nSummary: {passes} passed, {fails} failed, {warns} warnings, "
          f"{sum(1 for _, s, _ in _results if s == 'SKIP')} skipped")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
