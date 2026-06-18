# Hand-off: wire the full `my_egeria` app into Egeria-Workspaces

Audience: maintainers of the **egeria-workspaces** repo.
Goal: expose the main **MyEgeria** Textual app in the portal (browser) and keep
it runnable in a terminal, alongside the existing `my_profile` app.

This is the same integration pattern already used for `my_profile`
(see `EGERIA_WORKSPACES_INTEGRATION.md` for the full design rationale and the
ME-1…ME-7 backlog history). This file lists what is **new** for the full app and
has been **reconciled against the actual repo wiring** — see the validation
section below for where the upstream hand-off's generic instructions diverge
from how this repo really works.

---

## Validation results (2026-06-18)

Checked the original hand-off against this repo + the local `egeria-python`
(6.0.15.1) clone and the live `my-profile` service.

**Confirmed (upstream side is done):**

- egeria-python **6.0.15.1** (published to PyPI) defines console entry points
  `my_egeria` → `my_egeria.main:main`, `serve_my_egeria` →
  `my_egeria.serve:serve_my_egeria`, and `serve_my_profile`.
- Module rename is done: `my_egeria/my_egeria/my_egeria_app.py` exists;
  `serve_my_egeria()` serves module `my_egeria.my_egeria_app`, port env
  `MY_EGERIA_PORT` (default `8021`), host env `MY_EGERIA_HOST`.
- The `my_egeria` package ships alongside `pyegeria`, so a container that does
  `pip install pyegeria --upgrade` (as `Dockerfile-my-egeria` already does) gets
  the app. **Build-time check still required:** confirm the installed wheel
  actually contains `my_egeria/my_egeria_app.py` (the host's pinned 6.0.12.9
  does *not*).

**Corrections — the original hand-off does NOT match this repo:**

| Hand-off said | This repo's reality |
|---|---|
| `image: python:3.12-slim` + `command: serve_my_egeria` | Custom **`Dockerfile-my-egeria`** (`pip install pyegeria --upgrade nest_asyncio` + `textual==6.1.0`, injects a missing `.tcss`, copies a **local serve wrapper**, `CMD` runs that wrapper). |
| Use the `serve_my_egeria` entry point directly | **Do NOT.** Upstream `serve.py` calls `textual serve …` with **no `public_url`** and relies on the `textual` console script (which `pip install textual` does *not* install). Through the Apache proxy this re-breaks CSP / mixed-content (the ME-7 bug). This repo runs `textual_serve.server.Server(..., public_url=…)` **programmatically** from a local `serve_*.py`. Add a new wrapper for the full app. |
| Ports `8021:8021` | Host-port scheme is **88xx (quickstart) / 78xx (freshstart)**, container port unchanged. `my-profile` = `8820:8020`. Full app → **`8821:8021`** (qs) / **`7821:8021`** (fs). |
| Port env `MY_EGERIA_PORT` for my_profile | The my_profile wrapper reads **`MY_PROFILE_PORT`** (8020). The full app reads **`MY_EGERIA_PORT`** (8021). Keep one `MY_*_PORT` per app; only `MY_EGERIA_HOST` is shared. |
| nginx `location` block | **Apache** `mod_proxy_wstunnel`. Routes go in the **shared** `sites-available/proxy-locations.conf` (included by *both* the HTTP `:8085` and HTTPS vhosts — so no per-vhost duplication and no "missing on SSL" regression). Use `upgrade=websocket`. |
| Portal `<a class="portal-card">` HTML | Portal tiles are a **JS `apps` array** in `demo-portal.html` (`{ icon, name, url, newTab, enabled }`). |
| (not mentioned) | **`MY_EGERIA_PUBLIC_URL`** is required for the CSP/same-origin fix; the demo overlay (`egeria-quickstart-demo.yaml`) overrides it to `https://…` to avoid a mixed-content WebSocket block. Also needs `extra_hosts` (host.docker.internal), `depends_on: egeria-main healthy`, and `networks: [egeria_network]`. |
| (not mentioned) | `quick-start-local` must **build + start** the new service and run its Podman network fix (`_podman_fix_network`) so the container lands on `egeria_network`. |

