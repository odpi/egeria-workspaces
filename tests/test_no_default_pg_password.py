"""Source guard (trellis TR-12 companion): no compose file brings the old Postgres password back.

Trellis no longer has a built-in password for its shared Postgres (`egeria_advisor`): RE and EA refuse to start
without PGVECTOR_PASSWORD, by name. A compose file that writes `${PGVECTOR_PASSWORD:-advisor}`, or a hand-built URL
carrying `egeria_advisor:advisor@`, would quietly put the old password back inside the container, so after a rotation
the container would fail to connect for a reason nobody can see. Use `${PGVECTOR_PASSWORD:?...}` instead.

Scope: compose, env-example and template files under compose-configs/ (`:-advisor`, `:advisor@`,
`PGVECTOR_PASSWORD=advisor`). Deliberately NOT the shared-infra init SQL or the
README, whose role password is the owner's decision.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "compose-configs"
PATTERNS = (re.compile(r":-advisor\b"), re.compile(r":advisor@"), re.compile(r"PGVECTOR_PASSWORD\s*[=:]\s*['\"]?advisor\b"))
GLOBS = ("*.yaml", "*.yml", "*.env.example", ".env.example", "*.env.template", ".env.template", "*.env.sample",
         ".env.sample", "*.template")


def _files():
    seen = set()
    for g in GLOBS:
        for p in ROOT.rglob(g):
            if p.is_file() and p not in seen:
                seen.add(p)
                yield p


def test_no_compose_file_defaults_the_postgres_password():
    hits = []
    for p in _files():
        for n, line in enumerate(p.read_text(errors="replace").splitlines(), 1):
            if any(rx.search(line) for rx in PATTERNS):
                hits.append(f"{p.relative_to(ROOT.parent)}:{n}: {line.strip()[:120]}")
    assert not hits, ("the old default Postgres password is back (use ${PGVECTOR_PASSWORD:?...}):\n"
                      + "\n".join(hits))


def test_the_guard_sees_the_shapes_it_must_refuse():
    assert PATTERNS[0].search('PGVECTOR_PASSWORD: "${PGVECTOR_PASSWORD:-advisor}"')
    assert PATTERNS[1].search("postgresql://egeria_advisor:advisor@egeria-shared-postgres:5442/egeria_advisor")
    assert PATTERNS[2].search("PGVECTOR_PASSWORD=advisor")
    assert PATTERNS[2].search('PGVECTOR_PASSWORD: "advisor"')
    assert PATTERNS[1].search("postgresql://someone:advisor@host:5442/db")
    for fine in ('PGVECTOR_PASSWORD: "${PGVECTOR_PASSWORD:?set PGVECTOR_PASSWORD (TR-12)}"', "PGVECTOR_PASSWORD=",
                 "PGVECTOR_DBNAME: egeria_advisor"):
        assert not any(rx.search(fine) for rx in PATTERNS), fine
