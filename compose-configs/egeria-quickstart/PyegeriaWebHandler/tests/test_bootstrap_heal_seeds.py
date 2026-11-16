"""Hand seeds folded into auto-heal (BRIEF-RESET-RECOVERY-TOOLING-2026-11-12, Part 1).

Offline: discovery reads this checkout's dr-egeria-inbox and extra roots; nothing talks to Egeria.

- egeria-held-specs is an extra-root batch; Security is an inbox batch; Useful Dashboards is on
  by default. The Dr.Egeria help glossary is NOT a batch (owner, 2026-11-12).
- _folder_order.json runs each batch after the batches it depends on.
- Each of these batches' canary is the LAST element its files create, so a batch that stops
  part-way still shows as not healed.
- The FIXUP_2026_11_11 documents are archived outside the inbox and never discovered.
- Manual steps (the saved query's first refresh) report done / pending / not checked.
"""
import copy
import json
import re
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
HANDLER = HERE.parent
sys.path.insert(0, str(HANDLER))

import bootstrap_batches as bb  # noqa: E402
import bootstrap_monitor_handler as bm  # noqa: E402

REPO = HANDLER.parent.parent.parent
INBOX = REPO / "exchange-quickstart" / "loading-bay" / "dr-egeria-inbox"
ARCHIVE = REPO / "exchange-quickstart" / "loading-bay" / "dr-egeria-archive" / "2026-11-11"


@pytest.fixture
def batches(monkeypatch, tmp_path):
    monkeypatch.setattr(bb, "_INBOX_ROOT", INBOX)
    monkeypatch.setattr(bb, "_SCAN_ROOTS", [])
    monkeypatch.setenv("PYEGERIA_BOOTSTRAP_STORE", str(tmp_path / "selection.json"))  # no saved selection
    return {b["id"]: b for b in bb.batches_with_selection()}


def test_new_batches_are_discovered_with_their_flags(batches):
    held = batches["egeria-held-specs"]
    assert held["files"][0]["name"] == "REPORT_SPEC_CONSUMER_FOLDERS.dr-egeria.md"
    assert [f["name"] for f in held["files"]] == ["REPORT_SPEC_CONSUMER_FOLDERS.dr-egeria.md",
                                                 "PORTAL_REPORT_SPECS.dr-egeria.md"]
    assert held["enabled"] and held["idempotent"] is True       # upsert Creates, Add Member and Parent ID check first
    reason = json.loads((HANDLER / "egeria-held-specs" / "_batch.json").read_text())["idempotentReason"]
    assert "CollectionHandler.java:2309" in reason and "processors.py:519" in reason

    sec = batches["Security"]
    assert sec["enabled"] and sec["idempotent"] is True        # one Create, upsert: true in the compact spec
    assert sec["canary"] == {"type": "ExternalReference",
                             "name": "Guidelines for API Protection of Cloud-Native Systems"}

    assert "Dr.Egeria Help Glossary" not in batches             # owner: not loaded in this dev environment
    assert not (INBOX / "Dr.Egeria Help Glossary").exists()

    useful = batches["Useful Dashboards"]
    assert useful["enabled"] and useful["idempotent"] is False  # Add Text / Add Member re-add
    assert [m["id"] for m in useful["manualSteps"]] == ["saved-query-first-refresh"]


def test_the_owners_four_stay_off(batches):
    for bid in ("ML-OPS", "Sales-Forecast", "Sustainability Commands", "portal-usage-workload"):
        assert batches[bid]["enabled"] is False, bid


# ── Order ─────────────────────────────────────────────────────────────────────
# batch -> the batches that must run before it (what each one's files need).
DEPENDS_ON = {
    "Dashboard Folders": ["Local Dashboards"],           # files the next-steps sheet in both folders
    "egeria-held-specs": ["Dashboard Folders"],          # brief: after Dashboard Folders
    "Useful Dashboards": ["Dashboard Folders",           # FOLDERS doc files its sheets there
                          "egeria-held-specs"],          # SAVED_QUERY_TILE files a spec in Consumer::Portal
}


