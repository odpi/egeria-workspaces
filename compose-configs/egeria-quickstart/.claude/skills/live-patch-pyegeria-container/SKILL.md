---
name: live-patch-pyegeria-container
description: Live-test a fix or new function made in the local egeria-python (pyegeria) dev checkout against the running quickstart-pyegeria-web container, which runs the *published* PyPI pyegeria package, not the dev checkout — before it's released. Use whenever editing files under egeria-python/pyegeria/ and you need to verify the change actually works in the live quickstart demo (e.g. a new overview_metrics.py function, a bugfix in an OMVS client). Covers where to docker cp, whether a reload or a full restart is needed, and the defensive-import pattern PyegeriaWebHandler code must use to call an unreleased pyegeria function safely.
---

# Live-patching pyegeria into quickstart-pyegeria-web

`quickstart-pyegeria-web`'s `requirements.txt` pins `pyegeria>=X.Y.Z` — it
installs pyegeria from **PyPI**, a real published release. Editing
`/Users/dwolfson/localGit/egeria-python/pyegeria/...` in the dev checkout
has **zero effect** on the running container until either a new pyegeria
version is released and the image rebuilt, or you live-patch the container's
installed copy directly. This is the fast path for iterating and verifying
a fix today, not a substitute for eventually releasing it.

Confirm the install location once per session if unsure:
```bash
docker exec quickstart-pyegeria-web python3 -c "import pyegeria; print(pyegeria.__file__)"
docker exec quickstart-pyegeria-web pip show pyegeria
```
Typically `/usr/local/lib/python3.12/site-packages/pyegeria/...` — note the
Python version can differ; always confirm via the command above rather than
assuming.

## 1. Edit and validate in the dev checkout first

```bash
cd /Users/dwolfson/localGit/egeria-python
python3 -c "import ast; ast.parse(open('pyegeria/view/overview_metrics.py').read())" && echo OK
.venv/bin/pytest -m unit -q --ignore=examples --ignore=my_egeria
```
(`--ignore=examples --ignore=my_egeria`: those paths have pre-existing,
unrelated collection errors in this checkout — not something this workflow
introduces or should try to fix.)

## 2. Defensive import on the calling side (PyegeriaWebHandler)

If the change is a **new function** (not just a bugfix to existing code),
any `PyegeriaWebHandler/*.py` that calls it must import it defensively —
otherwise an older/unpatched pyegeria (e.g. after a container rebuild before
the real release ships) crashes every route in that module, not just the
one using the new function. Match the existing pattern in
`overview_handler.py` (search for `ownership_coverage`/
`count_elements_by_property` for worked examples):
```python
try:
    from pyegeria.view.overview_metrics import your_new_function
except ImportError:
    your_new_function = None
```
Then guard every call site: `if your_new_function is not None: ...`.

## 3. docker cp into site-packages (not /app)

```bash
docker cp /Users/dwolfson/localGit/egeria-python/pyegeria/view/overview_metrics.py \
  quickstart-pyegeria-web:/usr/local/lib/python3.12/site-packages/pyegeria/view/overview_metrics.py
```
One `docker cp` per changed pyegeria file. Sanity-check the import lands:
```bash
docker exec quickstart-pyegeria-web python3 -c "from pyegeria.view.overview_metrics import your_new_function; print('OK')"
```
This only proves the file parses and the name exists — it does **not** mean
the *running* server process has picked it up (see step 4).

## 4. Reload vs. restart — know which one you need

`quickstart-pyegeria-web` runs `uvicorn --reload`, which watches `/app` via
WatchFiles. Site-packages is **not** under `/app`, so patching pyegeria
alone never triggers a reload on its own:

- **If you're also deploying an app-level file change in the same pass**
  (e.g. `overview_handler.py` under `/app`, per the
  `deploy-pyegeria-webhandler` skill) — that `docker cp` triggers a reload,
  and a reload re-imports everything from scratch, including your
  site-packages patch. No separate restart needed. Confirm via:
  ```bash
  docker logs quickstart-pyegeria-web --tail 10
  # look for: WatchFiles detected changes ... Reloading... / Application startup complete.
  ```
- **If you're patching pyegeria only** (no `/app` file touched) — the
  already-running process still has the old module in memory. Explicit
  restart required:
  ```bash
  docker restart quickstart-pyegeria-web
  sleep 5
  docker logs quickstart-pyegeria-web --tail 10   # confirm clean startup, no traceback
  ```

## 5. Diff-confirm, then curl-verify the real behavior

```bash
diff /Users/dwolfson/localGit/egeria-python/pyegeria/view/overview_metrics.py \
  <(docker exec quickstart-pyegeria-web cat /usr/local/lib/python3.12/site-packages/pyegeria/view/overview_metrics.py)
# expect 0 lines
```
Then hit the actual endpoint that exercises the new code — not just an
import check:
```bash
curl -sk "https://localhost:8843/api/overview/usage-context?server=qs-view-server&user_id=erinoverview" | python3 -m json.tool
```

## When something doesn't take effect

If a patched function still isn't reflected after both a diff-confirm and a
restart, suspect a stale bind-mount view before doubting the patch itself —
see project memory `bind_mount_cp_hazard`; the fix is always another
`docker restart`.

## Don't forget the real fix

This workflow verifies a fix works *today*, live. It does not replace
actually committing the change in `egeria-python` and, eventually, cutting a
real pyegeria release — the live-patched container reverts to the published
behavior on its next real rebuild/redeploy with no memory of this session's
patch.