**Naming conflict to resolve (decision needed):** the existing `/my-egeria/`
route and the "My Egeria" portal tile currently point at the **my_profile demo**
app, not the full app. Pick one:
- **(A)** Re-purpose `/my-egeria/` for the full app and move my_profile to
  `/my-profile/` (names match the apps; updates the existing route + tile). Recommended.
- **(B)** Add a second route like `/my-egeria-app/` and keep my_profile on
  `/my-egeria/` (less churn, but the labels stay misleading).

---

## What egeria-workspaces needs to do (repo-accurate steps)

These assume **option (A)** for routing; adjust paths for (B). Apply to **both**
quickstart and freshstart (per the shared-codebase convention).

### 1. Add a serve wrapper for the full app

Create `compose-configs/egeria-quickstart/serve_my_egeria_app.py`, mirroring the
existing `serve_my_egeria.py` (which serves my_profile) but pointing at the full
app module and reading `MY_EGERIA_PORT`:

```python
import os, sys, importlib.util
from textual_serve.server import Server

spec = importlib.util.find_spec("my_egeria.my_egeria_app")
app  = spec.origin
host = os.environ.get("MY_EGERIA_HOST", "0.0.0.0")
port = int(os.environ.get("MY_EGERIA_PORT", "8021"))
public_url = os.environ.get("MY_EGERIA_PUBLIC_URL") or None  # CSP same-origin

Server(command=f"{sys.executable} {app}", host=host, port=port,
       public_url=public_url).serve()
```

### 2. Build image for the full app

Add `Dockerfile-my-egeria-app` (copy of `Dockerfile-my-egeria`) that `COPY`s
`serve_my_egeria_app.py` and sets `CMD ["python", "/usr/local/bin/serve_my_egeria_app.py"]`,
`EXPOSE 8021`. (Or parametrise the existing Dockerfile with a build ARG.)

### 3. Add a compose service (quickstart) — mirror `my-profile`

```yaml
  my-egeria-app:
    image: egeria-quickstart-my-egeria-app:local
    container_name: quickstart-my-egeria-app
    build:
      context: .
      dockerfile: Dockerfile-my-egeria-app
    networks:
      - egeria_network
    ports:
      - "8821:8021"                       # 88xx host scheme
    environment:
      EGERIA_PLATFORM_URL:  "https://host.docker.internal:9443"
      EGERIA_VIEW_SERVER:   "qs-view-server"
      EGERIA_USER:          "${QUICKSTART_PERSONA_USER:-peterprofile}"
      EGERIA_USER_PASSWORD: "${QUICKSTART_PERSONA_PASSWORD:-secret}"
      MY_EGERIA_HOST:       "0.0.0.0"
      MY_EGERIA_PORT:       "8021"
      MY_EGERIA_PUBLIC_URL: "${MY_EGERIA_APP_PUBLIC_URL:-http://localhost:8885/my-egeria}"
    extra_hosts:
      - "${HOST_FQDN}:${HOST_GATEWAY_IP:-host-gateway}"
      - "host.docker.internal:${HOST_GATEWAY_IP:-host-gateway}"
    depends_on:
      egeria-main:
        condition: service_healthy
```

In `egeria-quickstart-demo.yaml`, override `MY_EGERIA_PUBLIC_URL` to
`"${DEMO_SITE_URL}/my-egeria"` (HTTPS) exactly as the `my-profile` block does.

For **freshstart**, same block with host port **`7821:8021`** and **omit**
`EGERIA_USER` / `EGERIA_USER_PASSWORD` so the app's own login prompts
(Option A in `EGERIA_WORKSPACES_INTEGRATION.md`).

