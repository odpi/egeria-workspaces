"""bin/egeria-upgrade-reset (BRIEF-RESET-RECOVERY-TOOLING-2026-11-12, Part 2), fully offline.

A fake runner answers every host command and records it; a fake HTTP layer answers the Portal and
Egeria; a temporary folder stands in for the deployment checkout. Nothing here touches Docker,
Postgres, laz or the live checkout. Standard library + pytest only (runs on the host or in the
Portal image).
"""
import gzip
import json
import re
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
QS = HERE.parent.parent
REPO = QS.parent.parent
sys.path.insert(0, str(QS / "bin"))

import egeria_upgrade_reset as m  # noqa: E402

OLD = "sha256:" + "1" * 64
NEW = "sha256:" + "2" * 64
OLD_IMG, NEW_IMG = "sha256:oldimage", "sha256:newimage"
SECRET_VALUE = "s3cr3t-value-never-printed"
DUMP = "--\n-- PostgreSQL database dump\n--\nCREATE TABLE x();\n\n--\n-- PostgreSQL database dump complete\n--\n"


def _secrets(users: dict) -> str:
    out = ["secretsCollections:", "  cocoUserDirectory:", "    users:"]
    for name, pw in users.items():
        out += [f"      {name}:", "        secrets:", f"          clearPassword: {pw}"]
    return "\n".join(out) + "\n"


@pytest.fixture
def deploy(tmp_path):
    root = tmp_path / "deploy"
    qs = root / "compose-configs" / "egeria-quickstart"
    (qs / "secrets").mkdir(parents=True)
    (qs / "Dockerfile-egeria-platform").write_text(f"#comment\nFROM docker.io/odpi/egeria-platform:latest@{OLD}\n")
    (qs / "secrets" / "coco-user-directory.omsecrets").write_text(
        _secrets({"erinoverview": SECRET_VALUE, "garygeeke": SECRET_VALUE, "olpgpubnpa": SECRET_VALUE}))
    (qs / "secrets" / "integration.omsecrets").write_text("secretsCollections:\n  x: {}\n")
    rt = root / "runtime-volumes" / "quickstart-platform-data" / "secrets"
    rt.mkdir(parents=True)
    (rt / "coco-user-directory.omsecrets").write_text(
        _secrets({"erinoverview": "old-" + SECRET_VALUE, "garygeeke": SECRET_VALUE, "retired": SECRET_VALUE}))
    (rt / "resource-explorer.omsecrets").write_text("re: keep me\n")
    (root / "compose-configs" / "shared-infra").mkdir(parents=True)
    (root / "compose-configs" / "shared-infra" / "reset-egeria-db.sql").write_text(
        (REPO / "compose-configs" / "shared-infra" / "reset-egeria-db.sql").read_text())
    (qs / "PyegeriaWebHandler" / "logs").mkdir(parents=True)
    return root


