"""Conformance report of one survey (Phase 2, notebook 05, B3). Reads the outputs of `recognizer.recognize` only; opens no file of the tree.

    python -m recognizer.conformance OUTDIR

Writes OUTDIR/conformance.json and puts a "Conformance" section into OUTDIR/report.md (replacing the section of an earlier run, so the outputs
are byte-identical however often it is run). The score is conformant checked items / checked items: every entry judged against a closed set,
every required path expected, and every content field checked is one item; a finding is one non-conformant item. Not-checked files are counted
beside the score, never in it.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BEGIN = "<!-- conformance:begin -->"
END = "<!-- conformance:end -->"
FINDING_KEYS = ("finding_id", "path", "kind", "status", "rule_id", "reason")


class ConformanceError(ValueError):
    pass


def conformance_findings(outdir: Path) -> list:
    """The conformance findings of a survey (grain conformance), in the survey's order (path, then rule id)."""
    out = []
    with open(Path(outdir) / "findings.jsonl", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                f = json.loads(line)
                if f.get("grain") == "conformance":
                    out.append(f)
    return out


def summarize(outdir: Path) -> dict:
    outdir = Path(outdir)
    classes = json.loads((outdir / "classes.json").read_text(encoding="utf-8"))
    c = classes.get("conformance")
    if c is None:
        raise ConformanceError(f"{outdir}: this survey's profile declares no conformance (no closed set, required path or content check)")
    found = conformance_findings(outdir)
    if len(found) != c["findings_total"]:
        raise ConformanceError(f"{outdir}: findings.jsonl has {len(found)} conformance findings, classes.json says {c['findings_total']}")
    by_kind = {k: sum(v.values()) for k, v in c["findings"].items()}
    return {
        "profile": classes["profile"],
        "score": c["score"],
        "checked": c["checked"],
        "conformant": c["conformant"],
        "findings_total": c["findings_total"],
        "findings_by_kind": dict(sorted(by_kind.items())),
        "findings_by_kind_status": c["findings"],
        "not_checked_files": c["not_checked"]["files"],
        "not_checked_roots": len(c["not_checked"]["roots"]),
        "content_reading": c.get("content_reading"),
        "by_category": c.get("by_category"),
        "total_files": classes["total_files"],
        "findings": [{k: f[k] for k in FINDING_KEYS if k in f} for f in found],
    }


def headline(s: dict) -> str:
    """'97% conformant; 12 findings' (the percentage floors, so a tree with any finding never shows 100%)."""
    pct = int(s["score"] * 100) if s["findings_total"] else 100
    n = s["findings_total"]
    return f"{pct}% conformant; {n} finding{'' if n == 1 else 's'}"


def section(s: dict) -> str:
    lines = [BEGIN, "## Conformance", "", f"**{headline(s)}** ({s['conformant']:,} of {s['checked']['total']:,} checked items; profile "
             f"{s['profile']['profile_id']} {s['profile']['version']}).", "",
             f"Checked: {s['checked']['entries']:,} entries against closed sets, {s['checked']['required']:,} required paths, "
             f"{s['checked'].get('fields', 0):,} content fields. Not checked: {s['not_checked_files']:,} of {s['total_files']:,} files "
             f"(below {s['not_checked_roots']:,} roots: outside the profile's subset, or below a finding).", ""]
    if s.get("by_category"):
        lines += ["By category: " + "; ".join(f"{cat.replace('-', ' ')} {int(v['score'] * 100) if v['findings'] else 100}% "
                                          f"({v['checked'] - v['findings']:,} of {v['checked']:,})" for cat, v in sorted(s["by_category"].items()))
                  + ". Study consistency (every subject has every session and folder seen) is this profile's expectation, not the standard's.", ""]
    cr = s.get("content_reading")
    if cr is not None:
        lines += [("Content read: " + ", ".join(cr["files_read"]) + ".") if cr["enabled"] and cr["files_read"]
                  else "Content read: none (" + ("no blob source" if not cr["enabled"] else "no content file at the root") + ").", ""]
    lines += ["| kind | status | findings |", "|---|---|---:|"]
    for kind, st in sorted(s["findings_by_kind_status"].items()):
        for status, n in sorted(st.items()):
            lines.append(f"| {kind} | {status} | {n:,} |")
    if not s["findings_by_kind_status"]:
        lines.append("| (none) | | 0 |")
    lines += ["", END, ""]
    return "\n".join(lines)


def put_section(report: Path, text: str, begin: str, end: str) -> None:
    """Replace the marked section of report.md (or append it): running twice gives the same file."""
    old = report.read_text(encoding="utf-8") if report.exists() else ""
    if begin in old and end in old:
        head, rest = old.split(begin, 1)
        tail = rest.split(end, 1)[1]
        tail = tail[1:] if tail.startswith("\n") else tail          # the newline after END belongs to the section
        new = head + text + tail
    else:
        new = old + ("" if old.endswith("\n\n") or not old else "\n") + text
    report.write_text(new, encoding="utf-8")


def write(outdir: Path) -> dict:
    outdir = Path(outdir)
    s = summarize(outdir)
    (outdir / "conformance.json").write_text(json.dumps(s, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    put_section(outdir / "report.md", section(s), BEGIN, END)
    return s


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("outdir", type=Path)
    a = ap.parse_args(argv)
    try:
        s = write(a.outdir)
    except ConformanceError as exc:
        print(f"conformance: {exc}", file=sys.stderr)
        return 2
    print(headline(s))
    return 0


if __name__ == "__main__":
    sys.exit(main())
