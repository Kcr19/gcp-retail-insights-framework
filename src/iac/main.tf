locals {
  env                 = "dev"
  location            = "US"
  friendly_name       = "rcim-datasets"
  dataset_description = "Datasets for Retail CIM"
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

# Create random ids for bucket name, id
resource "random_id" "id" {
  byte_length = 4
  prefix      = "rcim"
}

# Create buckets
module "gcs" {
  project       = var.project
  for_each = toset(["${var.project}_retail_if_9raw",
  "${var.project}_retail_if_9sample"])
  source              = "./modules/gcs"
  name                = each.value
  location            = local.location
  bucket_level_access = true
  versioning          = true
  environment         = "dev"
}

# Create bigquery
module "create_bq_datasets" {
  source        = "./modules/bq_dataset"
  count         = length(var.rcim_dataset)
  dataset_id    = var.rcim_dataset[count.index]["id"]
  friendly_name = local.friendly_name
  description   = local.dataset_description
  location      = var.rcim_dataset[count.index]["location"]
  project       = var.project
  environment  = local.env
  project_name = var.project

}

# Create tables
module "create_bq_tables" {
  source       = "./modules/bq_tables"
  count        = length(var.rcim_table)
  project      = var.project
  dataset_id   = var.rcim_table[count.index]["dataset_id"]
  table_id     = var.rcim_table[count.index]["table_id"]
  schema       = file("./table_schemas/${var.rcim_table[count.index]["schema_id"]}")
  depends_on   = [module.create_bq_datasets.bq_dataset_id]
  environment  = local.env
  project_name = var.project
}