class FakeRunner(m.Runner):
    """Answers host commands from a small model of the host; records every call."""

    def __init__(self, deploy: Path):
        self.calls, self.deploy = [], deploy
        self.running_image = OLD_IMG
        self.built_image = NEW_IMG
        self.free_kb = 50 * 1024 * 1024
        self.db_bytes = 381_000_000
        self.dump = DUMP
        self.dump_rc = 0
        self.container_secrets = None      # None: mirror the host folder (a healthy bind mount)
        self.procs = {79299: (1, "uv run --package resource-explorer web --port 8813"),
                      79303: (79299, "python resource-explorer web --port 8813"),
                      79339: (1, "python ../../.venv/bin/egeria-advisor-web --port 8880")}
        self.listeners = {8813: 79303, 8880: 79339}
        self.killed, self.spawned = [], []

    def run(self, cmd, *, input_text=None, cwd=None, check=True, timeout=None):
        self.calls.append(cmd)
        j = " ".join(cmd)
        r = self._answer(cmd, j, input_text)
        if check and r.rc != 0:
            raise m.StepFailed(f"{j[:60]} exited {r.rc}")
        return r

    def _answer(self, cmd, j, input_text):
        R = m.Result
        if j.startswith("docker inspect quickstart-egeria-main --format {{index"):
            wd = self.deploy / "compose-configs" / "egeria-quickstart"
            return R(0, f"egeria-quickstart|{wd}/egeria-quickstart.yaml,{wd}/egeria-quickstart-local.yaml|{wd}|{self.running_image}\n")
        if j.startswith("docker inspect quickstart-egeria-main --format {{.State.Running}}"):
            return R(0, "false\n")
        if j.startswith("docker inspect egeria-shared-postgres"):
            return R(0, "true\n")
        if "pg_database_size" in j:
            return R(0, f"{self.db_bytes}\n" if self.db_bytes is not None else "")
        if j.endswith("df -Pk /"):
            return R(0, f"Filesystem 1024-blocks Used Available Capacity Mounted\noverlay 1 1 {self.free_kb} 1% /\n")
        if cmd[:2] == ["ps", "-axo"]:
            return R(0, "".join(f"{p} {pp} {c}\n" for p, (pp, c) in self.procs.items()))
        if cmd[0] == "lsof" and "-sTCP:LISTEN" in cmd:
            port = int(cmd[2].split(":")[1])
            return R(0, f"{self.listeners[port]}\n" if port in self.listeners else "", "") if port in self.listeners else R(1)
        if cmd[0] == "lsof" and "cwd" in cmd:
            return R(0, "p1\nn/somewhere\n")
        if cmd[:3] == ["docker", "image", "inspect"]:
            return R(0, f"{self.built_image}\n")
        if "pg_stat_activity" in j:
            return R(0, "active=2 idle=5\n")
        if cmd[:2] == ["docker", "logs"]:
            return R(0, "INFO started\n")
        if "/deployments/secrets" in j:
            if self.container_secrets is None:
                rt = self.deploy / "runtime-volumes" / "quickstart-platform-data" / "secrets"
                return R(0, "".join(f"{f.stat().st_size} {f.name}\n" for f in sorted(rt.iterdir())))
            out, self.container_secrets = self.container_secrets, None   # stale once, fixed by the restart
            return R(0, out)
        if "compose" in cmd and "up" in cmd:
            self.running_image = self.built_image
            return R(0)
        if "egeria_resets" in j:
            return R(0, "INSERT 0 1\n")
        return R(0)

    def stream_gzip(self, cmd, dest):
        self.calls.append(cmd)
        with gzip.open(dest, "wt") as f:
            f.write(self.dump)
        return self.dump_rc

    def spawn(self, argv, cwd, log):
        self.spawned.append((argv, cwd))
        return 4242

    def kill(self, pid):
        self.killed.append(pid)


class FakeHttp:
    def __init__(self):
        self.calls = []
        self.status = {"reinitializing": False, "lastCheckAt": None, "families": {}}
        self.purposes = {"purposes": {f"T{i}": "GOVERNANCE" for i in range(94)}, "serverReportsPurpose": True}
        self.find_count = 1

    def request(self, method, url, body=None, headers=None, timeout=30):
        self.calls.append((method, url))
        if url.endswith("/api/bootstrap/status"):
            return 200, self.status
        if url.endswith("/api/bootstrap/batches"):
            return 200, [{"id": "Security", "enabled": True,
                          "canary": {"type": "ExternalReference", "name": "Guidelines"}},
                         {"id": "Off", "enabled": False, "canary": {"type": "X", "name": "y"}}]
        if url.endswith("/api/token"):
            return 200, "tok"
        if url.endswith("/by-search-conditions"):
            return 200, {"elements": [{"elementGUID": f"g{i}"} for i in range(self.find_count)]}
        if url.endswith("/members"):
            n = 2 if "g0" in url else 0
            return 200, {"elements": [{"properties": {"qualifiedName": f"m{i}"}} for i in range(5)]}
        if url.endswith("/classification-purposes"):
            return 200, self.purposes
        return 404, "nope"


class Clock:
    def __init__(self, t=1_762_941_600.0):
        self.t = t

    def now(self):
        return self.t

    def sleep(self, s):
        self.t += s


@pytest.fixture
def world(deploy, monkeypatch):
    runner, http, clock = FakeRunner(deploy), FakeHttp(), Clock()
    answers = {"clear": "egeria", "persona": "ok"}
    said = []

    def ask(prompt):
        return answers["clear"] if "DROP" in prompt or "database name" in prompt else \
            (answers.get("redo", "") if "run-once" in prompt else answers["persona"])

    ports = {8813: True, 8880: True}

    def port_open(p):
        return ports.get(p, False)

    def kill(pid):
        runner.killed.append(pid)
        for port, lp in runner.listeners.items():
            if lp in (pid,) or runner.procs.get(lp, (0,))[0] == pid:
                ports[port] = False

    def spawn(argv, cwd, log):
        runner.spawned.append((argv, cwd))
        for port in ports:
            if str(port) in " ".join(argv):
                ports[port] = True
        return 4242

    runner.kill, runner.spawn = kill, spawn
    # heal-wait: a monitor pass that started a full cycle after the recreate
    orig = http.request

    def request(method, url, body=None, headers=None, timeout=30):
        if url.endswith("/api/bootstrap/status"):
            http.status["lastCheckAt"] = m.iso(clock.now())
        return orig(method, url, body, headers, timeout)

    http.request = request
    env = m.Env(runner=runner, http=http, ask=ask, say=said.append, sleep=clock.sleep, now=clock.now,
                port_open=port_open, repo=deploy)
    return {"env": env, "runner": runner, "http": http, "clock": clock, "answers": answers, "said": said,
            "deploy": deploy, "ports": ports}


