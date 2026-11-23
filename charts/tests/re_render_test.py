#!/usr/bin/env python3
"""Render tests for charts/trellis-re (no cluster needed). Run: python3 charts/tests/re_render_test.py
HELM=helm3 to use another Helm binary."""
import os
import subprocess
import sys

import yaml

HELM = os.environ.get("HELM", "helm")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHART = os.path.join(ROOT, "trellis-re")
DIG = "sha256:" + "a" * 64
BASE = ["--set", "image.repository=r.example/re", "--set", "image.tag=t",
        "--set", "database.host=pg", "--set", "database.name=re", "--set", "database.user=re_rt", "--set", "database.existingSecret=re-db",
        "--set", "egeria.platformUrl=https://platform:9443", "--set", "egeria.daemon.userId=re", "--set", "egeria.daemon.existingSecret=re-egeria"]
DEMO = ["-f", os.path.join(CHART, "values-demo.yaml")]
PROD = ["-f", os.path.join(CHART, "values-production.yaml"), "--set", "image.digest=" + DIG, "--set", "secrets.existingSecret=re-secrets",
        "--set", "database.owner.user=re_owner", "--set", "database.owner.existingSecret=re-owner-db",
        "--set", "tls.caSecret=re-ca", "--set", "persistence.storageClassName=fast"]
CLUSTER_SCOPED = {"ClusterRole", "ClusterRoleBinding", "Namespace", "PersistentVolume", "StorageClass",
                  "CustomResourceDefinition", "SecurityContextConstraints", "PriorityClass", "IngressClass"}
failures = []


def template(args, release="r1"):
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


def without(args, value):
    """args minus one `--set value` pair."""
    i = args.index(value)
    return args[:i - 1] + args[i + 1:]


def kind(ds, k, name=None):
    return [d for d in ds if d["kind"] == k and (name is None or d["metadata"]["name"] == name)]


def env_of(dep, container):
    c = next(c for c in dep["spec"]["template"]["spec"]["containers"] if c["name"] == container)
    return {e["name"]: e for e in c.get("env", [])}


