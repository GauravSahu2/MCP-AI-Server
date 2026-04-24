# Aegis Operations Runbook

This runbook provides the standard operating procedures for deploying and managing the Aegis platform.

## 🛠 Prerequisites
- **Terraform** v1.5+
- **Kubectl**
- **Docker & Docker Compose**
- **Python 3.10+**

## 🚀 Deployment Procedures

### 1. Local Development (The Sandbox)
```bash
# Start the full stack
make deploy-local

# Bootstrap the database (Seeding Super Admin)
cd apps/model-control-plane && python bootstrap.py
```

### 2. AWS Production (High-Assurance)
```bash
# 1. Provision Infrastructure
cd 2-AWS-EKS-Edition/terraform && terraform apply

# 2. Setup GitOps
kubectl apply -f 2-AWS-EKS-Edition/k8s/argocd/root-app.yaml

# 3. Verify Health
kubectl get pods -n default
```

### 3. Oracle Failover (Sovereign Target)
```bash
cd 3-Oracle-Free-Edition/terraform && terraform apply
```

## 🌪 Chaos & Resilience Testing
To manually trigger a chaos experiment:
```bash
make chaos-inject
```
Check experiment status:
```bash
kubectl describe podchaos model-serving-kill
```

## 📊 Monitoring & Audit
- **Metrics**: Access Prometheus at `http://prometheus.aegis.ai`
- **Tracing**: Access Jaeger at `http://jaeger.aegis.ai`
- **Audit Logs**: Run `SELECT * FROM audit_logs;` in the Postgres database.

## 🆘 Troubleshooting
- **Database Connection**: Check `vault-agent` status for secret injection failures.
- **MCP connectivity**: Ensure the `CONTROL_PLANE_URL` environment variable is correctly set in the `mcp-server` deployment.
- **Redis Quota**: If you get a 429 error, check the `quota:tenant_id` key in Redis.
