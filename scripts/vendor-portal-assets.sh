#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
#
# vendor-portal-assets.sh: refresh portal-vendor/, the browser libraries the Portal serves at /vendor/ instead of loading them from a CDN.
#
#   scripts/vendor-portal-assets.sh            fetch: resolve each package's latest version within its major from the npm registry,
#                                              download the tarball, check its sha512 against the registry's integrity, extract only
#                                              the files the pages use, write portal-vendor/MANIFEST.tsv, then check every file
#   scripts/vendor-portal-assets.sh --check    no network: check that every file in portal-vendor/ is in MANIFEST.tsv with a matching
#                                              sha256, and that every MANIFEST row has its file
#
# The majors are fixed here (Dan's decision D-87a): viewer.html stays on marked 12 (its renderer uses the marked <=12 API),
# markdown-header.html uses marked 15, and mermaid 11, highlight.js 11 and DOMPurify 3. Moving a page to a new major is a code
# change, not a refresh.
#
# Fails (non-zero, portal-vendor/ untouched) if: a tarball's sha512 does not match the registry, a listed file is missing from a
# tarball, a written file's sha256 does not match what was extracted, or the total exceeds 15 MB (C6).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENDOR="$ROOT/portal-vendor"
REGISTRY="${NPM_REGISTRY:-https://registry.npmjs.org}"
MODE="${1:-fetch}"

exec python3 -I - "$MODE" "$VENDOR" "$REGISTRY" <<'PY'
import base64, hashlib, io, json, os, shutil, sys, tarfile, tempfile, urllib.request

mode, vendor, registry = sys.argv[1], sys.argv[2], sys.argv[3].rstrip("/")
MAX_BYTES = 15 * 1024 * 1024        # C6
MANIFEST = "MANIFEST.tsv"
HEADER = ["path", "package", "version", "sha256", "tarball", "integrity"]

# (folder under portal-vendor, npm package, major, [(path in tarball, path under the folder)], [tarball folder copied whole, folder])
# highlight.js: the npm package "highlight.js" is the Node build and has no browser highlight.min.js; the project publishes the
# browser build (the files the CDN URLs pointed at) as @highlightjs/cdn-assets, same version numbers.
PACKAGES = [
    ("marked@12", "marked", 12, [("marked.min.js", "marked.min.js"), ("LICENSE.md", "LICENSE.md")], []),
    ("marked@15", "marked", 15, [("marked.min.js", "marked.min.js"), ("LICENSE.md", "LICENSE.md")], []),
    ("mermaid@11", "mermaid", 11, [("dist/mermaid.min.js", "mermaid.min.js"), ("dist/mermaid.esm.min.mjs", "mermaid.esm.min.mjs"),
                                   ("LICENSE", "LICENSE")],
     [("dist/chunks/mermaid.esm.min/", "chunks/mermaid.esm.min/", ".mjs")]),       # every chunk mermaid.esm.min.mjs can import
    ("highlight.js@11", "@highlightjs/cdn-assets", 11, [("highlight.min.js", "highlight.min.js"),
                                                        ("styles/github.min.css", "styles/github.min.css"),
                                                        ("styles/github-dark.min.css", "styles/github-dark.min.css"),
                                                        ("LICENSE", "LICENSE")], []),
    ("dompurify@3", "dompurify", 3, [("dist/purify.min.js", "purify.min.js"), ("LICENSE", "LICENSE")], []),
]


