"""LD-3: Dashboard Sheets held in Egeria dashboard folders (pyegeria 6.2.34 LD-1), on the Local Dashboards page.

The list says where each sheet came from (local file, or the Egeria folders it was found in) and who uses it
("Used by", from pyegeria's dashboard consumer index), and absence is worded: no folders configured, a folder
not found or not visible, a read that failed -- never an empty list passed off as "no sheets". Egeria is faked.
"""
import json
import re
import shutil
import subprocess
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402

import local_dashboards_handler as ld  # noqa: E402
from test_local_dashboards_sources import _pl, _sheet, env  # noqa: E402,F401  (env is the shared fixture)

DIR = Path(__file__).resolve().parent.parent
HTML = (DIR / "local-dashboards.html").read_text()
PORTAL = "DashboardFolder::Consumer::Portal"


class _Listing(list):
    def __init__(self, sheets, notes=(), folders=()):
        super().__init__(sheets)
        self.notes, self.folders = list(notes), list(folders)


@pytest.fixture
def ld3(env, monkeypatch):
    """The shared fake, plus LD-1's listing shape, configured folders and a consumer index."""
    monkeypatch.setenv("PYEGERIA_DASHBOARD_FOLDERS", PORTAL)
    mod = sys.modules["pyegeria.view.dashboards"]
    env.update(notes=[], folders=[{"qualifiedName": PORTAL, "status": "read", "reason": None, "sheets": 0}],
               index={"status": "read", "reason": None, "root": "RootCollection::DashboardSheets",
                      "consumers": [{"name": "Portal", "status": "read", "sheets": 1},
                                    {"name": "EgeriaAdvisor", "status": "read", "sheets": 1}], "index": {}},
               index_calls=0, index_fail=None)
    plain = mod.list_dashboard_sheets

    def listing(client):
        return _Listing(plain(client), env["notes"], env["folders"])

    def index(client):
        env["index_calls"] += 1
        if env["index_fail"]:
            raise env["index_fail"]
        return env["index"]
    mod.list_dashboard_sheets = listing
    mod.read_dashboard_consumer_index = index
    mod.configured_dashboard_folders = lambda: [p for p in (ld.os.getenv("PYEGERIA_DASHBOARD_FOLDERS") or "").split(",") if p]
    return env


def _eg(name, folders=(), used_by=()):
    return _sheet(name, [_pl("Rep")], source="egeria", breaks=[], folders=list(folders), used_by=list(used_by))


def _rows(env):
    body = env["client"].get("/api/local-dashboards").json()
    return body, {s["name"]: s for s in body["sheets"]}


def test_sheets_carry_their_source_folders_and_used_by(ld3):
    ld3["egeria"] = {"shared": _eg("shared", [PORTAL], ["Portal"]), "portal-only": _eg("portal-only", [PORTAL], ["Portal"])}
    ld3["index"]["index"] = {"shared": ["EgeriaAdvisor", "Portal"], "portal-only": ["Portal"]}
    body, by = _rows(ld3)
    assert by["shared"]["source"] == "egeria" and by["shared"]["folders"] == [PORTAL]
    assert by["shared"]["usedBy"] == ["EgeriaAdvisor", "Portal"] and by["shared"]["usedByState"] == "read"
    assert by["portal-only"]["usedBy"] == ["Portal"]
    assert body["egeria"]["configuredFolders"] == [PORTAL] and body["egeria"]["folders"][0]["status"] == "read"
    assert body["consumers"]["status"] == "read" and {c["name"] for c in body["consumers"]["consumers"]} == {"Portal", "EgeriaAdvisor"}


def test_local_file_sheets_are_not_tracked_never_used_by_none(ld3):
    _, by = _rows(ld3)
    j = by["json-only"]
    assert j["source"] == "local file" and j["folders"] == []
    assert j["usedBy"] is None and j["usedByState"] == "not tracked"


