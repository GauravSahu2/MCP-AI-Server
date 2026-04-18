resource "linode_lke_cluster" "mcp_cluster" {
  label       = "mcp-ai-platform"
  k8s_version = "1.28"
  region      = "us-east"
  tags        = ["ai", "production"]

  # Linode Kubernetes Engine (LKE) is incredibly cost-effective.
  # We deploy 3 standard instances for our FAANG-grade setup.
  pool {
    type  = "g6-standard-2" # 2 CPU, 4GB RAM 
    count = 3
  }
}

# The kubeconfig is natively exported by the Linode Terraform provider!
output "kubeconfig" {
  value     = base64decode(linode_lke_cluster.mcp_cluster.kubeconfig)
  sensitive = true
}

output "api_endpoints" {
  value = linode_lke_cluster.mcp_cluster.api_endpoints
}
