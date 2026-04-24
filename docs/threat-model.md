# Aegis MCP Threat Model (STRIDE)

This document establishes the security baseline for the Aegis MCP platform using the STRIDE methodology.

| Category | Threat | Aegis Mitigation Strategy |
| :--- | :--- | :--- |
| **S**poofing | Rogue service claims to be `model-serving-api` | Istio STRICT mTLS (Phase 3), JWT auth on all endpoints, PeerAuthentication. |
| **T**ampering | Model weights or data modified in transit | SHA-256 checksums on artifacts, S3 object lock, encrypted data volumes. |
| **R**epudiation | Tenant denies calling a sensitive action | Immutable audit logs (Phase 2), append-only Postgres tables, CloudTrail. |
| **I**nformation Disclosure | Prompt contains PII reaching logs | PII Redaction Layer (Phase 6), OTel log scrubbing, DLP processors. |
| **D**enial of Service | Tenant floods server with tool calls | Rate limiting per tenant (Phase 9), HPA scale-out, Chaos validation (Phase 7). |
| **E**levation of Privilege | Low-privilege user triggers Chaos | Fine-grained RBAC middleware (Phase 2), OPA policy enforcement (Phase 6). |

## Security Anchors
- **Identity**: Standardized JWT + Tenant ID.
- **Transport**: Encrypted by default (mTLS).
- **Audit**: Every mutation must be logged.
- **Policy**: Declarative authorization (OPA).
