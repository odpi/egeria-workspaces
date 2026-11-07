"""Guards for the report-spec valid-values heal batch: the committed document is
what the generator emits, the manifest's canary names a value the document really
sets (last), and the batch registers with the bootstrap discovery."""
import json
import re
from pathlib import Path

import gen_report_spec_valid_values as gen

HERE = Path(__file__).resolve().parent
FOLDER = HERE / "report-spec-valid-values"
MANIFEST = json.loads((FOLDER / "_batch.json").read_text(encoding="utf-8"))


def test_committed_document_is_generated_output():
    assert (FOLDER / "REPORT_SPEC_VALID_VALUES.dr-egeria.md").read_text(encoding="utf-8") == gen.render()


def test_all_properties_covered_once():
    props = [p for p, _, _ in gen.PROPERTIES]
    assert sorted(props) == sorted([
        "completenessDeclared", "confidenceForm", "uncertaintyForm", "outputFormat", "renderer",
        "placementKind", "span", "presentationStyle", "layoutStyle"])
    assert len(props) == len(set(props))


def test_output_formats_include_those_missing_from_installed_pyegeria():
    for fmt in ("KPI", "BAR", "PIE", "SERIES", "GRAPH", "REPORT-GRAPH", "HTML"):
        assert fmt in gen.OUTPUT_FORMATS


def test_canary_names_last_value_the_document_sets():
    doc = gen.render()
    rows = re.findall(r"^\| (\S+) \| (\S+) \|", doc, re.M)
    rows = [r for r in rows if r[0] != "Preferred"]
    assert MANIFEST["canary"] == {"type": gen.CANARY_TYPE, "name": gen.canary_name()}
    assert rows[-1][1] == MANIFEST["canary"]["name"]  # displayName Egeria stores
    # unique across the document so no other value of ours can satisfy the canary
    assert [r[1] for r in rows].count(MANIFEST["canary"]["name"]) == 1


def test_manifest_flags():
    assert MANIFEST["defaultEnabled"] is True and MANIFEST["idempotent"] is True
    assert MANIFEST["files"] == ["REPORT_SPEC_VALID_VALUES.dr-egeria.md"]


def test_batch_root_registered():
    import bootstrap_batches as bb
    assert ("portal-report-spec-valid-values", FOLDER) in bb._EXTRA_BATCH_ROOTS


def test_placement_values_and_types():
    doc = gen.render()
    for prop in ("placementKind", "span", "presentationStyle"):
        for t in ("DisplayDataField", "DisplayDataContainer"):
            assert re.search(rf"### Metadata Property Name\n{prop}\n\n### Type Name\n{t}\n", doc)
    vals = {p: [v for v, _ in vs] for p, vs, _ in gen.PROPERTIES}
    assert vals["placementKind"] == ["report", "text"]
    assert vals["span"] == ["1", "2", "full"]
    assert vals["presentationStyle"] == ["kpi", "panel"]
