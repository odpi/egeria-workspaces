"""static/egeria-table.js: the shared renderer for pyegeria's structured TABLE (P1a).

BRIEF-P1-PORTAL-STRUCTURED-TABLE-2026-11-12 / DESIGN-REPORT-SPEC-COMPLEX-VALUES-RENDERING-2026-11-11 §2.2-2.5.
Real-shape fixtures: tests/fixtures/structured_table_laz_2026_11_12.json, captured read-only on laz
(pyegeria 6.2.39, table_shape="structured") from the CDO sheet's specs: Risk, Governance Metric, Project,
Digital-Products, Collections. kv and subtable do not occur in them, so those use synthetic results in the
same shape as pyegeria's structured_table.py.

Runs under node (tests/egeria_table_harness.js); skipped when node is not installed (the Portal container
has none): run on the host with `uvx pytest --noconftest`.
"""
import json
import re
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
MODULE = HERE.parent / "static" / "egeria-table.js"
HARNESS = HERE / "egeria_table_harness.js"
LAZ = json.loads((HERE / "fixtures" / "structured_table_laz_2026_11_12.json").read_text())
NO_LINK = "No link: this page gave the table no link builder."


def _node(req):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    out = subprocess.run([node, str(HARNESS), str(MODULE)], input=json.dumps(req), capture_output=True,
                         text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    res = json.loads(out.stdout)
    assert res.pop("ok"), res.get("error")
    return res


def html(result, link=False):
    return _node({"op": "html", "result": result, "link": link})["html"]


class Tree(HTMLParser):
    """A minimal element tree: enough to count rows/cells and read a cell's markup."""

    VOID = {"br", "col", "img", "input", "hr", "meta", "link"}

    def __init__(self, src):
        super().__init__(convert_charrefs=True)
        self.root = {"tag": "root", "attrs": {}, "kids": [], "text": ""}
        self.stack = [self.root]
        self.feed(src)

    def handle_starttag(self, tag, attrs):
        node = {"tag": tag, "attrs": dict(attrs), "kids": [], "text": ""}
        self.stack[-1]["kids"].append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i]["tag"] == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1]["kids"].append(data)


def find(node, tag, cls=None):
    out = []
    for k in node["kids"]:
        if isinstance(k, dict):
            if k["tag"] == tag and (cls is None or cls in (k["attrs"].get("class") or "").split()):
                out.append(k)
            out += find(k, tag, cls)
    return out


def text(node):
    return "".join(k if isinstance(k, str) else text(k) for k in node["kids"])


def main_table(src):
    tables = find(Tree(src).root, "table", "et-table")
    return tables[0]


def body_rows(src):
    """The main table's data rows (not the hidden subtable rows)."""
    t = main_table(src)
    tbody = [k for k in t["kids"] if isinstance(k, dict) and k["tag"] == "tbody"][0]
    rows = [k for k in tbody["kids"] if isinstance(k, dict) and k["tag"] == "tr"]
    return [r for r in rows if "et-sub" not in (r["attrs"].get("class") or "")], \
           [r for r in rows if "et-sub" in (r["attrs"].get("class") or "")]


def cells(row):
    return [k for k in row["kids"] if isinstance(k, dict) and k["tag"] == "td"]


def col_index(result, key):
    return [c["key"] for c in result["columns"]].index(key)


def footer(src):
    foot = find(Tree(src).root, "div", "et-foot")[-1]
    count = text(find(foot, "div", "et-count")[0])
    notes = [text(li) for li in find(foot, "li")]
    return count, notes


# ── The laz fixtures ──────────────────────────────────────────────────────────

SPECS = [k for k in LAZ if not k.startswith("_")]


@pytest.mark.parametrize("spec", SPECS)
def test_every_laz_result_renders_every_row_and_column(spec):
    r = LAZ[spec]
    src = html(r)
    heads = find(main_table(src), "th")
    assert [text(h) for h in heads] == [c["name"] for c in r["columns"]]   # the author's order, no column cap
    rows, _ = body_rows(src)
    assert len(rows) == len(r["rows"])
    assert all(len(cells(row)) == len(r["columns"]) for row in rows)
    assert "more columns" not in src and "+20" not in src
    count, notes = footer(src)
    for n in r["notes"]:
        assert n in notes                                                  # every pyegeria note is shown
    assert re.search(r"\d", count) and not count.startswith("All")          # one page is never "All N of N"
    assert "more may exist" in count or "Egeria doesn't promise it is the last" in count   # never a bare N


