import pytest
from pyspark.sql import SparkSession
from process_twitter_stream import process_tweet_content


class TestClass():

    def setup_method(self, method):
        name = 'Wordle Pulse processing'
        self.spark = SparkSession \
            .builder \
            .master('local[4]') \
            .appName(name) \
            .getOrCreate()

    def _create_read_stream(self, path):
        events = self.spark.readStream \
                      .format('text') \
                      .option('path', path) \
                      .load()

        return events

    def _create_write_stream(self, filtered_data):
        query = filtered_data \
            .writeStream \
            .format("memory") \
            .queryName('results') \
            .outputMode("append") \
            .start()

        return query

    @pytest.mark.parametrize("path", ["tests/fixtures/parsable_tweets/", ])
    def test_process_tweet_with_parsed_result(self, path: str):
        tweet = self._create_read_stream(path)
        processed_tweet = process_tweet_content(tweet)
        self.query = self._create_write_stream(processed_tweet)
        self.query.processAllAvailable()
        expected_result = "4"
        result = self.spark.sql("select attempts_count from results").collect()[0]['attempts_count']

        assert str(result) == expected_result

    @pytest.mark.parametrize("path", ["tests/fixtures/unparsable_tweets/", ])
    def test_process_tweet_with_unparsed_result(self, path: str):
        tweet = self._create_read_stream(path)
        processed_tweet = process_tweet_content(tweet)
        self.query = self._create_write_stream(processed_tweet)
        self.query.processAllAvailable()
        result = self.spark.sql("select attempts_count from results").collect()

        assert len(result) == 0

    def teardown_method(self, method):
        self.query.stop()
