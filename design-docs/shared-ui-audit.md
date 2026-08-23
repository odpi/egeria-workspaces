# MOD-1 — Shared UI Audit (Egeria Explorer ↔ Tech Catalog)

> ## ✅ Final state — MOD-1/2/3 complete (2026-06-20)
>
> `egeria-shared-ui.js` is loaded by both SPAs (served as a FastAPI static file,
> `<script>` before each app script; the two env copies stay byte-identical).
> Components are plain globals referenced by name, resolved at render time.
>
> **Shared module inventory** (`static/egeria-shared-ui.js`):
> - **Mermaid family:** `_MERMAID_FIELD_LABELS`, `_MERMAID_SECTION_FIELDS`,
>   `MermaidDiagram`, `DiagramPanelFromData`, `AvailableMermaidDiagrams`,
>   `DiagramPanel`, `MermaidSection` (the last two token-aware via CredContext).
> - **Markdown:** `renderMd` / `_renderMdHtml` (+ `--md-code-bg` CSS var).
> - **Layout/util:** `useResizable`, `ResizeDivider`, `copyToClipboard`
>   (execCommand fallback for non-secure http).
> - **Glossary:** `GlossaryTermRow`, `GlossaryTreeNode` (tree, injected `fetchJson`);
>   `GlossaryFolderDetail`, `GlossaryDetail`, `GlossaryTermDetail` + `_glsBadge`
>   (detail panes, Catalog visual design; term pane takes optional cross-link
>   callbacks + an injected `isElementLinkable` predicate).
> - **Feedback:** `EgeriaFeedbackWidget`, `EgeriaCommentsSection`, `FeedbackButton`
>   (+ `_SESSION_ID`).
> - **Auth seam:** `CredContext` (shared context — **both** SPAs now provide it via
>   `CredContext.Provider value={creds}`), `egeriaFetch` + `_tokenRefresher`
>   (token-aware; `url`/`server`/`user_id` as query params, `X-Egeria-Token` header,
>   password never in a URL).
>
> **Stays per-tool (Tier 3):** `ConnectionForm`, each App's `CredContext.Provider`
> wiring + creds state, and all tool-specific views/sections/splash/nav. Note: the
> `CredContext` *object* is shared; only the *provider value* is per-SPA.
> `VegaChart`/`AvailableCharts` remain Explorer-only (not needed by the Catalog).
>
> **Cross-tool nav:** the Catalog has no Data Design / Digital Products tabs, so it
> deep-links the Egeria Explorer via `TYPE_TO_NAV` + `handleNavigate`
> (`/egeria-explorer?guid=&kind=#<tab>`); the Explorer's `DataDesignView` /
> `DigitalProductsView` seed their selection from `?guid`/`?kind` on cold load.
>
> The original audit and recommendation below are retained for history.

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

### Tier 2 — ✅ DONE (2026-06-19/20)
- `EgeriaFeedbackWidget`, `EgeriaCommentsSection`, `FeedbackButton` (+ `_SESSION_ID`)
  all now live in `egeria-shared-ui.js`.
- **Resolution:** the feared blocker never bit. The Egeria-feedback widgets call
  the cookie-authed `/api/egeria-feedback/*` with bare `fetch()` (no creds in the
  call), and `FeedbackButton` posts to `/api/demo-feedback` the same way — so none
  of them embed the token-vs-query-param seam. The `egeriaFetch` unification from
  LE-4 phase 3 covered the data-fetching paths; the feedback components never
  needed it. Canonical = the richer Egeria Explorer `FeedbackButton`; the Catalog's
  stripped-down copy was retired in favour of a `pagePrefix="tech-catalog/"` prop.
- `credAppend` was removed entirely in LE-4 phase 4 (dead after `egeriaFetch`).

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
