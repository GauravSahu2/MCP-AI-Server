terraform {
  required_providers {
    linode = {
      source  = "linode/linode"
      version = "~> 2.8.0"
    }
  }
}

provider "linode" {
  token = var.linode_token
}

variable "linode_token" {
  sensitive = true
}
