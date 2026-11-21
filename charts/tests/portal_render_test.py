#!/usr/bin/env python3
"""Render tests for charts/egeria-portal (no cluster needed). Run: python3 charts/tests/portal_render_test.py
HELM=helm3 to use another Helm binary."""
import os
import subprocess
import sys

import yaml

HELM = os.environ.get("HELM", "helm")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHART = os.path.join(ROOT, "egeria-portal")
IMG = ["--set", "images.portal.repository=r.example/portal", "--set", "images.portal.tag=t",
       "--set", "images.apache.repository=r.example/apache", "--set", "images.apache.tag=t"]
BASE = ["--set", "platform.serviceName=egeria-platform"] + IMG
DEMO = ["-f", os.path.join(CHART, "values-demo.yaml")]
DIG = "sha256:" + "a" * 64
PROD = ["-f", os.path.join(CHART, "values-production.yaml"), "--set", "secrets.existingSecret=my-secrets",
        "--set", "tls.caSecret=my-ca", "--set", "persistence.storageClassName=fast",
        "--set", "images.portal.digest=" + DIG, "--set", "images.apache.digest=" + DIG]
CLUSTER_SCOPED = {"ClusterRole", "ClusterRoleBinding", "Namespace", "PersistentVolume", "StorageClass",
                  "CustomResourceDefinition", "SecurityContextConstraints", "PriorityClass", "IngressClass"}
failures = []


def template(args, release="r1"):
    p = subprocess.run([HELM, "template", release, CHART, "--namespace", "ns1"] + args, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def docs(out):
    return [d for d in yaml.safe_load_all(out) if d]


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else "  " + detail))
    if not cond:
        failures.append(name)


def renders(args):
    rc, out, err = template(args)
    if rc != 0:
        raise SystemExit("render failed unexpectedly: " + err)
    return docs(out)


def refuses(name, args, words):
    rc, out, err = template(args)
    check(name, rc != 0 and all(w in err for w in words), "rc=%s err=%s" % (rc, err[-300:]))


def kind(ds, k, name=None):
    return [d for d in ds if d["kind"] == k and (name is None or d["metadata"]["name"] == name)]


def env_of(dep, container):
    c = next(c for c in dep["spec"]["template"]["spec"]["containers"] if c["name"] == container)
    return {e["name"]: e for e in c.get("env", [])}


