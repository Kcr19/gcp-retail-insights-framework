resource "google_bigquery_dataset" "create_datasets" {
  dataset_id    = var.dataset_id
  friendly_name = var.friendly_name
  description   = var.description
  location      = var.location
  project       = var.project
  labels = {
    environment  = var.environment
    project_name = var.project_name
  }
}