def test_risk_implications_are_bullets_and_description_is_clamped():
    r = LAZ["Risk-DrE-Basic"]
    rows, _ = body_rows(html(r))
    impl = cells(rows[0])[col_index(r, "implications")]
    items = find(impl, "li")
    expected = r["rows"][0]["implications"]
    assert find(impl, "ul", "et-bullets") and len(items) == min(len(expected), 10)
    assert text(items[0]) == expected[0]                                   # one sentence per item, commas kept
    desc = cells(rows[0])[col_index(r, "description")]
    box = find(desc, "div", "et-clamp")[0]
    assert "-webkit-line-clamp:3" in box["attrs"]["style"] and box["attrs"]["data-et-lines"] == "3"
    assert [text(b) for b in find(desc, "button")] == ["more"]
    assert "**Likelihood:**" in text(box)                                  # markdown is not interpreted


def test_metric_measurement_keeps_its_line_breaks_and_is_clamped():
    r = LAZ["Governance-Metric-DrE-Basic"]
    i = col_index(r, "measurement")
    row = next(n for n, x in enumerate(r["rows"]) if "\n" in (x.get("measurement") or ""))
    rows, _ = body_rows(html(r))
    box = find(cells(rows[row])[i], "div", "et-text")[0]
    assert "et-clamp" in box["attrs"]["class"]
    assert text(box) == r["rows"][row]["measurement"]                      # the newline is kept (pre-line)


def test_digital_products_elements_none_and_footer():
    r = LAZ["Digital-Products"]
    src = html(r)
    rows, _ = body_rows(src)
    used_by = col_index(r, "used_by_digital_products")
    first = r["rows"][0]["used_by_digital_products"]
    spans = [s for s in find(cells(rows[0])[used_by], "span") if s["attrs"].get("title")]
    assert [text(s) for s in spans][:len(first)] == [e["displayName"] for e in first][:10]
    assert spans[0]["attrs"]["title"].startswith(first[0]["qualifiedName"]) and NO_LINK in spans[0]["attrs"]["title"]
    uses = col_index(r, "uses_digital_products")
    assert text(cells(rows[2])[uses]) == "none"                            # [] = read, and none
    count, notes = footer(src)
    assert count == "78 rows (one page; Egeria doesn't promise it is the last)."   # never "All" on one page
    assert "Uses Products: none on 55 rows (read at graph depth 3)." in notes


def test_digital_products_links_with_a_link_builder():
    r = LAZ["Digital-Products"]
    rows, _ = body_rows(html(r, link=True))
    cell = cells(rows[0])[col_index(r, "used_by_digital_products")]
    a = find(cell, "a")[0]
    first = r["rows"][0]["used_by_digital_products"][0]
    assert a["attrs"]["href"] == "/egeria-explorer?guid=" + first["guid"]
    assert a["attrs"]["title"] == first["qualifiedName"] and text(a) == first["displayName"]
    assert NO_LINK not in html(r, link=True)


def test_collections_count_column_and_more_may_exist():
    r = LAZ["Collections"]
    src = html(r)
    rows, _ = body_rows(src)
    i = col_index(r, "collection_members")
    assert r["columns"][i]["render"] == "count"
    members = r["rows"][0]["collection_members"]
    span = find(cells(rows[0])[i], "span")[0]
    assert text(span) == str(len(members))
    names = [e["displayName"] for e in members]
    assert span["attrs"]["title"] == ", ".join(names[:10]) + f", +{len(names) - 10} more"
    count, notes = footer(src)
    assert count == "First 100; more may exist."
    assert any("more may exist" in n for n in notes)


# ── Render kinds on synthetic results (pyegeria's shapes) ─────────────────────

def col(key, render, **kw):
    return {"key": key, "name": kw.pop("name", key.title()), "type": kw.pop("type", "scalar"), "render": render,
            "detail_spec": kw.pop("detail_spec", None), "valid_values": None,
            "max_items": kw.pop("max_items", None), "max_lines": kw.pop("max_lines", None), **kw}


