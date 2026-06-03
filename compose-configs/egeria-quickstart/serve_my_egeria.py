import os, sys
from textual_serve.server import Server

app = "/usr/local/lib/python3.12/site-packages/my_egeria/my_egeria/DemoCode/My_Profile/my_profile_app.py"
host = os.environ.get("MY_EGERIA_HOST", "0.0.0.0")
port = int(os.environ.get("MY_PROFILE_PORT", "8020"))

# public_url is the externally-visible URL the browser uses to reach this app
# through the Apache reverse proxy. Setting it makes textual-serve emit
# same-origin static-asset and WebSocket URLs, which the page's CSP ('self')
# requires. Without it, textual-serve emits http://0.0.0.0:8020 URLs that the
# browser blocks. Set MY_EGERIA_PUBLIC_URL in compose, e.g.
# http://localhost:8085/my-egeria
public_url = os.environ.get("MY_EGERIA_PUBLIC_URL") or None

Server(
    command=f"{sys.executable} {app}",
    host=host,
    port=port,
    public_url=public_url,
).serve()
