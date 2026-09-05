<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Trellis (Resource Explorer + Egeria Advisor) — optional runtime

Demo-profile compose for [Trellis](../../../../trellis): Resource Explorer (RE) and Egeria
Advisor (EA), containerized, joining this checkout's `egeria_network` alongside `shared-infra`
and an Ollama optional runtime. Design background:
`trellis/docs/runtime-architecture-plan.md`.

**This is the demo profile only.** On a dev box, Trellis apps run natively via `uv run`
(`make re-web`, `make ea-web` in the trellis repo) against the same shared-infra containers —
see `docker-compose.yaml`'s header comment for why containerizing the dev loop is dropped.

## Host-native Ollama (Mac dev profile, and trevor's first try)

When inference runs natively on the box (Metal on a Mac; a native CUDA or ROCm Ollama on Linux),
skip the ollama runtime entirely and use the host overlay, which points the apps at
`host.docker.internal:11434` (host Ollama must listen on `0.0.0.0`):

```bash
docker compose \
  -f docker-compose.yaml \
  -f docker-compose.ollama-host.yaml \
  --env-file .env up -d
```

`docker-compose.ollama-container.yaml` is the counterpart for the containerized variants: it joins
the optional ollama service to the shared network and must be in the stack whenever
`../ollama/docker-compose.yaml` is.

## Status

As of 2026-09-04 (trellis branch `re/docs-consolidation-part-2`) everything this runtime references
exists: the two images and `make images`, the `worker` role with leader election, `web` with
`--embed-worker`/`--workers`, and EA's `ADVISOR_MODEL_TIER`. This overlay has been validated with
`docker compose config` on all three variants (CPU, ROCm, NVIDIA) but has **not yet been brought up
on a demo box**. Known gaps: the A2A role is not exposed (no auth yet); the run queue (plan step 2b)
is pending; the EA image needs a writable `./data` mount as the non-root user and its MCP config
still points at a host-only egeria-python venv (see trellis `docs/packaging.md`).

Box-specific: trevor (RTX 2070 SUPER) must run native Docker Engine with the NVIDIA runtime —
Docker Desktop for Linux runs the engine in a VM that cannot see the GPU. hedwig's native Ollama
already carries the ROCm env this overlay's `docker-compose.ollama-rocm.yaml` reproduces.

## One-command bring-up, per box

All commands run from this directory (`compose-configs/optional-associated-runtimes/trellis/`).
Bring shared-infra and egeria-quickstart up first if they aren't already running (see the parent
`egeria-workspaces-fs` README/quickstart docs) — this runtime only adds the two Trellis apps and
Ollama on top of them.

### hedwig (Radeon 890M, ROCm 7.2) — `demo-gpu` tier

```bash
docker compose \
  -f ../ollama/docker-compose.yaml \
  -f docker-compose.ollama-container.yaml \
  -f docker-compose.ollama-rocm.yaml \
  -f docker-compose.yaml \
  --env-file .env up -d
```

### trevor (RTX 2070 SUPER, driver + toolkit installed 2026-09-04; needs native Docker Engine) — `demo-gpu` tier, 8B in every slot

```bash
docker compose \
  -f ../ollama/docker-compose.yaml \
  -f docker-compose.ollama-container.yaml \
  -f docker-compose.ollama-nvidia.yaml \
  -f docker-compose.yaml \
  --env-file .env up -d
```

### cray — `demo-cpu` tier (no LLM-interactive demos; see the plan's measurements)

```bash
docker compose \
  -f ../ollama/docker-compose.yaml \
  -f docker-compose.ollama-container.yaml \
  -f docker-compose.yaml \
  --env-file .env up -d
```

There's no `docker-compose.ollama-cpu.yaml` overlay — `../ollama/docker-compose.yaml` is already
CPU-only (`ollama/ollama:latest`, no GPU stanza), so the CPU path is just the base file with no
overlay, as in the command above.

Set `ADVISOR_MODEL_TIER` (and `TRELLIS_MODEL_CODE`) in `.env` per box first. Owner's decision 2026-09-04: trevor runs the 8B model in every slot including code, because codellama:13b (7.4 GB) does not fit beside llama3.1:8b in 8 GB of VRAM; hedwig can afford the 13B. Copy
`.env.example` to `.env` in this directory and see its tier table.

## Pulling models

Ollama has no models until you pull them, whichever variant is running:

```bash
docker exec ollama ollama pull llama3.1:8b
# demo-gpu boxes only (see .env.example's tier note — not used on demo-cpu):
docker exec ollama ollama pull codellama:13b
```

