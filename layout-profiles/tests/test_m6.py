"""M6: manifest reading. Synthetic manifests only (nothing copied from a real repository). Covers the closed list, the caps, the safe parsers, the
read log (what was and was NOT opened), member and aggregator handling, and that a run without a blob source is still names and sizes only."""
import json
import os
import subprocess
from pathlib import Path

import pytest
import yaml

from recognizer import manifests as mf
from recognizer.layout_profile import ProfileError, load_profile, parse_profile
from recognizer.recognize import Recognizer

PROFILES = Path(__file__).resolve().parent.parent / "profiles"


class Recording:
    """Wraps a blob source and logs every path it is asked for: the test asserts on this, independently of the recognizer's own read log."""

    def __init__(self, inner):
        self.inner, self.asked = inner, []

    def read(self, path, max_bytes):
        self.asked.append(path)
        return self.inner.read(path, max_bytes)

    def close(self):
        self.inner.close()


def make_tree(tmp_path, files: dict, name="tree"):
    root = tmp_path / name
    for rel, content in files.items():
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(content if isinstance(content, bytes) else content.encode())
    rows = sorted((rel, len(c if isinstance(c, bytes) else c.encode())) for rel, c in files.items())
    lst = tmp_path / f"{name}.tsv"
    lst.write_text("".join(f"{p}\t{n}\n" for p, n in rows))
    return root, lst


def survey(tmp_path, files, profile="code-repo-conventions", out="out", prof=None, source=True, name="tree"):
    root, lst = make_tree(tmp_path, files, name)
    src = Recording(mf.FileSource(str(root))) if source else None
    rec = Recognizer(prof or load_profile(profile, PROFILES), blob_source=src)
    c = rec.run(lst, tmp_path / out)
    f = [json.loads(x) for x in (tmp_path / out / "findings.jsonl").read_text().splitlines()]
    by = {x["path"]: x for x in f if not x["rule_id"].startswith("F-")}
    comps = (tmp_path / out / "components.txt").read_text().split()
    allc = (tmp_path / out / "components-all.txt").read_text().split()
    return types_ns(c=c, by=by, comps=comps, allc=allc, rec=rec, src=src, out=tmp_path / out)


def types_ns(**kw):
    from types import SimpleNamespace
    return SimpleNamespace(**kw)


NPM_WS = json.dumps({"name": "root", "private": True, "workspaces": ["packages/*"]})
PKG = lambda n: json.dumps({"name": n})          # noqa: E731


# ---- the parsers -------------------------------------------------------------------------------------------------------------------
def test_yaml_unknown_tags_become_null_and_nothing_is_constructed():
    doc = mf.parse_yaml(b"packages: [a, b]\nhook: !!python/name:os.system\nenv: !ENV [HOME]\nobj: !!python/object/apply:os.system [x]\n")
    assert doc["packages"] == ["a", "b"] and doc["hook"] is None and doc["env"] is None and doc["obj"] is None


def test_a_yaml_alias_bomb_is_refused():
    bomb = b"a: &a [x, x, x, x]\nb: &b [*a, *a, *a, *a]\nc: &c [*b, *b, *b, *b]\nd: [*c, *c, *c, *c]\n"
    with pytest.raises(mf.ManifestParseError, match="alias"):
        mf.parse_yaml(bomb)


@pytest.mark.parametrize("xml", [b'<!DOCTYPE project [<!ENTITY x "y">]><project/>', b'<project><!ENTITY a "b"></project>', b"<!doctype project><project/>"])
def test_xml_with_a_doctype_or_entity_is_refused(xml):
    with pytest.raises(mf.ManifestParseError, match="refused"):
        mf.parse_xml(xml)


def test_malformed_and_too_deep_documents_are_parse_errors_not_crashes():
    for fn, data in ((mf.parse_json, b"{not json"), (mf.parse_toml, b"[a\nb="), (mf.parse_yaml, b"a: [1, 2"), (mf.parse_xml, b"<project>")):
        with pytest.raises(mf.ManifestParseError):
            fn(data)
    with pytest.raises(mf.ManifestParseError, match="deep|Recursion"):
        mf.parse_json(b"[" * 80 + b"]" * 80)
    with pytest.raises(mf.ManifestParseError):
        mf.parse_json(b"[" * 100000 + b"]" * 100000)                  # not a stack overflow either


