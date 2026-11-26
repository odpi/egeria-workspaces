"""Layout profile model v0: a versioned YAML document (NOT an Egeria type), its loader and its validator.

A profile says which folders of a repository are components, which are source/test/docs/config and which are generated, vendored,
runtime output, copies or backups, as ORDERED rules: the FIRST rule that matches wins. Every rule carries a basis, a confidence and an
evidence string, because every claim must say why it is made. Anything the loader does not recognise is an error, never ignored:
an unknown role, an unknown relevance, an unknown key at any level, a duplicate rule id, a rule with no evidence.

Composition: `extends: [a, b]` puts the child's own rules first, then a's, then b's (an earlier list entry is checked first).
Only PyYAML and the standard library are used. Nothing here reads a repository.
"""
from __future__ import annotations

import fnmatch  # noqa: F401  (documents that globs are fnmatch-like; the translation below is our own, to give `**` a meaning)
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

STATUSES = ("proposed", "confirmed", "retired")
APPLIES_TO = ("any", "code-repo", "docs-site", "workspace-of-repos")
ROLES = ("component", "source", "test", "docs", "config", "generated", "vendored", "scratch", "archive", "audit", "runtime-output",
         "vcs-internal", "worktree-copy", "backup", "secret", "example", "ci", "tooling", "build", "data-fixture", "other")
RELEVANCES = ("primary", "supporting", "hidden")
GRAINS = ("subtree", "dir", "component")
BASES = ("manifest", "manifest-content", "convention", "judgement")
CONFIDENCES = ("high", "medium", "low")
MATCH_KEYS = ("path_glob", "path_segment", "name", "name_regex", "extension", "has_file", "parent_has_file", "has_entry", "ancestor_has_entry",
              "component_scope")
DIR_ONLY_KEYS = ("has_file", "parent_has_file", "has_entry", "ancestor_has_entry")   # evaluated against a directory, not a file
COMPONENT_SCOPES = ("within", "root")                  # file rules only: under some component / directly in a component's directory
FILE_ONLY_KEYS = ("extension",)                        # meaningful only for a file name
ASSIGN_KEYS = ("role", "relevance", "kind")
TOP_KEYS = ("profile_id", "version", "status", "applies_to", "extends", "roles", "relevance", "rules", "file_roles", "manifest_reading", "structural_rules", "path_grammar", "name_grammar")
RULE_KEYS = ("id", "match", "assign", "grain", "basis", "confidence", "evidence")
RULE_OPTIONAL_KEYS = ("tuned_on",)       # which repositories motivated the rule, so a reviewer can ablate it (a one-repository rule is suspect)
MANIFEST_READING_KEYS = ("readers", "max_file_bytes", "max_blobs", "max_total_bytes", "member_rule", "aggregator_rule", "section_rule", "fallback_section_rule",
                         "docs_content_rule", "site_output_rule", "fallback_site_rule")
MANIFEST_RULE_NAMES = ("member_rule", "aggregator_rule", "section_rule", "fallback_section_rule")
MANIFEST_RULE_KEYS = ("id", "role", "kind", "basis", "confidence", "evidence")
STRUCTURAL_OPS = ("sibling-manifests-top-level",)
STRUCTURAL_KEYS = ("id", "op", "min", "basis", "confidence", "evidence")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
SLUG = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
RULE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class ProfileError(ValueError):
    """The profile document is not valid. The message names the file, the rule and the problem."""


def glob_to_regex(pattern: str) -> str:
    """`*` = any run without `/`, `?` = one char without `/`, `**` = anything including `/`, `[..]` = a character class."""
    out, i = [], 0
    while i < len(pattern):
        c = pattern[i]
        if c == "*":
            if pattern[i:i + 2] == "**":
                out.append(".*")
                i += 2
                continue
            out.append("[^/]*")
        elif c == "?":
            out.append("[^/]")
        elif c == "[":
            j = pattern.find("]", i + 1)
            if j == -1:
                out.append(re.escape(c))
            else:
                out.append(pattern[i:j + 1])
                i = j
        else:
            out.append(re.escape(c))
        i += 1
    return "^" + "".join(out) + "$"