## Reaching the apps

- **A browser on the LAN**: `http://<box-hostname-or-tailscale-name>:8810` (Resource Explorer),
  `http://<box-hostname-or-tailscale-name>:8880` (Egeria Advisor) — both ports are published on
  the host by `docker-compose.yaml`.
- **The Portal → Advisor tile**: the Portal (`quickstart-pyegeria-web`, in
  `../../egeria-quickstart/egeria-quickstart.yaml`) reads `EGERIA_ADVISOR_URL` to know where EA
  is. Set it in `../../egeria-quickstart/.env` to `http://<box-hostname>:8880/` (or
  `http://trellis-ea-web:8880/` if the Portal container and this runtime share `egeria_network`
  and you'd rather use the container name). The SSO handoff additionally needs
  `EGERIA_ADVISOR_SSO_SECRET` there to equal `ADVISOR_PORTAL_SECRET` set in this directory's
  `.env` — otherwise the tile shows "Not configured" rather than failing loudly.

## Building the images

Bring shared-infra up first on its own (`docker compose -f ../../shared-infra/shared-infra.yaml up -d`), then this runtime from this directory with `--env-file .env`; this file never includes shared-infra.yaml, the same way ../prefect and ../ollama attach to the external `egeria_network`. Build the images from the trellis repo with `make images` (single-arch for the host) or pull the multi-arch images CI publishes to ghcr.io/dwolfson/trellis-resource-explorer and trellis-egeria-advisor and switch `image:` accordingly.

1. Add a Dockerfile per package (multi-stage, matching the ONNX-vs-torch decision
   `runtime-architecture-plan.md`'s sequencing step 1/3 calls for), and a `make images` target
   that builds both and tags them `trellis/resource-explorer:local` /
   `trellis/egeria-advisor:local` — the tags `docker-compose.yaml` in this directory expects.
2. `docker build -t trellis/resource-explorer:local -f packages/resource-explorer/Dockerfile .`
   (and the equivalent for egeria-advisor) is the manual equivalent until the Makefile target
   exists.

Once CI publishes multi-arch (arm64 + amd64) images to ghcr, per the plan's step 3, the intended
paths are:

```
ghcr.io/dwolfson/trellis-resource-explorer
ghcr.io/dwolfson/trellis-egeria-advisor
```

To switch from local images to ghcr ones, change `image:` in `docker-compose.yaml` for
`trellis-re-web` / `trellis-re-worker` (resource-explorer) and `trellis-ea-web`
(egeria-advisor) from the `trellis/...:local` tags to `ghcr.io/dwolfson/trellis-...:<tag>`, or
override per-deployment with a small `docker-compose.images.ghcr.yaml` overlay (not provided
here — the pattern is the same as the two Ollama GPU overlays in this directory) once those
images actually exist.

## What is not here

- **Prefect stays optional.** `PREFECT_ENABLED=false` in both Trellis services here regardless
  of whether the sibling `../prefect` optional runtime is also up — enable it explicitly (and
  point `PREFECT_API_URL` at `http://egeria-optional-prefect-server:4200/api`) only if you're
  actually using it; see `resource_explorer/config.py`'s `PrefectConfig.enabled` docstring for
  why the old default (`true`) leaked orphaned ephemeral servers.
- **No SQLite.** Both apps' registry/vector-store paths are Postgres-only here, matching
  `runtime-architecture-plan.md` §3 ("the SQLite fallback ... is retired").
- **A2A role not yet exposed.** The plan's §2 describes an `a2a` process role (agent-to-agent
  entry point, token-authenticated) for both apps; neither has one today (RE's existing
  `agentstack_server.py` / `resource-explorer serve` is unauthenticated and out of scope for this
  compose). Not included here.
- **`WORKERS` and `EMBED_WORKER`** are read by the image entrypoint; the demo profile runs `web` with `EMBED_WORKER=false` beside one `worker` replica, and leader election stops duplicate loops if both are ever set.
- **`../ollama/docker-compose.yaml`'s missing `egeria_network` join.** That file predates this
  optional runtime and joins no network of its own (reachable only via its published host port).
  `docker-compose.yaml` in this directory adds the join itself (a small `ollama:` service
  override, applied last in every bring-up command above, CPU-only included) rather than relying
  on the GPU overlays for it, so all three bring-up paths reach `ollama:11434` by service name.
  The GPU overlays also declare the same join for the boxes that need the rest of their content;
  the two declarations are redundant, not conflicting.
