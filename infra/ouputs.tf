output "workspace_id" {
  description = "The ID of the Azure Machine Learning workspace."
  value       = azurerm_machine_learning_workspace.main.id
}

output "workspace_name" {
  description = "The name of the Azure Machine Learning workspace."
  value       = azurerm_machine_learning_workspace.main.name
}