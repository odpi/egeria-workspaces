#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""egeria-upgrade-reset: upgrade the quickstart Egeria platform image and/or clear its metadata
store, as a resumable, checked procedure. HOST ONLY: it needs the Docker CLI and the shared
Postgres superuser (through `docker exec`), which no container, and never the Portal, has.

    egeria-upgrade-reset plan  [--digest sha256:... | --latest] [--no-clear]
    egeria-upgrade-reset apply --plan <reset dir or plan.json> [--dry-run] [--redo STEP]
    egeria-upgrade-reset status --plan <reset dir>
    egeria-upgrade-reset record --plan <reset dir>        # write the Portal's "last reset" row now
    egeria-upgrade-reset infra-check [--record] [--json] [--log FILE]   # shared-infra health; read-only

`plan` changes nothing. It reads the current state (pinned and target image digests, the running
container's image, the database size, Docker's free disk, the RE/EA writers, the secrets accounts)
and writes runtime-volumes/egeria-resets/<UTC>/plan.json and state.json. `apply` runs the steps in
order, records each as done/failed with its evidence in state.json, and stops at the first failure.
Run it again to resume at the first step that is not done. `apply` refuses when the state it finds
differs from the plan's (another image running, a container missing, a database of another size).

Run-once steps (backup, clear, secrets-sync) never repeat once done; repeating one takes
`--redo STEP` and typing the step's name. Two owner checkpoints: typing the database name before
the clear, and the persona sign-in checks in verify (the CLI never signs in as anyone).

Every check reports PASS / FAIL / NOT MEASURED with its evidence; nothing is reported as fine
because it could not be looked at. Lessons from the 2026-11-11 reset are encoded per step (see
each step's docstring). Standard library only (PyYAML is used for compose files when installed;
a small reader covers its absence).

`infra-check` (also run by verify) reports each shared-infra service as PASS / FAIL / WARN /
EXPECTED STOPPED / NOT MEASURED: running and healthy, restart policy as the yaml says, created from
this checkout's compose file. It only reads (`docker inspect`, `docker ps`, and kafka-get-offsets.sh
and stat inside the Kafka container; with a "prefect" entry in infra-health.json, the Prefect API's
health, pool and worker list); fixing a drift is a person's decision. With --log it emails on a change
of state, when INFRA_ALERT_EMAIL and INFRA_ALERT_SMTP_HOST are set (see alert_on_change).
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime as _dt
import difflib
import getpass
import gzip
import hashlib
import json
import os
import re
import shutil
import signal
import socket
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from typing import Any, Callable, Optional

# ── Defaults (quickstart) ─────────────────────────────────────────────────────

REPO = Path(__file__).resolve().parents[3]
QS = REPO / "compose-configs" / "egeria-quickstart"
RESET_SQL = REPO / "compose-configs" / "shared-infra" / "reset-egeria-db.sql"

PLATFORM_CONTAINER = "quickstart-egeria-main"
PLATFORM_SERVICE = "egeria-main"
PLATFORM_IMAGE = "egeria-quickstart-platform:local"
UPSTREAM_IMAGE = "docker.io/odpi/egeria-platform:latest"
PG_CONTAINER = "egeria-shared-postgres"
PG_PORT = "5442"
DATABASE = "egeria"
DEMO_DB = "coco_pharma"
PORTAL_URL = os.environ.get("EGERIA_RESET_PORTAL_URL", "http://127.0.0.1:8800")
EGERIA_URL = os.environ.get("EGERIA_RESET_EGERIA_URL", "https://localhost:9443")
VIEW_SERVER = os.environ.get("EGERIA_RESET_VIEW_SERVER", "qs-view-server")
WRITER_PORTS = {8813: "Resource Explorer", 8880: "Egeria Advisor"}
WRITER_PATTERNS = ("resource-explorer", "resource_explorer", "egeria-advisor", "egeria_advisor")
MIN_FREE_GB = 15
MONITOR_CYCLE_S = 600
DUMP_END_MARKER = "-- PostgreSQL database dump complete"
DB_NAME_RE = re.compile(r"^[a-z_][a-z0-9_]*$")

# Verify: what a healed quickstart holds (Part 1 batches; owner-approved counts).
FOLDER_WALKS = [
    ("DashboardFolder::Consumer::Portal", 5),
    ("DashboardFolder::Consumer::EgeriaAdvisor", 5),
    ("RootCollection::DashboardSheets", 2),
    ("ReportSpecFolder::Consumer::Portal", None),     # listed, no fixed count
]
# RE / EA are restarted ONLY through their own launcher scripts, which set the environment they need
# (a dozen EGERIA_* variables for RE, its venv and steps). Recorded argv is never replayed: it loses
# that environment, splits quoted arguments, and a bare `uv run --package` drops RE's survey steps.
# Override per port with EGERIA_RESET_LAUNCHER_<port> or `plan --launcher PORT=PATH`.
DEFAULT_LAUNCHERS = {8813: "~/.re-gate/start-8813.sh", 8880: "~/.re-gate/start-ea-8880.sh"}

# secrets-sync runs BEFORE recreate (read-back R-B1): the copy is host-side and in place, so the new
# container mounts the final files, and the only restart (a stale bind mount) happens in recreate,
# before Egeria is up and the Portal's heal can start. A restart mid-heal could half-run a batch that
# is not safe to re-run.
STEPS = ["disk-check", "repin", "build", "freeze-writers", "stop-platform", "backup", "clear",
         "secrets-sync", "recreate", "heal-wait", "unfreeze", "verify", "record"]
RUN_ONCE = {"backup", "clear", "secrets-sync"}
CLEAR_STEPS = {"backup", "clear"}       # left out by `plan --no-clear` (an image upgrade only)


class StepFailed(Exception):
    """A step's check failed; the message says which and why."""


class Refused(Exception):
    """apply will not run: the state differs from the plan, or a guard said no."""


# ── Seams (replaced in tests) ─────────────────────────────────────────────────

@dataclasses.dataclass
class Result:
    rc: int
    out: str = ""
    err: str = ""


class Runner:
    """Runs host commands. Tests pass a fake; nothing else in this module calls subprocess."""

    def run(self, cmd: list[str], *, input_text: Optional[str] = None, cwd: Optional[Path] = None,
            check: bool = True, timeout: Optional[float] = None) -> Result:
        p = subprocess.run(cmd, input=input_text, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        r = Result(p.returncode, p.stdout, p.stderr)
        if check and p.returncode != 0:
            raise StepFailed(f"{' '.join(cmd[:4])} … exited {p.returncode}: {p.stderr.strip()[-400:]}")
        return r

    def stream_gzip(self, cmd: list[str], dest: Path) -> int:
        """Run cmd, gzip its stdout into dest; return its exit code."""
        with gzip.open(dest, "wb") as gz:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert p.stdout is not None
            for chunk in iter(lambda: p.stdout.read(1 << 20), b""):
                gz.write(chunk)
            p.wait()
        return p.returncode

    def spawn(self, argv: list[str], cwd: str, log: Path) -> int:
        """Start a long-running process detached from this one; return its pid."""
        out = open(log, "ab")
        p = subprocess.Popen(argv, cwd=cwd, stdout=out, stderr=subprocess.STDOUT, start_new_session=True)
        return p.pid

    def kill(self, pid: int) -> None:
        os.kill(pid, signal.SIGTERM)


class Http:
    """GET/POST JSON. Self-signed localhost certificates are accepted (quickstart only)."""

    def __init__(self):
        self._ctx = ssl.create_default_context()
        self._ctx.check_hostname = False
        self._ctx.verify_mode = ssl.CERT_NONE

    def request(self, method: str, url: str, body: Any = None, headers: Optional[dict] = None,
                timeout: float = 30) -> tuple[int, Any]:
        data = None if body is None else (body if isinstance(body, (bytes, str)) else json.dumps(body))
        if isinstance(data, str):
            data = data.encode()
        req = urllib.request.Request(url, data=data, method=method,
                                     headers={"Content-Type": "application/json", **(headers or {})})
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=self._ctx) as r:
                text = r.read().decode("utf-8", "replace")
                status = r.status
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8", "replace")
        try:
            return status, json.loads(text)
        except ValueError:
            return status, text


@dataclasses.dataclass
class Env:
    runner: Runner
    http: Http
    ask: Callable[[str], str] = input
    say: Callable[[str], None] = print
    sleep: Callable[[float], None] = time.sleep
    now: Callable[[], float] = time.time
    port_open: Callable[[int], bool] = None  # type: ignore[assignment]
    repo: Path = REPO
    #: verify's persona-check answer given up front ("ok" or "skip": `apply --personas`, or
    #: EGERIA_RESET_PERSONAS), so a background run never waits on a prompt.
    personas: Optional[str] = None
    #: (host, port, security) -> an smtplib.SMTP-like object; infra-check's alert email. Tests pass a fake.
    smtp: Optional[Callable[[str, int, str], Any]] = None

    def __post_init__(self):
        if self.port_open is None:
            self.port_open = _port_open


def _port_open(port: int) -> bool:
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0