# ---- the extractors, one valid and one malformed file per format ------------------------------------------------------------------------
@pytest.mark.parametrize("reader,path,body,members,aggregator", [
    ("package-json", "package.json", NPM_WS, ["packages/*"], True),
    ("package-json", "package.json", json.dumps({"name": "r", "workspaces": {"packages": ["apps/*"]}}), ["apps/*"], True),
    ("pnpm-workspace", "pnpm-workspace.yaml", "packages:\n  - 'pkgs/*'\n  - '!pkgs/skip'\n", ["pkgs/*", "!pkgs/skip"], True),
    ("lerna", "lerna.json", json.dumps({"packages": ["modules/*"]}), ["modules/*"], True),
    ("cargo", "Cargo.toml", '[workspace]\nmembers = ["crates/*"]\nexclude = ["crates/old"]\n', ["crates/*"], True),
    ("cargo", "Cargo.toml", '[package]\nname = "p"\n[workspace]\nmembers = ["sub"]\n', ["sub"], False),
    ("uv", "pyproject.toml", '[project]\nname = "p"\n[tool.uv.workspace]\nmembers = ["libs/*"]\n', ["libs/*"], False),
    ("uv", "pyproject.toml", '[tool.uv.workspace]\nmembers = ["libs/*"]\n', ["libs/*"], True),
    ("go-work", "go.work", "go 1.21\nuse (\n\t./a\n\t./b // comment\n)\nuse ./c\n", ["./a", "./b", "./c"], True),
    ("maven", "pom.xml", "<project><artifactId>p</artifactId><packaging>pom</packaging><modules><module>a</module><module>b/c</module></modules></project>", ["a", "b/c"], True),
    ("maven", "pom.xml", '<project xmlns="http://maven.apache.org/POM/4.0.0"><artifactId>p</artifactId><modules><module>a</module></modules></project>', ["a"], False),
    ("gradle", "settings.gradle", "rootProject.name = 'x'\ninclude ':a', ':b:c'\ninclude 'd'\n// include 'ignored'\n", ["a", "b/c", "d"], False),
    ("gradle", "settings.gradle.kts", 'include(\n  ":k1",\n  ":k2:deep"\n)\n/* include("nope") */\n', ["k1", "k2/deep"], False),
])
def test_each_format_extracts_its_members(reader, path, body, members, aggregator):
    d = mf.extract(reader, path, body.encode())
    assert d is not None and d.members == members and d.aggregator is aggregator


@pytest.mark.parametrize("reader,path,body", [
    ("package-json", "package.json", "{oops"), ("pnpm-workspace", "pnpm-workspace.yaml", "packages: [a"), ("lerna", "lerna.json", "[1,"),
    ("cargo", "Cargo.toml", "[workspace\nmembers"), ("uv", "pyproject.toml", "[tool.uv\n"), ("maven", "pom.xml", "<project><modules>"),
])
def test_each_malformed_manifest_is_a_parse_error(reader, path, body):
    with pytest.raises(mf.ManifestParseError):
        mf.extract(reader, path, body.encode())


def test_a_manifest_that_declares_nothing_gives_no_declaration():
    assert mf.extract("go-work", "go.work", b"go 1.21\n") is None
    assert mf.extract("gradle", "settings.gradle", b"rootProject.name='x'\n") is None
    assert mf.extract("lerna", "lerna.json", b'{"version": "1"}') is None


