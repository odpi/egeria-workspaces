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

    if "Pyegeria Root" in environment:
        root_path = _stringify_env_value(environment["Pyegeria Root"])
        if root_path and not Path(root_path).is_absolute():
            # If relative, resolve against WORKSPACE_ROOT
            os.environ["EGERIA_ROOT_PATH"] = str(WORKSPACE_ROOT / root_path)
        else:
            os.environ["EGERIA_ROOT_PATH"] = root_path

    for config_key, env_key in profile_mappings.items():
        if config_key in user_profile:
            os.environ[env_key] = _stringify_env_value(user_profile[config_key])

    os.environ["EGERIA_USER"] = req.user_id
    os.environ["EGERIA_USER_PASSWORD"] = req.user_pass

    return view_server, platform_url


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
    server, url = _apply_request_configuration(req)

    cmd = dr_egeria_md.process_md_file
    func = getattr(cmd, "callback", cmd)

    console_output = _run_and_capture(
        func,
        input_file=req.input_file,
        output_folder=req.output_folder or "",
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
            input_file=req.input_file,
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
        input_file=req.input_file,
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