def utc_stamp(t: Optional[float] = None) -> str:
    return _dt.datetime.fromtimestamp(t if t is not None else time.time(), _dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def iso(t: float) -> str:
    return _dt.datetime.fromtimestamp(t, _dt.timezone.utc).isoformat(timespec="seconds")


# ── Small readers ─────────────────────────────────────────────────────────────

def dockerfile_path(repo: Path) -> Path:
    return repo / "compose-configs" / "egeria-quickstart" / "Dockerfile-egeria-platform"


_FROM_RE = re.compile(r"^(FROM\s+\S+?)@(sha256:[0-9a-f]{64})(.*)$", re.M)


def pinned_digest(dockerfile: Path) -> str:
    m = _FROM_RE.search(dockerfile.read_text())
    if not m:
        raise StepFailed(f"{dockerfile.name}: no FROM line pinned to a sha256 digest")
    return m.group(2)


def check_digest(d: str) -> str:
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", d or ""):
        raise Refused(f"not a sha256 digest: {d!r}")
    return d


def db_size_class(nbytes: Optional[int]) -> str:
    """Order of magnitude, so a plan stays valid while the database grows a little."""
    if nbytes is None:
        return "absent"
    for limit, label in ((10 ** 8, "<100MB"), (10 ** 9, "<1GB"), (10 ** 10, "<10GB"), (10 ** 11, "<100GB")):
        if nbytes < limit:
            return label
    return ">=100GB"


def psql(env: Env, sql: str, db: str = "postgres", check: bool = True) -> Result:
    return env.runner.run(["docker", "exec", PG_CONTAINER, "psql", "-h", "localhost", "-p", PG_PORT,
                           "-U", "postgres", "-d", db, "-v", "ON_ERROR_STOP=1", "-Atc", sql], check=check)


def db_size(env: Env, database: str) -> Optional[int]:
    r = psql(env, f"select pg_database_size(datname) from pg_database where datname = '{database}'")
    return int(r.out.strip()) if r.out.strip() else None


def docker_free_gb(env: Env) -> float:
    """Free space on the Docker VM's disk, read inside the running shared Postgres container
    (its root filesystem is an overlay on that disk). No new image is pulled."""
    out = env.runner.run(["docker", "exec", PG_CONTAINER, "df", "-Pk", "/"]).out.strip().splitlines()
    avail_kb = int(out[-1].split()[3])
    return round(avail_kb / 1024 / 1024, 1)


def compose_setup(env: Env, container: str = PLATFORM_CONTAINER) -> dict:
    """The running container's compose project, files and folder, from its labels, so the
    recreate uses exactly the compose setup that started it."""
    fmt = ('{{index .Config.Labels "com.docker.compose.project"}}|'
           '{{index .Config.Labels "com.docker.compose.project.config_files"}}|'
           '{{index .Config.Labels "com.docker.compose.project.working_dir"}}|{{.Image}}')
    proj, files, wd, image_id = env.runner.run(["docker", "inspect", container, "--format", fmt]).out.strip().split("|")
    if not proj or not files:
        raise StepFailed(f"{container} has no compose labels; it was not started by docker compose")
    return {"project": proj, "files": files.split(","), "workingDir": wd, "imageId": image_id}


def compose_cmd(setup: dict, *args: str) -> list[str]:
    cmd = ["docker", "compose", "-p", setup["project"]]
    for f in setup["files"]:
        cmd += ["-f", f]
    return cmd + list(args)


def image_id(env: Env, image: str) -> Optional[str]:
    r = env.runner.run(["docker", "image", "inspect", image, "--format", "{{.Id}}"], check=False)
    return r.out.strip() if r.rc == 0 and r.out.strip() else None


def resolve_latest(env: Env, image: str = UPSTREAM_IMAGE) -> str:
    r = env.runner.run(["docker", "buildx", "imagetools", "inspect", image, "--format", "{{json .Manifest}}"])
    return check_digest(json.loads(r.out)["digest"])


# ── Writers (RE / EA) ─────────────────────────────────────────────────────────

def _proc_table(env: Env) -> dict[int, tuple[int, str]]:
    out = env.runner.run(["ps", "-axo", "pid=,ppid=,command="]).out
    table = {}
    for line in out.splitlines():
        parts = line.strip().split(None, 2)
        if len(parts) == 3 and parts[0].isdigit():
            table[int(parts[0])] = (int(parts[1]), parts[2])
    return table


def _listener_pid(env: Env, port: int) -> Optional[int]:
    r = env.runner.run(["lsof", "-nP", f"-iTCP:{port}", "-sTCP:LISTEN", "-t"], check=False)
    pids = [int(x) for x in r.out.split() if x.strip().isdigit()]
    return pids[0] if pids else None


def _cwd(env: Env, pid: int) -> str:
    r = env.runner.run(["lsof", "-a", "-p", str(pid), "-d", "cwd", "-Fn"], check=False)
    for line in r.out.splitlines():
        if line.startswith("n"):
            return line[1:]
    return ""


def _is_writer(command: str) -> bool:
    return any(p in command for p in WRITER_PATTERNS)


def find_writers(env: Env) -> dict:
    """{known: [{port, name, pid, launcherPid, command, cwd}], unknown: [{pid, command}]}.
    The launcher is the topmost ancestor that is still an RE/EA command (for RE that is the
    `uv run … resource-explorer web` wrapper, so stopping it stops the child too). Any other
    RE/EA process on this host is unknown, and the procedure refuses to go on while one runs:
    it could write to Egeria during the clear (2026-11-11: check RE's other instances)."""
    procs = _proc_table(env)
    known, claimed = [], set()
    for port, name in WRITER_PORTS.items():
        pid = _listener_pid(env, port)
        if pid is None:
            continue
        top = pid
        while procs.get(top) and procs.get(procs[top][0]) and _is_writer(procs[procs[top][0]][1]):
            top = procs[top][0]
        tree = {pid, top}
        cur = pid
        while cur != top and cur in procs:
            cur = procs[cur][0]
            tree.add(cur)
        claimed |= tree
        cmd = procs.get(top, (0, ""))[1]
        known.append({"port": port, "name": name, "pid": pid, "launcherPid": top,
                      "command": cmd, "cwd": _cwd(env, top)})
    unknown = [{"pid": p, "command": c[:200]} for p, (pp, c) in procs.items()
               if _is_writer(c) and p not in claimed and pp not in claimed and "egeria-upgrade-reset" not in c
               and "grep" not in c]
    return {"known": known, "unknown": unknown}


def launchers(overrides: Optional[dict] = None) -> dict:
    """{port: {"path", "usable"}} for each writer port: --launcher, else EGERIA_RESET_LAUNCHER_<port>,
    else the default. `usable` means the file exists and is executable."""
    out = {}
    for port, default in DEFAULT_LAUNCHERS.items():
        raw = (overrides or {}).get(port) or os.environ.get(f"EGERIA_RESET_LAUNCHER_{port}") or default
        path = Path(os.path.expanduser(raw)) if raw else None
        out[str(port)] = {"path": str(path) if path else None,
                          "usable": bool(path and path.is_file() and os.access(path, os.X_OK))}
    return out


def classification_count(env: "Env") -> dict:
    """{count, serverReportsPurpose} from the Portal, or {notRead: reason}."""
    try:
        code, body = env.http.request("GET", f"{PORTAL_URL}/api/types/classification-purposes", timeout=120)
    except Exception as exc:  # noqa: BLE001
        return {"notRead": f"{type(exc).__name__}: {exc}"}
    if code != 200 or not isinstance(body, dict):
        return {"notRead": f"HTTP {code}"}
    return {"count": len(body.get("purposes") or {}), "serverReportsPurpose": body.get("serverReportsPurpose")}


# ── Secrets ───────────────────────────────────────────────────────────────────

def secret_accounts(path: Path) -> dict[str, str]:
    """{account name: fingerprint of its block} for an .omsecrets file. Only NAMES ever leave
    this function's callers; values are hashed, never printed (2026-11-11: a diff leaked one)."""
    accounts: dict[str, list[str]] = {}
    current = None
    in_users = False
    for line in path.read_text(errors="replace").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        if stripped == "users:":
            in_users, current = True, None
            continue
        if in_users and indent <= 4 and stripped.endswith(":") and stripped != "users:":
            in_users, current = False, None
        if in_users and indent == 6 and stripped.endswith(":"):
            current = stripped[:-1]
            accounts[current] = []
            continue
        if current is not None and indent > 6:
            accounts[current].append(stripped)
    return {k: hashlib.sha256("\n".join(v).encode()).hexdigest()[:12] for k, v in accounts.items()}


def secrets_diff(src_dir: Path, dst_dir: Path) -> dict:
    """Per file: accounts added / removed / changed, by name only."""
    out = {}
    for f in sorted(src_dir.glob("*.omsecrets")):
        new = secret_accounts(f)
        old = secret_accounts(dst_dir / f.name) if (dst_dir / f.name).exists() else {}
        out[f.name] = {"added": sorted(set(new) - set(old)), "removed": sorted(set(old) - set(new)),
                       "changed": sorted(k for k in set(new) & set(old) if new[k] != old[k]),
                       "accounts": len(new), "newFile": not (dst_dir / f.name).exists()}
    for f in sorted(dst_dir.glob("*")) if dst_dir.exists() else []:
        if f.is_file() and not (src_dir / f.name).exists():
            out[f.name] = {"extraFile": True}
    return out


def _names(names: list[str], limit: int = 12) -> str:
    if not names:
        return "-"
    return ", ".join(names) if len(names) <= limit else ", ".join(names[:limit]) + f" … (+{len(names) - limit} more)"


def secrets_line(d: dict) -> str:
    """One line per secrets file: account NAMES only, never values."""
    if d.get("extraFile"):
        return "kept as is (not in the compose secrets; never deleted)"
    if not d.get("accounts") and not d.get("removed"):
        return "no user accounts (copied as is)"
    return (f"{d['accounts']} accounts{' (new file)' if d.get('newFile') else ''}; added {_names(d['added'])}; "
            f"removed {_names(d['removed'])}; changed {_names(d['changed'])}")


# ── Plan ──────────────────────────────────────────────────────────────────────

def make_plan(env: Env, *, digest: Optional[str], latest: bool, clear: bool, reset_root: Optional[Path],
              allow_other_checkout: bool = False, launcher_overrides: Optional[dict] = None) -> Path:
    """Read everything; change nothing; write plan.json and state.json."""
    t = env.now()
    setup = compose_setup(env)
    # The DEPLOYMENT is the checkout the running container was started from (its compose
    # folder's repo), not wherever this script sits: the Dockerfile, the secrets and the logs
    # are that checkout's.
    deploy = Path(setup["workingDir"]).resolve().parents[1]
    env.say(f"Deployment (the running platform's compose folder): {setup['workingDir']}")
    env.say(f"This CLI's checkout:                                {env.repo}")
    if deploy != Path(env.repo).resolve() and not allow_other_checkout:
        raise Refused(f"the platform was started from {deploy}, but this CLI is in {env.repo}. Run the CLI from "
                      "the deployment's checkout, or pass --allow-other-checkout to mix them on purpose.")
    dfile = dockerfile_path(deploy)
    current = pinned_digest(dfile)
    target = check_digest(digest) if digest else (resolve_latest(env) if latest else current)
    size = db_size(env, DATABASE)
    free = docker_free_gb(env)
    writers = find_writers(env)
    src = deploy / "compose-configs" / "egeria-quickstart" / "secrets"
    dst = deploy / "runtime-volumes" / "quickstart-platform-data" / "secrets"
    steps = [s for s in STEPS if clear or s not in CLEAR_STEPS]
    blockers = []
    if free < MIN_FREE_GB:
        blockers.append(f"Docker has {free} GB free; at least {MIN_FREE_GB} GB is needed for the build")
    if writers["unknown"]:
        blockers.append("unknown RE/EA processes are running: " +
                        "; ".join(f"pid {w['pid']}: {w['command']}" for w in writers["unknown"]))
    plan = {
        "createdAt": iso(t), "createdBy": getpass.getuser(), "host": socket.gethostname(),
        "repo": str(env.repo), "deployRoot": str(deploy), "database": DATABASE, "clear": clear, "steps": steps,
        "image": {"dockerfile": str(dfile), "currentDigest": current, "targetDigest": target,
                  "repin": target != current, "runningImageId": setup["imageId"]},
        "compose": setup, "databaseBytes": size, "databaseSizeClass": db_size_class(size),
        "dockerFreeGb": free,
        "writers": writers,
        "launchers": launchers(launcher_overrides),
        "classificationTypes": classification_count(env),
        "allowOtherCheckout": allow_other_checkout,
        "secrets": {"from": str(src), "to": str(dst), "diff": secrets_diff(src, dst)},
        "backup": {"to": None},
        "blockers": blockers,
    }
    run_dir = (reset_root or deploy / "runtime-volumes" / "egeria-resets") / utc_stamp(t)
    run_dir.mkdir(parents=True, exist_ok=False)
    if clear:
        plan["backup"]["to"] = str(run_dir / f"{DATABASE}-{utc_stamp(t)}.sql.gz")
    write_json(run_dir / "plan.json", plan)
    write_json(run_dir / "state.json", {"steps": {s: {"status": "pending"} for s in steps}})
    print_plan(env, plan, run_dir)
    return run_dir


def print_plan(env: Env, plan: dict, run_dir: Path) -> None:
    say = env.say
    img = plan["image"]
    say(f"Plan written to {run_dir}/plan.json")
    say(f"  image   {img['currentDigest']}  ->  {img['targetDigest']}"
        f"{'' if img['repin'] else '  (unchanged: rebuild only)'}")
    say(f"  running image id {img['runningImageId']}")
    say(f"  database '{plan['database']}': {plan['databaseBytes']} bytes ({plan['databaseSizeClass']})"
        + ("" if plan["clear"] else "  -- NOT cleared (--no-clear)"))
    if plan["clear"]:
        say(f"  backup  -> {plan['backup']['to']}")
    say(f"  Docker free disk {plan['dockerFreeGb']} GB (need >= {MIN_FREE_GB})")
    for w in plan["writers"]["known"]:
        ln = plan["launchers"].get(str(w["port"])) or {}
        say(f"  writer  {w['name']} on {w['port']}: pid {w['launcherPid']}: {w['command'][:100]}")
        say(f"          restarted by {ln.get('path')}" if ln.get("usable") else
            f"          NO usable launcher ({ln.get('path')}): it will NOT be restarted automatically; a person must")
    ct = plan["classificationTypes"]
    say(f"  classification types {ct['count']} (serverReportsPurpose={ct.get('serverReportsPurpose')})"
        if "count" in ct else f"  classification types not read: {ct['notRead']} (verify will say NOT MEASURED)")
    for f, d in plan["secrets"]["diff"].items():
        say(f"  secrets {f}: {secrets_line(d)}")
    say("  steps   " + ", ".join(plan["steps"]))
    for b in plan["blockers"]:
        say(f"  BLOCKER {b}")
    say("Nothing has been changed. Run: egeria-upgrade-reset apply --plan " + str(run_dir))


# ── State ─────────────────────────────────────────────────────────────────────

def write_json(path: Path, data: Any) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, default=str))
    os.replace(tmp, path)