def _as_list(value: Any) -> list:
    return list(value) if isinstance(value, (list, tuple)) else [value]


@dataclass(frozen=True)
class Rule:
    id: str
    match: dict
    role: str
    relevance: str
    kind: str | None
    grain: str
    basis: str
    confidence: str
    evidence: str
    origin: str                                  # the profile that defined it
    tuned_on: tuple = ()                         # repositories that motivated the rule (documentation for ablation; never used to match)
    # compiled forms (filled by the loader)
    segments: frozenset = frozenset()
    names: frozenset = frozenset()
    extensions: tuple = ()
    globs: tuple = ()                            # compiled full-path regexes
    root_globs: tuple = ()                       # compiled regexes of the directory a subtree glob names (pattern minus `/**`)
    name_res: tuple = ()
    has_files: frozenset = frozenset()
    parent_has_files: frozenset = frozenset()
    has_entries: frozenset = frozenset()         # a FILE or a sub-DIRECTORY of this name sits directly in the directory (.git is either)
    ancestor_entries: frozenset = frozenset()    # some proper ancestor directory (the scanned root included) has such an entry
    scope: str = ""                              # file rules: '' | 'within' (under a component) | 'root' (directly in a component's directory)

    @property
    def is_dir_rule(self) -> bool:
        """A rule is evaluated against DIRECTORIES when it tests a directory's files (has_file / parent_has_file / has_entry /
        ancestor_has_entry) or claims a component: its path_glob / path_segment / name / name_regex then apply to the directory itself."""
        return bool(self.has_files or self.parent_has_files or self.has_entries or self.ancestor_entries) or self.grain == "component"


@dataclass(frozen=True)
class ManifestReading:
    """Which manifests the recognizer MAY read (a subset of the closed list in manifests.py), the caps, and the two rules whose ids, basis,
    confidence and evidence the findings copy: one for a directory that a manifest declares as a MEMBER (a workspace or module member), one for a
    directory that only AGGREGATES its members (it is not a component)."""
    readers: tuple
    max_file_bytes: int
    max_blobs: int
    max_total_bytes: int
    member_rule: Rule | None = None
    aggregator_rule: Rule | None = None
    section_rule: Rule | None = None             # mkdocs: a top-level nav section (kind doc-section, a part of its site)
    fallback_section_rule: Rule | None = None    # mkdocs: a top-level folder of the docs folder that holds pages, where there is no nav (low confidence)
    docs_content_rule: str | None = None         # id of the profile's rule that claims the docs folder (applied where mkdocs.yml names another docs_dir)
    site_output_rule: str | None = None          # id of the profile's rule that hides the built site (applied where mkdocs.yml names another site_dir)
    fallback_site_rule: str | None = None        # id of the profile's rule that recognizes a site by its generator's config FILE NAME (never read): the fallback sections apply there


@dataclass
class Profile:
    profile_id: str
    version: str
    status: str
    applies_to: str
    roles: tuple
    relevance: dict                              # role -> primary | supporting | hidden
    rules: list = field(default_factory=list)
    manifest_reading: ManifestReading | None = None
    file_roles: tuple = ()                       # the FILE-ROLE layer: path rules that give a file a role only where no rule above claimed it
    extends: tuple = ()
    path_grammar: tuple = ()
    name_grammar: tuple = ()
    composed_of: tuple = ()                      # ((profile_id, version), ...) in the order their rules are checked
    structural: tuple = ()                       # structural rules (dicts), the child's first

    @property
    def major(self) -> str:
        return self.version.split(".")[0]

    def rules_by_id(self) -> dict:
        return {r.id: r for r in (*self.rules, *self.file_roles)}


def _check_keys(where: str, obj: Any, allowed: tuple, required: tuple = ()) -> None:
    if not isinstance(obj, dict):
        raise ProfileError(f"{where}: expected a mapping, got {type(obj).__name__}")
    unknown = sorted(set(obj) - set(allowed))
    if unknown:
        raise ProfileError(f"{where}: unknown key(s) {unknown}; allowed {list(allowed)}")
    missing = [k for k in required if k not in obj]
    if missing:
        raise ProfileError(f"{where}: missing required key(s) {missing}")


