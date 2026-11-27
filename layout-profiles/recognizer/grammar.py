"""Path and name grammars, required paths and closed sets (Phase 2, notebook 05, B1): CONFORMANCE of a tree to a profile, by names only.

A profile may declare four lists (all empty in every Phase 1 profile, which therefore behave exactly as before):

  path_grammar   directory patterns with named tokens:  {id, pattern: "sub-{sub}/ses-{ses}", tokens: {sub: {regex: "[a-zA-Z0-9]+"}, ...}, yields?}
                 a token is {regex: R} (a full match of R) or {values: [a, b]} (one of these, exactly).
  name_grammar   an entity grammar for FILE names: ordered entity keys (key-label pairs joined by `_`), a label pattern, a suffix list and an
                 extension list:  <key>-<label>[_<key>-<label>...]_<suffix><extension>
  required       paths that must exist: a literal `path`, or every path of a path_grammar pattern (`of`) for each value of the `for_each` tokens
                 seen in the tree, with the other tokens taken from the combinations seen (cardinality per parent token).
  allowed_only   a closed set below a directory (`under`: "." for the root, or path_grammar ids): the sub-directories it allows (path_grammar ids),
                 the files (exact names and name_grammar ids), and the names declared `not_checked` (globs; counted, never judged).

Every entry of a directory that an allowed_only item covers is judged once:
  * it matches an allowed pattern or name exactly: conformant (a directory takes the pattern's type and tokens, and is looked into);
  * it matches a `not_checked` glob: not checked (counted, with everything below it);
  * it has the SHAPE of an allowed pattern (the pattern with literals compared ignoring case and any text for a regex token; a value token
    compared ignoring case; for a file, an entity key or a suffix of the grammar among its `_` parts; or an allowed exact name ignoring case):
    `naming`/`misnamed`, rule = that pattern, grammar or allowed_only item;
  * otherwise `structure`/`unexpected`, rule = the first allowed_only item that covers the directory.
Nothing below a misnamed or unexpected directory is judged (no cascade). A `required` path that is absent is `structure`/`missing` and its
finding's path is the EXPECTED path; it is not reported when its parent folder is absent too (the shallowest absence is the one reported) or when
a sibling that differs from it only in case was reported misnamed (that is the same deviation).

Only PyYAML-free standard library code; nothing here opens a file.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

FINDING_KINDS = ("structure", "naming", "content-type")
FINDING_STATUSES = {"structure": ("missing", "unexpected"), "naming": ("misnamed",), "content-type": ("missing-field", "invalid-value", "unreadable")}
CLAIM_KEYS = ("basis", "confidence", "evidence")
PG_KEYS = ("id", "pattern", "tokens") + CLAIM_KEYS
PG_OPTIONAL = ("yields", "tuned_on")
NG_KEYS = ("id", "entities", "label", "suffixes", "extensions") + CLAIM_KEYS
NG_OPTIONAL = ("tuned_on",)
ENTITY_KEYS = ("key",)
ENTITY_OPTIONAL = ("label", "token", "required_for")
RQ_KEYS = ("id",) + CLAIM_KEYS
RQ_OPTIONAL = ("path", "of", "for_each", "category", "tuned_on")
CATEGORIES = ("standard", "study-consistency")   # a required path the standard asks for, or one a study's own protocol makes regular (B2)
AO_KEYS = ("id", "under") + CLAIM_KEYS
AO_OPTIONAL = ("dirs", "files", "name_grammar", "not_checked", "tuned_on")
_TOKEN = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")
_KEY = re.compile(r"^[A-Za-z0-9]+$")


class GrammarError(ValueError):
    """A grammar, required or allowed_only item is not valid (the loader turns this into a ProfileError naming the file)."""


def _keys(where, obj, required, optional=()):
    if not isinstance(obj, dict):
        raise GrammarError(f"{where}: expected a mapping, got {type(obj).__name__}")
    unknown = sorted(set(obj) - set(required) - set(optional))
    if unknown:
        raise GrammarError(f"{where}: unknown key(s) {unknown}; allowed {list(required) + list(optional)}")
    missing = [k for k in required if k not in obj]
    if missing:
        raise GrammarError(f"{where}: missing required key(s) {missing}")


def _str_list(where, v, what="strings"):
    if not isinstance(v, list) or not v or not all(isinstance(x, str) and x for x in v) or len(set(v)) != len(v):
        raise GrammarError(f"{where}: needs a non-empty list of distinct {what}")
    return list(v)


def _regex(where, rx):
    if not isinstance(rx, str) or not rx:
        raise GrammarError(f"{where}: needs a regex")
    try:
        return re.compile(rx)
    except re.error as exc:
        raise GrammarError(f"{where}: bad regex {rx!r}: {exc}") from exc


@dataclass(frozen=True)
class Claim:
    id: str
    basis: str
    confidence: str
    evidence: str
    origin: str
    tuned_on: tuple = ()


@dataclass(frozen=True)
class PathPattern(Claim):
    pattern: str = ""
    yields: str | None = None
    token_names: tuple = ()
    segs: tuple = ()                         # per segment: (strict regex, loose regex, literal-only text or None)

    def match(self, path: str):
        """The tokens of `path` when it matches the pattern exactly, else None."""
        parts = path.split("/") if path else []
        if len(parts) != len(self.segs):
            return None
        caps: dict = {}
        for part, (strict, _, _) in zip(parts, self.segs):
            m = strict.fullmatch(part)
            if m is None:
                return None
            caps.update(m.groupdict())
        return caps

    def shaped(self, path: str) -> bool:
        """Does `path` match every segment but the last exactly, and the last by SHAPE (literals ignoring case, any text for a regex token)?"""
        parts = path.split("/") if path else []
        if len(parts) != len(self.segs):
            return False
        for part, (strict, _, _) in zip(parts[:-1], self.segs[:-1]):
            if strict.fullmatch(part) is None:
                return False
        return self.segs[-1][1].fullmatch(parts[-1]) is not None

    def render(self, caps: dict) -> str:
        return _TOKEN.sub(lambda m: caps[m.group(1)], self.pattern)


@dataclass(frozen=True)
class NameGrammar(Claim):
    entities: tuple = ()                     # (key, label regex, token | None, required_for suffixes)
    suffix_token: str | None = None          # the suffix list depends on this directory token (datatype), or None for one list
    suffixes: dict = field(default_factory=dict)    # token value (or '' for the plain list) -> tuple of suffixes
    ext_default: tuple = ()
    ext_by_suffix: dict = field(default_factory=dict)

    def _all_ext(self):
        return sorted(set(self.ext_default) | {e for v in self.ext_by_suffix.values() for e in v}, key=lambda e: (-len(e), e))

    def _split(self, name: str):
        ext = next((e for e in self._all_ext() if name.endswith(e) and len(name) > len(e)), None)
        stem = name[:-len(ext)] if ext else name.split(".", 1)[0]
        return stem, ext

    def check(self, name: str, caps: dict):
        """'' when `name` is in the grammar for a directory with tokens `caps`, else the first reason it is not (a short word)."""
        stem, ext = self._split(name)
        if ext is None:
            return "extension"
        parts = stem.split("_")
        if len(parts) < 2:
            return "no-entity"
        suffix, pairs = parts[-1], parts[:-1]
        keys = [e[0] for e in self.entities]
        lower = {k.lower(): k for k in keys}
        seen, last = {}, -1
        for pair in pairs:
            key, dash, label = pair.partition("-")
            if not dash or not key:
                return "not-an-entity"
            if key not in keys:
                return "case" if key.lower() in lower else "unknown-entity"
            i = keys.index(key)
            if key in seen:
                return "duplicate-entity"
            if i < last:
                return "entity-order"
            if self.entities[i][1].fullmatch(label) is None:
                return "label"
            seen[key], last = label, i
        allowed = self.suffixes.get(caps.get(self.suffix_token) if self.suffix_token else "", ())
        if suffix not in allowed:
            return "case" if suffix.lower() in {s.lower() for s in allowed} else "suffix"
        for key, _, token, req_for in self.entities:
            if token is not None:
                if token in caps and caps[token] is not None:
                    if seen.get(key) != caps[token]:
                        return "entity-differs-from-folder" if key in seen else "missing-entity"
                elif key in seen:
                    return "entity-without-folder"
            if req_for and suffix in req_for and key not in seen:
                return "missing-entity"
        if ext not in self.ext_by_suffix.get(suffix, self.ext_default):
            return "extension"
        return ""

    def shaped(self, name: str) -> bool:
        """Does `name` look like it means to follow the grammar: an entity key of the grammar (any case) or one of its suffixes (any case) among its parts?"""
        stem, _ = self._split(name)
        parts = stem.split("_")
        keys = {e[0].lower() for e in self.entities}
        sufs = {s.lower() for v in self.suffixes.values() for s in v}
        return any(p.partition("-")[0].lower() in keys and "-" in p for p in parts) or (len(parts) > 1 and parts[-1].lower() in sufs)


@dataclass(frozen=True)
class Required(Claim):
    path: str | None = None
    of: str | None = None
    for_each: tuple = ()
    category: str = "standard"


@dataclass(frozen=True)
class AllowedOnly(Claim):
    under: tuple = ()
    dirs: tuple = ()
    files: tuple = ()
    name_grammar: tuple = ()
    not_checked: tuple = ()
    not_checked_res: tuple = ()


def _claim(where, raw, origin, bases, confidences):
    for key, allowed in (("basis", bases), ("confidence", confidences)):
        if raw[key] not in allowed:
            raise GrammarError(f"{where}: {key} {raw[key]!r} is not one of {list(allowed)}")
    if not isinstance(raw["evidence"], str) or not raw["evidence"].strip():
        raise GrammarError(f"{where}: evidence must be a non-empty string")
    tuned = raw.get("tuned_on", [])
    if not isinstance(tuned, list) or not all(isinstance(x, str) and x for x in tuned):
        raise GrammarError(f"{where}: tuned_on must be a list of names")
    return dict(id=raw["id"], basis=raw["basis"], confidence=raw["confidence"], evidence=raw["evidence"].strip(), origin=origin, tuned_on=tuple(tuned))


def _id(where, raw, rule_id_re):
    if not isinstance(raw.get("id"), str) or not rule_id_re.match(raw["id"]):
        raise GrammarError(f"{where}: id must be a simple identifier")


def compile_path_grammar(where, raw, origin, bases, confidences, rule_id_re) -> PathPattern:
    _keys(where, raw, PG_KEYS, PG_OPTIONAL)
    _id(where, raw, rule_id_re)
    where = f"{where} {raw['id']!r}"
    pat = raw["pattern"]
    if not isinstance(pat, str) or not pat or pat.startswith("/") or pat.endswith("/") or any(s in ("", ".", "..") for s in pat.split("/")):
        raise GrammarError(f"{where}: pattern must be a relative path of directory segments, like 'sub-{{sub}}/ses-{{ses}}'")
    tokens = raw["tokens"]
    if not isinstance(tokens, dict):
        raise GrammarError(f"{where}: tokens must be a mapping (token -> {{regex: R}} or {{values: [..]}}); use {{}} for none")
    used = _TOKEN.findall(pat)
    if len(set(used)) != len(used):
        raise GrammarError(f"{where}: a token is used twice in the pattern")
    if set(used) != set(tokens):
        raise GrammarError(f"{where}: the pattern's tokens {sorted(used)} and the defined tokens {sorted(tokens)} differ")
    if "{" in _TOKEN.sub("", pat) or "}" in _TOKEN.sub("", pat):
        raise GrammarError(f"{where}: a brace that is not a {{token}}")
    defs = {}
    for t, d in tokens.items():
        w = f"{where} token {t!r}"
        if not isinstance(d, dict) or len(d) != 1 or next(iter(d)) not in ("regex", "values"):
            raise GrammarError(f"{w}: exactly one of regex or values")
        if "regex" in d:
            _regex(w, d["regex"])
            defs[t] = ("regex", d["regex"])
        else:
            vals = _str_list(w, d["values"], "values")
            if any("/" in v for v in vals):
                raise GrammarError(f"{w}: a value cannot hold '/'")
            defs[t] = ("values", vals)
    segs = []
    for seg in pat.split("/"):
        strict, loose, pos = [], [], 0
        for m in _TOKEN.finditer(seg):
            lit = re.escape(seg[pos:m.start()])
            strict.append(lit)
            loose.append(lit)
            kind, val = defs[m.group(1)]
            if kind == "regex":
                strict.append(f"(?P<{m.group(1)}>(?:{val}))")
                loose.append(".+")
            else:
                alt = "|".join(re.escape(v) for v in sorted(val, key=lambda v: (-len(v), v)))
                strict.append(f"(?P<{m.group(1)}>{alt})")
                loose.append(f"(?:{alt})")
            pos = m.end()
        strict.append(re.escape(seg[pos:]))
        loose.append(re.escape(seg[pos:]))
        try:
            segs.append((re.compile("".join(strict)), re.compile("".join(loose), re.IGNORECASE), None if _TOKEN.search(seg) else seg))
        except re.error as exc:
            raise GrammarError(f"{where}: the pattern does not compile: {exc}") from exc
    y = raw.get("yields")
    if y is not None and (not isinstance(y, str) or not y):
        raise GrammarError(f"{where}: yields must be a name")
    return PathPattern(**_claim(where, raw, origin, bases, confidences), pattern=pat, yields=y, token_names=tuple(used), segs=tuple(segs))


def compile_name_grammar(where, raw, origin, bases, confidences, rule_id_re) -> NameGrammar:
    _keys(where, raw, NG_KEYS, NG_OPTIONAL)
    _id(where, raw, rule_id_re)
    where = f"{where} {raw['id']!r}"
    default_label = raw["label"]
    _regex(f"{where} label", default_label)
    ents = raw["entities"]
    if not isinstance(ents, list) or not ents:
        raise GrammarError(f"{where}: entities must be a non-empty, ordered list")
    out, keys = [], []
    for n, e in enumerate(ents):
        w = f"{where} entities[{n}]"
        _keys(w, e, ENTITY_KEYS, ENTITY_OPTIONAL)
        if not isinstance(e["key"], str) or not _KEY.match(e["key"]):
            raise GrammarError(f"{w}: key must be letters and digits")
        if e["key"] in keys:
            raise GrammarError(f"{w}: key {e['key']!r} is listed twice")
        keys.append(e["key"])
        tok = e.get("token")
        if tok is not None and (not isinstance(tok, str) or not tok):
            raise GrammarError(f"{w}: token must name a path_grammar token")
        req = tuple(_str_list(f"{w} required_for", e["required_for"], "suffixes")) if "required_for" in e else ()
        out.append((e["key"], _regex(f"{w} label", e.get("label", default_label)), tok, req))
    sx = raw["suffixes"]
    if isinstance(sx, list):
        suffix_token, suffixes = None, {"": tuple(_str_list(f"{where} suffixes", sx, "suffixes"))}
    else:
        _keys(f"{where} suffixes", sx, ("by_token", "values"))
        if not isinstance(sx["by_token"], str) or not sx["by_token"] or not isinstance(sx["values"], dict) or not sx["values"]:
            raise GrammarError(f"{where} suffixes: by_token names a token and values maps each token value to a list of suffixes")
        suffix_token = sx["by_token"]
        suffixes = {str(k): tuple(_str_list(f"{where} suffixes.values.{k}", v, "suffixes")) for k, v in sx["values"].items()}
    for v in suffixes.values():
        for s in v:
            if not _KEY.match(s):
                raise GrammarError(f"{where}: suffix {s!r} must be letters and digits")
    ex = raw["extensions"]
    if isinstance(ex, list):
        ext_default, ext_by = tuple(_str_list(f"{where} extensions", ex, "extensions")), {}
    else:
        _keys(f"{where} extensions", ex, ("default", "by_suffix"))
        ext_default = tuple(_str_list(f"{where} extensions.default", ex["default"], "extensions"))
        if not isinstance(ex["by_suffix"], dict):
            raise GrammarError(f"{where} extensions.by_suffix: a mapping suffix -> extensions")
        all_sx = {s for v in suffixes.values() for s in v}
        ext_by = {}
        for k, v in ex["by_suffix"].items():
            if k not in all_sx:
                raise GrammarError(f"{where} extensions.by_suffix: {k!r} is not one of the suffixes")
            ext_by[k] = tuple(_str_list(f"{where} extensions.by_suffix.{k}", v, "extensions"))
    for e in set(ext_default) | {x for v in ext_by.values() for x in v}:
        if not e.startswith(".") or "/" in e or "_" in e or len(e) < 2:
            raise GrammarError(f"{where}: extension {e!r} must start with '.' and hold no '/' or '_'")
    return NameGrammar(**_claim(where, raw, origin, bases, confidences), entities=tuple(out), suffix_token=suffix_token, suffixes=suffixes,
                       ext_default=ext_default, ext_by_suffix=ext_by)


def compile_required(where, raw, origin, bases, confidences, rule_id_re) -> Required:
    _keys(where, raw, RQ_KEYS, RQ_OPTIONAL)
    _id(where, raw, rule_id_re)
    where = f"{where} {raw['id']!r}"
    cat = raw.get("category", "standard")
    if cat not in CATEGORIES:
        raise GrammarError(f"{where}: category {cat!r} is not one of {list(CATEGORIES)}")
    if ("path" in raw) == ("of" in raw):
        raise GrammarError(f"{where}: exactly one of path (a literal path) or of (a path_grammar id, with for_each)")
    if "path" in raw:
        p = raw["path"]
        if "for_each" in raw:
            raise GrammarError(f"{where}: for_each belongs to of")
        if not isinstance(p, str) or not p or p.startswith("/") or p.endswith("/") or any(s in ("", ".", "..") for s in p.split("/")) or "{" in p:
            raise GrammarError(f"{where}: path must be a literal relative path")
        return Required(**_claim(where, raw, origin, bases, confidences), path=p, category=cat)
    if not isinstance(raw["of"], str) or not raw["of"]:
        raise GrammarError(f"{where}: of must name a path_grammar id")
    fe = tuple(_str_list(f"{where} for_each", raw.get("for_each"), "token names")) if "for_each" in raw else ()
    if not fe:
        raise GrammarError(f"{where}: of needs for_each (the tokens whose every value seen must have the path)")
    return Required(**_claim(where, raw, origin, bases, confidences), of=raw["of"], for_each=fe, category=cat)


def compile_allowed_only(where, raw, origin, bases, confidences, rule_id_re, glob_to_regex) -> AllowedOnly:
    _keys(where, raw, AO_KEYS, AO_OPTIONAL)
    _id(where, raw, rule_id_re)
    where = f"{where} {raw['id']!r}"
    under = tuple(_str_list(f"{where} under", raw["under"] if isinstance(raw["under"], list) else [raw["under"]], "'.' or path_grammar ids"))
    lists = {k: tuple(_str_list(f"{where} {k}", raw[k])) if k in raw else () for k in ("dirs", "files", "name_grammar", "not_checked")}
    if not (lists["dirs"] or lists["files"] or lists["name_grammar"]):
        raise GrammarError(f"{where}: allows nothing (name dirs, files or name_grammar)")
    for f in lists["files"] + lists["not_checked"]:
        if "/" in f:
            raise GrammarError(f"{where}: {f!r}: names and globs are of ONE entry, without '/'")
    res = tuple(re.compile(glob_to_regex(g)) for g in lists["not_checked"])
    return AllowedOnly(**_claim(where, raw, origin, bases, confidences), under=under, dirs=lists["dirs"], files=lists["files"],
                       name_grammar=lists["name_grammar"], not_checked=lists["not_checked"], not_checked_res=res)


def check_references(where, path_grammar, name_grammar, required, allowed_only) -> None:
    """Every id an item names must exist in the composed profile; a token named by for_each or by a name grammar's suffix list must be one the patterns define."""
    pg = {p.id: p for p in path_grammar}
    ng = {n.id for n in name_grammar}
    for r in required:
        if r.of is not None:
            if r.of not in pg:
                raise GrammarError(f"{where} required {r.id!r}: of names {r.of!r}, not a path_grammar id")
            missing = [t for t in r.for_each if t not in pg[r.of].token_names]
            if missing:
                raise GrammarError(f"{where} required {r.id!r}: for_each {missing} are not tokens of {r.of!r}")
    for a in allowed_only:
        for u in a.under:
            if u != "." and u not in pg:
                raise GrammarError(f"{where} allowed_only {a.id!r}: under {u!r} is neither '.' nor a path_grammar id")
        for d in a.dirs:
            if d not in pg:
                raise GrammarError(f"{where} allowed_only {a.id!r}: dirs names {d!r}, not a path_grammar id")
        for n in a.name_grammar:
            if n not in ng:
                raise GrammarError(f"{where} allowed_only {a.id!r}: name_grammar names {n!r}, not a name_grammar id")


