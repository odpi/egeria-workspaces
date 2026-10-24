# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **The Catalog's Infrastructure section has a tab for each direct subtype of `Infrastructure`**, read from Egeria's type system, so a newly defined subtype (for example `Equipment`) gets its own tab. An "All Infrastructure" tab is added when Infrastructure has several subtypes or can have instances of its own. New endpoint `GET /api/tech-catalog/infrastructure/types`; `GET /api/tech-catalog/infrastructure` takes `?type_name=` (default `ITInfrastructure`).
- **Egeria Explorer's Type Explorer shows inheritance for relationships and classifications**: the Relationships tab has the same Show inherited toggle as Properties, with an own/total count and an "own" badge. A new Classifications tab lists every classification the type can carry and the type in its supertype chain that makes it valid.
- **`--lan` for `quick-start-local` and `fresh-start-local`**: publishes the ports on every interface (`0.0.0.0`) for that run, so the stack is reachable by machine name and from other machines. On Docker Desktop the default since [#644](https://github.com/odpi/egeria-workspaces/pull/644) is `127.0.0.1`, which answers on `localhost` only.

### Fixed
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
