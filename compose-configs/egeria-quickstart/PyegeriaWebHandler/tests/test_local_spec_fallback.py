"""The Portal's own report specs are fallbacks for their Egeria-held copies (local_spec_fallback.py).

- Egeria holds the label: no local copy is registered, and the label resolves to the Egeria copy.
- Egeria does not hold it (cold cache, tier unavailable, spec pruned): the local copy is registered.

The EGERIA tier is replaced by in-memory copies built through pyegeria's own sync code
(egeria_spec_cache._build) from the Dr.Egeria document's Microflow text. No Egeria call is made.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402

import local_spec_fallback as lsf  # noqa: E402
import re_analytics  # noqa: E402
import report_spec_sync  # noqa: E402
from pyegeria.view import base_report_formats as brf  # noqa: E402
from pyegeria.view import egeria_spec_cache as esc  # noqa: E402
from pyegeria.view._output_format_models import FormatSetDict  # noqa: E402
from pyegeria.view.analytic_registry import get_analytic_registry  # noqa: E402
from pyegeria.view.microflow import format_set_to_microflow  # noqa: E402

DOC = Path(__file__).resolve().parent.parent / "egeria-held-specs" / "PORTAL_REPORT_SPECS.dr-egeria.md"
LABELS = [lsf.METRIC_TREND_LABEL, re_analytics.TILE_LABEL]


def _doc_commands() -> list[dict]:
    """Each `## Create Report Spec` block of the document as {attribute: value}."""
    out = []
    for block in DOC.read_text().split("\n## ")[1:]:
        head, *rest = block.split("\n### ")
        if not head.startswith("Create Report Spec"):
            continue
        attrs = {}
        for part in rest:
            name, _, value = part.partition("\n")
            attrs[name.strip()] = re.split(r"\n___", value)[0].strip()
        out.append(attrs)
    return out


def _egeria_copy(attrs: dict):
    """What the sync builds from the document's element (pyegeria's own _build)."""
    el = {"elementHeader": {"guid": "fe5aad27-0000-0000-0000-000000000000",
                            "type": {"typeName": "ReportSpec", "superTypeNames": ["ReportType", "Collection"]},
                            "versions": {"version": 1}},
          "properties": {"qualifiedName": attrs["Qualified Name"], "displayName": attrs["Display Name"],
                         "purpose": attrs["Purpose"], "description": attrs["Description"],
                         "category": attrs["Category"], "contentStatus": attrs["Content Status"],
                         "microflow": attrs["Microflow"]}}
    return esc._build(el, folders=["ReportSpecFolder::Consumer::Portal"], identity="test").format_set


@pytest.fixture
def egeria_holds(monkeypatch):
    """Make the EGERIA tier hold the given labels, as the sync would load them."""
    copies = {c["Display Name"]: c for c in _doc_commands()}

    def _set(labels):
        lsf._register_analytics()
        tier = FormatSetDict({label: _egeria_copy(copies[label]) for label in labels})
        monkeypatch.setattr(esc, "egeria_tier", lambda force=False: tier)
        monkeypatch.setattr(brf, "_egeria_tier", lambda: tier)
        return tier
    return _set


@pytest.fixture(autouse=True)
def _restore(monkeypatch):
    yield
    monkeypatch.undo()
    lsf.reconcile()   # back to whatever the real tier says


def _tier(label):
    _fs, tier, _label = brf.lookup_report_spec(label)
    return tier


def test_document_matches_the_local_definitions():
    cmds = {c["Display Name"]: c for c in _doc_commands()}
    assert sorted(cmds) == sorted(LABELS)
    for label, _source, build in lsf.fallbacks():
        attrs, fs = cmds[label], build()[label]
        # The sync's label rule (egeria_spec_cache._identify): ReportSpec::<label>, displayName == label.
        assert attrs["Qualified Name"] == f"ReportSpec::{label}"
        assert esc.label_from_qualified_name(attrs["Qualified Name"]) == label
        assert attrs["Content Status"] == "ACTIVE"
        assert attrs["Parent ID"] == "ReportSpecFolder::Consumer::Portal"
        assert json.loads(attrs["Microflow"]) == json.loads(format_set_to_microflow(fs).to_json())
        assert attrs["Purpose"] == fs.heading and attrs["Description"] == fs.description
        assert attrs["Category"] == fs.family
        assert [t.strip() for t in attrs["Output Types"].split(",")] == [t for f in fs.formats for t in f.types]
        eg = _egeria_copy(attrs)
        a, b = fs.model_dump(), eg.model_dump()
        assert a["formats"] == b["formats"] and a["target_type"] == b["target_type"]
        # The only action difference: "" vs None for the (absent) find function.
        assert {k: v for k, v in a["action"].items() if k != "function"} == \
               {k: v for k, v in b["action"].items() if k != "function"}
        assert not a["action"]["function"] and not b["action"]["function"]


def test_egeria_lacks_the_labels_local_copies_registered(egeria_holds):
    egeria_holds([])
    result = lsf.reconcile()
    assert result == {label: "local" for label in LABELS}
    for label in LABELS:
        assert label in brf._RUNTIME_REPORT_FORMATS.keys()
        assert _tier(label) == "local"


def test_egeria_holds_the_labels_no_local_copy(egeria_holds):
    egeria_holds([])
    lsf.reconcile()                       # start with the local copies registered
    egeria_holds(LABELS)
    result = lsf.reconcile()
    assert result == {label: "egeria" for label in LABELS}
    for label in LABELS:
        assert label not in brf._RUNTIME_REPORT_FORMATS.keys()
        assert _tier(label) == "egeria"
        assert brf.report_spec_source(label)["tier"] == "egeria"
    # The Curation Coverage analytic stays registered: the Egeria copy needs it to load and run.
    assert re_analytics.TILE_FUNCTION in get_analytic_registry()


def test_one_held_one_not(egeria_holds):
    egeria_holds([lsf.METRIC_TREND_LABEL])
    assert lsf.reconcile() == {lsf.METRIC_TREND_LABEL: "egeria", re_analytics.TILE_LABEL: "local"}
    assert _tier(lsf.METRIC_TREND_LABEL) == "egeria"
    assert _tier(re_analytics.TILE_LABEL) == "local"


def test_pruned_from_egeria_local_copy_comes_back(egeria_holds):
    egeria_holds(LABELS)
    lsf.reconcile()
    egeria_holds([])                      # a later sync pruned both
    assert lsf.reconcile() == {label: "local" for label in LABELS}
    for label in LABELS:
        assert _tier(label) == "local"


def test_tier_unavailable_uses_local_copies(monkeypatch):
    def boom(force=False):
        raise OSError("cache dir unreadable")
    monkeypatch.setattr(esc, "egeria_tier", boom)
    assert lsf.reconcile() == {label: "local" for label in LABELS}


def test_reconcile_is_idempotent(egeria_holds):
    egeria_holds([])
    assert lsf.reconcile() == lsf.reconcile() == {label: "local" for label in LABELS}
    egeria_holds(LABELS)
    assert lsf.reconcile() == lsf.reconcile() == {label: "egeria" for label in LABELS}


def test_a_sync_reconciles(monkeypatch):
    calls = []
    monkeypatch.setattr(lsf, "reconcile", lambda: calls.append(1) or {})
    monkeypatch.setattr(report_spec_sync, "configured_folders", lambda: ["ReportSpecFolder::Consumer::Portal"])

    class _Client:
        def close_session(self):
            pass

    class _Report:
        def to_dict(self):
            return {"folders": ["ReportSpecFolder::Consumer::Portal"], "added": [], "updated": [], "unchanged": [],
                    "pruned": [], "notes": [], "skipped": []}

    monkeypatch.setattr(report_spec_sync, "_service_client", lambda: _Client())
    monkeypatch.setattr(esc, "sync_report_specs", lambda client, shared=True: _Report())
    saved = dict(report_spec_sync._STATE)
    try:
        assert report_spec_sync._sync_once() == "synced"
    finally:
        report_spec_sync._STATE.clear()
        report_spec_sync._STATE.update(saved)
    assert calls == [1]
