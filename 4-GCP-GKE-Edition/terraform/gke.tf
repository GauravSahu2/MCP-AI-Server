# In GCP, Google has perfected Kubernetes with 'GKE Autopilot'.
# Unlike AWS EKS where we manage raw EC2 instances and node groups, 
# GKE Autopilot manages the entire node infrastructure abstractly. We only pay for the exact CPU/RAM the pod uses.

resource "google_compute_network" "vpc" {
  name                    = "mcp-gcp-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "mcp-subnet"
  region        = var.region
  network       = google_compute_network.vpc.name
  ip_cidr_range = "10.0.0.0/24"
}

resource "google_container_cluster" "primary" {
  name     = "mcp-gke-cluster"
  location = var.region

  # Enables GKE Autopilot - The ultimate serverless Kubernetes
  enable_autopilot = true

  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name

  # Enable Workload Identity for extremely secure pod-to-GCP-secret access
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }
}

output "kubernetes_cluster_name" {
  value       = google_container_cluster.primary.name
}
