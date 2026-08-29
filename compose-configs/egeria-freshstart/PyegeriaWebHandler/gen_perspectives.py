#!/usr/bin/env python3
"""Generate a loadable Dr.Egeria doc for the Overview dashboard Perspective/Question
library, from the PERSPECTIVES data in egeria-overview.html. Single source of truth."""
import re, html as htmllib

SRC = "/Users/dwolfson/localGit/egeria-v6/egeria-workspaces-fs/compose-configs/egeria-freshstart/PyegeriaWebHandler/egeria-overview.html"
OUT = "/Users/dwolfson/localGit/egeria-v6/egeria-workspaces-fs/compose-configs/egeria-freshstart/PyegeriaWebHandler/OVERVIEW_PERSPECTIVES.dr-egeria.md"

# 2026-08-27: unlike quickstart, freshstart's Egeria instance is genuinely
# separate/isolated (its own fs-metadata-store, no shared data with
# quickstart's qs-metadata-store) -- confirmed live via /api/perspectives
# returning only the original "Security Officer" sample-data Perspective,
# none of Resource Explorer's reconciled set. So there is nothing to adopt
# here: all 10 PERSPECTIVES entries get a real "Create Perspective" block.
# Still uses the plain "Perspective::<Label>" qualified-name convention
# (not "overview-"-prefixed) rather than freshstart-specific naming, so
# that if Resource Explorer (or anything else) ever runs its own
# reconciliation against freshstart's server later, it lines up by
# qualifiedName instead of creating a second parallel set the way
# quickstart's first attempt did (see that commit's history). If a future
# environment DOES already have some of these, add it to this dict the
# same way quickstart's copy does -- this script's shape supports both.
EXISTING_PERSPECTIVES = {}

def clean(s):
    s = re.sub(r"<[^>]+>", "", s)                 # strip HTML tags
    s = s.replace("&nbsp;", " ").replace("&amp;", "&")
    s = htmllib.unescape(s)
    return re.sub(r"\s+", " ", s).strip()

doc = open(SRC).read()
block = re.search(r"const PERSPECTIVES = \{(.*?)\n\};", doc, re.S).group(1)
heads = re.findall(r"(\w+):\s*\{\s*icon:'([^']*)',\s*label:'([^']*)',\s*q:'([^']*)',", block)
keys = [h[0] for h in heads]

out = []
out.append("<!-- SPDX-License-Identifier: CC-BY-4.0 -->")
out.append("<!-- Copyright Contributors to the ODPi Egeria project. -->")
out.append("")
out.append("# Egeria Overview — Perspective / Question Library")
out.append("")
out.append("> Loadable **Dr.Egeria** document that materialises the Overview dashboard's")
out.append("> per-perspective question sets as real Egeria elements: each **Perspective**")
out.append("> (a viewpoint held by an actor) is linked via **ScopedBy** to its **Questions**")
out.append("> (GlossaryTerms classified `Question`). Generated from `egeria-overview.html`")
out.append("> `PERSPECTIVES` — the single source of truth. Regenerate with gen_perspectives.py.")
out.append(">")
out.append("> freshstart's Egeria instance is isolated from quickstart's -- none of these")
out.append("> Perspectives pre-exist here (see EXISTING_PERSPECTIVES in this script, empty),")
out.append("> so every one of them gets a real Create Perspective command below.")
out.append(">")
out.append("> Starter questions scavenged from DAMA-DMBOK / EDM-Council DCAM / FAIR / DataOps.")
out.append("> **Run with VALIDATE first, then PROCESS.** Create commands carry user-specified")
out.append("> Qualified Names so the Link commands can cross-reference them within this doc.")
out.append("")
out.append("---")
out.append("")

for i, (key, icon, label, q) in enumerate(heads):
    label = clean(label)
    start = block.find(key + ":")
    end = block.find(keys[i + 1] + ":") if i + 1 < len(keys) else len(block)
    seg = block[start:end]
    qs = re.findall(r"Q\('([^']*)','((?:[^'\\]|\\.)*)','((?:[^'\\]|\\.)*)'", seg)
    existing_qn = EXISTING_PERSPECTIVES.get(key)
    p_qn = existing_qn or f"Perspective::{label}"

    if existing_qn:
        out.append(f"# {label} — perspective (existing — not created here)")
        out.append("")
        out.append(f"Questions below link to the existing `{existing_qn}` Perspective element;")
        out.append("no Create Perspective command for it in this doc.")
        out.append("")
        out.append("---")
        out.append("")
    else:
        out.append(f"# {label} — perspective")
        out.append("")
        out.append("## Create Perspective")
        out.append("")
        out.append("### Display Name")
        out.append(label)
        out.append("")
        out.append("### Category")
        out.append("Overview Dashboard Perspective")
        out.append("")
        out.append("### Description")
        out.append(f"{clean(q).strip(chr(34))}  (Egeria Overview dashboard perspective.)")
        out.append("")
        out.append("### Qualified Name")
        out.append(p_qn)
        out.append("")
        out.append("### Version Identifier")
        out.append("1.0")
        out.append("")
        out.append("---")
        out.append("")

    for n, (qi, qt, qsrc) in enumerate(qs, 1):
        q_qn = f"Question::overview-{key}-{n:02d}"
        text = clean(qt)
        usage = clean(qsrc)
        out.append("## Create Question")
        out.append("")
        out.append("### Display Name")
        out.append(text)
        out.append("")
        out.append("### Summary")
        out.append(text)
        out.append("")
        out.append("### Usage")
        out.append(usage)
        out.append("")
        out.append("### Category")
        out.append("Overview Dashboard Question")
        out.append("")
        out.append("### Content Status")
        out.append("ACTIVE")
        out.append("")
        out.append("### Qualified Name")
        out.append(q_qn)
        out.append("")
        out.append("### Version Identifier")
        out.append("1.0")
        out.append("")
        out.append("## Link Perspective to Question")
        out.append("")
        out.append("### Perspective Name")
        out.append(p_qn)
        out.append("")
        out.append("### Question Name")
        out.append(q_qn)
        out.append("")
        out.append("### Label")
        out.append("ScopedBy")
        out.append("")
        out.append("---")
        out.append("")

open(OUT, "w").write("\n".join(out))
n_q = sum(len(re.findall(r"Q\('", block[block.find(k+':'):(block.find(keys[j+1]+':') if j+1<len(keys) else len(block))])) for j,k in enumerate(keys))
print(f"wrote {OUT}\nperspectives={len(heads)} questions={n_q}")
