#!/usr/bin/env python3
"""Keep the Egeria Portal files that quickstart and freshstart share byte-identical (SHARE-3).

The canonical copy of every file listed in ``shared-portal-files.txt`` (next to this
script) is the one under ``egeria-quickstart/PyegeriaWebHandler/``. Freshstart's copy is
a mirror: edit quickstart's, then run this script to copy it across.

    python3 compose-configs/sync_shared_portal_files.py           # copy quickstart -> freshstart
    python3 compose-configs/sync_shared_portal_files.py --check   # exit 1 if any copy differs

Why copies rather than one file: freshstart's pyegeria-web container bind-mounts
``egeria-freshstart/PyegeriaWebHandler`` at /app and its image is built from that
directory (compose, and the Helm portal image), so a symlink pointing into
egeria-quickstart would dangle inside the container and the image. See
DESIGN-SHARE-3-PHASE1.md at the repository root.

tests/test_shared_portal_files.py fails CI on any difference.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "shared-portal-files.txt"
CANONICAL = HERE / "egeria-quickstart" / "PyegeriaWebHandler"
MIRROR = HERE / "egeria-freshstart" / "PyegeriaWebHandler"

# Files that differ by environment on purpose (compose-configs/ENVIRONMENT_DIVERGENCE.md).
# Listing one in the manifest would copy quickstart's demo behaviour over freshstart's.
PER_ENV = frozenset({
    "demo_auth_handler.py", "demo_config.py", "demo_db.py",
    "demo-admin.html", "demo-login.html", "demo-portal.html", "demo-register.html",
    "demo-reset-password.html", "demo_reset_handler.py", "local-admin.html",
    "demo-profile.html", "dr_egeria_md_bdl.py", "dr_egeria_md_prev.py", "user-directory.omsecrets",
})


def shared_files() -> list[str]:
    """Manifest entries (paths relative to PyegeriaWebHandler/), comments and blanks skipped."""
    out = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            out.append(line)
    return out


def problems() -> list[str]:
    """Every reason the mirror is not an exact copy of the canonical files, in words."""
    found = []
    for rel in shared_files():
        if Path(rel).name in PER_ENV:
            found.append(f"{rel}: per-environment file (ENVIRONMENT_DIVERGENCE.md) - must not be shared")
            continue
        src, dst = CANONICAL / rel, MIRROR / rel
        if not src.is_file() or src.is_symlink():
            found.append(f"{rel}: canonical copy missing or not a regular file: {src}")
        elif not dst.is_file() or dst.is_symlink():
            found.append(f"{rel}: freshstart copy missing or not a regular file: {dst}")
        elif src.read_bytes() != dst.read_bytes():
            found.append(f"{rel}: freshstart copy differs from quickstart's")
    return found


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="report differences and exit 1; copy nothing")
    args = ap.parse_args(argv)

    if args.check:
        found = problems()
        for p in found:
            print(p)
        n = len(shared_files())
        print(f"{n - len(found)} of {n} shared files identical" if found else f"all {n} shared files identical")
        return 1 if found else 0

    copied = 0
    for rel in shared_files():
        if Path(rel).name in PER_ENV:
            print(f"refusing {rel}: per-environment file (ENVIRONMENT_DIVERGENCE.md)", file=sys.stderr)
            return 2
        src, dst = CANONICAL / rel, MIRROR / rel
        if not src.is_file():
            print(f"missing canonical file {src}", file=sys.stderr)
            return 2
        if dst.is_file() and not dst.is_symlink() and dst.read_bytes() == src.read_bytes():
            continue
        if dst.is_symlink():
            dst.unlink()
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        print(f"copied {rel}")
        copied += 1
    print(f"{copied} file(s) copied, {len(shared_files()) - copied} already identical")
    return 0


if __name__ == "__main__":
    sys.exit(main())
