variable "project_id" {
  default = "testvaluex"
}

variable "project" {

}

variable "new_project_name" {
  default = "new_project_value"
}

variable "rcim_dataset" {
  type = list(object({
    id       = string
    location = string
  }))
}

variable "rcim_table" {
  type = list(object({
    dataset_id = string
    table_id   = string
    schema_id  = string
  }))
}