"""Shared-infrastructure health (BRIEF-SHARED-INFRA-HEALTH-2026-11-12), fully offline.

(a) `egeria-upgrade-reset infra-check` and its verify lines; (b) the Portal's read-only "Shared
infrastructure" line (GET /api/admin/infra-health, static/infra-health-panel.js) and the launchd plist.

The docker answers are real-shape: tests/fixtures/shared_infra_inspect_laz_2026_11_12.json is the six
containers' `docker inspect`, read-only on laz (trimmed, no environment). A fake runner answers from it
and records every command; the check must only read. Standard library + pytest (+ node for the panel).
"""
import copy
import datetime as dt
import json
import plistlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
QS = ROOT.parent
REPO = QS.parent.parent
sys.path.insert(0, str(QS / "bin"))
sys.path.insert(0, str(ROOT))

import egeria_upgrade_reset as m  # noqa: E402

LAZ = json.loads((HERE / "fixtures" / "shared_infra_inspect_laz_2026_11_12.json").read_text())["containers"]
AIRFLOW = json.loads((HERE / "fixtures" / "airflow_marquez_inspect_laz_2026_11_12.json").read_text())["containers"]
AIRFLOW_YAML = Path("compose-configs") / "optional-associated-runtimes" / "airflow-marquez" / "airflow-marquez.yaml"
KAFKA_DIGEST = "docker.io/cleanstart/kafka@sha256:3bfad519feac67e6bd1ae2b18b3e4770cdf2fedf53ecff7b38a520a7c5d77564"
SECRET = "do-not-print-this-resend-key"


@pytest.fixture(autouse=True)
def _no_alert_settings_from_the_host(monkeypatch):
    """Alert settings come from the process environment first: never from the machine running the tests."""
    for k in m.ALERT_KEYS:
        monkeypatch.delenv(k, raising=False)


@pytest.fixture
def checkout(tmp_path):
    """A stand-in deployment checkout: the repo's real shared-infra.yaml, a .env, and an infra-health.json
    that lists nothing else (the optional runtimes have their own fixture, checkout_marquez)."""
    root = tmp_path / "checkout"
    si = root / "compose-configs" / "shared-infra"
    si.mkdir(parents=True)
    shutil.copy(REPO / m.INFRA_COMPOSE, si / "shared-infra.yaml")
    (si / "infra-health.json").write_text(json.dumps({"extraComposeFiles": [], "expectedStopped": []}))
    (si / ".env").write_text(f"SHARED_KAFKA_IMAGE={KAFKA_DIGEST}\nSHARED_POSTGRES_IMAGE=docker.io/pgvector/pgvector:pg17\n"
                             f"RESEND_API_KEY={SECRET}\n")
    return root


class InfraRunner(m.Runner):
    """Answers `docker inspect`, `docker ps` and the two reads inside Kafka; records every command."""

    def __init__(self, root: Path):
        self.calls = []
        self.containers = {k: json.loads(json.dumps(v).replace("__CHECKOUT__", str(root)))
                           for k, v in copy.deepcopy(LAZ).items()}
        self.offsets = "openlineage.events:0:902071\n"
        self.offsets_rc = 0
        self.stat = "1794487082\n"
        self.docker_down = False
        self.ps_rc = 0

    def run(self, cmd, *, input_text=None, cwd=None, check=True, timeout=None):
        self.calls.append(list(cmd))
        R = m.Result
        if self.docker_down and cmd[0] == "docker":
            return R(1, "", "Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?")
        if cmd[:2] == ["docker", "inspect"] and len(cmd) == 3:
            c = self.containers.get(cmd[2])
            return R(0, json.dumps([c])) if c else R(1, "[]", f"Error: No such object: {cmd[2]}")
        if cmd[:2] == ["docker", "inspect"]:                     # compose_setup's --format read
            return R(1, "", "Error: No such object: quickstart-egeria-main")
        if cmd[:2] == ["docker", "ps"]:
            if self.ps_rc:
                return R(self.ps_rc, "", "permission denied while trying to connect to the Docker daemon socket")
            want = {a.split("=", 1)[1].split("=", 1)[0]: a.split("=", 2)[2] for a in cmd if a.startswith("label=")}
            names = [n for n, c in self.containers.items()
                     if all(((c.get("Config") or {}).get("Labels") or {}).get(k) == v for k, v in want.items())]
            return R(0, "".join(n + "\n" for n in sorted(names)))
        if cmd[:3] == ["docker", "exec", m.INFRA_KAFKA] and "kafka-get-offsets.sh" in cmd[3]:
            return R(self.offsets_rc, self.offsets if self.offsets_rc == 0 else "",
                     "" if self.offsets_rc == 0 else "Error: timed out waiting for a node assignment")
        if cmd[:3] == ["docker", "exec", m.INFRA_KAFKA] and cmd[3:5] == ["sh", "-c"] and cmd[5].startswith("stat "):
            return R(0, self.stat)
        if "psql" in cmd:
            return R(0, "INSERT 0 1\n")
        raise AssertionError(f"unexpected command: {cmd}")


def _env(runner, root, said=None):
    return m.Env(runner=runner, http=None, ask=lambda p: "", say=(said.append if said is not None else (lambda s: None)),
                 now=lambda: 1_794_487_200.0, repo=root)


def _check(checkout, runner=None):
    runner = runner or InfraRunner(checkout)
    return m.infra_check(_env(runner, checkout), checkout), runner


def _by(result):
    return {s["service"]: s for s in result["services"]}


# ── The service list comes from the yaml ──────────────────────────────────────

EXPECTED = {"proxy": ("egeria-shared-openlineage-proxy-backend", "always"),
            "kafka": ("egeria-shared-kafka", "always"), "postgres": ("egeria-shared-postgres", "always"),
            "kroki": ("egeria-shared-kroki", "unless-stopped"), "autoheal": ("egeria-shared-autoheal", "always"),
            "kroki-mermaid": ("egeria-shared-kroki-mermaid", "unless-stopped")}


def test_services_are_read_from_the_repo_yaml():
    svcs = m.compose_services(REPO / m.INFRA_COMPOSE)
    assert {s["service"]: (s["container"], s["restart"]) for s in svcs} == EXPECTED
    assert next(s for s in svcs if s["service"] == "kafka")["image"] == "${SHARED_KAFKA_IMAGE}"


def test_the_fallback_reader_agrees_with_pyyaml():
    raw = m._mini_compose_services((REPO / m.INFRA_COMPOSE).read_text())
    assert {k: (v.get("container_name"), v.get("restart")) for k, v in raw.items()} == EXPECTED
    assert raw["kroki"]["image"] == "yuzutech/kroki:latest"


def test_a_new_service_is_covered_and_restart_defaults_to_no(tmp_path):
    f = tmp_path / "c.yaml"
    f.write_text("services:\n  extra:\n    image: x:1\n    ports:\n      - \"${EGERIA_BIND_IP:-127.0.0.1}:1:1\"\n"
                 "  named:\n    container_name: n1\n    restart: always\n")
    assert m.compose_services(f) == [{"service": "extra", "container": None, "restart": "no", "image": "x:1",
                                      "project": None},
                                     {"service": "named", "container": "n1", "restart": "always", "image": None,
                                      "project": None}]
    assert {k: v.get("restart") for k, v in m._mini_compose_services(f.read_text()).items()} == {"extra": None, "named": "always"}


# ── Verdicts on the laz shapes ────────────────────────────────────────────────

def test_today_on_laz_five_pass_and_kroki_warns(checkout):
    result, _ = _check(checkout)
    by = _by(result)
    assert {k: v["verdict"] for k, v in by.items()} == {"proxy": "PASS", "kafka": "PASS", "postgres": "PASS",
                                                        "kroki": "WARN", "autoheal": "PASS", "kroki-mermaid": "PASS"}
    assert "(missing): a recreate from the repo may change it" in by["kroki"]["words"]
    assert by["kroki"]["configFilesMatch"] is False and by["proxy"]["configFilesMatch"] is True
    assert by["kafka"]["health"] == "healthy" and by["kafka"]["imageYaml"] == KAFKA_DIGEST
    assert result["verdict"] == "WARN" and result["counts"]["FAIL"] == 0
    assert result["openlineage"]["offset"] == 902071 and result["openlineage"]["latestAt"] == m.iso(1794487082)


