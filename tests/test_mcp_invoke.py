import asyncio
import json
import sys
import os

async def test_mcp_local():
    # Use the script directory to find mcp_server.py
    mcp_server_path = "compose-configs/egeria-quickstart/PyegeriaWebHandler/mcp_server.py"
    
    # Define a markdown block to process
    markdown_block = "# View Glossaries\n___\n"
    
    # Prepare the JSON-RPC call for dr_egeria_run_block
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "dr_egeria_run_block",
            "arguments": {
                "markdown_block": markdown_block,
                "url": "https://localhost:9443", # Dummy URL
                "server_name": "qs-view-server",
                "user_id": "erinoverview",
                "user_pass": "secret",
                "directive": "display"
            }
        }
    }

    # Run the mcp_server.py using stdio
    # We need to simulate the environment variables if needed
    env = os.environ.copy()
    env["PYEGERIA_LOG_DIRECTORY"] = "/tmp/pyegeria_logs"
    env["EGERIA_ROOT_PATH"] = "/tmp/egeria_root"
    os.makedirs("/tmp/pyegeria_logs", exist_ok=True)
    os.makedirs("/tmp/egeria_root", exist_ok=True)

    proc = await asyncio.create_subprocess_exec(
        sys.executable, mcp_server_path,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env
    )

    # First, we need to handle the initialization
    init_request = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"}
        }
    }
    
    proc.stdin.write((json.dumps(init_request) + "\n").encode())
    await proc.stdin.drain()
    
    # Read initialize response
    line = await proc.stdout.readline()
    print(f"Init Response: {line.decode()}")

    # Send tool call
    proc.stdin.write((json.dumps(request) + "\n").encode())
    await proc.stdin.drain()

    # Read tool response
    line = await proc.stdout.readline()
    if line:
        print(f"Tool Response: {line.decode()}")
    else:
        print("No tool response")
        err = await proc.stderr.read()
        print(f"Stderr: {err.decode()}")

    proc.terminate()
    await proc.wait()

if __name__ == "__main__":
    asyncio.run(test_mcp_local())
