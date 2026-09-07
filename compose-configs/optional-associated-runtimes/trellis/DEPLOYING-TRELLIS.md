<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Deploying, configuring and running Trellis with the Egeria QuickStart

Trellis is two applications that sit beside an Egeria deployment:

- **Resource Explorer (RE)** scouts, surveys, publishes and curates software resources (GitHub
  repositories today) into Egeria, and answers questions about them.
- **Egeria Advisor (EA)** answers questions about Egeria itself and runs Egeria reports, with a
  retrieval corpus over the Egeria code bases and documentation.

Both use the QuickStart's Egeria platform, the shared Postgres (pgvector) and Kroki from
`shared-infra`, an Ollama model server, and the QuickStart Portal's login. This document covers the
three ways they are run, what each needs, and how to check that it works:

| Configuration | Egeria + infra | RE and EA | Ollama | Typical box |
|---|---|---|---|---|
| **QuickStart demo** (§2) | containers | containers, from the `trellis` optional runtime | host-native or container | a demo box on the LAN |
| **Mac developer** (§3) | containers (Docker Desktop) | native, `uv run` from a trellis checkout | host-native, Metal | M-series laptop |
| **Linux developer** (§4) | containers (native Docker Engine) | native, `uv run` from a trellis checkout | host-native, CUDA or ROCm | workstation or laptop with a GPU |

The same document is kept in both repositories:
`egeria-workspaces/compose-configs/optional-associated-runtimes/trellis/DEPLOYING-TRELLIS.md` and
`trellis/docs/deploying-trellis-with-quickstart.md`. Change both.

---

## 1. Common ground

### 1.1 Repositories

| Repository | What it holds | Where |
|---|---|---|
| `egeria-workspaces` | shared-infra, the QuickStart, the Portal, and the `trellis` optional runtime (compose files, `.env.example`) | `compose-configs/optional-associated-runtimes/trellis/` |
| `trellis` | RE and EA source, the Dockerfiles, the Makefile used in the developer configurations | `packages/resource-explorer`, `packages/egeria-advisor`, `docker/` |

Check them out side by side. The developer configurations run the apps from the `trellis`
checkout; the demo configuration only needs it if you build the images locally.

### 1.2 What must already be running

In every configuration, bring these up first from the `egeria-workspaces` checkout, as described
in the QuickStart's own documentation (`portal-docs/quickstart/`):

1. The external Docker network: `docker network create egeria_network` (declared `external`
   everywhere, created nowhere).
2. `shared-infra` (Kafka, Postgres with pgvector on host port 5442, Kroki).
3. The QuickStart (`./quick-start-local`), which starts the Egeria platform on port 9443 with the
   `qs-*` servers and the Portal on port 8800 (8843 with TLS).

Wait for `OMAG Server 'qs-view-server' successful start` in `docker logs quickstart-egeria-main`
before starting either app.

### 1.3 Identities

All identities are the QuickStart's demo users, defined in
`compose-configs/egeria-quickstart/secrets/coco-user-directory.omsecrets` (password `secret`):

