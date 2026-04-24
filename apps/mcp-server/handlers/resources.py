# apps/mcp-server/handlers/resources.py

RESOURCES = [
    {
        "uri": "aegis://models/catalog",
        "name": "Model Catalog",
        "description": "Registry of all models",
        "mimeType": "application/json"
    }
]

async def handle_resources_list(params: dict) -> dict:
    return {"resources": RESOURCES}

async def handle_resources_read(params: dict) -> dict:
    uri = params.get("uri")
    return {
        "contents": [{
            "uri": uri,
            "mimeType": "application/json",
            "text": "{\"models\": []}"
        }]
    }
