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
         "vcs-internal", "worktree-copy", "backup", "secret", "example", "ci", "tooling", "build", "data-fixture", "other", "fixture", "static-assets", "theme", "include-fragments", "test-support")
RELEVANCES = ("primary", "supporting", "hidden")
GRAINS = ("subtree", "dir", "component")
BASES = ("manifest", "manifest-content", "convention", "judgement")
CONFIDENCES = ("high", "medium", "low")
MATCH_KEYS = ("path_glob", "path_segment", "name", "name_regex", "extension", "has_file", "parent_has_file", "has_entry", "ancestor_has_entry",
              "component_scope", "no_source_files", "parent_name_token", "has_child_dir", "orphaned", "segment_regex", "child_segment_regex", "groups_projects", "group_segment_regex", "min_content", "parent_not_role", "only_files")
DIR_ONLY_KEYS = ("has_file", "parent_has_file", "has_entry", "ancestor_has_entry", "no_source_files", "parent_name_token", "has_child_dir", "orphaned", "segment_regex", "child_segment_regex", "groups_projects", "group_segment_regex", "min_content", "parent_not_role", "only_files")   # evaluated against a directory, not a file
COMPONENT_SCOPES = ("within", "root")                  # file rules only: under some component / directly in a component's directory
FILE_ONLY_KEYS = ("extension",)                        # meaningful only for a file name
ASSIGN_KEYS = ("role", "relevance", "kind")
TOP_KEYS = ("profile_id", "version", "status", "applies_to", "extends", "roles", "relevance", "rules", "file_roles", "manifest_reading", "structural_rules", "path_grammar", "name_grammar",
            "required", "allowed_only", "content_checks", "states")   # conformance (recognizer/grammar.py, Phase 2 notebook 05; states: 04a)
RULE_KEYS = ("id", "match", "assign", "grain", "basis", "confidence", "evidence")
RULE_OPTIONAL_KEYS = ("tuned_on", "file_scope")   # tuned_on: which repositories motivated the rule, so a reviewer can ablate it (a one-repository rule is suspect);
                                                  # file_scope (H1): a grain-dir directory claim whose files are classified as if it were a component (component_scope)
MANIFEST_READING_KEYS = ("readers", "max_file_bytes", "max_blobs", "max_total_bytes", "member_rule", "aggregator_rule", "section_rule", "fallback_section_rule",
                         "docs_content_rule", "site_output_rule", "fallback_site_rule", "submodule_rule", "translation_rule", "included_build_rule")
MANIFEST_RULE_NAMES = ("member_rule", "aggregator_rule", "section_rule", "fallback_section_rule", "translation_rule", "included_build_rule")
OPTIONAL_MANIFEST_RULES = ("translation_rule", "included_build_rule")        # allowed with the mkdocs reader, never required
MANIFEST_RULE_KEYS = ("id", "role", "kind", "basis", "confidence", "evidence")
STRUCTURAL_OPS = ("sibling-manifests-top-level", "compose-deployment", "notebook-folder", "mostly-extension-folder")
STRUCTURAL_OPTIONAL = ("tuned_on", "kind", "share", "extensions", "no_code", "name_regex", "yaml_key")
STRUCTURAL_KEYS = ("id", "op", "min", "basis", "confidence", "evidence")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
SLUG = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
COMPOSITE_ID = re.compile(r"^[a-z0-9][a-z0-9._-]*(\+[a-z0-9][a-z0-9._-]*)+$")      # `a+b`: a composition made at run time, never a file name
RULE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


CONFORMANCE_KINDS = ("structure", "naming", "content-type")   # the `kind` of a CONFORMANCE finding (grain conformance); never a component or role kind


