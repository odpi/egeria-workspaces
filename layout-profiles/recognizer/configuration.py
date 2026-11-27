"""Phase 1j J5: the provenance of a survey's configuration. What profile chain ran (ids, versions, shipped or overlay), every setting's value and whether it is
the default, the rules disabled and replaced, the lists overridden, and `config_sha256`, the hash of the canonical effective configuration (the chain, the
settings, the lists, every effective rule as compiled, the structural rules, the grammars and what is read). Documentation text (evidence, tuned_on, the
settings' doc) is not part of the hash. Names only: nothing here reads a repository.
"""
from __future__ import annotations

import hashlib
import json


def _rule(r) -> dict:
    return {"id": r.id, "origin": r.origin, "role": r.role, "relevance": r.relevance, "kind": r.kind, "grain": r.grain, "basis": r.basis,
            "confidence": r.confidence, "match": r.match, "file_scope": r.file_scope, "when": r.when}


def _reading(m) -> dict | None:
    if m is None:
        return None
    ids = {k: (getattr(m, k).id if getattr(m, k) is not None else None)
           for k in ("member_rule", "aggregator_rule", "section_rule", "fallback_section_rule", "translation_rule", "included_build_rule")}
    refs = {k: getattr(m, k) for k in ("docs_content_rule", "site_output_rule", "fallback_site_rule", "submodule_rule")}
    return {"readers": sorted(m.readers), "max_file_bytes": m.max_file_bytes, "max_blobs": m.max_blobs, "max_total_bytes": m.max_total_bytes,
            "skip_fields": sorted(m.skip_fields), **ids, **refs}


def chain(profile) -> list:
    shipped = dict(getattr(profile, "chain_shipped", ()) or ())
    return [{"profile_id": pid, "version": ver, "shipped": shipped.get(pid)} for pid, ver in profile.composed_of]


def canonical(profile) -> dict:
    """The effective configuration, as plain data in a fixed order (the input of config_sha256)."""
    strip = lambda d: {k: v for k, v in d.items() if k not in ("evidence", "tuned_on", "origin")}          # noqa: E731 (origin: the J6 defining profile)
    return {
        "chain": chain(profile),
        "settings": {k: profile.settings[k] for k in sorted(getattr(profile, "settings", {}) or {})},
        "lists": {k: list(v) for k, v in sorted((getattr(profile, "lists", {}) or {}).items())},
        "rules": [_rule(r) for r in profile.rules],
        "file_roles": [_rule(r) for r in profile.file_roles],
        "structural": [strip(dict(s)) for s in profile.structural],
        "path_grammar": [strip(dict(x)) if isinstance(x, dict) else repr(x) for x in profile.path_grammar],
        "name_grammar": [strip(dict(x)) if isinstance(x, dict) else repr(x) for x in profile.name_grammar],
        "manifest_reading": _reading(profile.manifest_reading),
        "disabled": list(getattr(profile, "disabled", ())), "replaced": list(getattr(profile, "replaced", ())),
        "overridden": list(getattr(profile, "overridden", ())),
    }


def config_sha256(profile) -> str:
    blob = json.dumps(canonical(profile), sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=repr)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def provenance(profile) -> dict:
    """The `configuration` block of classes.json."""
    decl = getattr(profile, "settings_decl", {}) or {}
    values = getattr(profile, "settings", {}) or {}
    settings = {n: {"value": values[n], "default": decl[n]["default"], "is_default": values[n] == decl[n]["default"]} for n in sorted(decl)}
    non_default = [n for n in sorted(decl) if not settings[n]["is_default"]]
    ch = chain(profile)
    overlays = [c["profile_id"] for c in ch if c["shipped"] is False]
    disabled, replaced, overridden = list(getattr(profile, "disabled", ())), list(getattr(profile, "replaced", ())), list(getattr(profile, "overridden", ()))
    default = not (non_default or disabled or replaced or overridden or overlays)
    return {"chain": ch, "overlays": overlays, "settings": settings, "settings_set": list(getattr(profile, "settings_set", ())), "non_default_settings": non_default,
            "disabled_rules": disabled, "replaced_rules": replaced, "overridden_lists": overridden, "default_configuration": default,
            "config_sha256": config_sha256(profile)}


def report_section(conf: dict) -> list:
    """The Configuration section of report.md (lines)."""
    lines = ["", "## Configuration", "",
             "Profile chain: " + ", ".join(f"{c['profile_id']} {c['version']} ({'shipped' if c['shipped'] else 'composition' if c['shipped'] is None else 'OVERLAY'})"
                                          for c in conf["chain"]) + ".", ""]
    if conf["default_configuration"]:
        lines += ["Default configuration (Dan's rulings): the configuration the held-out runs confirm.", ""]
    else:
        lines += ["**NON-DEFAULT CONFIGURATION.** Only the default configuration is held-out-confirmed; these results are not.", ""]
    if conf["settings"]:
        lines += ["| setting | value | default |", "|---|---|---|"]
        for n, s in conf["settings"].items():
            mark = "" if s["is_default"] else " **(set)**"
            lines.append(f"| {n} | {json.dumps(s['value'])}{mark} | {json.dumps(s['default'])} |")
        lines.append("")
    for label, key in (("Settings set by a profile", "settings_set"), ("Disabled rules", "disabled_rules"), ("Replaced rules", "replaced_rules"),
                       ("Overridden lists", "overridden_lists"), ("Overlay profiles", "overlays")):
        lines.append(f"{label}: {', '.join(conf[key]) if conf[key] else 'none'}.")
    lines += ["", f"config_sha256: `{conf['config_sha256']}`"]
    return lines
