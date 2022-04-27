
variable "app_name" {
  type = string
}

variable "s3_bucket_name" {
  type = string
}

# variable "kinesis_visibility_timeout_seconds" {
#   default = 30
# }

# variable "kinesis_kms_data_key_reuse_period_seconds" {
#   default = 300
# }

# variable "kinesis_delay_seconds" {
#   default = 90
# }

# variable "kinesis_max_message_size" {
#   default = 2048
# }

# variable "kinesis_message_retention_seconds" {
#   default = 86400
# }

# variable "kinesis_receive_wait_time_seconds" {
#   default = 10
# }

variable "kinesis_shard_count" {
  default = 1
}

variable "kinesis_retention_period" {
  default = 24
}

variable "kinesis_encryption_type" {
  type    = string
  default = "NONE"
}

variable "kinesis_shard_level_metrics" {
  type = list(any)
  default = [
    "IncomingBytes",
    "OutgoingBytes",
  ]
}

variable "kinesis_destination" {
  type    = string
  default = "s3"
}

variable "kinesis_buffer_size" {
  default = 10
}

variable "kinesis_buffer_interval" {
  default = 400
}

variable "kinesis_compression_format" {
  type    = string
  default = "ZIP"
}