def load_run(plan_arg: str) -> tuple[Path, dict, dict]:
    p = Path(plan_arg)
    run_dir = p.parent if p.is_file() else p
    plan = json.loads((run_dir / "plan.json").read_text())
    state = json.loads((run_dir / "state.json").read_text())
    return run_dir, plan, state


def done(state: dict, step: str) -> bool:
    return state["steps"].get(step, {}).get("status") == "done"


def check_still_matches(env: Env, plan: dict, state: dict) -> None:
    """Refuse when what apply finds differs from what the plan read."""
    if plan.get("blockers"):
        raise Refused("the plan has blockers: " + "; ".join(plan["blockers"]) + ". Make a new plan once they are cleared.")
    if not done(state, "recreate"):
        setup = compose_setup(env)
        if setup["imageId"] != plan["image"]["runningImageId"]:
            raise Refused(f"{PLATFORM_CONTAINER} now runs image {setup['imageId']}, the plan read "
                          f"{plan['image']['runningImageId']}. Make a new plan.")
    for c in (PG_CONTAINER,):
        if env.runner.run(["docker", "inspect", c, "--format", "{{.State.Running}}"], check=False).out.strip() != "true":
            raise Refused(f"{c} is not running")
    if plan["clear"] and not done(state, "clear"):
        cls = db_size_class(db_size(env, plan["database"]))
        if cls != plan["databaseSizeClass"]:
            raise Refused(f"database '{plan['database']}' is now {cls}, the plan read {plan['databaseSizeClass']}. "
                          "Make a new plan.")
    deploy = Path(plan.get("deployRoot") or env.repo).resolve()
    if deploy != Path(env.repo).resolve() and not plan.get("allowOtherCheckout"):
        raise Refused(f"the plan's deployment is {deploy}, but this CLI is in {env.repo} (plan without --allow-other-checkout)")
    current = pinned_digest(Path(plan["image"]["dockerfile"]))
    if current not in (plan["image"]["currentDigest"], plan["image"]["targetDigest"]):
        raise Refused(f"the Dockerfile is pinned to {current}, neither the plan's current nor target digest")


# ── Steps ─────────────────────────────────────────────────────────────────────

def step_disk_check(env, plan, state, run_dir):
    """Refuse below MIN_FREE_GB free on the Docker VM (2026-11-04: a build filled it, Postgres stopped writing)."""
    free = docker_free_gb(env)
    if free < MIN_FREE_GB:
        raise StepFailed(f"Docker has {free} GB free; {MIN_FREE_GB} GB is the minimum. Try `docker builder prune`.")
    return {"freeGb": free}


def step_repin(env, plan, state, run_dir):
    """Pin Dockerfile-egeria-platform's FROM line to the target digest, and show the diff."""
    path = Path(plan["image"]["dockerfile"])
    old_text = path.read_text()
    target = plan["image"]["targetDigest"]
    new_text = _FROM_RE.sub(lambda m: f"{m.group(1)}@{target}{m.group(3)}", old_text, count=1)
    diff = "".join(difflib.unified_diff(old_text.splitlines(True), new_text.splitlines(True),
                                        str(path.name), str(path.name)))
    if new_text != old_text:
        path.write_text(new_text)
        env.say(diff)
    return {"from": plan["image"]["currentDigest"], "to": target, "changed": new_text != old_text,
            "diff": diff or "(already pinned)"}


def step_build(env, plan, state, run_dir):
    """Keep the current image as a rollback tag, then build the platform image from the pin."""
    rollback = f"egeria-quickstart-platform:rollback-{run_dir.name.lower()}"
    old = image_id(env, PLATFORM_IMAGE)
    if old:
        env.runner.run(["docker", "tag", PLATFORM_IMAGE, rollback])
    env.runner.run(compose_cmd(plan["compose"], "build", "--pull", PLATFORM_SERVICE),
                   cwd=Path(plan["compose"]["workingDir"]), timeout=3600)
    new = image_id(env, PLATFORM_IMAGE)
    if not new:
        raise StepFailed(f"the build finished but {PLATFORM_IMAGE} does not exist")
    return {"rollbackTag": rollback if old else None, "previousImageId": old, "builtImageId": new,
            "baseDigest": plan["image"]["targetDigest"]}


def step_freeze_writers(env, plan, state, run_dir):
    """Stop RE (8813) and EA (8880) so nothing writes to Egeria while it is cleared (owner:
    "Yes, with RE (Recommended)"). Refuse if any other RE/EA process runs. Part 3 adds a
    maintenance mode; until then the processes are stopped and restarted by unfreeze."""
    w = find_writers(env)
    if w["unknown"]:
        raise StepFailed("unknown RE/EA processes are running, stop them first: " +
                         "; ".join(f"pid {u['pid']}: {u['command']}" for u in w["unknown"]))
    stopped = []
    for k in w["known"]:
        env.runner.kill(k["launcherPid"])
        deadline = env.now() + 60
        while env.port_open(k["port"]) and env.now() < deadline:
            env.sleep(2)
        if env.port_open(k["port"]):
            raise StepFailed(f"{k['name']} still listens on {k['port']} 60 s after SIGTERM to pid {k['launcherPid']}")
        stopped.append(k)
    note = None if stopped else "no RE/EA writer was running"
    return {"stopped": stopped, "monitorPause": "not available: the Portal's bootstrap monitor has no pause; "
            "while Egeria is down its canary checks cannot reach it and never heal", "note": note}


def step_stop_platform(env, plan, state, run_dir):
    """Stop the platform container (it is recreated, never restarted, later)."""
    env.runner.run(["docker", "stop", PLATFORM_CONTAINER], timeout=300)
    running = env.runner.run(["docker", "inspect", PLATFORM_CONTAINER, "--format", "{{.State.Running}}"]).out.strip()
    if running != "false":
        raise StepFailed(f"{PLATFORM_CONTAINER} still running after docker stop")
    return {"stopped": PLATFORM_CONTAINER}


def verify_dump(path: Path) -> dict:
    """gzip -t equivalent, the end marker, size and sha256. Raises StepFailed on any problem."""
    h = hashlib.sha256()
    last = b""
    try:
        with gzip.open(path, "rb") as gz:
            for chunk in iter(lambda: gz.read(1 << 20), b""):
                last = (last + chunk)[-4096:]
    except (OSError, EOFError) as exc:
        raise StepFailed(f"{path.name} is not a complete gzip file ({type(exc).__name__}: {exc})")
    if DUMP_END_MARKER.encode() not in last:
        raise StepFailed(f"{path.name} has no '{DUMP_END_MARKER}' line at its end: the dump is truncated")
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return {"file": str(path), "bytes": path.stat().st_size, "sha256": h.hexdigest(), "gzipTest": "ok",
            "endMarker": "found"}


def step_backup(env, plan, state, run_dir):
    """pg_dump | gzip, then gzip -t, the end marker and sha256. Nothing goes on if a check fails."""
    dest = Path(plan["backup"]["to"])
    rc = env.runner.stream_gzip(["docker", "exec", PG_CONTAINER, "pg_dump", "-h", "localhost", "-p", PG_PORT,
                                 "-U", "postgres", plan["database"]], dest)
    if rc != 0:
        raise StepFailed(f"pg_dump exited {rc}")
    return verify_dump(dest)


def step_clear(env, plan, state, run_dir):
    """Owner checkpoint: type the database name. Then the shared reset SQL (reset-egeria-db.sql):
    DROP … WITH (FORCE), CREATE, GRANT. Never `docker start` afterwards (that is the old-image trap)."""
    db = plan["database"]
    if not DB_NAME_RE.match(db) or db == "postgres" or db.startswith("template"):
        raise StepFailed(f"refusing database name {db!r}")
    if not done(state, "backup"):
        raise StepFailed("no verified backup: the backup step is not done")
    answer = env.ask(f"Type the database name ({db}) to DROP and recreate it: ").strip()
    if answer != db:
        raise StepFailed(f"checkpoint not passed (typed {answer!r}); nothing was dropped")
    env.runner.run(["docker", "exec", "-i", PG_CONTAINER, "psql", "-h", "localhost", "-p", PG_PORT, "-U", "postgres",
                    "-v", "ON_ERROR_STOP=1", "-v", f"db={db}", "-f", "-"],
                   input_text=(env.repo / "compose-configs" / "shared-infra" / "reset-egeria-db.sql").read_text())
    size = db_size(env, db)
    return {"database": db, "recreatedBytes": size, "sql": "compose-configs/shared-infra/reset-egeria-db.sql"}


def step_recreate(env, plan, state, run_dir):
    """`compose up -d --no-deps --force-recreate egeria-main`, never `docker start` (2026-11-11:
    reset-egeria-db.sh restarted the old container, which kept the OLD image). Then the running
    container's image must be the one build made, and its /deployments/secrets must match the host
    (one restart if the bind mount is stale, while Egeria is still starting)."""
    built = state["steps"].get("build", {}).get("evidence", {}).get("builtImageId")
    env.runner.run(compose_cmd(plan["compose"], "up", "-d", "--no-deps", "--force-recreate", PLATFORM_SERVICE),
                   cwd=Path(plan["compose"]["workingDir"]), timeout=600)
    running = compose_setup(env)["imageId"]
    if built and running != built:
        raise StepFailed(f"{PLATFORM_CONTAINER} runs {running}, not the image build made ({built})")
    # The stale-mount check, at once: Egeria is still starting, so the Portal's heal cannot have begun,
    # and the one restart it may need cannot interrupt a batch (read-back R-B1).
    host = _host_sizes(Path(plan["secrets"]["to"]))
    restarted = False
    seen = _container_sizes(env)
    if seen != host:
        env.runner.run(["docker", "restart", PLATFORM_CONTAINER], timeout=300)
        restarted = True
        seen = _container_sizes(env)
        if seen != host:
            raise StepFailed(f"after one restart the container still sees {seen} in /deployments/secrets; "
                             f"the host has {host}")
    return {"runningImageId": running, "matchesBuild": running == built if built else None,
            "recreatedAt": iso(env.now()), "secretsMountMatches": True, "restartedForStaleMount": restarted}


def step_secrets_sync(env, plan, state, run_dir):
    """Copy the compose secrets into runtime-volumes IN PLACE, while the platform is stopped, so the
    recreated container mounts the final files. Accounts added/removed/changed are listed by NAME only;
    files not in the compose secrets are KEPT (laz holds resource-explorer.omsecrets there). The
    container's view is checked in recreate, before Egeria is up (read-back R-B1)."""
    src, dst = Path(plan["secrets"]["from"]), Path(plan["secrets"]["to"])
    diff = secrets_diff(src, dst)
    dst.mkdir(parents=True, exist_ok=True)
    for f in src.glob("*.omsecrets"):
        shutil.copyfile(f, dst / f.name)    # truncates and rewrites the same inode: the bind mount stays valid
    for name, d in diff.items():
        env.say(f"  secrets {name}: {secrets_line(d)}")
    ev = {"diff": diff, "hostFiles": sorted(f.name for f in dst.iterdir() if f.is_file())}
    if done(state, "recreate"):
        # A redo after the recreate: Egeria may be healing, so no restart here. Check and report.
        seen, host = _container_sizes(env), _host_sizes(dst)
        if seen != host:
            raise StepFailed(f"the running container sees {seen}, the host has {host}; restart "
                             f"{PLATFORM_CONTAINER} only when no heal is running")
        ev["containerMatches"] = True
    return ev


def _host_sizes(dst: Path) -> dict:
    return {f.name: f.stat().st_size for f in dst.iterdir() if f.is_file()}


def _container_sizes(env: Env) -> dict:
    r = env.runner.run(["docker", "exec", PLATFORM_CONTAINER, "sh", "-c",
                        "for f in /deployments/secrets/*; do [ -f \"$f\" ] && echo \"$(wc -c < \"$f\") $(basename \"$f\")\"; done"],
                       check=False)
    out = {}
    for line in r.out.splitlines():
        parts = line.strip().split(None, 1)
        if len(parts) == 2 and parts[0].isdigit():
            out[parts[1]] = int(parts[0])
    return out


def portal_status(env: Env) -> tuple[Optional[dict], Optional[str]]:
    try:
        code, body = env.http.request("GET", f"{PORTAL_URL}/api/bootstrap/status", timeout=15)
    except Exception as exc:  # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"
    if code != 200 or not isinstance(body, dict):
        return None, f"HTTP {code}"
    return body, None


