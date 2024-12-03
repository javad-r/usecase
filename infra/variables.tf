variable "region" {
  type    = string
  default = "westeurope"
}

variable "resource_group_prefix" {
  type    = string
  default = "usecase"
}

variable "workspace_name" {
  description = "Name of the Azure Machine Learning workspace."
  type        = string
  default     = "usecasetest"
}

variable "storage_account_name" {
  description = "Name of the storage account used by the workspace."
  type        = string
  default     = "usecasetest"
}

variable "key_vault_name" {
  description = "Name of the Key Vault for workspace secrets."
  type        = string
  default     = "usecasetest"
}

variable "app_insights_name" {
  description = "Name of the Application Insights instance."
  type        = string
  default     = "usecasetest"
}

variable "container_registry_name" {
  description = "Name of the Azure Container Registry."
  type        = string
  default     = "usecasetest"
}

variable "app_service_plan_name" {
  description = "Name of the App service plan."
  type        = string
  default     = "usecasetest"
}

variable "app_service_name" {
  description = "Name of the App service."
  type        = string
  default     = "usecasetest"
}

variable "AZURE_ML_ENDPOINT" {
  description = "Azure ML endpoint."
  type        = string
}

variable "AZURE_ML_API_KEY" {
  description = "Azure ML API key."
  type        = string
}

variable "APP_SERVICE_API_KEY" {
  description = "API key for the App Service."
  type        = string
}
