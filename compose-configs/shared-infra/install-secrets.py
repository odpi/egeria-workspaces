#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project.
"""Copy the Egeria secrets files into runtime-volumes, filling in the passwords that do not live in git (TR-28).

    python3 compose-configs/shared-infra/install-secrets.py [--keep-existing] <template secrets dir> <runtime secrets dir>

Each ``*.omsecrets`` file in the template directory is written to the runtime directory with every
``__NAME__`` placeholder in PLACEHOLDERS replaced by NAME's value from compose-configs/shared-infra/.env (written by
gen-env.sh) or, when set, from the environment.

- Each file is rewritten IN PLACE (truncate + write, the same inode), never removed and recreated: egeria-main
  bind-mounts the runtime directory, and a running platform must never see a file missing, or the placeholder.
- A value is never printed.  If a value is missing, the placeholder is left as it is and a warning names the
  variable: the secret then fails to sign in, visibly, rather than with an old password.
- Files in the runtime directory that are not in the template directory are left alone; the callers prune them.
- ``--keep-existing`` (freshstart, whose runtime secrets are edited in place, e.g. by the user directory): a runtime
  file that already exists keeps its content, except that each secret whose template value is a placeholder gets the
  filled-in value.  So a rotated password still reaches an existing install.  A missing file is installed in full.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

PLACEHOLDERS = ("PROVISIONER_PASSWORD",)
SHARED_INFRA_ENV = Path(__file__).resolve().parent / ".env"


def read_env_file(path: Path) -> dict[str, str]:
    """KEY=VALUE lines, with gen-env.sh's single or double quoting removed. Never sourced, so nothing runs."""
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text(errors="replace").splitlines():
        if "=" not in line or line.lstrip().startswith("#"):
            continue
        key, _, val = line.partition("=")
        val = val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "'\"":
            val = val[1:-1]
        values[key.strip()] = val
    return values


def placeholder_values(env_file: Path = SHARED_INFRA_ENV, environ=os.environ) -> dict[str, str]:
    from_file = read_env_file(env_file)
    return {name: environ.get(name) or from_file.get(name, "") for name in PLACEHOLDERS}


def render(text: str, values: dict[str, str]) -> tuple[str, list[str]]:
    """The text with each placeholder filled in, and the names of the ones left unfilled."""
    missing = []
    for name, value in values.items():
        token = f"__{name}__"
        if token not in text:
            continue
        if value:
            text = text.replace(token, value)
        else:
            missing.append(name)
    return text, missing


def write_in_place(path: Path, text: str) -> None:
    """Truncate and rewrite the same inode, so a bind mount of the directory keeps seeing this file."""
    mode = "r+" if path.exists() else "w"
    with open(path, mode) as f:
        f.seek(0)
        f.write(text)
        f.truncate()


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def _is_header(line: str) -> bool:
    """A secrets collection's name line: `  Name:` at indent 2, nothing after the colon."""
    return _indent(line) == 2 and line.rstrip().endswith(":") and not line.lstrip().startswith("#")


def placeholder_lines(template: str, names) -> list[tuple[str, str, str]]:
    """(collection header, key, template line) for each template line that holds a placeholder."""
    out, header = [], None
    for line in template.splitlines():
        if _is_header(line):
            header = line.strip()
        if header and not line.lstrip().startswith("#") and any(f"__{n}__" in line for n in names):
            out.append((header, line.strip().split(":", 1)[0], line))
    return out


def refresh_existing(runtime: str, template: str, values: dict[str, str]) -> tuple[str, list[str]]:
    """The runtime text with only the placeholder-valued secrets replaced by their filled-in template lines."""
    lines = runtime.splitlines(keepends=True)
    problems = []
    for header, key, tline in placeholder_lines(template, values):
        filled, unfilled = render(tline, values)
        if unfilled:
            problems.extend(unfilled)
            continue
        start = next((i for i, l in enumerate(lines) if _is_header(l) and l.strip() == header), None)
        done = False
        if start is not None:
            for i in range(start + 1, len(lines)):
                l = lines[i]
                if l.strip() and not l.lstrip().startswith("#") and _indent(l) <= 2:
                    break
                if _indent(l) > 2 and l.strip().split(":", 1)[0] == key and not l.lstrip().startswith("#"):
                    lines[i] = " " * _indent(l) + filled.strip() + ("\n" if l.endswith("\n") else "")
                    done = True
                    break
        if not done:
            problems.append(f"{header.rstrip(':')} {key} (not found in the runtime file)")
    return "".join(lines), problems


def install(src_dir: Path, dst_dir: Path, values: dict[str, str], keep_existing: bool = False) -> list[str]:
    """Install every template file; return the placeholder names (or secrets) that could not be filled in."""
    dst_dir.mkdir(parents=True, exist_ok=True)
    missing: set[str] = set()
    for src in sorted(src_dir.glob("*.omsecrets")):
        dst = dst_dir / src.name
        template = src.read_text()
        if keep_existing and dst.exists():
            current = dst.read_text()
            text, unfilled = refresh_existing(current, template, values)
            missing.update(unfilled)
            if text != current:
                write_in_place(dst, text)
            continue
        text, unfilled = render(template, values)
        missing.update(unfilled)
        write_in_place(dst, text)
    return sorted(missing)


def main(argv: list[str]) -> int:
    args = argv[1:]
    keep_existing = "--keep-existing" in args
    args = [a for a in args if a != "--keep-existing"]
    if len(args) != 2:
        print(__doc__.strip().splitlines()[2].strip(), file=sys.stderr)
        return 2
    missing = install(Path(args[0]), Path(args[1]), placeholder_values(), keep_existing=keep_existing)
    for name in missing:
        print(f"[install-secrets] WARNING: could not fill in {name}; that secret cannot sign in. Check "
              f"compose-configs/shared-infra/.env (run compose-configs/shared-infra/gen-env.sh), then run this again.",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
