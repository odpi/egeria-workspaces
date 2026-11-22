"""A StatementOfApplicability must get a "View →" button wherever another Explorer screen lists one
(governance-control ControlApplicability links, a CertificationType's governed elements, an
Organization's scoped elements, Folio members, search results), and other apps must route it to the
Explorer section. Its supertypes are only AuthoredReferenceable/Referenceable/OpenMetadataRoot, so no
generic fallback in _elementIsLinkable catches it; PO-23 was the missing entry.

The _elementIsLinkable check runs the real function under node with its helper tables stubbed; it is
skipped when node is not installed (the container has none). The other checks are static."""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

_DIR = Path(__file__).resolve().parent.parent
HTML = (_DIR / "type-explorer.html").read_text()
NAV_MAP = json.loads((_DIR / "static" / "type-nav-map.json").read_text())

SOA_SUPERS = ["AuthoredReferenceable", "Referenceable", "OpenMetadataRoot"]   # live 6.3 shape


def _linkable(item):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    m = re.search(r"function _elementIsLinkable\(item\) \{.*?\n\}\n", HTML, re.S)
    assert m, "_elementIsLinkable not found in type-explorer.html"
    stubs = ("var EXT_REF_TYPES = [], AGREEMENT_TYPES = [], DD_TYPES_SET = {};\n"
             "function _actorKindForType() { return null; }\n")
    out = subprocess.run([node, "-e", stubs + m.group(0) + f"\nconsole.log(JSON.stringify(_elementIsLinkable({json.dumps(item)})));"],
                         capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_soa_is_linkable_with_and_without_supertypes():
    assert _linkable({"typeName": "StatementOfApplicability", "superTypeNames": SOA_SUPERS}) is True
    assert _linkable({"typeName": "StatementOfApplicability"}) is True      # some serializers omit them


def test_plain_referenceable_is_still_not_linkable():
    assert _linkable({"typeName": "Referenceable", "superTypeNames": ["OpenMetadataRoot"]}) is False


def test_dispatcher_routes_soa_to_its_section():
    assert "if (typeName === 'StatementOfApplicability') { onNavigateToSoa(guid); return; }" in HTML
    assert "setSection('statements-of-applicability')" in HTML


def test_type_nav_map_routes_soa_to_explorer():
    assert NAV_MAP["StatementOfApplicability"] == {"explorerHash": "statements-of-applicability"}
    # the hash must be one the Explorer accepts
    assert "'statements-of-applicability'" in HTML[HTML.index("new Set(["):]