def _plan(w, **kw):
    kw.setdefault("digest", NEW)
    run_dir = m.make_plan(w["env"], digest=kw["digest"], latest=False, clear=kw.get("clear", True),
                          reset_root=w["deploy"] / "runtime-volumes" / "egeria-resets")
    return run_dir


MUTATING = re.compile(r"^docker (stop|start|restart|tag|compose .* (build|up))|DROP DATABASE|-f -$")


def _mutations(calls):
    return [c for c in calls if MUTATING.search(" ".join(c)) or c[:2] == ["docker", "start"]]


# ── plan ──────────────────────────────────────────────────────────────────────

def test_plan_reads_and_changes_nothing(world):
    before = (world["deploy"] / "compose-configs/egeria-quickstart/Dockerfile-egeria-platform").read_text()
    run_dir = _plan(world)
    plan = json.loads((run_dir / "plan.json").read_text())
    state = json.loads((run_dir / "state.json").read_text())
    assert plan["image"] == {"dockerfile": str(world["deploy"] / "compose-configs/egeria-quickstart/Dockerfile-egeria-platform"),
                             "currentDigest": OLD, "targetDigest": NEW, "repin": True, "runningImageId": OLD_IMG}
    assert plan["databaseSizeClass"] == "<1GB" and plan["steps"] == m.STEPS and plan["blockers"] == []
    assert [w["launcherPid"] for w in plan["writers"]["known"]] == [79299, 79339]
    assert all(v["status"] == "pending" for v in state["steps"].values())
    assert _mutations(world["runner"].calls) == []
    assert (world["deploy"] / "compose-configs/egeria-quickstart/Dockerfile-egeria-platform").read_text() == before
    out = "\n".join(world["said"])
    assert "Nothing has been changed" in out and OLD in out and NEW in out


def test_plan_secrets_names_only(world):
    _plan(world)
    out = "\n".join(world["said"])
    assert "added olpgpubnpa" in out and "removed retired" in out and "changed erinoverview" in out
    assert "resource-explorer.omsecrets: kept as is" in out
    assert SECRET_VALUE not in out and "clearPassword" not in out


def test_plan_without_clear_drops_backup_and_clear(world):
    plan = json.loads((_plan(world, clear=False) / "plan.json").read_text())
    assert "clear" not in plan["steps"] and "backup" not in plan["steps"] and plan["backup"]["to"] is None


@pytest.mark.parametrize("setup, words", [
    (lambda r: setattr(r, "free_kb", 10 * 1024 * 1024), "GB free"),
    (lambda r: r.procs.update({555: (1, "python resource-explorer web --port 8810")}), "unknown RE/EA"),
])
def test_plan_blockers_and_apply_refuses(world, setup, words):
    setup(world["runner"])
    run_dir = _plan(world)
    plan = json.loads((run_dir / "plan.json").read_text())
    assert any(words in b for b in plan["blockers"])
    with pytest.raises(m.Refused, match="blockers"):
        m.apply(world["env"], str(run_dir))


# ── dry run, refusals ─────────────────────────────────────────────────────────

def test_dry_run_touches_nothing(world):
    run_dir = _plan(world)
    world["runner"].calls.clear()
    state_before = (run_dir / "state.json").read_text()
    assert m.apply(world["env"], str(run_dir), dry_run=True) == 0
    assert world["runner"].calls == [] and world["http"].calls == []
    assert (run_dir / "state.json").read_text() == state_before


def test_apply_refuses_another_running_image(world):
    run_dir = _plan(world)
    world["runner"].running_image = "sha256:someoneelse"
    with pytest.raises(m.Refused, match="now runs image"):
        m.apply(world["env"], str(run_dir))


def test_apply_refuses_another_database_size(world):
    run_dir = _plan(world)
    world["runner"].db_bytes = 5_000_000_000
    with pytest.raises(m.Refused, match="<10GB"):
        m.apply(world["env"], str(run_dir))


