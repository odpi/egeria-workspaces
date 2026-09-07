# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [6.2.0] - 2026-09-04

### Added
- **Pyegeria Cache Refresh Flag**: Added `--refresh-pyegeria` flag to `quick-start-local` and `fresh-start-local` to bust cached pyegeria pip-install layers in `pyegeria-web` and `jupyter` images on startup ([`86cb47d`](https://github.com/odpi/egeria-workspaces/commit/86cb47de), [#426](https://github.com/odpi/egeria-workspaces/pull/426)).

### Changed
- **Dr.Egeria Command Templates**: Regenerated the complete Dr.Egeria markdown command template library under `templates/basic/` and `templates/advanced/` against the latest pyegeria release ([`0ed6091`](https://github.com/odpi/egeria-workspaces/commit/0ed6091f), [#427](https://github.com/odpi/egeria-workspaces/pull/427)).
- **Portal Documentation**: Updated documentation across Egeria Explorer, Egeria Overview, and Tech Catalog tools in `portal-docs/` to reflect recent UI and persona enhancements ([`f66f116`](https://github.com/odpi/egeria-workspaces/commit/f66f1166), [#425](https://github.com/odpi/egeria-workspaces/pull/425)).

### Fixed
- **Egeria Main Platform Healthcheck**: Updated `egeria-main` healthcheck to validate HTTP status codes (200 or 401), ensuring server error states (e.g., 500) properly mark the container unhealthy ([`890796b`](https://github.com/odpi/egeria-workspaces/commit/890796bc)).
- **Digest Pinning Script Path Resolution**: Resolved `pin-latest-digest.sh` from the repository root in startup scripts when running with `--refresh-platform` ([`c55b721`](https://github.com/odpi/egeria-workspaces/commit/c55b7212)).
- **Jupyter Pyegeria Installation Environment**: Documented and resolved the dual pyegeria install environment behavior in the Jupyter container ([`9bafc8b`](https://github.com/odpi/egeria-workspaces/commit/9bafc8b9)).

[6.2.0]: https://github.com/odpi/egeria-workspaces/compare/v6.1...v6.2.0