| Purpose | User |
|---|---|
| Service account for background work (the RE worker role, EA's non-interactive calls) | `erinoverview` |
| Signing in to either app, in the browser or on the command line | any demo user, e.g. `peterprofile` |
| Platform-services reads used in the checks below | `garygeeke` |

**Login is required by both apps.** A signed-in user's Egeria bearer token travels inside the app's
session token; the apps never hold the user's password. Everything a user publishes, surveys or
runs is attributed to that user in Egeria (Ownership, `createdBy`, report provenance). Egeria's
platform tokens last one hour; an app session is the shorter of that and the app's own TTL.

### 1.4 Secrets and where they come from

| Key | Meaning | Source |
|---|---|---|
| `TRELLIS_JWT_SECRET` | signs the apps' own session tokens; every RE/EA process on a box must share it | generate once per box: `openssl rand -hex 32` |
| `ADVISOR_PORTAL_SECRET` / `TRELLIS_PORTAL_SECRET` | lets the Portal hand a signed-in user to EA and RE | the same value as the QuickStart's `EGERIA_ADVISOR_SSO_SECRET` |
| `PGVECTOR_PASSWORD` | the `egeria_advisor` Postgres role | `shared-infra/docker-entrypoint-initdb.d/init_egeria.sql` (default `advisor`) |
| `GITHUB_TOKEN` | RE's GitHub API access for surveys and discovery | a personal token with read scope; without it GitHub's 60 calls/hour are gone in one survey |
| `EGERIA_USER` / `EGERIA_USER_PASSWORD` | the service account above | `erinoverview` / `secret` |

Never commit any of these, and never bake them into an image (the trellis `.dockerignore`
excludes `.env` files for that reason).

### 1.5 Ports

| Port | Service |
|---|---|
| 8810 | Resource Explorer web (and API) |
| 8880 | Egeria Advisor web (and API) |
| 9443 | Egeria platform (HTTPS, self-signed) |
| 8800 / 8843 | QuickStart Portal (HTTP / HTTPS) |
| 5442 | shared Postgres (pgvector) |
| 11434 | Ollama |

### 1.6 Model tiers

Both apps read a model tier that chooses models, context size and retrieval budget:

| Tier | Where | Models | Notes |
|---|---|---|---|
| `dev` | developer laptops | `llama3.1:8b` general, `codellama:13b` code, 32k context | the default when unset |
| `demo-gpu` | a demo box with a usable GPU | `llama3.1:8b`, code model per box, 8k context, 2k retrieval budget | interactive: seconds to first token |
| `demo-cpu` | a demo box without a GPU | `llama3.1:8b` everywhere, 8k context, 2k retrieval budget | not interactive: minutes to first token; demo the non-LLM paths |

In the demo configuration one variable, `TRELLIS_MODEL_TIER`, feeds both apps. In the developer
configurations set `EXPLORER_MODEL_TIER` (RE) and `ADVISOR_MODEL_TIER` (EA), or leave them unset.

Pull the models into whichever Ollama you run: `ollama pull llama3.1:8b` (and `codellama:13b`
where the tier uses it).

---

## 2. QuickStart demo configuration (everything in containers)

This is the `trellis` optional runtime: three containers (`trellis-re-web`, `trellis-re-worker`,
`trellis-ea-web`) joining `egeria_network` beside the QuickStart. All commands run from
`compose-configs/optional-associated-runtimes/trellis/`.

### 2.1 Images

Either pull the multi-arch images CI publishes on every merge to `main`:

```
ghcr.io/dwolfson/trellis-resource-explorer:main
ghcr.io/dwolfson/trellis-egeria-advisor:main
```

or build them on the box from the trellis checkout (`make images`, about six minutes with a warm
cache; tags `trellis/resource-explorer:local` and `trellis/egeria-advisor:local`). The compose file
names the tags it expects; edit `image:` or add a small overlay to switch between the two.

### 2.2 Environment

```bash
cp .env.example .env && chmod 600 .env
```

Fill in the keys from §1.4 and set `TRELLIS_MODEL_TIER` for the box. The file documents every
other knob (worker count, model names, CORS origins).

### 2.3 Bring-up, by where Ollama runs

Always pass `--env-file .env` (compose reads the `.env` next to the *first* file it is given) and
never include `shared-infra.yaml` in the command: this runtime attaches to the existing network
like the other optional runtimes.

**Host-native Ollama** (a Mac, or a Linux box whose GPU is used by a native Ollama). The host
Ollama must listen on all interfaces, `OLLAMA_HOST=0.0.0.0:11434`:

```bash
docker compose -p trellis -f docker-compose.yaml -f docker-compose.ollama-host.yaml --env-file .env up -d
```

**Ollama in a container, CPU only:**

```bash
docker compose -p trellis -f ../ollama/docker-compose.yaml -f docker-compose.ollama-container.yaml \
  -f docker-compose.yaml --env-file .env up -d
```

**Ollama in a container with an NVIDIA GPU** (needs the NVIDIA driver, `nvidia-container-toolkit`,
and native Docker Engine, see §4.1):

```bash
docker compose -p trellis -f ../ollama/docker-compose.yaml -f docker-compose.ollama-container.yaml \
  -f docker-compose.ollama-nvidia.yaml -f docker-compose.yaml --env-file .env up -d
```

**Ollama in a container with an AMD GPU (ROCm):** as above with `docker-compose.ollama-rocm.yaml`.

Then pull the models into the container: `docker exec ollama ollama pull llama3.1:8b`.

### 2.4 Portal tiles

The Portal shows a tile for each app. In the QuickStart's `compose-configs/egeria-quickstart/.env`
set:

```
EGERIA_ADVISOR_URL=http://<box-hostname>:8880/
EGERIA_RESOURCE_EXPLORER_URL=http://<box-hostname>:8810/
EGERIA_ADVISOR_SSO_SECRET=<same value as ADVISOR_PORTAL_SECRET in the trellis .env>
```

Use the hostname a browser on the LAN will use, not `localhost`, unless the browser runs on the
box itself. With the secret set on both sides, opening a tile signs the Portal's user into the app;
without it the tile still opens the app, which then asks for a login.

`./quick-start-local` regenerates that `.env` on each run. It carries `EGERIA_ADVISOR_URL` and
`EGERIA_ADVISOR_SSO_SECRET` over from the previous file, but not `EGERIA_RESOURCE_EXPLORER_URL`,
which falls back to `http://localhost:8810/`. Re-add it after each run on a LAN demo box.

### 2.5 Check that it works

```bash
curl -s localhost:8810/health/ready; curl -s localhost:8880/health            # both ok
curl -s -o /dev/null -w '%{http_code}\n' localhost:8810/api/projects/           # 401: login is required
docker logs trellis-re-worker | grep 'worker loop started'                       # three loops, leader=true
docker logs trellis-ea-web | grep -E 'Initialized Ollama client|MCP agent'      # Ollama reached, MCP connected
```

Open `http://<box>:8810` and `http://<box>:8880`, sign in as a demo user, and confirm the user is
shown as signed in. From the Portal, open both tiles.

A signed-in end-to-end run through the command line, using the web image (`C` is the compose
command from §2.3):

```bash
C='docker compose -p trellis -f docker-compose.yaml -f docker-compose.ollama-host.yaml --env-file .env'
$C run --rm --no-deps trellis-re-web cli add https://github.com/odpi/egeria-python.git --yes
echo secret | $C run --rm --no-deps -T --entrypoint sh trellis-re-web -c \
  'resource-explorer login --user erinoverview; resource-explorer survey egeria_python_git --publish'
```

The published asset and its survey report read back from Egeria with `createdBy` and
`Ownership.owner` equal to the user who logged in, and zone `resource-explorer-draft` until a
curator accepts it.

Load EA's retrieval corpus once per box (clones the Egeria repositories into the container's data
volume and indexes them into pgvector):

