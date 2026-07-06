output "cloud_run_url" {
  description = "Public URL of the Cloud Run service."
  value       = google_cloud_run_v2_service.app.uri
}

output "artifact_registry_repository" {
  description = "Name of the Artifact Registry repository."
  value       = google_artifact_registry_repository.app.repository_id
}
