"""M5b: Dan's tightenings (build output needs corroboration, worktree copies need a .git file, log and backup files hide as files only, a declared
submodule is not vendored) and the four new rules (.ipynb_checkpoints, exchange-*/distribution-hub, `private` in a certificate folder). Synthetic only."""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from recognizer import manifests as mf
from recognizer.layout_profile import ProfileError, load_profile, parse_profile
from recognizer.recognize import Recognizer, name_tokens

PROFILES = Path(__file__).resolve().parent.parent / "profiles"


def run(tmp_path, files, profile="egeria-workspace", out="out", source=False, name="tree"):
    """files: path -> content (str). Writes the tree when a blob source is wanted. Returns per-file findings by path and the class table."""
    root = tmp_path / name
    for rel, content in files.items():
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content)
    lst = tmp_path / f"{name}.tsv"
    lst.write_text("".join(f"{p}\t{len(files[p].encode())}\n" for p in sorted(files)))

    class Rec:
        def __init__(self):
            self.inner, self.asked = mf.FileSource(str(root)), []

        def read(self, path, max_bytes):
            self.asked.append(path)
            return self.inner.read(path, max_bytes)

        def close(self):
            pass
    src = Rec() if source else None
    rec = Recognizer(load_profile(profile, PROFILES), blob_source=src)
    c = rec.run(lst, tmp_path / out, per_file=True)
    pf = {x["path"]: x for x in map(json.loads, (tmp_path / out / "findings-files.jsonl").read_text().splitlines())}
    return SimpleNamespace(c=c, pf=pf, rec=rec, src=src, out=tmp_path / out)


def rule_of(r, path):
    return (r.pf[path]["rule_id"], r.pf[path]["relevance"]) if path in r.pf else None


# ---- build output: corroboration or it is shown ---------------------------------------------------------------------------------------
@pytest.mark.parametrize("name", ["build", "target", "dist", ".next"])
def test_a_build_folder_with_a_manifest_beside_it_is_hidden(tmp_path, name):
    r = run(tmp_path, {"app/package.json": "{}", f"app/{name}/bundle.js": "x", f"app/{name}/sub/x.map": "x"})
    assert rule_of(r, f"app/{name}/bundle.js") == ("R-gen-build-output", "hidden")                 # source-like files inside do not matter when a manifest corroborates
    assert r.pf[f"app/{name}/sub/x.map"]["confidence"] == "medium"


@pytest.mark.parametrize("name", ["build", "target", "dist", ".next"])
def test_a_build_folder_with_no_manifest_but_no_source_below_it_is_hidden(tmp_path, name):
    r = run(tmp_path, {f"x/{name}/a.class": "x", f"x/{name}/lib/b.jar": "x", "x/README.txt": "x"})
    assert rule_of(r, f"x/{name}/a.class") == ("R-gen-build-output-no-source", "hidden") and rule_of(r, f"x/{name}/lib/b.jar")[1] == "hidden"


@pytest.mark.parametrize("name", ["build", "target", "dist", ".next"])
def test_a_build_folder_with_no_manifest_and_source_inside_is_shown_with_low_confidence(tmp_path, name):
    r = run(tmp_path, {f"x/{name}/tool.py": "x", f"x/{name}/data.csv": "x", "x/README.txt": "x"})
    for p in (f"x/{name}/tool.py", f"x/{name}/data.csv"):
        f = r.pf[p]
        assert f["rule_id"] == "R-gen-build-output-unconfirmed" and f["relevance"] == "supporting" and f["role"] == "generated" and f["confidence"] == "low"
    assert r.c["by_relevance"].get("hidden", {}).get("files", 0) == 0


def test_source_found_anywhere_below_the_folder_counts_and_a_deeper_build_folder_is_covered_by_the_outer_one(tmp_path):
    r = run(tmp_path, {"p/build/deep/er/x.go": "x", "p/build/ok.bin": "x", "q/dist/a.bin": "x", "q/dist/node/b.ts": "x", "q/src/x.txt": "x"})
    assert rule_of(r, "p/build/ok.bin")[0] == "R-gen-build-output-unconfirmed"                      # a .go file anywhere below makes it a source-like folder
    assert rule_of(r, "q/dist/a.bin")[0] == "R-gen-build-output-unconfirmed"
    r2 = run(tmp_path, {"app/pom.xml": "<project/>", "app/target/classes/x.class": "x", "app/target/dist/y.js": "x"}, out="o2", name="t2")
    assert {rule_of(r2, p)[0] for p in ("app/target/classes/x.class", "app/target/dist/y.js")} == {"R-gen-build-output"}


