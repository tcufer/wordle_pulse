import os

CHECKPOINT_BUCKET = f"s3a://{os.environ.get('S3_BUCKET')}/{os.environ.get('S3_FOLDER')}/"
DB_CONN_STRING = f"jdbc:postgresql://{os.environ.get('PG_HOST')}:{os.environ.get('PG_PORT')}/{os.environ.get('PG_DBNAME')}"
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
KINESIS_STREAM_NAME = os.environ.get("KINESIS_STREAM_NAME")
KINESIS_ENDPOINT_URL = os.environ.get("KINESIS_ENDPOINT_URL")

PG_USER=os.environ.get("PG_USER")
PG_PASSWORD=os.environ.get("PG_PASSWORD")
PG_TABLE="tweets"