```bash
docker exec -w /app/packages/egeria-advisor trellis-ea-web python scripts/clone_repos.py --phase 1
docker exec -w /app/packages/egeria-advisor trellis-ea-web python scripts/ingest_collections.py --phase 1
```

### 2.6 Operating

- Logs: `docker logs -f trellis-re-web`, `trellis-re-worker`, `trellis-ea-web`.
- Stop: the same compose command with `stop` (keeps data) or `down` (keeps named volumes).
- Upgrade: pull or rebuild the images, then `up -d` again. Both apps migrate their own Postgres
  schemas at start.
- Data lives in the named volumes mounted at `/app/data` and in the shared Postgres. Nothing is
  written into the image.

### 2.7 Docker Desktop instead of native Docker Engine

The same compose files run under Docker Desktop on Linux or Mac. What changes:

- **No GPU inside the Desktop VM**, so use a host-native Ollama with the host overlay (§2.3).
- **Two engines, one CLI.** Starting Desktop makes `desktop-linux` the active context; every
  `docker` command then talks to the VM until you switch back with `docker context use default`.
  Check `docker context show` first when both are installed.
- **VM sizing.** Give the VM at least 24 GB and most cores: the Egeria core needs about 8 GB and
  the two apps another 5 GB.
- **Separate state.** Images, named volumes and networks built on one engine do not exist on the
  other; bind mounts under `runtime-volumes/` are host paths and work the same.