# ── the whole run ─────────────────────────────────────────────────────────────

def _state(run_dir):
    return json.loads((run_dir / "state.json").read_text())


def test_full_apply(world):
    run_dir = _plan(world)
    assert m.apply(world["env"], str(run_dir)) == 0
    st = _state(run_dir)
    assert all(v["status"] == "done" for v in st["steps"].values()), {k: v.get("error") for k, v in st["steps"].items()}
    calls = [" ".join(c) for c in world["runner"].calls]
    # re-pinned and built, with a rollback tag first
    assert NEW in (world["deploy"] / "compose-configs/egeria-quickstart/Dockerfile-egeria-platform").read_text()
    tag = next(i for i, c in enumerate(calls) if c.startswith("docker tag egeria-quickstart-platform:local"))
    build = next(i for i, c in enumerate(calls) if " build " in c)
    assert tag < build
    # recreate, never start
    assert any("up -d --no-deps --force-recreate egeria-main" in c for c in calls)
    assert not any(c.startswith("docker start") for c in calls)
    assert st["steps"]["recreate"]["evidence"]["runningImageId"] == NEW_IMG
    # the backup was checked
    ev = st["steps"]["backup"]["evidence"]
    assert ev["endMarker"] == "found" and ev["gzipTest"] == "ok" and len(ev["sha256"]) == 64
    # the clear ran the shared SQL with the database name as a variable
    assert any(c.endswith("-v db=egeria -f -") for c in calls)
    # writers stopped then restarted the way they were started
    assert world["runner"].killed == [79299, 79339]
    assert [a for a, _ in world["runner"].spawned] == [w["argv"] for w in st["steps"]["freeze-writers"]["evidence"]["stopped"]]
    # heal waited a full monitor cycle after the recreate
    rec = st["steps"]["recreate"]["finishedAt"]
    assert world["clock"].now() >= rec + m.MONITOR_CYCLE_S
    # verify ran every check; the record row was written
    verdicts = {c["check"]: c["verdict"] for c in st["steps"]["verify"]["evidence"]["checks"]}
    assert verdicts["canary Security"] == "PASS" and verdicts["classification purposes"] == "PASS"
    assert verdicts["persona sign-ins"] == "PASS" and verdicts["saved-query tile"] == "NOT MEASURED"
    assert any("demo.egeria_resets" in c for c in calls)
    # secrets: names only, extra file kept, no value printed anywhere
    out = "\n".join(world["said"])
    assert SECRET_VALUE not in out
    assert (world["deploy"] / "runtime-volumes/quickstart-platform-data/secrets/resource-explorer.omsecrets").exists()


def test_resume_after_a_failed_step(world):
    run_dir = _plan(world)
    world["runner"].dump = "-- truncated\nCREATE TABLE x("          # no end marker
    assert m.apply(world["env"], str(run_dir)) == 1
    st = _state(run_dir)
    assert st["steps"]["backup"]["status"] == "failed" and "truncated" in st["steps"]["backup"]["error"]
    assert st["steps"]["clear"]["status"] == "pending"
    assert not any("-f -" in " ".join(c) for c in world["runner"].calls)     # nothing dropped
    stops = sum(1 for c in world["runner"].calls if c[:2] == ["docker", "stop"])
    world["runner"].dump = DUMP
    world["runner"].running_image = OLD_IMG
    assert m.apply(world["env"], str(run_dir)) == 0
    assert sum(1 for c in world["runner"].calls if c[:2] == ["docker", "stop"]) == stops   # not repeated
    assert _state(run_dir)["steps"]["backup"]["status"] == "done"


def test_run_once_steps_need_redo_and_the_typed_name(world):
    run_dir = _plan(world)
    assert m.apply(world["env"], str(run_dir)) == 0
    n_dumps = sum(1 for c in world["runner"].calls if "pg_dump" in c)
    assert m.apply(world["env"], str(run_dir)) == 0                       # nothing left to do
    assert sum(1 for c in world["runner"].calls if "pg_dump" in c) == n_dumps
    world["answers"]["redo"] = "nope"
    with pytest.raises(m.Refused, match="not typed"):
        m.apply(world["env"], str(run_dir), redo="backup")
    world["answers"]["redo"] = "backup"
    assert m.apply(world["env"], str(run_dir), redo="backup") == 0
    assert sum(1 for c in world["runner"].calls if "pg_dump" in c) == n_dumps + 1


