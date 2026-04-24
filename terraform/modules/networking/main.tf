# terraform/modules/networking/main.tf
variable "provider_type" {
  type = string
}

variable "environment" {
  type = string
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

# AWS VPC Example
resource "aws_vpc" "main" {
  count                = var.provider_type == "aws" ? 1 : 0
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  tags = {
    Name        = "aegis-${var.environment}-vpc"
    Environment = var.environment
  }
}

# AWS Private Subnets
resource "aws_subnet" "private" {
  count             = var.provider_type == "aws" ? 2 : 0
  vpc_id            = aws_vpc.main[0].id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  tags = {
    Name = "aegis-${var.environment}-private-${count.index}"
  }
}

# OCI VCN (Oracle Free)
resource "oci_core_vcn" "main" {
  count          = var.provider_type == "oci" ? 1 : 0
  compartment_id = var.compartment_id
  cidr_block     = var.vpc_cidr
  display_name   = "aegis-${var.environment}-vcn"
  dns_label      = "aegis"
}

output "vpc_id" {
  value = var.provider_type == "aws" ? aws_vpc.main[0].id : (var.provider_type == "oci" ? oci_core_vcn.main[0].id : null)
}
