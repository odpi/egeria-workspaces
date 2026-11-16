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


# ── TR-28: the provisioner role (owner, 2026-11-16: "Rotate on a branch") ─────────────────────────────────────────
# The old literal is spelled in two halves so that this file does not itself carry it.
OLD_PROVISIONER_PASSWORD = "provisioner" + "4egeria"
REPO = ROOT.parent


def _tracked_text_files():
    import subprocess
    out = subprocess.run(["git", "ls-files", "-z"], cwd=REPO, capture_output=True, check=True).stdout
    for name in out.decode().split("\0"):
        p = REPO / name
        if name and p.is_file() and p.suffix not in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".ico", ".woff", ".woff2"}:
            yield p


def test_no_tracked_file_carries_the_old_provisioner_password():
    import pytest
    if not (REPO / ".git").exists():
        pytest.skip("not a git checkout (e.g. a git archive copy); `git grep` the literal instead")
    hits = [str(p.relative_to(REPO)) for p in _tracked_text_files()
            if OLD_PROVISIONER_PASSWORD in p.read_text(errors="replace")]
    assert not hits, "the old provisioner password is back (use PROVISIONER_PASSWORD):\n" + "\n".join(hits)


def test_the_ods_init_script_sets_provisioner_from_the_environment():
    sql = (SHARED_INFRA / "docker-entrypoint-initdb.d" / "init_egeria_ods.sql").read_text()
    assert "\\getenv prov_password PROVISIONER_PASSWORD" in sql
    assert "ALTER ROLE provisioner WITH PASSWORD :'prov_password';" in sql
    # R1: the client-interpolated password must not reach pg_stat_statements' query-text file.
    assert sql.index("SET pg_stat_statements.track_utility = off;") < sql.index("ALTER ROLE provisioner WITH PASSWORD")
    ensure = (SHARED_INFRA / "ensure-shared-infra.sh").read_text()
    assert "-e PROVISIONER_PASSWORD egeria-shared-postgres" in ensure  # by name: the value is not on a command line


def test_the_secrets_templates_hold_the_placeholder():
    for env_name in ("egeria-quickstart", "egeria-freshstart"):
        text = (ROOT / env_name / "secrets" / "integration.omsecrets").read_text()
        assert "clearPassword: __PROVISIONER_PASSWORD__" in text, env_name


def test_airflow_takes_the_provisioner_password_from_the_environment():
    yaml = (ROOT / "optional-associated-runtimes" / "airflow-marquez" / "airflow-marquez.yaml").read_text()
    assert "postgres://provisioner:${PROVISIONER_PASSWORD:?" in yaml


def _installer():
    import importlib.util
    spec = importlib.util.spec_from_file_location("install_secrets", SHARED_INFRA / "install-secrets.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


TEMPLATE = """secretsCollections:
  PostgreSQL Server Secret:
    secrets:
      userId: surveyor
      clearPassword: keep
  PostgreSQL Provisioning Secret:
    refreshTimeInterval: 10
    secrets:
      userId: provisioner
      # Filled in from PROVISIONER_PASSWORD
      clearPassword: __PROVISIONER_PASSWORD__
  Other:
    secrets:
      clearPassword: other
"""


def test_install_fills_in_the_placeholder_in_place(tmp_path):
    inst = _installer()
    src, dst = tmp_path / "src", tmp_path / "dst"
    src.mkdir(); dst.mkdir()
    (src / "integration.omsecrets").write_text(TEMPLATE)
    (dst / "integration.omsecrets").write_text("old content that is longer than the new one " * 20)
    inode = (dst / "integration.omsecrets").stat().st_ino
    assert inst.install(src, dst, {"PROVISIONER_PASSWORD": "abc123"}) == []
    out = (dst / "integration.omsecrets").read_text()
    assert (dst / "integration.omsecrets").stat().st_ino == inode  # the bind mount keeps seeing it
    assert "clearPassword: abc123" in out and "__PROVISIONER_PASSWORD__" not in out
    assert out == TEMPLATE.replace("__PROVISIONER_PASSWORD__", "abc123")


def test_install_leaves_a_missing_value_visible(tmp_path):
    inst = _installer()
    src, dst = tmp_path / "src", tmp_path / "dst"
    src.mkdir()
    (src / "integration.omsecrets").write_text(TEMPLATE)
    assert inst.install(src, dst, {"PROVISIONER_PASSWORD": ""}) == ["PROVISIONER_PASSWORD"]
    assert "clearPassword: __PROVISIONER_PASSWORD__" in (dst / "integration.omsecrets").read_text()


def test_keep_existing_replaces_only_the_placeholder_secret(tmp_path):
    inst = _installer()
    src, dst = tmp_path / "src", tmp_path / "dst"
    src.mkdir(); dst.mkdir()
    (src / "integration.omsecrets").write_text(TEMPLATE)
    (src / "new.omsecrets").write_text("a: __PROVISIONER_PASSWORD__\n")
    existing = (TEMPLATE.replace("__PROVISIONER_PASSWORD__", "the-old-one")
                .replace("clearPassword: keep", "clearPassword: edited-by-the-user")
                .replace("clearPassword: other", "clearPassword: also-edited"))
    (dst / "integration.omsecrets").write_text(existing)
    assert inst.install(src, dst, {"PROVISIONER_PASSWORD": "rotated"}, keep_existing=True) == []
    out = (dst / "integration.omsecrets").read_text()
    assert out == existing.replace("clearPassword: the-old-one", "clearPassword: rotated")
    assert (dst / "new.omsecrets").read_text() == "a: rotated\n"  # a missing file is installed in full


def test_keep_existing_reports_a_secret_it_cannot_find(tmp_path):
    inst = _installer()
    src, dst = tmp_path / "src", tmp_path / "dst"
    src.mkdir(); dst.mkdir()
    (src / "integration.omsecrets").write_text(TEMPLATE)
    (dst / "integration.omsecrets").write_text("secretsCollections:\n  Something Else:\n    secrets: {}\n")
    problems = inst.install(src, dst, {"PROVISIONER_PASSWORD": "x"}, keep_existing=True)
    assert problems == ["PostgreSQL Provisioning Secret clearPassword (not found in the runtime file)"]


def test_env_file_values_are_unquoted_and_the_environment_wins(tmp_path):
    inst = _installer()
    env = tmp_path / ".env"
    env.write_text("A=1\nPROVISIONER_PASSWORD='from-file'\n")
    assert inst.placeholder_values(env, {}) == {"PROVISIONER_PASSWORD": "from-file"}
    assert inst.placeholder_values(env, {"PROVISIONER_PASSWORD": "from-env"}) == {"PROVISIONER_PASSWORD": "from-env"}
    assert inst.placeholder_values(tmp_path / "missing", {}) == {"PROVISIONER_PASSWORD": ""}