def main():
    subprocess.run([HELM, "dependency", "update", CHART], capture_output=True, check=True)
    for env, port, vs, user, host in (("quickstart", 9443, "qs-view-server", "erinoverview", "quickstart-pyegeria-web"),
                                      ("freshstart", 8443, "fs-view-server", "bootstrap", "freshstart-pyegeria-web")):
        for posture, extra in (("demo", DEMO), ("production", PROD)):
            ds = renders(extra + BASE + ["--set", "environment=" + env])
            tag = "%s/%s" % (env, posture)
            portal = kind(ds, "Deployment", "r1-portal")[0]
            e = env_of(portal, "portal")
            check(tag + ": platform URL, view server and user come from the environment",
                  e["EGERIA_PLATFORM_URL"]["value"] == "https://egeria-platform:%d" % port and e["EGERIA_VIEW_SERVER"]["value"] == vs
                  and e["EGERIA_USER"]["value"] == user, str(e["EGERIA_PLATFORM_URL"]))
            check(tag + ": EGERIA_ROOT_PATH is never / (a non-root user cannot write there)",
                  e["EGERIA_ROOT_PATH"]["value"] == "/app/dr-egeria" and e["EGERIA_INBOX_PATH"]["value"] != "/" and e["EGERIA_OUTBOX_PATH"]["value"] != "/")
            check(tag + ": password, JWT secret and token come from a Secret, never a literal",
                  all("valueFrom" in e[k] for k in ("EGERIA_USER_PASSWORD", "JWT_SECRET", "MCP_ACCESS_TOKEN")))
            check(tag + ": one pod, volume shared, so strategy Recreate", portal["spec"]["strategy"]["type"] == "Recreate" and portal["spec"]["replicas"] == 1)
            check(tag + ": readiness is an Egeria call, liveness is not",
                  "egeria-token" in str(portal["spec"]["template"]["spec"]["containers"][0]["readinessProbe"])
                  and "httpGet" in portal["spec"]["template"]["spec"]["containers"][0]["livenessProbe"])
            check(tag + ": the platform's client label is on the Portal pod", portal["spec"]["template"]["metadata"]["labels"].get("egeria.odpi.org/client") == "true")
            check(tag + ": no cluster-scoped kinds", not [d["kind"] for d in ds if d["kind"] in CLUSTER_SCOPED])
            # security
            for dep in kind(ds, "Deployment"):
                ps = dep["spec"]["template"]["spec"]
                ok = ps["securityContext"].get("runAsNonRoot") is True and ps["securityContext"]["seccompProfile"]["type"] == "RuntimeDefault" \
                    and all(c["securityContext"]["allowPrivilegeEscalation"] is False and c["securityContext"]["capabilities"]["drop"] == ["ALL"] for c in ps["containers"])
                check("%s: %s is non-root, no escalation, caps dropped" % (tag, dep["metadata"]["name"]), ok)
            # Apache config
            cm = kind(ds, "ConfigMap", "r1-portal-web-conf")[0]["data"]
            allconf = "\n".join(cm.values())
            check(tag + ": Apache proxies to this release's Portal Service, not a compose host",
                  "http://r1-portal:8000" in allconf and host not in allconf, host)
            check(tag + ": Apache serves HTTP on 8085 only (TLS ends at the Ingress)", "<VirtualHost *:8085>" in cm["fastapi-proxy.conf"] and "Listen 443" not in allconf and "SSLEngine" not in allconf)
            check(tag + ": /api keeps its 300 s proxy timeout", "timeout=300" in allconf)
            # demo vs production secrets
            secrets = kind(ds, "Secret")
            if posture == "demo":
                check(tag + ": the demo Secret is created", len(secrets) == 1 and set(secrets[0]["data"]) == {"jwt-secret", "mcp-access-token", "egeria-user-password"})
            else:
                check(tag + ": production renders no Secret (yours is required)", not secrets)
            # no secret value in a ConfigMap
            demo_pw = open(os.path.join(CHART, "files", env, "egeria-user-password")).read().strip()
            check(tag + ": no password in a ConfigMap or env value",
                  all(demo_pw not in str(c.get("data", "")) for c in kind(ds, "ConfigMap")) and all(e[k].get("value") != demo_pw for k in e))

    # OpenShift: no runAsUser/runAsGroup/fsGroup
    ds = renders(DEMO + BASE + ["--set", "global.openshift=true"])
    check("openshift: no runAsUser, runAsGroup or fsGroup is rendered",
          all(not ({"runAsUser", "runAsGroup", "fsGroup"} & set(d["spec"]["template"]["spec"]["securityContext"])) for d in kind(ds, "Deployment")))

    # refusals, each naming the setting
    refuses("refuses without platform.serviceName", DEMO + IMG, ["platform.serviceName"])
    refuses("refuses without image repository", DEMO + ["--set", "platform.serviceName=p"], ["images.portal.repository"])
    refuses("refuses more than one replica", DEMO + BASE + ["--set", "replicas=2"], ["replicas", "one pod"])
    refuses("refuses a bad environment", DEMO + BASE + ["--set", "environment=bogus"], ["environment"])
    refuses("production refuses without secrets.existingSecret", [a for a in PROD if a != "my-secrets"][:0] + ["-f", os.path.join(CHART, "values-production.yaml")] + BASE + ["--set", "persistence.storageClassName=fast", "--set", "images.portal.digest=" + DIG, "--set", "images.apache.digest=" + DIG, "--set", "tls.caSecret=c"], ["secrets.existingSecret"])
    refuses("production refuses tls.verify=false", PROD + BASE + ["--set", "tls.verify=false"], ["tls.verify"])
    refuses("production requires tls.caSecret", PROD + BASE + ["--set", "tls.caSecret="], ["tls.caSecret"])
    refuses("production requires image digests", ["-f", os.path.join(CHART, "values-production.yaml"), "--set", "secrets.existingSecret=s", "--set", "tls.caSecret=c", "--set", "persistence.storageClassName=f"] + BASE, ["digest"])
    refuses("production requires a StorageClass", PROD + BASE + ["--set", "persistence.storageClassName="], ["persistence.storageClassName"])
    refuses("production refuses demoMode", PROD + BASE + ["--set", "demoMode=true"], ["demoMode"])
    refuses("ingress needs a host", DEMO + BASE + ["--set", "ingress.enabled=true"], ["ingress.host"])
    refuses("production ingress needs TLS", PROD + BASE + ["--set", "ingress.enabled=true", "--set", "ingress.host=h.example"], ["ingress.tlsSecretName"])

    # optional pieces
    ds = renders(PROD + BASE + ["--set", "ingress.enabled=true", "--set", "ingress.host=h.example", "--set", "ingress.tlsSecretName=tls"])
    check("production renders an Ingress with TLS and a NetworkPolicy", len(kind(ds, "Ingress")) == 1 and len(kind(ds, "NetworkPolicy")) == 1
          and kind(ds, "Ingress")[0]["spec"]["tls"][0]["secretName"] == "tls")
    ds = renders(DEMO + BASE + ["--set", "content.cocoWorkbooks.existingClaim=wb", "--set", "exchange.loadingBay.existingClaim=lb"])
    vols = {v["name"]: v for v in kind(ds, "Deployment", "r1-portal")[0]["spec"]["template"]["spec"]["volumes"]}
    check("an existing claim is mounted, others are empty directories",
          vols["content-coco-workbooks"]["persistentVolumeClaim"]["claimName"] == "wb" and "emptyDir" in vols["content-work"]
          and vols["exchange-loading-bay"]["persistentVolumeClaim"]["readOnly"] is True)
    # two releases do not collide
    a = {(d["kind"], d["metadata"]["name"]) for d in renders(DEMO + BASE)}
    rc, out, _ = template(DEMO + BASE, release="r2")
    b = {(d["kind"], d["metadata"]["name"]) for d in docs(out)}
    check("two releases share no object name", not (a & b))
    # canary
    rc, out, _ = template(DEMO + BASE)
    check("helm test canary ends in a PASS line", "PASS: portal up, front door and Egeria token verified" in out)

    if failures:
        print("\n%d FAILED" % len(failures))
        sys.exit(1)
    print("\nall portal render tests passed")


main()
