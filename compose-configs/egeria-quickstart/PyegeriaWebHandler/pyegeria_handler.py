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

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pyegeria import print_basic_exception

import dr_egeria_md


app = FastAPI(
    title="Dr. Egeria Markdown Processor API",
    description="POST an instruction to process a Markdown file via dr_egeria_md.process_markdown_file and get structured command status back.",
    version="1.0.0",
)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)


class ProcessRequest(BaseModel):
    input_file: str = Field(..., description="Markdown file to process")
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
        "console_width": "PYEGERIA_CONSOLE_WIDTH",
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
        os.environ["EGERIA_ROOT_PATH"] = "/"
        os.environ["EGERIA_INBOX_PATH"] = "."
        print(f"DEBUG: Absolute path detected. Forcing EGERIA_ROOT_PATH='/' and EGERIA_INBOX_PATH='.'")
    else:
        # If relative, check if it already starts with root_path (redundant but safe)
        root_path = os.environ.get("EGERIA_ROOT_PATH", "/")
        if root_path != "/" and req.input_file.startswith(root_path.rstrip("/") + "/"):
             os.environ["EGERIA_INBOX_PATH"] = "."
             print(f"DEBUG: Relative path already contains root. Setting EGERIA_INBOX_PATH='.'")

    for config_key, env_key in profile_mappings.items():
        if config_key in user_profile:
            os.environ[env_key] = _stringify_env_value(user_profile[config_key])

    os.environ["EGERIA_USER"] = req.user_id
    os.environ["EGERIA_USER_PASSWORD"] = req.user_pass

    # Check if the file actually exists using the combination
    combined_path = Path(os.environ.get("EGERIA_ROOT_PATH", "/")) / os.environ.get("EGERIA_INBOX_PATH", ".") / req.input_file
    print(f"DEBUG: Combined absolute path check: {combined_path}")
    
    if combined_path.exists():
        print(f"DEBUG: FILE FOUND at {combined_path}. Using absolute path for processor.")
        # If found, use the absolute path to bypass internal library resolution issues.
        # However, we must ensure EGERIA_OUTBOX_PATH is absolute or correctly rooted.
        
        # If the outbox is relative, we should try to keep it relative to the vault root 
        # that we discovered during combined_path construction.
        current_root = os.environ.get("EGERIA_ROOT_PATH", "/")
        outbox = os.environ.get("EGERIA_OUTBOX_PATH", "dr-egeria-outbox")
        
        if not Path(outbox).is_absolute() and current_root != "/":
            # Force outbox to be absolute relative to the vault root
            absolute_outbox = str(Path(current_root) / outbox)
            os.environ["EGERIA_OUTBOX_PATH"] = absolute_outbox
            print(f"DEBUG: Forced absolute EGERIA_OUTBOX_PATH: {absolute_outbox}")

        os.environ["EGERIA_ROOT_PATH"] = "/"
        os.environ["EGERIA_INBOX_PATH"] = "."
        return str(combined_path), view_server, platform_url
    else:
        print(f"DEBUG: FILE NOT FOUND at {combined_path}")

    return req.input_file, view_server, platform_url


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
        input_file=input_file,
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
    """Refresh Dr. Egeria command specifications from JSON files."""
    try:
        from md_processing.md_processing_utils.md_processing_constants import load_commands
        load_commands()
        return {"status": "success", "message": "Command specifications refreshed"}
    except Exception as e:
        print_basic_exception(e)
        raise HTTPException(status_code=500, detail=f"Refresh failed: {e}")


@app.on_event("shutdown")
async def on_shutdown():
    executor.shutdown(wait=True)