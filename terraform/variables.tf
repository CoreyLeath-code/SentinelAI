variable "project_name" {
  description = "Prefix used for SentinelAI AWS resources."
  type        = string
  default     = "sentinelai"
}

variable "aws_region" {
  description = "AWS region for SentinelAI telemetry infrastructure."
  type        = string
  default     = "us-east-1"
}

variable "telemetry_bucket_name" {
  description = "Optional globally unique S3 bucket name. Leave empty to derive one from the AWS account and region."
  type        = string
  default     = ""
}

variable "telemetry_retention_days" {
  description = "Number of days to retain delivered telemetry objects in S3."
  type        = number
  default     = 30

  validation {
    condition     = var.telemetry_retention_days >= 1
    error_message = "telemetry_retention_days must be at least 1."
  }
}

variable "telemetry_bucket_force_destroy" {
  description = "Whether Terraform may delete the S3 bucket while it still contains telemetry objects."
  type        = bool
  default     = false
}