def step_heal_wait(env, plan, state, run_dir, *, timeout_s: float = 3 * 3600, poll_s: float = 30):
    """Wait for the Portal's heal: reinitializing false, and a check pass that STARTED at least one
    full monitor cycle (600 s) after the last heal ended, so `present` is not a stale read. Then the
    rotated Portal logs are read for errors since the recreate."""
    start = env.now()
    last_heal_end = state["steps"].get("recreate", {}).get("finishedAt") or start
    last_heal_end = last_heal_end if isinstance(last_heal_end, (int, float)) else start
    while True:
        st, err = portal_status(env)
        if st is not None:
            for fam in (st.get("families") or {}).values():
                t = _parse_iso(fam.get("lastHealedAt"))
                if t:
                    last_heal_end = max(last_heal_end, t)
            checked = _parse_iso(st.get("lastCheckAt"))
            if not st.get("reinitializing") and checked and checked >= last_heal_end + MONITOR_CYCLE_S:
                break
        if env.now() - start > timeout_s:
            raise StepFailed(f"the heal did not settle within {timeout_s / 3600:.1f} h"
                             + (f" (status not read: {err})" if err else ""))
        env.sleep(poll_s)
    fams = st.get("families") or {}
    missing = sorted(n for n, f in fams.items() if f.get("present") is False)
    result = {n: {"present": f.get("present"), "lastHealResult": f.get("lastHealResult"),
                  "manualSteps": f.get("manualSteps")} for n, f in fams.items()}
    errors = scan_logs(env, since=state["steps"].get("recreate", {}).get("finishedAt") or start,
                       root=Path(plan.get("deployRoot") or env.repo))
    ev = {"families": result, "missing": missing, "logErrors": errors[:50], "logErrorCount": len(errors),
          "settledAt": iso(env.now())}
    if missing:
        raise StepFailed("canaries still missing after the heal: " + ", ".join(missing))
    return ev


def _parse_iso(v) -> Optional[float]:
    if not v:
        return None
    try:
        return _dt.datetime.fromisoformat(str(v).replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def scan_logs(env: Env, since: float, root: Path) -> list[str]:
    """ERROR lines from the Portal's pyegeria.log and its rotated zips written since `since`."""
    logs = root / "compose-configs" / "egeria-quickstart" / "PyegeriaWebHandler" / "logs"
    lines: list[str] = []
    if not logs.is_dir():
        return [f"NOT MEASURED: no log folder at {logs}"]
    for f in sorted(logs.glob("pyegeria*.log*")):
        if f.stat().st_mtime < since:
            continue
        if f.suffix == ".zip":
            with zipfile.ZipFile(f) as z:
                for n in z.namelist():
                    text = z.read(n).decode("utf-8", "replace")
                    lines += [f"{f.name}: {l}" for l in text.splitlines() if " ERROR " in l or "| ERROR |" in l]
        else:
            lines += [f"{f.name}: {l}" for l in f.read_text(errors="replace").splitlines()
                      if " ERROR " in l or "| ERROR |" in l]
    return lines


class NeedsPerson(Exception):
    """The step did what it could; a person must finish it. Recorded as `needs a person`; the run goes on."""

    def __init__(self, message: str, evidence: dict):
        super().__init__(message)
        self.evidence = evidence


def step_unfreeze(env, plan, state, run_dir):
    """Restart RE and EA through their configured launcher scripts (never by replaying their command
    line), then print the RE recovery step. A writer with no usable launcher is left for a person."""
    stopped = state["steps"].get("freeze-writers", {}).get("evidence", {}).get("stopped", [])
    started, manual = [], []
    for k in stopped:
        if env.port_open(k["port"]):
            started.append({"name": k["name"], "port": k["port"], "restarted": "already running"})
            continue
        ln = (plan.get("launchers") or {}).get(str(k["port"])) or {}
        path = ln.get("path")
        if not (path and Path(path).is_file() and os.access(path, os.X_OK)):
            manual.append({"name": k["name"], "port": k["port"], "launcher": path,
                           "command": k.get("command"), "cwd": k.get("cwd")})
            env.say(f"  {k['name']} ({k['port']}) NOT restarted: no usable launcher ({path}). It ran as:\n"
                    f"    cd {k.get('cwd')} && {k.get('command')}")
            continue
        log = run_dir / f"{k['name'].replace(' ', '-').lower()}.log"
        pid = env.runner.spawn([path], str(Path(path).parent), log)
        deadline = env.now() + 120
        while not env.port_open(k["port"]) and env.now() < deadline:
            env.sleep(3)
        if not env.port_open(k["port"]):
            raise StepFailed(f"{k['name']} did not listen on {k['port']} within 120 s ({path}, pid {pid}, log {log})")
        started.append({"name": k["name"], "port": k["port"], "pid": pid, "launcher": path, "log": str(log)})
    nxt = (f"resource-explorer registry recover-after-egeria-reset --reset-at {iso(_reset_time(plan, state))}  "
           "(Part 3; until it exists, follow trellis docs/egeria-operations.md §8.1)")
    env.say("Next, RE recovery: " + nxt)
    ev = {"started": started, "needsPerson": manual, "next": nxt}
    if manual:
        raise NeedsPerson("restart by hand: " + ", ".join(f"{m['name']} ({m['port']})" for m in manual), ev)
    return ev


def _reset_time(plan, state) -> float:
    t = state["steps"].get("clear", {}).get("finishedAt") or state["steps"].get("recreate", {}).get("finishedAt")
    return t if isinstance(t, (int, float)) else time.time()


# ── Verify ───────────────────────────────────────────────────────────────────

class Egeria:
    """Read-only Egeria lookups from the host, as the service account."""

    def __init__(self, env: Env, user: str, password: str):
        self.env, self.user, self.password, self.token = env, user, password, None

    def _token(self) -> str:
        if not self.token:
            code, body = self.env.http.request("POST", f"{EGERIA_URL}/servers/{VIEW_SERVER}/api/token",
                                               {"userId": self.user, "password": self.password})
            if code != 200 or not isinstance(body, str) or not body.strip():
                raise StepFailed(f"Egeria token: HTTP {code}")
            self.token = body.strip()
        return self.token

    def find(self, type_name: str, prop: str, value: str, page: int = 2) -> list:
        body = {"class": "FindRequestBody", "metadataElementTypeName": type_name,
                "searchProperties": {"class": "SearchProperties", "matchCriteria": "ALL", "conditions": [
                    {"property": prop, "operator": "EQ",
                     "value": {"class": "PrimitiveTypePropertyValue", "typeName": "string", "primitiveValue": value}}]},
                "limitResultsByStatus": ["ACTIVE"], "graphQueryDepth": 0, "startFrom": 0, "pageSize": page}
        code, resp = self.env.http.request(
            "POST", f"{EGERIA_URL}/servers/{VIEW_SERVER}/api/open-metadata/metadata-expert/metadata-elements/by-search-conditions",
            body, headers={"Authorization": f"Bearer {self._token()}"})
        if code != 200 or not isinstance(resp, dict):
            raise StepFailed(f"find {type_name} {value!r}: HTTP {code}")
        # OpenMetadataElementsResponse: {"elements": [{"elementGUID", "elementProperties", ...}]}
        # (checked on laz, 2026-11-12). No "elements" key means none found.
        return resp.get("elements") or []

    def members(self, guid: str, page: int = 200) -> list:
        code, resp = self.env.http.request(
            "POST", f"{EGERIA_URL}/servers/{VIEW_SERVER}/api/open-metadata/collection-manager/collections/{guid}/members",
            {"class": "ResultsRequestBody", "startFrom": 0, "pageSize": page},
            headers={"Authorization": f"Bearer {self._token()}"})
        if code != 200 or not isinstance(resp, dict):
            raise StepFailed(f"members of {guid}: HTTP {code}")
        # {"elements": [{"elementHeader", "properties": {"qualifiedName", ...}, ...}]} (laz, 2026-11-12)
        return resp.get("elements") or []


def _check(name: str, fn: Callable[[], tuple[str, str]]) -> dict:
    try:
        verdict, evidence = fn()
    except Exception as exc:  # noqa: BLE001
        verdict, evidence = "NOT MEASURED", f"{type(exc).__name__}: {exc}"
    return {"check": name, "verdict": verdict, "evidence": evidence}


def step_verify(env, plan, state, run_dir, *, watch_s: float = 600, watch_every_s: float = 60):
    """Read-only checks, each PASS / FAIL / NOT MEASURED with evidence."""
    status, err = portal_status(env)
    fams = (status or {}).get("families") or {}
    eg = Egeria(env, os.environ.get("EGERIA_USER", "erinoverview"), os.environ.get("EGERIA_USER_PASSWORD", "secret"))
    checks = []

    canaries, source = _canaries(env)
    env.say(f"  canaries from {source}")
    for bid, canary in canaries:
        def one(c=canary):
            els = eg.find(c["type"], "displayName", c["name"], page=3)
            n = len(els)
            return ("PASS" if n == 1 else "FAIL", f"{c['type']} '{c['name']}': {n} found (want exactly 1)")
        checks.append(_check(f"canary {bid}", one))

    for qn, want in FOLDER_WALKS:
        def walk(q=qn, w=want):
            found = eg.find("Collection", "qualifiedName", q, page=3)
            if len(found) != 1:
                return "FAIL", f"{q}: {len(found)} collections with that name (want 1)"
            guid = found[0].get("elementGUID") or (found[0].get("elementHeader") or {}).get("guid")
            mem = eg.members(guid)
            names = sorted(((m.get("properties") or {}).get("qualifiedName") or "?") for m in mem)
            dup = sorted({n for n in names if names.count(n) > 1})
            if w is None:
                return ("FAIL" if dup else "PASS"), f"{q}: {len(mem)} members {names}" + (f"; duplicated {dup}" if dup else "")
            ok = len(mem) == w and not dup
            return ("PASS" if ok else "FAIL"), f"{q}: {len(mem)} members (want {w})" + (f"; duplicated {dup}" if dup else "")
        checks.append(_check(f"folder {qn}", walk))

    def sq():
        if status is None:
            return "NOT MEASURED", f"bootstrap status not read: {err}"
        steps = [s for f in fams.values() for s in (f.get("manualSteps") or []) if s.get("id") == "saved-query-first-refresh"]
        if not steps:
            return "NOT MEASURED", "no saved-query manual step in the bootstrap status"
        s = steps[0]
        return ("PASS" if s["state"] == "done" else ("FAIL" if s["state"] == "pending" else "NOT MEASURED")), \
            f"{s['state']}: {s.get('detail')}"
    checks.append(_check("saved-query tile", sq))

    checks.append(_check("classification purposes", lambda: classification_verdict(plan, classification_count(env))))

    checks.append(persona_check(env))

    try:
        infra = infra_check(env, Path(plan.get("deployRoot") or env.repo))
        checks += infra_verify_checks(infra)
    except Exception as exc:  # noqa: BLE001
        checks.append({"check": "infra (shared-infra compose)", "verdict": "NOT MEASURED",
                       "evidence": f"{type(exc).__name__}: {exc}"})

    checks.append(_check("connections and 401s", lambda: _watch(env, watch_s, watch_every_s)))
    failed = [c["check"] for c in checks if c["verdict"] == "FAIL"]
    for c in checks:
        env.say(f"  {c['verdict']:<12} {c['check']}: {c['evidence']}")
    return {"checks": checks, "failed": failed, "notMeasured": [c["check"] for c in checks if c["verdict"] == "NOT MEASURED"],
            "warnings": [c["check"] for c in checks if c["verdict"] in ("WARN", "EXPECTED STOPPED")]}


def classification_verdict(plan: dict, now: dict) -> tuple[str, str]:
    """Compare the count with the plan's baseline (read-back R-B3): equal PASS; changed with a new image
    CHANGED (reported for review, not a failure); fewer, or changed on the same image, FAIL; unreadable
    NOT MEASURED. Purposes no longer reported is a FAIL."""
    base = plan.get("classificationTypes") or {"notRead": "no baseline in the plan"}
    if "count" not in now:
        return "NOT MEASURED", f"not read now: {now.get('notRead')}"
    if "count" not in base:
        return "NOT MEASURED", f"{now['count']} types now; no baseline ({base.get('notRead')})"
    a, b = base["count"], now["count"]
    if base.get("serverReportsPurpose") and not now.get("serverReportsPurpose"):
        return "FAIL", f"{b} types, but the server no longer reports purposes (it did: {a})"
    if a == b:
        return "PASS", f"{b} classification types, as before"
    new_image = plan["image"]["targetDigest"] != plan["image"]["currentDigest"]
    if b < a:
        return "FAIL", f"{a}→{b}: fewer classification types"
    if new_image:
        return "CHANGED", f"CHANGED {a}→{b} (new image): review"
    return "FAIL", f"{a}→{b} on the same image"


def _canaries(env: Env) -> tuple[list[tuple[str, dict]], str]:
    """The canary of every batch ENABLED on this Portal (its saved selection wins over a
    manifest's defaultEnabled), from /api/bootstrap/batches; if the Portal cannot be read, every
    enabled-by-default batch's canary from the manifests in this checkout, and the source says so."""
    try:
        code, body = env.http.request("GET", f"{PORTAL_URL}/api/bootstrap/batches", timeout=30)
        if code == 200 and isinstance(body, (list, dict)):
            items = body if isinstance(body, list) else (body.get("batches") or [])
            got = [(b["id"], b["canary"]) for b in items
                   if b.get("enabled") and isinstance(b.get("canary"), dict) and b["canary"].get("name")]
            return got, "the Portal's enabled batches (/api/bootstrap/batches)"
    except Exception:  # noqa: BLE001
        pass
    return _manifest_canaries(env), "the manifests' defaultEnabled (the Portal could not be read)"


def _manifest_canaries(env: Env) -> list[tuple[str, dict]]:
    inbox = env.repo / "exchange-quickstart" / "loading-bay" / "dr-egeria-inbox"
    extra = env.repo / "compose-configs" / "egeria-quickstart" / "PyegeriaWebHandler"
    out = []
    for m in sorted(list(inbox.glob("*/_batch.json")) + [extra / "_batch.json", extra / "egeria-held-specs" / "_batch.json",
                                                         extra / "report-spec-valid-values" / "_batch.json"]):
        if not m.exists():
            continue
        d = json.loads(m.read_text())
        if d.get("defaultEnabled") and isinstance(d.get("canary"), dict):
            out.append((m.parent.name, d["canary"]))
    return out


PERSONA_PROMPT = ("Persona checks (the CLI never signs in): sign in to the Portal as each demo persona you use "
                  "and open a sheet. Type 'ok' when they all work, 'skip' to leave them unchecked, or describe the "
                  "failure: ")
PERSONA_ANSWERS = ("ok", "skip")


def persona_check(env: Env) -> dict:
    """The persona sign-in checkpoint. The answer given up front (`apply --personas ok|skip`, or
    EGERIA_RESET_PERSONAS) wins; otherwise the operator is asked. With no terminal to ask (a background
    run) and no answer given, or when the prompt hits end of input, it is NOT MEASURED: never a crash,
    and never PASS."""
    given = (env.personas or os.environ.get("EGERIA_RESET_PERSONAS") or "").strip().lower()
    if given:
        if given not in PERSONA_ANSWERS:
            return {"check": "persona sign-ins", "verdict": "NOT MEASURED",
                    "evidence": f"the up-front answer {given!r} is not one of {', '.join(PERSONA_ANSWERS)}"}
        return {"check": "persona sign-ins", "verdict": "PASS" if given == "ok" else "NOT MEASURED",
                "evidence": f"answered up front: {given}"}
    if env.ask is input and not sys.stdin.isatty():
        return {"check": "persona sign-ins", "verdict": "NOT MEASURED",
                "evidence": "no terminal to ask and no --personas answer (a background run)"}
    try:
        answer = env.ask(PERSONA_PROMPT).strip()
    except (EOFError, OSError) as exc:
        return {"check": "persona sign-ins", "verdict": "NOT MEASURED",
                "evidence": f"could not ask ({type(exc).__name__}: end of input); pass --personas ok|skip"}
    return {"check": "persona sign-ins", "verdict": "PASS" if answer.lower() == "ok" else
            ("NOT MEASURED" if answer.lower() in ("", "skip") else "FAIL"),
            "evidence": f"operator said: {answer or '(nothing)'}"}


#: A genuine authentication failure in the platform log: UNAUTHORIZED / NOT_AUTHORIZED, an Egeria message
#: code -401-NNN, or 401 as a number of its own (an HTTP status). Never "401" inside a GUID (engine action
#: aee401cf-..., 2026-11-12) or other hex, nor a timestamp's milliseconds (12:00:00.401).
AUTH_FAILURE = re.compile(r"UNAUTHORIZED|NOT_AUTHORIZED|-401-\d{3}(?!\d)|(?<![\w.:/-])401(?![\w-])", re.I)


def auth_failure_lines(text: str) -> list[str]:
    return [l for l in text.splitlines() if AUTH_FAILURE.search(l)]


def _watch(env: Env, total_s: float, every_s: float) -> tuple[str, str]:
    """PG connections on the egeria DB (the leak pattern: idle in transaction climbing) and
    UNAUTHORIZED/401 lines in the platform log, sampled every `every_s` for `total_s`."""
    since = iso(env.now())
    samples = []
    t_end = env.now() + total_s
    while True:
        r = psql(env, "select coalesce(state,'none')||'='||count(*) from pg_stat_activity "
                      f"where datname = '{DATABASE}' group by state order by 1", check=False)
        samples.append(dict(x.split("=", 1) for x in r.out.split() if "=" in x))
        if env.now() >= t_end:
            break
        env.sleep(every_s)
    logs = env.runner.run(["docker", "logs", "--since", since, PLATFORM_CONTAINER], check=False)
    hits = auth_failure_lines(logs.out + logs.err)
    n401 = len(hits)
    iit = [int(s.get("idle in transaction", 0)) for s in samples]
    total = [sum(int(v) for v in s.values()) for s in samples]
    growing = len(total) > 2 and total[-1] > total[0] + 10
    ok = n401 == 0 and max(iit or [0]) <= 2 and not growing
    shown = "; ".join(h.strip()[:160] for h in hits[:3])
    return ("PASS" if ok else "FAIL"), (f"{len(samples)} samples: connections {total}, idle in transaction {iit}; "
                                        f"{n401} authentication-failure lines in the platform log"
                                        + (f" (first: {shown})" if hits else ""))


# ── Shared-infrastructure health (BRIEF-SHARED-INFRA-HEALTH-2026-11-12) ───────
# Report only: this section runs `docker inspect`, `docker ps` and, inside the Kafka container,
# `kafka-get-offsets.sh` and `stat`. It never starts, stops, restarts, recreates or updates anything
# (tests/test_infra_check.py asserts the verbs). On 2026-11-10 the OpenLineage proxy came back from a
# reboot with restart=no (the yaml says always) and stayed down two days with nothing showing it.

INFRA_COMPOSE = Path("compose-configs") / "shared-infra" / "shared-infra.yaml"
INFRA_CONFIG = Path("compose-configs") / "shared-infra" / "infra-health.json"
INFRA_KAFKA = "egeria-shared-kafka"
OPENLINEAGE_TOPIC = "openlineage.events"
INFRA_STALE_S = 30 * 60          # the Portal greys a row older than this (egeria_resets_handler.py)
INFRA_KEEP_ROWS = 500
INFRA_VERDICTS = ("PASS", "FAIL", "WARN", "EXPECTED STOPPED", "NOT MEASURED")


def _mini_compose_services(text: str) -> dict:
    """The `services:` mapping of a compose file, for hosts without PyYAML: each service's scalar
    keys (container_name, restart, image) at the indentation compose files use."""
    services, current, in_services, svc_indent = {}, None, False, None
    for raw in text.splitlines():
        line = raw.split(" #", 1)[0].rstrip() if not raw.lstrip().startswith("#") else ""
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        if indent == 0:
            in_services = line.strip() == "services:"
            current = None
            continue
        if not in_services:
            continue
        if svc_indent is None:
            svc_indent = indent
        if indent == svc_indent and line.strip().endswith(":"):
            current = line.strip()[:-1].strip("'\"")
            services[current] = {}
        elif current is not None and indent > svc_indent and ":" in line:
            key, _, val = line.strip().partition(":")
            if indent == svc_indent * 2 and val.strip():
                services[current][key.strip()] = val.strip().strip("'\"")
    return services


def compose_services(path: Path) -> list[dict]:
    """[{service, container, restart, image}] from a compose file, read at check time so a new
    service is covered without a code change. restart defaults to compose's own default, "no"."""
    text = path.read_text()
    try:
        import yaml  # type: ignore
        doc = yaml.safe_load(text) or {}
        raw = {k: (v or {}) for k, v in (doc.get("services") or {}).items()}
    except ImportError:
        raw = _mini_compose_services(text)
    out = []
    project = compose_project(path, text)
    for name, svc in raw.items():
        out.append({"service": name, "container": svc.get("container_name"),
                    "restart": str(svc.get("restart") or "no"), "image": svc.get("image"), "project": project})
    return out


def compose_project(path: Path, text: Optional[str] = None) -> Optional[str]:
    """The compose project the file names (its top-level `name:`), else None: without one the project
    is whatever `-p` the stack was started with (shared-infra runs as egeria-shared-infra, not its
    folder's name), so it is not guessed."""
    m = re.search(r"^name:\s*['\"]?([^'\"\s#]+)", text if text is not None else path.read_text(), re.M)
    return m.group(1) if m else None


def _env_values(env_file: Path, names: set) -> dict:
    """Only the named keys of a .env file (image variables): nothing else is read into memory."""
    out = {}
    if not env_file.exists():
        return out
    for line in env_file.read_text().splitlines():
        key, sep, val = line.partition("=")
        if sep and key.strip() in names:
            out[key.strip()] = val.strip().strip("'\"")
    return out


_VAR_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::?-([^}]*))?\}")


