import json
import httpx
import os
from security.resilience import serving_breaker

# Control Plane internal URL
CONTROL_PLANE_URL = os.getenv("CONTROL_PLANE_URL", "http://model-control-plane.default.svc.cluster.local:8000")

TOOLS = [
    {
        "name": "list_models",
        "description": "List all registered AI models for the tenant.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["staging", "production", "archived"]}
            }
        }
    },
    {
        "name": "promote_model",
        "description": "Promote a model version to production.",
        "inputSchema": {
            "type": "object",
            "required": ["model_id"],
            "properties": {
                "model_id": {"type": "string"},
                "reason": {"type": "string"}
            }
        }
    }
]

async def handle_tools_list(params: dict) -> dict:
    return {"tools": TOOLS}

@serving_breaker
async def handle_tools_call(params: dict, tenant_id: str, auth_token: str) -> dict:
    name = params.get("name")
    args = params.get("arguments", {})

    headers = {"Authorization": f"Bearer {auth_token}"}
    
    async with httpx.AsyncClient() as client:
        if name == "list_models":
            resp = await client.get(
                f"{CONTROL_PLANE_URL}/api/v1/models",
                headers=headers
            )
            return {
                "content": [{"type": "text", "text": json.dumps(resp.json())}],
                "isError": resp.status_code >= 400
            }
            
        elif name == "promote_model":
            resp = await client.put(
                f"{CONTROL_PLANE_URL}/api/v1/models/{args['model_id']}/status",
                json={"status": "PRODUCTION"},
                headers=headers
            )
            return {
                "content": [{"type": "text", "text": json.dumps(resp.json())}],
                "isError": resp.status_code >= 400
            }

    return {
        "content": [{"type": "text", "text": f"Tool {name} not found or not implemented."}],
        "isError": True
    }
