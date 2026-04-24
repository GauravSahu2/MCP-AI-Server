# 4-GCP-GKE-Edition/terraform/main.tf
module "networking" {
  source        = "../../terraform/modules/networking"
  provider_type = "gcp"
  environment   = "production"
}

module "postgres" {
  source        = "../../terraform/modules/postgres"
  provider_type = "gcp"
  environment   = "production"
}

module "k8s_cluster" {
  source        = "../../terraform/modules/k8s-cluster"
  provider_type = "gcp"
  environment   = "production"
  cluster_name  = "aegis-gke-cluster"
  region        = var.region
}
