# my-profile: pass the launching user's identity, don't hardcode it

**Status:** design only, not implemented. Written 2026-08-16 for the `my_egeria`/pyegeria
package owner to pick up — most of the actual fix lives in that package, not in this repo.

## The problem

The `my-profile` Textual TUI, served in the quickstart demo portal at `/my-egeria/`, always
runs as whatever `EGERIA_USER` is baked into the container's environment
(`compose-configs/egeria-quickstart/egeria-quickstart.yaml`, `quickstart-my-profile` service,
currently `peterprofile`). Every browser session sees peterprofile's profile, actions, and
activity — never the identity of the person actually using the portal.

This surfaced while chasing an unrelated bug (ME-7a in `BACKLOG.md`: `/my-profile` 401s for
`erinoverview`/`garygeeke`). That turned out to be a different, since-resolved issue (stale
platform state after long uptime — see `BACKLOG.md`'s ME-7a and INFRA-1 entries). But
investigating it surfaced this real, separate problem: even once the 401 is fixed, the app was
never going to show the *right* user's data, because the identity is fixed at container-launch
time, not per browser session.

## Why this doesn't just work today

`compose-configs/egeria-quickstart/serve_my_egeria.py` (this repo) is a thin wrapper:

```python
from textual_serve.server import Server
Server(
    command=f"{sys.executable} {app}",   # my_profile_app.py, one fixed command
    host=host, port=port,
    public_url=public_url,
).serve()
```

Traced into `textual_serve` (the library `my_egeria`/pyegeria depends on, version installed in
the `quickstart-my-profile` image — check `pip show textual-serve` there for the exact pin):

- `textual_serve.server.Server.__init__` takes one fixed `command` string for the life of the
  server process. There's no per-connection parameterization of it.
- `textual_serve.server.Server.handle_websocket()` (the handler that fires on every new browser
  connection) reads `width`/`height` from the WebSocket URL's query string (purely for terminal
  sizing) but nothing else from the request — no persona, no token, no cookie.
- `textual_serve.app_service.AppService._build_environment()` builds the spawned subprocess's
  environment via `dict(os.environ.copy())` plus a few `TEXTUAL_*` vars — i.e. it always
  inherits the *container's* environment, not anything request-scoped.
- `AppService._open_app_process()` spawns via `asyncio.create_subprocess_shell(self.command,
  ..., env=environment)` — the environment dict built above.

So today, no matter who opens `/my-egeria/` in a browser, the spawned `my_profile_app.py`
process always gets the same `EGERIA_USER`/`EGERIA_USER_PASSWORD` from the container's env.
There is currently no code path anywhere in this chain that varies per browser session.

## What needs to change

Two pieces, in two different repos:

### 1. This repo (`egeria-workspaces`) — pass the current user's identity to the tile URL

