import os, sys
from textual_serve.server import Server

app = "/usr/local/lib/python3.12/site-packages/my_egeria/my_egeria/DemoCode/My_Profile/my_profile_app.py"
host = os.environ.get("MY_EGERIA_HOST", "0.0.0.0")
port = int(os.environ.get("MY_PROFILE_PORT", "8020"))
Server(command=f"{sys.executable} {app}", host=host, port=port).serve()
