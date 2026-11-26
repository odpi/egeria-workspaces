"""Apply a layout profile to a list of repository paths. Names and sizes ONLY: no file is opened, no network, no Egeria.

    python -m recognizer.recognize PATHLIST --out OUTDIR [--profile generic-relevance] [--profiles-dir DIR]

PATHLIST: one repo-relative file path per line, optionally `path<TAB>size-in-bytes` (from `git ls-files`, a `git archive` listing, or
recognizer/listpaths.py; never from a dirty working tree). Paths use `/`, are relative, and appear once.

Outputs in OUTDIR (byte-identical for the same input and profile; nothing in them depends on time, run id or the tree sha):
  components.txt  one directory per line, the input format of the Phase 0 scorer (top-level components; parts of a component are findings)
  findings.jsonl  one finding per recognized node (a subtree root, a matched file, or a claimed directory)
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
        self.claims: dict[str, Rule] = {}             # directory -> the first dir rule that claims it
        self.subtree_claims: dict[str, set] = {}      # rule id -> directories claimed with grain subtree

    # ---- directory rules (has_file / parent_has_file) -------------------------------------------------------------------
    def index_directories(self, path_list: Path) -> None:
        if not self.dir_rules:
            return
        holders: dict[str, set] = {}
        all_dirs: set = set()
        need_all = any(r.parent_has_files for r in self.dir_rules)
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
    def run(self, path_list: Path, out: Path) -> dict:
        out.mkdir(parents=True, exist_ok=True)
        self.index_directories(path_list)

        components = sorted(d for d, r in self.claims.items() if r.grain == "component")
        comp_set = set(components)
        dir_findings = []
        top_components = []
        for d in sorted(self.claims):
            r = self.claims[d]
            extra = None
            if r.grain == "component":
                parent = None
                segs = d.split("/") if d else []
                for i in range(len(segs) - 1, 0, -1):          # the nearest enclosing component, deepest first
                    if "/".join(segs[:i]) in comp_set:
                        parent = "/".join(segs[:i])
                        break
                if parent is None and d and "" in comp_set:    # the repository root is itself a component
                    parent = "."
                if parent is None:
                    top_components.append(d or ".")
                extra = {"part_of": parent} if parent else None
            dir_findings.append(self.finding(r, d or ".", r.grain, extra))
        dir_findings.sort(key=lambda f: (f["path"], f["rule_id"]))

        by_role: dict[str, list] = {}
        by_rel: dict[str, list] = {}
        by_rule: dict[str, list] = {}
        total_files = total_bytes = 0
        emitted: set = set()
        di = 0

        def bump(table, key, size):
            cell = table.setdefault(key, [0, 0])
            cell[0] += 1
            cell[1] += size

        with open(out / "findings.jsonl", "w", encoding="utf-8", newline="\n") as fj:
            def put(f):
                fj.write(json.dumps(f, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n")

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
                if rule.is_dir_rule:                      # its directory finding is already in dir_findings
                    continue
                key = (rule.id, node)
                if grain == "subtree" and key in emitted:
                    continue
                if grain == "subtree":
                    emitted.add(key)
                while di < len(dir_findings) and dir_findings[di]["path"] < node:
                    put(dir_findings[di])
                    di += 1
                put(self.finding(rule, node, grain))
            while di < len(dir_findings):
                put(dir_findings[di])
                di += 1

        top_components.sort()
        (out / "components.txt").write_text("".join(c + "\n" for c in top_components), encoding="utf-8")

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
            "components": {"top_level": len(top_components), "parts": len(components) - len(top_components)},
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
    a = ap.parse_args(argv)
    prof = load_profile(a.profile, a.profiles_dir)
    c = Recognizer(prof).run(a.pathlist, a.out)
    print(f"{prof.profile_id} {prof.version}: {c['total_files']:,} files; unclassified {c['shares']['unclassified_files']:.1%}, "
          f"hidden {c['shares']['hidden_files']:.1%}; components {c['components']['top_level']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
