"""quick-start-local carries the mail settings through gen-env.sh's rewrite of .env.

The real script block (from `pushd compose-configs/egeria-quickstart` to the ssl-define.conf step) is
run in a temporary copy of the layout, with a stub gen-env.sh that rewrites .env as the real one does.
No Docker, no real .env. Values are fake and are checked never to reach stdout/stderr.
"""
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[4]
SCRIPT = REPO / "quick-start-local"
START = "pushd compose-configs/egeria-quickstart >/dev/null"
END = "  # Generate runtime ssl-define.conf"

MAIL = {
    "RESEND_API_KEY": "re_fake_key_123", "RESEND_FROM": "Egeria <noreply@example.test>",
    "SMTP_HOST": "smtp.example.test", "SMTP_PORT": "2525", "SMTP_SSL": "true", "SMTP_USER": "u@example.test",
    "SMTP_PASSWORD": "fake-smtp-pw-456", "SMTP_FROM": "infra@example.test", "INFRA_ALERT_EMAIL": "ops@example.test",
}
SECRETS = ("re_fake_key_123", "fake-smtp-pw-456")


def _block():
    text = SCRIPT.read_text()
    start, end = text.index(START), text.index(END)
    return text[start:end]


def _layout(tmp_path):
    qs = tmp_path / "compose-configs" / "egeria-quickstart"
    qs.mkdir(parents=True)
    gen = qs / "gen-env.sh"     # the real one rewrites .env from scratch every run
    gen.write_text("#!/usr/bin/env bash\nprintf 'HOST_FQDN=test.example\\nGENERATED=1\\n' > .env\n")
    gen.chmod(0o755)
    certs = tmp_path / "certs"
    certs.mkdir()
    for f in ("server.crt", "server.key", "server-ca.crt"):
        (certs / f).write_text("x")
    (qs / ".env.ssl").write_text(f"CERT_DIR={certs}\nHTTPS_PORT=8843\nSITE_URL=\n")
    return qs, certs


def _env(path, values):
    path.write_text("HOST_FQDN=old\n" + "".join(f"{k}={v}\n" for k, v in values.items()))


def _read(path):
    return dict(ln.split("=", 1) for ln in path.read_text().splitlines() if "=" in ln)


def _run(tmp_path, demo):
    bash = shutil.which("bash")
    if not bash:
        pytest.skip("bash not available")
    script = ("set -euo pipefail\nDEMO_MODE_FLAG=%d\nEGERIA_MEM_LIMIT=\nEGERIA_CPU_LIMIT=\n" % demo) + _block() + "\npopd >/dev/null\n"
    out = subprocess.run([bash, "-c", script], cwd=tmp_path, stdin=subprocess.DEVNULL, capture_output=True,
                         text=True, timeout=60, env={**os.environ, "PATH": os.environ.get("PATH", "")})
    assert out.returncode == 0, out.stderr[-2000:]
    for s in SECRETS:
        assert s not in out.stdout + out.stderr
    return out


def test_the_block_markers_are_still_there():
    """The block runs from the FIRST pushd (a later one starts the compose step) to ssl-define.conf."""
    text = SCRIPT.read_text()
    assert text.count(END) == 1 and text.index(START) < text.index(END)
    block = _block()
    assert "./gen-env.sh" in block and "_carried_mail_lines" in block and "docker" not in block.split("./gen-env.sh")[1]


def test_a_plain_run_keeps_the_mail_settings_in_env(tmp_path):
    qs, _ = _layout(tmp_path)
    _env(qs / ".env", {**MAIL, "ALERT_EMAIL_TO": "watch@example.test"})
    _run(tmp_path, demo=0)
    got = _read(qs / ".env")
    assert got["GENERATED"] == "1"                     # gen-env.sh really rewrote it
    for k, v in MAIL.items():
        assert got.get(k) == v, k
    assert got["ALERT_EMAIL_TO"] == "watch@example.test"
    assert not (qs / ".env.demo").exists()


def test_a_plain_run_adds_no_empty_keys(tmp_path):
    qs, _ = _layout(tmp_path)
    _env(qs / ".env", {})
    _run(tmp_path, demo=0)
    text = (qs / ".env").read_text()
    for k in MAIL:
        assert not re.search(rf"^{k}=", text, re.M), k


def test_a_second_plain_run_still_has_them(tmp_path):
    qs, _ = _layout(tmp_path)
    _env(qs / ".env", MAIL)
    _run(tmp_path, demo=0)
    _run(tmp_path, demo=0)
    got = _read(qs / ".env")
    assert all(got.get(k) == v for k, v in MAIL.items())
    assert all((qs / ".env").read_text().count(f"\n{k}=") == 1 for k in MAIL)


def test_demo_prefers_env_demo_and_keeps_every_mail_key_in_both_files(tmp_path):
    qs, certs = _layout(tmp_path)
    demo_vals = {"JWT_SECRET": "j", "WORKBENCH_SECRET": "w", "CERT_DIR": str(certs), "ADMIN_BOOTSTRAP_EMAIL": "a@example.test",
                 "ADMIN_BOOTSTRAP_PASSWORD": "p", "SITE_URL": "https://test.example", "HTTPS_PORT": "443",
                 "RESEND_API_KEY": MAIL["RESEND_API_KEY"], "RESEND_FROM": MAIL["RESEND_FROM"],
                 "SMTP_HOST": "demo-smtp.example.test", "SMTP_PASSWORD": MAIL["SMTP_PASSWORD"]}
    _env(qs / ".env.demo", demo_vals)
    _env(qs / ".env", {"SMTP_HOST": "env-smtp.example.test", "INFRA_ALERT_EMAIL": "ops@example.test",
                       "SMTP_PORT": "2525"})
    _run(tmp_path, demo=1)
    for name in (".env.demo", ".env"):
        got = _read(qs / name)
        assert got["SMTP_HOST"] == "demo-smtp.example.test", name       # .env.demo wins
        assert got["SMTP_PASSWORD"] == MAIL["SMTP_PASSWORD"], name
        assert got["INFRA_ALERT_EMAIL"] == "ops@example.test", name     # only in .env: carried over
        assert got["SMTP_PORT"] == "2525", name
        assert got["RESEND_API_KEY"] == MAIL["RESEND_API_KEY"], name
        assert "SMTP_USER" not in got, name                               # unset stays absent
    assert oct((qs / ".env.demo").stat().st_mode & 0o777) == "0o600"
