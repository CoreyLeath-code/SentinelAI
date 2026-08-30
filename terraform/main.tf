terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current" {}

locals {
  telemetry_bucket_name = var.telemetry_bucket_name != "" ? var.telemetry_bucket_name : "${var.project_name}-telemetry-${data.aws_caller_identity.current.account_id}-${var.aws_region}"
  common_tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
    Component = "telemetry"
  }
}

resource "aws_s3_bucket" "sentinel_logs" {
  bucket        = local.telemetry_bucket_name
  force_destroy = var.telemetry_bucket_force_destroy
  tags          = local.common_tags
}

resource "aws_s3_bucket_public_access_block" "sentinel_logs" {
  bucket = aws_s3_bucket.sentinel_logs.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "sentinel_logs" {
  bucket = aws_s3_bucket.sentinel_logs.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_versioning" "sentinel_logs" {
  bucket = aws_s3_bucket.sentinel_logs.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "sentinel_logs" {
  bucket = aws_s3_bucket.sentinel_logs.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "sentinel_logs" {
  bucket = aws_s3_bucket.sentinel_logs.id

  rule {
    id     = "expire-telemetry"
    status = "Enabled"

    filter {}

    expiration {
      days = var.telemetry_retention_days
    }
  }
}

resource "aws_ecr_repository" "sentinel_repo" {
  name                 = "${var.project_name}-repo"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "firehose" {
  name              = "/aws/firehose/${var.project_name}-telemetry"
  retention_in_days = 14
  tags              = local.common_tags
}

resource "aws_cloudwatch_log_stream" "firehose" {
  name           = "S3Delivery"
  log_group_name = aws_cloudwatch_log_group.firehose.name
}

data "aws_iam_policy_document" "firehose_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["firehose.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "firehose" {
  name               = "${var.project_name}-firehose-delivery"
  assume_role_policy = data.aws_iam_policy_document.firehose_assume_role.json
  tags               = local.common_tags
}

data "aws_iam_policy_document" "firehose_delivery" {
  statement {
    sid    = "S3BucketMetadata"
    effect = "Allow"
    actions = [
      "s3:GetBucketLocation",
      "s3:ListBucket",
      "s3:ListBucketMultipartUploads"
    ]
    resources = [aws_s3_bucket.sentinel_logs.arn]
  }

  statement {
    sid    = "S3ObjectDelivery"
    effect = "Allow"
    actions = [
      "s3:AbortMultipartUpload",
      "s3:PutObject"
    ]
    resources = ["${aws_s3_bucket.sentinel_logs.arn}/*"]
  }

  statement {
    sid     = "CloudWatchDeliveryLogs"
    effect  = "Allow"
    actions = ["logs:PutLogEvents"]
    resources = [
      "${aws_cloudwatch_log_group.firehose.arn}:*"
    ]
  }
}

resource "aws_iam_role_policy" "firehose_delivery" {
  name   = "${var.project_name}-firehose-delivery"
  role   = aws_iam_role.firehose.id
  policy = data.aws_iam_policy_document.firehose_delivery.json
}

resource "aws_kinesis_firehose_delivery_stream" "sentinel_telemetry" {
  name        = "${var.project_name}-telemetry"
  destination = "extended_s3"
  tags        = local.common_tags

  extended_s3_configuration {
    role_arn           = aws_iam_role.firehose.arn
    bucket_arn         = aws_s3_bucket.sentinel_logs.arn
    buffering_interval = 60
    buffering_size     = 5
    compression_format = "GZIP"

    prefix = "inference/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/hour=!{timestamp:HH}/"
    error_output_prefix = "errors/!{firehose:error-output-type}/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/"

    cloudwatch_logging_options {
      enabled         = true
      log_group_name  = aws_cloudwatch_log_group.firehose.name
      log_stream_name = aws_cloudwatch_log_stream.firehose.name
    }
  }

  depends_on = [aws_iam_role_policy.firehose_delivery]
}

data "aws_iam_policy_document" "firehose_writer" {
  statement {
    sid    = "PublishSentinelTelemetry"
    effect = "Allow"
    actions = [
      "firehose:PutRecord",
      "firehose:PutRecordBatch"
    ]
    resources = [aws_kinesis_firehose_delivery_stream.sentinel_telemetry.arn]
  }
}

resource "aws_iam_policy" "firehose_writer" {
  name        = "${var.project_name}-firehose-writer"
  description = "Allows SentinelAI ingestion workloads to publish telemetry to Amazon Data Firehose."
  policy      = data.aws_iam_policy_document.firehose_writer.json
  tags        = local.common_tags
}