def _resolve_image(image: Optional[str], env_file: Path) -> Optional[str]:
    if not image:
        return image
    names = {m_.group(1) for m_ in _VAR_RE.finditer(image)}
    values = _env_values(env_file, names)
    return _VAR_RE.sub(lambda m_: values.get(m_.group(1)) or os.environ.get(m_.group(1)) or (m_.group(2) or m_.group(0)),
                       image)


def infra_config(root: Path) -> dict:
    """infra-health.json: extra compose files and services deliberately stopped. Missing or empty =
    shared-infra only, nothing expected stopped."""
    p = root / INFRA_CONFIG
    cfg = {}
    if p.exists() and p.read_text().strip():
        cfg = json.loads(p.read_text())
    return {"extraComposeFiles": list(cfg.get("extraComposeFiles") or []),
            "expectedStopped": {e["service"]: e for e in (cfg.get("expectedStopped") or []) if e.get("service")},
            "prefect": cfg.get("prefect") or None}


def infra_reference(env: Env) -> tuple[Path, str]:
    """The checkout the stack was deployed from: the running platform's compose folder (as `plan`
    reads it); this CLI's own checkout when that cannot be read."""
    try:
        setup = compose_setup(env)
        return Path(setup["workingDir"]).resolve().parents[1], "the running platform's compose folder"
    except Exception as exc:  # noqa: BLE001
        return Path(env.repo), f"this CLI's checkout (the platform's compose folder was not read: {exc})"


def _inspect(env: Env, container: str) -> tuple[Optional[dict], Optional[str]]:
    """(inspect JSON, None), (None, "missing") or (None, <why it was not read>)."""
    r = env.runner.run(["docker", "inspect", container], check=False)
    if r.rc != 0:
        text = (r.err or r.out or "").strip()
        if "No such object" in text or "No such container" in text:
            return None, "missing"
        return None, text.splitlines()[-1][:200] if text else f"docker inspect exited {r.rc}"
    try:
        data = json.loads(r.out)
        return (data[0] if isinstance(data, list) and data else None), (None if data else "missing")
    except ValueError as exc:
        return None, f"docker inspect gave no JSON ({exc})"


