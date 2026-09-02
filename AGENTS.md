# AGENTS Guide for `egeria-workspaces`

## What this repo is
- This repo is primarily Docker Compose orchestration for Egeria workspaces, not a single app binary.
- Two isolated deployments are first-class: quickstart (`9443/7888/8085`) and freshstart (`8443/7889/8086`), both sharing Kafka/Postgres/proxy.
- Start from root scripts, not direct compose, unless debugging compose behavior.

## System architecture (read these together)
- Root overview and topology: `README.md`.
- Quickstart stack definition: `compose-configs/egeria-quickstart/egeria-quickstart.yaml`.
- Freshstart stack definition: `compose-configs/egeria-freshstart/egeria-freshstart.yaml`.
- Shared infra boundary: `compose-configs/shared-infra/shared-infra.yaml` and `compose-configs/shared-infra/ensure-shared-infra.sh`.
- Runtime/exchange data flow: `exchange-*/landing-area` -> integration daemon cataloging; Egeria outputs to `exchange-*/distribution-hub`; runtime state persists in `runtime-volumes/*`.

## Critical workflows
- Preferred startup paths: local scripts for single-machine dev, multi-host scripts for real DNS/FQDN routing.
- Startup scripts always call `compose-configs/shared-infra/ensure-shared-infra.sh` first; do not duplicate shared Kafka/Postgres startup logic elsewhere.
- Rebuild behavior is intentional: scripts use `docker compose build --pull` and `up -d --pull always`; `NO_CACHE=1` adds `--no-cache` via `compose-configs/shared-infra/compose-build-flags.sh`; `--refresh-platform` on `*-start-local` forces platform image refresh; `--refresh-pyegeria` on `*-start-local` busts the cached pyegeria pip-install layer for pyegeria-web + jupyter (see `compose-configs/shared-infra/pin-latest-digest.sh` and each Dockerfile's `PYEGERIA_BUST` ARG for why a plain rebuild alone doesn't pick up a newer pyegeria release).
- **Synchronization workflow:** `user-sync` and `quick-start-local --sync-*` automate exporting/importing demo DB schemas (`demo_auth`, `demo`) via SSH/SCP. They use `REMOTE_USER` and `REMOTE_PASSWORD` env vars or flags, and rely on `sshpass` if passwords are provided.

## Project-specific conventions
- `quick-start-*` and `fresh-start-*` repopulate runtime server configs on each start from `compose-configs/egeria-quickstart/servers` into `runtime-volumes/*/data/servers`.
- Freshstart secrets are seeded from templates in `compose-configs/egeria-freshstart/secrets/` only when files are missing (never overwrite existing runtime secrets).
- `gen-env.sh` in each deployment rewrites `exchange-*/config/config.json` with current `HOST_FQDN`, server names (`qs-*` vs `fs-*`), and saves `config.json.bak` once.
- Local vs multi-host overlays differ mainly by `extra_hosts` host-gateway mapping (`*-local.yaml` vs `*-cluster.yaml`); keep this behavior symmetric across quickstart/freshstart.
- When changing one flavor, check the sibling flavor for parity (`egeria-quickstart` <-> `egeria-freshstart`).

## PyegeriaWebHandler and MCP integration
- Main backend entrypoint: `compose-configs/egeria-quickstart/PyegeriaWebHandler/pyegeria_handler.py` (FastAPI + router modules by domain).
- MCP server entrypoint: `compose-configs/egeria-quickstart/PyegeriaWebHandler/mcp_server.py`; Obsidian MCP plugin is in `obsidian-plugins/call-dr-egeria/`.
- Token-gated SSE/messages endpoints rely on `MCP_ACCESS_TOKEN` (see middleware in `pyegeria_handler.py`).
- `pyegeria-web` is mounted read-write to workspace folders (`/app`, `/config`, `/work`, templates, demo data), so path changes must preserve container mount assumptions.
- **Async invariant:** `async def` FastAPI routes must use `*_async` client factories (e.g. `_runtime_manager_async`, `_security_officer_async`) that call `await async_apply_token(mgr)` from `egeria_auth.py`. Never call sync `apply_token()` or `create_egeria_bearer_token()` from an async route — they call `run_until_complete()` internally and raise `RuntimeError` on Python 3.10+. See CLAUDE.md for the full pattern and `operations_handler.py` / `audit_handler.py` for reference implementations.
- **`dr_egeria_md.py`'s `setup_dispatcher` is imported directly from pyegeria's `md_processing.dr_egeria` — do not reintroduce a local copy.** It carried a hand-duplicated fork of that function for ~3+ months (same structure, no app-specific processors) that silently drifted out of sync as pyegeria added new command families upstream, missing `Create Report`/`Update Report` and the entire Dashboard Sheet family entirely (fixed 2026-07-31). A local command unrecognized here doesn't necessarily mean pyegeria lacks it — check `python3 -c "from md_processing.dr_egeria import setup_dispatcher; ..."` against the real one before concluding a feature isn't released yet.
- **When adding a new Dr.Egeria command/processor in egeria-python, verify it actually works through this app's `/api/dr-egeria/execute-document` (or `/api/dr-egeria/execute`) endpoint, not just the egeria-python dev venv CLI.** This app has its own request path into `md_processing`; a working `dr_egeria --process` in the dev checkout does not by itself prove the deployed web app can run the same command (see the `setup_dispatcher` note above for exactly this failure mode).
- **A new local (non-Egeria) persisted store in pyegeria/Dr.Egeria (e.g. `~/.pyegeria/dashboard_sheets.json`) needs a `runtime-volumes/*-pyegeria-state` bind mount added to *both* `egeria-quickstart.yaml` and `egeria-freshstart.yaml` at the same time it's introduced** — otherwise it's container-local ephemeral state, silently wiped on the next `docker compose up -d --build`/`--force-recreate`, with no error to signal it.

## Tests and diagnostics
- Focused Python tests exist in `compose-configs/egeria-quickstart/PyegeriaWebHandler/tests/`.
- Typical targeted test run: `python -m pytest compose-configs/egeria-quickstart/PyegeriaWebHandler/tests`.
- Useful logs/artifacts: root `build*.log`, `compose-configs/debug_log.log`, and `compose-configs/egeria-quickstart/PyegeriaWebHandler/debug_log.log`.
- For infra readiness, use `docker compose -p egeria-shared-infra -f compose-configs/shared-infra/shared-infra.yaml ps`.

## Change safety checklist for agents
- Keep service names and server-name prefixes consistent (`qs-` quickstart, `fs-` freshstart).
- Do not break shared network/ports contract (`egeria_network`, Kafka `9192/9193/9194`, Postgres `5442`, proxy `6000/6001`).
- Preserve host-mounted persistence paths under `runtime-volumes/` and `exchange-*`.
- If editing compose/env generation, verify both startup scripts and matching README sections remain aligned.
- **Never write an absolute, machine-specific filesystem path (e.g. `/Users/<name>/...`, `/home/<user>/...`) into anything committed** — compose bind mounts, docs, scripts, CLAUDE.md/AGENTS.md notes. This repo is cloned onto multiple machines with different absolute paths (see CLAUDE.md's "If you're Claude running on a different machine than usual"). Compose bind mounts must stay relative to the compose file's own directory (`../../runtime-volumes/...`, matching every existing mount) — never the checkout's absolute path on whichever machine happened to write them.
