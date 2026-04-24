# terraform/modules/observability/main.tf
variable "provider_type" {
  type = string
}

variable "environment" {
  type = string
}

# AWS CloudWatch Log Group
resource "aws_cloudwatch_log_group" "main" {
  count             = var.provider_type == "aws" ? 1 : 0
  name              = "/aegis/${var.environment}/logs"
  retention_in_days = 30
}

# GCP Cloud Monitoring Dashboard (Example)
resource "google_monitoring_dashboard" "aegis" {
  count          = var.provider_type == "gcp" ? 1 : 0
  dashboard_json = var.dashboard_json
}

# Shared Prometheus/Grafana Configuration (Local/Oracle/Akamai)
# In these editions, we deploy the stack via Helm in the cluster, 
# so the TF module might just provision a bucket for long-term storage (e.g. Thanos).

resource "aws_s3_bucket" "metrics_storage" {
  count  = var.provider_type == "aws" ? 1 : 0
  bucket = "aegis-${var.environment}-metrics"
}
