# Phase 9: Local Verification Runbook (Minikube Edition)

This runbook outlines the required execution commands to deploy the **1-Local-VM-Edition** to a Minikube cluster acting as our initial edge validation node. By completing these steps, you will validate the ArgoCD synchronization, Istio mTLS boundary limits, and the Chaos Mesh failure tolerance logic.

> [!IMPORTANT]
> **Prerequisites:** Ensure you have an active Virtual Machine or local environment with **Docker**, **Minikube**, and **kubectl** installed before tracing this Runbook. The local Windows host currently detected does not have these containerization binaries natively linked. 

## 1. Boot up the Cluster
First, we spin up the lightweight Kubernetes cluster and enable the NGINX ingress:

```bash
minikube start --memory 8192 --cpus 4 --driver=docker
minikube addons enable ingress
```

## 2. Deploy Foundational Core
Deploy the Istio Control Plane via Helm to ensure the zero-trust `mtls-strict` and `istio-injection` namespaces are validated correctly.

```bash
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update
helm install istiod istio/istiod -n istio-system --create-namespace
helm install chaos-mesh chaos-mesh/chaos-mesh -n chaos-testing --create-namespace --set chaosDaemon.runtime=containerd --set chaosDaemon.socketPath=/run/containerd/containerd.sock
```

## 3. Apply the AI Control Plane
Because our Kubernetes manifests are segmented gracefully, we can deploy the workloads natively:

```bash
cd "The MCP+AI Project/1-Local-VM-Edition"
kubectl apply -f k8s/security
kubectl apply -f k8s/apps
```

## 4. Trigger the Chaos Network
Verify the API can withstand the 50ms latency block across the nodes:

```bash
kubectl describe networkchaos model-serving-network-delay -n default
# Observe testing logs in the target pod:
kubectl logs -l app=model-serving-api
```

> [!TIP]
> The Python fastAPI tests are also successfully verifying the application internals natively. Run `pytest tests/ -v` to observe the boundary endpoints returning HTTP 200s!