def test_the_name_must_be_the_whole_folder_name_and_a_manifest_in_a_parent_further_up_does_not_corroborate(tmp_path):
    r = run(tmp_path, {"pom.xml": "<project/>", "a/builds/x.py": "x", "a/dist-info/y.py": "x", "a/rebuild/z.py": "x", "a/sub/dist/w.py": "x"})
    assert all(p not in r.pf for p in ("a/builds/x.py", "a/dist-info/y.py", "a/rebuild/z.py"))
    assert rule_of(r, "a/sub/dist/w.py")[0] == "R-gen-build-output-unconfirmed"                      # the manifest is two levels up, not beside it


# ---- worktree copies: name AND a .git file ------------------------------------------------------------------------------------------------
def test_a_worktree_name_with_a_git_file_is_hidden_and_the_name_alone_is_shown(tmp_path):
    r = run(tmp_path, {"wt-a/.git": "gitdir: ../.git/worktrees/a", "wt-a/src/x.py": "x", "wt-b/src/x.py": "x", "ws-c/.git/HEAD": "ref", "ws-c/src/y.py": "x",
                       "ews-d/.git": "gitdir: x", "ews-d/z.txt": "x", "trellis-wt1/.git": "g", "trellis-wt1/a.txt": "x", "keep/a.txt": "x"})
    assert rule_of(r, "wt-a/src/x.py") == ("R-copy-worktree-name", "hidden") and rule_of(r, "ews-d/z.txt")[1] == "hidden" and rule_of(r, "trellis-wt1/a.txt")[1] == "hidden"
    b = r.pf["wt-b/src/x.py"]
    assert b["rule_id"] == "R-copy-worktree-name-only" and b["relevance"] == "supporting" and b["confidence"] == "low" and b["role"] == "worktree-copy"
    assert rule_of(r, "ws-c/src/y.py")[0] == "R-copy-worktree-name-only"                              # a .git FOLDER is a clone, not a worktree: the name alone
    assert "keep/a.txt" not in r.pf


def test_the_worktree_name_rule_still_claims_top_level_folders_only(tmp_path):
    r = run(tmp_path, {"repo/wt-x/.git": "g", "repo/wt-x/a.txt": "x"})
    assert "repo/wt-x/a.txt" not in r.pf


# ---- log and backup files: hidden as files, never their folder -------------------------------------------------------------------------------
def test_one_stray_log_or_backup_hides_only_itself(tmp_path):
    r = run(tmp_path, {"svc/app.log": "x", "svc/main.py": "x", "svc/README.txt": "x", "svc/old.bak": "x", "svc/cfg.json": "x"})
    assert rule_of(r, "svc/app.log") == ("R-run-log", "hidden") and rule_of(r, "svc/old.bak") == ("R-backup-file", "hidden")
    assert all(p not in r.pf for p in ("svc/main.py", "svc/README.txt", "svc/cfg.json"))             # the folder and its other files are untouched
    assert not any(f["grain"] == "subtree" and f["path"] == "svc" for f in r.pf.values())


# ---- the four new rules -------------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("path", ["nb/.ipynb_checkpoints/a-checkpoint.ipynb", ".ipynb_checkpoints/x", "deep/er/.ipynb_checkpoints/sub/y"])
def test_ipynb_checkpoints_are_generated_and_hidden_at_any_depth(tmp_path, path):
    f = run(tmp_path, {path: "x"}).pf[path]
    assert f["rule_id"] == "R-gen-ipynb-checkpoints" and f["role"] == "generated" and f["relevance"] == "hidden"


@pytest.mark.parametrize("path", ["exchange-quickstart/distribution-hub/a.json", "repo/exchange-freshstart/distribution-hub/sub/b", "x/y/exchange-z/distribution-hub/c"])
def test_distribution_hub_output_is_generated_and_hidden(tmp_path, path):
    f = run(tmp_path, {path: "x"}).pf[path]
    assert f["rule_id"] == "R-gen-distribution-hub" and f["role"] == "generated" and f["relevance"] == "hidden"


@pytest.mark.parametrize("path", ["exchange/distribution-hub/a", "exchange-q/other/a", "exchange-q/distribution-hubs/a", "xexchange-q/distribution-hub/a", "distribution-hub/a"])
def test_other_paths_are_not_distribution_hub_output(tmp_path, path):
    assert path not in run(tmp_path, {path: "x"}).pf


@pytest.mark.parametrize("parent", ["EgeriaRootCA", "EgeriaIntermediateCA", "certs-ca", "my_cert", "Certificate", "pki", "PKI-store", "root.ca", "ca", "CA"])
def test_a_private_folder_in_a_certificate_folder_is_a_hidden_secret(tmp_path, parent):
    path = f"x/{parent}/private/key.pem"
    f = run(tmp_path, {path: "KEY"}).pf[path]
    assert f["rule_id"] == "R-secret-private-in-cert-dir" and f["role"] == "secret" and f["relevance"] == "hidden"


