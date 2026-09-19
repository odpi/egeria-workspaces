# Enable Egeria Advisor + Resource Explorer portal tiles (quickstart)

## Context

Egeria Advisor has gone multi-user (login, Postgres session store, per-user
namespaces, ownership-checked reads) since `advisor_lock_handler.py`'s
exclusive-lock/SSO handoff was originally built for a single-instance
Advisor. As part of that change, Advisor's own auth now **rejects the
Portal's current handoff token with a 400** — the token today carries
`{"egeria_user","egeria_password","iat","exp"}`; Advisor now expects
`{"sub","role","display_name","egeria_token","iat","exp"}`. This is a live
break: the Advisor tile does not currently work end-to-end.

Separately, Resource Explorer (same "trellis" family of apps, port 8810,
already fully built out in
`compose-configs/optional-associated-runtimes/trellis/`) is ready to be
exposed from the portal for the first time — it currently sits behind a
hardcoded `enabled: false, badge: 'Preview soon'` tile with no backend
handler at all.

This was coordinated directly with the trellis-side session (relayed via
Dan) and cross-checked against the actual `trellis/docker-compose.yaml` /
`.env.example` already committed in this repo — the shared-secret plumbing
(`ADVISOR_PORTAL_SECRET` → `EGERIA_ADVISOR_SSO_SECRET` on our side /
`TRELLIS_PORTAL_SECRET` on theirs) and RE's port 8810 both check out
against real files, not just the relay.

