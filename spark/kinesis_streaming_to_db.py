from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json, col
from pyspark.sql.types import LongType, StructType, StringType, IntegerType
from datetime import datetime
import os
import yaml
import configparser
from src.tweet_parser import TweetParser


with open('../secrets.yml', 'r') as file:
    config = yaml.safe_load(file)

s3_conf = configparser.ConfigParser()
config_path = os.path.join(os.path.expanduser('~'), '.aws/credentials')
s3_conf.read(config_path)


def get_or_create_spark_session(name):
    session = SparkSession \
        .builder \
        .appName(name) \
        .getOrCreate()

    return session


def prepare_kinesis_read_stream(spark):
    events = spark \
        .readStream \
        .format("kinesis") \
        .option("streamName", config['kinesis']['streamName']) \
        .option("endpointUrl", config['kinesis']['endpointUrl']) \
        .option("awsAccessKeyId", s3_conf.get('development', 'aws_access_key_id')) \
        .option("awsSecretKey", s3_conf.get('development', 'aws_secret_access_key')) \
        .option("initialPosition", "latest") \
        .load()

    return events


@udf
def parseCreatedAtDatetime(datetime_string):
    return str(datetime.strptime(datetime_string, '%a %b %d %H:%M:%S +0000 %Y'))


@udf
def getCurrentDatetime():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


@udf
def getResults(text):
    return TweetParser(text).perform()


def process_tweet_content(tweet):
    schema = StructType(). \
        add('id', LongType(), False). \
        add('created_at', StringType(), False) .\
        add('user', StructType().add("id_str", StringType(), False), False). \
        add('text', StringType(), False)

    processed_tweet = tweet \
        .selectExpr('CAST(data AS STRING)') \
        .select(from_json('data', schema).alias('tweet_data')) \
        .selectExpr('tweet_data.id',
                    'tweet_data.created_at',
                    'tweet_data.user.id_str AS user_id',
                    'tweet_data.text AS message') \
        .withColumn("created_at", parseCreatedAtDatetime(col('created_at'))) \
        .withColumn('processed_at', getCurrentDatetime()) \
        .withColumn('results', getResults(col('message'))) \
        .dropDuplicates(["id"])

    processed_tweet = processed_tweet.filter(col('results') != "{}")

    results_schema = StructType(). \
        add('wordle_id', StringType(), False). \
        add('attempts_count', IntegerType(), False). \
        add('attempts', StringType(), False)

    result = processed_tweet \
        .withColumn('results', from_json('results', results_schema)) \
        .select('id',
                'created_at',
                'processed_at',
                'user_id',
                'message',
                'results.wordle_id',
                'results.attempts_count',
                'results.attempts')

    return result


def postgres_sink(df, batch_id):
    dbtable = 'tweets_v4'
    url = f"jdbc:postgresql://{config['dbhost']}:{config['dbport']}/{config['dbname']}"
    properties = {
        "driver": "org.postgresql.Driver",
        "user": config['dbuser'],
        "password": config['dbpass'],
        "stringtype": "unspecified"
    }
    df.write.jdbc(
        url=url,
        table=dbtable,
        mode="append",
        properties=properties)


def prepare_postgres_write_stream(filtered_data):
    write_stream = filtered_data \
                    .writeStream \
                    .trigger(processingTime='15 seconds') \
                    .outputMode("append") \
                    .foreachBatch(postgres_sink)

    return write_stream


def main():
    spark = get_or_create_spark_session('Wordle Pulse processing')
    tweets = prepare_kinesis_read_stream(spark)
    filtered_data = process_tweet_content(tweets)
    prepare_postgres_write_stream(filtered_data).start()

    spark.streams.awaitAnyTermination()


if __name__ == '__main__':
    main()
