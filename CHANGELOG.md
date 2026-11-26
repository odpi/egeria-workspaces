# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Dr.Egeria templates for solution boundaries** ([#927](https://github.com/odpi/egeria-workspaces/pull/927)): *Create Solution Boundary* and *Create Design Model Boundary*, basic and advanced, under `templates/*/Solution Architect/`, copied unchanged from egeria-python v6.3.4. They need pyegeria 6.3.4 and an Egeria platform with odpi/egeria#9465. Members are added with the Collection Membership commands, and Egeria refuses to delete a boundary that still has members. **Known issue (egeria-python #613):** on an Update, give the Version Identifier, Qualified Name or GUID; an Update that names only the Display Name can create a duplicate. `templates/README.md` and the Portal's advanced templates page say so.
- **A Roles tab for solution roles on the Solution Architect page**, quickstart ([#923](https://github.com/odpi/egeria-workspaces/pull/923)) and freshstart ([#924](https://github.com/odpi/egeria-workspaces/pull/924)). A `SolutionActorRole` is an `ActorRole` by supertype, so links to one used to land on the Actors card. It now has its own card, with "Who holds it" and "Also a member of", served by `/api/solution/roles` and `/api/solution/roles/{guid}`.
- **Egeria 6.4 cards in the Explorer and The Catalog** ([#911](https://github.com/odpi/egeria-workspaces/pull/911)): a Decisions section in Egeria Explorer, and Configuration Values (`DataValue` / `LiteralDataValue`) and Models and Runs (analytics models and model runs, with parameters, results and signature) in The Catalog. Existing cards show an element's Egeria 6.4 links and a Branch badge. On an Egeria 6.3 platform these say they need 6.4. The Type Coverage Registry is regenerated for Egeria 6.4.
- **Helm charts for Kubernetes and OpenShift** (`charts/`, TR-112: [#908](https://github.com/odpi/egeria-workspaces/pull/908), [#909](https://github.com/odpi/egeria-workspaces/pull/909), [#915](https://github.com/odpi/egeria-workspaces/pull/915), [#916](https://github.com/odpi/egeria-workspaces/pull/916)): `egeria-platform`, `egeria-portal` (Portal and Apache front door, on new non-root images), the `egeria-stack` umbrella, `trellis-re` (Resource Explorer web, worker and schema Job, with optional Prefect worker and A2A role), demo PostgreSQL and Kafka, and a shared `egeria-common` library. A production posture refuses the public demo keystore password; `helm test` runs a canary; `charts/docs/` has deployment, configuration, operations, OpenShift and testing guides.
- **SMTP mail for the demo Portal** when Resend is not configured ([#911](https://github.com/odpi/egeria-workspaces/pull/911)): `SMTP_HOST`, `SMTP_PORT`, `SMTP_SSL`, `SMTP_USER`, `SMTP_PASSWORD` and `SMTP_FROM`. `gen-env.sh` keeps the mail settings when it rewrites `.env`.
- **A script to prune old Airflow run log directories** in `optional-associated-runtimes/airflow-marquez/` ([#905](https://github.com/odpi/egeria-workspaces/pull/905)). Airflow keeps no file-log retention of its own.

### Changed
- **The quickstart Egeria platform is pinned to the 6.4-SNAPSHOT build that has solution boundaries** (odpi/egeria#9465), by digest `sha256:5a8d6a12…0309f`, instead of the released 6.3 ([#925](https://github.com/odpi/egeria-workspaces/pull/925)). The freshstart platform Dockerfile and the `egeria-platform` Helm chart use the same pin, and the multi-host scripts and `fresh-start-local --refresh-platform` now re-pin the tag in the Dockerfile's `FROM` line, so they stay on that snapshot instead of moving back to 6.3 or `latest` ([#926](https://github.com/odpi/egeria-workspaces/pull/926)).
- **Published ports also answer on IPv6** ([#926](https://github.com/odpi/egeria-workspaces/pull/926)). With `--lan` or `--demo` on Docker, on a host with IPv6, the start scripts add `egeria-quickstart-ipv6.yaml` or `egeria-freshstart-ipv6.yaml`, so a host name that resolves to an IPv6 address no longer gives intermittent "network error"s. `EGERIA_BIND_IP6=none` turns this off.
- **The shared Kafka broker is 4.4.0** (was 4.1.1, [#918](https://github.com/odpi/egeria-workspaces/pull/918)). The image's Kafka home is `/opt/kafka` and the broker runs as uid 1000. On Linux, an existing installation's Kafka data must change owner before the first start; see *Kafka image versions* in `compose-configs/shared-infra/README.md`.
- **The pyegeria floor is 6.3.4** ([#927](https://github.com/odpi/egeria-workspaces/pull/927)) in both Portal `requirements.txt` files and every `PYEGERIA_VERSION` default (Portal fast-api and portal images, Apache web images, Jupyter, My Egeria). It was raised to 6.3.3 on 2026-11-24 ([#917](https://github.com/odpi/egeria-workspaces/pull/917)), and My Egeria to 6.3.2 ([#910](https://github.com/odpi/egeria-workspaces/pull/910)).
- **Freshstart's Portal shares four files with quickstart's** (SHARE-3 phase 1, [#906](https://github.com/odpi/egeria-workspaces/pull/906), [#913](https://github.com/odpi/egeria-workspaces/pull/913)): `perspectives_handler.py`, `type_system_handler.py`, `digital_products_handler.py` and `static/egeria-shared-ui.js`. Quickstart's copy is canonical; `compose-configs/sync_shared_portal_files.py` writes the mirror and a test fails on drift. Freshstart gains the quickstart features in those files, such as classification purposes and the digital products mesh.
- **The Resource Browser finds code repositories that Resource Explorer publishes as `SourceControlLibrary`** ([#904](https://github.com/odpi/egeria-workspaces/pull/904)).
- **The PyegeriaWebHandler images no longer bake in local leftovers** ([#927](https://github.com/odpi/egeria-workspaces/pull/927)): a `.dockerignore` in the quickstart and freshstart build contexts leaves out `logs/`, `debug_log.log`, `__pycache__/` and `.pytest_cache/`.

### Fixed
- **`quick-start-local --demo` on a host with IPv6 no longer publishes JupyterHub on `[::]:8888`** ([#926](https://github.com/odpi/egeria-workspaces/pull/926)). The IPv6 overlay is now added before `egeria-quickstart-demo.yaml`, whose port resets then also remove the IPv6 entries.
- **Freshstart Portal fixes** ([#905](https://github.com/odpi/egeria-workspaces/pull/905)): the home page points at freshstart's ports, not quickstart's (PO-61); `/api/collections/by-type` is served (PO-60); the Perspectives list and detail routes work again (PO-59).
- **Portal fixes** ([#911](https://github.com/odpi/egeria-workspaces/pull/911)):
  - The Catalog lists only an asset's own relationships, not every relationship in its subgraph.
  - Dr.Egeria execute runs as the sign-in token's user (PO-20, PO-21).
  - Egeria's 403 is told apart from a refused sign-in by exception class and code, not message text, so operations, glossary and The Catalog no longer answer every auth error with "session expired" (PO-9).
  - Insights' exhaustive searches page to an empty page, not a short one, and a complete count is not called "exact".
  - Statements of Applicability are linked from other screens (PO-23); a collection's non-collection members open (PO-24).
  - The Resource Locator page is served with `Cache-Control: no-store`.
- **The Overview's karma leaderboard says when it could not be read**, instead of "Loading…" for good (PO-86, [#917](https://github.com/odpi/egeria-workspaces/pull/917)).

### Security
- **The freshstart Portal has a server-side sign-in gate** (PO-78, [#912](https://github.com/odpi/egeria-workspaces/pull/912)). Before it, a read route answered a caller with no session as the Portal's service user.
- **`/api/egeria-token` needs a signed-in user when no password is sent** (PO-68, [#907](https://github.com/odpi/egeria-workspaces/pull/907)). On freshstart, an empty request used to mint a token for the service user.
- **Neither stack publishes its MCP token** (PO-79, PO-82, [#914](https://github.com/odpi/egeria-workspaces/pull/914)). `MCP_ACCESS_TOKEN` is generated into `.env` and kept; the value that used to be published is refused; on freshstart, unset means MCP is off.
- **The auth routes are rate-limited again, per real client IP** (PO-83, [#914](https://github.com/odpi/egeria-workspaces/pull/914)). In the Helm chart the Portal trusts `X-Forwarded-For` only from its Apache pods ([#915](https://github.com/odpi/egeria-workspaces/pull/915)).
- **Freshstart's caches key on the presented credential**, not a bare `?user_id=` (PO-80, [#914](https://github.com/odpi/egeria-workspaces/pull/914)).
- **Report-spec reads run as the signed-in user**, and the report-spec sync status names no skipped spec or zone to non-admins ([#911](https://github.com/odpi/egeria-workspaces/pull/911)).
- **With no token and no sign-in required, Dr.Egeria uses the service password, never a built-in one** ([#911](https://github.com/odpi/egeria-workspaces/pull/911)).
- **`quick-start-local --demo` no longer echoes the Resend API key** as it is typed ([#911](https://github.com/odpi/egeria-workspaces/pull/911)).

## [6.3] - 2026-11-19

This release goes with Egeria 6.3 and needs pyegeria 6.3.0 or later. [RELEASE_NOTES.md](RELEASE_NOTES.md) summarizes the main changes.

### Added
- **`egeria-upgrade-reset`, a host-only CLI for upgrading or resetting the quickstart Egeria** (`compose-configs/egeria-quickstart/bin/`). `plan` reads the state and changes nothing; `apply` runs the steps, resumably, with each step's evidence in a state file: disk check (15 GB), re-pin and build (with a rollback tag), stop RE and EA, stop the platform, a verified backup (gzip test, end marker, sha256), the clear (checkpoint: type the database name; SQL shared with `reset-egeria-db.sh` in `reset-egeria-db.sql`), a secrets sync that prints account names only (while the platform is stopped), `compose up --force-recreate` on the new image (never `docker start`) with the stale-mount check before the heal can start, the heal wait, restarting RE and EA through their launcher scripts (or marking the step for a person), read-only checks (PASS / FAIL / NOT MEASURED, and CHANGED for a classification count that moved with a new image) and a record. It refuses to run from another checkout than the deployment's unless told to. Run-once steps need `--redo` and the step's name typed. The Portal's **Admin → Data Initialization** shows the last reset, read only (`GET /api/admin/egeria-resets`, table `demo.egeria_resets`). See *Upgrading or resetting the quickstart Egeria*.
- **After an Egeria reset, the hand-run seeds now heal on their own.** Data Initialization gains two batches: `egeria-held-specs` (the report-spec consumer folders, then the Portal's held specs; safe to re-run) and **Security**. **Useful Dashboards** is on by default (owner: "Yes, ON (Recommended)"). `_folder_order.json` runs Dashboard Folders, then `egeria-held-specs`, then Useful Dashboards. Each of these batches' canary is the last element it creates, so a batch that stops part-way shows as not healed. A batch can declare **manual steps**; the saved query behind the Catalog Health "Assets with No Lineage" tile must be refreshed once by a signed-in user, and `/api/bootstrap/status` reports it as done, pending or not checked. The two 2026-11-11 fix-up documents moved to `dr-egeria-archive/2026-11-11/` (never run on a clean Egeria).
- **Tutorials: Report Specs and Analytic Functions**, and refreshed Local Dashboards and Saved Queries tutorials (`portal-docs/tutorials/`). *Report Specs: Local and Held in Egeria* covers user spec files, precedence (local > egeria > builtin), `Create Report Spec`, consumer folders and the sync. *Add and Use Analytic Functions* covers writing a function and registering it in Jupyter, the quickstart Portal, freshstart and Egeria Advisor. Local Dashboards now explains the "not visible to you" tile for a Report in a zone the viewer cannot see. Local Dashboards, the Query tool and the Egeria report-spec sync are marked quickstart only. *Worked Examples* gives several end-to-end examples of different kinds for each area, with input, steps and output.
- **Docs brought up to date for pyegeria 6.2.37/6.2.38 and the Portal changes of 2026-11-11.**
  - *Report Specs* tutorial, new Part C: which output type for which surface (Portal, Trellis and the terminal render; MCP and A2A take un-rendered DICT; JSON is raw Egeria output; at most two levels in a table; TREE-VIEW later); what 6.2.37 changed in rendered output (LIST cells drawn by what the value is, classifications "A, B", `False` and `0` shown, "Showing the first N…; more may exist"); the column settings `render`, `max_items`, `max_lines` and `label`; the opt-in `table_shape="structured"` and `dict_shape="native"`; DOCUMENT output and the DCAT catalog.
  - *Local Dashboards* tutorial and tool page: dashboard folders and "Used by"; how results look in a tile (scrolling tables with a sticky header, line breaks in cells, whole-row caps with "first N of M rows", named hidden columns, the real-scope note); a worked example on the CDO sheet's register tiles; troubleshooting rows for each.
  - *Worked Examples* R6 to R9 (a LIST register with lists in cells, column render settings, native values for a program, a DCAT catalog); *Egeria Explorer* notes on what a result looks like and the type API without `user_id`; *Saved Queries* tile column limit.
- **Report specs are organised by the tools that use them (consumer folders)**. The root collection `RootCollection::ReportSpecs` holds one folder per tool (`ReportSpecFolder::Consumer::<Portal|EgeriaAdvisor|ResourceExplorer|Pyegeria|MyEgeria|Jupyter>`); putting a spec in a tool's folder publishes it to that tool. `egeria-held-specs/REPORT_SPEC_CONSUMER_FOLDERS.dr-egeria.md` builds the tree. The Portal reads `ReportSpecFolder::Consumer::Portal` (the old `ReportSpecFolder::EgeriaPortal`, renamed in place).
  - **Egeria Explorer's Report Specs view** shows a **Used by** chip row on each spec and a consumer filter, including "Used by none". It says "not read" (with the reason) when the consumer folders could not be read, and "not tracked" for built-in and local specs; with pyegeria 6.2.32 or earlier every spec says "not read".
  - See *Upgrade notes* in RELEASE_NOTES.md for other deployments' Egeria.
- **Classifications are organised by Egeria's classification purpose.** Egeria now gives every classification type a purpose too. It has six: Governance, Governance Implementation, Category, Descriptive, Analytical and Management. Each is its own group, followed by any purpose the Portal doesn't recognise ("Not recognised: X") and then "No purpose reported".
  - **Egeria Explorer's Type Explorer:** classification type pages show the purpose and Egeria's description. An entity type's Classifications tab groups by purpose, with purpose filter chips and a Purpose column in the flat view. The sidebar's CLASSIFICATIONS list is grouped into folded purposes.
  - **Detail panels, Data Mesh and The Catalog:** the Classifications section groups an element's classifications by purpose.
  - **Servers that report no purposes** keep the flat lists, with a one-line note.
  - **API:** `/api/types` classifications carry `classificationPurpose` (and `classificationPurposeUnrecognised` for a value the Portal doesn't know), and the new `GET /api/types/classification-purposes` returns the type → purpose map.
  - **Security:** `/api/types`, `/api/types/names`, `/api/types/relationship-purposes` and `/api/types/classification-purposes` no longer take a `user_id` query parameter. With the service password it could sign in as any demo persona; they now use the caller's Egeria token, else the service account.
  - See *Classification purposes* in the Egeria Explorer docs.
- **Relationships are organised by Egeria's relationship purpose** ([#752](https://github.com/odpi/egeria-workspaces/pull/752) and a follow-up). Egeria gives every relationship type a purpose; the portal groups the eleven purposes into six families (Composition, Governance & Description, Organization, Associations, Design & Deployment, Operations) plus Unclassified.
  - **Egeria Explorer's Type Explorer:** relationship type pages show the purpose, Egeria's description and an anchored-graph chip. An entity type's Relationships tab groups by family, with purpose filter chips. The sidebar's RELATIONSHIPS list is grouped into folded families.
  - **Detail panels, Data Mesh and The Catalog:** relationships are grouped into families that start folded and remember being opened. Purpose badges appear where they add information.
  - **Servers that report no purposes** keep the flat lists, with a one-line note.
  - **API:** `/api/types` relationships carry `relationshipPurpose`, and the new `GET /api/types/relationship-purposes` returns the type → purpose map.
  - See *Relationship purposes* in the Egeria Explorer docs.
- **Every column and pane width in the portal can be changed by the user, and is remembered per page.**
  - **Panes:** the shared `useResizable` hook remembers each pane's width and lets it grow to the window width minus 200px; most panes were capped at a fixed 420–900px. All 47 resizable panes use it, including Data Mesh's detail pane (was a private hook capped at 640px).
  - **Tables, grids and drawers:** the new `static/egeria-resize.js`, loaded by every portal page, adds:
    - drag-to-resize table columns (double-click an edge to reset)
    - draggable splits for the dashboard pages' column grids (Overview, Resource Browser, Governance Metrics, Local Dashboards), which still collapse to one column at their responsive breakpoints
    - a draggable left edge on the Overview drawer
  - **New handle:** Egeria Explorer's Python API sidebar (was fixed at 270px).
- **The Catalog's Infrastructure section has a tab for each direct subtype of `Infrastructure`**, read from Egeria's type system, so a newly defined subtype (for example `Equipment`) gets its own tab. An "All Infrastructure" tab is added when Infrastructure has several subtypes or can have instances of its own. New endpoint `GET /api/tech-catalog/infrastructure/types`; `GET /api/tech-catalog/infrastructure` takes `?type_name=` (default `ITInfrastructure`).
- **Egeria Explorer's Type Explorer shows inheritance for relationships and classifications**: the Relationships tab has the same Show inherited toggle as Properties, with an own/total count and an "own" badge. A new Classifications tab lists every classification the type can carry and the type in its supertype chain that makes it valid.
- **`quick-start-local` starts Airflow and Marquez with the demo**: new `--with-airflow-marquez` and `--skip-airflow-marquez` flags (on by default with `--demo`, off otherwise). Their ports stay on `127.0.0.1` even when the demo binds `0.0.0.0`, because Airflow's admin login can run arbitrary code and Marquez has no login. `airflow-marquez.yaml` now maps `host.docker.internal` to the host gateway so Airflow and Marquez reach the shared Postgres on native Docker Engine (Linux).
- **Airflow's OpenLineage events reach Egeria as well as Marquez**: `openlineage.env` defaults to the composite transport (Marquez directly, and Egeria through the shared-infra OpenLineage proxy and the `openlineage.events` Kafka topic). A new "OpenLineage Events" bootstrap batch runs `HarvestOpenLineageEvents::CreateAsCatalogTargetGovernanceActionProcess` to catalog that topic, and the portal's bootstrap monitor redoes it after a demo reset. Airflow's events also carry information supply chain information.
- **Dr.Egeria templates for the Security Officer commands** (`Create Statement of Applicability`, `Link Control Applicability`) and for the Business Capability commands (`Business Capability`, `Business Capability Dependency`, `Digital Support`), with their sections in the portal's `templates-basic` page.
- **Coco Pharmaceuticals content**: security support, sustainability reference data, and more resilient batch loading for the Coco Data Hub, clinical trials and strategic digital products workbooks (0, 1 and 3).
- **Tutorials are part of the Portal Docs**: the Local Dashboards, Digital Product & Subscription and Saved Queries tutorials moved from `PyegeriaWebHandler/` to `portal-docs/tutorials/`, so they are served at `/docs/` with a Tutorials section and overview page on the docs hub. Their screenshots live in `portal-docs/images/`, and the docs viewer now resolves images relative to each page.
- **Saved Queries tutorial** (`portal-docs/tutorials/saved-queries.md`): builds, saves and refreshes a query in the Query tool, then shows its results set on a Local Dashboard through a `Collection Members` report. It has screenshots (`portal-docs/images/saved-query-*.png`), diagrams and links to and from the Local Dashboards tutorial.
- **Coco systems feed Egeria, and Egeria feeds an operational data store** ([#870](https://github.com/odpi/egeria-workspaces/pull/870)).
  Egeria subscribes to the Coco products for people, roles, user identities, departments and locations, and the new
  Airflow DAG `coco_subscriptions_egeria` loads them into Egeria. A new `egeria_ods` database in the shared PostgreSQL,
  with a `provisioner` role, is set up to receive Egeria's own digital products, one table per product; tables arrive
  once Egeria's daily refresh subscriptions run on a schedule. `ensure-shared-infra.sh` runs `init_egeria_ods.sql` on
  every start, creating only what is missing. The Open Lineage Cataloguer's account now defines `publishZones` (empty),
  because from Egeria 6.3 publishing fails for an account that doesn't define it.
- **Dashboards held in Egeria.** Dashboard sheets and their tiles can be held in Egeria as Egeria 6.3 Dashboard
  elements with an owner, behind a token-only dashboards API ([#818](https://github.com/odpi/egeria-workspaces/pull/818)).
  Local Dashboards shows a folder tree of Egeria-held sheets with a Used by row
  ([#829](https://github.com/odpi/egeria-workspaces/pull/829), [#830](https://github.com/odpi/egeria-workspaces/pull/830)).
  Report tiles pin a collection by qualifiedName ([#824](https://github.com/odpi/egeria-workspaces/pull/824)).
  Server-side result and sheet caches keep placements quick
  ([#814](https://github.com/odpi/egeria-workspaces/pull/814), [#815](https://github.com/odpi/egeria-workspaces/pull/815)).
- **Four ready-made dashboard sheets and repository trend tiles** in the demo ([#826](https://github.com/odpi/egeria-workspaces/pull/826)).
- **Report spec declarations, resolution and refusals in the Portal**: each spec shows what it declares, whether it
  can run and why not ([#809](https://github.com/odpi/egeria-workspaces/pull/809)); the Portal supplies a spec's
  inputs by role ([#806](https://github.com/odpi/egeria-workspaces/pull/806)).
- **Resource Browser** phases 1 to 3 and the contents view: a page per resource, search, home, browse, working sets and
  team sharing ([#620](https://github.com/odpi/egeria-workspaces/pull/620), [#621](https://github.com/odpi/egeria-workspaces/pull/621),
  [#622](https://github.com/odpi/egeria-workspaces/pull/622), [#625](https://github.com/odpi/egeria-workspaces/pull/625)).
  **Curation Coverage** tile ([#628](https://github.com/odpi/egeria-workspaces/pull/628)).
- **Overview**: Trellis perspectives, `asset_composition`, background measurement of slow sections
  ([#788](https://github.com/odpi/egeria-workspaces/pull/788), [#793](https://github.com/odpi/egeria-workspaces/pull/793),
  [#790](https://github.com/odpi/egeria-workspaces/pull/790)).
- **Lineage Explorer** hop limit and cut markers ([#749](https://github.com/odpi/egeria-workspaces/pull/749)).
- **Resource Locator**: search on columns, attributes and data fields; several kinds at once; hover help on terms;
  set, change and clear Data Scope; create and edit Data Lenses that govern working sets ([#889](https://github.com/odpi/egeria-workspaces/pull/889)).
- **The Overview marks unconfirmed figures**: "at least N" or "N found", with the reason, when paging can't confirm
  a count read to the end, in the counts, viewer totals and the Ownership and Semantic Grounding tiles
  ([#890](https://github.com/odpi/egeria-workspaces/pull/890)).
- **Resource Locator follow-ups**: Browse by folder, search keyword and category; glossary terms as a search kind;
  Browse lists filtered by a Data Lens; select several results and add them to a working set; a breadcrumb back to the
  list with its search, filters, scroll and Show-more rows; "Resource Locator Home"; a Data Scope year, month or day means the whole of it;
  emptying a scope or pressing Clear clears it, after asking ([#893](https://github.com/odpi/egeria-workspaces/pull/893), [#894](https://github.com/odpi/egeria-workspaces/pull/894)).
- **Working sets**: called "working set" throughout (PO-42); the owner can delete one after a plan and a confirm, members
  are never deleted, and Resource Explorer's own sets are refused (PO-43, [#895](https://github.com/odpi/egeria-workspaces/pull/895)).
- **Mermaid Expand viewer** ([#781](https://github.com/odpi/egeria-workspaces/pull/781)).
- **Filter and sort** on long relationship and property lists, and on schema, column and attribute-index tables
  ([#656](https://github.com/odpi/egeria-workspaces/pull/656), [#657](https://github.com/odpi/egeria-workspaces/pull/657));
  **View buttons** on schema rows and related elements ([#709](https://github.com/odpi/egeria-workspaces/pull/709)).
- **Collections grouped by type** ([#816](https://github.com/odpi/egeria-workspaces/pull/816), [#817](https://github.com/odpi/egeria-workspaces/pull/817)).
- **Data initialization runs notebooks** and scans roots for manifests ([#662](https://github.com/odpi/egeria-workspaces/pull/662)),
  with notebook docs and Data Hub notebooks ([#664](https://github.com/odpi/egeria-workspaces/pull/664),
  [#685](https://github.com/odpi/egeria-workspaces/pull/685)); usage workload batch ([#684](https://github.com/odpi/egeria-workspaces/pull/684)).
- **Workbenches isolated behind an egress allow-list** ([#733](https://github.com/odpi/egeria-workspaces/pull/733));
  evict a stuck workbench ([#739](https://github.com/odpi/egeria-workspaces/pull/739)).
- **Egeria Advisor service account** `egeriaadvisornpa` ([#828](https://github.com/odpi/egeria-workspaces/pull/828));
  Phoenix compose ([#645](https://github.com/odpi/egeria-workspaces/pull/645)); optional TestGen runtime
  ([#663](https://github.com/odpi/egeria-workspaces/pull/663)); Governance Engine view service
  ([#639](https://github.com/odpi/egeria-workspaces/pull/639)); Pepys (see PR [#636](https://github.com/odpi/egeria-workspaces/pull/636));
  Pasteur in the nanny daemons ([#822](https://github.com/odpi/egeria-workspaces/pull/822)).
- **Coco content**: Chief Data Officer dashboard for Jules Keeper ([#780](https://github.com/odpi/egeria-workspaces/pull/780)),
  Airflow DAGs ([#653](https://github.com/odpi/egeria-workspaces/pull/653)), system data layer
  ([#660](https://github.com/odpi/egeria-workspaces/pull/660)).
- **Dr.Egeria templates** for report specs and dashboards ([#803](https://github.com/odpi/egeria-workspaces/pull/803)).
- **Heap dump** when the platform runs out of memory ([#773](https://github.com/odpi/egeria-workspaces/pull/773));
  `pg_stat_statements` on the shared Postgres ([#804](https://github.com/odpi/egeria-workspaces/pull/804)).
- **DCAT support**: DCAT configuration for the quickstart and freshstart metadata stores and integration daemons,
  with loading-bay `dcat/` folders ([#849](https://github.com/odpi/egeria-workspaces/pull/849)); an OpenLineage log store notebook, and Pasteur in the nanny daemons
  ([#847](https://github.com/odpi/egeria-workspaces/pull/847)).
- **One renderer for pyegeria's structured TABLE** (`egeria-table.js`); Local Dashboards and Report Specs draw TABLE
  results from the structured shape ([#855](https://github.com/odpi/egeria-workspaces/pull/855), [#856](https://github.com/odpi/egeria-workspaces/pull/856)).
- **Data Initialization batch status**: each batch shows its status, one run per batch at a time; best-practice docs
  for the Data Initialization notebooks ([#883](https://github.com/odpi/egeria-workspaces/pull/883)).
- **Statements of Applicability view** in Egeria Explorer: an implementation summary and a sortable, filterable table
  of controls ([#882](https://github.com/odpi/egeria-workspaces/pull/882)).
- **Coco sample statement of applicability** for ISO/IEC 27001 ([#881](https://github.com/odpi/egeria-workspaces/pull/881)).
- **Dr.Egeria templates for Egeria 6.3**: Limit Result by Status lists the five element statuses, lifecycle filters
  are added, deployment status uses `REJECTED`, and activity status gains `FOR_INFO`. The templates match pyegeria
  6.3.0's ([#887](https://github.com/odpi/egeria-workspaces/pull/887)).
- **A Dr.Egeria best-practices doc** with the same status values ([#887](https://github.com/odpi/egeria-workspaces/pull/887)).
- **`init_trellis.sh`** creates the Trellis role and database from `PGVECTOR_PASSWORD`, and `gen-env.sh` generates
  that password for a brand-new install. The shared-infra README covers creating the role on an existing volume and
  setting or changing its password (TR-27, [#887](https://github.com/odpi/egeria-workspaces/pull/887)).
- **The 16 MetadataExpert Dr.Egeria templates** (type and enum definitions, instances, classify, link and publish,
  Update Relationship, Count Metadata Elements), the same as pyegeria 6.3.0's ([#888](https://github.com/odpi/egeria-workspaces/pull/888)).
- **Coco security operational data store**: `init_security_ods.sql` creates `security_ods`, which only `provisioner`
  (delivery) and `surveyor` (read) can connect to, and `ensure-shared-infra.sh` runs it on every start. The Security
  Observability subscription moves to a new workbook run as Ivor Padlock, because Peter Profile can't see the security
  zone; the OpenLineage notebook joins the Data Hub batch. `4. keeping-safe` gains Simon Burr's STRIDE threat models
  for the Batch Manufacturing and Release supply chain, with links from four Austin systems
  ([#896](https://github.com/odpi/egeria-workspaces/pull/896)).

### Changed
- **Data Mesh uses the shared relationship components** from `static/egeria-shared-ui.js` instead of private copies, so its rows also show each related element's description. Its detail pane uses the shared resize hook, so it can be dragged up to the window width minus 200px (it stopped at 640px) and remembers its width.
- **The `pyegeria` floor was raised to 6.2.11** in the pyegeria-web and Jupyter/my-egeria images (quickstart and freshstart), and has been raised since: on 2026-11-10 the quickstart Portal requires `pyegeria>=6.2.28` (it runs 6.2.32) and freshstart's is capped at `>=6.2.21,<6.2.27`. 6.2.11 adds the Business Capability commands, routes deprecated wrappers of removed Egeria endpoints to their replacements, and makes `get_platform_organization` read `/api/public/app/info`.
- **`call-dr-egeria` Obsidian plugin dependencies updated** (`npm audit` now reports 0 vulnerabilities, down from 8 advisories including 1 critical); the committed `node_modules` and bundled `main.js` were rebuilt. Supersedes Dependabot PRs #650, #665, #678, #689, #690, #696 and #697.
- **README**: the OpenSSF Scorecard badge now links to this repository's scorecard (it pointed at `odpi/egeria`), the license badge points at this repository, and the Airflow/Marquez and Unity Catalog startup flags are documented.
- **Breaking for Trellis deployments: `TRELLIS_DB_CREDENTIAL_KEY` is required** in the Trellis `.env` and the Prefect
  Resource Explorer worker's `.env.re-worker`. Stored database passwords no longer become unreadable when a container
  is recreated; re-enter each one once. An older `RE_DB_CREDENTIAL_KEY` takes precedence ([#894](https://github.com/odpi/egeria-workspaces/pull/894)).
- **The shared-infra README says to re-run the other stack's start script** after the `provisioner` password changes,
  on a host that runs both the quickstart and a freshstart (TR-28, [#894](https://github.com/odpi/egeria-workspaces/pull/894)).
- **Freshstart pins the released `egeria-platform:6.3`**, at the same digest as the quickstart. Both start scripts
  re-pin the image their Dockerfile uses, and `pin-latest-digest.sh` fails when it finds nothing to re-pin
  (TR-36, [#897](https://github.com/odpi/egeria-workspaces/pull/897)).
- **The start scripts say what "healthy" means**: the platform's web server is up, and Egeria's servers need about 4
  more minutes ([#897](https://github.com/odpi/egeria-workspaces/pull/897)).
- **Platform**: quickstart and freshstart on Egeria 6.3-SNAPSHOT; the quickstart pin tracks the Pasteur build
  ([#647](https://github.com/odpi/egeria-workspaces/pull/647), [#748](https://github.com/odpi/egeria-workspaces/pull/748),
  [#740](https://github.com/odpi/egeria-workspaces/pull/740), [#798](https://github.com/odpi/egeria-workspaces/pull/798),
  [#800](https://github.com/odpi/egeria-workspaces/pull/800), [#805](https://github.com/odpi/egeria-workspaces/pull/805),
  [#808](https://github.com/odpi/egeria-workspaces/pull/808), [#810](https://github.com/odpi/egeria-workspaces/pull/810),
  [#827](https://github.com/odpi/egeria-workspaces/pull/827)).
- **Bearer tokens last two hours** ([#651](https://github.com/odpi/egeria-workspaces/pull/651)).
- **Analytic functions and metric paths by registered name** ([#741](https://github.com/odpi/egeria-workspaces/pull/741),
  [#742](https://github.com/odpi/egeria-workspaces/pull/742), [#743](https://github.com/odpi/egeria-workspaces/pull/743),
  [#811](https://github.com/odpi/egeria-workspaces/pull/811)).
- **Dashboard placements**: `presentationStyle` replaces `emphasis`; MeasurementSpecification references become
  relationships (docs: [#796](https://github.com/odpi/egeria-workspaces/pull/796), [#795](https://github.com/odpi/egeria-workspaces/pull/795)).
- **Freshstart catches up with the quickstart**: shared helper modules and 11 handlers
  ([#891](https://github.com/odpi/egeria-workspaces/pull/891)), then the Overview, with pyegeria 6.3.0 or later
  replacing the earlier cap below 6.2.27 ([#892](https://github.com/odpi/egeria-workspaces/pull/892),
  [#807](https://github.com/odpi/egeria-workspaces/pull/807)).
- **pyegeria image floors** raised step by step to 6.2.24 ([#667](https://github.com/odpi/egeria-workspaces/pull/667),
  [#680](https://github.com/odpi/egeria-workspaces/pull/680), [#688](https://github.com/odpi/egeria-workspaces/pull/688),
  [#695](https://github.com/odpi/egeria-workspaces/pull/695), [#707](https://github.com/odpi/egeria-workspaces/pull/707),
  [#712](https://github.com/odpi/egeria-workspaces/pull/712), [#731](https://github.com/odpi/egeria-workspaces/pull/731),
  [#736](https://github.com/odpi/egeria-workspaces/pull/736), [#751](https://github.com/odpi/egeria-workspaces/pull/751),
  [#772](https://github.com/odpi/egeria-workspaces/pull/772), [#789](https://github.com/odpi/egeria-workspaces/pull/789),
  [#802](https://github.com/odpi/egeria-workspaces/pull/802)).
- **Shared infrastructure**: autoheal started and Postgres checkpointing tuned ([#686](https://github.com/odpi/egeria-workspaces/pull/686));
  Airflow lineage to Egeria only ([#784](https://github.com/odpi/egeria-workspaces/pull/784)); Kafka's own server logs
  capped by size ([#820](https://github.com/odpi/egeria-workspaces/pull/820)).
- **Dependencies**: Dependabot and consolidated bumps ([#652](https://github.com/odpi/egeria-workspaces/pull/652),
  [#708](https://github.com/odpi/egeria-workspaces/pull/708), [#718](https://github.com/odpi/egeria-workspaces/pull/718),
  [#737](https://github.com/odpi/egeria-workspaces/pull/737), [#757](https://github.com/odpi/egeria-workspaces/pull/757)
  to [#771](https://github.com/odpi/egeria-workspaces/pull/771)); Actions bumps ([#542](https://github.com/odpi/egeria-workspaces/pull/542),
  [#543](https://github.com/odpi/egeria-workspaces/pull/543), [#596](https://github.com/odpi/egeria-workspaces/pull/596),
  [#764](https://github.com/odpi/egeria-workspaces/pull/764), [#765](https://github.com/odpi/egeria-workspaces/pull/765)).
- **pyegeria 6.3.0 is the quickstart's minimum**, in the four Dockerfiles and `requirements.txt` ([#887](https://github.com/odpi/egeria-workspaces/pull/887)).
- **The Portal's report-spec consumer folder is found by its qualified name**, not a hard-coded GUID (RK-22, [#887](https://github.com/odpi/egeria-workspaces/pull/887)).
- **The shared Postgres service gains a `PGVECTOR_PASSWORD` setting**, so the first start after upgrading recreates
  the `egeria-shared-postgres` container once. Data and existing passwords are kept ([#887](https://github.com/odpi/egeria-workspaces/pull/887)).

### Fixed
- **The Portal shows pyegeria's notes beside a result.** pyegeria 6.2.37 returns words beside a result in `notes`, for example "Showing the first 100: the query stopped at its page size of 100; more may exist." for a query that filled its page. The Portal received them but never showed them, so a capped DICT or TABLE result read as the whole answer. They now show, escaped, one per line, under every Local Dashboards tile, in the drill-down drawer and in Egeria Explorer's Run Report panel; a result without notes looks as before.
- **Local Dashboards no longer cuts long tables mid-row, or says a scoped placement has no scope.** A long LIST or TABLE result was cut at 20,000 characters, so the CDO Governance Metric Register showed 12 of its 46 rows, followed by the note "this placement has no query scope", although it is scoped by `search_string`. Tables are now capped only at whole rows (1,000 rows or about 1 MB each; they scroll inside the tile) with "Showing the first N of M rows (this tile's render limit)". The 20,000-character cap applies only to text outside tables, and its note names the placement's real scope or says it has none.
- **`<br>` in markdown table cells shows as a line break, not as the text "&lt;br&gt;".** pyegeria 6.2.37 writes `<br>` in table cells for newlines in a value and between LIST bullets (for example the CDO register tiles). The renderers in Local Dashboards and the shared `renderMd` (The Catalog, the Explorer's Report Specs and other pages), in quickstart and freshstart, now turn back only the exact escaped forms of `<br>`, `<br/>` and `<br />` in table cells; everything else stays escaped. Needed before the Portal moves to pyegeria 6.2.37.
- **Local Dashboards: large tables scroll inside their tile.** Tables scroll vertically past 420px and sideways when wide, with always-visible scroll bars and a header row that stays in view; tables with five or more columns keep a 120px minimum column width instead of wrapping every few characters. Column widths stay draggable. The drill-down drawer's tables stop at 70% of the window height, so their header stays in view too. JSON/DICT results now show up to 200 rows and 20 columns (was 25 and 8, with extra columns dropped silently); anything beyond is counted, and hidden columns are named. Small tables are unchanged.
- **The Catalog no longer goes blank when Namespaces, Survey Types or Governance Processes is opened before a connection exists** (a fresh visitor with no persona chosen). Those views read the connection settings while they were still empty; they now load with the server's defaults, as the other sections do.
- **Related-element rows no longer clip their "View →" button in narrow panes.** Badges and actions wrap under the element name. In Data Mesh's default 380px detail pane, 58 of 60 buttons on a busy product were cut off.
- **The Catalog's Survey Annotations detail pane dragged the wrong way**: it sits to the right of its divider, so dragging left now widens it.
- **OpenSSF Scorecard workflow never ran, so the README badge showed "invalid repo path".** `.github/workflows/scorecard.yml` pinned an `ossf/scorecard-action` commit that does not exist; it is now pinned to the v2.4.3 commit, so results are published for `odpi/egeria-workspaces`. The README badge link also pointed at `odpi/egeria` and now points at this repository.
- **The shared OpenLineage proxy now has `restart: always`.** It had no restart policy, so once it stopped, lineage silently stopped reaching Egeria.
- **Relationship cards show each relationship once**, instead of repeating it from both ends.
- **`extendedProperties` are flattened in every shared portal property serializer**, and The Catalog's asset detail now shows `extendedProperties` and `additionalProperties`.
- **Egeria Operations' "Engine Action ↗" link** opened The Catalog, which sent engine actions straight back to Egeria Operations' main page. The Catalog now opens them in its own Processes › Actions tab. Links into Egeria Operations' Engine Actions tab now carry `?guid=` and select that action.
- **Actor profiles, roles and user identities show all their properties**, including `additionalProperties` and type-specific ones such as `pronouns` and `givenNames`. The detail serializer used to copy only a fixed list of keys.
- **Type Explorer lists both directions of a relationship whose two ends are both in the type's inheritance chain** (for example `Referenceable`↔`Referenceable`); only the first end was listed before.
- **Start-up summary URLs**: on a loopback bind, `quick-start-local` and `fresh-start-local` printed `https://<HOST_FQDN>:…` URLs that refuse connections. They now print `localhost` URLs, show the bind address, and point to `--lan`.
- **Token reuse** (PO-40, [#895](https://github.com/odpi/egeria-workspaces/pull/895)): the Portal returns a still-valid token for the same user instead of signing in
  again, so a reload no longer starts the per-user caches cold.
- **Dr.Egeria run block** (PY-30, [#895](https://github.com/odpi/egeria-workspaces/pull/895)): a block that runs no command isn't a success, with hints naming the
  line and the fix when pyegeria provides them (feature-detected).
- **Freshstart on a fresh clone**: it no longer crash-loops on a platform image older than `DCATContentPack`, and the
  start scripts stop and explain a missing `EGERIA_ADMIN_CALLER_PASSWORD` instead of failing after 3 s (TR-36,
  [#897](https://github.com/odpi/egeria-workspaces/pull/897)).
- **The Catalog opens a plain Asset**, and Asset subtypes it doesn't know, under Data Assets, instead of saying it
  isn't part of The Catalog ([#897](https://github.com/odpi/egeria-workspaces/pull/897)).
- **Three dead README links**, and freshstart's `demo-mode.md`, which described the quickstart
  ([#897](https://github.com/odpi/egeria-workspaces/pull/897)).
- **The Type Explorer shows each type's real Egeria area**, read first from the type's Egeria wiki link; the fallback
  list no longer puts data stores in an invented Area 6. Report is Area 2, SurveyReport Area 6
  ([#902](https://github.com/odpi/egeria-workspaces/pull/902)).
- **The Overview shows only what it measured** ([#783](https://github.com/odpi/egeria-workspaces/pull/783),
  [#785](https://github.com/odpi/egeria-workspaces/pull/785), [#791](https://github.com/odpi/egeria-workspaces/pull/791),
  [#807](https://github.com/odpi/egeria-workspaces/pull/807)); the Overview no longer stops running
  `egeria-shared-ui.js` halfway ([#755](https://github.com/odpi/egeria-workspaces/pull/755)).
- **The Catalog**: every list pages to the end, Data Assets tree, list caches ([#659](https://github.com/odpi/egeria-workspaces/pull/659),
  [#658](https://github.com/odpi/egeria-workspaces/pull/658), [#661](https://github.com/odpi/egeria-workspaces/pull/661),
  [#666](https://github.com/odpi/egeria-workspaces/pull/666)).
- **Blank Data Mesh and Resource Locator pages; text contrast** ([#654](https://github.com/odpi/egeria-workspaces/pull/654),
  [#655](https://github.com/odpi/egeria-workspaces/pull/655)).
- **Type Explorer** fixes ([#777](https://github.com/odpi/egeria-workspaces/pull/777), [#750](https://github.com/odpi/egeria-workspaces/pull/750),
  [#745](https://github.com/odpi/egeria-workspaces/pull/745), [#746](https://github.com/odpi/egeria-workspaces/pull/746));
  solution components ([#716](https://github.com/odpi/egeria-workspaces/pull/716), [#717](https://github.com/odpi/egeria-workspaces/pull/717)).
- **Information supply chain graphs on Egeria 6.3**, and a 404 for a missing supply chain
  ([#710](https://github.com/odpi/egeria-workspaces/pull/710), [#648](https://github.com/odpi/egeria-workspaces/pull/648)).
- **Demo reset** ([#646](https://github.com/odpi/egeria-workspaces/pull/646), [#729](https://github.com/odpi/egeria-workspaces/pull/729));
  shared infra ([#624](https://github.com/odpi/egeria-workspaces/pull/624)); loading bay Bitol folder
  ([#681](https://github.com/odpi/egeria-workspaces/pull/681)); secrets refresh ([#638](https://github.com/odpi/egeria-workspaces/pull/638));
  empty limits ([#641](https://github.com/odpi/egeria-workspaces/pull/641)); compose build ([#626](https://github.com/odpi/egeria-workspaces/pull/626));
  the self-heal step now loads valid metadata values first ([#801](https://github.com/odpi/egeria-workspaces/pull/801)).
- **MCP SSE headers** ([#738](https://github.com/odpi/egeria-workspaces/pull/738)).
- **Three Coco Data Initialization notebooks** fit their cell limits and are safe to run again; the Local Dashboards
  Dr.Egeria inbox models its subscription as a Digital Subscription ([#883](https://github.com/odpi/egeria-workspaces/pull/883)).
- **Marquez restarts after a reboot**, and the infra check covers `airflow-marquez` ([#857](https://github.com/odpi/egeria-workspaces/pull/857)); the scheduled infra
  check writes one bounded log line per run ([#854](https://github.com/odpi/egeria-workspaces/pull/854)).
- **`gen-env.sh` quotes the Kafka directory paths**, so shared infrastructure starts from a checkout whose path contains
  a space ([#888](https://github.com/odpi/egeria-workspaces/pull/888)).
- **`fresh-start-local` waits for a healthy platform** and handles Podman like `quick-start-local`; the shared-infra
  README says re-running a start script keeps the `provisioner` password ([#893](https://github.com/odpi/egeria-workspaces/pull/893)).

### Security
- **No well-known password for the `provisioner` database user.** It comes from `PROVISIONER_PASSWORD` in
  `shared-infra/.env`, generated when missing; the first start rotates it with the runtime secrets and Airflow, and
  it is kept out of `pg_stat_statements`' query-text file (TR-28, [#889](https://github.com/odpi/egeria-workspaces/pull/889)).
- **Credentials are sent only to allow-listed Egeria platforms** ([#819](https://github.com/odpi/egeria-workspaces/pull/819)).
- **A signed-in user's request is never run as the service user** ([#715](https://github.com/odpi/egeria-workspaces/pull/715)).
- **Continued hardening of the Portal environment** ([#640](https://github.com/odpi/egeria-workspaces/pull/640),
  [#642](https://github.com/odpi/egeria-workspaces/pull/642), [#643](https://github.com/odpi/egeria-workspaces/pull/643)).
- **Ports bind to `127.0.0.1` by default** ([#644](https://github.com/odpi/egeria-workspaces/pull/644)); `--lan` opens them
  ([#687](https://github.com/odpi/egeria-workspaces/pull/687)).
- **Jupyter no longer trusts the emSign ECC G3 root** ([#776](https://github.com/odpi/egeria-workspaces/pull/776)).
- **No built-in Portal service passwords** (PO-45, [#895](https://github.com/odpi/egeria-workspaces/pull/895)): the quickstart Portal and my-profile read
  `QUICKSTART_PERSONA_PASSWORD` from `egeria-quickstart/.env` (written by `quick-start-local` if missing); freshstart's
  `EGERIA_ADMIN_CALLER_PASSWORD` has no default and must be set (breaking). One getter refuses in words when the
  password isn't configured, replacing the built-in fallbacks in both handler copies; freshstart's `gen-env.sh` no
  longer drops a user's `EGERIA_ADMIN_CALLER_PASSWORD`.
- **A named user needs their own token or password** (PO-41, [#895](https://github.com/odpi/egeria-workspaces/pull/895)): a request naming a user other than the
  service user, without a token or password, is refused (HTTP 400, in words) instead of running as that user on the
  service password; this includes `?user_id=` in a URL (breaking). No route reads a password from a URL.
- **The MCP tools no longer publish the service password** (PO-44, [#895](https://github.com/odpi/egeria-workspaces/pull/895)): no credential defaults in the tool
  schema; credentials are resolved at call time, the platform must be allow-listed, and the named-user rule applies.
- **Optional firewall unit for the shared Postgres port 5442** (TR-28, [#895](https://github.com/odpi/egeria-workspaces/pull/895)).
- **Freshstart's session key is generated and kept** (RK-24b, [#897](https://github.com/odpi/egeria-workspaces/pull/897)): `gen-env.sh` no longer drops
  `JWT_SECRET`, so sessions are no longer signed with a value published in this repository; the compose file has no
  default. The next start generates a new key, so everyone signs in again once.
- **The quickstart's session key is kept or generated** (PO-46b, [#901](https://github.com/odpi/egeria-workspaces/pull/901)): `gen-env.sh` keeps `JWT_SECRET`
  or generates one; the compose file requires it; a published value is refused, and sign-in answers 503 in words.
- **No default `egeria_advisor` password**: `init_egeria.sql` no longer creates the role with a well-known password
  (TR-27, [#887](https://github.com/odpi/egeria-workspaces/pull/887)).

### Removed
- The tracked repo-root `.env` (a stale March 2026 file with `HOST_FQDN=hedwig`). Nothing reads it; each environment uses its own `compose-configs/*/.env`.

## [6.2] - 2026-10-08

Aligns with Egeria 6.2 and pyegeria 6.2.0. See [RELEASE_NOTES.md](RELEASE_NOTES.md) for the narrative summary.

### Added
- **Data Initialization loads subfolders, in a declared order, as the owning user**: folders under `dr-egeria-inbox` now include their subfolders; `_batch.json` `files` entries can name subfolders (`"sub/"`) or files in them, a new `exclude` field skips prose files, and a new `userid` (per folder, or per entry as `{"file", "userid"}`) loads each file as its owner, with passwords from `EGERIA_BOOTSTRAP_PASSWORD_<USERID>`. Each file runs once per pass, a subfolder that is its own batch is skipped by its parent, and the admin panel shows per-file run status, run-as user and ordering notes ([#618](https://github.com/odpi/egeria-workspaces/pull/618)).
- **User guide** `DR_EGERIA_AUTO_LOADING_GUIDE.md` for people who maintain folders of Dr.Egeria files ([#618](https://github.com/odpi/egeria-workspaces/pull/618)).
- **Pyegeria Cache Refresh Flag**: Added `--refresh-pyegeria` flag to `quick-start-local` and `fresh-start-local` to bust cached pyegeria pip-install layers in `pyegeria-web` and `jupyter` images on startup ([`86cb47d`](https://github.com/odpi/egeria-workspaces/commit/86cb47de), [#426](https://github.com/odpi/egeria-workspaces/pull/426)).

### Changed
- **Egeria platform images pinned to the 6.2 release**: quickstart and freshstart now build from `odpi/egeria-platform:6.2` (digest-pinned) instead of a `latest` digest. `--refresh-platform` still re-resolves to `latest`.
- **coco-workbooks load in their README order**: `_folder_order.json` and the `_batch.json` manifests now follow the order and per-file users the coco-workbooks READMEs give ([#618](https://github.com/odpi/egeria-workspaces/pull/618)).
- **pyegeria tracks the latest release by default**: `quick-start-local` and `fresh-start-local` now install the latest pyegeria from PyPI into `pyegeria-web` and `jupyter` on every run (the version is the layer's cache key, so an unchanged release is a no-op). New `--pyegeria-version X.Y.Z` pins a release (persisted in `compose-configs/<env>/.env.pyegeria`; `latest` clears it) and `--no-refresh-pyegeria` skips the check; `--refresh-pyegeria` now forces a rebuild of the same version. Previously an install or `--refresh-platform` upgrade recreated the containers from the old image, silently reverting pyegeria (e.g. to 6.1.18) and discarding any in-container upgrade.
- **pyegeria floor raised to 6.1.22** in both `PyegeriaWebHandler` images and `Dockerfile-jupyter` (needed for the new link attributes in the regenerated templates).
- **Dr.Egeria Command Templates**: Regenerated the complete Dr.Egeria markdown command template library under `templates/basic/` and `templates/advanced/` against the latest pyegeria release ([`0ed6091`](https://github.com/odpi/egeria-workspaces/commit/0ed6091f), [#427](https://github.com/odpi/egeria-workspaces/pull/427)).
- **Portal Documentation**: Updated documentation across Egeria Explorer, Egeria Overview, and Tech Catalog tools in `portal-docs/` to reflect recent UI and persona enhancements ([`f66f116`](https://github.com/odpi/egeria-workspaces/commit/f66f1166), [#425](https://github.com/odpi/egeria-workspaces/pull/425)).

### Fixed
- **Egeria Main Platform Healthcheck**: Updated `egeria-main` healthcheck to validate HTTP status codes (200 or 401), ensuring server error states (e.g., 500) properly mark the container unhealthy ([`890796b`](https://github.com/odpi/egeria-workspaces/commit/890796bc)).
- **Digest Pinning Script Path Resolution**: Resolved `pin-latest-digest.sh` from the repository root in startup scripts when running with `--refresh-platform` ([`c55b721`](https://github.com/odpi/egeria-workspaces/commit/c55b7212)).
- **Jupyter Pyegeria Installation Environment**: Documented and resolved the dual pyegeria install environment behavior in the Jupyter container ([`9bafc8b`](https://github.com/odpi/egeria-workspaces/commit/9bafc8b9)).

[Unreleased]: https://github.com/odpi/egeria-workspaces/compare/v6.3...HEAD
[6.3]: https://github.com/odpi/egeria-workspaces/compare/v6.2...v6.3
[6.2]: https://github.com/odpi/egeria-workspaces/compare/v6.1...v6.2