# ---- evaluation ---------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class Result:
    findings: list = field(default_factory=list)          # dicts: path, kind, status, rule (the Claim), reason?
    checked_entries: int = 0
    checked_required: int = 0
    checked_by_category: dict = field(default_factory=dict)  # category -> checked items (entries are 'standard'; required paths by their category)
    not_checked_files: int = 0
    not_checked: list = field(default_factory=list)       # {path, reason, rule_id?, files}
    typed: dict = field(default_factory=dict)             # directory -> {path_grammar id: tokens}


def evaluate(paths, path_grammar, name_grammar, required, allowed_only) -> Result:
    """Judge a tree, given as its (non-hidden) file paths, against the grammars. Deterministic: entries are visited in sorted order."""
    pg = {p.id: p for p in path_grammar}
    ng = {n.id: n for n in name_grammar}
    kids: dict = {"": (set(), set())}
    below: dict = {}                                      # directory -> number of files at any depth below it
    files_set: set = set()
    for path in paths:
        files_set.add(path)
        parts = path.split("/")
        for i in range(len(parts) - 1):
            d = "/".join(parts[:i])
            kids.setdefault(d, (set(), set()))[0].add("/".join(parts[:i + 1]))
            kids.setdefault("/".join(parts[:i + 1]), (set(), set()))
        parent = "/".join(parts[:-1])
        kids.setdefault(parent, (set(), set()))[1].add(path)
        for i in range(len(parts)):
            d = "/".join(parts[:i])
            below[d] = below.get(d, 0) + 1
    res = Result()
    res.typed = {"": {".": {}}}
    misnamed_by_parent: dict = {}                         # (parent, rule id) -> lower-cased names reported misnamed
    queue = [""]
    while queue:
        d = queue.pop(0)
        scopes = res.typed[d]
        aos = [a for a in allowed_only if any(u in scopes for u in a.under)]
        sub_dirs, sub_files = kids.get(d, (set(), set()))
        if not aos:
            for c in sorted(sub_dirs):
                if c not in res.typed:
                    res.not_checked.append({"path": c, "reason": "no-closed-set", "files": below.get(c, 0)})
                    res.not_checked_files += below.get(c, 0)
            if sub_files:
                res.not_checked_files += len(sub_files)
                if d:
                    res.not_checked.append({"path": d, "reason": "no-closed-set-files", "files": len(sub_files)})
            continue
        caps: dict = {}
        for k in sorted(scopes):
            caps.update(scopes[k])
        allow_dirs = [x for a in aos for x in a.dirs]
        allow_files = {x: a for a in reversed(aos) for x in a.files}
        allow_ng = [x for a in aos for x in a.name_grammar]
        nc = [(a, rx) for a in aos for rx in a.not_checked_res]
        for c in sorted(sub_dirs | sub_files):
            is_dir = c in sub_dirs
            name = c.rpartition("/")[2]
            if is_dir:
                hit = {i: m for i in dict.fromkeys(allow_dirs) for m in [pg[i].match(c)] if m is not None}
                if hit:
                    res.checked_entries += 1
                    res.typed[c] = hit
                    queue.append(c)
                    continue
            elif name in allow_files or any(ng[i].check(name, caps) == "" for i in allow_ng):
                res.checked_entries += 1
                continue
            skip = next((a for a, rx in nc if rx.match(name)), None)
            if skip is not None:
                n = below.get(c, 0) if is_dir else 1
                res.not_checked.append({"path": c, "reason": "not-checked", "rule_id": skip.id, "files": n})
                res.not_checked_files += n
                continue
            res.checked_entries += 1
            finding = None
            if is_dir:
                shape = next((pg[i] for i in dict.fromkeys(allow_dirs) if pg[i].shaped(c)), None)
                if shape is not None:
                    finding = {"path": c, "kind": "naming", "status": "misnamed", "rule": shape, "reason": "pattern"}
            else:
                lit = next((x for x in allow_files if x.lower() == name.lower()), None)
                if lit is not None:
                    finding = {"path": c, "kind": "naming", "status": "misnamed", "rule": allow_files[lit], "reason": "case"}
                else:
                    g = next((ng[i] for i in dict.fromkeys(allow_ng) if ng[i].shaped(name)), None)
                    if g is not None:
                        finding = {"path": c, "kind": "naming", "status": "misnamed", "rule": g, "reason": g.check(name, caps)}
            if finding is None:
                finding = {"path": c, "kind": "structure", "status": "unexpected", "rule": aos[0]}
            else:
                misnamed_by_parent.setdefault((d, finding["rule"].id), set()).add(name.lower())
            res.findings.append(finding)
            if is_dir and below.get(c, 0):
                res.not_checked.append({"path": c, "reason": "below-finding", "files": below[c]})
                res.not_checked_files += below[c]

    dirs_present = set(kids)

    def same_as_misnamed(path, rule_ids):
        parent, _, name = path.rpartition("/")
        return any(name.lower() in misnamed_by_parent.get((parent, rid), ()) for rid in rule_ids)

    seen_missing: set = set()
    for r in required:
        if r.path is not None:
            expected = [(r.path, ())]
        else:
            p = pg[r.of]
            observed = [toks for dd, t in sorted(res.typed.items()) for pid, toks in t.items() if pid == r.of]
            others = [t for t in p.token_names if t not in r.for_each]
            shapes = sorted({tuple(o[t] for t in others) for o in observed})
            combos = sorted({tuple(t[k] for k in r.for_each) for dd, tt in res.typed.items() for t in tt.values() if all(k in t for k in r.for_each)})
            expected = []
            for combo in combos:
                for shape in shapes:
                    toks = dict(zip(r.for_each, combo)) | dict(zip(others, shape))
                    expected.append((p.render(toks), (p.id,)))
        for path, pids in expected:
            if path in files_set or path in dirs_present:
                res.checked_required += 1
                res.checked_by_category[r.category] = res.checked_by_category.get(r.category, 0) + 1
                continue
            parent = path.rpartition("/")[0]
            if parent and parent not in dirs_present:
                continue                                  # the parent is absent too: the shallowest absence is the one reported
            if same_as_misnamed(path, pids + tuple(a.id for a in allowed_only)):
                continue                                  # a sibling differing only in case was reported misnamed: the same deviation
            if path in seen_missing:
                continue
            seen_missing.add(path)
            res.checked_required += 1
            res.checked_by_category[r.category] = res.checked_by_category.get(r.category, 0) + 1
            res.findings.append({"path": path, "kind": "structure", "status": "missing", "rule": r})
    return res


