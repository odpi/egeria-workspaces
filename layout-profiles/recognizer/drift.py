"""Drift between two surveys of the same dataset (Phase 2, notebook 05, B3), by stable finding_id. Reads the outputs of `recognizer.recognize` only.

    python -m recognizer.drift OLD_OUTDIR NEW_OUTDIR [--out DRIFT.json]

First checks the two surveys' configurations (`recognizer.config_drift.config_change`, Phase 1j J5): when they differ, the result is a
CONFIGURATION CHANGE (or UNRECORDED), reported as such, and the findings are not compared. Otherwise it compares the CONFORMANCE findings of the two surveys by finding_id (`sha256(profile_id@major | rule_id | path)`): `new` are in NEW only, `resolved`
in OLD only, `unchanged` in both (an unchanged id whose status or reason changed, for example a field that went from invalid to missing, is
marked `changed` with the old status). The two surveys must use the same profile id and major version, or the ids are not comparable.
Writes NEW_OUTDIR/drift.json (or --out) and puts a "Drift" section into NEW_OUTDIR/report.md, replacing an earlier one.

04a F6: when either survey has PART findings (component findings with part_of), drift.json also has `parts: {new, resolved}`, the parts compared
by finding_id (which is path-based: a renamed part is one resolved and one new). Without part findings the key is absent.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from .conformance import FINDING_KEYS, conformance_findings, put_section
    from .config_drift import config_change, headline as config_headline
except ImportError:                                   # run as a script
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from conformance import FINDING_KEYS, conformance_findings, put_section  # type: ignore
    from config_drift import config_change, headline as config_headline  # type: ignore

BEGIN = "<!-- drift:begin -->"
END = "<!-- drift:end -->"


class DriftError(ValueError):
    pass


def _profile(outdir: Path) -> dict:
    return json.loads((Path(outdir) / "classes.json").read_text(encoding="utf-8"))["profile"]


def part_findings(outdir: Path) -> list:
    """The PART findings of a survey: component findings that are part_of a component."""
    out = []
    with open(Path(outdir) / "findings.jsonl", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                f = json.loads(line)
                if f.get("grain") == "component" and f.get("part_of"):
                    out.append(f)
    return out


def diff(old: Path, new: Path) -> dict:
    po, pn = _profile(old), _profile(new)
    change = config_change(old, new)                    # J5: first; a configuration change is not finding drift
    if change is not None:
        return {"old_profile": po, "new_profile": pn, "configuration_change": change}
    if po["profile_id"] != pn["profile_id"] or po["version"].split(".")[0] != pn["version"].split(".")[0]:
        raise DriftError(f"the surveys use {po['profile_id']} {po['version']} and {pn['profile_id']} {pn['version']}: finding ids are comparable only "
                         "for the same profile id and major version")
    a = {f["finding_id"]: f for f in conformance_findings(old)}
    b = {f["finding_id"]: f for f in conformance_findings(new)}

    def slim(f):
        return {k: f[k] for k in FINDING_KEYS if k in f}

    def order(ids, src):
        return sorted(ids, key=lambda i: (src[i]["path"], src[i]["rule_id"], i))

    unchanged = []
    for i in order(set(a) & set(b), b):
        x = slim(b[i])
        if (a[i]["status"], a[i].get("reason")) != (b[i]["status"], b[i].get("reason")):
            x.update({"changed": True, "old_status": a[i]["status"]})
            if a[i].get("reason"):
                x["old_reason"] = a[i]["reason"]
        unchanged.append(x)
    new_ = [slim(b[i]) for i in order(set(b) - set(a), b)]
    resolved = [slim(a[i]) for i in order(set(a) - set(b), a)]
    d = {"old_profile": po, "new_profile": pn,
         "counts": {"new": len(new_), "resolved": len(resolved), "unchanged": len(unchanged), "changed": sum(1 for x in unchanged if x.get("changed"))},
         "new": new_, "resolved": resolved, "unchanged": unchanged}
    pa = {f["finding_id"]: f for f in part_findings(old)}
    pb = {f["finding_id"]: f for f in part_findings(new)}
    if pa or pb:                                          # F6: only when a survey has parts, so drift.json is unchanged for every other profile
        part = lambda f: {"finding_id": f["finding_id"], "path": f["path"], "kind": f["kind"], "part_of": f["part_of"]}
        d["parts"] = {"new": [part(pb[i]) for i in sorted(set(pb) - set(pa), key=lambda i: (pb[i]["path"], i))],
                      "resolved": [part(pa[i]) for i in sorted(set(pa) - set(pb), key=lambda i: (pa[i]["path"], i))],
                      "unchanged": len(set(pa) & set(pb))}
    return d


def headline(d: dict) -> str:
    if "configuration_change" in d:
        return config_headline(d["configuration_change"])
    c = d["counts"]
    return f"{c['new']} new since last survey; {c['resolved']} resolved; {c['unchanged']} unchanged"


def section(d: dict) -> str:
    if "configuration_change" in d:
        return "\n".join([BEGIN, "## Drift since the previous survey", "", f"**{headline(d)}**; findings are not compared (see drift.json).", "", END, ""])
    lines = [BEGIN, "## Drift since the previous survey", "", f"**{headline(d)}** (by finding id).", ""]
    if "parts" in d:
        pt = d["parts"]
        lines += [f"Parts: {len(pt['new'])} new, {len(pt['resolved'])} resolved, {pt['unchanged']} unchanged (by finding id, which is path-based: a "
                  "renamed part is one resolved and one new).", ""]
        for name in ("new", "resolved"):
            if pt[name]:
                lines += [f"Parts {name}:", "", "| path | kind |", "|---|---|"] + [f"| {f['path']} | {f['kind']} |" for f in pt[name][:200]] + [""]
    for name in ("new", "resolved"):
        if d[name]:
            lines += [f"{name.capitalize()}:", "", "| path | kind | status | rule |", "|---|---|---|---|"]
            lines += [f"| {f['path']} | {f['kind']} | {f['status']} | {f['rule_id']} |" for f in d[name][:200]]
            if len(d[name]) > 200:
                lines.append(f"| ... {len(d[name]) - 200:,} more in drift.json | | | |")
            lines.append("")
    lines += [END, ""]
    return "\n".join(lines)


def write(old: Path, new: Path, out: Path | None = None) -> dict:
    d = diff(old, new)
    target = Path(out) if out else Path(new) / "drift.json"
    target.write_text(json.dumps(d, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    put_section(Path(new) / "report.md", section(d), BEGIN, END)
    return d


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("old", type=Path)
    ap.add_argument("new", type=Path)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    try:
        d = write(a.old, a.new, a.out)
    except DriftError as exc:
        print(f"drift: {exc}", file=sys.stderr)
        return 2
    print(headline(d))
    return 0


if __name__ == "__main__":
    sys.exit(main())