@pytest.mark.parametrize("parent", ["Select", "CalendarChart", "configuration", "certs", "capital", "Republic", "special-cases", "scatter"])
def test_a_private_folder_elsewhere_is_not_a_secret(tmp_path, parent):
    assert f"x/{parent}/private/a.txt" not in run(tmp_path, {f"x/{parent}/private/a.txt": "x"}).pf


def test_name_tokens_split_at_punctuation_and_case_changes():
    assert name_tokens("EgeriaRootCA") == {"egeria", "root", "ca"} and name_tokens("pki-certs") == {"pki", "certs"} and name_tokens("CaCert") == {"ca", "cert"}
    assert name_tokens("HTTPServer") == {"http", "server"} and name_tokens("a_b.c") == {"a", "b", "c"} and name_tokens("") == set()


def test_a_secret_folder_is_never_read_and_its_manifests_are_not_components(tmp_path):
    files = {"x/CA/private/package.json": '{"name": "k"}', "x/CA/private/key.pem": "KEY", "x/package.json": "{}"}
    r = run(tmp_path, files, profile="code-repo-conventions", source=True)
    assert "x/CA/private/package.json" not in r.src.asked
    comps = (r.out / "components-all.txt").read_text().split()
    assert "x/CA/private" not in comps and "x" in comps


# ---- submodules: .gitmodules path entries only ---------------------------------------------------------------------------------------------------
SUB = {".git/HEAD": "ref", ".gitmodules": '[submodule "a"]\n\tpath = libs/a\n\turl = https://token@example.invalid/secret.git\n[submodule "b"]\n\tpath = tools/b\n\turl = https://x\n',
       "libs/a/.git": "gitdir: ../../.git/modules/a", "libs/a/pyproject.toml": "[project]\nname='a'\n", "libs/a/a.py": "x",
       "libs/c/.git": "gitdir: ../../.git/modules/c", "libs/c/c.py": "x", "pyproject.toml": "[project]\nname='root'\n"}


def test_a_submodule_declared_in_gitmodules_is_part_of_the_outer_repository_when_the_file_is_read(tmp_path):
    r = run(tmp_path, SUB, profile="code-repo-conventions", source=True)
    assert "libs/a/a.py" not in r.pf or r.pf["libs/a/a.py"]["relevance"] != "hidden"
    assert rule_of(r, "libs/c/c.py") == ("R-vend-nested-repo", "hidden")                          # an undeclared nested repository is still vendored
    comps = (r.out / "components-all.txt").read_text().split()
    assert "libs/a" in comps and "libs/c" not in comps
    assert r.rec.submodules_exempt == [(".", "libs/a")]
    assert ".gitmodules" in r.rec.reading.log and "libs/a/.gitmodules" not in r.src.asked
    blob = json.dumps(r.rec.reading.decls, default=lambda o: o.__dict__) + (r.out / "report.md").read_text() + (r.out / "findings.jsonl").read_text()
    assert "example.invalid" not in blob and "token" not in blob                                    # the url is never extracted, so it is never in a finding or a report


def test_without_a_blob_source_every_nested_repository_is_vendored_as_before(tmp_path):
    r = run(tmp_path, SUB, profile="code-repo-conventions", source=False)
    assert rule_of(r, "libs/a/a.py") == ("R-vend-nested-repo", "hidden") and r.rec.submodules_exempt == []


def test_gitmodules_in_a_nested_repository_is_not_read_and_only_submodule_sections_count(tmp_path):
    files = {"x/.git/HEAD": "r", "x/n/.git": "g", "x/n/.gitmodules": '[submodule "z"]\n\tpath = z\n', "x/n/z/.git": "g", "x/n/z/a.py": "x", "x/a.py": "x"}
    r = run(tmp_path, files, source=True)
    assert "x/n/.gitmodules" not in r.src.asked                                                   # hidden wins before any read
    d = mf.extract("gitmodules", ".gitmodules", b'[remote "o"]\n\tpath = no\n[submodule "s"]\n\tpath = yes\n\turl = u\n\tbranch = main\n[submodule "t"]\n\turl = only-url\n')
    assert d.members == ["yes"]


def test_a_gitmodules_path_that_is_unsafe_is_ignored(tmp_path):
    files = {".git/HEAD": "r", ".gitmodules": '[submodule "a"]\n\tpath = ../outside\n[submodule "b"]\n\tpath = /abs\n', "n/.git": "g", "n/a.py": "x"}
    r = run(tmp_path, files, profile="code-repo-conventions", source=True)
    assert rule_of(r, "n/a.py") == ("R-vend-nested-repo", "hidden") and r.rec.submodules_exempt == []


