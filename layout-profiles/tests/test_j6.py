"""Phase 1j J6 (D-J3): finding_id = sha256(defining-profile-id@major | rule | path), where the defining profile is the one whose file defines the rule (an
in-place replacement defines it anew in the overlay). Composed profile ids no longer enter the hash. Synthetic trees only."""
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import yaml

from recognizer.layout_profile import compose_profiles, load_profile
from recognizer.recognize import Recognizer, finding_id

PROFILES = Path(__file__).resolve().parent.parent / "profiles"
TREE = {"pyproject.toml": "[project]\nname='r'\n", "core/pyproject.toml": "[project]\nname='c'\n", "lib/pom.xml": "<project/>", "scripts/run.sh": "x",
        "tests/a.py": "x", "docs/a.md": "x", "docs/b.md": "x", "node_modules/x/package.json": "{}", "README.md": "x", "core/x.py": "x", ".github/w.yml": "x"}


def run(tmp_path, profile, out, files=TREE):
    lst = tmp_path / "t.tsv"
    lst.write_text("".join(f"{k}\t{len(v)}\n" for k, v in sorted(files.items())))
    Recognizer(profile).run(lst, tmp_path / out, per_file=True)
    rows = [json.loads(x) for x in (tmp_path / out / "findings.jsonl").read_text().splitlines()]
    return {(f["path"], f["rule_id"]): f["finding_id"] for f in rows}, rows


def overlay(tmp_path, name, **doc):
    (tmp_path / f"{name}.yaml").write_text(yaml.safe_dump({"profile_id": name, "version": "0.1.0", "status": "proposed", "applies_to": "code-repo",
                                                           "extends": ["code-repo-conventions"], "roles": ["component", "tooling"],
                                                           "relevance": {"primary": ["component"], "supporting": ["tooling"], "hidden": []}, "rules": [], **doc}))
    return load_profile(name, tmp_path)


def defined_by(p):
    return {r.id: r.origin for r in (*p.all_rules, *p.all_file_roles)}


def test_every_id_is_made_from_the_defining_profile(tmp_path):
    p = load_profile("code-repo-conventions", PROFILES)
    ids, rows = run(tmp_path, p, "o")
    by = defined_by(p)
    vers = dict(p.composed_of)
    for f in rows:
        o = by[f["rule_id"]]
        assert f["finding_id"] == hashlib.sha256(f"{o}@{vers[o].split('.')[0]}|{f['rule_id']}|{f['path']}".encode()).hexdigest()[:16]
    origins = {by[f["rule_id"]] for f in rows}
    assert {"code-repo-conventions", "code-repo", "generic-relevance"} <= origins       # three defining profiles in one run


def test_an_overlay_that_changes_nothing_keeps_every_id(tmp_path):
    a, _ = run(tmp_path, load_profile("code-repo-conventions", PROFILES), "a")
    b, _ = run(tmp_path, overlay(tmp_path, "mine"), "b")
    assert a == b and len(a) > 10


def test_an_overlay_that_only_sets_a_setting_keeps_the_ids_of_the_findings_it_does_not_change(tmp_path):
    a, _ = run(tmp_path, load_profile("code-repo-conventions", PROFILES), "a")
    b, _ = run(tmp_path, overlay(tmp_path, "mine", settings={"docs-min-files": 3}), "b")
    common = set(a) & set(b)
    assert all(a[k] == b[k] for k in common) and ("docs", "R-conv-docs") in set(a) - set(b)


def test_an_overlay_that_replaces_one_rule_changes_only_that_rules_ids(tmp_path):
    raw = yaml.safe_load((PROFILES / "code-repo-conventions.yaml").read_text())
    scripts = next(r for r in raw["rules"] if r["id"] == "R-conv-scripts")
    p = overlay(tmp_path, "mine", rules=[{**scripts, "match": {"path_glob": "*", "segment_regex": ["(?i)^scripts$"]}}])
    a, _ = run(tmp_path, load_profile("code-repo-conventions", PROFILES), "a")
    b, _ = run(tmp_path, p, "b")
    assert set(a) == set(b)
    changed = {k for k in a if a[k] != b[k]}
    assert changed and all(rid == "R-conv-scripts" for _, rid in changed)
    assert b[("scripts", "R-conv-scripts")] == hashlib.sha256(b"mine@0|R-conv-scripts|scripts").hexdigest()[:16]


def test_a_composition_keeps_the_ids_of_its_parts(tmp_path):
    a, _ = run(tmp_path, load_profile("code-repo-conventions", PROFILES), "a")
    c, _ = run(tmp_path, compose_profiles("code-repo-conventions,docs-site", PROFILES), "c")
    common = set(a) & set(c)
    assert len(common) > 10 and all(a[k] == c[k] for k in common)                     # the composite's own id (a+b) is not in the hash


def test_a_rule_keeps_its_id_whichever_profile_runs_it(tmp_path):
    g, _ = run(tmp_path, load_profile("generic-relevance", PROFILES), "g")
    a, _ = run(tmp_path, load_profile("code-repo-conventions", PROFILES), "a")
    hidden = [k for k in g if k[1].startswith("R-") and k in a]
    assert hidden and all(g[k] == a[k] for k in hidden)                               # e.g. node_modules, hidden by generic-relevance in both


def test_a_structural_rule_is_identified_by_the_profile_that_defines_it(tmp_path):
    w = load_profile("workspace-repo", PROFILES)
    files = {"svc/docker-compose.yml": "services: {}\n", "svc/app.py": "x"}
    ids, rows = run(tmp_path, w, "o", files)
    st = [f for f in rows if f.get("structure_rule_id")]
    assert st
    for f in st:
        sr = next(x for x in w.structural if x["id"] == f["structure_rule_id"])
        assert sr["origin"] == "workspace-repo" and f["finding_id"] == hashlib.sha256(f"workspace-repo@0|{f['rule_id']}|{f['path']}".encode()).hexdigest()[:16]


def test_the_major_version_of_the_defining_profile_counts():
    p = SimpleNamespace(profile_id="top", version="0.3.0", major="0", composed_of=(("top", "0.3.0"), ("base", "2.1.0")))
    assert finding_id(p, "R", "x", "base") == hashlib.sha256(b"base@2|R|x").hexdigest()[:16]
    assert finding_id(p, "R", "x", "top") == hashlib.sha256(b"top@0|R|x").hexdigest()[:16]
    assert finding_id(p, "R", "x") == hashlib.sha256(b"top@0|R|x").hexdigest()[:16]           # no origin: the run's profile (the pre-J6 id)


def test_the_configuration_hash_does_not_move_with_j6():
    from recognizer.configuration import canonical
    p = load_profile("workspace-repo", PROFILES)
    assert all("origin" not in s for s in canonical(p)["structural"])