def test_restart_drift_is_a_fail_naming_both_policies(checkout):
    runner = InfraRunner(checkout)
    runner.containers["egeria-shared-openlineage-proxy-backend"]["HostConfig"]["RestartPolicy"]["Name"] = "no"
    result, _ = _check(checkout, runner)
    proxy = _by(result)["proxy"]
    assert proxy["verdict"] == "FAIL" and proxy["restartContainer"] == "no" and proxy["restartYaml"] == "always"
    assert ("drift: container restart=no, yaml says always (recreate it from the yaml to fix; this check never does)"
            in proxy["words"])
    assert result["verdict"] == "FAIL"


def test_an_empty_policy_name_is_compose_no(checkout):
    runner = InfraRunner(checkout)
    runner.containers["egeria-shared-kroki-mermaid"]["HostConfig"]["RestartPolicy"]["Name"] = ""
    assert _by(_check(checkout, runner)[0])["kroki-mermaid"]["restartContainer"] == "no"


def test_missing_container_fails(checkout):
    runner = InfraRunner(checkout)
    del runner.containers["egeria-shared-autoheal"]
    a = _by(_check(checkout, runner)[0])["autoheal"]
    assert a["verdict"] == "FAIL" and a["state"] == "missing" and a["words"] == "no such container"


def test_stopped_container_fails(checkout):
    runner = InfraRunner(checkout)
    st = runner.containers["egeria-shared-openlineage-proxy-backend"]["State"]
    st.update(Status="exited", Running=False, ExitCode=143)
    p = _by(_check(checkout, runner)[0])["proxy"]
    assert p["verdict"] == "FAIL" and "exited (exit code 143)" in p["words"]


def test_unhealthy_fails(checkout):
    runner = InfraRunner(checkout)
    runner.containers["egeria-shared-kafka"]["State"]["Health"]["Status"] = "unhealthy"
    k = _by(_check(checkout, runner)[0])["kafka"]
    assert k["verdict"] == "FAIL" and "running but unhealthy" in k["words"]


def test_expected_stopped_is_reported_not_failed(checkout):
    cfg = checkout / m.INFRA_CONFIG
    cfg.write_text(json.dumps({"extraComposeFiles": [], "expectedStopped": [
        {"service": "proxy", "reason": "no Airflow on this host", "by": "owner 2026-11-12"},
        {"service": "autoheal", "reason": "testing", "by": "owner"}]}))
    runner = InfraRunner(checkout)
    runner.containers["egeria-shared-openlineage-proxy-backend"]["State"].update(Status="exited", Running=False)
    del runner.containers["egeria-shared-autoheal"]
    by = _by(_check(checkout, runner)[0])
    assert by["proxy"]["verdict"] == "EXPECTED STOPPED" and "no Airflow on this host (owner 2026-11-12)" in by["proxy"]["words"]
    assert by["autoheal"]["verdict"] == "EXPECTED STOPPED" and by["autoheal"]["state"] == "missing"


def test_expected_stopped_but_running_warns(checkout):
    (checkout / m.INFRA_CONFIG).write_text(json.dumps({"expectedStopped": [{"service": "postgres", "reason": "r", "by": "b"}]}))
    p = _by(_check(checkout)[0])["postgres"]
    assert p["verdict"] == "WARN" and "listed as expected stopped" in p["words"]


def test_an_empty_config_file_means_shared_infra_only(checkout):
    (checkout / m.INFRA_CONFIG).write_text("")
    assert m.infra_config(checkout) == {"extraComposeFiles": [], "expectedStopped": {}, "prefect": None}
    (checkout / m.INFRA_CONFIG).unlink()
    assert m.infra_config(checkout) == {"extraComposeFiles": [], "expectedStopped": {}, "prefect": None}


def test_a_pinned_image_that_differs_warns(checkout):
    runner = InfraRunner(checkout)
    runner.containers["egeria-shared-kafka"]["Config"]["Image"] = "docker.io/cleanstart/kafka@sha256:" + "0" * 64
    k = _by(_check(checkout, runner)[0])["kafka"]
    assert k["verdict"] == "WARN" and "differs from the yaml's pinned" in k["words"]


def test_an_unpinned_image_is_information_only(checkout):
    runner = InfraRunner(checkout)
    runner.containers["egeria-shared-postgres"]["Config"]["Image"] = "docker.io/pgvector/pgvector:pg16"
    p = _by(_check(checkout, runner)[0])["postgres"]
    assert p["verdict"] == "PASS" and "image docker.io/pgvector/pgvector:pg16" in p["words"]


def test_openlineage_unreadable_is_not_read_and_fails_nothing(checkout):
    runner = InfraRunner(checkout)
    runner.offsets_rc = 1
    result, _ = _check(checkout, runner)
    assert result["openlineage"] == {"notRead": "offsets of openlineage.events not read: "
                                                "Error: timed out waiting for a node assignment"}
    assert result["counts"]["FAIL"] == 0 and result["verdict"] == "WARN"


def test_a_quiet_topic_is_never_an_alert(checkout):
    runner = InfraRunner(checkout)
    runner.stat = "1000000000\n"                     # 2001: years without an event
    result, _ = _check(checkout, runner)
    assert result["verdict"] == "WARN" and result["counts"]["FAIL"] == 0
    assert [c["verdict"] for c in m.infra_verify_checks(result) if "openlineage" in c["check"]] == ["INFO"]


def test_docker_unreachable_is_not_measured_not_missing(checkout):
    runner = InfraRunner(checkout)
    runner.docker_down = True
    result, _ = _check(checkout, runner)
    assert {s["verdict"] for s in result["services"]} == {"NOT MEASURED"}
    assert "Cannot connect to the Docker daemon" in result["services"][0]["words"]
    assert result["verdict"] == "NOT MEASURED" and "notRead" in result["openlineage"]


def test_missing_compose_file_is_not_measured(checkout):
    (checkout / m.INFRA_COMPOSE).unlink()
    result, _ = _check(checkout)
    assert result["verdict"] == "NOT MEASURED" and "not found" in result["services"][0]["words"]


# ── Read-only ─────────────────────────────────────────────────────────────────

MUTATING = {"up", "start", "stop", "restart", "rm", "update", "kill", "create", "run", "pause", "unpause",
            "compose", "rename", "pull", "build", "tag"}


def _assert_read_only(calls):
    for c in calls:
        if c[:2] in (["docker", "inspect"], ["docker", "ps"]):
            continue
        assert c[:3] == ["docker", "exec", m.INFRA_KAFKA], c
        assert c[3].endswith("kafka-get-offsets.sh") or (c[3:5] == ["sh", "-c"] and c[5].startswith("stat ")), c
    assert not [c for c in calls if c[0] == "docker" and len(c) > 1 and c[1] in MUTATING]


@pytest.mark.parametrize("tweak", ["none", "drift", "missing", "unhealthy", "docker_down"])
def test_the_check_only_reads(checkout, tweak):
    runner = InfraRunner(checkout)
    if tweak == "drift":
        runner.containers["egeria-shared-openlineage-proxy-backend"]["HostConfig"]["RestartPolicy"]["Name"] = "no"
    elif tweak == "missing":
        del runner.containers["egeria-shared-kroki"]
    elif tweak == "unhealthy":
        runner.containers["egeria-shared-postgres"]["State"]["Health"]["Status"] = "unhealthy"
    elif tweak == "docker_down":
        runner.docker_down = True
    _check(checkout, runner)
    assert runner.calls
    _assert_read_only(runner.calls)


def test_the_infra_section_has_no_mutating_docker_verb_in_its_source():
    src = (QS / "bin" / "egeria_upgrade_reset.py").read_text()
    section = src[src.index("# ── Shared-infrastructure health"):src.index("# ── Record (the Portal")]
    commands = re.findall(r'\["docker",\s*"([a-z]+)"', section)
    assert set(commands) == {"inspect", "ps", "exec"}, commands


def test_no_secret_from_the_env_file_is_printed(checkout):
    said = []
    runner = InfraRunner(checkout)
    assert m.main(["infra-check", "--checkout", str(checkout), "--json"], env=_env(runner, checkout, said)) == 0
    assert SECRET not in "\n".join(said)


# ── The CLI ───────────────────────────────────────────────────────────────────

