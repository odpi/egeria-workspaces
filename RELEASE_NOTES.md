# Since v6.02

Four and a half months, 985 commits, and two demo environments that finally act like siblings.

Since the `v6.02` tag on April 2, `egeria-workspaces` went from a single working demo to a small
constellation of purpose-built apps over Egeria — plus the plumbing, time-travel, bulk actions, and
bug fixes that make them trustworthy. Here's what shipped.

**985** commits &middot; **228** features &middot; **227** fixes &middot; **4.5** months

## Try it

- **Live demo, no install** — **[egeria.pdr-associates.com](https://egeria.pdr-associates.com)**. Register
  free, pick a Coco Pharmaceuticals persona, explore in your browser.
- **Run it yourself** — [Getting started](https://github.com/odpi/egeria-workspaces#getting-started)
  (Quickstart or Freshstart, local via Docker/Podman).
- **Watch** (Egeria Project on YouTube):
  [Quickstart — Egeria up and running in under 2 mins](https://www.youtube.com/watch?v=1Sfu5mHA1u8) &middot;
  [Accessing Egeria's Demo Environment](https://www.youtube.com/watch?v=JV2UdEo1k8A) &middot;
  [Egeria Workspaces](https://www.youtube.com/watch?v=igIVACD4b_g)

---

## Apr–May: the portal, and the first tool worth living in

The period opens with QuickStart already running, and Freshstart — the clean-slate, bring-your-own-metadata
sibling environment — still mostly scaffolding. Most of April and May went into turning Egeria Explorer from
a type browser into the app people actually reached for, and giving both environments a real front door.

- Egeria Explorer's type hierarchy now builds **dynamically from the live Egeria type system** instead of a
  hardcoded tree, with domain grouping, abstract-type filtering, and inherited-method display.
- **Element-level Favorites** rolled out across terms, report specs, digital products, data assets, and six
  more sections — persisted in Egeria itself via `ActorManager` against the user's own Person element, not a
  side database. Later renamed to **Bookmarks** with delete support.
- Egeria native **Likes, Ratings, and Comments** landed on every detail pane, alongside a separate
  **user-feedback widget** ("how's this page working for you?") that persists to Postgres — two distinct
  feedback systems, kept deliberately apart.
- The demo portal got a real shape: grouped nav dropdowns, a **persona picker**, a **local-admin panel** for
  small-team deployments, and a **`--demo`** mode with its own account flow, welcome email, and verification.
- **Obsidian** arrived as a portal tile, running Dr.Egeria markdown against a Coco Pharmaceuticals vault via a
  session-locked container.
- **my-egeria** — a Textual TUI, served over the browser via `textual_serve` — joined the portal as its first
  non-React tile.

## May–Jun: three more apps, and time travel for all of them

Egeria Explorer stopped being the only tool. Three purpose-built apps shipped in quick succession, and a
cross-cutting capability — asking "what did this look like on a given date" — got wired into nearly every
list and detail view across the whole portal.

- **The Catalog** *(since Jun 6)* — a dedicated technical asset catalog: infrastructure, data assets, APIs,
  and processes, with tabular data preview, schema/lineage sub-panes, and classification-based sidebar
  filtering.
- **Egeria Operations** *(since Jun 22)* — governance engines, engine actions, and integration connectors in
  one place, with a resizable docked side panel and a non-blocking cache so a slow connector report never
  hangs the page.
- **Egeria Audit** *(since Jun 22)* — platform users, accounts, and a shared bidirectional relationship
  viewer, built around a new cross-app resolver every later app reused instead of inventing its own.
- **Lineage Explorer** *(since Jun 11)* — data lineage centred on a focus asset, with a shared time-slider
  component extracted here first and later reused across the portal.
- **`as_of_time`** ("time travel") shipped for the Data Assets detail pane, Digital Products and Collections
  trees, Locations, Communities, Perspectives, Glossary, Projects, and Actors — one view at a time, each
  verified against real before/after data, not just accepted-and-ignored parameters.
- Auth moved off password-bearing URLs: a shared `egeria_auth.py` token seam, then a cross-app `egeriaFetch`
  helper with automatic 401 retry, replacing `user_id`/`user_pwd` query params everywhere.
- **Self-hosted Kroki** replaced pyegeria's hard dependency on the public kroki.io for Mermaid rendering in
  Jupyter — fixing the intermittent crashes and drifting diagram colors that came with sharing someone else's
  multi-tenant renderer.

## Jul: governance search, and a dashboard model built to last

July's two headline efforts: a proper cross-cutting governance search app, and the start of building
dashboards as real, declarative metadata instead of hand-wired React state — the piece that made everything
after it in Egeria Overview possible.

- **Egeria Insights** *(since Jul 15)* — classification- and zone-faceted governance search over Egeria's
  native `find_metadata_elements`, with a dashboard tab and compound AND/OR search. Later renamed **Query**
  to match what it actually does.
- **Egeria Overview** *(since Jul 22)* — a KPI dashboard for the whole demo (assets, governance coverage,
  growth, business value) built on a new architecture rather than a page of hand-coded numbers.
- The dashboard architecture: KPI tiles as real pyegeria `FormatSet` objects (single source of truth), a
  `Container`/`Placement` model so a "perspective" is a genuine filtered lens rather than a second hardcoded
  list, and a **Vega-Lite chart engine** (line, area, scatter, funnel generators) chosen over Mermaid for
  anything that isn't a diagram.
- **Naming Vocabulary, Policy Enforcement, Action Center, and Duplicate Review** panes shipped — closing four
  of the type-coverage gap-analysis's open items.
- **Run Dr.Egeria documents from the browser** — validate or process a markdown command file with no
  `docker exec` required, plus a structured execute-result panel with real error classification instead of a
  wall of text.
- Global search grew a **type-faceted, physical/logical semantic bridge** and combinable property-value +
  classification + relationship conditions — the same backend later promoted to a portal-level omni-search
  bar.

## Aug: user-authored dashboards, bulk governance, and closing the gap

August pushed the reporting model out to actual users — dashboards anyone can build from a markdown file —
while a parallel thread went back through Freshstart line by line to close the gap that four months of
quickstart-first development had opened up.

- **Local Dashboards** — a portal tile for browsing and running user-authored Dashboard Sheets, with inline
  execution, KPI-tile rendering with sparklines, drill-down navigation, viewer-facing parameter overrides,
  and a caching layer once all of that made every page load slow.
- **Governance Metrics browser** (Tier 1 of a 3-tier lineage design) — real `GovernanceMetric` elements
  linked to a Report, each with an Information Supply Chain documenting its conceptual data flow.
- **Bulk actions** grew from collection add/remove to **zone membership** and then
  **classify/declassify** (Confidentiality, Criticality, Impact) — propagated to roughly thirty list views,
  then ported to Freshstart in full.
- **HTTPS by default** across every deployment mode (local and multi-host, both environments), with automatic
  HTTP→HTTPS redirect and a Let's Encrypt fallback for `--demo`.
- A systematic **Freshstart parity audit** found and fixed real accidental drift — a stale MCP API, missing
  cache headers, a silently-broken async-token pattern reintroducing the exact `RuntimeError` class this
  repo's own conventions exist to prevent — alongside confirming most of the remaining divergence is
  legitimately by-design (auth model, branding, container names).
- Cross-machine **demo data sync** for users and feedback, so two machines running the same demo don't drift
  apart.

## Underneath all of it

- **227 fixes** landed alongside the 228 features — real production concerns, not polish: a Postgres
  connection leak that periodically took Operations offline, a stale-bind-mount class of bug that made config
  edits silently not take effect, browser-cache issues that turned a shared-JS edit into a blank page for
  anyone with an old cached copy, and a recurring pattern of pyegeria methods that accepted `as_of_time` and
  silently ignored it.
- The **`egeria-shared-ui.js`** component library grew from an idea into the real dependency both
  environments' five-plus apps now import from, closing years of copy-paste drift between quickstart and
  freshstart on the components that matter most.
- The host-port scheme was renumbered onto a clean, collision-free **88xx / 78xx** block, freeing the problem
  port 8000 and giving quickstart and freshstart the same last two digits for the same service.

**Commits by author:** 881 — Dan Wolfson &middot; 60 — Mandy Chessell &middot; 7 — Claude

---

## Where the detail lives

This is the shape of it, not the whole thing — 985 commits don't fit in a release note. The blow-by-blow,
including root causes and what was tried and rejected along the way, lives in `BACKLOG.md` for anything
still open and `BACKLOG-ARCHIVE.md` for everything closed.

*egeria-workspaces &middot; v6.02 → today &middot; compiled from git history*
