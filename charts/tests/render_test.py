#!/usr/bin/env python3
"""Render tests for charts/egeria-platform (no cluster needed).

Run:  python3 charts/tests/render_test.py            (uses `helm` on PATH)
      HELM=helm3 python3 charts/tests/render_test.py (to test another Helm binary)
Every test is a helm template call; a failing render is asserted by its message.
"""
import os
import re
import subprocess
import sys

import yaml

HELM = os.environ.get("HELM", "helm")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHART = os.path.join(ROOT, "egeria-platform")
BASE = ["--set", "postgres.host=pg.example", "--set", "kafka.bootstrapServers=kafka.example:9092"]
DEMO = ["-f", os.path.join(CHART, "values-demo.yaml")]
PROD = ["-f", os.path.join(CHART, "values-production.yaml"),
        "--set", "secrets.existingSecret=my-secrets", "--set", "persistence.storageClassName=fast", "--set", "resources.limits.cpu=4"]
# kinds that live outside a namespace; none may be rendered by default (design note section 16, rule 2)
CLUSTER_SCOPED = {"ClusterRole", "ClusterRoleBinding", "Namespace", "PersistentVolume", "StorageClass",
                  "CustomResourceDefinition", "SecurityContextConstraints", "PriorityClass",
                  "ValidatingWebhookConfiguration", "MutatingWebhookConfiguration", "IngressClass"}

failures = []


def template(args, release="r1", namespace="default"):
    p = subprocess.run([HELM, "template", release, CHART, "--namespace", namespace] + args,
                       capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def docs(out):
    return [d for d in yaml.safe_load_all(out) if d]


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else "  " + detail))
    if not cond:
        failures.append(name)


def renders(args, **kw):
    rc, out, err = template(args, **kw)
    if rc != 0:
        raise SystemExit("render failed unexpectedly: " + err)
    return out


def refuses(name, args, words):
    rc, out, err = template(args)
    check(name, rc != 0 and all(w in err for w in words), "rc=%s err=%s" % (rc, err[-300:]))


