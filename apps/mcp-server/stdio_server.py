# apps/mcp-server/stdio_server.py
import sys, asyncio, json
from main import dispatch

async def stdio_loop():
    # Use standard input/output for JSON-RPC
    # Note: On Windows, we might need special handling for pipes
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await asyncio.get_event_loop().connect_read_pipe(lambda: protocol, sys.stdin)

    while True:
        line = await reader.readline()
        if not line:
            break
        try:
            request = json.loads(line.decode())
            response = await dispatch(request)
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
        except Exception as e:
            error = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(error) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(stdio_loop())
