# Aegis: Technical Explanation & Logic Flow

This document explains the internal logic and "wire-up" of the Aegis MCP-AI-Server.

## 1. The MCP Request Lifecycle
When an AI Agent (e.g., Claude) sends a command:
1. **Transport**: The request arrives at the `mcp-server` via SSE or stdio.
2. **Security**: The `mcp-server` validates the JWT and runs the **DLP Processor** to redact any PII.
3. **Dispatch**: The request is translated into a JSON-RPC 2.0 call and forwarded to the **Control Plane**.
4. **Authz**: The Control Plane checks permissions using **OPA** and the RBAC database.
5. **Execution**: If authorized, the Control Plane interacts with the **Postgres** database or the **Serving API**.
6. **Metering**: The `mcp-server` calculates the token cost and records it asynchronously in the **Billing Ledger**.

## 2. Multi-Cloud Failover Logic
The `failover-controller` acts as a regional watchdog:
- It monitors the `/health` endpoint of the primary region (AWS).
- If the SLO drops below 99.9%, it triggers a **Traffic Shift** manifest in Istio.
- Traffic is rerouted to the secondary region (Oracle Cloud).

## 3. RAG Intelligence Flow
The `model-serving-api` uses a hybrid retrieval strategy:
- **Embedding**: Uses `BAAI/bge-small-en-v1.5` for state-of-the-art vectorization.
- **Persistence**: Vectors are stored in **Milvus** (Cloud) or **FAISS** (Local fallback).
- **Context Awareness**: The retrieval engine automatically shrinks or expands the `top_k` results based on the remaining context window of the LLM.

## 4. Operational Resilience
- **Argo Rollouts**: We use Canary deployments. A new version is only promoted to 100% if Prometheus metrics confirm that the success rate is >95% and latency is <500ms.
- **Chaos Mesh**: The system is continuously stressed with scheduled pod-kills and network latency injection to ensure self-healing logic works under pressure.

## 5. Directory Mapping
- `apps/`: The Python/Next.js source code.
- `terraform/modules/`: The reusable infrastructure components.
- `k8s/`: The Kubernetes manifests for security, GitOps, and chaos.
