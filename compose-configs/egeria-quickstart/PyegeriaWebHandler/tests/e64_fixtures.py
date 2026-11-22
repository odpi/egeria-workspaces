"""Egeria 6.4 element shapes for the e64 tests, with no live server.

laz's Egeria (6.4-SNAPSHOT, built 2026-11-21T19:52:59Z) holds no Decision or DataValue yet, and these tests
may not write to it. So the shapes are built from Egeria's own definitions at 90232870b2:
- OpenMetadataRootElement / AttributedMetadataElement: each 6.4 list is a list of RelatedMetadataElementSummary
  ({relationshipHeader, relationshipProperties, relatedElement});
- the property names and value kinds are the `.http` samples' (egeria-python tests/fixtures/egeria-6.4,
  Egeria-api-governance-officer.http createDecision / linkDecisionOutcome / linkAssessment), so importance
  and disposition are strings and implications is a list;
- Branch has no header key of its own in 6.4 (ElementHeader.java), so it arrives in otherClassifications.
"""


def client_error(status=404, url="https://egeria.test:9443/servers/qs-view-server/api/open-metadata/x"):
    """A real pyegeria PyegeriaClientException carrying a bare transport status (an endpoint that is not
    served answers HTTP 404 with no Egeria body)."""
    import httpx
    from pyegeria.core._exceptions import PyegeriaClientException
    return PyegeriaClientException(httpx.Response(status, request=httpx.Request("POST", url)))


def rel(rel_type, rel_guid, el_guid, el_type="GlossaryTerm", el_props=None, rel_props=None, super_types=None):
    return {
        "class": "RelatedMetadataElementSummary",
        "relationshipHeader": {"guid": rel_guid, "type": {"typeName": rel_type}},
        "relationshipProperties": {"class": f"{rel_type}Properties", **(rel_props or {})},
        "relatedElement": {
            "elementHeader": {"guid": el_guid, "type": {"typeName": el_type,
                                                        "superTypeNames": super_types or ["Referenceable"]}},
            "properties": {"qualifiedName": f"{el_type}::{el_guid}", **(el_props or {})},
        },
    }


DECISION_PROPS = {
    "class": "DecisionProperties",
    "qualifiedName": "Decision::Adopt open lineage",
    "identifier": "DEC-7",
    "displayName": "Adopt OpenLineage for pipelines",
    "description": "Pipelines report their runs as OpenLineage events.",
    "summary": "Use OpenLineage for all new pipelines.",
    "scope": "Data platform",
    "usage": "Pipeline design reviews",
    "importance": "High",
    "disposition": "Approved",
    "implications": ["Every pipeline needs an OpenLineage emitter", "Old pipelines migrate by Q3"],
    "notes": "Agreed at the architecture board.",
    "startTime": "2026-01-01T00:00:00.000+00:00",
    "lastReviewTime": "2026-06-01T00:00:00.000+00:00",
    "nextReviewTime": "2026-09-01T00:00:00.000+00:00",
    "expiryTime": "2027-01-01T00:00:00.000+00:00",
    "authors": ["Erin Overview"],
    "contentStatus": "ACTIVE",
}


def assessment(rel_guid, el_guid, name, label, when, **kw):
    return rel("Assessment", rel_guid, el_guid, el_props={"displayName": name},
               rel_props={"label": label, "assessmentTime": when, **kw})


def decision(guid="dec-1", assessments=None, outcomes=None, extra=None, props=None):
    el = {
        "class": "OpenMetadataRootElement",
        "elementHeader": {"guid": guid, "status": "ACTIVE",
                          "type": {"typeName": "Decision",
                                   "superTypeNames": ["AuthoredReferenceable", "Referenceable", "OpenMetadataRoot"]}},
        "properties": {**DECISION_PROPS, **(props or {})},
    }
    if assessments is not None:
        el["inputsToDecision"] = assessments
    if outcomes is not None:
        el["decisionOutcomes"] = outcomes
    el.update(extra or {})
    return el


TWO_ASSESSMENTS_ONE_ELEMENT = [
    assessment("as-1", "term-1", "Lineage", "Initial review", "2026-02-01T10:00:00.000+00:00",
               assessor="Erin Overview", assessorTypeName="Person", notes="Looks right"),
    assessment("as-2", "term-1", "Lineage", "Re-review", "2026-05-01T10:00:00.000+00:00",
               assessor="Lineage checker", assessorTypeName="SoftwareCapability", assessorPropertyName="score"),
    assessment("as-3", "term-2", "Pipelines", "Initial review", "2026-02-02T10:00:00.000+00:00"),
]