---

## 3. Mac developer configuration

Infra and Egeria in Docker Desktop, the apps and Ollama native. The apps reload on code changes.

### 3.1 Prerequisites

- Docker Desktop, with `shared-infra` and the QuickStart running (§1.2). The Portal's own local
  setup guide is `portal-docs/quickstart/local/overview.md`.
- [uv](https://docs.astral.sh/uv/) and Python 3.13 (uv installs it).
- Ollama for macOS, running natively (it uses Metal). Pull `llama3.1:8b` and `codellama:13b`.
- A trellis checkout: `git clone https://github.com/odpi/egeria-trellis.git trellis`.

### 3.2 Install

```bash
cd trellis && uv sync --all-packages
```

This creates one virtual environment for the workspace with both apps, the shared `trellis-*`
libraries, and `pyegeria`. EA launches pyegeria's MCP server from this same interpreter, so
nothing else is needed for reports.

### 3.3 App environment files

Each app reads a `.env` in its own package directory. Start from the examples:

```bash
cp packages/resource-explorer/.env.example packages/resource-explorer/.env
cp packages/egeria-advisor/.env.example    packages/egeria-advisor/.env
```

Minimum edits:

| File | Keys |
|---|---|
| both | `TRELLIS_JWT_SECRET=<one value shared by both files>` so sessions survive restarts (`RE_JWT_SECRET` / `ADVISOR_JWT_SECRET` per app also work) |
| RE | `GITHUB_TOKEN`; `EGERIA_PLATFORM_URL=https://localhost:9443`, `EGERIA_VIEW_SERVER=qs-view-server`, `EGERIA_USER=erinoverview`, `EGERIA_USER_PASSWORD=secret`; `LLM__OLLAMA__BASE_URL=http://localhost:11434` |
| EA | `EGERIA_VIEW_SERVER_URL=https://localhost:9443`, `EGERIA_VIEW_SERVER=qs-view-server`, `EGERIA_USER` / `EGERIA_PASSWORD`; `OLLAMA_BASE_URL=http://localhost:11434`; `ADVISOR_DATA_PATH` to where EA's corpus should live |
| optional | `ADVISOR_PORTAL_SECRET` / `RE_PORTAL_SECRET` equal to the QuickStart's `EGERIA_ADVISOR_SSO_SECRET` for tile handoff; `EXPLORER_MODEL_TIER` / `ADVISOR_MODEL_TIER` (default `dev`) |

Postgres defaults (`localhost:5442`, database `egeria_advisor`, user `egeria_advisor`, password
`advisor`) match `shared-infra`; override the `PGVECTOR_*` keys only if you changed the init SQL.

`TRELLIS_ANONYMOUS_READ=true` is a developer-only override that lets read-only requests through
without a login. Do not use it on a demo box.

### 3.4 Run

```bash
make dev        # RE web on 8810 with the worker embedded, and EA web on 8880; Ctrl-C stops both
```

or individually: `make re-web`, `make re-worker`, `make ea-web`. `make ps` lists every trellis
process and container with its role, age and port. `make help` lists the rest (tests, lint,
image builds).

Command-line use needs a login once per hour; the token is cached under
`~/.config/trellis/<app>/session.json`:

```bash
uv run --package resource-explorer resource-explorer login --user peterprofile
uv run --package egeria-advisor egeria-advisor login --user peterprofile
```

### 3.5 Portal tiles on a laptop

With the QuickStart Portal on the same machine, the compose defaults already point the tiles at
`http://localhost:8880/` and `http://localhost:8810/`. Set `EGERIA_ADVISOR_SSO_SECRET` in the
QuickStart `.env` to the value in the app `.env` files if you want the handoff.

### 3.6 Check that it works

Same as §2.5, against `localhost`, plus the two things that only exist natively:

- EA's startup log ends with `MCP agent pre-warmed on startup` (the pyegeria MCP server started).
- `make ps` shows the RE web process holding the three leader locks (embedded worker) and no
  stray processes.

Load EA's corpus with the same two scripts as §2.5, run from `packages/egeria-advisor` with
`uv run python scripts/...`.

---

## 4. Linux developer configuration

Identical to the Mac configuration except for the engine, the GPU and the paths. Follow §3 with
these changes.

### 4.1 Engine and GPU

- Use native Docker Engine (`docker-ce`) rather than Docker Desktop for Linux: Desktop's VM cannot
  see the GPU, and starting it flips the active `docker context` (§2.7). If both are installed,
  `systemctl --user disable docker-desktop` and `docker context use default`.
- NVIDIA: the proprietary driver plus `nvidia-container-toolkit`; then
  `sudo nvidia-ctk runtime configure --runtime=docker && sudo systemctl restart docker`.
  `docker run --rm --gpus all ubuntu:22.04 nvidia-smi -L` must list the card. This matters only if
  you want a *containerized* Ollama; a native Ollama uses the driver directly.
- AMD: a native Ollama picks up ROCm on supported cards; for an integrated GPU it may need
  `HSA_OVERRIDE_GFX_VERSION` (the ROCm overlay in the trellis runtime shows the values used on a
  Radeon 890M).
- Ollama on Linux ships as `.tar.zst` releases. Run it as a user service with
  `OLLAMA_HOST=0.0.0.0:11434` if containers must reach it; `127.0.0.1` is enough when only the
  native apps use it.

### 4.2 Embeddings device

The apps auto-detect `cuda`, `mps` or `cpu` for the sentence-transformer embeddings. Set
`EMBEDDINGS__DEVICE` (RE) and `EMBEDDING_DEVICE` (EA) explicitly if detection picks the wrong one.

### 4.3 Expectations

Measured with `llama3.1:8b` and a 5.3k-token prompt: an RTX 2070 SUPER answers in about three
seconds to first token; a Radeon 890M in about twenty; the same CPUs without a GPU take two to
three minutes. On a CPU-only Linux box use the `demo-cpu` tier and treat the LLM features as
batch, not interactive.

---

## 5. Configuration reference

Keys the apps read, grouped by concern. `<APP>_` forms override the shared `TRELLIS_` form.

| Concern | Resource Explorer | Egeria Advisor | Demo compose (`trellis/.env`) |
|---|---|---|---|
| Session signing secret | `RE_JWT_SECRET` or `TRELLIS_JWT_SECRET` | `ADVISOR_JWT_SECRET` or `TRELLIS_JWT_SECRET` | `TRELLIS_JWT_SECRET` |
| Session lifetime | `RE_JWT_TTL_HOURS` (default 8; Egeria's token caps it at 1 h) | same mechanism | inherited |
| Portal handoff secret | `RE_PORTAL_SECRET` or `TRELLIS_PORTAL_SECRET` | `ADVISOR_PORTAL_SECRET` | `ADVISOR_PORTAL_SECRET` (fed to both) |
| Login policy | `TRELLIS_REQUIRE_LOGIN` (default true), `TRELLIS_ANONYMOUS_READ` (dev only), `RE_PUBLIC_PATHS` | same, `TRELLIS_PUBLIC_PATHS` | defaults |
| Egeria platform | `EGERIA_PLATFORM_URL`, `EGERIA_VIEW_SERVER`, `EGERIA_USER`, `EGERIA_USER_PASSWORD`, `PYEGERIA_TIMEOUT_SECONDS` | `EGERIA_VIEW_SERVER_URL`, `EGERIA_VIEW_SERVER`, `EGERIA_USER`, `EGERIA_PASSWORD` | set in compose; service account from `EGERIA_USER` / `EGERIA_USER_PASSWORD` |
| Ollama | `LLM__OLLAMA__BASE_URL`, `LLM__OLLAMA__MODEL` | `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, `OLLAMA_CODE_MODEL` | `TRELLIS_MODEL_GENERAL`, `TRELLIS_MODEL_CODE`, plus the overlay choice |
| Model tier | `EXPLORER_MODEL_TIER` | `ADVISOR_MODEL_TIER` | `TRELLIS_MODEL_TIER` |
| Postgres / pgvector | `PGVECTOR_*` or `REGISTRY_DATABASE_URL` | `PGVECTOR_*` | `PGVECTOR_PASSWORD` |
| Kroki | `KROKI_URL` | `KROKI_URL` | set in compose |
| GitHub | `GITHUB_TOKEN`, `GITHUB_WEBHOOK_SECRET` | | `GITHUB_TOKEN` |
| Process roles | `EXPLORER_EMBED_WORKER`, `EXPLORER_SYNC_POOL_SIZE` | | `TRELLIS_RE_WEB_WORKERS`; `WORKERS` / `EMBED_WORKER` read by the image entrypoint |
| Data root | `data/` under the package | `ADVISOR_DATA_PATH`, `ADVISOR_CACHE_DIR` | `/app/data` volumes |
| Observability (optional) | `OBSERVABILITY__MLFLOW__*`, `OBSERVABILITY__PHOENIX__*` | `MLFLOW_*`, `PHOENIX_*` | off |

Neither app uses SQLite in these configurations; the registry, run queue and vector store are all
in the shared Postgres.

---

## 6. Troubleshooting

| Symptom | Cause and fix |
|---|---|
| Every API call returns 401 | Login is required. Sign in in the browser, or run the app's `login` command for the CLI. |
| Sessions vanish on every restart | No shared signing secret: set `TRELLIS_JWT_SECRET` (both app `.env` files, or the compose `.env`). The apps warn once at start when they fall back to a derived secret. |
| Portal tile says "Not configured" | `EGERIA_ADVISOR_SSO_SECRET` (QuickStart) and `ADVISOR_PORTAL_SECRET` (trellis) differ or are unset. |
| EA start shows `No response from MCP server` | The pyegeria MCP server failed at import; the usual cause is an mcp package below 2.0 (pyegeria declares too loose a floor). Trellis pins `mcp>=2.0`; re-run `uv sync`. |
| Reports fail with `User ... is not recognized` in the platform log | The view server cannot read the user directory. Check `/deployments/secrets` inside `quickstart-egeria-main` has the `.omsecrets` files; if it is empty, restart that container (a Docker Desktop bind mount went stale after the host directory was rewritten). |
| Surveys stop with GitHub 403 / rate limit | No `GITHUB_TOKEN`; unauthenticated GitHub allows 60 calls an hour. |
| `docker compose` cannot find `egeria_network` | Create it once: `docker network create egeria_network`. |
| Stack "disappeared" after starting Docker Desktop on Linux | The active context flipped to `desktop-linux`; `docker context use default`. |
| Docker Desktop's log pane is blank for a container | A viewer glitch after restart or log rotation; reopen the tab, or use `docker logs -f <container>`. |
| Orphaned `prefect` server processes | Prefect is off by default (`PREFECT_ENABLED=false`); `make ps` lists strays. Enable it only against the Prefect optional runtime. |
| `qs-engine-host` logs `startMissedEngineActions` errors every few seconds on a fresh repository | Egeria-side (egeria-python `PYEGERIA_ISSUES.md` ISSUE-90); costs CPU but does not affect the apps. |
| The apps talk to Egeria through `host.docker.internal` rather than the container name | Deliberate: the platform image's certificate names only `localhost` and `host.docker.internal`. A request for more SANs is filed with Egeria; do not switch to the container name until it lands. |

---

## 7. Further reading

- `trellis/docs/runtime-architecture-plan.md`: why the profiles, process roles, login model and
  tiers look the way they do, with the measurements behind the tier table.
- `trellis/docs/demo-deployment-runbook.md`: the verbatim sequence that brought the demo
  configuration up on a Linux box with an NVIDIA GPU, including the host-prerequisite steps.
- `trellis/docs/portal-integration.md`: the Portal handoff contract.
- `trellis/docs/packaging.md` and `packages/resource-explorer/docs/process-model.md`: images,
  entrypoints and the web / worker / cli / a2a roles.
- `egeria-workspaces/portal-docs/quickstart/local/overview.md`: the QuickStart's own local setup.
- `egeria-workspaces/portal-docs/tools/egeria-advisor.md` and `resource-explorer.md`: using the
  two tools from the Portal.