def test_folder_not_found_is_said_and_never_an_empty_egeria_list(ld3):
    # Today's live case: the folder is not seeded yet (LD-2).
    ld3["egeria"] = {}
    reason = f"not found, or not visible to erinoverview"
    ld3["folders"] = [{"qualifiedName": PORTAL, "status": "not found", "reason": reason, "sheets": 0}]
    ld3["notes"] = [f"{PORTAL}: {reason}"]
    body, by = _rows(ld3)
    assert body["egeria"]["available"] is True
    assert body["egeria"]["folders"] == [{"qualifiedName": PORTAL, "status": "not found", "reason": reason, "sheets": 0}]
    assert body["egeria"]["notes"] == [f"{PORTAL}: {reason}"]
    assert set(by) == {"json-only", "twin"}           # the local file still answers


def test_no_folders_configured_is_reported_as_unscoped(ld3, monkeypatch):
    monkeypatch.setenv("PYEGERIA_DASHBOARD_FOLDERS", "")
    ld3["folders"], ld3["notes"] = [], ["no dashboard folders configured: listing every Dashboard:: sheet"]
    body, _ = _rows(ld3)
    assert body["egeria"]["configuredFolders"] == [] and body["egeria"]["notes"]


def test_egeria_read_failure_keeps_the_configured_folders_and_says_so(ld3):
    ld3["fail"] = ConnectionError("platform down")
    body, by = _rows(ld3)
    assert body["egeria"]["available"] is False and "platform down" in body["egeria"]["error"]
    assert body["egeria"]["configuredFolders"] == [PORTAL]
    assert body["consumers"]["status"] == "not read" and ld3["index_calls"] == 0


def test_index_not_read_is_unknown_and_falls_back_to_the_folder_it_was_found_in(ld3):
    ld3["egeria"] = {"in-portal": _eg("in-portal", [PORTAL], ["Portal"]), "unscoped": _eg("unscoped")}
    ld3["index"] = {"status": "not read", "reason": "the root RootCollection::DashboardSheets was not found, "
                    "or is not visible to erinoverview", "consumers": [], "index": {}}
    body, by = _rows(ld3)
    assert by["unscoped"]["usedBy"] is None and by["unscoped"]["usedByState"] == "not read"
    assert "was not found" in by["unscoped"]["usedByReason"]
    assert by["in-portal"]["usedBy"] == ["Portal"] and by["in-portal"]["usedByState"] == "partial"
    assert body["consumers"]["status"] == "not read"


def test_index_read_and_in_no_consumer_folder_is_an_empty_list(ld3):
    ld3["egeria"] = {"lonely": _eg("lonely")}
    _, by = _rows(ld3)
    assert by["lonely"]["usedBy"] == [] and by["lonely"]["usedByState"] == "read"


def test_index_failure_is_not_cached_and_a_clean_read_is(ld3):
    ld3["egeria"] = {"e": _eg("e")}
    ld3["index_fail"] = ConnectionError("blip")
    _, by = _rows(ld3)
    assert by["e"]["usedByState"] == "not read" and "blip" in by["e"]["usedByReason"]
    ld3["index_fail"] = None
    _rows(ld3)
    _rows(ld3)
    assert ld3["index_calls"] == 2                     # failed once (not cached), then read once and cached


def test_root_not_found_is_cached_like_a_clean_answer(ld3):
    ld3["index"] = {"status": "not read", "reason": "the root X was not found, or is not visible to erin",
                    "consumers": [], "index": {}}
    _rows(ld3); _rows(ld3)
    assert ld3["index_calls"] == 1


def test_a_sheet_outside_the_folders_still_opens_by_name(ld3):
    # The cached list is folder-scoped: a name missing from it is not "Egeria does not hold it".
    ld3["egeria"] = {"in-portal": _eg("in-portal", [PORTAL], ["Portal"]), "elsewhere": _eg("elsewhere")}
    mod = sys.modules["pyegeria.view.dashboards"]
    full = mod.list_dashboard_sheets
    mod.list_dashboard_sheets = lambda client: _Listing([ld3["egeria"]["in-portal"]])
    _, by = _rows(ld3)
    assert "elsewhere" not in by
    d = ld3["client"].get("/api/local-dashboards/elsewhere")
    assert d.status_code == 200 and d.json()["source"] == "egeria" and ld3["loads"] >= 1
    mod.list_dashboard_sheets = full


