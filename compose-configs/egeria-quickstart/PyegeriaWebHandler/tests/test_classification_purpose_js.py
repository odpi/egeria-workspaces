"""Classification-purpose helpers in static/egeria-shared-ui.js, run under node,
plus checks that type-explorer.html wires them in. Standalone; the node tests
are skipped when node is not installed (the Portal container has none).

The purpose map used here is the real one laz reported on 2026-11-11
(fixtures/classification_defs_laz_2026_11_11.json)."""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
UI = (ROOT / "static" / "egeria-shared-ui.js").read_text()
TE = (ROOT / "type-explorer.html").read_text()
LAZ_ALL = json.loads((Path(__file__).resolve().parent / "fixtures" / "classification_defs_laz_2026_11_11.json").read_text())["allPurposes"]


def _block():
    """The data + pure helpers of the classification-purpose block (no React)."""
    grab = lambda pat: re.search(pat, UI, re.S).group(0)
    return "\n".join([
        grab(r"var CLS_PURPOSES = \{.*?\n\};"),
        grab(r"var CLS_PURPOSE_ORDER = [^\n]*;"),
        grab(r"Object\.keys\(CLS_PURPOSES\)\.forEach[^\n]*\n"),
        grab(r"var _CLS_NO_PURPOSE = \{.*?\};"),
        grab(r"function clsPurposeInfo\(purpose\) \{.*?\n\}"),
        grab(r"function clsPurposeKey\(purpose, unrecognised\) \{.*?\n\}"),
        grab(r"function clsPurposeInfoForKey\(key\) \{.*?\n\}"),
        grab(r"var _clsPurposeCache = \{\};"),
        grab(r"function _clsPurposeEntry\(creds\) \{.*?\n\}"),
        grab(r"function _clsPurposeNotify\(entry\) \{.*?\n\}"),
        grab(r"function seedClassificationPurposes\(map, serverReportsPurpose, creds, unrecognised\) \{.*?\n\}"),
        grab(r"function groupByClassificationPurpose\(items, getTypeName, purposeOf, unrecognisedOf\) \{.*?\n\}"),
    ])


def _node(body):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    js = _block() + "\n" + body
    out = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_six_purposes_match_the_backend():
    # Read the backend tuple from source: this file runs where node is (the
    # host), which need not have the handler's dependencies.
    src = (ROOT / "type_system_handler.py").read_text()
    backend = re.findall(r'"([A-Z_]+)"', re.search(r"CLS_PURPOSES: tuple\[str, \.\.\.\] = \((.*?)\)", src, re.S).group(1))
    assert len(backend) == 6
    keys = _node("console.log(JSON.stringify([Object.keys(CLS_PURPOSES).sort(), CLS_PURPOSE_ORDER]));")
    assert keys[0] == sorted(backend)
    assert sorted(keys[1]) == sorted(backend)


def test_group_laz_types_in_display_order_unclassified_last():
    groups = _node(
        f"var m = {json.dumps(LAZ_ALL)};"
        "var g = groupByClassificationPurpose(Object.keys(m).sort(), function(n){return n;}, function(n){return m[n];});"
        "console.log(JSON.stringify(g.map(function(x){return [x.purpose, x.info.label, x.items.length];})));"
    )
    assert groups == [
        ["GOVERNANCE", "Governance", 15],
        ["GOVERNANCE_IMPLEMENTATION", "Governance Implementation", 10],
        ["CATEGORY", "Category", 46],
        ["DESCRIPTIVE", "Descriptive", 6],
        ["ANALYTICAL", "Analytical", 6],
        ["MANAGEMENT", "Management", 10],
        [None, "No purpose reported", 1],
    ]


def test_empty_groups_are_dropped_and_unknown_is_unclassified_not_category():
    groups = _node(
        "var m = {Confidentiality: 'GOVERNANCE', Odd: 'STRUCTURAL', Bare: null};"
        "var g = groupByClassificationPurpose(['Confidentiality','Odd','Bare','NotInMap'], function(n){return n;}, function(n){return m[n] || null;});"
        "console.log(JSON.stringify(g.map(function(x){return [x.purpose, x.items];})));"
    )
    # A value with no recognised purpose and no raw value is "No purpose reported".
    assert groups == [["GOVERNANCE", ["Confidentiality"]], [None, ["Odd", "Bare", "NotInMap"]]]


def test_seed_from_api_types_dict_derives_server_reports():
    res = _node(
        "seedClassificationPurposes({A: {classificationPurpose: 'CATEGORY'}, B: {}, C: {classificationPurpose: 'BOGUS'}}, undefined, {url:'u', server:'s'});"
        "var e = _clsPurposeEntry({url:'u', server:'s'});"
        "seedClassificationPurposes({X: {}, Y: {classificationPurpose: null}}, undefined, {url:'u', server:'old'});"
        "var o = _clsPurposeEntry({url:'u', server:'old'});"
        "console.log(JSON.stringify([e.purposes, e.serverReportsPurpose, o.purposes, o.serverReportsPurpose]));"
    )
    assert res == [{"A": "CATEGORY", "B": None, "C": None}, True, {"X": None, "Y": None}, False]


