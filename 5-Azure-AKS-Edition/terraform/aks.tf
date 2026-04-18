resource "azurerm_resource_group" "rg" {
  name     = "mcp-ai-platform-rg"
  location = "East US"
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = "mcp-aks-cluster"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "mcp"

  default_node_pool {
    name       = "system"
    node_count = 2
    vm_size    = "Standard_DS2_v2" # 2 vCPU, 7GB RAM
  }

  # Azure native highly-secure role-based access identity hook
  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
  }

  tags = {
    Environment = "Production"
  }
}

output "kube_config" {
  value     = azurerm_kubernetes_cluster.aks.kube_config_raw
  sensitive = true
}
