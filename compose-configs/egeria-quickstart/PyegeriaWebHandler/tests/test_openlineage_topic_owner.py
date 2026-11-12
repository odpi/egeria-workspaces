"""One owner for the Kafka topic openlineage.events (owner, 2026-11-12).

On 2026-11-12 the quickstart had two Topic assets for openlineage.events, one from the OpenLineage
Events batch (LocalKafka2) and one from the Coco Data Hub tutorial notebook (Kafka-Broker), both
catalog targets of the OpenLineageKafkaListener, so every event was consumed twice. The batch owns
the topic; the notebook is excluded from the Data Hub batch and skips registration when any Topic
named openlineage.events exists. Offline: discovery reads this checkout; nothing talks to Egeria.
"""
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import bootstrap_batches as bb  # noqa: E402

REPO = HERE.parent.parent.parent.parent
INBOX = REPO / "exchange-quickstart" / "loading-bay" / "dr-egeria-inbox"
NOTEBOOK = REPO / "coco-workbooks" / "1. coco-data-hub" / "receiving-open-lineage-events.ipynb"


@pytest.fixture
def batches(monkeypatch, tmp_path):
    monkeypatch.setattr(bb, "_INBOX_ROOT", INBOX)
    monkeypatch.setattr(bb, "_SCAN_ROOTS", [REPO / "coco-workbooks"])
    monkeypatch.setenv("PYEGERIA_BOOTSTRAP_STORE", str(tmp_path / "selection.json"))
    return {b["id"]: b for b in bb.discover_batches()}


def test_data_hub_batch_no_longer_runs_the_notebook(batches):
    hub = batches["Coco - 1. Data Hub"]
    assert not [f for f in hub["files"] if "receiving-open-lineage-events" in f]
    manifest = json.loads((REPO / "coco-workbooks" / "1. coco-data-hub" / "_batch.json").read_text())
    assert "receiving-open-lineage-events.ipynb" in manifest["exclude"]
    assert "OpenLineage Events batch owns openlineage.events" in manifest["excludeReasons"]["receiving-open-lineage-events.ipynb"]
    assert "receiving the OpenLineage events" not in manifest["description"]
    # The Data Hub canary is made by a document the batch still runs.
    assert manifest["canary"]["name"] in (REPO / "coco-workbooks" / "1. coco-data-hub" /
                                          "software-development-governance-program.md").read_text()


def test_no_batch_runs_the_notebook(batches):
    for b in batches.values():
        assert not [f for f in b["files"] if f.endswith("receiving-open-lineage-events.ipynb")], b["id"]


def test_openlineage_events_batch_owns_the_topic(batches):
    ol = batches["OpenLineage Events"]
    assert ol["canary"] == {"type": "Topic", "name": "openlineage.events"}
    assert ol["files"] == ["harvest-open-lineage-events.ipynb"]
    assert "only owner" in (INBOX / "OpenLineage Events" / "README.md").read_text()


def _cells():
    nb = json.loads(NOTEBOOK.read_text())
    return ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]


def test_notebook_skips_when_any_openlineage_topic_exists():
    code = "\n".join(_cells())
    # the guard: any active Topic whose display name is exactly openlineage.events, whatever its QN
    assert 'get_elements_by_property_value(\n        TOPIC_DISPLAY_NAME, ["displayName"], metadata_element_type="Topic"' in code
    assert "starts_with=False, ends_with=False, ignore_case=False" in code
    assert "already_connected = bool(topics)" in code
    assert "already catalogued as {qualified_name} ({guid}); skipping" in code
    # the process that creates the topic only starts when none exists
    start = code.index("instance_guid = automated_curation.initiate_gov_action_process")
    guard = code.rindex("if already_connected:", 0, start)
    assert guard < start and "nothing is created" in code[guard:start]
