<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Extraction pipeline for *Patterns of Information Management*

These scripts regenerate the `poim-*.md` Dr.Egeria command files from
`Patterns of Information Management_Book copy.pdf`.  They are kept so the extraction can be
re-run when the Dr.Egeria command set changes.  They need `pdftotext` and `pdftohtml`
(poppler) on the PATH, and they read/write a working directory set by `SP` at the top of each
script.

Preparation (from this directory's parent):

```
pdftotext -layout -f 99 -l 678 "Patterns of Information Management_Book copy.pdf" $SP/poim_body.txt
pdftohtml -xml -fontfullname -f 99 -l 678 -i "Patterns of Information Management_Book copy.pdf" $SP/poim_body
pdftohtml -xml -fontfullname -f 673 -l 678 -i "Patterns of Information Management_Book copy.pdf" $SP/gloss
```

Then run in order:

| Script | What it does |
|---|---|
| `outline.py` | Reads the heading fonts from the XML.  HelveticaNeue-Bd at 18pt is a pattern group, 17pt is a pattern, 15pt is one of the nine TOGAF subsections. |
| `captions.py` | Collects the real figure/table captions (they are set in HelveticaLTStd, body text is TimesLTStd) so body sentences that merely start "Figure 5.42 shows…" are not discarded. |
| `extract.py` | Walks the layout text page by page against the outline and fills Context / Problem / Example / Forces / Solution / Consequences / Example Resolved / Known Uses / Related Patterns.  Left margin 16 is a continuation, 22-24 starts a paragraph, 25-26 is a bullet, 27+ is a bullet continuation. |
| `patlets.py` | Parses the patlet tables (Icon / Pattern Name / Problem / Solution) by clustering `left` positions into columns.  This is the only source for the patterns the book summarises in a table but does not describe in full. |
| `supplement.json` | Hand-checked name spellings, plus the eight single-row patlet tables that are too small for the column detector. |
| `build.py` | Emits the seven `poim-chN-*.md` files and `poim-pattern-links.md`. |
| `buildglossary.py` | Emits `poim-glossary.md` from Appendix 1. |

The book sets pattern names in small capitals, which survive text extraction as ALL CAPS.
That is what `refs()` in `build.py` matches against the catalogue of pattern names to derive
the nested and related links, and what `smallcaps_to_title()` converts back to title case in
the emitted prose.
