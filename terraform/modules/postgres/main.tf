# terraform/modules/postgres/main.tf
variable "provider_type" {
  description = "Cloud provider type: aws | gcp | azure | oci | akamai | local"
  type        = string
}

variable "environment" {
  type    = string
  default = "staging"
}

resource "random_password" "db_password" {
  length  = 32
  special = true
}

# AWS RDS Example
resource "aws_db_instance" "main" {
  count               = var.provider_type == "aws" ? 1 : 0
  engine              = "postgres"
  engine_version      = "16.3"
  instance_class      = "db.t3.micro"
  allocated_storage   = 20
  storage_encrypted   = true
  deletion_protection = var.environment == "production" ? true : false
  skip_final_snapshot = var.environment == "production" ? false : true
  identifier          = "aegis-${var.environment}-db"
  password            = random_password.db_password.result
}

# GCP Cloud SQL Example
resource "google_sql_database_instance" "main" {
  count            = var.provider_type == "gcp" ? 1 : 0
  name             = "aegis-${var.environment}-db"
  database_version = "POSTGRES_15"
  settings {
    tier = "db-f1-micro"
  }
  root_password = random_password.db_password.result
}

# Oracle Autonomous Database (Always Free)
resource "oci_database_autonomous_database" "aegis_db" {
  count                    = var.provider_type == "oci" ? 1 : 0
  compartment_id           = var.compartment_id
  db_name                  = "aegisdb"
  cpu_core_count           = 1
  data_storage_size_in_tbs = 1
  is_free_tier             = true
  admin_password           = random_password.db_password.result
  db_workload              = "OLTP"
  is_auto_scaling_enabled  = false
}

output "db_password" {
  value     = random_password.db_password.result
  sensitive = true
}
