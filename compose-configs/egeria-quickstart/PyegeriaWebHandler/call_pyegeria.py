# Helper to call pyegeria from FastAPI endpoint(s)
import os
from typing import Optional

# Try multiple import paths for pyegeria components
EgeriaTech = None
load_app_config = None
Client2 = None
try:
    from pyegeria import EgeriaTech as _EgeriaTech, load_app_config as _load_app_config
    EgeriaTech = _EgeriaTech
    load_app_config = _load_app_config
except Exception:
    pass

# Client2 may live in different modules depending on pyegeria version
try:
    from pyegeria.client2 import Client2 as _Client2  # type: ignore
    Client2 = _Client2
except Exception:
    try:
        from pyegeria import Client2 as _Client2  # type: ignore
        Client2 = _Client2
    except Exception:
        Client2 = None


def _load_env_and_cfg():
    """Load pyegeria app config using the directory that contains .env and config JSONs.
    Many versions of load_app_config expect a directory path, not the .env file itself.
    """
    cfg_dir = os.path.dirname(__file__)
    cfg = None
    if load_app_config is not None:
        try:
            cfg = load_app_config(cfg_dir)
        except Exception:
            cfg = None
    return cfg


def _build_client2() -> Optional[object]:
    if _EgeriaTech is None:
        return None
    cfg = _load_env_and_cfg() or {}
    env_cfg = cfg.get("Environment", {}) if isinstance(cfg, dict) else {}
    server_name = env_cfg.get("Egeria View Server") or os.environ.get("EGERIA_VIEW_SERVER", "qs-view-server")
    platform_url = (
        env_cfg.get("Egeria Platform URL")
        or env_cfg.get("Egeria View Server URL")
        or os.environ.get("EGERIA_PLATFORM_URL")
        or "https://localhost:9443"
    )
    user = os.environ.get("EGERIA_USER", "erinoverview")
    pwd = os.environ.get("EGERIA_USER_PASSWORD", "secret")
    try:
        c =  _EgeriaTech(server_name="qs-view-server", platform_url="https://host.docker.internal:9443", user_id="erinoverview", user_pwd="secret")
        response = c.get_platform_origin()
        return response
    except Exception as e:
        raise RuntimeError(f"Client2 init failed (server={server_name}, url={platform_url}): {e}")


def _build_egeria_tech() -> Optional[object]:
    if EgeriaTech is None:
        return None
    cfg = _load_env_and_cfg() or {}
    env_cfg = cfg.get("Environment", {}) if isinstance(cfg, dict) else {}
    view_server = env_cfg.get("Egeria View Server") or os.environ.get("EGERIA_VIEW_SERVER", "qs-view-server")
    url = (
        env_cfg.get("Egeria Platform URL")
        or env_cfg.get("Egeria View Server URL")
        or os.environ.get("EGERIA_PLATFORM_URL")
        or "https://localhost:9443"
    )
    user = os.environ.get("EGERIA_USER", "erinoverview")
    pwd = os.environ.get("EGERIA_USER_PASSWORD", "secret")
    try:
        return EgeriaTech(view_server, url, user, pwd)
    except Exception as e:
        raise RuntimeError(f"EgeriaTech init failed (view_server={view_server}, url={url}): {e}")


def get_platform_origin() -> str:
    """Return the platform origin as a string using pyegeria.
    Preference order: Client2.get_platform_origin() -> EgeriaTech(.client2/variants).get_platform_origin().
    """
    # First try Client2 directly (as requested)
    c2 = _build_client2()
    last_err: Optional[Exception] = None
    if c2 is not None:
        try:
            res = c2.get_platform_origin()
            return res if isinstance(res, str) else str(res)
        except Exception as e:
            last_err = e

    # Fallback to EgeriaTech and search for method
    et = _build_egeria_tech()
    if et is None and last_err is not None:
        raise RuntimeError(f"Unable to initialize pyegeria client(s): {last_err}")
    if et is None:
        raise RuntimeError("pyegeria clients could not be initialized.")

    candidates = [et]
    for attr in ("client2", "platform", "platform_services", "admin", "platformServices"):
        if hasattr(et, attr):
            candidates.append(getattr(et, attr))

    for c in candidates:
        try:
            if hasattr(c, "get_platform_origin"):
                result = c.get_platform_origin()
                if isinstance(result, dict):
                    for key in ("origin", "result", "platformOrigin", "value"):
                        if key in result:
                            return str(result[key])
                    return str(result)
                return str(result)
        except Exception as e:
            last_err = e
            continue

    raise RuntimeError(f"get_platform_origin not available on pyegeria clients: {last_err}")
