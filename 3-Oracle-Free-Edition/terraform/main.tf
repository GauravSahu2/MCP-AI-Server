# 3-Oracle-Free-Edition/terraform/main.tf
module "networking" {
  source        = "../../terraform/modules/networking"
  provider_type = "oci"
  environment   = "production"
  compartment_id = var.compartment_id
}

module "postgres" {
  source        = "../../terraform/modules/postgres"
  provider_type = "oci"
  environment   = "production"
  compartment_id = var.compartment_id
}

module "secrets" {
  source        = "../../terraform/modules/secrets"
  provider_type = "oci"
  environment   = "production"
  secret_name   = "db-password"
  secret_value  = module.postgres.db_password
  compartment_id = var.compartment_id
  vault_id       = var.vault_id
  key_id         = var.key_id
}

module "k8s_cluster" {
  source        = "../../terraform/modules/k8s-cluster"
  provider_type = "oci"
  environment   = "production"
  cluster_name  = "aegis-oke-cluster"
  vcn_id         = module.networking.vpc_id
  lb_subnet_ids  = [module.networking.public_subnet_id]
  compartment_id = var.compartment_id
}
