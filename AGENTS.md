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
- Rebuild behavior is intentional: scripts use `docker compose build --pull` and `up -d --pull always`; `NO_CACHE=1` adds `--no-cache` via `compose-configs/shared-infra/compose-build-flags.sh`; `--refresh-platform` on `*-start-local` forces platform image refresh.

## Project-specific conventions
- `quick-start-*` and `fresh-start-*` repopulate runtime server configs on each start from `compose-configs/egeria-quickstart/servers` into `runtime-volumes/*/data/servers`.
- Freshstart secrets are seeded from templates in `compose-configs/egeria-freshstart/secrets/` only when files are missing (never overwrite existing runtime secrets).
- `gen-env.sh` in each deployment rewrites `exchange-*/config/config.json` with current `HOST_FQDN`, server names (`qs-*` vs `fs-*`), and saves `config.json.bak` once.
- Local vs multi-host overlays differ mainly by `extra_hosts` host-gateway mapping (`*-local.yaml` vs `*-cluster.yaml`); keep this behavior symmetric across quickstart/freshstart.
- When changing one flavor, check the sibling flavor for parity (`egeria-quickstart` <-> `egeria-freshstart`).

## PyegeriaWebHandler and MCP integration
- Main backend entrypoint: `compose-configs/egeria-quickstart/PyegeriaWebHandler/pyegeria_handler.py` (FastAPI + router modules by domain).
- MCP server entrypoint: `compose-configs/egeria-quickstart/PyegeriaWebHandler/mcp_server.py`; Obsidian MCP plugin is in `obsidian-plugins/calling-the-dr/`.
- Token-gated SSE/messages endpoints rely on `MCP_ACCESS_TOKEN` (see middleware in `pyegeria_handler.py`).
- `pyegeria-web` is mounted read-write to workspace folders (`/app`, `/config`, `/work`, templates, demo data), so path changes must preserve container mount assumptions.

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