def test_cli_text_and_exit_codes(checkout):
    said = []
    runner = InfraRunner(checkout)
    assert m.main(["infra-check", "--checkout", str(checkout)], env=_env(runner, checkout, said)) == 0   # WARN only
    out = "\n".join(said)
    assert re.search(r"^  WARN +kroki \(egeria-shared-kroki\): running, healthy, restart unless-stopped", out, re.M)
    assert re.search(r"^  INFO +openlineage\.events: latest event .* \(offset 902071\)$", out, re.M)
    runner.containers["egeria-shared-openlineage-proxy-backend"]["HostConfig"]["RestartPolicy"]["Name"] = "no"
    assert m.main(["infra-check", "--checkout", str(checkout)], env=_env(runner, checkout, [])) == 1
    _assert_read_only(runner.calls)


def test_record_writes_one_row_and_keeps_500(checkout):
    runner = InfraRunner(checkout)
    assert m.main(["infra-check", "--checkout", str(checkout), "--record"], env=_env(runner, checkout, [])) == 0
    sql = [c for c in runner.calls if "psql" in c][0][-1]
    assert sql.startswith(m.INFRA_DDL)
    assert "INSERT INTO demo.infra_checks (checked_at, host, compose_files, result) VALUES (" in sql
    assert "DELETE FROM demo.infra_checks WHERE id NOT IN (SELECT id FROM demo.infra_checks ORDER BY checked_at DESC, id DESC LIMIT 500)" in sql
    assert "egeria_resets" not in sql.split("INSERT", 1)[1]           # its own table only
    psql = [c for c in runner.calls if "psql" in c][0]
    assert psql[:3] == ["docker", "exec", m.PG_CONTAINER] and psql[psql.index("-d") + 1] == m.DEMO_DB


def test_record_quotes_json_with_apostrophes(checkout):
    runner = InfraRunner(checkout)
    runner.containers["egeria-shared-kroki"]["Config"]["Labels"]["com.docker.compose.project.config_files"] = "/x/o'brien.yaml"
    result = m.infra_check(_env(runner, checkout), checkout)
    m.record_infra(_env(runner, checkout), result)
    sql = [c for c in runner.calls if "psql" in c][0][-1]
    assert "o''brien.yaml" in sql and "o'brien" not in sql.replace("o''brien", "")


def test_infra_table_columns_match_initdb():
    initdb = (QS / "docker-entrypoint-initdb.d" / "init_egeria.sql").read_text()
    block = initdb[initdb.index("CREATE TABLE IF NOT EXISTS demo.infra_checks"):]
    block = block[:block.index(");")]
    assert re.findall(r"^\s+(\w+)\s", block, re.M) == re.findall(r" (\w+) (?:serial|timestamptz|text|jsonb)", m.INFRA_DDL)


# ── The verify step's lines ───────────────────────────────────────────────────

def test_verify_lines_fail_only_on_fail(checkout):
    runner = InfraRunner(checkout)
    runner.containers["egeria-shared-openlineage-proxy-backend"]["HostConfig"]["RestartPolicy"]["Name"] = "no"
    checks = m.infra_verify_checks(m.infra_check(_env(runner, checkout), checkout))
    v = {c["check"]: c["verdict"] for c in checks}
    assert v["infra proxy"] == "FAIL" and v["infra kroki"] == "WARN" and v["infra openlineage.events"] == "INFO"
    assert [c["check"] for c in checks if c["verdict"] == "FAIL"] == ["infra proxy"]


# ── (b) The Portal endpoint ───────────────────────────────────────────────────

NOW = dt.datetime(2026, 11, 12, 13, 0, tzinfo=dt.timezone.utc)


def _row(minutes_ago, result=None):
    return {"checked_at": NOW - dt.timedelta(minutes=minutes_ago), "host": "laz",
            "compose_files": ["/x/shared-infra.yaml"],
            "result": result or {"services": [{"service": "proxy", "verdict": "PASS", "words": "running"}],
                                 "counts": {"PASS": 1}}}


def _payload(reader, probe=lambda h, p: None):
    import egeria_resets_handler as h
    return h.infra_payload(reader=reader, now=NOW, probe=probe)


def test_payload_current_row():
    p = _payload(lambda: _row(5))
    assert p["state"] == "read" and p["stale"] is False and p["ageSeconds"] == 300 and p["host"] == "laz"
    assert p["result"]["services"][0]["verdict"] == "PASS"


def test_payload_stale_after_30_minutes():
    assert _payload(lambda: _row(29))["stale"] is False
    p = _payload(lambda: _row(31))
    assert p["stale"] is True and p["staleAfterSeconds"] == 1800


def test_payload_json_string_result_and_unknown_time_is_stale():
    p = _payload(lambda: {"checked_at": None, "host": "laz", "result": json.dumps({"services": []})})
    assert p["stale"] is True and p["result"] == {"services": []} and p["ageSeconds"] is None


def test_payload_never_checked():
    import egeria_resets_handler as h
    assert _payload(lambda: None)["message"] == h.NEVER_CHECKED
    def no_table():
        raise RuntimeError('(psycopg2.errors.UndefinedTable) relation "demo.infra_checks" does not exist')
    p = _payload(no_table)
    assert p["state"] == "none" and p["message"] == h.NEVER_CHECKED
    assert "egeria-upgrade-reset infra-check --record" in h.NEVER_CHECKED


def test_payload_not_read_names_the_reason():
    def boom():
        raise ConnectionError("could not connect to server: Connection refused")
    p = _payload(boom)
    assert p["state"] == "not read" and "Connection refused" in p["reason"]


def test_portal_reachability_is_its_own_labelled_fact():
    p = _payload(lambda: _row(5), probe=lambda h, port: None if port != 6000 else "ConnectionRefusedError: refused")
    r = p["reachability"]
    assert r["label"] == "reachable from the Portal now" and r["checkedAt"] == NOW.isoformat()
    assert [(x["name"], x["port"], x["reachable"]) for x in r["ports"]] == [
        ("postgres", 5442, True), ("kafka", 9192, True), ("openlineage proxy", 6000, False), ("kroki", 8000, True)]


def test_route_is_admin_only_and_get_only(monkeypatch):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    import egeria_resets_handler as h
    import report_specs_handler as rs
    app = FastAPI()
    app.include_router(h.router)
    monkeypatch.setattr(rs, "_is_admin_closed", lambda request: False)
    assert TestClient(app).get("/api/admin/infra-health").status_code == 403
    monkeypatch.setattr(rs, "_is_admin_closed", lambda request: True)
    monkeypatch.setattr(h, "_read_infra", lambda: _row(5))
    monkeypatch.setattr(h, "_probe", lambda host, port, timeout=1.0: None)
    r = TestClient(app).get("/api/admin/infra-health")
    assert r.status_code == 200 and r.json()["state"] == "read"
    assert {m_ for route in h.router.routes for m_ in route.methods} == {"GET"}


def test_the_portal_has_no_docker_access():
    src = (ROOT / "egeria_resets_handler.py").read_text()
    assert "subprocess" not in src and "docker.sock" not in src and "/var/run" not in src
    assert not re.search(r"""["']docker["']""", src) and "import docker" not in src


# ── (b) The panel ─────────────────────────────────────────────────────────────

def _render(data):
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available")
    js = ("var P = require(" + json.dumps(str(ROOT / "static" / "infra-health-panel.js")) + ");"
          "var el = {innerHTML: ''}; P.render(el, " + json.dumps(data, default=str) + "); console.log(JSON.stringify(el.innerHTML));")
    out = subprocess.run([node, "-"], input=js, capture_output=True, text=True, timeout=20)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


GREEN = ("var(--ok", "#4ade80")
REACH = {"label": "reachable from the Portal now", "checkedAt": "2026-11-12T13:00:00+00:00",
         "ports": [{"name": "postgres", "host": "egeria-shared-postgres", "port": 5442, "reachable": True, "error": None},
                   {"name": "openlineage proxy", "host": "p", "port": 6000, "reachable": False, "error": "refused"}]}
RESULT = {"services": [{"service": "proxy", "container": "egeria-shared-openlineage-proxy-backend", "verdict": "PASS",
                        "words": "running, restart always (yaml always)"},
                       {"service": "kroki", "container": "egeria-shared-kroki", "verdict": "WARN",
                        "words": "created from /tmp/x.yaml (missing): a recreate from the repo may change it"}],
          "counts": {"PASS": 1, "WARN": 1}, "openlineage": {"offset": 902071, "latestAt": "2026-11-12T12:40:03+00:00"}}


