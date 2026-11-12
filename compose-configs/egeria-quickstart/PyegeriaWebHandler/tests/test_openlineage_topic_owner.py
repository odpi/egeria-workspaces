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


def test_excludeReasons_is_ignored_by_discovery(monkeypatch, tmp_path):
    """bootstrap_batches reads known manifest keys only: the same folder with and without excludeReasons
    discovers the same batch, with no warning about the extra key."""
    def discover(manifest):
        root = tmp_path / ("with" if "excludeReasons" in manifest else "without")
        folder = root / "B"
        folder.mkdir(parents=True)
        (folder / "a.md").write_text("# a\n")
        (folder / "skip.md").write_text("# skip\n")
        (folder / "_batch.json").write_text(json.dumps(manifest))
        monkeypatch.setattr(bb, "_INBOX_ROOT", root)
        monkeypatch.setattr(bb, "_SCAN_ROOTS", [])
        monkeypatch.setenv("PYEGERIA_BOOTSTRAP_STORE", str(tmp_path / "selection.json"))
        found = [b for b in bb.discover_batches() if b["id"] == "B"]
        assert len(found) == 1
        return {k: v for k, v in found[0].items() if k != "path"}

    base = {"files": ["a.md"], "exclude": ["skip.md"], "canary": {"type": "Topic", "name": "x"}}
    plain = discover(base)
    extra = discover({**base, "excludeReasons": {"skip.md": "a reason"}})
    assert plain == extra
    assert extra["files"] == ["a.md"] and not [w for w in extra["warnings"] if "excludeReasons" in str(w)]


# ── The notebook's guard, run with a fake Egeria ──────────────────────────────

def _guard(answer):
    """Run the guard's definitions from the notebook's topic-check cell against a fake metadata_expert whose
    find returns (or raises) `answer`; return check_topics()."""
    import ast
    cell = next(c for c in _cells() if "def check_topics" in c)
    tree = ast.parse(cell)
    keep = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ("find_topics", "check_topics")
            or isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) in ("TOPIC_DISPLAY_NAME", "NO_ELEMENTS_FOUND")]

    class FakeExpert:
        def __init__(self): self.bodies = []
        def find_metadata_elements(self, body):
            self.bodies.append(body)
            if isinstance(answer, BaseException):
                raise answer
            return answer

    ns = {"metadata_expert": FakeExpert()}
    exec(compile(ast.Module(body=keep, type_ignores=[]), "cell", "exec"), ns)
    state = ns["check_topics"]()
    body = ns["metadata_expert"].bodies[0]
    cond = body["searchProperties"]["conditions"][0]
    assert body["metadataElementTypeName"] == "Topic" and cond["property"] == "displayName"
    assert cond["operator"] == "EQ" and cond["value"]["primitiveValue"] == "openlineage.events"
    assert body["graphQueryDepth"] == 0 and body["limitResultsByStatus"] == ["ACTIVE"]
    return state


# The shape find_metadata_elements returned read-only on laz, 2026-11-12, after the cleanup.
LAZ_TOPIC = {"elementGUID": "00daa9fb-11b7-409d-9ee2-1602ea0aff42", "status": "ACTIVE",
             "elementProperties": {"propertyValueMap": {"qualifiedName": {
                 "class": "PrimitiveTypePropertyValue", "typeName": "string",
                 "primitiveValue": "Topic::LocalKafka2.openlineage.events::inOut"}}}}


def test_guard_catalogued_names_the_topic():
    assert _guard([LAZ_TOPIC]) == ("catalogued", [("Topic::LocalKafka2.openlineage.events::inOut",
                                                   "00daa9fb-11b7-409d-9ee2-1602ea0aff42")])


def test_guard_only_no_elements_found_means_none():
    assert _guard("No elements found") == ("none", [])


@pytest.mark.parametrize("answer", [None, "", [], "Some other message", {"elements": []}, 0,
                                    ConnectionError("platform down"), TimeoutError("read timed out")])
def test_guard_any_other_answer_is_not_read(answer):
    state, reason = _guard(answer)
    assert state == "not read" and reason


def test_notebook_creates_nothing_unless_the_answer_is_none():
    code = "\n".join(_cells())
    assert "get_elements_by_property_value" not in code        # the by-exact-property-value endpoint timed out on laz
    assert 'create_blocked = topic_state != "none"' in code
    assert 'already_connected = topic_state == "catalogued"' in code
    assert "Could not read whether {TOPIC_DISPLAY_NAME} is catalogued ({topic_detail}); not creating one." in code
    assert "already catalogued as {qualified_name} ({guid}); skipping" in code
    # the process that creates the topic only starts past both guards
    start = code.index("instance_guid = automated_curation.initiate_gov_action_process")
    first = code.rindex("if already_connected:", 0, start)
    blocked = code.index("elif create_blocked:", first)
    assert first < blocked < start and "nothing is created" in code[blocked:start]
    # the tables wait is skipped too
    wait = code.index("tables_catalogued = already_connected")
    assert code.index("if create_blocked:", wait) < code.index("while True:", wait)
