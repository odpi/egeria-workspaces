"""Scan every PyegeriaWebHandler module: no cache key may be built from a bare user id or a token's
unverified `sub`.

A bare user_id is None for every token-authenticated user (they all shared one entry, and saw each other's
zone-filtered results); a token's `sub` is read without verifying the signature, and a cache hit makes no
Egeria call, so a forged token could read another user's entry. Key on result_cache.request_identity()
(or credential_identity()) instead: a hash of the credential actually presented.

How the scan works (ast, per function):
- a name is TAINTED when it is user_id / uid / user_name / username, or is assigned from an expression
  that uses a tainted name or calls token_user() / _token_user() / _token_sub(); a value produced by
  request_identity(...) / credential_identity(...) is clean whatever its arguments.
- a KEY expression is: the value assigned to a variable whose name ends in "key"; the return value of a
  function whose name contains "key"; the argument of <cache>.get(...) / <cache>.pop(...) or the index of
  <cache>[...] for any name containing "cache".
- a tainted key expression is a finding, unless it is in ALLOWED below with its reason.
"""
import ast
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent.parent

BARE_IDS = {"user_id", "uid", "user_name", "username"}
UNVERIFIED_CALLS = {"token_user", "_token_user", "_token_sub"}
LAUNDER_CALLS = {"request_identity", "credential_identity", "_credential_identity"}

# (module, function) -> why it is allowed. Keep this list short and every entry justified.
ALLOWED = {
    ("demo_auth_gate.py", "_authenticated"):
        "the sub comes from the Portal JWT that demo_auth_handler._decode_jwt has VERIFIED, and the cache "
        "only holds whether that account is still enabled",
}


def _call_name(node):
    f = node.func
    return f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else None)


# Helpers that hand back the caller's credentials (so their result carries the bare id): taint flows
# through these. Any other call is opaque: `mgr = _get_manager(url, server, user_id, user_pwd)` is a
# client, not an identity, and must not taint everything built from its results.
PASS_THROUGH_CALLS = {"_env", "_creds"}


def _tainted(expr, tainted_names) -> bool:
    """Does `expr` carry a bare user id or an unverified token sub into its value?"""
    if expr is None:
        return False
    if isinstance(expr, ast.Name):
        return expr.id in tainted_names
    if isinstance(expr, ast.Call):
        name = _call_name(expr)
        if name in UNVERIFIED_CALLS:
            return True
        if name in PASS_THROUGH_CALLS:
            return any(_tainted(a, tainted_names) for a in expr.args) or bool(set(_names(expr)) & BARE_IDS)
        if _builds_a_string(expr):                     # "|".join([...]), "{}".format(...), str(x): taint flows
            parts = list(expr.args) + [k.value for k in expr.keywords]
            if isinstance(expr.func, ast.Attribute) and not isinstance(expr.func.value, ast.Constant):
                parts.append(expr.func.value)          # x.format(...) / sep.join(...) with a variable receiver
            return any(_tainted(a, tainted_names) for a in parts)
        return False                                   # opaque (includes request_identity / credential_identity)
    if isinstance(expr, ast.Lambda):
        return False
    return any(_tainted(child, tainted_names) for child in ast.iter_child_nodes(expr))


def _builds_a_string(call) -> bool:
    f = call.func
    if isinstance(f, ast.Name):
        return f.id == "str"
    return isinstance(f, ast.Attribute) and f.attr in ("join", "format", "lower", "upper", "strip")


def _names(expr):
    return [n.id for n in ast.walk(expr) if isinstance(n, ast.Name)]


def _is_cache_name(node) -> bool:
    name = node.id if isinstance(node, ast.Name) else (node.attr if isinstance(node, ast.Attribute) else "")
    return "cache" in name.lower()


def _findings_in_function(fn):
    tainted = set(BARE_IDS)
    out = []
    # two passes so a name assigned late in the function but used in a loop is still caught
    for _ in range(2):
        for node in ast.walk(fn):
            if isinstance(node, ast.Assign) and _tainted(node.value, tainted):
                for t in node.targets:
                    # `u, sv, uid, pwd = _env(...)`: only the id slot carries the id, and it is caught by
                    # name (BARE_IDS); tainting u/sv/pwd too would flag every key built from url/server.
                    if isinstance(t, ast.Name):
                        tainted.add(t.id)
    for node in ast.walk(fn):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id.lower().endswith("key") and _tainted(node.value, tainted):
                    out.append((node.lineno, f"{t.id} = ... built from a bare user id / token sub"))
        elif isinstance(node, ast.Return) and "key" in fn.name.lower() and _tainted(node.value, tainted):
            out.append((node.lineno, f"{fn.name} returns a key built from a bare user id / token sub"))
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr in ("get", "pop", "setdefault") and _is_cache_name(node.func.value) \
                and node.args and _tainted(node.args[0], tainted):
            out.append((node.lineno, "cache looked up by a bare user id / token sub"))
        elif isinstance(node, ast.Subscript) and _is_cache_name(node.value) and _tainted(node.slice, tainted):
            out.append((node.lineno, "cache indexed by a bare user id / token sub"))
    return out