def test_panel_current_row_shows_verdicts_in_colour():
    html = _render({"state": "read", "stale": False, "checkedAt": "2026-11-12T12:55:00+00:00", "host": "laz",
                    "staleAfterSeconds": 1800, "result": RESULT, "reachability": REACH})
    assert 'data-stale="false"' in html and "Checked 2026-11-12T12:55:00+00:00" in html
    assert any(g in html for g in GREEN) and "1 pass, 1 warn" in html
    assert "(missing): a recreate from the repo may change it" in html
    assert "Info: latest OpenLineage event 2026-11-12T12:40:03+00:00 (offset 902071)" in html
    assert "reachable from the Portal now" in html and "says nothing about restart policies" in html


def test_panel_stale_row_is_grey_and_never_green():
    html = _render({"state": "read", "stale": True, "checkedAt": "2026-11-12T11:00:00+00:00", "host": "laz",
                    "staleAfterSeconds": 1800, "result": RESULT, "reachability": REACH})
    assert 'data-stale="true"' in html and "ih-stale" in html
    assert "last checked 2026-11-12T11:00:00+00:00: not current" in html
    assert not any(g in html for g in GREEN)


def test_panel_missing_stale_flag_is_not_current():
    html = _render({"state": "read", "checkedAt": None, "result": RESULT})
    assert "not current" in html and not any(g in html for g in GREEN)


def test_panel_never_checked_and_not_read():
    import egeria_resets_handler as h
    html = _render({"state": "none", "message": h.NEVER_CHECKED, "reachability": REACH})
    assert "not checked yet (run `egeria-upgrade-reset infra-check --record` on the host)" in html
    assert "Shared-infrastructure health not read: Connection refused" in _render({"state": "not read", "reason": "Connection refused"})


def test_panel_escapes():
    bad = {**RESULT, "services": [{"service": "<script>x</script>", "verdict": "FAIL", "words": "<img src=x>"}]}
    html = _render({"state": "read", "stale": False, "checkedAt": "t", "result": bad})
    assert "<script>" not in html and "<img" not in html and "&lt;script&gt;" in html


def test_panel_says_alerting_is_not_configured():
    res = {**RESULT, "alerting": {"outcome": "alerting not configured", "configured": False,
                                  "unset": ["INFRA_ALERT_EMAIL (or ALERT_EMAIL_TO)", "RESEND_API_KEY + RESEND_FROM (or SMTP_HOST)"]}}
    html = _render({"state": "read", "stale": False, "checkedAt": "t", "result": res})
    assert ("Alert email: not configured (unset: INFRA_ALERT_EMAIL (or ALERT_EMAIL_TO), "
            "RESEND_API_KEY + RESEND_FROM (or SMTP_HOST)): nothing is mailed") in html
    assert "var(--amber" in html.split("Alert email")[0].rsplit("<div", 1)[1]


def test_panel_says_alerting_is_configured_and_when_mail_last_went():
    res = {**RESULT, "alerting": {"outcome": "no change", "configured": True, "route": "resend",
                                  "lastSentAt": "2026-11-13T12:00:00+00:00"}}
    html = _render({"state": "read", "stale": False, "checkedAt": "t", "result": res})
    assert "Alert email: configured (resend) · this run: no change · last sent 2026-11-13T12:00:00+00:00" in html
    res["alerting"] = {"outcome": "change pending (1 of 2 runs)", "configured": True, "route": "smtp", "lastSentAt": None}
    assert "configured (smtp) · this run: change pending (1 of 2 runs) · last sent never" in _render(
        {"state": "read", "stale": False, "checkedAt": "t", "result": res})


def test_panel_never_leaves_alerting_blank():
    html = _render({"state": "read", "stale": False, "checkedAt": "t", "result": RESULT})   # no alerting key
    assert "Alert email: not reported by this check" in html
    off = {**RESULT, "alerting": {"outcome": "off for this run (--no-alert)", "configured": None}}
    assert "Alert email: off for this run (--no-alert)" in _render({"state": "read", "stale": False, "checkedAt": "t", "result": off})
    bad = {**RESULT, "alerting": {"outcome": "<b>x</b>", "configured": True, "route": "<i>"}}
    assert "<b>x" not in _render({"state": "read", "stale": False, "checkedAt": "t", "result": bad})


def test_pages_load_the_panel():
    for page in ("local-admin.html", "demo-admin.html"):
        html = (ROOT / page).read_text()
        assert "/static/infra-health-panel.js" in html and 'id="infraHealth"' in html
        assert "InfraHealthPanel.load('infraHealth')" in html
        assert html.index('id="egeriaResets"') < html.index('id="infraHealth"')


# ── (b) The launchd plist: in the repo, not installed by anything ─────────────

PLIST = QS / "bin" / "org.odpi.egeria.infra-check.plist"


def test_plist_runs_the_read_only_record_every_10_minutes():
    p = plistlib.loads(PLIST.read_text().replace("__REPO__", "/repo").replace("__PYTHON3__", "/opt/py/bin/python3")
                       .encode())
    assert p["Label"] == "org.odpi.egeria.infra-check" and p["StartInterval"] == 600
    assert p["ProgramArguments"][2:] == ["infra-check", "--record", "--log",
                                         "/repo/runtime-volumes/egeria-resets/infra-check.log"]
    assert p["ProgramArguments"][1] == "/repo/compose-configs/egeria-quickstart/bin/egeria-upgrade-reset"
    # an absolute, install-time interpreter: /usr/bin/env python3 found a silent framework 3.12 under launchd
    assert p["ProgramArguments"][0] == "/opt/py/bin/python3" and "/usr/bin/env" not in p["ProgramArguments"]
    # launchd's own output is discarded: the CLI's --log is the only, bounded, log
    assert p["StandardOutPath"] == "/dev/null" and p["StandardErrorPath"] == "/dev/null"
    assert "/usr/local/bin" in p["EnvironmentVariables"]["PATH"]


def test_nothing_installs_the_plist():
    hits = []
    for f in [*(REPO / "compose-configs").rglob("*"), *(REPO / "bin").rglob("*")]:
        if (not f.is_file() or f.suffix not in (".sh", ".py", ".yaml", ".yml", ".json") or ".git" in f.parts
                or "node_modules" in f.parts or "runtime-volumes" in f.parts):
            continue
        try:
            text = f.read_text(errors="ignore")
        except OSError:
            continue
        if "org.odpi.egeria.infra-check" in text and ("launchctl" in text or "LaunchAgents" in text):
            hits.append(str(f))
    assert hits == [] or all(h.endswith("test_infra_check.py") for h in hits), hits
    doc = (REPO / "portal-docs" / "Internals" / "upgrading-or-resetting-egeria.md").read_text()
    assert "Nothing installs it" in doc and "launchctl bootout" in doc


# ── The scheduled form: one bounded line per run ──────────────────────────────

def test_log_mode_prints_nothing_and_appends_one_line(checkout, tmp_path):
    said, log = [], tmp_path / "logs" / "infra-check.log"
    runner = InfraRunner(checkout)
    assert m.main(["infra-check", "--checkout", str(checkout), "--record", "--log", str(log)],
                  env=_env(runner, checkout, said)) == 0
    assert said == []
    lines = log.read_text().splitlines()
    assert len(lines) == 1
    assert re.fullmatch(r"\S+ WARN 5 pass, 1 warn \[kroki WARN\]; openlineage offset 902071 at \S+; "
                        r"alerting not configured \(unset: INFRA_ALERT_EMAIL \(or ALERT_EMAIL_TO\), RESEND_API_KEY \+ RESEND_FROM \(or SMTP_HOST\)\); recorded", lines[0])
    runner.containers["egeria-shared-openlineage-proxy-backend"]["HostConfig"]["RestartPolicy"]["Name"] = "no"
    assert m.main(["infra-check", "--checkout", str(checkout), "--log", str(log)], env=_env(runner, checkout, said)) == 1
    lines = log.read_text().splitlines()
    assert len(lines) == 2 and " FAIL " in lines[1] and "proxy FAIL" in lines[1] and "recorded" not in lines[1]
    _assert_read_only([c for c in runner.calls if "psql" not in c])


def test_log_keeps_only_the_newest_lines(tmp_path):
    log = tmp_path / "l.log"
    log.write_text("".join(f"old {i}\n" for i in range(5000)))
    m.append_bounded(log, "new\nline", keep=m.INFRA_LOG_KEEP)
    lines = log.read_text().splitlines()
    assert len(lines) == m.INFRA_LOG_KEEP == 2000
    assert lines[-1] == "new line" and lines[0] == "old 3001"
    assert not (tmp_path / "l.log.tmp").exists()