# ---- the profiles --------------------------------------------------------------------------------------------------------------------------------
def test_the_profiles_carry_the_review_provenance_and_the_new_rules_come_before_the_m5_rules():
    g = load_profile("generic-relevance", PROFILES)
    ids = [r.id for r in g.rules]
    assert g.version == "0.4.0" and load_profile("worktree-copies", PROFILES).version == "0.2.0"
    assert ids.index("R-gen-build-output") < ids.index("R-gen-tool-cache") and ids[-4:] == ["R-wt-claude-worktree", "R-tool-idea", "R-run-volume-logs", "R-vend-nested-repo"]
    assert ids.index("R-gen-ipynb-checkpoints") < ids.index("R-gen-distribution-hub") < ids.index("R-secret-private-in-cert-dir") < ids.index("R-wt-claude-worktree")
    by = {r.id: r for r in g.rules}
    for rid in ("R-gen-ipynb-checkpoints", "R-gen-distribution-hub", "R-secret-private-in-cert-dir"):
        assert by[rid].tuned_on == ("egeria-v6 re-check sample (be675143)",) and by[rid].relevance == "hidden"
    for rid in ("R-gen-build-output", "R-gen-build-output-no-source", "R-gen-build-output-unconfirmed", "R-run-log", "R-backup-file"):
        assert by[rid].tuned_on == ("Dan's review 2026-11-26",)
    assert by["R-gen-build-output-unconfirmed"].relevance == "supporting" and by["R-gen-build-output-unconfirmed"].confidence == "low"
    assert by["R-secret-private-in-cert-dir"].role == "secret"
    assert g.manifest_reading.readers == ("gitmodules",) and g.manifest_reading.submodule_rule == "R-vend-nested-repo"


def test_the_manifest_reading_blocks_of_a_child_and_its_base_combine():
    p = load_profile("code-repo-conventions", PROFILES)
    m = p.manifest_reading
    assert set(m.readers) == set(mf.CODE_READERS) | {"gitmodules"} and m.submodule_rule == "R-vend-nested-repo" and m.member_rule is not None
    d = yaml.safe_load((PROFILES / "code-repo.yaml").read_text())
    d["manifest_reading"]["max_blobs"] = 10
    (PROFILES / "..").resolve()
    merged = parse_profile(d, "t", PROFILES)
    assert merged.manifest_reading.max_blobs == 10 and merged.manifest_reading.submodule_rule == "R-vend-nested-repo"


def _rule(**over):
    r = {"id": "R-x", "match": {"name": "build"}, "assign": {"role": "generated"}, "grain": "subtree", "basis": "convention", "confidence": "low", "evidence": "e"}
    r.update(over)
    return r


def _doc(**kw):
    d = {"profile_id": "t", "version": "0.1.0", "status": "proposed", "applies_to": "any", "roles": ["generated"], "relevance": {"primary": [], "supporting": [], "hidden": ["generated"]},
         "rules": [_rule()]}
    d.update(kw)
    return d


def test_new_match_keys_are_validated_and_a_named_subtree_is_a_directory_rule():
    assert parse_profile(_doc()).rules[0].is_dir_rule
    assert parse_profile(_doc(rules=[_rule(match={"name": "build", "no_source_files": True})])).rules[0].no_source
    assert parse_profile(_doc(rules=[_rule(match={"name": "private", "parent_name_token": ["CA", "Pki"]})])).rules[0].parent_tokens == frozenset({"ca", "pki"})
    assert parse_profile(_doc(rules=[_rule(match={"path_glob": "wt-*/x"})])).rules[0].is_dir_rule                  # a subtree glob that names a directory
    for bad in ({"name": "build", "no_source_files": False}, {"name": "build", "no_source_files": "yes"}, {"name": "x", "parent_name_token": [""]}):
        with pytest.raises(ProfileError):
            parse_profile(_doc(rules=[_rule(match=bad)]))
    with pytest.raises(ProfileError, match="file-name"):
        parse_profile(_doc(rules=[_rule(match={"name": "build", "no_source_files": True, "extension": ".x"})]))


def test_submodule_rule_is_needed_exactly_when_the_gitmodules_reader_is_on():
    mr = {"readers": ["gitmodules"]}
    with pytest.raises(ProfileError, match="submodule_rule"):
        parse_profile(_doc(manifest_reading=mr))
    with pytest.raises(ProfileError, match="not a rule"):
        parse_profile(_doc(manifest_reading={**mr, "submodule_rule": "R-nope"}))
    assert parse_profile(_doc(manifest_reading={**mr, "submodule_rule": "R-x"})).manifest_reading.submodule_rule == "R-x"
