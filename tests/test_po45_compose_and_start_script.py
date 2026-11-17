"""PO-45 C2 (Architect ruling, option (a)): the Portal's Egeria password at start-up.

  - `docker compose config` fails without the variable, naming it, and passes with it (quickstart, freshstart);
  - with it, pyegeria-web (and my-profile) carry the KEY EGERIA_USER_PASSWORD; the test never prints a value;
  - the start-script logic (persona-password.sh, sourced by quick-start-local's gen-env.sh): keep an existing
    value, write the demo one when missing or empty, an exported value wins and is written back;
  - freshstart's gen-env.sh carries an existing value over and never makes one up.
The compose tests are skipped where `docker compose` is not available.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
QS = ROOT / "compose-configs" / "egeria-quickstart"
FS = ROOT / "compose-configs" / "egeria-freshstart"
SENTINEL = "po45-test-value-not-a-real-password"


def _docker_compose() -> bool:
    if shutil.which("docker") is None:
        return False
    return subprocess.run(["docker", "compose", "version"], capture_output=True).returncode == 0


needs_compose = pytest.mark.skipif(not _docker_compose(), reason="docker compose is not available")


def _config(cwd: Path, compose: str, env_extra: dict, tmp_path: Path):
    env_file = tmp_path / "empty.env"
    env_file.write_text("")
    env = {k: v for k, v in os.environ.items()
           if k not in ("QUICKSTART_PERSONA_PASSWORD", "EGERIA_ADMIN_CALLER_PASSWORD")}
    env.update({"HOST_FQDN": "po45.test"}, **env_extra)
    return subprocess.run(["docker", "compose", "--env-file", str(env_file), "-f", compose, "config", "--format", "json"],
                          cwd=cwd, env=env, capture_output=True, text=True, timeout=120)


@needs_compose
@pytest.mark.parametrize("cwd,compose,var,services", [
    (QS, "egeria-quickstart.yaml", "QUICKSTART_PERSONA_PASSWORD", ("pyegeria-web", "my-profile")),
    (FS, "egeria-freshstart.yaml", "EGERIA_ADMIN_CALLER_PASSWORD", ("freshstart-pyegeria-web",)),
])
def test_compose_config_needs_the_password_and_carries_only_the_key(tmp_path, cwd, compose, var, services):
    r = _config(cwd, compose, {}, tmp_path)
    assert r.returncode != 0 and var in r.stderr and "missing a value" in r.stderr
    r = _config(cwd, compose, {var: SENTINEL}, tmp_path)
    assert r.returncode == 0, r.stderr[:500]
    cfg = json.loads(r.stdout)
    for svc in services:
        envmap = cfg["services"][svc]["environment"]
        assert "EGERIA_USER_PASSWORD" in envmap                    # the key, checked without printing a value
        assert envmap["EGERIA_USER_PASSWORD"] == SENTINEL         # it is the variable, not a built-in


# ── persona-password.sh: the quickstart start-script logic ─────────────────────────────────────────────

def _resolve(tmp_path: Path, env_lines: str | None, exported: str | None, personas_pw: str | None = "demo-pw"):
    env_file = tmp_path / ".env"
    if env_lines is not None:
        env_file.write_text(env_lines)
    personas = tmp_path / "personas.json"
    if personas_pw is not None:
        personas.write_text(json.dumps({"erinoverview": {"password": personas_pw}, "peterprofile": {"password": personas_pw}}))
    script = (f'source "{QS / "persona-password.sh"}"; '
              f'if resolve_persona_password "{env_file}" "{personas}"; then '
              'printf "%s\\n%s" "$QUICKSTART_PERSONA_PASSWORD_VAL" "$QUICKSTART_PERSONA_PASSWORD_SOURCE"; else exit 3; fi')
    env = {k: v for k, v in os.environ.items() if k != "QUICKSTART_PERSONA_PASSWORD"}
    if exported is not None:
        env["QUICKSTART_PERSONA_PASSWORD"] = exported
    r = subprocess.run(["bash", "-c", script], env=env, capture_output=True, text=True, timeout=30)
    if r.returncode:
        return None, r.stderr
    value, source = r.stdout.split("\n", 1)
    return value, source


def test_an_existing_value_is_kept(tmp_path):
    assert _resolve(tmp_path, "HOST_FQDN=x\nQUICKSTART_PERSONA_PASSWORD=kept-pw\n", None) == ("kept-pw", "kept from .env")


def test_missing_writes_the_demo_persona_password(tmp_path):
    value, source = _resolve(tmp_path, "HOST_FQDN=x\n", None)
    assert value == "demo-pw" and "personas.json" in source
    (tmp_path / "none").mkdir()
    value, _ = _resolve(tmp_path / "none", None, None)              # no .env at all
    assert value == "demo-pw"


def test_an_empty_value_counts_as_missing(tmp_path):
    value, source = _resolve(tmp_path, "QUICKSTART_PERSONA_PASSWORD=\n", None)
    assert value == "demo-pw" and "personas.json" in source


def test_an_exported_value_wins(tmp_path):
    assert _resolve(tmp_path, "QUICKSTART_PERSONA_PASSWORD=kept-pw\n", "exported-pw") == ("exported-pw", "exported")


def test_nothing_to_use_refuses_in_words(tmp_path):
    value, err = _resolve(tmp_path, "QUICKSTART_PERSONA_PASSWORD=\n", None, personas_pw=None)
    assert value is None and "no QUICKSTART_PERSONA_PASSWORD" in err


def test_gen_env_writes_it_back_never_prints_it_and_keeps_the_file_private():
    src = (QS / "gen-env.sh").read_text()
    assert 'source "${SCRIPT_DIR}/persona-password.sh"' in src
    assert "QUICKSTART_PERSONA_PASSWORD=${QUICKSTART_PERSONA_PASSWORD_VAL}" in src     # written back to .env
    assert "chmod 600 .env" in src and "umask 077" in src
    echoes = [l for l in src.splitlines() if l.strip().startswith(("echo", "printf"))]
    assert not any("PASSWORD_VAL" in l for l in echoes)                                 # never printed
    assert "(not shown)" in src


def test_freshstart_gen_env_carries_the_value_over_and_never_makes_one_up():
    src = (FS / "gen-env.sh").read_text()
    assert 'EGERIA_ADMIN_CALLER_PASSWORD_VAL="${EGERIA_ADMIN_CALLER_PASSWORD:-}"' in src
    assert "grep -E '^EGERIA_ADMIN_CALLER_PASSWORD=' .env" in src
    assert "secret" not in src.lower().replace("secrets", "")                            # no built-in value
    assert "chmod 600 .env" in src
    echoes = [l for l in src.splitlines() if l.strip().startswith("echo")]
    assert not any("PASSWORD_VAL" in l for l in echoes)