def test_order_runs_every_dependency_first(batches):
    order = json.loads((INBOX / "_folder_order.json").read_text())
    ids = list(batches)                                  # discovery order = run order
    for batch, needs in DEPENDS_ON.items():
        assert batch in order, f"{batch} must be listed in _folder_order.json"
        for need in needs:
            assert need in order, f"{need} must be listed in _folder_order.json"
            assert ids.index(need) < ids.index(batch), f"{need} must run before {batch}"


def test_every_listed_id_exists(batches):
    order = json.loads((INBOX / "_folder_order.json").read_text())
    assert [i for i in order if i not in batches] == []


# ── Canary = the last element created ─────────────────────────────────────────

def _blocks(text):
    """(command, {attribute: value}) for each `## Command` block."""
    out = []
    for m in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", text, re.M | re.S):
        attrs = {}
        for a in re.finditer(r"^### (.+?)\n+(.*?)(?=^### |^___|\Z)", m.group(2), re.M | re.S):
            attrs[a.group(1).strip()] = a.group(2).strip()
        out.append((m.group(1).strip(), attrs))
    return out


_CREATE_TYPE = {"Create Report Spec": "ReportSpec", "Create External Reference": "ExternalReference",
                "Create Term": "GlossaryTerm", "Create Report": "Report", "Create Saved Query": "SavedQuery",
                "Create Results Set": "ResultsSet", "Create Dashboard Sheet": "Dashboard",
                "Create Collection Folder": "CollectionFolder", "Create Root Collection": "RootCollection",
                "Create Glossary": "Glossary"}


def _created(command, attrs):
    """(type, displayName) of the element a command creates, or None."""
    if command in ("Link Report to Dashboard Sheet", "Add Text on Dashboard Sheet"):
        # A placement: a DisplayDataField named "<sheet> / <placement name>"
        # (md_processing/v2/dashboard_sheet.placement_display_name).
        name = attrs.get("Placement Name") or attrs.get("Report Name")
        return "DisplayDataField", f"{attrs['Dashboard Sheet Name']} / {name}"
    if command in _CREATE_TYPE:
        return _CREATE_TYPE[command], attrs.get("Display Name")
    if command.startswith(("Create ", "Add Text")):
        raise AssertionError(f"unmapped creating command {command!r}: add it to _CREATE_TYPE")
    return None                       # Add Member, Link ... between existing elements


@pytest.mark.parametrize("bid", ["egeria-held-specs", "Security", "Useful Dashboards"])
def test_canary_is_the_last_element_created(batches, bid):
    b = batches[bid]
    last = None
    for f in b["files"]:
        for command, attrs in _blocks((Path(b["path"]) / f["name"]).read_text()):
            made = _created(command, attrs)
            if made:
                last = made
    assert last == (b["canary"]["type"], b["canary"]["name"])


# ── FIXUPs archived ───────────────────────────────────────────────────────────

def test_fixups_are_archived_and_never_discovered(batches):
    assert sorted(p.name for p in ARCHIVE.glob("FIXUP_2026_11_11_*.md")) == [
        "FIXUP_2026_11_11_SAVED_QUERY_TILE_ROUTE_B.dr-egeria.md",
        "FIXUP_2026_11_11_USEFUL_SHEETS_TEXT.dr-egeria.md"]
    assert "never run" in (ARCHIVE / "README.md").read_text().lower()
    assert list(INBOX.rglob("FIXUP_*")) == []
    for b in batches.values():
        assert not [f for f in b["files"] if "FIXUP" in f["name"]], b["id"]
    assert "exclude" not in json.loads((INBOX / "Useful Dashboards" / "_batch.json").read_text())


# ── Manual step: the saved query's first refresh ──────────────────────────────

STEP = json.loads((INBOX / "Useful Dashboards" / "_batch.json").read_text())["manualSteps"][0]
BASE = {"id": STEP["id"], "description": STEP["description"], "how": STEP["how"]}


# The real find response for the step's element, fetched read-only as erinoverview on laz
# (2026-11-13): a raw OpenMetadataElement, additionalProperties as a MapTypePropertyValue.
REAL = json.loads((Path(__file__).parent / "fixtures" / "saved_query_find_raw_laz_2026_11_13.json").read_text())


