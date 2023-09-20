# Create multiple BQ Tables
resource "google_bigquery_table" "create_tables" {
  project             = var.project
  dataset_id          = var.dataset_id
  table_id            = var.table_id
  schema              = var.schema
  depends_on          = [var.dataset_id]
  deletion_protection = false
  labels = {
    environment  = var.environment
    project_name = var.project_name
  }
}