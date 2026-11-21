#!/usr/bin/env python3
"""Compose <-> chart drift test for egeria-platform. READS compose, never writes it.

Compose is the source of truth (design note section 2.1). For both environments this
compares the chart's values and rendered output with compose-configs/ and the tracked
runtime files, and fails on any difference that is not listed in ALLOWED below.

Run:  python3 charts/tests/drift_test.py
"""
import filecmp
import os
import re
import subprocess
import sys

import yaml

HELM = os.environ.get("HELM", "helm")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHART = os.path.join(REPO, "charts", "egeria-platform")
BASE = ["-f", os.path.join(CHART, "values-demo.yaml"),
        "--set", "postgres.host=pg.example", "--set", "kafka.bootstrapServers=kafka.example:9092"]

# Differences on purpose, each with the reason. Anything else is drift.
ALLOWED = {
    "HOST_FQDN": "compose host name for published ports; the chart has Services, nothing uses it",
}
failures = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else "  " + detail))
    if not cond:
        failures.append(name)


def compose_main(env):
    path = os.path.join(REPO, "compose-configs", "egeria-%s" % env, "egeria-%s.yaml" % env)
    services = yaml.safe_load(open(path))["services"]
    # quickstart calls it egeria-main, freshstart freshstart-egeria-main
    return next(s for n, s in services.items() if n.endswith("egeria-main"))


def dockerfile_from(env):
    p = os.path.join(REPO, "compose-configs", "egeria-%s" % env, "Dockerfile-egeria-platform")
    for line in open(p):
        if line.startswith("FROM "):
            return line.split()[1]


def default_of(text):
    """${NAME:-default} -> default"""
    m = re.search(r"\$\{[A-Z_]+:-(.*)\}\s*$", str(text), re.S)
    return m.group(1).strip() if m else str(text)


def render(env):
    p = subprocess.run([HELM, "template", "r1", CHART] + BASE + ["--set", "environment=" + env],
                       capture_output=True, text=True, check=True)
    return [d for d in yaml.safe_load_all(p.stdout) if d]


