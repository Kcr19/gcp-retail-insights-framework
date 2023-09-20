resource "google_storage_bucket" "create_gcs_bucket" {
  name                        = var.name
  location                    = var.location
  project                     = var.project
  uniform_bucket_level_access = var.bucket_level_access
  force_destroy = true
  versioning {
    enabled = var.versioning
  }
  labels = {
    environment  = var.environment
    project_name = var.project
  }
}