def test_clear_checkpoint_wrong_name_drops_nothing(world):
    run_dir = _plan(world)
    world["answers"]["clear"] = "egeria_typo"
    assert m.apply(world["env"], str(run_dir)) == 1
    st = _state(run_dir)
    assert st["steps"]["clear"]["status"] == "failed" and "checkpoint not passed" in st["steps"]["clear"]["error"]
    assert not any(" ".join(c).endswith("-f -") for c in world["runner"].calls)


@pytest.mark.parametrize("bad", ["not gzip at all", None])
def test_backup_checks(tmp_path, bad):
    p = tmp_path / "d.sql.gz"
    if bad is None:
        with gzip.open(p, "wt") as f:
            f.write(DUMP)
        p.write_bytes(p.read_bytes()[:-10])           # cut the gzip short
    else:
        p.write_text(bad)
    with pytest.raises(m.StepFailed, match="not a complete gzip file"):
        m.verify_dump(p)


def test_recreate_image_mismatch_fails(world):
    run_dir = _plan(world)
    world["runner"].built_image = NEW_IMG

    def up_wrong(cmd, j, inp, orig=world["runner"]._answer):
        if "compose" in cmd and "up" in cmd:
            world["runner"].running_image = "sha256:stale"
            return m.Result(0)
        return orig(cmd, j, inp)

    world["runner"]._answer = up_wrong
    assert m.apply(world["env"], str(run_dir)) == 1
    st = _state(run_dir)
    assert st["steps"]["recreate"]["status"] == "failed" and "not the image build made" in st["steps"]["recreate"]["error"]


def test_stale_secrets_mount_restarts_once(world):
    run_dir = _plan(world)
    world["runner"].container_secrets = ""            # the container sees an empty folder
    assert m.apply(world["env"], str(run_dir)) == 0
    ev = _state(run_dir)["steps"]["secrets-sync"]["evidence"]
    assert ev["restartedForStaleMount"] is True
    assert sum(1 for c in world["runner"].calls if c[:2] == ["docker", "restart"]) == 1


def test_unknown_writer_appearing_before_freeze_fails_the_step(world):
    run_dir = _plan(world)
    world["runner"].procs[555] = (1, "python egeria-advisor-web --port 8890")
    assert m.apply(world["env"], str(run_dir)) == 1
    st = _state(run_dir)
    assert st["steps"]["freeze-writers"]["status"] == "failed" and "unknown" in st["steps"]["freeze-writers"]["error"]
    assert world["runner"].killed == []


def test_duplicated_canary_fails_verify(world):
    world["http"].find_count = 2
    run_dir = _plan(world)
    assert m.apply(world["env"], str(run_dir)) == 0
    checks = {c["check"]: c for c in _state(run_dir)["steps"]["verify"]["evidence"]["checks"]}
    assert checks["canary Security"]["verdict"] == "FAIL" and "2 found" in checks["canary Security"]["evidence"]


# ── shared SQL and the reset table ────────────────────────────────────────────

def test_reset_sql_is_shared_not_forked():
    sh = (REPO / "compose-configs/shared-infra/reset-egeria-db.sh").read_text()
    assert "reset-egeria-db.sql" in sh and "DROP DATABASE IF EXISTS ${database}" not in sh
    sql = (REPO / "compose-configs/shared-infra/reset-egeria-db.sql").read_text()
    for stmt in ('DROP DATABASE IF EXISTS :"db" WITH (FORCE);', 'CREATE DATABASE :"db";',
                 'GRANT ALL PRIVILEGES ON DATABASE :"db" TO egeria_admin, egeria_user;'):
        assert stmt in sql
    src = (QS / "bin" / "egeria_upgrade_reset.py").read_text()
    assert "DROP DATABASE" not in src.split('"""', 2)[2]          # the CLI has no SQL of its own for the clear


def test_resets_table_columns_match_initdb():
    initdb = (QS / "docker-entrypoint-initdb.d" / "init_egeria.sql").read_text()
    block = initdb[initdb.index("CREATE TABLE IF NOT EXISTS demo.egeria_resets"):]
    block = block[:block.index(");")]
    cols_initdb = re.findall(r"^\s+(\w+)\s", block, re.M)
    cols_cli = re.findall(r" (\w+) (?:serial|timestamptz|text|bigint|jsonb)", m.RESETS_DDL)
    assert cols_initdb == cols_cli


def test_database_name_guard():
    for bad in ("postgres", "template1", "Egeria", "egeria; drop", ""):
        assert not (m.DB_NAME_RE.match(bad) and bad != "postgres" and not bad.startswith("template"))