def _container_for(env: Env, svc: dict) -> tuple[Optional[str], Optional[str]]:
    """(container name, None), (None, "missing"), or (None, why it is not known). A service without a
    container_name is found by its compose project AND service labels, so another project's "redis"
    never answers for this one."""
    if svc["container"]:
        return svc["container"], None
    cmd = ["docker", "ps", "-a", "--filter", f"label=com.docker.compose.service={svc['service']}"]
    if svc.get("project"):
        cmd += ["--filter", f"label=com.docker.compose.project={svc['project']}"]
    r = env.runner.run(cmd + ["--format", "{{.Names}}"], check=False)
    if r.rc != 0:
        text = (r.err or r.out or "").strip()
        return None, (text.splitlines()[-1][:200] if text else f"docker ps exited {r.rc}")
    names = [n for n in r.out.split() if n]
    if not names:
        return None, "missing"
    if len(names) > 1:
        return None, f"{len(names)} containers for this service ({', '.join(sorted(names))}); not checked"
    return names[0], None


def service_verdict(svc: dict, insp: Optional[dict], why: Optional[str], compose_file: Path,
                    expected: Optional[dict], env_file: Path) -> dict:
    """One line of the check: PASS / FAIL / WARN / EXPECTED STOPPED / NOT MEASURED, with words."""
    line = {"service": svc["service"], "container": svc.get("container"), "composeFile": str(compose_file),
            "state": None, "health": None, "restartYaml": svc["restart"], "restartContainer": None,
            "configFiles": None, "configFilesMatch": None, "image": None,
            "imageYaml": _resolve_image(svc.get("image"), env_file), "verdict": None, "words": ""}
    if insp is None:
        if why == "missing" or why is None:
            if expected:
                line.update(verdict="EXPECTED STOPPED", state="missing",
                            words=f"not created, as expected: {expected.get('reason')} ({expected.get('by')})")
            else:
                line.update(verdict="FAIL", state="missing", words="no such container")
        else:
            line.update(verdict="NOT MEASURED", words=f"not read: {why}")
        return line
    st = insp.get("State") or {}
    hc = insp.get("HostConfig") or {}
    labels = ((insp.get("Config") or {}).get("Labels")) or {}
    line["state"] = st.get("Status")
    line["health"] = (st.get("Health") or {}).get("Status")
    line["restartContainer"] = ((hc.get("RestartPolicy") or {}).get("Name")) or "no"
    line["image"] = (insp.get("Config") or {}).get("Image")
    fails, warns, notes = [], [], []

    if st.get("Status") != "running":
        if expected:
            # An entry may say how it should have stopped ("exitCode": 0 for a one-shot setup container):
            # a failed run is then a FAIL, not "as expected".
            code, want = st.get("ExitCode"), expected.get("exitCode")
            if want is not None and code != want:
                line.update(verdict="FAIL",
                            words=f"exited {code} (expected {want}), state {st.get('Status')}; listed as expected "
                                  f"stopped ({expected.get('reason')})")
            else:
                line.update(verdict="EXPECTED STOPPED",
                            words=f"{st.get('Status')} (exit code {code}), as expected: {expected.get('reason')} "
                                  f"({expected.get('by')})")
            return line
        fails.append(f"{st.get('Status') or 'not running'} (exit code {st.get('ExitCode')})")
    elif line["health"] == "unhealthy":
        fails.append("running but unhealthy")
    elif expected:
        warns.append(f"running, though listed as expected stopped ({expected.get('reason')})")

    if line["restartContainer"] != svc["restart"]:
        fails.append(f"drift: container restart={line['restartContainer']}, yaml says {svc['restart']} "
                     "(recreate it from the yaml to fix; this check never does)")

    cfg = labels.get("com.docker.compose.project.config_files")
    if cfg:
        files = [f.strip() for f in cfg.split(",") if f.strip()]
        line["configFiles"] = files
        want = str(compose_file.resolve())
        line["configFilesMatch"] = any(str(Path(f).resolve()) == want for f in files)
        if not line["configFilesMatch"]:
            gone = [f for f in files if not Path(f).exists()]
            shown = "; ".join(f + (" (missing)" if f in gone else "") for f in files)
            warns.append(f"created from {shown}: a recreate from the repo may change it")
    else:
        warns.append("no compose config_files label: not created by docker compose")

    pinned = line["imageYaml"] if line["imageYaml"] and "@sha256:" in line["imageYaml"] else None
    if pinned and line["image"] != pinned:
        warns.append(f"image {line['image']} differs from the yaml's pinned {pinned}")
    elif line["image"]:
        notes.append(f"image {line['image']}")

    head = f"{line['state']}" + (f", {line['health']}" if line["health"] else "") + \
           f", restart {line['restartContainer']} (yaml {svc['restart']})"
    line["verdict"] = "FAIL" if fails else ("WARN" if warns else "PASS")
    line["words"] = "; ".join([head] + fails + warns + notes)
    return line


def openlineage_info(env: Env) -> dict:
    """Information only, never an alert and no age threshold: the topic's latest offset (read-only
    kafka-get-offsets.sh) and the last write to its newest log segment (stat) inside the Kafka container."""
    r = env.runner.run(["docker", "exec", INFRA_KAFKA, "/usr/lib/kafka/bin/kafka-get-offsets.sh",
                        "--bootstrap-server", "localhost:9192", "--topic", OPENLINEAGE_TOPIC, "--time", "-1"],
                       check=False, timeout=60)
    offsets = {}
    for ln in (r.out or "").splitlines():
        parts = ln.strip().split(":")
        if len(parts) == 3 and parts[0] == OPENLINEAGE_TOPIC and parts[2].isdigit():
            offsets[parts[1]] = int(parts[2])
    if r.rc != 0 or not offsets:
        why = ((r.err or r.out or "").strip().splitlines() or [f"exited {r.rc}"])[-1][:200]
        return {"notRead": f"offsets of {OPENLINEAGE_TOPIC} not read: {why}"}
    out = {"offset": sum(offsets.values()), "partitions": offsets, "latestAt": None}
    t = env.runner.run(["docker", "exec", INFRA_KAFKA, "sh", "-c",
                        f'stat -c %Y "$KAFKA_CFG_LOG_DIRS"/{OPENLINEAGE_TOPIC}-*/*.log'], check=False, timeout=30)
    stamps = [int(x) for x in (t.out or "").split() if x.isdigit()]
    if t.rc == 0 and stamps:
        out["latestAt"] = iso(max(stamps))
        out["latestAtBasis"] = "the last write to the topic's newest log segment"
    else:
        out["latestAtNotRead"] = ((t.err or "").strip().splitlines() or [f"stat exited {t.rc}"])[-1][:200]
    return out


# ── Prefect: server health and live pool workers (DESIGN-PREFECT-ROLE-AND-RE-WORKER-2026-11-13 §4) ──
# Read only: GET /health, GET the pool, POST .../workers/filter (a query). Never FAIL, only WARN: RE
# falls back to running steps in its own process when no worker is live, so a missing worker loses
# Prefect run history and dispatch, not the run. Turned on by a "prefect" entry in infra-health.json.

PREFECT_LIVE_FACTOR = 3            # a heartbeat within 3 x the worker's interval is live (as RE's check)
PREFECT_DEFAULT_INTERVAL_S = 30    # Prefect's default worker heartbeat interval


def _age_words(seconds: float) -> str:
    """The same age wording as RE's pool check: s / min under 2 h, hours under 2 days, then days."""
    s = max(0, int(seconds))
    if s < 120:
        return f"{s} s"
    if s < 2 * 3600:
        return f"{s // 60} min"
    if s < 2 * 86400:
        return f"{s // 3600} hours"
    return f"{s // 86400} days"


def _worker_live(w: dict, now: float, factor: int = PREFECT_LIVE_FACTOR) -> bool:
    """Prefect's own status wins when it gives one (ONLINE = live, anything else = not); otherwise
    a heartbeat within factor x the worker's heartbeat interval. No heartbeat at all = not live."""
    status = w.get("status")
    if status:
        return status == "ONLINE"
    beat = _parse_iso(w.get("last_heartbeat_time"))
    interval = w.get("heartbeat_interval_seconds") or PREFECT_DEFAULT_INTERVAL_S
    return beat is not None and now - beat <= factor * interval


def _prefect_row(service: str, verdict: str, words: str) -> dict:
    return {"service": service, "container": None, "kind": "prefect", "verdict": verdict, "words": words}


def prefect_rows(env: Env, cfg: dict) -> list[dict]:
    """Two rows: "Prefect server" (API health) and, per pool, "Prefect pool <name> live workers".
    PASS or WARN only. An unread pool is WARN with the reason, never a 0 that looks like an empty pool."""
    api = str(cfg.get("apiUrl") or "http://localhost:4200/api").rstrip("/")
    pools = list(cfg.get("pools") or ["resource-explorer-pool"])
    now = env.now()

    def get(method, path, body=None):
        return env.http.request(method, api + path, body, timeout=15)

    rows = []
    server_ok, why = False, None
    try:
        code, body = get("GET", "/health")
        if code == 200 and body is True:
            server_ok = True
            try:
                vcode, version = get("GET", "/admin/version")
            except Exception:  # noqa: BLE001 -- the version is a note, not the check
                vcode, version = None, None
            rows.append(_prefect_row("Prefect server", "PASS", f"API healthy at {api}"
                                     + (f" (Prefect {version})" if vcode == 200 and isinstance(version, str) else "")))
        else:
            why = f"answered HTTP {code} {str(body)[:120]}"
    except Exception as exc:  # noqa: BLE001
        why = f"not reachable: {type(exc).__name__}: {str(exc)[:160]}"
    if not server_ok:
        rows.append(_prefect_row("Prefect server", "WARN",
                                 f"{api} {why}; runs are not recorded in Prefect, and dispatched steps run in "
                                 "RE's own process"))
    for pool in pools:
        name = f"Prefect pool {pool} live workers"
        if not server_ok:
            rows.append(_prefect_row(name, "WARN", "not checked: the Prefect server is not reachable"))
            continue
        try:
            code, info = get("GET", f"/work_pools/{pool}")
            if code == 404:
                rows.append(_prefect_row(name, "WARN", f"no such pool on {api}"))
                continue
            if code != 200 or not isinstance(info, dict):
                rows.append(_prefect_row(name, "WARN", f"pool not read: HTTP {code}"))
                continue
            code, workers = get("POST", f"/work_pools/{pool}/workers/filter", {})
            if code != 200 or not isinstance(workers, list):
                rows.append(_prefect_row(name, "WARN", f"workers not read: HTTP {code}"))
                continue
        except Exception as exc:  # noqa: BLE001
            rows.append(_prefect_row(name, "WARN", f"not read: {type(exc).__name__}: {str(exc)[:160]}"))
            continue
        registered = len(workers)
        live = [w for w in workers if isinstance(w, dict) and _worker_live(w, now)]
        beats = [t for t in (_parse_iso(w.get("last_heartbeat_time")) for w in workers if isinstance(w, dict)) if t]
        never = sum(1 for w in workers if isinstance(w, dict) and not w.get("last_heartbeat_time"))
        latest = max(beats) if beats else None
        pool_note = f"pool {info.get('status') or 'status not given'}" + ("; PAUSED" if info.get("is_paused") else "")
        if registered == 0:
            verdict, words = "WARN", "no registered workers"
        elif live:
            verdict = "WARN" if info.get("is_paused") else "PASS"
            words = f"{len(live)} live worker(s) of {registered} registered; last heartbeat {_age_words(now - latest)} ago"
        else:
            verdict = "WARN"
            words = (f"no live worker: {registered} registered, last heartbeat "
                     + (f"{_age_words(now - latest)} ago ({iso(latest)})" if latest else "never"))
        if never:
            words += f"; {never} never heard from"
        rows.append(_prefect_row(name, verdict, f"{words}; {pool_note}"))
    return rows