# ---- members are components, aggregators are not ----------------------------------------------------------------------------------------
def test_npm_workspace_members_are_top_level_components_and_the_aggregator_is_not(tmp_path):
    files = {"mono/package.json": NPM_WS, "mono/packages/a/package.json": PKG("a"), "mono/packages/b/package.json": PKG("b"),
             "mono/packages/a/src/x.js": "x", "mono/packages/notes/readme.md": "n", "svc/package.json": PKG("svc")}
    r = survey(tmp_path, files)
    assert r.comps == ["mono/packages/a", "mono/packages/b", "svc"]                  # mono aggregates; packages/notes has no package.json
    assert "mono" not in r.allc
    assert r.by["mono"]["rule_id"] == "M-aggregator" and r.by["mono"]["role"] == "other" and r.by["mono"]["manifest_kind"] == "node-package"
    assert r.by["mono"]["evidence_file"] == "mono/package.json" and r.by["mono"]["evidence_field"] == "workspaces" and r.by["mono"]["evidence_blob"]
    m = r.by["mono/packages/a"]
    assert m["rule_id"] == "R-comp-package-json" and m["member_of"] == "mono" and m["evidence_file"] == "mono/package.json"


def test_without_a_blob_source_the_run_is_names_and_sizes_only(tmp_path):
    files = {"mono/package.json": NPM_WS, "mono/packages/a/package.json": PKG("a")}
    r = survey(tmp_path, files, source=False)
    assert r.rec.reading is None and r.c["manifest_reading"]["enabled"] is False
    assert r.comps == ["mono"] and r.allc == ["mono", "mono/packages/a"]               # unchanged M2 behaviour: the parent is the component
    assert "Manifest reading: not enabled" in (r.out / "report.md").read_text()
    assert not (r.out / "manifest-reads.txt").exists()


def test_a_member_without_its_own_manifest_is_claimed_by_the_member_rule(tmp_path):
    files = {"settings.gradle": "include 'core', 'ghost'\n", "core/src/Main.java": "x", "build.gradle": "x"}
    r = survey(tmp_path, files)
    assert r.by["core"]["rule_id"] == "M-workspace-member" and r.by["core"]["basis"] == "manifest-content" and r.by["core"]["member_of"] == "."
    assert r.by["."]["unresolved_members"] == ["ghost"] and "ghost" not in r.by
    assert "core" in r.comps


def test_members_of_a_real_package_are_still_components_of_their_own(tmp_path):
    files = {"pyproject.toml": '[project]\nname = "root"\n[tool.uv.workspace]\nmembers = ["libs/*"]\n', "libs/a/pyproject.toml": '[project]\nname="a"\n',
             "libs/b/pyproject.toml": '[project]\nname="b"\n', "sub/pyproject.toml": '[project]\nname="s"\n', "sub/inner/pyproject.toml": '[project]\nname="i"\n',
             "sub/pkg/pyproject.toml": '[project]\nname="p"\n'}
    r = survey(tmp_path, files)
    assert {"libs/a", "libs/b"} <= set(r.comps) and r.by["."]["root"] is True       # the root stays a component (root-project)
    assert r.by["."]["manifest_name"] == "root"


def test_cargo_virtual_workspace_aggregates_and_exclude_is_honoured(tmp_path):
    files = {"rs/Cargo.toml": '[workspace]\nmembers = ["crates/*"]\nexclude = ["crates/old"]\n', "rs/crates/a/Cargo.toml": '[package]\nname="a"\n',
             "rs/crates/old/Cargo.toml": '[package]\nname="o"\n'}
    r = survey(tmp_path, files)
    assert "rs" not in r.comps and "rs/crates/a" in r.comps
    assert r.by["rs/crates/old"].get("member_of") is None                           # excluded: still a manifest directory, but not a declared member


def test_maven_pom_packaging_aggregates_and_modules_are_components(tmp_path):
    files = {"app/pom.xml": "<project><artifactId>app</artifactId><packaging>pom</packaging><modules><module>api</module><module>web</module></modules></project>",
             "app/api/pom.xml": "<project><artifactId>api</artifactId></project>", "app/web/pom.xml": "<project><artifactId>web</artifactId></project>"}
    r = survey(tmp_path, files)
    assert r.comps == ["app/api", "app/web"] and r.by["app"]["rule_id"] == "M-aggregator"


