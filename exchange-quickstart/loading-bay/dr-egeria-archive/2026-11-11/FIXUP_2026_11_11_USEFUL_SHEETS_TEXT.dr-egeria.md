<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Fix-up: the four "What these tiles measure" text placements (one run, 2026-11-11)

> Loadable **Dr.Egeria** document, **for one run on a platform where `LOCAL_DASHBOARDS_USEFUL_SHEETS.dr-egeria.md`
> already ran before its fix** (laz, 2026-11-11). There, its four `Add Text on Dashboard Sheet` commands failed with
> "MD Content is required": each value began with a `####` heading line, and Dr.Egeria ends an attribute's value
> at the first line starting with `###` (so `####` too). Everything else in that document applied.
>
> This file holds **only** those four commands, with the heading written as bold text, and the same Dashboard
> Sheet Name, Placement Name, Placement Span and Placement Emphasis as the sheets document. Each upserts the
> text placement named "What these tiles measure" on its sheet; nothing else is read or written.
>
> **Not in any batch** (`_batch.json` lists it under `exclude`): a fresh platform gets the corrected text from the
> sheets document itself. Shared Egeria write: `--validate` first, `--process` once under the peer check.
> Re-running it replaces the same placements by name.

___

## Add Text on Dashboard Sheet
### Dashboard Sheet Name
catalog-health

### Placement Name
What these tiles measure

### MD Content
**What these tiles measure**

The readiness funnel counts assets at each step from cataloged to AI-ready. Ownership counts assets with an owner, by the kind of owner. Stale assets have not changed in 180 days. The composition chart shows the asset types the catalog holds.

### Placement Span
full

### Placement Emphasis
panel

___

## Add Text on Dashboard Sheet
### Dashboard Sheet Name
glossary-and-meaning

### Placement Name
What these tiles measure

### MD Content
**What these tiles measure**

Definition completeness is the share of terms with a description. Terms in use counts terms that something refers to; the rest are orphans. Active and draft count terms by content status. Semantic grounding counts assets linked to a term.

### Placement Span
full

### Placement Emphasis
panel

___

## Add Text on Dashboard Sheet
### Dashboard Sheet Name
governance-and-compliance

### Placement Name
What these tiles measure

### MD Content
**What these tiles measure**

Governance coverage counts elements that carry a governance classification or zone. Certifications counts active and expiring certifications, licenses and exceptions. Usage context counts information supply chains and blueprints; solution design context counts assets placed in a solution design.

### Placement Span
full

### Placement Emphasis
panel

___

## Add Text on Dashboard Sheet
### Dashboard Sheet Name
community-and-feedback

### Placement Name
What these tiles measure

### MD Content
**What these tiles measure**

Feedback counts comments, ratings, likes, tags and note logs. Engagement shows the same events by the week they were made, over the last twelve weeks. Contributors and the karma leaderboard show who is adding to the catalog.

### Placement Span
full

### Placement Emphasis
panel

___
