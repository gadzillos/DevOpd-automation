variable "location" {
  type        = string
  default     = "Germany West Central"
  description = "default resources location"
}

variable "resource_group_name" {
  type        = string
  default     = "WildfyGroup"
  description = "resource group name"
}

variable "storage_account_name" {
  type        = string
  default     = "WildfyStorage"
  description = "storage account name"
}