"""Source guard (PO-45, TR-12 shape): no Portal compose file gives the Portal's Egeria password a default.

The Portal (quickstart pyegeria-web and my-profile, freshstart pyegeria-web) used to get
`${QUICKSTART_PERSONA_PASSWORD:-secret}` / `${EGERIA_ADMIN_CALLER_PASSWORD:-secret}` or nothing at all, and its
handlers fell back to the well-known "secret". Now the compose files say `${VAR:?...}` (refuse to start without
it) and the handlers refuse in words (egeria_auth.service_password). This keeps a `:-secret`, or any other
password default, from coming back into the Portal's compose files.

Scope: compose-configs/egeria-quickstart, egeria-freshstart and shared-infra (*.yaml, *.yml). The optional
associated runtimes (Airflow, Dagster, MinIO samples) are third-party examples, reported in PO-45, not scanned.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "compose-configs"
DIRS = ("egeria-quickstart", "egeria-freshstart", "shared-infra")
PASSWORD_DEFAULT = re.compile(r"\$\{(?P<var>[A-Z0-9_]*(?:PASSWORD|PASS|PWD)[A-Z0-9_]*):?-(?P<default>[^}]+)\}")
SECRET_DEFAULT = re.compile(r":-secret\}")


def _files():
    for d in DIRS:
        for g in ("*.yaml", "*.yml"):
            yield from sorted((ROOT / d).glob(g))


def _hits(text: str) -> list:
    return [m.group(0) for m in PASSWORD_DEFAULT.finditer(text)] + [m.group(0) for m in SECRET_DEFAULT.finditer(text)]


def test_no_portal_compose_file_defaults_a_password():
    bad = []
    for p in _files():
        for n, line in enumerate(p.read_text(errors="replace").splitlines(), 1):
            for h in _hits(line):
                bad.append(f"{p.relative_to(ROOT.parent)}:{n}: {h}")
    assert bad == [], "a password default is back (use ${VAR:?...}):\n" + "\n".join(bad)


def test_the_portal_services_require_their_password():
    qs = (ROOT / "egeria-quickstart" / "egeria-quickstart.yaml").read_text()
    fs = (ROOT / "egeria-freshstart" / "egeria-freshstart.yaml").read_text()
    assert qs.count('EGERIA_USER_PASSWORD: "${QUICKSTART_PERSONA_PASSWORD:?') == 2      # pyegeria-web, my-profile
    assert fs.count('EGERIA_USER_PASSWORD: "${EGERIA_ADMIN_CALLER_PASSWORD:?') == 1


def test_the_guard_sees_the_shapes_it_must_refuse():
    for bad in ('EGERIA_USER_PASSWORD: "${QUICKSTART_PERSONA_PASSWORD:-secret}"', "${X_PASSWORD-hunter2}",
                "${DB_PWD:-x}", "${FOO:-secret}"):
        assert _hits(bad), bad
    for fine in ('EGERIA_USER_PASSWORD: "${QUICKSTART_PERSONA_PASSWORD:?set it}"', "${SMTP_PASSWORD:-}",
                 "EGERIA_USER: \"${QUICKSTART_PERSONA_USER:-peterprofile}\""):
        assert not _hits(fine), fine
