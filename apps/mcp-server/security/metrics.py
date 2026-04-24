# apps/mcp-server/security/metrics.py
from prometheus_client import Counter, Histogram, generate_latest
from fastapi import Response

# RED Metrics
REQUEST_COUNT = Counter(
    "aegis_requests_total", 
    "Total request count", 
    ["method", "endpoint", "tenant_id"]
)

REQUEST_LATENCY = Histogram(
    "aegis_request_latency_seconds", 
    "Request latency in seconds", 
    ["method", "endpoint"]
)

ERROR_COUNT = Counter(
    "aegis_errors_total", 
    "Total error count", 
    ["method", "endpoint", "error_code"]
)

def metrics_endpoint():
    return Response(content=generate_latest(), media_type="text/plain")