### 4. Add the Apache route (shared include)

In `sites-available/proxy-locations.conf` (add once — it is included by both
vhosts):

```apache
<Location "/my-egeria/">
    ProxyPreserveHost On
    ProxyPass        http://quickstart-my-egeria-app:8021/ upgrade=websocket
    ProxyPassReverse http://quickstart-my-egeria-app:8021/
    Require all granted
</Location>
```

Under option (A) also move the existing my_profile route to `/my-profile/`
(target `quickstart-my-profile:8020`). `mod_proxy_wstunnel` must be loaded
(already is, from ME-4).

### 5. Update the portal tile

In `demo-portal.html`, point the existing "My Egeria" entry at the full app's
route (option A keeps `url: '/my-egeria/'`), and — if desired — add a separate
"My Profile" tile for `/my-profile/`.

### 6. Wire into `quick-start-local`

Add the new service to the build + startup list and to the `_podman_fix_network`
container cycle, matching how `my-profile` was added in commit `577fc9b2`.

---

## Required env vars

| Variable               | Example (quickstart)                | Notes                                |
|------------------------|-------------------------------------|--------------------------------------|
| `EGERIA_PLATFORM_URL`  | `https://host.docker.internal:9443` | Egeria platform REST endpoint        |
| `EGERIA_VIEW_SERVER`   | `qs-view-server`                    | View server name                     |
| `EGERIA_USER`          | `peterprofile`                      | Active persona (quickstart only)     |
| `EGERIA_USER_PASSWORD` | `secret`                            | Password (quickstart only)           |
| `MY_EGERIA_HOST`       | `0.0.0.0`                           | Listen host (shared by all apps)     |
| `MY_EGERIA_PORT`       | `8021`                              | Listen port for the full app         |
| `MY_EGERIA_PUBLIC_URL` | `http://localhost:8885/my-egeria`   | **Required** — same-origin for CSP; demo overlay sets HTTPS |

---

## Verifying the hand-off

1. **Build check:** in the built image, `python -c "import importlib.util as u; print(u.find_spec('my_egeria.my_egeria_app'))"` must be non-None (proves the wheel shipped the app).
2. **Terminal:** `my_egeria` launches the full TUI.
3. **Local browser:** `MY_EGERIA_PORT=8021 python serve_my_egeria_app.py`, open `http://localhost:8021/`.
4. **Through the portal:** `/my-egeria/` loads and the WebSocket connects — dev-tools Network shows **`101 Switching Protocols`** on the WS request, and **no CSP errors** in the console (this is what `MY_EGERIA_PUBLIC_URL` guarantees).

If the app loads but can't reach Egeria, recheck `EGERIA_PLATFORM_URL` /
`EGERIA_VIEW_SERVER` and that the container is on `egeria_network`. If assets/WS
are blocked by CSP, `MY_EGERIA_PUBLIC_URL` is wrong or unset.

---

## Notes / gotchas

- **Do not** rely on the upstream `serve_my_egeria` console entry point in the
  proxied deployment — it omits `public_url` and needs the `textual` CLI. Use the
  local `Server(..., public_url=…)` wrapper (steps 1–2).
- Reference only the stable `my_egeria` / `serve_my_egeria` entry points or the
  `my_egeria.my_egeria_app` module — never internal `DemoCode/...` paths.
- ME-7a is still open: some personas (erinoverview, garygeeke) 401 on
  `/my-profile`; quickstart defaults to `peterprofile`. The full app may hit the
  same persona/token issue — test with peterprofile first.
- "Adding more apps" recipe: `EGERIA_WORKSPACES_INTEGRATION.md` (egeria-python:
  add `serve_<app>()` + entry point; workspaces: serve wrapper + Dockerfile +
  compose service + proxy route + portal tile + `quick-start-local`).
- Backlog items ME-8 / ME-9 cover this work; update them when it lands.
