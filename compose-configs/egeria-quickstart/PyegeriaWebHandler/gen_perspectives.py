#!/usr/bin/env python3
"""Generate a loadable Dr.Egeria doc for the Overview dashboard Perspective/Question
library, from the PERSPECTIVES data in egeria-overview.html. Single source of truth."""
import re, html as htmllib

SRC = "/Users/dwolfson/localGit/egeria-v6/egeria-workspaces-fs/compose-configs/egeria-quickstart/PyegeriaWebHandler/egeria-overview.html"
OUT = "/Users/dwolfson/localGit/egeria-v6/egeria-workspaces-fs/compose-configs/egeria-quickstart/PyegeriaWebHandler/OVERVIEW_PERSPECTIVES.dr-egeria.md"

# 2026-08-27: Resource Explorer already ran its own Perspective/Question
# reconciliation against this same Egeria instance, materialising 9 of our
# 10 perspectives as real Perspective elements (verified live via
# /api/perspectives) -- Governance, Steward, Data Owner, Consumer,
# Architecture, Security, App/AI Builder, Privacy, Community. Decision:
# adopt those elements rather than create a second, confusingly-parallel
# "overview-"-prefixed set (see the commit that first generated a duplicate
# set, then walked it back). Only "Engineering" has no existing match, so
# only it gets a real "Create Perspective" block below; everything else
# links its Questions straight to the existing qualifiedName. If a future
# PERSPECTIVES entry's key isn't in this map, this script creates a new
# Perspective for it -- same as it always has -- so a genuinely new
# perspective doesn't require touching this map at all.
EXISTING_PERSPECTIVES = {
    "governance": "Perspective::Governance",
    "steward": "Perspective::Steward",
    "owner": "Perspective::Data Owner",
    "consumer": "Perspective::Consumer",
    "architecture": "Perspective::Architecture",
    "security": "Perspective::Security",
    "builder": "Perspective::App/AI Builder",
    "privacy": "Perspective::Privacy",
    "community": "Perspective::Community",
}

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
out.append("> Most of these Perspectives already exist (Resource Explorer's own")
out.append("> reconciliation ran first) -- see EXISTING_PERSPECTIVES in this script. Only")
out.append("> `Engineering` is created new here; everything else links its Questions")
out.append("> straight to the existing element by qualified name.")
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
        out.append(f"# {label} — perspective (existing — adopted from Resource Explorer, not created here)")
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
