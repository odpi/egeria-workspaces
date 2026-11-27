"""N6 (Phase 1c): the workspace-repo profile. Four STRUCTURAL rules by file kinds and names (never a repository's folder names) for repositories whose parts are deployments,
notebooks, templates and documents: (a) a compose directory is a deployment, (b) a folder of notebooks or an Obsidian vault is `notebooks`, (c) a mostly-Markdown top-level folder
is `documentation`, (d) a mostly-data top-level folder with no code is `sample-data`. Synthetic only."""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from recognizer import manifests as mf
from recognizer.layout_profile import ProfileError, compose_profiles, load_profile, parse_profile
from recognizer.recognize import Recognizer

PROFILES = Path(__file__).resolve().parent.parent / "profiles"
SVC = "services:\n  web:\n    image: x\n"


def survey(tmp_path, files, out="out", name="tree", source=True, profile="workspace-repo"):
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

        def read(self, path, mx):
            self.asked.append(path)
            return self.inner.read(path, mx)

        def close(self):
            pass
    src = Rec() if source else None
    rec = Recognizer(compose_profiles(profile, PROFILES), blob_source=src)
    c = rec.run(lst, tmp_path / out)
    f = {x["path"]: x for x in map(json.loads, (tmp_path / out / "findings.jsonl").read_text().splitlines()) if x["role"] == "component"}
    return SimpleNamespace(c=c, f=f, rec=rec, src=src, out=tmp_path / out, allc=(tmp_path / out / "components-all.txt").read_text().split(),
                           comps=(tmp_path / out / "components.txt").read_text().split())


def kinds(r, kind):
    return sorted(p for p, x in r.f.items() if x.get("kind") == kind and x.get("structure_rule_id"))


# ---- (a) deployments -------------------------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("name", ["compose.yml", "compose.yaml", "docker-compose.yml", "docker-compose.override.yaml", "docker-compose-dev.yml", "web-compose.yml", "Docker-Compose.YML"])
def test_a_directory_with_a_compose_named_file_is_a_deployment_without_reading_anything(tmp_path, name):
    r = survey(tmp_path, {f"stack/{name}": "not even yaml: [", "stack/readme.md": "x"}, source=False)
    assert kinds(r, "deployment") == ["stack"] and r.f["stack"]["structure_rule_id"] == "S-compose-deployment" and r.f["stack"]["role"] == "component"


@pytest.mark.parametrize("name", ["docker.yml", "composer.yml", "compose.json", "mycompose.yml", "docker-compose.txt"])
def test_names_that_are_not_compose_files_do_not_count_without_a_services_key(tmp_path, name):
    r = survey(tmp_path, {f"stack/{name}": "key: 1\n"})
    assert kinds(r, "deployment") == []


def test_a_yaml_file_with_a_top_level_services_mapping_makes_a_deployment(tmp_path):
    files = {"stack/egeria-stack.yaml": SVC, "other/app.yaml": "name: x\nservices: [a, b]\n", "third/c.yaml": "services: {}\n", "fourth/d.yaml": "nested:\n  services:\n    a: 1\n"}
    r = survey(tmp_path, files)
    assert kinds(r, "deployment") == ["stack"]                                          # a list, an empty mapping and a nested key are not services
    assert "stack/egeria-stack.yaml" in r.rec.reading.log and r.c["manifest_reading"]["readers"][0] == "compose-services"


def test_without_a_blob_source_only_the_names_count(tmp_path):
    r = survey(tmp_path, {"a/egeria-stack.yaml": SVC, "b/compose.yml": SVC}, source=False)
    assert kinds(r, "deployment") == ["b"]


