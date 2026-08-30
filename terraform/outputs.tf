output "firehose_delivery_stream_name" {
  description = "Amazon Data Firehose stream used by the SentinelAI ingestion mirror."
  value       = aws_kinesis_firehose_delivery_stream.sentinel_telemetry.name
}

output "firehose_delivery_stream_arn" {
  description = "ARN of the SentinelAI Amazon Data Firehose stream."
  value       = aws_kinesis_firehose_delivery_stream.sentinel_telemetry.arn
}

output "firehose_writer_policy_arn" {
  description = "IAM policy ARN to attach to the SentinelAI workload role (for example an EKS IRSA role)."
  value       = aws_iam_policy.firehose_writer.arn
}

output "telemetry_bucket_name" {
  description = "S3 bucket receiving compressed SentinelAI telemetry objects."
  value       = aws_s3_bucket.sentinel_logs.bucket
}

output "telemetry_bucket_arn" {
  description = "ARN of the S3 telemetry bucket."
  value       = aws_s3_bucket.sentinel_logs.arn
}