def table(columns, rows, total=None, shown=None, notes=None, basis="one page"):
    return {"kind": "table", "columns": columns, "rows": rows, "total": len(rows) if total == "n" else total,
            "total_basis": basis, "shown": len(rows) if shown is None else shown, "notes": notes or []}


def el(n):
    return {"guid": f"g-{n}", "qualifiedName": f"QN::{n}", "displayName": f"Name {n}", "type": "Asset"}


def test_join_past_max_items_names_the_rest():
    r = table([col("m", "join", type="elements")], [{"m": [el(i) for i in range(13)]}], total="n")
    cell = cells(body_rows(html(r))[0][0])[0]
    det = find(cell, "details", "et-rest")[0]
    assert text(find(det, "summary")[0]) == "+3 more"
    assert "Name 10" in text(det) and "Name 12" in text(det) and "Name 9" not in text(det)
    assert text(cell).startswith("Name 0, Name 1")


def test_join_respects_the_columns_max_items_and_label():
    r = table([col("m", "join", type="elements", max_items=2, label="qualifiedName")],
              [{"m": [el(1), el(2), el(3)]}], total="n")
    cell = cells(body_rows(html(r))[0][0])[0]
    assert text(cell).startswith("QN::1, QN::2") and text(find(cell, "summary")[0]) == "+1 more"


def test_bullets_past_max_items_are_expandable_not_dropped():
    r = table([col("b", "bullets", type="list")], [{"b": [f"item {i}" for i in range(12)]}], total="n")
    cell = cells(body_rows(html(r))[0][0])[0]
    assert len(find(cell, "li")) == 12 and text(find(cell, "summary")[0]) == "+2 more"


def test_kv_is_a_mini_table_and_a_nested_object_is_reduced():
    r = table([col("p", "kv", type="map")],
              [{"p": {"owner": "Erin", "count": 0, "flag": False, "deep": {"a": 1}, "tags": ["x", "y"]}}], total="n")
    src = html(r)
    kv = find(cells(body_rows(src)[0][0])[0], "table", "et-kv")[0]
    assert "data-no-col-resize" in kv["attrs"]
    pairs = [[text(td) for td in cells(tr)] for tr in find(kv, "tr")]
    assert ["owner", "Erin"] in pairs and ["count", "0"] in pairs and ["flag", "false"] in pairs
    assert ["tags", "x, y"] in pairs and ["deep", "1: (unnamed)"] in pairs
    assert any("P · deep holds a third level" in n for n in footer(src)[1])


def test_subtable_opens_under_the_row_with_the_sub_rows_keys():
    sub = [{"Name": "Step 1", "Status": "done", "Owner": {"guid": "g-o", "displayName": "Erin"}},
           {"Name": "Step 2", "Status": "open", "Owner": None, "Tags": ["a", "b"]}]
    r = table([col("display_name", "text", name="Display Name"),
               col("steps", "subtable", type="table", detail_spec="Steps-Basic")],
              [{"display_name": "Plan A", "steps": sub}], total="n")
    src = html(r)
    rows, subrows = body_rows(src)
    btn = find(cells(rows[0])[1], "button")[0]
    assert text(btn) == "▸ 2 rows" and btn["attrs"]["aria-expanded"] == "false"
    assert len(subrows) == 1 and "hidden" in subrows[0]["attrs"]
    assert subrows[0]["attrs"]["data-et-sub-row"] == btn["attrs"]["data-et-sub"]
    assert "Plan A · Steps" in text(subrows[0]) and "Steps-Basic" in text(subrows[0])
    nested = find(subrows[0], "table", "et-table")[0]
    assert [text(h) for h in find(nested, "th")] == ["Name", "Status", "Owner", "Tags"]
    assert len(find(nested, "table")) == 0                                  # never a third table
    trs = [tr for tr in find(nested, "tr") if find(tr, "td")]
    assert [text(td) for td in cells(trs[0])] == ["Step 1", "done", "1: Erin", "—"]
    assert [text(td) for td in cells(trs[1])] == ["Step 2", "open", "—", "a, b"]
    assert "Steps · Owner holds a third level, shown as a count and names (a table shows two levels)." in footer(src)[1]


