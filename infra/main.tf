data "azurerm_client_config" "current" {}

resource "random_string" "main" {
  length  = 8
  upper   = false
  lower = true
  special = false
  numeric = true
}

resource "azurerm_resource_group" "main" {
  name     = "${var.resource_group_prefix}${random_string.main.result}"
  location = var.region
}

resource "azurerm_storage_account" "main" {
  name                     = "${var.storage_account_name}${random_string.main.result}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_key_vault" "main" {
  name                        = "${var.key_vault_name}${random_string.main.result}"
  resource_group_name         = azurerm_resource_group.main.name
  location                    = azurerm_resource_group.main.location
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "standard"
}

resource "azurerm_application_insights" "main" {
  name                = "${var.app_insights_name}${random_string.main.result}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  application_type    = "web"
}

# resource "azurerm_container_registry" "main" {
#   name                     = var.container_registry_name
#   resource_group_name      = azurerm_resource_group.main.name
#   location                 = azurerm_resource_group.main.location
#   sku                      = "Basic"
#   admin_enabled            = true
# }

resource "azurerm_machine_learning_workspace" "main" {
  name                = "${var.workspace_name}${random_string.main.result}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  application_insights_id = azurerm_application_insights.main.id
  key_vault_id            = azurerm_key_vault.main.id
  storage_account_id      = azurerm_storage_account.main.id
  public_network_access_enabled = true

  identity {
    type = "SystemAssigned"
  }
}