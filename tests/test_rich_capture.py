import io
from contextlib import redirect_stdout
from rich.console import Console

def test_rich_capture():
    stdout_buf = io.StringIO()
    with redirect_stdout(stdout_buf):
        console = Console()
        console.print("Hello from [bold]Rich[/bold]!")
    
    output = stdout_buf.getvalue()
    print(f"Captured: {repr(output)}")
    if "Hello from Rich!" in output:
        print("SUCCESS: Rich output captured")
    else:
        print("FAILURE: Rich output NOT captured")

if __name__ == "__main__":
    test_rich_capture()