def _compile_rule(where: str, raw: dict, roles: tuple, rel_map: dict, origin: str) -> Rule:
    _check_keys(where, raw, RULE_KEYS + RULE_OPTIONAL_KEYS, RULE_KEYS)
    rid = raw["id"]
    tuned_on = raw.get("tuned_on", [])
    if not isinstance(tuned_on, list) or not all(isinstance(x, str) and x for x in tuned_on):
        raise ProfileError(f"{where} rule {rid!r}: tuned_on must be a list of repository names")
    where = f"{where} rule {rid!r}"
    if not isinstance(rid, str) or not RULE_ID.match(rid):
        raise ProfileError(f"{where}: id must be a simple identifier")
    match = raw["match"]
    _check_keys(f"{where} match", match, MATCH_KEYS)
    if not match:
        raise ProfileError(f"{where}: match must name at least one of {list(MATCH_KEYS)}")
    assign = raw["assign"]
    _check_keys(f"{where} assign", assign, ASSIGN_KEYS, ("role",))
    role = assign["role"]
    if role not in roles:
        raise ProfileError(f"{where}: unknown role {role!r}; allowed {list(roles)}")
    relevance = assign.get("relevance") or rel_map.get(role)
    if relevance is None:
        raise ProfileError(f"{where}: role {role!r} has no relevance (name it in the profile's `relevance` map or in the rule)")
    if relevance not in RELEVANCES:
        raise ProfileError(f"{where}: unknown relevance {relevance!r}; allowed {list(RELEVANCES)}")
    for key, allowed in (("grain", GRAINS), ("basis", BASES), ("confidence", CONFIDENCES)):
        if raw[key] not in allowed:
            raise ProfileError(f"{where}: {key} {raw[key]!r} is not one of {list(allowed)}")
    evidence = raw["evidence"]
    if not isinstance(evidence, str) or not evidence.strip():
        raise ProfileError(f"{where}: evidence must be a non-empty string")

    dir_keys = [k for k in DIR_ONLY_KEYS if k in match]
    file_keys = [k for k in FILE_ONLY_KEYS if k in match]
    dir_rule = bool(dir_keys) or raw["grain"] == "component"
    scope = match.get("component_scope", "")
    if scope and scope not in COMPONENT_SCOPES:
        raise ProfileError(f"{where}: component_scope {scope!r} is not one of {list(COMPONENT_SCOPES)}")
    if scope and dir_rule:
        raise ProfileError(f"{where}: component_scope applies to a FILE rule; this rule tests a directory")
    if dir_rule and file_keys:
        raise ProfileError(f"{where}: a directory rule ({dir_keys or 'grain component'}) cannot test {file_keys} (a file-name test)")
    for key in ("name", "extension", "path_segment", "path_glob", "name_regex", "has_file", "parent_has_file", "has_entry", "ancestor_has_entry"):
        if key in match:
            for v in _as_list(match[key]):
                if not isinstance(v, str) or not v:
                    raise ProfileError(f"{where}: match.{key} needs non-empty strings")
    grain = raw["grain"]
    globs, root_globs = [], []
    for g in _as_list(match.get("path_glob", [])):
        try:
            globs.append(re.compile(glob_to_regex(g)))
        except re.error as exc:
            raise ProfileError(f"{where}: bad path_glob {g!r}: {exc}") from exc
        if grain == "subtree" and not dir_rule:
            if not g.endswith("/**"):
                raise ProfileError(f"{where}: a subtree rule's path_glob must end with '/**' (it names the root directory), got {g!r}")
            root_globs.append(re.compile(glob_to_regex(g[:-3])))
    if grain == "subtree" and not dir_rule and "path_segment" not in match and "path_glob" not in match:
        raise ProfileError(f"{where}: grain subtree needs path_segment or path_glob to say where the subtree starts")
    if grain == "component" and not any(k in match for k in ("has_file", "parent_has_file", "path_glob", "path_segment", "name", "name_regex")):
        raise ProfileError(f"{where}: grain component is a directory claim: it needs a test of the directory")
    if grain == "component" and role != "component":
        raise ProfileError(f"{where}: grain component must assign role 'component' (a part of a component gets its own rule)")
    name_res = []
    for rx in _as_list(match.get("name_regex", [])):
        try:
            name_res.append(re.compile(rx))
        except re.error as exc:
            raise ProfileError(f"{where}: bad name_regex {rx!r}: {exc}") from exc
    return Rule(
        tuned_on=tuple(tuned_on), id=rid, match=dict(match), role=role, relevance=relevance, kind=assign.get("kind"), grain=grain, basis=raw["basis"],
        confidence=raw["confidence"], evidence=evidence.strip(), origin=origin,
        segments=frozenset(_as_list(match.get("path_segment", []))), names=frozenset(_as_list(match.get("name", []))),
        extensions=tuple(_as_list(match.get("extension", []))), globs=tuple(globs), root_globs=tuple(root_globs),
        name_res=tuple(name_res), has_files=frozenset(_as_list(match.get("has_file", []))),
        parent_has_files=frozenset(_as_list(match.get("parent_has_file", []))),
        has_entries=frozenset(_as_list(match.get("has_entry", []))), ancestor_entries=frozenset(_as_list(match.get("ancestor_has_entry", []))),
        scope=scope,
    )