def main():
    ds = renders(DEMO + BASE)
    check("demo renders web, worker, Job, PVC, Secret, Service, test Pod", sorted(d["kind"] for d in ds) ==
          sorted(["Deployment", "Deployment", "Job", "PersistentVolumeClaim", "Secret", "Service", "Pod"]), str(sorted(d["kind"] for d in ds)))
    check("nothing is cluster-scoped", not [d for d in ds if d["kind"] in CLUSTER_SCOPED])
    web, worker = kind(ds, "Deployment", "r1-re-web")[0], kind(ds, "Deployment", "r1-re-worker")[0]
    job = kind(ds, "Job")[0]
    check("web runs `web` and the worker runs `worker`, the Job `schema-apply`, all on one image",
          web["spec"]["template"]["spec"]["containers"][0]["args"] == ["web"] and worker["spec"]["template"]["spec"]["containers"][0]["args"] == ["worker"]
          and job["spec"]["template"]["spec"]["containers"][0]["args"] == ["schema-apply"]
          and len({d["spec"]["template"]["spec"]["containers"][0]["image"] for d in (web, worker, job)}) == 1)
    # the schema split (TR-115): pods are external, the Job is the process that sends DDL
    we, wo, je = env_of(web, "web"), env_of(worker, "worker"), env_of(job, "schema")
    check("web and worker run RE_SCHEMA_MODE=external", we["RE_SCHEMA_MODE"]["value"] == "external" and wo["RE_SCHEMA_MODE"]["value"] == "external")
    check("the Job runs RE_SCHEMA_MODE=auto (it is the one that sends DDL)", je["RE_SCHEMA_MODE"]["value"] == "auto")
    check("the Job is a pre-install and pre-upgrade hook", job["metadata"]["annotations"]["helm.sh/hook"] == "pre-install,pre-upgrade")
    check("the Job and the pods use the runtime role's Secret by default (demo)",
          je["PGVECTOR_PASSWORD"]["valueFrom"]["secretKeyRef"]["name"] == "re-db" and we["PGVECTOR_PASSWORD"]["valueFrom"]["secretKeyRef"]["name"] == "re-db"
          and je["PGVECTOR_USER"]["value"] == "re_rt")
    own = ["--set", "database.owner.user=re_owner", "--set", "database.owner.existingSecret=re-owner-db", "--set", "database.owner.passwordKey=pw"]
    ds2 = renders(DEMO + BASE + own)
    je2, we2 = env_of(kind(ds2, "Job")[0], "schema"), env_of(kind(ds2, "Deployment", "r1-re-web")[0], "web")
    check("with an owner role the Job uses it and the pods keep the runtime role",
          je2["PGVECTOR_USER"]["value"] == "re_owner" and je2["PGVECTOR_PASSWORD"]["valueFrom"]["secretKeyRef"] == {"name": "re-owner-db", "key": "pw"}
          and we2["PGVECTOR_USER"]["value"] == "re_rt" and we2["PGVECTOR_PASSWORD"]["valueFrom"]["secretKeyRef"]["name"] == "re-db")
    check("no pod receives the owner credentials", "re-owner-db" not in str(kind(ds2, "Deployment")))
    # shared secrets: sessions and stored DB credentials are keyed on them, so every pod reads the same Secret
    check("web and worker read the same JWT and credential-key Secret", all(
          e[k]["valueFrom"]["secretKeyRef"]["name"] == "r1-re-secrets" for e in (we, wo) for k in ("RE_JWT_SECRET", "TRELLIS_DB_CREDENTIAL_KEY")))
    check("pyegeria logs go to a pod-local writable path (an arbitrary OpenShift UID cannot create /app/logs)", we["PYEGERIA_LOG_DIRECTORY"]["value"] == "/tmp/pyegeria-logs" and wo["PYEGERIA_LOG_DIRECTORY"]["value"] == "/tmp/pyegeria-logs")
    check("the web pod does not embed the worker loops", we["EMBED_WORKER"]["value"] == "0")
    check("Prefect, MLflow and Phoenix are off", all(we[k]["value"] == "false" for k in ("PREFECT_ENABLED", "OBSERVABILITY__MLFLOW__ENABLED", "OBSERVABILITY__PHOENIX__ENABLED")))
    sec = kind(ds, "Secret")[0]
    check("the demo Secret has jwt-secret and db-credential-key", sorted(sec["data"]) == ["db-credential-key", "jwt-secret"])
    # platform access: the pods carry the platform chart's client label so its NetworkPolicy lets them in
    check("web and worker carry the platform client label",
          all(d["spec"]["template"]["metadata"]["labels"].get("egeria.odpi.org/client") == "true" for d in (web, worker)))
    # security context
    ps = web["spec"]["template"]["spec"]["securityContext"]
    check("default: runs as the image's user with fsGroup", ps.get("runAsUser") == 1000 and ps.get("fsGroup") == 1000 and ps["runAsNonRoot"] is True)
    dso = renders(DEMO + BASE + ["--set", "global.openshift=true"])
    pso = kind(dso, "Deployment", "r1-re-web")[0]["spec"]["template"]["spec"]["securityContext"]
    check("global.openshift: no runAsUser, runAsGroup or fsGroup", not ({"runAsUser", "runAsGroup", "fsGroup"} & set(pso)))
    # storage
    pvc = kind(ds, "PersistentVolumeClaim")[0]
    check("the data claim is ReadWriteMany by default and kept on uninstall", pvc["spec"]["accessModes"] == ["ReadWriteMany"]
          and pvc["metadata"]["annotations"]["helm.sh/resource-policy"] == "keep")
    dsr = renders(DEMO + BASE + ["--set", "persistence.accessModes={ReadWriteOnce}"])
    check("accessModes can be ReadWriteOnce for a single-node cluster", kind(dsr, "PersistentVolumeClaim")[0]["spec"]["accessModes"] == ["ReadWriteOnce"])
    dse = renders(DEMO + BASE + ["--set", "persistence.existingClaim=mine"])
    check("an existing claim is used and none is created", not kind(dse, "PersistentVolumeClaim")
          and kind(dse, "Deployment", "r1-re-web")[0]["spec"]["template"]["spec"]["volumes"][0]["persistentVolumeClaim"]["claimName"] == "mine")
    # tls
    dst = renders(DEMO + BASE + ["--set", "tls.caSecret=my-ca", "--set", "tls.verify=true"])
    wt = kind(dst, "Deployment", "r1-re-web")[0]
    check("a CA Secret is mounted and PYEGERIA_CA_BUNDLE points at it", env_of(wt, "web")["PYEGERIA_CA_BUNDLE"]["value"] == "/etc/egeria-ca/ca.crt"
          and any(v.get("secret", {}).get("secretName") == "my-ca" for v in wt["spec"]["template"]["spec"]["volumes"]))
    # probes
    pc = web["spec"]["template"]["spec"]["containers"][0]
    check("web probes: /health liveness, /health/ready readiness", pc["livenessProbe"]["httpGet"]["path"] == "/health" and pc["readinessProbe"]["httpGet"]["path"] == "/health/ready")
    check("the worker has no port and no HTTP probe", "ports" not in worker["spec"]["template"]["spec"]["containers"][0]
          and "readinessProbe" not in worker["spec"]["template"]["spec"]["containers"][0])
    # production
    dp = renders(PROD + BASE)
    check("production renders", any(d["kind"] == "Job" for d in dp) and not kind(dp, "Secret"))
    check("production pins the image by digest", all(DIG in d["spec"]["template"]["spec"]["containers"][0]["image"] for d in kind(dp, "Deployment")))
    check("production creates no Secret (secrets come from existingSecret)", not kind(dp, "Secret"))
    check("production renders a NetworkPolicy for web and worker", sorted(d["metadata"]["name"] for d in kind(dp, "NetworkPolicy")) == ["r1-re-web", "r1-re-worker"])
    # refusals, each naming the setting
    refuses("refuses without image.repository", DEMO + without(BASE, "image.repository=r.example/re"), ["image.repository"])
    refuses("refuses without database.host", DEMO + BASE + ["--set", "database.host="], ["database.host"])
    refuses("refuses without database.existingSecret", DEMO + BASE + ["--set", "database.existingSecret="], ["database.existingSecret", "pre-install"])
    refuses("refuses without the daemon Secret", DEMO + BASE + ["--set", "egeria.daemon.existingSecret="], ["egeria.daemon.existingSecret"])
    refuses("refuses without egeria.platformUrl", DEMO + BASE + ["--set", "egeria.platformUrl="], ["egeria.platformUrl"])
    refuses("refuses a bad posture", BASE + ["--set", "posture=bogus"], ["posture"])
    refuses("refuses a bad llm.backend", DEMO + BASE + ["--set", "llm.backend=bogus"], ["llm.backend"])
    refuses("refuses zero workers", DEMO + BASE + ["--set", "worker.replicas=0"], ["worker.replicas"])
    refuses("production requires secrets.existingSecret", without(PROD, "secrets.existingSecret=re-secrets") + BASE, ["secrets.existingSecret"])
    refuses("production requires an image digest", without(PROD, "image.digest=" + DIG) + BASE, ["image.digest"])
    # TR-115: production must have a separate owner role, so the pods' runtime role never needs DDL (Architect read-back W1)
    refuses("production refuses without database.owner.user", without(PROD, "database.owner.user=re_owner") + BASE, ["database.owner.user", "no DDL rights"])
    refuses("production refuses without database.owner.existingSecret", without(PROD, "database.owner.existingSecret=re-owner-db") + BASE, ["database.owner.existingSecret"])
    refuses("production refuses an owner that is the runtime role", PROD + BASE + ["--set", "database.owner.user=re_rt"], ["same role", "database.user"])
    dpo = renders(PROD + BASE)
    jo = env_of(kind(dpo, "Job")[0], "schema")
    check("production Job runs as the owner role with the owner's Secret, the pods as the runtime role",
          jo["PGVECTOR_USER"]["value"] == "re_owner" and jo["PGVECTOR_PASSWORD"]["valueFrom"]["secretKeyRef"]["name"] == "re-owner-db"
          and env_of(kind(dpo, "Deployment", "r1-re-web")[0], "web")["PGVECTOR_USER"]["value"] == "re_rt")
    check("demo may keep one role (the defaults)", bool(renders(DEMO + BASE)))
    refuses("production requires tls.verify", PROD + BASE + ["--set", "tls.verify=false"], ["tls.verify"])
    refuses("production requires a StorageClass or claim", without(PROD, "persistence.storageClassName=fast") + BASE, ["persistence.storageClassName"])
    refuses("production Ingress needs TLS", PROD + BASE + ["--set", "ingress.enabled=true", "--set", "ingress.host=h.example"], ["ingress.tlsSecretName"])
    refuses("an Ingress needs a host", DEMO + BASE + ["--set", "ingress.enabled=true"], ["ingress.host"])
    refuses("extraEnv cannot override what the chart owns", DEMO + BASE + ["--set", "extraEnv[0].name=RE_SCHEMA_MODE", "--set", "extraEnv[0].value=auto"], ["RE_SCHEMA_MODE"])
    ds3 = renders(DEMO + BASE + ["--set", "extraEnv[0].name=MY_SETTING", "--set-string", "extraEnv[0].value=1"])
    check("extraEnv reaches web and worker", all(env_of(kind(ds3, "Deployment", n)[0], c)["MY_SETTING"]["value"] == "1" for n, c in (("r1-re-web", "web"), ("r1-re-worker", "worker"))))
    ing = renders(DEMO + BASE + ["--set", "ingress.enabled=true", "--set", "ingress.host=h.example"])
    check("an Ingress points at the web Service on its http port", kind(ing, "Ingress")[0]["spec"]["rules"][0]["http"]["paths"][0]["backend"]["service"]["name"] == "r1-re-web")
    # Prefect worker (increment 2): off by default; on, a worker deployment of the SAME image
    check("Prefect is off by default: no Prefect worker, PREFECT_ENABLED false", not [d for d in ds if d["metadata"]["name"] == "r1-re-prefect-worker"] and we["PREFECT_ENABLED"]["value"] == "false")
    PF = ["--set", "prefect.enabled=true", "--set", "prefect.apiUrl=http://prefect-server:4200/api"]
    dpf = renders(DEMO + BASE + PF)
    pw = kind(dpf, "Deployment", "r1-re-prefect-worker")[0]
    pwc = pw["spec"]["template"]["spec"]["containers"][0]
    wfe, pfe = env_of(kind(dpf, "Deployment", "r1-re-worker")[0], "worker"), env_of(pw, "prefect-worker")
    check("the Prefect worker runs the `prefect-worker` role on the SAME image as web and worker (one commit, which RE requires to dispatch)",
          pwc["args"] == ["prefect-worker"] and pwc["image"] == kind(dpf, "Deployment", "r1-re-web")[0]["spec"]["template"]["spec"]["containers"][0]["image"])
    check("web, worker and the Prefect worker all get PREFECT_ENABLED true, the API URL and the pool", all(
          e["PREFECT_ENABLED"]["value"] == "true" and e["PREFECT_API_URL"]["value"] == "http://prefect-server:4200/api" and e["PREFECT_WORK_POOL"]["value"] == "resource-explorer-pool"
          for e in (env_of(kind(dpf, "Deployment", "r1-re-web")[0], "web"), wfe, pfe)))
    check("the Prefect worker is external-mode like the others (it runs steps that read the registry)", pfe["RE_SCHEMA_MODE"]["value"] == "external")
    ic = pw["spec"]["template"]["spec"]["initContainers"][0]
    check("an init step makes the work pool first (prefect deploy needs it to exist)", ic["name"] == "work-pool" and "work-pool create" in ic["args"][0] and "--type process" in ic["args"][0])
    check("the Prefect worker mounts the shared data claim, has no port and no HTTP probe", any(v["name"] == "data" for v in pw["spec"]["template"]["spec"]["volumes"])
          and "ports" not in pwc and "readinessProbe" not in pwc)
    check("the Prefect worker carries the platform client label", pw["spec"]["template"]["metadata"]["labels"].get("egeria.odpi.org/client") == "true")
    dpk = renders(DEMO + BASE + PF + ["--set", "prefect.apiKeySecret=pf-key", "--set", "prefect.dispatchSteps=survey"])
    check("an API key Secret and the dispatch steps reach the pods; the key is read from the Secret, never rendered",
          env_of(kind(dpk, "Deployment", "r1-re-prefect-worker")[0], "prefect-worker")["PREFECT_API_KEY"]["valueFrom"]["secretKeyRef"] == {"name": "pf-key", "key": "api-key"}
          and env_of(kind(dpk, "Deployment", "r1-re-web")[0], "web")["PREFECT_DISPATCH_STEPS"]["value"] == "survey")
    dpp = renders(PROD + BASE + PF)
    check("production + Prefect renders a NetworkPolicy for the Prefect worker too", "r1-re-prefect-worker" in [d["metadata"]["name"] for d in kind(dpp, "NetworkPolicy")])
    tp = kind(dpf, "Pod")[0]["spec"]["containers"][0]
    check("with Prefect the helm test also waits for an ONLINE worker on the pool", "workers/filter" in tp["args"][0] and {e["name"] for e in tp["env"]} >= {"PREFECT_API_URL", "PREFECT_WORK_POOL"})
    refuses("Prefect enabled needs prefect.apiUrl", DEMO + BASE + ["--set", "prefect.enabled=true"], ["prefect.apiUrl", "does not run a Prefect server"])
    refuses("extraEnv cannot override the Prefect settings the chart owns", DEMO + BASE + PF + ["--set", "extraEnv[0].name=PREFECT_API_URL", "--set", "extraEnv[0].value=x"], ["PREFECT_API_URL"])
    # A2A (increment 3): off by default; on, a Service-only deployment of the SAME image on its own port, without the Egeria service account
    check("A2A is off by default: nothing named re-a2a renders", not [d for d in ds if "re-a2a" in d["metadata"]["name"]])
    check("an install without a2a renders exactly as before (same kinds, same names)", sorted((d["kind"], d["metadata"]["name"]) for d in ds) ==
          sorted((d["kind"], d["metadata"]["name"]) for d in renders(DEMO + BASE + ["--set", "a2a.enabled=false"])))
    dA = renders(DEMO + BASE + ["--set", "a2a.enabled=true"])
    aw = kind(dA, "Deployment", "r1-re-a2a")[0]
    ac = aw["spec"]["template"]["spec"]["containers"][0]
    ae, we2 = env_of(aw, "a2a"), env_of(kind(dA, "Deployment", "r1-re-web")[0], "web")
    check("the A2A pod runs the `a2a` role on the SAME image as web", ac["args"] == ["a2a"] and ac["image"] == kind(dA, "Deployment", "r1-re-web")[0]["spec"]["template"]["spec"]["containers"][0]["image"])
    check("PORT is set explicitly to the A2A port, so the image's PORT=8810 cannot leak through", ae["PORT"]["value"] == "8100" and ac["ports"][0]["containerPort"] == 8100)
    check("A2A_PUBLIC_URL defaults to the in-cluster Service URL", ae["A2A_PUBLIC_URL"]["value"] == "http://r1-re-a2a:8100")
    dAu = renders(DEMO + BASE + ["--set", "a2a.enabled=true", "--set", "a2a.publicUrl=https://a2a.example.org", "--set", "a2a.port=9000"])
    check("a2a.publicUrl and a2a.port are honoured", env_of(kind(dAu, "Deployment", "r1-re-a2a")[0], "a2a")["A2A_PUBLIC_URL"]["value"] == "https://a2a.example.org"
          and env_of(kind(dAu, "Deployment", "r1-re-a2a")[0], "a2a")["PORT"]["value"] == "9000")
    check("A2A_ALLOW_ANONYMOUS is false", ae["A2A_ALLOW_ANONYMOUS"]["value"] == "false")
    svc = kind(dA, "Service", "r1-re-a2a")[0]
    check("a ClusterIP Service only: no Ingress, no other exposure", svc["spec"].get("type", "ClusterIP") == "ClusterIP" and not kind(dA, "Ingress"))
    check("the A2A pod does not get RE's Egeria service account (least privilege)", "RE_DAEMON_USER_ID" not in ae and "RE_DAEMON_USER_PASSWORD" not in ae)
    dAs = renders(DEMO + BASE + ["--set", "a2a.enabled=true", "--set", "a2a.serviceAccount=true"])
    check("a2a.serviceAccount=true is the explicit opt-in to the service account", "RE_DAEMON_USER_PASSWORD" in env_of(kind(dAs, "Deployment", "r1-re-a2a")[0], "a2a"))
    check("it uses the RUNTIME database role in external mode, never the owner", ae["RE_SCHEMA_MODE"]["value"] == "external" and ae["PGVECTOR_USER"]["value"] == "re_rt"
          and "re-owner-db" not in str(aw))
    same = ["JWT" , "RE_JWT_SECRET", "TRELLIS_DB_CREDENTIAL_KEY", "EGERIA_PLATFORM_URL", "EGERIA_VIEW_SERVER", "PYEGERIA_SSL_VERIFY", "LLM__BACKEND", "EMBEDDINGS__DEVICE",
            "PGVECTOR_HOST", "PGVECTOR_PASSWORD", "PGVECTOR_SCHEMA"]
    check("A2A reads the same secrets, Egeria, database and LLM settings as web", all(ae[k] == we2[k] for k in same if k != "JWT"))
    dAl = renders(DEMO + BASE + ["--set", "a2a.enabled=true", "--set", "llm.backend=openai", "--set", "llm.ollama.baseUrl=http://ollama:11434",
                                 "--set", "extraEnvFrom[0].secretRef.name=llm-keys"])
    pa, pw_ = kind(dAl, "Deployment", "r1-re-a2a")[0]["spec"]["template"]["spec"]["containers"][0], kind(dAl, "Deployment", "r1-re-web")[0]["spec"]["template"]["spec"]["containers"][0]
    check("the LLM settings and the API-key envFrom reach A2A exactly as they reach web",
          {e["name"]: e.get("value") for e in pa["env"] if e["name"].startswith("LLM__")} == {e["name"]: e.get("value") for e in pw_["env"] if e["name"].startswith("LLM__")}
          and pa["envFrom"] == pw_["envFrom"] == [{"secretRef": {"name": "llm-keys"}}])
    check("A2A has probes on /health only (no database in it)", ac["livenessProbe"]["httpGet"]["path"] == "/health" and ac["readinessProbe"]["httpGet"]["path"] == "/health")
    dAp = renders(PROD + BASE + ["--set", "a2a.enabled=true"])
    anp = [d for d in kind(dAp, "NetworkPolicy") if d["metadata"]["name"] == "r1-re-a2a"][0]
    check("production: a NetworkPolicy lets anything that can reach the Service in on the A2A port only (and the helm test pod is covered by that)",
          anp["spec"]["ingress"] == [{"ports": [{"protocol": "TCP", "port": 8100}]}] and anp["spec"]["policyTypes"] == ["Ingress"])
    refuses("A2A refuses more than one replica (the context store is in memory)", DEMO + BASE + ["--set", "a2a.enabled=true", "--set", "a2a.replicas=2"], ["a2a.replicas", "in memory"])
    refuses("A2A_ALLOW_ANONYMOUS cannot be passed through extraEnv, in words", DEMO + BASE + ["--set", "a2a.enabled=true", "--set", "extraEnv[0].name=A2A_ALLOW_ANONYMOUS", "--set-string", "extraEnv[0].value=true"],
            ["A2A_ALLOW_ANONYMOUS", "bearer-token gate"])
    refuses("extraEnv cannot override A2A_PUBLIC_URL or PORT", DEMO + BASE + ["--set", "a2a.enabled=true", "--set", "extraEnv[0].name=PORT", "--set", "extraEnv[0].value=1"], ["PORT"])
    refuses("production + A2A still needs secrets.existingSecret (the JWT secret that verifies app tokens)", without(PROD, "secrets.existingSecret=re-secrets") + BASE + ["--set", "a2a.enabled=true"], ["secrets.existingSecret"])
    ta = kind(dA, "Pod")[0]["spec"]["containers"][0]["args"][0]
    check("with A2A the helm test checks /health, the public index, and that an anonymous call is refused with a WWW-Authenticate challenge",
          "http://r1-re-a2a:8100" in ta and "$a2a/health" in ta and "agents.json" in ta and "www-authenticate" in ta.lower())
    # helm test
    t = kind(ds, "Pod")[0]
    check("the helm test pod is a test hook that reaches the web Service", t["metadata"]["annotations"]["helm.sh/hook"] == "test"
          and "http://r1-re-web:8810" in t["spec"]["containers"][0]["args"][0])
    # --- the worker waits for the view server to be ACTIVE (init container); the web does not ---
    def inits(ds, name_suffix):
        dep = next(d for d in ds if d["kind"] == "Deployment" and d["metadata"]["name"].endswith(name_suffix))
        return dep["spec"]["template"]["spec"].get("initContainers", [])
    ds = renders(DEMO + BASE)
    w = inits(ds, "re-worker")
    check("the worker has the wait-for-egeria init container", [c["name"] for c in w] == ["wait-for-egeria"], str(w))
    check("the web has no init container (it reports Egeria unreachable instead of waiting)", inits(ds, "re-web") == [])
    check("no other RE Deployment or Job gets the wait", all(not d["spec"]["template"]["spec"].get("initContainers") for d in ds if d["kind"] in ("Deployment", "Job") and not d["metadata"]["name"].endswith("re-worker")))
    ie = {e["name"]: e for e in w[0]["env"]}
    check("the wait targets the platform URL and view server", ie["BASE"]["value"] == "https://platform:9443" and ie["SERVERS"]["value"] == "qs-view-server", str(ie["BASE"]) + str(ie["SERVERS"]))
    check("the wait takes the password only from the daemon Secret (secretKeyRef), the user as a plain value",
          ie["WAIT_PASSWORD"]["valueFrom"]["secretKeyRef"] == {"name": "re-egeria", "key": "password"} and "value" not in ie["WAIT_PASSWORD"] and ie["WAIT_USER"]["value"] == "re")
    script = w[0]["command"][2]
    check("the password is not put in argv or echoed (stdin only)", '--data @-' in script and 'echo "$WAIT_PASSWORD' not in script and '-d "' not in script and "WAIT_PASSWORD\"" not in script.replace('"$WAIT_PASSWORD"', ""))
    check("the wait is bounded and says why it failed", "end=$(( $(date +%s) + TIMEOUT ))" in script and "exit 1" in script and "allowed to list active servers" in script and "waiting:" in script)
    check("demo: the wait skips TLS verification like the platform canary", ie["STRICT"]["value"] == "false" and "curl -s -k" in script)
    ds = renders(DEMO + BASE + ["--set", "egeria.waitTimeoutSeconds=1200"])
    check("egeria.waitTimeoutSeconds reaches the init container", {e["name"]: e for e in inits(ds, "re-worker")[0]["env"]}["TIMEOUT"]["value"] == "1200")
    ds = renders(PROD + BASE + ["--set", "egeria.platformUrl=https://platform:8443"])
    wp = inits(ds, "re-worker")[0]
    pe = {e["name"]: e for e in wp["env"]}
    check("production: the wait verifies TLS with the CA Secret (--cacert from the mounted ca.crt)", pe["STRICT"]["value"] == "true" and pe["CA_FILE"]["value"] == "/etc/egeria-ca/ca.crt"
          and "--cacert $CA_FILE" in wp["command"][2] and any(m["mountPath"] == "/etc/egeria-ca" for m in wp["volumeMounts"]))
    check("production: the wait does not use -k when verifying", "STRICT\" = true" in wp["command"][2] or '"$STRICT" = true' in wp["command"][2])
    if failures:
        print("\n%d FAILED" % len(failures))
        sys.exit(1)
    print("\nall RE render tests passed")


main()