def infra_check(env: Env, root: Optional[Path] = None) -> dict:
    """Read-only: every service of the shared-infra compose file (plus infra-health.json's extra files)."""
    ref_words = "given"
    if root is None:
        root, ref_words = infra_reference(env)
    cfg = infra_config(root)
    files = [root / INFRA_COMPOSE] + [root / f for f in cfg["extraComposeFiles"]]
    result = {"checkedAt": iso(env.now()), "host": socket.gethostname(), "checkout": str(root),
              "checkoutFrom": ref_words, "composeFiles": [str(f) for f in files], "services": [],
              "openlineage": None, "errors": []}
    for f in files:
        if not f.exists():
            result["errors"].append(f"compose file {f} not found")
            result["services"].append({"service": f"(all of {f.name})", "container": None, "verdict": "NOT MEASURED",
                                       "words": f"compose file {f} not found"})
            continue
        env_file = f.parent / ".env"
        for svc in compose_services(f):
            container, why = _container_for(env, svc)
            svc = {**svc, "container": container}
            insp = None
            if container is not None:
                insp, why = _inspect(env, container)
            result["services"].append(service_verdict(svc, insp, why, f, cfg["expectedStopped"].get(svc["service"]),
                                                      env_file))
    if cfg["prefect"]:
        try:
            result["services"] += prefect_rows(env, cfg["prefect"])
        except Exception as exc:  # noqa: BLE001
            result["services"].append(_prefect_row("Prefect", "WARN", f"not checked: {type(exc).__name__}: {exc}"))
    try:
        result["openlineage"] = openlineage_info(env)
    except Exception as exc:  # noqa: BLE001
        result["openlineage"] = {"notRead": f"{type(exc).__name__}: {exc}"}
    counts = {v: sum(1 for s in result["services"] if s["verdict"] == v) for v in INFRA_VERDICTS}
    result["counts"] = counts
    result["verdict"] = "FAIL" if counts["FAIL"] else ("NOT MEASURED" if counts["NOT MEASURED"] else
                                                       ("WARN" if counts["WARN"] else "PASS"))
    return result


def infra_lines(result: dict) -> list[str]:
    out = [f"Shared infrastructure, {result['checkedAt']} (checkout {result['checkout']}, {result['checkoutFrom']}):"]
    for s in result["services"]:
        name = s["service"] + (f" ({s['container']})" if s.get("container") else "")
        out.append(f"  {s['verdict']:<16} {name}: {s['words']}")
    ol = result.get("openlineage") or {}
    if "notRead" in ol:
        out.append(f"  {'INFO':<16} {OPENLINEAGE_TOPIC}: {ol['notRead']}")
    else:
        at = ol.get("latestAt") or f"time not read ({ol.get('latestAtNotRead')})"
        out.append(f"  {'INFO':<16} {OPENLINEAGE_TOPIC}: latest event {at} (offset {ol.get('offset')})")
    return out


def infra_verify_checks(result: dict) -> list[dict]:
    """The verify step's lines: one per service. A FAIL fails verify; WARN and EXPECTED STOPPED are
    reported and do not; the OpenLineage line is information (INFO), never a verdict."""
    checks = [{"check": f"infra {s['service']}", "verdict": s["verdict"], "evidence": s["words"]}
              for s in result["services"]]
    ol = result.get("openlineage") or {}
    checks.append({"check": f"infra {OPENLINEAGE_TOPIC}", "verdict": "INFO",
                   "evidence": ol.get("notRead") or f"latest event {ol.get('latestAt')} (offset {ol.get('offset')})"})
    return checks


INFRA_LOG_KEEP = 2000            # ~2 weeks of 10-minute runs, one line each


def infra_summary(result: dict) -> str:
    """One line for a scheduled run's log: time, overall verdict, counts, and the services not PASS."""
    counts = result.get("counts") or {}
    bad = [f"{s['service']} {s['verdict']}" for s in result.get("services") or [] if s.get("verdict") != "PASS"]
    ol = result.get("openlineage") or {}
    ol_text = ("openlineage not read" if "notRead" in ol
               else f"openlineage offset {ol.get('offset')} at {ol.get('latestAt')}")
    return (f"{result.get('checkedAt')} {result.get('verdict')} "
            + ", ".join(f"{n} {v.lower()}" for v, n in counts.items() if n)
            + (f" [{'; '.join(bad)}]" if bad else "") + f"; {ol_text}")


def append_bounded(path: Path, line: str, keep: int = INFRA_LOG_KEEP) -> None:
    """Append one line and keep only the newest `keep` lines (rewritten through a temp file)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = path.read_text(errors="replace").splitlines() if path.exists() else []
    lines = (lines + [line.replace("\n", " ")])[-keep:]
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text("\n".join(lines) + "\n")
    os.replace(tmp, path)


# ── Alert email (owner, 2026-11-13: "Email is good - the address should be in the .env") ──────────
# Sent only on a change: a row going into WARN / FAIL / NOT MEASURED (or a different one of those), and
# on recovery to all PASS. The last notified state is kept next to the log. Settings come from the
# process environment, else from these keys of the quickstart .env (only these keys are read, and no
# value is ever logged). Unset recipient or SMTP host = "alerting not configured" on every log line,
# nothing sent, and the state is not advanced, so the first run after configuring reports what is wrong.

ALERT_ENV_FILE = Path("compose-configs") / "egeria-quickstart" / ".env"
ALERT_KEYS = ("INFRA_ALERT_EMAIL", "INFRA_ALERT_SMTP_HOST", "INFRA_ALERT_SMTP_PORT", "INFRA_ALERT_SMTP_USER",
              "INFRA_ALERT_SMTP_PASSWORD", "INFRA_ALERT_FROM", "INFRA_ALERT_SMTP_SECURITY")
ALERT_REQUIRED = ("INFRA_ALERT_EMAIL", "INFRA_ALERT_SMTP_HOST")
ALERT_DEGRADED = ("FAIL", "WARN", "NOT MEASURED", "ERROR")


def alert_settings(root: Path) -> dict:
    """{key: value} for ALERT_KEYS: the process environment first, then the quickstart .env."""
    from_file = _env_values(Path(root) / ALERT_ENV_FILE, set(ALERT_KEYS))
    return {k: (os.environ.get(k) or from_file.get(k) or "") for k in ALERT_KEYS}


def degraded_rows(result: Optional[dict], error: Optional[str] = None) -> dict:
    """{row name: verdict} for every row that is not fine. EXPECTED STOPPED and PASS are fine."""
    if error is not None:
        return {"infra-check": "ERROR"}
    return {s["service"]: s["verdict"] for s in (result or {}).get("services") or []
            if s.get("verdict") in ALERT_DEGRADED}


def alert_message(host: str, at: str, before: dict, now: dict, result: Optional[dict], error: Optional[str]) -> tuple[str, str]:
    words = {s["service"]: s.get("words", "") for s in (result or {}).get("services") or []}
    if error is not None:
        words["infra-check"] = error
    if not now:
        subject = f"[infra-check {host}] recovered: everything PASS"
    else:
        worst = next(v for v in ALERT_DEGRADED if v in now.values())
        subject = f"[infra-check {host}] {worst}: " + ", ".join(sorted(now))[:150]
    lines = [f"infra-check on {host} at {at}.", ""]
    for name in sorted(set(now) | set(before)):
        old, new = before.get(name), now.get(name)
        if new and old != new:
            lines.append(f"NOW {new}{f' (was {old})' if old else ''}: {name}: {words.get(name, '')}")
    for name in sorted(now):
        if before.get(name) == now[name]:
            lines.append(f"still {now[name]}: {name}: {words.get(name, '')}")
    for name in sorted(set(before) - set(now)):
        lines.append(f"recovered (was {before[name]}): {name}")
    lines += ["", "Read only: infra-check fixes nothing. The full result is in the Portal's Shared "
              "infrastructure panel and in infra-check.log on the host."]
    return subject, "\n".join(lines) + "\n"


def _smtp_default(host: str, port: int, security: str):
    import smtplib
    if security == "ssl":
        return smtplib.SMTP_SSL(host, port, timeout=30)
    conn = smtplib.SMTP(host, port, timeout=30)
    if security == "starttls":
        conn.starttls(context=ssl.create_default_context())
    return conn


def send_alert(env: Env, settings: dict, subject: str, body: str) -> None:
    from email.message import EmailMessage
    security = (settings.get("INFRA_ALERT_SMTP_SECURITY") or "").lower() or \
        ("ssl" if settings.get("INFRA_ALERT_SMTP_PORT") == "465" else "starttls")
    if security not in ("starttls", "ssl", "none"):
        raise ValueError(f"INFRA_ALERT_SMTP_SECURITY must be starttls, ssl or none, not {security!r}")
    port = int(settings.get("INFRA_ALERT_SMTP_PORT") or (465 if security == "ssl" else 587))
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.get("INFRA_ALERT_FROM") or settings.get("INFRA_ALERT_SMTP_USER") or \
        f"infra-check@{socket.gethostname()}"
    msg["To"] = settings["INFRA_ALERT_EMAIL"]
    msg.set_content(body)
    conn = (env.smtp or _smtp_default)(settings["INFRA_ALERT_SMTP_HOST"], port, security)
    try:
        if settings.get("INFRA_ALERT_SMTP_USER"):
            conn.login(settings["INFRA_ALERT_SMTP_USER"], settings.get("INFRA_ALERT_SMTP_PASSWORD") or "")
        conn.send_message(msg)
    finally:
        try:
            conn.quit()
        except Exception:  # noqa: BLE001
            pass


def alert_on_change(env: Env, state_path: Path, root: Path, result: Optional[dict],
                    error: Optional[str] = None) -> dict:
    """Compare this run's not-fine rows with the last notified ones; email on a change. Returns
    {"outcome": ..., "configured": bool, ...} for the log line and the recorded result. Never raises."""
    now_rows = degraded_rows(result, error)
    try:
        settings = alert_settings(root)
    except Exception as exc:  # noqa: BLE001
        return {"outcome": f"alerting not configured: settings not read ({type(exc).__name__})", "configured": False}
    missing = [k for k in ALERT_REQUIRED if not settings.get(k)]
    if missing:        # said on every run, changed or not: an unconfigured alert is never silent
        return {"outcome": "alerting not configured", "configured": False, "unset": missing}
    try:
        before = (json.loads(state_path.read_text()).get("degraded") or {}) if state_path.exists() else {}
    except (ValueError, OSError, AttributeError):
        before = {}
    if now_rows == before:
        return {"outcome": "no change", "configured": True}
    at = (result or {}).get("checkedAt") or iso(env.now())
    subject, body = alert_message(socket.gethostname(), at, before, now_rows, result, error)
    try:
        send_alert(env, settings, subject, body)
    except Exception as exc:  # noqa: BLE001 -- the state is not advanced, so the next run tries again
        text = str(exc).replace(settings.get("INFRA_ALERT_SMTP_PASSWORD") or "\0", "***")[:200]
        return {"outcome": f"alert NOT sent: {type(exc).__name__}: {text}", "configured": True}
    state_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = state_path.with_name(state_path.name + ".tmp")
    tmp.write_text(json.dumps({"degraded": now_rows, "notifiedAt": iso(env.now()), "subject": subject}, indent=2) + "\n")
    os.replace(tmp, state_path)
    return {"outcome": "alert sent" if now_rows else "recovery sent", "configured": True, "subject": subject}


def alert_words(a: dict) -> str:
    if a["outcome"] == "alerting not configured":
        return "alerting not configured (unset: " + ", ".join(a.get("unset") or []) + ")"
    return a["outcome"]


def infra_check_logged(env: Env, log: Path, *, record: bool, checkout: Optional[Path],
                       alert: bool = True) -> int:
    """The scheduled form: nothing on stdout/stderr, one bounded log line per run, whatever happens.
    With `alert`, an email on a change of state (alert_on_change); the state file sits next to the log."""
    state_path = log.with_name(log.stem + "-alert-state.json")
    try:
        result = infra_check(env, checkout)
        line = infra_summary(result)
        if alert:
            a = alert_on_change(env, state_path, Path(result.get("checkout") or env.repo), result)
            result["alerting"] = a
            line += "; " + alert_words(a)
        if record:
            try:
                record_infra(env, result)
                line += "; recorded"
            except Exception as exc:  # noqa: BLE001
                line += f"; NOT recorded: {type(exc).__name__}: {str(exc)[:200]}"
        rc = 1 if result["counts"]["FAIL"] else 0
    except Exception as exc:  # noqa: BLE001
        err = f"{type(exc).__name__}: {str(exc)[:300]}"
        line, rc = f"{iso(env.now())} ERROR {err}", 1
        if alert:
            line += "; " + alert_words(alert_on_change(env, state_path, Path(checkout or env.repo), None, err))
    append_bounded(log, line)
    return rc


INFRA_DDL = (
    "CREATE SCHEMA IF NOT EXISTS demo; "
    "CREATE TABLE IF NOT EXISTS demo.infra_checks ("
    " id serial PRIMARY KEY, checked_at timestamptz NOT NULL, host text, compose_files jsonb, result jsonb); "
    "ALTER TABLE demo.infra_checks OWNER TO demo_user")


def record_infra(env: Env, result: dict) -> None:
    """One row in coco_pharma.demo.infra_checks for the Portal; keeps the newest INFRA_KEEP_ROWS (this
    table only)."""
    sql = (INFRA_DDL + "; INSERT INTO demo.infra_checks (checked_at, host, compose_files, result) VALUES ("
           + _sql_str(result["checkedAt"]) + ", " + _sql_str(result["host"]) + ", "
           + _sql_str(json.dumps(result["composeFiles"])) + "::jsonb, " + _sql_str(json.dumps(result)) + "::jsonb); "
           + "DELETE FROM demo.infra_checks WHERE id NOT IN (SELECT id FROM demo.infra_checks "
           + f"ORDER BY checked_at DESC, id DESC LIMIT {INFRA_KEEP_ROWS})")
    psql(env, sql, db=DEMO_DB)


# ── Record (the Portal's "last reset" panel) ──────────────────────────────────

RESETS_DDL = (
    "CREATE SCHEMA IF NOT EXISTS demo; "
    "CREATE TABLE IF NOT EXISTS demo.egeria_resets ("
    " id serial PRIMARY KEY, started_at timestamptz NOT NULL, finished_at timestamptz,"
    " outcome text NOT NULL, operator text, host text, database text,"
    " old_digest text, new_digest text, old_image_id text, new_image_id text,"
    " backup_path text, backup_bytes bigint, backup_sha256 text,"
    " heal jsonb, verify jsonb, steps jsonb, state_dir text); "
    "ALTER TABLE demo.egeria_resets OWNER TO demo_user")


def _sql_str(v) -> str:
    if v is None:
        return "NULL"
    return "'" + str(v).replace("'", "''") + "'"


def record_row(env: Env, plan: dict, state: dict, run_dir: Path) -> dict:
    ev = lambda s: state["steps"].get(s, {}).get("evidence") or {}
    statuses = {s: v.get("status") for s, v in state["steps"].items()}
    rest = {k: v for k, v in statuses.items() if k != "record"}
    outcome = ("completed" if all(v == "done" for v in rest.values())
               else "failed" if "failed" in rest.values()
               else "completed, needs a person" if all(v in ("done", "needs a person") for v in rest.values())
               else "incomplete")
    row = {
        "started_at": plan["createdAt"], "finished_at": iso(env.now()), "outcome": outcome,
        "operator": plan.get("createdBy"), "host": plan.get("host"), "database": plan["database"] if plan["clear"] else None,
        "old_digest": plan["image"]["currentDigest"], "new_digest": plan["image"]["targetDigest"],
        "old_image_id": plan["image"]["runningImageId"], "new_image_id": ev("recreate").get("runningImageId"),
        "backup_path": ev("backup").get("file"), "backup_bytes": ev("backup").get("bytes"),
        "backup_sha256": ev("backup").get("sha256"),
        "heal": json.dumps(ev("heal-wait") or None), "verify": json.dumps(ev("verify") or None),
        "steps": json.dumps(statuses), "state_dir": str(run_dir),
    }
    cols = list(row)
    sql = (RESETS_DDL + "; INSERT INTO demo.egeria_resets (" + ", ".join(cols) + ") VALUES ("
           + ", ".join(_sql_str(row[c]) + ("::jsonb" if c in ("heal", "verify", "steps") else "") for c in cols) + ")")
    psql(env, sql, db=DEMO_DB)
    return {"outcome": outcome, "row": {k: v for k, v in row.items() if k not in ("heal", "verify")}}


def step_record(env, plan, state, run_dir):
    """Write the Portal's "last reset" row (demo.egeria_resets) and print a HANDOFF summary."""
    r = record_row(env, plan, state, run_dir)
    env.say(handoff_summary(plan, state, r["outcome"]))
    return r