def test_third_level_already_reduced_by_pyegeria_is_shown_and_linked():
    reduced = {"count": 1, "names": ["Erin Overview"], "guid": "g-erin"}
    note = "Steps: 'Owner' is a third level, shown as a count and names (a table shows two levels; use REPORT or a detail_spec drill-down for more)."
    r = table([col("steps", "subtable", type="table")], [{"steps": [{"Name": "s", "Owner": reduced}]}],
              total="n", notes=[note])
    src = html(r, link=True)
    sub = body_rows(src)[1][0]
    a = find(sub, "a")[0]
    assert a["attrs"]["href"] == "/egeria-explorer?guid=g-erin" and text(a) == "1: Erin Overview"
    _, notes = footer(src)
    assert notes == [note]                                                  # pyegeria's note; no second one


def test_count_and_link_renders():
    r = table([col("c", "count", type="elements"), col("l", "link", type="elements")],
              [{"c": [el(1), el(2)], "l": el(3)}], total="n")
    row = body_rows(html(r, link=True))[0][0]
    c, l = cells(row)
    assert text(c) == "2" and find(c, "span")[0]["attrs"]["title"] == "Name 1, Name 2"
    a = find(l, "a")[0]
    assert a["attrs"]["href"] == "/egeria-explorer?guid=g-3" and text(a) == "Name 3"
    plain = cells(body_rows(html(r))[0][0])[1]
    assert not find(plain, "a") and NO_LINK in find(plain, "span")[0]["attrs"]["title"]


def test_zero_false_none_and_missing_are_all_distinct():
    r = table([col("a", "text"), col("b", "text"), col("c", "join", type="elements"), col("d", "text")],
              [{"a": 0, "b": False, "c": [], "d": None}], total="n")
    row = body_rows(html(r))[0][0]
    assert [text(td) for td in cells(row)] == ["0", "false", "none", "—"]


def test_a_value_that_does_not_fit_its_render_is_shown_by_shape_with_a_note():
    r = table([col("a", "text"), col("b", "sparkle")], [{"a": ["x", "y"], "b": "v"}], total="n")
    src = html(r)
    row = body_rows(src)[0][0]
    assert find(cells(row)[0], "ul", "et-bullets") and text(cells(row)[1]) == "v"
    notes = footer(src)[1]
    assert 'A: some values do not fit render "text"; those are shown by their shape.' in notes
    assert 'B: render "sparkle" is not known here; shown by its value\'s shape.' in notes


def test_short_text_has_no_more_button_and_max_lines_is_honoured():
    r = table([col("a", "text", max_lines=1), col("b", "text")], [{"a": "x" * 61, "b": "short"}], total="n")
    row = body_rows(html(r))[0][0]
    a, b = cells(row)
    assert find(a, "div", "et-clamp")[0]["attrs"]["style"] == "-webkit-line-clamp:1"
    assert not find(b, "button") and not find(b, "div", "et-clamp")


# ── Footer wording ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("total,shown,nrows,basis,expected", [
    # pyegeria's only basis today: the rows fit one page, which Egeria does not promise is the last
    (12, 12, 2, "one page", "12 rows (one page; Egeria doesn't promise it is the last)."),
    (1, 1, 1, "one page", "1 row (one page; Egeria doesn't promise it is the last)."),
    # the bases that prove the total is every row
    (12, 12, 2, "counted", "All 12 of 12 rows (counted)."),
    (12, 12, 2, "paged to empty", "All 12 of 12 rows (paged to empty)."),
    # a basis this renderer does not know, or none at all: not claimed complete
    (12, 12, 2, "sampled", "12 rows (sampled; not shown to be every row)."),
    (12, 12, 2, None, "12 rows (not shown to be every row)."),
    # a full page, or more counted than shown, whatever the basis
    (None, 100, 2, "one page", "First 100; more may exist."),
    (445, 100, 2, "counted", "First 100 of 445."),
    # an empty page is the paging contract's "done"
    (0, 0, 0, "one page", "No rows."),
    (None, 0, 0, "one page", "First 0; more may exist."),
])
def test_footer_never_says_a_bare_n(total, shown, nrows, basis, expected):
    r = table([col("a", "text")], [{"a": i} for i in range(nrows)], total=total, shown=shown, basis=basis)
    assert footer(html(r))[0] == expected


