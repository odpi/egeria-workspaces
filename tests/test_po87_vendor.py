"""PO-87 C3: the Tier 1 pages load their browser libraries from the Portal (/vendor/), never from another host.

Tier 1 pages:
- portal-docs/viewer.html (the Portal Docs viewer);
- compose-configs/egeria-quickstart/markdown-header.html (the Apache markdown viewer, /markdown-viewer; freshstart mounts it too);
- every HTML page under coco-workbooks/**/mermaid_graphs/ (the pyegeria mermaid graph pages: blueprints and supply chains).
Plus the vendored CSS under portal-vendor/.

In those files, after removing comments (HTML <!-- -->, CSS and JS /* */, and JS // line comments), no address in any of these
may name another host (a scheme such as https:, or a leading //):
- <script src>, <link href> (stylesheets, preload and modulepreload alike);
- import(...), import ... from '...', import '...';
- CSS @import and url(...) (data: URLs are allowed in url()).
Every /vendor/ address a page uses must be a file listed in portal-vendor/MANIFEST.tsv.

MANIFEST.tsv itself: every file under portal-vendor/ has a row and every row has its file; each sha256 matches; each row's version
has the major named by its folder (<package>@<major>/); a folder named with a full version (<package>@<x.y.z>/) holds exactly that version.

The vendored JavaScript is not scanned: it is the packages' own code, recorded by sha256 in MANIFEST.tsv.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "portal-vendor"
MANIFEST = VENDOR / "MANIFEST.tsv"
HEADER = ["path", "package", "version", "sha256", "tarball", "integrity"]

NAMED_PAGES = ("portal-docs/viewer.html", "compose-configs/egeria-quickstart/markdown-header.html")
GRAPH_ROOT = "coco-workbooks"


def tier1_pages() -> list[Path]:
    pages = [ROOT / p for p in NAMED_PAGES]
    pages += sorted(p for p in (ROOT / GRAPH_ROOT).rglob("*.html") if "mermaid_graphs" in p.relative_to(ROOT).parts)
    return pages


def vendored_css() -> list[Path]:
    return sorted(VENDOR.rglob("*.css"))


# ---- the scanner ----

HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)
LINE_COMMENT = re.compile(r"(?m)^\s*//.*$")        # a // comment on its own line (a URL's // is never at the start of a line)

SCRIPT_SRC = re.compile(r"<script\b[^>]*?\bsrc\s*=\s*([\"'])(.*?)\1", re.I | re.S)
LINK_HREF = re.compile(r"<link\b[^>]*?\bhref\s*=\s*([\"'])(.*?)\1", re.I | re.S)
DYNAMIC_IMPORT = re.compile(r"\bimport\s*\(\s*([\"'`])(.*?)\1\s*\)")
STATIC_IMPORT = re.compile(r"\bimport\b[^;\"'`()]*?\bfrom\s*([\"'])(.*?)\1")
BARE_IMPORT = re.compile(r"\bimport\s*([\"'])(.*?)\1")
CSS_IMPORT = re.compile(r"@import\s+(?:url\(\s*)?([\"']?)([^\"')\s;]+)\1", re.I)
CSS_URL = re.compile(r"url\(\s*([\"']?)(.*?)\1\s*\)", re.I)

CONSTRUCTS = (("script src", SCRIPT_SRC), ("link href", LINK_HREF), ("import()", DYNAMIC_IMPORT), ("import from", STATIC_IMPORT),
              ("import", BARE_IMPORT), ("@import", CSS_IMPORT), ("url()", CSS_URL))
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def strip_comments(text: str, kind: str) -> str:
    if kind == "html":
        text = HTML_COMMENT.sub("", text)
    text = BLOCK_COMMENT.sub("", text)
    if kind == "html":                 # inline scripts; a CSS file has no // comments
        text = LINE_COMMENT.sub("", text)
    return text


def off_host(addr: str, construct: str) -> bool:
    a = addr.strip()
    if construct == "url()" and a.lower().startswith("data:"):
        return False
    return a.startswith("//") or bool(SCHEME.match(a))


def addresses(text: str, kind: str) -> list[tuple[str, str]]:
    """(construct, address) for every address the constructs name, comments removed."""
    body = strip_comments(text, kind)
    return [(name, m.group(2)) for name, rx in CONSTRUCTS for m in rx.finditer(body)]


def off_host_addresses(text: str, kind: str) -> list[tuple[str, str]]:
    return [(c, a) for c, a in addresses(text, kind) if off_host(a, c)]


# ---- the scanner, on synthetic input (each construct is caught; comments are not) ----

@pytest.mark.parametrize("snippet", [
    '<script src="https://cdn.example.org/x.js"></script>',
    "<script type='module' src='//cdn.example.org/x.mjs'></script>",
    '<link rel="stylesheet" href="https://cdn.example.org/x.css">',
    '<link rel="preload" as="script" href="https://cdn.example.org/x.js">',
    '<link rel="modulepreload" href="http://cdn.example.org/x.mjs">',
    "<script type=\"module\">import mermaid from 'https://cdn.example.org/m.mjs';</script>",
    "<script type=\"module\">import { a, b } from \"https://cdn.example.org/m.mjs\";</script>",
    "<script type=\"module\">import 'https://cdn.example.org/side-effect.mjs';</script>",
    "<script>const m = await import('https://cdn.example.org/m.mjs');</script>",
    "<style>@import url('https://fonts.example.org/f.css');</style>",
    '<style>@import "https://fonts.example.org/f.css";</style>',
    "<style>.x { background: url(https://img.example.org/a.png); }</style>",
])
def test_scanner_flags_each_construct(snippet):
    assert off_host_addresses(snippet, "html"), snippet


@pytest.mark.parametrize("snippet", [
    '<script src="/vendor/mermaid@11/mermaid.min.js"></script>',
    "<script type=\"module\">import mermaid from '/vendor/mermaid@11/mermaid.esm.min.mjs';</script>",
    '<link rel="stylesheet" href="/vendor/highlight.js@11/styles/github-dark.min.css">',
    '<link rel="icon" href="/favicon.ico">',
    "<style>.x { background: url(data:image/png;base64,AAAA); }</style>",
    '<!-- <script src="https://cdn.example.org/old.js"></script> -->',
    "<script>/* import('https://cdn.example.org/m.mjs') */</script>",
    "<script>\n  // import mermaid from 'https://cdn.example.org/m.mjs';\n</script>",
    '<a href="https://egeria-project.org/">docs</a>',      # a link the user follows is not a load
])
def test_scanner_allows_same_host_and_comments(snippet):
    assert not off_host_addresses(snippet, "html"), snippet


def test_scanner_ignores_css_licence_comments():
    css = "/*!\n  Theme: GitHub Dark\n  URL: https://github.com/primer/github-syntax-dark\n  url(https://example.org/x)\n*/\n.hljs{color:#c9d1d9}"
    assert not off_host_addresses(css, "css")
    assert off_host_addresses(css + "\n.a{background:url(https://example.org/x.png)}", "css")


# ---- the real files ----

def _manifest_rows() -> list[dict]:
    lines = MANIFEST.read_text(encoding="utf-8").splitlines()
    assert lines and lines[0].split("\t") == HEADER, "MANIFEST.tsv header"
    return [dict(zip(HEADER, line.split("\t"))) for line in lines[1:] if line]


def test_tier1_pages_found():
    pages = tier1_pages()
    missing = [p for p in pages if not p.is_file()]
    assert not missing, missing
    graphs = [p for p in pages if "mermaid_graphs" in p.parts]
    assert len(graphs) >= 18, f"expected the 18 tracked mermaid graph pages, found {len(graphs)}"
    assert vendored_css(), "no vendored CSS found"


@pytest.mark.parametrize("rel", [p.relative_to(ROOT).as_posix() for p in tier1_pages()])
def test_tier1_page_loads_nothing_off_host(rel):
    text = (ROOT / rel).read_text(encoding="utf-8")
    bad = off_host_addresses(text, "html")
    assert not bad, f"{rel} loads from another host: {bad}"


@pytest.mark.parametrize("rel", [p.relative_to(ROOT).as_posix() for p in vendored_css()])
def test_vendored_css_loads_nothing_off_host(rel):
    bad = off_host_addresses((ROOT / rel).read_text(encoding="utf-8"), "css")
    assert not bad, f"{rel} loads from another host: {bad}"


def test_every_vendor_address_is_in_the_manifest():
    listed = {r["path"] for r in _manifest_rows()}
    used, missing = set(), []
    for page in tier1_pages():
        for construct, addr in addresses(page.read_text(encoding="utf-8"), "html"):
            if addr.startswith("/vendor/"):
                path = addr[len("/vendor/"):].split("?")[0].split("#")[0]
                used.add(path)
                if path not in listed:
                    missing.append(f"{page.relative_to(ROOT).as_posix()}: {addr}")
    assert used, "no page loads from /vendor/"
    assert not missing, f"/vendor/ addresses not in MANIFEST.tsv: {missing}"


def test_manifest_matches_the_files():
    rows = _manifest_rows()
    listed = [r["path"] for r in rows]
    assert len(set(listed)) == len(listed), "a path is listed twice"
    on_disk = {p.relative_to(VENDOR).as_posix() for p in VENDOR.rglob("*") if p.is_file()} - {"MANIFEST.tsv"}
    assert on_disk == set(listed), f"not in MANIFEST: {sorted(on_disk - set(listed))[:5]}; no file: {sorted(set(listed) - on_disk)[:5]}"
    bad = [r["path"] for r in rows if hashlib.sha256((VENDOR / r["path"]).read_bytes()).hexdigest() != r["sha256"]]
    assert not bad, f"sha256 does not match MANIFEST: {bad}"


FOLDER = re.compile(r"^(?P<name>.+)@(?P<ver>\d+(?:\.\d+\.\d+)?)$")
VERSION = re.compile(r"^\d+\.\d+\.\d+$")


def test_manifest_versions_match_their_folders():
    bad = []
    for r in _manifest_rows():
        folder = r["path"].split("/")[0]
        m = FOLDER.match(folder)
        if not m or not VERSION.match(r["version"]):
            bad.append(f"{r['path']}: folder {folder!r} or version {r['version']!r} is not <name>@<major|x.y.z> / x.y.z")
            continue
        want = m.group("ver")
        got = r["version"] if "." in want else r["version"].split(".")[0]
        if got != want:
            bad.append(f"{r['path']}: folder says {want}, MANIFEST says {r['version']}")
    assert not bad, bad


@pytest.mark.parametrize("folder,version,ok", [
    ("mermaid@11", "11.17.2", True), ("mermaid@11", "10.8.0", False),
    ("mermaid@10.8.0", "10.8.0", True), ("mermaid@10.8.0", "10.8.1", False),
    ("svg-pan-zoom@3.6.0", "3.6.0", True), ("svg-pan-zoom@3", "3.6.2", True),
])
def test_folder_version_rule(folder, version, ok):
    want = FOLDER.match(folder).group("ver")
    got = version if "." in want else version.split(".")[0]
    assert (got == want) is ok