def handoff_summary(plan: dict, state: dict, outcome: str) -> str:
    lines = [f"Egeria reset {plan['createdAt']} on {plan.get('host')}: {outcome}",
             f"  image {plan['image']['currentDigest'][:19]}… -> {plan['image']['targetDigest'][:19]}…"]
    for s in plan["steps"]:
        st = state["steps"].get(s, {})
        lines.append(f"  {s:<15} {st.get('status')}" + (f"  ({st.get('error')})" if st.get("error") else ""))
    for c in (state["steps"].get("verify", {}).get("evidence") or {}).get("checks", []):
        lines.append(f"  verify {c['verdict']:<12} {c['check']}")
    return "\n".join(lines)


# ── Apply ─────────────────────────────────────────────────────────────────────

STEP_FUNCS = {
    "disk-check": step_disk_check, "repin": step_repin, "build": step_build,
    "freeze-writers": step_freeze_writers, "stop-platform": step_stop_platform, "backup": step_backup,
    "clear": step_clear, "recreate": step_recreate, "secrets-sync": step_secrets_sync,
    "heal-wait": step_heal_wait, "unfreeze": step_unfreeze, "verify": step_verify, "record": step_record,
}


def apply(env: Env, plan_arg: str, *, dry_run: bool = False, redo: Optional[str] = None) -> int:
    run_dir, plan, state = load_run(plan_arg)
    if dry_run:
        env.say(f"Dry run of {run_dir}: nothing is run or changed.")
        for s in plan["steps"]:
            st = state["steps"].get(s, {}).get("status", "pending")
            doc = (STEP_FUNCS[s].__doc__ or "").strip().splitlines()
            env.say(f"  {s:<15} {st:<8} {doc[0] if doc else ''}")
        return 0
    if redo:
        if redo not in plan["steps"]:
            raise Refused(f"no step {redo!r} in this plan")
        if redo in RUN_ONCE and done(state, redo):
            typed = env.ask(f"{redo} is a run-once step that is already done. Type its name to run it again: ").strip()
            if typed != redo:
                raise Refused(f"not repeating {redo}: the name was not typed")
        state["steps"][redo] = {"status": "pending", "redoneFrom": state["steps"].get(redo)}
        write_json(run_dir / "state.json", state)
    check_still_matches(env, plan, state)
    needs_person = False
    for s in plan["steps"]:
        if done(state, s):
            continue
        env.say(f"== {s}")
        started = env.now()
        state["steps"][s] = {"status": "running", "startedAt": started}
        write_json(run_dir / "state.json", state)
        try:
            evidence = STEP_FUNCS[s](env, plan, state, run_dir)
        except NeedsPerson as exc:
            state["steps"][s] = {"status": "needs a person", "startedAt": started, "finishedAt": env.now(),
                                 "error": str(exc), "evidence": exc.evidence}
            write_json(run_dir / "state.json", state)
            env.say(f"NEEDS A PERSON {s}: {exc}. The run goes on; run apply again after, to mark it done.")
            needs_person = True
            continue
        except (StepFailed, Refused) as exc:
            state["steps"][s] = {"status": "failed", "startedAt": started, "finishedAt": env.now(), "error": str(exc)}
            write_json(run_dir / "state.json", state)
            env.say(f"FAILED {s}: {exc}\nFix it, then run apply again to resume at {s}.")
            return 1
        state["steps"][s] = {"status": "done", "startedAt": started, "finishedAt": env.now(), "evidence": evidence}
        write_json(run_dir / "state.json", state)
    return 3 if needs_person else 0


def main(argv: Optional[list[str]] = None, env: Optional[Env] = None) -> int:
    ap = argparse.ArgumentParser(prog="egeria-upgrade-reset", description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan", help="read the current state and write a plan; changes nothing")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--digest", help="target odpi/egeria-platform digest (sha256:...)")
    g.add_argument("--latest", action="store_true", help=f"resolve {UPSTREAM_IMAGE}'s current digest")
    p.add_argument("--no-clear", action="store_true", help="upgrade the image only; keep the metadata store")
    p.add_argument("--reset-root", default=None, help="where reset folders go (default runtime-volumes/egeria-resets)")
    p.add_argument("--allow-other-checkout", action="store_true",
                   help="allow this CLI to run from another checkout than the one the platform was started from")
    p.add_argument("--launcher", action="append", default=[], metavar="PORT=PATH",
                   help="the script that restarts the writer on PORT (default: " +
                        ", ".join(f"{k}={v}" for k, v in DEFAULT_LAUNCHERS.items()) + ")")
    a = sub.add_parser("apply", help="run (or resume) a plan")
    a.add_argument("--plan", required=True)
    a.add_argument("--dry-run", action="store_true", help="print the steps and their state; run nothing")
    a.add_argument("--redo", help="run this step again (a run-once step needs its name typed)")
    a.add_argument("--personas", choices=PERSONA_ANSWERS,
                   help="answer verify's persona sign-in check up front (ok = checked and working; skip = not "
                        "checked, NOT MEASURED), so the run never waits on a prompt (also EGERIA_RESET_PERSONAS)")
    s = sub.add_parser("status", help="show a plan's step states")
    s.add_argument("--plan", required=True)
    r = sub.add_parser("record", help="write the Portal's reset row now (e.g. after a failed run)")
    r.add_argument("--plan", required=True)
    ic = sub.add_parser("infra-check", help="read-only health of the shared-infra containers; restarts nothing")
    ic.add_argument("--record", action="store_true", help="also write the result to coco_pharma.demo.infra_checks")
    ic.add_argument("--json", action="store_true", help="print the result as JSON")
    ic.add_argument("--log", default=None, metavar="FILE",
                    help="for scheduled runs: print nothing; append ONE line per run to FILE, keeping its newest "
                         f"{INFRA_LOG_KEEP} lines (errors too)")
    ic.add_argument("--no-alert", action="store_true",
                    help="with --log: send no alert email (by default one is sent when the state changes, if "
                         "INFRA_ALERT_EMAIL and INFRA_ALERT_SMTP_HOST are set)")
    ic.add_argument("--checkout", default=None,
                    help="the checkout whose compose files to compare with (default: the running platform's)")
    args = ap.parse_args(argv)
    env = env or Env(runner=Runner(), http=Http())
    try:
        if args.cmd == "plan":
            root = Path(args.reset_root) if args.reset_root else None
            overrides = {}
            for item in args.launcher:
                port, _, path = item.partition("=")
                if not port.isdigit() or int(port) not in DEFAULT_LAUNCHERS or not path:
                    raise Refused(f"--launcher wants PORT=PATH with PORT one of {sorted(DEFAULT_LAUNCHERS)}: {item!r}")
                overrides[int(port)] = path
            make_plan(env, digest=args.digest, latest=args.latest, clear=not args.no_clear, reset_root=root,
                      allow_other_checkout=args.allow_other_checkout, launcher_overrides=overrides)
            return 0
        if args.cmd == "apply":
            if args.personas:
                env.personas = args.personas
            return apply(env, args.plan, dry_run=args.dry_run, redo=args.redo)
        if args.cmd == "infra-check" and args.log:
            return infra_check_logged(env, Path(args.log), record=args.record, alert=not args.no_alert,
                                      checkout=Path(args.checkout).resolve() if args.checkout else None)
        if args.cmd == "infra-check":
            result = infra_check(env, Path(args.checkout).resolve() if args.checkout else None)
            env.say(json.dumps(result, indent=2) if args.json else "\n".join(infra_lines(result)))
            if args.record:
                record_infra(env, result)
                env.say(f"recorded in {DEMO_DB}.demo.infra_checks")
            return 1 if result["counts"]["FAIL"] else 0
        run_dir, plan, state = load_run(args.plan)
        if args.cmd == "status":
            env.say(handoff_summary(plan, state, "status"))
            return 0
        res = record_row(env, plan, state, run_dir)
        env.say(f"recorded: {res['outcome']}")
        return 0
    except Refused as exc:
        env.say(f"REFUSED: {exc}")
        return 2
    except StepFailed as exc:
        env.say(f"FAILED: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
