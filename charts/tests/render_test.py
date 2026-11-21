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
        "--set", "secrets.existingSecret=my-secrets", "--set", "tls.existingSecret=my-tls", "--set", "persistence.storageClassName=fast", "--set", "resources.limits.cpu=4"]
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
    subprocess.run([HELM, "dependency", "update", CHART], capture_output=True, check=True)

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

    refuses("production without tls.existingSecret fails", ["-f", os.path.join(CHART, "values-production.yaml"), "--set", "secrets.existingSecret=s", "--set", "persistence.storageClassName=fast", "--set", "resources.limits.cpu=4"] + BASE, ["tls.existingSecret", "demo"])
    refuses("production refuses strictSsl=false", PROD + BASE + ["--set", "tls.strictSsl=false"], ["strictSsl", "demo only"])

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
            envd = {e["name"]: e.get("value") for e in c["env"]}
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
            seed = [i for i in ss["spec"]["template"]["spec"]["initContainers"] if i["name"] == "seed-config-documents"][0]
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

    # 6. TLS: no password in any ConfigMap; production never renders the tracked demo secrets
    demo_secret_words = []
    demo_passwords = []  # short words: only looked for in Secrets and env values, not in free text
    for env in ("quickstart", "freshstart"):
        sec = os.path.join(CHART, "files", env, "secrets")
        for f in os.listdir(sec):
            demo_secret_words.append(open(os.path.join(sec, f)).read())
        props = open(os.path.join(CHART, "files", env, "application.properties")).read()
        for m in re.finditer(r"^server\.ssl\.(?:key|trust)-store-password=(.+)$", props, re.M):
            demo_passwords.append(m.group(1))
        for label, extra in (("demo", DEMO), ("production", PROD)):
            out = renders(extra + BASE + ["--set", "environment=" + env])
            ds = docs(out)
            cms = "".join(str(d.get("data")) for d in ds if d["kind"] == "ConfigMap")
            check("%s/%s no TLS password or key alias in a ConfigMap" % (env, label),
                  not re.search(r"(?m)^(server\.ssl\.(key-store-password|trust-store-password|keyAlias)|rsa\.key-id)=", cms.replace("\\n", "\n")))
            ss = [d for d in ds if d["kind"] == "StatefulSet"][0]["spec"]["template"]["spec"]
            c = ss["containers"][0]
            envd = {e["name"]: e for e in c["env"]}
            check("%s/%s TLS passwords come from a Secret" % (env, label),
                  "secretKeyRef" in envd["server.ssl.key-store-password"]["valueFrom"] and "secretKeyRef" in envd["server.ssl.trust-store-password"]["valueFrom"])
            check("%s/%s strict.ssl is %s" % (env, label, "false" if label == "demo" else "true"),
                  envd["strict.ssl"]["value"] == ("false" if label == "demo" else "true"))
            if label == "production":
                check("%s/production mounts and uses the TLS Secret keystore" % env,
                      envd["server.ssl.key-store"]["value"].startswith("/deployments/tls/") and any(v["name"] == "tls" and v["secret"]["secretName"] == "my-tls" for v in ss["volumes"]))
                leaked = [w for w in demo_secret_words if w.strip() and w.strip() in out]
                check("%s/production renders none of the tracked demo secret contents" % env, not leaked, "%d demo secret values found" % len(leaked))
                where = str([d for d in ds if d["kind"] == "Secret"]) + str(c["env"])
                check("%s/production renders no tracked demo keystore password" % env, not any(("'%s'" % w) in where for w in demo_passwords))

    # 7. helm test canary
    for env, vs in (("quickstart", "qs-view-server"), ("freshstart", "fs-view-server")):
        ds = docs(renders(DEMO + BASE + ["--set", "environment=" + env]))
        pod = [d for d in ds if d["kind"] == "Pod"][0]
        check("%s: canary is a helm test hook" % env, pod["metadata"]["annotations"]["helm.sh/hook"] == "test")
        ce = {e["name"]: e for e in pod["spec"]["containers"][0]["env"]}
        check("%s: canary reads the environment's view server" % env, ce["VIEW_SERVER"]["value"] == vs)
        check("%s: canary lists every server" % env, len(ce["SERVERS"]["value"].split()) == 5)
        check("%s: canary credentials come from a Secret" % env, "secretKeyRef" in ce["CANARY_PASSWORD"]["valueFrom"])
        cs = [d for d in ds if d["kind"] == "Secret" and d["metadata"]["name"].endswith("-canary")]
        check("%s: demo creates a canary Secret for a non-personal account" % env, len(cs) == 1 and "password" in cs[0]["data"])
        check("%s: canary pod carries the NetworkPolicy client label" % env, pod["metadata"]["labels"].get("egeria.odpi.org/client") == "true")
    ds = docs(renders(PROD + BASE))
    check("production creates no canary Secret", not [d for d in ds if d["kind"] == "Secret"])
    pod = [d for d in ds if d["kind"] == "Pod"][0]
    check("production without canary.existingSecret: the test fails with words", "canary.existingSecret" in pod["spec"]["containers"][0]["command"][2] and "CANARY_PASSWORD" not in {e["name"] for e in pod["spec"]["containers"][0]["env"]})
    ds = docs(renders(PROD + BASE + ["--set", "canary.existingSecret=my-canary"]))
    pod = [d for d in ds if d["kind"] == "Pod"][0]
    ce = {e["name"]: e for e in pod["spec"]["containers"][0]["env"]}
    check("production with canary.existingSecret uses it", ce["CANARY_USER"]["valueFrom"]["secretKeyRef"]["name"] == "my-canary")

    # 8. bundled demo infra (demo only)
    INFRA = ["-f", os.path.join(CHART, "values-demo-infra.yaml")]
    refuses("production refuses demoPostgres", PROD + BASE + ["--set", "demoPostgres.enabled=true"], ["demo only"])
    refuses("production refuses demoKafka", PROD + BASE + ["--set", "demoKafka.enabled=true"], ["demo only"])
    for env, db in (("quickstart", "egeria"), ("freshstart", "egeria_freshstart")):
        out = renders(DEMO + INFRA + ["--set", "environment=" + env])
        ds = docs(out)
        props = [d for d in ds if d["kind"] == "ConfigMap" and d["metadata"]["name"].endswith("-properties")][0]["data"]["application.properties"]
        check("%s: demo infra: platform points at the bundled Postgres and database %s" % (env, db), 'jdbc:postgresql://r1-demo-postgres:5442/%s"' % db in props)
        check("%s: demo infra: platform points at the bundled Kafka" % env, '"kafkaEndpoint" : "r1-demo-kafka.default.svc.cluster.local:9192"' in props)
        kinds = {(d["kind"], d["metadata"]["name"]) for d in ds}
        check("%s: demo infra renders Postgres, its init Job and Kafka" % env, {("StatefulSet", "r1-demo-postgres"), ("Job", "r1-demo-postgres-init"), ("Deployment", "r1-demo-kafka")} <= kinds)
        job = [d for d in ds if d["kind"] == "Job"][0]
        check("%s: init Job is a post-install,post-upgrade hook" % env, job["metadata"]["annotations"]["helm.sh/hook"] == "post-install,post-upgrade")
        sqls = "".join(d["data"]["init-egeria-demo.sql"] for d in ds if d["kind"] == "ConfigMap" and "init-egeria-demo.sql" in d.get("data", {}))
        check("%s: init SQL never drops or truncates" % env, not re.search(r"(?i)\b(drop|truncate)\b", sqls))
        check("%s: init SQL only creates what is missing" % env, "IF NOT EXISTS" in sqls or "WHERE NOT EXISTS" in sqls)
        check("%s: no cluster-scoped objects with demo infra" % env, not [d["kind"] for d in ds if d["kind"] in CLUSTER_SCOPED])
        ss = [d for d in ds if d["kind"] == "StatefulSet" and d["metadata"]["name"] == "r1-platform"][0]
        check("%s: platform waits for its dependencies" % env, ss["spec"]["template"]["spec"]["initContainers"][0]["name"] == "wait-for-dependencies")
    out = renders(DEMO + INFRA + ["--set", "postgres.host=other", "--set", "kafka.bootstrapServers=k:9"])
    check("explicit postgres.host and kafka.bootstrapServers win over demo infra", "jdbc:postgresql://other:" in out and '"kafkaEndpoint" : "k:9"' in out)

    print("\n%d failed" % len(failures) if failures else "\nall passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
