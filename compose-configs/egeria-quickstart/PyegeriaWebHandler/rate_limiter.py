"""Shared slowapi limiter instance — imported by pyegeria_handler, demo_auth_handler and tech_catalog_handler.

PO-83: limits are counted per REAL client IP. Behind the stack's Apache the TCP peer is Apache's own container
address (uvicorn trusts X-Forwarded-For only from 127.0.0.1 by default), so keying on the peer would put every
user in one bucket. So the client is read from X-Forwarded-For, but ONLY when the request came straight from a
trusted proxy (PORTAL_TRUSTED_PROXIES: the stack's Apache), walking the header right to left past trusted hops:
Apache appends the address it saw, so the rightmost untrusted entry is the real client and anything a caller
wrote further left is ignored. From anyone else (a notebook container on egeria_network, the workbench gateway,
a direct caller on the published port) the header is ignored and the peer address is the key.

Both trees carry this file byte for byte (it is not on the SHARE-3 list; keep them identical by hand).
"""
import ipaddress
import os
import socket
import time
from typing import Optional

from slowapi import Limiter

#: The limits PO-83 restored (c0039ccc's were lost in 085f9446). Per client IP.
LOGIN_LIMIT = "10/minute"          # sign-in and credential exchange: password guessing
ACCOUNT_EMAIL_LIMIT = "5/hour"     # register, password reset, verification mail: account and mail abuse

#: Comma-separated hostnames, IPs or CIDRs. Default: the two stacks' Apache containers (compose container_name).
#: Hostnames are resolved (cached for _RESOLVE_TTL: container addresses change on a restart); one that does not
#: resolve here trusts nothing.
DEFAULT_TRUSTED_PROXIES = "quickstart-web-server,freshstart-web-server"
_RESOLVE_TTL = 60.0
_resolved: dict = {"spec": None, "at": 0.0, "nets": ()}


def _ip(text: Optional[str]):
    """The address in `text` (IPv4-mapped IPv6 unwrapped), or None."""
    try:
        ip = ipaddress.ip_address((text or "").strip().split("%")[0])
    except ValueError:
        return None
    if ip.version == 6 and ip.ipv4_mapped:
        ip = ip.ipv4_mapped
    return ip


def trusted_networks() -> tuple:
    spec = os.environ.get("PORTAL_TRUSTED_PROXIES", DEFAULT_TRUSTED_PROXIES)
    now = time.monotonic()
    if _resolved["spec"] == spec and now - _resolved["at"] < _RESOLVE_TTL:
        return _resolved["nets"]
    nets = []
    for item in (s.strip() for s in spec.split(",")):
        if not item:
            continue
        try:
            nets.append(ipaddress.ip_network(item, strict=False))
            continue
        except ValueError:
            pass
        try:
            for info in socket.getaddrinfo(item, None):
                ip = _ip(info[4][0])
                if ip is not None:
                    nets.append(ipaddress.ip_network(ip))
        except OSError:
            pass                       # not resolvable here (e.g. the other stack's Apache): trusts nothing
    _resolved.update(spec=spec, at=now, nets=tuple(nets))
    return _resolved["nets"]


def _trusted(ip) -> bool:
    return ip is not None and any(ip.version == n.version and ip in n for n in trusted_networks())


def client_ip(request) -> str:
    """The rate-limit key: the real client address (see the module docstring)."""
    peer_text = request.client.host if request.client else ""
    peer = _ip(peer_text)
    key = str(peer) if peer is not None else (peer_text or "unknown")
    xff = request.headers.get("x-forwarded-for")
    if not xff or not _trusted(peer):  # no header, or not from our Apache: never read it (and never resolve)
        return key
    for hop in reversed([h for h in xff.split(",") if h.strip()]):
        ip = _ip(hop)
        if ip is None:
            return key                 # malformed where our proxy wrote: trust none of it
        if not _trusted(ip):
            return str(ip)
    return key


limiter = Limiter(key_func=client_ip)