def test_log_mode_records_errors_as_a_line(checkout, tmp_path, monkeypatch):
    log = tmp_path / "e.log"
    def boom(env, checkout=None):
        raise RuntimeError("docker: command not found")
    monkeypatch.setattr(m, "infra_check", boom)
    said = []
    assert m.main(["infra-check", "--log", str(log)], env=_env(InfraRunner(checkout), checkout, said)) == 1
    assert said == [] and re.fullmatch(r"\S+ ERROR RuntimeError: docker: command not found; alerting not configured "
                                       r"\(unset: INFRA_ALERT_EMAIL \(or ALERT_EMAIL_TO\), RESEND_API_KEY \+ RESEND_FROM \(or SMTP_HOST\)\)", log.read_text().strip())


def test_log_mode_says_when_the_record_failed(checkout, tmp_path, monkeypatch):
    log = tmp_path / "r.log"
    def no_pg(env, result):
        raise m.StepFailed("docker exec egeria-shared-postgres psql exited 2")
    monkeypatch.setattr(m, "record_infra", no_pg)
    assert m.main(["infra-check", "--checkout", str(checkout), "--record", "--log", str(log)],
                  env=_env(InfraRunner(checkout), checkout, [])) == 0
    assert log.read_text().strip().endswith("; NOT recorded: StepFailed: docker exec egeria-shared-postgres psql exited 2")



def test_install_docs_choose_and_check_the_interpreter():
    doc = (REPO / "portal-docs" / "Internals" / "upgrading-or-resetting-egeria.md").read_text()
    assert 's|__PYTHON3__|$PY|g' in doc and "env -i HOME=" in doc and "infra-check --log /tmp/infra-check-probe.log" in doc
    assert "No line\n   means this `python3` does not work under launchd" in doc


# ── Optional runtimes: airflow-marquez (owner 2026-11-12: "Start marquez", and cover it) ─────────

@pytest.fixture
def checkout_marquez(checkout):
    """The checkout with the repo's real infra-health.json and the airflow-marquez compose file."""
    shutil.copy(REPO / m.INFRA_CONFIG, checkout / m.INFRA_CONFIG)
    (checkout / AIRFLOW_YAML).parent.mkdir(parents=True)
    shutil.copy(REPO / AIRFLOW_YAML, checkout / AIRFLOW_YAML)
    return checkout


def _marquez_runner(root):
    runner = InfraRunner(root)
    runner.containers.update({k: json.loads(json.dumps(v).replace("__CHECKOUT__", str(root)))
                              for k, v in copy.deepcopy(AIRFLOW).items()})
    return runner


def test_repo_config_covers_airflow_marquez():
    cfg = json.loads((REPO / m.INFRA_CONFIG).read_text())
    assert cfg["extraComposeFiles"] == [str(AIRFLOW_YAML)]
    assert [(e["service"], bool(e["reason"]), bool(e["by"]), e.get("exitCode")) for e in cfg["expectedStopped"]] \
        == [("airflow-init", True, True, 0)]


def test_marquez_restarts_unless_stopped_in_the_yaml():
    svcs = {s["service"]: s for s in m.compose_services(REPO / AIRFLOW_YAML)}
    assert svcs["marquez"]["restart"] == svcs["marquez-web"]["restart"] == "unless-stopped"
    assert {s["project"] for s in svcs.values()} == {"airflow-marquez"}
    assert all(s["container"] is None for s in svcs.values())
    raw = m._mini_compose_services((REPO / AIRFLOW_YAML).read_text())
    assert raw["marquez"]["restart"] == raw["marquez-web"]["restart"] == "unless-stopped"


def test_laz_today_with_marquez(checkout_marquez):
    """The laz containers of 2026-11-12: marquez and marquez-web were created with restart=no (FAIL drift
    until recreated from the yaml); airflow-init exited by design; the airflow-* containers were created
    from a temporary compose file (WARN)."""
    result, runner = _check(checkout_marquez, _marquez_runner(checkout_marquez))
    by = {s["service"]: s for s in result["services"]}
    assert {k: by[k]["verdict"] for k in ("redis", "marquez", "marquez-web", "airflow-init", "airflow-scheduler",
                                          "airflow-apiserver", "airflow-worker")} == {
        "redis": "PASS", "marquez": "FAIL", "marquez-web": "FAIL", "airflow-init": "EXPECTED STOPPED",
        "airflow-scheduler": "WARN", "airflow-apiserver": "WARN", "airflow-worker": "WARN"}
    assert "drift: container restart=no, yaml says unless-stopped" in by["marquez"]["words"]
    assert "one-shot setup container" in by["airflow-init"]["words"]
    assert by["marquez"]["container"] == "airflow-marquez-marquez-1"
    assert result["verdict"] == "FAIL"
    # found by project AND service label, read-only
    ps = [c for c in runner.calls if c[:2] == ["docker", "ps"]]
    assert ps and all("label=com.docker.compose.project=airflow-marquez" in c for c in ps)
    _assert_read_only(runner.calls)


def test_marquez_recreated_from_the_yaml_passes(checkout_marquez):
    runner = _marquez_runner(checkout_marquez)
    for name in ("airflow-marquez-marquez-1", "airflow-marquez-marquez-web-1"):
        runner.containers[name]["HostConfig"]["RestartPolicy"]["Name"] = "unless-stopped"
    by = {s["service"]: s for s in _check(checkout_marquez, runner)[0]["services"]}
    assert by["marquez"]["verdict"] == "PASS" and by["marquez-web"]["verdict"] == "PASS"


def test_another_projects_container_never_answers(checkout_marquez):
    runner = _marquez_runner(checkout_marquez)
    other = copy.deepcopy(runner.containers["airflow-marquez-redis-1"])
    other["Config"]["Labels"]["com.docker.compose.project"] = "some-other-project"
    other["HostConfig"]["RestartPolicy"]["Name"] = "no"
    runner.containers["some-other-project-redis-1"] = other
    by = {s["service"]: s for s in _check(checkout_marquez, runner)[0]["services"]}
    assert by["redis"]["container"] == "airflow-marquez-redis-1" and by["redis"]["verdict"] == "PASS"


def test_two_containers_for_one_service_is_not_measured(checkout_marquez):
    runner = _marquez_runner(checkout_marquez)
    runner.containers["airflow-marquez-redis-2"] = copy.deepcopy(runner.containers["airflow-marquez-redis-1"])
    r = {s["service"]: s for s in _check(checkout_marquez, runner)[0]["services"]}["redis"]
    assert r["verdict"] == "NOT MEASURED"
    assert r["words"] == ("not read: 2 containers for this service (airflow-marquez-redis-1, airflow-marquez-redis-2); "
                          "not checked")


def test_missing_marquez_container_fails(checkout_marquez):
    runner = _marquez_runner(checkout_marquez)
    del runner.containers["airflow-marquez-marquez-web-1"]
    w = {s["service"]: s for s in _check(checkout_marquez, runner)[0]["services"]}["marquez-web"]
    assert w["verdict"] == "FAIL" and w["state"] == "missing"


def test_docker_ps_error_is_not_measured_not_missing(checkout_marquez):
    runner = _marquez_runner(checkout_marquez)
    runner.ps_rc = 1
    r = {s["service"]: s for s in _check(checkout_marquez, runner)[0]["services"]}["marquez"]
    assert r["verdict"] == "NOT MEASURED" and "permission denied" in r["words"]


def test_compose_project_name():
    assert m.compose_project(REPO / AIRFLOW_YAML) == "airflow-marquez"
    assert m.compose_project(REPO / m.INFRA_COMPOSE) is None    # no name: started with -p, not guessed



# ── expectedStopped with an exit code ─────────────────────────────────────────

def test_airflow_init_exited_0_is_expected_stopped_and_says_the_code(checkout_marquez):
    by = {s["service"]: s for s in _check(checkout_marquez, _marquez_runner(checkout_marquez))[0]["services"]}
    init = by["airflow-init"]
    assert init["verdict"] == "EXPECTED STOPPED"
    assert init["words"].startswith("exited (exit code 0), as expected: a one-shot setup container")


def test_airflow_init_failed_migration_is_a_fail(checkout_marquez):
    runner = _marquez_runner(checkout_marquez)
    runner.containers["airflow-marquez-airflow-init-1"]["State"]["ExitCode"] = 1
    init = {s["service"]: s for s in _check(checkout_marquez, runner)[0]["services"]}["airflow-init"]
    assert init["verdict"] == "FAIL"
    assert init["words"].startswith("exited 1 (expected 0), state exited; listed as expected stopped (a one-shot setup")


