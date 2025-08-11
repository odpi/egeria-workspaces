# main.py
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# import pyegeria
import asyncio
import concurrent.futures # For running sync code in a thread pool



# from commands.cat.dr_egeria_md import process_markdown_file
# from pyegeria import EgeriaTech, load_app_config

# config = load_app_config(".env")

# Initialize FastAPI app
app = FastAPI(
    title="Local Library Wrapper API",
    description="A simple API to demonstrate wrapping a local library that calls a remote server.",
    version="1.0.0",
)

# --- Pydantic Models for Request/Response ---
class UserRequest(BaseModel):
    user_id: int

class PostRequest(BaseModel):
    post_id: int

class RemoteDataResponse(BaseModel):
    status: str
    data: dict

# --- Thread Pool for Synchronous Operations ---
# It's crucial to run synchronous (blocking) code in a separate thread pool
# when using an ASGI framework like FastAPI to avoid blocking the event loop.
# This pool will be used for my_local_library.get_user_data_sync
executor = concurrent.futures.ThreadPoolExecutor(max_workers=5) # Adjust max_workers as needed

# --- API Endpoints ---

@app.get("/")
async def read_root():
    # Define paths for input and output directories
    INBOX_DIR = "./dr-egeria-inbox"
    OUTBOX_DIR = "./dr-egeria-outbox"
    VIEW_SERVER = "qs-view-server"
    URL = "https://localhost:9443"
    USER = "erinoverview"
    PWD = "secret"


    return {"message": "Welcome to the Local Library Wrapper API!"}

@app.post("/users/data_sync", response_model=RemoteDataResponse)
async def get_user_data_endpoint(request: UserRequest):
    """
    Fetches user data using a synchronous call to the local library.
    This call is run in a thread pool to avoid blocking FastAPI's event loop.
    """
    try:
        # Run the synchronous function in the thread pool
        # This makes the synchronous call non-blocking for FastAPI's event loop
        user_data = await asyncio.get_event_loop().run_in_executor(
            executor,
            simulated_pyegeria.get_user_data_sync,
            request.user_id
        )
        return RemoteDataResponse(status="success", data=user_data)
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to retrieve user data: {e}"
        )
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )

@app.post("/posts/data_async", response_model=RemoteDataResponse)
async def get_post_data_endpoint(request: PostRequest):
    """
    Fetches post data using an asynchronous call to the local library.
    This call is naturally non-blocking.
    """
    try:
        # Directly await the asynchronous function
        post_data = await simulated_pyegeria.get_post_data_async(request.post_id)
        return RemoteDataResponse(status="success", data=post_data)
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to retrieve post data: {e}"
        )
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )

# --- Shutdown Hook (Optional but good practice for thread pools) ---
@app.on_event("shutdown")
async def shutdown_event():
    """Shuts down the thread pool when the application stops."""
    executor.shutdown(wait=True)
    print("Thread pool shut down.")