# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Tutorials: Report Specs and Analytic Functions**, and refreshed Local Dashboards and Saved Queries tutorials (`portal-docs/tutorials/`). *Report Specs: Local and Held in Egeria* covers user spec files, precedence (local > egeria > builtin), `Create Report Spec`, consumer folders and the sync. *Add and Use Analytic Functions* covers writing a function and registering it in Jupyter, the quickstart Portal, freshstart and Egeria Advisor. Local Dashboards now explains the "not visible to you" tile for a Report in a zone the viewer cannot see. Local Dashboards, the Query tool and the Egeria report-spec sync are marked quickstart only. *Worked Examples* gives several end-to-end examples of different kinds for each area, with input, steps and output.
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
- **`--lan` for `quick-start-local` and `fresh-start-local`**: publishes the ports on every interface (`0.0.0.0`) for that run, so the stack is reachable by machine name and from other machines. On Docker Desktop the default since [#644](https://github.com/odpi/egeria-workspaces/pull/644) is `127.0.0.1`, which answers on `localhost` only.
- **`quick-start-local` starts Airflow and Marquez with the demo**: new `--with-airflow-marquez` and `--skip-airflow-marquez` flags (on by default with `--demo`, off otherwise). Their ports stay on `127.0.0.1` even when the demo binds `0.0.0.0`, because Airflow's admin login can run arbitrary code and Marquez has no login. `airflow-marquez.yaml` now maps `host.docker.internal` to the host gateway so Airflow and Marquez reach the shared Postgres on native Docker Engine (Linux).
- **Airflow's OpenLineage events reach Egeria as well as Marquez**: `openlineage.env` defaults to the composite transport (Marquez directly, and Egeria through the shared-infra OpenLineage proxy and the `openlineage.events` Kafka topic). A new "OpenLineage Events" bootstrap batch runs `HarvestOpenLineageEvents::CreateAsCatalogTargetGovernanceActionProcess` to catalog that topic, and the portal's bootstrap monitor redoes it after a demo reset. Airflow's events also carry information supply chain information.
- **Dr.Egeria templates for the Security Officer commands** (`Create Statement of Applicability`, `Link Control Applicability`) and for the Business Capability commands (`Business Capability`, `Business Capability Dependency`, `Digital Support`), with their sections in the portal's `templates-basic` page.
- **Coco Pharmaceuticals content**: security support, sustainability reference data, and more resilient batch loading for the Coco Data Hub, clinical trials and strategic digital products workbooks (0, 1 and 3).
- **Tutorials are part of the Portal Docs**: the Local Dashboards, Digital Product & Subscription and Saved Queries tutorials moved from `PyegeriaWebHandler/` to `portal-docs/tutorials/`, so they are served at `/docs/` with a Tutorials section and overview page on the docs hub. Their screenshots live in `portal-docs/images/`, and the docs viewer now resolves images relative to each page.
- **Saved Queries tutorial** (`portal-docs/tutorials/saved-queries.md`): builds, saves and refreshes a query in the Query tool, then shows its results set on a Local Dashboard through a `Collection Members` report. It has screenshots (`portal-docs/images/saved-query-*.png`), diagrams and links to and from the Local Dashboards tutorial.

### Changed
- **Data Mesh uses the shared relationship components** from `static/egeria-shared-ui.js` instead of private copies, so its rows also show each related element's description. Its detail pane uses the shared resize hook, so it can be dragged up to the window width minus 200px (it stopped at 640px) and remembers its width.
- **The `pyegeria` floor was raised to 6.2.11** in the pyegeria-web and Jupyter/my-egeria images (quickstart and freshstart), and has been raised since: on 2026-11-10 the quickstart Portal requires `pyegeria>=6.2.28` (it runs 6.2.32) and freshstart's is capped at `>=6.2.21,<6.2.27`. 6.2.11 adds the Business Capability commands, routes deprecated wrappers of removed Egeria endpoints to their replacements, and makes `get_platform_organization` read `/api/public/app/info`.
- **`call-dr-egeria` Obsidian plugin dependencies updated** (`npm audit` now reports 0 vulnerabilities, down from 8 advisories including 1 critical); the committed `node_modules` and bundled `main.js` were rebuilt. Supersedes Dependabot PRs #650, #665, #678, #689, #690, #696 and #697.
- **README**: the OpenSSF Scorecard badge now links to this repository's scorecard (it pointed at `odpi/egeria`), the license badge points at this repository, and the Airflow/Marquez and Unity Catalog startup flags are documented.

### Fixed
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

[6.2]: https://github.com/odpi/egeria-workspaces/compare/v6.1...v6.2