OUTCOMES = [
    rel("Outcome", "out-1", "proj-1", el_type="Project", el_props={"displayName": "OpenLineage rollout"},
        rel_props={"label": "Rollout", "importance": "High", "disposition": "Started"}),
]


class FakeExplorer:
    """Fake ClassificationExplorer: an /api/about answer, by-type pages and a get-by-guid result.

    `about` is the platform's /api/about JSON (or an Exception to raise: an unreadable version).
    `fail` is raised by every read; `pages` are served by start_from; `elements` by guid."""

    def __init__(self, about=None, pages=None, elements=None, fail=None, url="https://egeria.test:9443"):
        self.about, self.pages, self.elements, self.fail = about, pages or [], elements or {}, fail
        self.platform_url = url
        self.calls = []

    async def async_get_platform_origin(self):
        if isinstance(self.about, Exception):
            raise self.about
        import json
        return json.dumps(self.about) if isinstance(self.about, dict) else self.about

    async def _async_get_elements(self, metadata_element_type="Referenceable", start_from=0, page_size=10,
                                  output_format="JSON", **kw):
        self.calls.append(("by-type", metadata_element_type, start_from))
        if self.fail:
            raise self.fail
        i = start_from // page_size
        return self.pages[i] if i < len(self.pages) else "No elements found"

    async def _async_get_element_by_guid(self, guid, element_type_name=None, graph_query_depth=3, **kw):
        self.calls.append(("by-guid", guid, element_type_name, graph_query_depth))
        if self.fail:
            raise self.fail
        return self.elements.get(guid, "No elements found")


ABOUT_6_4 = {"version": "6.4-SNAPSHOT", "time": "2026-11-21T19:52:59.236Z"}
ABOUT_6_3 = {"version": "6.3", "time": "2026-11-16T12:00:00Z"}


# ── DataValue / LiteralDataValue (Egeria-api-data-engineer.http createDataValue, link* samples) ──────────

DATA_VALUE_PROPS = {
    "class": "LiteralDataValueProperties",
    "qualifiedName": "LiteralDataValue::retry-limits",
    "identifier": "DV-3",
    "displayName": "Retry limits",
    "description": "How often a pipeline step retries.",
    "dataFormat": "text/plain",
    "length": 3,
    "dataType": "string",
    "usage": "Pipeline configuration",
    "fingerprint": "ab12",
    "fingerprintAlgorithm": "sha-256",
    "hash": 12345,
    "hashAlgorithm": "murmur3",
}


def positioned(rel_type, rel_guid, el_guid, name, position=None, el_type="DataValue", **kw):
    rp = {"label": kw.pop("label", ""), **kw}
    if position is not None:
        rp["position"] = position
    return rel(rel_type, rel_guid, el_guid, el_type=el_type, el_props={"displayName": name}, rel_props=rp,
               super_types=kw.pop("super_types", None))


def data_value(guid="dv-1", literal=True, value=None, lists=None):
    props = {**DATA_VALUE_PROPS, **(value or {})}
    if not literal:
        props["class"] = "DataValueProperties"
    type_name = "LiteralDataValue" if literal else "DataValue"
    supers = (["DataValue"] if literal else []) + ["Referenceable", "OpenMetadataRoot"]
    el = {
        "class": "OpenMetadataRootElement",
        "elementHeader": {"guid": guid, "status": "ACTIVE", "type": {"typeName": type_name, "superTypeNames": supers}},
        "properties": props,
    }
    el.update(lists or {})
    return el


EMBEDDED = [
    positioned("EmbeddedDataValue", "emb-3", "dv-13", "Third", 3),
    positioned("EmbeddedDataValue", "emb-0", "dv-10", "Zero means unset", 0),
    positioned("EmbeddedDataValue", "emb-1", "dv-11", "First", 1),
    positioned("EmbeddedDataValue", "emb-n", "dv-19", "No position at all"),
]
USED_BY = [
    positioned("ProcessingVariable", "pv-2", "proc-1", "Nightly load", 2, el_type="Process", super_types=["Asset"]),
    positioned("ProcessingVariable", "pv-1", "proc-2", "Hourly load", 1, el_type="Process", super_types=["Asset"]),
]
STORED_IN = [rel("DataValueSource", "src-1", "file-1", el_type="CSVFile", el_props={"displayName": "limits.csv"},
                 super_types=["DataFile", "Asset"])]
PART_OF = [positioned("EmbeddedDataValue", "par-1", "dv-0", "All settings", 4)]
