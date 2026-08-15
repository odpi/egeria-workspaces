---
name: deploy-pyegeria-webhandler
description: Deploy and verify a change to PyegeriaWebHandler (quickstart's FastAPI + inline-React portal app) against the live quickstart-pyegeria-web container — syntax-check, deploy, confirm reload, curl-verify, diff-confirm. Use whenever editing .py/.html files under compose-configs/egeria-quickstart/PyegeriaWebHandler/.
---

# Deploy & verify a PyegeriaWebHandler change

Five-step recipe used dozens of times across sessions working on
`compose-configs/egeria-quickstart/PyegeriaWebHandler/`. Same steps, same
order, every time — don't skip steps under time pressure, the syntax-check
and diff-confirm steps are what catch mistakes before they reach the user.

## 0. Know the terrain first

`quickstart-pyegeria-web`'s `/app` is **bind-mounted 1:1** to this host
directory (confirmed via `docker inspect quickstart-pyegeria-web --format
'{{range .Mounts}}{{.Type}}: {{.Source}} -> {{.Destination}}{{"\n"}}{{end}}'`
— look for `bind: .../PyegeriaWebHandler -> /app`). That means:

- Editing the file on the host (Edit/Write tools) already changes what the
  container sees — there is no separate "container copy."
- `docker cp` in step 2 below is technically writing the file onto itself,
  but keep doing it anyway: it's a clean, explicit "deploy" checkpoint in
  the workflow and costs nothing since it's a no-op on a bind mount.
- **Never treat the running container as a backup.** If you need to undo an
  editing mistake, `git status`/`git diff`/git history, or the IDE's local
  history, are the only real recovery paths — the container has no
  independent copy of anything under `/app`. See project memory
  `pyegeria_webhandler_bind_mount` for how this bit a session badly once.

## 1. Syntax-check before deploying

**Python files** — quick, cheap, catches typos/indentation before they hit
a running FastAPI process:
```bash
python3 -c "import ast; ast.parse(open('<file>.py').read())" && echo SYNTAX_OK
```

**HTML files** (React apps embedded as one large inline `<script>` — these
files are 500KB-800KB+, mostly one script block per file): extract the
largest `<script>...</script>` body and run it through Node's parser:
```bash
node -e '
const fs = require("fs");
const html = fs.readFileSync("<file>.html", "utf8");
const scripts = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m => m[1]);
let biggest = "";
for (const s of scripts) if (s.length > biggest.length) biggest = s;
fs.writeFileSync("/tmp/chk.js", biggest);
'
node --check /tmp/chk.js && echo SYNTAX_OK
rm -f /tmp/chk.js
```
For `static/egeria-shared-ui.js` (plain JS, not embedded in HTML), just
`node --check static/egeria-shared-ui.js` directly.

If editing multiple files in one pass, loop this over all of them before
moving to step 2 — don't deploy anything until everything you touched is
syntax-clean.

## 2. Deploy

```bash
docker cp <file> quickstart-pyegeria-web:/app/<file>
```
Repeat per file. For `static/egeria-shared-ui.js` specifically, see step 3a
below first — it needs an extra step before this.

## 3. Confirm the app actually reloaded (Python only)

FastAPI runs under `uvicorn --reload`, which watches `/app` for changes.
After `docker cp`-ing a `.py` file, check the tail of the logs for a clean
reload with no traceback:
```bash
docker logs quickstart-pyegeria-web --tail 15
```
Look for `WatchFiles detected changes in '<file>.py'. Reloading...` followed
by `Application startup complete.` — no exception between those two lines.
(HTML/JS files are served directly, no reload step applies to them, but the
container's file cache should reflect the new content instantly given the
bind mount.)

### 3a. If you changed `static/egeria-shared-ui.js`

This file is shared by **7 consumer HTML pages** (as of this writing:
`tech-catalog.html`, `type-explorer.html`, `egeria-audit.html`,
`egeria-operations.html`, `egeria-overview.html`, `lineage-explorer.html`,
`egeria-insights.html` — grep `egeria-shared-ui.js?v=` across `*.html` to
get the current authoritative list, don't trust this comment blindly).
Each loads it with a cache-busting query string:
```html
<script src="/static/egeria-shared-ui.js?v=2026-08-14g"></script>
```
Bump the trailing letter (or date) **consistently across all 7 files** any
time the shared file's content changes, or some pages will silently keep
running stale cached JS after deploy:
```bash
sed -i '' 's/egeria-shared-ui\.js?v=2026-08-14f/egeria-shared-ui.js?v=2026-08-14g/' *.html
```
Then `docker cp` all 7 HTML files plus `static/egeria-shared-ui.js` itself.

## 4. Live-verify with curl

Hit the actual behavior you changed, not just "does the page load":
```bash
# Page loads and title/content reflects the change
curl -sk "https://localhost:8843/<route>" | grep -o "<title>[^<]*</title>"

# An API endpoint you touched returns what you expect
curl -sk "https://localhost:8843/api/<endpoint>?..." | python3 -m json.tool
```
Quickstart serves HTTPS-only on `:8843` (self-signed cert, `-k` required).
Browser automation in this sandbox is reliably blocked by the cert
interstitial — don't burn time retrying it; curl is the verification path.

## 5. Confirm the deploy actually landed

Diff the container's copy against the source file — should always be zero
lines given the bind mount, but this is the cheapest possible check that
step 2 didn't silently fail (wrong container name, `/app` typo, etc.):
```bash
diff <file> <(docker exec quickstart-pyegeria-web cat /app/<file>) | wc -l
```
Non-zero means something is wrong — stop and investigate before telling the
user the change is live.

## When something doesn't take effect

If a config or code change "isn't working" even though these steps all
passed, suspect a **stale bind-mount view** before doubting the change
itself — a known, recurring issue on this Docker Desktop/Mac setup,
independent of the PyegeriaWebHandler-specific note in step 0. See project
memory `bind_mount_cp_hazard`: symptom is the container silently serving
stale/truncated/empty content with no error at mount time; fix is always
`docker restart <container>`, confirmed on `quickstart-web-server` (Apache)
and `quickstart-egeria-main` so far.
