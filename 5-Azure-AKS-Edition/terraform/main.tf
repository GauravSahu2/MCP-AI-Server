# 5-Azure-AKS-Edition/terraform/main.tf
module "networking" {
  source        = "../../terraform/modules/networking"
  provider_type = "azure"
  environment   = "production"
}

module "postgres" {
  source        = "../../terraform/modules/postgres"
  provider_type = "azure"
  environment   = "production"
}

module "k8s_cluster" {
  source        = "../../terraform/modules/k8s-cluster"
  provider_type = "azure"
  environment   = "production"
  cluster_name  = "aegis-aks-cluster"
}
