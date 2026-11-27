"""Phase 1j J5: compare two surveys of the same tree. When their configurations differ (config_sha256), the difference is a CONFIGURATION CHANGE, not
finding drift: the result names the settings, rules and lists that differ and does not compare findings. Otherwise it compares the findings by finding_id.
Reads the outputs of `recognizer.recognize` only.

    python -m recognizer.config_drift OLD_OUTDIR NEW_OUTDIR

`config_change(old, new)` is the check to run first in any drift comparison (the Phase 2 drift report included, when the branches meet).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def configuration(outdir) -> dict | None:
    return json.loads((Path(outdir) / "classes.json").read_text(encoding="utf-8")).get("configuration")


def config_change(old, new) -> dict | None:
    """None when both surveys record the same config_sha256; otherwise what differs. A survey without a recorded configuration (before J5) is UNRECORDED."""
    a, b = configuration(old), configuration(new)
    if a is None or b is None:
        return {"status": "CONFIGURATION UNRECORDED", "old_recorded": a is not None, "new_recorded": b is not None}
    if a["config_sha256"] == b["config_sha256"]:
        return None
    names = sorted(set(a["settings"]) | set(b["settings"]))
    settings = {n: {"old": a["settings"].get(n, {}).get("value"), "new": b["settings"].get(n, {}).get("value")} for n in names
                if a["settings"].get(n, {}).get("value") != b["settings"].get(n, {}).get("value")}
    out = {"status": "CONFIGURATION CHANGED", "old_config_sha256": a["config_sha256"], "new_config_sha256": b["config_sha256"], "settings": settings}
    for k in ("disabled_rules", "replaced_rules", "overridden_lists", "overlays"):
        if a[k] != b[k]:
            out[k] = {"old": a[k], "new": b[k]}
    if [(c["profile_id"], c["version"]) for c in a["chain"]] != [(c["profile_id"], c["version"]) for c in b["chain"]]:
        out["chain"] = {"old": a["chain"], "new": b["chain"]}
    return out


def _findings(outdir) -> dict:
    out = {}
    with open(Path(outdir) / "findings.jsonl", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                f = json.loads(line)
                out[f["finding_id"]] = f
    return out


def compare(old, new) -> dict:
    change = config_change(old, new)
    if change is not None:
        return change                                   # not finding drift: the surveys ran different configurations
    a, b = _findings(old), _findings(new)
    key = lambda f: (f["path"], f["rule_id"])            # noqa: E731
    return {"status": "SAME CONFIGURATION", "counts": {"new": len(set(b) - set(a)), "resolved": len(set(a) - set(b)), "unchanged": len(set(a) & set(b))},
            "new": sorted((key(b[i]) for i in set(b) - set(a))), "resolved": sorted((key(a[i]) for i in set(a) - set(b)))}


def headline(d: dict) -> str:
    if d["status"] == "SAME CONFIGURATION":
        c = d["counts"]
        return f"SAME CONFIGURATION: {c['new']} new, {c['resolved']} resolved, {c['unchanged']} unchanged (by finding id)"
    if d["status"] == "CONFIGURATION CHANGED":
        parts = [f"{n} {json.dumps(v['old'])} -> {json.dumps(v['new'])}" for n, v in d["settings"].items()]
        parts += [k.replace("_", " ") for k in ("disabled_rules", "replaced_rules", "overridden_lists", "overlays", "chain") if k in d]
        return "CONFIGURATION CHANGED (not finding drift): " + ("; ".join(parts) if parts else "rules or lists differ")
    return "CONFIGURATION UNRECORDED: at least one survey predates the configuration record; findings are not compared"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("old", type=Path)
    ap.add_argument("new", type=Path)
    a = ap.parse_args(argv)
    d = compare(a.old, a.new)
    print(headline(d))
    print(json.dumps(d, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