def test_helm_templates_and_hidden_and_unparseable_yaml_are_not_deployments_and_are_not_opened(tmp_path):
    files = {"chart/Chart.yaml": "name: c\n", "chart/templates/dep.yaml": "services:\n  {{ .Values.x }}\n", "node_modules/p/stack.yaml": SVC, "bad/s.yaml": "services: [unclosed\n",
             "tagged/t.yaml": "services: !!python/object/apply:os.system [x]\n", "alias/a.yaml": "a: &x {k: 1}\nservices: *x\n"}
    r = survey(tmp_path, files)
    assert kinds(r, "deployment") == []
    asked = set(r.src.asked)
    assert "chart/templates/dep.yaml" not in asked and "node_modules/p/stack.yaml" not in asked and "bad/s.yaml" in asked


def test_the_unit_is_the_child_of_the_nearest_grouping_folder(tmp_path):
    files = {"group/alpha/compose.yml": SVC, "group/beta/docker-compose.yml": SVC, "group/many/one/compose.yml": SVC, "group/many/two/compose.yml": SVC, "group/many/two/deeper/compose.yml": SVC,
             "README.md": "x"}
    r = survey(tmp_path, files, source=False)
    assert kinds(r, "deployment") == ["group/alpha", "group/beta", "group/many"]         # many/one and many/two are inside the unit `many`
    assert r.f["group/many"]["deployment_dirs"] == 3


def test_without_a_grouping_folder_the_outermost_compose_directory_is_the_unit(tmp_path):
    r = survey(tmp_path, {"solo/deploy/compose.yml": SVC, "solo/deploy/sub/compose.yml": SVC, "other/x/y/docker-compose.yml": SVC}, source=False)
    assert kinds(r, "deployment") == ["other/x/y", "solo/deploy"]


def test_the_repository_root_is_never_a_grouping_folder_and_a_root_compose_file_claims_nothing(tmp_path):
    r = survey(tmp_path, {"a/compose.yml": SVC, "b/compose.yml": SVC, "compose.yml": SVC}, source=False)
    assert kinds(r, "deployment") == ["a", "b"]


def test_a_deployment_is_not_claimed_inside_a_component_a_fixture_or_a_hidden_folder(tmp_path):
    files = {"pyproject.toml": "[project]\nname='p'\n", "pkg/pyproject.toml": "[project]\nname='k'\n", "pkg/deploy/compose.yml": SVC, "tests/up/compose.yml": SVC, "samples/s/compose.yml": SVC,
             "node_modules/m/compose.yml": SVC, "real/compose.yml": SVC}
    r = survey(tmp_path, files, source=False)
    assert kinds(r, "deployment") == ["real"]


def test_the_projects_built_inside_a_deployment_are_its_parts(tmp_path):
    files = {"g/a/compose.yml": SVC, "g/b/compose.yml": SVC, "g/a/img/Dockerfile": "FROM x", "g/b/Dockerfile": "FROM y", "g/a/readme.md": "x"}
    r = survey(tmp_path, files, source=False)
    assert "g/a" in r.comps and "g/a/img" not in r.comps and "g/a/img" in r.allc and r.f["g/a/img"]["part_of"] == "g/a"


# ---- (b) notebooks ---------------------------------------------------------------------------------------------------------------------------------------
def test_the_shallowest_directory_with_three_notebooks_below_it_is_a_notebooks_component(tmp_path):
    files = {"wb/a/1.ipynb": "{}", "wb/a/2.ipynb": "{}", "wb/b/3.ipynb": "{}", "few/1.ipynb": "{}", "few/2.ipynb": "{}", "readme.md": "x"}
    r = survey(tmp_path, files, source=False)
    assert kinds(r, "notebooks") == ["wb"] and r.f["wb"]["notebooks"] == 3 and "few" not in r.f and "wb/a" not in r.f


def test_an_obsidian_vault_is_a_notebooks_component_wherever_it_is_and_checkpoints_do_not_count(tmp_path):
    files = {"vault/.obsidian/app.json": "{}", "vault/note.md": "x", "deep/er/vault2/.obsidian/x.json": "{}", "ck/.ipynb_checkpoints/a-checkpoint.ipynb": "{}", "ck/.ipynb_checkpoints/b.ipynb": "{}",
             "ck/.ipynb_checkpoints/c.ipynb": "{}"}
    r = survey(tmp_path, files, source=False)
    assert kinds(r, "notebooks") == ["deep/er/vault2", "vault"] and r.f["vault"]["vault"] is True and "ck" not in r.f


