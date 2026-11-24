#!/usr/bin/env python3
"""Regenerates charts/egeria-portal/files/{httpd.conf,proxy-locations.conf,<env>/vhost-body.conf} from compose.

The chart serves plain HTTP on 8085 (TLS ends at the Ingress), so the HTTPS vhost's body is reused without the
SSL lines. drift_test.py runs this in --check mode. Compose stays the source of truth."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CC = ROOT / "compose-configs"
OUT = ROOT / "charts" / "egeria-portal" / "files"


def vhost_body(text: str) -> str:
    """The lines of the 443 vhost from DocumentRoot up to (not including) ErrorLog, SSL lines removed."""
    m = re.search(r"<VirtualHost \*:443>(.*?)</VirtualHost>", text, re.S)
    body = m.group(1)
    start = body.index("    DocumentRoot")
    end = body.index("    ErrorLog")
    return body[start:end].rstrip() + "\n"


def build() -> dict:
    out = {
        "httpd.conf": (CC / "egeria-quickstart" / "httpd.conf").read_text(),
        "proxy-locations.conf": (CC / "egeria-quickstart" / "sites-available" / "proxy-locations.conf").read_text(),
    }
    for env in ("quickstart", "freshstart"):
        out[f"{env}/vhost-body.conf"] = vhost_body((CC / f"egeria-{env}" / "sites-available" / "fastapi-ssl.conf").read_text())
    return out


if __name__ == "__main__":
    want = build()
    bad = [k for k, v in want.items() if not (OUT / k).is_file() or (OUT / k).read_text() != v]
    if "--check" in sys.argv:
        print("\n".join(f"DRIFT: charts/egeria-portal/files/{k} differs from compose" for k in bad) or "portal conf files match compose")
        sys.exit(1 if bad else 0)
    for k, v in want.items():
        (OUT / k).write_text(v)
    print("wrote", ", ".join(want))