def _manifest_reading(where: str, doc: Any, roles: tuple, rel_map: dict, origin: str):
    if doc is None:
        return None
    from .manifests import DEFAULT_MAX_BLOBS, DEFAULT_MAX_FILE_BYTES, DEFAULT_MAX_TOTAL_BYTES, READERS
    w = f"{where} manifest_reading"
    _check_keys(w, doc, MANIFEST_READING_KEYS + ("tuned_on",), ("readers",))
    readers = doc["readers"]
    if not isinstance(readers, list) or not readers or any(r not in READERS for r in readers) or len(set(readers)) != len(readers):
        raise ProfileError(f"{w}: readers must be a non-empty list of distinct names from {list(READERS)}")
    caps = {}
    for key, default in (("max_file_bytes", DEFAULT_MAX_FILE_BYTES), ("max_blobs", DEFAULT_MAX_BLOBS), ("max_total_bytes", DEFAULT_MAX_TOTAL_BYTES)):
        v = doc.get(key, default)
        if not isinstance(v, int) or isinstance(v, bool) or v < 1 or v > default:
            raise ProfileError(f"{w}: {key} must be an integer from 1 to {default} (a profile may tighten a cap, never raise it)")
        caps[key] = v
    from .manifests import CODE_READERS
    need = set()
    if set(readers) & set(CODE_READERS):
        need |= {"member_rule", "aggregator_rule"}
    if "mkdocs" in readers:
        need |= {"section_rule", "fallback_section_rule"}
    for which in MANIFEST_RULE_NAMES:
        if (which in doc) != (which in need):
            raise ProfileError(f"{w}: {which} is {'required' if which in need else 'not allowed'} for readers {list(readers)}")
    rules = {}
    for which in (x for x in MANIFEST_RULE_NAMES if x in doc):
        raw = doc[which]
        _check_keys(f"{w} {which}", raw, MANIFEST_RULE_KEYS + ("tuned_on",), MANIFEST_RULE_KEYS)
        if raw["role"] not in roles:
            raise ProfileError(f"{w} {which}: unknown role {raw['role']!r}; allowed {list(roles)}")
        if which in ("member_rule", "section_rule", "fallback_section_rule") and raw["role"] != "component":
            raise ProfileError(f"{w} {which}: the role must be 'component'")
        if which == "aggregator_rule" and raw["role"] == "component":
            raise ProfileError(f"{w} aggregator_rule: an aggregator is NOT a component")
        rel = rel_map.get(raw["role"])
        if rel is None:
            raise ProfileError(f"{w} {which}: role {raw['role']!r} has no relevance")
        for key, allowed in (("basis", BASES), ("confidence", CONFIDENCES)):
            if raw[key] not in allowed:
                raise ProfileError(f"{w} {which}: {key} {raw[key]!r} is not one of {list(allowed)}")
        if not isinstance(raw["evidence"], str) or not raw["evidence"].strip():
            raise ProfileError(f"{w} {which}: evidence must be a non-empty string")
        if not isinstance(raw["id"], str) or not RULE_ID.match(raw["id"]):
            raise ProfileError(f"{w} {which}: id must be a simple identifier")
        tuned = raw.get("tuned_on", [])
        if not isinstance(tuned, list) or not all(isinstance(x, str) and x for x in tuned):
            raise ProfileError(f"{w} {which}: tuned_on must be a list of repository names")
        rules[which] = Rule(id=raw["id"], match={}, role=raw["role"], relevance=rel, kind=raw["kind"], grain="dir" if which == "aggregator_rule" else "component",
                            basis=raw["basis"], confidence=raw["confidence"], evidence=raw["evidence"].strip(), origin=origin, tuned_on=tuple(tuned))
    ids = [r.id for r in rules.values()]
    if len(set(ids)) != len(ids):
        raise ProfileError(f"{w}: the manifest rules need different ids")
    for key in ("docs_content_rule", "site_output_rule", "fallback_site_rule"):
        if key in doc and (not isinstance(doc[key], str) or not RULE_ID.match(doc[key]) or "mkdocs" not in readers):
            raise ProfileError(f"{w}: {key} must name a rule id and needs the mkdocs reader")
    return ManifestReading(readers=tuple(readers), docs_content_rule=doc.get("docs_content_rule"), site_output_rule=doc.get("site_output_rule"),
                           fallback_site_rule=doc.get("fallback_site_rule"),
                           **{k: rules.get(k) for k in MANIFEST_RULE_NAMES}, **caps)


