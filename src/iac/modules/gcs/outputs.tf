output "bucket" {
  description = "The created storage bucket"
  value       = google_storage_bucket.create_gcs_bucket
}

output "name" {
  description = "Bucket name."
  value       = google_storage_bucket.create_gcs_bucket.name
}