# egeria-workspaces — Claude Code instructions

## Git commits

**All commits must be signed.** The global git config has `commit.gpgsign=true` and `gpg.format=ssh` set. Never use `--no-gpg-sign`, `--no-verify`, or any other flag that bypasses signing.

When committing, always pass the message via a heredoc. Every commit **must** include both a `Signed-off-by` trailer (DCO) and a `Co-Authored-By` trailer:
```
git commit -m "$(cat <<'EOF'
type(scope): short summary

Body here.

Signed-off-by: Dan Wolfson <dan.wolfson@pdr-associates.com>
Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
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
