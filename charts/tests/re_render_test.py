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
    refuses("production requires tls.verify", PROD + BASE + ["--set", "tls.verify=false"], ["tls.verify"])
    refuses("production requires a StorageClass or claim", without(PROD, "persistence.storageClassName=fast") + BASE, ["persistence.storageClassName"])
    refuses("production Ingress needs TLS", PROD + BASE + ["--set", "ingress.enabled=true", "--set", "ingress.host=h.example"], ["ingress.tlsSecretName"])
    refuses("an Ingress needs a host", DEMO + BASE + ["--set", "ingress.enabled=true"], ["ingress.host"])
    refuses("extraEnv cannot override what the chart owns", DEMO + BASE + ["--set", "extraEnv[0].name=RE_SCHEMA_MODE", "--set", "extraEnv[0].value=auto"], ["RE_SCHEMA_MODE"])
    ds3 = renders(DEMO + BASE + ["--set", "extraEnv[0].name=MY_SETTING", "--set-string", "extraEnv[0].value=1"])
    check("extraEnv reaches web and worker", all(env_of(kind(ds3, "Deployment", n)[0], c)["MY_SETTING"]["value"] == "1" for n, c in (("r1-re-web", "web"), ("r1-re-worker", "worker"))))
    ing = renders(DEMO + BASE + ["--set", "ingress.enabled=true", "--set", "ingress.host=h.example"])
    check("an Ingress points at the web Service on its http port", kind(ing, "Ingress")[0]["spec"]["rules"][0]["http"]["paths"][0]["backend"]["service"]["name"] == "r1-re-web")
    # helm test
    t = kind(ds, "Pod")[0]
    check("the helm test pod is a test hook that reaches the web Service", t["metadata"]["annotations"]["helm.sh/hook"] == "test"
          and "http://r1-re-web:8810" in t["spec"]["containers"][0]["args"][0])
    if failures:
        print("\n%d FAILED" % len(failures))
        sys.exit(1)
    print("\nall RE render tests passed")


main()