def _not_conformance_kind(where: str, kind) -> None:
    if kind in CONFORMANCE_KINDS:
        raise ProfileError(f"{where}: kind {kind!r} is reserved for conformance findings (structure, naming, content-type); a component or role kind needs another name")


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
    segment_res: tuple = ()                      # directory rules: some WHOLE segment of the directory's path matches one of these regexes (write (?i) for case-insensitive)
    child_dirs: frozenset = frozenset()          # directory rules: the directory directly contains a sub-directory with one of these relative paths (docs/javadoc is two levels)
    orphaned: bool = False                       # directory rules: the PARENT directory holds nothing but this directory (no files, no other sub-directories)
    no_source: bool = False                      # directory rules: no file anywhere below the directory has a source-code extension
    parent_tokens: frozenset = frozenset()       # directory rules: one of these is a whole word of the PARENT directory's name (split at punctuation and case changes)
    child_seg_parents: frozenset = frozenset()   # directory rules (F1): child_segment_regex's `parent`: the exact names a segment's PARENT segment must have
    child_seg_res: tuple = ()                    # child_segment_regex's `regex` (case-sensitive unless written (?i)); with segment_res it forms ONE segment test (either may match)
    group_files: frozenset = frozenset()         # directory rules (E1): the manifest names that make a directory a project, for groups_projects / group_segment_regex
    group_min: int = 0                           # groups_projects: the directory is not itself a project and at least this many projects lie below it
    group_seg_res: tuple = ()                    # group_segment_regex: some PROPER ancestor whose own name matches one of these regexes groups at least group_min projects
    content_files: frozenset = frozenset()       # directory rules (G2): min_content's `files`: a site or build configuration NAME directly in the directory or in a direct child folder
    content_min: int = 0                         # min_content's `min_files`: otherwise at least this many files with one of content_exts anywhere below the directory (names only)
    content_exts: tuple = ()                     # min_content's `extensions`
    only_dirs: frozenset = frozenset()           # directory rules (H2): only_files' `child_dirs` (lower-case): any file below a DIRECT child folder of one of these names qualifies
    only_res: tuple = ()                         # only_files' `names` (globs, case-insensitive): a file whose NAME matches one qualifies
    only_files: bool = False                     # only_files is set: the directory holds at least one file and EVERY file anywhere below it qualifies (names only)
    parent_not_roles: frozenset = frozenset()    # directory rules (H1): the PARENT directory is not claimed by a rule whose assigned role is one of these
    file_scope: bool = False                     # H1: the directory this (grain dir) rule claims is a file-role scope, like a component directory, though it is not a component
    named_dir: bool = False                      # a subtree rule that names the directory (`name`) rather than a path: it is a directory rule
    scope: str = ""                              # file rules: '' | 'within' (under a component) | 'root' (directly in a component's directory)

    @property
    def is_dir_rule(self) -> bool:
        """A rule is evaluated against DIRECTORIES when it tests a directory's files (has_file / parent_has_file / has_entry /
        ancestor_has_entry) or claims a component: its path_glob / path_segment / name / name_regex then apply to the directory itself."""
        return bool(self.has_files or self.parent_has_files or self.has_entries or self.ancestor_entries or self.no_source or self.parent_tokens or self.child_dirs or self.orphaned or self.segment_res or self.child_seg_res or self.group_min or self.content_min or self.parent_not_roles or self.only_files) \
            or self.grain == "component" or self.named_dir

    @property
    def has_segment_test(self) -> bool:
        return bool(self.segment_res or self.child_seg_res)

    def segment_matches(self, segs: list) -> bool:
        """The rule's ONE segment test: some whole segment of the path matches segment_regex, or some segment whose PARENT segment is exactly one of
        child_segment_regex's `parent` names matches its `regex` (F1). The directory's own name counts as a segment, as for segment_regex."""
        if self.segment_res and any(rx.search(sg) for sg in segs for rx in self.segment_res):
            return True
        return bool(self.child_seg_res) and any(segs[i - 1] in self.child_seg_parents and any(rx.search(segs[i]) for rx in self.child_seg_res) for i in range(1, len(segs)))


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
    included_build_rule: Rule | None = None      # gradle: a directory named by `includeBuild('dir')` is internal tooling (role tooling), and so is every manifest project below it
    translation_rule: Rule | None = None         # mkdocs: a site whose mkdocs.yml INHERITs another site's is a translation of it (kind doc-translation), not a site
    fallback_section_rule: Rule | None = None    # mkdocs: a top-level folder of the docs folder that holds pages, where there is no nav (low confidence)
    docs_content_rule: str | None = None         # id of the profile's rule that claims the docs folder (applied where mkdocs.yml names another docs_dir)
    site_output_rule: str | None = None          # id of the profile's rule that hides the built site (applied where mkdocs.yml names another site_dir)
    submodule_rule: str | None = None            # id of the profile's nested-repository rule: a directory the outer repository's .gitmodules declares is NOT claimed by it
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
    path_grammar: tuple = ()                     # grammar.PathPattern, the child's first (conformance; empty in every Phase 1 profile)
    name_grammar: tuple = ()                     # grammar.NameGrammar
    required: tuple = ()                         # grammar.Required
    allowed_only: tuple = ()                     # grammar.AllowedOnly
    content_checks: tuple = ()                   # grammar.ContentCheck (only dataset_description.json, only under bids-dataset)
    states: tuple = ()                           # grammar.State (04a F3: counts per typed folder, never findings)
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
    _not_conformance_kind(where, assign.get("kind"))

    dir_keys = [k for k in DIR_ONLY_KEYS if k in match]
    file_keys = [k for k in FILE_ONLY_KEYS if k in match]
    # a subtree rule that names a DIRECTORY (by `name`, or by a path_glob that does not end in /**) is a directory rule: it claims that directory and everything below it
    named_dir = raw["grain"] == "subtree" and "path_segment" not in match and (
        ("name" in match and "path_glob" not in match) or ("path_glob" in match and not any(str(g).endswith("/**") for g in _as_list(match["path_glob"]))))
    dir_rule = bool(dir_keys) or raw["grain"] == "component" or named_dir
    scope = match.get("component_scope", "")
    if scope and scope not in COMPONENT_SCOPES:
        raise ProfileError(f"{where}: component_scope {scope!r} is not one of {list(COMPONENT_SCOPES)}")
    if scope and dir_rule:
        raise ProfileError(f"{where}: component_scope applies to a FILE rule; this rule tests a directory")
    if dir_rule and file_keys:
        raise ProfileError(f"{where}: a directory rule ({dir_keys or 'grain component'}) cannot test {file_keys} (a file-name test)")
    for flag in ("no_source_files", "orphaned"):
        if flag in match and match[flag] is not True:
            raise ProfileError(f"{where}: match.{flag} must be true")
    for c in _as_list(match.get("has_child_dir", [])):
        if not isinstance(c, str) or not c or c.startswith("/") or c.endswith("/") or any(x in ("", "..", ".") for x in c.split("/")):
            raise ProfileError(f"{where}: match.has_child_dir needs relative folder paths like 'classes' or 'docs/javadoc', got {c!r}")
    for key in ("name", "extension", "path_segment", "path_glob", "name_regex", "has_file", "parent_has_file", "has_entry", "ancestor_has_entry", "parent_name_token"):
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
    seg_res = []
    for rx in _as_list(match.get("segment_regex", [])):
        if not isinstance(rx, str) or not rx:
            raise ProfileError(f"{where}: match.segment_regex needs non-empty regexes")
        try:
            seg_res.append(re.compile(rx))
        except re.error as exc:
            raise ProfileError(f"{where}: bad segment_regex {rx!r}: {exc}") from exc
    child_parents, child_res = frozenset(), []
    if "child_segment_regex" in match:
        cs = match["child_segment_regex"]
        if not isinstance(cs, dict) or set(cs) != {"parent", "regex"} or not _as_list(cs["parent"]) or not _as_list(cs["regex"]) \
                or not all(isinstance(x, str) and x and "/" not in x for x in _as_list(cs["parent"])):
            raise ProfileError(f"{where}: match.child_segment_regex needs a mapping with parent (exact folder names, no '/') and regex (non-empty regexes)")
        child_parents = frozenset(_as_list(cs["parent"]))
        for rx in _as_list(cs["regex"]):
            if not isinstance(rx, str) or not rx:
                raise ProfileError(f"{where}: match.child_segment_regex needs non-empty regexes")
            try:
                child_res.append(re.compile(rx))
            except re.error as exc:
                raise ProfileError(f"{where}: bad child_segment_regex {rx!r}: {exc}") from exc
    group_files, group_min, group_seg_res = frozenset(), 0, []
    for key in ("groups_projects", "group_segment_regex"):
        if key in match:
            g = match[key]
            if not isinstance(g, dict) or set(g) - {"min", "files", "regex"} or not isinstance(g.get("min"), int) or isinstance(g.get("min"), bool) or g["min"] < 2 \
                    or not g.get("files") or not all(isinstance(x, str) and x for x in _as_list(g["files"])):
                raise ProfileError(f"{where}: match.{key} needs a mapping with min (an integer of 2 or more: 'more than one project') and files (the manifest names of a project)"
                                   + (" and regex" if key == "group_segment_regex" else ""))
            if (key == "group_segment_regex") != ("regex" in g):
                raise ProfileError(f"{where}: match.{key}: regex belongs to group_segment_regex only")
            if group_min and (group_min != g["min"] or group_files != frozenset(_as_list(g["files"]))):
                raise ProfileError(f"{where}: groups_projects and group_segment_regex of one rule must use the same min and files")
            group_min, group_files = g["min"], frozenset(_as_list(g["files"]))
            for rx in (_as_list(g["regex"]) if key == "group_segment_regex" else []):
                try:
                    group_seg_res.append(re.compile(rx))
                except (re.error, TypeError) as exc:
                    raise ProfileError(f"{where}: bad group_segment_regex {rx!r}: {exc}") from exc
    content_files, content_min, content_exts = frozenset(), 0, ()
    if "min_content" in match:
        mc = match["min_content"]
        if not isinstance(mc, dict) or set(mc) != {"files", "min_files", "extensions"} or not isinstance(mc["min_files"], int) or isinstance(mc["min_files"], bool) or mc["min_files"] < 1 \
                or not _as_list(mc["files"]) or not all(isinstance(x, str) and x and "/" not in x for x in _as_list(mc["files"])) \
                or not _as_list(mc["extensions"]) or not all(isinstance(x, str) and len(x) > 1 and x.startswith(".") and "/" not in x for x in _as_list(mc["extensions"])):
            raise ProfileError(f"{where}: match.min_content needs a mapping with files (configuration file names, no '/'), min_files (an integer of 1 or more) and extensions ('.md', ...)")
        content_files, content_min, content_exts = frozenset(_as_list(mc["files"])), mc["min_files"], tuple(_as_list(mc["extensions"]))
    only_dirs, only_res = frozenset(), []
    if "only_files" in match:
        of = match["only_files"]
        if not isinstance(of, dict) or set(of) != {"child_dirs", "names"} or not isinstance(of["child_dirs"], list) or not isinstance(of["names"], list) \
                or not (of["child_dirs"] or of["names"]) or not all(isinstance(x, str) and x and "/" not in x for x in of["child_dirs"] + of["names"]):
            raise ProfileError(f"{where}: match.only_files needs a mapping with child_dirs (folder names) and names (file-name globs), lists of strings without '/', not both empty")
        only_dirs = frozenset(x.lower() for x in of["child_dirs"])
        for g in of["names"]:
            try:
                only_res.append(re.compile(glob_to_regex(g), re.IGNORECASE))
            except re.error as exc:
                raise ProfileError(f"{where}: bad only_files name glob {g!r}: {exc}") from exc
    file_scope = raw.get("file_scope", False)
    if not isinstance(file_scope, bool) or (file_scope and (not dir_rule or raw["grain"] != "dir" or role == "component")):
        raise ProfileError(f"{where}: file_scope is a boolean, and true only on a directory rule of grain dir whose role is not component")
    parent_not = _as_list(match.get("parent_not_role", []))
    if "parent_not_role" in match and (not parent_not or not all(isinstance(x, str) and x in roles for x in parent_not)):
        raise ProfileError(f"{where}: match.parent_not_role needs role names the profile knows")
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
        segment_res=tuple(seg_res), child_dirs=frozenset(_as_list(match.get("has_child_dir", []))), orphaned=bool(match.get("orphaned", False)),
        no_source=bool(match.get("no_source_files", False)), parent_tokens=frozenset(t.lower() for t in _as_list(match.get("parent_name_token", []))),
        scope=scope, named_dir=named_dir, group_files=group_files, group_min=group_min, group_seg_res=tuple(group_seg_res),
        child_seg_parents=child_parents, child_seg_res=tuple(child_res),
        content_files=content_files, content_min=content_min, content_exts=content_exts, file_scope=file_scope,
        parent_not_roles=frozenset(parent_not), only_dirs=only_dirs, only_res=tuple(only_res), only_files="only_files" in match,
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
    if "translation_rule" in doc and "mkdocs" not in readers:
        raise ProfileError(f"{w}: translation_rule needs the mkdocs reader")
    if "included_build_rule" in doc and "gradle" not in readers:
        raise ProfileError(f"{w}: included_build_rule needs the gradle reader")
    for which in (x for x in MANIFEST_RULE_NAMES if x not in OPTIONAL_MANIFEST_RULES):
        if (which in doc) != (which in need):
            raise ProfileError(f"{w}: {which} is {'required' if which in need else 'not allowed'} for readers {list(readers)}")
    rules = {}
    for which in (x for x in MANIFEST_RULE_NAMES if x in doc):
        raw = doc[which]
        _check_keys(f"{w} {which}", raw, MANIFEST_RULE_KEYS + ("tuned_on",), MANIFEST_RULE_KEYS)
        if raw["role"] not in roles:
            raise ProfileError(f"{w} {which}: unknown role {raw['role']!r}; allowed {list(roles)}")
        if which in ("member_rule", "section_rule", "fallback_section_rule", "translation_rule") and raw["role"] != "component":
            raise ProfileError(f"{w} {which}: the role must be 'component'")
        if which == "aggregator_rule" and raw["role"] == "component":
            raise ProfileError(f"{w} aggregator_rule: an aggregator is NOT a component")
        if which == "included_build_rule" and raw["role"] == "component":
            raise ProfileError(f"{w} included_build_rule: an included build is internal tooling, NOT a component")
        rel = rel_map.get(raw["role"])
        if rel is None:
            raise ProfileError(f"{w} {which}: role {raw['role']!r} has no relevance")
        _not_conformance_kind(f"{w} {which}", raw["kind"])
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
        rules[which] = Rule(id=raw["id"], match={}, role=raw["role"], relevance=rel, kind=raw["kind"], grain="dir" if which in ("aggregator_rule", "included_build_rule") else "component",
                            basis=raw["basis"], confidence=raw["confidence"], evidence=raw["evidence"].strip(), origin=origin, tuned_on=tuple(tuned))
    ids = [r.id for r in rules.values()]
    if len(set(ids)) != len(ids):
        raise ProfileError(f"{w}: the manifest rules need different ids")
    if ("submodule_rule" in doc) != ("gitmodules" in readers):
        raise ProfileError(f"{w}: submodule_rule is needed exactly when the gitmodules reader is enabled")
    for key in ("docs_content_rule", "site_output_rule", "fallback_site_rule", "submodule_rule"):
        if key in doc and (not isinstance(doc[key], str) or not RULE_ID.match(doc[key]) or (key != "submodule_rule" and "mkdocs" not in readers)):
            raise ProfileError(f"{w}: {key} must name a rule id and needs the mkdocs reader")
    return ManifestReading(readers=tuple(readers), docs_content_rule=doc.get("docs_content_rule"), site_output_rule=doc.get("site_output_rule"),
                           fallback_site_rule=doc.get("fallback_site_rule"), submodule_rule=doc.get("submodule_rule"),
                           **{k: rules.get(k) for k in MANIFEST_RULE_NAMES}, **caps)


