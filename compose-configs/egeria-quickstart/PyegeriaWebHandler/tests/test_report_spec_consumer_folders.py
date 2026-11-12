"""Report-spec consumer folders, phase 1: the Dr.Egeria document, and the Portal surviving the rename.

The Portal folder `ReportSpecFolder::EgeriaPortal` (fe5aad27) is renamed in place to
`ReportSpecFolder::Consumer::Portal` (egeria-held-specs/REPORT_SPEC_CONSUMER_FOLDERS.dr-egeria.md).
For the phase 1 deploy the Portal's default PYEGERIA_REPORT_SPEC_FOLDERS listed both names, so the
rename and the deploy could land in either order; the rename ran on 2026-11-10 and phase 2 drops
the old name. The sync tests run pyegeria's own sync_report_specs against an in-memory Egeria. No
Egeria call is made.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402

from pyegeria.view import egeria_spec_cache as esc  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
DOC = HERE / "egeria-held-specs" / "REPORT_SPEC_CONSUMER_FOLDERS.dr-egeria.md"
SPECS_DOC = HERE / "egeria-held-specs" / "PORTAL_REPORT_SPECS.dr-egeria.md"
COMPOSE = HERE.parent / "egeria-quickstart.yaml"

ROOT = "RootCollection::ReportSpecs"
OLD, NEW = "ReportSpecFolder::EgeriaPortal", "ReportSpecFolder::Consumer::Portal"
PORTAL_GUID = "fe5aad27-1587-4d4e-a7c0-ab806650a6e2"
CONSUMERS = [NEW] + [f"ReportSpecFolder::Consumer::{n}"
                     for n in ("EgeriaAdvisor", "ResourceExplorer", "Pyegeria", "MyEgeria", "Jupyter")]
LABEL = "Analytic - Generic Metric Trend"


def _blocks(path: Path) -> list[tuple[str, dict]]:
    """Each `## <command>` block as (command, {attribute: value})."""
    out = []
    for block in path.read_text().split("\n## ")[1:]:
        head, *rest = block.split("\n### ")
        attrs = {}
        for part in rest:
            name, _, value = part.partition("\n")
            attrs[name.strip()] = re.split(r"\n___", value)[0].strip()
        out.append((head.splitlines()[0].strip(), attrs))
    return out


# ── The document ──

def test_document_builds_the_tree():
    blocks = _blocks(DOC)
    roots = [a for c, a in blocks if c == "Create Root Collection"]
    assert [(a["Qualified Name"], a["Display Name"]) for a in roots] == [(ROOT, "Report Specs")]
    folders = {a["Qualified Name"]: a for c, a in blocks if c == "Create Collection Folder"}
    assert sorted(folders) == sorted(CONSUMERS)
    # The rename is an in-place update of the existing element, picked by its GUID.
    assert folders[NEW]["GUID"] == PORTAL_GUID and folders[NEW]["Display Name"] == "Portal"
    assert [q for q, a in folders.items() if "GUID" in a] == [NEW]
    # Every element command names its Qualified Name, so a re-run finds it and updates in place.
    assert all(a.get("Qualified Name") for c, a in blocks if c.startswith("Create "))
    links = [a for c, a in blocks if c == "Add Member to Collection"]
    assert all(a["Collection Id"] == ROOT for a in links)
    assert sorted(a["Element Id"] for a in links) == sorted(CONSUMERS)


def test_document_never_uses_parent_id():
    """Dr.Egeria's Parent ID on an Update deletes an existing CollectionMembership it does not
    recognise (the Portal folder's spec memberships). The tree is linked by Add Member only, and
    nothing is anchored to the root."""
    for command, attrs in _blocks(DOC):
        assert not any(k.startswith("Parent") for k in attrs), command
        assert attrs.get("Make Anchor", "false").lower() == "false", command


def test_the_portal_spec_document_points_at_the_new_name():
    parents = [a["Parent ID"] for c, a in _blocks(SPECS_DOC) if c == "Create Report Spec"]
    assert parents == [NEW, NEW]


@pytest.mark.skipif(not COMPOSE.is_file(), reason="egeria-quickstart.yaml is not beside this checkout (a container's /app)")
def test_compose_default_is_the_consumer_folder_alone():
    """The rename is live (2026-11-10), so the old name is dropped: it would only add a
    "folder not found" line to every sync report."""
    line = next(l for l in COMPOSE.read_text().splitlines() if "PYEGERIA_REPORT_SPEC_FOLDERS:" in l)
    default = re.search(r":-([^}]*)}", line).group(1)
    assert [p.strip() for p in default.split(",")] == [NEW]


# ── The Portal across the rename (pyegeria's own sync, in-memory Egeria) ──

SPEC_GUID = "7e6b0cd2-0000-0000-0000-000000000000"


def _spec_element() -> dict:
    attrs = next(a for c, a in _blocks(SPECS_DOC) if c == "Create Report Spec" and a["Display Name"] == LABEL)
    return {"elementHeader": {"guid": SPEC_GUID,
                              "type": {"typeName": "ReportSpec", "superTypeNames": ["ReportType", "Collection"]},
                              "versions": {"version": 3}},
            "properties": {"qualifiedName": attrs["Qualified Name"], "displayName": attrs["Display Name"],
                           "purpose": attrs["Purpose"], "description": attrs["Description"],
                           "category": attrs["Category"], "contentStatus": attrs["Content Status"],
                           "microflow": attrs["Microflow"]}}


class _Egeria:
    """The Portal folder under one qualified name or the other, holding one spec."""

    def __init__(self, folder_qn: str):
        self.folder_qn = folder_qn
        self.user_id = "test"
        self.platform_url = "https://test:9443"
        self.view_server = "test-view"

    def get_collections_by_name(self, name, metadata_element_type=None, output_format=None):
        if name == self.folder_qn and metadata_element_type == "CollectionFolder":
            return [{"elementHeader": {"guid": PORTAL_GUID, "type": {"typeName": "CollectionFolder"}},
                     "properties": {"qualifiedName": self.folder_qn}}]
        return "No elements found"

    def get_collection_members(self, collection_guid=None, output_format=None, start_from=0, page_size=None, **_):
        # The spec sync pages member reads (pyegeria 6.2.36+). One spec on the first page, then an
        # empty page, which is how a reader knows it has them all (Egeria's paging contract).
        assert collection_guid == PORTAL_GUID
        return [_spec_element()] if not start_from else []

    def get_collection_by_guid(self, guid, output_format=None):
        assert guid == SPEC_GUID
        return _spec_element()


def _sync(tmp_path, folder_qn, folders):
    return esc.sync_report_specs(_Egeria(folder_qn), folders=folders, cache_dir=str(tmp_path))


def _manifest(tmp_path) -> dict:
    return json.loads(next(tmp_path.rglob("manifest.json")).read_text())


@pytest.fixture(autouse=True)
def _fresh_tier():
    yield
    esc._invalidate_tier()


def test_deploy_first_then_rename_keeps_the_spec(tmp_path):
    before = _sync(tmp_path, OLD, [NEW, OLD])          # deployed, folder not renamed yet
    assert before.added == [LABEL] and not before.pruned
    assert any(NEW in who for who, _ in before.skipped)
    after = _sync(tmp_path, NEW, [NEW, OLD])           # the rename has run
    assert after.unchanged == [LABEL] and not after.pruned and not after.added
    assert any(OLD in who for who, _ in after.skipped)
    entry = _manifest(tmp_path)["entries"][LABEL]
    assert entry["guid"] == SPEC_GUID and entry["folders"] == [NEW]


def test_rename_first_then_deploy_keeps_the_spec(tmp_path):
    _sync(tmp_path, OLD, [OLD])                        # today: old default, old name
    renamed = _sync(tmp_path, NEW, [NEW, OLD])         # renamed, then deployed with both names
    assert LABEL in renamed.added + renamed.unchanged and not renamed.pruned


def test_old_name_alone_after_the_rename_prunes(tmp_path):
    """Why the default carries both names: an old-name-only Portal after the rename finds no folder
    and prunes the spec (the Portal then falls back to its local copy, local_spec_fallback.py)."""
    _sync(tmp_path, OLD, [OLD])
    stale = _sync(tmp_path, NEW, [OLD])
    assert stale.pruned == [LABEL]
