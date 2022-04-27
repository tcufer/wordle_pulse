variable "region" {
  type    = string
  default = "eu-central-1"
}

variable "profile" {
  type    = string
  default = ""
}

variable "s3_bucket_name" {
  type    = string
  default = "wordle-pulse"
}

variable "app_name" {
  type = string
  default = "wordle_pulse"
}