def _merge_reading(own, base):
    """Two manifest_reading blocks (the child's and an extended profile's) combine: the readers are the union (child's first), each rule or rule id is the
    child's where it has one, and every cap is the TIGHTER of the two. The child's block alone, or the base's alone, is returned unchanged."""
    if own is None or base is None:
        return own if own is not None else base
    from dataclasses import replace
    readers = tuple(dict.fromkeys(own.readers + base.readers))
    kw = {k: (getattr(own, k) if getattr(own, k) is not None else getattr(base, k)) for k in MANIFEST_RULE_NAMES + ("docs_content_rule", "site_output_rule", "fallback_site_rule", "submodule_rule")}
    return replace(own, readers=readers, max_file_bytes=min(own.max_file_bytes, base.max_file_bytes), max_blobs=min(own.max_blobs, base.max_blobs),
                   max_total_bytes=min(own.max_total_bytes, base.max_total_bytes), **kw)


def _grammar(source: str, key: str, items: Any, origin: str) -> tuple:
    """Compile one of the conformance lists (path_grammar, name_grammar, required, allowed_only); see recognizer/grammar.py."""
    if items is None or items == []:
        return ()
    gm = _gm()
    if not isinstance(items, list):
        raise ProfileError(f"{source} {key}: expected a list")
    make = {"path_grammar": gm.compile_path_grammar, "name_grammar": gm.compile_name_grammar, "required": gm.compile_required,
            "content_checks": gm.compile_content_check, "states": gm.compile_state}.get(key)
    out = []
    for n, item in enumerate(items):
        try:
            if make is None:
                out.append(gm.compile_allowed_only(f"{source} {key}[{n}]", item, origin, BASES, CONFIDENCES, RULE_ID, glob_to_regex))
            else:
                out.append(make(f"{source} {key}[{n}]", item, origin, BASES, CONFIDENCES, RULE_ID))
        except gm.GrammarError as exc:
            raise ProfileError(str(exc)) from exc
    return tuple(out)


