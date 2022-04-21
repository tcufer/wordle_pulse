from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json, col
from pyspark.sql.types import LongType, StructType, StringType, IntegerType
from datetime import datetime
from src.tweet_parser import TweetParser
from src.constants import CONFIG, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


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
        .option("streamName", CONFIG['kinesis']['streamName']) \
        .option("endpointUrl", CONFIG['kinesis']['endpointUrl']) \
        .option("awsAccessKeyId", AWS_ACCESS_KEY_ID) \
        .option("awsSecretKey", AWS_SECRET_ACCESS_KEY) \
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


def prepare_tweet_content(tweet):
    schema = StructType(). \
        add('id', LongType(), False). \
        add('created_at', StringType(), False) .\
        add('user', StructType().add("id_str", StringType(), False), False). \
        add('text', StringType(), False)

    type_name = tweet.schema.fields[0].name
    select_expression = f"CAST({type_name} AS STRING)"
    print(type_name)
    print(select_expression)
    processed_tweet = tweet \
        .selectExpr(select_expression) \
        .select(from_json(type_name, schema).alias('tweet_data'))

    return processed_tweet


def process_tweet_content(tweet):
    processed_tweet = prepare_tweet_content(tweet) \
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
    url = f"jdbc:postgresql://{CONFIG['dbhost']}:{CONFIG['dbport']}/{CONFIG['dbname']}"
    properties = {
        "driver": "org.postgresql.Driver",
        "user": CONFIG['dbuser'],
        "password": CONFIG['dbpass'],
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
