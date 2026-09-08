import glob, os, sys
from textual_serve.server import Server

# Resolve the site-packages path dynamically instead of hardcoding the
# interpreter's minor version — a Python base-image bump (e.g. 3.12 -> 3.14)
# otherwise leaves this pointing at a path that no longer exists, and
# textual-serve silently fails to launch (its startup banner prints the
# literal command in the browser, then the pty subprocess exits immediately).
_candidates = glob.glob(
    "/usr/local/lib/python3.*/site-packages/my_egeria/my_egeria/DemoCode/My_Profile/my_profile_app.py"
)
if not _candidates:
    raise FileNotFoundError(
        "my_profile_app.py not found under /usr/local/lib/python3.*/site-packages/my_egeria/ "
        "- is the my_egeria package installed?"
    )
app = _candidates[0]
host = os.environ.get("MY_EGERIA_HOST", "0.0.0.0")
port = int(os.environ.get("MY_PROFILE_PORT", "8020"))

# public_url is the externally-visible URL the browser uses to reach this app
# through the Apache reverse proxy. Setting it makes textual-serve emit
# same-origin static-asset and WebSocket URLs, which the page's CSP ('self')
# requires. Without it, textual-serve emits http://0.0.0.0:8020 URLs that the
# browser blocks. Set MY_EGERIA_PUBLIC_URL in compose, e.g.
# https://localhost:8843/my-egeria
public_url = os.environ.get("MY_EGERIA_PUBLIC_URL") or None

Server(
    command=f"{sys.executable} {app}",
    host=host,
    port=port,
    public_url=public_url,
).serve()