GRAMMAR_LISTS = ("path_grammar", "name_grammar", "required", "allowed_only", "content_checks", "states")


def _gm():
    try:
        from . import grammar
    except ImportError:                                  # run as a script (recognizer/ on sys.path)
        import grammar  # type: ignore
    return grammar


def _structural(where: str, items: Any) -> tuple:
    if items is None:
        return ()
    if not isinstance(items, list):
        raise ProfileError(f"{where}: structural_rules must be a list")
    out = []
    for n, item in enumerate(items):
        w = f"{where} structural_rules[{n}]"
        _check_keys(w, item, STRUCTURAL_KEYS + STRUCTURAL_OPTIONAL, STRUCTURAL_KEYS)
        if item["op"] not in STRUCTURAL_OPS:
            raise ProfileError(f"{w}: op {item['op']!r} is not one of {list(STRUCTURAL_OPS)}")
        least = 2 if item["op"] == "sibling-manifests-top-level" else 1
        if not isinstance(item["min"], int) or isinstance(item["min"], bool) or item["min"] < least:
            raise ProfileError(f"{w}: min must be an integer of at least {least}")
        if item["op"] != "sibling-manifests-top-level":                     # the ops that CLAIM a directory as a component say what kind it is
            if not isinstance(item.get("kind"), str) or not item["kind"].strip():
                raise ProfileError(f"{w}: op {item['op']!r} needs a kind")
        elif "kind" in item:
            raise ProfileError(f"{w}: op 'sibling-manifests-top-level' takes no kind")
        _not_conformance_kind(w, item.get("kind"))
        if item["op"] == "mostly-extension-folder":
            exts = item.get("extensions")
            share = item.get("share")
            if not isinstance(exts, list) or not exts or not all(isinstance(x, str) and x.startswith(".") for x in exts):
                raise ProfileError(f"{w}: op 'mostly-extension-folder' needs extensions, a list of endings like '.md'")
            if not isinstance(share, (int, float)) or isinstance(share, bool) or not 0.5 <= share <= 1:
                raise ProfileError(f"{w}: share must be a number from 0.5 to 1")
        elif "extensions" in item or "share" in item or "no_code" in item:
            raise ProfileError(f"{w}: extensions, share and no_code belong to op 'mostly-extension-folder'")
        if "no_code" in item and item["no_code"] is not True:
            raise ProfileError(f"{w}: no_code must be true")
        if item["op"] == "compose-deployment":
            rx = item.get("name_regex", [])
            if not isinstance(rx, list) or not all(isinstance(x, str) and x for x in rx):
                raise ProfileError(f"{w}: name_regex must be a list of regexes")
            for x in rx:
                try:
                    re.compile(x)
                except re.error as exc:
                    raise ProfileError(f"{w}: bad name_regex {x!r}: {exc}") from exc
            if "yaml_key" in item and (not isinstance(item["yaml_key"], str) or not item["yaml_key"]):
                raise ProfileError(f"{w}: yaml_key must be a key name")
        elif "name_regex" in item or "yaml_key" in item:
            raise ProfileError(f"{w}: name_regex and yaml_key belong to op 'compose-deployment'")
        for key, allowed in (("basis", BASES), ("confidence", CONFIDENCES)):
            if item[key] not in allowed:
                raise ProfileError(f"{w}: {key} {item[key]!r} is not one of {list(allowed)}")
        if not isinstance(item["evidence"], str) or not item["evidence"].strip():
            raise ProfileError(f"{w}: evidence must be a non-empty string")
        if not isinstance(item["id"], str) or not RULE_ID.match(item["id"]):
            raise ProfileError(f"{w}: id must be a simple identifier")
        out.append({**item, "evidence": item["evidence"].strip(), "tuned_on": list(item.get("tuned_on", []))})
    return tuple(out)


