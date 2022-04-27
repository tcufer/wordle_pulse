resource "aws_kinesis_firehose_delivery_stream" "kinesis" {
  //A name to identify the stream
  name = "${var.app_name}_kinesis"

  //This is the destination to where the data is delivered
  destination = var.kinesis_destination

  s3_configuration {
    //The ARN of the AWS credentials.
    role_arn = aws_iam_role.kinesis.arn

    //The ARN of the S3 bucket
    bucket_arn = aws_s3_bucket.kinesis.arn

    //Buffer incoming data to the specified size, in MBs, before delivering it to the destination.
    buffer_size = var.kinesis_buffer_size

    //Buffer incoming data for the specified period of time, in seconds, before delivering it to the destination.
    buffer_interval = var.kinesis_buffer_interval

    //The compression format
    compression_format = var.kinesis_compression_format
  }

  kinesis_source_configuration {
    role_arn = aws_iam_role.kinesis.arn
    kinesis_stream_arn = aws_kinesis_stream.kinesis.arn
  }
}
