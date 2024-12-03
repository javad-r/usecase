data "azurerm_client_config" "current" {}

resource "random_string" "main" {
  length  = 8
  upper   = false
  lower   = true
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
  name                = "${var.key_vault_name}${random_string.main.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"
}

resource "azurerm_application_insights" "main" {
  name                = "${var.app_insights_name}${random_string.main.result}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  application_type    = "web"
}

resource "azurerm_container_registry" "main" {
  name                = var.container_registry_name
  resource_group_name = azurerm_resource_group.main.name
  location            = var.region
  sku                 = "Basic"
  admin_enabled       = true
}

resource "azurerm_machine_learning_workspace" "main" {
  name                = "${var.workspace_name}${random_string.main.result}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  container_registry_id         = azurerm_container_registry.main.id
  application_insights_id       = azurerm_application_insights.main.id
  key_vault_id                  = azurerm_key_vault.main.id
  storage_account_id            = azurerm_storage_account.main.id
  public_network_access_enabled = true

  identity {
    type = "SystemAssigned"
  }
}

# App Service Plan
resource "azurerm_service_plan" "main" {
  name                = "${var.app_service_plan_name}${random_string.main.result}"
  location            = var.region
  resource_group_name = azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}

# App Service
resource "azurerm_linux_web_app" "main" {
  name                = "${var.app_service_name}-${random_string.main.result}" # Unique name
  location            = var.region
  resource_group_name = azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  identity {
    type = "SystemAssigned"
  }

  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "AZURE_ML_ENDPOINT"                   = var.AZURE_ML_ENDPOINT
    AZURE_ML_API_KEY                        = var.AZURE_ML_API_KEY
    "API_KEY"                             = var.APP_SERVICE_API_KEY
  }

  site_config {
    always_on = true
    application_stack {
      docker_image_name = "myapp:latest"
      docker_registry_url = "https://${azurerm_container_registry.main.login_server}"
    }
  }
}

resource "azurerm_role_assignment" "acr_pull_app_service" {
  scope                = azurerm_container_registry.main.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_linux_web_app.main.identity[0].principal_id
  lifecycle { ignore_changes = [ principal_id ]}
}