def test_the_workspace_siblings_heuristic_still_applies_where_no_content_declares_them(tmp_path):
    files = {f"mono/p{i}/package.json": PKG(f"p{i}") for i in range(5)}
    files["mono/package.json"] = PKG("mono")                                         # five sibling manifests, none declared: the S rule is the fallback
    r = survey(tmp_path, files)
    assert [c for c in r.comps if c.startswith("mono/p")] == [f"mono/p{i}" for i in range(5)]


def test_a_dotdot_member_is_unresolved_and_nothing_outside_is_read(tmp_path):
    files = {"a/package.json": json.dumps({"workspaces": ["../b", "/etc", "c:/x", "ok"]}), "b/package.json": PKG("b"), "a/ok/package.json": PKG("ok")}
    r = survey(tmp_path, files)
    assert r.by["a"]["unresolved_members"] == ["../b", "/etc", "c:/x"]
    assert "b" not in {k for k, v in r.by.items() if v.get("member_of")} and r.by["a/ok"]["member_of"] == "a"


# ---- what is never opened -------------------------------------------------------------------------------------------------------------------
def test_lock_files_data_files_and_hidden_subtrees_are_never_opened(tmp_path):
    files = {"package.json": NPM_WS, "package-lock.json": "{}", "yarn.lock": "x", "Cargo.lock": "x", "uv.lock": "x", "data/data.json": "{}", "conf/values.yaml": "a: 1",
             ".env": "SECRET=1", "notes/book.ipynb": "{}", "packages/a/package.json": PKG("a"), "node_modules/x/package.json": PKG("x"),
             "node_modules/y/pom.xml": "<project/>", "build/out/package.json": PKG("b"), ".venv/lib/pyproject.toml": "[project]\n",
             "outer/.git/HEAD": "ref", "outer/in/.git": "gitdir: x", "outer/in/package.json": NPM_WS, "outer/in/packages/z/package.json": PKG("z"),
             "outer/package.json": PKG("outer"), ".claude/worktrees/w/package.json": PKG("w"), ".claude/worktrees/w/.git": "gitdir: y"}
    r = survey(tmp_path, files)
    opened = set(r.src.asked)
    assert opened == {"package.json", "packages/a/package.json", "outer/package.json"}
    assert set(r.rec.reading.log) == opened
    assert (r.out / "manifest-reads.txt").read_text().split() == sorted(opened, key=lambda p: (p.count("/"), p))
    for bad in ("package-lock.json", "yarn.lock", "Cargo.lock", "uv.lock", "data/data.json", "conf/values.yaml", ".env", "notes/book.ipynb"):
        assert bad not in opened
    assert r.c["manifest_reading"]["skipped_hidden"] >= 6


def test_a_file_name_not_on_the_closed_list_is_never_a_candidate(tmp_path):
    files = {"setup.py": "import os; os.system('x')", "build.gradle": "x", "Dockerfile": "x", "metadata.yaml": "a: 1", "CODEOWNERS": "* @someone",
             "mkdocs.yml": "site_name: x", "Chart.yaml": "name: c", "catalog-info.yaml": "kind: Component"}
    r = survey(tmp_path, files)
    assert r.src.asked == []


def test_an_over_cap_manifest_is_skipped_with_a_note_and_stays_presence_only(tmp_path):
    big = json.dumps({"name": "big", "workspaces": ["p/*"], "pad": "x" * (mf.DEFAULT_MAX_FILE_BYTES + 10)})
    files = {"w/package.json": big, "w/p/a/package.json": PKG("a")}
    r = survey(tmp_path, files)
    assert r.src.asked == ["w/p/a/package.json"] and r.c["manifest_reading"]["skipped_size"] == 1      # the big one is never opened
    assert r.by["w"]["skipped"] == "size" and r.by["w"]["rule_id"] == "R-comp-package-json"
    assert r.comps == ["w"]                                                           # presence-only: the parent stays the component


