"""Source guard (trellis TR-12 companion): no compose file brings the old Postgres password back.

Trellis no longer has a built-in password for its shared Postgres (`egeria_advisor`): RE and EA refuse to start
without PGVECTOR_PASSWORD, by name. A compose file that writes `${PGVECTOR_PASSWORD:-advisor}`, or a hand-built URL
carrying `egeria_advisor:advisor@`, would quietly put the old password back inside the container, so after a rotation
the container would fail to connect for a reason nobody can see. Use `${PGVECTOR_PASSWORD:?...}` instead.

Scope: compose, env-example and template files under compose-configs/ (`:-advisor`, `:advisor@`,
`PGVECTOR_PASSWORD=advisor`). Since TR-27 (owner, 2026-11-16: "Replace it") the shared-infra init scripts and README
are covered too: the egeria_advisor role is created by init_trellis.sh from PGVECTOR_PASSWORD, and no init file
or README command creates or sets it with a literal password.
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


SHARED_INFRA = ROOT / "shared-infra"
LITERAL_ROLE_PASSWORD = re.compile(r"egeria_advisor\b.*\bpassword\s+'[^']+'", re.IGNORECASE)


def test_no_init_script_or_readme_gives_egeria_advisor_a_literal_password():
    files = list((SHARED_INFRA / "docker-entrypoint-initdb.d").glob("*")) + [SHARED_INFRA / "README.md"]
    hits = []
    for p in files:
        for n, line in enumerate(p.read_text(errors="replace").splitlines(), 1):
            if LITERAL_ROLE_PASSWORD.search(line):
                hits.append(f"{p.relative_to(ROOT.parent)}:{n}: {line.strip()[:120]}")
    assert not hits, "egeria_advisor is given a literal password (use PGVECTOR_PASSWORD):\n" + "\n".join(hits)


def test_the_advisor_init_script_reads_the_password_from_the_environment():
    script = (SHARED_INFRA / "docker-entrypoint-initdb.d" / "init_trellis.sh").read_text()
    assert "\\getenv adv_password PGVECTOR_PASSWORD" in script
    assert "ALTER ROLE egeria_advisor WITH PASSWORD :'adv_password'" in script
    sql = (SHARED_INFRA / "docker-entrypoint-initdb.d" / "init_egeria.sql").read_text()
    assert "egeria_advisor" not in sql.split("-- egeria_advisor (Trellis) is created by")[0]


def test_the_literal_password_guard_sees_the_old_line():
    assert LITERAL_ROLE_PASSWORD.search("create user egeria_advisor with login password 'advisor';")
    assert LITERAL_ROLE_PASSWORD.search('-c "CREATE USER egeria_advisor WITH LOGIN PASSWORD \'advisor\';"')
    assert not LITERAL_ROLE_PASSWORD.search("ALTER ROLE egeria_advisor WITH PASSWORD :'p';")
