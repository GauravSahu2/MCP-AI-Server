# apps/mcp-server/main.py
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
import asyncio, json, uuid, os, httpx
import redis.asyncio as redis
from handlers.initialize import handle_initialize
from handlers.tools import handle_tools_list, handle_tools_call
from handlers.resources import handle_resources_list, handle_resources_read
from security.dlp import dlp_processor
from security.tracing import setup_tracing
from security.metering import cost_meter
from fastapi.security import HTTPBearer

bearer = HTTPBearer()
app = FastAPI(title="Aegis MCP Server", description="High-Assurance JSON-RPC 2.0 over SSE")

# Initialize OpenTelemetry
setup_tracing(app, "aegis-mcp-server")

# Initialize Redis for rate limiting (Phase 7)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(REDIS_URL)

CONTROL_PLANE_URL = os.getenv("CONTROL_PLANE_URL", "http://localhost:8000")

# ── Phase 3: Stateful Cost Metering Background Task ──────────────────────────

async def record_usage(tenant_id: str, tokens: int, cost: float, auth_token: str):
    try:
        async with httpx.AsyncClient() as client:
            # Pushes usage to Control Plane ledger
            headers = {"Authorization": f"Bearer {auth_token}"}
            await client.post(
                f"{CONTROL_PLANE_URL}/api/v1/billing/usage",
                json={"tenant_id": tenant_id, "tokens": tokens, "cost": cost},
                headers=headers
            )
    except Exception as e:
        print(f"Error recording usage: {e}")

# ── JSON-RPC 2.0 Dispatcher ──────────────────────────────────────────────────

async def dispatch(request_body: dict, tenant_id: str, auth_token: str) -> dict:
    # ── Phase 7: Resilience Layer (Redis Token Quota) ────────────────────────
    try:
        current_usage = await redis_client.incrby(f"quota:{tenant_id}", 1)
        if current_usage == 1:
            await redis_client.expire(f"quota:{tenant_id}", 60) # 1 min rolling window
        if current_usage > 100: # Max 100 req/min
            raise HTTPException(status_code=429, detail="Tenant rate limit exceeded")
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        print(f"Redis Quota Error: {e}") # Fail open if Redis is down, but log it

    # ── Phase 2/3/6: DLP + Metering ──────────────────────────────────────────
    body_str = json.dumps(request_body)
    scrubbed_body_str, pii_found = dlp_processor.redact(body_str)
    if pii_found:
        request_body = json.loads(scrubbed_body_str)
    
    tokens = cost_meter.estimate_tokens(scrubbed_body_str)
    cost = cost_meter.calculate_cost(tokens)

    # Fire-and-forget ledger write (Phase 3)
    asyncio.create_task(record_usage(tenant_id, tokens, cost, auth_token))

    method = request_body.get("method")
    params = request_body.get("params", {})
    req_id = request_body.get("id")

    handlers = {
        "initialize":          lambda p: handle_initialize(p),
        "tools/list":          lambda p: handle_tools_list(p),
        "tools/call":          lambda p: handle_tools_call(p, tenant_id, auth_token),
        "resources/list":      lambda p: handle_resources_list(p),
        "resources/read":      lambda p: handle_resources_read(p),
    }

    handler = handlers.get(method)
    if not handler:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}

    try:
        result = await handler(params)
        return {"jsonrpc": "2.0", "id": req_id, "result": result}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32603, "message": str(e)}}

# ── Transport Endpoints ──────────────────────────────────────────────────────

@app.get("/sse")
async def sse_endpoint(request: Request):
    async def event_generator():
        yield {"event": "endpoint", "data": json.dumps({"uri": "/messages"})}
        while True:
            if await request.is_disconnected(): break
            await asyncio.sleep(15)
            yield {"event": "ping", "data": ""}
    return EventSourceResponse(event_generator())

@app.post("/messages")
async def messages_endpoint(request: Request, token=Depends(bearer)):
    # In a real environment, we would decode the token here to get tenant_id
    # For now, we'll extract it from the token payload (Phase 2)
    from auth.jwt import verify_token
    payload = verify_token(token.credentials)
    
    body   = await request.json()
    result = await dispatch(body, payload.tenant_id, token.credentials)
    return result

@app.get("/health")
def health(): return {"status": "ok"}
