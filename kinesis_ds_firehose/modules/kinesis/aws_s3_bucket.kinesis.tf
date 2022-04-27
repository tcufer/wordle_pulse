resource "aws_s3_bucket" "kinesis" {
  bucket = "${var.s3_bucket_name}-kinesis"
  tags = {
    Name        = "Kinesis"
    Environment = lower(var.s3_bucket_name)
  }
}

resource "aws_s3_bucket_acl" "kinesis" {
  bucket = aws_s3_bucket.kinesis.id
  acl    = "private"
}
