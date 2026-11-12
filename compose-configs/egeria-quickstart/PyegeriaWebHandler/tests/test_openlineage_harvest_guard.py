"""The OpenLineage Events batch's notebook runs CreateAsCatalogTarget once (2026-11-12).

Under Egeria bug B5 (pageSize 1 -> "No elements found") the Portal's monitor read the canary topic as
missing and re-ran this notebook every pass: the listener 980b989c ended with 21 CatalogTargets on topic
00daa9fb. The notebook now skips when a Topic openlineage.events exists AND is already a catalog target
of the OpenLineageKafkaListener; only Egeria's own "No elements found" means none; anything else is
"not read" and it refuses, in words, creating nothing. Its finds ask for a page of 25, never 1.

The cells are run from the notebook's own source against fake clients; nothing talks to Egeria.
"""
import json
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent.parent
NOTEBOOK = (REPO / "exchange-quickstart" / "loading-bay" / "dr-egeria-inbox" / "OpenLineage Events"
            / "harvest-open-lineage-events.ipynb")
CELLS = ["".join(c["source"]) for c in json.loads(NOTEBOOK.read_text())["cells"] if c["cell_type"] == "code"]
GUARD = next(c for c in CELLS if "def check_listener" in c)
RUN = next(c for c in CELLS if "initiate_gov_action_process" in c)

NO = "No elements found"
LISTENER = "980b989c-de78-4e6a-a58d-51049d7381bf"
TOPIC = {"elementGUID": "00daa9fb-11b7-409d-9ee2-1602ea0aff42", "status": "ACTIVE",
         "elementProperties": {"propertyValueMap": {"qualifiedName": {
             "class": "PrimitiveTypePropertyValue", "typeName": "string",
             "primitiveValue": "Topic::LocalKafka2.openlineage.events::inOut"}}}}


def related(n):
    """A related-element-list envelope with n CatalogTarget links to the listener."""
    return {"class": "RelatedMetadataElementList", "elementList": [
        {"relationshipGUID": f"r{i}", "type": {"typeName": "CatalogTarget"},
         "element": {"elementGUID": LISTENER, "elementProperties": {"propertyValueMap": {
             "qualifiedName": {"primitiveValue": "OpenLineageKafkaListener"}}}}} for i in range(n)]}


class FakeExpert:
    """B5-faithful: a find or related read with page size 1 answers "No elements found"."""

    def __init__(self, topics=NO, targets=None, raise_find=None, raise_related=None):
        self.topics, self.targets = topics, targets or {}
        self.raise_find, self.raise_related = raise_find, raise_related
        self.calls = []

    def find_metadata_elements(self, body):
        self.calls.append(("find", body))
        if self.raise_find:
            raise self.raise_find
        return NO if body.get("pageSize") == 1 else self.topics

    def get_related_metadata_elements(self, guid, relationship_type, body, starting_at_end=0, start_from=0,
                                      page_size=500, **kw):
        self.calls.append(("related", guid, relationship_type, starting_at_end, page_size))
        if self.raise_related:
            raise self.raise_related
        return NO if page_size == 1 else self.targets.get(guid, NO)


def run_guard(expert):
    ns = {"metadata_expert": expert}
    exec(compile(GUARD, "guard-cell", "exec"), ns)
    return ns


def test_connected_topic_is_skipped_and_finds_ask_for_25():
    expert = FakeExpert([TOPIC], {TOPIC["elementGUID"]: related(1)})
    ns = run_guard(expert)
    assert ns["listener_state"] == "connected"
    assert ns["listener_detail"] == [("Topic::LocalKafka2.openlineage.events::inOut", TOPIC["elementGUID"], 1)]
    find = expert.calls[0][1]
    assert find["pageSize"] == 25 and find["metadataElementTypeName"] == "Topic"
    cond = find["searchProperties"]["conditions"][0]
    assert cond["property"] == "displayName" and cond["operator"] == "EQ"
    assert cond["value"]["primitiveValue"] == "openlineage.events"
    assert expert.calls[1] == ("related", TOPIC["elementGUID"], "CatalogTarget", 2, 25)


def test_the_21_duplicates_are_said(capsys):
    ns = run_guard(FakeExpert([TOPIC], {TOPIC["elementGUID"]: related(21)}))
    assert ns["listener_state"] == "connected" and ns["listener_detail"][0][2] == 21
    assert "21 times: duplicates to clean up" in capsys.readouterr().out


def test_no_topic_means_create():
    ns = run_guard(FakeExpert(NO))
    assert ns["listener_state"] == "none" and ns["listener_detail"] == "no Topic named openlineage.events"


def test_a_topic_that_is_not_a_catalog_target_means_create():
    ns = run_guard(FakeExpert([TOPIC], {}))
    assert ns["listener_state"] == "none"
    assert "exists (Topic::LocalKafka2.openlineage.events::inOut) but is not a catalog target" in ns["listener_detail"]


def test_a_topic_linked_to_another_connector_is_not_connected():
    other = {"elementList": [{"element": {"elementGUID": "aaaa", "elementProperties": {"propertyValueMap": {
        "qualifiedName": {"primitiveValue": "SomeOtherCataloguer"}}}}}]}
    assert run_guard(FakeExpert([TOPIC], {TOPIC["elementGUID"]: other}))["listener_state"] == "none"


@pytest.mark.parametrize("expert", [
    FakeExpert(None), FakeExpert(""), FakeExpert([]), FakeExpert("Some other message"), FakeExpert({"elements": []}),
    FakeExpert(raise_find=ConnectionError("platform down")),
    FakeExpert([{"no": "guid"}]),
    FakeExpert([TOPIC], raise_related=TimeoutError("read timed out")),
    FakeExpert([TOPIC], {TOPIC["elementGUID"]: "Unexpected text"}),
], ids=["None", "empty-string", "empty-list", "other-string", "dict", "find-error", "no-guid",
        "related-error", "related-odd-string"])
def test_anything_else_is_not_read_and_refuses_in_words(expert):
    with pytest.raises(RuntimeError) as exc:
        run_guard(expert)
    assert str(exc.value).startswith("Could not read whether openlineage.events is already a catalog target of "
                                     "OpenLineageKafkaListener (")
    assert str(exc.value).endswith("); not creating one.")


class FakeCuration:
    def __init__(self):
        self.started = []

    def initiate_gov_action_process(self, *args):
        self.started.append(args)
        return "process-guid"


@pytest.mark.parametrize("state,starts", [("none", 1), ("connected", 0), ("not read", 0)])
def test_the_process_starts_only_when_the_guard_says_none(state, starts):
    import os
    curation = FakeCuration()
    exec(compile(RUN, "run-cell", "exec"), {"listener_state": state, "automated_curation": curation, "os": os})
    assert len(curation.started) == starts
    if starts:
        assert curation.started[0][0] == "HarvestOpenLineageEvents::CreateAsCatalogTargetGovernanceActionProcess"


def test_no_page_size_1_anywhere_in_the_notebook():
    assert "PAGE_SIZE = 25" in GUARD
    for cell in CELLS:
        assert '"pageSize": 1' not in cell and "page_size=1" not in cell
