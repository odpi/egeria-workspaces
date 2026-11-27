"""Phase 1j J4 (D-J2): one key per repository, with per-setting deltas. Given a key and the settings a run used, return the EFFECTIVE key the run is scored
against, and say which settings the key cannot score.

Key format (the parts this library reads; everything else is carried over unchanged):

    assumes: {setting: value, ...}        # the settings the labels rely on; a setting not named here is assumed at its shipped default
    components: [path | {path: ..., ...}, ...]
    excluded:   [path | {path: ..., ...}, ...]
    when:                                 # deltas, each applied when ALL of its settings hold in the run
      - when: {scripts-are-tooling: false}
        components_add: [...]             # entries as in components (a path string or a mapping with `path`)
        components_remove: [...]          # paths
        excluded_add: [...]
        excluded_remove: [...]

A run whose settings equal the assumed ones gets the key unchanged. For every setting where the run differs from the assumption, the when-blocks that hold
and name that setting are applied (in key order); a differing setting that no applying block names is UNSCOREABLE: the result lists it with the paths it
touches in that run (the paths of the run's findings whose rule is governed by the setting), so a scorer reports them instead of scoring them silently.

Names only: this reads the key and the run's findings it is given; it opens nothing else. The Architect adopts it into the scorer separately.
"""
from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

DELTA_KEYS = ("components_add", "components_remove", "excluded_add", "excluded_remove")


class KeyFormatError(ValueError):
    """The key's assumes or when blocks are not valid."""


@dataclass
class EffectiveKey:
    key: dict                                          # the effective key: components and excluded after the deltas; no `assumes` or `when`
    run_settings: dict                                 # the settings of the run
    assumed: dict                                      # the settings the key assumes (defaults filled in)
    differing: list = field(default_factory=list)      # settings where the run differs from the assumption, in name order
    applied: list = field(default_factory=list)        # indexes of the when-blocks applied, in key order
    unscoreable: dict = field(default_factory=dict)    # setting -> sorted paths of the run's findings governed by it

    @property
    def scoreable(self) -> bool:
        return not self.unscoreable


def _path_of(entry: Any) -> str:
    if isinstance(entry, str) and entry:
        return entry
    if isinstance(entry, dict) and isinstance(entry.get("path"), str) and entry["path"]:
        return entry["path"]
    raise KeyFormatError(f"a key entry must be a path or a mapping with a path, got {entry!r}")


def governed_rules(profile) -> dict:
    """setting -> the ids of the rules it governs in `profile` (a loaded layout profile): rules with a `when:` on it, and rules whose match refers to it
    (`$setting`, or a conditional list element)."""
    names = set(getattr(profile, "settings_decl", {}) or {})
    out: dict = {n: set() for n in names}
    rules = tuple(getattr(profile, "all_rules", ()) or profile.rules) + tuple(getattr(profile, "all_file_roles", ()) or profile.file_roles)
    for r in rules:
        for n in (set(r.when) | set(r.list_refs)) & names:
            out[n].add(r.id)
    return out


def shipped_defaults(profile) -> dict:
    return {n: d["default"] for n, d in (getattr(profile, "settings_decl", {}) or {}).items()}


def read_findings(path: str | Path) -> list:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def effective_key(key: dict, run_settings: dict, *, defaults: dict, governed: dict | None = None, findings: Iterable[dict] | None = None) -> EffectiveKey:
    """Return the effective key for a run with `run_settings` (setting -> value). `defaults` are the shipped defaults (setting -> value), also the
    names a key may use. `governed` (setting -> rule ids) and `findings` (the run's findings: dicts with `path` and `rule_id`) give the paths of an
    UNSCOREABLE setting; without them its path list is empty."""
    if not isinstance(key, dict):
        raise KeyFormatError("a key is a mapping")
    known = set(defaults)
    assumes = key.get("assumes") or {}
    if not isinstance(assumes, dict):
        raise KeyFormatError("assumes must be a mapping of setting -> value")
    for n, v in assumes.items():
        if n not in known:
            raise KeyFormatError(f"assumes names {n!r}, which is not a setting")
        if type(v) is not type(defaults[n]):
            raise KeyFormatError(f"assumes {n}: {v!r} does not match the setting's type")
    assumed = {n: assumes.get(n, defaults[n]) for n in sorted(known)}
    for n in run_settings:
        if n not in known:
            raise KeyFormatError(f"the run names a setting {n!r} that the defaults do not know")
    run = {n: run_settings.get(n, defaults[n]) for n in sorted(known)}

    blocks = key.get("when") or []
    if not isinstance(blocks, list):
        raise KeyFormatError("when must be a list of blocks")
    for i, b in enumerate(blocks):
        if not isinstance(b, dict) or "when" not in b or set(b) - {"when", *DELTA_KEYS}:
            raise KeyFormatError(f"when[{i}]: a block has `when` and only {list(DELTA_KEYS)}")
        cond = b["when"]
        if not isinstance(cond, dict) or not cond:
            raise KeyFormatError(f"when[{i}]: when needs a mapping of setting -> value")
        for n, v in cond.items():
            if n not in known:
                raise KeyFormatError(f"when[{i}]: {n!r} is not a setting")
            if type(v) is not type(defaults[n]):
                raise KeyFormatError(f"when[{i}]: {n}: {v!r} does not match the setting's type")
        if all(assumed[n] == v for n, v in cond.items()):
            raise KeyFormatError(f"when[{i}]: its settings are the assumed ones, so it would change the key at the assumed settings")
        for k in DELTA_KEYS:
            if k in b and (not isinstance(b[k], list) or not b[k]):
                raise KeyFormatError(f"when[{i}].{k}: a non-empty list")

    differing = [n for n in sorted(known) if run[n] != assumed[n]]
    out = {k: copy.deepcopy(v) for k, v in key.items() if k not in ("assumes", "when")}
    comps = list(out.get("components") or [])
    excl = list(out.get("excluded") or [])
    applied, covered = [], set()
    for i, b in enumerate(blocks):
        cond = b["when"]
        if not all(run[n] == v for n, v in cond.items()):
            continue
        applied.append(i)
        covered |= set(cond)
        for lst, add, rem in ((comps, "components_add", "components_remove"), (excl, "excluded_add", "excluded_remove")):
            for p in b.get(rem, []):
                p = _path_of(p)
                at = [j for j, e in enumerate(lst) if _path_of(e) == p]
                if not at:
                    raise KeyFormatError(f"when[{i}].{rem}: {p!r} is not in the key at this point")
                del lst[at[0]]
            for e in b.get(add, []):
                p = _path_of(e)
                if any(_path_of(x) == p for x in lst):
                    raise KeyFormatError(f"when[{i}].{add}: {p!r} is already in the key at this point")
                lst.append(copy.deepcopy(e))
    if "components" in key or comps:
        out["components"] = comps
    if "excluded" in key or excl:
        out["excluded"] = excl

    unscoreable = {}
    found = list(findings or [])
    for n in differing:
        if n in covered:
            continue
        rules = (governed or {}).get(n, set())
        unscoreable[n] = sorted({f["path"] for f in found if f.get("rule_id") in rules})
    return EffectiveKey(key=out, run_settings=run, assumed=assumed, differing=differing, applied=applied, unscoreable=unscoreable)
