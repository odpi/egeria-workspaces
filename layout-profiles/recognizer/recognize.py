"""Apply a layout profile to a list of repository paths. Names and sizes ONLY: no file is opened, no network, no Egeria.

    python -m recognizer.recognize PATHLIST --out OUTDIR [--profile generic-relevance] [--profiles-dir DIR]

PATHLIST: one repo-relative file path per line, optionally `path<TAB>size-in-bytes` (from `git ls-files`, a `git archive` listing, or
recognizer/listpaths.py; never from a dirty working tree). Paths use `/`, are relative, and appear once.

Outputs in OUTDIR (byte-identical for the same input and profile; nothing in them depends on time, run id or the tree sha):
  components.txt      one directory per line, the input format of the Phase 0 scorer (top-level components)
  components-all.txt  the same plus the parts of components (a manifest nested inside a component), for the manifest-probe regression
  candidate-copies.json  (with --copies-of KIND) groups of components of that kind whose sets of relative file names are identical (names only)
  findings.jsonl      one finding per (rule, directory) that a rule claimed, with the files and bytes it claimed, sorted by path then rule
                      (--per-file also writes findings-files.jsonl: one finding per file, large, for debugging)
  classes.json    files and bytes per role, per relevance and per rule; the classified, hidden and unclassified shares
  report.md       a short human summary

Rules are applied in order and the FIRST match wins. 'unclassified' is a result of its own, never dropped. Confidence, basis and evidence
are copied from the rule that matched, never invented. The recognizer streams a sorted list (it re-reads the file; it does not hold it) and
falls back to sorting in memory only when the list is not already sorted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

try:
    from .layout_profile import Profile, Rule, compose_profiles, load_profile
    from . import manifests as mf
except ImportError:                                   # run as a script
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from layout_profile import Profile, Rule, compose_profiles, load_profile  # type: ignore
    import manifests as mf  # type: ignore

UNCLASSIFIED = "unclassified"
SOURCE_EXTENSIONS = (".py", ".pyi", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".java", ".kt", ".scala", ".go", ".rs", ".rb", ".php", ".c", ".h", ".cc", ".cpp",
                     ".hpp", ".cs", ".swift", ".sh", ".sql")                    # a file with one of these endings is source-like (the no_source_files test)
_TOKEN = re.compile(r"[A-Z]+(?![a-z])|[A-Z]?[a-z]+|[0-9]+")


def name_tokens(name: str) -> set:
    """The whole words of a directory name, lower-case: split at punctuation and at case changes (`EgeriaRootCA` -> egeria, root, ca; `pki-certs` -> pki, certs)."""
    return {t.lower() for t in _TOKEN.findall(name)}


DOC_SKIP_NAMES = frozenset({"assets", "js", "css", "img", "images", "overrides", "snippets", "includes"})   # never a documentation section on their own
DEFAULT_PROFILES = Path(__file__).resolve().parent.parent / "profiles"


def finding_id(profile: Profile, rule_id: str, path: str) -> str:
    """Stable across surveys: the profile, its MAJOR version, the rule and the repo-relative path. No time, run id or tree sha."""
    return hashlib.sha256(f"{profile.profile_id}@{profile.major}|{rule_id}|{path}".encode("utf-8")).hexdigest()[:16]


def parse_line(line: str, number: int) -> tuple[str, int]:
    line = line.rstrip("\n").rstrip("\r")
    path, size = line, 0
    if "\t" in line:
        head, _, tail = line.rpartition("\t")
        if tail.isdigit():
            path, size = head, int(tail)
    if not path or path.startswith("/"):
        raise ValueError(f"line {number}: empty or absolute path {path!r}")
    if path.startswith("./"):
        path = path[2:]
    segs = path.split("/")
    if any(s in ("", "..") for s in segs):
        raise ValueError(f"line {number}: path {path!r} has an empty or '..' segment")
    return path, size


def read_rows(path: Path):
    """Yield (path, size) in sorted order; stream if the file is already sorted, otherwise sort in memory. Duplicates are an error."""
    def raw():
        with open(path, encoding="utf-8", newline="") as fh:
            for n, line in enumerate(fh, 1):
                if line.strip():
                    yield parse_line(line, n)

    prev, ordered = None, True
    for p, _ in raw():
        if prev is not None and p <= prev:
            if p == prev:
                raise ValueError(f"duplicate path {p!r}")
            ordered = False
            break
        prev = p
    if ordered:
        yield from raw()
        return
    rows = sorted(raw())
    for a, b in zip(rows, rows[1:]):
        if a[0] == b[0]:
            raise ValueError(f"duplicate path {a[0]!r}")
    yield from rows


class Recognizer:
    def __init__(self, profile: Profile, blob_source=None):
        self.p = profile
        self.blob_source = blob_source                # where manifests may be read from (a git object database or a tree); None = names and sizes only
        self.reading = None                           # the ManifestReading result of the last run (None when nothing was read)
        self.member_of: dict = {}                     # directory -> the Decl that declares it a workspace or module member
        self.aggregators: dict = {}                   # directory -> the Decl that makes it an aggregator (not a component)
        self.extras: dict = {}                        # directory -> extra finding fields (content evidence, notes)
        self.hidden_roots: list = []
        self.hidden_root_set: set = set()
        self._child_rel: dict = {}                    # directory -> the has_child_dir paths that exist directly below it
        self._file_count: dict = {}                   # directory -> number of files directly in it
        self._dir_count: dict = {}                    # directory -> number of sub-directories directly in it
        self.tooling_roots: set = set()               # directories an includeBuild marked as internal tooling (nothing below them is a component)
        self._children: dict | None = None            # directory -> its sub-directories (built when first needed)
        self._src_dirs: set = set()                   # candidate-named directories that have a source-like file below them (for no_source_files rules)
        self._gm_index: dict = {}                     # directory -> (path, size) of its .gitmodules
        self._gm_cache: dict = {}                     # directory -> the set of directories its .gitmodules declares as submodules
        self.submodules_exempt: list = []             # (outer, path) pairs the nested-repository rule did NOT claim because .gitmodules declares them
        self.file_components: dict = {}               # path of a FILE that is a component (a doc section that is one page) -> (rule, site directory, extra fields)
        self.docs_stats = {"sites_read": 0, "sections": 0, "unresolved": 0, "fallback_sections": 0, "landing_pages": 0, "merged": 0, "translations": 0, "inherit_warnings": 0}
        self.file_rules = [r for r in profile.rules if not r.is_dir_rule]
        self.dir_rules = [r for r in profile.rules if r.is_dir_rule]
        self.needed_names = set()                    # file names (and entry names) whose presence in a directory a dir rule asks about
        self.needed_dir_entries = set()              # names of SUB-DIRECTORIES a dir rule asks about (has_entry: .git is a file OR a directory)
        for r in self.dir_rules:
            self.needed_names |= r.has_files | r.parent_has_files | r.has_entries | r.ancestor_entries
            self.needed_dir_entries |= r.has_entries | r.ancestor_entries
        self.hidden_dir_rules = [r for r in self.dir_rules if r.grain == "subtree" and r.relevance == "hidden"]
        self.child_first: dict = {}                   # first segment of a has_child_dir path -> the paths that start with it
        self.nosource_names = set()
        for r in self.dir_rules:
            if r.no_source:
                self.nosource_names |= r.names
            for cp in r.child_dirs:
                self.child_first.setdefault(cp.split("/")[0], set()).add(cp)
        self.component_dirs: set = set()             # directories a component rule claims (filled by index_directories); '' is the root
        # hidden subtree rules that depend on the path alone (a rule that also tests a file name cannot say a DIRECTORY is hidden)
        self.hidden_subtrees = [r for r in self.file_rules if r.grain == "subtree" and r.relevance == "hidden"
                                and set(r.match) <= {"path_segment", "path_glob"}]
        self.claims: dict[str, Rule] = {}             # directory -> the first dir rule that claims it
        self.subtree_claims: dict[str, set] = {}      # rule id -> directories claimed with grain subtree

    def inside_hidden_subtree(self, d: str) -> bool:
        """Is directory `d` inside (or at the root of) a subtree that a hidden-relevance path rule claims? Such a directory can never be a
        component: a pyproject.toml inside node_modules is vendored, not a component."""
        if not self.hidden_subtrees or not d:
            return False
        segs = d.split("/")
        for r in self.hidden_subtrees:
            if r.segments and any(x in r.segments for x in segs):
                return True
            if r.root_globs and any(g.match("/".join(segs[:i + 1])) for g in r.root_globs for i in range(len(segs))):
                return True
        return False

    # ---- directory rules (has_file / parent_has_file) -------------------------------------------------------------------
    def _dir_rule_matches(self, r: Rule, d: str, own: set, par: set, anc: list, holders: dict, segs: list, name: str, subdirs: dict | None = None) -> bool:
        subdirs = subdirs if subdirs is not None else {}
        if r.has_files and not (r.has_files & own):
            return False
        if r.has_entries and not (r.has_entries & (own | subdirs.get(d, set()))):
            return False
        if r.ancestor_entries and not any(r.ancestor_entries & (holders.get(a, set()) | subdirs.get(a, set())) for a in anc):
            return False
        if r.no_source and d in self._src_dirs:
            return False
        if r.child_dirs and not (r.child_dirs & self._child_rel.get(d, set())):
            return False
        if r.orphaned:
            parent = d[:d.rfind("/")] if "/" in d else ""
            if self._file_count.get(parent, 0) or self._dir_count.get(parent, 0) != 1:
                return False
        if r.parent_tokens:
            parent_name = segs[-2] if len(segs) >= 2 else ""
            if not (r.parent_tokens & name_tokens(parent_name)):
                return False
        if r.parent_has_files and not (r.parent_has_files & par):
            return False
        if r.segments and not any(s in r.segments for s in segs):
            return False
        if r.segment_res and not any(rx.search(sg) for sg in segs for rx in r.segment_res):
            return False
        if r.globs and (not d or not any(g.match(d) for g in r.globs)):
            return False
        if r.names and name not in r.names:
            return False
        if r.name_res and not any(rx.search(name) for rx in r.name_res):
            return False
        return True

    def index_directories(self, path_list: Path) -> None:
        if not self.dir_rules:
            return
        holders: dict[str, set] = {}
        subdirs: dict[str, set] = {}                              # directory -> names of SUB-DIRECTORIES that a rule asked about (has_entry)
        all_dirs: set = set()
        need_all = any(not (r.has_files or r.has_entries) for r in self.dir_rules)   # a rule that does not start from an entry must see every directory
        mr = self.p.manifest_reading if self.blob_source is not None else None
        mr_any = self.p.manifest_reading
        collect_dirs = need_all or mr is not None or (mr_any is not None and mr_any.fallback_site_rule is not None)
        candidates_m: list = []                                  # (path, size) of files whose NAME is on the closed list of manifests
        if mr is not None:
            self.reading = mf.ManifestReading()
        for path, size in read_rows(path_list):
            cut = path.rfind("/")
            d, name = (path[:cut], path[cut + 1:]) if cut >= 0 else ("", path)
            if name in self.needed_names:
                holders.setdefault(d, set()).add(name)
            if self.needed_dir_entries:                      # a sub-directory entry: `.git/HEAD` under `x` makes `.git` an entry of `x`
                segs = path.split("/")
                for i in range(len(segs) - 1):
                    if segs[i] in self.needed_dir_entries:
                        subdirs.setdefault("/".join(segs[:i]), set()).add(segs[i])
            if self.nosource_names and path.endswith(SOURCE_EXTENSIONS):
                segs = path.split("/")
                for i in range(len(segs) - 1):
                    if segs[i] in self.nosource_names:
                        self._src_dirs.add("/".join(segs[:i + 1]))
            if self.child_first:
                segs = path.split("/")
                for i in range(len(segs) - 1):
                    for cp in self.child_first.get(segs[i], ()):
                        parts = cp.split("/")
                        if segs[i:i + len(parts)] == parts and i + len(parts) <= len(segs) - 1:
                            self._child_rel.setdefault("/".join(segs[:i]), set()).add(cp)       # `docs/javadoc` directly below `.../build`
            if mr is not None and name in mf.ALLOWED_FILES:
                candidates_m.append((path, size))
                if name == ".gitmodules":
                    self._gm_index[d] = (path, size)
            if collect_dirs:
                self._file_count[d] = self._file_count.get(d, 0) + 1
                while d and d not in all_dirs:
                    all_dirs.add(d)
                    d = d[:d.rfind("/")] if "/" in d else ""
                    self._dir_count[d] = self._dir_count.get(d, 0) + 1
        candidates = set(holders) | set(subdirs) | all_dirs if need_all else set(holders) | set(subdirs)
        order = sorted(candidates)

        def context(d):
            parent = d[:d.rfind("/")] if "/" in d else ""
            segs = d.split("/") if d else []
            anc = [""] + ["/".join(segs[:i]) for i in range(1, len(segs))] if d else []
            return holders.get(d, set()), (holders.get(parent, set()) if d else set()), anc, segs, (d.rsplit("/", 1)[-1] if d else "")

        # pass 1: a directory that a HIDDEN subtree dir rule claims (a nested repository) is vendored, whatever manifest it holds: vendored wins
        hidden_roots: list = []
        for d in order:
            if self.inside_hidden_subtree(d) or self._under_hidden_root(d):
                continue
            own, par, anc, segs, name = context(d)
            for r in self.hidden_dir_rules:
                if self._dir_rule_matches(r, d, own, par, anc, holders, segs, name, subdirs):
                    if mr is not None and r.id == mr.submodule_rule and self._declared_submodule(d, mr):
                        continue                               # the outer repository's .gitmodules declares it: part of the outer repository, not vendored
                    self.claims[d] = r
                    self.subtree_claims.setdefault(r.id, set()).add(d)
                    hidden_roots.append(d)
                    self.hidden_root_set.add(d)
                    break
        self.hidden_roots = hidden_roots
        if mr is not None:
            self._read_manifests(mr, candidates_m)
            if self.reading is not None and "mkdocs" in mr.readers:
                self._apply_docs_dirs(mr, all_dirs)
        # pass 2: every other directory rule
        for d in order:
            if self.inside_hidden_subtree(d) or self._under_hidden_root(d):
                continue                                       # vendored (or any hidden subtree) wins over a manifest inside it
            own, par, anc, segs, name = context(d)
            for r in self.dir_rules:
                if r in self.hidden_dir_rules or not self._dir_rule_matches(r, d, own, par, anc, holders, segs, name, subdirs):
                    continue
                self.claims[d] = r
                if r.grain == "subtree":
                    self.subtree_claims.setdefault(r.id, set()).add(d)
                break
        if mr is not None and self.reading is not None:
            dir_files: dict = {}
            for path, _ in candidates_m:
                dir_files.setdefault(path.rpartition("/")[0], set()).add(path.rpartition("/")[2])
            self._apply_manifest_content(mr, all_dirs, dir_files)
            if "mkdocs" in mr.readers:
                self._apply_docs_sections(mr, path_list, all_dirs)
        if self.p.manifest_reading is not None and self.p.manifest_reading.fallback_site_rule is not None:
            self._apply_generator_sites(self.p.manifest_reading, path_list, all_dirs, holders)
        self._apply_structural_dirs(path_list, all_dirs)
        self.component_dirs = {d for d, r in self.claims.items() if r.grain == "component"}

    # ---- structural claims by file kinds and names (N6) -------------------------------------------------------------------
    def _structural_rule(self, sr: dict) -> Rule:
        return Rule(id=sr["id"], match={}, role="component", relevance="primary", kind=sr["kind"], grain="component", basis=sr["basis"], confidence=sr["confidence"],
                    evidence=sr["evidence"], origin="structural", tuned_on=tuple(sr.get("tuned_on", [])))

    def _structural_blocked(self, d: str, exclusion: bool) -> bool:
        """May `d` NOT be claimed by a structural rule? It is claimed already, hidden, inside a claimed component (the repository root does not count), or, for the
        deployment and notebook rules, a fixture, sample or tooling path."""
        if d in self.claims or self._dir_is_hidden(d):
            return True
        if exclusion and self._segment_exclusion(d) is not None:
            return True
        parts = d.split("/")
        for i in range(1, len(parts)):
            if "/".join(parts[:i]) in self.tooling_roots:
                return True
            a = self.claims.get("/".join(parts[:i]))
            if a is not None and a.grain == "component":
                return True
        return False

    def _claim_structural(self, d: str, sr: dict, extra: dict) -> None:
        self.claims[d] = self._structural_rule(sr)
        self.extras.setdefault(d, {}).update({"structure_rule_id": sr["id"], "structure_op": sr["op"], "structure_basis": sr["basis"],
                                              "structure_confidence": sr["confidence"], "structure_evidence": sr["evidence"], **extra})

    def _apply_structural_dirs(self, path_list: Path, dirs: set) -> None:
        """AFTER every other claim. Four structural rules by file KINDS and NAMES, never by a repository's folder names:
        (a) a directory holding a compose file (by name, or a YAML file whose top-level `services` key is a mapping, read under the manifest caps) is a deployment;
            the unit is the child of the nearest GROUPING folder (a folder with two or more children that hold deployments), else the outermost compose directory;
        (b) the shallowest directory with at least `min` notebooks below it, or that holds an Obsidian vault (.obsidian/), is a notebooks component;
        (c)/(d) a top-level directory of at least `min` files, at least `share` of them of the listed extensions (and, for data, holding no code), is a component of that kind."""
        ops = [sr for sr in self.p.structural if sr["op"] != "sibling-manifests-top-level"]
        if not ops:
            return
        compose_ops = [sr for sr in ops if sr["op"] == "compose-deployment"]
        nb_ops = [sr for sr in ops if sr["op"] == "notebook-folder"]
        ext_ops = [sr for sr in ops if sr["op"] == "mostly-extension-folder"]
        compose_rx = [re.compile(x) for sr in compose_ops for x in sr.get("name_regex", [])]
        want_ext = tuple(sorted({e for sr in ext_ops for e in sr["extensions"]}))
        named_compose: set = set()
        yaml_cands: list = []
        chart_dirs: set = set()
        ipynb: dict = {}
        vaults: set = set()
        top: dict = {}
        hidden_cache: dict = {}

        def dir_hidden(d):
            if d not in hidden_cache:
                hidden_cache[d] = self._dir_is_hidden(d)
            return hidden_cache[d]

        for path, size in read_rows(path_list):
            cut = path.rfind("/")
            d, name = (path[:cut], path[cut + 1:]) if cut >= 0 else ("", path)
            if dir_hidden(d):
                continue
            first = path.split("/", 1)[0] if cut >= 0 else None
            if name == "Chart.yaml":
                chart_dirs.add(d)
            if compose_rx and any(rx.search(name) for rx in compose_rx):
                if not self._file_is_hidden(path):
                    named_compose.add(d)
            elif compose_ops and name.endswith((".yml", ".yaml")):
                yaml_cands.append((path, size))
            if nb_ops:
                if name.endswith(".ipynb") and not self._file_is_hidden(path):
                    parts = path.split("/")[:-1]
                    for i in range(1, len(parts) + 1):
                        ipynb["/".join(parts[:i])] = ipynb.get("/".join(parts[:i]), 0) + 1
                if "/.obsidian/" in "/" + path:
                    seg = path.split("/")
                    vaults.add("/".join(seg[:seg.index(".obsidian")]))
            if ext_ops and first is not None and first not in self.claims and not dir_hidden(first):
                if self._file_is_hidden(path):
                    continue
                st = top.setdefault(first, {"files": 0, "ext": {}, "code": False})
                st["files"] += 1
                for e in want_ext:
                    if name.endswith(e):
                        st["ext"][e] = st["ext"].get(e, 0) + 1
                        break
                if name.endswith(SOURCE_EXTENSIONS):
                    st["code"] = True

        # (a) deployments
        for sr in compose_ops:
            mr = self.p.manifest_reading
            found = set(named_compose)
            key = sr.get("yaml_key")
            if key and self.blob_source is not None and mr is not None and "compose-services" in mr.readers and self.reading is not None:
                cands = [(p, sz) for p, sz in yaml_cands if p.rpartition("/")[0] not in found
                         and not (p.rpartition("/")[0].rpartition("/")[2] == "templates" and p.rpartition("/")[0].rpartition("/")[0] in chart_dirs)]
                found |= mf.read_yaml_key(cands, self.blob_source, self._file_is_hidden, key, out=self.reading, max_file_bytes=mr.max_file_bytes,
                                          max_blobs=mr.max_blobs, max_total_bytes=mr.max_total_bytes)
            cdirs = sorted(c for c in found if c and not self._structural_blocked(c, True))
            kids: dict = {}
            for c in cdirs:
                parts = c.split("/")
                for i in range(1, len(parts)):
                    kids.setdefault("/".join(parts[:i]), set()).add(parts[i])
            groups = {g for g, k in kids.items() if len(k) >= 2 and g not in found}
            units: dict = {}
            for c in cdirs:
                parts = c.split("/")
                unit = None
                for i in range(1, len(parts)):                     # the shallowest grouping ancestor: the unit is its child on the way to c
                    if "/".join(parts[:i]) in groups:
                        unit = "/".join(parts[:i + 1])
                        break
                if unit is None:                                    # no grouping folder: the outermost compose directory on the way
                    unit = next(("/".join(parts[:i]) for i in range(1, len(parts) + 1) if "/".join(parts[:i]) in found), c)
                units.setdefault(unit, []).append(c)
            for unit in sorted(units):
                if not self._structural_blocked(unit, True):
                    self._claim_structural(unit, sr, {"deployment_dirs": len(units[unit])})

        # (b) notebooks
        for sr in nb_ops:
            cands = {d for d, n in ipynb.items() if n >= sr["min"]} | vaults
            for d in sorted(cands, key=lambda x: (x.count("/"), x)):
                if d and not self._structural_blocked(d, True):
                    self._claim_structural(d, sr, {"notebooks": ipynb.get(d, 0), "vault": d in vaults})

        # (c) and (d) top-level directories that are mostly one kind of file
        for sr in ext_ops:
            for t in sorted(top):
                st = top[t]
                n = sum(st["ext"].get(e, 0) for e in sr["extensions"])
                if st["files"] < sr["min"] or n < sr["share"] * st["files"] or (sr.get("no_code") and st["code"]):
                    continue
                if not self._structural_blocked(t, False):
                    self._claim_structural(t, sr, {"files_counted": st["files"], "share": round(n / st["files"], 3)})

    # ---- manifest reading (M6) --------------------------------------------------------------------------------------------
    def _under_hidden_root(self, d: str) -> bool:
        """Is `d` a hidden-subtree root that a directory rule claimed, or inside one? (a walk up the prefixes against a set: no scan of the roots)"""
        if not self.hidden_root_set:
            return False
        while d:
            if d in self.hidden_root_set:
                return True
            d = d[:d.rfind("/")] if "/" in d else ""
        return False

    def _dir_is_hidden(self, d: str) -> bool:
        return self.inside_hidden_subtree(d) or self._under_hidden_root(d)

    def _file_is_hidden(self, path: str) -> bool:
        rule, _, _ = self.classify(path)
        return rule is not None and rule.relevance == "hidden"

    def _declared_submodule(self, d: str, mr) -> bool:
        """Does the .gitmodules of an enclosing, visible repository declare `d` as a submodule? Only the `path` entries are read (never the url), and only
        where a blob source is given; the file is read at most once per directory and counts against the caps."""
        parts = d.split("/")
        for i in range(len(parts)):                              # proper ancestors, shallowest first: '' (the root), a, a/b ...
            a = "/".join(parts[:i])
            if a not in self._gm_index or self._dir_is_hidden(a):
                continue
            if a not in self._gm_cache:
                path, size = self._gm_index[a]
                before = len(self.reading.log)
                mf.read_manifests([(path, size)], self.blob_source, {"gitmodules"}, self._file_is_hidden, max_file_bytes=mr.max_file_bytes,
                                  max_blobs=mr.max_blobs, max_total_bytes=mr.max_total_bytes, out=self.reading)
                decls = self.reading.decls.get(path, [])
                self._gm_cache[a] = {self._join(a, rel) for dec in decls for m in dec.members for rel in [self._safe_rel(m)] if rel not in (None, ".")}
            if d in self._gm_cache[a]:
                self.submodules_exempt.append((a or ".", d))
                return True
        return False

    def _read_manifests(self, mr, candidates: list) -> None:
        self.reading = mf.read_manifests(candidates, self.blob_source, set(mr.readers) - {"gitmodules"}, self._file_is_hidden, max_file_bytes=mr.max_file_bytes,
                                         max_blobs=mr.max_blobs, max_total_bytes=mr.max_total_bytes, out=self.reading)

    @staticmethod
    def _safe_rel(p):
        """A folder name from a manifest as a clean relative path ('' = the site directory itself), or None when absolute, with `..`, or not a string."""
        if not isinstance(p, str):
            return None
        q = p.strip().replace("\\", "/")
        if q.startswith("./"):
            q = q[2:]
        q = q.rstrip("/")
        if q.startswith("/") or any(x == ".." for x in q.split("/")) or (len(q) > 1 and q[1] == ":"):
            return None
        return "." if q == "" else q

    @staticmethod
    def _join(base: str, rel: str) -> str:
        return base if rel in (".", "") else (base + "/" + rel if base else rel)

    def _mkdocs_decls(self):
        for path in sorted(self.reading.decls):
            for decl in self.reading.decls[path]:
                if decl.reader == "mkdocs":
                    yield decl

    def _apply_docs_dirs(self, mr, dirs: set) -> None:
        """BEFORE the component claims: where mkdocs.yml names another docs_dir or site_dir, claim them as the profile's content and output rules claim the
        defaults (the built site becomes a hidden subtree that nothing inside can escape)."""
        by_id = {r.id: r for r in self.p.rules}
        for decl in self._mkdocs_decls():
            site = decl.directory
            if self._dir_is_hidden(site):
                continue
            for key, rid, default in (("docs_dir", mr.docs_content_rule, "docs"), ("site_dir", mr.site_output_rule, "site")):
                raw = getattr(decl, key)
                rel = default if raw is None else self._safe_rel(raw)
                if rel is None or rel == "." or rid is None:
                    continue
                d = self._join(site, rel)
                if d in dirs and d not in self.claims and not self._dir_is_hidden(d):
                    r = by_id[rid]
                    self.claims[d] = r
                    self.subtree_claims.setdefault(r.id, set()).add(d)
                    if r.relevance == "hidden":
                        self.hidden_roots.append(d)
                        self.hidden_root_set.add(d)

    def _apply_docs_sections(self, mr, path_list: Path, dirs: set) -> None:
        """AFTER the component claims. Each top-level nav entry of a read mkdocs.yml is a `doc-section` component, a part of its site. SECTION IDENTITY:
        collect the entry's page paths in nav order (sub-groups included); skip URLs and anchors; keep those that resolve to a FILE of the path list inside
        docs_dir. If every kept page sits under ONE top-level folder of docs_dir (at any depth below it; a page directly in docs_dir does not) the identity
        is that folder, otherwise the first kept page's file path. No kept page: no component (unresolved). The entry for docs_dir/index.md is the landing
        page, not a section. Where mkdocs.yml has no nav, each top-level folder of docs_dir that holds pages (not assets, js, css, img, images, overrides,
        snippets, includes) is a section of LOW confidence."""
        import posixpath
        sites = []
        wanted: set = set()
        fallback_roots: dict = {}
        inherit: dict = {}                                       # site directory -> (the INHERIT string, the resolved path of its target or None)
        for decl in self._mkdocs_decls():
            site = decl.directory
            r = self.claims.get(site)
            if r is None or r.grain != "component" or self._dir_is_hidden(site):
                continue
            ex = self.extras.setdefault(site, {})
            ex.setdefault("evidence_file", decl.file)
            ex.setdefault("evidence_blob", decl.blob)
            if decl.inherit and mr.translation_rule is not None:
                q = decl.inherit.replace("\\", "/")
                full = None if (q.startswith("/") or (len(q) > 1 and q[1] == ":")) else posixpath.normpath(posixpath.join(site, q) if site else q)
                if full is not None and (full.startswith("..") or full in (".", "")):
                    full = None                                  # above the repository root: never resolved
                inherit[site] = (decl.inherit, full)
                if full is not None:
                    wanted.add(full)
            dd = "docs" if decl.docs_dir is None else self._safe_rel(decl.docs_dir)
            if dd is None:
                ex["unresolved_docs_dir"] = decl.docs_dir if isinstance(decl.docs_dir, str) else None
                continue
            docs_root = self._join(site, dd)
            ex["docs_dir"] = dd
            ex["site_dir"] = "site" if decl.site_dir is None else (self._safe_rel(decl.site_dir) or "site")
            self.docs_stats["sites_read"] += 1
            entries = []
            for sec in decl.sections:
                kept = []
                for raw in sec["pages"]:
                    if mf.is_nav_url_or_anchor(raw):
                        continue
                    q = raw.strip().split("#", 1)[0].replace("\\", "/")
                    if q.startswith("./"):
                        q = q[2:]
                    if not q or q.startswith("/") or any(x in ("..", "") for x in q.split("/")):
                        continue
                    full = self._join(docs_root, posixpath.normpath(q)) if docs_root else posixpath.normpath(q)
                    kept.append(full)
                    wanted.add(full)
                entries.append((sec["title"], sec["pages"], kept))
            sites.append((decl, site, docs_root, entries))
            if not decl.has_nav:
                fallback_roots[docs_root] = site
        if not sites:
            return
        existing: set = set()
        tops: dict = {root: set() for root in fallback_roots}
        for path, _ in read_rows(path_list):
            if path in wanted:
                existing.add(path)
            if fallback_roots and path.endswith((".md", ".mdx", ".rst")):
                for root in fallback_roots:
                    pre = root + "/" if root else ""
                    if path.startswith(pre) and "/" in path[len(pre):]:
                        tops[root].add(path[len(pre):].split("/", 1)[0])
        # translations: a config whose INHERIT resolves to ANOTHER site's mkdocs.yml (a file of the path list, never read through) makes its directory a translation of that site
        base_of: dict = {}
        warnings: dict = {}
        for site, (raw, full) in inherit.items():
            if full is None:
                warnings[site] = f"INHERIT {raw!r} is not a path inside the repository"
            elif full not in existing:
                warnings[site] = f"INHERIT target not found: {full}"
            elif full.rpartition("/")[2] not in ("mkdocs.yml", "mkdocs.yaml"):
                warnings[site] = f"INHERIT target is not a mkdocs.yml: {full}"
            elif full.rpartition("/")[0] == site or self._dir_is_hidden(full.rpartition("/")[0]):
                warnings[site] = f"INHERIT target is not another site: {full}"
            else:
                base_of[site] = full.rpartition("/")[0]
        for site in sorted(base_of):                             # an INHERIT cycle makes none of its members a translation
            seen_c, cur = {site}, base_of[site]
            while cur in base_of:
                if cur in seen_c:
                    warnings[site] = f"INHERIT cycle through {cur or '.'}"
                    break
                seen_c.add(cur)
                cur = base_of[cur]
        base_of = {k: v for k, v in base_of.items() if k not in warnings}
        for site, base in base_of.items():
            decl = next(x[0] for x in sites if x[1] == site)
            self.claims[site] = mr.translation_rule
            self.extras.setdefault(site, {}).update({"site": base, "translation_of": base or ".", "evidence_file": decl.file, "evidence_field": "INHERIT",
                                                     "evidence_blob": decl.blob, "inherit": decl.inherit})
            self.docs_stats["translations"] += 1
        for site, msg in warnings.items():
            self.extras.setdefault(site, {})["inherit_warning"] = msg
            self.docs_stats["inherit_warnings"] += 1
        for decl, site, docs_root, entries in sites:
            if site in base_of:
                continue                                         # a translation: its nav entries are NOT sections
            ex = self.extras[site]
            landing, unresolved, seen = None, [], set()
            ev = {"evidence_file": decl.file, "evidence_field": "nav", "evidence_blob": decl.blob, "site": site or "."}
            for title, raw_pages, kept in entries:
                kept = [k for k in kept if k in existing]
                if not kept:
                    unresolved.append(title or raw_pages[0])
                    continue
                if kept == [self._join(docs_root, "index.md")]:
                    landing = kept[0]
                    continue
                prefix = docs_root + "/" if docs_root else ""
                tops_of = {k[len(prefix):].split("/", 1)[0] for k in kept if "/" in k[len(prefix):]}
                if len(tops_of) == 1 and all("/" in k[len(prefix):] for k in kept):
                    identity, how = prefix + next(iter(tops_of)), "folder"
                else:
                    identity, how = kept[0], "first-page"
                if identity in seen:
                    self.docs_stats["merged"] += 1
                    continue
                seen.add(identity)
                info = {**ev, "nav_title": title, "identity": how, "pages_kept": len(kept)}
                self._add_section(mr.section_rule, identity, how, site, info, dirs)
            if not decl.has_nav:
                for top in sorted(tops.get(docs_root, ())):
                    if top.lower() in DOC_SKIP_NAMES or top.startswith((".", "_")):
                        continue
                    identity = self._join(docs_root, top)
                    if identity in seen:
                        continue
                    seen.add(identity)
                    info = {**ev, "evidence_field": "docs_dir", "identity": "folder-fallback", "pages_kept": None, "nav_title": None}
                    self._add_section(mr.fallback_section_rule, identity, "folder", site, info, dirs)
                    self.docs_stats["fallback_sections"] += 1
            if landing:
                ex["landing_page"] = landing
                self.docs_stats["landing_pages"] += 1
            if unresolved:
                ex["unresolved_nav"] = unresolved[:50]
                self.docs_stats["unresolved"] += len(unresolved)

    def _apply_generator_sites(self, mr, path_list: Path, dirs: set, holders: dict) -> None:
        """A documentation site recognized by its generator's config FILE NAME only (the file is never read): its content folder is the generator's default,
        `docs/` beside the config, and the fallback applies there: one low-confidence section per top-level folder of that folder that holds pages."""
        sites = {}
        marker_rule = next((r for r in self.p.rules if r.id == mr.fallback_site_rule), None)
        markers = marker_rule.has_files if marker_rule is not None else frozenset()
        for d in sorted(holders):                           # by the marker file NAME, whoever claimed the directory (in a composition the first-listed profile may have)
            if holders[d] & markers and not self._dir_is_hidden(d):
                sites[self._join(d, "docs")] = d
        if not sites:
            return
        tops: dict = {root: set() for root in sites}
        for path, _ in read_rows(path_list):
            if path.endswith((".md", ".mdx", ".rst")):
                for root in sites:
                    pre = root + "/"
                    if path.startswith(pre) and "/" in path[len(pre):]:
                        tops[root].add(path[len(pre):].split("/", 1)[0])
        for root, site in sites.items():
            ex = self.extras.setdefault(site, {})
            ex["docs_dir"] = "docs"
            for top in sorted(tops[root]):
                if top.lower() in DOC_SKIP_NAMES or top.startswith((".", "_")):
                    continue
                info = {"site": site or ".", "identity": "folder-fallback", "evidence_field": "generator-default-docs-dir", "pages_kept": None, "nav_title": None}
                self._add_section(mr.fallback_section_rule, self._join(root, top), "folder", site, info, dirs)
                self.docs_stats["fallback_sections"] += 1

    def _add_section(self, rule, identity: str, how: str, site: str, info: dict, dirs: set) -> None:
        if how == "first-page":
            if not self._dir_is_hidden(identity.rpartition("/")[0]):
                self.file_components[identity] = (rule, site, info)
                self.docs_stats["sections"] += 1
        elif identity in dirs and not self._dir_is_hidden(identity) and identity not in self.claims:
            self.claims[identity] = rule
            self.extras.setdefault(identity, {}).update(info)
            self.docs_stats["sections"] += 1

    def _segment_exclusion(self, d: str):
        """A declared member (it has no manifest of its own to be claimed by) whose path has a fixture, sample, template or tooling segment is claimed by the
        profile's exclusion rule for that segment instead of the member rule: the same principle as for a manifest project."""
        segs = d.split("/")
        for r in self.dir_rules:
            if r.role in ("fixture", "example", "tooling", "test-support") and r.grain == "dir" and (r.segment_res or r.segments):
                if (r.segments and any(x in r.segments for x in segs)) or (r.segment_res and any(rx.search(x) for x in segs for rx in r.segment_res)):
                    return r
        return None

    def _apply_included_builds(self, mr, decl, dirs: set) -> None:
        """D3: `includeBuild('dir')` in settings.gradle(.kts) (a string literal, never evaluated) marks `dir` as internal tooling: the directory and every manifest
        project below it are role tooling, not components. A path that leaves the repository or is not a directory of the list is ignored."""
        import posixpath
        rule = mr.included_build_rule
        if rule is None or not decl.included_builds:
            return
        for raw in decl.included_builds:
            q = raw.replace("\\", "/")
            if q.startswith("/") or (len(q) > 1 and q[1] == ":"):
                continue
            full = posixpath.normpath(posixpath.join(decl.directory, q) if decl.directory else q)
            if full.startswith("..") or full in (".", "") or full not in dirs or self._dir_is_hidden(full):
                continue
            self.tooling_roots.add(full)
            for d in [full] + sorted(x for x in list(self.claims) if x.startswith(full + "/")):
                c = self.claims.get(d)
                if d == full or (c is not None and c.grain == "component"):
                    self.claims[d] = rule
                    self.extras.setdefault(d, {}).update({"tooling_of": decl.directory or ".", "evidence_file": decl.file, "evidence_field": "includeBuild", "evidence_blob": decl.blob})
                    self.member_of.pop(d, None)
            self.docs_stats.setdefault("included_builds", 0)

    def _gradle_aggregators(self, members: list, dirs: set) -> set:
        """Included Gradle projects that only AGGREGATE: no file of their own and every sub-directory an included project too (a parent such as `a` for
        `include 'a:b', 'a:c'`)."""
        inc = set(members)
        if self._children is None:
            self._children = {}
            for x in dirs:
                self._children.setdefault(x[:x.rfind("/")] if "/" in x else "", set()).add(x)
        out = set()
        for m in inc:
            kids = self._children.get(m, set())
            if kids and not self._file_count.get(m, 0) and kids <= inc:
                out.add(m)
        return out

    def _apply_manifest_content(self, mr, dirs: set, dir_files: dict) -> None:
        """Turn what the manifests declared into claims: a declared member is a component (claimed by the member rule where no manifest rule
        already claimed it); a manifest directory that only AGGREGATES its members is not one. Hidden directories never take part."""
        rd = self.reading
        ladder = {"high": "medium", "medium": "low", "low": "low"}
        for path in sorted(rd.decls):
            for decl in rd.decls[path]:
                if decl.reader not in mf.CODE_READERS:
                    continue                                       # mkdocs and gitmodules declarations are not workspace members
                members, unresolved = mf.resolve_members(decl, dirs, dir_files)
                members = [m for m in members if not self._dir_is_hidden(m)]
                d = decl.directory
                ex = self.extras.setdefault(d, {})
                if decl.members:
                    ex.setdefault("evidence_file", decl.file)
                    ex.setdefault("evidence_field", decl.field)
                    ex.setdefault("evidence_blob", decl.blob)
                    ex["members_declared"] = ex.get("members_declared", 0) + len(members)
                    if unresolved:
                        ex["unresolved_members"] = sorted(set(ex.get("unresolved_members", [])) | set(unresolved))
                if decl.name and "manifest_name" not in ex:
                    ex["manifest_name"] = decl.name
                if decl.reader == "gradle" and members:
                    aggs = self._gradle_aggregators(members, dirs)
                    ex["gradle_aggregators"] = sorted(aggs)
                    for a in aggs:                                  # an included project whose only children are other included projects is not a component
                        if a not in self.claims:
                            self.claims[a] = mr.aggregator_rule
                            self.extras.setdefault(a, {}).update({"member_of": d or ".", "evidence_file": decl.file, "evidence_field": decl.field, "evidence_blob": decl.blob})
                    members = [m for m in members if m not in aggs]
                for m in members:
                    if m in self.member_of:
                        continue
                    self.member_of[m] = decl
                    me = self.extras.setdefault(m, {})
                    me.update({"member_of": d or ".", "evidence_file": decl.file, "evidence_field": decl.field, "evidence_blob": decl.blob})
                    if m not in self.claims:
                        self.claims[m] = self._segment_exclusion(m) or mr.member_rule
                if decl.aggregator and d != "" and d in self.claims and self.claims[d].grain == "component" and self.claims[d].basis == "manifest":
                    self.aggregators[d] = decl
                    ex["manifest_kind"] = self.claims[d].kind
                    self.claims[d] = mr.aggregator_rule
        for path in sorted(rd.decls):                          # D3: included builds are internal tooling (after every member claim, so nothing below them stays a component)
            for decl in rd.decls[path]:
                if decl.reader == "gradle":
                    self._apply_included_builds(mr, decl, dirs)
        for path, note in sorted(rd.notes.items()):
            d = path.rpartition("/")[0]
            if d not in self.claims or note == "missing":
                continue
            ex = self.extras.setdefault(d, {})
            if note.startswith("parse_error"):
                ex["parse_error"] = note.split(": ", 1)[1]
                ex["confidence"] = ladder[self.claims[d].confidence]
            else:
                ex["skipped"] = note

    # ---- file rules -----------------------------------------------------------------------------------------------------
    def _under_component(self, dirs: list, root_only: bool) -> bool:
        if not self.component_dirs:
            return False
        if root_only:
            return "/".join(dirs) in self.component_dirs
        return "" in self.component_dirs or any("/".join(dirs[:i + 1]) in self.component_dirs for i in range(len(dirs)))

    def _file_match(self, r: Rule, path: str, name: str, dirs: list, dirset: set):
        """Does FILE rule `r` claim this file? Returns (rule, node_path, node_grain) or None."""
        idx = -1
        if r.segments:
            if not (r.segments & dirset):
                return None
            idx = next(i for i, s in enumerate(dirs) if s in r.segments)
        if r.names and name not in r.names:
            return None
        if r.extensions and not any(name.endswith(e) for e in r.extensions):
            return None
        if r.name_res and not any(rx.search(name) for rx in r.name_res):
            return None
        if r.globs and not any(g.match(path) for g in r.globs):
            return None
        if r.scope and not self._under_component(dirs, r.scope == "root"):
            return None
        if r.grain == "subtree":
            if idx < 0:
                idx = next((i for i in range(len(dirs)) if any(g.match("/".join(dirs[:i + 1])) for g in r.root_globs)), -1)
            if idx < 0:
                return None
            return r, "/".join(dirs[:idx + 1]), "subtree"
        return r, path, "dir"

    def classify(self, path: str):
        """Return (rule, node_path, node_grain) for the first rule that claims this file, or (None, None, None). The rules come first (in
        order); the FILE-ROLE layer (profile.file_roles) is consulted only for a file no rule claimed, so it can never un-hide a file."""
        parts = path.split("/")
        name = parts[-1]
        dirs = parts[:-1]
        dirset = set(dirs)
        for r in self.p.rules:
            if r.is_dir_rule:
                claimed = self.subtree_claims.get(r.id)
                if claimed and r.grain == "subtree":
                    for i in range(len(dirs)):
                        pre = "/".join(dirs[:i + 1])
                        if pre in claimed:
                            return r, pre, "subtree"
                continue
            hit = self._file_match(r, path, name, dirs, dirset)
            if hit:
                return hit
        for r in self.p.file_roles:
            hit = self._file_match(r, path, name, dirs, dirset)
            if hit:
                return hit
        return None, None, None

    def finding(self, rule: Rule, path: str, grain: str, extra: dict | None = None) -> dict:
        f = {
            "finding_id": finding_id(self.p, rule.id, path), "path": path, "role": rule.role, "kind": rule.kind, "relevance": rule.relevance,
            "rule_id": rule.id, "basis": rule.basis, "confidence": rule.confidence, "evidence": rule.evidence, "grain": grain,
            "profile_id": self.p.profile_id, "profile_version": self.p.version,
        }
        if extra:
            f.update(extra)
        return f

    # ---- the run --------------------------------------------------------------------------------------------------------
    def candidate_copies(self, path_list: Path, kinds: tuple) -> list:
        """NAMES-ONLY report (not a rule): group the components of the given kinds whose sorted sets of relative file names are identical. The
        files counted are those under the component that the profile does not hide (a built site/ or a venv does not make two copies differ).
        A group is evidence for the later duplicate-tree test; nothing is hidden or merged because of it."""
        members = {d: set() for d, r in self.claims.items() if r.grain == "component" and r.kind in kinds}
        if not members:
            return []
        for path, _ in read_rows(path_list):
            dirs = path.split("/")[:-1]
            hits = [("/".join(dirs[:i + 1]), i + 1) for i in range(len(dirs)) if "/".join(dirs[:i + 1]) in members]
            if "" in members:
                hits.append(("", 0))
            if not hits:
                continue
            rule, _, _ = self.classify(path)
            if rule is not None and rule.relevance == "hidden":
                continue
            for d, depth in hits:
                members[d].add(path[len(d) + 1:] if d else path)
        groups: dict[str, list] = {}
        for d, names in members.items():
            if names:
                key = hashlib.sha256("\n".join(sorted(names)).encode("utf-8")).hexdigest()
                groups.setdefault(key, []).append(d or ".")
        return [{"names_sha256": k, "files": len(members["" if v[0] == "." else v[0]]), "members": sorted(v)}
                for k, v in sorted(groups.items(), key=lambda kv: (sorted(kv[1]), kv[0])) if len(v) > 1]

    def run(self, path_list: Path, out: Path, per_file: bool = False, copies_of: tuple = ()) -> dict:
        out.mkdir(parents=True, exist_ok=True)
        self.index_directories(path_list)

        comp_dirs = sorted(d for d, r in self.claims.items() if r.grain == "component")
        comp_set = set(comp_dirs)
        # only a component that a MANIFEST declares can have parts: a convention folder (docker/, docs/) groups things, it does not contain them
        # a deployment that a structural rule found (a compose directory) also has parts: the images and projects built inside it belong to it
        part_parents = {d for d in comp_dirs if self.claims[d].basis == "manifest" or (self.claims[d].origin == "structural" and self.claims[d].kind == "deployment")}
        top_components, all_components = [], []
        parts_of: dict[str, str | None] = {}
        for d in comp_dirs:
            parent = None
            segs = d.split("/") if d else []
            for i in range(len(segs) - 1, 0, -1):              # the nearest enclosing component, deepest first
                if "/".join(segs[:i]) in part_parents:
                    parent = "/".join(segs[:i])
                    break
            # a manifest at the repository root makes the root a component (kind root-project) but NOT the parent of the others:
            # parts exist only below a non-root component
            parts_of[d] = parent
            all_components.append(d or ".")
        for d in comp_dirs:                                      # a declared workspace or module member is a component of its own, not a part of its parent
            if d in self.member_of:
                parts_of[d] = None
            elif self.claims[d].kind in ("doc-section", "doc-translation") and self.extras.get(d, {}).get("site") is not None:
                parts_of[d] = self.extras[d]["site"] or "."      # a documentation section is a part of its site, whatever the site's depth
        for fpath in sorted(self.file_components):               # a section that is ONE PAGE: a component whose path is the page file, a part of its site
            all_components.append(fpath)
        promoted: dict[str, dict] = {}                           # part -> the structural rule that made it a top-level component
        for sr in self.p.structural:
            if sr["op"] != "sibling-manifests-top-level":
                continue
            groups: dict[tuple, list] = {}
            for d, parent in parts_of.items():
                if parent is not None and d not in promoted:
                    groups.setdefault((d.rpartition("/")[0], self.claims[d].kind), []).append(d)
            for (_, _), members in sorted(groups.items()):
                if len(members) >= sr["min"]:
                    for d in members:
                        promoted[d] = sr
                        parts_of[d] = None
        top_components = [d or "." for d in comp_dirs if parts_of[d] is None]

        by_role: dict[str, list] = {}
        by_rel: dict[str, list] = {}
        by_rule: dict[str, list] = {}
        counts: dict[tuple, list] = {}                         # (directory, rule id) -> [files, bytes] claimed
        rules_by_id = self.p.rules_by_id()
        total_files = total_bytes = 0

        def bump(table, key, size):
            cell = table.setdefault(key, [0, 0])
            cell[0] += 1
            cell[1] += size

        fj = open(out / "findings-files.jsonl", "w", encoding="utf-8", newline="\n") if per_file else None
        try:
            for path, size in read_rows(path_list):
                total_files += 1
                total_bytes += size
                rule, node, grain = self.classify(path)
                if rule is None:
                    bump(by_role, UNCLASSIFIED, size)
                    bump(by_rel, UNCLASSIFIED, size)
                    bump(by_rule, "(none)", size)
                    continue
                bump(by_role, rule.role, size)
                bump(by_rel, rule.relevance, size)
                bump(by_rule, rule.id, size)
                if grain == "dir":                              # a file-name rule: the finding is the directory that holds the file
                    cut = path.rfind("/")
                    directory = path[:cut] if cut >= 0 else "."
                else:
                    directory = node or "."
                cell = counts.setdefault((directory, rule.id), [0, 0])
                cell[0] += 1
                cell[1] += size
                if fj is not None:
                    f = self.finding(rule, path, grain)
                    f["files"], f["bytes"] = 1, size
                    fj.write(json.dumps(f, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n")
        finally:
            if fj is not None:
                fj.close()

        findings = []
        for (directory, rid), (nf, nb) in counts.items():
            r = rules_by_id[rid]
            grain = "subtree" if r.grain == "subtree" else "dir"
            f = self.finding(r, directory, grain)
            f["files"], f["bytes"] = nf, nb
            findings.append(f)
        done = {(f["path"], f["rule_id"]) for f in findings}
        for d, r in self.claims.items():                       # a claimed directory with no file counted against it (components)
            key = (d or ".", r.id)
            if key in done:
                f = next(x for x in findings if (x["path"], x["rule_id"]) == key)
                if parts_of.get(d):
                    f["part_of"] = parts_of[d]
                f.update(self.extras.get(d, {}))
                continue
            extra = {"part_of": parts_of[d]} if parts_of.get(d) else None
            if d in promoted:
                sr = promoted[d]
                extra = {"structure_rule_id": sr["id"], "structure_basis": sr["basis"], "structure_confidence": sr["confidence"],
                         "structure_evidence": sr["evidence"]}
            if d == "" and r.grain == "component":             # the repository root: flag it, keep what the manifest rule said
                extra = {"root": True, "kind": "root-project", "manifest_kind": r.kind}
            extra = {**(extra or {}), **self.extras.get(d, {})} or None
            f = self.finding(r, d or ".", r.grain, extra)
            findings.append(f)
        for fpath, (rule, site, info) in self.file_components.items():
            findings.append(self.finding(rule, fpath, "component", {**info, "part_of": site or "."}))
        findings.sort(key=lambda f: (f["path"], f["rule_id"]))
        with open(out / "findings.jsonl", "w", encoding="utf-8", newline="\n") as fh:
            for f in findings:
                fh.write(json.dumps(f, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n")

        if copies_of:
            groups = self.candidate_copies(path_list, tuple(copies_of))
            (out / "candidate-copies.json").write_text(json.dumps({"kinds": sorted(copies_of), "groups": groups}, indent=2, sort_keys=True) + "\n",
                                                       encoding="utf-8")
        if self.reading is not None:                                # names only: the paths opened, in order (evidence for the read log)
            (out / "manifest-reads.txt").write_text("".join(p + "\n" for p in self.reading.log), encoding="utf-8")
        top_components.sort()
        all_components.sort()
        (out / "components.txt").write_text("".join(c + "\n" for c in top_components), encoding="utf-8")
        (out / "components-all.txt").write_text("".join(c + "\n" for c in all_components), encoding="utf-8")

        def table(t):
            return {k: {"files": v[0], "bytes": v[1]} for k, v in sorted(t.items())}

        def share(n, d):
            return round(n / d, 6) if d else 0.0

        unc = by_role.get(UNCLASSIFIED, [0, 0])
        hid = by_rel.get("hidden", [0, 0])
        classes = {
            "profile": {"profile_id": self.p.profile_id, "version": self.p.version, "status": self.p.status,
                        "composed_of": [list(c) for c in self.p.composed_of]},
            "total_files": total_files, "total_bytes": total_bytes,
            "by_role": table(by_role), "by_relevance": table(by_rel), "by_rule": table(by_rule),
            "shares": {
                "classified_files": share(total_files - unc[0], total_files), "hidden_files": share(hid[0], total_files),
                "unclassified_files": share(unc[0], total_files),
                "classified_bytes": share(total_bytes - unc[1], total_bytes), "hidden_bytes": share(hid[1], total_bytes),
                "unclassified_bytes": share(unc[1], total_bytes),
            },
            "components": {"top_level": len(top_components), "parts": len(all_components) - len(top_components)},
            "findings": len(findings),
        }
        if self.p.manifest_reading is not None:
            mrd = self.p.manifest_reading
            classes["manifest_reading"] = {"enabled": self.reading is not None, "readers": list(mrd.readers), "max_file_bytes": mrd.max_file_bytes,
                                           "max_blobs": mrd.max_blobs, "max_total_bytes": mrd.max_total_bytes,
                                           "members": len(self.member_of), "aggregators": sorted(d or "." for d in self.aggregators)}
            if "mkdocs" in mrd.readers:
                classes["manifest_reading"]["docs_sections"] = dict(self.docs_stats)
            if self.reading is not None:
                classes["manifest_reading"].update(self.reading.stats.as_dict())
        if self.p.file_roles:                                      # the file-role layer: `other` is classified, and reported beside the target
            classes["shares"]["other_files"] = share(by_role.get("other", [0, 0])[0], total_files)
            classes["shares"]["other_bytes"] = share(by_role.get("other", [0, 0])[1], total_bytes)
        (out / "classes.json").write_text(json.dumps(classes, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
        (out / "report.md").write_text(render_report(classes), encoding="utf-8")
        return classes


def render_report(c: dict) -> str:
    lines = [f"# Layout recognition: {c['profile']['profile_id']} {c['profile']['version']} ({c['profile']['status']})", "",
             f"Files: {c['total_files']:,}. Bytes: {c['total_bytes']:,}.", "",
             "Shares of files: " + ", ".join(f"{k.split('_')[0]} {v:.1%}" for k, v in c["shares"].items() if k.endswith("_files")) + ".",
             f"Components: {c['components']['top_level']} top-level, {c['components']['parts']} parts.", "",
             "| role | files | bytes |", "|---|---:|---:|"]
    for role, v in sorted(c["by_role"].items(), key=lambda kv: (-kv[1]["files"], kv[0])):
        lines.append(f"| {role} | {v['files']:,} | {v['bytes']:,} |")
    lines += ["", "| relevance | files | bytes |", "|---|---:|---:|"]
    for rel, v in sorted(c["by_relevance"].items(), key=lambda kv: (-kv[1]["files"], kv[0])):
        lines.append(f"| {rel} | {v['files']:,} | {v['bytes']:,} |")
    mr = c.get("manifest_reading")
    if mr is not None:
        if not mr["enabled"]:
            lines += ["", "Manifest reading: not enabled for this run (no blob source); names and sizes only."]
        else:
            lines += ["", f"Manifest reading: {mr['blobs_read']:,} manifest(s) read ({mr['bytes_read']:,} bytes) of {mr['candidates']:,} candidate(s); "
                      f"{mr['members']:,} declared member(s), {len(mr['aggregators'])} aggregator(s); skipped: {mr['skipped_size']} over the size cap, "
                      f"{mr['skipped_hidden']} in hidden subtrees; {mr['parse_errors']} parse error(s)."]
            if mr["cap_reached"]:
                lines += [f"CAP REACHED ({mr['cap_reached']}): {mr['cap_skipped']:,} manifest(s) were not read; their findings stay names-only."]
    lines += ["", "| rule | files | bytes |", "|---|---:|---:|"]
    for rid, v in sorted(c["by_rule"].items(), key=lambda kv: (-kv[1]["files"], kv[0])):
        lines.append(f"| {rid} | {v['files']:,} | {v['bytes']:,} |")
    lines += ["", "Unclassified is a result, not a failure: no rule of this profile claims those files.", ""]
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("pathlist", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--profile", default="generic-relevance", help="a profile id, or several joined by commas: the first-listed wins a conflict (code-repo-conventions,docs-site)")
    ap.add_argument("--profiles-dir", type=Path, default=DEFAULT_PROFILES)
    ap.add_argument("--copies-of", action="append", default=[], metavar="KIND",
                    help="also write candidate-copies.json: components of this kind with identical sets of file names (names only; repeatable)")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--blobs-git", nargs=2, metavar=("REPO", "REV"), help="let the profile's manifest reading read blobs of REV from the git repository REPO")
    src.add_argument("--blobs-dir", type=Path, metavar="DIR", help="let the profile's manifest reading read files below DIR (a non-git tree; symlinks not followed)")
    ap.add_argument("--per-file", action="store_true", help="also write findings-files.jsonl, one finding per file (debugging; large)")
    a = ap.parse_args(argv)
    prof = compose_profiles(a.profile, a.profiles_dir)
    source = mf.GitBlobSource(*a.blobs_git) if a.blobs_git else (mf.FileSource(str(a.blobs_dir)) if a.blobs_dir else None)
    try:
        c = Recognizer(prof, blob_source=source).run(a.pathlist, a.out, per_file=a.per_file, copies_of=tuple(a.copies_of))
    finally:
        if source is not None:
            source.close()
    print(f"{prof.profile_id} {prof.version}: {c['total_files']:,} files; unclassified {c['shares']['unclassified_files']:.1%}, "
          f"hidden {c['shares']['hidden_files']:.1%}; components {c['components']['top_level']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
