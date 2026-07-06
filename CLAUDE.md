# egeria-workspaces — Claude Code instructions

## Git commits

**All commits must be signed.** The global git config has `commit.gpgsign=true` and `gpg.format=ssh` set. Never use `--no-gpg-sign`, `--no-verify`, or any other flag that bypasses signing.

When committing, always pass the message via a heredoc. Every commit **must** include both a `Signed-off-by` trailer (DCO) and a `Co-Authored-By` trailer:
```
git commit -m "$(cat <<'EOF'
type(scope): short summary

Body here.

Signed-off-by: Dan Wolfson <dan.wolfson@pdr-associates.com>./
EOF
)"
```

The `Signed-off-by` is required by the `.githooks/commit-msg` hook (active via `core.hooksPath=.githooks`) and the `commit-policy.yml` GitHub Actions workflow. Commits missing this trailer will be rejected by the hook.

Stage specific files by name rather than `git add -A` or `git add .` to avoid accidentally including runtime files (e.g. `runtime-volumes/`, `*.db`, `.env`).

## Project layout

- `compose-configs/egeria-quickstart/` — public demo environment (FastAPI + Apache)
- `compose-configs/shared-infra/` — shared Kafka, PostgreSQL (port 5442)
- `runtime-volumes/` — Docker bind-mount data, never commit contents

## Key services

| Service | Container name | Notes |
|---------|---------------|-------|
| Egeria platform | `quickstart-egeria-main` | Metadata store on `egeria` DB |
| FastAPI web | `quickstart-pyegeria-web` | Demo auth + Dr. Egeria API |
| Shared Postgres | `egeria-shared-postgres` | Port 5442, multiple schemas |

## PyegeriaWebHandler — async invariants

**Never call `create_egeria_bearer_token()` (sync) from an `async def` FastAPI route.** It calls `asyncio.get_event_loop().run_until_complete()` internally, which raises `RuntimeError: This event loop is already running` on Python 3.10+.

**Pattern for async routes — use `*_async` factories and `async_apply_token`:**

```python
# egeria_auth.py provides both:
from egeria_auth import apply_token, async_apply_token

# Sync factory — for sync (def) routes only:
def _my_client(url, server, user_id, user_pwd):
    mgr = SomeClient(...)
    apply_token(mgr)          # calls create_egeria_bearer_token() — OK in a thread
    return mgr

# Async factory — required for async routes:
async def _my_client_async(url, server, user_id, user_pwd):
    mgr = SomeClient(...)
    await async_apply_token(mgr)   # calls _async_create_egeria_bearer_token()
    return mgr

# Async route:
@router.get("/api/...")
async def my_endpoint(...):
    client = await _my_client_async(url, server, user_id, user_pwd)
    result = await client._async_some_method(...)
    ...
```

**When converting a sync route to async:** replace `asyncio.get_event_loop().run_until_complete(coro)` with `await coro` directly — no sub-loop needed.

**httpx session settings (load-bearing — do not remove):** The `AsyncClient` in pyegeria is configured with `keepalive_expiry=20 s`. This prevents dead-connection failures when a reverse proxy (nginx/Caddy idle timeout: 60–75 s) closes a socket that pyegeria still holds in the pool. Removing or raising this value will cause silent timeouts on the demo site.

**Platforms list poll interval (`egeria-operations.html`):** 30 s (`PLATFORMS_POLL_MS`). The `setInterval` in the `useEffect` for `/api/operations/platforms` keeps the left-nav server list current. The effect returns `clearInterval(timer)` for cleanup — preserve that return value.

## operations_handler.py — caching and timeout design

**Why the Integration Connectors tab uses a non-blocking cache:** Egeria's `/instance/report` endpoint polls every connector for live status and can take several minutes. Blocking the HTTP request on it always loses against Apache's 300 s `ProxyPass timeout`. Instead:

1. **Cold start** — `_get_server_report_cached` (sync, no `await`) fires a background `asyncio.Task` via `_fetch_and_cache` and returns `is_loading=True` immediately. The endpoint returns `{"connectors": [], "loading": true}`. The frontend polls every 8 s until `loading` becomes `false`.
2. **In-flight** — subsequent requests while the Task is running return `loading: true`. Exactly one Task runs per cache key (keyed on `server_guid|url|server|user_id`).
3. **Fresh hit** — returned instantly (TTL = 60 s, `_REPORT_TTL`).
4. **Stale hit** — returned instantly; a background refresh Task is spawned; `{"stale": true}` triggers an amber banner in the UI.
5. **After start/stop** — `_invalidate_server_cache(server_guid)` drops the cached entry so the next load fetches fresh state.

**`_get_server_report_cached` must stay sync (no `await`).** The check-and-create-task must be atomic within the asyncio event loop to prevent concurrent cold-start Tasks for the same key.

**`RuntimeManager` timeout** is `time_out=180` (seconds). The Egeria view server is the bottleneck; 180 s gives the background task enough headroom. Apache's `/api` proxy timeout is 300 s. When pyegeria eventually ships a lighter-weight connector-list API, swap out `_fetch_and_cache` and reduce this.

**pyegeria sync methods call `run_until_complete` internally** — never call them from an `async def` route or from `run_in_executor` (the executor thread shares the main event loop's httpx client). Use `_async_*` variants with `await` instead. This is why `_platform_server_guids` (sync) has an async twin `_platform_server_guids_async` that awaits `_async_get_platforms_by_type` directly.

**Error mapping in `_raise_http`:**
- `asyncio.TimeoutError` or pyegeria `TIMEOUT_ERROR_408` → HTTP 504
- pyegeria `401/403` auth errors → HTTP 401
- everything else → HTTP 500