def scan_source(src: str, filename: str):
    tree = ast.parse(src, filename)
    findings = []
    for fn in ast.walk(tree):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if (filename, fn.name) in ALLOWED:
                continue
            for line, why in _findings_in_function(fn):
                findings.append(f"{filename}:{line} in {fn.name}(): {why}")
    return sorted(set(findings))


def _modules():
    return sorted(p for p in HERE.glob("*.py"))


def test_no_cache_key_is_built_from_a_bare_user_id_or_token_sub():
    findings = []
    for p in _modules():
        findings += scan_source(p.read_text(), p.name)
    assert not findings, ("cache keys must use result_cache.request_identity(), not a bare user id or a "
                          "token's unverified sub:\n  " + "\n  ".join(findings))


def test_every_allowed_exception_still_exists():
    """An allow-list entry for code that is gone (or renamed) would silently allow its replacement."""
    names = {}
    for p in _modules():
        tree = ast.parse(p.read_text(), p.name)
        names[p.name] = {n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    for module, fn in ALLOWED:
        assert fn in names.get(module, set()), f"ALLOWED entry {module}:{fn} no longer exists; remove it"


# ── the scan catches the shapes it is meant to (so a green run means something) ──

BAD = {
    "bare user_id in an f-string key": '''
def route(url, server, user_id, user_pwd):
    cache_key = f"{url}|{server}|{user_id or ''}"
    return _TREE_CACHE.get(cache_key)
''',
    "uid from _env": '''
def state(url, server, user_id, user_pwd, as_of):
    u, sv, uid, pwd = _env(url, server, user_id, user_pwd)
    key = f"{u}|{sv}|{uid}|{as_of}"
''',
    "token sub via a helper variable": '''
def _list_key(kind, url, server, user_id, user_pwd):
    who = _token_user() or _creds(url, server, user_id, user_pwd)[2]
    return f"{kind}|{who}"
''',
    "token sub inline": '''
async def _cached(name):
    key = f"{name}|{_token_user() or '-'}"
''',
    "token sub joined into a key (the old overview _section_key)": '''
def _section_key(section, *args, url=None, server=None, user_id=None, user_pwd=None):
    u, sv, uid, _ = _env(url, server, user_id, user_pwd)
    viewer = token_user() or uid
    return "|".join([section, u, sv, viewer, *(str(a) for a in args)]) + lineage_key()
''',
    "cache indexed directly by user_id": '''
def check(user_id):
    return _USER_CACHE.get(user_id)
''',
    "cache key passed through a key helper": '''
def _report_cache_key(server_guid, url, server, user_id):
    return f"{server_guid}|{url}|{server}|{user_id}"
''',
}

GOOD = {
    "request_identity": '''
def route(url, server, user_id, user_pwd):
    who = request_identity(user_id, user_pwd)
    cache_key = f"{url}|{server}|{who}"
    return _TREE_CACHE.get(cache_key) if who else None
''',
    "credential_identity with user_id as an argument": '''
def _roots_cache_key(url, server, user_id, user_pwd):
    identity = credential_identity(get_request_token(), user_id, user_pwd, "svc")
    return f"{url}|{server}|{identity}"
''',
    "service-user key": '''
async def list_survey_types(url, server, user_id, user_pwd):
    svc_user = os.environ.get("EGERIA_USER", "erinoverview")
    cache_key = f"svc:{svc_user}"
''',
}


@pytest.mark.parametrize("label", sorted(BAD))
def test_scan_flags_known_bad_shapes(label):
    assert scan_source(BAD[label], "fixture.py"), f"scan missed: {label}"


@pytest.mark.parametrize("label", sorted(GOOD))
def test_scan_accepts_known_good_shapes(label):
    assert scan_source(GOOD[label], "fixture.py") == [], f"scan wrongly flagged: {label}"
