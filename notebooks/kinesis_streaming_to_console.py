from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json, to_date, col, to_utc_timestamp, explode, split
from pyspark.sql.types import LongType, StructType, StringType
from datetime import datetime
from mypckg.tweet_parser import TweetParser
import yaml
import configparser
import os
import pytz

spark = SparkSession.builder.appName("Wordle score streaming").getOrCreate()

config = ""
with open('../secrets.yml', 'r') as file:
    config = yaml.safe_load(file)

s3_conf = configparser.ConfigParser()
config_path = os.path.join(os.path.expanduser('~'), '.aws/credentials')
s3_conf.read(config_path)

def getResults(text):
    return TweetParser(text).wordle_result_exist()

## Converting date string format
def getDate(x):
    if x is not None:
        return str(datetime.strptime(x,'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC).strftime("%Y-%m-%d %H:%M:%S"))
    else:
        return None

## UDF declaration
date_fn = udf(getDate, StringType())
attempts_fn = udf(lambda  x: getResults(x), StringType())

lines = spark \
	.readStream \
	.format("kinesis") \
	.option("streamName", "twitter_wordle_stream") \
   	.option("endpointUrl", "https://kinesis.eu-central-1.amazonaws.com") \
    .option("awsAccessKeyId", s3_conf.get('development', 'aws_access_key_id')) \
    .option("awsSecretKey", s3_conf.get('development', 'aws_secret_access_key')) \
    .option("startingposition", "TRIM_HORIZON") \
	.load()

schema = StructType(). \
    add('id', LongType(), False). \
    add('created_at', StringType(), False) .\
    add('user', StructType().add("id_str",StringType(), False), False). \
    add('text', StringType(), False)

filtered_data = lines \
    .selectExpr('CAST(data AS STRING)') \
    .select(from_json('data', schema).alias('tweet_data')) \
    .selectExpr('tweet_data.id', 'tweet_data.created_at', 'tweet_data.user.id_str AS user_id', 'tweet_data.text AS message') \
    .withColumn("created_at", to_utc_timestamp(date_fn("created_at"),"UTC")) \
    .withColumn('results', attempts_fn(col('message')))

filtered_data = filtered_data.filter(col('results') != "false")


filtered_data.printSchema()

# Start running the query that prints tweet data to the console
query = filtered_data \
    .writeStream \
    .format("console") \
    .outputMode("append") \
    .trigger(processingTime= "5 seconds") \
    .start()

query.awaitTermination()
