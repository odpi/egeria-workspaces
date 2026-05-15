# FastAPI app for Dr. Egeria Markdown processing

import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEPLOYMENT_DIR = SCRIPT_DIR.parent
WORKSPACE_ROOT = DEPLOYMENT_DIR.parent.parent
EXCHANGE_ROOT = WORKSPACE_ROOT / "exchange-quickstart"


def _bootstrap_runtime_defaults() -> None:
    log_directory = os.environ.setdefault("PYEGERIA_LOG_DIRECTORY", str(SCRIPT_DIR / "logs"))
    os.makedirs(log_directory, exist_ok=True)

    os.environ.setdefault("EGERIA_USER", "erinoverview")
    os.environ.setdefault("EGERIA_USER_PASSWORD", "secret")
    os.environ.setdefault("EGERIA_WIDTH", "100")

    root_default: str
    inbox_default: str
    outbox_default: str

    if os.path.exists("/.dockerenv"):
        root_default = "/"
        inbox_default = "dr-egeria-inbox"
        outbox_default = "dr-egeria-outbox"
    elif EXCHANGE_ROOT.is_dir():
        root_default = str(EXCHANGE_ROOT)
        inbox_default = "loading-bay/dr-egeria-inbox"
        outbox_default = "distribution-hub/dr-egeria-outbox"
    else:
        root_default = str(SCRIPT_DIR)
        inbox_default = "dr-egeria-inbox"
        outbox_default = "dr-egeria-outbox"

    os.environ.setdefault("EGERIA_ROOT_PATH", str(root_default))
    os.environ.setdefault("EGERIA_INBOX_PATH", str(inbox_default))
    os.environ.setdefault("EGERIA_OUTBOX_PATH", str(outbox_default))


_bootstrap_runtime_defaults()

import asyncio
import concurrent.futures
import io
from contextlib import redirect_stderr, redirect_stdout
from typing import Any, Callable

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pyegeria import print_basic_exception
import pyegeria
pyegeria.enable_ssl_check = False
pyegeria.disable_ssl_warnings = True

import dr_egeria_md


app = FastAPI(
    title="Dr. Egeria Markdown Processor API",
    description="POST an instruction to process a Markdown file via dr_egeria_md.process_markdown_file and get structured command status back.",
    version="1.0.0",
)

# Security Token (Simplified for local use)
MCP_ACCESS_TOKEN = os.environ.get("MCP_ACCESS_TOKEN", "egeria-secret-mcp-token")

# Use a standard ASGI middleware instead of BaseHTTPMiddleware to avoid 
# issues with custom response types like SSE.
class MCPTokenMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        path = request.url.path
        
        # Check for SSE or messages endpoints.
        if path.endswith("/sse") or path.endswith("/messages") or "/sse/" in path or "/messages/" in path:
            if request.method == "OPTIONS":
                await self.app(scope, receive, send)
                return

            # For /messages POST requests, the token might be missing if established via SSE.
            # We allow it if it has a session_id, as that was established via a token-authenticated SSE call.
            if (path.endswith("/messages") or "/messages/" in path) and request.method == "POST":
                if request.query_params.get("session_id"):
                    await self.app(scope, receive, send)
                    return

            token = request.query_params.get("token") or request.headers.get("X-API-Key")
            if token != MCP_ACCESS_TOKEN:
                response = JSONResponse(
                    status_code=403, 
                    content={"detail": "Invalid MCP Access Token"}
                )
                await response(scope, receive, send)
                return

        await self.app(scope, receive, send)

app.add_middleware(MCPTokenMiddleware)

# CORS configuration for Obsidian security
# CORSMiddleware is added AFTER other middlewares so it wraps them
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)


class ProcessRequest(BaseModel):
    input_file: str = Field(..., description="Markdown file to process")
    source_file: str | None = Field(None, description="Original source filename")
    output_folder: str = Field("", description="Output folder")
    directive: str = Field("process", description="Processing directive: display | validate | process")

    environment_key: str = Field(..., description="Logical key/name for the selected Environment configuration")
    user_profile_key: str = Field(..., description="Logical key/name for the selected User Profile configuration")
    environment: dict[str, Any] = Field(default_factory=dict, description="Environment configuration")
    user_profile: dict[str, Any] = Field(default_factory=dict, description="User Profile configuration")

    user_id: str = Field(..., description="Egeria user id")
    user_pass: str = Field(..., description="Egeria user password")