def _el(additional):
    """The real element with its additionalProperties map replaced, in the real (raw) shape."""
    el = copy.deepcopy(REAL[0])
    el["elementProperties"]["propertyValueMap"]["additionalProperties"]["mapValues"]["propertyValueMap"] = {
        k: {"class": "PrimitiveTypePropertyValue", "typeName": "string",
            "primitiveTypeCategory": "OM_PRIMITIVE_TYPE_STRING", "primitiveValue": v}
        for k, v in additional.items()}
    return [el]


def test_manual_step_done_on_the_real_find_response():
    assert REAL[0]["elementProperties"]["propertyValueMap"]["qualifiedName"]["primitiveValue"] == STEP["qualifiedName"]
    st = bm._manual_step_from_elements(STEP, BASE, REAL)
    assert st["state"] == "done"
    assert st["detail"] == "lastRefreshedTime = 2026-11-12T16:58:59.395564+00:00; resultCount = 48"


def test_manual_step_flat_shape_still_read_as_a_fallback():
    flat = [{"properties": {"qualifiedName": STEP["qualifiedName"],
                            "additionalProperties": {"lastRefreshedTime": "t", "resultCount": "3"}}}]
    assert bm._manual_step_from_elements(STEP, BASE, flat)["detail"] == "lastRefreshedTime = t; resultCount = 3"


def test_manual_step_element_without_additional_properties_is_pending():
    el = copy.deepcopy(REAL[0])
    del el["elementProperties"]["propertyValueMap"]["additionalProperties"]
    assert bm._manual_step_from_elements(STEP, BASE, [el])["state"] == "pending"


def _raw_additional(value):
    el = copy.deepcopy(REAL[0])
    el["elementProperties"]["propertyValueMap"]["additionalProperties"] = value
    return el


@pytest.mark.parametrize("el", [
    {"elementGUID": "g"},                                         # neither raw nor flat
    {"elementHeader": {}, "props": {"additionalProperties": {}}},  # some other reshaping
    "not an element",
    None,
    {"elementProperties": "x"},
    _raw_additional({"class": "MapTypePropertyValue"}),           # raw, map without mapValues
    _raw_additional("lastRefreshedTime=t"),                       # raw, map not a map
    {"properties": {"additionalProperties": ["lastRefreshedTime"]}},  # flat, map not a dict
], ids=["no-properties", "other-reshape", "string", "none", "elementProperties-not-dict",
        "raw-no-mapValues", "raw-map-is-string", "flat-map-is-list"])
def test_manual_step_unrecognised_element_shape_is_not_checked(el):
    st = bm._manual_step_from_elements(STEP, BASE, [el])
    assert st["state"] == "not checked"            # never "pending" on a shape we could not read
    assert "unrecognised element shape" in st["detail"]


def test_manual_step_flat_element_without_additional_properties_is_pending():
    flat = [{"properties": {"qualifiedName": STEP["qualifiedName"]}}]
    assert bm._manual_step_from_elements(STEP, BASE, flat)["state"] == "pending"


def test_manual_step_done_names_time_and_count():
    st = bm._manual_step_from_elements(STEP, BASE, _el({"lastRefreshedTime": "2026-11-12T10:00:00Z", "resultCount": "17"}))
    assert st["state"] == "done"
    assert st["detail"] == "lastRefreshedTime = 2026-11-12T10:00:00Z; resultCount = 17"


def test_manual_step_pending_says_not_yet_refreshed():
    st = bm._manual_step_from_elements(STEP, BASE, _el({"pyegeriaInsightsQuery": "true"}))
    assert st["state"] == "pending" and st["detail"].startswith("saved query not yet refreshed")


@pytest.mark.parametrize("els", [[], None, "No elements found"])
def test_manual_step_without_the_element_is_not_checked(els):
    st = bm._manual_step_from_elements(STEP, BASE, els)
    assert st["state"] == "not checked"            # never "pending" or a silent 0


def test_manual_step_lookup_failure_is_not_checked(monkeypatch):
    import asyncio
    import pyegeria

    class Boom:
        def __init__(self, *a, **k): raise ConnectionError("platform down")

    monkeypatch.setattr(pyegeria, "MetadataExpert", Boom)
    st = asyncio.run(bm._manual_step_state(STEP))
    assert st["state"] == "not checked" and "ConnectionError" in st["detail"]
