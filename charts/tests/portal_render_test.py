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
        "--set", "images.portal.digest=" + DIG, "--set", "images.apache.digest=" + DIG,
        "--set", "platform.userDirectorySecret=my-platform-secrets"]
CLUSTER_SCOPED = {"ClusterRole", "ClusterRoleBinding", "Namespace", "PersistentVolume", "StorageClass",
                  "CustomResourceDefinition", "SecurityContextConstraints", "PriorityClass", "IngressClass"}
failures = []


def template(args, release="r1"):
    p = subprocess.run([HELM, "template", release, CHART, "--namespace", "ns1"] + args, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def notes(args, release="r1"):
    """The NOTES text `helm install --dry-run` prints."""
    p = subprocess.run([HELM, "install", release, CHART, "--namespace", "ns1", "--dry-run=client"] + args, capture_output=True, text=True)
    return p.returncode, p.stdout.split("NOTES:", 1)[-1] if "NOTES:" in p.stdout else "", p.stderr


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
    refuses("production requires image digests", ["-f", os.path.join(CHART, "values-production.yaml"), "--set", "environment=freshstart", "--set", "secrets.existingSecret=s", "--set", "tls.caSecret=c", "--set", "persistence.storageClassName=f", "--set", "platform.userDirectorySecret=u"] + BASE, ["digest"])
    refuses("production requires a StorageClass", PROD + BASE + ["--set", "persistence.storageClassName="], ["persistence.storageClassName"])
    refuses("production refuses demoMode", PROD + BASE + ["--set", "demoMode=true"], ["demoMode"])
    refuses("ingress needs a host", DEMO + BASE + ["--set", "ingress.enabled=true"], ["ingress.host"])
    # PO-78: the freshstart Portal has no server-side API gate, so it is never exposed through an Ingress (or a Route made from it)
    PO78 = ["PO-78", "no server-side API gate", "port-forward"]
    refuses("production + freshstart + Ingress is refused (PO-78)", PROD + BASE + ["--set", "ingress.enabled=true", "--set", "ingress.host=h.example", "--set", "ingress.tlsSecretName=tls", "--set", "networkPolicy.enabled=true"], PO78)
    refuses("demo + freshstart + Ingress is refused (PO-78)", DEMO + BASE + ["--set", "environment=freshstart", "--set", "ingress.enabled=true", "--set", "ingress.host=h.example", "--set", "networkPolicy.enabled=true"], PO78)
    refuses("freshstart + Ingress with the OpenShift Route annotation is refused (PO-78): a Route is made from the Ingress", PROD + BASE + ["--set", "ingress.enabled=true", "--set", "ingress.host=h.example", "--set", "ingress.tlsSecretName=tls", "--set", "networkPolicy.enabled=true", "--set-string", "ingress.annotations.route\\.openshift\\.io/termination=edge", "--set", "global.openshift=true"], PO78)
    check("production + freshstart WITHOUT an Ingress still renders (port-forward)", bool(renders(PROD + BASE)))
    check("demo + freshstart WITHOUT an Ingress still renders (port-forward)", bool(renders(DEMO + BASE + ["--set", "environment=freshstart"])))
    check("the PO-78 refusal says why in words (the sign-in page is a screen only)", "sign-in page is a screen only" in template(PROD + BASE + ["--set", "ingress.enabled=true", "--set", "ingress.host=h.example"])[2])

    # optional pieces
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
    refuses("allowUngatedPortal is refused in production", PROD + BASE + ["--set", "allowUngatedPortal=true"], ["allowUngatedPortal"])
    # the Portal Service on 8000 is reachable only from the front door whenever there is an Ingress
    refuses("an Ingress requires networkPolicy.enabled", DEMO + BASE + ING + ["--set", "demoMode=true"], ["networkPolicy.enabled", "8000"])
    for tag, extra in (("demo/quickstart+demoMode", DEMO + BASE + NP + ING + ["--set", "demoMode=true"]),):
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
    rc, dm, _ = template(DEMO + BASE + ["--set", "demoMode=true"])
    tb = [l for l in dm.splitlines() if "TOKEN_BASE" in l]
    ro = [l for l in dm.splitlines() if "REDIRECT_OK" in l and "name:" in l]
    check("demoMode: TOKEN_BASE is the Portal Service, REDIRECT_OK true", tb and "r1-portal:8000" in tb[0] and ro and '"true"' in ro[0], str(tb + ro))
    check("the canary message names the address it used (not 'front door' when it went to 8000)", "via {os.environ['TOKEN_BASE']}" in dm and "through the front door (HTTP" not in dm)
    check("gated Portal (demoMode): the canary asserts that an empty token request without a session gets 401 (PO-68)", "a request with no password and no session is refused" in dm and "need(s == 401" in dm)
    rc, fs, _ = template(DEMO + BASE + ["--set", "environment=freshstart"])
    fro = [l for l in fs.splitlines() if "REDIRECT_OK" in l and "name:" in l]
    check("freshstart: REDIRECT_OK is true, so the canary runs the PO-68 401 check", fro and '"true"' in fro[0] and "need(s == 401" in fs, str(fro))
    rc, qs, _ = template(DEMO + BASE)
    tb = [l for l in qs.splitlines() if "TOKEN_BASE" in l]
    ro = [l for l in qs.splitlines() if "REDIRECT_OK" in l and "name:" in l]
    check("ungated quickstart: TOKEN_BASE is the front door, REDIRECT_OK false (so the PO-68 401 check is skipped)", tb and "r1-portal-web:8085" in tb[0] and ro and '"false"' in ro[0], str(tb + ro))
    check("the canary accepts a redirect on freshstart only", 'name: REDIRECT_OK, value: "true"' in out.replace("- {", "{") or "REDIRECT_OK" in out)

    # --- TR-123 ---
    # (2) production freshstart names the platform's user-directory Secret; demo keeps the default name (optional mount)
    noud = [a for a in PROD if a != "platform.userDirectorySecret=my-platform-secrets"][:-1]
    refuses("production freshstart without platform.userDirectorySecret is refused, naming it", noud + BASE, ["platform.userDirectorySecret", "egeria-user-directory.omsecrets"])
    vols = {v["name"]: v for v in kind(renders(PROD + BASE), "Deployment", "r1-portal")[0]["spec"]["template"]["spec"]["volumes"]}
    check("production: the user directory is mounted from the named Secret", vols["platform-userdir"]["secret"]["secretName"] == "my-platform-secrets")
    vols = {v["name"]: v for v in kind(renders(DEMO + BASE + ["--set", "environment=freshstart"]), "Deployment", "r1-portal")[0]["spec"]["template"]["spec"]["volumes"]}
    check("demo freshstart: the default <platform>-secrets is still used (the platform's demo Secret)", vols["platform-userdir"]["secret"]["secretName"] == "egeria-platform-secrets")
    # (3) pull Secrets and ServiceAccount on all three pods (Portal, Apache, test)
    rc, out, err = template(DEMO + BASE + ["--set", "imagePullSecrets[0]=regcred", "--set", "global.imagePullSecrets[0].name=shared", "--set", "serviceAccountName=portal-sa"])
    ds = docs(out)
    specs = [d["spec"]["template"]["spec"] for d in kind(ds, "Deployment")] + [d["spec"] for d in kind(ds, "Pod")]
    check("imagePullSecrets (own + global) and serviceAccountName are on the Portal, Apache and test pods",
          len(specs) == 3 and all([x["name"] for x in s["imagePullSecrets"]] == ["regcred", "shared"] and s["serviceAccountName"] == "portal-sa" for s in specs),
          str([(s.get("imagePullSecrets"), s.get("serviceAccountName")) for s in specs]))
    # (4) Apache gets the chart's tolerations and affinity, like the Portal
    ds = renders(DEMO + BASE + ["--set", "tolerations[0].key=dedicated", "--set", "tolerations[0].operator=Exists",
                                "--set", "affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[0].matchExpressions[0].key=zone",
                                "--set", "affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[0].matchExpressions[0].operator=Exists",
                                "--set", "nodeSelector.pool=egeria"])
    web = kind(ds, "Deployment", "r1-portal-web")[0]["spec"]["template"]["spec"]
    por = kind(ds, "Deployment", "r1-portal")[0]["spec"]["template"]["spec"]
    check("Apache has the same nodeSelector, tolerations and affinity as the Portal",
          all(web.get(k) and web.get(k) == por.get(k) for k in ("nodeSelector", "tolerations", "affinity")), str({k: web.get(k) for k in ("tolerations", "affinity")}))
    # (5) probes: today's numbers by default, overridable, handler fixed
    ds = renders(DEMO + BASE)
    pc = kind(ds, "Deployment", "r1-portal")[0]["spec"]["template"]["spec"]["containers"][0]
    ac = kind(ds, "Deployment", "r1-portal-web")[0]["spec"]["template"]["spec"]["containers"][0]
    check("default Portal probes keep the earlier numbers",
          pc["startupProbe"] == {"httpGet": {"path": "/", "port": "http"}, "periodSeconds": 10, "failureThreshold": 60}
          and pc["readinessProbe"] == {"httpGet": {"path": "/", "port": "http"}, "periodSeconds": 10, "timeoutSeconds": 5, "failureThreshold": 3}
          and pc["livenessProbe"] == {"httpGet": {"path": "/", "port": "http"}, "periodSeconds": 30, "timeoutSeconds": 10, "failureThreshold": 5},
          str({k: pc[k] for k in ("startupProbe", "readinessProbe", "livenessProbe")}))
    check("default Apache probes keep the earlier numbers",
          ac["readinessProbe"] == {"tcpSocket": {"port": "http"}, "periodSeconds": 10}
          and ac["livenessProbe"] == {"tcpSocket": {"port": "http"}, "periodSeconds": 30, "failureThreshold": 5}, str((ac["readinessProbe"], ac["livenessProbe"])))
    ds = renders(DEMO + BASE + ["--set", "probes.portal.startup.failureThreshold=120", "--set", "probes.portal.readiness.timeoutSeconds=9",
                                "--set", "probes.apache.liveness.periodSeconds=7", "--set", "probes.apache.readiness.initialDelaySeconds=3"])
    pc = kind(ds, "Deployment", "r1-portal")[0]["spec"]["template"]["spec"]["containers"][0]
    ac = kind(ds, "Deployment", "r1-portal-web")[0]["spec"]["template"]["spec"]["containers"][0]
    check("probe overrides reach the Portal and Apache, the checks stay GET / and TCP",
          pc["startupProbe"]["failureThreshold"] == 120 and pc["startupProbe"]["periodSeconds"] == 10 and pc["readinessProbe"]["timeoutSeconds"] == 9
          and pc["startupProbe"]["httpGet"]["path"] == "/" and ac["livenessProbe"]["periodSeconds"] == 7 and ac["readinessProbe"]["initialDelaySeconds"] == 3
          and "tcpSocket" in ac["livenessProbe"])
    refuses("a probe value that is not a timing is refused", DEMO + BASE + ["--set", "probes.portal.readiness.httpGet.path=/x"], ["probes.portal.readiness.httpGet", "not allowed"])
    # (7) PO-83: the Portal trusts X-Forwarded-For only from the Apache pods, named by a headless Service
    for tag, args in (("demo/quickstart", DEMO + BASE), ("demo/freshstart", DEMO + BASE + ["--set", "environment=freshstart"]), ("production/freshstart", PROD + BASE)):
        ds = renders(args)
        pe = env_of(kind(ds, "Deployment", "r1-portal")[0], "portal")
        check(tag + ": PORTAL_TRUSTED_PROXIES defaults to the headless Apache Service's full name", pe["PORTAL_TRUSTED_PROXIES"]["value"] == "r1-portal-web-hl.ns1.svc.cluster.local", str(pe.get("PORTAL_TRUSTED_PROXIES")))
        hl = kind(ds, "Service", "r1-portal-web-hl")
        web = kind(ds, "Deployment", "r1-portal-web")[0]
        check(tag + ": the headless Service has no cluster IP and selects exactly the Apache pods",
              len(hl) == 1 and hl[0]["spec"]["clusterIP"] == "None" and hl[0]["spec"]["selector"] == web["spec"]["selector"]["matchLabels"], str(hl))
    ds = renders(DEMO + BASE + ["--set-string", "trustedProxies= 10.0.0.0/8 \\, apache.example.org "])
    check("trustedProxies replaces the default; whitespace is stripped (an IP, a CIDR and a hostname may be mixed)",
          env_of(kind(ds, "Deployment", "r1-portal")[0], "portal")["PORTAL_TRUSTED_PROXIES"]["value"] == "10.0.0.0/8,apache.example.org")
    refuses("extraEnv cannot set PORTAL_TRUSTED_PROXIES", DEMO + BASE + ["--set", "extraEnv[0].name=PORTAL_TRUSTED_PROXIES", "--set", "extraEnv[0].value=0.0.0.0/0"], ["PORTAL_TRUSTED_PROXIES"])
    # (8) PO-83 behind an Ingress controller: its range is ADDED, narrow only, and a NOTES warning when it is missing
    HL = "r1-portal-web-hl.ns1.svc.cluster.local"
    def trusted(extra):
        return env_of(kind(renders(DEMO + BASE + extra), "Deployment", "r1-portal")[0], "portal")["PORTAL_TRUSTED_PROXIES"]["value"]
    check("ingressControllerCidr is ADDED to the default (the headless Apache Service stays)", trusted(["--set", "ingressControllerCidr=10.244.3.0/24"]) == HL + ",10.244.3.0/24", trusted(["--set", "ingressControllerCidr=10.244.3.0/24"]))
    check("it is added to an explicit trustedProxies too, and several ranges may be listed (comma, whitespace ignored)",
          trusted(["--set", "trustedProxies=192.168.1.5", "--set-string", "ingressControllerCidr=10.244.3.0/24 \\, 2001:db8::/80"]) == "192.168.1.5,10.244.3.0/24,2001:db8::/80")
    check("unset, the list is exactly the default", trusted([]) == HL)
    for wide in ("0.0.0.0/0", "::/0", "10.0.0.0/8", "10.244.0.0/15", "fd00::/8", "2001:db8::/48"):
        refuses("ingressControllerCidr " + wide + " is refused as too wide, in words", DEMO + BASE + ["--set-string", "ingressControllerCidr=" + wide], ["too wide", "never the pod network"])
    check("a /16 (IPv4) is the widest accepted", trusted(["--set", "ingressControllerCidr=10.244.0.0/16"]) == HL + ",10.244.0.0/16")
    ING = ["--set", "demoMode=true", "--set", "ingress.enabled=true", "--set", "ingress.host=h.example", "--set", "networkPolicy.enabled=true"]
    WARN = "Ingress controller's rate-limit budget"
    check("NOTES warns when an Ingress is on and no controller range is set", WARN in notes(DEMO + BASE + ING)[1])
    check("no warning once ingressControllerCidr is set", WARN not in notes(DEMO + BASE + ING + ["--set", "ingressControllerCidr=10.244.3.0/24"])[1])
    check("no warning when trustedProxies is set explicitly (the operator chose the list)", WARN not in notes(DEMO + BASE + ING + ["--set", "trustedProxies=10.244.3.0/24"])[1])
    check("no warning without an Ingress", WARN not in notes(DEMO + BASE)[1])
    # (6) the image message points at the docs
    refuses("a missing image repository points at charts/docs/kubernetes.md#images", DEMO + ["--set", "platform.serviceName=p"], ["charts/docs/kubernetes.md#images"])
    if failures:
        print("\n%d FAILED" % len(failures))
        sys.exit(1)
    print("\nall portal render tests passed")


main()
