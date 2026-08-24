<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Design Patterns

Dr.Egeria command files that load two published design pattern languages into the open metadata
ecosystem as `DesignPattern` elements (type [0595](https://egeria-project.org/types/5/0595-Design-Patterns/)),
along with the specialization, nesting and relationship links between them.

> **The source PDFs are copyright IBM and are excluded by `.gitignore`.**  Keep local copies in
> this directory if you want to re-run the extraction, but never commit or publish them.  Every
> generated pattern carries a `Legal` attribute with the book's copyright and full attribution;
> do not remove it.

## Common Information Models for an Open, Analytical, and Agile World

Mandy Chessell, Gandhi Sivakumar, Dan Wolfson, Kerard Hogg and Ray Harishankar, IBM Press, 2015.

| File | Contents |
|---|---|
| `cim-structural-patterns.md` | The 5 structural patterns from chapter 3, plus 4 specialization and 5 related links. |

## Patterns of Information Management

Mandy Chessell and Harald C. Smith, IBM Press, 2013.  232 patterns in 18 pattern groups, taken
from chapters 3-9, with the glossary from appendix 1.

| File | Contents |
|---|---|
| `poim-ch3-people-and-organizations.md` | 15 patterns |
| `poim-ch4-information-architecture.md` | 45 patterns |
| `poim-ch5-information-at-rest.md` | 64 patterns |
| `poim-ch6-information-in-motion.md` | 16 patterns |
| `poim-ch7-information-processing.md` | 37 patterns |
| `poim-ch8-information-protection.md` | 36 patterns |
| `poim-ch9-solutions-for-information-management.md` | 19 patterns |
| `poim-pattern-links.md` | 218 specialized, 285 nested and 555 related links |
| `poim-glossary.md` | 1 glossary, 64 terms and 86 semantic assignments onto the patterns |

Load the pattern files before `poim-pattern-links.md` and `poim-glossary.md`, since those
reference the patterns by qualified name.

## How the links are derived

Chapter 1 of *Patterns of Information Management* defines the structure, and each kind of
statement maps onto a different relationship:

- Every pattern group has a **lead pattern** describing the core principles of the group; the
  others "enhance one or more characteristics of the lead pattern to support a more specialized
  situation" — `Link Specialized Design Patterns`.
- "A pattern can be used as a component in the solution described by another pattern" —
  `Link Nested Design Patterns`, taken from the pattern names referenced in each Solution.
- The cross-references in each pattern's *Related Patterns* section —
  `Link Related Design Patterns`.

Both books set pattern names in small capitals wherever a pattern is referenced.  Those
small-capital names are the display names here, and are what the extraction matches on to build
the links.  See `extraction-tools/README.md` to regenerate the files.