def test_no_row_or_column_cap():
    columns = [col(f"c{i}", "text") for i in range(30)]
    rows = [{f"c{i}": f"r{n}c{i}" for i in range(30)} for n in range(300)]
    src = html(table(columns, rows, total="n"))
    t = main_table(src)
    assert "et-wide" in t["attrs"]["class"] and "--et-cols:30" in t["attrs"]["style"]
    assert len(body_rows(src)[0]) == 300 and "r299c29" in src


def test_not_a_table_result_says_so():
    assert "Not a structured table result (kind json); nothing to show here." in html({"kind": "json", "data": []})


# ── Escaping ──────────────────────────────────────────────────────────────────

def test_escaping_pipes_scripts_newlines_and_br():
    r = table([col("t", "text"), col("b", "bullets", type="list"), col("j", "join", type="elements")],
              [{"t": "a | b <script>alert(1)</script>\nline 2<br>line 3 &lt;br&gt; kept",
                "b": ["<script>x</script>", "c<br>d"],
                "j": [{"guid": "g", "qualifiedName": "Q\"<x>", "displayName": "<img src=x onerror=1>"}]}],
              total="n")
    src = html(r)
    assert "<script>" not in src and "<img" not in src
    assert "a | b &lt;script&gt;alert(1)&lt;/script&gt;\nline 2<br>line 3 &amp;lt;br&amp;gt; kept" in src
    assert "<li>c&lt;br&gt;d</li>" in src                                   # <br> is a break only in text cells
    assert 'title="Q&quot;&lt;x&gt; — ' in src and "&lt;img src=x onerror=1&gt;" in src


def test_headers_are_escaped():
    r = table([col("k", "text", name="<b>x</b>")], [{"k": 1}], total="n")
    assert "<th title=\"k · scalar · text\">&lt;b&gt;x&lt;/b&gt;</th>" in html(r)


# ── Interactions ──────────────────────────────────────────────────────────────

def test_attach_toggles_more_and_subtable_rows_and_detaches():
    r = table([col("t", "text"), col("s", "subtable", type="table")],
              [{"t": "x" * 400, "s": [{"a": 1}]}, {"t": "y" * 400, "s": [{"a": 2}, {"a": 3}]}], total="n")
    res = _node({"op": "attach", "result": r, "clicks": ["more:0", "sub:1", "more:0"]})
    assert res["more"][0] == {"open": False, "label": "more", "expanded": "false"}     # opened, then closed
    assert res["more"][1] == {"open": False, "label": "more", "expanded": "false"}
    assert res["subs"][0] == {"hidden": True, "label": "▸ 1 row", "expanded": "false"}
    assert res["subs"][1] == {"hidden": False, "label": "▾ 2 rows", "expanded": "true"}
    assert res["listenersLeft"] == 0
    res = _node({"op": "attach", "result": r, "clicks": ["more:1"]})
    assert res["more"][1] == {"open": True, "label": "less", "expanded": "true"}


# ── Standalone: no Portal globals ─────────────────────────────────────────────

def test_no_portal_globals():
    src = MODULE.read_text()
    code = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    code = re.sub(r"(^|[^:])//[^\n]*", r"\1", code)
    for name in ("window", "React", "ReactDOM", "EgeriaResize", "EgeriaNotMeasured", "EgeriaSharedUI",
                 "localStorage", "sessionStorage", "fetch(", "location", "renderMdToHtml", "tableWrapOpen"):
        assert name not in code, name
    # the one global it defines, and document only behind typeof / opts
    assert "root.EgeriaTable = api" in code
    assert "typeof document !== 'undefined' ? document : null" in code
    bare = re.sub(r"'(?:[^'\\\n]|\\.)*'", "''", code)                   # string literals out
    assert len(re.findall(r"(?<![.\w])document\b", bare)) == 2           # only in that typeof guard (opts.document aside)


def test_module_loads_in_a_bare_vm_context():
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    js = ("const vm=require('vm'),fs=require('fs');const ctx={};vm.createContext(ctx);"
          "vm.runInContext(fs.readFileSync(" + json.dumps(str(MODULE)) + ",'utf8'),ctx);"
          "console.log(typeof ctx.EgeriaTable.renderHtml, Object.keys(ctx).join(','))")
    out = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == "function EgeriaTable"


