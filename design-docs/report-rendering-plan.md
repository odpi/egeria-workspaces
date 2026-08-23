# Report Rendering Plan — Egeria Explorer

**Status**: Revised after review  
**Context**: Egeria Explorer single-page app (`type-explorer.html` + FastAPI routers)

---

## Background

The `POST /api/report-specs/execute` endpoint already works. It calls pyegeria's
`exec_report_spec` and returns a structured result. A format selector already exists
in the execution panel. The gap is entirely in how the UI **renders** what comes back:
no Markdown/Mermaid handling in output, no Vega-Lite charts, and no master-detail
navigation.

The pyegeria executor returns content in different shapes depending on `output_format`:

| Format | Return shape | Content |
|--------|--------------|---------|
| DICT | `dict` | List of materialized Python dicts |
| JSON | `dict` | Raw Egeria response — always available for any spec |
| LIST | `text/markdown` | Markdown table; master rows may include `[details]` anchor links |
| REPORT | `text/markdown` | Rich vertical Markdown with bullet-list nesting |
| REPORT-GRAPH | `text/markdown` | Recursive wiki-style Markdown with GUID anchors |
| FORM | `text/markdown` | Editable Markdown form |
| MERMAID | `text/markdown` | Mermaid diagram text |
| GRAPH / HTML | `text/html` | Standalone HTML page with `vega-embed` charts pre-wired |

**Key constraint**: not every spec declares a `DICT` format. `JSON` is always
available and returns the raw Egeria response. This affects the GRAPH strategy
(see Phase 1).

The plan is four phases ordered by dependency. Backend normalisation was dropped
(response shape is already consistent).

---

## Phase 1 — GRAPH Format: JSON + Auto-Charts Fallback

**What**: The format selector already exists and works for text formats. The one
gap is GRAPH: pyegeria returns a self-contained HTML page for this format, which
can't be embedded cleanly in the SPA. The fix is to never send `GRAPH` to the
executor — instead, treat it as a UI-side rendering mode.

**Changes**:
- When the user selects GRAPH in the format dropdown, the execution panel sends
  `DICT` if the spec has a `DICT` format, otherwise falls back to `JSON`.
- The result is then rendered by `DictResultView` (Phase 4) with `AvailableCharts`
  active (Phase 3b), producing inline Vega-Lite charts matched to the dark theme.
- The existing HTML page from pyegeria's GRAPH output is not used.

**Why JSON is the right fallback**: JSON is the raw Egeria response and is always
available regardless of what formats a spec declares. It gives `AvailableCharts`
enough data to find `*BarGraph`/`*PieGraph` keys, since those are generated during
materialisation and appear in the DICT response — which is what JSON approximates.

---

## Phase 2 — Smart Text Renderer (`SmartReportRenderer`)

**What**: For any text-format result (LIST, REPORT, FORM, MERMAID, REPORT-GRAPH),
tokenize the output before rendering so that embedded code fences are handled by
the right component rather than shown as raw text.

**New component**: `SmartReportRenderer({ content })`

