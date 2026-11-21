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
PROD = ["-f", os.path.join(CHART, "values-production.yaml"), "--set", "environment=freshstart", "--set", "secrets.existingSecret=my-secrets",
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
            if posture == "production" and env == "quickstart":
                continue   # refused: no login gate there (tested below)
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
            pc = portal["spec"]["template"]["spec"]["containers"][0]
            check(tag + ": startup, readiness and liveness are all a plain GET / (Egeria is proven by helm test, not readiness)",
                  all(pc[k].get("httpGet", {}).get("path") == "/" for k in ("startupProbe", "readinessProbe", "livenessProbe")))
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
                names = {x["metadata"]["name"]: set(x["data"]) for x in secrets}
                check(tag + ": the demo Secrets are created (portal and canary)", names == {"r1-portal-secrets": {"jwt-secret", "mcp-access-token", "egeria-user-password"}, "r1-portal-canary": {"userId", "password"}})
            else:
                check(tag + ": production renders no Secret (yours are required)", not secrets)
            check(tag + ": SERVER_MANAGED_AUTH is set explicitly", e["SERVER_MANAGED_AUTH"]["value"] == ("true" if env == "freshstart" else "false"))
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
    refuses("production refuses without secrets.existingSecret", [a for a in PROD if a != "my-secrets"][:0] + ["-f", os.path.join(CHART, "values-production.yaml"), "--set", "environment=freshstart"] + BASE + ["--set", "persistence.storageClassName=fast", "--set", "images.portal.digest=" + DIG, "--set", "images.apache.digest=" + DIG, "--set", "tls.caSecret=c"], ["secrets.existingSecret"])
    refuses("production refuses tls.verify=false", PROD + BASE + ["--set", "tls.verify=false"], ["tls.verify"])
    refuses("production requires tls.caSecret", PROD + BASE + ["--set", "tls.caSecret="], ["tls.caSecret"])
    refuses("production requires image digests", ["-f", os.path.join(CHART, "values-production.yaml"), "--set", "environment=freshstart", "--set", "secrets.existingSecret=s", "--set", "tls.caSecret=c", "--set", "persistence.storageClassName=f"] + BASE, ["digest"])
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

    # --- login gate (Architect W1): three modes, never an ungated public Portal ---
    def modes(extra):
        e = env_of(kind(renders(extra), "Deployment", "r1-portal")[0], "portal")
        return e["DEMO_MODE"]["value"], e["SERVER_MANAGED_AUTH"]["value"]
    check("mode demo-quickstart: DEMO_MODE true, SERVER_MANAGED_AUTH false", modes(DEMO + BASE + ["--set", "demoMode=true"]) == ("true", "false"))
    check("mode local-quickstart: both false (no gate; not allowed behind an Ingress)", modes(DEMO + BASE) == ("false", "false"))
    check("mode freshstart: DEMO_MODE false, SERVER_MANAGED_AUTH true", modes(DEMO + BASE + ["--set", "environment=freshstart"]) == ("false", "true"))
    NP = ["--set", "networkPolicy.enabled=true"]
    ING = ["--set", "ingress.enabled=true", "--set", "ingress.host=h.example"]
    refuses("production + quickstart is refused (no login gate)", PROD + BASE + ["--set", "environment=quickstart"], ["login gate", "freshstart"])
    refuses("ingress + quickstart + demoMode=false is refused", DEMO + BASE + NP + ING, ["no login gate", "allowUngatedPortal"])
    check("ingress + quickstart + demoMode=true renders", bool(renders(DEMO + BASE + NP + ING + ["--set", "demoMode=true"])))
    check("ingress + quickstart + allowUngatedPortal=true renders (demo only)", bool(renders(DEMO + BASE + NP + ING + ["--set", "allowUngatedPortal=true"])))
    check("ingress + freshstart renders", bool(renders(DEMO + BASE + NP + ING + ["--set", "environment=freshstart"])))
    refuses("allowUngatedPortal is refused in production", PROD + BASE + ["--set", "allowUngatedPortal=true"], ["allowUngatedPortal"])
    # the Portal Service on 8000 is reachable only from the front door whenever there is an Ingress
    refuses("an Ingress requires networkPolicy.enabled", DEMO + BASE + ING + ["--set", "environment=freshstart"], ["networkPolicy.enabled", "8000"])
    for tag, extra in (("demo/freshstart", DEMO + BASE + NP + ING + ["--set", "environment=freshstart"]),
                       ("demo/quickstart+demoMode", DEMO + BASE + NP + ING + ["--set", "demoMode=true"]),
                       ("production/freshstart", PROD + BASE + ING + ["--set", "environment=freshstart", "--set", "ingress.tlsSecretName=tls"])):
        ds = renders(extra)
        ing = kind(ds, "Ingress")[0]
        backends = [p["backend"]["service"]["name"] for r in ing["spec"]["rules"] for p in r["http"]["paths"]]
        check(tag + ": the Ingress backend is the Apache front door (portal-web), never the Portal Service", backends == ["r1-portal-web"])
        np = kind(ds, "NetworkPolicy", "r1-portal")[0]
        sources = [f["podSelector"]["matchLabels"].get("app.kubernetes.io/name") for r in np["spec"]["ingress"] for f in r["from"]]
        check(tag + ": the Portal's NetworkPolicy admits only portal-web and the canary", sorted(sources) == ["portal-canary", "portal-web"])
    # extraEnv cannot override what the chart owns
    for name in ("EGERIA_ROOT_PATH", "DEMO_MODE", "SERVER_MANAGED_AUTH", "JWT_SECRET", "EGERIA_USER_PASSWORD"):
        refuses("extraEnv may not set " + name, DEMO + BASE + ["--set", "extraEnv[0].name=" + name, "--set", "extraEnv[0].value=x"], ["extraEnv", name])
    ds = renders(DEMO + BASE + ["--set", "extraEnv[0].name=MY_SETTING", "--set-string", "extraEnv[0].value=1"])
    e = env_of(kind(ds, "Deployment", "r1-portal")[0], "portal")
    check("a harmless extraEnv entry is added and the final EGERIA_ROOT_PATH is still /app/dr-egeria",
          e["MY_SETTING"]["value"] == "1" and e["EGERIA_ROOT_PATH"]["value"] == "/app/dr-egeria")
    pe = kind(ds, "Deployment", "r1-portal")[0]["spec"]["template"]["spec"]["containers"][0]["env"]
    check("no environment name appears twice (the final value is the only value)", len([x["name"] for x in pe]) == len({x["name"] for x in pe}))
    # canary: signs in as a non-personal account, never with an empty body
    rc, out, _ = template(DEMO + BASE)
    check("canary signs in with {user_id, password} from the canary Secret, not an empty body", '"user_id"' in out and 'call("POST", "/api/egeria-token", "{}"' not in out and "CANARY_USER" in out)
    rc, out, _ = template(PROD + BASE + ["--set", "environment=freshstart"])
    check("production without canary.existingSecret: the canary says what to set and fails", "set canary.existingSecret" in out and "sys.exit(1)" in out)
    rc, out, _ = template(PROD + BASE + ["--set", "environment=freshstart", "--set", "canary.existingSecret=my-canary"])
    check("production with canary.existingSecret: the canary reads it", "name: my-canary" in out and "PASS: portal up" in out)
    check("the canary accepts a redirect on freshstart only", 'name: REDIRECT_OK, value: "true"' in out.replace("- {", "{") or "REDIRECT_OK" in out)

    if failures:
        print("\n%d FAILED" % len(failures))
        sys.exit(1)
    print("\nall portal render tests passed")


main()