def test_notebooks_inside_a_component_or_a_fixture_or_the_root_are_not_claimed(tmp_path):
    files = {"pyproject.toml": "[project]\nname='p'\n", "1.ipynb": "{}", "2.ipynb": "{}", "3.ipynb": "{}", "pkg/pyproject.toml": "[project]\nname='k'\n", "pkg/n/1.ipynb": "{}",
             "pkg/n/2.ipynb": "{}", "pkg/n/3.ipynb": "{}", "examples/1.ipynb": "{}", "examples/2.ipynb": "{}", "examples/3.ipynb": "{}"}
    r = survey(tmp_path, files, source=False)
    assert kinds(r, "notebooks") == []


# ---- (c) mostly documentation and (d) mostly data ------------------------------------------------------------------------------------------------------
def test_a_top_level_folder_that_is_at_least_80_percent_markdown_is_documentation(tmp_path):
    files = {**{f"guides/{i}.md": "x" for i in range(4)}, "guides/logo.png": "x", **{f"mixed/{i}.md": "x" for i in range(3)}, "mixed/a.png": "x", "mixed/b.png": "x",
             "tiny/a.md": "x", "tiny/b.md": "x", "deep/sub/1.md": "x", "deep/sub/2.md": "x", "deep/sub/3.md": "x", "deep/sub/4.md": "x"}
    r = survey(tmp_path, files, source=False)
    assert kinds(r, "documentation") == ["deep", "guides"]                                # 4/5 = 0.8 is enough; 3/5 and a two-file folder are not
    assert r.f["guides"]["share"] == 0.8 and r.f["guides"]["files_counted"] == 5 and r.f["guides"]["structure_confidence"] == "low"


def test_a_top_level_folder_that_is_mostly_data_with_no_code_is_sample_data(tmp_path):
    files = {"data/a.csv": "x", "data/b.json": "x", "data/c.jsonl": "x", "data/d.parquet": "x", "data/e.yaml": "x", "data/notes.txt": "x",
             "coded/a.csv": "x", "coded/b.csv": "x", "coded/c.csv": "x", "coded/gen.py": "x", "two/a.csv": "x", "two/b.csv": "x"}
    r = survey(tmp_path, files, source=False)
    assert kinds(r, "sample-data") == ["data"] and "coded" not in r.f and "two" not in r.f


def test_hidden_files_are_not_counted_and_other_claims_win(tmp_path):
    files = {**{f"docsy/{i}.md": "x" for i in range(4)}, "docsy/build/x.bin": "x", "docsy/node_modules/a.js": "x", "docs/1.md": "x", "docs/2.md": "x", "docs/3.md": "x",
             "pkg/pyproject.toml": "[project]\nname='k'\n", "pkg/a.md": "x", "pkg/b.md": "x", "pkg/c.md": "x"}
    r = survey(tmp_path, files, source=False)
    assert "docsy" in kinds(r, "documentation")                                           # build/ and node_modules/ are hidden, so 4 of 4 files
    assert r.f["docs"]["rule_id"] == "R-conv-docs" and r.f["pkg"]["rule_id"] == "R-comp-pyproject"


def test_a_folder_is_claimed_once_and_runs_are_identical(tmp_path):
    files = {"x/1.md": "x", "x/2.md": "x", "x/3.md": "x", "x/1.ipynb": "{}", "x/2.ipynb": "{}", "x/3.ipynb": "{}", "d/compose.yml": SVC}
    a = survey(tmp_path, files, out="a", name="ta")
    b = survey(tmp_path, files, out="b", name="tb")
    assert a.f["x"]["kind"] == "notebooks" and a.f["x"]["structure_rule_id"] == "S-notebooks"            # the earlier rule (notebooks) wins; the same directory is not claimed twice
    assert [x for x in (tmp_path / "a" / "findings.jsonl").read_text().splitlines() if json.loads(x)["path"] == "x" and json.loads(x)["role"] == "component"].__len__() == 1
    for n in ("components.txt", "components-all.txt", "findings.jsonl", "classes.json", "manifest-reads.txt"):
        assert (a.out / n).read_bytes() == (b.out / n).read_bytes(), n