def test_the_per_survey_cap_stops_reading_and_is_reported(tmp_path):
    doc = yaml.safe_load((PROFILES / "code-repo.yaml").read_text())
    doc["manifest_reading"]["max_blobs"] = 2
    doc["extends"] = []
    doc["rules"] = [r for r in doc["rules"] if r["id"] == "R-comp-package-json"]
    prof = parse_profile(doc, "tight", PROFILES)
    files = {f"p{i}/package.json": PKG(f"p{i}") for i in range(5)}
    r = survey(tmp_path, files, prof=prof)
    st = r.c["manifest_reading"]
    assert st["blobs_read"] == 2 and st["cap_reached"] == "blobs" and st["cap_skipped"] == 3 and len(r.src.asked) == 2
    assert "CAP REACHED (blobs): 3" in (r.out / "report.md").read_text()
    assert len(r.comps) == 5                                                          # names-only claims are kept for the manifests not read
    assert sum(1 for f in r.by.values() if f.get("skipped") == "cap") == 3


def test_a_parse_error_falls_back_to_presence_with_a_lower_confidence(tmp_path):
    files = {"w/package.json": "{not json", "w/packages/a/package.json": PKG("a")}
    r = survey(tmp_path, files)
    f = r.by["w"]
    assert f["rule_id"] == "R-comp-package-json" and f["parse_error"].startswith("json") and f["confidence"] == "medium"        # high -> medium
    assert r.c["manifest_reading"]["parse_errors"] == 1 and "w" in r.comps and "w/packages/a" in r.allc


def test_a_manifest_that_is_a_symlink_is_not_followed(tmp_path):
    root, lst = make_tree(tmp_path, {"a/package.json": PKG("a"), "secret.txt": "S3CR3T"})
    os.symlink(root / "secret.txt", root / "b.json")
    os.makedirs(root / "link")
    os.symlink(root / "a" / "package.json", root / "link" / "package.json")
    src = mf.FileSource(str(root))
    assert src.read("link/package.json", 1000) == (None, None, "missing")
    assert src.read("a/package.json", 1000)[2] == ""


# ---- evidence, stability, determinism -------------------------------------------------------------------------------------------------------
def test_a_finding_id_does_not_change_when_an_unrelated_manifest_field_changes(tmp_path):
    a = survey(tmp_path, {"t/package.json": json.dumps({"name": "r", "version": "1", "workspaces": ["p/*"]}), "t/p/a/package.json": PKG("a")}, out="a", name="ta")
    b = survey(tmp_path, {"t/package.json": json.dumps({"name": "r", "version": "2", "license": "MIT", "workspaces": ["p/*"]}), "t/p/a/package.json": PKG("a")},
               out="b", name="tb")
    assert {k: v["finding_id"] for k, v in a.by.items()} == {k: v["finding_id"] for k, v in b.by.items()}
    assert a.by["t"]["evidence_blob"] != b.by["t"]["evidence_blob"]                    # the blob differs; the id does not


def test_two_runs_are_byte_identical_and_git_and_file_sources_agree(tmp_path):
    files = {"mono/package.json": NPM_WS, "mono/packages/a/package.json": PKG("a"), "mono/packages/b/package.json": PKG("b"), "svc/package.json": PKG("s"),
             "pom.xml": "<project><artifactId>x</artifactId><packaging>pom</packaging><modules><module>m</module></modules></project>", "m/pom.xml": "<project/>"}
    r1 = survey(tmp_path, files, out="o1", name="t1")
    r2 = survey(tmp_path, files, out="o2", name="t2")
    for n in ("components.txt", "components-all.txt", "findings.jsonl", "classes.json", "manifest-reads.txt"):
        assert (r1.out / n).read_bytes() == (r2.out / n).read_bytes(), n
    # the same tree through a git object database
    root = tmp_path / "t1"
    env = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull}
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=env)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True, env=env)
    tree = subprocess.run(["git", "-C", str(root), "write-tree"], check=True, capture_output=True, text=True, env=env).stdout.strip()
    (root / "mono" / "package.json").write_text('{"workspaces": ["DIRTY/*"]}')            # a dirty working tree must not leak in
    src = mf.GitBlobSource(str(root), tree)
    rec = Recognizer(load_profile("code-repo-conventions", PROFILES), blob_source=src)
    rec.run(tmp_path / "t1.tsv", tmp_path / "o3")
    src.close()
    for n in ("components.txt", "components-all.txt"):
        assert (tmp_path / "o3" / n).read_bytes() == (r1.out / n).read_bytes(), n
    f1 = {x["path"]: x for x in map(json.loads, (r1.out / "findings.jsonl").read_text().splitlines())}
    f3 = {x["path"]: x for x in map(json.loads, (tmp_path / "o3" / "findings.jsonl").read_text().splitlines())}
    assert f1["mono"]["evidence_blob"] == f3["mono"]["evidence_blob"]                    # a git blob id in both (the file source hashes like git)