def main():
    subprocess.run([HELM, "dependency", "build", CHART], capture_output=True, check=True)
    values = yaml.safe_load(open(os.path.join(CHART, "values.yaml")))
    for env in ("quickstart", "freshstart"):
        c = compose_main(env)
        ds = render(env)
        ss = [d for d in ds if d["kind"] == "StatefulSet"][0]
        pod = ss["spec"]["template"]["spec"]
        main_c = pod["containers"][0]
        cenv = {e["name"]: e["value"] for e in main_c["env"]}
        menv = {k: str(v) for k, v in c["environment"].items()}

        # image: the compose Dockerfile's FROM line, tag and digest
        frm = dockerfile_from(env)
        img = values["image"]
        want = "%s:%s@%s" % (img["repository"], img["tag"], img["digest"])
        check("%s: image matches the compose Dockerfile FROM" % env, frm == want, "%s != %s" % (frm, want))
        check("%s: rendered image is that image" % env, main_c["image"] == want)

        # environment keys: same set, except the allowed ones
        missing = set(menv) - set(cenv) - set(ALLOWED)
        extra = set(cenv) - set(menv)
        check("%s: no compose environment key is missing from the chart" % env, not missing, str(sorted(missing)))
        check("%s: the chart adds no environment key compose lacks" % env, not extra, str(sorted(extra)))
        for k in ("XTDB_ENABLE_BYTEUTILS_SHA1", "XTDB_DISABLE_LIBCRYPTO", "server.port", "startup.server.list"):
            check("%s: %s equals compose" % (env, k), cenv.get(k) == menv.get(k), "%s != %s" % (cenv.get(k), menv.get(k)))
        # JVM flags: compose default vs chart default, whitespace-insensitive
        norm = lambda s: " ".join(str(s).split())
        check("%s: JAVA_OPTS_APPEND default equals compose" % env,
              norm(cenv["JAVA_OPTS_APPEND"]) == norm(default_of(menv["JAVA_OPTS_APPEND"])),
              "%s != %s" % (norm(cenv["JAVA_OPTS_APPEND"]), norm(default_of(menv["JAVA_OPTS_APPEND"]))))
        # resources: compose mem_limit 6g / cpus 4
        mem = default_of(c["mem_limit"]).replace("g", "Gi")
        cpu = default_of(c["cpus"]) if "cpus" in c else None
        lim = main_c["resources"]["limits"]
        check("%s: memory limit equals compose mem_limit (%s)" % (env, mem), lim["memory"] == mem, str(lim))
        check("%s: cpu limit equals compose cpus (%s)" % (env, cpu), (str(lim.get("cpu")) if "cpu" in lim else None) == cpu, str(lim))

        # health check: compose probe is the same endpoint family and accepts 200 or 401
        test = " ".join(c["healthcheck"]["test"])
        port = int(menv["server.port"])
        check("%s: compose container port is the chart's" % env, any(str(port) in str(p) for p in c["ports"]))
        check("%s: compose probe path ends with the chart's health path" % env,
              values["platform"]["healthPath"].replace("/open-metadata/platform-services/", "") in test, test[-160:])
        check("%s: compose accepts 200 or 401, so does the chart" % env,
              "200|401" in test and "= 401" in main_c["startupProbe"]["exec"]["command"][2])
        hc = c["healthcheck"]
        check("%s: chart startup window is at least compose's start_period + retries x interval" % env,
              main_c["startupProbe"]["periodSeconds"] * main_c["startupProbe"]["failureThreshold"]
              >= int(str(hc["start_period"]).rstrip("s")) + int(hc["retries"]) * int(str(hc["interval"]).rstrip("s")))

        # the exchange and runtime folders compose mounts are all offered (optional) by the chart
        mounts = {v.split(":")[1] for v in c["volumes"]}
        offered = {"/deployments/" + n for n in values["exchange"]} | {
            "/deployments/data", "/deployments/logs", "/deployments/logs/security",
            "/deployments/secrets", "/deployments/application.properties"}
        # quickstart-only demo folders are quickstart's; freshstart mounts a subset
        check("%s: every compose /deployments mount has a chart equivalent" % env,
              all(m in offered for m in mounts if m.startswith("/deployments/")),
              str(sorted(m for m in mounts if m.startswith("/deployments/") and m not in offered)))

        # files copied into the chart equal their compose originals
        files = os.path.join(CHART, "files", env)
        pfx = "qs" if env == "quickstart" else "fs"
        runtime = os.path.join(REPO, "runtime-volumes", "%s-platform-data" % env, "%s.application.properties" % env)
        check("%s: chart properties file equals the tracked compose file" % env,
              filecmp.cmp(os.path.join(files, "application.properties"), runtime, shallow=False))
        srvdir = os.path.join(REPO, "compose-configs", "egeria-quickstart", "servers")
        same = True
        names = sorted(n for n in os.listdir(srvdir) if n.startswith(pfx + "-"))
        for n in names:
            same &= filecmp.cmp(os.path.join(files, "servers", n, n + ".config"),
                                os.path.join(srvdir, n, "config", n + ".config"), shallow=False)
        check("%s: the chart's config documents equal the tracked originals (%d)" % (env, len(names)), same and len(names) == 5)
        secdir = os.path.join(REPO, "compose-configs", "egeria-%s" % env, "secrets")
        sec = sorted(f for f in os.listdir(secdir) if f.endswith(".omsecrets"))
        check("%s: demo secret files equal the tracked originals" % env,
              sec == sorted(os.listdir(os.path.join(files, "secrets"))) and all(
                  filecmp.cmp(os.path.join(files, "secrets", f), os.path.join(secdir, f), shallow=False) for f in sec))

        # the rendered placeholders equal compose's, except the endpoints the chart must re-point
        props = [d for d in ds if d["kind"] == "ConfigMap" and d["metadata"]["name"].endswith("-properties")][0]["data"]["application.properties"]
        rendered = dict(re.findall(r'"([A-Za-z]+)" : (.*?),?\\?$', props.split("platform.placeholder.variables=")[1].split("\n  }")[0], re.M))
        orig = dict(re.findall(r'"([A-Za-z]+)" : (.*?),?\\?$', open(runtime).read().split("platform.placeholder.variables=")[1].split("\n  }")[0], re.M))
        repointed = {"kafkaEndpoint", "egeriaEndpoint", "repositoryDatabaseURL"}
        diff = {k for k in orig if rendered.get(k) != orig[k]} - repointed
        check("%s: placeholder variables equal compose except the re-pointed endpoints" % env, not diff, str(sorted(diff)))

    print("\n%d failed" % len(failures) if failures else "\nno drift")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