def _grammar(where: str, items: Any, must: tuple) -> tuple:
    if items is None:
        return ()
    if not isinstance(items, list):
        raise ProfileError(f"{where}: expected a list")
    out = []
    for n, item in enumerate(items):
        _check_keys(f"{where}[{n}]", item, must, must)
        out.append(dict(item))
    return tuple(out)


def _structural(where: str, items: Any) -> tuple:
    if items is None:
        return ()
    if not isinstance(items, list):
        raise ProfileError(f"{where}: structural_rules must be a list")
    out = []
    for n, item in enumerate(items):
        w = f"{where} structural_rules[{n}]"
        _check_keys(w, item, STRUCTURAL_KEYS + ("tuned_on",), STRUCTURAL_KEYS)
        if item["op"] not in STRUCTURAL_OPS:
            raise ProfileError(f"{w}: op {item['op']!r} is not one of {list(STRUCTURAL_OPS)}")
        if not isinstance(item["min"], int) or isinstance(item["min"], bool) or item["min"] < 2:
            raise ProfileError(f"{w}: min must be an integer of at least 2")
        for key, allowed in (("basis", BASES), ("confidence", CONFIDENCES)):
            if item[key] not in allowed:
                raise ProfileError(f"{w}: {key} {item[key]!r} is not one of {list(allowed)}")
        if not isinstance(item["evidence"], str) or not item["evidence"].strip():
            raise ProfileError(f"{w}: evidence must be a non-empty string")
        if not isinstance(item["id"], str) or not RULE_ID.match(item["id"]):
            raise ProfileError(f"{w}: id must be a simple identifier")
        out.append({**item, "evidence": item["evidence"].strip(), "tuned_on": list(item.get("tuned_on", []))})
    return tuple(out)


