#!/usr/bin/env python3
"""Render tests for charts/egeria-stack (the umbrella). Run: python3 charts/tests/stack_render_test.py (HELM=helm3 too)."""
import os
import subprocess
import sys

import yaml

HELM = os.environ.get("HELM", "helm")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHART = os.path.join(ROOT, "egeria-stack")
DIG = "sha256:" + "a" * 64
IMGS = ["--set", "portal.images.portal.repository=r/p", "--set", "portal.images.portal.tag=t",
        "--set", "portal.images.apache.repository=r/a", "--set", "portal.images.apache.tag=t",
        "--set", "core.postgres.host=pg.example", "--set", "core.kafka.bootstrapServers=k.example:9092"]
V = lambda n: ["-f", os.path.join(CHART, n)]
PROD = V("values-production.yaml") + V("values-freshstart.yaml") + IMGS + [
    "--set", "core.secrets.existingSecret=s", "--set", "core.tls.existingSecret=t", "--set", "core.persistence.storageClassName=fast",
    "--set", "core.resources.limits.cpu=4", "--set", "portal.secrets.existingSecret=ps", "--set", "portal.tls.caSecret=ca",
    "--set", "portal.persistence.storageClassName=fast", "--set", "portal.images.portal.digest=" + DIG, "--set", "portal.images.apache.digest=" + DIG,
    "--set", "portal.platform.userDirectorySecret=s"]
failures = []


def template(args, release="s"):
    p = subprocess.run([HELM, "template", release, CHART, "--namespace", "ns1"] + args, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else "  " + detail))
    if not cond:
        failures.append(name)


def renders(args):
    rc, out, err = template(args)
    if rc != 0:
        raise SystemExit("render failed unexpectedly: " + err)
    return [d for d in yaml.safe_load_all(out) if d]


def refuses(name, args, words):
    rc, out, err = template(args)
    check(name, rc != 0 and all(w in err for w in words), "rc=%s err=%s" % (rc, err[-300:]))