def test_an_entry_without_an_exit_code_accepts_any_and_shows_it(checkout):
    (checkout / m.INFRA_CONFIG).write_text(json.dumps({"expectedStopped": [{"service": "proxy", "reason": "r", "by": "b"}]}))
    runner = InfraRunner(checkout)
    runner.containers["egeria-shared-openlineage-proxy-backend"]["State"].update(Status="exited", Running=False,
                                                                                 ExitCode=137)
    p = _by(_check(checkout, runner)[0])["proxy"]
    assert p["verdict"] == "EXPECTED STOPPED" and p["words"] == "exited (exit code 137), as expected: r (b)"


# ── Prefect rows (DESIGN-PREFECT-ROLE-AND-RE-WORKER-2026-11-13 §4): WARN at worst, never FAIL ──────
# tests/fixtures/prefect_pool_laz_2026_11_13.json is the Prefect API's real answers on laz (read only).

PREFECT = json.loads((HERE / "fixtures" / "prefect_pool_laz_2026_11_13.json").read_text())
ONLINE_BEAT = m._parse_iso(next(w for w in PREFECT["workers"] if w["status"] == "ONLINE")["last_heartbeat_time"])
PREFECT_CFG = {"apiUrl": "http://localhost:4200/api", "pools": ["resource-explorer-pool"]}


class PrefectHttp:
    """Answers the three Prefect reads from the laz fixture; records every request."""

    def __init__(self, workers=None, health=True, down=False, pool_code=200):
        self.calls, self.down, self.health, self.pool_code = [], down, health, pool_code
        self.workers = copy.deepcopy(PREFECT["workers"] if workers is None else workers)

    def request(self, method, url, body=None, headers=None, timeout=30):
        import urllib.error
        self.calls.append((method, url))
        if self.down:
            raise urllib.error.URLError(ConnectionRefusedError(61, "Connection refused"))
        path = url.split("/api", 1)[1]
        if path == "/health":
            return 200, self.health
        if path == "/admin/version":
            return 200, "3.8.6"
        if path == "/work_pools/resource-explorer-pool" and method == "GET":
            return (200, PREFECT["pool"]) if self.pool_code == 200 else (self.pool_code, {"detail": "not found"})
        if path == "/work_pools/resource-explorer-pool/workers/filter" and method == "POST":
            return 200, self.workers
        raise AssertionError(f"unexpected request {method} {url}")


def _prefect(http, now=ONLINE_BEAT + 20):
    env = m.Env(runner=None, http=http, ask=lambda p: "", say=lambda s: None, now=lambda: now)
    return {r["service"]: r for r in m.prefect_rows(env, PREFECT_CFG)}


def _read_only_prefect(calls):
    assert all(meth == "GET" or url.endswith("/workers/filter") for meth, url in calls), calls


def test_prefect_on_laz_today_one_live_worker_of_four():
    http = PrefectHttp()
    rows = _prefect(http)
    assert rows["Prefect server"]["verdict"] == "PASS"
    assert rows["Prefect server"]["words"] == "API healthy at http://localhost:4200/api (Prefect 3.8.6)"
    pool = rows["Prefect pool resource-explorer-pool live workers"]
    assert pool["verdict"] == "PASS"
    assert pool["words"] == "1 live worker(s) of 4 registered; last heartbeat 20 s ago; pool READY"
    _read_only_prefect(http.calls)


def test_prefect_registered_but_silent_workers_warn_with_their_age():
    """The 2026-11-13 finding: 3 registered, last heartbeat 2026-10-12, no process running."""
    workers = [w for w in PREFECT["workers"] if w["status"] == "OFFLINE"]
    pool = _prefect(PrefectHttp(workers))["Prefect pool resource-explorer-pool live workers"]
    assert pool["verdict"] == "WARN"
    # 2026-10-12T12:17:13Z to 11:32:53Z on 11-13 is 31.97 days: whole days, floored
    assert pool["words"].startswith("no live worker: 3 registered, last heartbeat 31 days ago (2026-10-12T12:17:13")


def test_prefect_status_wins_and_a_heartbeat_decides_only_without_one():
    online_old = {"status": "ONLINE", "last_heartbeat_time": "2026-01-01T00:00:00Z", "heartbeat_interval_seconds": 30}
    offline_new = {"status": "OFFLINE", "last_heartbeat_time": m.iso(ONLINE_BEAT), "heartbeat_interval_seconds": 30}
    no_status_recent = {"last_heartbeat_time": m.iso(ONLINE_BEAT - 60), "heartbeat_interval_seconds": 30}
    no_status_stale = {"last_heartbeat_time": m.iso(ONLINE_BEAT - 200), "heartbeat_interval_seconds": 30}
    never = {"last_heartbeat_time": None}
    now = ONLINE_BEAT + 20
    assert [m._worker_live(w, now) for w in (online_old, offline_new, no_status_recent, no_status_stale, never)] \
        == [True, False, True, False, False]
    pool = _prefect(PrefectHttp([offline_new, never]))["Prefect pool resource-explorer-pool live workers"]
    assert pool["verdict"] == "WARN" and pool["words"].startswith("no live worker: 2 registered, last heartbeat 20 s ago")
    assert "1 never heard from" in pool["words"]


def test_prefect_pool_with_no_workers_warns():
    pool = _prefect(PrefectHttp([]))["Prefect pool resource-explorer-pool live workers"]
    assert pool["verdict"] == "WARN" and pool["words"].startswith("no registered workers")


def test_prefect_server_unreachable_warns_and_the_pool_is_not_checked():
    http = PrefectHttp(down=True)
    rows = _prefect(http)
    assert {r["verdict"] for r in rows.values()} == {"WARN"}
    assert "not reachable: URLError" in rows["Prefect server"]["words"]
    assert "runs are not recorded in Prefect" in rows["Prefect server"]["words"]
    assert rows["Prefect pool resource-explorer-pool live workers"]["words"] == \
        "not checked: the Prefect server is not reachable"
    assert [u for _, u in http.calls] == ["http://localhost:4200/api/health"]


@pytest.mark.parametrize("http, words", [
    (PrefectHttp(health=False), "answered HTTP 200 False"),
    (PrefectHttp(pool_code=404), "no such pool on http://localhost:4200/api"),
])
def test_prefect_other_answers_warn_never_fail(http, words):
    rows = _prefect(http)
    assert "FAIL" not in {r["verdict"] for r in rows.values()}
    assert any(words in r["words"] for r in rows.values())


def test_prefect_rows_join_the_check_only_when_configured(checkout):
    http = PrefectHttp(workers=[])
    env = m.Env(runner=InfraRunner(checkout), http=http, ask=lambda p: "", say=lambda s: None,
                now=lambda: ONLINE_BEAT + 20, repo=checkout)
    assert not [s for s in m.infra_check(env, checkout)["services"] if s.get("kind") == "prefect"]
    assert http.calls == []
    (checkout / m.INFRA_CONFIG).write_text(json.dumps({"prefect": PREFECT_CFG}))
    result = m.infra_check(env, checkout)
    by = _by(result)
    assert by["Prefect pool resource-explorer-pool live workers"]["verdict"] == "WARN"
    assert result["verdict"] == "WARN" and result["counts"]["FAIL"] == 0
    assert any("Prefect pool resource-explorer-pool live workers WARN" in x for x in [m.infra_summary(result)])


def test_repo_config_checks_the_re_pool():
    assert json.loads((REPO / m.INFRA_CONFIG).read_text())["prefect"] == PREFECT_CFG


# ── Alert email on a change of state (owner 2026-11-13), through the Portal's mail settings ─────

API_KEY = "re_do-not-print-this-resend-key"
PASSWORD = "do-not-print-this-smtp-password"
RESEND = {"ALERT_EMAIL_TO": "ops@example.test", "RESEND_API_KEY": API_KEY, "RESEND_FROM": "Egeria <noreply@example.test>"}
SMTP = {"INFRA_ALERT_EMAIL": "ops@example.test", "SMTP_HOST": "smtp.example.test", "SMTP_USER": "sender@example.test",
        "SMTP_PASSWORD": PASSWORD}


class FakeMail:
    """Stands in for both senders: Resend (api_key, payload) and an smtplib-like connection."""

    def __init__(self, fail=None):
        self.resend_sent, self.smtp_sent, self.opened, self.logins, self.fail = [], [], [], [], fail

    def resend(self, api_key, payload):
        if self.fail:
            raise self.fail
        self.resend_sent.append((api_key, payload))

    def smtp(self, host, port, security):
        self.opened.append((host, port, security))
        return self

    def login(self, user, pwd):
        self.logins.append((user, pwd))

    def send_message(self, msg):
        if self.fail:
            raise self.fail
        self.smtp_sent.append(msg)

    def quit(self):
        pass


