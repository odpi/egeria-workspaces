# PyegeriaWebHandler tests

For the overall strategy (why this tier exists, how it fits with `browser/`
and `analyze.py`, how to interpret failures), see `../TESTING.md`. This file
covers just the mechanics of this one tier.

These tests exercise real handler code against the LIVE Egeria platform the
`quickstart-pyegeria-web` container is wired to — there is no mocked backend.
That means they must run **inside the container** (or an equivalent
environment where `EGERIA_PLATFORM_URL` / `host.docker.internal` resolve),
not from a bare host shell.

## Setup (once per container)

```bash
docker exec quickstart-pyegeria-web pip install -r requirements-test.txt
```

## Run

```bash
docker exec quickstart-pyegeria-web pytest tests/ --ignore=tests/browser -v
```

`--ignore=tests/browser` matters: that subdirectory has its own venv meant
to run from the HOST (see `browser/README.md`) — it has no `fastapi`/
`pyegeria` installed, so pytest inside the container can't collect it (and
shouldn't try to).

## What's here

- `test_fastapi_handler_health.py` — pre-existing basic health check.
- `test_mcp_server_basic.py` — pre-existing, mocked `mcp_server.py` unit tests.
- `golden_anchors.py` — stable, known-good entities from the Coco
  Pharmaceuticals seed data (`CocoComboArchive`), used as regression
  baselines across BOTH this directory and `browser/`. See the module
  docstring for why these are safe to hardcode and what to do if a
  content-pack update ever changes one of them.
- `test_golden_anchors.py` — characterization tests asserting exact values
  against the anchors above. Read-only, safe to run anytime against the
  shared live environment.
- `test_schema_fuzz.py` — Schemathesis, driven directly off the app's own
  `/openapi.json` (no hand-written cases). Scoped narrowly for now — see its
  module docstring for why and how to widen it.
- `browser/` — Playwright/E2E tests (Phase 2). Runs from the host, not this
  container — see `browser/README.md`.

## Tracking gaps found in `pyegeria` itself (not this app's code)

See `../PYEGERIA_GAPS.md`. Do not act on any of those without explicit
approval — that file is a tracking log, not a work queue.