`compose-configs/egeria-quickstart/PyegeriaWebHandler/demo-portal.html`'s `launch(url, newTab,
toolName)` function currently does nothing but log the event and navigate — it doesn't append
any credentials to the URL (this is also true for every other tile today; nothing in this repo
currently passes credentials via query string — `BACKLOG.md`'s RE-1/RE-2 items note the *same*
gap for Resource Explorer/Egeria Advisor, so this isn't a special case, it's a first instance of
a pattern that needs building).

**Do not put a raw password in the URL.** This codebase's own convention (see
`feedback_token_auth` in project memory, and every recent bulk-action handler built this
session) is token-only, never `user_id`/`user_pwd` in a query string or anywhere logged. The
right shape: fetch (or reuse an already-cached) short-lived Egeria bearer token for the current
persona, and pass that — e.g. `/my-egeria/?token=<jwt>` — analogous to how `MY_EGERIA_PUBLIC_URL`
already routes through Apache today. The my-profile side (below) is what actually needs to
accept and use it.

### 2. `my_egeria`/pyegeria package — make textual-serve identity-aware per connection

This is the real fix, and it doesn't exist in this repo — `serve_my_egeria.py` here is a
15-line wrapper around a `Server` class the package owner controls the usage of, but the
parameterization gap is inside `textual_serve` itself (whether that's a third-party library to
subclass around, or a package `my_egeria` also owns/vendors, needs the owner to confirm).

Concretely, something needs to:

1. Read an identity/token from the incoming HTTP request when the page first loads (before the
   WebSocket upgrade) — `Server`'s existing static/HTML-serving route is the natural place,
   parallel to how it already reads `fontsize` from query params today.
2. Thread that value through to the point where the subprocess environment is built
   (`AppService._build_environment()`) so the spawned `my_profile_app.py` gets a per-connection
   `EGERIA_USER`/token instead of the container-wide default.

The cleanest version of this is a subclass — `class UserAwareServer(Server)` /
`class UserAwareAppService(AppService)` — overriding `handle_websocket` (to extract the token
from `request.query` or a cookie and pass it into the `AppService` it constructs) and
`_build_environment` (to inject it into the spawned env instead of just copying
`os.environ`). Whether that's feasible depends on how `textual_serve` is licensed/structured for
subclassing — the package owner will know that better than this repo does.

**Fallback if per-connection subprocess env isn't practical**: `my_profile_app.py` itself could
read the token from an environment variable that's normally absent, and if present, use it
instead of `EGERIA_USER`/`EGERIA_USER_PASSWORD` to construct its Egeria client connection in
`on_mount`. That still requires the env-injection plumbing above to get the token from the
HTTP request into that subprocess's environment, so it doesn't avoid the core work — it only
changes where in the app the token gets consumed.

## Open questions for the package owner

1. Is `textual_serve` a dependency `my_egeria`/pyegeria doesn't control (making a monkey-patch/
   subclass the only option), or does the team already have a fork/vendored copy where this
   could go in more directly?
2. Multi-tenancy implication: each browser connection already gets its own subprocess
   (`AppService` is instantiated per-WebSocket-connection, confirmed by reading
   `handle_websocket`), so per-connection env *should* be safe to add without touching
   concurrency/isolation — but worth the owner's explicit confirmation given they know the
   library's threading/async model better.
3. Token lifetime/refresh: `my_profile_app.py`'s `on_mount` only runs once per session at
   startup — if the Egeria token it's given expires mid-session (long-running TUI sessions are
   the norm for this kind of app), does anything already handle re-auth, or does that also need
   building?
4. Where should the identity actually come from on the query string — a full JWT, or something
   this repo's `/api/egeria-token` endpoint already issues that could be reused as-is? Worth
   confirming with whoever owns `egeria_auth.py` in this repo (`PyegeriaWebHandler`) so the two
   sides agree on one token shape.

## Where things live (for reference)

- This repo: `compose-configs/egeria-quickstart/serve_my_egeria.py`,
  `compose-configs/egeria-quickstart/Dockerfile-my-egeria`,
  `compose-configs/egeria-quickstart/egeria-quickstart.yaml` (`my-profile` service — port 8020,
  env `MY_EGERIA_PUBLIC_URL`/`EGERIA_USER`/`EGERIA_USER_PASSWORD`),
  `compose-configs/egeria-quickstart/PyegeriaWebHandler/demo-portal.html` (`launch()` — the tile
  click handler that would need to append the token).
- Installed package (inside the `quickstart-my-profile` container):
  `/usr/local/lib/python3.12/site-packages/my_egeria/my_egeria/DemoCode/My_Profile/my_profile_app.py`
  (the actual TUI app, `on_mount` calls `pyegeria.omvs.my_profile.MyProfile._async_get_my_profile`),
  `/usr/local/lib/python3.12/site-packages/pyegeria/omvs/my_profile.py` (the client class),
  `/usr/local/lib/python3.12/site-packages/textual_serve/server.py` +
  `/usr/local/lib/python3.12/site-packages/textual_serve/app_service.py` (the serving layer this
  design targets).