# ---- the profile and the loader -------------------------------------------------------------------------------------------------------------------------------
def test_the_profile_extends_the_code_and_docs_profiles_and_carries_its_provenance():
    p = load_profile("workspace-repo", PROFILES)
    assert [pid for pid, _ in p.composed_of][:3] == ["workspace-repo", "code-repo-conventions", "code-repo"] and "docs-site" in [pid for pid, _ in p.composed_of]
    assert [s["id"] for s in p.structural][:4] == ["S-compose-deployment", "S-notebooks", "S-mostly-docs", "S-mostly-data"] and p.structural[-1]["id"] == "S-workspace-siblings"
    assert all(s["tuned_on"] == ["egeria-workspaces dogfood key (fact-rich)"] and s["evidence"] for s in p.structural[:4])
    assert "compose-services" in p.manifest_reading.readers and "package-json" in p.manifest_reading.readers and "mkdocs" in p.manifest_reading.readers
    assert not [r for r in p.rules if r.origin == "workspace-repo"]                         # all four are structural, none is a rule


def test_no_structural_rule_names_a_folder():
    text = json.dumps(load_profile("workspace-repo", PROFILES).structural).lower()
    for banned in ("compose-configs", "coco", "workbooks", "portal-docs", "design-docs", "exchange", "runtime-volumes", "obsidian-plugins", "charts"):
        assert banned not in text, banned


def _doc(**sr):
    base = {"id": "S-x", "op": "mostly-extension-folder", "min": 3, "share": 0.8, "extensions": [".md"], "kind": "documentation", "basis": "convention", "confidence": "low", "evidence": "e"}
    base.update(sr)
    return {"profile_id": "t", "version": "0.1.0", "status": "proposed", "applies_to": "any", "roles": ["component"], "relevance": {"primary": ["component"], "supporting": [], "hidden": []},
            "rules": [], "structural_rules": [base]}


@pytest.mark.parametrize("change,msg", [
    ({"kind": None}, "needs a kind"), ({"extensions": ["md"]}, "extensions"), ({"extensions": []}, "extensions"), ({"share": 0.2}, "share"), ({"share": "most"}, "share"), ({"min": 0}, "min"),
    ({"no_code": False}, "no_code"), ({"op": "compose-deployment", "name_regex": ["("], "share": None, "extensions": None}, "bad name_regex"), ({"op": "notebook-folder", "share": 0.9}, "belong to"),
    ({"op": "notebook-folder", "extensions": [".md"]}, "belong to"), ({"op": "mostly-extension-folder", "yaml_key": "services"}, "belong to"), ({"op": "wizard"}, "not one of"),
    ({"op": "sibling-manifests-top-level", "min": 5, "share": None}, "takes no kind"),
])
def test_bad_structural_rules_are_load_errors(change, msg):
    d = _doc()
    for k, v in change.items():
        if v is None:
            d["structural_rules"][0].pop(k, None)
        else:
            d["structural_rules"][0][k] = v
    with pytest.raises(ProfileError, match=msg):
        parse_profile(d, "t")


def test_a_valid_notebook_and_compose_rule_loads():
    d = _doc(op="notebook-folder")
    d["structural_rules"][0].pop("share"); d["structural_rules"][0].pop("extensions")
    assert parse_profile(d, "t").structural[0]["op"] == "notebook-folder"
    d2 = _doc(op="compose-deployment", name_regex=["^compose\\.yml$"], yaml_key="services")
    d2["structural_rules"][0].pop("share"); d2["structural_rules"][0].pop("extensions")
    assert parse_profile(d2, "t").structural[0]["yaml_key"] == "services"
