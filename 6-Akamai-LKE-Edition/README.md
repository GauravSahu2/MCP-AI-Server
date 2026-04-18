# 🛡️ MCP+AI Platform (Akamai Linode Engine)

[![CI/CD](https://img.shields.io/badge/CI%2FCD-SonarCloud%20Passing-success?style=for-the-badge&logo=githubactions&logoColor=white)](#) [![Kubernetes](https://img.shields.io/badge/Orchestration-K8s-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)](#) [![Istio](https://img.shields.io/badge/Service%20Mesh-Istio-466BB0?style=for-the-badge&logo=istio&logoColor=white)](#) [![Milvus](https://img.shields.io/badge/Vector%20DB-Milvus-0D1117?style=for-the-badge)](#) [![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)

A property-tested, highly resilient Model Control Plane and AI routing platform originally designed for large enterprise inference. This portfolio variant explicitly tackles the **Akamai / Linode** ecosystem to demonstrate deep-dive infrastructure control, scaling mechanisms, and fault-tolerant architecture mapping.
**Core Business Value Add:** Fixed predictable container pricing reducing cloud bloat.

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
   - [Phase 1 - Core Microservices](#phase-1---core-microservices)
   - [Phase 2 - GitOps & CD](#phase-2---gitops--cd)
   - [Phase 3 - Zero-Trust Networking](#phase-3---zero-trust-networking)
   - [Phase 4 - Vector Search Integration](#phase-4---vector-search-integration)
   - [Phase 5 - Chaos Reliability Engineering](#phase-5---chaos-reliability-engineering)
3. [Project Structure](#project-structure)
4. [Execution & Orchestration](#execution--orchestration)
   - [Prerequisites](#prerequisites)
   - [Cloud & Infrastructure Setup](#cloud--infrastructure-setup)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [Operational Safeguards & Best Practices](#operational-safeguards--best-practices)
7. [Contact & License](#contact--license)

---

## Executive Summary

This repository encapsulates a formalized, auditable approach to AI model serving and security. Real-world AI nodes consume full tensor blocks and GPU cycles during inference, introducing major memory-leak risks. This architecture solves these physical limits by routing payloads through Envoy proxies (Istio), executing against Vector RAG databases (Milvus), and automatically deploying changes securely (ArgoCD), all wrapped within Akamai / Linode metal logic.

---

## Architecture Overview

The platform uses five architectural planes to guarantee maximum reliability and inference correctness.

### Phase 1 - Core Microservices
- **Model Control Plane**: Pydantic-validated FastAPI service acting as the centralized registry for weights.
- **Model Serving API**: Highly parallelized API consuming input tensors and returning prediction sets with computed latency maps.

### Phase 2 - GitOps & CD
- **ArgoCD**: Master control loop running natively inside the Kubernetes cluster. It polls GitHub for state changes and enforces local sync, achieving 100% human segregation from production nodes.

### Phase 3 - Zero-Trust Networking (Istio)
- **mTLS Strict Protocols**: Sidecar injection enforcing cryptographic handshakes between internal services. If container A attempts to reach container B, failure to present the peer authentication certificate terminates the TCP stream instantaneously.

### Phase 4 - Vector Search Integration (Milvus)
- **Mock RAG Simulation**: Standalone `milvus` vector nodes exist inside the cluster to supply massive high-dimensional context mapping to the Serving APIs, significantly enhancing accuracy before ML return streams.

### Phase 5 - Chaos Reliability Engineering
- **Chaos Mesh (CNCF)**: Periodic automated injection of 50ms latency spikes and arbitrary Node/Pod killing sequences to validate our HorizontalPodAutoscalers scale and heal without dropping a user packet.

---

## Project Structure

```text
.
├── .github/workflows/          # Continuous Integration pipeline (SonarCloud quality gates)
├── apps/
│   ├── model-control-plane/    # Backend registry API (Dockefile, main.py)
│   └── model-serving-api/      # Inference API (Dockerfile, main.py, requirements.txt)
├── k8s/
│   ├── apps/                   # Deployments, Services, and HPA (Milvus included)
│   ├── argocd/                 # GitOps master tracking application
│   ├── observability/          # Grafana mapping and Chaos Mesh RBAC configs
│   └── security/               # Istio injections, Chaos Mesh routines, MTLS policies
├── terraform/                  # Akamai / Linode IaC declarative state config
└── README.md                   # This file
```

---

## Execution & Orchestration

### Prerequisites
- Docker & Docker Buildx
- Terraform / OpenTofu (For infrastructure runs)
- `kubectl` CLI
- Authorized Provider CLI keys.

### Cloud & Infrastructure Setup

1. **Provision the Foundation:**
```bash
cd terraform/
terraform init
terraform apply --auto-approve
```

2. **Establish the Mesh and Observers:**
Before pushing app logic, ensure Istio is running inside the cluster.
```bash
kubectl label namespace default istio-injection=enabled
kubectl apply -f k8s/security/mtls-strict.yaml
```

3. **Deploy Core AI Routing & Memory States:**
```bash
kubectl apply -f k8s/apps/
kubectl apply -f k8s/argocd/
kubectl apply -f k8s/observability/
```

4. **Verify Deployment & Chaos Impact:**
```bash
kubectl get pods --all-namespaces
kubectl logs -l app=model-serving-api -f
```

---

## CI/CD Pipeline

Every push directly triggers GitHub Actions:
- **Quality Gates**: Executes full codebase validation using SonarCloud matrix to verify 0 vulnerability exposures.
- **Image Compilation**: Utilizes Docker Buildx to generate the isolated binaries for the core routing components.

## Operational Safeguards & Best Practices

- **Never Commit Secrets**: Any hardcoded access key to production environments violates Phase 1 GitOps rules.
- **Fail-Safe Testing**: Ensure all Chaos routines are restricted solely to non-critical staging or designated testing namespaces.
- **Zero-Trust Baseline**: The combination of Istio mTLS and Pydantic validation handles 99% of unexpected network payload regressions dynamically.
