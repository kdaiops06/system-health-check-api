variable "project_id" {
  description = "Google Cloud project ID."
  type        = string
}

variable "region" {
  description = "Google Cloud region."
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "Cloud Run service name."
  type        = string
  default     = "system-health-check-api"
}

variable "artifact_registry_repository" {
  description = "Artifact Registry repository name."
  type        = string
  default     = "system-health-check"
}

variable "image_name" {
  description = "Container image name."
  type        = string
  default     = "system-health-check-api"
}