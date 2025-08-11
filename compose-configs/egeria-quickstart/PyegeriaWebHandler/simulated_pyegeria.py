# my_local_library.py
import time
import random
import asyncio
import httpx # For async HTTP requests (install: pip install httpx)
import requests # For sync HTTP requests (install: pip install requests)

# For demonstration, let's assume this comes from an environment variable
REMOTE_SERVER_BASE_URL = "https://jsonplaceholder.typicode.com" # A public API for testing

def _simulate_remote_call(delay_seconds: float = 0.5, fail_chance: float = 0.1):
    """Simulates a call to a remote server with a delay and a chance of failure."""
    time.sleep(delay_seconds) # Simulate network latency
    if random.random() < fail_chance:
        raise ConnectionError("Simulated remote server connection failed!")
    return {"status": "success", "data": "Remote data fetched."}

async def _simulate_async_remote_call(delay_seconds: float = 0.5, fail_chance: float = 0.1):
    """Simulates an async call to a remote server with a delay and a chance of failure."""
    await asyncio.sleep(delay_seconds) # Simulate async network latency
    if random.random() < fail_chance:
        raise ConnectionError("Simulated async remote server connection failed!")
    return {"status": "success", "data": "Async remote data fetched."}

# --- Synchronous function that calls a remote server ---
def get_user_data_sync(user_id: int):
    """
    Synchronously fetches user data from a remote server.
    This simulates your existing local library's synchronous call.
    """
    print(f"Local Library (Sync): Fetching data for user {user_id}...")
    try:
        # Simulate an actual HTTP GET request using 'requests'
        response = requests.get(f"{REMOTE_SERVER_BASE_URL}/users/{user_id}", timeout=5)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        print(f"Local Library (Sync): Successfully fetched data for user {user_id}.")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Local Library (Sync) Error: Failed to fetch data for user {user_id}: {e}")
        raise ConnectionError(f"Failed to connect to remote server: {e}")

# --- Asynchronous function that calls a remote server ---
async def get_post_data_async(post_id: int):
    """
    Asynchronously fetches post data from a remote server.
    This demonstrates how an async local library function would work.
    """
    print(f"Local Library (Async): Fetching data for post {post_id}...")
    async with httpx.AsyncClient() as client:
        try:
            # Simulate an actual HTTP GET request using 'httpx'
            response = await client.get(f"{REMOTE_SERVER_BASE_URL}/posts/{post_id}", timeout=5)
            response.raise_for_status() # Raise HTTPStatusError for bad responses (4xx or 5xx)
            data = response.json()
            print(f"Local Library (Async): Successfully fetched data for post {post_id}.")
            return data
        except httpx.RequestError as e:
            print(f"Local Library (Async) Error: Failed to fetch data for post {post_id}: {e}")
            raise ConnectionError(f"Failed to connect to remote server: {e}")