# ---- content checks (B2; NOTE-PHASE2 §2 row and §10) ----------------------------------------------------------------------------------------------
# The ONLY file content conformance may read: a closed list of (file, fields), each tied to the one profile allowed to read it, read only at the
# scanned root (the dataset root the profile recognizes), under the manifest caps, by the safe JSON parser. Values longer than MAX_VALUE are not stored.
CONTENT_FILES = {"dataset_description.json": {"fields": ("BIDSVersion", "Name", "License"), "profile": "bids-dataset"}}
MAX_VALUE = 256
CT_KEYS = ("id", "file") + CLAIM_KEYS
CT_OPTIONAL = ("field", "check", "unreadable", "tuned_on")


@dataclass(frozen=True)
class ContentCheck(Claim):
    file: str = ""
    field: str | None = None                 # None for the file's `unreadable` item
    regex: object = None                     # compiled; the field must fully match it
    non_empty: bool = False                  # the field must not be empty (after stripping white space)

    def judge(self, value):
        """('', None) when the field passes, else (status, value to store or None)."""
        if not isinstance(value, str):
            return "missing-field", None
        if len(value) > MAX_VALUE:
            return "invalid-value", None
        if self.non_empty and not value.strip():
            return "invalid-value", value
        if self.regex is not None and self.regex.fullmatch(value) is None:
            return "invalid-value", value
        return "", None


