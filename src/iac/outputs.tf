output "names" {
  description = "Bucket names."
  value = { for name, bucket in module.gcs :
    name => bucket.name
  }
}