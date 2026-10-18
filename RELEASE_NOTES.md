# Egeria Workspaces 6.2

Seven weeks, 686 commits, and an Overview dashboard that now shows only what it has actually measured.

Since the `v6.1` tag on August 20, `egeria-workspaces` has been about trust and operability: dashboards that
stop inventing numbers, a portal with one consistent frame and a global Promise/Memento toggle, a
bootstrap process that loads Dr.Egeria content as the right people, and a quickstart that heals itself
and survives a reboot. It aligns with **Egeria 6.2** and **pyegeria 6.2.0**. **This is the 6.2 release.**

**6.2** &middot; **686** commits &middot; **45** features &middot; **93** fixes &middot; **1.6** months

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

## Late Aug: a platform that heals, and bootstrap you can watch

After 6.1 the first job was making the stack harder to knock over and easier to see into.

- **Auto-heal for unhealthy containers** in the shared infrastructure, with alerting, plus restart policies
  on every Freshstart service (it had none) and a `egeria-main` healthcheck that can now actually fail.
- **Let's Encrypt issuance and renewal fixed**, with a cert-watch notifier and SANs preserved across renewals.
- **Bootstrap runs batches in the background and polls for completion**, logs per-file outcomes, and adds an
  **Activity Log** tab and a **Recent Activity** panel for `bootstrap.log` in the admin area. Orphaned
  `dr_egeria` subprocesses are killed on timeout or cancel.
- **Design patterns** gained a load-order manifest and a viewer in Solution Architect; the Coco workbook
  scenario folders are linked into the Dr.Egeria inbox with their source numbering.
- A **capability hierarchy** screen and governance-process drill-down for QuickStart; the superseded
  GovernanceStrategy group is hidden from the governance tree.
- Slow list endpoints got caches or cheaper queries: Operations engine actions, collection roots, and
  governance definitions (graph depth 0).
- Every list pane that lacked one now has a **Refresh** button, mirrored into Freshstart.

## Early Sep: security hardening and the Egeria Advisor / Resource Explorer tiles

- **Security fixes** in the REST API and dashboards: path-traversal guards, an SSRF guard on OpenAPI spec
  fetch, lexical validation of `http_collections_path`, and no more raw exception text returned to clients.
  The repository was also hardened against OpenSSF Scorecard checks.
- **Omni-search** now includes REST API endpoints and pyegeria classes and methods.
- **Egeria Advisor and Resource Explorer** (both marked Alpha) work from the portal: SSO handoff fixed,
  optional HTTPS vhosts, wildcard certificates via DNS-01, tile URLs derived from the request, and the
  Advisor's exclusive-access lock removed.
- **Trellis** can reach Egeria from all three services, and there is a guide to deploying it with the QuickStart.
- Performance and tuning: the platform JVM and shared Postgres were retuned off stock defaults, Kafka
  retention and heap settings now take effect, the parentless-collections list dropped from 46.6 s to 12.5 s,
  and the Catalog's Annotations tab no longer times out at 90 s.
- **`jdbcMaximumPoolSize`** is set in the server-config template, addressing HikariPool connection-pool timeouts.
- The nightly demo reset is visible instead of looking like an outage; the Portal restarts after a reboot and
  keeps the alert address; a cached persona no longer carries across Portal accounts.

## Mid Sep: Explorer, Data Mesh, and docs

- **Data Mesh** app for the Digital Products graph, with wrapped labels and a roughly 17x faster load.
- **Egeria Explorer**: a new **Namespaces** tab, Collections fixes, Governance Process properties, the ISC
  Mermaid mismatch fixed, lists alphabetised, and detail views now default to graph depth 5.
  Relationship lists show the real relationship type instead of a misleading "Appointments" suffix.
- **Project classifications** (including ProjectKind) were always empty and now display.
- **Local Dashboards** gained a Digital Product and Subscription tutorial and generic analytic report specs.
- Dr.Egeria templates were regenerated several times to follow pyegeria attribute changes, with new
  Curation, Investigation, NamingStandardsVocabulary, subscription, data contract, and data product templates.