def main():
    subprocess.run([HELM, "dependency", "update", os.path.join(ROOT, "egeria-platform")], capture_output=True, check=True)
    subprocess.run([HELM, "dependency", "update", os.path.join(ROOT, "egeria-portal")], capture_output=True, check=True)
    subprocess.run([HELM, "dependency", "update", CHART], capture_output=True, check=True)
    for env, port in (("quickstart", 9443), ("freshstart", 8443)):
        ds = renders(V("values-demo.yaml") + V("values-%s.yaml" % env) + IMGS)
        keys = [(d["kind"], d["metadata"]["name"]) for d in ds]
        check(env + ": both parts render, with no duplicate object", len(keys) == len(set(keys)) and ("StatefulSet", "s-platform") in keys and ("Deployment", "s-portal") in keys, str(len(keys)))
        portal = next(d for d in ds if d["kind"] == "Deployment" and d["metadata"]["name"] == "s-portal")
        e = {x["name"]: x.get("value") for x in portal["spec"]["template"]["spec"]["containers"][0]["env"]}
        check(env + ": the Portal points at this release's platform Service and port", e["EGERIA_PLATFORM_URL"] == "https://s-platform:%d" % port, str(e["EGERIA_PLATFORM_URL"]))
        check(env + ": the Portal is not given a Secret name that the platform also creates",
              not [k for k in keys if keys.count(k) > 1])
        tests = sorted(d["metadata"]["name"] for d in ds if d["kind"] == "Pod")
        check(env + ": helm test runs both canaries", tests == ["s-platform-canary", "s-portal-canary"], str(tests))
    ds = renders(PROD)
    check("production freshstart renders both parts with their requirements", any(d["kind"] == "StatefulSet" for d in ds) and any(d["kind"] == "NetworkPolicy" and d["metadata"]["name"] == "s-portal" for d in ds))
    # the public demo keystore password is kept only to recognise it. It is a common word, so a substring test would match labels;
    # test where a password would live instead: a Secret value, a ConfigMap value or a "password=<it>" line, an env value.
    import base64, re
    demo_pw = open(os.path.join(CHART, "files", "demo-keystore-password")).read().strip()

    def holders(ds):
        found = []
        for d in ds:
            name = d["metadata"]["name"]
            vals = []
            if d["kind"] == "Secret":
                vals += [base64.b64decode(v).decode(errors="replace").strip() for v in (d.get("data") or {}).values() if v]
                vals += [str(v).strip() for v in (d.get("stringData") or {}).values()]
            if d["kind"] == "ConfigMap":
                for v in (d.get("data") or {}).values():
                    vals += [str(v).strip()] + re.findall(r"(?i)(?:password|pwd)[^=:\n]*[=:]\s*(\S+)", str(v))
            if d["kind"] in ("Deployment", "StatefulSet", "Pod"):
                spec = d["spec"].get("template", {}).get("spec", d["spec"])
                for c in spec.get("containers", []) + spec.get("initContainers", []):
                    vals += [str(e.get("value", "")).strip() for e in c.get("env", [])]
            if demo_pw in vals:
                found.append(name)
        return found
    rc, prod_out, _ = template(PROD)
    check("production: the public demo keystore password is in no Secret, ConfigMap or env value", rc == 0 and holders([d for d in yaml.safe_load_all(prod_out) if d]) == [], str(holders([d for d in yaml.safe_load_all(prod_out) if d])))
    for env in ("quickstart", "freshstart"):
        h = holders(renders(V("values-demo.yaml") + V("values-%s.yaml" % env) + IMGS))
        check(env + " demo: the public demo keystore password is held only by the platform's demo TLS Secret", h == ["s-platform-tls"], str(h))
    refuses("production + quickstart is refused (no Portal login gate)", V("values-production.yaml") + V("values-quickstart.yaml") + IMGS, ["login gate"])
    # agreement checks
    base = V("values-demo.yaml") + V("values-quickstart.yaml") + IMGS
    refuses("a core.environment that differs is refused", base + ["--set", "core.environment=freshstart"], ["core.environment", "freshstart"])
    refuses("a portal.environment that differs is refused", base + ["--set", "portal.environment=freshstart"], ["portal.environment"])
    refuses("differing postures are refused", base + ["--set", "portal.posture=production"], ["posture"])
    refuses("posture=production alone (parts still demo) is refused, naming values-production.yaml",
            base + ["--set", "posture=production"], ["posture", "values-production.yaml"])
    refuses("core.posture=production alone is refused", base + ["--set", "core.posture=production"], ["posture"])
    refuses("a portal.platform.serviceName that is not this release's platform is refused", base + ["--set", "portal.platform.serviceName=other"], ["portal.platform.serviceName", "s-platform"])
    refuses("a bad top-level environment is refused", base + ["--set", "environment=bogus"], ["environment"])
    # two releases do not collide
    a = {(d["kind"], d["metadata"]["name"]) for d in renders(base)}
    rc, out, _ = template(base, release="t")
    b = {(d["kind"], d["metadata"]["name"]) for d in yaml.safe_load_all(out) if d}
    check("two releases share no object name", not (a & b))
    # one part only
    ds = renders(base + ["--set", "portal.enabled=false"])
    check("portal.enabled=false renders only the platform", not any(d["metadata"]["name"].startswith("s-portal") for d in ds))
    ds = renders(base + ["--set", "core.enabled=false"])
    check("core.enabled=false renders only the Portal (still pointing at <release>-platform)", not any(d["metadata"]["name"] == "s-platform" for d in ds) and any(d["metadata"]["name"] == "s-portal" for d in ds))
    # openshift: global reaches both
    ds = renders(base + ["--set", "global.openshift=true"])
    ok = all(not ({"runAsUser", "runAsGroup", "fsGroup"} & set(d["spec"]["template"]["spec"]["securityContext"])) for d in ds if d["kind"] in ("Deployment", "StatefulSet"))
    check("global.openshift reaches both parts: no runAsUser, runAsGroup or fsGroup", ok)
    # TR-123: a production freshstart Portal names the platform's Secret for its user directory (no silent optional mount)
    refuses("production freshstart without portal.platform.userDirectorySecret is refused, naming it",
            [a for a in PROD if a != "portal.platform.userDirectorySecret=s"][:-1], ["portal.platform.userDirectorySecret", "secrets.existingSecret"])
    ds = renders(PROD)
    dep = next(d for d in ds if d["kind"] == "Deployment" and d["metadata"]["name"] == "s-portal")
    vol = next(v for v in dep["spec"]["template"]["spec"]["volumes"] if v["name"] == "platform-userdir")
    check("production: the Portal's user directory comes from the named platform Secret", vol["secret"]["secretName"] == "s")
    # TR-123: pull Secrets and ServiceAccounts reach every pod; global.imagePullSecrets is set once for all parts
    ds = renders(base + ["--set", "core.demoPostgres.enabled=true", "--set", "core.demoKafka.enabled=true",
                         "--set", "global.imagePullSecrets[0]=regcred", "--set", "core.imagePullSecrets[0].name=core-only",
                         "--set", "core.serviceAccountName=egeria-sa", "--set", "portal.serviceAccountName=portal-sa",
                         "--set", "core.demoPostgres.serviceAccountName=pg-sa"])
    pods = {}
    for d in ds:
        if d["kind"] in ("Deployment", "StatefulSet", "Job"):
            pods[d["metadata"]["name"]] = d["spec"]["template"]["spec"]
        elif d["kind"] == "Pod":
            pods[d["metadata"]["name"]] = d["spec"]
    names = lambda ps: [x["name"] for x in ps.get("imagePullSecrets", [])]
    check("global.imagePullSecrets reaches every pod, test pods and demo infra included (%d pods)" % len(pods),
          len(pods) >= 8 and all("regcred" in names(ps) for ps in pods.values()), str({k: names(v) for k, v in pods.items()}))
    check("a part's own imagePullSecrets is added to the global ones, only for that part",
          names(pods["s-platform"]) == ["core-only", "regcred"] and names(pods["s-platform-canary"]) == ["core-only", "regcred"] and names(pods["s-portal"]) == ["regcred"])
    sa = {k: v.get("serviceAccountName") for k, v in pods.items()}
    check("serviceAccountName per part: platform (and its test), Portal, Apache, Portal test, demo Postgres (and its Job)",
          sa["s-platform"] == sa["s-platform-canary"] == "egeria-sa" and sa["s-portal"] == sa["s-portal-web"] == sa["s-portal-canary"] == "portal-sa"
          and sa["s-demo-postgres"] == sa["s-demo-postgres-init"] == "pg-sa" and sa["s-demo-kafka"] is None, str(sa))
    ds = renders(base)
    check("no serviceAccountName or imagePullSecrets is rendered by default",
          not any(("serviceAccountName" in (d["spec"]["template"]["spec"] if d["kind"] != "Pod" else d["spec"]) or "imagePullSecrets" in (d["spec"]["template"]["spec"] if d["kind"] != "Pod" else d["spec"]))
                  for d in ds if d["kind"] in ("Deployment", "StatefulSet", "Job", "Pod")))
    refuses("an imagePullSecrets entry with no name is refused", base + ["--set", "global.imagePullSecrets[0].foo=bar"], ["imagePullSecrets"])
    if failures:
        print("\n%d FAILED" % len(failures))
        sys.exit(1)
    print("\nall stack render tests passed")


main()
