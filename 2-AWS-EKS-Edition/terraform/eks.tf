module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.16.0"

  cluster_name    = "mcp-cluster"
  cluster_version = "1.28"

  cluster_endpoint_public_access  = true

  vpc_id                   = module.vpc.vpc_id
  subnet_ids               = module.vpc.private_subnets
  control_plane_subnet_ids = module.vpc.private_subnets

  # OIDC provider for IRSA (IAM Roles for Service Accounts)
  enable_irsa = true

  eks_managed_node_groups = {
    general = {
      min_size     = 2
      max_size     = 5
      desired_size = 2

      instance_types = ["t3.medium"]
      capacity_type  = "ON_DEMAND"
    }
    
    # Dedicated nodes for high-compute AI Model Serving
    inference = {
      min_size     = 1
      max_size     = 3
      desired_size = 1

      instance_types = ["t3.large"] # Switch to g4dn.xlarge for real GPUs
      capacity_type  = "ON_DEMAND"
      
      taints = {
        dedicated = {
          key    = "node.kubernetes.io/role"
          value  = "inference"
          effect = "NO_SCHEDULE"
        }
      }
    }
  }

  tags = {
    Environment = "production"
    Project     = "mcp-ai-platform"
  }
}