def test_unrecognised_is_its_own_group_between_known_and_none():
    groups = _node(
        "var p = {Confidentiality: 'GOVERNANCE', FutureKind: null, Other: null, Bare: null};"
        "var u = {FutureKind: 'PROVENANCE', Other: 'ARCHIVAL'};"
        "var g = groupByClassificationPurpose(Object.keys(p), function(n){return n;}, function(n){return p[n];}, function(n){return u[n] || null;});"
        "console.log(JSON.stringify(g.map(function(x){return [x.key, x.info.label, x.items];})));"
    )
    assert groups == [
        ["GOVERNANCE", "Governance", ["Confidentiality"]],
        ["__unrec:ARCHIVAL", "Not recognised: ARCHIVAL", ["Other"]],
        ["__unrec:PROVENANCE", "Not recognised: PROVENANCE", ["FutureKind"]],
        ["__none", "No purpose reported", ["Bare"]],
    ]


def test_unrecognised_info_names_the_value():
    info = _node("console.log(JSON.stringify([clsPurposeInfoForKey('__unrec:PROVENANCE'), clsPurposeInfoForKey('__none').desc]));")
    assert info[0]["desc"].startswith("Purpose not recognised by this Portal: PROVENANCE")
    assert info[0]["raw"] == "PROVENANCE"
    assert info[1] == "The server reports no purpose for these classification types."


def test_seed_keeps_unrecognised_values():
    res = _node(
        "seedClassificationPurposes({A: {classificationPurpose: null, classificationPurposeUnrecognised: 'PROVENANCE'}, "
        "B: {classificationPurpose: 'NEWER_THAN_PAGE'}, C: {}}, undefined, {url:'u', server:'s3'});"
        "var e = _clsPurposeEntry({url:'u', server:'s3'});"
        "seedClassificationPurposes({X: null}, true, {url:'u', server:'s4'}, {X: 'PROVENANCE'});"
        "var f = _clsPurposeEntry({url:'u', server:'s4'});"
        "console.log(JSON.stringify([e.purposes, e.unrecognised, e.serverReportsPurpose, f.unrecognised]));"
    )
    assert res == [{"A": None, "B": None, "C": None}, {"A": "PROVENANCE", "B": "NEWER_THAN_PAGE"}, True, {"X": "PROVENANCE"}]


def test_seed_from_endpoint_payload_keeps_explicit_flag():
    res = _node(
        "seedClassificationPurposes({}, false, null);"
        "var e = _clsPurposeEntry(null);"
        "console.log(JSON.stringify([e.purposes, e.serverReportsPurpose]));"
    )
    assert res == [{}, False]


# ── Wiring (static checks) ────────────────────────────────────────────────────

def test_shared_ui_exports_and_endpoint():
    for name in ("function useClassificationPurposes(creds)", "function ClsPurposeBadge(",
                 "function ClsPurposeChips(", "function ClsPurposeGroup(",
                 "'/api/types/classification-purposes'",
                 "https://egeria-project.org/concepts/classification-purpose/"):
        assert name in UI, name


def test_element_panels_group_by_purpose_and_say_when_none():
    body = re.search(r"function ClassificationsAndRawJson\(\{ item, creds \}\) \{.*?\n\}\n", UI, re.S).group(0)
    assert "useClassificationPurposes(effectiveCreds)" in body
    assert body.index("useClassificationPurposes") < body.index("if (!item) return null")   # hook before early return
    assert "cp.ready && cp.serverReportsPurpose === true" in body                            # flat until known
    assert "cp.serverReportsPurpose === false && " in body and "CLS_PURPOSE_NONE_HINT" in body
    assert "defaultOpen: false" in body                                                      # section still starts folded


def test_type_explorer_wiring():
    assert "seedClassificationPurposes(data.classifications || {}, undefined, creds);" in TE
    assert "renderClassifRows(filtClassif, true)" in TE and "renderClassifRows(filtClassif, false)" in TE
    assert "React.createElement(ClsPurposeChips, {" in TE
    assert "About classification purposes" in TE
    assert "allClassifs.length > 0 && !clsPurposesReported" in TE                        # hint, not empty groups
    assert "Purpose not recognised by this Portal: " in TE                               # C2: type page
    assert "No purpose reported: the server gives this classification type no purpose." in TE
    assert "cp.purposeOf, cp.unrecognisedOf" in UI                                         # C2: detail panels
