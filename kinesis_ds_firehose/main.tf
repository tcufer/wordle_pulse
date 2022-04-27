module "kinesis" {
    source = "./modules/kinesis"
    s3_bucket_name = var.s3_bucket_name
    app_name = var.app_name
}
