# The AI Platform Runbook

This runbook acts as your operational manual to deploy the High-Assurance AI Infrastructure, access the new Next.js User Dashboard, and manage heterogeneous AI Models running across the Control Plane.

## 1. Local Cluster Boot-Up
Follow these steps to deploy the foundation elements to a local Kubernetes environment (Minikube). 

```bash
# 1. Initialize the Cluster
minikube start --memory 8192 --cpus 4 --driver=docker

# 2. Deploy Network and Security Backbone (Istio & Chaos Mesh)
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update
helm install istiod istio/istiod -n istio-system --create-namespace
helm install chaos-mesh chaos-mesh/chaos-mesh -n chaos-testing --create-namespace

# 3. Apply Custom AI Applications
kubectl apply -f k8s/security
kubectl apply -f k8s/apps
```

## 2. Dashboard Interaction (Frontend)
The platform now includes a rich Next.js Glassmorphic Dashboard allowing interactive model management and inference. Once the pods are healthy, the Service is mapped to NodePort `30080`.

```bash
# Verify Pods are Running
kubectl get pods -n default

# Access the Dashboard (Minikube Tunnel)
minikube service mcp-dashboard --url
# Alternatively, open your browser to http://127.0.0.1:30080
```

## 3. Advanced Multi-Model Ecosystem Integration
The Model Control Plane serves as the universal source of truth connecting various specialized models. Different AI environments seamlessly synchronize with this central plane using standardized REST payloads.

### How it Works
When a new model is booted anywhere in your architecture (AWS SageMaker, HuggingFace Inference Endpoints, Llama 3 Local, OpenAI APIs), it MUST ping the Control Plane Registration API.

#### 1. Registering Local Open-Source Models (e.g., Llama 3 or Mistral)
When running your own instance using vLLM or Ollama, run a sidecar webhook that emits this payload to `http://mcp-dashboard:30080/api/v1/models`:
```json
{
  "name": "llama-3-8b-instruct",
  "version": "v1.0",
  "description": "Local low-latency instruction tuned model",
  "framework": "vLLM",
  "s3_uri": "local://ollama/llama3"
}
```

#### 2. Registering Cloud API Ensembles (e.g., OpenAI / Gemini API)
If the Control plane handles remote LLMs, register an API wrapper identifier to orchestrate rate limits properly:
```json
{
  "name": "gpt-4-turbo",
  "version": "2024-04",
  "description": "Remote High-Intelligence LLM via Azure/OpenAI",
  "framework": "OpenAI API",
  "s3_uri": "api://openai.com/v1/"
}
```

#### Managing Model Topologies
Once registered, the Control Plane allocates a UUID. Through the Dashboard, human developers can assign status tags:
- **`REGISTERED`**: Awaiting validation.
- **`STAGING`**: Currently undergoing Chaos Mesh testing payload injection.
- **`PRODUCTION`**: Route active user traffic using Istio traffic-shifting to this UUID. 

By implementing this agnostic JSON payload registry, you guarantee your High-Assurance Architecture remains modular—you can swap Llama for OpenAI internally without breaking the RAG API endpoints.
