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
import sys
from pathlib import Path

try:
    from .layout_profile import Profile, Rule, load_profile
except ImportError:                                   # run as a script
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from layout_profile import Profile, Rule, load_profile  # type: ignore

UNCLASSIFIED = "unclassified"
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
    def __init__(self, profile: Profile):
        self.p = profile
        self.file_rules = [r for r in profile.rules if not r.is_dir_rule]
        self.dir_rules = [r for r in profile.rules if r.is_dir_rule]
        self.needed_names = set()
        for r in self.dir_rules:
            self.needed_names |= r.has_files | r.parent_has_files
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
    def index_directories(self, path_list: Path) -> None:
        if not self.dir_rules:
            return
        holders: dict[str, set] = {}
        all_dirs: set = set()
        need_all = any(not r.has_files for r in self.dir_rules)      # a rule that does not start from a file must see every directory
        for path, _ in read_rows(path_list):
            cut = path.rfind("/")
            d, name = (path[:cut], path[cut + 1:]) if cut >= 0 else ("", path)
            if name in self.needed_names:
                holders.setdefault(d, set()).add(name)
            if need_all:
                while d and d not in all_dirs:
                    all_dirs.add(d)
                    d = d[:d.rfind("/")] if "/" in d else ""
        candidates = set(holders) | all_dirs if need_all else set(holders)
        for d in sorted(candidates):
            if self.inside_hidden_subtree(d):                # vendored (or any hidden subtree) wins over a manifest inside it
                continue
            parent = d[:d.rfind("/")] if "/" in d else ""
            own = holders.get(d, set())
            par = holders.get(parent, set()) if d else set()
            segs, name = (d.split("/") if d else []), (d.rsplit("/", 1)[-1] if d else "")
            for r in self.dir_rules:
                if r.has_files and not (r.has_files & own):
                    continue
                if r.parent_has_files and not (r.parent_has_files & par):
                    continue
                if r.segments and not any(s in r.segments for s in segs):
                    continue
                if r.globs and (not d or not any(g.match(d) for g in r.globs)):
                    continue
                if r.names and name not in r.names:
                    continue
                if r.name_res and not any(rx.search(name) for rx in r.name_res):
                    continue
                self.claims[d] = r
                if r.grain == "subtree":
                    self.subtree_claims.setdefault(r.id, set()).add(d)
                break

    # ---- file rules -----------------------------------------------------------------------------------------------------
    def classify(self, path: str):
        """Return (rule, node_path, node_grain) for the first rule that claims this file, or (None, None, None)."""
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
            idx = -1
            if r.segments:
                if not (r.segments & dirset):
                    continue
                idx = next(i for i, s in enumerate(dirs) if s in r.segments)
            if r.names and name not in r.names:
                continue
            if r.extensions and not any(name.endswith(e) for e in r.extensions):
                continue
            if r.name_res and not any(rx.search(name) for rx in r.name_res):
                continue
            if r.globs and not any(g.match(path) for g in r.globs):
                continue
            if r.grain == "subtree":
                if idx < 0:
                    idx = next((i for i in range(len(dirs)) if any(g.match("/".join(dirs[:i + 1])) for g in r.root_globs)), -1)
                if idx < 0:
                    continue
                return r, "/".join(dirs[:idx + 1]), "subtree"
            return r, path, "dir"
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
        part_parents = {d for d in comp_dirs if self.claims[d].basis == "manifest"}
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
                continue
            extra = {"part_of": parts_of[d]} if parts_of.get(d) else None
            if d in promoted:
                sr = promoted[d]
                extra = {"structure_rule_id": sr["id"], "structure_basis": sr["basis"], "structure_confidence": sr["confidence"],
                         "structure_evidence": sr["evidence"]}
            if d == "" and r.grain == "component":             # the repository root: flag it, keep what the manifest rule said
                extra = {"root": True, "kind": "root-project", "manifest_kind": r.kind}
            f = self.finding(r, d or ".", r.grain, extra)
            findings.append(f)
        findings.sort(key=lambda f: (f["path"], f["rule_id"]))
        with open(out / "findings.jsonl", "w", encoding="utf-8", newline="\n") as fh:
            for f in findings:
                fh.write(json.dumps(f, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n")

        if copies_of:
            groups = self.candidate_copies(path_list, tuple(copies_of))
            (out / "candidate-copies.json").write_text(json.dumps({"kinds": sorted(copies_of), "groups": groups}, indent=2, sort_keys=True) + "\n",
                                                       encoding="utf-8")
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
    lines += ["", "| rule | files | bytes |", "|---|---:|---:|"]
    for rid, v in sorted(c["by_rule"].items(), key=lambda kv: (-kv[1]["files"], kv[0])):
        lines.append(f"| {rid} | {v['files']:,} | {v['bytes']:,} |")
    lines += ["", "Unclassified is a result, not a failure: no rule of this profile claims those files.", ""]
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("pathlist", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--profile", default="generic-relevance")
    ap.add_argument("--profiles-dir", type=Path, default=DEFAULT_PROFILES)
    ap.add_argument("--copies-of", action="append", default=[], metavar="KIND",
                    help="also write candidate-copies.json: components of this kind with identical sets of file names (names only; repeatable)")
    ap.add_argument("--per-file", action="store_true", help="also write findings-files.jsonl, one finding per file (debugging; large)")
    a = ap.parse_args(argv)
    prof = load_profile(a.profile, a.profiles_dir)
    c = Recognizer(prof).run(a.pathlist, a.out, per_file=a.per_file, copies_of=tuple(a.copies_of))
    print(f"{prof.profile_id} {prof.version}: {c['total_files']:,} files; unclassified {c['shares']['unclassified_files']:.1%}, "
          f"hidden {c['shares']['hidden_files']:.1%}; components {c['components']['top_level']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
