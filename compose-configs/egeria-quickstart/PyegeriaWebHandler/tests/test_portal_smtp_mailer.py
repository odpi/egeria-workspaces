"""The Portal's mailer: Resend, else SMTP (demo-mode.md "SMTP email"), else skipped in words.

The real callers (resend-verification, forgot-password, the welcome mail with its bcc) run against a
fake smtplib; no network. The SMTP password and the Resend key never reach the log.
"""
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402
from loguru import logger  # noqa: E402

import demo_auth_handler as h  # noqa: E402

PASSWORD = "fake-smtp-pw-7731"
API_KEY = "re_fake_key_4410"


class FakeSMTP:
    """Records what smtplib.SMTP / SMTP_SSL would have been asked to do."""
    made = []

    def __init__(self, host, port, timeout=None, context=None, ssl=False, fail_login=False):
        self.host, self.port, self.timeout, self.context, self.ssl = host, port, timeout, context, ssl
        self.starttls_ctx, self.logins, self.sent, self.quit_called = None, [], [], False
        self.fail_login = fail_login
        FakeSMTP.made.append(self)

    def starttls(self, context=None):
        self.starttls_ctx = context

    def login(self, user, pwd):
        if self.fail_login:
            raise RuntimeError(f"535 authentication failed for {user} with {pwd}")
        self.logins.append((user, pwd))

    def send_message(self, msg, to_addrs=None):
        self.sent.append((msg, list(to_addrs or [])))

    def quit(self):
        self.quit_called = True

    def close(self):
        pass


@pytest.fixture
def smtp(monkeypatch):
    FakeSMTP.made = []
    fail = {"login": False}
    monkeypatch.setattr(h.smtplib, "SMTP", lambda host, port, timeout=None: FakeSMTP(host, port, timeout,
                                                                                     fail_login=fail["login"]))
    monkeypatch.setattr(h.smtplib, "SMTP_SSL", lambda host, port, timeout=None, context=None:
                        FakeSMTP(host, port, timeout, context, ssl=True, fail_login=fail["login"]))
    monkeypatch.setattr(h, "RESEND_API_KEY", "")
    monkeypatch.setattr(h, "RESEND_FROM", "")
    for k, v in {"SMTP_HOST": "smtp.example.test", "SMTP_PORT": 587, "SMTP_SSL": False, "SMTP_USER": "sender@example.test",
                 "SMTP_PASSWORD": PASSWORD, "SMTP_FROM": "Egeria Demo <noreply@example.test>"}.items():
        monkeypatch.setattr(h, k, v)
    return SimpleNamespace(made=FakeSMTP.made, fail=fail)


@pytest.fixture
def logs():
    lines = []
    sink = logger.add(lambda m: lines.append(str(m)), level="DEBUG")
    yield lines
    logger.remove(sink)
    text = "\n".join(lines)
    assert PASSWORD not in text and API_KEY not in text


class FakeQuery:
    def __init__(self, user):
        self.user = user

    def filter(self, *a, **k):
        return self

    def first(self):
        return self.user


class FakeDB:
    def __init__(self, user):
        self.user = user

    def query(self, model):
        return FakeQuery(self.user)

    def commit(self):
        pass

    def add(self, obj):         # log_event's audit row
        pass

    def refresh(self, obj):
        pass


def _user(verified):
    return SimpleNamespace(email="erin@pdr-demo.org", display_name="Erin Overview", verified=verified, org=None,
                           verify_token=None, reset_token=None, reset_expires=None, id=1)


def _parts(msg):
    return {p.get_content_type(): p.get_content() for p in msg.iter_parts()}


def test_verification_mail_goes_by_starttls_with_login(smtp, logs):
    h.resend_verification(h.ForgotPasswordRequest(email="erin@pdr-demo.org"), db=FakeDB(_user(verified=False)))
    (conn,) = smtp.made
    assert (conn.host, conn.port, conn.ssl, conn.timeout) == ("smtp.example.test", 587, False, h.SMTP_TIMEOUT_S)
    assert conn.starttls_ctx is not None and conn.starttls_ctx.verify_mode.name == "CERT_REQUIRED"
    assert conn.logins == [("sender@example.test", PASSWORD)] and conn.quit_called
    msg, to = conn.sent[0]
    assert to == ["erin@pdr-demo.org"] and msg["To"] == "erin@pdr-demo.org"
    assert msg["From"] == "Egeria Demo <noreply@example.test>" and msg["Subject"] == "Verify your Egeria Demo account"
    parts = _parts(msg)
    assert "/api/auth/verify/" in parts["text/plain"] and "Verify Email" in parts["text/html"]
    assert any("Email sent to 'erin@pdr-demo.org' (smtp)" in ln for ln in logs)


def test_reset_mail(smtp, logs):
    h.forgot_password(h.ForgotPasswordRequest(email="erin@pdr-demo.org"), db=FakeDB(_user(verified=True)))
    msg, to = smtp.made[0].sent[0]
    assert to == ["erin@pdr-demo.org"] and msg["Subject"] == "Reset your Egeria Demo password"
    assert "/reset-password?token=" in _parts(msg)["text/plain"]


def test_welcome_bcc_is_in_the_envelope_never_a_header(smtp, logs):
    h._send_welcome_email(_user(verified=True))
    msg, to = smtp.made[0].sent[0]
    assert to == ["erin@pdr-demo.org", "info@pdr-associates.com"]
    assert msg["Bcc"] is None and "info@pdr-associates.com" not in msg.as_string()