def parse_profile(doc: Any, source: str = "<profile>", profiles_dir: Path | None = None, _stack: tuple = ()) -> Profile:
    """Validate a parsed YAML document and return the composed Profile (its `extends` resolved from `profiles_dir`)."""
    _check_keys(source, doc, TOP_KEYS, ("profile_id", "version", "status", "applies_to", "roles", "relevance", "rules"))
    pid = doc["profile_id"]
    if not isinstance(pid, str) or not SLUG.match(pid):
        raise ProfileError(f"{source}: profile_id must be a lowercase slug")
    if pid in _stack:
        raise ProfileError(f"{source}: extends cycle {' -> '.join(_stack + (pid,))}")
    version = doc["version"]
    if not isinstance(version, str) or not SEMVER.match(version):
        raise ProfileError(f"{source}: version must be a semver string like '0.1.0' (quote it), got {version!r}")
    if doc["status"] not in STATUSES:
        raise ProfileError(f"{source}: status {doc['status']!r} is not one of {list(STATUSES)}")
    if doc["applies_to"] not in APPLIES_TO:
        raise ProfileError(f"{source}: applies_to {doc['applies_to']!r} is not one of {list(APPLIES_TO)}")
    roles = doc["roles"]
    if not isinstance(roles, list) or not roles:
        raise ProfileError(f"{source}: roles must be a non-empty list")
    bad = [r for r in roles if r not in ROLES]
    if bad:
        raise ProfileError(f"{source}: unknown role(s) {bad}; allowed {list(ROLES)}")
    if len(set(roles)) != len(roles):
        raise ProfileError(f"{source}: roles lists a role twice")
    rel = doc["relevance"]
    _check_keys(f"{source} relevance", rel, RELEVANCES)
    rel_map: dict[str, str] = {}
    for level, members in rel.items():
        if not isinstance(members, list):
            raise ProfileError(f"{source} relevance.{level}: expected a list of roles")
        for role in members:
            if role not in roles:
                raise ProfileError(f"{source} relevance.{level}: role {role!r} is not in this profile's roles")
            if role in rel_map:
                raise ProfileError(f"{source} relevance: role {role!r} is listed under {rel_map[role]!r} and {level!r}")
            rel_map[role] = level

    extends = doc.get("extends") or []
    if not isinstance(extends, list):
        raise ProfileError(f"{source}: extends must be a list of profile ids")
    own_rules = []
    raw_rules = doc["rules"]
    if not isinstance(raw_rules, list):
        raise ProfileError(f"{source}: rules must be a list")
    for n, raw in enumerate(raw_rules):
        own_rules.append(_compile_rule(f"{source} rules[{n}]", raw, tuple(roles), rel_map, pid))

    mreading = _manifest_reading(source, doc.get("manifest_reading"), tuple(roles), rel_map, pid)
    raw_fr = doc.get("file_roles") or []
    if not isinstance(raw_fr, list):
        raise ProfileError(f"{source}: file_roles must be a list")
    own_fr = []
    for n, raw in enumerate(raw_fr):
        r = _compile_rule(f"{source} file_roles[{n}]", raw, tuple(roles), rel_map, pid)
        if r.is_dir_rule or r.grain != "dir":
            raise ProfileError(f"{source} file_roles[{n}] rule {r.id!r}: a file-role rule tests a FILE and has grain 'dir'")
        own_fr.append(r)
    all_roles = list(roles)
    merged_rel = dict(rel_map)
    rules = list(own_rules)
    composed = [(pid, version)]
    path_grammar = _grammar(f"{source} path_grammar", doc.get("path_grammar"), ("id", "pattern", "yields"))
    name_grammar = _grammar(f"{source} name_grammar", doc.get("name_grammar"), ("id", "pattern", "yields"))
    structural_own = _structural(source, doc.get("structural_rules"))
    structural = list(structural_own)
    for base_id in extends:
        if profiles_dir is None:
            raise ProfileError(f"{source}: extends {base_id!r} but no profiles directory was given")
        base = load_profile(base_id, profiles_dir, _stack + (pid,))
        for role in base.roles:
            if role not in all_roles:
                all_roles.append(role)
        for role, level in base.relevance.items():
            merged_rel.setdefault(role, level)          # the child's mapping wins
        rules.extend(base.rules)
        own_fr.extend(base.file_roles)
        if mreading is None:
            mreading = base.manifest_reading             # the child's own wins; otherwise the first extended profile that has one
        structural.extend(base.structural)
        composed.extend(base.composed_of)
    own_ids = [r.id for r in own_rules] + [r.id for r in own_fr if r.origin == pid]
    if len(set(own_ids)) != len(own_ids):
        raise ProfileError(f"{source}: rule id {next(i for i in own_ids if own_ids.count(i) > 1)!r} is used twice in this profile; ids must be unique")
    own_sids = [x["id"] for x in structural_own]
    if len(set(own_sids)) != len(own_sids) or set(own_sids) & set(own_ids):
        raise ProfileError(f"{source}: structural rule ids must be unique and differ from rule ids")
    # A profile reached twice (a diamond: two extended profiles share a base) contributes its rules ONCE, at the first place it is met.
    # The same rule id coming from two DIFFERENT profiles is still an error.
    deduped, seen = [], {}
    for rule in rules:
        if rule.id in seen:
            if seen[rule.id] == rule.origin:
                continue
            raise ProfileError(f"{source}: rule id {rule.id!r} is used twice (in {seen[rule.id]!r} and {rule.origin!r}); ids must be unique")
        seen[rule.id] = rule.origin
        deduped.append(rule)
    rules = deduped
    if mreading is not None:
        ids_now = {r.id for r in rules}
        for key in ("docs_content_rule", "site_output_rule", "fallback_site_rule"):
            ref = getattr(mreading, key)
            if ref is not None and ref not in ids_now:
                raise ProfileError(f"{source}: manifest_reading.{key} names {ref!r}, which is not a rule of this profile")
    fr_out = []
    for rule in own_fr:                                  # same dedupe for the file-role layer; ids are unique across both lists
        if rule.id in seen:
            if seen[rule.id] == rule.origin and any(x.id == rule.id for x in fr_out):
                continue
            raise ProfileError(f"{source}: rule id {rule.id!r} is used twice (in {seen[rule.id]!r} and {rule.origin!r}); ids must be unique")
        seen[rule.id] = rule.origin
        fr_out.append(rule)
    uniq, seen_s = [], set()
    for x in structural:
        if x["id"] not in seen_s:
            seen_s.add(x["id"])
            uniq.append(x)
    structural = uniq
    if seen_s & set(seen):
        raise ProfileError(f"{source}: structural rule ids must differ from rule ids")
    composed = list(dict.fromkeys(composed))
    return Profile(profile_id=pid, version=version, status=doc["status"], applies_to=doc["applies_to"], roles=tuple(all_roles),
                   relevance=merged_rel, rules=rules, file_roles=tuple(fr_out), manifest_reading=mreading, extends=tuple(extends), path_grammar=path_grammar, name_grammar=name_grammar,
                   composed_of=tuple(composed), structural=tuple(structural))


def load_profile(profile_id_or_path: str, profiles_dir: Path | str | None = None, _stack: tuple = ()) -> Profile:
    """Load `profiles_dir/<profile_id>.yaml` (or a path to a .yaml file) and validate it."""
    p = Path(profile_id_or_path)
    if p.suffix not in (".yaml", ".yml"):
        if profiles_dir is None:
            raise ProfileError(f"profile id {profile_id_or_path!r} needs a profiles directory")
        p = Path(profiles_dir) / f"{profile_id_or_path}.yaml"
        base_dir = Path(profiles_dir)
    else:
        base_dir = Path(profiles_dir) if profiles_dir else p.parent
    if not p.is_file():
        raise ProfileError(f"profile file not found: {p}")
    try:
        doc = yaml.safe_load(p.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ProfileError(f"{p}: not valid YAML: {exc}") from exc
    prof = parse_profile(doc, str(p), base_dir, _stack)
    if p.stem != prof.profile_id and p.suffix in (".yaml", ".yml") and not str(profile_id_or_path).endswith((".yaml", ".yml")):
        raise ProfileError(f"{p}: profile_id {prof.profile_id!r} does not match the file name")
    return prof
