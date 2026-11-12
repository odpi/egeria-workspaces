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
# The real pg_dump 17.6+ tail: the marker, then `\unrestrict <token>` (read-back: pg_dump 17.10 on laz).
DUMP = ("--\n-- PostgreSQL database dump\n--\n\\restrict Abc123\nCREATE TABLE x();\n\n--\n"
        "-- PostgreSQL database dump complete\n--\n\n\\unrestrict Abc123\n")


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
        if j.startswith("docker inspect quickstart-egeria-main --format {{.State.StartedAt}}"):
            return R(0, "2026-11-12T16:59:47.123456789Z\n")
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
        # the Portal's report-spec sync (POST to start, GET for the outcome)
        self.sync_post = 200
        self.sync_post_body = {"started": True, "already_running": False}
        self.sync = {"running": False, "outcome": "synced", "finished_at": "2099-01-01T00:00:00+00:00",
                     "error": None, "report": {"consumers": {"status": "read", "consumers": 2, "labels": 7}}}

    def request(self, method, url, body=None, headers=None, timeout=30):
        self.calls.append((method, url))
        if url.endswith("/api/report-specs/sync"):
            return (self.sync_post, self.sync_post_body) if method == "POST" else (200, self.sync)
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


def _launchers(root: Path) -> dict:
    out = {}
    for port, name in ((8813, "start-8813.sh"), (8880, "start-ea-8880.sh")):
        p = root / "launchers" / name
        p.parent.mkdir(exist_ok=True)
        p.write_text("#!/bin/sh\nexit 0\n")
        p.chmod(0o755)
        out[port] = str(p)
    return out


def _plan(w, **kw):
    kw.setdefault("digest", NEW)
    run_dir = m.make_plan(w["env"], digest=kw["digest"], latest=False, clear=kw.get("clear", True),
                          reset_root=w["deploy"] / "runtime-volumes" / "egeria-resets",
                          allow_other_checkout=kw.get("allow_other_checkout", False),
                          launcher_overrides=kw.get("launchers", _launchers(w["deploy"])))
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
    world["http"].calls.clear()
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
    # restarted through the launcher scripts, run from their own folder; never the recorded command
    assert [a for a, _ in world["runner"].spawned] == [[str(world["deploy"] / "launchers" / "start-8813.sh")],
                                                       [str(world["deploy"] / "launchers" / "start-ea-8880.sh")]]
    assert all(cwd == str(world["deploy"] / "launchers") for _, cwd in world["runner"].spawned)
    stopped = st["steps"]["freeze-writers"]["evidence"]["stopped"]
    assert stopped[0]["command"].startswith("uv run --package resource-explorer")       # kept as evidence
    # R-B1: secrets synced while stopped, before the recreate; the mount checked in the recreate
    order = list(st["steps"])
    assert order.index("secrets-sync") < order.index("recreate") < order.index("heal-wait")
    assert st["steps"]["recreate"]["evidence"]["secretsMountMatches"] is True
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
    st = _state(run_dir)
    assert st["steps"]["recreate"]["evidence"]["restartedForStaleMount"] is True
    # the restart came after the recreate and before the heal started waiting (R-B1)
    restart_i = next(i for i, c in enumerate(world["runner"].calls) if c[:2] == ["docker", "restart"])
    up_i = next(i for i, c in enumerate(world["runner"].calls) if "up" in c and "compose" in c)
    assert up_i < restart_i
    assert st["steps"]["heal-wait"]["startedAt"] >= st["steps"]["recreate"]["finishedAt"]
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


# ── read-back R-B2: no usable launcher, no auto-restart ──────────────────────

def test_writer_without_a_launcher_needs_a_person(world):
    lns = _launchers(world["deploy"])
    lns[8880] = str(world["deploy"] / "launchers" / "missing.sh")
    run_dir = _plan(world, launchers=lns)
    assert "NO usable launcher" in "\n".join(world["said"])
    assert m.apply(world["env"], str(run_dir)) == 3
    st = _state(run_dir)
    assert st["steps"]["unfreeze"]["status"] == "needs a person"
    manual = st["steps"]["unfreeze"]["evidence"]["needsPerson"]
    assert [x["port"] for x in manual] == [8880] and "egeria-advisor-web" in manual[0]["command"]
    assert [a for a, _ in world["runner"].spawned] == [[lns[8813]]]           # only RE restarted
    assert st["steps"]["verify"]["status"] == "done" and st["steps"]["record"]["status"] == "done"
    assert st["steps"]["record"]["evidence"]["outcome"] == "completed, needs a person"


