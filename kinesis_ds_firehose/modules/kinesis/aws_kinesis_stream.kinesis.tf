resource "aws_kinesis_stream" "kinesis" { // Created a new kinesis stream resource
  // A name to identify the stream
  name = "${var.app_name}_kinesis"

  //The number of shard that the stream will use A shard is a unit of throughput capacity.
  shard_count = var.kinesis_shard_count

  // Length of time data records are accessible after they are added to the stream
  retention_period = var.kinesis_retention_period

  //The encryption type to use
  encryption_type = var.kinesis_encryption_type

  //A list of shard-level CloudWatch metrics which can be enabled for the stream
  shard_level_metrics = var.kinesis_shard_level_metrics

  //A mapping of tags  to assign to the resource
  tags = {
    Environment = lower(var.app_name)
  }
}