class ProcessResponse(BaseModel):
    status: str
    message: str
    input_file: str
    output_folder: str
    output_file: str | None = None
    output_path: str | None = None
    console_output: str = ""
    environment_key: str
    user_profile_key: str


# Initialize MCP Server with consolidated tools
from mcp_server import server as mcp_server
from type_system_handler import router as type_system_router
app.include_router(type_system_router)
from report_specs_handler import router as report_specs_router
app.include_router(report_specs_router)
from glossary_handler import router as glossary_router
app.include_router(glossary_router)
from reference_data_handler import router as reference_data_router
app.include_router(reference_data_router)
from digital_products_handler import router as digital_products_router
app.include_router(digital_products_router)
from valid_values_handler import router as valid_values_router
app.include_router(valid_values_router)
# Mount the MCP SSE application
# FastMCP.sse_app() returns a Starlette app with /sse and /messages routes
mcp_app = mcp_server.sse_app()
app.mount("/", mcp_app)


@app.get("/")
async def health():
    return {"status": "ok", "service": "dr-egeria-md"}


def _stringify_env_value(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    if value is None:
        return ""
    return str(value)


def _apply_request_configuration(req: ProcessRequest) -> tuple[str, str]:
    environment = req.environment or {}
    user_profile = req.user_profile or {}

    print(f"DEBUG: Request environment: {environment}")

    platform_url = str(
        environment.get("Egeria Platform URL")
        or environment.get("Egeria View Server URL")
        or os.environ.get("EGERIA_PLATFORM_URL", "https://host.docker.internal:9443")
    )

    view_server = str(
        environment.get("Egeria View Server")
        or os.environ.get("EGERIA_VIEW_SERVER", "qs-view-server")
    )

    env_mappings = {
        "Egeria Kafka Endpoint": "EGERIA_KAFKA_ENDPOINT",
        "Egeria Jupyter": "EGERIA_JUPYTER",
        "Dr.Egeria Outbox": "EGERIA_OUTBOX_PATH",
        "Dr.Egeria Inbox": "EGERIA_INBOX_PATH",
        "Egeria Integration Daemon": "EGERIA_INTEGRATION_DAEMON",
        "Egeria Integration Daemon URL": "EGERIA_INTEGRATION_DAEMON_URL",
        "Egeria View Server": "EGERIA_VIEW_SERVER",
        "Egeria View Server URL": "EGERIA_VIEW_SERVER_URL",
        "Egeria Metadata Store": "EGERIA_METADATA_STORE",
        "Egeria Platform URL": "EGERIA_PLATFORM_URL",
        "Egeria Engine Host": "EGERIA_ENGINE_HOST",
        "Egeria Engine Host URL": "EGERIA_ENGINE_HOST_URL",
        "Egeria Glossary Path": "EGERIA_GLOSSARY_PATH",
        "Egeria Mermaid Folder": "EGERIA_MERMAID_FOLDER",
        "Pyegeria Root": "PYEGERIA_ROOT_PATH",
        "Pyegeria Config Directory": "PYEGERIA_CONFIG_DIRECTORY",
        "Pyegeria User Format Sets Dir": "PYEGERIA_USER_FORMAT_SETS_DIR",
        "Pyegeria Publishing Root": "PYEGERIA_PUBLISHING_ROOT",
        "console_width": "EGERIA_WIDTH",
    }

    profile_mappings = {
        "Egeria Home Glossary Name": "EGERIA_HOME_GLOSSARY_NAME",
        "Egeria Local Qualifier": "EGERIA_LOCAL_QUALIFIER",
        "Egeria Home Collection": "EGERIA_HOME_COLLECTION",
    }

    for config_key, env_key in env_mappings.items():
        if config_key in environment:
            os.environ[env_key] = _stringify_env_value(environment[config_key])

    # Re-apply EGERIA_ROOT_PATH if Pyegeria Root was in environment
    if "Pyegeria Root" in environment:
        root_path = _stringify_env_value(environment["Pyegeria Root"])
        if root_path and not Path(root_path).is_absolute():
            os.environ["EGERIA_ROOT_PATH"] = str(WORKSPACE_ROOT / root_path)
        else:
            os.environ["EGERIA_ROOT_PATH"] = root_path
    
    # Re-apply EGERIA_INBOX_PATH if it was in environment (mapped via env_mappings)
    if "Dr.Egeria Inbox" in environment:
        os.environ["EGERIA_INBOX_PATH"] = _stringify_env_value(environment["Dr.Egeria Inbox"])

    # Log values after configuration application
    print(f"DEBUG: Configured EGERIA_ROOT_PATH: {os.environ.get('EGERIA_ROOT_PATH')}")
    print(f"DEBUG: Configured EGERIA_INBOX_PATH: {os.environ.get('EGERIA_INBOX_PATH')}")

    # Special handling for absolute paths sent from plugin
    if req.input_file.startswith("/"):
        # If the file path is already absolute, we don't need to prepend anything,
        # but we do want to check fallbacks if it's not found at the literal path.
        print(f"DEBUG: Absolute path detected in request: {req.input_file}")
    
    for config_key, env_key in profile_mappings.items():
        if config_key in user_profile:
            os.environ[env_key] = _stringify_env_value(user_profile[config_key])

    os.environ["EGERIA_USER"] = req.user_id
    os.environ["EGERIA_USER_PASSWORD"] = req.user_pass

    # Check if the file actually exists using the combination
    current_root = os.environ.get("EGERIA_ROOT_PATH", "/")
    current_inbox = os.environ.get("EGERIA_INBOX_PATH", ".")
    combined_path = Path(current_root) / current_inbox / req.input_file
    resolved_path = combined_path.resolve()
    print(f"DEBUG: Combined absolute path check: {resolved_path}")
    
    # List of possible mount points to check if not found at the primary path
    mount_points = ["/work", "/coco-workbooks", "/work/Work-Obsidian"]
    
    if resolved_path.exists():
        print(f"DEBUG: FILE FOUND at {resolved_path}. Using absolute path for processor.")
    else:
        print(f"DEBUG: FILE NOT FOUND at {resolved_path}. Checking fallback mount points...")
        found_fallback = False
        for mp in mount_points:
            fallback_path = Path(mp) / req.input_file.lstrip("/")
            if fallback_path.exists():
                resolved_path = fallback_path.resolve()
                print(f"DEBUG: FILE FOUND at fallback {resolved_path}")
                found_fallback = True
                break
        
        if not found_fallback:
            print(f"DEBUG: FILE NOT FOUND in any common location.")
            return req.input_file, view_server, platform_url

    # If found, use the absolute path to bypass internal library resolution issues.
    # However, we must ensure EGERIA_OUTBOX_PATH is absolute or correctly rooted.
    outbox = os.environ.get("EGERIA_OUTBOX_PATH", "dr-egeria-outbox")
    
    # Discover the correct root for the outbox based on where we found the file
    discovered_root = "/"
    for mp in mount_points:
        if str(resolved_path).startswith(mp):
            discovered_root = mp
            break
            
    if not Path(outbox).is_absolute():
        # Force outbox to be absolute relative to the discovered root
        absolute_outbox = str(Path(discovered_root) / outbox)
        os.environ["EGERIA_OUTBOX_PATH"] = absolute_outbox
        print(f"DEBUG: Forced absolute EGERIA_OUTBOX_PATH: {absolute_outbox}")

    os.environ["EGERIA_ROOT_PATH"] = "/"
    os.environ["EGERIA_INBOX_PATH"] = "."
    return str(resolved_path), view_server, platform_url


def _run_and_capture(func: Callable, *args, **kwargs) -> str:
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()

    with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
        try:
            func(*args, **kwargs)
        except SystemExit:
            pass

    out = stdout_buf.getvalue()
    err = stderr_buf.getvalue()
    return (out + ("\n" if out and err else "") + err).strip()


def _resolve_output_path(output_folder: str, output_file: str | None) -> str | None:
    if not output_file:
        return None

    output_path = Path(output_file)
    if output_path.is_absolute():
        return str(output_path)

    if output_folder:
        folder_path = Path(output_folder)
        if folder_path.is_absolute():
            return str(folder_path / output_file)

        root_path = Path(os.environ.get("EGERIA_ROOT_PATH", ""))
        if str(root_path):
            return str(root_path / output_folder / output_file)

        return str(folder_path / output_file)

    return output_file


def _extract_output_file(console_output: str) -> str | None:
    for line in reversed(console_output.splitlines()):
        lower = line.lower()
        if "output file:" in lower:
            return line.split(":", 1)[1].strip()
        if "output path:" in lower:
            return line.split(":", 1)[1].strip()
    return None


def _console_output_indicates_error(console_output: str) -> bool:
    lower_output = console_output.lower()
    error_markers = [
        "error:",
        "file not found",
        "exception",
        "traceback",
        "failed"
    ]
    return any(marker in lower_output for marker in error_markers)


def _invoke_processor(req: ProcessRequest) -> ProcessResponse:
    input_file, server, url = _apply_request_configuration(req)

    cmd = dr_egeria_md.process_md_file
    func = getattr(cmd, "callback", cmd)
    
    # Ensure output_folder is also absolute if we've resolved a root
    output_folder = req.output_folder or ""
    if not Path(output_folder).is_absolute():
        # Look for the vault root in the input_file path
        # If input_file is /coco-workbooks/..., the root is /coco-workbooks
        if input_file.startswith("/coco-workbooks"):
            output_folder = str(Path("/coco-workbooks") / output_folder)
        elif input_file.startswith("/work/Work-Obsidian"):
            output_folder = str(Path("/work/Work-Obsidian") / output_folder)
        elif input_file.startswith("/work"):
             output_folder = str(Path("/work") / output_folder)

    print(f"DEBUG: Invoking processor with input_file: {input_file}")
    print(f"DEBUG: Invoking processor with output_folder: {output_folder}")

    console_output = _run_and_capture(
        func,
        input_file=req.source_file if req.source_file else input_file,
        output_folder=output_folder,
        directive=req.directive,
        server=server,
        url=url,
        userid=req.user_id,
        user_pass=req.user_pass,
    )

    output_file = _extract_output_file(console_output)
    output_path = _resolve_output_path(req.output_folder, output_file)

    if _console_output_indicates_error(console_output):
        return ProcessResponse(
            status="error",
            message="Dr.Egeria command completed with errors.",
            input_file=input_file,
            output_folder=req.output_folder or "",
            output_file=output_file,
            output_path=output_path,
            console_output=console_output or "(no output)",
            environment_key=req.environment_key,
            user_profile_key=req.user_profile_key,
        )

    return ProcessResponse(
        status="success",
        message="Dr.Egeria command completed successfully.",
        input_file=input_file,
        output_folder=req.output_folder or "",
        output_file=output_file,
        output_path=output_path,
        console_output=console_output or "(no output)",
        environment_key=req.environment_key,
        user_profile_key=req.user_profile_key,
    )

@app.post("/dr-egeria/process", response_model=ProcessResponse)
async def process_markdown(request: ProcessRequest):
    try:
        print(f"DEBUG: Received request for input_file: {request.input_file}")
        loop = asyncio.get_event_loop()
        result: ProcessResponse = await loop.run_in_executor(executor, _invoke_processor, request)
        return JSONResponse(content=result.model_dump())
    except Exception as e:
        print_basic_exception(e)
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": f"Processing failed: {e}",
                "input_file": request.input_file,
                "output_folder": request.output_folder,
                "environment_key": request.environment_key,
                "user_profile_key": request.user_profile_key,
            },
        )


@app.post("/dr-egeria/refresh")
async def refresh_commands():
    """Refresh Dr. Egeria command specifications and reload dispatcher logic."""
    try:
        import importlib
        import dr_egeria_md
        from md_processing.md_processing_utils.md_processing_constants import load_commands
        
        # 1. Reload command specifications from JSON
        load_commands()
        
        # 2. Force reload the dispatcher module to pick up any code fixes
        importlib.reload(dr_egeria_md)
        
        return {"status": "success", "message": "Command specifications and dispatcher module reloaded"}
    except Exception as e:
        print_basic_exception(e)
        raise HTTPException(status_code=500, detail=f"Refresh failed: {e}")


@app.on_event("shutdown")
async def on_shutdown():
    executor.shutdown(wait=True)