def test_smtp_ssl_is_implicit_tls_on_465(smtp, logs, monkeypatch):
    monkeypatch.setattr(h, "SMTP_SSL", True)
    monkeypatch.setattr(h, "SMTP_PORT", 465)
    h._send_email("a@example.test", "s", "<p>x</p>", "x")
    (conn,) = smtp.made
    assert conn.ssl and conn.port == 465 and conn.starttls_ctx is None
    assert conn.context is not None and conn.context.verify_mode.name == "CERT_REQUIRED"


def test_no_login_without_a_password(smtp, logs, monkeypatch):
    monkeypatch.setattr(h, "SMTP_PASSWORD", "")
    h._send_email("a@example.test", "s", "<p>x</p>")
    conn = smtp.made[0]
    assert conn.logins == [] and len(conn.sent) == 1
    assert "HTML-capable" in _parts(conn.sent[0][0])["text/plain"]     # no text given: a plain fallback


def test_resend_wins_over_smtp(smtp, logs, monkeypatch):
    sent = []
    monkeypatch.setattr(h, "RESEND_API_KEY", API_KEY)
    monkeypatch.setattr(h, "RESEND_FROM", "Egeria <noreply@example.test>")
    monkeypatch.setattr(h._resend.Emails, "send", lambda params: sent.append(params))
    h._send_email("a@example.test", "s", "<p>x</p>", "x", bcc=["b@example.test"])
    assert smtp.made == [] and sent[0]["to"] == ["a@example.test"] and sent[0]["bcc"] == ["b@example.test"]
    assert any("(resend)" in ln for ln in logs)


def test_a_resend_key_without_a_sender_skips_and_does_not_fall_back(smtp, logs, monkeypatch):
    monkeypatch.setattr(h, "RESEND_API_KEY", API_KEY)
    h._send_email("a@example.test", "s", "<p>x</p>")
    assert smtp.made == [] and any("RESEND_FROM not set — skipped email" in ln for ln in logs)


def test_both_blank_skips_in_words(smtp, logs, monkeypatch):
    monkeypatch.setattr(h, "SMTP_HOST", "")
    h._send_email("a@example.test", "Verify", "<p>x</p>")
    assert smtp.made == []
    assert any("Email not configured (RESEND_API_KEY + RESEND_FROM, or SMTP_HOST, unset) — skipped email to "
               "'a@example.test': Verify" in ln for ln in logs)


def test_smtp_without_a_sender_skips_in_words(smtp, logs, monkeypatch):
    monkeypatch.setattr(h, "SMTP_FROM", "")
    h._send_email("a@example.test", "s", "<p>x</p>")
    assert smtp.made == [] and any("SMTP_FROM (or SMTP_USER / ADMIN_BOOTSTRAP_EMAIL) not set" in ln for ln in logs)


def test_a_failure_is_logged_with_the_password_masked_and_never_raises(smtp, logs):
    smtp.fail["login"] = True
    h._send_email("a@example.test", "s", "<p>x</p>")      # must not raise into the route
    err = [ln for ln in logs if "Failed to send email" in ln]
    assert err and "(smtp): RuntimeError: 535 authentication failed for sender@example.test with ***" in err[0]
    assert smtp.made[0].quit_called


def test_a_resend_failure_has_the_key_masked(smtp, logs, monkeypatch):
    monkeypatch.setattr(h, "RESEND_API_KEY", API_KEY)
    monkeypatch.setattr(h, "RESEND_FROM", "x@example.test")

    def boom(params):
        raise RuntimeError(f"401 bad key {API_KEY}")
    monkeypatch.setattr(h._resend.Emails, "send", boom)
    h._send_email("a@example.test", "s", "<p>x</p>")
    assert any("(resend): 401 bad key ***" in ln for ln in logs)


def test_config_defaults(monkeypatch):
    import importlib
    import demo_config
    for k in ("SMTP_HOST", "SMTP_PORT", "SMTP_SSL", "SMTP_USER", "SMTP_PASSWORD", "SMTP_FROM"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setenv("ADMIN_BOOTSTRAP_EMAIL", "admin@example.test")
    try:
        c = importlib.reload(demo_config)
        assert (c.SMTP_HOST, c.SMTP_PORT, c.SMTP_SSL) == ("", 587, False)
        assert c.SMTP_USER == "admin@example.test" and c.SMTP_FROM == "admin@example.test"
        monkeypatch.setenv("SMTP_SSL", "true")
        monkeypatch.setenv("SMTP_USER", "u@example.test")
        c = importlib.reload(demo_config)
        assert c.SMTP_PORT == 465 and c.SMTP_SSL and c.SMTP_FROM == "u@example.test"
        monkeypatch.setenv("SMTP_PORT", "25x")        # a typo falls back, never breaks import
        assert importlib.reload(demo_config).SMTP_PORT == 465
        monkeypatch.setenv("SMTP_PORT", "2525")
        monkeypatch.setenv("SMTP_FROM", "f@example.test")
        c = importlib.reload(demo_config)
        assert c.SMTP_PORT == 2525 and c.SMTP_FROM == "f@example.test"
    finally:
        for k in ("SMTP_SSL", "SMTP_USER", "SMTP_PORT", "SMTP_FROM", "ADMIN_BOOTSTRAP_EMAIL"):
            monkeypatch.delenv(k, raising=False)
        importlib.reload(demo_config)


def test_the_compose_file_passes_smtp_through_without_a_password_default():
    yaml_text = (Path(__file__).resolve().parents[1].parent / "egeria-quickstart.yaml").read_text()
    for k in ("SMTP_HOST", "SMTP_PORT", "SMTP_SSL", "SMTP_USER", "SMTP_FROM"):
        assert f'{k}: "${{{k}:-}}"' in yaml_text, k
    assert 'SMTP_PASSWORD: "${SMTP_PASSWORD:-}"' in yaml_text