def _write_env(checkout, demo=None, main=None):
    qs = checkout / m.QS_DIR
    qs.mkdir(parents=True, exist_ok=True)
    for name, values in ((".env.demo", demo), (".env", main)):
        if values is not None:
            (qs / name).write_text("".join(f"{k}={v}\n" for k, v in values.items()) + "OTHER_SECRET=nope\n")


def _results(*states):
    """infra_check results whose rows have the given verdicts: {"kafka": "PASS", ...}."""
    for i, st in enumerate(states):
        yield {"checkedAt": f"2026-11-13T12:{i:02d}:00+00:00", "checkout": None, "verdict": "x",
               "services": [{"service": k, "verdict": v, "words": f"{k} is {v}"} for k, v in st.items()],
               "counts": {"PASS": 0, "FAIL": sum(v == "FAIL" for v in st.values())}, "openlineage": {}}


def _run(monkeypatch, checkout, tmp_path, states, mail):
    it = _results(*states)
    monkeypatch.setattr(m, "infra_check", lambda env, c=None: next(it))
    log = tmp_path / "rv" / "infra-check.log"
    env = m.Env(runner=None, http=None, ask=lambda p: "", say=lambda s: None, now=lambda: 1_794_487_200.0,
                repo=checkout, smtp=mail.smtp, resend=mail.resend)
    for _ in states:
        m.infra_check_logged(env, log, record=False, checkout=checkout)
    return log.read_text().splitlines(), log.with_name("infra-check-alert-state.json")


def test_alerts_only_on_changes_and_on_recovery_through_resend(monkeypatch, checkout, tmp_path):
    _write_env(checkout, demo=RESEND)
    mail = FakeMail()
    lines, state = _run(monkeypatch, checkout, tmp_path, [
        {"kafka": "PASS", "pool": "PASS"},                    # fine from the start: nothing to say
        {"kafka": "PASS", "pool": "WARN"},                    # into WARN: pending
        {"kafka": "PASS", "pool": "WARN"},                    # held twice: email
        {"kafka": "PASS", "pool": "WARN"},                    # same: nothing, however many runs
        {"kafka": "FAIL", "pool": "WARN"},                    # a second row goes bad: pending
        {"kafka": "FAIL", "pool": "WARN"},                    # held: email
        {"kafka": "PASS", "pool": "PASS", "x": "EXPECTED STOPPED"},  # recovery: pending
        {"kafka": "PASS", "pool": "PASS"},                    # held: one recovery email
    ], mail)
    assert [ln.rsplit("; ", 1)[1] for ln in lines] == [
        "no change", "change pending (1 of 2 runs)", "alert sent (resend)", "no change",
        "change pending (1 of 2 runs)", "alert sent (resend)", "change pending (1 of 2 runs)", "recovery sent (resend)"]
    assert mail.smtp_sent == [] and {k for k, _ in mail.resend_sent} == {API_KEY}
    payloads = [p for _, p in mail.resend_sent]
    assert {p["from"] for p in payloads} == {"Egeria <noreply@example.test>"}
    assert {tuple(p["to"]) for p in payloads} == {("ops@example.test",)}
    assert payloads[0]["subject"].endswith("] WARN: pool") and payloads[1]["subject"].endswith("] FAIL: kafka, pool")
    assert "recovered: everything PASS" in payloads[2]["subject"]
    assert "NOW FAIL: kafka: kafka is FAIL" in payloads[1]["text"] and "still WARN: pool" in payloads[1]["text"]
    assert "recovered (was WARN): pool" in payloads[2]["text"]
    assert json.loads(state.read_text())["degraded"] == {} and state.parent == tmp_path / "rv"
    everything = "\n".join(lines) + json.dumps(payloads) + state.read_text()
    assert API_KEY not in everything and "OTHER_SECRET" not in everything and "nope" not in everything


def test_resend_wins_over_smtp_as_in_the_portal(monkeypatch, checkout, tmp_path):
    _write_env(checkout, demo={**SMTP, **RESEND})
    mail = FakeMail()
    lines, _ = _run(monkeypatch, checkout, tmp_path, [{"kafka": "FAIL"}] * 2, mail)
    assert lines[-1].endswith("; alert sent (resend)") and mail.opened == [] and len(mail.resend_sent) == 1


def test_a_resend_key_without_a_sender_is_not_configured_and_does_not_fall_back(monkeypatch, checkout, tmp_path):
    """The Portal skips when RESEND_API_KEY is set without RESEND_FROM; it does not try SMTP."""
    _write_env(checkout, demo={**SMTP, "RESEND_API_KEY": API_KEY})
    mail = FakeMail()
    lines, _ = _run(monkeypatch, checkout, tmp_path, [{"kafka": "FAIL"}], mail)
    assert lines[-1].endswith("; alerting not configured (unset: RESEND_FROM)")
    assert mail.opened == [] and mail.resend_sent == []


def test_smtp_when_resend_is_unset(monkeypatch, checkout, tmp_path):
    _write_env(checkout, demo=SMTP)
    mail = FakeMail()
    lines, _ = _run(monkeypatch, checkout, tmp_path, [{"kafka": "WARN"}] * 2, mail)
    assert lines[-1].endswith("; alert sent (smtp)")
    assert mail.opened == [("smtp.example.test", 587, "starttls")]
    assert mail.logins == [("sender@example.test", PASSWORD)]
    msg = mail.smtp_sent[0]
    assert msg["From"] == "sender@example.test" and msg["To"] == "ops@example.test"
    assert PASSWORD not in msg.as_string() + "\n".join(lines)


def test_smtp_ssl_and_the_documented_user_fallback(monkeypatch, checkout, tmp_path):
    _write_env(checkout, demo={"ALERT_EMAIL_TO": "a@example.test, b@example.test", "SMTP_HOST": "smtp.example.test",
                               "SMTP_SSL": "true", "SMTP_PASSWORD": PASSWORD, "SMTP_FROM": "infra@example.test",
                               "ADMIN_BOOTSTRAP_EMAIL": "admin@example.test"})
    mail = FakeMail()
    _run(monkeypatch, checkout, tmp_path, [{"kafka": "WARN"}] * 2, mail)
    assert mail.opened == [("smtp.example.test", 465, "ssl")]
    assert mail.logins == [("admin@example.test", PASSWORD)]
    assert mail.smtp_sent[0]["From"] == "infra@example.test"
    assert mail.smtp_sent[0]["To"] == "a@example.test, b@example.test"


def test_where_settings_come_from(monkeypatch, checkout):
    """Process environment, else .env.demo (where quick-start-local keeps secrets), else .env; only the
    named keys are read."""
    _write_env(checkout, demo={"RESEND_FROM": "demo@example.test"},
               main={"RESEND_FROM": "main@example.test", "RESEND_API_KEY": API_KEY, "ALERT_EMAIL_TO": "to@example.test"})
    got = m.alert_settings(checkout)
    assert got["RESEND_FROM"] == "demo@example.test" and got["RESEND_API_KEY"] == API_KEY
    assert set(got) == set(m.ALERT_KEYS) and "OTHER_SECRET" not in got
    monkeypatch.setenv("RESEND_FROM", "env@example.test")
    monkeypatch.setenv("INFRA_ALERT_EMAIL", "infra@example.test")
    got = m.alert_settings(checkout)
    assert got["RESEND_FROM"] == "env@example.test"
    assert m.mail_route(got) == ("resend", "infra@example.test", [])     # INFRA_ALERT_EMAIL over ALERT_EMAIL_TO


def test_not_configured_says_so_every_run_and_sends_nothing(monkeypatch, checkout, tmp_path):
    _write_env(checkout, demo={"RESEND_API_KEY": API_KEY, "RESEND_FROM": "x@example.test"})   # no recipient
    mail = FakeMail()
    lines, state = _run(monkeypatch, checkout, tmp_path, [{"kafka": "PASS"}, {"kafka": "FAIL"}, {"kafka": "FAIL"}], mail)
    assert all(ln.endswith("; alerting not configured (unset: INFRA_ALERT_EMAIL (or ALERT_EMAIL_TO))") for ln in lines)
    assert mail.resend_sent == [] and not state.exists()
    assert API_KEY not in "\n".join(lines)