def parse_profile(doc: Any, source: str = "<profile>", profiles_dir: Path | None = None, _stack: tuple = (), _composite: bool = False) -> Profile:
    """Validate a parsed YAML document and return the composed Profile (its `extends` resolved from `profiles_dir`)."""
    _check_keys(source, doc, TOP_KEYS, ("profile_id", "version", "status", "applies_to", "roles", "relevance", "rules"))
    pid = doc["profile_id"]
    if not isinstance(pid, str) or not (SLUG.match(pid) or (_composite and COMPOSITE_ID.match(pid))):
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
    gram_own = {k: _grammar(source, k, doc.get(k), pid) for k in GRAMMAR_LISTS}
    gram = {k: list(v) for k, v in gram_own.items()}
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
        mreading = _merge_reading(mreading, base.manifest_reading)
        structural.extend(base.structural)
        for k in GRAMMAR_LISTS:
            gram[k].extend(getattr(base, k))
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
        for key in ("docs_content_rule", "site_output_rule", "fallback_site_rule", "submodule_rule"):
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
    gram_ids = [x.id for k in GRAMMAR_LISTS for x in gram_own[k]]
    if len(set(gram_ids)) != len(gram_ids):
        raise ProfileError(f"{source}: grammar, required and allowed_only ids must be unique")
    for k in GRAMMAR_LISTS:                              # the same dedupe as for rules: a profile reached twice contributes once; a real clash is an error
        out, by = [], {}
        for x in gram[k]:
            if x.id in by:
                if by[x.id] == x.origin:
                    continue
                raise ProfileError(f"{source}: {k} id {x.id!r} is used twice (in {by[x.id]!r} and {x.origin!r})")
            by[x.id] = x.origin
            out.append(x)
        gram[k] = tuple(out)
    all_gram = [x.id for k in GRAMMAR_LISTS for x in gram[k]]
    if len(set(all_gram)) != len(all_gram) or set(all_gram) & (set(seen) | seen_s):
        raise ProfileError(f"{source}: grammar, required and allowed_only ids must be unique and differ from rule ids (a finding id is made from the id)")
    if any(gram[k] for k in GRAMMAR_LISTS):
        gm = _gm()
        try:
            gm.check_references(source, gram["path_grammar"], gram["name_grammar"], gram["required"], gram["allowed_only"], gram["states"])
            gm.check_content(source, gram["content_checks"])
        except gm.GrammarError as exc:
            raise ProfileError(str(exc)) from exc
    composed = list(dict.fromkeys(composed))
    return Profile(profile_id=pid, version=version, status=doc["status"], applies_to=doc["applies_to"], roles=tuple(all_roles),
                   relevance=merged_rel, rules=rules, file_roles=tuple(fr_out), manifest_reading=mreading, extends=tuple(extends), path_grammar=gram["path_grammar"], name_grammar=gram["name_grammar"],
                   required=gram["required"], allowed_only=gram["allowed_only"], content_checks=gram["content_checks"], states=gram["states"],
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


def compose_profiles(spec: str, profiles_dir: Path | str | None = None) -> Profile:
    """`a` loads one profile; `a,b,c` composes several in the order given: the FIRST-listed profile's rules are checked first, so it wins a conflict, a directory is
    claimed once, and a profile that two of them extend (generic-relevance) is loaded once. The composite is named `a+b+c` (its parts and versions are in `composed_of`)."""
    ids = [x.strip() for x in str(spec).split(",") if x.strip()]
    if not ids:
        raise ProfileError("no profile named")
    if len(set(ids)) != len(ids):
        raise ProfileError(f"a profile is listed twice in {spec!r}")
    if len(ids) == 1:
        return load_profile(ids[0], profiles_dir)
    if profiles_dir is None:
        raise ProfileError("composing profiles needs a profiles directory")
    doc = {"profile_id": "+".join(ids), "version": "0.0.0", "status": "proposed", "applies_to": "any", "roles": ["component"],
           "relevance": {"primary": ["component"], "supporting": [], "hidden": []}, "extends": ids, "rules": []}
    return parse_profile(doc, f"<composition {spec}>", Path(profiles_dir), (), _composite=True)