def test_launcher_flag_must_name_a_writer_port(world, monkeypatch):
    monkeypatch.setattr(m, "make_plan", lambda *a, **k: None)
    assert m.main(["plan", "--launcher", "9999=/x"], env=world["env"]) == 2
    assert m.main(["plan", "--launcher", "8813=/x"], env=world["env"]) == 0


# ── read-back R-B3: the classification count against the plan's baseline ────

def _cplan(count, new_image=True, reports=True):
    return {"classificationTypes": {"count": count, "serverReportsPurpose": reports},
            "image": {"currentDigest": OLD, "targetDigest": NEW if new_image else OLD}}


@pytest.mark.parametrize("plan, now, verdict, words", [
    (_cplan(94), {"count": 94, "serverReportsPurpose": True}, "PASS", "as before"),
    (_cplan(94), {"count": 96, "serverReportsPurpose": True}, "CHANGED", "CHANGED 94→96 (new image): review"),
    (_cplan(94, new_image=False), {"count": 96, "serverReportsPurpose": True}, "FAIL", "same image"),
    (_cplan(94), {"count": 90, "serverReportsPurpose": True}, "FAIL", "fewer"),
    (_cplan(94), {"count": 94, "serverReportsPurpose": False}, "FAIL", "no longer reports"),
    (_cplan(94), {"notRead": "HTTP 502"}, "NOT MEASURED", "HTTP 502"),
    ({"classificationTypes": {"notRead": "HTTP 401"}, "image": {"currentDigest": OLD, "targetDigest": NEW}},
     {"count": 94, "serverReportsPurpose": True}, "NOT MEASURED", "no baseline"),
])
def test_classification_verdicts(plan, now, verdict, words):
    v, ev = m.classification_verdict(plan, now)
    assert v == verdict and words in ev


def test_plan_records_the_baseline(world):
    plan = json.loads((_plan(world) / "plan.json").read_text())
    assert plan["classificationTypes"] == {"count": 94, "serverReportsPurpose": True}
    assert not hasattr(m, "CLASSIFICATION_TYPES")


def test_changed_count_on_a_new_image_does_not_fail_the_reset(world):
    run_dir = _plan(world)
    world["http"].purposes = {"purposes": {f"T{i}": "GOVERNANCE" for i in range(97)}, "serverReportsPurpose": True}
    assert m.apply(world["env"], str(run_dir)) == 0
    checks = {c["check"]: c for c in _state(run_dir)["steps"]["verify"]["evidence"]["checks"]}
    assert checks["classification purposes"]["verdict"] == "CHANGED"
    assert "classification purposes" not in _state(run_dir)["steps"]["verify"]["evidence"]["failed"]


# ── read-back small item: the CLI and the deployment must be one checkout ─────

def test_other_checkout_refused_unless_allowed(world, tmp_path):
    world["env"].repo = tmp_path / "some-worktree"
    with pytest.raises(m.Refused, match="allow-other-checkout"):
        _plan(world)
    run_dir = _plan(world, allow_other_checkout=True)
    out = "\n".join(world["said"])
    assert "Deployment (the running platform's compose folder)" in out and "This CLI's checkout" in out
    assert json.loads((run_dir / "plan.json").read_text())["allowOtherCheckout"] is True


def test_apply_refuses_a_plan_from_another_checkout(world, tmp_path):
    run_dir = _plan(world)
    world["env"].repo = tmp_path / "some-worktree"
    with pytest.raises(m.Refused, match="allow-other-checkout"):
        m.apply(world["env"], str(run_dir))


def test_dump_with_the_real_pg17_tail_passes():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "x.sql.gz"
        with gzip.open(p, "wt") as f:
            f.write(DUMP)
        assert m.verify_dump(p)["endMarker"] == "found"
        assert DUMP.rstrip().splitlines()[-1].startswith("\\unrestrict")