def main():
    subprocess.run([HELM, "dependency", "build", CHART], capture_output=True, check=True)

    # 1. refusals say which setting to change
    refuses("empty secret fails with the setting's name", BASE, ["secrets.existingSecret"])
    refuses("replicas 2 fails with words", DEMO + BASE + ["--set", "replicas=2"], ["replicas", "cannot be scaled"])
    refuses("missing postgres.host fails with its name", DEMO + ["--set", "kafka.bootstrapServers=k:1"], ["postgres.host"])
    refuses("missing kafka.bootstrapServers fails with its name", DEMO + ["--set", "postgres.host=p"], ["kafka.bootstrapServers"])
    refuses("startup probe under 600 s fails", DEMO + BASE + ["--set", "probes.startup.failureThreshold=10"], ["probes.startup", "600"])
    refuses("unknown environment fails", DEMO + BASE + ["--set", "environment=other"], ["environment"])
    refuses("port below 1024 fails", DEMO + BASE + ["--set", "platform.port=443"], ["platform.port", "1024"])
    refuses("a server with no config document fails naming it",
            DEMO + BASE + ["--set", "platform.serverList={qs-metadata-store,qs-nonexistent}"], ["qs-nonexistent", "configuration document"])
    refuses("production refuses demo secret files", PROD + BASE + ["--set", "secrets.useDemoFiles=true"], ["demo only"])
    refuses("production without existingSecret fails", ["-f", os.path.join(CHART, "values-production.yaml")] + BASE + ["--set", "persistence.storageClassName=fast"], ["secrets.existingSecret"])
    refuses("production without storageClassName fails", ["-f", os.path.join(CHART, "values-production.yaml"), "--set", "secrets.existingSecret=s"] + BASE, ["persistence.storageClassName"])

    # 2. per environment: port, probes, no leftovers
    for env, port in (("quickstart", 9443), ("freshstart", 8443)):
        for label, extra in (("demo", DEMO), ("production", PROD)):
            out = renders(extra + BASE + ["--set", "environment=" + env])
            ds = docs(out)
            ss = [d for d in ds if d["kind"] == "StatefulSet"][0]
            c = ss["spec"]["template"]["spec"]["containers"][0]
            ports = [p["containerPort"] for p in c["ports"]]
            check("%s/%s containerPort is %d" % (env, label, port), ports == [port], str(ports))
            check("%s/%s every containerPort >= 1024" % (env, label), all(p >= 1024 for p in ports))
            envd = {e["name"]: e["value"] for e in c["env"]}
            check("%s/%s server.port is always set" % (env, label), envd.get("server.port") == str(port))
            cmd = c["startupProbe"]["exec"]["command"][2]
            check("%s/%s probe uses the environment's port and the common health path" % (env, label),
                  ("localhost:%d/open-metadata/platform-services/server-platform/origin" % port) in cmd and "garygeeke" not in cmd)
            st = c["startupProbe"]
            check("%s/%s startup window >= 600 s" % (env, label), st["periodSeconds"] * st["failureThreshold"] >= 600)
            check("%s/%s no host.docker.internal anywhere" % (env, label), "host.docker.internal" not in out)
            svc = [d for d in ds if d["kind"] == "Service" and d["metadata"]["name"] == "r1-platform"][0]
            check("%s/%s Service port is %d" % (env, label, port), svc["spec"]["ports"][0]["port"] == port)
            servers = envd["startup.server.list"].split(",")
            prefix = "qs-" if env == "quickstart" else "fs-"
            check("%s/%s has its five servers" % (env, label), len(servers) == 5 and all(s.startswith(prefix) for s in servers), str(servers))
            # every ~{name}~ used by a config document is defined in the placeholder variables
            cd = [d for d in ds if d["kind"] == "ConfigMap" and d["metadata"]["name"].endswith("-configdocs")][0]
            props = [d for d in ds if d["kind"] == "ConfigMap" and d["metadata"]["name"].endswith("-properties")][0]["data"]["application.properties"]
            block = re.search(r"platform\.placeholder\.variables=\\\n(.*?)\n  \}", props, re.S).group(1)
            defined = set(re.findall(r'"([A-Za-z]+)" :', block))
            used = set()
            for text in cd["data"].values():
                used |= set(re.findall(r"~\{([A-Za-z]+)\}~", text))
            check("%s/%s every ~{x}~ in the config documents has a value" % (env, label), used <= defined, "undefined: %s" % sorted(used - defined))
            check("%s/%s placeholder values are all non-empty" % (env, label), not re.search(r'"[A-Za-z]+" : ""', block))
            check("%s/%s configdocs ConfigMap holds only this environment's five" % (env, label),
                  sorted(cd["data"]) == sorted(s + ".config" for s in servers))
            seed = ss["spec"]["template"]["spec"]["initContainers"][0]
            check("%s/%s config documents are seeded only when absent (overwrite=false)" % (env, label),
                  {e["name"]: e["value"] for e in seed["env"]}["OVERWRITE"] == "false")

    # 3. OpenShift: no user ids, no SCC
    out = renders(DEMO + BASE + ["--set", "global.openshift=true"])
    sc = [d for d in docs(out) if d["kind"] == "StatefulSet"][0]["spec"]["template"]["spec"]["securityContext"]
    check("openshift: no runAsUser, runAsGroup or fsGroup", not any(k in sc for k in ("runAsUser", "runAsGroup", "fsGroup")), str(sc))
    check("openshift: runAsNonRoot and seccomp stay", sc.get("runAsNonRoot") is True and sc.get("seccompProfile", {}).get("type") == "RuntimeDefault")
    check("openshift: no SCC objects", "SecurityContextConstraints" not in out)
    out = renders(DEMO + BASE)
    sc = [d for d in docs(out) if d["kind"] == "StatefulSet"][0]["spec"]["template"]["spec"]["securityContext"]
    check("plain Kubernetes: fixed user ids", sc.get("runAsUser") == 185 and sc.get("runAsGroup") == 0)

    # 4. two releases of one environment in ONE namespace: no duplicate names, nothing cluster-scoped
    seen = {}
    dup = []
    cluster = []
    for rel in ("fs-one", "fs-two"):
        for d in docs(renders(DEMO + BASE + ["--set", "environment=freshstart"], release=rel)):
            key = (d["kind"], d["metadata"]["name"])
            if key in seen:
                dup.append(key)
            seen[key] = rel
            if d["kind"] in CLUSTER_SCOPED:
                cluster.append(key)
    check("two releases in one namespace: no duplicate object names", not dup, str(dup))
    check("no cluster-scoped objects by default", not cluster, str(cluster))

    # 5. production: NetworkPolicy, existing secret used, no Secret created
    ds = docs(renders(PROD + BASE))
    kinds = [d["kind"] for d in ds]
    check("production renders a NetworkPolicy", "NetworkPolicy" in kinds)
    check("production creates no Secret (existingSecret is used)", "Secret" not in kinds)
    ss = [d for d in ds if d["kind"] == "StatefulSet"][0]
    vol = [v for v in ss["spec"]["template"]["spec"]["volumes"] if v["name"] == "secrets"][0]
    check("production mounts the named secret", vol["secret"]["secretName"] == "my-secrets")

    print("\n%d failed" % len(failures) if failures else "\nall passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