# ── Link schemes ──────────────────────────────────────────────────────────────

REFUSED = "A link was not shown: only relative, http and https links are allowed."


@pytest.mark.parametrize("href,allowed", [
    ("/egeria-explorer?guid=g-1", True),
    ("type-explorer.html#g-1", True),
    ("?guid=g-1", True),
    ("https://example.org/x", True),
    ("HTTP://example.org/x", True),
    ("javascript:alert(1)", False),
    ("JavaScript:alert(1)", False),
    (" java\tscript:alert(1)", False),
    ("data:text/html,<b>x</b>", False),
    ("vbscript:x", False),
    ("file:///etc/passwd", False),
    # protocol-relative: another host, not a relative link
    ("//other.host/x", False),
    ("\\\\other.host/x", False),
    ("/\\other.host/x", False),
    ("\\/other.host/x", False),
    (" //other.host/x", False),
    ("/\t/other.host/x", False),
])
def test_link_builder_href_scheme_is_allow_listed(href, allowed):
    r = table([col("l", "link", type="elements")], [{"l": el(1)}], total="n")
    src = _node({"op": "html", "result": r, "hrefs": {"g-1": href}})["html"]
    cell = cells(body_rows(src)[0][0])[0]
    if allowed:
        assert find(cell, "a")[0]["attrs"]["href"] == href and REFUSED not in src
    else:
        assert not find(cell, "a") and text(cell) == "Name 1"
        assert REFUSED in find(cell, "span")[0]["attrs"]["title"]
        assert footer(src)[1] == [REFUSED]


def test_one_listener_for_many_tables_opens_the_right_sub_row():
    """A page may attach once, at its body (Local Dashboards). Sub-row ids restart in every table, so a
    click must open the row of ITS table, not the first table's row with the same id."""
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    js = """
const T = require(%s);
function el(attrs, parent) {
  return { attrs: Object.assign({}, attrs), parentNode: parent || null, textContent: attrs.__t || '',
    getAttribute(n) { return n in this.attrs ? this.attrs[n] : null; },
    setAttribute(n, v) { this.attrs[n] = String(v); }, removeAttribute(n) { delete this.attrs[n]; } };
}
const listeners = [];
const body = el({});
function table(name) {
  const wrap = el({'data-et-table': ''}, body);
  const row = el({'data-et-sub-row': '1', hidden: ''}, wrap);
  wrap.querySelector = (sel) => sel === 'tr[data-et-sub-row="1"]' ? row : null;
  const btn = el({'data-et-sub': '1', 'aria-expanded': 'false', __t: '\\u25b8 2 rows'}, wrap);
  return { wrap, row, btn, name };
}
const a = table('a'), b = table('b');
body.addEventListener = (t, fn) => listeners.push(fn);
body.removeEventListener = () => {};
body.querySelector = (sel) => a.wrap.querySelector(sel);   // the whole page: the FIRST match is table a's
body.querySelectorAll = () => [];
T.attach(body);
listeners.forEach((fn) => fn({ target: b.btn }));
console.log(JSON.stringify({ aHidden: 'hidden' in a.row.attrs, bHidden: 'hidden' in b.row.attrs, b: b.btn.textContent }));
""" % json.dumps(str(MODULE))
    out = subprocess.run([node, "-"], input=js, capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    assert json.loads(out.stdout) == {"aHidden": True, "bHidden": False, "b": "▾ 2 rows"}


def test_trim_is_exported_for_pages_that_attach_once():
    assert "trim: trimToggles" in MODULE.read_text()


@pytest.mark.parametrize("label,shown", [("qualified_name", "QN::1"), ("display_name", "Name 1"),
                                         ("qualifiedName", "QN::1"), (None, "Name 1")])
def test_column_label_uses_pyegerias_values(label, shown):
    c = col("m", "join", type="elements")
    if label:
        c["label"] = label
    cell = cells(body_rows(html(table([c], [{"m": [el(1)]}], total="n")))[0][0])[0]
    assert text(cell) == shown