1. Splits the content string into an ordered list of typed segments:
   - `plain` — ordinary Markdown prose and tables
   - `mermaid` — content of a ` ```mermaid ` fence
   - `vega-lite` — content of a ` ```vega-lite ` fence
   - `json` — content of a ` ```json ` fence (pretty-printed with copy button)
2. Renders each segment with its appropriate component:
   - `plain` → existing `renderMd`
   - `mermaid` → existing `MermaidDiagram`
   - `vega-lite` → new `VegaChart` (Phase 3a)
   - `json` → syntax-highlighted code block
3. **Master-detail anchor handling** — pyegeria's LIST output uses this pattern:
   - Master table rows include `[details](#guid)` links.
   - Detail sections are appended below the table with `<a id="{guid}">` anchors.
   - Currently `renderMd` (marked.js) strips raw HTML, so anchors are lost.
   - Fix: configure marked.js with a custom renderer that passes `<a id=...>`
     tags through (no `href`, so no XSS concern).
   - Add bi-directional linking: each detail section heading renders a small
     "↑ Back to table" link pointing at a stable `#master-table` anchor placed
     above the master table. This lets users navigate down to a detail and back.

---

## Phase 3 — Vega-Lite Chart Rendering

Two delivery paths: 3a from text output (` ```vega-lite ` fences), 3b from DICT/JSON
output (`*BarGraph`/`*PieGraph` keys).

### 3a — `VegaChart` component

Used by `SmartReportRenderer` when a ` ```vega-lite ` fence is encountered, and
by `AvailableCharts` (3b) when rendering chart specs from data.

- Parse the fence/value content as JSON to get a Vega-Lite spec object.
- `VegaChart({ spec })` component:
  - Calls `vegaEmbed(ref.current, parsedSpec, { actions: false, theme: 'dark' })`
    inside a `useEffect` on mount.
  - Shows a spinner while vega-embed initialises.
  - Renders a clear error message if the spec is invalid JSON or vega-embed rejects it.
- `vega-embed` (~300 KB) is loaded **unconditionally** via a `<script>` tag in the
  page head. Simple to reason about; can be revisited if load time becomes a concern.

### 3b — `AvailableCharts` component

Parallel to `AvailableMermaidDiagrams`. Used by `DictResultView` to surface charts
that pyegeria's materializer auto-generates from numeric dict fields.

- Scans a data object for keys matching `/BarGraph$|PieGraph$/i`.
- For each match, renders a collapsible `VegaChart` panel with a human-readable
  label derived from the key (e.g. `typeMembershipBarGraph` → "Type Membership Bar").
- No spec-specific configuration needed — works generically on any DICT/JSON result.

---

## Phase 4 — DICT Result Navigator (`DictResultView`)

**What**: Replace the raw JSON dump for DICT/JSON results with a navigable
master-detail view driven by the spec's declared column list.

**New component**: `DictResultView({ rows, columns })`

- `rows`: the top-level array from the response.
- `columns`: the `attributes` array from the matched `Format` in the spec
  (already available from `/api/report-specs`). This is the authoritative
  column list — it reflects what the spec author decided to show.

**Rendering rules**:
- Each `Column` with a scalar value renders as a table column.
- Each `Column` with a `detailSpec` key renders as a **▶ expand** chevron rather
  than an inline column. Clicking opens a sub-panel below that row, which runs
  `DictResultView` recursively using the columns defined in the named `detailSpec`.
- `AvailableCharts` and `AvailableMermaidDiagrams` run automatically on each
  expanded row object so that chart/diagram keys produce render buttons without
  any additional configuration.
- GUIDs (keys named `guid`) render as `<code>` with a copy button.
- A filter bar above the table narrows rows against the first visible string column.
- Recursion is hard-capped at 3 levels regardless of how deep `detailSpec` chains go.

**Honouring the spec**: columns are spec-driven, not inferred from the data shape.
If a user wants a different view, they create a new report spec. This keeps the UI
predictable and consistent with what pyegeria already defines.

---

## Implementation Order and Effort

| Phase | Description | Effort | Depends on |
|-------|-------------|--------|------------|
| 1 | GRAPH→JSON/DICT fallback in format selector | XS | — |
| 2 | `SmartReportRenderer` (text tokenizer + anchor fix + bi-di links) | M | 1 |
| 3a | `VegaChart` + unconditional vega-embed load | M | 2 |
| 3b | `AvailableCharts` (scan for `*BarGraph`/`*PieGraph`) | S | 3a |
| 4 | `DictResultView` (spec-driven master-detail table) | M–L | 3b |

Phases 1 + 2 are a natural first commit — no chart library required.  
Phases 3a + 3b add chart rendering cleanly on top.  
Phase 4 is the richest piece; it can be prototyped against a real DICT call to
validate that the spec `attributes` list reliably matches the actual response keys
before finalising.