def compile_content_check(where, raw, origin, bases, confidences, rule_id_re) -> ContentCheck:
    _keys(where, raw, CT_KEYS, CT_OPTIONAL)
    _id(where, raw, rule_id_re)
    where = f"{where} {raw['id']!r}"
    f = raw["file"]
    if f not in CONTENT_FILES:
        raise GrammarError(f"{where}: file {f!r} is not on the closed list of files whose content may be read ({sorted(CONTENT_FILES)})")
    if CONTENT_FILES[f]["profile"] != origin:
        raise GrammarError(f"{where}: {f} may be read only by the {CONTENT_FILES[f]['profile']!r} profile")
    if raw["basis"] != "manifest-content":
        raise GrammarError(f"{where}: a content check has basis manifest-content")
    claim = _claim(where, raw, origin, bases, confidences)
    if raw.get("unreadable") is not None:
        if raw["unreadable"] is not True or "field" in raw or "check" in raw:
            raise GrammarError(f"{where}: unreadable: true stands alone (no field, no check)")
        return ContentCheck(**claim, file=f)
    fld = raw.get("field")
    if fld not in CONTENT_FILES[f]["fields"]:
        raise GrammarError(f"{where}: field {fld!r} is not one of the fields that may be extracted from {f} ({list(CONTENT_FILES[f]['fields'])})")
    chk = raw.get("check")
    if not isinstance(chk, dict) or len(chk) != 1 or next(iter(chk)) not in ("regex", "non_empty"):
        raise GrammarError(f"{where}: check is {{regex: R}} or {{non_empty: true}}")
    if "regex" in chk:
        return ContentCheck(**claim, file=f, field=fld, regex=_regex(f"{where} check", chk["regex"]))
    if chk["non_empty"] is not True:
        raise GrammarError(f"{where}: non_empty must be true")
    return ContentCheck(**claim, file=f, field=fld, non_empty=True)


def check_content(where, items) -> None:
    """Each file with field checks has exactly one `unreadable` item, and each field is checked once."""
    for f in sorted({c.file for c in items}):
        mine = [c for c in items if c.file == f]
        if sum(1 for c in mine if c.field is None) != 1:
            raise GrammarError(f"{where} content_checks: {f} needs exactly one item with unreadable: true")
        fields = [c.field for c in mine if c.field is not None]
        if len(set(fields)) != len(fields):
            raise GrammarError(f"{where} content_checks: a field of {f} is checked twice")
