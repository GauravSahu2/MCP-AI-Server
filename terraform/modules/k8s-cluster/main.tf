# terraform/modules/k8s-cluster/main.tf
variable "provider_type" {
  type = string
}

variable "environment" {
  type = string
}

variable "cluster_name" {
  type = string
}

# AWS EKS Cluster
resource "aws_eks_cluster" "main" {
  count    = var.provider_type == "aws" ? 1 : 0
  name     = var.cluster_name
  role_arn = var.cluster_role_arn

  vpc_config {
    subnet_ids = var.subnet_ids
  }
}

# Oracle Container Engine for Kubernetes (OKE)
resource "oci_containerengine_cluster" "main" {
  count          = var.provider_type == "oci" ? 1 : 0
  compartment_id = var.compartment_id
  vcn_id         = var.vcn_id
  name           = var.cluster_name
  kubernetes_version = "v1.28.2"

  options {
    service_lb_subnet_ids = var.lb_subnet_ids
  }
}

# GKE Autopilot (GCP)
resource "google_container_cluster" "main" {
  count            = var.provider_type == "gcp" ? 1 : 0
  name             = var.cluster_name
  location         = var.region
  enable_autopilot = true
}

output "cluster_endpoint" {
  value = var.provider_type == "aws" ? aws_eks_cluster.main[0].endpoint : (var.provider_type == "gcp" ? google_container_cluster.main[0].endpoint : null)
}