def test_git_source_reads_the_commit_not_the_working_tree_and_discards_oversize(tmp_path):
    root = tmp_path / "g"
    root.mkdir()
    env = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull}
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=env)
    (root / "package.json").write_text('{"name": "committed"}')
    (root / "big.json").write_text("x" * 5000)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True, env=env)
    tree = subprocess.run(["git", "-C", str(root), "write-tree"], check=True, capture_output=True, text=True, env=env).stdout.strip()
    (root / "package.json").write_text('{"name": "dirty"}')
    src = mf.GitBlobSource(str(root), tree)
    data, sha, note = src.read("package.json", 1000)
    assert json.loads(data)["name"] == "committed" and len(sha) == 40 and note == ""
    assert src.read("big.json", 1000) == (None, src.read("big.json", 10**6)[1], "size")
    assert src.read("absent.json", 1000) == (None, None, "missing")
    assert src.read("package.json", 1000)[0] is not None                                  # the stream is still in step after a discarded blob
    src.close()


# ---- the profile -----------------------------------------------------------------------------------------------------------------------
def test_the_shipped_profiles_enable_manifest_reading_with_the_note_s_caps():
    p = load_profile("code-repo-conventions", PROFILES)
    m = p.manifest_reading
    assert p.version == "0.6.0" and load_profile("code-repo", PROFILES).version == "0.4.0"
    assert (m.max_file_bytes, m.max_blobs, m.max_total_bytes) == (256 * 1024, 5000, 64 * 1024 * 1024)
    assert set(m.readers) == set(mf.CODE_READERS) | {"gitmodules"} and m.member_rule.basis == "manifest-content" and m.aggregator_rule.role == "other"
    assert not set(mf.ALLOWED_FILES) & {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "Cargo.lock", "poetry.lock", "uv.lock", "go.sum", ".env", "CODEOWNERS"}
    assert all(r.evidence and r.tuned_on for r in (m.member_rule, m.aggregator_rule))


def _doc(**mr):
    d = yaml.safe_load((PROFILES / "code-repo.yaml").read_text())
    d["extends"] = []
    d["manifest_reading"].update(mr)
    return d


@pytest.mark.parametrize("change,msg", [
    ({"readers": ["package-json", "setup-py"]}, "readers"), ({"readers": []}, "readers"), ({"max_blobs": 5001}, "never raise"),
    ({"max_file_bytes": 0}, "max_file_bytes"), ({"bogus": 1}, "unknown key"),
    ({"aggregator_rule": {"id": "M-agg", "role": "component", "kind": "k", "basis": "manifest-content", "confidence": "high", "evidence": "e"}}, "NOT a component"),
    ({"member_rule": {"id": "M-aggregator", "role": "component", "kind": "k", "basis": "manifest-content", "confidence": "high", "evidence": "e"}}, "different ids"),
    ({"member_rule": {"id": "M-m", "role": "other", "kind": "k", "basis": "manifest-content", "confidence": "high", "evidence": "e"}}, "'component'"),
    ({"member_rule": {"id": "M-m", "role": "component", "kind": "k", "basis": "manifest-content", "confidence": "high"}}, "missing"),
])
def test_a_bad_manifest_reading_block_is_a_load_error(change, msg):
    with pytest.raises(ProfileError, match=msg):
        parse_profile(_doc(**change), "t", PROFILES)


def test_a_profile_may_tighten_a_cap():
    p = parse_profile(_doc(max_blobs=10, max_file_bytes=1024), "t", PROFILES)
    assert p.manifest_reading.max_blobs == 10 and p.manifest_reading.max_file_bytes == 1024