def test_once_configured_the_first_run_reports_what_is_already_wrong(monkeypatch, checkout, tmp_path):
    mail = FakeMail()
    _run(monkeypatch, checkout, tmp_path, [{"kafka": "FAIL"}], mail)
    assert mail.resend_sent == []
    _write_env(checkout, demo=RESEND)
    lines, _ = _run(monkeypatch, checkout, tmp_path, [{"kafka": "FAIL"}] * 2, mail)
    assert lines[-1].endswith("; alert sent (resend)") and len(mail.resend_sent) == 1


def test_a_failed_send_is_logged_without_the_key_and_retried(monkeypatch, checkout, tmp_path):
    _write_env(checkout, demo=RESEND)
    mail = FakeMail(fail=RuntimeError(f"Resend answered HTTP 401: bad key {API_KEY}"))
    lines, state = _run(monkeypatch, checkout, tmp_path, [{"kafka": "FAIL"}] * 2, mail)
    assert "; alert NOT sent (resend): RuntimeError: Resend answered HTTP 401: bad key ***" in lines[-1]
    st = json.loads(state.read_text())     # not notified: still pending, so the next run tries again
    assert API_KEY not in lines[-1] + state.read_text() and "degraded" not in st and st["pending"]["runs"] == 2
    mail.fail = None
    lines, _ = _run(monkeypatch, checkout, tmp_path, [{"kafka": "FAIL"}], mail)
    assert lines[-1].endswith("; alert sent (resend)") and len(mail.resend_sent) == 1


def test_an_infra_check_error_alerts_too(monkeypatch, checkout, tmp_path):
    _write_env(checkout, demo=RESEND)
    mail = FakeMail()
    def boom(env, c=None):
        raise RuntimeError("docker: command not found")
    monkeypatch.setattr(m, "infra_check", boom)
    log = tmp_path / "rv" / "infra-check.log"
    env = m.Env(runner=None, http=None, ask=lambda p: "", say=lambda s: None, now=lambda: 1.0, repo=checkout,
                resend=mail.resend)
    assert m.infra_check_logged(env, log, record=False, checkout=checkout) == 1
    assert log.read_text().strip().endswith("; change pending (1 of 2 runs)") and mail.resend_sent == []
    assert m.infra_check_logged(env, log, record=False, checkout=checkout) == 1
    assert log.read_text().strip().endswith("; alert sent (resend)")
    payload = mail.resend_sent[0][1]
    assert payload["subject"].endswith("] ERROR: infra-check") and "docker: command not found" in payload["text"]


def test_no_alert_flag_sends_nothing(monkeypatch, checkout, tmp_path):
    _write_env(checkout, demo=RESEND)
    mail = FakeMail()
    it = _results({"kafka": "FAIL"})
    monkeypatch.setattr(m, "infra_check", lambda env, c=None: next(it))
    log = tmp_path / "n.log"
    env = m.Env(runner=None, http=None, ask=lambda p: "", say=lambda s: None, now=lambda: 1.0, repo=checkout,
                resend=mail.resend)
    m.main(["infra-check", "--checkout", str(checkout), "--log", str(log), "--no-alert"], env=env)
    assert mail.resend_sent == [] and "alert" not in log.read_text()


def test_a_flapping_row_sends_nothing(monkeypatch, checkout, tmp_path):
    """A worker OFFLINE -> ONLINE -> OFFLINE -> ONLINE never holds for two runs: no mail at all."""
    _write_env(checkout, demo=RESEND)
    mail = FakeMail()
    lines, state = _run(monkeypatch, checkout, tmp_path,
                        [{"pool": "WARN"}, {"pool": "PASS"}, {"pool": "WARN"}, {"pool": "PASS"}, {"pool": "WARN"}], mail)
    assert mail.resend_sent == []
    assert [ln.rsplit("; ", 1)[1] for ln in lines] == [
        "change pending (1 of 2 runs)", "no change (pending change did not hold)", "change pending (1 of 2 runs)",
        "no change (pending change did not hold)", "change pending (1 of 2 runs)"]
    assert json.loads(state.read_text())["pending"]["runs"] == 1


def test_a_flap_between_two_bad_sets_sends_nothing(monkeypatch, checkout, tmp_path):
    """WARN -> FAIL -> WARN -> FAIL: each new set restarts the count, so none is mailed."""
    _write_env(checkout, demo=RESEND)
    mail = FakeMail()
    _run(monkeypatch, checkout, tmp_path, [{"k": "WARN"}, {"k": "FAIL"}, {"k": "WARN"}, {"k": "FAIL"}], mail)
    assert mail.resend_sent == []


def test_a_change_held_twice_sends_exactly_once(monkeypatch, checkout, tmp_path):
    _write_env(checkout, demo=RESEND)
    mail = FakeMail()
    lines, state = _run(monkeypatch, checkout, tmp_path, [{"pool": "WARN"}] * 5, mail)
    assert len(mail.resend_sent) == 1 and lines[1].endswith("; alert sent (resend)")
    assert all(ln.endswith("; no change") for ln in lines[2:])
    st = json.loads(state.read_text())
    assert st["degraded"] == {"pool": "WARN"} and "pending" not in st


def test_a_recovery_held_twice_sends_one_recovery_mail(monkeypatch, checkout, tmp_path):
    _write_env(checkout, demo=RESEND)
    mail = FakeMail()
    lines, _ = _run(monkeypatch, checkout, tmp_path,
                    [{"pool": "WARN"}, {"pool": "WARN"}, {"pool": "PASS"}, {"pool": "WARN"},   # recovery did not hold
                     {"pool": "PASS"}, {"pool": "PASS"}, {"pool": "PASS"}], mail)
    subjects = [p["subject"] for _, p in mail.resend_sent]
    assert len(subjects) == 2 and "recovered" in subjects[1]
    assert lines[3].endswith("; no change (pending change did not hold)")
    assert lines[5].endswith("; recovery sent (resend)") and lines[6].endswith("; no change")


def test_the_recorded_result_carries_alerting_for_the_panel(monkeypatch, checkout, tmp_path):
    _write_env(checkout, demo=RESEND)
    mail = FakeMail()
    recorded = []
    monkeypatch.setattr(m, "record_infra", lambda env, result: recorded.append(result))
    it = _results({"pool": "WARN"}, {"pool": "WARN"}, {"pool": "WARN"})
    monkeypatch.setattr(m, "infra_check", lambda env, c=None: next(it))
    log = tmp_path / "rv" / "infra-check.log"
    env = m.Env(runner=None, http=None, ask=lambda p: "", say=lambda s: None, now=lambda: 1_794_487_200.0,
                repo=checkout, resend=mail.resend)
    for _ in range(3):
        m.infra_check_logged(env, log, record=True, checkout=checkout)
    a = [r["alerting"] for r in recorded]
    assert [x["outcome"] for x in a] == ["change pending (1 of 2 runs)", "alert sent (resend)", "no change"]
    assert a[0]["lastSentAt"] is None and a[2]["lastSentAt"] == a[1]["lastSentAt"] is not None
    assert all(x["configured"] is True and x["route"] == "resend" for x in a)
    assert API_KEY not in json.dumps(recorded)
    recorded.clear()
    it2 = _results({"pool": "WARN"})
    monkeypatch.setattr(m, "infra_check", lambda env, c=None: next(it2))
    m.infra_check_logged(env, log, record=True, checkout=checkout, alert=False)
    assert recorded[0]["alerting"] == {"outcome": "off for this run (--no-alert)", "configured": None}


def test_the_resend_request_verifies_tls_and_matches_cert_watch(monkeypatch):
    seen = {}

    class Resp:
        status = 200
        def __enter__(self): return self
        def __exit__(self, *a): return False

    def urlopen(req, timeout=None, context=None):
        seen.update(url=req.full_url, method=req.get_method(), auth=req.get_header("Authorization"),
                    body=json.loads(req.data), verify=context.verify_mode, hostname=context.check_hostname)
        return Resp()

    monkeypatch.setattr(m.urllib.request, "urlopen", urlopen)
    m._resend_default(API_KEY, {"from": "f", "to": ["t"], "subject": "s", "text": "b"})
    import ssl as _ssl
    assert seen["url"] == "https://api.resend.com/emails" and seen["method"] == "POST"
    assert seen["auth"] == f"Bearer {API_KEY}" and seen["body"]["to"] == ["t"]
    assert seen["verify"] == _ssl.CERT_REQUIRED and seen["hostname"] is True