## Late Sep–Oct: one portal frame, Promise/Memento, and honest Overview data

- **One shared app bar on every portal app**, and a **My Profile** app served from the portal.
- **Global Promise/Memento (`forLineage`) toggle**, on by default, to show or hide Promise and Memento
  elements, also available on the Data Mesh view. It is per tab and page, restores the selected item in
  Explorer and the Tech Catalog, and is hidden on the Explorer home.
- **Time sliders reach back to the oldest element in view.**
- **Detail panes paint faster**: solution blueprint and component detail show a quick depth-1 view first,
  the component tree comes from a single relationships call, and list-everything-and-filter fallbacks
  were replaced.
- **Egeria Overview now shows real data only.** KPI tiles show a dash rather than a sample number, static
  markup no longer ships invented content, and section badges follow what loaded. New live KPIs cover
  quality, schema, confidentiality, **survey coverage** (failed surveys are distinguished from successful
  ones; coverage counts completed surveys only), survey freshness, data stores by kind, engine-action
  health, **assets by technology**, and **recent activity** from curated content types (people's changes only).
  Queries run as the persona picked in the Portal, and the header chip says whom the data is for.
- **Coco Pharmaceuticals Video Blog** box on the portal home.
- **Data Initialization recurses into subfolders** ([#618](https://github.com/odpi/egeria-workspaces/pull/618)):
  `_batch.json` can order subfolders and use an `exclude` field; a per-file or per-folder `userid` loads
  content as the owning persona; each file runs once per pass; the admin panel shows a run ledger and
  validation notes; the Coco workbooks are ordered from their READMEs. See `DR_EGERIA_AUTO_LOADING_GUIDE.md`.

## Underneath all of it

- **93 fixes** alongside 45 features. Among them: a proxy header bug (invalid `X-Forwarded-Host`) that broke
  tile URLs, Promise/Memento toggling that lost the Tech Catalog section, Lineage Explorer search that could
  not tell "searching" from "no results", and the Supply Chains list that was slow to load.
- **pyegeria tracking**: `quick-start-local` and `fresh-start-local` install the latest pyegeria on every run
  unless pinned; a new `--refresh-pyegeria` flag busts cached layers; the Jupyter dual-install gotcha is
  documented and fixed. pyegeria 6.2.0 is released alongside this release, so images pick it up on
  their next build.
- **Egeria 6.2**: platform images are pinned to `odpi/egeria-platform:6.2` rather than a moving digest, and
  Overview reads survey findings correctly given 6.2's annotation reuse.
- Prefect (optional) upgraded to 3.8.6; the Airflow scheduler health server is enabled; a
  `reset-egeria-db.sh` helper was added.

**Commits by author:** 470 — Dan Wolfson &middot; 164 — Mandy Chessell &middot; 52 — dependabot[bot]

---

## Upgrade notes

- **Data Initialization now loads files as persona users.** Files and folders can name a `userid`. Each
  user's password comes from `EGERIA_BOOTSTRAP_PASSWORD_<USERID>`, then `EGERIA_USER_PASSWORD`, then `secret`.
  Subfolders are now processed, so review your `_batch.json` files; `DR_EGERIA_AUTO_LOADING_GUIDE.md` explains how.
- **Overview no longer shows placeholder numbers.** A dash means "not measured yet", not zero.
- **Promise/Memento elements are shown by default.** Use the toggle in the app bar to hide them.
- **pyegeria is no longer pinned by default** in `quick-start-local` / `fresh-start-local`; pin it explicitly
  if you need a fixed version.
- **Platform images are pinned to `odpi/egeria-platform:6.2`.** Rebuild the `egeria-main` image to move to it.
  `--refresh-platform` re-pins to the newest `latest` image instead, which takes you off 6.2.

## Where the detail lives

This is the shape of it, not the whole thing — 686 commits don't fit in a release note. The blow-by-blow,
including root causes and what was tried and rejected along the way, lives in `BACKLOG.md` for anything
still open and `BACKLOG-ARCHIVE.md` for everything closed.

*egeria-workspaces 6.2 &middot; v6.1 → 6.2 &middot; compiled from git history*
