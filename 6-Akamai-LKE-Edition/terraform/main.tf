# 6-Akamai-LKE-Edition/terraform/main.tf
module "networking" {
  source        = "../../terraform/modules/networking"
  provider_type = "akamai"
  environment   = "production"
}

module "postgres" {
  source        = "../../terraform/modules/postgres"
  provider_type = "akamai"
  environment   = "production"
}

module "k8s_cluster" {
  source        = "../../terraform/modules/k8s-cluster"
  provider_type = "akamai"
  environment   = "production"
  cluster_name  = "aegis-lke-cluster"
}
