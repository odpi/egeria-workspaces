# FastAPI app for Dr. Egeria Markdown processing


import asyncio
import concurrent.futures
import io
import os
from contextlib import redirect_stdout, redirect_stderr
from typing import Callable

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field, ValidationError
from pyegeria import print_basic_exception

os.environ.setdefault("EGERIA_USER", "erinoverview")
os.environ.setdefault("EGERIA_USER_PASSWORD", "secret")
# Important: ensure root path is empty so container joins to /dr-egeria-inbox/<file>
os.environ.setdefault("EGERIA_ROOT_PATH", "/")
os.environ.setdefault("EGERIA_INBOX_PATH", "dr-egeria-inbox")
os.environ.setdefault("EGERIA_OUTBOX_PATH", "dr-egeria-outbox")

EGERIA_USER = os.environ.get("EGERIA_USER", "erinoverview")
EGERIA_USER_PASSWORD = os.environ.get("EGERIA_USER_PASSWORD", "secret")

import dr_egeria_md


app = FastAPI(
    title="Dr. Egeria Markdown Processor API",
    description="POST an instruction to process a Markdown file via dr_egeria_md.process_markdown_file and get the console output back.",
    version="1.0.0",
)

# Thread pool for blocking work
executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)


class ProcessRequest(BaseModel):
    input_file: str = Field(..., description="Name of the markdown file in the inbox to process")
    output_folder: str = Field("", description="Output folder (if used by the processor)")
    directive: str = Field("process", description="Processing directive: display | validate | process")
    url: str = Field(..., description="Egeria platform URL (e.g., https://host.docker.internal:9443)")
    server: str = Field(..., description="Egeria view server name (e.g., qs-view-server)")
    user_id: str = Field(..., description="Egeria user id")
    user_pass: str = Field(..., description="Egeria user password")


@app.get("/")
async def health():
    return {"status": "ok", "service": "dr-egeria-md"}


def _run_and_capture(func: Callable, *args, **kwargs) -> str:
    """Run a callable capturing both stdout and stderr and return the combined text."""
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    # Ensure environment variables expected by dr_egeria_md are available
    # (these provide defaults but we allow explicit args to override)
    # Not strictly required, but harmless if present.
    with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
        try:
            func(*args, **kwargs)
        except SystemExit:
            # In case click decorators try to exit, ignore for direct call
            pass
    out = stdout_buf.getvalue()
    err = stderr_buf.getvalue()
    return (out + ("\n" if out and err else "") + err).strip()


def _invoke_processor(req: ProcessRequest) -> str:
    # Click wraps the function; use the callback when present and pass kwargs
    cmd = dr_egeria_md.process_md_file
    func = getattr(cmd, "callback", cmd)

    return _run_and_capture(
        func,
        input_file=req.input_file,
        output_folder=req.output_folder or "",
        directive=req.directive,
        server=req.server,
        url=req.url,
        userid=req.user_id,
        user_pass=req.user_pass,
    )


@app.post("/dr-egeria/process", response_class=PlainTextResponse)
async def process_markdown(request: ProcessRequest):
    try:
        # Run the blocking processor off the event loop
        loop = asyncio.get_event_loop()
        text: str = await loop.run_in_executor(executor, _invoke_processor, request)
        if not text:
            text = "(no output)"
        return PlainTextResponse(content=text)
    except Exception as e:
        print_basic_exception(e)
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")


@app.on_event("shutdown")
async def on_shutdown():
    executor.shutdown(wait=True)