**Scope decision (confirmed with Dan):** fix only the actual break — the
handoff claim shape — and leave Advisor's exclusive-lock state machine
(`FREE`/`IN_USE`/`ADMIN_IN_USE`/`STUCK`, reservations, eviction, audit)
completely untouched in this pass. It's already effectively advisory (does
not block Advisor's own multi-user handling) and still provides real demo
UX (see who's using it, avoid piling concurrent heavy sessions onto
Advisor's LLM). **Revisit removing/relaxing the lock tomorrow**, once
multi-user behavior is confirmed working in practice, not just asserted.

**Design decision (confirmed with Dan):** `egeria_token` will be a real,
short-lived Egeria bearer token minted server-side at handoff time — not a
renamed copy of the persona password. This reuses the same pattern already
proven in `rest_api_handler.py`'s `_async_bearer_token_for_spec_fetch`
(`ValidMetadataManager(...)._async_create_egeria_bearer_token()`), so
Advisor/Resource Explorer never see a raw credential.

**Scope**: quickstart only (this integration is Coco-persona/DEMO_MODE
specific, matching how other demo-only features have been scoped in this
repo). Freshstart is not touched.

## Changes

### 1. Shared helper: `_make_portal_sso_token()` (new, in a shared module — `pyegeria_handler.py` or a new small `trellis_sso.py`)

Extract token-minting into one function both Advisor and Resource Explorer
call, so the claim shape only exists in one place:

```python
async def _make_portal_sso_token(user: User, persona_id: str, persona: dict) -> str:
    egeria_token = await _acquire_egeria_bearer_for_handoff(
        user_id=persona_id, user_pwd=persona["password"],
    )
    payload = {
        "sub": user.id if user else persona_id,
        "role": user.role if user else "guest",
        "display_name": persona.get("display_name", persona_id),
        "egeria_token": egeria_token,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(seconds=120),
    }
    return jwt.encode(payload, EGERIA_ADVISOR_SSO_SECRET, algorithm="HS256")
```

`_acquire_egeria_bearer_for_handoff(user_id, user_pwd)` mirrors
`rest_api_handler.py`'s `_async_bearer_token_for_spec_fetch` exactly
(`ValidMetadataManager(...)._async_create_egeria_bearer_token()`), sourced
from the same `_env_defaults()`-style platform URL/view-server config
already used there. On failure, raise a clear 502/503 rather than silently
falling back to a password-shaped claim Advisor will reject anyway.

Keep the 120-second expiry and `#pt=<token>` fragment format as-is per the
relay — both already match Advisor's contract.

### 2. `advisor_lock_handler.py` — fix the call site only

- Replace `_make_advisor_portal_token(body.persona, persona["password"])`
  in `acquire()` (~line 405-470) with a call to the new shared helper,
  passing the `user` (`User` DB model or `None` outside DEMO_MODE, already
  available at that call site via `_require_verified_or_local`) and
  `persona`.
- Delete the now-unused `_make_advisor_portal_token()` (lines 159-167).
- **No other change** — state machine, all other endpoints, reachability
  cache, audit log stay exactly as they are.

### 3. New `resource_explorer_handler.py` — minimal, no lock

Single endpoint, `POST /api/resource-explorer/handoff`:
- Requires a verified user in DEMO_MODE (same `_require_verified_or_local`
  pattern as Advisor), takes `{persona}` in the body.
- Looks up persona from the same `personas.json` (via the existing
  personas-loading helper Advisor/Obsidian already use — reuse, don't
  duplicate).
- Calls the shared `_make_portal_sso_token()` helper.
- Returns `{"resource_explorer_sso_url": f"{EGERIA_RESOURCE_EXPLORER_URL.rstrip('/')}/#pt=<token>"}`.
- A lightweight reachability check mirroring `_advisor_reachable`'s
  15s-TTL-cached pattern, but hitting RE's `/health/ready`.
- **No** state machine, no keepalive/release/extend/reservations/audit —
  per the relay, RE needs no lock.

### 4. Config — `.env.example` and `egeria-quickstart.yaml`

Add, next to the existing `EGERIA_ADVISOR_URL`/`EGERIA_ADVISOR_SSO_SECRET`
entries:
```
EGERIA_RESOURCE_EXPLORER_URL=http://localhost:8810/
```
Reuse `EGERIA_ADVISOR_SSO_SECRET` as the signing secret for both — the
relay confirmed trellis's compose already feeds `TRELLIS_PORTAL_SECRET`
from the same `ADVISOR_PORTAL_SECRET` value, so no new secret var is
needed on our side.

Flag explicitly to Dan (not something I can set correctly from here): both
`EGERIA_ADVISOR_URL` and `EGERIA_RESOURCE_EXPLORER_URL` currently default
to `localhost`, which only works for the operator's own browser. Each real
deployment needs its actual browser-reachable hostname in `.env`.

### 5. `demo-portal.html` — new Resource Explorer tile

- Change the existing tile object (~line 458-460) from
  `url: '/resource-explorer', newTab: false, enabled: false, badge: 'Preview soon'`
  to a boolean-flag tile (`resourceExplorer: true`, `enabled: true`),
  matching how `jupyter`/`obsidian`/`advisor` tiles work today.
- Add `refreshResourceExplorerTile()` / `_renderRETile()` /
  `acquireResourceExplorer()`, modeled on the Advisor block (~line
  845-980) but **simplified to match "no lock"**: no busy/in-use/extend/
  release states — just "not configured" / "not reachable" / a single
  launch button that POSTs to `/api/resource-explorer/handoff` and opens
  `resource_explorer_sso_url` the same way `acquireAdvisor()` opens
  `advisor_sso_url` (the synchronous `window.open('', '_blank')` popup-
  blocker dodge, then redirect once the fetch resolves).
- Advisor's tile itself needs no frontend change — the claim-shape fix is
  entirely server-side; `acquireAdvisor()`'s handling of
  `data.advisor_sso_url` is unaffected.

## Verification

1. `python3 -c "import ast; ast.parse(open(f).read())"` on every changed
   `.py` file before deploying (per the `deploy-pyegeria-webhandler` skill).
2. `docker cp` each changed file into `quickstart-pyegeria-web` (bind-mount,
   so this is a formality/checkpoint, not a real copy) and confirm a clean
   `WatchFiles ... Reloading...` / `Application startup complete.` with no
   traceback.
3. Log in as a demo user, select a Coco persona, click **Egeria Advisor**
   from the portal — confirm it lands logged into Advisor (no 400), and
   that Advisor's own UI shows the correct `display_name`/role rather than
   a generic/failed session.
4. Bring up the trellis compose stack
   (`compose-configs/optional-associated-runtimes/trellis/docker-compose.yaml`,
   alongside shared-infra) if not already running, click **Resource
   Explorer**, confirm the same clean handoff.
5. `curl -sk https://localhost:8843/api/resource-explorer/handoff` (POST,
   with a valid session cookie) directly to confirm the JSON shape and a
   real (non-password-shaped) `egeria_token` claim inside the minted JWT
   (decode it manually, don't just trust the 200).
6. Confirm the Advisor tile's existing lock/busy-state UI (Extend/Release,
   "in use by X") is visually and functionally unchanged — no regression
   from touching the same file's token-minting call site.
7. Diff-confirm every deployed file against source
   (`diff <file> <(docker exec quickstart-pyegeria-web cat /app/<file>)`)
   per the standard deploy skill.

## Explicitly deferred (revisit tomorrow)

Whether to remove/relax Advisor's exclusive lock, once multi-user behavior
is confirmed working in practice rather than just asserted by the relay.