def test_compose_sets_the_portal_dashboard_folder_and_lets_empty_mean_unscoped():
    path = DIR.parent / "egeria-quickstart.yaml"
    if not path.exists():
        pytest.skip("the compose file is not beside this copy of the handler")
    yaml = path.read_text()
    assert 'PYEGERIA_DASHBOARD_FOLDERS: "${PYEGERIA_DASHBOARD_FOLDERS-DashboardFolder::Consumer::Portal}"' in yaml


# ── the page ─────────────────────────────────────────────────────────────────

def _call(fn, *args, extra=()):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    src = ""
    for name in (fn,) + tuple(extra):
        m = re.search(r"function " + name + r"\(.*?\n\}\n", HTML, re.S)
        assert m, f"{name} not found"
        src += m.group(0)
    js = ("function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\"/g,'&quot;');}"
          + src + f"console.log(JSON.stringify({fn}(...{json.dumps(list(args))})));")
    out = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


SHEETS = [{"name": "a", "source": "egeria", "usedBy": ["Portal"]},
          {"name": "b", "source": "egeria", "usedBy": []},
          {"name": "c", "source": "egeria", "usedBy": None},
          {"name": "d", "source": "local file", "usedBy": None}]


def test_filter_by_source_and_consumer():
    names = lambda f: [s["name"] for s in _call("filterSheets", SHEETS, f)]
    assert names({}) == ["a", "b", "c", "d"]
    assert names({"source": "egeria"}) == ["a", "b", "c"] and names({"source": "local file"}) == ["d"]
    assert names({"usedBy": "Portal"}) == ["a"]
    assert names({"usedBy": "__none__"}) == ["b"]          # read, in no consumer folder
    assert names({"usedBy": "__unknown__"}) == ["c"]       # never counted as "none"


def test_folder_note_words():
    none = _call("folderNote", {"available": True, "configuredFolders": []})
    assert "No dashboard folders are configured" in none and "every Dashboard Sheet held in Egeria" in none
    nf = _call("folderNote", {"available": True, "configuredFolders": [PORTAL],
                              "folders": [{"qualifiedName": PORTAL, "status": "not found", "reason": "not visible to erin"}]})
    assert "was not found, or is not visible to you" in nf and 'unknown, not "none"' in nf and "src-note" in nf
    nr = _call("folderNote", {"available": True, "configuredFolders": [PORTAL],
                              "folders": [{"qualifiedName": PORTAL, "status": "not read", "reason": "boom"}]})
    assert "could not be read" in nr
    ok = _call("folderNote", {"available": True, "configuredFolders": [PORTAL],
                              "folders": [{"qualifiedName": PORTAL, "status": "read"}]})
    assert "src-info" in ok and "not found" not in ok
    assert _call("folderNote", {"available": False}) == ""   # egeriaNote already says Egeria could not be read


def test_used_by_line_never_says_none_for_unknown():
    assert _call("usedByLine", {"usedByState": "not tracked"}) == ""
    assert "not read" in _call("usedByLine", {"usedByState": "not read", "usedBy": None})
    assert "no consumer folder" in _call("usedByLine", {"usedByState": "read", "usedBy": []})
    line = _call("usedByLine", {"usedByState": "partial", "usedBy": ["Portal"], "usedByReason": "x"})
    assert "Portal" in line and "partly read" in line


def test_wiring():
    assert "egeriaNote(data.egeria) + folderNote(data.egeria)" in HTML
    assert "filterSheets(data.sheets, LIST_FILTER)" in HTML
    assert "usedByLine(s)" in HTML and "In Egeria folder" in HTML
    assert "the Egeria-held ones are unknown" in HTML