def die(msg):
    print(f"vendor-portal-assets: FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def get(url, accept=None):
    req = urllib.request.Request(url, headers={"Accept": accept} if accept else {})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def latest_in_major(pkg, major):
    doc = json.loads(get(f"{registry}/{pkg.replace('/', '%2F')}", "application/vnd.npm.install-v1+json"))
    best = None
    for v, meta in doc["versions"].items():
        parts = v.split(".")
        if len(parts) != 3 or not all(p.isdigit() for p in parts) or int(parts[0]) != major or meta.get("deprecated"):
            continue                    # releases only: no pre-releases, no deprecated versions
        key = tuple(int(p) for p in parts)
        if best is None or key > best[0]:
            best = (key, v, meta["dist"])
    if best is None:
        die(f"{pkg}: no release in major {major}")
    return best[1], best[2]


def check_integrity(blob, integrity, what):
    algo, _, want = integrity.partition("-")
    if algo != "sha512":
        die(f"{what}: registry integrity is {algo}, expected sha512")
    if base64.b64encode(hashlib.sha512(blob).digest()).decode() != want:
        die(f"{what}: tarball sha512 does not match the registry integrity")


def read_manifest(path):
    with open(path, encoding="utf-8") as fh:
        rows = [line.rstrip("\n").split("\t") for line in fh if line.strip()]
    if not rows or rows[0] != HEADER:
        die(f"{path}: bad header")
    return [dict(zip(HEADER, r)) for r in rows[1:]]


def check(root):
    mpath = os.path.join(root, MANIFEST)
    if not os.path.isfile(mpath):
        die(f"{mpath} is missing")
    rows = read_manifest(mpath)
    listed = {r["path"]: r for r in rows}
    if len(listed) != len(rows):
        die("MANIFEST lists a path twice")
    on_disk = set()
    for d, _, files in os.walk(root):
        for f in files:
            rel = os.path.relpath(os.path.join(d, f), root).replace(os.sep, "/")
            if rel != MANIFEST:
                on_disk.add(rel)
    if on_disk - set(listed):
        die(f"files not in MANIFEST: {sorted(on_disk - set(listed))[:5]}")
    if set(listed) - on_disk:
        die(f"MANIFEST rows without a file: {sorted(set(listed) - on_disk)[:5]}")
    total = 0
    for rel, r in sorted(listed.items()):
        with open(os.path.join(root, rel), "rb") as fh:
            b = fh.read()
        total += len(b)
        if sha256(b) != r["sha256"]:
            die(f"{rel}: sha256 does not match MANIFEST")
    if total > MAX_BYTES:
        die(f"total {total} bytes is over the 15 MB limit")
    print(f"vendor-portal-assets: OK: {len(listed)} files, {total} bytes, all sha256 match MANIFEST")


def fetch():
    stage = tempfile.mkdtemp(prefix="portal-vendor.")
    try:
        rows, total = [], 0
        for folder, pkg, major, files, trees in PACKAGES:
            version, dist = latest_in_major(pkg, major)
            url, integrity = dist["tarball"], dist.get("integrity", "")
            blob = get(url)
            check_integrity(blob, integrity, f"{pkg}@{version}")
            with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tf:
                members = {m.name[len("package/"):]: m for m in tf.getmembers() if m.isfile() and m.name.startswith("package/")}
                wanted = list(files)
                for src_dir, dst_dir, suffix in trees:
                    sub = sorted(n for n in members if n.startswith(src_dir) and n.endswith(suffix) and "/" not in n[len(src_dir):])
                    if not sub:
                        die(f"{pkg}@{version}: nothing under {src_dir}")
                    wanted += [(n, dst_dir + n[len(src_dir):]) for n in sub]
                for src, dst in wanted:
                    if src not in members:
                        die(f"{pkg}@{version}: {src} is not in the tarball")
                    data = tf.extractfile(members[src]).read()
                    rel = f"{folder}/{dst}"
                    out = os.path.join(stage, rel)
                    os.makedirs(os.path.dirname(out), exist_ok=True)
                    with open(out, "wb") as fh:
                        fh.write(data)
                    total += len(data)
                    rows.append([rel, pkg, version, sha256(data), url, integrity])
            print(f"  {pkg}@{version} -> {folder}/ ({len(wanted)} files)")
        if total > MAX_BYTES:
            die(f"total {total} bytes is over the 15 MB limit (C6): stop for a ruling")
        rows.sort(key=lambda r: r[0])
        with open(os.path.join(stage, MANIFEST), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\t".join(HEADER) + "\n")
            for r in rows:
                fh.write("\t".join(r) + "\n")
        check(stage)                    # every staged file against the MANIFEST just written
        if os.path.isdir(vendor):
            shutil.rmtree(vendor)
        shutil.copytree(stage, vendor)
        check(vendor)                   # and again where it landed
    finally:
        shutil.rmtree(stage, ignore_errors=True)


if mode == "--check":
    check(vendor)
elif mode == "fetch":
    fetch()
else:
    die(f"unknown argument {mode!r} (use no argument to fetch, or --check)")
PY
