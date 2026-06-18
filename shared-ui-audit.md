# MOD-1 — Shared UI Audit (Egeria Explorer ↔ Tech Catalog)

**Goal:** identify components/helpers duplicated between `type-explorer.html`
(Egeria Explorer SPA) and `tech-catalog.html` (Tech Catalog SPA), and define the
boundary for what moves into a shared `egeria-shared-ui.js` (MOD-2) vs what stays
per-tool.

**Method:** extracted every `function Name(...) { … }` body from both SPAs
(brace-matched), normalised whitespace, and compared. The minified React UMD
bundle accounts for ~400 single/two-letter "common" names — ignored. The
meaningful shared candidates are below.

---

## Inventory

| Component / helper | In Explorer | In TechCat | Diff | Notes |
|--------------------|:-----------:|:----------:|------|-------|
| `MermaidDiagram` | ✅ | ✅ | diverged | Explorer is the superset (mermaid-load retry/poll + error fallback `<pre>`); both now have the "⧉ Copy source" button. **Canonical = Explorer.** |
| `MermaidSection` | ✅ | ✅ | **identical** | Lazy `/api/.../mermaid` fetch panel. |
| `DiagramPanel` | ✅ | ✅ | diverged (minor) | Same shape; small wording/field differences. |
| `DiagramPanelFromData` | ✅ | ✅ | diverged (minor) | Near-identical. |
| `AvailableMermaidDiagrams` | ✅ | ✅ | diverged (minor) | Driven by the `_ALL_*MERMAID_FIELDS` / `_MERMAID_FIELD_LABELS` constants (present in both). |
| `_ALL_*MERMAID_FIELDS`, `_MERMAID_FIELD_LABELS` | ✅ | ✅ | drift-prone | Two copies that must be kept in sync by hand today — prime single-source candidate. |
| `ResizeDivider` | ✅ | ✅ | diverged (minor) | Layout primitive. |
| `useResizable` | ✅ | ✅ | diverged (minor) | Layout hook. |
| `renderMd` / `_renderMdHtml` | ✅ | ✅ | diverged | Explorer's `renderMd` is the richer superset; TechCat carries `_renderMdHtml` already commented "shared with type-explorer.html". **Canonical = Explorer.** |
| `credAppend` | ✅ | ✅ | diverged (equivalent) | Both append `url`/`server`/`user_id`; Explorer delegates to `credQS`, TechCat inlines `URLSearchParams`. |
| `EgeriaFeedbackWidget` | ✅ | ✅ | identical* | *body identical, but the fetch/auth path differs (see blocker). |
| `EgeriaCommentsSection` | ✅ | ✅ | diverged | Comment CRUD; differs in fetch/auth path. |
| `FeedbackButton` | ✅ | ✅ | diverged | Per-page user feedback; differs in fetch/auth path. |
| `ConnectionForm` | ✅ | ✅ | diverged | Auth seam — intentionally tool-specific. |
| `CredContext` | ✅ | ✅ | concept shared | Each SPA provides its own provider; shared components only *consume* it. |
| `VegaChart`, `AvailableCharts`, `CollapsibleChartPanel` | ✅ | ❌ | Explorer-only | Report-rendering charts; not yet needed by TechCat but tool-agnostic → eligible for the shared module. |

---

## Boundary (three tiers)

### Tier 1 — share now (pure presentation, no backend coupling)
Lift the **richer Explorer version** as canonical; zero auth/token dependency:
- Mermaid family: `MermaidDiagram`, `MermaidSection`, `DiagramPanel`,
  `DiagramPanelFromData`, `AvailableMermaidDiagrams` **+** the
  `_ALL_*MERMAID_FIELDS` / `_MERMAID_FIELD_LABELS` constants (single source).
- Layout: `ResizeDivider`, `useResizable`.
- Markdown: `renderMd` / `_renderMdHtml`.
- Charts (ready for reuse): `VegaChart`, `AvailableCharts`, `CollapsibleChartPanel`.

These are the immediate win — e.g. the "Copy source" button I just had to add to
**both** SPAs separately would be a one-line change in the shared module.

### Tier 2 — share *after* unifying the fetch/auth model
- `credAppend`, `EgeriaFeedbackWidget`, `EgeriaCommentsSection`, `FeedbackButton`.
- **Blocker:** the two SPAs talk to the backend differently — Tech Catalog uses a
  token wrapper (`fetchWithToken` + `X-Egeria-Token`, ~19 refs) while Egeria
  Explorer uses query-param credentials (0 token refs). The feedback components
  embed that difference. Sharing them cleanly needs a single shared fetch helper
  (e.g. `egeriaFetch(url, creds)`) that handles both token and query-param modes.
  This dovetails with **LE-4** (move handlers to token-only) — sequence MOD-2 Tier 2
  with that migration.

### Tier 3 — stays per-tool
- `ConnectionForm` (auth seam), the `CredContext` *provider* wiring, and every
  tool-specific view/detail/section/splash/nav component.

---

## Dependencies a shared module must assume

Shared components reference these — both host SPAs must provide them (or the
shared bundle must include them):
- **CSS custom props:** `--accent --border --panel --dim --muted --text --hover --fg`.
- **CSS classes:** `.mermaid-wrap`, `.spinner` (consider moving shared CSS to a
  companion stylesheet so it doesn't drift either).
- **Globals:** `React` (+ hooks), `window.mermaid`, `vegaEmbed` (only for charts),
  the markdown lib used by `_renderMdHtml`.
- **`CredContext`** — consumed via `React.useContext`; each SPA supplies the provider.

---

## Recommendation for MOD-2 / MOD-3

1. Create `egeria-shared-ui.js`, served as a FastAPI static file, loaded via a
   plain `<script>` **before** each SPA's app script. Expose on a namespace
   (`window.EgeriaUI = { MermaidDiagram, renderMd, ResizeDivider, … }`) to avoid
   global collisions.
2. **MOD-2 step 1:** move Tier 1 (zero coupling) + the mermaid field constants.
   Refactor both SPAs to consume them; delete the duplicated blocks. Verify each
   SPA still loads (JS check) and mermaid/markdown/charts render.
3. **MOD-2 step 2:** introduce `egeriaFetch` (token-or-query-param), then move
   Tier 2 feedback components on top of it — coordinate with LE-4.
4. Keep Tier 3 per-tool.
5. Move shared CSS (`.mermaid-wrap`, `.spinner`, and the custom-prop palette) into
   a shared stylesheet to remove the parallel CSS drift too.

**Expected payoff:** the backlog estimates ~25–30% size reduction per SPA, and it
ends the "edit the same component in two files (× two envs)" tax — the single
biggest source of drift in this codebase.