# ── Shared-infrastructure lines in verify (BRIEF-SHARED-INFRA-HEALTH-2026-11-12) ─

def _infra(verdicts):
    return {"services": [{"service": k, "verdict": v, "words": f"{k} words"} for k, v in verdicts.items()],
            "openlineage": {"offset": 5, "latestAt": "2026-11-12T12:00:00+00:00"}}


def test_verify_fails_on_an_infra_fail_and_reports_warn(world, monkeypatch):
    seen = []
    monkeypatch.setattr(m, "infra_check", lambda env, root: seen.append(root) or
                        _infra({"proxy": "FAIL", "kroki": "WARN", "airflow": "EXPECTED STOPPED"}))
    run_dir = _plan(world)
    assert m.apply(world["env"], str(run_dir)) == 0
    ev = _state(run_dir)["steps"]["verify"]["evidence"]
    v = {c["check"]: c["verdict"] for c in ev["checks"]}
    assert v["infra proxy"] == "FAIL" and v["infra kroki"] == "WARN" and v["infra openlineage.events"] == "INFO"
    assert "infra proxy" in ev["failed"] and "infra kroki" not in ev["failed"]
    assert ev["warnings"] == ["infra kroki", "infra airflow"]
    assert seen == [world["deploy"]]                      # the deployment checkout from the plan


def test_verify_with_infra_warn_only_does_not_fail(world, monkeypatch):
    monkeypatch.setattr(m, "infra_check", lambda env, root: _infra({"proxy": "PASS", "kroki": "WARN"}))
    run_dir = _plan(world)
    m.apply(world["env"], str(run_dir))
    ev = _state(run_dir)["steps"]["verify"]["evidence"]
    assert not [f for f in ev["failed"] if f.startswith("infra")]


def test_verify_infra_error_is_not_measured(world, monkeypatch):
    def boom(env, root):
        raise RuntimeError("docker not on PATH")
    monkeypatch.setattr(m, "infra_check", boom)
    run_dir = _plan(world)
    m.apply(world["env"], str(run_dir))
    c = [c for c in _state(run_dir)["steps"]["verify"]["evidence"]["checks"] if c["check"].startswith("infra")]
    assert c == [{"check": "infra (shared-infra compose)", "verdict": "NOT MEASURED",
                  "evidence": "RuntimeError: docker not on PATH"}]


# ── verify in the background: the persona checkpoint (2026-11-12, first real run) ────────

def _bare_env(ask=input, personas=None):
    return m.Env(runner=None, http=None, ask=ask, say=lambda s: None, personas=personas)


@pytest.mark.parametrize("answer,verdict", [("ok", "PASS"), ("skip", "NOT MEASURED"), ("OK", "PASS")])
def test_persona_answer_given_up_front_never_asks(answer, verdict):
    def ask(prompt):
        raise AssertionError("asked although the answer was given up front")
    c = m.persona_check(_bare_env(ask=ask, personas=answer))
    assert c["verdict"] == verdict and c["evidence"] == f"answered up front: {answer.lower()}"


def test_persona_answer_from_the_environment(monkeypatch):
    monkeypatch.setenv("EGERIA_RESET_PERSONAS", "skip")
    assert m.persona_check(_bare_env(ask=lambda p: "ok"))["verdict"] == "NOT MEASURED"


def test_a_bad_up_front_answer_is_not_measured():
    c = m.persona_check(_bare_env(personas="yes"))
    assert c["verdict"] == "NOT MEASURED" and "not one of ok, skip" in c["evidence"]


def test_no_terminal_and_no_answer_is_not_measured_without_asking(monkeypatch):
    monkeypatch.delenv("EGERIA_RESET_PERSONAS", raising=False)
    monkeypatch.setattr(m.sys.stdin, "isatty", lambda: False, raising=False)
    c = m.persona_check(_bare_env(ask=input))
    assert c == {"check": "persona sign-ins", "verdict": "NOT MEASURED",
                 "evidence": "no terminal to ask and no --personas answer (a background run)"}


