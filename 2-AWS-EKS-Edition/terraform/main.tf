# 2-AWS-EKS-Edition/terraform/main.tf
module "networking" {
  source        = "../../terraform/modules/networking"
  provider_type = "aws"
  environment   = "production"
  vpc_cidr      = "10.0.0.0/16"
}

module "postgres" {
  source        = "../../terraform/modules/postgres"
  provider_type = "aws"
  environment   = "production"
}

module "secrets" {
  source        = "../../terraform/modules/secrets"
  provider_type = "aws"
  environment   = "production"
  secret_name   = "db-password"
  secret_value  = module.postgres.db_password
}

module "k8s_cluster" {
  source        = "../../terraform/modules/k8s-cluster"
  provider_type = "aws"
  environment   = "production"
  cluster_name  = "aegis-eks-cluster"
  subnet_ids    = module.networking.private_subnet_ids
  cluster_role_arn = var.eks_role_arn # defined in variables.tf
}

module "observability" {
  source        = "../../terraform/modules/observability"
  provider_type = "aws"
  environment   = "production"
}
