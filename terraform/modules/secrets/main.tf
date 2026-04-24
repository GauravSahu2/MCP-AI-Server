# terraform/modules/secrets/main.tf
variable "provider_type" {
  type = string
}

variable "environment" {
  type = string
}

variable "secret_name" {
  type = string
}

variable "secret_value" {
  type      = string
  sensitive = true
}

# AWS Secrets Manager
resource "aws_secretsmanager_secret" "main" {
  count                   = var.provider_type == "aws" ? 1 : 0
  name                    = "aegis/${var.environment}/${var.secret_name}"
  recovery_window_in_days = 7
}

resource "aws_secretsmanager_secret_version" "main" {
  count         = var.provider_type == "aws" ? 1 : 0
  secret_id     = aws_secretsmanager_secret.main[0].id
  secret_string = var.secret_value
}

# OCI Vault Secret
resource "oci_vault_secret" "main" {
  count          = var.provider_type == "oci" ? 1 : 0
  compartment_id = var.compartment_id
  vault_id       = var.vault_id
  key_id         = var.key_id
  secret_name    = "aegis-${var.secret_name}"
  secret_content {
    content_type = "BASE64"
    content      = base64encode(var.secret_value)
  }
}