def test_end_of_input_at_the_prompt_is_not_measured_never_a_crash(monkeypatch):
    monkeypatch.delenv("EGERIA_RESET_PERSONAS", raising=False)
    def eof(prompt):
        raise EOFError
    c = m.persona_check(_bare_env(ask=eof))
    assert c["verdict"] == "NOT MEASURED" and "end of input" in c["evidence"] and "--personas" in c["evidence"]


def test_the_operator_answer_is_still_recorded(monkeypatch):
    monkeypatch.delenv("EGERIA_RESET_PERSONAS", raising=False)
    assert m.persona_check(_bare_env(ask=lambda p: "ok"))["verdict"] == "PASS"
    c = m.persona_check(_bare_env(ask=lambda p: "garygeeke cannot open the CDO sheet"))
    assert c["verdict"] == "FAIL" and "garygeeke" in c["evidence"]


def test_apply_personas_flag_reaches_verify(world, monkeypatch):
    """apply --personas skip: verify records NOT MEASURED and the persona prompt is never shown."""
    world["answers"]["persona"] = "THIS WAS ASKED"
    run_dir = _plan(world)
    assert m.main(["apply", "--plan", str(run_dir), "--personas", "skip"], env=world["env"]) == 0
    checks = {c["check"]: c for c in _state(run_dir)["steps"]["verify"]["evidence"]["checks"]}
    assert checks["persona sign-ins"]["verdict"] == "NOT MEASURED"
    assert checks["persona sign-ins"]["evidence"] == "answered up front: skip"


# ── the watch: genuine authentication failures only ───────────────────────────

GUID_LINE = ("Thu Nov 12 13:05:11 GMT 2026 qs-engine-host Information OMES-GOVERNANCE-ACTION-0011 The governance "
             "action aee401cf-6b2e-4c51-9f3b-0d2b1a40128e has completed with status ACTIONED")
TIMESTAMP_LINE = "2026-11-12 13:05:11.401 INFO  [qs-view-server] request completed in 0.401 s"
REAL = [
    "Thu Nov 12 13:06:01 GMT 2026 qs-view-server Error OMAG-USER-SECURITY-401-001 The user erinoverview is not authorized",
    "WARN request to https://localhost:9443/servers/qs-view-server/api failed with HTTP Code: 401",
    "org.odpi.openmetadata.frameworks.openmetadata.ffdc.UserNotAuthorizedException: USER_NOT_AUTHORIZED",
    "status=UNAUTHORIZED for peterprofile",
]


def test_a_guid_or_a_timestamp_holding_401_is_not_a_failure():
    assert m.auth_failure_lines(GUID_LINE + "\n" + TIMESTAMP_LINE + "\nINFO started") == []
    assert m.auth_failure_lines("element 4011-abcd and 9401 and v1.401.2 and /api/401x") == []


@pytest.mark.parametrize("line", REAL)
def test_genuine_authentication_failures_are_found(line):
    assert m.auth_failure_lines(line) == [line]


def test_the_watch_passes_on_guids_and_fails_on_a_real_401(world):
    env, runner = world["env"], world["runner"]
    logs = {"text": GUID_LINE + "\n" + TIMESTAMP_LINE + "\n"}
    orig = runner._answer

    def answer(cmd, j, input_text):
        if cmd[:2] == ["docker", "logs"]:
            return m.Result(0, logs["text"], "")
        return orig(cmd, j, input_text)
    runner._answer = answer
    verdict, evidence = m._watch(env, 0, 60)
    assert verdict == "PASS" and "0 authentication-failure lines" in evidence
    logs["text"] += REAL[0] + "\n"
    verdict, evidence = m._watch(env, 0, 60)
    assert verdict == "FAIL" and "1 authentication-failure lines" in evidence and "OMAG-USER-SECURITY-401-001" in evidence



# ── report specs after the restart (BRIEF-CDO-SHEET-TABLE-2026-11-12 sec. 5) ────────────

