# Portal and Apache images for Kubernetes (TR-112a)

Compose does not use these files. It builds `Dockerfile-fast-api` and `Dockerfile-apache-web`, bind-mounts
the code, and runs as root. These are the images a Helm chart runs.

| Image | Dockerfile | Build context | Tag |
|---|---|---|---|
| `portal-quickstart` | `egeria-quickstart/PyegeriaWebHandler/Dockerfile-portal-image` | that directory | `quickstart-<egeria release>-<short sha>` |
| `portal-freshstart` | `egeria-freshstart/PyegeriaWebHandler/Dockerfile-portal-image` | that directory | `freshstart-<egeria release>-<short sha>` |
| `apache-web` | `egeria-quickstart/Dockerfile-apache-web-nonroot` | `egeria-quickstart/` | `<egeria release>-<short sha>` (one image, environment-neutral) |

Build and prove them with `sg docker -c 'bash charts/tests/proof112a.sh build'` (without `build` it re-tests the current tags).

## What each image does

* Runs as **UID 1001, GID 0**. Every written path is group 0 with `g=u`, so OpenShift's arbitrary UID (GID 0) works.
* Portal: the code is baked in (`COPY . .`) and uvicorn runs **without `--reload`**, bound to `0.0.0.0:8000`
  (`PORTAL_BIND` overrides; compose's `::` is IPv6-only under asyncio). Health route: `GET /` answers 200 `{"status":"ok"}`.
* `HOME=/home/portal`: pyegeria has no single state-directory variable. Its state, the report-spec cache, the
  bootstrap ledger, dashboard sheets and notebook runs all resolve `~/.pyegeria`, so `HOME` moves them. Mount the state volume at `/home/portal/.pyegeria`.
* Logs go to `/app/logs` (`PYEGERIA_LOG_DIRECTORY`).
* Dr.Egeria's inbox and outbox: compose sets `EGERIA_ROOT_PATH=/`, which a non-root user cannot write. The image defaults to
  `EGERIA_ROOT_PATH=/app/dr-egeria`, `EGERIA_INBOX_PATH=dr-egeria-inbox`, `EGERIA_OUTBOX_PATH=dr-egeria-outbox`
  (group 0, `g=u`). Mount a volume at `/app/dr-egeria` to keep them.
* `egeria_request_body_catalog.json` is tracked and rebuilt in place by `_rebuild_catalog`, so the file and `/app` are `g=u`.
* `Dockerfile-portal-image.dockerignore` (BuildKit; compose's `Dockerfile-fast-api` build is untouched) keeps logs, `debug_log.log`,
  `.venv`, `.hypothesis`, result XML and `.db` files out of `COPY . .`; the proof builds from a context with such files and checks.
* The Obsidian handler writes its plugin `data.json` under `/coco-workbooks/.obsidian/`. With `/coco-workbooks` mounted read-only
  that write fails: mount it writable if the Obsidian lock feature is used (demo mode), or leave that feature off.
* Apache: listens on 8085, PID file `/tmp/httpd.pid`, writable `logs/`. There is one Apache image for both environments,
  with one environment-neutral tag. Its built-in `httpd.conf`, `fastapi-proxy.conf` and `proxy-locations.conf` are
  **quickstart's**: an HTTP vhost that only redirects to https, and `proxy-locations.conf` points at `quickstart-pyegeria-web`.
  They exist so the image starts alone. **The chart supplies the real serving vhost** (and the freshstart proxy target) as a ConfigMap
  mounted over `conf/extra/`.
  It inherits `EXPOSE 80` from the httpd base image (metadata only; it never listens there, and the test proves that).
  `fastapi-ssl.conf` is not baked in: `httpd.conf` includes it optionally and it fails without its certificates.
  Set `HTTPS_REDIRECT_PORT` (compose does); unset, the http listener's redirect to https carries a literal `${HTTPS_REDIRECT_PORT}`.

## Content compose mounts: baked in or mounted?

Nothing is baked in except the handler code. Each is left for the chart to mount, because it lives outside the
build context (the repository root, not `PyegeriaWebHandler/`), is edited by users, or is state.

| Compose mount | In the image? | Why |
|---|---|---|
| `./PyegeriaWebHandler:/app` | **baked** (`COPY . .`) | the code |
| `exchange-*/config:/config` | mounted | environment config, outside the context |
| `work:/work` | mounted | user working files |
| `coco-workbooks:/coco-workbooks` | mounted | user-edited notebooks, large, outside the context |
| `design-patterns:/design-patterns` | mounted | content, outside the context |
| `templates:/app/templates` | mounted | shared with Dr.Egeria, outside the context (a ConfigMap or PVC) |
| `runtime-volumes/*-demo-data:/app/demo-data` | mounted | sqlite state (demo.db, feedback.db, lock files) |
| `runtime-volumes/*-pyegeria-state:/root/.pyegeria` | mounted at `/home/portal/.pyegeria` | state |
| `exchange-*/coco-dags:/app/coco-dags` | mounted | content |
| five `exchange-*/<name>:/deployments/<name>:ro` (loading-bay, landing-area, coco-data-lake, distribution-hub, treasury-dts-history) | mounted read-only | the platform's data exchange folders (same PVCs) |
| Apache: `work`, `coco-workbooks`, `templates`, `portal-docs` under `htdocs`, `logs` | mounted | content and logs |

The two Portal copies are separate because the code diverges. `proof112a.sh` also checks that `docker compose config`
for both compose files is identical to the commit before this work.

## Not done here

The images are built and tagged locally. They are not pushed anywhere: a local registry on this machine is a separate step.
