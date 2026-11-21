"""SHARE-3 drift guard: Portal files shared by quickstart and freshstart stay one file.

compose-configs/shared-portal-files.txt lists the PyegeriaWebHandler files whose
canonical copy is quickstart's; freshstart holds a byte-identical mirror written by
compose-configs/sync_shared_portal_files.py. These tests fail when
  - a freshstart copy has been edited (or quickstart's edited without syncing),
  - a shared file has been dropped from the manifest so it can drift again as a
    separate copy (SHARED_FLOOR below only ever grows),
  - a per-environment file (ENVIRONMENT_DIVERGENCE.md) has been listed, or
  - a copy has been replaced by a symlink (dangles in freshstart's container and image).
Fix a failure by editing quickstart's copy and running
    python3 compose-configs/sync_shared_portal_files.py
"""
import importlib.util
import re
import sys
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "compose-configs" / "sync_shared_portal_files.py"

_spec = importlib.util.spec_from_file_location("sync_shared_portal_files", SCRIPT)
sync = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sync)

# Every file ever shared. Add to this when a later SHARE-3 phase shares more; never remove.
SHARED_FLOOR = {
    "digital_products_handler.py",
    "static/egeria-shared-ui.js",
    "type_system_handler.py",
    "perspectives_handler.py",
}


def test_floor_files_are_still_listed():
    missing = SHARED_FLOOR - set(sync.shared_files())
    assert not missing, f"removed from shared-portal-files.txt, so they could drift again: {sorted(missing)}"


def test_manifest_has_no_duplicates():
    files = sync.shared_files()
    assert len(files) == len(set(files))


@pytest.mark.parametrize("rel", sorted(sync.shared_files()))
def test_shared_file_identical(rel):
    assert Path(rel).name not in sync.PER_ENV, f"{rel} is per-environment (ENVIRONMENT_DIVERGENCE.md)"
    src, dst = sync.CANONICAL / rel, sync.MIRROR / rel
    assert src.is_file() and not src.is_symlink(), f"canonical copy missing or a symlink: {src}"
    assert dst.is_file() and not dst.is_symlink(), f"freshstart copy missing or a symlink: {dst}"
    assert src.read_bytes() == dst.read_bytes(), (
        f"{rel}: freshstart's copy differs from quickstart's. Edit quickstart's copy, then run "
        f"python3 compose-configs/sync_shared_portal_files.py"
    )


@pytest.mark.parametrize("rel", sorted(sync.shared_files()))
def test_git_tracks_regular_files(rel):
    """A symlink committed in place of a copy passes on a Mac checkout but dangles in the container."""
    for env in ("egeria-quickstart", "egeria-freshstart"):
        path = f"compose-configs/{env}/PyegeriaWebHandler/{rel}"
        out = subprocess.run(["git", "ls-files", "-s", "--", path], cwd=ROOT,
                             capture_output=True, text=True)
        if out.returncode != 0 or not out.stdout.strip():
            pytest.skip("not a git checkout, or file not yet committed")
        assert not out.stdout.startswith("120000"), f"{path} is committed as a symlink"


def test_check_mode_agrees():
    assert sync.main(["--check"]) == 0


# ── Both trees really run the shared file (not a stale or shadowing copy) ──────────────────

ENVS = {
    "egeria-quickstart": ROOT / "compose-configs" / "egeria-quickstart",
    "egeria-freshstart": ROOT / "compose-configs" / "egeria-freshstart",
}
_SKIP_DIRS = {".venv", "venv", "node_modules", "__pycache__", ".pytest_cache"}


def _files_named(tree: Path, name: str) -> list:
    return [p for p in tree.rglob(name) if not (set(p.relative_to(tree).parts) & _SKIP_DIRS)]


@pytest.mark.parametrize("env", sorted(ENVS))
@pytest.mark.parametrize("rel", sorted(r for r in sync.shared_files() if r.endswith(".py")))
def test_python_module_resolves_to_the_shared_copy(env, rel):
    """The app runs from PyegeriaWebHandler/ (/app): `import <module>` must find the mirrored file
    there, and no second copy of it may exist anywhere in the tree to shadow it."""
    app = ENVS[env] / "PyegeriaWebHandler"
    mod = Path(rel).with_suffix("").as_posix().replace("/", ".")
    out = subprocess.run(
        [sys.executable, "-c", "import importlib.util,sys; sys.path.insert(0,'.'); "
         f"s=importlib.util.find_spec({mod!r}); print(s.origin if s else '')"],
        cwd=app, capture_output=True, text=True)
    assert Path(out.stdout.strip()).resolve() == (app / rel).resolve(), out.stdout + out.stderr
    others = [p for p in _files_named(app, Path(rel).name) if p.resolve() != (app / rel).resolve()]
    assert not others, f"{env}: other copies of {Path(rel).name} could be imported or served instead: {others}"


@pytest.mark.parametrize("env", sorted(ENVS))
def test_shared_js_is_what_the_pages_load(env):
    """Each env's pages load /static/egeria-shared-ui.js; the app mounts /static from
    PyegeriaWebHandler/static; that env's Apache proxies /static to its own pyegeria-web. So the
    browser gets the mirrored file, and there is exactly one file of that name in the tree."""
    app = ENVS[env] / "PyegeriaWebHandler"
    copies = _files_named(app, "egeria-shared-ui.js")
    assert copies == [app / "static" / "egeria-shared-ui.js"], copies
    assert re.search(r'_static_dir\s*=\s*SCRIPT_DIR\s*/\s*"static"', (app / "pyegeria_handler.py").read_text())
    for page in sorted(app.glob("*.html")):
        for src in re.findall(r'<script[^>]+src="([^"]*egeria-shared-ui\.js[^"]*)"', page.read_text(encoding="utf-8")):
            assert src.split("?")[0] == "/static/egeria-shared-ui.js", f"{page.name} loads {src}"
    container = "quickstart-pyegeria-web" if env == "egeria-quickstart" else "freshstart-pyegeria-web"
    apache = "\n".join(p.read_text(encoding="utf-8") for p in (ENVS[env] / "sites-available").glob("*.conf"))
    assert re.search(rf'<Location "/static">\s*ProxyPreserveHost On\s*ProxyPass http://{container}:8000/static', apache), \
        f"{env}: Apache no longer proxies /static to {container}"


_TOP_DECL = re.compile(r"^(async\s+function|function|var|const|let|class)\s+([A-Za-z0-9_$]+)", re.M)


@pytest.mark.parametrize("env", sorted(ENVS))
def test_pages_do_not_redeclare_shared_js_names_lexically(env):
    """Pages load after egeria-shared-ui.js in the same global scope. A page `const`/`let`/`class`
    with a name the shared file declares is a SyntaxError that blanks the page; node --check on
    either file alone cannot see it."""
    app = ENVS[env] / "PyegeriaWebHandler"
    shared = {m.group(2) for m in _TOP_DECL.finditer((app / "static" / "egeria-shared-ui.js").read_text(encoding="utf-8"))}
    clashes = []
    for page in sorted(app.glob("*.html")):
        text = page.read_text(encoding="utf-8")
        if "egeria-shared-ui.js" not in text:
            continue
        for m in _TOP_DECL.finditer(text):
            if m.group(2) in shared and m.group(1) in ("const", "let", "class"):
                clashes.append(f"{page.name}: {m.group(1)} {m.group(2)}")
    assert not clashes, clashes
