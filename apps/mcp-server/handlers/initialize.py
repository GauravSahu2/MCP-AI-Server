# apps/mcp-server/handlers/initialize.py

AEGIS_CAPABILITIES = {
    "protocolVersion": "2024-11-05",
    "capabilities": {
        "tools":     {"listChanged": True},
        "resources": {"subscribe": True, "listChanged": True},
        "prompts":   {"listChanged": True}
    },
    "serverInfo": {
        "name":    "Aegis MCP Control Plane",
        "version": "1.0.0"
    }
}

async def handle_initialize(params: dict) -> dict:
    client_version = params.get("protocolVersion", "")
    if client_version < "2024-11-05":
        raise ValueError(f"Unsupported protocol version: {client_version}")
    return AEGIS_CAPABILITIES