def test_report_spec_sync_step_runs_after_heal_wait_and_the_index_is_read(world):
    assert m.STEPS.index("heal-wait") < m.STEPS.index("report-spec-sync") < m.STEPS.index("verify")
    assert "report-spec-sync" not in m.RUN_ONCE                 # only the Portal's cache: safe to repeat
    run_dir = _plan(world)
    assert m.apply(world["env"], str(run_dir)) == 0
    st = _state(run_dir)
    ev = st["steps"]["report-spec-sync"]["evidence"]
    assert ev == {"outcome": "synced", "finishedAt": "2099-01-01T00:00:00+00:00", "alreadyRunning": False,
                  "consumerIndex": "read", "consumers": 2, "specs": 7}
    assert ("POST", m.PORTAL_URL + "/api/report-specs/sync") in world["http"].calls
    checks = {c["check"]: c for c in st["steps"]["verify"]["evidence"]["checks"]}
    assert checks["report-spec consumer index"]["verdict"] == "PASS"
    assert "egeria-main started 2026-11-12T16:59:47" in checks["report-spec consumer index"]["evidence"]


def test_report_spec_sync_with_an_unread_index_fails_with_the_remedy(world):
    world["http"].sync.update(outcome="index_not_read", error="the consumer index was not read: root not found",
                              report={"consumers": {"status": "not read", "consumers": 0, "labels": 0}})
    run_dir = _plan(world)
    m.apply(world["env"], str(run_dir))
    step = _state(run_dir)["steps"]["report-spec-sync"]
    assert step["status"] == "failed" and "index_not_read" in step["error"]
    assert "POST /api/report-specs/sync on the Portal as an administrator" in step["error"]


def test_report_spec_sync_refused_needs_a_person(world):
    world["http"].sync_post = 403
    run_dir = _plan(world)
    m.apply(world["env"], str(run_dir))
    st = _state(run_dir)
    assert st["steps"]["report-spec-sync"]["status"] == "needs a person"
    assert st["steps"]["verify"]["status"] == "done"            # the run goes on


def _verdict(world, **sync):
    world["http"].sync.update(sync)
    return m.report_spec_index_verdict(world["env"])


def test_verify_index_read_after_the_start_passes(world):
    v, ev = _verdict(world)
    assert v == "PASS" and "read (2 consumer folders, 7 specs)" in ev


def test_verify_index_not_read_fails_with_the_remedy(world):
    v, ev = _verdict(world, report={"consumers": {"status": "not read", "reason": "root not visible"}})
    assert v == "FAIL" and "the consumer index is 'not read' (root not visible)" in ev
    assert "Remedy: re-sync report specs" in ev


def test_verify_index_read_before_the_restart_fails(world):
    v, ev = _verdict(world, finished_at="2026-11-12T16:00:00+00:00")
    assert v == "FAIL" and "read before quickstart-egeria-main last started" in ev and "Remedy" in ev


def test_verify_without_an_answer_is_not_measured(world, monkeypatch):
    v, ev = _verdict(world, report=None)
    assert v == "NOT MEASURED" and "says nothing about the consumer index" in ev
    orig = world["http"].request
    world["http"].request = lambda method, url, **k: (502, "bad gateway") if url.endswith("/sync") else orig(method, url, **k)
    v, ev = m.report_spec_index_verdict(world["env"])
    assert v == "NOT MEASURED" and "HTTP 502" in ev


def test_verify_check_is_read_only(world):
    world["http"].calls.clear()
    m.report_spec_index_verdict(world["env"])
    assert world["http"].calls == [("GET", m.PORTAL_URL + "/api/report-specs/sync")]


@pytest.mark.parametrize("raw,expected", [
    ("2026-11-12T16:59:47.123456789Z", "2026-11-12T16:59:47"), ("2026-11-12T16:59:47Z", "2026-11-12T16:59:47"),
    ("0001-01-01T00:00:00Z", None), ("", None), ("garbage", None)])
def test_docker_start_times(raw, expected):
    t = m._docker_time(raw)
    assert (m.iso(t)[:19] if t is not None else None) == expected



def test_report_spec_sync_records_a_run_it_did_not_start(world):
    world["http"].sync_post_body = {"started": False, "already_running": True}
    run_dir = _plan(world)
    assert m.apply(world["env"], str(run_dir)) == 0
    ev = _state(run_dir)["steps"]["report-spec-sync"]["evidence"]
    assert ev["alreadyRunning"] is True and ev["consumerIndex"] == "read"
