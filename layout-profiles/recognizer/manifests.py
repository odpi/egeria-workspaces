"""Manifest reading (Phase 1b, M6): what the recognizer may read INSIDE a short, closed list of manifest files, and how it reads it safely.

Principle: read only the files named in ALLOWED_FILES, extract only the named fields, read them from the git object database at the commit being
surveyed (never a working tree), never run anything and never fetch anything a manifest names. Everything else stays names and sizes only.
Lock files, .env files, data files, notebooks and anything inside a hidden subtree are never opened (the recognizer filters hidden paths BEFORE it
asks this module to read; the read log records every path actually opened, so a test can assert on it).

Safety: JSON by json.loads, TOML by tomllib, YAML by a SafeLoader that turns every unknown tag into null and refuses aliases, XML refused when it
carries a DOCTYPE or an ENTITY, Gradle by a regex over the string literals of `include` calls (never evaluated). A parse error never aborts a survey.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import signal
import subprocess
import threading
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

import yaml

try:
    import tomllib
except ImportError:                                                   # pragma: no cover (Python < 3.11)
    tomllib = None

# ---- the closed list --------------------------------------------------------------------------------------------------------------
READERS = ("package-json", "pnpm-workspace", "lerna", "cargo", "uv", "go-work", "maven", "gradle")
ALLOWED_FILES = {                                         # exact file name -> readers that may extract fields from it
    "package.json": ("package-json",), "pnpm-workspace.yaml": ("pnpm-workspace",), "lerna.json": ("lerna",), "Cargo.toml": ("cargo",),
    "pyproject.toml": ("uv",), "go.work": ("go-work",), "pom.xml": ("maven",), "settings.gradle": ("gradle",), "settings.gradle.kts": ("gradle",),
}
MEMBER_MANIFESTS = {                                      # a GLOB member must hold one of these files directly (the tools ignore directories without one)
    "package-json": {"package.json"}, "pnpm-workspace": {"package.json"}, "lerna": {"package.json"}, "cargo": {"Cargo.toml"}, "uv": {"pyproject.toml"},
    "go-work": set(), "maven": set(), "gradle": set(),
}
DEFAULT_MAX_FILE_BYTES = 256 * 1024
DEFAULT_MAX_BLOBS = 5000
DEFAULT_MAX_TOTAL_BYTES = 64 * 1024 * 1024
PARSE_SECONDS = 1.0
MAX_DEPTH = 50


class ManifestParseError(Exception):
    pass


# ---- sources ----------------------------------------------------------------------------------------------------------------------
class GitBlobSource:
    """Read blobs from the git object database: `git cat-file --batch` on `<rev>:<path>`. A dirty working tree cannot leak in."""

    def __init__(self, repo: str, rev: str):
        self.repo, self.rev = str(repo), rev
        self.proc = subprocess.Popen(["git", "-C", self.repo, "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.DEVNULL, env={**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull})

    def read(self, path: str, max_bytes: int):
        """Return (bytes | None, blob_sha | None, note): note is '' or 'missing' or 'size'. Oversize content is discarded, never returned."""
        self.proc.stdin.write(f"{self.rev}:{path}\n".encode("utf-8", "surrogateescape"))
        self.proc.stdin.flush()
        header = self.proc.stdout.readline().split()
        if len(header) != 3 or header[1] != b"blob":
            return None, None, "missing"
        sha, size = header[0].decode(), int(header[2])
        left, chunks = size, []
        keep = size <= max_bytes
        while left > 0:
            chunk = self.proc.stdout.read(min(left, 1 << 16))
            if not chunk:
                raise OSError("git cat-file ended early")
            left -= len(chunk)
            if keep:
                chunks.append(chunk)
        self.proc.stdout.read(1)                                        # the newline after the object
        return (b"".join(chunks), sha, "") if keep else (None, sha, "size")

    def close(self):
        try:
            self.proc.stdin.close()
            self.proc.wait(timeout=5)
        except Exception:                                               # pragma: no cover
            self.proc.kill()


class FileSource:
    """Read regular files below ROOT without following symlinks (for a non-git tree made by listpaths.py). The blob id is the git blob hash of the content."""

    def __init__(self, root: str):
        self.root = os.path.realpath(root)

    def read(self, path: str, max_bytes: int):
        full = os.path.join(self.root, path)
        try:
            if os.path.realpath(os.path.dirname(full)) != os.path.dirname(full):          # a symlink somewhere in the parents
                return None, None, "missing"
            fd = os.open(full, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        except OSError:
            return None, None, "missing"
        try:
            st = os.fstat(fd)
            if not os.path.isfile(full) or os.path.islink(full):
                return None, None, "missing"
            if st.st_size > max_bytes:
                return None, None, "size"
            data = os.read(fd, st.st_size + 1)
        finally:
            os.close(fd)
        return data, hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(), ""

    def close(self):
        pass


# ---- safe parsers -------------------------------------------------------------------------------------------------------------------
class _TimeLimit:
    """Wall-clock limit for one parse (SIGALRM, main thread of a Unix process only; elsewhere the size and depth caps are the limit)."""

    def __init__(self, seconds: float):
        self.seconds = seconds
        self.active = hasattr(signal, "setitimer") and threading.current_thread() is threading.main_thread()

    def __enter__(self):
        if self.active:
            self.old = signal.signal(signal.SIGALRM, self._raise)
            signal.setitimer(signal.ITIMER_REAL, self.seconds)

    def __exit__(self, *exc):
        if self.active:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, self.old)
        return False

    @staticmethod
    def _raise(signum, frame):
        raise ManifestParseError("time limit")


class _SafeLoader(yaml.SafeLoader):
    """Unknown tags (!ENV, !!python/name:...) become null; aliases and anchors are refused, so nothing is constructed or expanded."""

    def compose_node(self, parent, index):
        if self.check_event(yaml.events.AliasEvent):
            raise ManifestParseError("YAML alias refused")
        return super().compose_node(parent, index)


_SafeLoader.add_constructor(None, lambda loader, node: None)


def _depth_ok(obj, depth=0):
    if depth > MAX_DEPTH:
        return False
    if isinstance(obj, dict):
        return all(_depth_ok(v, depth + 1) for v in obj.values())
    if isinstance(obj, list):
        return all(_depth_ok(v, depth + 1) for v in obj)
    return True


def parse_json(data: bytes):
    try:
        with _TimeLimit(PARSE_SECONDS):
            obj = json.loads(data.decode("utf-8"))
    except ManifestParseError:
        raise
    except (ValueError, RecursionError) as exc:
        raise ManifestParseError(f"json: {type(exc).__name__}") from exc
    if not _depth_ok(obj):
        raise ManifestParseError("nesting too deep")
    return obj


def parse_toml(data: bytes):
    if tomllib is None:                                              # pragma: no cover
        raise ManifestParseError("toml: unavailable")
    try:
        with _TimeLimit(PARSE_SECONDS):
            obj = tomllib.loads(data.decode("utf-8"))
    except ManifestParseError:
        raise
    except (ValueError, RecursionError) as exc:
        raise ManifestParseError(f"toml: {type(exc).__name__}") from exc
    if not _depth_ok(obj):
        raise ManifestParseError("nesting too deep")
    return obj


def parse_yaml(data: bytes):
    try:
        with _TimeLimit(PARSE_SECONDS):
            obj = yaml.load(data.decode("utf-8"), Loader=_SafeLoader)          # noqa: S506 (a SafeLoader subclass that constructs only plain data)
    except ManifestParseError:
        raise
    except (yaml.YAMLError, ValueError, RecursionError) as exc:
        raise ManifestParseError(f"yaml: {type(exc).__name__}") from exc
    if not _depth_ok(obj):
        raise ManifestParseError("nesting too deep")
    return obj


_XML_FORBIDDEN = re.compile(rb"<!\s*(DOCTYPE|ENTITY)", re.IGNORECASE)


def parse_xml(data: bytes):
    if _XML_FORBIDDEN.search(data):
        raise ManifestParseError("xml: DOCTYPE or ENTITY refused")
    try:
        with _TimeLimit(PARSE_SECONDS):
            root = ET.fromstring(data)
    except ManifestParseError:
        raise
    except (ET.ParseError, ValueError, RecursionError) as exc:
        raise ManifestParseError(f"xml: {type(exc).__name__}") from exc
    for el in root.iter():                                           # drop namespaces so `{ns}modules` is `modules`
        el.tag = el.tag.rsplit("}", 1)[-1] if isinstance(el.tag, str) else el.tag
    return root


# ---- extractors: one declaration per manifest ---------------------------------------------------------------------------------------
@dataclass
class Decl:
    """What one manifest says. Strings only: names and member patterns, no other file text."""
    reader: str
    file: str                                   # repo-relative path of the manifest
    directory: str                              # its directory ('' = the repository root)
    field: str                                  # the field the members came from (workspaces, packages, members, modules, include, use)
    name: str | None = None
    members: list = field(default_factory=list)  # patterns relative to `directory`; a leading '!' is an exclusion
    excludes: list = field(default_factory=list)
    aggregator: bool = False                    # this directory only AGGREGATES its members (it is not itself a package)
    blob: str | None = None


def _strs(value) -> list:
    return [v for v in value if isinstance(v, str)] if isinstance(value, list) else []


def extract(reader: str, path: str, data: bytes) -> Decl | None:
    """Parse `data` (already size-capped) and return a Decl, or None when the file declares nothing of interest. Raises ManifestParseError."""
    directory = path.rpartition("/")[0]
    if reader == "package-json":
        doc = parse_json(data)
        if not isinstance(doc, dict):
            raise ManifestParseError("package.json is not an object")
        ws = doc.get("workspaces")
        members = _strs(ws.get("packages") if isinstance(ws, dict) else ws)
        name = doc.get("name") if isinstance(doc.get("name"), str) else None
        return Decl(reader, path, directory, "workspaces", name, members, aggregator=bool(members)) if (members or name) else None
    if reader == "pnpm-workspace":
        doc = parse_yaml(data)
        members = _strs(doc.get("packages")) if isinstance(doc, dict) else []
        return Decl(reader, path, directory, "packages", None, members, aggregator=bool(members)) if members else None
    if reader == "lerna":
        doc = parse_json(data)
        members = _strs(doc.get("packages")) if isinstance(doc, dict) else []
        return Decl(reader, path, directory, "packages", None, members, aggregator=bool(members)) if members else None
    if reader == "cargo":
        doc = parse_toml(data)
        pkg, ws = doc.get("package"), doc.get("workspace")
        name = pkg.get("name") if isinstance(pkg, dict) and isinstance(pkg.get("name"), str) else None
        if isinstance(ws, dict):
            return Decl(reader, path, directory, "members", name, _strs(ws.get("members")), _strs(ws.get("exclude")), aggregator=not isinstance(pkg, dict))
        return Decl(reader, path, directory, "package", name) if name else None
    if reader == "uv":
        doc = parse_toml(data)
        project, tool = doc.get("project"), doc.get("tool")
        name = project.get("name") if isinstance(project, dict) and isinstance(project.get("name"), str) else None
        poetry = tool.get("poetry") if isinstance(tool, dict) else None
        if name is None and isinstance(poetry, dict) and isinstance(poetry.get("name"), str):
            name = poetry["name"]
        uv = tool.get("uv") if isinstance(tool, dict) else None
        ws = uv.get("workspace") if isinstance(uv, dict) else None
        if isinstance(ws, dict):
            return Decl(reader, path, directory, "tool.uv.workspace.members", name, _strs(ws.get("members")), _strs(ws.get("exclude")),
                        aggregator=(name is None))
        return Decl(reader, path, directory, "project.name", name) if name else None
    if reader == "go-work":
        text = data.decode("utf-8", "replace")
        uses: list = []
        for block in re.finditer(r"^\s*use\s*\(([^)]*)\)", text, re.MULTILINE):
            uses += [ln.split("//")[0].strip().strip('"') for ln in block.group(1).splitlines()]
        uses += [m.group(1).strip('"') for m in re.finditer(r'^\s*use\s+("?[^\s(/][^\s]*"?|"?\.[^\s]*"?)\s*(?://.*)?$', text, re.MULTILINE)]
        uses = [u for u in uses if u]
        return Decl(reader, path, directory, "use", None, uses, aggregator=bool(uses)) if uses else None
    if reader == "maven":
        root = parse_xml(data)
        if root.tag != "project":
            raise ManifestParseError("pom.xml has no project element")
        name = (root.findtext("artifactId") or "").strip() or None
        packaging = (root.findtext("packaging") or "jar").strip()
        modules = [(m.text or "").strip() for m in root.findall("modules/module")]
        modules = [m for m in modules if m]
        return Decl(reader, path, directory, "modules", name, modules, aggregator=(packaging == "pom")) if (modules or packaging == "pom") else None
    if reader == "gradle":
        text = re.sub(r"/\*.*?\*/", "", data.decode("utf-8", "replace"), flags=re.DOTALL)
        text = re.sub(r"//[^\n]*", "", text)
        members: list = []
        for m in re.finditer(r"\binclude\s*\(?\s*((?:[\"'][^\"'\n]+[\"']\s*,?\s*)+)", text):
            for lit in re.findall(r"[\"']([^\"'\n]+)[\"']", m.group(1)):
                members.append(lit.strip().lstrip(":").replace(":", "/"))
        return Decl(reader, path, directory, "include", None, members, aggregator=False) if members else None
    raise ValueError(f"unknown reader {reader!r}")


# ---- caps and the survey of one tree ------------------------------------------------------------------------------------------------
@dataclass
class ReadStats:
    blobs_read: int = 0
    bytes_read: int = 0
    skipped_size: int = 0
    skipped_hidden: int = 0
    skipped_missing: int = 0
    parse_errors: int = 0
    cap_reached: str = ""                                  # '' | 'blobs' | 'bytes'
    cap_skipped: int = 0
    candidates: int = 0

    def as_dict(self) -> dict:
        return dict(self.__dict__)


@dataclass
class ManifestReading:
    """The result of reading the candidate manifests of a survey, in a deterministic order (shallow first, then by path)."""
    decls: dict = field(default_factory=dict)              # manifest path -> list[Decl]
    notes: dict = field(default_factory=dict)              # manifest path -> 'size' | 'cap' | 'parse_error: ...' | 'missing'
    log: list = field(default_factory=list)                # every path actually opened, in order
    stats: ReadStats = field(default_factory=ReadStats)
    blobs: dict = field(default_factory=dict)              # manifest path -> blob sha


def read_manifests(candidates: list, source, readers, hidden, *, max_file_bytes=DEFAULT_MAX_FILE_BYTES, max_blobs=DEFAULT_MAX_BLOBS,
                   max_total_bytes=DEFAULT_MAX_TOTAL_BYTES) -> ManifestReading:
    """`candidates` is a list of (path, size) whose file NAME is on the closed list. `hidden(path)` says a path is inside a hidden subtree.
    Order: shallowest first, then by path, so the caps drop the deepest first and the result is deterministic."""
    out = ManifestReading()
    out.stats.candidates = len(candidates)
    for path, size in sorted(candidates, key=lambda c: (c[0].count("/"), c[0])):
        name = path.rpartition("/")[2]
        rs = [r for r in ALLOWED_FILES.get(name, ()) if r in readers]
        if not rs:
            continue
        if hidden(path):
            out.stats.skipped_hidden += 1
            continue
        if size > max_file_bytes:
            out.stats.skipped_size += 1
            out.notes[path] = "size"
            continue
        if out.stats.blobs_read >= max_blobs or out.stats.bytes_read >= max_total_bytes:
            out.stats.cap_reached = out.stats.cap_reached or ("blobs" if out.stats.blobs_read >= max_blobs else "bytes")
            out.stats.cap_skipped += 1
            out.notes[path] = "cap"
            continue
        out.log.append(path)
        data, sha, note = source.read(path, max_file_bytes)
        if note == "size":
            out.stats.skipped_size += 1
            out.notes[path] = "size"
            continue
        if data is None:
            out.stats.skipped_missing += 1
            out.notes[path] = "missing"
            continue
        out.stats.blobs_read += 1
        out.stats.bytes_read += len(data)
        out.blobs[path] = sha
        for r in rs:
            try:
                d = extract(r, path, data)
            except ManifestParseError as exc:
                out.stats.parse_errors += 1
                out.notes[path] = f"parse_error: {exc}"
                continue
            if d is not None:
                d.blob = sha
                out.decls.setdefault(path, []).append(d)
    return out


# ---- resolving member patterns against the path list -------------------------------------------------------------------------------
def _clean_member(pattern: str) -> str | None:
    p = pattern.strip().replace("\\", "/")
    if p.startswith("./"):
        p = p[2:]
    p = p.rstrip("/")
    if not p or p.startswith("/") or re.match(r"^[A-Za-z]:", p) or any(s == ".." for s in p.split("/")):
        return None
    return p


def resolve_members(decl: Decl, dirs: set, dir_files: dict) -> tuple[list, list]:
    """Return (member directories, unresolved patterns). `dirs` is the set of directories of the path list, `dir_files` maps a directory to the
    manifest file names it holds. A path that is absolute, has `..` or matches no directory of the list is `unresolved`; nothing is created or read."""
    from .layout_profile import glob_to_regex                         # local import: layout_profile has no dependency on this module
    need = MEMBER_MANIFESTS.get(decl.reader, set())
    base = decl.directory
    found: list = []
    unresolved: list = []
    negatives = [p[1:] for p in decl.members if p.startswith("!")] + list(decl.excludes)
    exclude_rx = []
    for n in negatives:
        c = _clean_member(n)
        if c is not None:
            exclude_rx.append(re.compile(glob_to_regex((base + "/" if base else "") + c)))
    for raw in decl.members:
        if raw.startswith("!"):
            continue
        c = _clean_member(raw)
        if c is None:
            unresolved.append(raw)
            continue
        full = (base + "/" if base else "") + c
        if decl.reader == "maven" and c.endswith(".xml"):               # a module may name a pom file: its directory is the module
            full = full.rpartition("/")[0]
            if not full and not base:
                unresolved.append(raw)
                continue
        is_glob = any(ch in c for ch in "*?[")
        if is_glob:
            rx = re.compile(glob_to_regex(full))
            hits = sorted(d for d in dirs if rx.match(d) and (not need or dir_files.get(d, set()) & need))
        else:
            hits = [full] if full in dirs else []
        if not hits:
            unresolved.append(raw)                                        # matches nothing in the list: recorded, never created or fetched
            continue
        found.extend(h for h in hits if h != base and not any(x.match(h) for x in exclude_rx))
    return sorted(set(found)), sorted(set(unresolved))
