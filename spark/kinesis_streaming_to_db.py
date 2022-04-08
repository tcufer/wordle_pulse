from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json, to_date, col, to_utc_timestamp, explode, split, current_timestamp
from pyspark.sql.types import LongType, StructType, StringType, IntegerType
from datetime import datetime
import os
import pytz
import sys
import yaml
import configparser
from time import gmtime, strftime
from src.tweet_parser import TweetParser

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.hadoop:hadoop-aws:3.3.1 pyspark-shell'

config = ""
with open('../secrets.yml', 'r') as file:
    config = yaml.safe_load(file)

s3_conf = configparser.ConfigParser()
config_path = os.path.join(os.path.expanduser('~'), '.aws/credentials')
s3_conf.read(config_path)


# spark = SparkSession(sc) \
spark = SparkSession \
    .builder \
    .appName('Wordle score streaming') \
    .getOrCreate()

lines = spark \
    .readStream \
    .format("kinesis") \
    .option("streamName", config['streamName']) \
    .option("endpointUrl", "https://kinesis.eu-central-1.amazonaws.com") \
    .option("awsAccessKeyId", s3_conf.get('development', 'aws_access_key_id')) \
    .option("awsSecretKey", s3_conf.get('development', 'aws_secret_access_key')) \
    .option("initialPosition", "latest") \
    .load()

## Converting date string format
def getDate(x):
    if x is not None:
        # return str(datetime.strptime(x,'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC).strftime("%Y-%m-%d %H:%M:%S"))
        return str(datetime.strptime(x,'%a %b %d %H:%M:%S +0000 %Y'))
    else:
        return None

def getResults(text):
    return TweetParser(text).wordle_result_exist()

def getSystemTimeZone():
    return strftime("%z", gmtime())

## UDF declaration
date_fn = udf(getDate, StringType())
attempts_fn = udf(lambda  x: getResults(x), StringType())

schema = StructType(). \
    add('id', LongType(), False). \
    add('created_at', StringType(), False) .\
    add('user', StructType().add("id_str",StringType(), False), False). \
    add('text', StringType(), False)

filtered_data = lines \
    .selectExpr('CAST(data AS STRING)') \
    .select(from_json('data', schema).alias('tweet_data')) \
    .selectExpr('tweet_data.id', 'tweet_data.created_at', 'tweet_data.user.id_str AS user_id', 'tweet_data.text AS message') \
    .withColumn("created_at", to_utc_timestamp(date_fn("created_at"), "UTC")) \
    .withColumn('processed_at', to_utc_timestamp(current_timestamp(), getSystemTimeZone())) \
    .withColumn('results', attempts_fn(col('message'))) \
    .dropDuplicates(["id"])


filtered_data = filtered_data.filter(col('results') != "{}")

results_schema = StructType(). \
    add('wordle_id', StringType(), False). \
    add('attempts_count', IntegerType(), False). \
    add('attempts', StringType(), False)


filtered_data = filtered_data \
    .withColumn('results', from_json('results', results_schema)) \
    .select('id', 'created_at', 'processed_at', 'user_id', 'message', 'results.wordle_id', 'results.attempts_count', 'results.attempts')

filtered_data.printSchema()


def postgres_sink(df, batch_id):

    dbname = config['dbname']
    dbtable = 'tweets_v4'
    dbuser = config['dbuser']
    dbpass = config['dbpass']
    dbhost = config['dbhost']
    dbport = config['dbport']

    url = "jdbc:postgresql://"+dbhost+":"+str(dbport)+"/"+dbname
    properties = {
        "driver": "org.postgresql.Driver",
        "user": dbuser,
        "password": dbpass,
        "stringtype":"unspecified"
    }
    df.write.jdbc(
        url=url,
        table=dbtable,
        mode="append",
        properties=properties)


# Write to Postgres
query = filtered_data \
    .writeStream \
    .trigger(processingTime='15 seconds') \
    .outputMode("append") \
    .foreachBatch(postgres_sink) \
    .start()

query.awaitTermination()
